<#
    Starts the http server with: 'npx tsx http-server.ts'.
    Background Thread: On change in $PATHS_TO_WATCH:Array<file|dir>, rebuilds frontend project into dist.
#>

<# Main Thread #>
$HTTP_SERVER_PROJECT_ROOT = "$PWD\node"

<# Background Thread Parameters #>
$VITE_ROOT  = "$PWD\node\_vite-frontend"
$PATHS_TO_WATCH = @(
    "$VITE_ROOT\index.html",
    "$VITE_ROOT\index.ts",
    "$VITE_ROOT\src",
    "$VITE_ROOT\..\_shared"
)


$tokenSource = [System.Threading.CancellationTokenSource]::new()
$token = $tokenSource.Token
Start-ThreadJob -ArgumentList $VITE_ROOT, $PATHS_TO_WATCH, $token -StreamingHost $Host -ScriptBlock  {
    param($npm_project_dir, $paths_to_watch, $token)

    $paths_to_watch | ForEach-Object {
        if(-not(Test-Path $_)) {  Write-Host "PATHS_TO_WATCH has a non-real path. path: $_" -ForegroundColor DarkRed  }
    }

    function NpmBuild {
        cd $npm_project_dir
        npm run build | Out-Null
        return [datetime]::UtcNow.Ticks;
    }

    $vite_last_built = NpmBuild
    while (-not $token.IsCancellationRequested) {
        Start-Sleep -Milliseconds 250
        foreach ($path in $paths_to_watch) {
            if($vite_last_built -lt (Get-Item $path).LastWriteTimeUtc.Ticks) {
                $vite_last_built = NpmBuild; break;
            }
            $change_detected = $false;
            if((Get-Item $path).PSIsContainer) {
                foreach($file in $(Get-ChildItem -Path $path -Recurse -File)) {
                    if($vite_last_built -lt (Get-Item $file).LastWriteTimeUtc.Ticks) {
                        $vite_last_built = NpmBuild; $change_detected = $true; break;  }
                }
            }
            if($change_detected) {  break;  }
        }
    }
}

<#
    MAIN THREAD
#>
$START_PATH = $PWD.Path

Clear-Host
try {
    cd $HTTP_SERVER_PROJECT_ROOT
    npx tsx http-server.ts
    $exitCode = $LASTEXITCODE
}
finally {
    $tokenSource.Cancel()
    Start-Sleep -Milliseconds 75

    cd $START_PATH
}
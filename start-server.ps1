<#
    Background Thread: watches an Array<file|directory>. onchange -> 'npm run build' in $VITE_ROOT 
    Main Thread: 'npx tsx http-server.ts'
#>
param(
    [string]$browser = $null        # e.g: "chrome.exe" / "msedge.exe"  [Optional Param] -> Launches browser at: "http://127.0.0.1:8080/"
)


<# Main Thread Parameters #>
$HTTP_SERVER_DIRECTORY = "$PWD\node"
$STARTING_PATH = $PWD.Path    # will cd back into on script exit

<# Background Thread Parameters #>
$VITE_ROOT  = "$PWD\node\_vite-frontend"
$PATHS_TO_WATCH = @(
    "$VITE_ROOT\src",
    "$VITE_ROOT\index.html",
    "$VITE_ROOT\index.scss",
    "$VITE_ROOT\index.ts",
    # "$VITE_ROOT\report.html",
    "$VITE_ROOT\..\_shared"
)


<#  BACKGROUND THREAD  #>
$tokenSource = [System.Threading.CancellationTokenSource]::new()
$token = $tokenSource.Token
Start-ThreadJob -ArgumentList $VITE_ROOT, $PATHS_TO_WATCH, $token -StreamingHost $Host -ScriptBlock {
    param(
        $npm_project_directory,     # what the thread will cd into to run NpmBuild
        $paths_to_watch,            # Array<file|directory>
        $token                      # Main Thread uses to signal thread to stop running. Type: [System.Threading.CancellationTokenSource]::new().Token
    )

    $global:build_failed_message_sent = $false  # Warning that NpmBuild failed, only sent once per run.
    $paths_to_watch | ForEach-Object {
        if(-not(Test-Path $_)) {  Write-Host "PATHS_TO_WATCH has a non-real path. path: $_" -ForegroundColor DarkRed  }
    }

    function NpmBuild($last_built) {
        <# 
        Returns:
            [LastModified] New Ticks - 'npm run build' was successful
            || $last_built (Old Ticks) - error running: 'npm run build'
        #>
        $err = $( $null = npm run build ) 2>&1
        if($err) {
            $err = [string]$err
            if($err.Contains("Build failed")) {
                # if($global:build_failed_message_sent -eq $false) {
                Write-Host "`nWatch Thread: NpmBuild Failed!" -ForegroundColor Red
                    # $global:build_failed_message_sent = $true

                while($true) {
                    Start-Sleep .3
                    $err = $( $null = npm run build ) 2>&1
                    if($err) {
                        $err = [string]$err
                        if(-not($err.Contains("Build failed"))) {
                            Write-Host "Watch Thread: NpmBuild Success!`n" -ForegroundColor Green
                            return [datetime]::UtcNow.Ticks;
                        }
                    }
                }
            }
                # return $last_built
            #     return $false
            # }
        }
        return [datetime]::UtcNow.Ticks;
    }

    Start-Sleep .2  # Theory: ENOENT error caused by 'npm run build' holding lock

    cd $npm_project_directory
    $vite_last_built = NpmBuild
    while (-not $token.IsCancellationRequested) {
        Start-Sleep -Milliseconds 125
        
        foreach ($path in $paths_to_watch) {
            if((Get-Item $path).PSIsContainer) {
                foreach($file in $(Get-ChildItem $path -Recurse -File)) {              <# Yes: all files are checked recursively, Stan (eye-check: at least dirs of dirs) #>
                    if($vite_last_built -lt (Get-Item $file).LastWriteTimeUtc.Ticks) {
                        # Write-Host "start-server.ps1: Change has been detected in `$PATHS_TO_WATCH. Running NpmBuild()..."
                        $vite_last_built = NpmBuild
                        $escape_hatch_needed = $true
                        break;
            }}}
            if($escape_hatch_needed) { break; }     <#  Nap-Time  #>

            <#  Else: is a file #>
            if($vite_last_built -lt (Get-Item $path).LastWriteTimeUtc.Ticks) {
                # Write-Host "start-server.ps1: Change has been detected in `$PATHS_TO_WATCH. Running NpmBuild()..."
                $vite_last_built = NpmBuild
                break;
}}}}


<#  MAIN THREAD  #>             # try-finally allows work after Ctrl+C 
Clear-Host
try {
    cd $HTTP_SERVER_DIRECTORY
    if($browser) {
        Start-Process $browser "--new-window http://127.0.0.1:8080/"
    }
    npx tsx http-server.ts
    $exitCode = $LASTEXITCODE
}
finally {
    $tokenSource.Cancel()
    Start-Sleep -Milliseconds 75
    cd $STARTING_PATH
}
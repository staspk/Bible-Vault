<#
    Starts the http server that serves the frontend: ./node/http-server.ts
    In the background: Watches for changes in vite-frontend, rebuilding project when necessary
#>

$START_PATH = $PWD.Path


$watcherJob = Start-ThreadJob -ScriptBlock {
    $VITE_ROOT = "$PWD/node/vite-frontend"
    cd $VITE_ROOT
    npm run build
    $VITE_LAST_BUILT = [datetime]::UtcNow.Ticks


    $index_html = "$VITE_ROOT/index.html"; if(-not(Test-Path $index_html)) {  Write-Host "SERIOUS ERROR! `$index_html not real path" -ForegroundColor DarkRed  }
    $src_folder = "$VITE_ROOT/src";        if(-not(Test-Path $src_folder)) {  Write-Host "SERIOUS ERROR! `$src_folder not real path" -ForegroundColor DarkRed  }


    while ($true) {
        Start-Sleep -Milliseconds 420

        $last_changed = (Get-Item "$index_html").LastWriteTimeUtc.Ticks
        if($last_changed -gt $VITE_LAST_BUILT) {
            cd $VITE_ROOT
            npm run build
            $VITE_LAST_BUILT = [datetime]::UtcNow.Ticks
            continue
        }
        Get-ChildItem -Path $src_folder -Recurse -File | ForEach-Object {
            if($((Get-Item $_).LastWriteTimeUtc.Ticks) -gt $VITE_LAST_BUILT) {
                cd $VITE_ROOT
                npm run build
                $VITE_LAST_BUILT = [datetime]::UtcNow.Ticks
                continue
            }
        }
    }
}

Clear-Host
try {
    cd "$START_PATH/node"
    npx tsx http-server.ts
    $exitCode = $LASTEXITCODE
}
finally {
    Set-Location $START_PATH
    if($exitCode -eq 0) {
        Clear-Host
    }
}
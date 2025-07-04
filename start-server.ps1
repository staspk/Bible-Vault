<#
    Starts the http server that serves the frontend: ./node/http-server.ts
#>

$location = $PWD.Path

Clear-Host
try {
    Set-Location ./node
    npx tsx http-server.ts
    $exitCode = $LASTEXITCODE
}
finally {
    Set-Location $location

    if($exitCode -eq 0) {
        Clear-Host
    }
}
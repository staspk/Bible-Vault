$location = $PWD.Path

try {
    Set-Location ./node
    npx tsx app.ts
    $exitCode = $LASTEXITCODE
}
finally {
    Set-Location $location

    if($exitCode -eq 0) {
        Clear-Host
    }
}
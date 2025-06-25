$location = $PWD.Path

try {
    Set-Location ./node
    npx tsx app.ts start-server.ps1
}
finally {
    Set-Location $location
}
$location = $PWD.Path

Set-Location ./node
npx tsx app.ts
Set-Location $location
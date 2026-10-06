$ErrorActionPreference='Stop'
$taskRoot=$PSScriptRoot
$taskOut=Join-Path $taskRoot 'output/video-03'
$taskRenderId=[int](Get-Content -LiteralPath (Join-Path $taskOut 'render.pid'))
while(Get-Process -Id $taskRenderId -ErrorAction SilentlyContinue){Start-Sleep -Seconds 10}
if(-not ((Get-Content -LiteralPath (Join-Path $taskOut 'render-progress.log') -Raw) -match 'FINISHED ')){throw 'Render did not complete'}
Set-Location -LiteralPath $taskRoot
& node verify-video3.cjs 1> (Join-Path $taskOut 'verification-progress.log') 2> (Join-Path $taskOut 'verification-error.log')
if($LASTEXITCODE -ne 0){throw 'Verification failed'}

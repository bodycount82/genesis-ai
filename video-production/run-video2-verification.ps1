param([int]$RenderProcessId)
$ErrorActionPreference = 'Stop'
$productionRoot = $PSScriptRoot
if ($RenderProcessId) { Wait-Process -Id $RenderProcessId -ErrorAction SilentlyContinue }
$renderLog = Get-Content -Raw -LiteralPath (Join-Path $productionRoot 'output/video-02/render.log')
if ($renderLog -notmatch 'FINISHED ') { throw 'Render did not finish successfully. Inspect render-error.log and encode.log.' }
Set-Location -LiteralPath $productionRoot
& (Get-Command node).Source 'verify-video2.cjs' *> (Join-Path $productionRoot 'output/video-02/verification.log')
$verificationExit = $LASTEXITCODE
Set-Content -LiteralPath (Join-Path $productionRoot 'output/video-02/verification-exit.txt') -Value $verificationExit
exit $verificationExit

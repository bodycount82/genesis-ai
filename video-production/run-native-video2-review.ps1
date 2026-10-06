param([int]$RenderProcessId)
$ErrorActionPreference = 'Stop'
if ($RenderProcessId) { Wait-Process -Id $RenderProcessId -ErrorAction SilentlyContinue }
Set-Location -LiteralPath $PSScriptRoot
$renderLog = Get-Content -Raw -LiteralPath 'output/video-02/render.log'
if ($renderLog -notmatch 'FINISHED ') { throw 'Master has not finished rendering.' }
& (Get-Command node).Source 'native-frames-video2.cjs' *> 'output/video-02/native-review.log'
$nativeExit = $LASTEXITCODE
Set-Content -LiteralPath 'output/video-02/native-review-exit.txt' -Value $nativeExit
exit $nativeExit

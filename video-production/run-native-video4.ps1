$ErrorActionPreference='Stop'
$taskRoot=$PSScriptRoot
$taskOut=Join-Path $taskRoot 'output/video-04'
$taskEvidence=Join-Path $taskRoot '../../../Claude and OpenAI docs/Genesis-Knowledge/evidence/tutorial-video-4-20261002'
$taskRenderId=[int](Get-Content -LiteralPath (Join-Path $taskOut 'render.pid'))
while(Get-Process -Id $taskRenderId -ErrorAction SilentlyContinue){Start-Sleep -Seconds 10}
if(-not ((Get-Content -LiteralPath (Join-Path $taskOut 'render-progress.log') -Raw) -match 'FINISHED ')){throw 'Render did not complete'}
while(-not (Test-Path -LiteralPath (Join-Path $taskEvidence 'audio-analysis.json'))){
  if(Test-Path -LiteralPath (Join-Path $taskOut 'verification-error.log')){
    if((Get-Item -LiteralPath (Join-Path $taskOut 'verification-error.log')).Length -gt 0){throw 'Verification needs attention'}
  }
  Start-Sleep -Seconds 10
}
Set-Location -LiteralPath $taskRoot
& node native-frames-video4.cjs 1> (Join-Path $taskOut 'native-progress.log') 2> (Join-Path $taskOut 'native-error.log')
if($LASTEXITCODE -ne 0){throw 'Native frame extraction failed'}

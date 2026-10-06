$ErrorActionPreference='Stop'
Set-Location -LiteralPath $PSScriptRoot
& node native-frames-video3.cjs
if($LASTEXITCODE -ne 0){throw 'Native frame extraction failed'}
& node review-frames-video3.cjs
if($LASTEXITCODE -ne 0){throw 'Review sheets failed'}

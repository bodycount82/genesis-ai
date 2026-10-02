$ErrorActionPreference = 'Stop'
$previewAddress = 'http://127.0.0.1:4179/tutorials/'
$websiteRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
function Test-TutorialPreview {
    try {
        $previewResponse = Invoke-WebRequest -Uri $previewAddress -TimeoutSec 2 -UseBasicParsing
        return $previewResponse.StatusCode -eq 200 -and $previewResponse.Content.Contains('Learn Genesis')
    } catch { return $false }
}
if (-not (Test-TutorialPreview)) {
    $previewNode = (Get-Command node.exe -ErrorAction Stop).Source
    Start-Process -FilePath $previewNode -ArgumentList 'tutorials/tools/serve.cjs' -WorkingDirectory $websiteRoot -WindowStyle Hidden
    for ($previewAttempt = 0; $previewAttempt -lt 20; $previewAttempt++) {
        Start-Sleep -Milliseconds 250
        if (Test-TutorialPreview) { break }
    }
}
if (-not (Test-TutorialPreview)) { throw 'The local preview could not start on port 4179. Check whether another program uses that port.' }
# The browser is intentionally visible: this launcher opens the owner's review.
Start-Process $previewAddress

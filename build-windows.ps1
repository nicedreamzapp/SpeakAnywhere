# Build the Windows download: dist\Speak-Anywhere-windows.zip
#   powershell -NoProfile -ExecutionPolicy Bypass -File build-windows.ps1 [-Python <python.exe>]
# Uses its own clean environment (.buildvenv), so it never changes the Python you run the app from.
param([string]$Python = "python")
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
$log = Join-Path $PSScriptRoot "build-windows.log"
"start $(Get-Date)" | Out-File -Encoding utf8 $log
if (-not (Test-Path .buildvenv)) { & $Python -m venv .buildvenv 2>&1 | Out-File -Append -Encoding utf8 $log }
& .buildvenv\Scripts\python.exe -m pip install -q -r requirements.txt pyinstaller 2>&1 | Select-Object -Last 5 | Out-File -Append -Encoding utf8 $log
& .buildvenv\Scripts\python.exe -m PyInstaller --noconfirm speak_anywhere.spec 2>&1 | Select-Object -Last 8 | Out-File -Append -Encoding utf8 $log
$out = Join-Path $PSScriptRoot "dist\Speak Anywhere"
if (Test-Path (Join-Path $out "Speak Anywhere.exe")) {
    $zip = Join-Path $PSScriptRoot "dist\Speak-Anywhere-windows.zip"
    Remove-Item $zip -ErrorAction SilentlyContinue
    Compress-Archive -Path $out -DestinationPath $zip
    "built $((Get-Item $zip).Length) bytes" | Out-File -Append -Encoding utf8 $log
} else {
    "BUILD FAILED: no Speak Anywhere.exe" | Out-File -Append -Encoding utf8 $log
}
"BUILD-END $(Get-Date)" | Out-File -Append -Encoding utf8 $log

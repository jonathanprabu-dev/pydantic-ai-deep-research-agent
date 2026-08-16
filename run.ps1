$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $projectRoot ".venv"
$pythonPath = Join-Path $venvPath "Scripts\python.exe"

Set-Location $projectRoot

if (-not (Test-Path $pythonPath)) {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw "Python was not found. Install Python 3.11+ and run .\run.ps1 again."
    }

    Write-Host "Creating virtual environment..."
    & python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create the virtual environment."
    }
}

Write-Host "Installing dependencies..."
& $pythonPath -m pip install -r (Join-Path $projectRoot "requirements.txt")
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

Write-Host "Starting the Gradio app..."
& $pythonPath (Join-Path $projectRoot "app.py")
exit $LASTEXITCODE

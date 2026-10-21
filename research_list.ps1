# Research a list of accounts in one step:
#   .\research_list.ps1 accounts.xlsx
#   .\research_list.ps1 accounts.xlsx --focus "contact center"
#
# Run it again whenever you like: it researches only new or unfinished companies
# and keeps everything already done. Sets up .venv the first time.
$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"

if ($args.Count -eq 0) {
    Write-Host 'Usage: .\research_list.ps1 <your list .xlsx or .csv> [--focus "topic"] [--limit N] [--fresh]'
    exit 1
}

if (-not (Test-Path $pythonPath)) {
    if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
        throw "Python was not found. Install Python 3.11+ and run this again."
    }
    Write-Host "First run: setting up the project (one time only)..."
    & python -m venv (Join-Path $projectRoot ".venv")
    if ($LASTEXITCODE -ne 0) { throw "Could not create the virtual environment." }
    & $pythonPath -m pip install -q -r (Join-Path $projectRoot "requirements.txt")
    if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
}

& $pythonPath (Join-Path $projectRoot "account_list.py") @args
exit $LASTEXITCODE

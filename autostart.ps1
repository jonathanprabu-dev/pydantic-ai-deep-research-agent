# Starts the Pydantic AI Deep Research Agent at login and opens it in Chrome.
#
# Installed by install-autostart.ps1, which drops a .vbs stub in the Startup
# folder so this runs without a console window flashing on screen.
#
# Safe to run by hand at any time: if the app is already listening it will not
# start a second copy, it just opens the tab.

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonPath = Join-Path $projectRoot ".venv\Scripts\python.exe"
$port = 7860
$url = "http://127.0.0.1:$port"

function Test-AppListening {
    # A listening socket, not an HTTP request: Gradio serves the page long
    # before the agent is ready, and all we need to know is whether to start
    # another copy.
    $null -ne (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue)
}

if (-not (Test-Path $pythonPath)) {
    throw "No virtualenv at $pythonPath. Run .\run.ps1 once to create it."
}

if (-not (Test-AppListening)) {
    Set-Location $projectRoot
    # -u so app.log stays live rather than block-buffering; the log is the only
    # window into a process that has no console.
    Start-Process -FilePath $pythonPath `
        -ArgumentList "-u", "app.py" `
        -WorkingDirectory $projectRoot `
        -WindowStyle Hidden `
        -RedirectStandardOutput (Join-Path $projectRoot "app.log") `
        -RedirectStandardError (Join-Path $projectRoot "app.err.log")

    # Gradio takes ~20s to import torch/gradio on a cold start. Poll rather than
    # sleep a fixed guess: opening Chrome early shows a connection error.
    $deadline = (Get-Date).AddSeconds(90)
    while (-not (Test-AppListening)) {
        if ((Get-Date) -gt $deadline) {
            throw "The app did not start listening on port $port within 90s. See app.err.log."
        }
        Start-Sleep -Milliseconds 500
    }
}

# Chrome by name where it exists, since the app is built around it; the default
# browser is only a fallback so a missing Chrome still gets you a usable tab.
$chrome = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LocalAppData\Google\Chrome\Application\chrome.exe"
) | Where-Object { Test-Path $_ } | Select-Object -First 1

if ($chrome) {
    Start-Process -FilePath $chrome -ArgumentList $url
} else {
    Start-Process $url
}

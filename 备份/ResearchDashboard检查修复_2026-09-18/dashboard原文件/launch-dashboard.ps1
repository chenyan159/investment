$ErrorActionPreference = 'Stop'

$dashboardDir = $PSScriptRoot
$port = if ($env:RESEARCH_DASHBOARD_PORT) { [int]$env:RESEARCH_DASHBOARD_PORT } else { 4317 }
$url = "http://127.0.0.1:$port"
$healthUrl = "$url/api/health"

function Test-DashboardHealth {
    try {
        $response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 2
        return [bool]$response.ok
    }
    catch {
        return $false
    }
}

if (-not (Test-DashboardHealth)) {
    $process = Start-Process -FilePath "node" -ArgumentList @("server.mjs") -WorkingDirectory $dashboardDir -WindowStyle Hidden -PassThru
    $ready = $false
    for ($attempt = 0; $attempt -lt 40; $attempt++) {
        Start-Sleep -Milliseconds 250
        if (Test-DashboardHealth) {
            $ready = $true
            break
        }
        if ($process.HasExited) {
            break
        }
        $process.Refresh()
    }
    if (-not $ready) {
        throw "Dashboard did not become healthy at $healthUrl."
    }
}

Start-Process $url

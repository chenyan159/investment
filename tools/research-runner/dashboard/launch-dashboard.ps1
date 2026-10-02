param([switch]$NoBrowser)

$ErrorActionPreference = 'Stop'

$dashboardDir = $PSScriptRoot
$port = if ($env:RESEARCH_DASHBOARD_PORT) { [int]$env:RESEARCH_DASHBOARD_PORT } else { 4319 }
if ($port -lt 1 -or $port -gt 65535) { throw 'RESEARCH_DASHBOARD_PORT must be between 1 and 65535.' }
$projectRoot = [IO.Path]::GetFullPath((Join-Path $dashboardDir '..\..\..')).TrimEnd('\')
$url = "http://127.0.0.1:$port"
$healthUrl = "$url/api/health"

function Test-DashboardHealth {
    try {
        $response = Invoke-RestMethod -Uri $healthUrl -Method Get -TimeoutSec 2
        return [bool]($response.ok -and $response.service -eq 'research-runner-dashboard' -and
            $response.projectRoot -and [IO.Path]::GetFullPath($response.projectRoot).TrimEnd('\') -eq $projectRoot)
    }
    catch {
        return $false
    }
}

if (-not (Test-DashboardHealth)) {
    $listener = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue
    if ($listener) {
        throw "Port $port is occupied by a different service or workspace. Set RESEARCH_DASHBOARD_PORT to a free port; no running process was stopped."
    }
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

if (-not $NoBrowser) { Start-Process $url }
Write-Output $url

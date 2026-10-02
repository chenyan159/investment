$ErrorActionPreference = 'Stop'
$taskRoot = [System.IO.Path]::GetFullPath('D:\drive\Investment')
$taskOut = Join-Path $taskRoot '备份\公司行业索引分类升级_2026-09-10'
$taskPlan = Get-Content -LiteralPath (Join-Path $taskOut '迁移计划.json') -Raw | ConvertFrom-Json
$taskJournal = Join-Path $taskOut '执行日志.jsonl'

function Assert-WorkspacePath([string]$Value) {
    $absolute = [System.IO.Path]::GetFullPath($Value)
    if (-not $absolute.StartsWith($taskRoot + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Target escapes intended workspace: $absolute"
    }
    return $absolute
}

function Move-Checked($Operation) {
    $source = Assert-WorkspacePath $Operation.source
    $destination = Assert-WorkspacePath $Operation.destination
    if (-not (Test-Path -LiteralPath $source)) { throw "Missing source: $source" }
    if (Test-Path -LiteralPath $destination) { throw "Destination already exists: $destination" }
    $item = Get-Item -LiteralPath $source -Force
    if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
        throw "Refusing to move a reparse point: $source"
    }
    if ($destination.StartsWith($source + '\', [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Destination is nested in source: $destination"
    }
    $parent = Split-Path -Parent $destination
    if (-not (Test-Path -LiteralPath $parent)) {
        New-Item -ItemType Directory -Path $parent -Force | Out-Null
    }
    Move-Item -LiteralPath $source -Destination $destination -Force
    @{action='move';source=$source;destination=$destination;time=(Get-Date).ToString('o')} |
        ConvertTo-Json -Compress | Add-Content -LiteralPath $taskJournal -Encoding utf8
}

if (Test-Path -LiteralPath (Join-Path $taskOut '执行完成.json')) {
    throw 'Migration was already executed.'
}
if (Test-Path -LiteralPath (Join-Path $taskRoot 'tools\research-runner\runner.lock')) {
    throw 'Runner lock appeared. No files have been changed by this script.'
}
foreach ($property in $taskPlan.original_index_hashes.PSObject.Properties) {
    $indexPath = Assert-WorkspacePath $property.Name
    $actual = (Get-FileHash -LiteralPath $indexPath -Algorithm SHA256).Hash
    if ($actual -ne $property.Value) { throw "Index changed since preflight: $indexPath" }
}
foreach ($operation in @($taskPlan.renames) + @($taskPlan.archive_dirs) + @($taskPlan.file_moves)) {
    $null = Assert-WorkspacePath $operation.source
    $null = Assert-WorkspacePath $operation.destination
}

# 按目录约定先更新权威索引，再迁移分类目录。只复制索引，不生成报告。
foreach ($operation in $taskPlan.index_updates) {
    $source = Assert-WorkspacePath $operation.source
    $destination = Assert-WorkspacePath $operation.destination
    Copy-Item -LiteralPath $source -Destination $destination -Force
    @{action='index';source=$source;destination=$destination;time=(Get-Date).ToString('o')} |
        ConvertTo-Json -Compress | Add-Content -LiteralPath $taskJournal -Encoding utf8
}
foreach ($operation in $taskPlan.renames) { Move-Checked $operation }
foreach ($directory in $taskPlan.ensure_dirs) {
    $absolute = Assert-WorkspacePath $directory
    if (-not (Test-Path -LiteralPath $absolute)) {
        New-Item -ItemType Directory -Path $absolute -Force | Out-Null
    }
}
foreach ($operation in $taskPlan.file_moves) { Move-Checked $operation }
foreach ($operation in $taskPlan.archive_dirs) { Move-Checked $operation }
foreach ($directory in $taskPlan.ensure_dirs) {
    $absolute = Assert-WorkspacePath $directory
    if (-not (Test-Path -LiteralPath $absolute)) {
        New-Item -ItemType Directory -Path $absolute -Force | Out-Null
    }
}
@{
    finishedAt=(Get-Date).ToString('o')
    updatedIndices=@($taskPlan.index_updates).Count
    renamedDirectories=@($taskPlan.renames).Count
    movedCurrentCompanyReports=@($taskPlan.file_moves).Count
    archivedDirectories=@($taskPlan.archive_dirs).Count
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskOut '执行完成.json') -Encoding utf8
Get-Content -LiteralPath (Join-Path $taskOut '执行完成.json') -Raw

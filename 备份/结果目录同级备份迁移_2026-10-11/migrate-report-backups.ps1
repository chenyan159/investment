param([switch]$Apply)
$ErrorActionPreference = 'Stop'
$taskRoot = [IO.Path]::GetFullPath('D:\investment')
$auditRoot = Join-Path $taskRoot '备份\结果目录同级备份迁移_2026-10-11'
if (Test-Path -LiteralPath (Join-Path $taskRoot 'tools\research-runner\runner.lock')) { throw 'Runner lock exists; migration requires an idle runner.' }
$activeQueue = Get-Content -LiteralPath (Join-Path $taskRoot 'tools\queue.jsonl') | Where-Object { $_.Trim() } | ForEach-Object { ConvertFrom-Json $_ }
if (@($activeQueue | Where-Object status -eq 'running').Count) { throw 'Running queue items exist.' }

function Assert-WorkspacePath([string]$value) {
    $resolved = [IO.Path]::GetFullPath($value)
    if (-not $resolved.StartsWith($taskRoot + '\', [StringComparison]::OrdinalIgnoreCase)) { throw "Outside workspace: $resolved" }
    return $resolved
}
function Relative([string]$value) { return [IO.Path]::GetRelativePath($taskRoot, $value).Replace('\','/') }

$specs = @(
    @{Result='基本面/公司调研/结果'; Backup='基本面/公司调研/备份'; Categorized=$true; Pattern='_公司调研_\d{4}-\d{2}-\d{2}\.md$'},
    @{Result='基本面/行业调研/结果'; Backup='基本面/行业调研/备份'; Categorized=$true; Pattern='^行业调研_.+_\d{4}-\d{2}-\d{2}\.md$'},
    @{Result='分析报告/公司情景投资决策/结果'; Backup='分析报告/公司情景投资决策/备份'; Categorized=$false; Pattern='^.+_经营情景市场状态投资决策_\d{4}-\d{2}-\d{2}\.md$'},
    @{Result='分析报告/公司对比/结果'; Backup='分析报告/公司对比/备份'; Categorized=$false; Pattern='^.+_逐家公司投资思路对比_\d{4}-\d{2}-\d{2}\.md$'},
    @{Result='情绪面/公司情绪'; Backup='情绪面/备份/公司情绪'; Categorized=$false; Pattern='^.+_公司情绪_\d{4}-\d{2}-\d{2}\.md$'},
    @{Result='基本面/特征量化/量化评分'; Backup='基本面/特征量化/备份'; Categorized=$false; Pattern='^[NG]\d{2}_.+_量化评分_\d{4}-\d{2}-\d{2}\.md$'}
)
$moves = [Collections.Generic.List[object]]::new()
$formal = [Collections.Generic.List[object]]::new()
$cleanup = [Collections.Generic.List[string]]::new()
$existingBackups = [Collections.Generic.List[object]]::new()
foreach ($spec in $specs) {
    $result = Assert-WorkspacePath (Join-Path $taskRoot $spec.Result)
    $backup = Assert-WorkspacePath (Join-Path $taskRoot $spec.Backup)
    $entries = @(Get-ChildItem -LiteralPath $result -Recurse -Force)
    if (@($entries | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }).Count) { throw "Reparse point found in $result" }
    if (Test-Path -LiteralPath $backup) {
        foreach ($f in Get-ChildItem -LiteralPath $backup -Recurse -File -Force) {
            $existingBackups.Add(@{Path=(Relative $f.FullName); Sha256=(Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash})
        }
    }
    foreach ($d in $entries | Where-Object PSIsContainer) {
        $relative = [IO.Path]::GetRelativePath($result, $d.FullName)
        if (-not $spec.Categorized -or $relative.Contains('\') -or $d.Name -in @('备份','tmp','_work')) { $cleanup.Add($d.FullName) }
    }
    foreach ($f in $entries | Where-Object { -not $_.PSIsContainer }) {
        $relative = [IO.Path]::GetRelativePath($result, $f.FullName).Replace('\','/')
        $parts = $relative.Split('/')
        $expectedDepth = if ($spec.Categorized) { 2 } else { 1 }
        $hash = (Get-FileHash -LiteralPath $f.FullName -Algorithm SHA256).Hash
        if ($parts.Count -eq $expectedDepth -and $f.Name -match $spec.Pattern) {
            $formal.Add(@{Path=(Relative $f.FullName);Sha256=$hash;Bytes=$f.Length;Stage=$spec.Result})
            continue
        }
        $backupIndex = [Array]::IndexOf($parts, '备份')
        $expectedBackupIndex = if ($spec.Categorized) { 1 } else { 0 }
        if ($backupIndex -eq $expectedBackupIndex) {
            $targetParts = @($parts | Select-Object -Skip ($backupIndex + 1))
            $targetRelative = $targetParts -join '/'
            if ($spec.Categorized) { $targetRelative = $parts[0] + '/' + $targetRelative }
            $reason = 'nested-backup'
        } else {
            $targetRelative = '结果杂项迁移_2026-10-11/' + $relative
            $reason = 'non-formal-material'
        }
        $target = Assert-WorkspacePath (Join-Path $backup $targetRelative)
        if (Test-Path -LiteralPath $target) { throw "Destination collision: $target" }
        $moves.Add(@{From=(Relative $f.FullName);To=(Relative $target);Sha256=$hash;Bytes=$f.Length;Reason=$reason;Stage=$spec.Result})
    }
}
if (@($moves | Group-Object To | Where-Object Count -gt 1).Count) { throw 'Duplicate migration destinations.' }
$summary = @{MoveFiles=$moves.Count;FormalFiles=$formal.Count;ExistingBackupFiles=$existingBackups.Count;ByStage=@($moves | Group-Object Stage | ForEach-Object { @{Stage=$_.Name;Count=$_.Count} })}
$summary | ConvertTo-Json -Depth 5
if (-not $Apply) { return }
if (Test-Path -LiteralPath $auditRoot) { throw "Audit directory already exists: $auditRoot" }
New-Item -ItemType Directory -Path $auditRoot | Out-Null
$manifest = @{Date='2026-10-11';Root=$taskRoot;Moves=@($moves);FormalBefore=@($formal);ExistingBackups=@($existingBackups);Summary=$summary}
$manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $auditRoot 'manifest.json') -Encoding utf8
$moves | Select-Object From,To,Sha256,Bytes,Reason,Stage | Export-Csv -LiteralPath (Join-Path $auditRoot '旧路径映射.csv') -NoTypeInformation -Encoding utf8BOM
Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $auditRoot 'migrate-report-backups.ps1')
foreach ($move in $moves) {
    if (Test-Path -LiteralPath (Join-Path $taskRoot 'tools\research-runner\runner.lock')) { throw 'Runner started during migration; see manifest to resume.' }
    $source = Assert-WorkspacePath (Join-Path $taskRoot $move.From)
    $destination = Assert-WorkspacePath (Join-Path $taskRoot $move.To)
    if ((Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash -ne $move.Sha256) { throw "Source changed: $source" }
    if (Test-Path -LiteralPath $destination) { throw "Destination appeared: $destination" }
    New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($destination)) -Force | Out-Null
    Move-Item -LiteralPath $source -Destination $destination
    if ((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $move.Sha256) { throw "Hash mismatch: $destination" }
}
foreach ($directory in $cleanup | Sort-Object Length -Descending -Unique) {
    $checked = Assert-WorkspacePath $directory
    if ((Test-Path -LiteralPath $checked) -and @(Get-ChildItem -LiteralPath $checked -Force).Count -eq 0) {
        Remove-Item -LiteralPath $checked -Force
    }
}
foreach ($entry in @($formal) + @($existingBackups)) {
    $file = Assert-WorkspacePath (Join-Path $taskRoot $entry.Path)
    if ((Get-FileHash -LiteralPath $file -Algorithm SHA256).Hash -ne $entry.Sha256) { throw "Preserved file changed: $file" }
}
$after = @()
foreach ($spec in $specs) {
    $result = Join-Path $taskRoot $spec.Result
    $files = @(Get-ChildItem -LiteralPath $result -File -Recurse -Force)
    $expectedCount = @($formal | Where-Object Stage -eq $spec.Result).Count
    if ($files.Count -ne $expectedCount) { throw "Unexpected remaining files: $result" }
    if (@(Get-ChildItem -LiteralPath $result -Directory -Recurse -Force | Where-Object Name -in @('备份','tmp','_work')).Count) { throw "Unexpected auxiliary directory: $result" }
    $after += @{Stage=$spec.Result;FormalReports=$files.Count}
}
@{Verified=$true;MovedFiles=$moves.Count;PreservedFormalFiles=$formal.Count;PreservedExistingBackups=$existingBackups.Count;Results=$after} | ConvertTo-Json -Depth 5 | Tee-Object -FilePath (Join-Path $auditRoot 'verification.json')

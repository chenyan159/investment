$ErrorActionPreference='Stop'
$taskRoot='D:\investment'
$auditRoot=Join-Path $taskRoot '备份/结果目录同级备份迁移_2026-10-11'
$manifest=Get-Content -LiteralPath (Join-Path $auditRoot 'manifest.json') -Raw | ConvertFrom-Json
$repairs=@()
if(Test-Path -LiteralPath (Join-Path $auditRoot 'link-repairs.json')){$repairs=@(Get-Content -LiteralPath (Join-Path $auditRoot 'link-repairs.json') -Raw | ConvertFrom-Json)}
if (Test-Path -LiteralPath (Join-Path $taskRoot 'tools/research-runner/runner.lock')) {throw 'Runner started; do not change directories.'}
foreach($stage in $manifest.FormalBefore.Stage | Select-Object -Unique){
    $result=[IO.Path]::GetFullPath((Join-Path $taskRoot $stage))
    $dirs=Get-ChildItem -LiteralPath $result -Directory -Recurse -Force | Sort-Object {$_.FullName.Length} -Descending
    foreach($d in $dirs){
        $full=[IO.Path]::GetFullPath($d.FullName)
        if(-not $full.StartsWith($result+'\',[StringComparison]::OrdinalIgnoreCase)){throw "Outside result: $full"}
        if(@(Get-ChildItem -LiteralPath $full -Force).Count -eq 0){Remove-Item -LiteralPath $full -Force}
    }
}
foreach($move in $manifest.Moves){
    if(Test-Path -LiteralPath (Join-Path $taskRoot $move.From)){throw "Source remains: $($move.From)"}
    if((Get-FileHash -LiteralPath (Join-Path $taskRoot $move.To) -Algorithm SHA256).Hash -ne $move.Sha256){throw "Hash mismatch: $($move.To)"}
}
foreach($entry in @($manifest.FormalBefore)+@($manifest.ExistingBackups)){
    $repair=$repairs | Where-Object Path -eq $entry.Path
    $expectedHash=$entry.Sha256
    if($repair){
        $expectedHash=$repair.AfterSha256
        if((Get-FileHash -LiteralPath (Join-Path $taskRoot $repair.OriginalBackup) -Algorithm SHA256).Hash -ne $entry.Sha256){throw "Original backup mismatch: $($entry.Path)"}
    }
    if((Get-FileHash -LiteralPath (Join-Path $taskRoot $entry.Path) -Algorithm SHA256).Hash -ne $expectedHash){throw "Preserved file changed: $($entry.Path)"}
}
$results=@()
foreach($stage in $manifest.FormalBefore.Stage | Select-Object -Unique){
    $result=Join-Path $taskRoot $stage
    $files=@(Get-ChildItem -LiteralPath $result -File -Recurse -Force)
    $expected=@($manifest.FormalBefore | Where-Object Stage -eq $stage)
    if($files.Count -ne $expected.Count){throw "Unexpected result count: $stage"}
    if(@(Get-ChildItem -LiteralPath $result -Directory -Recurse -Force | Where-Object Name -in @('备份','tmp','_work')).Count){throw "Auxiliary directory remains: $stage"}
    $results+=@{Stage=$stage;FormalReports=$files.Count}
}
@{Verified=$true;MovedFiles=$manifest.Moves.Count;PreservedFormalFiles=$manifest.FormalBefore.Count;PreservedExistingBackups=$manifest.ExistingBackups.Count;RepairedReports=$repairs.Count;RepairedLinks=@($repairs.Links).Count;Results=$results} | ConvertTo-Json -Depth 5 | Tee-Object -FilePath (Join-Path $auditRoot 'verification.json')
Copy-Item -LiteralPath $PSCommandPath -Destination (Join-Path $auditRoot 'verify-report-backups.ps1')

param([ValidateSet('Prepare','Apply','Verify')][string]$Phase='Prepare')
$ErrorActionPreference='Stop'
$root='D:\investment'
$rank=Join-Path $root '分析报告\公司排序'
$audit=$PSScriptRoot
$manifestPath=Join-Path $audit 'manifest.json'
function Assert-InProject([string]$p) {
    $full=[IO.Path]::GetFullPath($p)
    if(-not $full.StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)){throw "Outside project: $full"}
    return $full
}
function Snapshot([string]$dir) {
    $dir=Assert-InProject $dir
    $rootItem=Get-Item -LiteralPath $dir -Force
    if(-not $rootItem.PSIsContainer -or ($rootItem.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw "Not a real directory: $dir"}
    $stack=[Collections.Generic.Stack[string]]::new();$stack.Push($dir)
    $rows=[Collections.Generic.List[object]]::new()
    while($stack.Count){
        foreach($item in Get-ChildItem -LiteralPath $stack.Pop() -Force){
            if($item.Attributes -band [IO.FileAttributes]::ReparsePoint){throw "Nested reparse point: $($item.FullName)"}
            $rel=[IO.Path]::GetRelativePath($dir,$item.FullName)
            if($item.PSIsContainer){$rows.Add([pscustomobject]@{Path=$rel;Kind='directory';Length=0;Hash=''});$stack.Push($item.FullName)}
            else{$rows.Add([pscustomobject]@{Path=$rel;Kind='file';Length=$item.Length;Hash=(Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash})}
        }
    }
    return @($rows | Sort-Object Path)
}
function Assert-Same($a,$b,[string]$label){
    $one=ConvertTo-Json -InputObject @($a) -Depth 5 -Compress
    $two=ConvertTo-Json -InputObject @($b) -Depth 5 -Compress
    if($one -cne $two){throw "Snapshot mismatch: $label"}
}
function Assert-Link($entry){
    $p=Assert-InProject $entry.Path
    $item=Get-Item -LiteralPath $p -Force
    if(-not $item.PSIsContainer -or $item.LinkType -ne 'Junction' -or -not ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)){throw "Not expected Junction: $p"}
    if([string]$item.Target -ne $entry.Target){throw "Target changed: $p"}
    if($entry.Action -eq 'copy'){
        if([IO.Path]::GetDirectoryName($p) -ne $rank){throw "Unexpected ranking parent: $p"}
    }elseif($p -notin @((Join-Path $root '基本面\分析报告'),(Join-Path $root '基本面\日度资料'))){throw "Unexpected deletion path: $p"}
}
if($Phase -eq 'Prepare'){
    if(Test-Path -LiteralPath $manifestPath){throw 'Manifest already exists'}
    $entries=@();$index=0
    $basic=@('基本面\分析报告','基本面\日度资料')
    foreach($rel in $basic){$item=Get-Item -LiteralPath (Join-Path $root $rel) -Force;$entry=[pscustomobject]@{Path=$item.FullName;Target=[string]$item.Target;Action='unlink';Stage='';Snapshot=@()};Assert-Link $entry;$entries+=$entry}
    $links=@(Get-ChildItem -LiteralPath $rank -Force | Where-Object LinkType -EQ 'Junction' | Sort-Object Name)
    if($links.Count -ne 24){throw "Expected 24 ranking junctions, got $($links.Count)"}
    foreach($link in $links){
        $index++;$target=Assert-InProject ([string]$link.Target)
        if(-not $target.StartsWith($rank+'\',[StringComparison]::OrdinalIgnoreCase)){throw "Unexpected target: $target"}
        $entry=[pscustomobject]@{Path=$link.FullName;Target=$target;Action='copy';Stage=(Join-Path $audit ('staging\{0:D2}' -f $index));Snapshot=@()}
        Assert-Link $entry
        # Refuse unreadable/nested targets rather than deleting a healthy link on a transient error.
        $entry.Snapshot=@(Snapshot $target)
        New-Item -ItemType Directory -Path $entry.Stage | Out-Null
        foreach($row in $entry.Snapshot | Where-Object Kind -EQ 'directory' | Sort-Object { $_.Path.Length }){New-Item -ItemType Directory -Path (Join-Path $entry.Stage $row.Path) | Out-Null}
        foreach($row in $entry.Snapshot | Where-Object Kind -EQ 'file'){Copy-Item -LiteralPath (Join-Path $target $row.Path) -Destination (Join-Path $entry.Stage $row.Path)}
        Assert-Same $entry.Snapshot (Snapshot $entry.Stage) $entry.Path
        $entries+=$entry
        Write-Output "Prepared $index/24: $($link.Name)"
    }
    $protected=@((Join-Path $root 'AGENTS.md'),(Join-Path $root '基本面\AGENTS.md'),(Join-Path $root '分析报告\AGENTS.md'))
    $protected+=@(Get-ChildItem -LiteralPath $rank -File -Force | Select-Object -ExpandProperty FullName)
    $protected+=@(rg --files --hidden 'D:\investment\tools\research-runner' -g '*.mjs' -g '*.json' -g 'README.md' -g '!**/node_modules/**' -g '!**/logs/**' -g '!**/queue-backups/**')
    $protected+=@((Join-Path $root 'tools\queue.jsonl'),(Join-Path $root 'tools\queue.done.jsonl'),(Join-Path $root 'tools\queue.control.json'))
    $hashes=@($protected | Sort-Object -Unique | ForEach-Object { [pscustomobject]@{Path=$_;Hash=(Get-FileHash -LiteralPath $_ -Algorithm SHA256).Hash} })
    [pscustomobject]@{Entries=$entries;Protected=$hashes} | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $manifestPath -Encoding utf8
    Write-Output "PREPARED: $($entries.Count) links; protected files: $($hashes.Count)"
    exit
}
$manifest=Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
if($Phase -eq 'Apply'){
    # Validate the entire batch again before removing any junction object.
    foreach($entry in $manifest.Entries){Assert-Link $entry;if($entry.Action -eq 'copy'){Assert-Same $entry.Snapshot (Snapshot $entry.Target) $entry.Target;Assert-Same $entry.Snapshot (Snapshot $entry.Stage) $entry.Stage}}
    foreach($entry in $manifest.Entries){
        Assert-Link $entry
        # Non-recursive .NET deletion removes only the Junction itself, never its target tree.
        [IO.Directory]::Delete((Assert-InProject $entry.Path),$false)
        if($entry.Action -eq 'copy'){
            $source=Assert-InProject $entry.Stage;$destination=Assert-InProject $entry.Path
            Move-Item -LiteralPath $source -Destination $destination
        }
        [pscustomobject]@{Path=$entry.Path;Action=$entry.Action;CompletedAt=(Get-Date -Format o)} | ConvertTo-Json -Compress | Add-Content -LiteralPath (Join-Path $audit 'operations.jsonl') -Encoding utf8
        Write-Output "Completed $($entry.Action): $($entry.Path)"
    }
}
$files=0;$bytes=0
foreach($entry in $manifest.Entries){
    if($entry.Action -eq 'unlink'){
        if(Test-Path -LiteralPath $entry.Path){throw "Deleted alias remains: $($entry.Path)"}
        if(-not (Test-Path -LiteralPath $entry.Target -PathType Container)){throw "Target missing: $($entry.Target)"}
    }else{
        Assert-Same $entry.Snapshot (Snapshot $entry.Target) "Original target $($entry.Target)"
        Assert-Same $entry.Snapshot (Snapshot $entry.Path) "Independent copy $($entry.Path)"
        foreach($row in $entry.Snapshot | Where-Object Kind -EQ 'file'){$files++;$bytes+=$row.Length}
    }
}
foreach($row in $manifest.Protected){if((Get-FileHash -LiteralPath $row.Path -Algorithm SHA256).Hash -ne $row.Hash){throw "Protected file changed: $($row.Path)"}}
$result=[pscustomobject]@{RemovedBasicLinks=2;MaterializedRankingDirectories=24;CopiedFiles=$files;CopiedBytes=$bytes;OriginalTargetsUnchanged=$true;AllCopyHashesMatch=$true;ProtectedFilesUnchanged=$manifest.Protected.Count;CompletedAt=(Get-Date -Format o)}
$result | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $audit 'verification.json') -Encoding utf8
$result | ConvertTo-Json

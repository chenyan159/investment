$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$workspace = [IO.Path]::GetFullPath('D:\drive\Investment')
$oldAnalysis = [IO.Path]::GetFullPath('D:\drive\Investment\基本面\分析报告')
$oldDaily = [IO.Path]::GetFullPath('D:\drive\Investment\基本面\日度资料')
$newAnalysis = [IO.Path]::GetFullPath('D:\drive\Investment\分析报告')
$newFinancial = [IO.Path]::GetFullPath('D:\drive\Investment\金融资料')
$manifestPath = [IO.Path]::GetFullPath(
    'D:\drive\Investment\备份\目录迁移_2026-07-23_分析报告与金融资料\junction清单_迁移前.csv'
)

foreach ($target in @($newAnalysis, $newFinancial)) {
    if (-not $target.StartsWith($workspace + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "迁移目标越界: $target"
    }
    if (-not (Test-Path -LiteralPath $target -PathType Container)) {
        throw "迁移目标不存在: $target"
    }
}

foreach ($oldLink in @($oldAnalysis, $oldDaily)) {
    if (Test-Path -LiteralPath $oldLink) {
        throw "旧入口已存在，停止避免覆盖: $oldLink"
    }
}

$rows = Import-Csv -LiteralPath $manifestPath
if (@($rows).Count -ne 24) {
    throw "junction 数量异常，预期 24，实际 $(@($rows).Count)"
}

$planned = foreach ($row in $rows) {
    if (-not $row.LinkPath.StartsWith($oldAnalysis + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "junction 路径越界: $($row.LinkPath)"
    }
    if (-not $row.LinkTarget.StartsWith($oldAnalysis + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "junction 目标越界: $($row.LinkTarget)"
    }

    $newLink = $newAnalysis + $row.LinkPath.Substring($oldAnalysis.Length)
    $newTarget = $newAnalysis + $row.LinkTarget.Substring($oldAnalysis.Length)
    if (-not $newLink.StartsWith($newAnalysis + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "新 junction 路径越界: $newLink"
    }
    if (-not $newTarget.StartsWith($newAnalysis + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "新 junction 目标越界: $newTarget"
    }
    if (-not (Test-Path -LiteralPath $newTarget)) {
        throw "新 junction 目标不存在: $newTarget"
    }

    $parent = [IO.Path]::GetDirectoryName($newLink)
    $leaf = [IO.Path]::GetFileName($newLink)
    $existing = @(
        Get-ChildItem -LiteralPath $parent -Force |
            Where-Object { $_.Name -ceq $leaf }
    )
    if ($existing.Count -ne 1) {
        throw "移动后的 junction 对象数量异常: $newLink"
    }
    if (-not ($existing[0].Attributes -band [IO.FileAttributes]::ReparsePoint)) {
        throw "预期替换对象不是 reparse point: $newLink"
    }

    [pscustomobject]@{
        LinkPath = $newLink
        LinkTarget = $newTarget
    }
}

foreach ($item in $planned) {
    Remove-Item -LiteralPath $item.LinkPath -Force
    $created = New-Item -ItemType Junction -Path $item.LinkPath -Target $item.LinkTarget
    $created.Attributes = (
        $created.Attributes -bor
        [IO.FileAttributes]::Hidden -bor
        [IO.FileAttributes]::System
    )
}

foreach ($pair in @(
    [pscustomobject]@{ Link = $oldAnalysis; Target = $newAnalysis },
    [pscustomobject]@{ Link = $oldDaily; Target = $newFinancial }
)) {
    $created = New-Item -ItemType Junction -Path $pair.Link -Target $pair.Target
    $created.Attributes = (
        $created.Attributes -bor
        [IO.FileAttributes]::Hidden -bor
        [IO.FileAttributes]::System
    )
}

$verification = [ordered]@{
    completedAt = (Get-Date).ToString('o')
    physicalTargets = @($newAnalysis, $newFinancial)
    compatibilityLinks = @(
        [ordered]@{
            path = $oldAnalysis
            target = (Get-Item -LiteralPath $oldAnalysis -Force).LinkTarget
            attributes = [string](Get-Item -LiteralPath $oldAnalysis -Force).Attributes
        },
        [ordered]@{
            path = $oldDaily
            target = (Get-Item -LiteralPath $oldDaily -Force).LinkTarget
            attributes = [string](Get-Item -LiteralPath $oldDaily -Force).Attributes
        }
    )
    rebuiltInternalJunctions = @($planned).Count
}

$resultPath = Join-Path ([IO.Path]::GetDirectoryName($manifestPath)) '迁移执行结果.json'
$verification | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $resultPath -Encoding utf8

[pscustomobject]@{
    AnalysisCompatibilityTarget = (Get-Item -LiteralPath $oldAnalysis -Force).LinkTarget
    DailyCompatibilityTarget = (Get-Item -LiteralPath $oldDaily -Force).LinkTarget
    InternalJunctionsRebuilt = @($planned).Count
} | Format-List

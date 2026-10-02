$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

$workspace = [IO.Path]::GetFullPath('D:\drive\Investment')
$scriptRoot = [IO.Path]::GetFullPath('D:\drive\Investment\基本面\scripts')
$featurePlanRoot = [IO.Path]::GetFullPath('D:\drive\Investment\基本面\特征量化\研究方案')
$manifestRoot = [IO.Path]::GetFullPath('D:\drive\Investment\备份\目录迁移_2026-07-23_分析报告与金融资料')
$utf8NoBom = [Text.UTF8Encoding]::new($false)
$utf8Bom = [Text.UTF8Encoding]::new($true)
$log = [Collections.Generic.List[object]]::new()

foreach ($root in @($scriptRoot, $featurePlanRoot, $manifestRoot)) {
    if (-not $root.StartsWith($workspace + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "路径越界: $root"
    }
    if (-not (Test-Path -LiteralPath $root -PathType Container)) {
        throw "目录不存在: $root"
    }
}

function Update-TextFile {
    param(
        [Parameter(Mandatory)]
        [string] $Path,
        [Parameter(Mandatory)]
        [Collections.Specialized.OrderedDictionary] $Replacements,
        [Parameter(Mandatory)]
        [string] $Group
    )

    $resolved = [IO.Path]::GetFullPath($Path)
    if (-not $resolved.StartsWith($workspace + '\', [StringComparison]::OrdinalIgnoreCase)) {
        throw "文件路径越界: $resolved"
    }

    $bytes = [IO.File]::ReadAllBytes($resolved)
    $hasBom = (
        $bytes.Length -ge 3 -and
        $bytes[0] -eq 0xEF -and
        $bytes[1] -eq 0xBB -and
        $bytes[2] -eq 0xBF
    )
    $encoding = if ($hasBom) { $utf8Bom } else { $utf8NoBom }
    $beforeHash = (Get-FileHash -LiteralPath $resolved -Algorithm SHA256).Hash
    $content = [IO.File]::ReadAllText($resolved)
    $replacementCount = 0

    foreach ($old in $Replacements.Keys) {
        $new = [string]$Replacements[$old]
        $count = [regex]::Matches($content, [regex]::Escape([string]$old)).Count
        if ($count) {
            $content = $content.Replace([string]$old, $new)
            $replacementCount += $count
        }
    }

    if ($replacementCount -gt 0) {
        [IO.File]::WriteAllText($resolved, $content, $encoding)
    }
    $afterHash = (Get-FileHash -LiteralPath $resolved -Algorithm SHA256).Hash
    $log.Add([pscustomobject]@{
        Group = $Group
        File = [IO.Path]::GetRelativePath($workspace, $resolved)
        ReplacementCount = $replacementCount
        Changed = $beforeHash -ne $afterHash
        BeforeSHA256 = $beforeHash
        AfterSHA256 = $afterHash
    })
}

$pythonReplacements = [ordered]@{
    'D:\drive\Investment\基本面\分析报告' = 'D:\drive\Investment\分析报告'
    'D:\drive\Investment\基本面\日度资料' = 'D:\drive\Investment\金融资料'
    'D:/drive/Investment/基本面/分析报告' = 'D:/drive/Investment/分析报告'
    'D:/drive/Investment/基本面/日度资料' = 'D:/drive/Investment/金融资料'
    'ROOT / "分析报告"' = 'ROOT.parent / "分析报告"'
    "ROOT / '分析报告'" = "ROOT.parent / '分析报告'"
    'ROOT / "日度资料"' = 'ROOT.parent / "金融资料"'
    "ROOT / '日度资料'" = "ROOT.parent / '金融资料'"
    '基本面/分析报告' = '分析报告'
    '基本面\分析报告' = '分析报告'
    '基本面/日度资料' = '金融资料'
    '基本面\日度资料' = '金融资料'
    '日度资料/' = '金融资料/'
    '日度资料\' = '金融资料\'
    '日度资料' = '金融资料'
}

$pythonFiles = @(
    Get-ChildItem -LiteralPath $scriptRoot -Recurse -File -Filter '*.py' |
        Sort-Object FullName
)
foreach ($file in $pythonFiles) {
    Update-TextFile -Path $file.FullName -Replacements $pythonReplacements -Group '基本面/scripts'
}

$featureReplacements = [ordered]@{
    'D:\drive\Investment\基本面\分析报告' = 'D:\drive\Investment\分析报告'
    'D:\drive\Investment\基本面\日度资料' = 'D:\drive\Investment\金融资料'
    'D:/drive/Investment/基本面/分析报告' = 'D:/drive/Investment/分析报告'
    'D:/drive/Investment/基本面/日度资料' = 'D:/drive/Investment/金融资料'
    '基本面/分析报告' = '分析报告'
    '基本面\分析报告' = '分析报告'
    '基本面/日度资料' = '金融资料'
    '基本面\日度资料' = '金融资料'
    '日度资料/' = '金融资料/'
    '日度资料\' = '金融资料\'
    '日度资料' = '金融资料'
}

$featureFiles = @(
    Get-ChildItem -LiteralPath $featurePlanRoot -File -Filter '*.md' |
        Where-Object { $_.Name -match '^[NG]\d{2}_.+_研究方案\.md$' } |
        Sort-Object FullName
)
if ($featureFiles.Count -ne 19) {
    throw "当前特征研究方案数量异常，预期 19，实际 $($featureFiles.Count)"
}
foreach ($file in $featureFiles) {
    Update-TextFile -Path $file.FullName -Replacements $featureReplacements -Group '特征量化/研究方案'
}

$oldPythonReferences = @(
    Select-String -LiteralPath $pythonFiles.FullName -Pattern @(
        'ROOT\s*/\s*["'']分析报告["'']',
        'ROOT\s*/\s*["'']日度资料["'']',
        '基本面[\\/]分析报告',
        '基本面[\\/]日度资料',
        '日度资料'
    )
)
if ($oldPythonReferences.Count) {
    throw "Python 活动脚本仍有旧路径引用，共 $($oldPythonReferences.Count) 处"
}

foreach ($file in $featureFiles) {
    $content = [IO.File]::ReadAllText($file.FullName)
    foreach ($required in @(
        '`基本面/公司调研/`',
        '`基本面/行业调研/`',
        '`金融资料/每日金融数据/`'
    )) {
        if (-not $content.Contains($required)) {
            throw "$($file.Name) 缺少允许输入路径: $required"
        }
    }
    if ($content -match '基本面[\\/]分析报告|基本面[\\/]日度资料|日度资料') {
        throw "$($file.Name) 仍含旧目录引用"
    }
}

$logPath = Join-Path $manifestRoot '批量活动引用修改记录.csv'
$log | Export-Csv -LiteralPath $logPath -NoTypeInformation -Encoding utf8
$summary = [ordered]@{
    completedAt = (Get-Date).ToString('o')
    pythonFilesScanned = $pythonFiles.Count
    pythonFilesChanged = @($log | Where-Object { $_.Group -eq '基本面/scripts' -and $_.Changed }).Count
    featurePlansScanned = $featureFiles.Count
    featurePlansChanged = @($log | Where-Object { $_.Group -eq '特征量化/研究方案' -and $_.Changed }).Count
    totalReplacements = [int](($log | Measure-Object ReplacementCount -Sum).Sum)
}
$summary | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $manifestRoot '批量活动引用修改摘要.json') -Encoding utf8
$summary | Format-List

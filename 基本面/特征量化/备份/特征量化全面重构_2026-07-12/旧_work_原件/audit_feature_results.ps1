[CmdletBinding()]
param(
    [Parameter()]
    [string]$InvestmentRoot = 'D:\drive\Investment',

    [Parameter()]
    [string]$OutputDirectory
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $InvestmentRoot '基本面\特征量化\_work\restructure_20260712'
}

$resultDirectory = Join-Path $InvestmentRoot '基本面\特征量化\量化评分'
New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

function Get-Sha256Text {
    param([AllowEmptyString()][string]$Text)
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
    $hash = [System.Security.Cryptography.SHA256]::HashData($bytes)
    return [Convert]::ToHexString($hash).ToLowerInvariant()
}

function ConvertFrom-MarkdownTableRow {
    param([Parameter(Mandatory)][string]$Line)

    $text = $Line.Trim()
    if ($text.StartsWith('|')) { $text = $text.Substring(1) }
    if ($text.EndsWith('|')) { $text = $text.Substring(0, $text.Length - 1) }

    $cells = [System.Collections.Generic.List[string]]::new()
    $buffer = [System.Text.StringBuilder]::new()
    $escaped = $false

    foreach ($char in $text.ToCharArray()) {
        if ($escaped) {
            [void]$buffer.Append($char)
            $escaped = $false
            continue
        }
        if ($char -eq '\') {
            [void]$buffer.Append($char)
            $escaped = $true
            continue
        }
        if ($char -eq '|') {
            $cells.Add($buffer.ToString().Trim())
            [void]$buffer.Clear()
            continue
        }
        [void]$buffer.Append($char)
    }
    $cells.Add($buffer.ToString().Trim())
    return $cells.ToArray()
}

function Get-SectionLines {
    param(
        [Parameter(Mandatory)][AllowEmptyCollection()][AllowEmptyString()][string[]]$Lines,
        [Parameter(Mandatory)][string]$Heading
    )
    $start = [Array]::IndexOf($Lines, $Heading)
    if ($start -lt 0) { return @() }
    $output = [System.Collections.Generic.List[string]]::new()
    for ($i = $start + 1; $i -lt $Lines.Count; $i++) {
        if ($Lines[$i] -match '^##\s+') { break }
        $output.Add($Lines[$i])
    }
    return $output.ToArray()
}

function Get-FirstRegexGroup {
    param(
        [AllowEmptyString()][string]$Text,
        [Parameter(Mandatory)][string]$Pattern,
        [int]$Group = 1
    )
    if ($Text -match $Pattern) { return $Matches[$Group] }
    return $null
}

function Get-PearsonCorrelation {
    param(
        [Parameter(Mandatory)][double[]]$X,
        [Parameter(Mandatory)][double[]]$Y
    )
    if ($X.Count -ne $Y.Count -or $X.Count -lt 2) { return $null }
    $meanX = ($X | Measure-Object -Average).Average
    $meanY = ($Y | Measure-Object -Average).Average
    [double]$sumXY = 0
    [double]$sumX2 = 0
    [double]$sumY2 = 0
    for ($i = 0; $i -lt $X.Count; $i++) {
        $dx = $X[$i] - $meanX
        $dy = $Y[$i] - $meanY
        $sumXY += $dx * $dy
        $sumX2 += $dx * $dx
        $sumY2 += $dy * $dy
    }
    if ($sumX2 -eq 0 -or $sumY2 -eq 0) { return $null }
    return $sumXY / [Math]::Sqrt($sumX2 * $sumY2)
}

function Export-Utf8Csv {
    param(
        [Parameter(Mandatory)][AllowEmptyCollection()][object[]]$Data,
        [Parameter(Mandatory)][string]$Path
    )
    if ($Data.Count -eq 0) {
        Set-Content -LiteralPath $Path -Value '' -Encoding utf8
        return
    }
    $Data | Export-Csv -LiteralPath $Path -NoTypeInformation -Encoding utf8
}

function Export-Utf8Json {
    param(
        [Parameter(Mandatory)][object]$Data,
        [Parameter(Mandatory)][string]$Path,
        [int]$Depth = 6,
        [switch]$AsArray
    )
    if ($AsArray) {
        $json = $Data | ConvertTo-Json -Depth $Depth -AsArray
    } else {
        $json = $Data | ConvertTo-Json -Depth $Depth
    }
    Set-Content -LiteralPath $Path -Value $json -Encoding utf8
}

$formalFiles = Get-ChildItem -LiteralPath $resultDirectory -File |
    Where-Object { $_.Name -match '^F(?<number>\d{2})_(?<feature>.+)_量化评分_(?<date>\d{4}-\d{2}-\d{2})\.md$' } |
    Sort-Object Name

if ($formalFiles.Count -ne 52) {
    throw "Expected 52 formal result files in the score root, found $($formalFiles.Count)."
}

$metadata = [System.Collections.Generic.List[object]]::new()
$longRows = [System.Collections.Generic.List[object]]::new()
$qaRows = [System.Collections.Generic.List[object]]::new()
$expectedHeader = @('排名', '股票代号', '公司名称', '分类目录', '特征分', '证据等级', '置信度', '核心证据', '缺失/降权', '后续核验')

foreach ($file in $formalFiles) {
    if ($file.Name -notmatch '^F(?<number>\d{2})_(?<feature>.+)_量化评分_(?<date>\d{4}-\d{2}-\d{2})\.md$') {
        throw "Unexpected formal file name: $($file.Name)"
    }
    $featureId = "F$($Matches.number)"
    $featureNumber = [int]$Matches.number
    $featureName = $Matches.feature
    $fileDate = $Matches.date
    $lines = @(Get-Content -LiteralPath $file.FullName -Encoding utf8)
    $titleLine = if ($lines.Count -gt 0) { $lines[0].Trim() } else { '' }
    $headingDate = Get-FirstRegexGroup -Text $titleLine -Pattern '(\d{4}-\d{2}-\d{2})\s*$'

    $metaLines = @(Get-SectionLines -Lines $lines -Heading '## 运行元信息')
    $metaText = ($metaLines | Where-Object { $_.Trim() } | ForEach-Object { $_.Trim() }) -join ' ⏎ '
    $metaMap = [ordered]@{}
    foreach ($line in $metaLines) {
        $metaMatch = [regex]::Match($line, '^\s*-\s*([^：:]+)[：:]\s*(.*)$')
        if ($metaMatch.Success) {
            $label = $metaMatch.Groups[1].Value.Trim()
            $value = $metaMatch.Groups[2].Value.Trim()
            if (-not $metaMap.Contains($label)) { $metaMap[$label] = $value }
        }
    }

    $bodyFeatureName = if ($metaMap.Contains('特征名称')) { $metaMap['特征名称'] } else { $null }
    $bodyScoreDate = if ($metaMap.Contains('评分日期')) { Get-FirstRegexGroup -Text $metaMap['评分日期'] -Pattern '(\d{4}-\d{2}-\d{2})' } else { $null }
    $declaredCount = if ($metaMap.Contains('公司数量')) {
        $numberText = Get-FirstRegexGroup -Text $metaMap['公司数量'] -Pattern '(\d+)'
        if ($numberText) { [int]$numberText } else { $null }
    } else { $null }

    $snapshotPath = if ($metaMap.Contains('金融数据')) { $metaMap['金融数据'] } else { $null }
    if (-not $snapshotPath) {
        $snapshotPath = Get-FirstRegexGroup -Text $metaText -Pattern '([^\s；;，,`]*每日金融数据_\d{4}-\d{2}-\d{2}\.md)'
    }
    $snapshotDate = Get-FirstRegexGroup -Text $metaText -Pattern '每日金融数据_(\d{4}-\d{2}-\d{2})\.md'

    $dataRelatedText = ($metaLines | Where-Object { $_ -match '金融|价格|估值|数据日期|数据生成|采集日期|采集时间' }) -join ' '
    $dataDates = @([regex]::Matches($dataRelatedText, '\b\d{4}-\d{2}-\d{2}\b') | ForEach-Object { $_.Value } | Sort-Object -Unique)
    $inputGeneratedTimestamp = Get-FirstRegexGroup -Text $dataRelatedText -Pattern '(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\s+(?:PDT|PST)(?:-?\d{4})?)?)'
    $bodyExactRunTimestamp = Get-FirstRegexGroup -Text $metaText -Pattern '(?:本次)?运行时间[：:]?\s*(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}(?:\s+(?:PDT|PST)(?:-?\d{4})?)?)'

    $tableLines = @(Get-SectionLines -Lines $lines -Heading '## 全公司排序表')
    $headerIndex = -1
    $headerCells = @()
    for ($i = 0; $i -lt $tableLines.Count; $i++) {
        if ($tableLines[$i].Trim() -match '^\|.*\|$') {
            $candidate = @(ConvertFrom-MarkdownTableRow -Line $tableLines[$i])
            if ($candidate.Count -gt 0 -and $candidate[0] -eq '排名') {
                $headerIndex = $i
                $headerCells = $candidate
                break
            }
        }
    }
    if ($headerIndex -lt 0) { throw "No all-company table header in $($file.Name)" }

    $featureRows = [System.Collections.Generic.List[object]]::new()
    for ($i = $headerIndex + 2; $i -lt $tableLines.Count; $i++) {
        $line = $tableLines[$i].Trim()
        if (-not $line) { if ($featureRows.Count -gt 0) { break } else { continue } }
        if ($line -notmatch '^\|.*\|$') { if ($featureRows.Count -gt 0) { break } else { continue } }
        $cells = @(ConvertFrom-MarkdownTableRow -Line $line)
        if ($cells.Count -lt 7) { continue }
        [int]$rank = 0
        [double]$score = [double]::NaN
        $rankOk = [int]::TryParse($cells[0], [ref]$rank)
        $scoreOk = [double]::TryParse($cells[4], [Globalization.NumberStyles]::Float, [Globalization.CultureInfo]::InvariantCulture, [ref]$score)
        $row = [pscustomobject][ordered]@{
            FeatureId       = $featureId
            FeatureName     = $featureName
            FileName        = $file.Name
            FileDate        = $fileDate
            Rank            = if ($rankOk) { $rank } else { $null }
            Ticker          = $cells[1].Trim()
            Company         = $cells[2].Trim()
            Category        = $cells[3].Trim()
            Score           = if ($scoreOk) { $score } else { $null }
            EvidenceGrade   = $cells[5].Trim()
            Confidence      = $cells[6].Trim()
            RawColumnCount  = $cells.Count
        }
        $featureRows.Add($row)
        $longRows.Add($row)
    }

    $tickers = @($featureRows | ForEach-Object { $_.Ticker })
    $uniqueTickers = @($tickers | Sort-Object -Unique)
    $ranks = @($featureRows | ForEach-Object { $_.Rank })
    $validScores = @($featureRows | Where-Object { $null -ne $_.Score } | ForEach-Object { [double]$_.Score })
    $duplicateTickers = @($featureRows | Group-Object Ticker | Where-Object Count -gt 1 | ForEach-Object Name)
    $duplicateRanks = @($featureRows | Group-Object Rank | Where-Object Count -gt 1 | ForEach-Object Name)
    $expectedRanks = if ($featureRows.Count -gt 0) { 1..$featureRows.Count } else { @() }
    $missingRanks = @($expectedRanks | Where-Object { $_ -notin $ranks })
    $rankSequenceValid = (($missingRanks.Count -eq 0) -and ($duplicateRanks.Count -eq 0) -and ($ranks.Count -eq $featureRows.Count))
    $scoreOrderValid = $true
    for ($i = 1; $i -lt $featureRows.Count; $i++) {
        if (($null -eq $featureRows[$i - 1].Score) -or ($null -eq $featureRows[$i].Score) -or
            ([double]$featureRows[$i].Score -gt [double]$featureRows[$i - 1].Score)) {
            $scoreOrderValid = $false
            break
        }
    }
    $invalidScoreCount = @($featureRows | Where-Object {
        ($null -eq $_.Score) -or ([double]$_.Score -lt 1.0) -or ([double]$_.Score -gt 10.0) -or
        ([Math]::Abs(([double]$_.Score * 10) - [Math]::Round([double]$_.Score * 10)) -gt 1e-9)
    }).Count
    $invalidConfidence = @($featureRows | Where-Object { $_.Confidence -notin @('高', '中', '低') })
    $invalidGrade = @($featureRows | Where-Object { $_.EvidenceGrade -notmatch '^[A-D]$' })
    $columnCountAnomalies = @($featureRows | Where-Object RawColumnCount -ne 10)
    $tickerSetHash = Get-Sha256Text (($uniqueTickers -join "`n"))
    $tickerOrderHash = Get-Sha256Text (($tickers -join "`n"))
    $scoreHash = Get-Sha256Text ((@($featureRows | Sort-Object Ticker | ForEach-Object { "$($_.Ticker)=$($_.Score)" }) -join "`n"))
    $rankHash = Get-Sha256Text ((@($featureRows | Sort-Object Ticker | ForEach-Object { "$($_.Ticker)=$($_.Rank)" }) -join "`n"))

    $metadata.Add([pscustomobject][ordered]@{
        FeatureId                   = $featureId
        FeatureNumber               = $featureNumber
        FeatureNameFromFile         = $featureName
        FeatureNameFromBody         = $bodyFeatureName
        FileName                    = $file.Name
        FileDate                    = $fileDate
        HeadingDate                 = $headingDate
        BodyScoreDate               = $bodyScoreDate
        BodyExactRunTimestamp       = $bodyExactRunTimestamp
        BodyExactRunTimePresent     = [bool]$bodyExactRunTimestamp
        DeclaredCompanyCount        = $declaredCount
        DataSnapshotPath            = $snapshotPath
        DataSnapshotFileDate        = $snapshotDate
        DataDatesInMetadata         = $dataDates -join ';'
        InputGeneratedTimestamp     = $inputGeneratedTimestamp
        CreationTimeLocal           = $file.CreationTime.ToString('yyyy-MM-dd HH:mm:ss.fff zzz')
        LastWriteTimeLocal          = $file.LastWriteTime.ToString('yyyy-MM-dd HH:mm:ss.fff zzz')
        CreationTimeUtc             = $file.CreationTimeUtc.ToString('yyyy-MM-dd HH:mm:ss.fffZ')
        LastWriteTimeUtc            = $file.LastWriteTimeUtc.ToString('yyyy-MM-dd HH:mm:ss.fffZ')
        LengthBytes                 = $file.Length
        TitleLine                   = $titleLine
        RunMetadataRaw              = $metaText
    })

    $qaRows.Add([pscustomobject][ordered]@{
        FeatureId                   = $featureId
        FeatureName                 = $featureName
        RowCount                    = $featureRows.Count
        DeclaredCompanyCount        = $declaredCount
        UniqueTickerCount           = $uniqueTickers.Count
        DuplicateTickerCount        = $duplicateTickers.Count
        DuplicateTickers            = $duplicateTickers -join ';'
        MissingRankCount            = $missingRanks.Count
        MissingRanks                = $missingRanks -join ';'
        DuplicateRankCount          = $duplicateRanks.Count
        DuplicateRanks              = $duplicateRanks -join ';'
        RankSequenceValid           = $rankSequenceValid
        ScoreDescendingValid        = $scoreOrderValid
        InvalidScoreCount           = $invalidScoreCount
        ScoreMin                    = if ($validScores.Count) { ($validScores | Measure-Object -Minimum).Minimum } else { $null }
        ScoreMax                    = if ($validScores.Count) { ($validScores | Measure-Object -Maximum).Maximum } else { $null }
        ScoreAverage                = if ($validScores.Count) { [Math]::Round(($validScores | Measure-Object -Average).Average, 6) } else { $null }
        InvalidConfidenceCount      = $invalidConfidence.Count
        InvalidConfidenceValues     = (@($invalidConfidence | ForEach-Object Confidence | Sort-Object -Unique) -join ';')
        InvalidEvidenceGradeCount   = $invalidGrade.Count
        InvalidEvidenceGradeValues  = (@($invalidGrade | ForEach-Object EvidenceGrade | Sort-Object -Unique) -join ';')
        TableColumnCountAnomalyCount = $columnCountAnomalies.Count
        HeaderExactMatch            = (($headerCells.Count -eq $expectedHeader.Count) -and (($headerCells -join "`n") -eq ($expectedHeader -join "`n")))
        TickerSetSha256             = $tickerSetHash
        TickerOrderSha256           = $tickerOrderHash
        ScoreVectorSha256           = $scoreHash
        RankVectorSha256            = $rankHash
    })
}

$featureIds = @($metadata | Sort-Object FeatureId | ForEach-Object FeatureId)
$tickerGroups = @($longRows | Group-Object Ticker | Sort-Object Name)
$tickerPool = [System.Collections.Generic.List[object]]::new()

foreach ($group in $tickerGroups) {
    $rows = @($group.Group)
    $presentFeatures = @($rows | ForEach-Object FeatureId | Sort-Object -Unique)
    $missingFeatures = @($featureIds | Where-Object { $_ -notin $presentFeatures })
    $companyGroups = @($rows | Group-Object Company | Sort-Object @{ Expression = 'Count'; Descending = $true }, @{ Expression = 'Name'; Descending = $false })
    $categoryGroups = @($rows | Group-Object Category | Sort-Object @{ Expression = 'Count'; Descending = $true }, @{ Expression = 'Name'; Descending = $false })
    $companies = @($companyGroups | ForEach-Object Name | Sort-Object -Unique)
    $categories = @($categoryGroups | ForEach-Object Name | Sort-Object -Unique)
    $tickerPool.Add([pscustomobject][ordered]@{
        Ticker              = $group.Name
        CompanyCanonical    = $companyGroups[0].Name
        CompanyVariants     = $companies -join ' | '
        CompanyVariantBreakdown = @($companyGroups | ForEach-Object { "$($_.Name) ($($_.Count))" }) -join ' | '
        CompanyVariantCount = $companies.Count
        CategoryCanonical   = $categoryGroups[0].Name
        CategoryVariants    = $categories -join ' | '
        CategoryVariantBreakdown = @($categoryGroups | ForEach-Object { "$($_.Name) ($($_.Count))" }) -join ' | '
        CategoryVariantCount = $categories.Count
        FeatureCount        = $presentFeatures.Count
        MissingFeatureCount = $missingFeatures.Count
        MissingFeatures     = $missingFeatures -join ';'
    })
}

$featureTickerLookup = @{}
foreach ($featureId in $featureIds) { $featureTickerLookup[$featureId] = @{} }
foreach ($row in $longRows) { $featureTickerLookup[$row.FeatureId][$row.Ticker] = $row }

function New-WideTable {
    param(
        [Parameter(Mandatory)][string]$ValueProperty,
        [Parameter(Mandatory)][AllowEmptyString()][string]$ColumnPrefix
    )
    $wide = [System.Collections.Generic.List[object]]::new()
    foreach ($tickerRow in $tickerPool) {
        $row = [ordered]@{
            Ticker   = $tickerRow.Ticker
            Company  = $tickerRow.CompanyCanonical
            Category = $tickerRow.CategoryCanonical
        }
        foreach ($featureId in $featureIds) {
            $columnName = if ($ColumnPrefix) { "${ColumnPrefix}_${featureId}" } else { $featureId }
            $featureLookup = $featureTickerLookup[$featureId]
            $row[$columnName] = if ($featureLookup.ContainsKey($tickerRow.Ticker)) { $featureLookup[$tickerRow.Ticker].$ValueProperty } else { $null }
        }
        $wide.Add([pscustomobject]$row)
    }
    return $wide.ToArray()
}

$scoresWide = @(New-WideTable -ValueProperty 'Score' -ColumnPrefix '')
$ranksWide = @(New-WideTable -ValueProperty 'Rank' -ColumnPrefix '')
$confidenceWide = @(New-WideTable -ValueProperty 'Confidence' -ColumnPrefix '')

$pairwise = [System.Collections.Generic.List[object]]::new()
for ($i = 0; $i -lt $featureIds.Count; $i++) {
    for ($j = $i + 1; $j -lt $featureIds.Count; $j++) {
        $f1 = $featureIds[$i]
        $f2 = $featureIds[$j]
        $leftLookup = $featureTickerLookup[$f1]
        $rightLookup = $featureTickerLookup[$f2]
        $paired = @($tickerPool | ForEach-Object {
            $ticker = $_.Ticker
            $left = if ($leftLookup.ContainsKey($ticker)) { $leftLookup[$ticker] } else { $null }
            $right = if ($rightLookup.ContainsKey($ticker)) { $rightLookup[$ticker] } else { $null }
            if ($left -and $right) { [pscustomobject]@{ Left = $left; Right = $right } }
        })
        $xScore = [double[]]@($paired | ForEach-Object { [double]$_.Left.Score })
        $yScore = [double[]]@($paired | ForEach-Object { [double]$_.Right.Score })
        $xRank = [double[]]@($paired | ForEach-Object { [double]$_.Left.Rank })
        $yRank = [double[]]@($paired | ForEach-Object { [double]$_.Right.Rank })
        $scoreEqualCount = @($paired | Where-Object { [double]$_.Left.Score -eq [double]$_.Right.Score }).Count
        $rankEqualCount = @($paired | Where-Object { [int]$_.Left.Rank -eq [int]$_.Right.Rank }).Count
        $scoreCorrelation = Get-PearsonCorrelation -X $xScore -Y $yScore
        $rankCorrelation = Get-PearsonCorrelation -X $xRank -Y $yRank
        $pairwise.Add([pscustomobject][ordered]@{
            Feature1             = $f1
            Feature2             = $f2
            CommonTickerCount    = $paired.Count
            ScorePearson         = if ($null -ne $scoreCorrelation) { [Math]::Round($scoreCorrelation, 8) } else { $null }
            RankPearson          = if ($null -ne $rankCorrelation) { [Math]::Round($rankCorrelation, 8) } else { $null }
            EqualScoreCount      = $scoreEqualCount
            EqualRankCount       = $rankEqualCount
            ExactScoreVector     = ($scoreEqualCount -eq $paired.Count)
            ExactRankVector      = ($rankEqualCount -eq $paired.Count)
        })
    }
}

$exactDuplicatePairs = @($pairwise | Where-Object { $_.ExactScoreVector -or $_.ExactRankVector })
$nearDuplicatePairs = @($pairwise | Where-Object { (-not $_.ExactScoreVector) -and [Math]::Abs([double]$_.ScorePearson) -ge 0.95 } | Sort-Object @{ Expression = { [Math]::Abs([double]$_.ScorePearson) }; Descending = $true })
$highSimilarityPairs = @($pairwise | Where-Object { (-not $_.ExactScoreVector) -and [Math]::Abs([double]$_.ScorePearson) -ge 0.85 } | Sort-Object @{ Expression = { [Math]::Abs([double]$_.ScorePearson) }; Descending = $true })
$tableAnomalies = @($longRows | Where-Object RawColumnCount -ne 10)

$featureSetHashes = @($qaRows | Group-Object TickerSetSha256)
$scoreDuplicateGroups = @($qaRows | Group-Object ScoreVectorSha256 | Where-Object Count -gt 1 | ForEach-Object {
    [pscustomobject]@{
        ScoreVectorSha256 = $_.Name
        FeatureCount      = $_.Count
        Features          = (@($_.Group | ForEach-Object FeatureId | Sort-Object) -join ';')
    }
})
$rankDuplicateGroups = @($qaRows | Group-Object RankVectorSha256 | Where-Object Count -gt 1 | ForEach-Object {
    [pscustomobject]@{
        RankVectorSha256 = $_.Name
        FeatureCount     = $_.Count
        Features         = (@($_.Group | ForEach-Object FeatureId | Sort-Object) -join ';')
    }
})

$paths = [ordered]@{
    metadata_csv             = Join-Path $OutputDirectory 'feature_files_metadata.csv'
    metadata_json            = Join-Path $OutputDirectory 'feature_files_metadata.json'
    scores_long_csv          = Join-Path $OutputDirectory 'feature_scores_long.csv'
    scores_long_json         = Join-Path $OutputDirectory 'feature_scores_long.json'
    scores_wide_csv          = Join-Path $OutputDirectory 'feature_scores_wide.csv'
    ranks_wide_csv           = Join-Path $OutputDirectory 'feature_ranks_wide.csv'
    confidence_wide_csv      = Join-Path $OutputDirectory 'feature_confidence_wide.csv'
    unified_ticker_pool_csv  = Join-Path $OutputDirectory 'unified_ticker_pool.csv'
    feature_qa_csv           = Join-Path $OutputDirectory 'feature_qa.csv'
    pairwise_similarity_csv  = Join-Path $OutputDirectory 'feature_pairwise_similarity.csv'
    duplicate_pairs_csv      = Join-Path $OutputDirectory 'duplicate_score_rank_pairs.csv'
    near_duplicate_pairs_csv = Join-Path $OutputDirectory 'near_duplicate_score_pairs.csv'
    high_similarity_pairs_csv = Join-Path $OutputDirectory 'high_similarity_score_pairs_ge_0_85.csv'
    table_anomalies_csv      = Join-Path $OutputDirectory 'table_column_anomalies.csv'
    manifest_json            = Join-Path $OutputDirectory 'audit_manifest.json'
}

Export-Utf8Csv -Data @($metadata) -Path $paths.metadata_csv
Export-Utf8Json -Data @($metadata) -Path $paths.metadata_json -Depth 4 -AsArray
Export-Utf8Csv -Data @($longRows) -Path $paths.scores_long_csv
Export-Utf8Json -Data @($longRows) -Path $paths.scores_long_json -Depth 4 -AsArray
Export-Utf8Csv -Data $scoresWide -Path $paths.scores_wide_csv
Export-Utf8Csv -Data $ranksWide -Path $paths.ranks_wide_csv
Export-Utf8Csv -Data $confidenceWide -Path $paths.confidence_wide_csv
Export-Utf8Csv -Data @($tickerPool) -Path $paths.unified_ticker_pool_csv
Export-Utf8Csv -Data @($qaRows) -Path $paths.feature_qa_csv
Export-Utf8Csv -Data @($pairwise) -Path $paths.pairwise_similarity_csv
Export-Utf8Csv -Data $exactDuplicatePairs -Path $paths.duplicate_pairs_csv
Export-Utf8Csv -Data $nearDuplicatePairs -Path $paths.near_duplicate_pairs_csv
Export-Utf8Csv -Data $highSimilarityPairs -Path $paths.high_similarity_pairs_csv
Export-Utf8Csv -Data $tableAnomalies -Path $paths.table_anomalies_csv

$manifest = [ordered]@{
    generated_at_local = (Get-Date).ToString('yyyy-MM-dd HH:mm:ss.fff zzz')
    investment_root = $InvestmentRoot
    result_directory = $resultDirectory
    scope_rule = 'Only files matching Fdd_*_量化评分_YYYY-MM-DD.md directly in 量化评分 root; backup subdirectory excluded.'
    formal_file_count = $formalFiles.Count
    feature_ids = $featureIds
    all_filename_dates = @($metadata | ForEach-Object FileDate | Sort-Object -Unique)
    all_heading_dates = @($metadata | ForEach-Object HeadingDate | Sort-Object -Unique)
    all_body_score_dates = @($metadata | ForEach-Object BodyScoreDate | Sort-Object -Unique)
    body_exact_run_timestamp_file_count = @($metadata | Where-Object BodyExactRunTimePresent).Count
    output_row_count = $longRows.Count
    unified_ticker_count = $tickerPool.Count
    feature_row_count_distribution = @($qaRows | Group-Object RowCount | ForEach-Object { [ordered]@{ row_count = [int]$_.Name; feature_count = $_.Count } })
    unique_ticker_set_hash_count = $featureSetHashes.Count
    score_duplicate_groups = $scoreDuplicateGroups
    rank_duplicate_groups = $rankDuplicateGroups
    exact_duplicate_pair_count = $exactDuplicatePairs.Count
    near_duplicate_pair_count_abs_pearson_ge_0_95_excluding_exact = $nearDuplicatePairs.Count
    high_similarity_pair_count_abs_pearson_ge_0_85_excluding_exact = $highSimilarityPairs.Count
    table_column_anomaly_row_count = $tableAnomalies.Count
    files = $paths
}
Export-Utf8Json -Data $manifest -Path $paths.manifest_json -Depth 8

$manifest | ConvertTo-Json -Depth 8

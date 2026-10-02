#requires -Version 7.0

[CmdletBinding()]
param(
    [string]$FeatureRoot = 'D:\drive\Investment\基本面\特征量化',
    [datetime]$AsOfDate = [datetime]'2026-07-12',
    [int]$PauseMilliseconds = 120
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
[System.Globalization.CultureInfo]::CurrentCulture = [System.Globalization.CultureInfo]::InvariantCulture
[System.Globalization.CultureInfo]::CurrentUICulture = [System.Globalization.CultureInfo]::InvariantCulture

$OutputDir = Join-Path $FeatureRoot '_work\restructure_20260712'
$ScoreDir = Join-Path $FeatureRoot '量化评分'
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# Research-ticker to current Yahoo Finance symbol. Only use documented identity-preserving
# changes; do not guess replacements for missing quotes.
$TickerMap = @{
    'PSTG' = [pscustomobject]@{
        YahooSymbol = 'P'
        Note = 'Everpure official ticker change PSTG->P effective 2026-04-17; CUSIP unchanged'
        Source = 'https://www.everpuredata.com/company/newsroom/press-releases/everpure-to-change-ticker-symbol.html'
    }
}

$Benchmarks = @('SPY', 'QQQ', 'SOXX')
$YahooAdjustedCloseHelp = 'https://uk.help.yahoo.com/kb/finance/adjusted-close-sln28256.html'

function Get-IsoDateFromEpoch {
    param([long]$Epoch)
    return [DateTimeOffset]::FromUnixTimeSeconds($Epoch).UtcDateTime.ToString('yyyy-MM-dd')
}

function Get-YahooChartUrl {
    param(
        [string]$Symbol,
        [datetime]$StartDate,
        [datetime]$EndDateExclusive
    )
    $p1 = [DateTimeOffset]::new($StartDate.ToUniversalTime()).ToUnixTimeSeconds()
    $p2 = [DateTimeOffset]::new($EndDateExclusive.ToUniversalTime()).ToUnixTimeSeconds()
    $encoded = [Uri]::EscapeDataString($Symbol)
    return "https://query1.finance.yahoo.com/v8/finance/chart/$encoded`?period1=$p1&period2=$p2&interval=1d&events=div%2Csplits%2CcapitalGains"
}

function Invoke-YahooChart {
    param([string]$Url)
    $lastError = $null
    for ($attempt = 1; $attempt -le 4; $attempt++) {
        try {
            $payload = Invoke-RestMethod -Uri $Url -Method Get -Headers @{
                'User-Agent' = 'Mozilla/5.0 (compatible; feature-return-audit/1.0)'
                'Accept' = 'application/json'
            } -TimeoutSec 30
            if ($null -ne $payload.chart.error) {
                throw "Yahoo chart error: $($payload.chart.error.code) $($payload.chart.error.description)"
            }
            if (@($payload.chart.result).Count -eq 0) {
                throw 'Yahoo chart returned no result object'
            }
            return $payload.chart.result[0]
        }
        catch {
            $lastError = $_.Exception.Message
            if ($attempt -lt 4) {
                Start-Sleep -Milliseconds (350 * $attempt)
            }
        }
    }
    throw $lastError
}

function Get-FormalUniverse {
    param([string]$Directory)

    $formalFiles = @(Get-ChildItem -LiteralPath $Directory -File -Filter '*.md' |
        Where-Object { $_.Name -match '^F\d{2}_.+_量化评分_(\d{4}-\d{2}-\d{2})\.md$' } |
        Sort-Object Name)
    if ($formalFiles.Count -eq 0) {
        throw "No formal score files found in $Directory"
    }

    $records = @{}
    foreach ($file in $formalFiles) {
        if ($file.Name -notmatch '^F\d{2}_.+_量化评分_(\d{4}-\d{2}-\d{2})\.md$') { continue }
        $resultDate = $Matches[1]
        $seenThisFile = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
        foreach ($line in Get-Content -LiteralPath $file.FullName -Encoding utf8) {
            if ($line -notmatch '^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|') { continue }
            $ticker = $Matches[2].Trim().ToUpperInvariant()
            $name = $Matches[3].Trim()
            $category = $Matches[4].Trim()
            if (-not $seenThisFile.Add($ticker)) { continue }
            if (-not $records.ContainsKey($ticker)) {
                $records[$ticker] = [ordered]@{
                    Ticker = $ticker
                    Names = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
                    Categories = [System.Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
                    FileDates = [System.Collections.Generic.List[string]]::new()
                    LastWrites = [System.Collections.Generic.List[datetime]]::new()
                    Files = [System.Collections.Generic.List[string]]::new()
                }
            }
            $rec = $records[$ticker]
            $null = $rec['Names'].Add($name)
            $null = $rec['Categories'].Add($category)
            $rec['FileDates'].Add($resultDate)
            $rec['LastWrites'].Add($file.LastWriteTime)
            $rec['Files'].Add($file.Name)
        }
    }

    # A real ticker is KEYS, so do not use $records.Keys: PowerShell's adapted
    # hashtable member lookup would resolve that as the value stored under KEYS.
    $recordKeys = @($records.GetEnumerator() | ForEach-Object { $_.Key } | Sort-Object)
    $universe = foreach ($ticker in $recordKeys) {
        $rec = $records[$ticker]
        $dates = @($rec['FileDates'] | Sort-Object)
        $writes = @($rec['LastWrites'] | Sort-Object)
        [pscustomobject]@{
            feature_ticker = $ticker
            company_name = (@($rec['Names']) | Sort-Object) -join ' / '
            category = (@($rec['Categories']) | Sort-Object) -join ' / '
            formal_result_file_count = $rec['Files'].Count
            total_formal_result_files = $formalFiles.Count
            first_result_file_date = $dates[0]
            last_result_file_date = $dates[-1]
            earliest_result_lastwrite_local = $writes[0].ToString('yyyy-MM-ddTHH:mm:sszzz')
            latest_result_lastwrite_local = $writes[-1].ToString('yyyy-MM-ddTHH:mm:sszzz')
            present_in_all_formal_results = [int]($rec['Files'].Count -eq $formalFiles.Count)
        }
    }
    return [pscustomobject]@{ Files = $formalFiles; Universe = @($universe) }
}

function Get-EventObjects {
    param(
        $Result,
        [string]$EventName
    )
    $eventsProperty = $Result.PSObject.Properties['events']
    if ($null -eq $eventsProperty -or $null -eq $eventsProperty.Value) { return @() }
    $property = $eventsProperty.Value.PSObject.Properties[$EventName]
    if ($null -eq $property -or $null -eq $property.Value) { return @() }
    return @($property.Value.PSObject.Properties | ForEach-Object { $_.Value })
}

function Convert-YahooResult {
    param(
        [string]$FeatureTicker,
        [string]$YahooSymbol,
        [string]$Kind,
        [string]$SourceUrl,
        $Result,
        [datetime]$SignalDate,
        [datetime]$AsOfDate
    )

    $timestamps = @($Result.timestamp)
    $quote = $Result.indicators.quote[0]
    $adjBlock = $Result.indicators.adjclose[0]
    $opens = @($quote.open)
    $highs = @($quote.high)
    $lows = @($quote.low)
    $closes = @($quote.close)
    $volumes = @($quote.volume)
    $adjCloses = @($adjBlock.adjclose)

    $splitEvents = @(Get-EventObjects -Result $Result -EventName 'splits')
    $dividendEvents = @(Get-EventObjects -Result $Result -EventName 'dividends')
    $capitalGainEvents = @(Get-EventObjects -Result $Result -EventName 'capitalGains')
    $splitByDate = @{}
    $dividendByDate = @{}
    $capitalGainByDate = @{}
    foreach ($event in $splitEvents) {
        $date = Get-IsoDateFromEpoch -Epoch ([long]$event.date)
        $ratio = if ($event.splitRatio) { [string]$event.splitRatio } else { "$($event.numerator):$($event.denominator)" }
        $splitByDate[$date] = $ratio
    }
    foreach ($event in $dividendEvents) {
        $date = Get-IsoDateFromEpoch -Epoch ([long]$event.date)
        $dividendByDate[$date] = [double]$event.amount
    }
    foreach ($event in $capitalGainEvents) {
        $date = Get-IsoDateFromEpoch -Epoch ([long]$event.date)
        $capitalGainByDate[$date] = [double]$event.amount
    }

    $daily = [System.Collections.Generic.List[object]]::new()
    for ($i = 0; $i -lt $timestamps.Count; $i++) {
        if ($null -eq $closes[$i] -or $null -eq $adjCloses[$i]) { continue }
        $date = Get-IsoDateFromEpoch -Epoch ([long]$timestamps[$i]
        )
        $close = [double]$closes[$i]
        $adjClose = [double]$adjCloses[$i]
        $factor = if ($close -ne 0) { $adjClose / $close } else { [double]::NaN }
        $open = if ($i -lt $opens.Count -and $null -ne $opens[$i]) { [double]$opens[$i] } else { [double]::NaN }
        $high = if ($i -lt $highs.Count -and $null -ne $highs[$i]) { [double]$highs[$i] } else { [double]::NaN }
        $low = if ($i -lt $lows.Count -and $null -ne $lows[$i]) { [double]$lows[$i] } else { [double]::NaN }
        $volume = if ($i -lt $volumes.Count -and $null -ne $volumes[$i]) { [long]$volumes[$i] } else { $null }
        $daily.Add([pscustomobject]@{
            kind = $Kind
            feature_ticker = $FeatureTicker
            yahoo_symbol = $YahooSymbol
            date = $date
            open_split_adjusted = if ([double]::IsNaN($open)) { $null } else { [math]::Round($open, 8) }
            adjusted_open_total_return_basis = if ([double]::IsNaN($open) -or [double]::IsNaN($factor)) { $null } else { [math]::Round($open * $factor, 8) }
            high_split_adjusted = if ([double]::IsNaN($high)) { $null } else { [math]::Round($high, 8) }
            low_split_adjusted = if ([double]::IsNaN($low)) { $null } else { [math]::Round($low, 8) }
            close_split_adjusted_ex_distributions = [math]::Round($close, 8)
            adjusted_close_total_return_basis = [math]::Round($adjClose, 8)
            adjustment_factor = [math]::Round($factor, 10)
            volume = $volume
            dividend_cash = if ($dividendByDate.ContainsKey($date)) { $dividendByDate[$date] } else { 0 }
            capital_gain_cash = if ($capitalGainByDate.ContainsKey($date)) { $capitalGainByDate[$date] } else { 0 }
            split_ratio = if ($splitByDate.ContainsKey($date)) { $splitByDate[$date] } else { '' }
            source_url = $SourceUrl
        })
    }

    $window = @($daily | Where-Object { $_.date -ge $SignalDate.ToString('yyyy-MM-dd') -and $_.date -le $AsOfDate.ToString('yyyy-MM-dd') } | Sort-Object date)
    if ($window.Count -eq 0) {
        throw 'No valid daily prices in requested return window'
    }
    $entry = $window[0]
    $exit = $window[-1]
    if ($null -eq $entry.adjusted_open_total_return_basis) {
        throw "Missing opening price on entry date $($entry.date)"
    }

    $primaryReturn = [double]$exit.adjusted_close_total_return_basis / [double]$entry.adjusted_open_total_return_basis - 1
    $closeReturn = [double]$exit.adjusted_close_total_return_basis / [double]$entry.adjusted_close_total_return_basis - 1
    $closeExDistribution = [double]$exit.close_split_adjusted_ex_distributions / [double]$entry.close_split_adjusted_ex_distributions - 1

    $maxAbsClose = 0.0
    $maxAbsAdj = 0.0
    for ($i = 1; $i -lt $window.Count; $i++) {
        $rClose = [double]$window[$i].close_split_adjusted_ex_distributions / [double]$window[$i - 1].close_split_adjusted_ex_distributions - 1
        $rAdj = [double]$window[$i].adjusted_close_total_return_basis / [double]$window[$i - 1].adjusted_close_total_return_basis - 1
        $maxAbsClose = [math]::Max($maxAbsClose, [math]::Abs($rClose))
        $maxAbsAdj = [math]::Max($maxAbsAdj, [math]::Abs($rAdj))
    }

    $windowSplits = @($splitEvents | Where-Object {
        $d = Get-IsoDateFromEpoch -Epoch ([long]$_.date)
        $d -ge $entry.date -and $d -le $exit.date
    })
    $windowDividends = @($dividendEvents | Where-Object {
        $d = Get-IsoDateFromEpoch -Epoch ([long]$_.date)
        $d -ge $entry.date -and $d -le $exit.date
    })
    $windowCapitalGains = @($capitalGainEvents | Where-Object {
        $d = Get-IsoDateFromEpoch -Epoch ([long]$_.date)
        $d -ge $entry.date -and $d -le $exit.date
    })

    $splitDetails = @($windowSplits | ForEach-Object {
        $ratio = if ($_.splitRatio) { [string]$_.splitRatio } else { "$($_.numerator):$($_.denominator)" }
        "$(Get-IsoDateFromEpoch -Epoch ([long]$_.date)) $ratio"
    }) -join '; '
    $dividendDetails = @($windowDividends | ForEach-Object {
        "$(Get-IsoDateFromEpoch -Epoch ([long]$_.date)) $([double]$_.amount)"
    }) -join '; '
    $capitalGainDetails = @($windowCapitalGains | ForEach-Object {
        "$(Get-IsoDateFromEpoch -Epoch ([long]$_.date)) $([double]$_.amount)"
    }) -join '; '

    $meta = $Result.meta
    $longNameProperty = $meta.PSObject.Properties['longName']
    $shortNameProperty = $meta.PSObject.Properties['shortName']
    $resolvedLongName = if ($null -ne $longNameProperty -and $longNameProperty.Value) {
        [string]$longNameProperty.Value
    } elseif ($null -ne $shortNameProperty -and $shortNameProperty.Value) {
        [string]$shortNameProperty.Value
    } else { '' }
    $summary = [pscustomobject]@{
        feature_ticker = $FeatureTicker
        yahoo_symbol = $YahooSymbol
        yahoo_long_name = $resolvedLongName
        instrument_type = [string]$meta.instrumentType
        exchange = [string]$meta.exchangeName
        full_exchange_name = [string]$meta.fullExchangeName
        currency = [string]$meta.currency
        exchange_timezone = [string]$meta.exchangeTimezoneName
        requested_signal_date = $SignalDate.ToString('yyyy-MM-dd')
        entry_trading_date = $entry.date
        entry_open_split_adjusted = $entry.open_split_adjusted
        entry_adjusted_open = $entry.adjusted_open_total_return_basis
        entry_close_split_adjusted_ex_distributions = $entry.close_split_adjusted_ex_distributions
        entry_adjusted_close = $entry.adjusted_close_total_return_basis
        latest_available_date = $exit.date
        latest_close_split_adjusted_ex_distributions = $exit.close_split_adjusted_ex_distributions
        latest_adjusted_close = $exit.adjusted_close_total_return_basis
        primary_adj_open_to_adj_close_return = $primaryReturn
        auxiliary_adj_close_to_adj_close_return = $closeReturn
        close_to_close_ex_distributions_return = $closeExDistribution
        dividend_effect_pp = ($closeReturn - $closeExDistribution) * 100
        observation_count = $window.Count
        entry_delay_calendar_days = ([datetime]$entry.date - $SignalDate.Date).Days
        latest_lag_calendar_days = ($AsOfDate.Date - [datetime]$exit.date).Days
        split_event_count = $windowSplits.Count
        split_details = $splitDetails
        dividend_event_count = $windowDividends.Count
        dividend_details = $dividendDetails
        capital_gain_event_count = $windowCapitalGains.Count
        capital_gain_details = $capitalGainDetails
        max_abs_daily_close_return = $maxAbsClose
        max_abs_daily_adj_return = $maxAbsAdj
        source_url = $SourceUrl
        adjusted_close_method_url = $YahooAdjustedCloseHelp
    }
    return [pscustomobject]@{ Summary = $summary; Daily = @($daily) }
}

function Get-Median {
    param([double[]]$Values)
    $sorted = @($Values | Sort-Object)
    if ($sorted.Count -eq 0) { return $null }
    $mid = [math]::Floor($sorted.Count / 2)
    if ($sorted.Count % 2 -eq 1) { return [double]$sorted[$mid] }
    return ([double]$sorted[$mid - 1] + [double]$sorted[$mid]) / 2
}

$universeResult = Get-FormalUniverse -Directory $ScoreDir
$universe = @($universeResult.Universe)
$universe | Export-Csv -LiteralPath (Join-Path $OutputDir 'universe_audit.csv') -NoTypeInformation -Encoding utf8BOM

$signalDates = @($universe.first_result_file_date | Sort-Object -Unique)
if ($signalDates.Count -ne 1) {
    throw "Expected one common formal result date, found: $($signalDates -join ', ')"
}
$SignalDate = [datetime]$signalDates[0]
$DownloadStart = $SignalDate.AddDays(-5)
$DownloadEndExclusive = $AsOfDate.Date.AddDays(1)

$downloads = @{}
$downloadErrors = [System.Collections.Generic.List[object]]::new()
$dailyRows = [System.Collections.Generic.List[object]]::new()
$symbolsToDownload = @($Benchmarks + $universe.feature_ticker)

foreach ($featureTicker in $symbolsToDownload) {
    $kind = if ($featureTicker -in $Benchmarks) { 'benchmark' } else { 'company' }
    $map = if ($TickerMap.ContainsKey($featureTicker)) { $TickerMap[$featureTicker] } else { $null }
    $yahooSymbol = if ($null -ne $map) { $map.YahooSymbol } else { $featureTicker }
    $url = Get-YahooChartUrl -Symbol $yahooSymbol -StartDate $DownloadStart -EndDateExclusive $DownloadEndExclusive
    try {
        $result = Invoke-YahooChart -Url $url
        $converted = Convert-YahooResult -FeatureTicker $featureTicker -YahooSymbol $yahooSymbol -Kind $kind -SourceUrl $url -Result $result -SignalDate $SignalDate -AsOfDate $AsOfDate
        $downloads[$featureTicker] = $converted.Summary
        foreach ($row in $converted.Daily) { $dailyRows.Add($row) }
    }
    catch {
        $downloadErrors.Add([pscustomobject]@{
            feature_ticker = $featureTicker
            yahoo_symbol_used = $yahooSymbol
            status = 'download_or_window_failure'
            default_effectiveness_sample_include = 0
            reason = $_.Exception.Message
            split_details = ''
            ticker_change_note = if ($null -ne $map) { $map.Note } else { '' }
            source_url = $url
            documentation_url = if ($null -ne $map) { $map.Source } else { '' }
        })
    }
    if ($PauseMilliseconds -gt 0) { Start-Sleep -Milliseconds $PauseMilliseconds }
}

$benchmarkRows = foreach ($ticker in $Benchmarks) {
    if (-not $downloads.ContainsKey($ticker)) { continue }
    $s = $downloads[$ticker]
    [pscustomobject]@{
        benchmark = $ticker
        yahoo_symbol = $s.yahoo_symbol
        entry_trading_date = $s.entry_trading_date
        entry_adjusted_open = $s.entry_adjusted_open
        entry_adjusted_close = $s.entry_adjusted_close
        latest_available_date = $s.latest_available_date
        latest_adjusted_close = $s.latest_adjusted_close
        primary_adj_open_to_adj_close_return = [math]::Round([double]$s.primary_adj_open_to_adj_close_return, 10)
        auxiliary_adj_close_to_adj_close_return = [math]::Round([double]$s.auxiliary_adj_close_to_adj_close_return, 10)
        split_event_count = $s.split_event_count
        split_details = $s.split_details
        dividend_event_count = $s.dividend_event_count
        dividend_details = $s.dividend_details
        source_url = $s.source_url
    }
}

$spyPrimary = if ($downloads.ContainsKey('SPY')) { [double]$downloads['SPY'].primary_adj_open_to_adj_close_return } else { $null }
$qqqPrimary = if ($downloads.ContainsKey('QQQ')) { [double]$downloads['QQQ'].primary_adj_open_to_adj_close_return } else { $null }
$soxxPrimary = if ($downloads.ContainsKey('SOXX')) { [double]$downloads['SOXX'].primary_adj_open_to_adj_close_return } else { $null }
$spyAux = if ($downloads.ContainsKey('SPY')) { [double]$downloads['SPY'].auxiliary_adj_close_to_adj_close_return } else { $null }
$qqqAux = if ($downloads.ContainsKey('QQQ')) { [double]$downloads['QQQ'].auxiliary_adj_close_to_adj_close_return } else { $null }
$soxxAux = if ($downloads.ContainsKey('SOXX')) { [double]$downloads['SOXX'].auxiliary_adj_close_to_adj_close_return } else { $null }
$benchmarkLatest = @($benchmarkRows.latest_available_date | Sort-Object -Descending | Select-Object -First 1)[0]

$companyRows = [System.Collections.Generic.List[object]]::new()
$qualityIssues = [System.Collections.Generic.List[object]]::new()
foreach ($u in $universe) {
    $ticker = $u.feature_ticker
    if (-not $downloads.ContainsKey($ticker)) { continue }
    $s = $downloads[$ticker]
    $map = if ($TickerMap.ContainsKey($ticker)) { $TickerMap[$ticker] } else { $null }
    $isOtc = $s.full_exchange_name -match 'OTC|Pink' -or $s.exchange -match 'PNK|OQX|OQB|OTC'
    $isStale = $s.latest_available_date -lt $benchmarkLatest
    $entryDelayed = [int]$s.entry_delay_calendar_days -gt 0
    $largeGap = [double]$s.max_abs_daily_adj_return -gt 0.50
    $status = if ($isStale) { 'stale_quote_exclude' } elseif ($entryDelayed) { 'late_entry_review' } elseif ($largeGap) { 'large_move_review' } elseif ($null -ne $map) { 'ok_ticker_changed' } else { 'ok' }
    $defaultInclude = [int](-not $isStale -and -not $entryDelayed -and -not $largeGap)
    $listingClass = if ($isOtc) { 'OTC quote; often ADR/foreign ordinary proxy' } elseif ($s.full_exchange_name -match 'Nasdaq|NYSE') { 'US exchange listed' } else { 'other exchange metadata' }

    $row = [pscustomobject]@{
        feature_ticker = $ticker
        yahoo_symbol_used = $s.yahoo_symbol
        company_name_from_results = $u.company_name
        yahoo_long_name = $s.yahoo_long_name
        category = $u.category
        formal_result_file_count = $u.formal_result_file_count
        first_result_file_date = $u.first_result_file_date
        earliest_result_lastwrite_local = $u.earliest_result_lastwrite_local
        latest_result_lastwrite_local = $u.latest_result_lastwrite_local
        status = $status
        default_effectiveness_sample_include = $defaultInclude
        ticker_change_note = if ($null -ne $map) { $map.Note } else { '' }
        ticker_change_source = if ($null -ne $map) { $map.Source } else { '' }
        instrument_type = $s.instrument_type
        exchange = $s.exchange
        full_exchange_name = $s.full_exchange_name
        listing_class = $listingClass
        currency = $s.currency
        requested_signal_date = $s.requested_signal_date
        entry_trading_date = $s.entry_trading_date
        entry_open_split_adjusted = $s.entry_open_split_adjusted
        entry_adjusted_open = $s.entry_adjusted_open
        entry_close_split_adjusted_ex_distributions = $s.entry_close_split_adjusted_ex_distributions
        entry_adjusted_close = $s.entry_adjusted_close
        latest_available_date = $s.latest_available_date
        latest_close_split_adjusted_ex_distributions = $s.latest_close_split_adjusted_ex_distributions
        latest_adjusted_close = $s.latest_adjusted_close
        primary_adj_open_to_adj_close_return = [math]::Round([double]$s.primary_adj_open_to_adj_close_return, 10)
        auxiliary_adj_close_to_adj_close_return = [math]::Round([double]$s.auxiliary_adj_close_to_adj_close_return, 10)
        close_to_close_ex_distributions_return = [math]::Round([double]$s.close_to_close_ex_distributions_return, 10)
        primary_excess_spy = if ($null -eq $spyPrimary) { $null } else { [math]::Round([double]$s.primary_adj_open_to_adj_close_return - $spyPrimary, 10) }
        primary_excess_qqq = if ($null -eq $qqqPrimary) { $null } else { [math]::Round([double]$s.primary_adj_open_to_adj_close_return - $qqqPrimary, 10) }
        primary_excess_soxx = if ($null -eq $soxxPrimary) { $null } else { [math]::Round([double]$s.primary_adj_open_to_adj_close_return - $soxxPrimary, 10) }
        auxiliary_excess_spy = if ($null -eq $spyAux) { $null } else { [math]::Round([double]$s.auxiliary_adj_close_to_adj_close_return - $spyAux, 10) }
        auxiliary_excess_qqq = if ($null -eq $qqqAux) { $null } else { [math]::Round([double]$s.auxiliary_adj_close_to_adj_close_return - $qqqAux, 10) }
        auxiliary_excess_soxx = if ($null -eq $soxxAux) { $null } else { [math]::Round([double]$s.auxiliary_adj_close_to_adj_close_return - $soxxAux, 10) }
        split_event_count = $s.split_event_count
        split_details = $s.split_details
        dividend_event_count = $s.dividend_event_count
        dividend_details = $s.dividend_details
        capital_gain_event_count = $s.capital_gain_event_count
        capital_gain_details = $s.capital_gain_details
        dividend_effect_pp = [math]::Round([double]$s.dividend_effect_pp, 6)
        observation_count = $s.observation_count
        entry_delay_calendar_days = $s.entry_delay_calendar_days
        latest_lag_calendar_days = $s.latest_lag_calendar_days
        max_abs_daily_adj_return = [math]::Round([double]$s.max_abs_daily_adj_return, 10)
        source_url = $s.source_url
        adjusted_close_method_url = $s.adjusted_close_method_url
    }
    $companyRows.Add($row)

    if ($status -ne 'ok') {
        $reason = switch ($status) {
            'ok_ticker_changed' { 'Documented ticker change; corrected symbol used. Old-symbol series must not be used.' }
            'stale_quote_exclude' { "Latest quote $($s.latest_available_date) trails benchmark latest $benchmarkLatest" }
            'late_entry_review' { "No quote on signal date; first quote $($s.entry_trading_date)" }
            'large_move_review' { "Maximum absolute adjusted daily return exceeded 50%: $([math]::Round(100 * [double]$s.max_abs_daily_adj_return, 2))%" }
            default { $status }
        }
        $qualityIssues.Add([pscustomobject]@{
            feature_ticker = $ticker
            yahoo_symbol_used = $s.yahoo_symbol
            status = $status
            default_effectiveness_sample_include = $defaultInclude
            reason = $reason
            split_details = $s.split_details
            ticker_change_note = if ($null -ne $map) { $map.Note } else { '' }
            source_url = $s.source_url
            documentation_url = if ($null -ne $map) { $map.Source } else { '' }
        })
    }
}

foreach ($e in $downloadErrors) { $qualityIssues.Add($e) }

$companyRows = @($companyRows | Sort-Object feature_ticker)
$benchmarkRows = @($benchmarkRows | Sort-Object benchmark)
$companyRows | Export-Csv -LiteralPath (Join-Path $OutputDir 'company_returns_2026-06-04_to_latest.csv') -NoTypeInformation -Encoding utf8BOM
$benchmarkRows | Export-Csv -LiteralPath (Join-Path $OutputDir 'benchmark_returns_2026-06-04_to_latest.csv') -NoTypeInformation -Encoding utf8BOM
$dailyRows | Sort-Object kind, feature_ticker, date | Export-Csv -LiteralPath (Join-Path $OutputDir 'price_history_daily.csv') -NoTypeInformation -Encoding utf8BOM
$qualityIssues | Export-Csv -LiteralPath (Join-Path $OutputDir 'data_quality_issues.csv') -NoTypeInformation -Encoding utf8BOM

$splitRows = @($companyRows | Where-Object { [int]$_.split_event_count -gt 0 } | Select-Object feature_ticker, yahoo_symbol_used, company_name_from_results, split_event_count, split_details, primary_adj_open_to_adj_close_return, auxiliary_adj_close_to_adj_close_return, max_abs_daily_adj_return, status, source_url)
$splitRows | Export-Csv -LiteralPath (Join-Path $OutputDir 'split_action_checks.csv') -NoTypeInformation -Encoding utf8BOM

$included = @($companyRows | Where-Object { [int]$_.default_effectiveness_sample_include -eq 1 })
$primaryValues = [double[]]@($included.primary_adj_open_to_adj_close_return)
$auxValues = [double[]]@($included.auxiliary_adj_close_to_adj_close_return)
$winners = @($included | Sort-Object primary_adj_open_to_adj_close_return -Descending)
$losers = @($included | Sort-Object primary_adj_open_to_adj_close_return)
$summary = [System.Collections.Generic.List[object]]::new()
function Add-Summary([string]$Metric, $Value, [string]$Note = '') {
    $summary.Add([pscustomobject]@{ metric = $Metric; value = $Value; note = $Note })
}
Add-Summary 'formal_result_file_count' $universeResult.Files.Count 'Formal files only; backups excluded'
Add-Summary 'universe_company_count' $universe.Count 'Unique tickers parsed across all formal results'
Add-Summary 'downloaded_company_count' $companyRows.Count ''
Add-Summary 'default_included_company_count' $included.Count 'Excludes failures, stale quotes, late entries, and >50% one-day adjusted-price anomalies'
Add-Summary 'quality_issue_count' $qualityIssues.Count 'Ticker changes are recorded as issues but may remain included after correction'
Add-Summary 'signal_date' $SignalDate.ToString('yyyy-MM-dd') 'All formal result files were written before the 2026-06-04 US market open'
Add-Summary 'latest_benchmark_date' $benchmarkLatest ''
Add-Summary 'primary_mean_return' ([math]::Round(($primaryValues | Measure-Object -Average).Average, 10)) 'Adjusted 2026-06-04 open to latest adjusted close'
Add-Summary 'primary_median_return' ([math]::Round((Get-Median $primaryValues), 10)) ''
Add-Summary 'primary_positive_rate' ([math]::Round((@($primaryValues | Where-Object { $_ -gt 0 }).Count / $primaryValues.Count), 10)) ''
Add-Summary 'auxiliary_mean_return' ([math]::Round(($auxValues | Measure-Object -Average).Average, 10)) 'Adjusted 2026-06-04 close to latest adjusted close'
Add-Summary 'auxiliary_median_return' ([math]::Round((Get-Median $auxValues), 10)) ''
Add-Summary 'primary_best_ticker' $winners[0].feature_ticker ''
Add-Summary 'primary_best_return' $winners[0].primary_adj_open_to_adj_close_return ''
Add-Summary 'primary_worst_ticker' $losers[0].feature_ticker ''
Add-Summary 'primary_worst_return' $losers[0].primary_adj_open_to_adj_close_return ''
foreach ($b in $benchmarkRows) {
    Add-Summary "$($b.benchmark)_primary_return" $b.primary_adj_open_to_adj_close_return ''
    Add-Summary "$($b.benchmark)_auxiliary_return" $b.auxiliary_adj_close_to_adj_close_return ''
}
Add-Summary 'split_affected_company_count' $splitRows.Count 'Yahoo split events in the measured window; adjusted series used'
Add-Summary 'otc_quote_count' @($companyRows | Where-Object { $_.listing_class -like 'OTC*' }).Count 'Returns use the US OTC quote and its stated currency'
Add-Summary 'methodology_source' $YahooAdjustedCloseHelp 'Yahoo says adjusted close reflects splits and dividend distributions'
$summary | Export-Csv -LiteralPath (Join-Path $OutputDir 'return_run_summary.csv') -NoTypeInformation -Encoding utf8BOM

Write-Host "Formal files: $($universeResult.Files.Count)"
Write-Host "Universe: $($universe.Count); downloaded: $($companyRows.Count); default included: $($included.Count)"
Write-Host "Signal date: $($SignalDate.ToString('yyyy-MM-dd')); latest benchmark date: $benchmarkLatest"
Write-Host "Primary median: $([math]::Round(100 * (Get-Median $primaryValues), 2))%; mean: $([math]::Round(100 * ($primaryValues | Measure-Object -Average).Average, 2))%"
Write-Host "Splits in window: $($splitRows.Count); quality issues: $($qualityIssues.Count)"
Write-Host "Output: $OutputDir"

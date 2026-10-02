#requires -Version 7.0
<#
Save the current project state to GitHub. Run from any working directory.
Exit codes: 0 = synchronized; 1 = failed; 2 = uploaded, but local changes remain.
#>
param([string]$Message = ("Update investment workspace {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz')))

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$projectRoot = Split-Path -Parent $PSScriptRoot
$updateLock = $null
$exitCode = 0

function Invoke-ProjectGit([string[]]$Arguments) {
    $output = @(& git -C $projectRoot @Arguments)
    if ($LASTEXITCODE -ne 0) {
        throw "Git failed (exit $LASTEXITCODE): git $($Arguments -join ' ')"
    }
    $output
}

try {
    # These overrides could redirect Git away from this project or its normal index.
    foreach ($name in @('GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE', 'GIT_COMMON_DIR')) {
        if ([Environment]::GetEnvironmentVariable($name)) { throw "Unset $name before running this script." }
    }
    $actualRoot = (Invoke-ProjectGit @('rev-parse', '--show-toplevel')) -join ''
    if ([IO.Path]::GetFullPath($actualRoot) -ne [IO.Path]::GetFullPath($projectRoot)) {
        throw 'The script must be inside the Investment repository tools directory.'
    }
    $remote = (Invoke-ProjectGit @('remote', 'get-url', '--push', 'origin')) -join ''
    if ($remote -notin @('https://github.com/chenyan159/investment.git', 'git@github.com:chenyan159/investment.git')) {
        throw 'Origin does not point to chenyan159/investment. No changes were staged.'
    }
    $branch = (Invoke-ProjectGit @('symbolic-ref', '--quiet', '--short', 'HEAD')) -join ''
    if ($branch -ne 'main') { throw 'Switch to main deliberately before using this script.' }
    $gitDirectory = (Invoke-ProjectGit @('rev-parse', '--absolute-git-dir')) -join ''
    $updateLock = [IO.File]::Open(
        (Join-Path $gitDirectory 'github-update.lock'),
        [IO.FileMode]::OpenOrCreate, [IO.FileAccess]::ReadWrite, [IO.FileShare]::None
    )
    foreach ($marker in @('index.lock', 'HEAD.lock', 'MERGE_HEAD', 'CHERRY_PICK_HEAD', 'REVERT_HEAD', 'rebase-merge', 'rebase-apply', 'BISECT_START')) {
        if (Test-Path -LiteralPath (Join-Path $gitDirectory $marker)) {
            throw "Another Git operation needs attention ($marker). Retry after it finishes."
        }
    }

    Write-Host "Project: $projectRoot"
    Invoke-ProjectGit @('add', '--all', '--', '.')
    $gitlinks = @(Invoke-ProjectGit @('ls-files', '--stage') | Where-Object { $_ -match '^160000 ' })
    if ($gitlinks.Count) { throw 'An embedded repository would be recorded as a gitlink. Review the staged changes first.' }
    $staged = @(Invoke-ProjectGit @('diff', '--cached', '--name-only'))
    if ($staged.Count) {
        Invoke-ProjectGit @('diff', '--cached', '--shortstat') | ForEach-Object { Write-Host $_ }
        Invoke-ProjectGit @('commit', '--quiet', '-m', $Message)
        Write-Host "Committed $($staged.Count) changed paths."
    } else {
        Write-Host 'No new file changes to commit.'
    }

    # Always push: an earlier attempt may have committed successfully while offline.
    # A normal, non-forced push refuses to overwrite divergent remote history.
    Invoke-ProjectGit @('push', 'origin', 'HEAD:refs/heads/main') | ForEach-Object { Write-Host $_ }
    $localHead = (Invoke-ProjectGit @('rev-parse', 'HEAD')) -join ''
    $remoteLines = @(Invoke-ProjectGit @('ls-remote', '--exit-code', $remote, 'refs/heads/main'))
    if ($remoteLines.Count -ne 1 -or ($remoteLines[0] -split '\s+')[0] -ne $localHead) {
        throw 'The remote commit could not be confirmed equal to local HEAD. Retry to verify.'
    }
    $remaining = @(Invoke-ProjectGit @('status', '--porcelain=v1', '--untracked-files=all'))
    $finalHead = (Invoke-ProjectGit @('rev-parse', 'HEAD')) -join ''
    if ($remaining.Count -or $finalHead -ne $localHead) {
        Write-Warning "Uploaded $localHead, but local files or commits changed during the update ($($remaining.Count) pending paths). Run again after other writers finish."
        $exitCode = 2
    } else {
        Write-Host "SUCCESS: GitHub main matches the current project state (excluding ignored files). Commit: $localHead"
    }
} catch {
    Write-Host "UPDATE FAILED: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host 'Existing files and local commits are retained. Resolve the reported issue and run again; no automatic pull, reset or force push is performed.'
    $exitCode = 1
} finally {
    if ($null -ne $updateLock) { $updateLock.Dispose() }
}
exit $exitCode

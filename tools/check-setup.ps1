# Read-only setup audit for the Jewelry Studio workshop.
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1
#   powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1 -StudioRoot 'C:\JewelryStudio'

[CmdletBinding()]
param(
    [string]$StudioRoot = 'D:\JewelryStudio',
    [string]$RepoRoot = '',
    [int]$Port = 9876,
    [string]$OpenCodeConfig = "$env:USERPROFILE\.config\opencode\opencode.json"
)

$ErrorActionPreference = 'Continue'

if (-not $RepoRoot) {
    if ($PSScriptRoot) {
        $RepoRoot = Split-Path -Parent $PSScriptRoot
    } elseif ($MyInvocation.MyCommand.Path) {
        $RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    } else {
        $RepoRoot = (Get-Location).Path
    }
}

$script:FailCount = 0
$script:WarnCount = 0

function Add-Result {
    param(
        [ValidateSet('PASS', 'WARN', 'FAIL', 'INFO')]
        [string]$Status,
        [string]$Message
    )
    $color = 'Green'
    if ($Status -eq 'WARN') { $color = 'Yellow'; $script:WarnCount++ }
    if ($Status -eq 'FAIL') { $color = 'Red'; $script:FailCount++ }
    if ($Status -eq 'INFO') { $color = 'Gray' }
    Write-Host ("{0,-4}  {1}" -f $Status, $Message) -ForegroundColor $color
}

Write-Host ''
Write-Host 'Jewelry Studio setup audit' -ForegroundColor Cyan
Write-Host "Studio root: $StudioRoot"
Write-Host "Repository:  $RepoRoot"
Write-Host ''

# --- OS -------------------------------------------------------------------
try {
    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction Stop
    $is64 = [Environment]::Is64BitOperatingSystem
    $caption = $os.Caption
    if (-not $is64) {
        Add-Result FAIL "Operating system is not 64-bit ($caption)"
    } elseif ($caption -match 'Windows XP|Windows Vista|Windows 7') {
        Add-Result FAIL "Unsupported OS: $caption. This workflow needs Windows 10/11 64-bit."
    } elseif ($caption -match 'Windows 8') {
        Add-Result WARN "Windows 8.1 is below the tested minimum ($caption). Windows 10/11 64-bit is required for OpenCode."
    } elseif ($caption -match 'Windows 10|Windows 11') {
        Add-Result PASS "$caption (64-bit) ($($os.Version))"
    } else {
        Add-Result WARN "Unrecognised Windows version: $caption"
    }
} catch {
    Add-Result WARN "Could not read the Windows version: $($_.Exception.Message)"
}

# --- PowerShell -----------------------------------------------------------
$psVersion = $PSVersionTable.PSVersion
if ($psVersion.Major -ge 5) {
    Add-Result PASS "PowerShell $psVersion"
} else {
    Add-Result FAIL "PowerShell $psVersion is too old; use Windows PowerShell 5.1 or PowerShell 7+"
}

# --- Git ------------------------------------------------------------------
$git = Get-Command git -ErrorAction SilentlyContinue
if ($git) {
    try {
        $gitVersion = (& git --version 2>&1 | Select-Object -First 1)
        Add-Result PASS "$gitVersion"
    } catch {
        Add-Result WARN "git found but could not run: $($_.Exception.Message)"
    }
} else {
    Add-Result WARN 'Git not found on PATH. Needed to clone the repository; download the ZIP instead if you prefer.'
}

# --- uv / uvx -------------------------------------------------------------
$uvx = Get-Command uvx -ErrorAction SilentlyContinue
if ($uvx) {
    try {
        $uvxVersion = (& uvx --version 2>&1 | Select-Object -First 1)
        Add-Result PASS "$uvxVersion at $($uvx.Source)"
    } catch {
        Add-Result FAIL "uvx found at $($uvx.Source) but could not run: $($_.Exception.Message)"
    }
} else {
    Add-Result FAIL 'uvx not found on PATH. Install uv (winget install --id astral-sh.uv -e) and reopen PowerShell.'
}

# --- BLENDER_USER_RESOURCES ----------------------------------------------
$expectedResources = Join-Path $StudioRoot 'Blender-4.5-LTS\4.5'
if ($env:BLENDER_USER_RESOURCES) {
    $actualResources = $env:BLENDER_USER_RESOURCES.TrimEnd('\')
    if ($actualResources -ieq $expectedResources.TrimEnd('\')) {
        Add-Result PASS "BLENDER_USER_RESOURCES points at the portable Blender"
    } else {
        Add-Result WARN "BLENDER_USER_RESOURCES is set to '$($env:BLENDER_USER_RESOURCES)' but the portable Blender expects '$expectedResources'. Blender may load another installation's addons."
    }
} else {
    Add-Result PASS 'BLENDER_USER_RESOURCES is not set (portable Blender will use its own folder)'
}

# --- Blender --------------------------------------------------------------
$blender = Join-Path $StudioRoot 'Blender-4.5-LTS\blender.exe'
if (Test-Path $blender) {
    try {
        $blenderVersion = (& $blender --version 2>&1 | Select-Object -First 1)
        if ($blenderVersion -match 'Blender 4\.5\.14') {
            Add-Result PASS "$blenderVersion at $blender"
        } elseif ($blenderVersion -match 'Blender 4\.5\.') {
            Add-Result WARN "$blenderVersion (pinned build is 4.5.14) at $blender"
        } elseif ($blenderVersion -match 'Blender ') {
            Add-Result WARN "$blenderVersion (expected Blender 4.5.x) at $blender"
        } else {
            Add-Result FAIL "Could not read the Blender version from $blender"
        }
    } catch {
        Add-Result FAIL "Blender found but could not run: $($_.Exception.Message)"
    }
} else {
    Add-Result FAIL "Blender not found at $blender"
}

# --- JewelCraft -----------------------------------------------------------
$jewelCraft = $null
$extensionsRoot = Join-Path $StudioRoot 'Blender-4.5-LTS\4.5\extensions'
if (Test-Path $extensionsRoot) {
    $jewelCraft = Get-ChildItem $extensionsRoot -Recurse -Filter blender_manifest.toml -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -match 'jewelcraft' } |
        Select-Object -First 1
}
if ($jewelCraft) {
    Add-Result PASS "JewelCraft manifest found: $($jewelCraft.FullName)"
} else {
    Add-Result FAIL "JewelCraft not found under $extensionsRoot. Install jewelcraft-3.0.1.zip as an extension."
}

# --- MCP addon ------------------------------------------------------------
$mcpExtension = Join-Path $StudioRoot 'Blender-4.5-LTS\4.5\extensions\user_default\blender_mcp\blender_manifest.toml'
$mcpLegacy = Join-Path $StudioRoot 'Blender-4.5-LTS\4.5\scripts\addons\blender_mcp.py'
if (Test-Path $mcpExtension) {
    Add-Result PASS "MCP addon extension found: $mcpExtension"
} elseif (Test-Path $mcpLegacy) {
    Add-Result FAIL "MCP addon is installed as a legacy .py file, which Blender 4.5 does not reliably load. Run tools\install-mcp-addon.ps1."
} else {
    Add-Result FAIL "MCP addon not found. Install it and run tools\install-mcp-addon.ps1."
}

# --- MCP port -------------------------------------------------------------
try {
    $portOpen = Test-NetConnection -ComputerName localhost -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue
    if ($portOpen) {
        Add-Result PASS "MCP port $Port is listening"
    } else {
        Add-Result WARN "MCP port $Port is not listening. Open Blender and click Start MCP Server."
    }
} catch {
    Add-Result WARN "Could not test port $Port`: $($_.Exception.Message)"
}

# --- OpenCode -------------------------------------------------------------
$opencode = Get-Command opencode -ErrorAction SilentlyContinue
if ($opencode) {
    try {
        $ocVersion = (& opencode --version 2>&1 | Select-Object -First 1)
        Add-Result PASS "OpenCode $ocVersion"
    } catch {
        Add-Result WARN "OpenCode found but could not run: $($_.Exception.Message)"
    }
} else {
    Add-Result WARN 'OpenCode not found on PATH. Install it and sign in before using the workshop.'
}

# --- OpenCode MCP config --------------------------------------------------
if (Test-Path $OpenCodeConfig) {
    try {
        $config = Get-Content $OpenCodeConfig -Raw | ConvertFrom-Json
        $entry = $null
        if ($config.PSObject.Properties.Name -contains 'mcp') {
            $entry = $config.mcp.blender
        }
        if ($null -eq $entry) {
            Add-Result FAIL "OpenCode config has no mcp.blender entry: $OpenCodeConfig"
        } else {
            if ($entry.enabled -ne $true) {
                Add-Result FAIL 'OpenCode mcp.blender entry is not enabled'
            } else {
                Add-Result PASS 'OpenCode config has an enabled blender entry'
            }
            $commandText = ($entry.command -join ' ')
            if ($commandText -match 'mcp-for-blender') {
                Add-Result PASS "OpenCode launches: $commandText"
            } else {
                Add-Result FAIL "OpenCode blender command does not mention mcp-for-blender: $commandText"
            }
            $firstCommand = ''
            if ($entry.command -is [System.Array]) {
                $firstCommand = [string]$entry.command[0]
            } else {
                $firstCommand = ([string]$entry.command).Split(' ')[0]
            }
            if ($firstCommand -match '[\\/]') {
                Add-Result PASS 'OpenCode uses an absolute uvx path (safe for GUI launches)'
            } else {
                Add-Result WARN 'OpenCode uses a bare uvx command. If you launch OpenCode from a GUI and see spawn uvx ENOENT, replace it with the full path.'
            }
            if ($entry.environment -and $entry.environment.BLENDER_MCP_SAFE_MODE -eq '1') {
                Add-Result PASS 'Safe mode is on'
            } else {
                Add-Result WARN 'BLENDER_MCP_SAFE_MODE is not 1 in the OpenCode config'
            }
        }
    } catch {
        Add-Result FAIL "Could not parse $OpenCodeConfig`: $($_.Exception.Message)"
    }
} else {
    Add-Result FAIL "OpenCode config not found: $OpenCodeConfig"
}

# --- Workshop files -------------------------------------------------------
$required = @(
    (Join-Path $RepoRoot 'templates\ring-template.blend'),
    (Join-Path $RepoRoot 'example-solitaire\ring.blend'),
    (Join-Path $RepoRoot 'example-solitaire\scripts\verify_scene.py'),
    (Join-Path $RepoRoot 'example-solitaire\reference\target.jpg')
)
$missing = @()
foreach ($path in $required) {
    if (-not (Test-Path $path)) { $missing += $path }
}
if ($missing.Count -eq 0) {
    Add-Result PASS 'Workshop template, example, scripts, and reference image are present'
} else {
    Add-Result WARN ("Missing workshop files: " + ($missing -join ', '))
}

$projects = Join-Path $RepoRoot 'projects'
if (Test-Path $projects) {
    Add-Result PASS "Local projects folder exists: $projects"
} else {
    Add-Result WARN "Local projects folder is missing: $projects"
}

# --- Summary --------------------------------------------------------------
Write-Host ''
if ($script:FailCount -eq 0) {
    Write-Host "RESULT: PASS ($script:WarnCount warning(s))" -ForegroundColor Green
    exit 0
} else {
    Write-Host "RESULT: $script:FailCount failure(s), $script:WarnCount warning(s)" -ForegroundColor Red
    Write-Host 'Fix the FAIL lines, then run this audit again. See docs\TROUBLESHOOTING.md.'
    exit 1
}

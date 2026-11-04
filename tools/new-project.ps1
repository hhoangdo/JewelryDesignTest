# Create a new ring project from the corrected template.
# Usage:
#   powershell -ExecutionPolicy Bypass -File .\tools\new-project.ps1 -Name first-ring

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Name,
    [string]$RepoRoot = '',
    [string]$Template = ''
)

$ErrorActionPreference = 'Stop'

if (-not $RepoRoot) {
    if ($PSScriptRoot) {
        $RepoRoot = Split-Path -Parent $PSScriptRoot
    } elseif ($MyInvocation.MyCommand.Path) {
        $RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
    } else {
        $RepoRoot = (Get-Location).Path
    }
}

if (-not $Template) {
    $Template = Join-Path $RepoRoot 'templates\ring-template.blend'
}

if ($Name -notmatch '^[A-Za-z0-9][A-Za-z0-9_-]*$') {
    throw "Project name must use letters, digits, hyphens, or underscores, and start with a letter or digit."
}

if (-not (Test-Path $Template)) {
    throw "Template not found: $Template"
}

$projectRoot = Join-Path $RepoRoot "projects\$Name"
if (Test-Path $projectRoot) {
    throw "Project already exists: $projectRoot"
}

New-Item -ItemType Directory -Force -Path (Join-Path $projectRoot 'scripts'), (Join-Path $projectRoot 'renders') | Out-Null
Copy-Item $Template (Join-Path $projectRoot 'ring.blend')

$readme = @"
# Project: $Name

Created from ``templates/ring-template.blend``.

## Open

1. Open ``ring.blend`` in Blender.
2. Start OpenCode at the repository root (``$RepoRoot`` or your clone path).
3. Paste a prompt such as:

> Build a solitaire ring: US size 7 (17.3 mm inner diameter), 5 mm round brilliant center stone, 6 claw prongs, yellow gold, 2 mm band width. Use the GEMS and METAL collections. Save each script to ``projects/$Name/scripts/``, save the scene to ``projects/$Name/ring.blend``, and render the hero to ``projects/$Name/renders/hero.png``.

## Rules

- One parameter per iteration.
- Inspect with ``look`` before rendering.
- Do not edit the template or the example.
- This folder is ignored by Git.
"@

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $projectRoot 'README.md'), $readme, $utf8NoBom)

Write-Host "Created project: $projectRoot"
Write-Host "  ring.blend"
Write-Host "  scripts\"
Write-Host "  renders\"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Open $projectRoot\ring.blend in Blender."
Write-Host "  2. Start OpenCode at $RepoRoot."
Write-Host "  3. Paste the prompt from $projectRoot\README.md."

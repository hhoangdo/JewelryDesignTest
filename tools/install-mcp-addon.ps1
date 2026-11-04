# Package the installed MCP-for-Blender addon as a Blender 4.5 extension.
#
# Blender 4.5 loads extensions from:
#   <Blender>\4.5\extensions\user_default\<id>\
# The mcp-for-blender installer writes a legacy single-file addon to
#   <Blender>\4.5\scripts\addons\blender_mcp.py
# which Blender 4.5 does not reliably load. This script copies that file into
# the extension layout and writes the manifest. It then disables the legacy
# copy so the two cannot fight over the same module name.

[CmdletBinding()]
param(
    [string]$StudioRoot = 'D:\JewelryStudio',
    [string]$BlenderVersion = '4.5'
)

$ErrorActionPreference = 'Stop'

$versionRoot = Join-Path $StudioRoot "Blender-4.5-LTS\$BlenderVersion"
$legacy = Join-Path $versionRoot 'scripts\addons\blender_mcp.py'
$extensionRoot = Join-Path $versionRoot 'extensions\user_default\blender_mcp'
$manifestPath = Join-Path $extensionRoot 'blender_manifest.toml'
$initPath = Join-Path $extensionRoot '__init__.py'

if (-not (Test-Path $versionRoot)) {
    throw "Blender version folder not found: $versionRoot"
}

if ((Test-Path $initPath) -and (Test-Path $manifestPath) -and -not (Test-Path $legacy)) {
    Write-Host "MCP addon is already packaged as a Blender extension:"
    Write-Host "  $extensionRoot"
    Write-Host "Open Blender -> Edit -> Preferences -> Add-ons -> enable 'MCP for Blender'."
    exit 0
}

if (-not (Test-Path $legacy)) {
    throw "Legacy addon not found: $legacy. Run: `$env:BLENDERMCP_ADDONS_DIR='$versionRoot\scripts\addons'; uvx mcp-for-blender==2.2.6 install-addon"
}

$addonText = Get-Content $legacy -Raw
$version = '1.8.0'
if ($addonText -match '"version"\s*:\s*\((\d+),\s*(\d+)(?:,\s*(\d+))?\)') {
    $minor = $matches[2]
    $patch = '0'
    if ($matches[3]) { $patch = $matches[3] }
    $version = "$($matches[1]).$minor.$patch"
}

# Blender 4.2+ extension loading does not expose bl_info as a module global at
# call time, but the addon's handshake and headers still reference it. Capture
# the values at import time and replace the runtime references, matching the
# compatibility patch used by the verified setup.
$patched = $addonText
$patched = $patched -replace 'tuple\(bl_info\["version"\]\)', 'tuple(globals().get("ADDON_VERSION", (1, 8)))'
$patched = $patched -replace 'list\(bl_info\.get\("version", \(0, 0\)\)\)', 'list(globals().get("ADDON_VERSION", (1, 8)))'
$patched = $patched -replace 'bl_info\.get\("name", "MCP for Blender"\)', 'globals().get("ADDON_NAME", "MCP for Blender")'
$patched = $patched -replace 'bl_info\["version"\]', 'ADDON_VERSION'
$insert = "`r`n`r`nADDON_VERSION = tuple(bl_info.get(`"version`", (1, 8)))`r`nADDON_NAME = bl_info.get(`"name`", `"MCP for Blender`")"
$patched = $patched -replace '(?s)(bl_info\s*=\s*\{.*?\r?\n\})', ('$1' + $insert)

New-Item -ItemType Directory -Force -Path $extensionRoot | Out-Null
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($initPath, $patched, $utf8NoBom)

$manifest = @"
schema_version = "1.0.0"
id = "blender_mcp"
version = "$version"
name = "MCP for Blender"
tagline = "Control Blender 3D with any LLM over MCP"
maintainer = "Siddharth Ahuja <https://github.com/ahujasid>"
type = "add-on"
blender_version_min = "4.2.0"
website = "https://www.mcp-for-blender.com/"
license = ["SPDX:MIT"]
"@

# Write without a UTF-8 BOM; Blender's TOML parser rejects a BOM.
[System.IO.File]::WriteAllText($manifestPath, $manifest, $utf8NoBom)

# Keep the legacy file as .disabled so it is recoverable but not loaded.
$disabled = $legacy + '.disabled'
Move-Item $legacy $disabled -Force

Write-Host "MCP addon packaged as a Blender 4.5 extension:"
Write-Host "  $extensionRoot"
Write-Host "Manifest version: $version"
Write-Host ""
Write-Host "Next:"
Write-Host "  1. Open Blender."
Write-Host "  2. Edit -> Preferences -> Add-ons -> search 'MCP for Blender' -> enable it."
Write-Host "  3. Press N in the 3D viewport -> MCP for Blender -> Start MCP Server."
Write-Host "  4. Verify: (Test-NetConnection -ComputerName localhost -Port 9876).TcpTestSucceeded"

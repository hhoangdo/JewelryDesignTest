# 2. Install

This page installs the toolkit from zero. It assumes OpenCode is already installed and signed in; if it is not, see [Prerequisites](01-prerequisites.md).

The commands use `D:\JewelryStudio` as the toolkit root. Replace it consistently if you chose another drive.

## Step 0 — Open PowerShell and set the root

Use **Windows PowerShell 5.1** or PowerShell 7. Do not run the whole guide as Administrator; the portable Blender does not need it.

```powershell
$StudioRoot = 'D:\JewelryStudio'
New-Item -ItemType Directory -Force -Path $StudioRoot, "$StudioRoot\downloads" | Out-Null
```

If you are using PowerShell 7 and script execution is blocked later, run this once for the current window:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Step 1 — Install Git (only if missing)

```powershell
git --version
```

If that fails:

```powershell
winget install --id Git.Git -e --source winget
```

Close and reopen PowerShell, then run `git --version` again. Expected: `git version 2.x`.

## Step 2 — Install uv and uvx

```powershell
uvx --version
```

If that fails:

```powershell
winget install --id astral-sh.uv -e --source winget
```

Close and reopen PowerShell. Verify:

```powershell
uvx --version
(Get-Command uvx).Source
```

Expected: a version such as `uvx 0.11.7` and a path such as `C:\Users\<you>\.local\bin\uvx.exe`. Keep that path; the OpenCode config needs it when OpenCode is launched from a GUI.

### Optional: keep uv caches off the C: drive

The original setup redirected uv's cache, Python installs, and tools to the studio root. Do this before the first `uvx` run if C: is small:

```powershell
[Environment]::SetEnvironmentVariable('UV_CACHE_DIR', "$StudioRoot\uv-cache", 'User')
[Environment]::SetEnvironmentVariable('UV_PYTHON_INSTALL_DIR', "$StudioRoot\uv-python", 'User')
[Environment]::SetEnvironmentVariable('UV_TOOL_DIR', "$StudioRoot\uv-tools", 'User')
New-Item -ItemType Directory -Force -Path "$StudioRoot\uv-cache", "$StudioRoot\uv-python", "$StudioRoot\uv-tools" | Out-Null
```

Close and reopen PowerShell, then check `$env:UV_CACHE_DIR`. If you skip this step, uv uses its default location under your user profile; that is fine when C: has space.

## Step 3 — Install Blender 4.5.14 LTS (portable)

This guide pins **4.5.14** because the example and its verification were made with it. Blender 4.5.15 exists; it will probably work, but it is not the verified build.

```powershell
$zip = 'blender-4.5.14-windows-x64.zip'
$url = "https://download.blender.org/release/Blender4.5/$zip"
Invoke-WebRequest -Uri $url -OutFile "$StudioRoot\downloads\$zip"
```

Verify the download (optional but recommended):

```powershell
$expected = 'b9533d2397ac1984db4466fb23a7a4649391cca93f6e84209f9bcc60d071c8b9'
$actual = (Get-FileHash "$StudioRoot\downloads\$zip" -Algorithm SHA256).Hash.ToLower()
if ($actual -ne $expected) { throw "Blender checksum mismatch: $actual" }
```

Extract:

```powershell
Expand-Archive -Path "$StudioRoot\downloads\$zip" -DestinationPath "$StudioRoot\Blender-4.5-LTS" -Force
```

The zip contains a `blender-4.5.14-windows-x64` subfolder. Move its contents up one level so the executable is directly at `$StudioRoot\Blender-4.5-LTS\blender.exe`:

```powershell
$inner = Get-ChildItem "$StudioRoot\Blender-4.5-LTS" -Directory | Select-Object -First 1
Get-ChildItem $inner.FullName -Force | Move-Item -Destination "$StudioRoot\Blender-4.5-LTS" -Force
Remove-Item $inner.FullName -Recurse -Force
```

Verify:

```powershell
& "$StudioRoot\Blender-4.5-LTS\blender.exe" --version
```

Expected first line: `Blender 4.5.14 LTS`.

> **Portable means portable.** Blender's preferences, addons, and extensions live inside `$StudioRoot\Blender-4.5-LTS\4.5\`, not under `%APPDATA%`. Keeping the folder in one place makes backup and removal easy.

> **Check `BLENDER_USER_RESOURCES`.** If this environment variable is set, Blender loads preferences and addons from that path instead of the portable folder. Check it with `echo $env:BLENDER_USER_RESOURCES`. If it points at another Blender installation, remove it or set it to `$StudioRoot\Blender-4.5-LTS\4.5`. The setup audit warns when it does not match.

## Step 4 — Install JewelCraft 3.0.1

JewelCraft is the free jewelry toolkit. Version 3.0.1 requires Blender 4.5+ and installs as a Blender **extension**.

```powershell
$jc = 'jewelcraft-3.0.1.zip'
Invoke-WebRequest -Uri "https://github.com/mrachinskiy/jewelcraft/releases/download/v3.0.1/$jc" -OutFile "$StudioRoot\downloads\$jc"
```

Install it with Blender's command-line extension installer:

```powershell
& "$StudioRoot\Blender-4.5-LTS\blender.exe" --command extension install-file "$StudioRoot\downloads\$jc" --repo user_default
```

Verify the manifest exists:

```powershell
Get-ChildItem "$StudioRoot\Blender-4.5-LTS\4.5\extensions" -Recurse -Filter blender_manifest.toml |
  Where-Object { $_.FullName -match 'jewelcraft' } |
  Select-Object -ExpandProperty FullName
```

Expected: a path ending in `...\user_default\jewelcraft\blender_manifest.toml`.

Blender may print a long list of "Registering ... has been registered before" messages and a `GPU functions for drawing are not available in background mode` error after the install. These are harmless in this command; the manifest check above is authoritative.

Now open Blender:

1. In the 3D viewport, press `N` to open the sidebar.
2. Confirm there is a **JewelCraft** tab with gems, prongs, spacing, and weighting tools.

If the tab is missing, read [Troubleshooting](TROUBLESHOOTING.md#jewelcraft-tab-missing).

## Step 5 — Install the MCP-for-Blender addon and configure OpenCode

The MCP server and the Blender addon must be the same generation. This guide pins **mcp-for-blender 2.2.6**.

### 5.1 Install the bundled addon file

```powershell
$env:BLENDERMCP_ADDONS_DIR = "$StudioRoot\Blender-4.5-LTS\4.5\scripts\addons"
$env:PYTHONIOENCODING = 'utf-8'
uvx mcp-for-blender==2.2.6 install-addon
```

Expected: `Installed MCP for Blender addon to ...\4.5\scripts\addons\blender_mcp.py`.

`PYTHONIOENCODING` prevents a harmless `UnicodeEncodeError` while the installer prints an arrow character. If you see that error **after** the "Installed ..." line, the install still succeeded; check that `blender_mcp.py` exists.

### 5.2 Package it as a Blender 4.5 extension

Blender 4.5 loads addons from the **extensions** folder. The installer writes a legacy single-file addon that Blender 4.5 does not reliably load. Package it with the repository helper:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install-mcp-addon.ps1 -StudioRoot $StudioRoot
```

Expected:

```
MCP addon packaged as a Blender 4.5 extension:
  D:\JewelryStudio\Blender-4.5-LTS\4.5\extensions\user_default\blender_mcp
```

The helper:

- copies `blender_mcp.py` into the extension layout as `__init__.py`;
- writes a BOM-free `blender_manifest.toml`;
- applies the compatibility patch for Blender's extension loader;
- moves the legacy file to `blender_mcp.py.disabled`.

Verify the manifest:

```powershell
Get-ChildItem "$StudioRoot\Blender-4.5-LTS\4.5\extensions\user_default\blender_mcp" |
  Select-Object Name, Length
```

Expected: `blender_manifest.toml` and `__init__.py`.

### 5.3 Configure OpenCode

Edit (or create) the OpenCode global config at:

```
C:\Users\<you>\.config\opencode\opencode.json
```

Add this block, keeping any existing keys:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "blender": {
      "type": "local",
      "command": ["C:/Users/YOU/.local/bin/uvx.exe", "mcp-for-blender==2.2.6"],
      "enabled": true,
      "environment": {
        "BLENDER_HOST": "localhost",
        "BLENDER_PORT": "9876",
        "BLENDER_MCP_SAFE_MODE": "1",
        "DISABLE_TELEMETRY": "true",
        "UV_PYTHON_PREFERENCE": "only-managed"
      }
    }
  }
}
```

Replace `C:/Users/YOU/.local/bin/uvx.exe` with the exact path printed by `(Get-Command uvx).Source`. Use forward slashes in JSON. Save the file and validate it:

```powershell
Get-Content "$env:USERPROFILE\.config\opencode\opencode.json" -Raw | ConvertFrom-Json | Out-Null
"JSON OK"
```

Expected: `JSON OK`.

### 5.4 Enable the addon in Blender

1. Open Blender.
2. **Edit → Preferences → Add-ons**.
3. Search for **MCP for Blender** and enable it.
4. If you see two entries, enable the one whose module starts with `bl_ext.user_default`. Disable any old `blender_mcp` entry that reports `No module named`.
5. In the 3D viewport press `N` → **MCP for Blender** tab.
6. If the status says **Not connected**, click **Start MCP Server**.

Verify the port:

```powershell
(Test-NetConnection -ComputerName localhost -Port 9876).TcpTestSucceeded
```

Expected: `True`. If it is `False`, see [Troubleshooting](TROUBLESHOOTING.md#port-9876-is-not-listening).

## Step 6 — Restart OpenCode and check the tools

Fully quit OpenCode (on Windows, quit from the system tray, not just the window), then start it from the repository root:

```powershell
cd D:\JewelryDesignTest
opencode
```

Ask:

> What Blender MCP tools do you have?

Expected tools include:

- `get_addon_status`
- `execute_blender_code`
- `get_scene_info`
- `look`

If OpenCode reports `spawn uvx ENOENT`, see [Troubleshooting](TROUBLESHOOTING.md#spawn-uvx-enoent).

## Step 7 — Run the setup audit

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1
```

Expected: no `FAIL` lines. `WARN` lines are acceptable when Blender is closed or a local project folder is intentionally absent.

If everything passes, continue to [3. Verify](03-verify.md).

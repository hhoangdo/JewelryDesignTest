# 1. Prerequisites

This page checks the machine before anything is installed. If a check fails here, fix it before downloading Blender.

## Operating system

| | Supported | Notes |
|---|---|---|
| Windows 11 64-bit | ✅ Recommended | Best driver and terminal support |
| Windows 10 64-bit | ✅ Supported | The minimum for this guide |
| Windows 8.1 64-bit | ⚠️ Blender may run | OpenCode requires Windows 10/11, so the full workflow is not supported |
| Windows XP / Vista / 7 | ❌ Not supported | Blender 4.5 cannot run; see the table below |

### Why Windows XP cannot work

| Component | Needs | Last XP-compatible version |
|---|---|---|
| Blender | 64-bit Windows 8.1+, SSE4.2, 8 GB RAM, OpenGL 4.3 | Blender 2.76 (2014) |
| JewelCraft | Blender 4.5+ | None — JewelCraft 3.x is an extension for modern Blender |
| mcp-for-blender addon | Blender 3.0+ | None |
| OpenCode | Windows 10/11 64-bit | None |

There is no combination of the current stack that runs on XP. Use a Windows 10/11 64-bit machine, or connect to one with Remote Desktop.

## Hardware check

Open **Windows PowerShell** (not the legacy Command Prompt) and run:

```powershell
[Environment]::Is64BitOperatingSystem
Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, OSArchitecture
Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores
Get-CimInstance Win32_VideoController | Select-Object Name, AdapterRAM, DriverVersion
Get-PSDrive C, D -ErrorAction SilentlyContinue | Select-Object Name, @{n='FreeGB';e={[math]::Round($_.Free/1GB,1)}}
```

What to expect:

- `Is64BitOperatingSystem` → `True`.
- Windows caption contains `Windows 10` or `Windows 11`.
- At least 8 GB RAM.
- A GPU with OpenGL 4.3 support. NVIDIA RTX is fastest for Cycles; AMD/Intel GPUs work with their own Cycles backend. No GPU is fine for modeling, but renders will use the CPU and take longer.
- At least 2 GB free on the target drive. 10 GB is more comfortable once caches and projects accumulate.

If the GPU driver is old, update it from the manufacturer's site before rendering. Blender may refuse to start with an outdated OpenGL driver.

## Software already on the machine

The guide assumes **OpenCode is installed and signed in**. Check:

```powershell
opencode --version
```

If OpenCode is missing, install it from <https://opencode.ai/docs/> and authenticate with your model provider (`opencode auth login`, or the provider flow shown on first launch). This repository does not include API keys.

Also check:

```powershell
git --version
uvx --version
```

- `git` is needed to clone the repository. If it is missing, the install page shows how to add it.
- `uvx` is needed to run the MCP server. If it is missing, the install page adds it.
- Node.js is **not** required for this workflow when OpenCode is already installed. If you install OpenCode via npm, install Node.js 18+ first.

## Choose a studio root

The guide uses one folder for the toolkit and one folder for the repository:

```
D:\JewelryStudio\        ← Blender, downloads, caches, temporary test copies
D:\JewelryDesignTest\    ← the cloned repository and your projects
```

If you do not have a `D:` drive, use `C:\JewelryStudio` and `C:\JewelryDesignTest`. The commands in the guide use `D:` as the example; replace it consistently.

Avoid paths with non-ASCII characters or spaces in the toolkit root. Blender and Python handle them, but some command-line tools are less forgiving.

## Network and permissions

You need:

- Internet access to download Blender, JewelCraft, Python packages, and the repository.
- Permission to extract a portable app into the studio root. Administrator rights are **not** required for portable Blender, but `winget` may prompt for elevation when installing Git or uv.
- About 1 GB of temporary space for the Blender zip and extraction.

## What "done" looks like

At the end of the setup you will have:

1. Blender 4.5.14 LTS at `D:\JewelryStudio\Blender-4.5-LTS\blender.exe`.
2. JewelCraft 3.0.1 visible as a sidebar tab in Blender.
3. The MCP-for-Blender addon enabled and listening on `localhost:9876`.
4. OpenCode listing `blender` tools such as `execute_blender_code`, `get_scene_info`, and `look`.
5. `tools/check-setup.ps1` reporting no `FAIL` lines.

Next: [2. Install](02-install.md).

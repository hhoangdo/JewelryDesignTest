# Jewelry Studio — Text-to-Ring with Blender + OpenCode

A free, Windows-based workshop that turns plain-English ring prompts into editable Blender models and studio-quality renders. The AI writes Blender Python (`bpy`) through the Model Context Protocol (MCP); it does not generate a blob mesh.

![Reference ring](example-solitaire/reference/target.jpg)
![Rendered example](example-solitaire/renders/hero.png)

*Left: the reference photograph. Right: the example solitaire built by this workflow.*

> **On a fresh machine with OpenCode?** Paste the planning prompt from [START-HERE.md](START-HERE.md) into OpenCode first. It inspects the machine and plans the setup; it does not install or edit anything until you approve the plan.

## What you will build

The worked example is a **white-gold, US 7, four-prong cushion solitaire** with an open V-head. It is deliberately one example, not a gallery: the point is that you can reproduce it, understand it, and then build your own design from a prompt.

## Requirements

| | Minimum | Notes |
|---|---|---|
| OS | **Windows 10 or 11, 64-bit** | Windows XP is **not supported** — see below |
| CPU | 4 cores with SSE4.2 | Blender 4.5 will not start without SSE4.2 |
| RAM | 8 GB | 16 GB is comfortable |
| GPU | OpenGL 4.3, 2 GB VRAM | NVIDIA RTX is recommended for fast Cycles renders; CPU rendering works |
| Disk | ~2 GB free | Blender is ~1 GB extracted; caches and projects add more |
| Software | OpenCode, Git, uv | The install guide adds Blender, JewelCraft, and the MCP addon |
| Accounts | GitHub (to clone) and an OpenCode model provider | No paid Blender/Jewelry addon is required |

### Windows XP is not supported

Windows XP cannot run any part of this stack:

| Component | Minimum | XP possible? |
|---|---|---|
| Blender 4.5 LTS | 64-bit Windows 8.1+, SSE4.2, 8 GB RAM, OpenGL 4.3 | No — the last XP build is Blender 2.76 (2014) |
| JewelCraft 3.0.1 | Blender 4.5+ | No |
| MCP-for-Blender addon | Blender 3.0+ | No |
| OpenCode | Windows 10/11 64-bit | No |

If a colleague is still on XP, the only path is to move to a Windows 10/11 64-bit machine (or use Remote Desktop to one). Do not try to force Blender 4.5 onto XP.

## Quick start

If you are using an AI agent on a fresh machine, start with [START-HERE.md](START-HERE.md) instead of following the manual steps below. The prompt makes the agent read the guide, inspect the machine, and plan before installing anything.

```powershell
# 1. Clone the workshop
cd D:\
git clone https://github.com/hhoangdo/JewelryDesignTest.git
cd JewelryDesignTest

# 2. Follow the setup guide
#    docs\02-install.md  (installs Blender 4.5.14, JewelCraft 3.0.1, mcp-for-blender 2.2.6)

# 3. Verify the machine
powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1

# 4. Create your first project
powershell -ExecutionPolicy Bypass -File .\tools\new-project.ps1 -Name first-ring

# 5. Open projects\first-ring\ring.blend in Blender, start OpenCode at the repo root,
#    and paste the prompt from docs\04-first-project.md
```

The full details, expected outputs, and failure fixes are in [docs](docs/).

## How the workflow works

```
plain-English prompt
        │
        ▼
OpenCode agent  ──MCP──►  mcp-for-blender  ──TCP :9876──►  Blender addon
        │                                                   │
        │  writes bpy scripts                               │ builds mesh
        │  saves them in projects/<name>/scripts/            │
        ▼                                                   ▼
   `look` screenshot ◄────────────────────────────  Cycles render
        │
        ▼
   compare, iterate one parameter, save hero.png
```

- **OpenCode** is the chat/agent client.
- **mcp-for-blender** translates MCP tool calls into Blender commands.
- **Blender** runs the Python and renders.
- **`look`** returns a viewport screenshot so the AI can inspect its own work before rendering.
- **Safe mode** keeps the AI's Blender scripts to modeling-only Python (`bpy`, `math`, `mathutils`); it cannot read/write arbitrary files or change your preferences.

## Repository layout

| Path | What it is |
|---|---|
| `START-HERE.md` | The planning prompt to give a fresh OpenCode session before installing anything |
| `example-solitaire/` | The single worked example: model, hero render, reference image, and the five scripts that rebuild it |
| `templates/` | The corrected starting `.blend` and the maintainer script that regenerates it |
| `docs/` | Setup, verification, first-project, recreate-example, troubleshooting, glossary, resources |
| `projects/` | Your local work; ignored by Git |
| `tools/` | `check-setup.ps1`, `new-project.ps1`, and the MCP extension packager |
| `AGENTS.md` | Ring-building rules the AI reads automatically |

## Known-good versions

| Tool | Version | Why this version |
|---|---|---|
| Blender | **4.5.14 LTS** | The example was built and verified with it; 4.5.15 exists but is not the verified build |
| JewelCraft | **3.0.1** | Requires Blender 4.5+; installed as an extension |
| mcp-for-blender | **2.2.6** | Pinned so the addon/server protocol does not drift |
| uv / uvx | 0.11.7 or newer | Verified with 0.11.7 |
| OpenCode | 2.x | Verified with 2.2.5; the MCP config syntax is the same in 1.19+ |

See [docs/VERIFICATION.md](docs/VERIFICATION.md) for the dated test results.

## Scope

This is a **visual modeling workshop**: renders and previews, not casting or printing certification. Dimensions are real millimetres and the example is geometrically consistent, but manufacturing tolerances, metal shrinkage, and stone-setting engineering are out of scope.

## License and credits

- Code and documentation: [MIT](LICENSE).
- The reference photograph in `example-solitaire/reference/` is supplied by the repository author for visual comparison; it is not covered by the MIT license.
- [Blender](https://www.blender.org/) is free software.
- [JewelCraft](https://github.com/mrachinskiy/jewelcraft) is GPL-3.0; this repository downloads it separately and does not redistribute it.
- [mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) is MIT.
- [OpenCode](https://opencode.ai/) is the agent client.

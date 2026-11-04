# Start here — the OpenCode planning prompt

New machine, only OpenCode installed, repository cloned? Paste the prompt below into OpenCode **before** installing anything. It makes the agent inspect the machine, read the guide, and produce a plan without changing files.

## How to use it

1. Clone the repository and open OpenCode at the repo root.
2. Select the **Plan** agent (or keep the agent read-only for this first message).
3. Paste the prompt.
4. Review the plan. If it is wrong, correct it in chat.
5. Switch to **Build** mode and send: *"Plan approved. Execute it in order. Stop at the first failed check and report the exact command and output."*

## The prompt

```text
You are setting up the Jewelry Studio workshop on a fresh Windows machine.
Assume OpenCode is the only AI tool installed; Blender, Git, uv, JewelCraft, and
the MCP addon are not installed yet.

Repository: https://github.com/hhoangdo/JewelryDesignTest
Work from the repository root. Follow AGENTS.md. This guide covers OpenCode only;
do not configure Codex or other clients.

Work in PLAN mode. Do not install, edit, delete, commit, or push anything yet.
Read, inspect, and plan.

Read, in this order:
- README.md
- docs/01-prerequisites.md
- docs/02-install.md
- docs/03-verify.md
- docs/VERIFICATION.md
- docs/05-recreate-example.md

Inspect and report:
- Windows edition/version and whether it is 64-bit. Windows XP is unsupported; stop if you see XP.
- CPU SSE4.2 support, RAM, GPU/OpenGL, and free disk.
- Whether OpenCode, Git, uv/uvx, Blender, JewelCraft, and the MCP addon are present.
- The absolute path of uvx.exe.
- The value of BLENDER_USER_RESOURCES and whether it points at the intended portable Blender.

Then produce a step-by-step plan that:
- Uses the pinned versions: Blender 4.5.14 LTS, JewelCraft 3.0.1,
  mcp-for-blender 2.2.6, uv 0.11.7+.
- Follows docs/02-install.md exactly, including tools/install-mcp-addon.ps1.
  Do not use the upstream automatic `mcp-for-blender setup` as a substitute;
  it writes a legacy addon that Blender 4.5 does not load.
- Parameterizes every path with the actual repo root and studio root; do not
  hardcode D:\JewelryDesignTest or a username.
- Gives the exact command, expected output, and stop condition for each step.
- Ends with: tools/check-setup.ps1 → live MCP test → deterministic example
  replay → new project.

Stop and report if:
- Windows is XP, 32-bit, or the CPU lacks SSE4.2.
- The Blender checksum mismatches.
- The JewelCraft manifest or MCP addon extension is missing after installation.
- Port 9876 is owned by another process (change the addon and OpenCode config together).
- Any check fails. Do not claim success without the command output.

Done means:
- tools/check-setup.ps1 has no FAIL.
- Blender shows the MCP-for-Blender and JewelCraft panels.
- OpenCode lists get_scene_info, execute_blender_code, and look.
- look returns a viewport image.
- The example replay prints five PASS lines and writes
  example-solitaire/renders/hero.png.
- A new project under projects/ has a hero render matching the example's composition.

Known quirk: get_addon_status may report a handshake warning with the pinned
2.2.6 build. If get_scene_info, execute_blender_code, and look work, continue;
docs/VERIFICATION.md records this as diagnostic-only.

Present the plan in chat and ask for approval. Do not execute until I switch
you to Build mode.
```

## Short version

For a colleague who wants the essentials without the detailed stop conditions:

```text
Read README.md and docs/01-prerequisites.md, docs/02-install.md,
docs/03-verify.md, and docs/05-recreate-example.md. You are on a fresh Windows
machine with only OpenCode installed. Plan the full setup using the pinned
versions and tools/install-mcp-addon.ps1. Do not install or edit anything yet.
Inspect the machine, list blockers, and present a step-by-step plan with exact
commands and expected outputs. Ask for approval before executing.
```

## Why this prompt exists

The setup has three failure modes that a fresh agent gets wrong without guidance:

1. **It installs "the latest" instead of the pinned versions.** The tutorial is verified against Blender 4.5.14, JewelCraft 3.0.1, and mcp-for-blender 2.2.6.
2. **It uses the upstream automatic MCP setup.** That writes a legacy addon file Blender 4.5 does not load; `tools/install-mcp-addon.ps1` packages it as a proper extension.
3. **It claims success without evidence.** The prompt requires `check-setup.ps1`, a live MCP tool check, the deterministic replay, and a new project before the work is called done.

The human-facing guide starts at [README.md](README.md). The setup details are in [docs/02-install.md](docs/02-install.md).

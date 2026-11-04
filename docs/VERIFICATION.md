# Verification record

This page records what was actually tested, on which machine, and what was **not** tested. "It works" is not evidence.

## Test machine

| | |
|---|---|
| Date | 2026-11-04 |
| OS | Windows 11 Home, version 10.0.26300, 64-bit |
| CPU | 13th Gen Intel Core i7-13620H, 10 cores |
| RAM | 32 GB |
| GPU | NVIDIA GeForce RTX 4060 Laptop GPU (4 GB reported), Intel UHD Graphics |
| Blender | 4.5.14 LTS, build 2026-09-15 |
| JewelCraft | 3.0.1 |
| mcp-for-blender | 2.2.6 |
| uv | 0.11.7 |
| OpenCode | 2.2.5 |

This is the author's machine, not a clean Windows install. The clean-room section below is the important one for a new user.

## 1. Template regeneration

Command:

```powershell
& "D:\JewelryStudio\Blender-4.5-LTS\blender.exe" --background --factory-startup --python templates\make_template.py
```

Result: **PASS**

```
TEMPLATE SAVED D:/JewelryDesignTest/templates/ring-template.blend
SCALE 1.0 LEN MILLIMETERS
OBJECTS [('Camera', 'CAMERA'), ('Light', 'LIGHT')]
COLLS [('GEMS', 0), ('METAL', 0), ('REFERENCE', 0)]
MATS ['Gem_Center', 'Gold_Rose', 'Gold_White', 'Gold_Yellow', 'Silver']
```

The template has no default cube and no stray material.

## 2. Checked-in example verification

Command:

```powershell
& "D:\JewelryStudio\Blender-4.5-LTS\blender.exe" --background --factory-startup `
  "example-solitaire\ring.blend" --python "example-solitaire\scripts\verify_scene.py"
```

Result: **PASS — 5/5 groups**

```
PASS band: OD 21.7000 mm, ID 17.3000 mm; scene scale 1; band geometry checked
PASS gem: 5.5x5.5x3.1 mm; table 3.685 mm; crown .6 mm; 217 closed outward facets; clearance 1.05 mm
PASS head: four closed tapered V-arms, two compact shoulders, white metal; no rail/foot/ball tips
PASS claws: 4 integrated hooks, actual seat/tip mesh contact <= 0.0202 mm; low table-edge tips
PASS studio: Cycles, denoise, 1000x1000, valid clipping; vertical coverage 82.7%
```

## 3. Full rebuild from the template on the working machine

A scratch project was created from `templates/ring-template.blend`, then the five example scripts were run in order:

1. `build_band.py` → `BUILT band: OD 21.7 mm, ID 17.3 mm, top Z 21.7 mm`
2. `build_gem.py` → `BUILT cushion: 5.5 mm, table 67%, crown 0.6 mm, 217 facets; girdle Z 25.200 mm`
3. `build_head.py` → `BUILT 4 sculpted V-arms + 2 compact shoulders; integrated claws=True; no rail or cone`
4. `studio_render.py` → `HERO saved to .../renders/hero.png` (1000×1000, **712,904 bytes**)
5. `verify_scene.py` → all five groups **PASS**

This proves the example is self-contained: it does not depend on the old `04` project or on the author's live scene.

## 4. Clean-room install

A separate installation was created at `D:\JewelryStudio\clean-test` using the exact pinned versions and the commands in `docs/02-install.md`. The author's working Blender was not modified.

| Check | Expected | Result |
|---|---|---|
| Blender 4.5.14 zip SHA256 | `b9533d23…c8b9` | **PASS** — hash matched |
| Blender version | `Blender 4.5.14 LTS` | **PASS** |
| JewelCraft 3.0.1 extension install | `blender_manifest.toml` present | **PASS** |
| `uvx mcp-for-blender==2.2.6 install-addon` | `blender_mcp.py` written | **PASS** |
| `tools/install-mcp-addon.ps1` packaging | extension `blender_mcp` with a BOM-free manifest | **PASS** |
| `tools/check-setup.ps1 -StudioRoot ...\clean-test\Studio` | no `FAIL` | **PASS** — one expected `WARN` because Blender was closed |
| Template opens with scale 1.0 and mm | scale `1.0`, `MILLIMETERS` | **PASS** |
| Example replay from the clean template | five `PASS` groups + hero | **PASS** — hero 1000×1000, **712,894 bytes** |
| Clean-test folder removed | path no longer exists | **PASS** |

The clean-room replay used a copy of `templates/ring-template.blend` and the five scripts from `example-solitaire/scripts/`. It did not reuse the checked-in `ring.blend`.

## 5. Live MCP test

With the clean-room Blender open and the MCP server started, OpenCode successfully ran:

- `get_scene_info` — returned the default Cube/Camera/Light scene.
- `execute_blender_code` — returned the addon info dictionary, including Blender `4.5.14 LTS` and protocol `15`.
- `look` — returned a viewport screenshot.

`get_addon_status` reported a handshake warning (`Connection to Blender lost`) even though the three tools above worked. A direct TCP command to the addon returned:

```json
{"status": "success", "result": {"name": "MCP for Blender", "addon_version": [1, 8], "protocol_version": 15, "blender_version": "4.5.14 LTS"}}
```

This is recorded as a **known diagnostic quirk**, not a setup failure. The tutorial's verification steps use `get_scene_info`, `execute_blender_code`, and `look` rather than relying on the handshake.

## 6. Setup audit output

Working machine:

```
PASS  Microsoft Windows 11 Home (64-bit) (10.0.26300)
PASS  PowerShell 5.1.26100.9818
PASS  git version 2.54.0.windows.1
PASS  uvx 0.11.7 at C:\Users\hhoangdo\.local\bin\uvx.exe
PASS  BLENDER_USER_RESOURCES points at the portable Blender
PASS  Blender 4.5.14 LTS
PASS  JewelCraft manifest found
PASS  MCP addon extension found
WARN  MCP port 9876 is not listening (Blender was closed)
PASS  OpenCode opencode v2.2.5
PASS  OpenCode config has an enabled blender entry
PASS  OpenCode uses an absolute uvx path
PASS  Safe mode is on
PASS  Workshop template, example, scripts, and reference image are present
RESULT: PASS (1 warning)
```

Clean-room machine:

```
PASS  Blender 4.5.14 LTS at ...\clean-test\Studio\Blender-4.5-LTS\blender.exe
PASS  JewelCraft manifest found
PASS  MCP addon extension found
PASS  (with BLENDER_USER_RESOURCES pointed at the clean-test folder)
RESULT: PASS (1 warning: port not listening)
```

## 7. Cleanup

The clean-room Blender, its downloads, logs, temporary start script, and PID file were deleted after the test. The temporary clone was also deleted. `D:\JewelryStudio\clean-test` and the clone folder no longer exist.

## 8. Clone test

The public repository was cloned into a different folder to prove the paths are portable:

```powershell
git clone https://github.com/hhoangdo/JewelryDesignTest.git `
  C:\Users\<you>\AppData\Local\Temp\opencode\JewelryDesignTest-clone
```

| Check | Result |
|---|---|
| `check-setup.ps1` from the clone | **PASS** — one warning because Blender was closed |
| `verify_scene.py` on the cloned example | **PASS — 5/5 groups** |
| `new-project.ps1 -Name clone-smoke` | **PASS** — `ring.blend`, `scripts\`, `renders\` created |

The first clone test **failed** the studio check: the checked-in `ring.blend` stored an absolute hero path (`D:/JewelryDesignTest/...`), so the path assertion broke when the repository moved. The fix was to store `//renders/hero.png` in the blend and resolve it with `bpy.path.abspath()` in `verify_scene.py` and `studio_render.py`. The clone was repeated after the fix and passed.

## 9. Known limitations

- The example is a **visual model**, not a manufacturing/casting certification.
- The reference photograph cannot fully determine the hidden pavilion/setting geometry.
- Shoulder junctions and claw tips remain slightly different from the reference; this is recorded in `example-solitaire/README.md`.
- Headless Blender runs with the MCP addon enabled can print `SystemError: GPU functions for drawing are not available in background mode` **after** the save/checks complete. Using `--factory-startup` avoids it.
- The clean-room test uses the same Windows machine and GPU; it does not prove behaviour on every Windows 10/11 configuration.
- The MCP addon is installed as an extension by `tools/install-mcp-addon.ps1` because the upstream `install-addon` command writes a legacy file that Blender 4.5 does not reliably load. This is documented in `docs/02-install.md` and `docs/TROUBLESHOOTING.md`.

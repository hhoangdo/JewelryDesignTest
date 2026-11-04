# Troubleshooting

Start with the audit:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1
```

The `FAIL` line names the broken component. The sections below explain the common fixes.

## Blender will not start

**Symptoms:** a dialog about OpenGL, Vulkan, or an unsupported GPU; the window closes immediately.

**Fixes:**

1. Update the GPU driver from NVIDIA/AMD/Intel. Do not rely on Windows Update.
2. Confirm the GPU supports OpenGL 4.3. Very old integrated graphics may not.
3. Try the safe-start scripts in the Blender folder:
   ```powershell
   & "D:\JewelryStudio\Blender-4.5-LTS\blender_startup_opengl.cmd"
   ```
4. If the machine is a laptop with switchable graphics, force Blender to use the discrete GPU in the vendor control panel.

Blender 4.5 requires a 64-bit OS and a CPU with SSE4.2. Windows XP cannot run it.

## JewelCraft tab missing

**Symptoms:** Blender opens, but the `N` sidebar has no JewelCraft tab.

**Fixes:**

1. Confirm the manifest exists:
   ```powershell
   Get-ChildItem "D:\JewelryStudio\Blender-4.5-LTS\4.5\extensions" -Recurse -Filter blender_manifest.toml |
     Where-Object { $_.FullName -match 'jewelcraft' }
   ```
2. If it is missing, rerun the install:
   ```powershell
   & "D:\JewelryStudio\Blender-4.5-LTS\blender.exe" --command extension install-file `
     "D:\JewelryStudio\downloads\jewelcraft-3.0.1.zip" --repo user_default
   ```
3. In Blender: **Edit → Preferences → Add-ons**, search `JewelCraft`, and enable it.
4. Restart Blender. Extension changes are not always picked up live.
5. If the install says the extension is incompatible, you are not on Blender 4.5+. JewelCraft 3.0.1 requires 4.5.

## Port 9876 is not listening

**Symptoms:** `Test-NetConnection localhost -Port 9876` returns `False`; OpenCode says it cannot connect to Blender.

**Fixes:**

1. Blender must be running. The MCP server lives inside Blender, not in OpenCode.
2. In Blender, press `N` → **MCP for Blender** → click **Start MCP Server**.
3. Check the port again:
   ```powershell
   (Test-NetConnection -ComputerName localhost -Port 9876).TcpTestSucceeded
   ```
4. If another program owns 9876, choose a free port in the addon panel, then change `BLENDER_PORT` in the OpenCode config to the same number. Restart Blender and OpenCode.
5. A firewall prompt for Blender should be allowed on private networks. The server binds to localhost, so no inbound internet rule is needed.

## spawn uvx ENOENT

**Symptoms:** OpenCode starts, but the Blender MCP server fails with `spawn uvx ENOENT`.

**Cause:** OpenCode was launched from a GUI and did not inherit the terminal `PATH`, so it cannot find `uvx`.

**Fixes:**

1. Find the absolute path:
   ```powershell
   (Get-Command uvx).Source
   ```
2. In `C:\Users\<you>\.config\opencode\opencode.json`, replace `"uvx"` or the old path with that exact path, using forward slashes:
   ```json
   "command": ["C:/Users/you/.local/bin/uvx.exe", "mcp-for-blender==2.2.6"]
   ```
3. Fully quit OpenCode from the system tray and reopen it.
4. Alternatively, launch OpenCode from a PowerShell window where `uvx --version` works. That inherits the PATH.

## OpenCode does not see Blender tools

**Symptoms:** OpenCode answers normally but has no `execute_blender_code`, `get_scene_info`, `look`, or `get_addon_status`.

**Fixes:**

1. Validate the config JSON:
   ```powershell
   Get-Content "$env:USERPROFILE\.config\opencode\opencode.json" -Raw | ConvertFrom-Json | Out-Null
   "JSON OK"
   ```
2. Confirm the `blender` entry exists, is `"enabled": true`, and its `command` points to a real `uvx.exe`.
3. Fully quit OpenCode (tray icon → Quit) and reopen. Closing the window is not enough.
4. Run OpenCode from the repository root so project-level config and `AGENTS.md` are picked up.
5. Check the MCP server manually:
   ```powershell
   uvx mcp-for-blender==2.2.6 --help
   ```
6. If the server starts but cannot reach Blender, see [Port 9876 is not listening](#port-9876-is-not-listening).

## MCP addon version mismatch

**Symptoms:** the addon panel says the server is newer/older; some tools fail; `get_addon_status` reports a protocol mismatch.

**Fixes:**

1. Update both halves together:
   ```powershell
   $env:PYTHONIOENCODING = 'utf-8'
   uvx mcp-for-blender==2.2.6 update
   ```
2. Re-package the addon as an extension:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .\tools\install-mcp-addon.ps1 -StudioRoot D:\JewelryStudio
   ```
3. Restart OpenCode completely.
4. In Blender, disable and re-enable **MCP for Blender**, or restart Blender.
5. If the addon was installed manually as `blender_mcp.py`, reinstall it with `uvx mcp-for-blender==2.2.6 install-addon` and enable the new copy.

## look returns no image

**Symptoms:** the AI calls `look`, but the chat shows an error or no image.

**Fixes:**

1. The Blender MCP panel must be connected. `look` uses the same socket as `execute_blender_code`.
2. Make sure a 3D viewport exists and is not minimized. The addon captures the viewport, not the whole desktop.
3. Bring the Blender window to the foreground once, then retry.
4. If the scene is empty, `look` can return a blank image. Open the template or a project first.
5. Check the Blender system console for addon errors (Window → Toggle System Console).

## Render is blank or tiny

**Symptoms:** `hero.png` is a few KB, all white, all black, or the ring is not visible.

**Fixes:**

1. Check the output path. The file should be under the project's `renders\` folder, not the old example folder.
2. Check camera clipping:
   ```python
   import bpy
   cam = bpy.context.scene.camera
   print(cam.data.clip_start, cam.data.clip_end)
   ```
   For this scale, `0.001` to `1.0` works. The whole ring is about 0.022 m tall.
3. Check that the camera points at the ring: `camera.location` should be around `(0.035, -0.055, 0.045)` metres and the target around `(0, 0, 0.014)`.
4. Check the resolution is 1000×1000 at 100%.
5. If the image is black, check the world strength and light energy. The studio script uses a neutral world and three area lights.
6. If the image is white, the exposure or world strength may be too high. Lower `WORLD_STRENGTH` in `studio_render.py`.

## GPU render fails or falls back to CPU

**Symptoms:** Cycles says there is no GPU device, or rendering is very slow.

**Fixes:**

1. Update the GPU driver.
2. In Blender: **Edit → Preferences → System → Cycles Render Devices**, select OptiX (NVIDIA), HIP (AMD), or oneAPI (Intel), and save.
3. If the machine has no supported GPU, set `USE_GPU = False` at the top of `studio_render.py`. Cycles will render on the CPU; it is slower but produces the same image.
4. For a quick preview, lower `SAMPLES` and the resolution in `studio_render.py`, then restore them for the final render.

## Everything is 1000× too small or too large

**Cause:** the scene scale and the millimetre conversion were applied twice, or only once when they should have been twice.

**Fix:** check the scene scale:

```python
import bpy
print(bpy.context.scene.unit_settings.scale_length)  # must be 1.0
```

The template uses `scale_length = 1.0` and millimetres displayed. Design in millimetres, then divide by 1000 for coordinates. Do not set `scale_length = 0.001` on top of that.

## PowerShell blocks the helper scripts

**Symptom:** `... cannot be loaded because running scripts is disabled on this system`.

**Fix:** run the helpers with a per-process bypass:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1
powershell -ExecutionPolicy Bypass -File .\tools\new-project.ps1 -Name first-ring
```

This does not change the machine-wide policy.

## The Blender checksum does not match

**Symptom:** the SHA256 check throws `Blender checksum mismatch`.

**Fixes:**

1. Delete the partial download and download again:
   ```powershell
   Remove-Item "D:\JewelryStudio\downloads\blender-4.5.14-windows-x64.zip" -Force
   ```
2. Use the official URL from [the install page](02-install.md#step-3--install-blender-4514-lts-portable).
3. If a corporate proxy rewrites downloads, verify the file size (about 398 MB) and use the official SHA256 from `https://download.blender.org/release/Blender4.5/blender-4.5.14.sha256`.

## Safe mode blocks a script

**Symptom:** the MCP addon rejects a script with a message about unsafe operations.

**Cause:** safe mode is on (recommended). It blocks filesystem access, `os`, preferences changes, and some dynamic operations.

**Fix:** rewrite the Blender-side script to use only `bpy`, `math`, and `mathutils`. Do file operations (creating folders, saving scripts) with OpenCode's file tools, not inside Blender. If a task genuinely needs preferences or external files, do it manually in Blender's GUI.

## Headless Blender prints `GPU functions for drawing are not available in background mode`

This is a known artifact when the MCP addon is enabled during a `--background` run. It usually appears **after** the script has finished and the file has been saved. It does not mean the build failed.

To avoid it for verification, use:

```powershell
& "D:\JewelryStudio\Blender-4.5-LTS\blender.exe" --background --factory-startup `
  "projects\replay-check\ring.blend" --python "example-solitaire\scripts\verify_scene.py"
```

`--factory-startup` disables user addons for that run.

## MCP addon installed but Blender does not list it

**Symptoms:** `uvx mcp-for-blender install-addon` reports success, but Preferences → Add-ons has no working **MCP for Blender** entry; or Blender logs `No module named 'blender_mcp'`.

**Cause:** Blender 4.5 loads addons from the **extensions** folder. The installer writes a legacy `scripts\addons\blender_mcp.py`, which Blender 4.5 does not reliably load. A second common cause is a `blender_manifest.toml` written with a UTF-8 BOM; Blender's TOML parser rejects it.

**Fix:**

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\install-mcp-addon.ps1 -StudioRoot D:\JewelryStudio
```

Then open Blender → **Edit → Preferences → Add-ons** → search **MCP for Blender** → enable the entry whose module starts with `bl_ext.user_default`. Restart Blender if the entry does not appear.

If you see two entries, disable the old `blender_mcp` one that reports `No module named`. The extension entry is the one to use.

## `BLENDER_USER_RESOURCES` points at another installation

**Symptoms:** Blender opens with the wrong preferences or addons; the setup audit warns that `BLENDER_USER_RESOURCES` does not match the portable Blender.

**Cause:** `BLENDER_USER_RESOURCES` overrides the folder Blender uses for preferences, addons, and extensions. It can point at a different Blender installation.

**Fix:**

```powershell
echo $env:BLENDER_USER_RESOURCES
```

If it is set and should not be, remove it for the current user:

```powershell
[Environment]::SetEnvironmentVariable('BLENDER_USER_RESOURCES', $null, 'User')
```

Close and reopen PowerShell and Blender. If you intentionally use the variable, set it to `D:\JewelryStudio\Blender-4.5-LTS\4.5`.

## `get_addon_status` reports a handshake warning

**Symptoms:** `get_addon_status` says `source: error`, `Addon handshake failed`, or `Connection to Blender lost`, but `get_scene_info`, `execute_blender_code`, and `look` work.

**Cause:** The pinned mcp-for-blender 2.2.6 server has a diagnostic handshake quirk with this addon build. The addon's `get_addon_info` command works when called directly, and normal modeling commands work.

**Fix:** Treat it as a diagnostic warning, not a setup failure. Verify the connection with:

> Use get_scene_info and tell me the Blender version.

> Use execute_blender_code to print the Blender version.

If both work, continue. The setup audit checks the port and the addon manifest directly, so it does not depend on this handshake.

## `install-addon` prints `UnicodeEncodeError`

**Symptoms:** the installer prints a traceback ending in `UnicodeEncodeError: 'charmap' codec can't encode character '\u2192'`.

**Cause:** the Windows console code page cannot print the arrow character in the installer's success message. The addon file is usually installed before the message is printed.

**Fix:** set UTF-8 output before running it:

```powershell
$env:PYTHONIOENCODING = 'utf-8'
uvx mcp-for-blender==2.2.6 install-addon
```

Then confirm the file exists:

```powershell
Test-Path "D:\JewelryStudio\Blender-4.5-LTS\4.5\scripts\addons\blender_mcp.py"
```

If it exists, continue with `tools\install-mcp-addon.ps1`.

## Still stuck

Collect:

1. The full `check-setup.ps1` output.
2. The Blender version (`blender.exe --version`).
3. The addon status from OpenCode (`get_addon_status`).
4. The exact error text from OpenCode and from Blender's system console.
5. The script that failed, or the last `BUILT`/`PASS` line that succeeded.

Then open an issue on the repository with those details. Do not paste API keys or personal file paths.

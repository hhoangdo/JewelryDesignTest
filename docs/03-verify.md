# 3. Verify the setup

Do this before building anything. It separates "the toolchain is broken" from "the model needs work".

## 3.1 Run the setup audit

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\check-setup.ps1
```

The script is read-only. It checks:

| Check | PASS means |
|---|---|
| Windows version | Windows 10/11 64-bit |
| PowerShell | 5.1 or newer |
| Git | `git --version` works |
| uvx | `uvx --version` works and the path is recorded |
| Blender | `blender.exe` exists and prints `Blender 4.5.x` |
| JewelCraft | `jewelcraft\blender_manifest.toml` exists in the portable Blender |
| MCP addon | `blender_mcp` extension exists with a valid manifest |
| MCP port | `localhost:9876` accepts a TCP connection |
| OpenCode config | the `blender` MCP entry exists and is enabled |
| uvx path | OpenCode uses an absolute `uvx.exe` path |
| Safe mode | the entry sets `BLENDER_MCP_SAFE_MODE=1` |

Typical output:

```
PASS  Microsoft Windows 11 Home (64-bit) (10.0.26300)
PASS  PowerShell 5.1.26100.9818
PASS  git version 2.54.0.windows.1
PASS  uvx 0.11.7 at C:\Users\you\.local\bin\uvx.exe
PASS  BLENDER_USER_RESOURCES points at the portable Blender
PASS  Blender 4.5.14 LTS at D:\JewelryStudio\Blender-4.5-LTS\blender.exe
PASS  JewelCraft manifest found
PASS  MCP addon extension found
WARN  MCP port 9876 is not listening. Open Blender and click Start MCP Server.
PASS  OpenCode opencode v2.2.5
PASS  OpenCode config has an enabled blender entry
PASS  OpenCode launches: C:/Users/you/.local/bin/uvx.exe mcp-for-blender==2.2.6
PASS  OpenCode uses an absolute uvx path (safe for GUI launches)
PASS  Safe mode is on
PASS  Workshop template, example, scripts, and reference image are present
PASS  Local projects folder exists
```

`WARN` is not a failure. `FAIL` means the step did not complete; fix it before continuing.

## 3.2 Check Blender's GUI

1. Open `D:\JewelryStudio\Blender-4.5-LTS\blender.exe`.
2. Press `N` in the 3D viewport.
3. Confirm the **MCP for Blender** tab exists and its status is connected.
4. Confirm the **JewelCraft** tab exists.
5. If the MCP panel says **Not connected**, click **Start MCP Server**.

Keep Blender open. The MCP server only works while Blender is running.

## 3.3 Check OpenCode's tool list

From the repository root:

```powershell
cd D:\JewelryDesignTest
opencode
```

Ask:

> What Blender MCP tools do you have?

You should see `execute_blender_code`, `get_scene_info`, `get_addon_status`, and `look`. If you only see generic tools, OpenCode has not loaded the MCP server. See [Troubleshooting](TROUBLESHOOTING.md#opencode-does-not-see-blender-tools).

## 3.4 First live MCP test

With Blender open and the MCP server started, ask OpenCode:

> Use get_scene_info and tell me what objects are in the current scene.

Expected: a scene summary with the default Cube, Camera, and Light, or your project's objects. This proves the MCP connection can execute commands in Blender.

Then ask:

> Use execute_blender_code to print the Blender version and the current scene unit scale.

Expected: `4.5.14 LTS` and `1.0`. This proves the AI can run Python in Blender, not just read metadata.

Then ask:

> Use look to send me a viewport screenshot of the current scene.

Expected: an image appears in the chat. This proves the AI can see its own work. If `look` returns an error, see [Troubleshooting](TROUBLESHOOTING.md#look-returns-no-image).

> **Known diagnostic quirk:** `get_addon_status` may report a handshake warning even when the connection works. The pinned 2.2.6 build can fail that diagnostic while `get_scene_info`, `execute_blender_code`, and `look` work normally. Treat it as a warning, not a setup failure. The setup audit checks the port and the addon manifest directly.

## 3.5 Open the template and inspect it

1. In Blender: **File → Open** → `D:\JewelryDesignTest\templates\ring-template.blend`.
2. Ask OpenCode: *Use get_scene_info and tell me the scene unit scale, collections, and materials.*
3. Expected: scene scale `1.0`, length unit `MILLIMETERS`, collections `GEMS` / `METAL` / `REFERENCE`, materials including `Gold_White` and `Gem_Center`.

Do not edit or save the template. It is the starting point for every new project.

## 3.6 Acceptance checklist

- [ ] `check-setup.ps1` has no `FAIL`.
- [ ] Blender shows the MCP-for-Blender panel and the JewelCraft tab.
- [ ] `localhost:9876` accepts connections while Blender is open.
- [ ] OpenCode lists the Blender MCP tools.
- [ ] `get_scene_info` returns the current scene.
- [ ] `execute_blender_code` prints the Blender version.
- [ ] `look` returns a viewport image.
- [ ] The template reports scene scale `1.0` and millimetre units.

When all boxes are checked, continue to [4. Your first project](04-first-project.md).

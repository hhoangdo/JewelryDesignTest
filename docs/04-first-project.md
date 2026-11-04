# 4. Your first project

This is the daily workflow: copy the template, open it in Blender, and let the AI build a model in the new project folder.

## 4.1 Create the project

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\new-project.ps1 -Name first-ring
```

Expected layout:

```
projects\first-ring\
├─ README.md
├─ ring.blend
├─ renders\
└─ scripts\
```

The script refuses to overwrite an existing project.

## 4.2 Open the project in Blender

1. Open Blender.
2. **File → Open** → `D:\JewelryDesignTest\projects\first-ring\ring.blend`.
3. Confirm the title bar shows `ring.blend`, not `ring-template.blend`.

The template contains a camera, a light, the `GEMS` / `METAL` / `REFERENCE` collections, the five starter materials, and a `START-HERE` text block.

## 4.3 Start OpenCode at the repository root

Open a new PowerShell window:

```powershell
cd D:\JewelryDesignTest
opencode
```

Run OpenCode at the **repository root**, not inside the project folder. The AI needs to read `AGENTS.md`, `templates/`, `example-solitaire/`, and the project folder. It will save scripts into the project.

## 4.4 Paste the first prompt

> The project is open at `projects/first-ring/ring.blend`. Build a solitaire ring: US size 7 (17.3 mm inner diameter), 5 mm round brilliant center stone, 6 claw prongs, yellow gold, 2 mm band width. Use the `GEMS` and `METAL` collections. Save each build script to `projects/first-ring/scripts/`, save the scene to `projects/first-ring/ring.blend`, and do not modify the template or the example.

The AI should:

1. Read `AGENTS.md` and inspect the scene with `get_scene_info`.
2. Build the band, stone, prongs, and head in separate scripts.
3. Save the scripts into `projects/first-ring/scripts/`.
4. Use `look` for a viewport screenshot before rendering.
5. Save renders to `projects/first-ring/renders/hero.png`.

## 4.5 Inspect before you render

Ask:

> Use look to send front, top, and three-quarter close-ups of the ring. Check that the prongs grip the stone and that the band is upright.

Look for:

- The band is a closed ring resting on the ground, not a flat disc.
- The stone sits in a head connected to the band, not floating above it.
- Each prong touches the stone near the girdle.
- The stone's table faces up.
- The camera is not clipping the model.

If something is wrong, fix **one** parameter per message. Examples:

> The prongs are too thick. Change the prong diameter to 1.2 mm and re-run the geometry checks.

> The stone is floating. Lower the head until the prong seats touch the band and re-run the checks.

## 4.6 Render the hero

Ask:

> Configure a neutral studio with Cycles, denoise, 1000×1000, and save to `projects/first-ring/renders/hero.png`. Use the GPU if available; otherwise use CPU. Inspect the camera with look before rendering.

Expected: a 1000×1000 PNG over 50 KB. A few-KB file usually means a blank or clipped frame.

## 4.7 Compare and iterate

Open the PNG and compare it with your prompt:

- Does the band read as a ring from the chosen angle?
- Does the stone have visible facets?
- Do the prongs look like claws rather than posts?
- Is the metal color what you asked for?

Change one parameter at a time. Keep every script. The `scripts/` folder is the learning trail, and the `ring.blend` is the current result.

## 4.8 Project hygiene

- `projects/` is ignored by Git. Your experiments stay local.
- The template is read-only in practice. If you damage `ring.blend`, create a fresh project with `new-project.ps1`.
- Do not edit `example-solitaire/` while experimenting; use it as a reference.
- If a render fails, see [Troubleshooting](TROUBLESHOOTING.md#render-is-blank-or-tiny).

Next: [5. Recreate the example](05-recreate-example.md).

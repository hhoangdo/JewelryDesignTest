# Ring template

`ring-template.blend` is the clean starting scene for every project.

## What is in it

| Item | Value |
|---|---|
| Scene scale | `1.0` (1 Blender unit = 1 metre) |
| Units | Metric, millimetres displayed |
| Collections | `GEMS`, `METAL`, `REFERENCE` (empty) |
| Materials | `Gold_Yellow`, `Gold_White`, `Gold_Rose`, `Silver`, `Gem_Center` |
| Camera | 55 mm lens at `(0.055, -0.038, 0.032)`, aimed at `(0, 0, 0.013)` |
| Light | A single 10 W point light, converted to a softbox by `studio_render.py` |
| Render | Cycles, denoise on, 1000 × 1000 |
| Text block | `START-HERE` with the unit convention |

There is no default cube and no stray material.

## How to use it

Do not open and save over the template. Create a project copy:

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\new-project.ps1 -Name first-ring
```

That copies the template to `projects\first-ring\ring.blend` and creates `scripts\` and `renders\`.

## Unit convention

Design in millimetres, then divide by 1000 for Blender coordinates. A 21.7 mm band is `0.0217` Blender units. The scene scale stays `1.0`. The old template used `scale_length = 0.001` together with a ÷1000 conversion, which applied the conversion twice; do not recreate that combination.

## Regenerating the template

The checked-in file was produced by `make_template.py`. To rebuild it:

```powershell
& "D:\JewelryStudio\Blender-4.5-LTS\blender.exe" --background --factory-startup `
  --python templates\make_template.py
```

Expected output:

```
TEMPLATE SAVED .../templates/ring-template.blend
SCALE 1.0 LEN MILLIMETERS
OBJECTS [('Camera', 'CAMERA'), ('Light', 'LIGHT')]
COLLS [('GEMS', 0), ('METAL', 0), ('REFERENCE', 0)]
MATS ['Gem_Center', 'Gold_Rose', 'Gold_White', 'Gold_Yellow', 'Silver']
```

The generator is a maintainer tool, not part of the beginner workflow. It uses `__file__` to find the repository root, so run it from a clone with the `templates` folder in place.

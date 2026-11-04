# AGENTS.md — Jewelry Studio

These rules apply when an AI agent works in this repository.

## Scope

- Work only inside `projects/<name>/`.
- Never modify `templates/`, `example-solitaire/`, or another project unless the user explicitly asks.
- `projects/` is gitignored. Do not try to commit it.

## Fresh machine setup

When the user is setting up a new machine, use [START-HERE.md](START-HERE.md) as the entry point. Inspect the machine, present a plan, and wait for approval before installing anything.

## Scene conventions

- Metric units, millimetres displayed.
- `scene.unit_settings.scale_length = 1.0`.
- Design in millimetres; divide by 1000 for Blender coordinates.
- Collections: `GEMS` for stones, `METAL` for metal, `REFERENCE` for reference objects.
- Starter materials: `Gold_Yellow`, `Gold_White`, `Gold_Rose`, `Silver`, `Gem_Center`.

## Workflow

1. Inspect the live scene with `get_scene_info` before changing it.
2. Build in stages: band → stone → head → claws → studio.
3. Save each stage as a script in `projects/<name>/scripts/`. The script is the deliverable; the `.blend` is the current result.
4. Change **one** independent parameter per follow-up. Name the old and new values.
5. Before rendering, inspect close-ups with `look` (front, top, three-quarter).
6. Save renders to `projects/<name>/renders/hero.png`.
7. Run the project's verification checks after each geometry stage.

## Blender-side safety

- Use only `bpy`, `math`, and `mathutils` in Blender scripts.
- Do not use `os`, `open`, filesystem access, preferences, or external libraries inside Blender.
- Do not disable safe mode or telemetry settings.
- Look up shader nodes by type, never by localized name.
- Read enum identifiers from RNA or the rejected-assignment message; do not guess.
- Keep the scene scale at `1.0`; do not "fix" sizes by changing it.

## Geometry checks

- Band: 21.7 mm OD, 17.3 mm ID, bottom at Z = 0.
- Stone: closed shell, positive volume, planar upward table, exactly one gem in `GEMS`.
- Head: four closed arms, two shoulders, no rail/foot/ball-tip objects.
- Claws: actual mesh contact with the stone, inward-curving tips, no floating tips.
- Studio: camera clipping encloses the ring, 1000×1000, Cycles, denoise.

## Honesty

- Say "visual model", not "casting-ready".
- Record remaining differences from the reference.
- Do not claim a check passed unless the command actually ran and printed `PASS`.

# Glossary

Plain-English definitions for beginners. No prior jewelry or Blender knowledge is assumed.

## Jewelry terms

| Term | Meaning |
|---|---|
| **Shank** | The ring's band — the part that wraps around your finger |
| **Prong / claw** | The metal fingers that hold a gemstone in place |
| **Gem seat** | The recess cut into the metal where the stone sits |
| **Girdle** | The rim around a cut gemstone where the prongs grip it |
| **Head / setting** | The assembly of seat, arms, and prongs that holds the stone |
| **Gallery** | The open space under the stone, between the head and the band |
| **Solitaire** | A ring with one center stone |
| **Trilogy** | Three stones side by side (often past–present–future) |
| **Signet** | A ring with a flat, engraved face |
| **Milgrain** | Tiny beaded metal decoration along an edge |
| **Carat (ct)** | Gemstone weight; 1 ct = 0.2 g. "Points" are hundredths of a carat |
| **US size** | Ring sizing scale; US 7 ≈ 17.3 mm inner diameter |
| **Alloy** | Metal mix, e.g. 18k yellow gold = 75% gold plus copper/silver |
| **Comfort fit** | A band with a rounded inner profile that is easier to slide on |
| **Pavé** | A surface set with many small stones |
| **Halo** | A ring of small stones around the center stone |

## Blender terms

| Term | Meaning |
|---|---|
| **Mesh** | A 3D shape made of vertices, edges, and faces |
| **Vertex / edge / face** | A point / a line between two points / a flat polygon |
| **Bevel** | Softening or chamfering a hard edge — the polished-metal look |
| **Extrude (E)** | Pulling new geometry out of selected faces or edges |
| **Modifier** | A non-destructive effect on an object (Solidify, Subdivision, Bevel…) |
| **Manifold** | A closed, solid shape with no holes in its surface |
| **Normal** | The direction a face points; used for lighting and inside/outside checks |
| **Shading** | How faces react to light: flat (faceted) or smooth (rounded) |
| **.blend** | Blender's project file: models, materials, scene, settings |
| **STL / 3MF** | Neutral 3D file formats for export and printing |
| **EEVEE** | Blender's fast real-time renderer; good for previews |
| **Cycles** | Blender's physically based path tracer; used for final renders |
| **OptiX / HIP / oneAPI** | GPU acceleration backends for NVIDIA / AMD / Intel |
| **HDRI** | An environment image that lights the scene and appears in reflections |
| **Material** | The surface recipe: color, metalness, roughness, transmission |
| **Collection** | A folder for organizing objects; this repo uses `GEMS`, `METAL`, `REFERENCE` |
| **Scene scale** | How many metres one Blender unit represents; this repo uses `1.0` |
| **Background mode** | Running Blender without a window, usually from the command line |

## Workflow terms

| Term | Meaning |
|---|---|
| **MCP** | Model Context Protocol — the standard that lets the AI call tools |
| **mcp-for-blender** | The server that translates MCP calls into Blender commands |
| **bpy** | Blender's Python API — how the AI writes 3D code |
| **`look`** | MCP tool that returns a viewport screenshot so the AI can inspect its work |
| **Safe mode** | Restricts Blender scripts to modeling-only Python (`bpy`, `math`, `mathutils`) |
| **JewelCraft** | Free jewelry addon: gems, prongs, cutters, spacing, weight calculation |
| **Headless** | Running Blender from the command line with `--background` |
| **OpenCode** | The terminal agent client used in this guide |

## Terms specific to this repository

| Term | Meaning |
|---|---|
| **Workshop** | The whole repository: setup docs, templates, example, tools, and your projects |
| **Setup** | The installed Blender + JewelCraft + MCP addon + OpenCode configuration |
| **Template** | `templates/ring-template.blend`, the clean starting scene |
| **Project** | A folder under `projects/<name>/` containing one `ring.blend` and its scripts/renders |
| **Example** | `example-solitaire/`, the single finished ring you can inspect and rebuild |
| **Replay** | Running the example's five scripts in order to reproduce it deterministically |
| **AI rebuild** | Creating a fresh project and asking the AI to recreate the example from the reference |
| **Hero** | The final 1000×1000 render saved as `renders/hero.png` |
| **One-parameter iteration** | Changing exactly one named value per follow-up, then re-checking |

## Units in this repo

| Term | Meaning |
|---|---|
| **Millimetre display** | Blender's UI shows millimetres |
| **Scene scale 1.0** | One Blender unit = one metre |
| **Design millimetres** | Dimensions are written in mm, then divided by 1000 for Blender coordinates |
| **Double conversion** | The old bug where `scale_length = 0.001` was combined with an extra ÷1000 |

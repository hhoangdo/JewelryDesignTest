# Resources

All resources here are free. The paid tiers of anything are not required.

## Blender basics

- **Official manual** — <https://docs.blender.org/manual/>. Search beats tutorials; bookmark it.
- **Blender keyboard cheat sheet** — <https://www.blender.org/download/> (the PDF link is on the download page).
- **Blender requirements** — <https://www.blender.org/download/requirements/>.

Essential keys only:

| Key | Action |
|---|---|
| Middle mouse drag | Orbit |
| Shift + middle mouse | Pan |
| Scroll | Zoom |
| G / R / S | Move / rotate / scale |
| Tab | Edit mode |
| E | Extrude |
| Ctrl+Z | Undo |
| Ctrl+S | Save |
| Z | Shading pie |
| N | Sidebar |
| Numpad 1 / 3 / 7 | Front / right / top views |

## Jewelry-specific

- **JewelCraft repository** — <https://github.com/mrachinskiy/jewelcraft>. README, video links, release notes, and the issue tracker.
- **JewelCraft workflows**: Add Gem, gem map, prongs, cutters, Distribute/Spacing, and Weighting. The Weighting menu can estimate metal weight once your model has real thickness.
- **Reference sizing**: US 7 ≈ 17.3 mm inner diameter. Always verify sizing before production.

## MCP and OpenCode

- **mcp-for-blender documentation** — <https://www.mcp-for-blender.com/docs>. Installation, MCP client setup, troubleshooting, and the addon changelog.
- **mcp-for-blender repository** — <https://github.com/ahujasid/mcp-for-blender>.
- **OpenCode documentation** — <https://opencode.ai/docs/>. Installation, providers, MCP servers, and the CLI.
- **OpenCode MCP servers** — <https://opencode.ai/docs/mcp-servers/>.

## Assets and lighting

- **Poly Haven** — <https://polyhaven.com/>. Free CC0 HDRIs, textures, and models. The MCP addon can search and import Poly Haven assets directly.
- **Blender Studio** — <https://studio.blender.org/>. Free training and production files.

## Rendering

- Use **EEVEE** for quick viewport previews and **Cycles** for finals.
- Cycles GPU is fastest with OptiX (NVIDIA), HIP (AMD), or oneAPI (Intel). CPU rendering works everywhere; lower the samples for drafts.
- The example uses 256 samples, denoising, and a neutral three-softbox studio.

## When stuck

1. Press `Ctrl+Z` in Blender.
2. Reopen the last saved `.blend`.
3. Run `tools/check-setup.ps1`.
4. Read [Troubleshooting](TROUBLESHOOTING.md).
5. Look at `example-solitaire/scripts/` — errors usually trace to one parameter.
6. Ask the AI with the exact error text and the last successful `BUILT`/`PASS` line.

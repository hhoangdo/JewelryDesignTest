# Example brief — reference solitaire

Use this brief in a new project, with `example-solitaire/reference/target.jpg` attached to the chat.

> Build a white-gold, US 7, four-prong cushion solitaire that matches the attached reference as closely as possible.
>
> **Band:** 21.7 mm outer diameter, 17.3 mm inner diameter (US 7), 2.2 mm rounded comfort section, upright in the XZ plane, bottom at Z = 0. Use `Gold_White` in the `METAL` collection.
>
> **Stone:** one 5.5 mm rounded-square cushion in the `GEMS` collection. Table 67% of the girdle width (3.685 mm), crown 0.6 mm, girdle 0.10 mm, pavilion 2.4 mm, total height 3.1 mm. Girdle center 3.5 mm above the band top (Z = 25.2 mm). Build a real multi-tier cut with star, bezel, upper-girdle, pavilion-main, and lower-girdle facets; closed shell, planar table facing up. Use `Gem_Center` with IOR 2.417 and transmission 1.0.
>
> **Head:** four slender sculpted V-arms rising from a compact shoulder, with an open pavilion. No full donut/gallery rail, no conical foot, no separate ball-tip prongs. Integrate the claws into the arms, curve them inward over the crown, and check actual mesh contact with the stone.
>
> **Studio:** neutral bright three-quarter view exposing the table, V-head, shoulder, and band opening. Three broad softboxes, a neutral world, a matte light-grey ground, and a reflection-only dark contrast card. Cycles, denoise, 1000 × 1000, PNG.
>
> **Process:** build one stage at a time — band, stone, head, claws, studio. Change one independent parameter per iteration. Inspect with `look` before every render. Save each script in `projects/<name>/scripts/` and the final render in `projects/<name>/renders/hero.png`.
>
> This is a visual model, not a manufacturing/casting certification.

## Units

- Scene: metric, millimetres displayed, `scale_length = 1.0`.
- Design dimensions are millimetres; divide by 1000 for Blender coordinates.
- Do not combine `scale_length = 0.001` with a second ÷1000 conversion. That was the old double-conversion bug.

## What "good" looks like

- The cushion outline is a softened square, not a circle or a beveled cube.
- The table is flat and bright; the crown and pavilion facets are readable.
- The V-head is open; the stone does not sit on a solid pedestal.
- The claws are slender, continuous with the arms, and touch the stone.
- The band is round and continuous, with a believable polished-metal reflection.

## Known limits

The reference is a single photograph, so the hidden pavilion and internal setting geometry are inferred. The example is an honest visual match, not an exact replica. See the "Known differences" section in [README.md](README.md).

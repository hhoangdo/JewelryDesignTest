"""Closed cushion brilliant: planar bezels/stars, fine girdle and pavilion facets."""
# pyright: reportMissingImports=false
import bpy
import math

WIDTH_MM = 5.5
TABLE_RATIO = 0.67
CROWN_MM = 0.6
GIRDLE_MM = 0.10
PAVILION_MM = 2.4
GIRDLE_RISE_MM = 3.5
CUSHION_EXPONENT = 3.5
SAMPLES = 64
TAG = "jewelry_studio_generated"


def outline(angle: float):
    c, s = math.cos(angle), math.sin(angle)
    power = 2.0 / CUSHION_EXPONENT
    half = WIDTH_MM / 2
    return (
        math.copysign(abs(c) ** power, c) * half,
        math.copysign(abs(s) ** power, s) * half,
    )


def facet_intersection(index: int, radial_scale: float, height: float):
    # Intersect adjacent main-facet planes at a fixed height. This makes
    # every four-sided bezel/pavilion main planar, unlike twisted quads.
    a, b = index * math.pi / 4, (index + 1) * math.pi / 4
    ax, ay, bx, by = math.cos(a), math.sin(a), math.cos(b), math.sin(b)
    ra, rb = math.hypot(*outline(a)) * radial_scale, math.hypot(*outline(b)) * radial_scale
    determinant = ax * by - ay * bx
    return (
        (ra * by - ay * rb) / determinant,
        (ax * rb - ra * bx) / determinant,
        height,
    )


def diamond_material():
    material = bpy.data.materials.get("Gem_Center")
    if material is None:
        material = bpy.data.materials.new("Gem_Center")
    material.use_nodes = True
    material.use_fake_user = True
    node = next(n for n in material.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    for key, value in (
        ("Base Color", (1, 1, 1, 1)),
        ("Metallic", 0),
        ("Roughness", 0.02),
        ("IOR", 2.417),
        ("Transmission Weight", 1),
    ):
        node.inputs[key].default_value = value
    return material


def build_gem() -> None:
    assert bpy.data.filepath.endswith("ring.blend"), "Save the project as ring.blend first"
    assert "ring-template" not in bpy.data.filepath, "Build in a project copy, not the template"
    scene = bpy.context.scene
    assert scene.unit_settings.scale_length == 1.0, "Scene scale must be 1.0, not 0.001"
    assert "band_top_mm" in scene, "Run build_band.py first"
    gz = float(scene["band_top_mm"]) + GIRDLE_RISE_MM
    upper, lower = GIRDLE_MM / 2, -GIRDLE_MM / 2

    vertices = []
    for height in (upper, lower):
        for i in range(SAMPLES):
            x, y = outline(i * 2 * math.pi / SAMPLES)
            vertices.append((x, y, height))
    table_start = len(vertices)
    for i in range(8):
        x, y = outline(i * math.pi / 4)
        vertices.append((x * TABLE_RATIO, y * TABLE_RATIO, upper + CROWN_MM))
    crown_start = len(vertices)
    for i in range(8):
        vertices.append(
            facet_intersection(
                i,
                1 - 0.55 * (1 - TABLE_RATIO),
                upper + CROWN_MM * 0.55,
            )
        )
    pavilion_start = len(vertices)
    for i in range(8):
        vertices.append(facet_intersection(i, 0.5, lower - PAVILION_MM * 0.5))
    culet = len(vertices)
    vertices.append((0, 0, lower - PAVILION_MM))

    faces = [tuple(table_start + i for i in range(8))]
    for i in range(8):
        nxt, prev = (i + 1) % 8, (i - 1) % 8
        gi = i * (SAMPLES // 8)
        faces.append((table_start + i, crown_start + i, table_start + nxt))
        faces.append((table_start + i, crown_start + prev, gi, crown_start + i))
        faces.append((SAMPLES + gi, pavilion_start + prev, culet, pavilion_start + i))
        for j in range(SAMPLES // 8):
            a, b = (gi + j) % SAMPLES, (gi + j + 1) % SAMPLES
            faces.append((a, b, crown_start + i))
            faces.append((SAMPLES + b, SAMPLES + a, pavilion_start + i))
    for i in range(SAMPLES):
        j = (i + 1) % SAMPLES
        faces.append((SAMPLES + i, SAMPLES + j, j, i))

    old = bpy.data.objects.get("CenterStone_Cushion55")
    if old is not None:
        assert old.get(TAG) or old.get("v2_generated"), "Refusing to replace an unrecognized stone"
        old_mesh = old.data
        bpy.data.objects.remove(old, do_unlink=True)
        if old_mesh.users == 0:
            bpy.data.meshes.remove(old_mesh)

    mesh = bpy.data.meshes.new("CushionBrilliant")
    mesh.from_pydata([tuple(c / 1000 for c in v) for v in vertices], [], faces)
    mesh.update()
    for polygon in mesh.polygons:
        polygon.use_smooth = False
    stone = bpy.data.objects.new("CenterStone_Cushion55", mesh)
    bpy.data.collections["GEMS"].objects.link(stone)
    stone.location.z = gz / 1000
    stone[TAG] = True
    for key, value in (
        ("girdle_width_mm", WIDTH_MM),
        ("table_ratio", TABLE_RATIO),
        ("crown_height_mm", CROWN_MM),
        ("girdle_thickness_mm", GIRDLE_MM),
        ("pavilion_depth_mm", PAVILION_MM),
        ("girdle_z_mm", gz),
        ("cushion_exponent", CUSHION_EXPONENT),
    ):
        stone[key] = value
    stone["seat_points_mm"] = [
        c for i in (1, 3, 5, 7) for c in (*outline(i * math.pi / 4), gz)
    ]
    stone["table_corner_points_mm"] = [
        c
        for i in (1, 3, 5, 7)
        for c in (
            vertices[table_start + i][0],
            vertices[table_start + i][1],
            gz + upper + CROWN_MM,
        )
    ]
    mesh.materials.append(diamond_material())
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print(
        f"BUILT cushion: {WIDTH_MM} mm, table {TABLE_RATIO * 100:.0f}%, "
        f"crown {CROWN_MM} mm, {len(faces)} facets; girdle Z {gz:.3f} mm"
    )


build_gem()

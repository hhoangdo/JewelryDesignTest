"""Read-only, staged checks for the reference solitaire. Run in Blender."""
# pyright: reportMissingImports=false
import bpy
import math
from mathutils import Vector
from mathutils.geometry import closest_point_on_tri

STAGE = "all"
TAG = "jewelry_studio_generated"
PROJECT_DIR = bpy.data.filepath.replace("\\", "/").rsplit("/", 1)[0]
HERO = PROJECT_DIR + "/renders/hero.png"


def world_vertices(obj):
    return [obj.matrix_world @ v.co for v in obj.data.vertices]


def verify_band() -> None:
    scene = bpy.context.scene
    band = bpy.data.objects.get("Band_WhiteGold")
    assert band is not None, "Missing band"
    assert scene.unit_settings.scale_length == 1.0, "Double mm conversion: scene scale must be 1"
    points = world_vertices(band)
    zmin, zmax = min(v.z for v in points), max(v.z for v in points)
    diameter = (zmax - zmin) * 1000
    center = (zmin + zmax) / 2
    inner = 2 * min(math.hypot(v.x, v.z - center) for v in points) * 1000
    assert abs(diameter - 21.7) < 0.01, f"Band OD {diameter} mm"
    assert abs(inner - 17.3) < 0.01, f"Band ID {inner} mm"
    assert abs(zmin * 1000) < 0.01, "Band no longer rests at Z=0"
    assert band.name in bpy.data.collections["METAL"].objects
    assert band.data.materials[0].name == "Gold_White"
    for prefix in ("band_", "v2_band_"):
        vertices_key = prefix + "vertices"
        if vertices_key in scene:
            assert [float(c) for v in band.data.vertices for c in v.co] == list(
                scene[vertices_key]
            ), "Band vertices changed"
            assert [i for p in band.data.polygons for i in p.vertices] == list(
                scene[prefix + "indices"]
            ), "Band topology changed"
            assert [float(c) for row in band.matrix_world for c in row] == list(
                scene[prefix + "matrix"]
            ), "Band transform changed"
            break
    print(
        f"PASS band: OD {diameter:.4f} mm, ID {inner:.4f} mm; "
        f"scene scale 1; band geometry checked"
    )


def verify_gem() -> None:
    gems = bpy.data.collections["GEMS"]
    assert len(gems.objects) == 1, f"Expected exactly one gem, found {len(gems.objects)}"
    stone = bpy.data.objects["CenterStone_Cushion55"]
    assert stone.name in gems.objects
    assert abs(stone.dimensions.x * 1000 - 5.5) < 0.01
    assert abs(stone.dimensions.y * 1000 - 5.5) < 0.01
    assert abs(stone.dimensions.z * 1000 - 3.1) < 0.01
    points = world_vertices(stone)
    zmin, zmax = min(v.z for v in points), max(v.z for v in points)
    assert abs(zmin * 1000 - 22.75) < 0.01
    assert abs(zmax * 1000 - 25.85) < 0.01
    assert abs(stone.location.z * 1000 - 25.2) < 0.01
    table = [
        p
        for p in stone.data.polygons
        if all(abs(points[i].z - zmax) < 1e-7 for i in p.vertices)
    ]
    assert len(table) == 1 and table[0].normal.z > 0.99, "Table winding/planarity incorrect"
    table_x = [points[i].x for i in table[0].vertices]
    assert abs((max(table_x) - min(table_x)) * 1000 - 3.685) < 0.01
    assert sum(abs(p.z * 1000 - 25.25) < 0.01 for p in points) >= 64, (
        "Missing upper girdle/crown datum"
    )
    assert all(math.isfinite(c) for p in points for c in p)
    incidences = {}
    for polygon in stone.data.polygons:
        ids = list(polygon.vertices)
        assert polygon.area > 1e-16, "Degenerate facet"
        for a, b in zip(ids, ids[1:] + ids[:1]):
            edge = tuple(sorted((a, b)))
            incidences[edge] = incidences.get(edge, 0) + 1
    assert all(n == 2 for n in incidences.values()), "Open/non-manifold gem"
    stone.data.calc_loop_triangles()
    volume = 0.0
    for tri in stone.data.loop_triangles:
        a, b, c = [stone.data.vertices[i].co for i in tri.vertices]
        volume += a.dot(b.cross(c)) / 6
    assert volume > 1e-12, "Inverted gem shell"
    assert len(stone.data.polygons) > 100, "Cut still lacks fine multi-tier faceting"
    assert len(stone["seat_points_mm"]) == len(stone["table_corner_points_mm"]) == 12
    material = stone.data.materials[0]
    assert material.name == "Gem_Center"
    node = next(n for n in material.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    assert abs(node.inputs["IOR"].default_value - 2.417) < 0.0001
    assert node.inputs["Transmission Weight"].default_value == 1.0
    assert node.inputs["Metallic"].default_value == 0.0
    print(
        f"PASS gem: 5.5x5.5x3.1 mm; table 3.685 mm; crown .6 mm; "
        f"{len(stone.data.polygons)} closed outward facets; "
        f"clearance {zmin * 1000 - 21.7:.2f} mm"
    )


def verify_head(require_claws: bool = False) -> None:
    arms = [
        o
        for o in bpy.data.collections["METAL"].objects
        if o.name.startswith("HeadArm_")
    ]
    assert len(arms) == 4, f"Expected four sculpted arms, found {len(arms)}"
    assert all(o.data.materials[0].name == "Gold_White" for o in arms)
    assert bpy.data.objects.get("Shoulder_Left") is not None
    assert bpy.data.objects.get("Shoulder_Right") is not None
    assert bpy.data.objects.get("Gallery_Rail") is None
    assert bpy.data.objects.get("Basket_Foot") is None
    assert not any(o.name.startswith("ProngTip_") for o in bpy.data.objects)
    for arm in arms:
        incidence = {}
        for polygon in arm.data.polygons:
            ids = list(polygon.vertices)
            for a, b in zip(ids, ids[1:] + ids[:1]):
                edge = tuple(sorted((a, b)))
                incidence[edge] = incidence.get(edge, 0) + 1
        assert all(n == 2 for n in incidence.values()), "Open metal arm"
        assert all(math.isfinite(c) for v in world_vertices(arm) for c in v)
    print(
        "PASS head: four closed tapered V-arms, two compact shoulders, "
        "white metal; no rail/foot/ball tips"
    )
    if require_claws:
        stone = bpy.data.objects["CenterStone_Cushion55"]
        gem_points = world_vertices(stone)
        stone.data.calc_loop_triangles()
        triangles = [
            [gem_points[i] for i in t.vertices] for t in stone.data.loop_triangles
        ]
        table_z = max(p.z for p in gem_points)
        errors = []
        for arm in arms:
            assert arm["include_claws"], "Missing integrated curved claws"
            metal = world_vertices(arm)
            assert max(p.z for p in metal) <= table_z + 0.00015, "Claw too high above table"
            for key in ("seat_vertex_indices", "tip_vertex_indices"):
                contact = [metal[i] for i in arm[key]]
                distance = min(
                    (p - closest_point_on_tri(p, *tri)).length
                    for p in contact
                    for tri in triangles
                )
                assert distance <= 0.00008, f"Floating {key}: {distance * 1000:.3f} mm"
                errors.append(distance * 1000)
            tip = Vector(
                tuple(
                    sum(metal[i][axis] for i in arm["tip_vertex_indices"])
                    / len(arm["tip_vertex_indices"])
                    for axis in range(3)
                )
            )
            seat = Vector(
                tuple(
                    sum(metal[i][axis] for i in arm["seat_vertex_indices"])
                    / len(arm["seat_vertex_indices"])
                    for axis in range(3)
                )
            )
            assert math.hypot(tip.x, tip.y) < math.hypot(seat.x, seat.y) - 0.0005, (
                "Claw does not curve inward"
            )
            assert abs(tip.z - table_z) < 0.00015, "Tip not tucked onto table edge"
        print(
            f"PASS claws: 4 integrated hooks, actual seat/tip mesh contact "
            f"<= {max(errors):.4f} mm; low table-edge tips"
        )


def verify_studio() -> None:
    scene = bpy.context.scene
    assert scene.render.filepath.replace("\\", "/") == HERO, "Hero targets the wrong project"
    assert scene.render.engine.lower() == "cycles"
    assert scene.cycles.use_denoising
    assert scene.render.resolution_x == scene.render.resolution_y == 1000
    assert scene.render.resolution_percentage == 100
    assert all(
        p.use_smooth for p in bpy.data.objects["Band_WhiteGold"].data.polygons
    ), "Band render normals still faceted"
    camera = scene.camera
    assert camera is not None
    assert camera.location.x > 0 and camera.location.y < 0 and camera.location.z > 0.02585
    stone = bpy.data.objects["CenterStone_Cushion55"]
    table_z = max(p.z for p in world_vertices(stone))
    table_angle = math.degrees(
        math.atan2(
            camera.location.z - table_z,
            math.hypot(camera.location.x, camera.location.y),
        )
    )
    assert 28 <= table_angle <= 36, (
        f"Reference table/V-head balance incorrect: {table_angle:.2f} degrees"
    )
    inverse = camera.matrix_world.inverted()
    points = [
        inverse @ p
        for name in ("GEMS", "METAL")
        for obj in bpy.data.collections[name].objects
        for p in world_vertices(obj)
    ]
    depths = [-p.z for p in points]
    assert camera.data.clip_start < min(depths) and max(depths) < camera.data.clip_end
    xs = [
        p.x / (-p.z * camera.data.sensor_width / camera.data.lens / 2) for p in points
    ]
    ys = [
        p.y / (-p.z * camera.data.sensor_width / camera.data.lens / 2) for p in points
    ]
    assert max(abs(v) for v in xs + ys) < 0.98, "Model clipped by camera frame"
    coverage = (max(ys) - min(ys)) / 2
    assert 0.75 <= coverage <= 0.96, f"Hero framing too loose/tight: {coverage:.3f}"
    print(
        f"PASS studio: Cycles, denoise, 1000x1000, valid clipping; "
        f"vertical coverage {coverage:.1%}"
    )


verify_band()
if STAGE != "band":
    verify_gem()
if STAGE in ("head", "claws", "all"):
    verify_head(STAGE != "head")
if STAGE == "all":
    verify_studio()

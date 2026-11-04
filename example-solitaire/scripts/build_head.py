"""Swept elliptical V-arms and shoulders, with integrated hooked claws."""
# pyright: reportMissingImports=false
import bpy
import math
from mathutils import Vector

INCLUDE_CLAWS = True
ROOT_WIDTH_MM = 1.05
ROOT_DEPTH_MM = 0.55
SEAT_WIDTH_MM = 0.45
SEAT_DEPTH_MM = 0.40
CLAW_WIDTH_MM = 0.30
TIP_WIDTH_MM = 0.22
SECTIONS = 20
ARM_STEPS = 40
CLAW_STEPS = 24
TAG = "jewelry_studio_generated"


def bezier(control, t: float):
    return (
        (1 - t) ** 3 * control[0]
        + 3 * (1 - t) ** 2 * t * control[1]
        + 3 * (1 - t) * t ** 2 * control[2]
        + t ** 3 * control[3]
    )


def sweep(name: str, points, widths, depths, reference):
    vertices, faces = [], []
    for i, point in enumerate(points):
        tangent = (
            points[min(i + 1, len(points) - 1)] - points[max(i - 1, 0)]
        ).normalized()
        u = (reference - tangent * reference.dot(tangent)).normalized()
        v = tangent.cross(u).normalized()
        for j in range(SECTIONS):
            angle = j * 2 * math.pi / SECTIONS
            position = (
                point
                + u * (widths[i] / 2 * math.cos(angle))
                + v * (depths[i] / 2 * math.sin(angle))
            )
            vertices.append(tuple(position / 1000))
    faces.append(tuple(reversed(range(SECTIONS))))
    for i in range(len(points) - 1):
        for j in range(SECTIONS):
            k = (j + 1) % SECTIONS
            faces.append(
                (
                    i * SECTIONS + j,
                    i * SECTIONS + k,
                    (i + 1) * SECTIONS + k,
                    (i + 1) * SECTIONS + j,
                )
            )
    faces.append(tuple((len(points) - 1) * SECTIONS + j for j in range(SECTIONS)))
    mesh = bpy.data.meshes.new("Swept_" + name)
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    for face in mesh.polygons:
        face.use_smooth = True
    mesh.materials.append(bpy.data.materials["Gold_White"])
    obj = bpy.data.objects.new(name, mesh)
    bpy.data.collections["METAL"].objects.link(obj)
    obj[TAG] = True
    return obj


def build_head() -> None:
    assert bpy.data.filepath.endswith("ring.blend"), "Save the project as ring.blend first"
    assert "ring-template" not in bpy.data.filepath, "Build in a project copy, not the template"
    scene = bpy.context.scene
    stone = bpy.data.objects["CenterStone_Cushion55"]
    top = float(scene["band_top_mm"])
    seats, tables = list(stone["seat_points_mm"]), list(stone["table_corner_points_mm"])
    names = [f"HeadArm_{i:02d}" for i in range(1, 5)] + [
        "Shoulder_Left",
        "Shoulder_Right",
    ]
    for name in names:
        old = bpy.data.objects.get(name)
        if old is not None:
            assert old.get(TAG) or old.get("v2_generated"), f"Unrecognized metal object: {name}"
            mesh = old.data
            bpy.data.objects.remove(old, do_unlink=True)
            if mesh.users == 0:
                bpy.data.meshes.remove(mesh)

    for i in range(4):
        seat = Vector(seats[i * 3 : i * 3 + 3])
        table = Vector(tables[i * 3 : i * 3 + 3])
        sx, sy = math.copysign(1, seat.x), math.copysign(1, seat.y)
        radial = Vector((seat.x, seat.y, 0)).normalized()
        end = seat + radial * 0.18 + Vector((0, 0, -0.07))
        control = [
            Vector((sx * 0.36, sy * 0.18, top - 0.18)),
            Vector((sx * 0.60, sy * 0.30, top + 0.55)),
            Vector((seat.x * 0.9, seat.y * 0.9, seat.z - 0.60)),
            end,
        ]
        points = [bezier(control, j / ARM_STEPS) for j in range(ARM_STEPS + 1)]
        widths = [
            ROOT_WIDTH_MM + (SEAT_WIDTH_MM - ROOT_WIDTH_MM) * (j / ARM_STEPS)
            for j in range(ARM_STEPS + 1)
        ]
        depths = [
            ROOT_DEPTH_MM + (SEAT_DEPTH_MM - ROOT_DEPTH_MM) * (j / ARM_STEPS)
            for j in range(ARM_STEPS + 1)
        ]
        if INCLUDE_CLAWS:
            tip = table - radial * 0.03 + Vector((0, 0, 0.025))
            claw = [
                end,
                end + radial * 0.02 + Vector((0, 0, 0.52)),
                table + radial * 0.15 + Vector((0, 0, 0.11)),
                tip,
            ]
            for j in range(1, CLAW_STEPS + 1):
                t = j / CLAW_STEPS
                points.append(bezier(claw, t))
                width = CLAW_WIDTH_MM + (TIP_WIDTH_MM - CLAW_WIDTH_MM) * t
                rounding = math.sqrt(
                    max(0.0025, 1 - max(0, (t - 0.85) / 0.15) ** 2)
                )
                widths.append(width * rounding)
                depths.append((0.28 - 0.08 * t) * rounding)
        obj = sweep(
            names[i],
            points,
            widths,
            depths,
            Vector((-radial.y, radial.x, 0)),
        )
        obj["include_claws"] = INCLUDE_CLAWS
        obj["seat_vertex_indices"] = list(
            range(ARM_STEPS * SECTIONS, (ARM_STEPS + 1) * SECTIONS)
        )
        obj["tip_vertex_indices"] = list(
            range((len(points) - 1) * SECTIONS, len(points) * SECTIONS)
        )

    for name, sign in (("Shoulder_Left", -1), ("Shoulder_Right", 1)):
        control = [
            Vector((sign * 2.6, 0, top - 0.44)),
            Vector((sign * 1.8, 0, top + 0.10)),
            Vector((sign * 0.7, 0, top + 0.30)),
            Vector((sign * 0.35, 0, top + 0.20)),
        ]
        points = [bezier(control, j / 24) for j in range(25)]
        sweep(
            name,
            points,
            [1.0 - 0.3 * j / 24 for j in range(25)],
            [0.35 + 0.20 * j / 24 for j in range(25)],
            Vector((0, 1, 0)),
        )

    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print(
        f"BUILT 4 sculpted V-arms + 2 compact shoulders; "
        f"integrated claws={INCLUDE_CLAWS}; no rail or cone"
    )


build_head()

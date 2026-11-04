"""Build the comfort-fit band and save the project.

Scene convention: metric, millimetres displayed, scale_length = 1.0.
Design dimensions are in millimetres and divided by 1000 for Blender units.
"""
# pyright: reportMissingImports=false
import bpy
import math

BAND_MAJOR_MM = 9.75
BAND_MINOR_MM = 1.1
BAND_TOP_MM = 21.7
TAG = "jewelry_studio_generated"


def ensure_units() -> None:
    scene = bpy.context.scene
    units = scene.unit_settings
    systems = units.bl_rna.properties["system"].enum_items
    units.system = next(i.identifier for i in systems if i.name.lower() == "metric")
    try:
        units.length_unit = "MILLIMETERS"
    except (TypeError, ValueError):
        try:
            units.length_unit = ""
        except (TypeError, ValueError) as error:
            valid = str(error).split("'")[1::2]
            units.length_unit = next(i for i in valid if i.lower().startswith("milli"))
    units.scale_length = 1.0


def move_to(obj, collection) -> None:
    try:
        obj.users_collection[0].objects.unlink(obj)
    except (IndexError, RuntimeError):
        pass
    if obj.name not in collection.objects:
        collection.objects.link(obj)


def build_band() -> None:
    assert bpy.data.filepath.endswith("ring.blend"), "Save the project as ring.blend first"
    assert "ring-template" not in bpy.data.filepath, "Build in a project copy, not the template"
    ensure_units()
    scene = bpy.context.scene
    metal = bpy.data.collections.get("METAL")
    assert metal is not None, "Template is missing the METAL collection"
    white = bpy.data.materials.get("Gold_White")
    assert white is not None, "Template is missing the Gold_White material"

    # Clear the template cube and any prior meshes; keep camera and lights.
    for obj in [o for o in list(bpy.data.objects) if o.type == "MESH"]:
        bpy.data.objects.remove(obj, do_unlink=True)

    major = BAND_MAJOR_MM / 1000
    minor = BAND_MINOR_MM / 1000
    center_z = major + minor
    bpy.ops.mesh.primitive_torus_add(
        major_radius=major,
        minor_radius=minor,
        major_segments=128,
        minor_segments=32,
        location=(0, 0, center_z),
    )
    band = bpy.context.active_object
    band.name = "Band_WhiteGold"
    band.rotation_euler.x = math.radians(90)  # upright: plane XZ, hole axis Y
    bpy.ops.object.transform_apply(rotation=True)
    band.data.materials.clear()
    band.data.materials.append(white)
    move_to(band, metal)
    band[TAG] = True

    band_top = center_z + major + minor
    scene["band_top_mm"] = round(band_top * 1000, 4)
    scene["band_vertices"] = [float(c) for v in band.data.vertices for c in v.co]
    scene["band_indices"] = [i for p in band.data.polygons for i in p.vertices]
    scene["band_matrix"] = [float(c) for row in band.matrix_world for c in row]

    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print(
        f"BUILT band: OD {BAND_TOP_MM:.1f} mm, "
        f"ID {2 * (BAND_MAJOR_MM - BAND_MINOR_MM):.1f} mm, "
        f"top Z {scene['band_top_mm']:.1f} mm"
    )


build_band()

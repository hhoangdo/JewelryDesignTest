"""Create templates/ring-template.blend from a factory-startup scene.

Run from the repository root:
    "D:\\JewelryStudio\\Blender-4.5-LTS\\blender.exe" --background --factory-startup --python templates/make_template.py
"""
# pyright: reportMissingImports=false
import bpy
from mathutils import Vector

ROOT = __file__.replace("\\", "/").rsplit("/", 2)[0]
OUTPUT = ROOT + "/templates/ring-template.blend"


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


def make_material(name, color, metallic, roughness, ior=1.45, transmission=0.0):
    material = bpy.data.materials.get(name)
    if material is None:
        material = bpy.data.materials.new(name)
    material.use_nodes = True
    material.use_fake_user = True
    node = next(n for n in material.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    node.inputs["Base Color"].default_value = (*color, 1.0)
    node.inputs["Metallic"].default_value = metallic
    node.inputs["Roughness"].default_value = roughness
    node.inputs["IOR"].default_value = ior
    node.inputs["Transmission Weight"].default_value = transmission
    return material


def main() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        bpy.data.collections.remove(collection)
    for mesh in list(bpy.data.meshes):
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    for camera_data in list(bpy.data.cameras):
        if camera_data.users == 0:
            bpy.data.cameras.remove(camera_data)
    for light_data in list(bpy.data.lights):
        if light_data.users == 0:
            bpy.data.lights.remove(light_data)
    for material in list(bpy.data.materials):
        if material.users == 0:
            bpy.data.materials.remove(material)

    ensure_units()
    scene = bpy.context.scene

    make_material("Gold_Yellow", (1.0, 0.766, 0.336), 1.0, 0.2)
    make_material("Gold_White", (0.96, 0.963, 0.97), 1.0, 0.15)
    make_material("Gold_Rose", (0.95, 0.66, 0.55), 1.0, 0.2)
    make_material("Silver", (0.97, 0.97, 0.97), 1.0, 0.2)
    make_material(
        "Gem_Center",
        (1.0, 1.0, 1.0),
        0.0,
        0.02,
        ior=2.417,
        transmission=1.0,
    )

    for name in ("GEMS", "METAL", "REFERENCE"):
        collection = bpy.data.collections.new(name)
        scene.collection.children.link(collection)

    camera_data = bpy.data.cameras.new("Camera")
    camera = bpy.data.objects.new("Camera", camera_data)
    scene.collection.objects.link(camera)
    camera.location = (0.055, -0.038, 0.032)
    target = Vector((0, 0, 0.013))
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera_data.lens = 55
    camera_data.clip_start = 0.001
    camera_data.clip_end = 10.0
    scene.camera = camera

    light_data = bpy.data.lights.new("Light", type="POINT")
    light_data.energy = 10.0
    light_data.shadow_soft_size = 0.005
    light = bpy.data.objects.new("Light", light_data)
    scene.collection.objects.link(light)
    light.location = (0.02, -0.025, 0.045)

    world = scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        scene.world = world
    world.use_nodes = True
    background = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    background.inputs["Color"].default_value = (0.85, 0.85, 0.85, 1)
    background.inputs["Strength"].default_value = 0.8

    scene.render.engine = "CYCLES"
    scene.cycles.use_denoising = True
    scene.render.resolution_x = 1000
    scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"

    text = bpy.data.texts.get("START-HERE") or bpy.data.texts.new("START-HERE")
    text.clear()
    text.write(
        "Jewelry Studio ring template\n\n"
        "Units: metric, millimetres displayed, scale_length = 1.0.\n"
        "Design in millimetres, then divide by 1000 for Blender coordinates.\n\n"
        "Collections: GEMS, METAL, REFERENCE.\n"
        "Materials: Gold_Yellow, Gold_White, Gold_Rose, Silver, Gem_Center.\n\n"
        "Use tools/new-project.ps1 to copy this file into projects/<name>/ring.blend.\n"
    )

    bpy.ops.wm.save_as_mainfile(filepath=OUTPUT)
    print("TEMPLATE SAVED", OUTPUT)
    print("SCALE", scene.unit_settings.scale_length, "LEN", scene.unit_settings.length_unit)
    print("OBJECTS", [(o.name, o.type) for o in bpy.data.objects])
    print("COLLS", [(c.name, len(c.objects)) for c in bpy.data.collections])
    print("MATS", [m.name for m in bpy.data.materials])


main()

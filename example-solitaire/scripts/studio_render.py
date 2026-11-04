"""Neutral softbox studio; configure first, inspect, then render the hero."""
# pyright: reportMissingImports=false
import bpy
import math
from mathutils import Vector

RENDER_NOW = True
USE_GPU = True
SAMPLES = 256
SMOOTH_BAND = True
LENS_MM = 95.0
CAMERA_ELEVATION_DEG = 40.0
KEY_WIDTH_MM = 20.0
WORLD_STRENGTH = 0.80
TAG = "jewelry_studio_generated"
PROJECT_DIR = bpy.data.filepath.replace("\\", "/").rsplit("/", 1)[0]
HERO = PROJECT_DIR + "/renders/hero.png"


def enum_id(owner, prop: str, label: str) -> str:
    token = "".join(c.lower() for c in label if c.isalnum())
    choices = [(i.identifier, i.name) for i in owner.bl_rna.properties[prop].enum_items]
    return next(
        identifier
        for identifier, name in choices
        if token in "".join(c.lower() for c in name if c.isalnum())
    )


def dynamic_enum_id(error, label: str) -> str:
    token = "".join(c.lower() for c in label if c.isalnum())
    return next(
        identifier
        for identifier in str(error).split("'")[1::2]
        if token in "".join(c.lower() for c in identifier if c.isalnum())
    )


def studio_surface(name: str, coordinates, color, collection):
    obj = bpy.data.objects.get(name)
    if obj is None:
        mesh = bpy.data.meshes.new("Studio_" + name)
        mesh.from_pydata(coordinates, [], [(0, 1, 2, 3)])
        mesh.update()
        material = bpy.data.materials.new("Studio_" + name)
        material.use_nodes = True
        node = next(n for n in material.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
        node.inputs["Base Color"].default_value = (*color, 1)
        node.inputs["Roughness"].default_value = 0.85
        mesh.materials.append(material)
        obj = bpy.data.objects.new(name, mesh)
        collection.objects.link(obj)
        obj[TAG] = True
    else:
        assert obj.get(TAG) or obj.get("v2_generated"), f"Unrecognized studio object: {name}"
    return obj


def configure_studio() -> None:
    assert bpy.data.filepath.endswith("ring.blend"), "Save the project as ring.blend first"
    scene = bpy.context.scene
    for polygon in bpy.data.objects["Band_WhiteGold"].data.polygons:
        polygon.use_smooth = SMOOTH_BAND
    collection = bpy.data.collections.get("STUDIO")
    if collection is None:
        collection = bpy.data.collections.new("STUDIO")
        scene.collection.children.link(collection)
    world = scene.world
    assert world is not None
    world.use_nodes = True
    background = next(n for n in world.node_tree.nodes if n.type == "BACKGROUND")
    background.inputs["Color"].default_value = (0.85, 0.85, 0.85, 1)
    background.inputs["Strength"].default_value = WORLD_STRENGTH
    target = Vector((0, 0, 0.014))
    area_type = next(
        i.identifier
        for i in bpy.data.objects["Light"].data.bl_rna.properties["type"].enum_items
        if i.name == "Area"
    )
    lights = [
        ("Light", (-0.020, -0.035, 0.050), 0.050, KEY_WIDTH_MM / 1000, 0.055),
        ("Studio_Fill", (0.028, -0.020, 0.036), 0.015, 0.020, 0.040),
        ("Studio_Rim", (0.0, 0.030, 0.045), 0.030, 0.025, 0.045),
    ]
    for name, position, energy, width, height in lights:
        obj = bpy.data.objects.get(name)
        if obj is None:
            data = bpy.data.lights.new("Studio_" + name, type=area_type)
            obj = bpy.data.objects.new(name, data)
            collection.objects.link(obj)
            obj[TAG] = True
        else:
            assert name == "Light" or obj.get(TAG) or obj.get("v2_generated")
            obj.data.type = area_type
        obj.data.shape = enum_id(obj.data, "shape", "Rectangle")
        obj.data.energy, obj.data.size, obj.data.size_y = energy, width, height
        obj.data.color = (1, 1, 1)
        obj.location = position
        obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()
    studio_surface(
        "Studio_Ground",
        [
            (-0.2, -0.2, -0.00002),
            (0.2, -0.2, -0.00002),
            (0.2, 0.2, -0.00002),
            (-0.2, 0.2, -0.00002),
        ],
        (0.83, 0.83, 0.83),
        collection,
    )
    card = studio_surface(
        "Studio_ContrastCard",
        [
            (-0.045, -0.028, 0),
            (-0.045, 0.028, 0),
            (-0.045, 0.028, 0.060),
            (-0.045, -0.028, 0.060),
        ],
        (0.008, 0.008, 0.008),
        collection,
    )
    card.visible_camera = False
    card.visible_shadow = False
    camera = bpy.data.objects.get("Camera")
    if camera is None:
        camera_data = bpy.data.cameras.new("Camera")
        camera = bpy.data.objects.new("Camera", camera_data)
        scene.collection.objects.link(camera)
    radius = Vector((0.035, -0.055, 0.031)).length
    azimuth = math.atan2(-55, 35)
    elevation = math.radians(CAMERA_ELEVATION_DEG)
    camera.location = target + Vector(
        (
            radius * math.cos(elevation) * math.cos(azimuth),
            radius * math.cos(elevation) * math.sin(azimuth),
            radius * math.sin(elevation),
        )
    )
    camera.rotation_euler = (target - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = LENS_MM
    camera.data.clip_start, camera.data.clip_end = 0.001, 1.0
    scene.camera = camera
    if scene.view_settings.view_transform.lower() != "agx":
        try:
            scene.view_settings.view_transform = ""
        except (TypeError, ValueError) as error:
            scene.view_settings.view_transform = dynamic_enum_id(error, "AgX")
    try:
        scene.view_settings.look = ""
    except (TypeError, ValueError) as error:
        scene.view_settings.look = dynamic_enum_id(error, "Medium High Contrast")
    scene.view_settings.exposure = 0
    scene.view_settings.gamma = 1
    if scene.render.engine.lower() != "cycles":
        try:
            scene.render.engine = ""
        except TypeError as error:
            engine = next(
                i for i in str(error).split("'")[1::2] if i.lower() == "cycles"
            )
            scene.render.engine = engine
    scene.cycles.device = enum_id(
        scene.cycles, "device", "GPU" if USE_GPU else "CPU"
    )
    scene.cycles.samples = SAMPLES
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 16
    scene.cycles.transmission_bounces = 12
    scene.cycles.glossy_bounces = 8
    scene.render.resolution_x = scene.render.resolution_y = 1000
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = enum_id(
        scene.render.image_settings, "file_format", "PNG"
    )
    scene.render.image_settings.color_mode = enum_id(
        scene.render.image_settings, "color_mode", "RGB"
    )
    scene.render.film_transparent = False
    scene.render.filepath = HERO
    bpy.context.view_layer.update()
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print(
        f"STUDIO configured: neutral world, 3 softboxes, contrast card; "
        f"lens {LENS_MM} mm; device {'GPU request' if USE_GPU else 'CPU'}; no render yet"
    )


def render_hero() -> None:
    assert bpy.data.filepath.endswith("ring.blend"), "Render only a saved project"
    render_path = bpy.path.abspath(bpy.context.scene.render.filepath).replace("\\", "/")
    assert render_path == HERO, "Hero path does not match this project"
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
    print("HERO saved to", HERO)


configure_studio()
if RENDER_NOW:
    render_hero()

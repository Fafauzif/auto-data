"""Render the KEY cover from the repository's original Zenix asset.
Run in the repository root with Blender: blender -b -t 4 -P tools/render_key_vehicle.py
The final WebP is exported from the transparent PNG in the temporary directory.
"""
import bpy
from mathutils import Vector
from pathlib import Path
import tempfile
def aim(obj, point):
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.gltf(filepath=str(Path("public/models/zenix.glb").resolve()))
scene = bpy.context.scene
scene.render.engine = "CYCLES"
scene.cycles.samples = 48
scene.cycles.use_denoising = False
scene.world = bpy.data.worlds.new("Showroom daylight")
scene.world.use_nodes = True
scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.56, 0.63, 0.78, 1)
scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.48
for material in bpy.data.materials:
    if material.name.startswith("BodyPaint"):
        shader = material.node_tree.nodes.get("Principled BSDF")
        if shader:
            shader.inputs["Base Color"].default_value = (0.68, 0.70, 0.72, 1)
            shader.inputs["Metallic"].default_value = 0.64
            shader.inputs["Roughness"].default_value = 0.26
for name, point, energy, size, color in [
    ("Key softbox", (-4, -5, 6), 1550, 5, (1, 0.91, 0.83)),
    ("Fill softbox", (5, -2, 4), 1200, 5, (0.77, 0.84, 1)),
    ("Side reflection", (-4, 3, 3), 1650, 4, (0.88, 0.93, 1)),
    ("Front highlights", (0, -6, 1.4), 270, 3, (1, 0.98, 0.91)),
]:
    bpy.ops.object.light_add(type="AREA", location=point)
    source = bpy.context.object
    source.name = name
    source.data.energy, source.data.size, source.data.color = energy, size, color
    aim(source, (0, 0, 0.85))
bpy.ops.object.camera_add(location=(-7.6, -9.6, 3.4))
camera = bpy.context.object
aim(camera, (0, 0, 0.94))
camera.data.type = "ORTHO"
camera.data.ortho_scale = 5.64
scene.camera = camera
scene.render.resolution_x, scene.render.resolution_y, scene.render.resolution_percentage = 1080, 620, 100
scene.render.image_settings.color_mode = "RGBA"
scene.render.film_transparent = True
scene.render.filepath = str(Path(tempfile.gettempdir()) / "digiroom-key-zenix.png")
bpy.ops.render.render(write_still=True)

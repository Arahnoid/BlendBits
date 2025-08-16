"""
create_material_palette_from_selected.py
----------------------------------------

Purpose:
    * Scans all selected mesh objects in the current Blender scene.
    * Collects every unique material from those objects.
    * Creates one UV sphere per unique material and assigns that material.
    * Arranges the spheres into a 2D grid (rows × columns), spaced evenly.
    * Places the grid at the location of the first selected object.

Usage:
    1. Open Blender (2.80 or newer) and switch to the "Scripting" workspace.
    2. Select the mesh objects whose materials you want to visualize.
    3. Open a new text block in the Text Editor, paste this script,
       and press **Run Script** (or Alt-P).
    4. A set of UV spheres will be created and selected, each with one material.
       The first sphere is set as the active object.

Customization:
    * `segments` – number of segments per UV sphere (default 8)
    * `rings`    – number of rings per UV sphere (default 4)
    * `radius`   – radius of each UV sphere (default 0.1)
    * `spacing`  – distance between spheres in grid (default 0.3)
    * `prefix`   – name prefix for spheres (default "")
    * `autogrid` – if `True` then UV spheres will be arranged in a grid pattern

Notes:
    * The script deselects all objects before creating spheres, then selects
      all the new ones.
    * You can easily move or group the entire palette since they are all selected.
"""

import math
from mathutils import Vector
import bpy


def create_material_spheres_grid(
    segments: int,
    rings: int,
    radius: float,
    spacing: float,
    prefix: str,
    autogrid: bool,
):
    selected_objects = bpy.context.selected_objects
    if not selected_objects:
        print("No objects selected.")
        return

    base_location = selected_objects[0].location.copy()

    # Collect unique materials from selected mesh objects
    unique_materials = set()
    for obj in selected_objects:
        if obj.type == "MESH":
            for slot in obj.material_slots:
                if slot.material:
                    unique_materials.add(slot.material)

    if not unique_materials:
        print("No materials found in selected objects.")
        return

    # Deselect all first
    bpy.ops.object.select_all(action="DESELECT")
    created_spheres = []

    num_materials = len(unique_materials)
    cols = math.ceil(math.sqrt(num_materials))  # square grid layout

    for idx, mat in enumerate(unique_materials):
        row = idx // cols
        col = idx % cols

        if autogrid:
            offset = Vector((col * spacing, row * spacing, 0))
        else:
            offset = Vector((idx * spacing, 0, 0))

        location = base_location + offset

        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=segments, ring_count=rings, radius=radius, location=location
        )
        sphere = bpy.context.active_object

        if prefix == "":
            sphere.name = f"{mat.name}"
        else:
            sphere.name = f"{prefix}_{mat.name}"

        if sphere.data.materials:
            sphere.data.materials[0] = mat
        else:
            sphere.data.materials.append(mat)

        created_spheres.append(sphere)

    for sphere in created_spheres:
        sphere.select_set(True)

    if created_spheres:
        bpy.context.view_layer.objects.active = created_spheres[0]

    print(
        f"Created and selected {len(created_spheres)} material spheres near first selected object."
    )


# Run
create_material_spheres_grid(
    segments=8, rings=4, radius=0.1, spacing=0.3, prefix="", autogrid=True
)

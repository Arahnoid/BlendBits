"""
swap_material_slots.py
----------------------

Purpose:
    Swaps the first and second material slots of all selected mesh objects,
    and updates polygon assignments so materials remain correctly mapped.

Usage:
    1. Select one or more mesh objects that have at least two material slots.
    2. Open this script in Blender's Text Editor and press **Run Script** (Alt-P).
    3. The first and second material slots will be exchanged, along with all
       face assignments using those slots.

Notes:
    * Only mesh objects are affected.
    * Objects with fewer than two material slots are skipped.
"""

import bpy


def swap_materials_and_assignments(obj):
    if obj.type != "MESH":
        return
    if len(obj.material_slots) < 2:
        return

    # Swap the actual material slots
    obj.material_slots[0].material, obj.material_slots[1].material = (
        obj.material_slots[1].material,
        obj.material_slots[0].material,
    )

    mesh = obj.data

    # Use a temporary index that won't clash
    temp_index = len(obj.material_slots)

    for poly in mesh.polygons:
        if poly.material_index == 0:
            poly.material_index = temp_index
        elif poly.material_index == 1:
            poly.material_index = 0

    for poly in mesh.polygons:
        if poly.material_index == temp_index:
            poly.material_index = 1


# Run on all selected mesh objects
for obj in bpy.context.selected_objects:
    swap_materials_and_assignments(obj)

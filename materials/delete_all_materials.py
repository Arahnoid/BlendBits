"""
delete_all_materials.py
-----------------------

Description:
    This script removes all materials from every selected object in Blender.
    It works with any object type that supports materials, such as meshes, curves,
    text, surfaces, and metaballs.

Usage:
    1. Select one or more objects in the 3D Viewport.
    2. Open the Script in Blender's Text Editor.
    3. Click 'Run Script'.

Details:
    - If an object has no materials, it will be skipped.
    - If an object type does not support materials (e.g., Empty, Camera), it will be skipped.
    - Outputs a log in the console indicating which objects had materials removed.
"""

import bpy

# Loop through all selected objects
for obj in bpy.context.selected_objects:
    if hasattr(obj.data, "materials"):  # Only objects with material slots
        mat_count = len(obj.data.materials)
        if mat_count > 0:
            # Clear all material slots
            obj.data.materials.clear()
            print(f"Removed {mat_count} materials from: {obj.name}")
        else:
            print(f"No materials found on: {obj.name}")
    else:
        print(f"Object type '{obj.type}' does not support materials: {obj.name}")

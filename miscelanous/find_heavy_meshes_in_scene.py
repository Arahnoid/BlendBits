"""
find_heavy_meshes_in_scene.py
-----------------------------
Purpose:
    This script scans all objects in the current Blender scene and
    automatically selects those mesh objects whose polygon count exceeds
    a specified threshold (default: 1,000 polygons).

Usage:
    1. Open the script in Blender's Text Editor.
    2. Adjust the threshold value in the `x` variable if needed.
    3. Run the script (`Alt+P` or the Run Script button).
    4. Selected objects will be highlighted in the viewport.

Note:
    - Only objects of type "MESH" are evaluated.
    - The script deselects all other objects to keep the selection clean.
"""

import bpy

MAX_POLYGONS = 1000

# Loop through all objects in the scene
for obj in bpy.context.scene.objects:
    if obj.type == "MESH":
        # Check if the object's polygon count is higher than X
        if len(obj.data.polygons) > MAX_POLYGONS:
            obj.select_set(True)
        else:
            obj.select_set(False)

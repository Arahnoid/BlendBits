"""
move_selected_to_collectios_suffix.py
-------------------------------------

Description:
    This Blender script moves each selected object into a new or existing
    collection whose name is the object's name plus a configurable suffix.
    If the object is already in the correct collection, it will be skipped
    to avoid unnecessary unlink/relink operations.

Usage:
    1. In Blender, set the `SUFFIX` variable to the desired text.
       Example: "_room", "_low", "_high"
    2. Select one or more objects in the Outliner or 3D View.
    3. Open the Text Editor, load this script, and run it (Alt+P).
    4. Each selected object will be moved to a collection named
       "<object_name><SUFFIX>".

Notes:
    - If the target collection does not exist, it is created automatically.
    - Objects already in the correct collection are skipped.
    - Works with all object types, not just meshes.
"""

import bpy

# ---- Configurable Suffix ----
SUFFIX = "_sufix"  # Change this to whatever suffix you want
# -----------------------------


def move_object_to_named_collection(obj, suffix):
    # Construct the collection name
    collection_name = f"{obj.name}{suffix}"

    # Create or get the collection
    if collection_name not in bpy.data.collections:
        new_collection = bpy.data.collections.new(collection_name)
        bpy.context.scene.collection.children.link(new_collection)
    else:
        new_collection = bpy.data.collections[collection_name]

    # Skip if object is already in the correct collection
    if obj.name in new_collection.objects:
        return

    # Remove object from all other collections
    for col in obj.users_collection:
        col.objects.unlink(obj)

    # Add object to the target collection
    new_collection.objects.link(obj)


# Process all selected objects
for obj in bpy.context.selected_objects:
    move_object_to_named_collection(obj, SUFFIX)

print(
    f"Objects successfully moved to their respective '{SUFFIX}' collections (skipped existing)."
)

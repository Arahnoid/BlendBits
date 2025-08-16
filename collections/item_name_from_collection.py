"""
item_name_from_collection.py
----------------------------

Description:
    This Blender script renames selected objects to match the name of
    their first linked collection.

Features:
    - Works on selected objects only (any type, but only renames data if
      type is MESH or CURVE).
    - Uses the first collection the object belongs to as the base name.
    - Skips renaming if the object already has the target name.
    - If multiple selected objects are in the same collection, appends suffixes
      "_001", "_002", etc.
    - Renames both the object and its data block (for meshes and curves) to keep
      them consistent.

Usage:
    1. Select the objects you want to rename.
    2. Run the script from Blender's Text Editor or assign it to a custom
       button.
    3. Objects will be renamed according to their collection name.

Example:
    Collection: "Tree"
    Selected Objects: Tree, Tree.001, Tree.002
    Result: Tree, Tree_001, Tree_002

"""

import bpy
from collections import defaultdict


def rename_selected_to_collection():
    # Dictionary: collection_name -> list of objects in that collection
    col_objects = defaultdict(list)

    # Gather selected objects grouped by their first collection
    for obj in bpy.context.selected_objects:
        if obj.users_collection:
            collection_name = obj.users_collection[0].name
            col_objects[collection_name].append(obj)

    # Rename in groups
    for collection_name, objs in col_objects.items():
        counter = 1
        for obj in objs:
            # Target name (without suffix for first object)
            if counter == 1:
                new_name = collection_name
            else:
                new_name = f"{collection_name}_{counter:03d}"

            # Skip if object already matches desired name
            if obj.name == new_name:
                counter += 1
                continue

            # Rename object
            obj.name = new_name

            # Rename its data if it has one and type is Mesh or Curve
            if obj.type in {"MESH", "CURVE"} and obj.data:
                obj.data.name = new_name

            counter += 1


# Run it
rename_selected_to_collection()

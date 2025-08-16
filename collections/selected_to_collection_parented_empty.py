"""
selected_to_collection_parented_empty.py
----------------------------------------

Description:
    This Blender script processes each selected mesh object by:
    1. Creating an Empty object with the same name (if it doesn’t already exist).
    2. Matching the Empty's location, rotation, and scale to the mesh.
    3. Parenting the mesh to the Empty without altering world transforms (if not already parented).
    4. Creating (or reusing) a collection named after the mesh.
    5. Moving both the mesh and the Empty into that collection, unlinking them from all others.

Usage:
    1. In Blender, select one or more mesh objects.
    2. Open the Text Editor, load this script, and run it (Alt+P).
    3. Each mesh will be parented to an Empty in a new or existing collection
       named after the mesh.

Notes:
    - Only mesh objects are processed; other object types are ignored.
    - Existing Empties and collections with the same name are reused.
    - Parenting preserves world transforms.
"""

import bpy


def main():
    selected_meshes = [
        obj for obj in bpy.context.selected_objects if obj.type == "MESH"
    ]

    if not selected_meshes:
        print("No mesh objects selected.")
        return

    for obj in selected_meshes:
        empty_name = obj.name

        # Create or get Empty with same name
        if (
            empty_name in bpy.data.objects
            and bpy.data.objects[empty_name].type == "EMPTY"
        ):
            empty = bpy.data.objects[empty_name]
        else:
            empty = bpy.data.objects.new(name=empty_name, object_data=None)
            empty.matrix_world = obj.matrix_world.copy()
            bpy.context.scene.collection.objects.link(empty)

        # Parent mesh to Empty if not already
        if obj.parent != empty:
            obj.parent = empty
            obj.matrix_parent_inverse = empty.matrix_world.inverted()

        # Create or get collection with the object's name
        if empty_name not in bpy.data.collections:
            new_collection = bpy.data.collections.new(empty_name)
            bpy.context.scene.collection.children.link(new_collection)
        else:
            new_collection = bpy.data.collections[empty_name]

        # Move both objects into the new collection if not already there
        for o in [obj, empty]:
            if o.name not in new_collection.objects:
                for coll in o.users_collection:
                    coll.objects.unlink(o)
                new_collection.objects.link(o)

    print("Done: All selected mesh objects processed.")


main()

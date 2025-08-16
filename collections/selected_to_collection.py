"""
selected_to_collection.py
-------------------------

Description:
    This Blender script moves each selected object into its own new collection
    named after the object. The object will be unlinked from any collections
    it currently belongs to, and then linked exclusively to its newly created
    collection.

Usage:
    1. In Blender, select the objects you want to move to new collections.
    2. Open the Text Editor, load this script, and run it (Alt+P).
    3. Each selected object will now have its own collection with the same name.

Notes:
    - Existing collections with the same name will be replaced if created anew.
    - Works with any object type (mesh, curve, light, etc.).
"""

import bpy


for obj in bpy.context.selected_objects:
    col = bpy.data.collections.new(name=obj.name)
    bpy.context.scene.collection.children.link(col)

    for other_col in obj.users_collection:
        other_col.objects.unlink(obj)
    if obj.name not in col.objects:
        col.objects.link(obj)

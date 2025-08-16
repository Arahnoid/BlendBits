"""
Rename Parent Collections
collection_name_from_selection.py
-------------------------

Description:
    This script renames the *first* (primary) collection of each selected
    object to match that object's own name.
    It is handy when you want the collection hierarchy to mirror the
    object names for easier organization.

Usage:
    1. In the 3‑D Viewport, select one or more objects.
    2. Open the **Text Editor**, load this script (or paste it into a new
    text block).
    3. Press **Run Script** (or hit `Alt+P`).

Notes:
    * If several selected objects share the same collection, the script
    renames that collection only once (the first time it is encountered).
    * If a collection with the desired name already exists, the script
    automatically appends a numeric suffix (`_1`, `_2`, …) so the name
    stays unique.
    * The script only considers the first collection in
    `object.users_collection`.  If an object belongs to multiple
    collections and you wish to rename all of them, modify the loop
    accordingly.
"""

import bpy


def rename_parent_collections():
    """Rename the first collection of each selected object to that object's name."""
    # Grab the current selection
    selected_objects = bpy.context.selected_objects
    if not selected_objects:
        print("Nothing selected – nothing to do.")
        return

    # Keep track of collections that were already renamed in this run
    renamed_collections = set()

    for obj in selected_objects:
        # An object may belong to multiple collections.
        # We'll rename the first one we find.
        if not obj.users_collection:
            print(f"Object '{obj.name}' is not in any collection – skipping.")
            continue

        parent_col = obj.users_collection[0]

        # Skip if we've already renamed this collection (possible when objects share a collection)
        if parent_col in renamed_collections:
            continue

        # Desired new name is the object's name
        desired_name = obj.name

        # Ensure the name is unique inside bpy.data.collections
        if (
            desired_name in bpy.data.collections
            and bpy.data.collections[desired_name] is not parent_col
        ):
            base_name = desired_name
            suffix = 1
            while desired_name in bpy.data.collections:
                desired_name = f"{base_name}_{suffix}"
                suffix += 1

        # Rename and remember
        parent_col.name = desired_name
        renamed_collections.add(parent_col)

        print(
            f"Renamed collection '{parent_col.name}' to '{desired_name}' for object '{obj.name}'."
        )


# ------------------------------------------------------------------
# Run the function
# ------------------------------------------------------------------
rename_parent_collections()

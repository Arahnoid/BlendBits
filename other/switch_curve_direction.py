"""
switch_curve_direction.py
-------------------------
Flips the direction of all selected curve objects in Blender.

How it works:
    - Iterates through all selected objects in the scene.
    - For each object of type 'CURVE':
        1. Makes it the active object.
        2. Switches to Edit mode.
        3. Selects all points in the curve.
        4. Runs Blender's built-in 'Switch Direction' operator.
        5. Returns to Object mode.
    - Non-curve objects in the selection are ignored.

Usage:
    1. Select one or more curve objects in the 3D View.
    2. Run this script from Blender's Text Editor (Alt+P).
    3. The direction of all selected curves will be reversed.

Notes:
    - The script uses Blender's native curve direction tool.
    - Meshes, lights, and other non-curve objects are skipped.
    - Works in Object mode; automatically changes modes as needed.
"""

import bpy


def switch_curves_direction():
    """Flip the direction of every selected CURVE object
    by invoking the built-in switch_direction operator."""

    # Ensure we start in Object mode
    if bpy.context.mode != "OBJECT":
        bpy.ops.object.mode_set(mode="OBJECT")

    selected_curves = [
        obj for obj in bpy.context.selected_objects if obj.type == "CURVE"
    ]

    if not selected_curves:
        print("No curve objects selected.")
        return

    for obj in selected_curves:
        bpy.ops.object.select_all(action="DESELECT")

        # Make this curve active
        bpy.context.view_layer.objects.active = obj

        # Switch to Edit mode
        bpy.ops.object.mode_set(mode="EDIT")

        # Select all points
        bpy.ops.curve.select_all(action="SELECT")

        # Reverse curve direction
        bpy.ops.curve.switch_direction()

        # Back to Object mode
        bpy.ops.object.mode_set(mode="OBJECT")

    print(f"Reversed direction for {len(selected_curves)} curve(s).")

    # Reselect curves
    for obj in selected_curves:
        bpy.data.objects[obj.name].select_set(True)


# Run
switch_curves_direction()

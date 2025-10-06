"""
Dissolve Selected Edge Loops
loops_dissolve.py
----------------------------

This script dissolves the edge loops based on the user’s current edge selection.
It is useful for quickly cleaning up geometry while preserving the surface shape.

Steps performed:
    1. Ensures the active object is a mesh and switches to Edit Mode.
    2. Expands the current edge selection into full loops (using `loop_multi_select`).
    3. Dissolves the selected edge loops (using `mesh.dissolve_edges`).

Usage:
    - Select a mesh object.
    - In Edit Mode, select one or more edges you want to dissolve loops through.
    - Run the script in the Scripting editor.
    - The loops corresponding to the selected edges will be dissolved.
"""

import bpy

# Ensure we are in Edit Mode
obj = bpy.context.object
if obj and obj.type == "MESH":
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.loop_multi_select(ring=False)
    # Dissolve all selected edge loops
    bpy.ops.mesh.dissolve_edges()

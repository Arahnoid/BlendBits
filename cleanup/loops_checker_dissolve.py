"""
Dissolve Every Nth Edge Loop
loops_checker_dissolve.py
----------------------------

This script automates the process of reducing mesh edge loops by selecting and dissolving
every second edge in Edit Mode. It is useful for simplifying meshes while maintaining
overall shape and topology.

Steps performed:
    1. Ensures the active object is a mesh and switches to Edit Mode.
    2. Selects every 2nd edge in the mesh (using `mesh.select_nth(2)`).
    3. Expands the selection to full loops (using `loop_multi_select`).
    4. Dissolves the selected edge loops (using `mesh.dissolve_edges`).

Usage:
    - Select a mesh object.
    - Run the script in the Scripting editor.
    - The script will simplify the mesh by dissolving alternating edge loops.
"""

import bpy

if bpy.context.mode != "EDIT_MESH":
    raise Exception("You must be in Edit Mode on a mesh.")

bpy.ops.mesh.select_nth(2)
bpy.ops.mesh.loop_multi_select(ring=False)
bpy.ops.mesh.dissolve_edges()

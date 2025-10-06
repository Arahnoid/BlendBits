"""
Dissolve Edge Loops Between Two Selected Edges
loops_ring_dissolve.py
--------------------------------------------

This script dissolves edge loops located between two user-selected edges.
It is useful for cleaning up dense geometry while maintaining topology continuity.

Steps performed:
    1. Ensures the active object is a mesh in Edit Mode; otherwise, raises an exception.
    2. Switches to EDGE selection mode.
    3. Uses `shortest_path_select` to select all edges between the first and second selected edge.
    4. Expands the selection to complete edge loops (`loop_multi_select`).
    5. Dissolves the selected loops (`mesh.dissolve_edges`).

Usage:
    - Enter Edit Mode on a mesh.
    - Select exactly two edges that mark the range of loops you want removed.
    - Run the script in the Scripting editor.
    - All edge loops between the two selected edges will be dissolved.
"""

import bpy

if bpy.context.mode != "EDIT_MESH":
    raise Exception("You must be in Edit Mode on a mesh.")

bpy.ops.mesh.select_mode(type="EDGE")
bpy.ops.mesh.shortest_path_select(
    use_face_step=True, use_topology_distance=True, use_fill=False
)
bpy.ops.mesh.loop_multi_select(ring=False)
bpy.ops.mesh.dissolve_edges()

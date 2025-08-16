"""
resize_texture_nodes.py
-----------------------

Description:
    A lightweight Blender‑Python tool that enlarges the visual width of all
    **Image Texture** (`TEX_IMAGE`) nodes in the node‑trees of selected objects’
    materials, making them easier to locate in the Shader Editor.

How it works:
    * Loops over every selected object.
    * For each object that has materials, it checks every material slot.
    * If a material uses nodes, it scans its node‑tree.
    * Every node of type `TEX_IMAGE` is set to a width of 400 pixels.
    * The node is optionally selected for quick visual identification.

Typical usage:
    1. Select the objects you want to process in the 3D Viewport.
    2. Open this script in Blender’s Text Editor.
    3. Press **Alt + P** (or click *Run Script*).

Feel free to adjust the width value or the selection logic to suit your workflow.
"""

import bpy

NODE_WIDTH = 400

# Loop through all selected objects
for obj in bpy.context.selected_objects:
    # Ensure the object has materials
    if not hasattr(obj.data, "materials"):
        continue

    # Loop through all material slots
    for mat in obj.data.materials:
        if mat and mat.use_nodes:
            nodes = mat.node_tree.nodes
            for node in nodes:
                if node.type == "TEX_IMAGE":
                    node.width = NODE_WIDTH
                    # node.select = True  # Optional: highlight

"""
Find Non-Latin Characters in .blend File
---------------------------------------

This script scans a .blend file for any datablocks whose names contain
non-Latin characters. It checks:

- Objects
- Object data (meshes, curves, armatures, lattices, metaballs, grease pencils)
- Materials, textures, images, collections, node groups
- Nodes inside materials and node groups
- Text datablocks

All matching names are collected and copied into the system clipboard,
with the specific non-Latin characters found shown in square brackets
for easier identification.

Usage:
    1. Open your .blend file in Blender.
    2. Paste this script into the Scripting editor.
    3. Run the script.
    4. Press Ctrl+V in any text editor to see the results.
"""

import bpy
import re
import os
import ctypes
import platform


def is_console_visible():
    """Check if Blender's console window is visible (Windows only)."""
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd == 0:
        return False
    return ctypes.windll.user32.IsWindowVisible(hwnd) != 0


def show_console():
    """Ensure Blender's console is open and visible."""
    if not is_console_visible():
        bpy.ops.wm.console_toggle()


def clear_console():
    """Clear console window."""
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


# Match all characters that are *not* in the basic Latin Unicode blocks:
#   - U+0000–U+007F (Basic Latin)
#   - U+0080–U+00FF (Latin-1 Supplement)
#   - U+0100–U+017F (Latin Extended-A)
#   - U+0180–U+024F (Latin Extended-B)
#   - U+1E00–U+1EFF (Latin Extended Additional)
non_latin_pattern = re.compile(
    r"[^\u0000-\u007F\u0080-\u00FF\u0100-\u017F\u0180-\u024F\u1E00-\u1EFF]")

bad_names = {}


def check_names(data, label):
    """Check a datablock collection for non-Latin names."""
    for item in data:
        matches = non_latin_pattern.findall(item.name)
        if matches:
            if label not in bad_names:
                bad_names[label] = []
            unique = "".join(sorted(set(matches)))
            bad_names[label].append(f"- {item.name} [{unique}]")


def check_nodes(node_tree, parent_label):
    """Check nodes inside a node tree."""
    if not node_tree:
        return
    for node in node_tree.nodes:
        matches = non_latin_pattern.findall(node.name)
        if matches:
            if parent_label not in bad_names:
                bad_names[parent_label] = []
            unique = "".join(sorted(set(matches)))
            bad_names[parent_label].append(f"- {node.name} [{unique}]")


# Datablock types to check
datablocks = [
    ("objects", "Object"),
    ("meshes", "Mesh"),
    ("curves", "Curve"),
    ("metaballs", "Metaball"),
    ("texts", "Text Data"),
    ("armatures", "Armature"),
    ("lattices", "Lattice"),
    ("grease_pencils", "Grease Pencil"),
    ("materials", "Material"),
    ("textures", "Texture"),
    ("images", "Image"),
    ("collections", "Collection"),
    ("node_groups", "Node Group"),
]

# Check existing datablocks
for attr, label in datablocks:
    if hasattr(bpy.data, attr):
        check_names(getattr(bpy.data, attr), label)

# Check nodes inside materials
for mat in bpy.data.materials:
    if mat.node_tree:
        check_nodes(mat.node_tree, f"Material '{mat.name}'")

# Check nodes inside node groups
for ng in bpy.data.node_groups:
    check_nodes(ng, f"NodeGroup '{ng.name}'")

# Format results
if bad_names:
    lines = []
    for category, items in bad_names.items():
        lines.append(f"{category}:")
        lines.extend(items)
        lines.append("")  # spacing
    result = "\n".join(lines).strip()
else:
    result = "No non-Latin names found."

# Copy to clipboard
bpy.context.window_manager.clipboard = result

show_console()
clear_console()

print("Copied to clipboard:")
print(result)
print("\nPress Ctrl+V in any text editor to paste.")

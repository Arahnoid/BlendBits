"""
remove_material_duplicates.py
-----------------------------

Description:
    This script scans all materials in the current .blend file and identifies
    duplicate materials created by Blender's automatic naming convention
    (e.g. "Material", "Material.001", "Material.002", etc.).

It performs the following steps:
    1. Detects "original" materials (without numeric suffix) and maps them
    to their duplicates (with .001, .002, etc.).
    2. Replaces all occurrences of duplicate materials in all objects
       across all scenes with their corresponding original material.
    3. Purges unused duplicate materials using Blender's Orphan Data Purge.

Usage:
    - Open the script in Blender's Text Editor.
    - Press Alt+P to run.
    - All duplicate materials will be replaced and removed automatically.

Note:
    - Only duplicates with numeric suffixes (.001, .002, etc.) are handled.
    - If the suffix-free original material does not exist, duplicates will be skipped.
"""

import bpy
import re

# --- CONFIG ---
suffix_pattern = re.compile(r"\.\d{3}$")  # Matches .001, .002, etc.

# Step 1: Map base material name → original material
base_to_original = {}
for mat in bpy.data.materials:
    base_name = suffix_pattern.sub("", mat.name)
    # Pick the first one without a suffix as "original"
    if not suffix_pattern.search(mat.name):
        base_to_original[base_name] = mat

# Step 2: Replace duplicates with original materials
for obj in bpy.data.objects:
    if not hasattr(obj.data, "materials"):
        continue
    for slot_index, mat in enumerate(obj.data.materials):
        if not mat:
            continue
        base_name = suffix_pattern.sub("", mat.name)
        if base_name in base_to_original and mat != base_to_original[base_name]:
            obj.data.materials[slot_index] = base_to_original[base_name]

# Step 3: Remove unused materials
bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)

print("✅ Duplicate materials replaced and purged.")

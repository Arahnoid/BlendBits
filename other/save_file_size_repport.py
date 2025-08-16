"""
save_file_size_repport.py
-------------------------
Description:
    This Blender script adds two handlers that monitor the size of the current .blend
    file before and after each save operation.  When a file is saved, the script
    compares the new file size to the previous size and displays a popup showing
    the change in megabytes.

Features:
    * Records the file size immediately before a save (`save_pre` handler).
    * Calculates the new file size after a save (`save_post` handler).
    * Shows a popup message with the format:
    "Before: X.mb / Change: ±Y.mb / After: Z.mb"

Usage:
    Simply run or append this script in a Blender project.  No additional setup is
    required; the handlers are automatically registered if they are not already
    present.
"""

import os
import bpy

# Access the current Blender context
context = bpy.context


def get_filesize():
    """
    Returns the current .blend file size in MB (rounded to 1 decimal).
    Returns 0.0 if the file hasn't been saved yet.
    """
    filepath = bpy.data.filepath
    if not filepath:
        return 0.0  # Prevent error if file is unsaved

    filesize_mb = round(os.path.getsize(filepath) / (1024 * 1024), 1)
    return filesize_mb


def save_before(scene):
    """
    Handler function to store file size before saving.
    """
    context.scene["pre_save_filesize"] = get_filesize()


def save_after(scene):
    """
    Handler function to compare file size after saving and show a popup.
    """
    pre_size = context.scene.get("pre_save_filesize", 0.0)
    post_size = get_filesize()
    size_change = round(post_size - pre_size, 1)

    change_str = f"{'+' if size_change > 0 else ''}{size_change}mb"

    # Define UI popup message
    def win_alert(self, context):
        self.layout.label(
            text=f"Before: {pre_size}mb / Change: {change_str} / After: {post_size}mb"
        )

    bpy.context.window_manager.popup_menu(
        win_alert, title="File Size Info", icon="INFO"
    )


# Avoid double registration of handlers
if save_before not in bpy.app.handlers.save_pre:
    bpy.app.handlers.save_pre.append(save_before)

if save_after not in bpy.app.handlers.save_post:
    bpy.app.handlers.save_post.append(save_after)

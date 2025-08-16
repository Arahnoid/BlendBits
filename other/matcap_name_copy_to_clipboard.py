"""
matcap_name_copy_to_clipboard.py
--------------------------------

Description:
    Copies the active MatCap ID (the ID of the studio light used in the 3‑D
    viewport shading) to the system clipboard so it can be pasted elsewhere.

Prerequisites:
    * Blender 2.8+ (the script uses the new `bpy.context.window.screen.areas`
      API).
    * On Linux you need `xclip` or an equivalent clipboard program
      installed, because the script falls back to `xclip -selection clipboard`.

How to use:
    1. Open the Scripting workspace in Blender.
    2. Create a new text block and paste the entire script.
    3. Press **Alt + P** (or click the “Run Script” button) to execute.
    4. The MatCap ID will be printed in the system console and copied to the
       clipboard – you can paste it into any text editor or terminal.

Notes:
    * The script must be executed while a 3‑D viewport is present in the
      current screen layout, otherwise it will print “3D Viewport not found in
      current context.” and will not copy anything.
    * The clipboard command varies by operating system:
      - Windows: uses the `clip` utility.
      - macOS: uses `pbcopy`.
      - Linux: uses `xclip` (or `xsel` if you modify the script).
"""

import subprocess
import platform
import bpy


def copy_to_clipboard(text):
    system = platform.system()
    if system == "Windows":
        subprocess.run("clip", universal_newlines=True, input=text)
    elif system == "Darwin":
        subprocess.run("pbcopy", universal_newlines=True, input=text)
    else:  # Linux
        subprocess.run(
            "xclip -selection clipboard",
            universal_newlines=True,
            input=text,
            shell=True,
        )


# Make sure we're in a 3D Viewport context
area = next(
    (area for area in bpy.context.window.screen.areas if area.type == "VIEW_3D"), None
)

if area:
    for space in area.spaces:
        if space.type == "VIEW_3D":
            matcap_id = space.shading.studio_light
            print(f"Active MatCap ID: {matcap_id}")
            copy_to_clipboard(matcap_id)
            break
else:
    print("3D Viewport not found in current context.")

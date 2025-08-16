bl_info = {
    "name": "Copy Objects Names from Outliner",
    "author": "BlendBits",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Outliner > Right-Click on Object",
    "description": "Adds a right-click option to copy selected items names to the clipboard",
    "category": "Outliner",
}

import bpy
import subprocess
import platform


def copy_to_clipboard(text):
    """Copy text to clipboard."""
    system = platform.system()
    try:
        if system == "Windows":
            subprocess.run("clip", universal_newlines=True, input=text)
        elif system == "Darwin":  # macOS
            subprocess.run("pbcopy", universal_newlines=True, input=text)
        else:  # Assume Linux
            subprocess.run(
                "xclip -selection clipboard",
                shell=True,
                universal_newlines=True,
                input=text,
            )
    except Exception as e:
        print("Error copying to clipboard:", e)


class OUTLINER_OT_copy_selected_names(bpy.types.Operator):
    """Copy selected object names to clipboard"""

    bl_idname = "outliner.copy_selected_names"
    bl_label = "Copy Selected Names"
    bl_options = {"REGISTER"}

    def execute(self, context):
        selected_objects = context.selected_ids
        names = [obj.name for obj in selected_objects if hasattr(obj, "name")]
        if names:
            text = "\n".join(names)
            copy_to_clipboard(text)
            self.report({"INFO"}, "Copied to clipboard")
        else:
            self.report({"WARNING"}, "No objects selected")
        return {"FINISHED"}


def draw_outliner_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(OUTLINER_OT_copy_selected_names.bl_idname, icon="COPYDOWN")


def register():
    bpy.utils.register_class(OUTLINER_OT_copy_selected_names)
    bpy.types.OUTLINER_MT_object.append(draw_outliner_menu)


def unregister():
    bpy.types.OUTLINER_MT_object.remove(draw_outliner_menu)
    bpy.utils.unregister_class(OUTLINER_OT_copy_selected_names)


if __name__ == "__main__":
    register()

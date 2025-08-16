"""
script_runner.py
----------------

Description:
    This add-on allows you to organize and run custom Python scripts
    directly inside Blender. Scripts are grouped into categories
    (subfolders), which makes managing large script collections easier.

Features:
    - Define a parent "scripts" folder that contains subfolders (categories).
    - Each subfolder appears as a Category in the UI.
    - Selecting a category updates the Script dropdown with available `.py` files.
    - Run the selected script with one click.
    - Optionally refresh the category/script lists with the refresh button.

Usage:
    1. Place your `.py` scripts in subfolders inside your chosen scripts directory.
    Example:
        scripts/
            modeling/
                bevel_tools.py
                cleanup.py
            rendering/
                setup_cycles.py
                render_preset.py

    2. In Blender, open the Sidebar (N-panel) in the 3D Viewport.
    3. Go to the "Tool" tab → "Script Runner" panel.
    4. Select a Category (subfolder).
    5. Choose a Script and click the Play button to run it.

Tips:
    - You can use a relative folder path (e.g., `//scripts/`).
    - To hide the script folder path from the UI, remove it from the panel draw function
      or move it to Add-on Preferences.
    - Works best when you keep reusable scripts organized by category.
"""

import os
import bpy

bl_info = {
    "name": "Script Runner",
    "author": "Your Name",
    "version": (1, 1, 0),
    "blender": (3, 0, 0),
    "location": "3D Viewport > Sidebar > Tool Tab > Script Runner",
    "description": "Run Python scripts from organized subfolders (categories).",
    "warning": "",
    "doc_url": "",
    "category": "Development",
}

# --- Callbacks to Populate Enums ---


def get_script_categories(self, context):
    base = self.folder_path
    if os.path.isdir(base):
        return [
            (d, d, "")
            for d in sorted(os.listdir(base))
            if os.path.isdir(os.path.join(base, d))
            and d not in SCRIPT_RUNNER_PN.IGNORED_FOLDERS
        ]
    return []


def get_scripts_in_category(self, context):
    base = self.folder_path
    cat = self.category
    cat_path = os.path.join(base, cat) if cat else ""
    if os.path.isdir(cat_path):
        return [(f, f, "") for f in sorted(os.listdir(cat_path)) if f.endswith(".py")]
    return []


# --- Property Group ---


class SCRIPT_RUNNER_PN(bpy.types.PropertyGroup):
    # Folders that should not appear in category list
    IGNORED_FOLDERS = {".git", "__pycache__", ".idea", ".vscode", "venv"}

    folder_path: bpy.props.StringProperty(
        name="",
        description="Path to parent folder with categories",
        default="//scripts/",
        subtype="DIR_PATH",
    )

    category: bpy.props.EnumProperty(
        name="",
        description="Choose script category (sub-folder)",
        items=lambda self, ctx: get_script_categories(self, ctx),
    )

    script_files: bpy.props.EnumProperty(
        name="",
        description="Scripts in selected category",
        items=lambda self, ctx: get_scripts_in_category(self, ctx),
    )


# --- Script Runner Operator ---


class SCRIPT_RUNNER_OT_run_script(bpy.types.Operator):
    bl_idname = "wm.run_selected_script"
    bl_label = "Run Selected Script"

    def execute(self, context):
        props = context.scene.script_runner_props
        folder = props.folder_path
        cat = props.category
        script = props.script_files

        if not (folder and cat and script):
            self.report({"ERROR"}, "Category or script not selected.")
            return {"CANCELLED"}

        script_path = os.path.join(folder, cat, script)
        try:
            with open(script_path, "r") as f:
                exec(compile(f.read(), script_path, "exec"), {"__name__": "__main__"})
            self.report({"INFO"}, f"Ran script: {cat}/{script}")
        except Exception as e:
            self.report({"ERROR"}, f"Error running {script}: {e}")
            return {"CANCELLED"}

        return {"FINISHED"}


# --- Refresh Operator (Manual Update) ---


class SCRIPT_RUNNER_OT_update_script_list(bpy.types.Operator):
    bl_idname = "wm.update_script_list"
    bl_label = ""
    bl_icon = "REFRESH"
    bl_description = "Refresh category and script list"

    # noinspection PyMethodMayBeStatic
    def execute(self, context):
        context.area.tag_redraw()
        return {"FINISHED"}


class SCRIPT_RUNNER_OT_set_folder(bpy.types.Operator):
    bl_idname = "wm.set_script_folder"
    bl_label = "Set Scripts Folder"
    bl_description = "Choose the root folder containing script categories"

    directory: bpy.props.StringProperty(
        name="Folder Path",
        description="Select the folder containing script categories",
        subtype="DIR_PATH",
    )

    def execute(self, context):
        props = context.scene.script_runner_props
        props.folder_path = self.directory
        self.report({"INFO"}, f"Script folder set to: {self.directory}")
        return {"FINISHED"}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


# --- UI Panel ---


class SCRIPT_RUNNER_PT_panel(bpy.types.Panel):
    bl_label = "Script Runner"
    bl_idname = "SCENE_PT_script_runner"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "DEV"

    def draw(self, context):
        layout = self.layout
        props = context.scene.script_runner_props

        row = layout.row()

        # Folder path
        # row.prop(props, "folder_path")
        row.operator(SCRIPT_RUNNER_OT_set_folder.bl_idname)
        row.operator(SCRIPT_RUNNER_OT_update_script_list.bl_idname, icon="FILE_REFRESH")

        layout.prop(props, "category")
        row = layout.row()
        if props.category:
            row.prop(props, "script_files")
            row.operator(SCRIPT_RUNNER_OT_run_script.bl_idname, text="", icon="PLAY")
        else:
            row.label(text="Select a category", icon="INFO")


# --- Registration ---

classes = (
    SCRIPT_RUNNER_PN,
    SCRIPT_RUNNER_PT_panel,
    SCRIPT_RUNNER_OT_run_script,
    SCRIPT_RUNNER_OT_set_folder,
    SCRIPT_RUNNER_OT_update_script_list,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.script_runner_props = bpy.props.PointerProperty(
        type=SCRIPT_RUNNER_PN
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.script_runner_props


if __name__ == "__main__":
    register()

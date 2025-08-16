bl_info = {
    "name": "Copy Collection Names from Outliner",
    "author": "BlendBits",
    "version": (1, 0),
    "blender": (4, 0, 0),
    "location": "Outliner > Right-Click on Collection",
    "description": "Adds a right-click option to copy selected collection names to the clipboard",
    "category": "Outliner",
}

import bpy

# -----------------------------------------------------------------------------
# Operator: Copies names of selected collections in the Outliner to clipboard
# -----------------------------------------------------------------------------


class OUTLINER_OT_copy_selected_collection_names(bpy.types.Operator):
    """Copy names of all selected collections in the Outliner to system clipboard"""

    bl_idname = "outliner.copy_selected_collection_names"
    bl_label = "Copy Collection Names"
    bl_description = "Copies names of selected collections in the Outliner to clipboard"

    def execute(self, context):
        # Get all selected items in the Outliner
        selected_ids = context.selected_ids
        selected_collections = [
            item for item in selected_ids if isinstance(item, bpy.types.Collection)
        ]

        if selected_collections:
            names = [col.name for col in selected_collections]
            text = "\n".join(names)
            context.window_manager.clipboard = text
            self.report(
                {"INFO"}, f"Copied {len(names)} collection name(s) to clipboard"
            )
        else:
            self.report({"WARNING"}, "No collections selected in Outliner")

        return {"FINISHED"}


# -----------------------------------------------------------------------------
# UI: Add menu entry to Outliner's Collection right-click context menu
# -----------------------------------------------------------------------------


def draw_collection_menu(self, context):
    layout = self.layout
    layout.separator()
    layout.operator(
        OUTLINER_OT_copy_selected_collection_names.bl_idname, icon="COPYDOWN"
    )


# -----------------------------------------------------------------------------
# Register / Unregister
# -----------------------------------------------------------------------------

classes = (OUTLINER_OT_copy_selected_collection_names,)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.OUTLINER_MT_collection.append(draw_collection_menu)


def unregister():
    bpy.types.OUTLINER_MT_collection.remove(draw_collection_menu)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


# -----------------------------------------------------------------------------
# Allow running script directly from Blender's text editor
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    register()

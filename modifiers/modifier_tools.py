"""
modifier_tools.py
-------------------

Description:
    This Blender add-on adds a panel to the 3D Viewport sidebar (N-panel) that allows you to:
        - Remove specific modifiers or all modifiers from selected objects.
        - Hide (disable) specific modifiers or all modifiers in the viewport.
        - Show (enable) specific modifiers or all modifiers in the viewport.

    The modifier type list is dynamically generated based on modifiers currently present
    in the selected objects.

Usage:
    1. Save this file and install it as an add-on in Blender, or run it directly
       from the Text Editor (Alt+P).
    2. Open the 3D Viewport and press "N" to open the sidebar.
    3. Go to the "Tool" tab and find the "Modifier Tools" panel.
    4. Select the modifier type from the dropdown.
    5. Use the buttons:
         - "Remove Modifier" → delete the modifier(s).
         - "Hide Modifier" → turn off in viewport.
         - "Show Modifier" → turn on in viewport.

Features:
    - Works for all object types that support modifiers.
    - Dynamic dropdown showing only modifiers present in selection.
    - Accurate reporting of affected modifiers.
    - Skips objects without the chosen modifier type.
    - Separate buttons for remove, hide, and show actions.

Notes:
    - Hiding/showing affects only viewport visibility (not render visibility).
    - Removing modifiers is irreversible unless undone (Ctrl+Z).
"""

import bpy
from bpy.types import Operator, Panel


bl_info = {
    "name": "Modifier Tools: Remove / Hide / Show",
    "author": "Your Name",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Tool Tab > Modifier Tools",
    "description": "Remove, hide, or show specific or all modifiers from selected objects.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}


# --------------------------------------------------------------------
# Utility: Get dropdown items dynamically from selected objects
# --------------------------------------------------------------------

def get_modifier_items(self, context):
    """Generate dropdown items based on selected objects."""
    if not context.selected_objects:
        return [("ALL", "All", "Affect every modifier")]
    types = {
        (m.type, m.type.title(), f"Affect {m.type.title()} modifiers")
        for obj in context.selected_objects
        for m in obj.modifiers
    }
    if not types:
        return [("ALL", "All", "Affect every modifier")]
    return [("ALL", "All", "Affect every modifier")] + sorted(types, key=lambda x: x[1])


# --------------------------------------------------------------------
# Operator: Remove modifiers
# --------------------------------------------------------------------
class RemoveModifierOperator(Operator):
    """Remove selected modifier(s) from all selected objects"""

    bl_idname = "object.remove_modifier"
    bl_label = "Delete"

    mod_type: bpy.props.EnumProperty(
        name="Modifier Type",
        description="Choose which modifier type to remove",
        items=get_modifier_items,
    )

    def execute(self, context):
        total_removed = 0
        for obj in context.selected_objects:
            to_remove = [
                m
                for m in obj.modifiers
                if self.mod_type == "ALL" or m.type == self.mod_type
            ]
            for m in to_remove:
                obj.modifiers.remove(m)
                total_removed += 1
        self.report({"INFO"}, f"Removed {total_removed} modifier(s)")
        return {"FINISHED"}


# --------------------------------------------------------------------
# Operator: Hide modifiers
# --------------------------------------------------------------------
class HideModifierOperator(Operator):
    """Hide selected modifier(s) in the viewport"""

    bl_idname = "object.hide_modifier"
    bl_label = "Hide"

    mod_type: bpy.props.EnumProperty(
        name="Modifier Type",
        description="Choose which modifier type to hide",
        items=get_modifier_items,
    )

    def execute(self, context):
        total_hidden = 0
        for obj in context.selected_objects:
            to_hide = [
                m
                for m in obj.modifiers
                if self.mod_type == "ALL" or m.type == self.mod_type
            ]
            for m in to_hide:
                m.show_viewport = False
                total_hidden += 1
        self.report({"INFO"}, f"Hidden {total_hidden} modifier(s)")
        return {"FINISHED"}


# --------------------------------------------------------------------
# Operator: Show modifiers
# --------------------------------------------------------------------
class ShowModifierOperator(Operator):
    """Show selected modifier(s) in the viewport"""

    bl_idname = "object.show_modifier"
    bl_label = "Show"

    mod_type: bpy.props.EnumProperty(
        name="Modifier Type",
        description="Choose which modifier type to show",
        items=get_modifier_items,
    )

    def execute(self, context):
        total_shown = 0
        for obj in context.selected_objects:
            to_show = [
                m
                for m in obj.modifiers
                if self.mod_type == "ALL" or m.type == self.mod_type
            ]
            for m in to_show:
                m.show_viewport = True
                total_shown += 1
        self.report({"INFO"}, f"Shown {total_shown} modifier(s)")
        return {"FINISHED"}


# --------------------------------------------------------------------
# Panel in 3D Viewport Sidebar
# --------------------------------------------------------------------
class VIEW3D_PT_modifier_tools_panel(Panel):
    bl_label = "Modifier Tools"
    bl_idname = "VIEW3D_PT_modifier_tools_panel"
    bl_space_type = "VIEW_3D"  # 3-D Viewport
    bl_region_type = "UI"  # Sidebar (N-panel)
    bl_category = "Tool"  # Tab name in the sidebar

    def draw(self, context):
        layout = self.layout
        layout.label(text="Choose Modifier Type:")
        layout.prop(context.scene, "modifier_tool_type", text="")
        row = layout.row()
        row.operator(RemoveModifierOperator.bl_idname, icon="TRASH").mod_type = (
            context.scene.modifier_tool_type
        )
        row.operator(HideModifierOperator.bl_idname, icon="HIDE_ON").mod_type = (
            context.scene.modifier_tool_type
        )
        row.operator(ShowModifierOperator.bl_idname, icon="HIDE_OFF").mod_type = (
            context.scene.modifier_tool_type
        )


# --------------------------------------------------------------------
# Registration
# --------------------------------------------------------------------

classes = (
    RemoveModifierOperator,
    HideModifierOperator,
    ShowModifierOperator,
    VIEW3D_PT_modifier_tools_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.modifier_tool_type = bpy.props.EnumProperty(
        name="Modifier Type",
        description="Choose which modifier type to affect",
        items=get_modifier_items,
        default="ALL",
    )


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.modifier_tool_type


if __name__ == "__main__":
    register()

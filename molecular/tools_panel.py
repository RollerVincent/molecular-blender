import bpy

class Tools_PT_Panel(bpy.types.Panel):
    bl_idname = "panel.tools"
    bl_label = "Tools"
    bl_category = "Molecular"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('button.clear', text = 'Clear scene')

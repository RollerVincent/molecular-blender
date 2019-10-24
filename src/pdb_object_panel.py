import bpy
from .pdb_object import PDB_Object

class PDB_Object_PT_Panel(bpy.types.Panel):
    bl_idname = "panel.pdb_object"
    bl_label = "PDB"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        
        layout.operator('dropdown.color')
        #row.prop(context.scene, "input_pdb_coloring")

    @classmethod
    def poll(cls, context):
        if context.object.name in PDB_Object.__objects__:
            return True
        else:
            return False

import bpy
from .pdb_object import PDB_Object

class PDB_Object_PT_Panel(bpy.types.Panel):
    bl_idname = "panel.pdb_object"
    bl_label = "PDBhh"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
   # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('button.pdb_rep_surf', text = '', icon = 'SHADING_WIRE')
        row.operator('button.pdb_rep_spf', text = '', icon = 'SHADING_SOLID')   
        row.operator('dropdown.color')

      

     

    @classmethod
    def poll(cls, context):
        if context.object.name in PDB_Object.__objects__:
            return True
        else:
            return False

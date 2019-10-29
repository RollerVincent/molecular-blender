import bpy
from .pdb_object import PDB_Object

class PDB_Object_PT_Panel(bpy.types.Panel):
    bl_idname = "panel.pdb_object"
    bl_label = "PDB"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
   # bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        box.label(text = 'ATOM')
        row = box.row()
        row.operator('button.pdb_rep_surf', text = '', icon = 'MOD_SMOKE')
        row.operator('button.pdb_rep_spf', text = '', icon = 'META_DATA')
        row.operator('button.pdb_rep_ssg', text = '', icon = 'STROKE')   
        row.operator('dropdown.color')

        box = layout.box()
        box.label(text = 'HETATM')
        row = box.row()
        row.operator('button.pdb_rep_surf_het', text = '', icon = 'MOD_SMOKE')
        row.operator('button.pdb_rep_spf_het', text = '', icon = 'META_DATA')
        row.operator('dropdown.color_het')

      

     

    @classmethod
    def poll(cls, context):
        if context.object.name in PDB_Object.__objects__:
            return True
        else:
            return False

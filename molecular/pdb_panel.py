import bpy

class PDB_PT_Panel(bpy.types.Panel):
    bl_idname = "panel.pdb"
    bl_label = "PDB"
    bl_icon ='WORLD_DATA'
    bl_category = "Molecular"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout
        layout.prop(context.scene, "input_pdb_id")
        layout.prop(context.scene, "input_object_name")
        layout.operator('button.pdb_id', text = 'Create Object')
        
        
        

        
        
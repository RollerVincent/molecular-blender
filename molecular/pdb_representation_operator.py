import bpy
from . pdb_object import PDB_Object

class PDB_Representation(bpy.types.Operator):
    bl_idname = "dropdown.rep"
    bl_label = "Representation"
    bl_register = True
    bl_options = {'REGISTER', 'UNDO'}


    total: bpy.props.IntProperty(name="Steps", default=2, min=1, max=100)



    def execute(self, context):
        print(self.total)
       




        
        
        


        
        return {'FINISHED'}

 
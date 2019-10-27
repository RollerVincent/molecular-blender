import bpy
from . pdb_data import PDB_Data
from . pdb_object import PDB_Object


class PDB_ID_OT_Operator(bpy.types.Operator):
    bl_idname = "button.pdb_id"
    bl_label = "PDB_ID_OT_Operator"
    bl_description = "load structure data"

    __current_id__ = None

    def execute(self, context):
        if context.scene.input_pdb_id != PDB_ID_OT_Operator.__current_id__:
            PDB_ID_OT_Operator.__current_id__ = context.scene.input_pdb_id
            PDB_Data(context.scene.input_pdb_id)
        pdb_obj = PDB_Object()
        return {'FINISHED'}

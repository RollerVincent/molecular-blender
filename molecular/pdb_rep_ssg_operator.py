import bpy
from . pdb_data import PDB_Data
from . pdb_object import PDB_Object


class PDB_REP_SSG_OT_Operator(bpy.types.Operator):
    bl_idname = "button.pdb_rep_ssg"
    bl_label = "Sausage"
    bl_description = "Change to sausage representation"

    def execute(self, context):
        obj = PDB_Object.__objects__[context.object.name]
        if obj.representation != 'sausage':
            obj.set_representation('sausage')
            obj.recolor(obj.color_sheme)
            obj.rescale(obj.atom_scale)
        return {'FINISHED'}

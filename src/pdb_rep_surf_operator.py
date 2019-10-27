import bpy
from . pdb_data import PDB_Data
from . pdb_object import PDB_Object


class PDB_REP_SURF_OT_Operator(bpy.types.Operator):
    bl_idname = "button.pdb_rep_surf"
    bl_label = "Surface"
    bl_description = "Change to surface representation"

    def execute(self, context):
        obj = PDB_Object.__objects__[context.object.name]
        if obj.representation != 'surface':
            obj.set_representation('surface')
            obj.recolor(obj.color_sheme)
            obj.rescale(obj.atom_scale)
        return {'FINISHED'}

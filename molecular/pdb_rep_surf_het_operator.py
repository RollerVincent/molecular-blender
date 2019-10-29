import bpy
from . pdb_data import PDB_Data
from . pdb_object import PDB_Object


class PDB_REP_SURF_HET_OT_Operator(bpy.types.Operator):
    bl_idname = "button.pdb_rep_surf_het"
    bl_label = "Surface"
    bl_description = "Change to surface representation"

    def execute(self, context):
        obj = PDB_Object.__objects__[context.object.name]
        if obj.het_representation != 'surface':
            obj.set_het_representation('surface')
            obj.het_recolor(obj.het_color_sheme)
            obj.het_rescale(obj.het_atom_scale)
        return {'FINISHED'}

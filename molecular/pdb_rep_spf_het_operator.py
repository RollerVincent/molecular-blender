import bpy
from . pdb_data import PDB_Data
from . pdb_object import PDB_Object


class PDB_REP_SPF_HET_OT_Operator(bpy.types.Operator):
    bl_idname = "button.pdb_rep_spf_het"
    bl_label = "SPACEFILL"
    bl_description = "Change to spacefill representation"

    def execute(self, context):
        obj = PDB_Object.__objects__[context.object.name]
        if obj.het_representation != 'spacefill':
            obj.set_het_representation('spacefill')
            obj.het_recolor(obj.het_color_sheme)
            obj.het_rescale(obj.het_atom_scale)
        return {'FINISHED'}

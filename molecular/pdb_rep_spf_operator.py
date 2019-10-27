import bpy
from . pdb_data import PDB_Data
from . pdb_object import PDB_Object


class PDB_REP_SPF_OT_Operator(bpy.types.Operator):
    bl_idname = "button.pdb_rep_spf"
    bl_label = "SPACEFILL"
    bl_description = "Change to spacefill representation"

    def execute(self, context):
        obj = PDB_Object.__objects__[context.object.name]
        if obj.representation != 'spacefill':
            obj.set_representation('spacefill')
            obj.recolor(obj.color_sheme)
            obj.rescale(obj.atom_scale)
        return {'FINISHED'}

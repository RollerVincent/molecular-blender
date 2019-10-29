import bpy
from . pdb_object import PDB_Object

class PDB_HET_Coloring(bpy.types.Operator):
    bl_idname = "dropdown.color_het"
    bl_label = "Apperance"
    bl_register = True
    bl_options = {'REGISTER', 'UNDO'}

    color_sheme = bpy.props.EnumProperty \
      (
        items = 
        (
            ('uni', 'Unicolor', 'Colors the structure in one color'), 
            ('element', 'Element', 'Colors the structure by element (Spacefill only)'),    
        ),
        name = "Coloring",
      )
    
    atom_scale = bpy.props.FloatProperty \
      (
        name = "Volume",
        default = 1.5
      )

    def execute(self, context):
        obj = PDB_Object.__objects__[context.object.name]
        obj.het_recolor(self.color_sheme)
        obj.het_rescale(self.atom_scale)
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = PDB_Object.__objects__[context.object.name]
        self.atom_scale = obj.het_atom_scale
        self.color_sheme = obj.het_color_sheme
        wm = context.window_manager
        return wm.invoke_props_popup(self, event)

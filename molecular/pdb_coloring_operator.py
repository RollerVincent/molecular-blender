import bpy
from . pdb_object import PDB_Object

class PDB_Coloring(bpy.types.Operator):
    bl_idname = "dropdown.color"
    bl_label = "Apperance"
    bl_register = True
    bl_options = {'REGISTER', 'UNDO'}

    color_sheme = bpy.props.EnumProperty \
      (
        items = 
        (
            ('compound', 'Compound', 'Colors the structure by compound'), 
            ('uni', 'Unicolor', 'Colors the structure in one color'),
            ('chain', 'Chain', 'Colors the structure by chain'),    
            ('compound', 'Compound', 'Colors the structure by compound'),    
            ('element', 'Element', 'Colors the structure by element (Spacefill only)'),    
        ),
        name = "Coloring",
      )
    
    atom_scale = bpy.props.FloatProperty \
      (
        name = "Volume",
        default = 1.8
      )

    def execute(self, context):
        obj = PDB_Object.__objects__[context.object.name]
        obj.recolor(self.color_sheme)
        obj.rescale(self.atom_scale)
        return {'FINISHED'}

    def invoke(self, context, event):
        obj = PDB_Object.__objects__[context.object.name]
        self.atom_scale = obj.atom_scale
        self.color_sheme = obj.color_sheme
        wm = context.window_manager
        return wm.invoke_props_popup(self, event)

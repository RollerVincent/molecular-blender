import bpy
from . pdb_object import PDB_Object

class PDB_Coloring(bpy.types.Operator):
    bl_idname = "dropdown.color"
    bl_label = "Apperance"
    bl_register = True
    bl_options = {'REGISTER', 'UNDO'}




 #   representation = bpy.props.EnumProperty \
  #    (
   #     items = 
    #    (
     #       ('spacefill', 'Spacefill', 'Colors the structure in one color'),
      #      ('surface', 'Surface', 'Colors the structure by chain'),       
       # ),
        #name = "Representation",
      #)


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

     #   if obj.color_sheme != self.color_sheme:
      #      obj.recolor(self.color_sheme)

      #  if obj.atom_scale != self.atom_scale:
       #     obj.rescale(self.atom_scale)

    #    if obj.representation != self.representation:
     #       obj.set_representation(self.representation)




        
        
        


        
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_popup(self, event)

import bpy


class Clear_OT_Operator(bpy.types.Operator):
    bl_idname = "button.clear"
    bl_label = "Clear_OT_Operator"
    bl_description = "Clear scene"

    def execute(self, context):
        
        bpy.ops.object.select_all(action='SELECT')

        bpy.data.objects['Camera'].select_set(False)
        bpy.data.objects['Light'].select_set(False)

        bpy.ops.object.delete() 

        
        return {'FINISHED'}

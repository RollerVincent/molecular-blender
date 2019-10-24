import bpy

class Assets:
    
    __element_templates_object__ = None
    __element_colors__ = None
    __element_radii__ = None

    def load(self):
        self.materials()

        obj = bpy.data.objects.new("Element_templates", None)
        bpy.context.scene.collection.objects.link(obj)
        obj.location = [1000000, 0, 0]
        Assets.__element_templates_object__ = obj.name

        Assets.__element_colors__ = {
                ' O': (0.9, 0.5, 0.5, 1),
                ' C': (0.7, 0.7, 0.7, 1),
                ' N': (0.5, 0.5, 0.9, 1),
                ' H': (1.0, 1.0, 1.0, 1),
                ' S': (0.9, 0.9, 0.5, 1),
                ' P': (0.9, 0.7, 0.5, 1)
        }
        Assets.__element_radii__ = {
                ' O': 0.66,
                ' C': 0.77,
                ' N': 0.71,
                ' H': 0.31,
                ' S': 1.05,
                ' P': 2
            }
       

    def __material__(name, template, color):
        
        mat = bpy.data.materials.new(name=name)

        if template == 'surface_base':
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes["Principled BSDF"].inputs[0].default_value = color

            nodes["Principled BSDF"].inputs[1].default_value = 0.2              # subsurface
            nodes["Principled BSDF"].inputs[5].default_value = 0.1                # specular

        return mat


    def materials(self):
        mat = bpy.data.materials.new(name="SpaceFill")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs[1].default_value = 0.05
        nodes["Principled BSDF"].inputs[5].default_value = 0.1
        vertex_colors = nodes.new('ShaderNodeAttribute')
        nodes["Attribute"].attribute_name = "Col"
        mat.node_tree.links.new(nodes["Attribute"].outputs["Color"], nodes["Principled BSDF"].inputs[0])
        tex_coord = nodes.new('ShaderNodeTexCoord')
        nodes["Principled BSDF"].inputs[5].default_value


        mat = bpy.data.materials.new(name="SurfaceBase")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes["Principled BSDF"].inputs[1].default_value = 0.05               # subsurface
        nodes["Principled BSDF"].inputs[5].default_value = 0.1                # specular
       
        

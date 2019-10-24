import bpy 
from .mesh import Mesh

class Sphere:

    def __init__(self, name, loc, scale, color, material):
        m = Mesh(name)
        m.spheres([loc], [scale], [color], subdivisions=2)   
        m.obj.data.materials.append(material)     
        for f in m.obj.data.polygons:
            f.use_smooth = True
        self.obj = m.obj
import bpy 
from math import sqrt 
import time



class PointCloud:
    def __init__(self, name):
        self.mesh = bpy.data.meshes.new(name)
        self.verts = []
        self.name = name
        self.obj = None
        
    def build(self):
        self.mesh.from_pydata(self.verts, [], [])
        self.obj = bpy.data.objects.new(self.name, self.mesh)
        bpy.context.scene.collection.objects.link(self.obj)

    def add_spheres(self, verts, scale, color, material):
        pass

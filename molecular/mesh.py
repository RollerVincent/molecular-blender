import bpy 
from math import sqrt 
import time



class Mesh:
    def __init__(self, name):
        self.mesh = bpy.data.meshes.new(name)
        self.verts = []
        self.faces = []
        self.name = name
        self.obj = None
        self.vert_colors = []
        
    def build(self):
        self.mesh.from_pydata(self.verts, [], self.faces)
        self.obj = bpy.data.objects.new(self.name, self.mesh)
        bpy.context.scene.collection.objects.link(self.obj)
 
 
        t = time.time()
 
        mesh = self.obj.data
        mesh.vertex_colors.new()

        vcol_layer = mesh.vertex_colors.active
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                loop_vert_index = mesh.loops[loop_index].vertex_index
                vcol_layer.data[loop_index].color = self.vert_colors[loop_vert_index]
                
        mesh.update()

        t2 = time.time()
        print('Coloring took ' + str(t2-t) + ' \n')

    def icosphere(self, subdivisions):
        phi = (1 + sqrt(5)) / 2
        def vertex(x, y, z):
            length = sqrt(x**2 + y**2 + z**2) 
            return [i / length for i in (x,y,z)]

        v = [
             vertex(-1, phi, 0),
             vertex( 1, phi, 0),
             vertex(-1, -phi, 0),
             vertex( 1, -phi, 0),
             vertex(0, -1, phi),
             vertex(0, 1, phi),
             vertex(0, -1, -phi),
             vertex(0, 1, -phi),
             vertex( phi, 0, -1),
             vertex( phi, 0, 1),
             vertex(-phi, 0, -1),
             vertex(-phi, 0, 1)
        ]

        f = [
            [0, 11, 5], 
            [0, 5, 1], 
            [0, 1, 7], 
            [0, 7, 10], 
            [0, 10, 11],
            [1, 5, 9], 
            [5, 11, 4], 
            [11, 10, 2], 
            [10, 7, 6], 
            [7, 1, 8],
            [3, 9, 4], 
            [3, 4, 2], 
            [3, 2, 6], 
            [3, 6, 8], 
            [3, 8, 9],
            [4, 9, 5], 
            [2, 4, 11], 
            [6, 2, 10], 
            [8, 6, 7], 
            [9, 8, 1]
        ]


        middle_point_cache = {}
        def middle_point(point_1, point_2):
            smaller_index = min(point_1, point_2)
            greater_index = max(point_1, point_2)

            key = '{0}-{1}'.format(smaller_index, greater_index)

            if key in middle_point_cache: 
                return middle_point_cache[key]

            vert_1 = v[point_1] 
            vert_2 = v[point_2]

            m = [(vert_1[0]+vert_2[0])/2.0, (vert_1[1]+vert_2[1])/2.0, (vert_1[2]+vert_2[2])/2.0]
            m = vertex(m[0], m[1], m[2])

          
            v.append(m)
            index = len(v) - 1
            middle_point_cache[key] = index

            return index


        for i in range(subdivisions): 
            faces_subdiv = [] 
            for tri in f: 
                v1 = middle_point(tri[0], tri[1]) 
                v2 = middle_point(tri[1], tri[2]) 
                v3 = middle_point(tri[2], tri[0]) 
                faces_subdiv.append([tri[0], v1, v3]) 
                faces_subdiv.append([tri[1], v2, v1]) 
                faces_subdiv.append([tri[2], v3, v2]) 
                faces_subdiv.append([v1, v2, v3]) 
            f = faces_subdiv

        return [v, f]

    def spheres(self, locations, scales, colors, subdivisions = 3):
        t = time.time()
        ico = self.icosphere(subdivisions)
        lv = len(ico[0])
        fc = 0
        for i,l in enumerate(locations):
            for v in ico[0]:
                self.verts.append([v[0]*scales[i]+l[0], v[1]*scales[i]+l[1], v[2]*scales[i]+l[2]])
                self.vert_colors.append(colors[i])
            for f in ico[1]:
                self.faces.append([f[0]+fc, f[1]+fc, f[2]+fc])
            fc += lv

        t2 = time.time()
        print('Generating mesh took ' + str(t2-t) + ' s\n')
        self.build()


    
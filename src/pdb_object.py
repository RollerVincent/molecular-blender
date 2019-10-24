import bpy
from . pdb_data import PDB_Data
from . mesh import Mesh
from . assets import Assets
from random import random
import time
from . point_cloud import PointCloud
from .sphere import Sphere

class PDB_Object:

    __objects__ = {}
   
    __assetsLoaded__ = False
   
    __idNum__ = {}
    __idUniColor__ = {}
    __idChainColors__ = {}
    __idCompoundColors__ = {}



    def __init__(self):
        if not PDB_Object.__assetsLoaded__:
            PDB_Object.__assetsLoaded__ = True
            Assets().load()

        self.data = PDB_Data.__current__
        self.id = self.data.id

        if self.id not in PDB_Object.__idNum__:
            PDB_Object.__idNum__.update({self.id:0})
            PDB_Object.__idChainColors__.update({self.id: self.colors(len(self.data.chains), 0.3, 0.1)})
            PDB_Object.__idCompoundColors__.update({self.id: self.colors(len(self.data.compounds), 0.3, 0.1)})
            PDB_Object.__idUniColor__.update({self.id: self.colors(1, 0.3, 0.1)[0]})
        PDB_Object.__idNum__[self.id] += 1
          
        name = (self.id + '_' + str(PDB_Object.__idNum__[self.id]))
        self.name = name.upper()
        obj = bpy.data.objects.new(name.upper(), None)
        bpy.context.scene.collection.objects.link(obj)
        PDB_Object.__objects__.update({obj.name:self})
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        self.obj = obj

        self.representation = None
        self.initialized_representations = set()
        

        # representaion spacefill
        self.chain_objects = {}
        self.element_objects = {}

        # representaion surface
        self.surface_template = 'surface_base'
        

        self.init_surface()
        self.recolor('compound')
        self.recolor('chain')
        self.recolor('uni')



     #   self.init_spacefill()
      #  if len(self.data.compounds) > 1:
       #     self.recolor('compound')
        #else:
         #   self.recolor('chain')
        #self.rescale(1.8)

        
        

    def colors(self, n, b, t):
        return [(random()*b+1-b-t, random()*b+1-b-t, random()*b+1-b-t, 1) for i in range(n)]

    def rescale(self, value):
        if self.representation == 'spacefill':
            for chain in self.chain_objects:
                for obj in self.chain_objects[chain]:
                    bpy.data.objects[obj].scale = [value, value, value]
        elif self.representation == 'surface':
            for chain in self.data.chains:
                obj_name = chain + '_' + self.name + '.pdb'
                obj = bpy.data.objects[obj_name]
                for i,e in enumerate(obj.data.elements):
                    e.radius = (e.rotation.x/e.rotation.w) * value / 1.8
                    
                print(len(obj.data.elements))
                print('fu')








    def recolor(self, sheme):
        if self.representation == 'spacefill':
            if sheme == 'chain':
                c = {}
                for i,chain in enumerate(self.chain_objects):
                    c.update({chain:self.chain_colors[i]})
                for chain in self.chain_objects:
                    for obj in self.chain_objects[chain]:
                        self.recolor_obj(bpy.data.objects[obj], c[chain])
            elif sheme == 'element':
                for ele in self.element_objects:
                    for obj in self.element_objects[ele]:
                        self.recolor_obj(bpy.data.objects[obj], Assets.__element_colors__[ele])
            elif sheme == 'compound':
                for i,c in enumerate(self.data.compounds):
                    for ch in self.data.compounds[c][1]:
                        for obj in self.chain_objects[ch]:
                            self.recolor_obj(bpy.data.objects[obj], self.compound_colors[i])
        
        if self.representation == 'surface':
            if sheme == 'compound':
                for i,c in enumerate(self.data.compounds):
                    for ch in self.data.compounds[c][1]:
                        obj = bpy.data.objects[ch + '_' + self.name + '.pdb']
                        nn = str(c) + '_' + self.id
                        chain_mat = None
                        if nn not in bpy.data.materials:
                            chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idCompoundColors__[self.id][i])
                        else:
                            chain_mat = bpy.data.materials[nn]
                        obj.data.materials[0] = chain_mat

            elif sheme == 'chain':
                for chain in self.data.chains:
                    obj = bpy.data.objects[chain + '_' + self.name + '.pdb']
                    nn = chain + '_' + self.id
                    chain_mat = None
                    if nn not in bpy.data.materials:
                        chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idChainColors__[self.id][ind])
                    else:
                        chain_mat = bpy.data.materials[nn]
                    obj.data.materials[0] = chain_mat

            elif sheme == 'uni':
                for chain in self.data.chains:
                    obj = bpy.data.objects[chain + '_' + self.name + '.pdb']
                    nn = 'uni' + '_' + self.id
                    chain_mat = None
                    if nn not in bpy.data.materials:
                        chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idUniColor__[self.id])
                    else:
                        chain_mat = bpy.data.materials[nn]
                    obj.data.materials[0] = chain_mat 
                        
                        
    def recolor_obj(self, obj, color):
        mesh = obj.data
        vcol_layer = mesh.vertex_colors.active
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                vcol_layer.data[loop_index].color = color  
        mesh.update()
        obj.data = mesh

    def init_spacefill(self):
        rep = 'spacefill'
        self.initialized_representations.add(rep)
        self.representation = rep
      
        scene = bpy.context.scene
        
        if rep == "spacefill":

            radii = Assets.__element_radii__
            
            colors = Assets.__element_colors__


            l = len(PDB_Object.__objects__)
            mat = bpy.data.materials.get("Spacefill")

            template_spheres = {}
            for j,chain in enumerate(self.data.chains):
                self.chain_objects.update({chain:[]})
                spheres = {}
                for e in radii:
                    spheres.update({e:Sphere(chain + '_' + e.strip() + '_' + self.obj.name, [0,0,0], radii[e]*0.03, colors[e], mat)})
                    if e not in self.element_objects:
                        self.element_objects.update({e:[]})
                    self.element_objects[e].append(spheres[e].obj.name)
                

                for i,s in enumerate(spheres):
                    spheres[s].obj.location = [0,0,0]
                    spheres[s].obj.parent = bpy.data.objects[Assets.__element_templates_object__]
                    self.chain_objects[chain].append(spheres[s].obj.name)
                template_spheres.update({chain:spheres})
            

            for chain in self.data.chains:
                per_elem_loc = {x:[] for x in radii}
                b = 0.4
                obs = []
                for atom in self.data.chains[chain].atoms:
                    if atom[-1] != ' H':
                        per_elem_loc[atom[-1]].append([atom[7]*0.03, atom[8]*0.03, atom[9]*0.03])
                for e in per_elem_loc:
                    if len(per_elem_loc[e]) != 0:
                        ps = self.add_particle_system(per_elem_loc[e], template_spheres[chain][e].obj, chain + '_' + e.strip())
                        obs.append(ps)

            
                obj = bpy.data.objects.new(chain + '_' + self.obj.name, None)
                obj.location = self.obj.location
                bpy.context.scene.collection.objects.link(obj)
                obj.parent = self.obj


                for o in obs:
                    o.parent = obj

    def init_surface(self):
        rep = 'surface'
        self.initialized_representations.add(rep)
        self.representation = rep
      
        
        scene = bpy.context.scene
        radii = Assets.__element_radii__
        colors = Assets.__element_colors__
        numObjs = len(PDB_Object.__objects__)

        for ind, chain in enumerate(self.data.chains):
            name = chain + '_' + self.obj.name + '.pdb'
            
            mball = bpy.data.metaballs.new('metaball_' + name)
            mball_obj = bpy.data.objects.new(name, mball)
            mball_obj.parent = self.obj
            scene.collection.objects.link(mball_obj)

            mball.resolution = 0.03
            mball.render_resolution = 0.01
            mball.threshold = 1.5

            for atom in self.data.chains[chain].atoms:
                if atom[-1] != ' H':
                    elem = mball.elements.new()
                    elem.co = (atom[7]*0.03, atom[8]*0.03, atom[9]*0.03)
                    elem.radius = radii[atom[-1]] * 0.03 * 4.5
                    elem.rotation = (1, radii[atom[-1]] * 0.03 * 4.5, 0, 0)

            nn = chain + '_' + self.id
            chain_mat = None
            if nn not in bpy.data.materials:
                chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idChainColors__[self.id][ind])
            else:
                chain_mat = bpy.data.materials[nn]
            
            mball_obj.data.materials.append(chain_mat)     
       
           # mball_obj.select_set(True)
           # bpy.context.view_layer.objects.active = mball_obj
           # bpy.ops.object.convert(target='MESH', keep_original=False)
           # print(len(bpy.context.selected_objects))

    def add_particle_system(self, locations, object_instance, name):
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata(locations, [], [])
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.collection.objects.link(obj)
        obj.parent = self.obj

        obj.modifiers.new("particle_system", type='PARTICLE_SYSTEM')
        part = obj.particle_systems[0]
        obj.show_instancer_for_render = False


        settings = part.settings
        settings.emit_from = 'VERT'
        settings.physics_type = 'NO'
        settings.particle_size = 1
        settings.render_type = 'OBJECT'
        settings.instance_object = object_instance
        settings.count = len(locations)
        settings.use_emit_random = False
        settings.frame_start = 0
        settings.frame_end = 0
        settings.normal_factor = 0
        settings.show_unborn = True
        settings.use_dead = True

        return obj
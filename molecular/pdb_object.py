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
    __idHetColor__ = {}
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
            PDB_Object.__idHetColor__.update({self.id: self.colors(1, 0.3, 0.1)[0]})
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
        self.het_representation = None
        self.initialized_representations = set()
        self.color_sheme = None
        self.het_color_sheme = None
        self.atom_scale = None
        self.het_atom_scale = None
        self.het_mols = {}

        # representaion spacefill
        self.chain_objects = {}
        self.element_objects = {}
        self.het_mol_objects = {}
        self.het_element_objects = {}



        # representaion surface
        self.surface_template = 'surface_base'
        self.spacefill_template = 'Spacefill'
        

        self.init_surface()
        # self.init_spacefill()
        #  self.init_sausage()
        self.recolor('compound')
        self.rescale(1.8)

        self.hetatoms('init')
        self.hetatoms('spacefill')
        self.het_rescale(1.5)


    def set_representation(self, representation):
        self.unset_representation()
        if representation == 'spacefill':
            self.chain_objects = {}
            self.element_objects = {}
            self.init_spacefill()
        elif representation == 'surface':
            self.init_surface()
        elif representation == 'sausage':
            self.init_sausage()
        
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        self.recolor(self.color_sheme)
        self.rescale(self.atom_scale)
        
    def set_het_representation(self, representation):
        self.unset_het_representation()
        if representation == 'spacefill':
            self.het_mol_objects = {}
            self.het_element_objects = {}
            self.hetatoms('spacefill')
        elif representation == 'surface':
            self.hetatoms('surface')
        dg = bpy.context.evaluated_depsgraph_get()
        dg.update()
        self.het_recolor(self.het_color_sheme)
        self.het_rescale(self.het_atom_scale)

    def unset_representation(self):
        for ch in bpy.data.objects[self.name].children:
            if not ch.name.startswith('HET'):
                for e in ch.children:
                    bpy.data.objects.remove(e)
                bpy.data.objects.remove(ch)

    def unset_het_representation(self):
        for ch in bpy.data.objects[self.name].children:
            if ch.name.startswith('HET'):
                for e in ch.children:
                    if len(e.children) > 0:
                        for x in e.children:
                            bpy.data.objects.remove(x)
                    bpy.data.objects.remove(e)
                
       
    def colors(self, n, b, t):
        return [(random()*b+1-b-t, random()*b+1-b-t, random()*b+1-b-t, 1) for i in range(n)]

    def rescale(self, value):
        self.atom_scale = value
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
        elif self.representation == 'sausage':
            for chain in self.data.chains:
                obj_name = chain + '_' + self.name
                obj = bpy.data.objects[obj_name]
                obj.children[0].scale = [value, value, value]

    def het_rescale(self, value):
        self.het_atom_scale = value
        if self.het_representation == 'spacefill':
            for mol in self.het_mol_objects:
                for obj in self.het_mol_objects[mol]:
                    bpy.data.objects[obj].scale = [value, value, value]
        elif self.het_representation == 'surface':
            for mol in self.het_mols:
                obj_name = str(mol) + '_' + self.name + '.pdb'
                obj = bpy.data.objects[obj_name]
                for i,e in enumerate(obj.data.elements):
                    e.radius = (e.rotation.x/e.rotation.w) * value / 1.8

        
    def recolor(self, sheme):
        self.color_sheme = sheme
        if self.representation == 'spacefill':
            if sheme == 'chain':
                c = {}
                for i,chain in enumerate(self.chain_objects):
                    c.update({chain:PDB_Object.__idChainColors__[self.data.id][i]})
                for chain in self.chain_objects:
                    for obj in self.chain_objects[chain]:
                        self.recolor_obj(bpy.data.objects[obj], c[chain])
            elif sheme == 'element':
                for ele in self.element_objects:
                    for obj in self.element_objects[ele]:
                        self.recolor_obj(bpy.data.objects[obj], Assets.__element_colors__[ele])
            elif sheme == 'compound':
                for i,c in enumerate(self.data.compounds):
                    for ch in self.data.compounds[c]:
                        for obj in self.chain_objects[ch]:
                            self.recolor_obj(bpy.data.objects[obj], PDB_Object.__idCompoundColors__[self.data.id][i])
            elif sheme == 'uni':
                for ele in self.element_objects:
                    for obj in self.element_objects[ele]:
                        self.recolor_obj(bpy.data.objects[obj], PDB_Object.__idUniColor__[self.data.id])

        elif self.representation == 'surface':
            if sheme == 'compound':
                for i,c in enumerate(self.data.compounds):
                    for ch in self.data.compounds[c]:
                        obj = bpy.data.objects[ch + '_' + self.name + '.pdb']
                        nn = str(c) + '_' + self.id
                        chain_mat = None
                        if nn not in bpy.data.materials:
                            chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idCompoundColors__[self.id][i])
                        else:
                            chain_mat = bpy.data.materials[nn]
                        obj.data.materials[0] = chain_mat

            elif sheme == 'chain':
                for ind, chain in enumerate(self.data.chains):
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

        elif self.representation == 'sausage':
            if sheme == 'compound':
                for i,c in enumerate(self.data.compounds):
                    for ch in self.data.compounds[c]:
                        obj = bpy.data.objects[ch + '_' + self.name]
                        nn = str(c) + '_' + self.id
                        chain_mat = None
                        if nn not in bpy.data.materials:
                            chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idCompoundColors__[self.id][i])
                        else:
                            chain_mat = bpy.data.materials[nn]

                        if len(obj.data.materials) == 0:
                            obj.data.materials.append(chain_mat)
                        else:
                            obj.data.materials[0] = chain_mat
            elif sheme == 'chain':
                for ind, chain in enumerate(self.data.chains):
                    obj = bpy.data.objects[chain + '_' + self.name]
                    nn = chain + '_' + self.id
                    chain_mat = None
                    if nn not in bpy.data.materials:
                        chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idChainColors__[self.id][ind])
                    else:
                        chain_mat = bpy.data.materials[nn]
                    
                    if len(obj.data.materials) == 0:
                        obj.data.materials.append(chain_mat)
                    else:
                        obj.data.materials[0] = chain_mat
            
            elif sheme == 'uni':
                for chain in self.data.chains:
                    obj = bpy.data.objects[chain + '_' + self.name]
                    nn = 'uni' + '_' + self.id
                    chain_mat = None
                    if nn not in bpy.data.materials:
                        chain_mat = Assets.__material__(nn, self.surface_template, PDB_Object.__idUniColor__[self.id])
                    else:
                        chain_mat = bpy.data.materials[nn]
                    
                    if len(obj.data.materials) == 0:
                        obj.data.materials.append(chain_mat)
                    else:
                        obj.data.materials[0] = chain_mat

    def het_recolor(self, sheme):
        self.het_color_sheme = sheme
        if self.het_representation == 'spacefill':
            if sheme == 'element':
                for ele in self.het_element_objects:
                    for obj in self.het_element_objects[ele]:
                        self.recolor_obj(bpy.data.objects[obj], Assets.__element_colors__[ele])
            elif sheme == 'uni':
                for ele in self.het_element_objects:
                    for obj in self.het_element_objects[ele]:
                        self.recolor_obj(bpy.data.objects[obj], PDB_Object.__idHetColor__[self.data.id])


    def recolor_obj(self, obj, color):
        mesh = obj.data
        vcol_layer = mesh.vertex_colors.active
        for poly in mesh.polygons:
            for loop_index in poly.loop_indices:
                vcol_layer.data[loop_index].color = color  
        mesh.update()
        obj.data = mesh

    def hetatoms(self, representation):

        radii = Assets.__element_radii__
        colors = Assets.__element_colors__


        object_name = 'HET' + '_' + self.name
        
        if representation == 'init':
            mol = 0
            for chain in self.data.chains:
                atoms = []
                bonds = {}
                for atm in self.data.chains[chain].hetatms:
                    if atm.comp != 'HOH':
                        atoms.append(atm)
                for i in range(len(atoms)):
                    for j in range(i+1, len(atoms)):
                        a, b = atoms[i], atoms[j]
                        dx = a.location[0] - b.location[0]
                        dy = a.location[1] - b.location[1]
                        dz = a.location[2] - b.location[2]
                        d2 = dx*dx + dy*dy + dz*dz
                        contact = (radii[a.element] + radii[b.element]) + 0.2
                        if d2 < contact * contact:
                            if a.id not in bonds:
                                bonds.update({a.id:set()})
                            if b.id not in bonds:
                                bonds.update({b.id:set()})
                            bonds[a.id].add(b)
                            bonds[b.id].add(a)
                processed = set()
                for atm in atoms:
                    if atm.id not in processed:
                        
                        processed.add(atm.id)
                        atm.mol_index = mol
                        remaining = set()
                        for b in bonds[atm.id]:
                            if b.id not in processed:
                                remaining.add(b)
                        
                        while len(remaining) > 0:
                            tmp = set()
                            for rem in remaining:
                                processed.add(rem.id)
                                rem.mol_index = mol
                                for b in bonds[rem.id]:
                                    if b.id not in processed:
                                        processed.add(b.id)
                                        b.mol_index = mol
                                        tmp.add(b)
                            remaining = tmp
                        mol += 1
            obj = bpy.data.objects.new(object_name, None)
            bpy.context.scene.collection.objects.link(obj)
            obj.parent = bpy.data.objects[self.name]

            self.het_mols = {}
            for chain in self.data.chains:
                for atm in self.data.chains[chain].hetatms:
                    if atm.comp != 'HOH':
                        if atm.mol_index not in self.het_mols:
                            self.het_mols.update({atm.mol_index:set()})
                        self.het_mols[atm.mol_index].add(atm)
        else: 
            self.het_representation = representation


            if representation == 'spacefill':
                self.het_color_sheme = 'element'
                mat = bpy.data.materials.get(self.spacefill_template)
                template_spheres = {}
                for j,mol in enumerate(self.het_mols):
                    self.het_mol_objects.update({mol:[]})
                    spheres = {}
                    for e in radii:
                        spheres.update({e:Sphere(str(mol) + '_' + e.strip() + '_' + self.name, [0,0,0], radii[e]*0.03, colors[e], mat)})
                        if e not in self.het_element_objects:
                            self.het_element_objects.update({e:[]})
                        self.het_element_objects[e].append(spheres[e].obj.name)
                    for i,s in enumerate(spheres):
                        spheres[s].obj.parent = bpy.data.objects[object_name]
                        spheres[s].obj.location = [0,0,0]
                        self.het_mol_objects[mol].append(spheres[s].obj.name)
                    template_spheres.update({mol:spheres})
                
                for mol in self.het_mols:
                    per_elem_loc = {x:[] for x in radii}
                    b = 0.4
                    obs = []
                    for atom in self.het_mols[mol]:
                        if atom.element != 'H':
                            per_elem_loc[atom.element].append([atom.x*0.03, atom.y*0.03, atom.z*0.03])
                    
                    bpy.ops.object.select_all(action='DESELECT')
                    for e in per_elem_loc:
                        if len(per_elem_loc[e]) != 0:
                            ps = self.add_particle_system(per_elem_loc[e][1:], template_spheres[mol][e].obj, str(mol) + '_' + e.strip())
                            template_spheres[mol][e].obj.location = per_elem_loc[e][0]
                            obs.append(ps)
                        else:
                            template_spheres[mol][e].obj.select_set(True)
                            self.het_mol_objects[mol].remove(str(mol) + '_' + e.strip() + '_' + self.name)
                            self.het_element_objects[e].remove(str(mol) + '_' + e.strip() + '_' + self.name)
                            
                    bpy.ops.object.delete() 
                
                    obj = bpy.data.objects.new(str(mol) + '_' + self.name + '.pdb', None)
                    bpy.context.scene.collection.objects.link(obj)
                    obj.parent = bpy.data.objects[object_name]

                    for o in obs:
                        o.parent = obj

            elif representation == 'surface':
                self.het_color_sheme = 'uni'
                scene = bpy.context.scene
                for ind, mol in enumerate(self.het_mols):
                    name = str(mol) + '_' + self.name + '.pdb'
                    
                    mball = bpy.data.metaballs.new('metaball_' + name)
                    mball_obj = bpy.data.objects.new(name, mball)
                    mball_obj.parent = bpy.data.objects[object_name]
                    scene.collection.objects.link(mball_obj)

                    mball.resolution = 0.02
                    mball.render_resolution = 0.01
                    mball.threshold = 1.5

                    for atom in self.het_mols[mol]:
                        if atom.element != 'H':
                            elem = mball.elements.new()
                            elem.co = (atom.x*0.03, atom.y*0.03, atom.z*0.03)
                            elem.radius = radii[atom.element] * 0.03 * 4.5
                            elem.rotation = (1, radii[atom.element] * 0.03 * 4.5, 0, 0)

                    
                    mat = Assets.__material__(str(mol) + '_' + self.name, self.surface_template, PDB_Object.__idHetColor__[self.id])
                    
                    mball_obj.data.materials.append(mat)   




        



    def init_sausage(self):
        rep = 'sausage'
        self.initialized_representations.add(rep)
        self.representation = rep
    
        for chain in self.data.chains:
            coords = []
            for atom in self.data.chains[chain].atoms:
                if atom.atom_id == 'CA':
                    coords.append([atom.x*0.03, atom.y*0.03, atom.z*0.03])

            curveData = bpy.data.curves.new(chain + '_' + self.name, type='CURVE')
            curveData.dimensions = '3D'

            polyline = curveData.splines.new('NURBS')
            polyline.points.add(len(coords)-1)
            for i, coord in enumerate(coords):
                x,y,z = coord
                polyline.points[i].co = (x, y, z, 1)

            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.curve.primitive_bezier_circle_add(
                                    radius = 0.03 * 0.77,
                                    location = (0.0, 0.0, 0.0),
                                    enter_editmode = False)

            circ = bpy.context.active_object
            bpy.context.scene.collection.objects.link(circ)
            bpy.data.collections['Collection'].objects.unlink(circ)

            curveData.bevel_object = circ
            curveData.use_fill_caps = True
            curveData.splines[0].use_endpoint_u = True
            curveData.resolution_u = 2

            
            curveOB = bpy.data.objects.new(chain + '_' + self.name, curveData)
            bpy.context.scene.collection.objects.link(curveOB)
            circ.parent = curveOB
            curveOB.parent = bpy.data.objects[self.name]
            
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[self.name].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects[self.name]
        
    def init_spacefill(self):
        rep = 'spacefill'
        self.initialized_representations.add(rep)
        self.representation = rep
      
        scene = bpy.context.scene
        
        if rep == "spacefill":

            radii = Assets.__element_radii__
            
            colors = Assets.__element_colors__


            mat = bpy.data.materials.get(self.spacefill_template)

            template_spheres = {}
            for j,chain in enumerate(self.data.chains):
                self.chain_objects.update({chain:[]})
                spheres = {}
                for e in radii:
                    spheres.update({e:Sphere(chain + '_' + e.strip() + '_' + self.name, [0,0,0], radii[e]*0.03, colors[e], mat)})
                    if e not in self.element_objects:
                        self.element_objects.update({e:[]})
                    self.element_objects[e].append(spheres[e].obj.name)
                

                for i,s in enumerate(spheres):
                    spheres[s].obj.parent = bpy.data.objects[self.name]
                    spheres[s].obj.location = [0,0,0]
                    self.chain_objects[chain].append(spheres[s].obj.name)
                template_spheres.update({chain:spheres})
            

            for chain in self.data.chains:
                per_elem_loc = {x:[] for x in radii}
                b = 0.4
                obs = []
                for atom in self.data.chains[chain].atoms:
                    if atom.element != 'H':
                        per_elem_loc[atom.element].append([atom.x*0.03, atom.y*0.03, atom.z*0.03])
                
                

                bpy.ops.object.select_all(action='DESELECT')
                for e in per_elem_loc:
                    if len(per_elem_loc[e]) != 0:
                        ps = self.add_particle_system(per_elem_loc[e], template_spheres[chain][e].obj, chain + '_' + e.strip())
                        template_spheres[chain][e].obj.location = per_elem_loc[e][0]
                        obs.append(ps)
                    else:
                        template_spheres[chain][e].obj.select_set(True)
                        self.chain_objects[chain].remove(chain + '_' + e.strip() + '_' + self.name)
                        self.element_objects[e].remove(chain + '_' + e.strip() + '_' + self.name)
                        
                bpy.ops.object.delete() 
            
                obj = bpy.data.objects.new(chain + '_' + self.name + '.pdb', None)
                bpy.context.scene.collection.objects.link(obj)
                obj.parent = bpy.data.objects[self.name]


                for o in obs:
                    o.parent = obj

    def init_surface(self, backbone = False):
        rep = 'surface'
        self.initialized_representations.add(rep)
        self.representation = rep
      
        
        scene = bpy.context.scene
        radii = Assets.__element_radii__
        colors = Assets.__element_colors__
        numObjs = len(PDB_Object.__objects__)

        for ind, chain in enumerate(self.data.chains):
            name = chain + '_' + self.name + '.pdb'
            
            mball = bpy.data.metaballs.new('metaball_' + name)
            mball_obj = bpy.data.objects.new(name, mball)
            mball_obj.parent = bpy.data.objects[self.name]
            scene.collection.objects.link(mball_obj)

            mball.resolution = 0.03
            mball.render_resolution = 0.01
            mball.threshold = 1.5

            for atom in self.data.chains[chain].atoms:
                if atom.element != 'H':
                    if not backbone or (backbone and (atom.id == 'CA' or atom.id == 'N' or atom.id == 'O')):
                        elem = mball.elements.new()
                        elem.co = (atom.x*0.03, atom.y*0.03, atom.z*0.03)
                        elem.radius = radii[atom.element] * 0.03 * 4.5
                        elem.rotation = (1, radii[atom.element] * 0.03 * 4.5, 0, 0)

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
        obj.parent = bpy.data.objects[self.name]

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
class Atom:
    def __init__(self, x, y, z, element, atom_id, comp, id):
        self.x = x
        self.y = y
        self.z = z
        self.location = [x,y,z]
        self.element = element
        self.atom_id = atom_id
        self.comp = comp
        self.id = id
        self.mol_index = -1
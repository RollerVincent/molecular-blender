
bl_info = {
    "name" : "molecular",
    "author" : "Vincent Roller",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Generic"
    
}


import bpy
import os



from . clear_button import Clear_OT_Operator
from . tools_panel import Tools_PT_Panel
from . pdb_panel import PDB_PT_Panel
from . pdb_id_button import PDB_ID_OT_Operator
from . pdb_object_panel import PDB_Object_PT_Panel
from . pdb_coloring_operator import PDB_Coloring
from . pdb_het_coloring_operator import PDB_HET_Coloring
from . pdb_representation_operator import PDB_Representation
from . pdb_rep_surf_operator import PDB_REP_SURF_OT_Operator
from . pdb_rep_spf_operator import PDB_REP_SPF_OT_Operator
from . pdb_rep_ssg_operator import PDB_REP_SSG_OT_Operator
from . pdb_rep_spf_het_operator import PDB_REP_SPF_HET_OT_Operator
from . pdb_rep_surf_het_operator import PDB_REP_SURF_HET_OT_Operator





classes = (
           PDB_PT_Panel,
           PDB_ID_OT_Operator,
           Clear_OT_Operator,
           Tools_PT_Panel,
           PDB_Object_PT_Panel,
           PDB_Coloring,
           PDB_HET_Coloring,
           PDB_Representation,
           PDB_REP_SURF_OT_Operator,
           PDB_REP_SPF_OT_Operator,
           PDB_REP_SSG_OT_Operator,
           PDB_REP_SURF_HET_OT_Operator,
           PDB_REP_SPF_HET_OT_Operator
          ) 


def register():

    for c in classes: bpy.utils.register_class(c)


    bpy.types.Scene.input_pdb_id = bpy.props.StringProperty \
      (
        name = "ID ",
        description = "PDB id ",
        default = "1hem"
      )

    bpy.types.Scene.input_object_name = bpy.props.StringProperty \
      (
        name = "Name ",
        description = "Object name",
        default = "object",
      )

   
    

    

    
def unregister():
    for c in classes: bpy.utils.unregister_class(c)

    del bpy.types.Scene.input_pdb_id
    del bpy.types.Scene.input_object_name

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "PDB",
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




classes = (
           PDB_PT_Panel,
           PDB_ID_OT_Operator,
           Clear_OT_Operator,
           Tools_PT_Panel,
           PDB_Object_PT_Panel,
           PDB_Coloring
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
        default = "object"
      )
    
    

    

    
def unregister():
    for c in classes: bpy.utils.unregister_class(c)

    del bpy.types.Scene.input_pdb_id
    del bpy.types.Scene.input_object_name

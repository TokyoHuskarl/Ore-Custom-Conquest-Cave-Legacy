from header_meshes import *

meshes = [
####################################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)
####################################################################################################################################

  ("lco_background", 0, "mp_ui_bg", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_background_split", 0, "mp_ui_profile", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_panel", 0, "longer_button", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_panel_down", 0, "longer_button_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_garbage_area", 0, "mp_score_b", 0, 0, 0, 0, 0, 0, 1, 1, 1), #1255 780
  ("lco_sort_inventory", 0, "small_arrow_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_sort_inventory_down", 0, "small_arrow_down_clicked", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_gold_icon", 0, "mp_ico_gold", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_square_button_up", 0, "button1_up", 0, 0, 0, 0, 0, 0, 1, 1, 1),
  ("lco_square_button_down", 0, "button1_down", 0, 0, 0, 0, 0, 0, 1, 1, 1),

####################################################################################################################################
# LAV MODIFICATIONS END (COMPANIONS OVERSEER MOD)
####################################################################################################################################
]

from util_common import *

def modmerge_meshes(orig_meshes):
    # add remaining meshes
    from util_common import add_objects
    num_appended, num_replaced, num_ignored = add_objects(orig_meshes, meshes)
    #print num_appended, num_replaced, num_ignored
	
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "meshes"
        orig_meshes = var_set[var_name_1]
        modmerge_meshes(orig_meshes)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
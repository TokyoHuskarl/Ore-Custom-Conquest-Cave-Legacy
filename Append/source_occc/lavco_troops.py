from header_troops import *
from header_skills import *

troops = [
####################################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)
####################################################################################################################################
  ["companions_overview", "{!}Hidden", "{!}Hidden",tf_hero,0,0,0,[],0,0,knows_inventory_management_10,0],
  ["companions_discard", "{!}Hidden", "{!}Hidden",tf_hero,0,0,0,[],0,0,knows_inventory_management_10,0],
####################################################################################################################################
# LAV MODIFICATIONS END (COMPANIONS OVERSEER MOD)
####################################################################################################################################
]

from util_common import add_objects

# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "troops"
        orig_troops = var_set[var_name_1]
        add_objects(orig_troops, troops)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
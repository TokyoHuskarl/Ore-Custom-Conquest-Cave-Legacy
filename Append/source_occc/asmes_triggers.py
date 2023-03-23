from header_common import *
from header_operations import *
from header_triggers import *

triggers = [

################################################################################
# [OSP] Advanced Soldier Management in Exchange Screens by Leonion
################################################################################

  (0, 0, ti_on_switch_to_map, [], [
    #(troop_set_slot, "trp_globals_troop", slot_adv_transfer_mode, 0),
    (assign, "$g_adv_transfer_mode", 0),
  ]),

]


# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "triggers"
        orig_triggers = var_set[var_name_1]
        orig_triggers.extend(triggers)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
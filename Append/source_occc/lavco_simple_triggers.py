from header_common import *
from header_operations import *
from module_constants import *
from header_mission_templates import *

simple_triggers = [
####################################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)
####################################################################################################################################

    (0,
        [
            (map_free),
            (this_or_next|key_clicked, key_o),
            (neq, "$g_lco_operation", 0),
            (try_begin),
                (this_or_next|key_clicked, key_o),
                (eq, "$g_lco_operation", lco_run_presentation),
                (assign, "$g_lco_operation", 0),
                (jump_to_menu, "mnu_lco_presentation"),
            (else_try),
                (eq, "$g_lco_operation", lco_view_character),
                (jump_to_menu, "mnu_lco_view_character"),
            (try_end),
        ]

    ),

####################################################################################################################################
# LAV MODIFICATIONS END (COMPANIONS OVERSEER MOD)
####################################################################################################################################
]

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "simple_triggers"
        orig_simple_triggers = var_set[var_name_1]
        orig_simple_triggers.extend(simple_triggers)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
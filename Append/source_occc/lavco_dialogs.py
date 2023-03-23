from header_common import *
from header_dialogs import *
from header_operations import *
from module_constants import *

lavco_talk_addon = [
####################################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)
####################################################################################################################################
  [anyone, "start", [(eq,"$g_lco_operation",lco_view_character)],"Here you are.","lco_conversation_end",[(change_screen_view_character)]],
####################################################################################################################################
# LAV MODIFICATIONS END (COMPANIONS OVERSEER MOD)
####################################################################################################################################
]

dialogs = [
####################################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)
####################################################################################################################################
  [anyone, "lco_conversation_end", [(troop_is_hero,"$g_lco_target"),(assign,"$g_lco_operation",lco_run_presentation)], "Nice to know you are not forgetting me!", "close_window", [(change_screen_return)]],
  [anyone, "lco_conversation_end", [(assign,"$g_lco_operation",lco_run_presentation)], "It's a honor to serve you, {sir/my lady}!", "close_window", [(change_screen_return)]],
####################################################################################################################################
# LAV MODIFICATIONS END (COMPANIONS OVERSEER MOD)
####################################################################################################################################
]

from util_common import *
from util_wrappers import *

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
		var_name_1 = "dialogs"
		orig_dialogs = var_set[var_name_1]
		orig_dialogs.extend(dialogs)
		pos = FindDialog_i(orig_dialogs, anyone, "start", "close_window")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, lavco_talk_addon)
		
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
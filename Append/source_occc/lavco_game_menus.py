from module_constants import *
from header_game_menus import *

## NMCml LCO begin: call from report
report_addon = [
####################################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERVIEW MOD)
####################################################################################################################################
     ("view_companions_overview",[],"Overview companions screen.",
        [
           (assign, "$g_lco_operation", lco_run_presentation),
           (change_screen_return),
        ]
       ),
####################################################################################################################################
# LAV MODIFICATIONS END (COMPANIONS OVERVIEW MOD)
####################################################################################################################################
]
## NMCml LCO end

game_menus = [
####################################################################################################################################
# LAV MODIFICATIONS START (COMPANIONS OVERSEER MOD)
####################################################################################################################################

    ("lco_presentation",0,"{!}Hidden Text","none",  ## NMCml LCO: hidden fix: add {!}
        [
            (jump_to_menu, "mnu_lco_presentation"), # Self-reference
            (try_begin),
                (eq, "$g_lco_page", 2),
                (start_presentation, "prsnt_equipment_overview"),
            (else_try),
                (start_presentation, "prsnt_companions_overview"),
            (try_end),
        ],
        [("lco_go_back",[],"{!}Return",[])]
    ),

    ("lco_view_character",0,"{!}Hidden Text","none",  ## NMCml LCO: hidden fix: add {!}
        [
            (modify_visitors_at_site,"scn_conversation_scene"),
            (reset_visitors),
            (set_visitor,0,"trp_player"),
            (set_visitor,17,"$g_lco_target"),
            (set_jump_mission,"mt_conversation_encounter"),
            (jump_to_scene,"scn_conversation_scene"),
            (change_screen_map_conversation, "$g_lco_target"),
        ],
        [("lco_go_back",[],"{!}Return",[])]
    ),

    ("lco_auto_return",0,"{!}Hidden Text","none",  ## NMCml LCO: hidden fix: add {!}
        [
            (try_begin),
                (gt, "$g_lco_auto_menu", 0),
                (jump_to_menu, "$g_lco_auto_menu"),
                (assign, "$g_lco_auto_menu", 0),
            (else_try),
                (change_screen_return),
            (try_end),
        ],
        [("lco_go_back",[],"{!}Return",[])]
    ),

####################################################################################################################################
# LAV MODIFICATIONS END (COMPANIONS OVERSEER MOD)
####################################################################################################################################
]

from util_wrappers import *
from util_common import *

## NMCml LCO begin: call from report
def modmerge_game_menus(orig_game_menus, check_duplicates = False):
	try:
		find_i = list_find_first_match_i( orig_game_menus, "reports" )
		menuoptions = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOptions()
		find_i = list_find_first_match_i(menuoptions, "cheat_faction_orders")
		OpBlockWrapper(menuoptions).InsertBefore(find_i, report_addon)
	except:
		import sys
		print "Injecton 1 failed:", sys.exc_info()[1]
		raise
## NMCml end

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "game_menus"
        orig_game_menus = var_set[var_name_1]
        orig_game_menus.extend(game_menus) 
        modmerge_game_menus(orig_game_menus)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
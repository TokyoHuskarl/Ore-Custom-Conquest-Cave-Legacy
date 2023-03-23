from header_game_menus import *

################################################################################
# [OSP] Advanced Soldier Management in Exchange Screens by Leonion
################################################################################

after_battle_flag = [
          #(troop_set_slot, "trp_globals_troop", slot_adv_transfer_mode, 10),
          (assign, "$g_adv_transfer_mode", 10),  # after battle
]

manage_garrison_flag = [
        #(troop_set_slot, "trp_globals_troop", slot_adv_transfer_mode, 12),
        (assign, "$g_adv_transfer_mode", 12),  # manage garrison
]


game_menus = [] #for any menus that need to be added to the end

from util_wrappers import *
from util_common import *

def modmerge_game_menus(orig_game_menus, check_duplicates = False):
	try:
		## CC-D begin: fit for difor
		#find_i = list_find_first_match_i( orig_game_menus, "total_victory" )
		#codeblock = GameMenuWrapper(orig_game_menus[find_i]).GetOpBlock()
		find_i = list_find_first_match_i( orig_game_menus, "ccd_get_all_captured_enemy" )
		menuoptions = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOptions()
		find_i = list_find_first_match_i(menuoptions, "select_prisoner")
		menu_manage = GameMenuOptionWrapper(menuoptions[find_i])
		codeblock = menu_manage.GetConsequenceBlock()
		## CC-D end
		pos = codeblock.FindLineMatching( (change_screen_exchange_with_party, "p_temp_party") )
		codeblock.InsertBefore(pos, after_battle_flag )
		
		find_i = list_find_first_match_i( orig_game_menus, "center_manage" )  ## CC-D: fit for CC: town->center_manage
		menuoptions = GameMenuWrapper(orig_game_menus[find_i]).GetMenuOptions()
		find_i = list_find_first_match_i(menuoptions, "castle_station_troops")
		menu_manage = GameMenuOptionWrapper(menuoptions[find_i])
		codeblock = menu_manage.GetConsequenceBlock()
		pos = codeblock.FindLineMatching( (change_screen_exchange_members, 1) )
		codeblock.InsertBefore(pos, manage_garrison_flag )
	except:
		import sys
		print "Injecton 1 failed:", sys.exc_info()[1]
		raise
	
	if( not check_duplicates ):
		orig_game_menus.extend(game_menus) # Use this only if there are no replacements (i.e. no duplicated item names)
	else:
    # Use the following loop to replace existing entries with same id
		for i in range (0,len(game_menus)-1):
			find_index = find_object(orig_game_menus, game_menus[i][0]); # find_object is from header_common.py
			if( find_index == -1 ):
				orig_game_menus.append(game_menus[i])
			else:
				orig_game_menus[find_index] = game_menus[i]

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
        var_name_1 = "game_menus"
        orig_game_menus = var_set[var_name_1]
        modmerge_game_menus(orig_game_menus)
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
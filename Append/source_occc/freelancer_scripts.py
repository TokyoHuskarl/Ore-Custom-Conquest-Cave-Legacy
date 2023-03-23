# Freelancer (1.3) by Taragoth
# Released 11 July 2011
# Edits by Caba'drin 14 Dec 2011
# Mod-Merger'd by Windyplains, Monnikje and Caba'drin

from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_items import *
#from header_troops import *  ## NMCml FL: individual script

####################################################################################################################
# scripts is a list of script records.
# Each script record contains the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################

scripts = [
#+freelancer start
   ("freelancer_attach_party",
    [
	    #prepare player to be part of lord's party
        (party_attach_to_party, "p_main_party", "$enlisted_party"),
        (set_camera_follow_party, "$enlisted_party"),
        (party_set_flags, "$enlisted_party", pf_always_visible, 1),
        (disable_party, "p_main_party"),

		#initialize service variable
		(assign, "$freelancer_state", 1),		
    ]),

   ("freelancer_detach_party",
    [
	    #removes player from commanders party
		(enable_party, "p_main_party"),
        (party_detach, "p_main_party"),
		
		(try_begin),
			(party_is_active, "$enlisted_party"),
			(party_relocate_near_party, "p_main_party", "$enlisted_party", 2),
			(party_set_flags, "$enlisted_party", pf_always_visible, 0),
		(try_end),	
		
	    (set_camera_follow_party, "p_main_party"),
		(assign, "$g_player_icon_state", pis_normal),
        (assign, "$g_infinite_camping", 0),  ## NMCml FL: fix enlist
	]),

# ADDS THE PLAYER TO THE LORD'S PARTY  
    ("event_player_enlists",
    [
	    #initialize service variables
        (troop_get_xp, ":xp", "trp_player"),
		(troop_set_slot, "trp_player", slot_troop_freelancer_start_xp, ":xp"),
        (store_current_day, ":day"), 
        (troop_set_slot, "trp_player", slot_troop_freelancer_start_date, ":day"),		
		(party_get_morale, ":morale", "p_main_party"),
		(party_set_slot, "p_main_party", slot_party_orig_morale, ":morale"),
        #(assign, "$freelancer_state", 1), #moved to script
	
        #needed to stop bug where parties attack the old player party
        (call_script, "script_set_parties_around_player_ignore_player", 2, 4),
        #set lord as your commander
		(assign, "$enlisted_lord", "$g_talk_troop"),
		(troop_get_slot, "$enlisted_party", "$enlisted_lord", slot_troop_leaded_party), 
        #removes troops from player party
        ## CC-D begin: keep player party refer from TinyModPatcher
        (try_begin),
          (eq, "$g_fl_keep_player_party", 0),
          
        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
        (try_for_range_backwards, ":cur_stack", 1, ":num_stacks"), #lower bound is 1 to ignore player character
           (party_stack_get_troop_id, ":cur_troops", "p_main_party", ":cur_stack"),
           (party_stack_get_size, ":cur_size", "p_main_party", ":cur_stack"),
           (party_remove_members, "p_main_party", ":cur_troops", ":cur_size"),
        (try_end),
          
          (assign, "$g_fl_keep_player_party_nobackup", 0),
          (display_message, "@You leave your party temporarily."),
        (else_try),
          (assign, "$g_fl_keep_player_party_nobackup", 1),
        (try_end),
        ## CC-D end
        
		#set faction relations to allow player to join battles
		(call_script, "script_fl_record_faction_relation"),  ## NMCml FL: keep reration
        (store_troop_faction, ":commander_faction", "$enlisted_lord"),
		(try_begin),
			(store_relation, ":player_relation", ":commander_faction", "fac_player_supporters_faction"),
			(lt, ":player_relation", 5),
			(call_script, "script_set_player_relation_with_faction", ":commander_faction", 5),
		(try_end),
        (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
           (neq, ":commander_faction", ":cur_faction"),
		   (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
		   (store_relation, ":player_relation", ":cur_faction", "fac_player_supporters_faction"),
		   (ge, ":player_relation", 0),
           (call_script, "script_set_player_relation_with_faction", ":cur_faction", -5),
        (try_end),		

        #adds standard issued equipment
		(try_begin),
			(neg|faction_slot_eq, ":commander_faction", slot_faction_freelancer_troop, 0),
			(faction_get_slot, "$player_cur_troop", ":commander_faction", slot_faction_freelancer_troop),
		(else_try),
            #occc start - extra enlistment
            (call_script, "script_occc_freelancer_extra_lord", "$enlisted_lord"),
            #occc end
		(try_end),		
		(call_script, "script_freelancer_equip_troop", "$player_cur_troop"),

		(call_script, "script_freelancer_attach_party"),
		#makes Lords banner the players
		## NMCml FL begin: keep banner
		(party_set_slot, "p_freelancer_party_backup", slot_freelancer_last_banner, 0),
		(troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
		(try_begin),
			(gt, ":banner", 0),
			(party_set_slot, "p_freelancer_party_backup", slot_freelancer_last_banner, ":banner"),
		(try_end),
		## NMCml FL end
		(troop_get_slot, ":banner", "$enlisted_lord", slot_troop_banner_scene_prop),
		(troop_set_slot, "trp_player", slot_troop_banner_scene_prop, ":banner"),
        (display_message, "@You have been enlisted!"),	

		## NMCml FL begin: quest fix
		(try_begin),
		  (check_quest_active, "qst_freelancer_enlisted"),
		  (call_script, "script_end_quest", "qst_freelancer_enlisted"),
		(try_end),
		## NMCml FL end
		
        (str_store_troop_name_link, s13, "$enlisted_lord"),
		(str_store_faction_name_link, s14, ":commander_faction"),
		(quest_set_slot, "qst_freelancer_enlisted", slot_quest_target_party, "$enlisted_party"),
		(quest_set_slot, "qst_freelancer_enlisted", slot_quest_importance, 5),
		(quest_set_slot, "qst_freelancer_enlisted", slot_quest_xp_reward, 1000),
		(quest_set_slot, "qst_freelancer_enlisted", slot_quest_gold_reward, 100),
		(setup_quest_text, "qst_freelancer_enlisted"),
		(str_clear, s2), #description. necessary?
        (call_script, "script_start_quest", "qst_freelancer_enlisted", "$enlisted_lord"),
		(str_store_troop_name, s5, "$player_cur_troop"),
		(str_store_string, s5, "@Current rank: {s5}"),
        (add_quest_note_from_sreg, "qst_freelancer_enlisted", 3, s5, 1),		
    ]),

#  RUNS IF THE PLAYER LEAVES THE ARMY

   ("event_player_discharge",
    [
		#removes faction relation given at enlist
		(store_troop_faction, ":commander_faction", "$enlisted_lord"),
		(call_script, "script_change_player_relation_with_faction_ex", ":commander_faction", 1),  ## CC-D 5->1
		## NMCml FL begin: keep relation
		#(try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        #    (neq, ":commander_faction", ":cur_faction"),
		#	(faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
		#	(store_relation, ":player_relation", ":cur_faction", "fac_player_supporters_faction"),
		#	(lt, ":player_relation", 0),
        #    (call_script, "script_set_player_relation_with_faction", ":cur_faction", 0),
        #(try_end),
        (call_script, "script_fl_recover_faction_relation", ":commander_faction"),
        ## NMCml FL end
		# removes standard issued equipment
		# (try_for_range, ":cur_inv_slot", ek_item_0, ek_food),
			# (troop_get_inventory_slot, ":soldier_equipment", "$player_cur_troop", ":cur_inv_slot"),
			# (ge, ":soldier_equipment", 0),
			# (troop_remove_item, "trp_player", ":soldier_equipment"),
		# (try_end),
		(call_script, "script_freelancer_unequip_troop", "$player_cur_troop"),		
		## CC-D begin: stop auto equip
		(try_begin),
		  (eq, "$g_fl_no_auto_equip", 0),
		
		(troop_equip_items, "trp_player"),
		
		(try_end),
		## CC-D end

		(troop_set_slot, "trp_player", slot_troop_current_mission, 0),
		#(troop_set_slot, "trp_player", slot_troop_days_on_mission, 0),  ## NMCml FL: quest fix
		## NMCml FL begin: keep banner
		#(troop_set_slot, "trp_player", slot_troop_banner_scene_prop, 0),
		(party_get_slot, ":banner", "p_freelancer_party_backup", slot_freelancer_last_banner),
		(troop_set_slot, "trp_player", slot_troop_banner_scene_prop, ":banner"),
		## NMCml FL end
		(assign, "$freelancer_state", 0),
		(call_script, "script_freelancer_detach_party"),
		(rest_for_hours, 0,0,0),
		(display_message, "@You have left your commander!"), 

        #(call_script, "script_cancel_quest", "qst_freelancer_enlisted"),
		## NMCml FL begin: quest fix
		(troop_get_slot, ":service_day_start", "trp_player", slot_troop_freelancer_start_date),
		(store_current_day, ":cur_day"),
		(store_sub, ":service_length", ":cur_day", ":service_day_start"),
		(call_script, "script_finish_quest", "qst_freelancer_enlisted", ":service_length"), #percentage--make based on days served?  ## NMCml FL: quest fix: 100->":day"
		## NMCml FL end
		## CC-D begin: local achievement
		(try_begin),
		  (neg|troop_slot_ge, "trp_ccd_treasure", slot_troop_ccd_rec_max_fl_days, ":service_length"),
		  (troop_set_slot, "trp_ccd_treasure", slot_troop_ccd_rec_max_fl_days, ":service_length"),
		(try_end),
		## CC-D end
    ]),
	
#  RUNS IF THE PLAYER GOES ON VACATION

    ("event_player_vacation",
    [
	    (troop_set_slot, "trp_player", slot_troop_current_mission, plyr_mission_vacation), ###move to quests, not missions
		#(troop_set_slot, "trp_player", slot_troop_days_on_mission, 14),  ## NMCml FL: quest fix
	
		#removes faction relation given at enlist
		(store_troop_faction, ":commander_faction", "$enlisted_lord"),
		## NMCml FL begin: keep relation
		#(try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
        #    (neq, ":commander_faction", ":cur_faction"),
		#	(faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
        #    (call_script, "script_set_player_relation_with_faction", ":cur_faction", 0),
        #(try_end),
        (call_script, "script_fl_recover_faction_relation", ":commander_faction"),
        ## NMCml FL end
		## NMCml FL begin: keep banner
		(party_get_slot, ":banner", "p_freelancer_party_backup", slot_freelancer_last_banner),
		(troop_set_slot, "trp_player", slot_troop_banner_scene_prop, ":banner"),
		## NMCml FL end

		(assign, "$freelancer_state", 2),
		(call_script, "script_freelancer_detach_party"),
		(rest_for_hours, 0,0,0),
		(display_message, "@You have been granted leave!"), 	

		(str_store_troop_name_link, s13, "$enlisted_lord"),
		(str_store_faction_name_link, s14, ":commander_faction"),
		(quest_set_slot, "qst_freelancer_vacation", slot_quest_target_party, "$enlisted_party"),
		(quest_set_slot, "qst_freelancer_vacation", slot_quest_importance, 0),
		(quest_set_slot, "qst_freelancer_vacation", slot_quest_xp_reward, 50),
		(quest_set_slot, "qst_freelancer_vacation",	slot_quest_expiration_days, 14),
		(setup_quest_text, "qst_freelancer_vacation"),
		(str_clear, s2), #description. necessary?
        (call_script, "script_start_quest", "qst_freelancer_vacation", "$enlisted_lord"),
    ]),

# RUNS WHEN PLAYER RETURNS FROM VACATION

  ("event_player_returns_vacation",
    [
        (troop_set_slot, "trp_player", slot_troop_current_mission, 0),
		#(troop_set_slot, "trp_player", slot_troop_days_on_mission, 0),  ## NMCml FL: quest fix
		
		#needed to stop bug where parties attack the old player party
        (call_script, "script_set_parties_around_player_ignore_player", 2, 4),

        #removes troops from player party #Caba--could use party_clear? and then add the player back?
        ## CC-D begin: keep player party refer from TinyModPatcher
        (try_begin),
          (eq, "$g_fl_keep_player_party", 0),
          
        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
        (try_for_range_backwards, ":cur_stack", 1, ":num_stacks"), #lower bound is 1 to ignore player character
           (party_stack_get_troop_id, ":cur_troops", "p_main_party", ":cur_stack"),
           (party_stack_get_size, ":cur_size", "p_main_party", ":cur_stack"),
           (party_remove_members, "p_main_party", ":cur_troops", ":cur_size"),
        (try_end),
          
          (assign, "$g_fl_keep_player_party_nobackup", 0),
          (display_message, "@You leave your party temporarily."),
        (else_try),
          (assign, "$g_fl_keep_player_party_nobackup", 1),
        (try_end),
        ## CC-D end
		
        #To fix any errors of the lord changing parties
		(troop_get_slot, "$enlisted_party", "$enlisted_lord", slot_troop_leaded_party), 
		
		#set faction relations to allow player to join battles
		(call_script, "script_fl_record_faction_relation"),  ## NMCml FL: keep relation
		(store_troop_faction, ":commander_faction", "$enlisted_lord"),
		(try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
           (neq, ":commander_faction", ":cur_faction"),
		   (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
           (call_script, "script_set_player_relation_with_faction", ":cur_faction", -5),
        (try_end),	
		(try_begin),
			(store_relation, ":player_relation", ":commander_faction", "fac_player_supporters_faction"),
			(lt, ":player_relation", 5),
			(call_script, "script_set_player_relation_with_faction", ":commander_faction", 5),
		(try_end),
		## NMCml FL begin: keep banner
		(party_set_slot, "p_freelancer_party_backup", slot_freelancer_last_banner, 0),
		(troop_get_slot, ":banner", "trp_player", slot_troop_banner_scene_prop),
		(try_begin),
			(gt, ":banner", 0),
			(party_set_slot, "p_freelancer_party_backup", slot_freelancer_last_banner, ":banner"),
		(try_end),
		(troop_get_slot, ":banner", "$enlisted_lord", slot_troop_banner_scene_prop),
		(troop_set_slot, "trp_player", slot_troop_banner_scene_prop, ":banner"),
		## NMCml FL end

		(call_script, "script_freelancer_attach_party"),
		## NMCml FL begin: quest fix
		(try_begin),
		  (check_quest_active, "qst_freelancer_vacation"),
		  (call_script, "script_end_quest", "qst_freelancer_vacation"),
		(try_end),
		## NMCml FL end
		(display_message, "@You have rejoined your commander!"), 		
    ]),
	
	
  # RUNS IF PLAYER DESERTS OR IS AWOL
  ("event_player_deserts",
   [     
   	(store_troop_faction, ":commander_faction", "$enlisted_lord"),
    (call_script, "script_fl_recover_faction_relation", ":commander_faction"),  ## NMCml FL: keep relation
	(call_script, "script_change_player_relation_with_faction_ex", ":commander_faction", -10), 
    (call_script, "script_change_player_relation_with_troop", "$enlisted_lord", -10),
    (call_script, "script_change_player_honor", -20),
	
	(troop_set_slot, "trp_player", slot_troop_current_mission, 0),
	#(troop_set_slot, "trp_player", slot_troop_days_on_mission, 0),  ## NMCml FL: quest fix
	(faction_set_slot, ":commander_faction", slot_faction_freelancer_troop, 0),
	## NMCml FL begin: keep banner
	#(troop_set_slot, "trp_player", slot_troop_banner_scene_prop, 0),
	(party_get_slot, ":banner", "p_freelancer_party_backup", slot_freelancer_last_banner),
	(troop_set_slot, "trp_player", slot_troop_banner_scene_prop, ":banner"),
	## NMCml FL end
	(rest_for_hours, 0,0,0),
	(assign, "$freelancer_state", 0),
	#(display_message, "@You have deserted your commander!"), #Taken care of elsewhere
	(call_script, "script_fail_quest", "qst_freelancer_enlisted"),
	## NMCml FL begin: quest fix
	(call_script, "script_end_quest", "qst_freelancer_enlisted"),
	## NMCml FL end
	## CC-D begin: local achievement
	(store_current_day, ":cur_day"),
	(troop_get_slot, ":service_day_start", "trp_player", slot_troop_freelancer_start_date),
	(store_sub, ":service_length", ":cur_day", ":service_day_start"),
	(try_begin),
	  (neg|troop_slot_ge, "trp_ccd_treasure", slot_troop_ccd_rec_max_fl_days, ":service_length"),
	  (troop_set_slot, "trp_ccd_treasure", slot_troop_ccd_rec_max_fl_days, ":service_length"),
	(try_end),
	## CC-D end
   ]),	
	
	
	# RETURNS PART OF THE ORIGINAL PARTY
    ("party_restore", 
    [
        ## CC-D begin: keep player party refer from TinyModPatcher
        (try_begin),
          (eq, "$g_fl_keep_player_party_nobackup", 0),
          
        (store_current_day, ":cur_day"),
        #formula for soldier desertion chance
		(troop_get_slot, ":service_day_start", "trp_player", slot_troop_freelancer_start_date),
        (store_sub, ":service_length", ":cur_day", ":service_day_start"), #gets number of days served
		(party_get_slot, ":morale", "p_main_party", slot_party_orig_morale),
        (store_add, ":return_chance", 800, ":morale"), #up to 100
        (val_sub, ":return_chance", ":service_length"), #up to far over 100

        #loop that looks at each troop stack in a party, 
        #then decides if troops of that stack will return, 
        #and randomly assigns a number of troops in that stack to return
        (party_get_num_companion_stacks, ":num_stacks", "p_freelancer_party_backup"),
        (try_for_range, ":cur_stack", 0, ":num_stacks"),
			(assign, ":stack_amount", 0),
			(party_stack_get_troop_id, ":return_troop", "p_freelancer_party_backup", ":cur_stack"),
			(neq, ":return_troop", "trp_player"),
			(try_begin),
				(troop_is_hero, ":return_troop"), #bugfix for companions (simple, they always return)
				(assign, ":stack_amount", 1),
			(else_try),
				#limit may need changed for more accurate probability
				(store_random_in_range, ":return_random", 0, 1000),
				(is_between, ":return_random", 0, ":return_chance"),
				(party_stack_get_size, ":stack_size", "p_freelancer_party_backup", ":cur_stack"),
				#checks what chance there is that all troops in stack will return
				(store_random_in_range, ":return_random", 0, 1000),
				(try_begin),
					(is_between, ":return_random", 0, ":return_chance"),
					(assign, ":stack_amount", ":stack_size"),
				(else_try),
					#else random number of troops return
					(store_random_in_range, ":stack_amount", 0, ":stack_size"),
				(try_end),
			(try_end),
			(ge, ":stack_amount", 1),
			(party_add_members, "p_main_party", ":return_troop", ":stack_amount"),
        (try_end),
          
          (display_message, "@You rejoin your party."),
        (try_end),
        ## CC-D end
		(party_clear, "p_freelancer_party_backup"),
    ]),

#  CALCULATES NUMBER OF DESERTING TROOPS

   ("get_desert_troops", #CABA - check this
    [
        (party_get_morale, ":commander_party_morale", "$enlisted_party"), #does this actually get tracked for non-player parties?
        (store_current_day, ":cur_day"),
        #formula for soldier desertion chance
        #gets number of days served
		(troop_get_slot, ":service_day_start", "trp_player", slot_troop_freelancer_start_date),
        (store_sub, ":service_length", ":cur_day", ":service_day_start"),
        #inverts the commander's party morale
        (store_sub, ":commander_neg_morale", 100, ":commander_party_morale"), #still a positive number... 100-80 = 20
        (store_skill_level, ":cur_leadership", "skl_leadership", "trp_player"),
        (store_skill_level, ":cur_persuasion", "skl_persuasion", "trp_player"),
        #had to multiply these skills to give them a decent effect on desertion chance
        (val_mul, ":cur_leadership", 10), #up to 100
        (val_mul, ":cur_persuasion", 10), #up to 100
        (store_add, ":desert_chance", ":cur_leadership", ":cur_persuasion"), #up to 200
		(val_add, ":desert_chance", ":service_length"), #up to 400 maybe
        (val_add, ":desert_chance", ":commander_neg_morale"), #up to 450, maybe? if party morale is down to 50
        #loop that looks at each troop stack in a party, 
        #then decides if troops of that stack will desert, 
        #and randomly assigns a number of troops in that stack to desert
        (party_get_num_companion_stacks, ":num_stacks", "$enlisted_party"),
        (try_for_range_backwards, ":cur_stack", 1, ":num_stacks"),
            #limit may need changed for more accurate probability
            (store_random_in_range, ":desert_random", 0, 1000),
            (is_between, ":desert_random", 0, ":desert_chance"),
			#switching deserting troops to player party
			(party_stack_get_troop_id, ":desert_troop", "$enlisted_party", ":cur_stack"),
			(party_stack_get_size, ":stack_size", "$enlisted_party", ":cur_stack"),
			(store_random_in_range, ":stack_amount", 0, ":stack_size"),
			(party_remove_members, "$enlisted_party", ":desert_troop", ":stack_amount"),
			(party_add_members, "p_main_party", ":desert_troop", ":stack_amount"),
        (try_end),        		
    ]),
	
  ("freelancer_keep_field_loot",
   [
	(get_player_agent_no, ":player"),
	(try_for_range, ":ek_slot", ek_item_0, ek_head),
		(agent_get_item_slot, ":item", ":player", ":ek_slot"), 
		(gt, ":item", 0),
		(neg|troop_has_item_equipped, "trp_player", ":item"),
		(troop_add_item, "trp_player", ":item"),
	(try_end),
	(agent_get_horse, ":horse", ":player"),
	(try_begin),
	  (gt, ":horse", 0),
	  (agent_get_item_id, ":horse", ":horse"),
	  (troop_get_inventory_slot, ":old_horse", "trp_player", ek_horse),
	  (neq, ":horse", ":old_horse"),
	  (try_begin),
		(gt, ":old_horse", 0),
		(troop_get_inventory_slot_modifier, ":horse_imod", "trp_player", ek_horse),
		(troop_add_item, "trp_player", ":old_horse", ":horse_imod"),
	  (try_end),
	  (troop_set_inventory_slot, "trp_player", ek_horse, ":horse"),
	(try_end),
   ]),
	  
   ("cf_freelancer_player_can_upgrade",
   #Reg0 outputs reason for failure
   [
	(store_script_param_1, ":source_troop"),
	
	(troop_get_inventory_capacity, ":troop_cap", ":source_troop"),	
	(assign, ":continue", 1),
	
	(assign, ":type_available", 0),
	(assign, ":type_count", 0),
	(assign, ":end", itp_type_arrows),
	(try_for_range, ":type", itp_type_one_handed_wpn, ":end"),
		#Count Items from Source Troop
		(assign, ":end2", ":troop_cap"),
		(try_for_range, ":inv_slot", 0, ":end2"),
		    (troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
			(gt, ":item", 0),
			(item_get_type, ":item_type", ":item"),
			(eq, ":item_type", ":type"),
			(val_add, ":type_count", 1),
			(call_script, freelancer_can_use_item, "trp_player", ":item", 0),
			(eq, reg0, 1),		
			(assign, ":type_available", 1),
			(assign, ":end2", 0), #break
		(try_end),
		(eq, ":type_available", 1),
		(assign, ":end", itp_type_one_handed_wpn), #break
	(try_end), #Melee loop
	(try_begin),
		(eq, ":type_available", 0),
		(gt, ":type_count", 0), #only care if there were items possible to equip
		(assign, ":continue", 0),
		(assign, reg0, 0),
	(try_end),
	(eq, ":continue", 1),
	
	(assign, ":type_available", 0),
	(assign, ":type_count", 0),
	(assign, ":end2", ":troop_cap"),
	(try_for_range, ":inv_slot", 0, ":end2"),
		(troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
		(gt, ":item", 0),
		(item_get_type, ":item_type", ":item"),
		(eq, ":item_type", itp_type_body_armor),
		(val_add, ":type_count", 1),
		(call_script, freelancer_can_use_item, "trp_player", ":item", 0),
		(eq, reg0, 1),		
		(assign, ":type_available", 1),
		(assign, ":end2", 0), #break
	(try_end),
	(try_begin),
		(eq, ":type_available", 0),
		(gt, ":type_count", 0), #only care if there were items possible to equip
		(assign, ":continue", 0),
		(assign, reg0, 1),
	(try_end),
	(eq, ":continue", 1),
	
	(try_begin),
		(troop_is_guarantee_ranged, ":source_troop"),
		(assign, ":type_available", 0),
		(assign, ":type_count", 0),
		(assign, ":end", itp_type_goods),
		(try_for_range, ":type", itp_type_bow, ":end"),
			#Count Items from Source Troop
			(assign, ":end2", ":troop_cap"),
			(try_for_range, ":inv_slot", 0, ":end2"),
				(troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
				(gt, ":item", 0),
				(item_get_type, ":item_type", ":item"),
				(eq, ":item_type", ":type"),
				(val_add, ":type_count", 1),
				(call_script, freelancer_can_use_item, "trp_player", ":item", 0),
				(eq, reg0, 1),		
				(assign, ":type_available", 1),
				(assign, ":end2", 0), #break
			(try_end),
			(eq, ":type_available", 1),
			(assign, ":end", itp_type_bow), #break
		(try_end), #Ranged loop
		(eq, ":type_available", 0),
		(gt, ":type_count", 0), #only care if there were items possible to equip
		(assign, ":continue", 0),
		(assign, reg0, 2), 
	(try_end),
	(eq, ":continue", 1),
	
	## NMCml FL begin: check gun
	(try_begin),
		(troop_is_guarantee_ranged, ":source_troop"),
		(assign, ":type_available", 0),
		(assign, ":type_count", 0),
		(assign, ":end", itp_type_bullets),
		(try_for_range, ":type", itp_type_pistol, ":end"),
			#Count Items from Source Troop
			(assign, ":end2", ":troop_cap"),
			(try_for_range, ":inv_slot", 0, ":end2"),
				(troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
				(gt, ":item", 0),
				(item_get_type, ":item_type", ":item"),
				(eq, ":item_type", ":type"),
				(val_add, ":type_count", 1),
				(call_script, freelancer_can_use_item, "trp_player", ":item", 0),
				(eq, reg0, 1),		
				(assign, ":type_available", 1),
				(assign, ":end2", 0), #break
			(try_end),
			(eq, ":type_available", 1),
			(assign, ":end", itp_type_pistol), #break
		(try_end), #Gun loop
		(eq, ":type_available", 0),
		(gt, ":type_count", 0), #only care if there were items possible to equip
		(assign, ":continue", 0),
		(assign, reg0, 2), 
	(try_end),
	(eq, ":continue", 1),
	## NMCml FL end
	
	(try_begin),
		(troop_is_guarantee_horse, ":source_troop"),
		(assign, ":type_available", 0),
		(assign, ":type_count", 0),
		(assign, ":end2", ":troop_cap"),
		(try_for_range, ":inv_slot", 0, ":end2"),
			(troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
			(gt, ":item", 0),
			(item_get_type, ":item_type", ":item"),
			(eq, ":item_type", itp_type_horse),
			(val_add, ":type_count", 1),
			(call_script, freelancer_can_use_item, "trp_player", ":item", 0),
			(eq, reg0, 1),		
			(assign, ":type_available", 1),
			(assign, ":end2", 0), #break
		(try_end),
		(eq, ":type_available", 0),
		(gt, ":type_count", 0), #only care if there were items possible to equip
		(assign, ":continue", 0),
		(assign, reg0, 3),
	(try_end),
	(eq, ":continue", 1),	
   ]),
   
   
    ("freelancer_equip_troop",
   [
    (store_script_param_1, ":source_troop"),
	
	(str_clear, s2),
	(set_show_messages, 0),
	
	(assign, ":recording_slot", slot_freelancer_equip_start),	
	(troop_get_inventory_capacity, ":troop_cap", ":source_troop"),
	(assign, ":melee_given", 0),
	(assign, ":needs_ammo", 0),
	(assign, ":open_weapon_slot", 0),
	(try_for_range, ":type", itp_type_horse, itp_type_animal),  ## NMCml FL: check gun: itp_type_pistol->itp_type_animal
	    (neq, ":type", itp_type_goods),
		(neq, ":type", itp_type_arrows),
		(neq, ":type", itp_type_bolts),
		(neq, ":type", itp_type_bullets),  ## NMCml FL: check gun
		
		#Assign Prob. of Getting Type
		(assign, ":continue", 0),
		(try_begin),
			(troop_is_guarantee_horse, ":source_troop"),
		    (eq, ":type", itp_type_horse),
			(assign, ":continue", 1),
		(else_try),
		    (troop_is_guarantee_ranged, ":source_troop"),
		    (this_or_next|eq, ":type", itp_type_bow),
			(this_or_next|eq, ":type", itp_type_crossbow),
			## NMCml FL begin: check gun
			(this_or_next|eq, ":type", itp_type_pistol),
			(this_or_next|eq, ":type", itp_type_musket),
			## NMCml FL end
			(eq, ":type", itp_type_thrown),
			(assign, ":continue", 1),
		(else_try),
		    (this_or_next|eq, ":type", itp_type_shield), #Shields and all armor pieces are guaranteed
		    (ge, ":type", itp_type_head_armor),
		    (lt, ":type", itp_type_pistol),  ## NMCml FL: check gun
			(assign, ":continue", 1),
		(else_try),
		    (neq, ":type", itp_type_horse),
		    (lt, ":open_weapon_slot", 4),
			(store_random_in_range, ":continue", 0, 3), # 1 chance in three of being 1
		(try_end),
		(eq, ":continue", 1),		
		
		#Clear Temp Array
		(try_for_range, ":inv_slot", 0, 20),
			(troop_set_slot, "trp_temp_array_a", ":inv_slot", 0),
		(try_end),	
		
		#Collect Items from Source Troop
		(assign, ":type_count", 0),
		(try_for_range, ":inv_slot", 0, ":troop_cap"),
		    (troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
			(gt, ":item", 0),
			(item_get_type, ":item_type", ":item"),
			(eq, ":item_type", ":type"),
			(call_script, freelancer_can_use_item, "trp_player", ":item", 0),
			(eq, reg0, 1),		
			(troop_set_slot, "trp_temp_array_a", ":type_count", ":item"),
			(val_add, ":type_count", 1),
		(try_end),
		(gt, ":type_count", 0),
		
		#Pick Random Item of Type from Troop
		(try_begin),
		    (eq, ":type_count", 1),
			(assign, ":index", 0),
		(else_try),
			(store_random_in_range, ":index", 0, ":type_count"),
		(try_end),
		(troop_get_slot, ":item", "trp_temp_array_a", ":index"),
		(gt, ":item", 0),		
		(str_store_item_name, s3, ":item"),
		(str_store_string, s2, "@{s3}, {s2}"),
		
		#Select correct EK slot to force equip
		(try_begin),
		    (eq, ":type", itp_type_horse),
			(assign, ":ek_slot", ek_horse),
		(else_try),
		    (is_between, ":type", itp_type_head_armor, itp_type_pistol),
			(store_sub, ":shift", ":type", itp_type_head_armor),
			(store_add, ":ek_slot", ek_head, ":shift"),
		(else_try),
			(store_add, ":ek_slot", ek_item_0, ":open_weapon_slot"),
		(try_end),
		
		## CC-D begin: stop auto equip
		(try_begin),
		  (eq, "$g_fl_no_auto_equip", 0),
		
		#Check for item already there, move it if present
		(try_begin),
		    (troop_get_inventory_slot, ":old_item", "trp_player", ":ek_slot"),
			(gt, ":old_item", 0),
			(troop_get_inventory_slot_modifier, ":old_item_imod", "trp_player", ":ek_slot"),
			(troop_add_item, "trp_player", ":old_item", ":old_item_imod"),
		(try_end),
		
		#Add Item
		(troop_set_inventory_slot, "trp_player", ":ek_slot", ":item"),
		
		(else_try),
		  (troop_add_item, "trp_player", ":item", 0),
		(try_end),
		## CC-D end
		(party_set_slot, "p_freelancer_party_backup", ":recording_slot", ":item"),
		(val_add, ":recording_slot", 1),
		(try_begin),
		    ## NMCml FL begin: check gun
		    (this_or_next|eq, ":type", itp_type_pistol),
		    (this_or_next|eq, ":type", itp_type_musket),
		    ## NMCml FL end
		    (is_between, ":type", itp_type_one_handed_wpn, itp_type_head_armor), #Uses one of the 4 weapon slots
		    (val_add, ":open_weapon_slot", 1),
			(try_begin),
				(is_between, ":type", itp_type_one_handed_wpn, itp_type_arrows),
				(assign, ":melee_given", 1),
            (else_try),
				(eq, ":type", itp_type_bow),
				(assign, ":needs_ammo", itp_type_arrows),
			(else_try),
				(eq, ":type", itp_type_crossbow),
				(assign, ":needs_ammo", itp_type_bolts),
			## NMCml FL begin: check gun
			(else_try),
				(this_or_next|eq, ":type", itp_type_pistol),
				(eq, ":type", itp_type_musket),
				(assign, ":needs_ammo", itp_type_bullets),
			## NMCml FL end
			(try_end),
		(try_end),
	(try_end), #Item Types Loop
	 
    #add ammo for any equipped bow
    (try_begin),
	    (neq, ":needs_ammo", 0),		
		#Check for item already in the last slot, move it if present
		## CC-D begin: stop auto equip
		(try_begin),
		  (eq, "$g_fl_no_auto_equip", 0),
		
		(try_begin), 
		    (troop_get_inventory_slot, ":old_item", "trp_player", ek_item_3),
			(gt, ":old_item", 0),
			(troop_get_inventory_slot_modifier, ":old_item_imod", "trp_player", ek_item_3),
			(troop_add_item, "trp_player", ":old_item", ":old_item_imod"), 
		(try_end),
		
		(try_end),
		## CC-D end
		
		(assign, ":end", ":troop_cap"),
		(try_for_range, ":inv_slot", 0, ":end"),
		    (troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
			(gt, ":item", 0),
			(item_get_type, ":type", ":item"),
			(eq, ":type", ":needs_ammo"),
			## CC-D begin: stop auto equip
			(try_begin),
			  (eq, "$g_fl_no_auto_equip", 0),
			
			(troop_set_inventory_slot, "trp_player", ek_item_3, ":item"),
			
			(else_try),
			  (troop_add_item, "trp_player", ":item", 0),
			(try_end),
			## CC-D end
			(party_set_slot, "p_freelancer_party_backup", ":recording_slot", ":item"),
		    (val_add, ":recording_slot", 1),
			(assign, ":open_weapon_slot", 4),
			(str_store_item_name, s3, ":item"),
		    (str_store_string, s2, "@{s3}, {s2}"),
			(assign, ":end", 0),
		(try_end),
	(try_end), 
	
	#double check melee was given
	(try_begin),
	    (eq, ":melee_given", 0),
		(assign, ":end", ":troop_cap"),
		(try_for_range, ":inv_slot", 0, ":end"),
		    (troop_get_inventory_slot, ":item", ":source_troop", ":inv_slot"),
			(gt, ":item", 0),
			(item_get_type, ":type", ":item"),
			(is_between, ":type", itp_type_one_handed_wpn, itp_type_arrows),
			(call_script, freelancer_can_use_item, "trp_player", ":item", 0),
			(eq, reg0, 1),	
			(try_begin),
			    (gt, ":open_weapon_slot", 3),
			    (assign, ":open_weapon_slot", 2),
			(try_end),
			
			## CC-D begin: stop auto equip
			(try_begin),
			  (eq, "$g_fl_no_auto_equip", 0),
			
			#Check for item already there
			(try_begin),
				(troop_get_inventory_slot, ":old_item", "trp_player", ":open_weapon_slot"),
				(gt, ":old_item", 0),
				(troop_get_inventory_slot_modifier, ":old_item_imod", "trp_player", ":open_weapon_slot"),
				(troop_add_item, "trp_player", ":old_item", ":old_item_imod"),
			(try_end),
			
			(troop_set_inventory_slot, "trp_player", ":open_weapon_slot", ":item"),		
			
			(else_try),
			  (troop_add_item, "trp_player", ":item", 0),
			(try_end),
			## CC-D end
			(party_set_slot, "p_freelancer_party_backup", ":recording_slot", ":item"),
		    (val_add, ":recording_slot", 1),
			(str_store_item_name, s3, ":item"),
		    (str_store_string, s2, "@{s3}, {s2}"),
		    (assign, ":end", 0),
		(try_end),
	(try_end), 
	
    (set_show_messages, 1),
	(try_begin),
		(neg|str_is_empty, s2),
		(val_sub, ":recording_slot", slot_freelancer_equip_start),
		(party_set_slot, "p_freelancer_party_backup", slot_freelancer_equip_start - 1, ":recording_slot"),	#Record Number of Items Added
		
		(str_store_troop_name, s1, ":source_troop"),
		(display_message, "@The equipment of a {s1}: {s2}is assigned to you."),	
	(try_end),
   ]),
	
  ("freelancer_unequip_troop",
   [
    (store_script_param_1, ":source_troop"),

	(str_clear, s2),	
	(set_show_messages, 0),
	
	(party_get_slot, ":num_items", "p_freelancer_party_backup", slot_freelancer_equip_start - 1), #Num of items previously given
	
    (troop_get_inventory_capacity, ":cap", "trp_player"),		
	(try_for_range, ":i", 0, ":num_items"),
	    (store_add, ":slot", slot_freelancer_equip_start, ":i"),
	    (party_get_slot, ":given_item", "p_freelancer_party_backup", ":slot"),
		(gt, ":given_item", 0),
		
		(assign, ":end", ":cap"),
		(try_for_range, ":inv_slot", 0, ":end"),
			(troop_get_inventory_slot, ":item", "trp_player", ":inv_slot"),
			(eq, ":item", ":given_item"),			
			(troop_get_inventory_slot_modifier, ":imod", "trp_player", ":inv_slot"),
			(eq, ":imod", 0), #Native troop items never have modifiers
			
			(troop_set_inventory_slot, "trp_player", ":inv_slot", -1),
			(str_store_item_name, s3, ":item"),
			(str_store_string, s2, "@{s3}, {s2}"),
			
			(assign, ":end", 0), #Break
		(try_end), #Player Inventory Loop
	(try_end), #Item Given Slot Loop

	(set_show_messages, 1),
	(try_begin),
		(neg|str_is_empty, s2),
		(party_set_slot, "p_freelancer_party_backup", slot_freelancer_equip_start - 1, 0),	#Reset Number of Items Added
		(str_store_troop_name, s1, ":source_troop"),
		(display_message, "@The equipment of a {s1}: {s2}is taken from you."),
	(try_end),	
	## CC-D begin: stop auto equip
	(try_begin),
	  (eq, "$g_fl_no_auto_equip", 0),
	
	(troop_equip_items, "trp_player"),
	
	(try_end),
	## CC-D end
   ]), 
#+freelancer end

### NMCml FL begin: individual script: script_troop_can_use_item based on CC
#   # Can a troop qualify to use this item?
#   # Returns 1 = yes, 0 = no.
#("fl_troop_can_use_item",
#  [
#    (store_script_param, ":troop", 1),
#    (store_script_param, ":item", 2),
#    (store_script_param, ":item_modifier", 3),
#
#    (item_get_type, ":type", ":item"),
#    (try_begin),
#      (eq, ":type", itp_type_book),
#      (item_get_slot, ":difficulty", ":item", slot_item_intelligence_requirement),
#    (else_try),
#      #(item_get_slot, ":difficulty", ":item", slot_item_difficulty),
#      (item_get_difficulty, ":difficulty", ":item"),  ##1.161
#    (try_end),
#
#    (try_begin),
#      (eq, ":difficulty", 0), # don't apply imod modifiers if item has no requirement
#    (else_try),
#      (eq, ":item_modifier", imod_stubborn),
#      (val_add, ":difficulty", 1),
#    (else_try),
#      (eq, ":item_modifier", imod_timid),
#      (val_sub, ":difficulty", 1),
#    (else_try),
#      (eq, ":item_modifier", imod_champion),  ##add
#      (val_add, ":difficulty", 2),
#    (else_try),
#      (eq, ":item_modifier", imod_heavy),
#      (neq, ":type", itp_type_horse), #heavy horses don't increase difficulty
#      (val_add, ":difficulty", 1),
#    (else_try),
#      (eq, ":item_modifier", imod_strong),
#      (val_add, ":difficulty", 2),
#    (else_try),
#      (eq, ":item_modifier", imod_masterwork),
#      (val_add, ":difficulty", 4),
#    (try_end),
#
#    (try_begin),
#      (eq, ":type", itp_type_horse),
#      (store_skill_level, ":skill", skl_riding, ":troop"),
#    (else_try),
#      (this_or_next|eq, ":type", itp_type_crossbow),
#      (this_or_next|eq, ":type", itp_type_one_handed_wpn),
#      (this_or_next|eq, ":type", itp_type_two_handed_wpn),
#      (this_or_next|eq, ":type", itp_type_polearm),
#      (this_or_next|eq, ":type", itp_type_head_armor),
#      (this_or_next|eq, ":type", itp_type_body_armor),
#      (this_or_next|eq, ":type", itp_type_foot_armor),
#      (eq, ":type", itp_type_hand_armor),
#      (store_attribute_level, ":skill", ":troop", ca_strength),
#    (else_try),
#      (eq, ":type", itp_type_shield),
#      (store_skill_level, ":skill", skl_shield, ":troop"),
#    (else_try),
#      (eq, ":type", itp_type_bow),
#      (store_skill_level, ":skill", skl_power_draw, ":troop"),
#    (else_try),
#      (eq, ":type", itp_type_thrown),
#      (store_skill_level, ":skill", skl_power_throw, ":troop"),
#    (else_try),
#      (eq, ":type", itp_type_book),
#      (store_attribute_level, ":skill", ":troop", ca_intelligence),
#    (try_end),
#
#    (try_begin),
#      (this_or_next|lt, ":skill", ":difficulty"),
#      (this_or_next|is_between, ":item", reference_books_begin, reference_books_end),
#      (eq, ":item_modifier", imod_lame),
#      (assign, reg0, 0),
#    #(else_try),
#    #  (troop_slot_eq, ":troop", slot_upgrade_horse, 1),
#    #  (item_slot_eq, ":item", slot_item_cant_on_horseback, 1),
#    #  (assign, reg0, 0),
#    (else_try),
#      (assign, reg0, 1),
#    (try_end),
#  ]),
### NMCml FL end
## NMCml FL begin: keep relation
  ("fl_record_faction_relation",
  [
    (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
      (store_relation, ":relation", ":cur_faction", "fac_player_supporters_faction"),
      (faction_set_slot, ":cur_faction", slot_faction_fl_last_relation, ":relation"),
    (try_end),
  ]),
  ("fl_recover_faction_relation",
  [
    (store_script_param_1, ":except_faction"),
    
    (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
      (neq, ":except_faction", ":cur_faction"),
      (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
      (faction_get_slot, ":relation", ":cur_faction", slot_faction_fl_last_relation),
      (call_script, "script_set_player_relation_with_faction", ":cur_faction", ":relation"),
    (try_end),
  ]),
## NMCml FL end
## CC-D begin
  ("ccd_fl_update_faction_relation",
  [
    (store_faction_of_party, ":commander_faction", "$enlisted_party"),
    (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
      (neq, ":commander_faction", ":cur_faction"),
      (faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
      (store_relation, ":caravan_relation", ":cur_faction", ":commander_faction"),
      (store_relation, ":player_relation", ":cur_faction", "fac_player_supporters_faction"),
      (try_begin),
        (ge, ":caravan_relation", 0),
        (lt, ":player_relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":cur_faction", 5),
      (else_try),
        (lt, ":caravan_relation", 0),
        (ge, ":player_relation", 0),
        (call_script, "script_set_player_relation_with_faction", ":cur_faction", -5),
      (try_end),
    (try_end),
  ]),
  ("event_player_enlists_caravan",
  [
    #initialize service variables
    (troop_get_xp, ":xp", "trp_player"),
    (troop_set_slot, "trp_player", slot_troop_freelancer_start_xp, ":xp"),
    (store_current_day, ":day"), 
    (troop_set_slot, "trp_player", slot_troop_freelancer_start_date, ":day"),
    (party_get_morale, ":morale", "p_main_party"),
    (party_set_slot, "p_main_party", slot_party_orig_morale, ":morale"),
    
    #needed to stop bug where parties attack the old player party
    (call_script, "script_set_parties_around_player_ignore_player", 2, 4),
    #set lord as your commander
    (assign, "$enlisted_lord", "$g_talk_troop"),
    #(troop_get_slot, "$enlisted_party", "$enlisted_lord", slot_troop_leaded_party), 
    (assign, "$enlisted_party", "$g_encountered_party"),   #change
    #removes troops from player party
    (try_begin),
      (eq, "$g_fl_keep_player_party", 0),
      (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
      (try_for_range_backwards, ":cur_stack", 1, ":num_stacks"), #lower bound is 1 to ignore player character
        (party_stack_get_troop_id, ":cur_troops", "p_main_party", ":cur_stack"),
        (party_stack_get_size, ":cur_size", "p_main_party", ":cur_stack"),
        (party_remove_members, "p_main_party", ":cur_troops", ":cur_size"),
      (try_end),
      (assign, "$g_fl_keep_player_party_nobackup", 0),
      (display_message, "@You leave your party temporarily."),
    (else_try),
      (assign, "$g_fl_keep_player_party_nobackup", 1),
    (try_end),
    
    #set faction relations to allow player to join battles
    #faction relation record, and fit
    (call_script, "script_fl_record_faction_relation"),
    (call_script, "script_ccd_fl_update_faction_relation"),
    
    #not change equip, banner and quest
    (assign, "$player_cur_troop", "trp_player"),
    
    (call_script, "script_freelancer_attach_party"),
    #makes Lords banner the players
    (display_message, "@You join the caravan."),
  ]),
  ("event_player_discharge_caravan",
  [
    #removes faction relation given at enlist
    (store_faction_of_party, ":commander_faction", "$enlisted_party"),
    #(call_script, "script_change_player_relation_with_faction_ex", ":commander_faction", 1),
    (call_script, "script_fl_recover_faction_relation", ":commander_faction"),
    
    (troop_set_slot, "trp_player", slot_troop_current_mission, 0),
    (troop_set_slot, "trp_player", slot_troop_days_on_mission, 0),
    (assign, "$freelancer_state", 0),
    (call_script, "script_freelancer_detach_party"),
    (rest_for_hours, 0, 0, 0),
    (display_message, "@You left the caravan."), 
    
    (store_current_day, ":cur_day"),
    (troop_get_slot, ":service_day_start", "trp_player", slot_troop_freelancer_start_date),
    (store_sub, ":service_length", ":cur_day", ":service_day_start"),
    (try_begin),
      (neq, ":service_length", 0),
      (store_mul, ":reward_period", ":service_length", 100),
      (val_div, ":reward_period", 30),
    (try_end),
    (troop_add_gold, "trp_player", ":reward_period"),
    
    ## CC-D begin: local achievement
    (try_begin),
      (neg|troop_slot_ge, "trp_ccd_treasure", slot_troop_ccd_rec_max_fl_days, ":service_length"),
      (troop_set_slot, "trp_ccd_treasure", slot_troop_ccd_rec_max_fl_days, ":service_length"),
    (try_end),
    ## CC-D end
    ]),
## CC-D end
##OCCC start

  # script_occc_freelancer_extra_lord
  # INPUT: p1=lord
  # OUTPUT:reg0:$player_cur_troop
  ("occc_freelancer_extra_lord",
  [
      (store_script_param, ":lord", 1),
      
            (store_troop_faction, ":commander_faction", ":lord"),
            (try_begin),
            #vader
                (eq,":lord","trp_knight_7_vader"),
                (assign,"$player_cur_troop","trp_occc_imperial_stormtrooper"),
            (else_try),
            #leonidas
                (eq,":lord","trp_knight_8_1"),
                (assign,"$player_cur_troop","trp_ore_spartanwarrior"),
            (else_try),
                (this_or_next|eq,":lord","trp_knight_2_1"),
                (eq,":lord","trp_knight_2_2"),#Red Coats 
                (neq,"$g_occc_make_factions_medieval",4),#Not Old Vaegir
                (neq,"$g_occc_make_factions_medieval",3),#Not Old Vaegir
                (neq,"$g_occc_make_factions_medieval",1),#Not Old Vaegir
                (assign,"$player_cur_troop","trp_ccc_vaegir_western_people_2"),
            (else_try),
                (faction_get_slot, "$player_cur_troop", ":commander_faction", slot_faction_tier_1_troop),
            (try_end),
      
      (assign,reg0,"$player_cur_troop"),
  ]),

##OCCC end
]


from util_wrappers import *
from util_scripts import *

scripts_directives = [
	[SD_OP_BLOCK_INSERT, "agent_reassign_team", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE,(party_stack_get_troop_id, ":leader_troop_id", ":party_no", 0),0,not_in_party],
    [SD_OP_BLOCK_INSERT, "game_start", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER,(assign, "$g_player_luck", 200),0,
	[
		(assign, "$freelancer_state", 0),
    ]],
	[SD_OP_BLOCK_INSERT, "encounter_init_variables", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (gt, "$g_starting_strength_friends", 0),0,
	[
		#(try_begin), #in the script 
      	    (eq, "$freelancer_state", 1),
			(store_character_level, "$g_strength_contribution_of_player", "$player_cur_troop"),
			(val_div, "$g_strength_contribution_of_player", 2),
			(val_max, "$g_strength_contribution_of_player", 5), #contribution(scale 0-100) = level/2, min 5 (so about 5-25)
			#(store_character_level, ":freelancer_player_contribution", "$player_cur_troop"),
			#(val_mul, ":freelancer_player_contribution", 6),
			#(val_div, ":freelancer_player_contribution", 5), #level * 1.2 (for a bit of a scaling bump)
			#(val_max, ":freelancer_player_contribution", 10), #and to give a base line
			#(assign, "$g_strength_contribution_of_player", ":freelancer_player_contribution"),
        (else_try),			
	]],
    [SD_OP_BLOCK_INSERT, "enter_court", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER,(party_stack_get_troop_id, ":stack_troop","p_temp_party",":i_stack"),0,
	[
		(gt, ":stack_troop", 0),
    ]],	
	## NMCml FL begin: fix marshall bug and player prisoner
    [SD_OP_BLOCK_INSERT, "game_event_simulate_battle", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE,(troop_set_slot, ":cur_troop_id", slot_troop_leaded_party, -1),0,
	[
		(neq, ":cur_troop_id", "trp_player"),
    ]],
	## NMCml FL end
	
	##FLORIS ONLY - Trade with Merchant Caravans
	#[SD_OP_BLOCK_INSERT, "party_give_xp_and_gold", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_BEFORE, (party_slot_eq, ":enemy_party", slot_party_type, spt_kingdom_caravan),0,not_in_party],	
	##FLORIS ONLY END	
]
                
def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
	# add remaining scripts
	add_scripts(orig_scripts, scripts, True)
	
# Used by modmerger framework version >= 200 to merge stuff
# This function will be looked for and called by modmerger if this mod is active
# Do not rename the function, though you can insert your own merging calls where indicated
def modmerge(var_set):
    try:
        var_name_1 = "scripts"
        orig_scripts = var_set[var_name_1]
    
        
		# START do your own stuff to do merging
		
        modmerge_scripts(orig_scripts)

		# END do your own stuff
        
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
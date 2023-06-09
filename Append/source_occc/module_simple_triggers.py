from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
##diplomacy start+
from header_terrain_types import *
from module_factions import dplmc_factions_end
##diplomacy end+

from module_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#  Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################



simple_triggers = [

# This trigger is deprecated. Use "script_game_event_party_encounter" in module_scripts.py instead
  (ti_on_party_encounter,
   [
    ]),


# This trigger is deprecated. Use "script_game_event_simulate_battle" in module_scripts.py instead
  (ti_simulate_battle,
   [
    ]),


  (1,
   [
      (try_begin),
        (eq, "$training_ground_position_changed", 0),
        (assign, "$training_ground_position_changed", 1),
		(set_fixed_point_multiplier, 100),
        (position_set_x, pos0, 7050),
        (position_set_y, pos0, 7200),
        (party_set_position, "p_training_ground_3", pos0),
      (try_end),

      (gt,"$auto_besiege_town",0),
      (gt,"$g_player_besiege_town", 0),
      (ge, "$g_siege_method", 1),
      (store_current_hours, ":cur_hours"),
      (eq, "$g_siege_force_wait", 0),
      (ge, ":cur_hours", "$g_siege_method_finish_hours"),
      (neg|is_currently_night),
      (rest_for_hours, 0, 0, 0), #stop resting
    ]),


  (0,
   [
      (try_begin),
        (eq, "$bug_fix_version", 0),

        #fix for hiding test_scene in older savegames
        (disable_party, "p_test_scene"),
        #fix for correcting town_1 siege type
        (party_set_slot, "p_town_1", slot_center_siege_with_belfry, 0),
        #fix for hiding player_faction notes
        (faction_set_note_available, "fac_player_faction", 0),
        #fix for hiding faction 0 notes
        (faction_set_note_available, "fac_no_faction", 0),
        #fix for removing kidnapped girl from party
        (try_begin),
          (neg|check_quest_active, "qst_kidnapped_girl"),
          (party_remove_members, "p_main_party", "trp_kidnapped_girl", 1),
        (try_end),
        #fix for not occupied but belong to a faction lords
        (try_for_range, ":cur_troop", lords_begin, lords_end),
          (try_begin),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_inactive),
            (store_troop_faction, ":cur_troop_faction", ":cur_troop"),
            (is_between, ":cur_troop_faction", "fac_kingdom_1", kingdoms_end),
            (troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
          (try_end),
        (try_end),
        #fix for an error in 1.105, also fills new slot values
        (call_script, "script_initialize_item_info"),

        (assign, "$bug_fix_version", 1),
      (try_end),

      (eq,"$g_player_is_captive",1),
      (gt, "$capturer_party", 0),
      (party_is_active, "$capturer_party"),
      (party_relocate_near_party, "p_main_party", "$capturer_party", 0),
    ]),


#Auto-menu
  (0,
   [
     (try_begin),
       (gt, "$g_last_rest_center", 0),
       (party_get_battle_opponent, ":besieger_party", "$g_last_rest_center"),
       (gt, ":besieger_party", 0),
       (store_faction_of_party, ":encountered_faction", "$g_last_rest_center"),
       (store_relation, ":faction_relation", ":encountered_faction", "fac_player_supporters_faction"),
       (store_faction_of_party, ":besieger_party_faction", ":besieger_party"),
       (store_relation, ":besieger_party_relation", ":besieger_party_faction", "fac_player_supporters_faction"),
       (ge, ":faction_relation", 0),
       (lt, ":besieger_party_relation", 0),
       (start_encounter, "$g_last_rest_center"),
       (rest_for_hours, 0, 0, 0), #stop resting
     (else_try),
       (store_current_hours, ":cur_hours"),
       (assign, ":check", 0),
       (try_begin),
         (neq, "$g_check_autos_at_hour", 0),
         (ge, ":cur_hours", "$g_check_autos_at_hour"),
         (assign, ":check", 1),
         (assign, "$g_check_autos_at_hour", 0),
       (try_end),
       (this_or_next|eq, ":check", 1),
       (map_free),
       (try_begin),
         (ge,"$auto_menu",1),
         (jump_to_menu,"$auto_menu"),
         (assign,"$auto_menu",-1),
       (else_try),
         (ge,"$auto_enter_town",1),
         (start_encounter, "$auto_enter_town"),
       ##Floris - to allow player to access inventory during siege, or to entrench during siege ; other part of code in Floris version trigger    
	  # (else_try),
         # (ge,"$auto_besiege_town",1),
         # (start_encounter, "$auto_besiege_town"),
	  ##Floris - end
	#occc start
       (else_try),
         (ge,"$g_camp_mode", 1),
         (assign, "$g_camp_mode", 0),
         (assign, "$g_infinite_camping", 0),
		 (try_begin),						#Floris Seafaring Addendum // Failsafe
			(party_get_current_terrain, ":terrain", "p_main_party"),
			(gt, ":terrain", 0),
			(assign, "$g_player_icon_state", pis_normal),		
         (else_try),
			(party_get_current_terrain, ":terrain", "p_main_party"),
			(eq, ":terrain", 0),
			(assign, "$g_player_icon_state", pis_ship),	 
			(party_set_flags, "p_main_party", pf_is_ship, 1),
		 (try_end),
	#occc end
         (rest_for_hours, 0, 0, 0), #stop camping
		 #(party_set_slot,"p_main_party",slot_party_entrenched,0),#TEMPERED ADDED LINE FOR CAMP ENTRENCHMENT

         (display_message, "@Breaking camp..."),
       (try_end),
     (try_end),
     ]),


#Notification menus
  (0,
   [
     (troop_slot_ge, "trp_notification_menu_types", 0, 1),
     (troop_get_slot, ":menu_type", "trp_notification_menu_types", 0),
     (troop_get_slot, "$g_notification_menu_var1", "trp_notification_menu_var1", 0),
     (troop_get_slot, "$g_notification_menu_var2", "trp_notification_menu_var2", 0),
     (jump_to_menu, ":menu_type"),
     (assign, ":end_cond", 2),
     (try_for_range, ":cur_slot", 1, ":end_cond"),
       (try_begin),
         (troop_slot_ge, "trp_notification_menu_types", ":cur_slot", 1),
         (val_add, ":end_cond", 1),
       (try_end),
       (store_sub, ":cur_slot_minus_one", ":cur_slot", 1),
       (troop_get_slot, ":local_temp", "trp_notification_menu_types", ":cur_slot"),
       (troop_set_slot, "trp_notification_menu_types", ":cur_slot_minus_one", ":local_temp"),
       (troop_get_slot, ":local_temp", "trp_notification_menu_var1", ":cur_slot"),
       (troop_set_slot, "trp_notification_menu_var1", ":cur_slot_minus_one", ":local_temp"),
       (troop_get_slot, ":local_temp", "trp_notification_menu_var2", ":cur_slot"),
       (troop_set_slot, "trp_notification_menu_var2", ":cur_slot_minus_one", ":local_temp"),
     (try_end),
    ]),

  #Music,
  (1,
   [
       (map_free),
       (call_script, "script_music_set_situation_with_culture", mtf_sit_travel),
	    ]),

  (0,
	[
	  #escort caravan quest auto dialog trigger
	  (try_begin),
        (eq, "$caravan_escort_state", 1),
        (party_is_active, "$caravan_escort_party_id"),

        (store_distance_to_party_from_party, ":caravan_distance_to_destination","$caravan_escort_destination_town","$caravan_escort_party_id"),
        (lt, ":caravan_distance_to_destination", 2),

        (store_distance_to_party_from_party, ":caravan_distance_to_player","p_main_party","$caravan_escort_party_id"),
        (lt, ":caravan_distance_to_player", 5),

        (assign, "$talk_context", tc_party_encounter),
        (assign, "$g_encountered_party", "$caravan_escort_party_id"),
        (party_stack_get_troop_id, ":caravan_leader", "$caravan_escort_party_id", 0),
        (party_stack_get_troop_dna, ":caravan_leader_dna", "$caravan_escort_party_id", 0),

        (start_map_conversation, ":caravan_leader", ":caravan_leader_dna"),
      (try_end),

      (try_begin),
        (gt, "$g_reset_mission_participation", 1),

        (try_for_range, ":troop", active_npcs_begin, kingdom_ladies_end),
          (troop_set_slot, ":troop", slot_troop_mission_participation, 0),
        (try_end),
      (try_end),
	]),

(24,
[
    (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end), ## NMC
      (faction_get_slot, ":faction_morale", ":kingdom_no",  slot_faction_morale_of_player_troops),

	  (store_sub, ":divisor", 140, "$player_right_to_rule"),
	  (val_div, ":divisor", 14),
	  (val_max, ":divisor", 1),

      (store_div, ":faction_morale_div_10", ":faction_morale", ":divisor"), #10 is the base, down to 2 for 100 rtr
      (val_sub, ":faction_morale", ":faction_morale_div_10"),
      
      #CC-C begin faction morale
      (try_begin),
        (lt,":faction_morale",-30),
        (val_add,":faction_morale",30),
      (try_end),
      #CC-C end

      (faction_set_slot, ":kingdom_no",  slot_faction_morale_of_player_troops, ":faction_morale"),
    (try_end),
]),


 (4, #Locate kingdom ladies
    [
      #change location for all ladies
      (try_for_range, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
        ##diplomacy start+ do not set the troop's center when the troop is leading a party
        (troop_slot_eq, ":troop_id", slot_troop_occupation, slto_kingdom_lady),
        (troop_get_slot, ":leaded_party", ":troop_id", slot_troop_leaded_party),
		(try_begin),
			(gt, ":leaded_party", 0),
			(neg|party_is_active, ":leaded_party"),
			(assign, ":leaded_party", -1),
		(try_end),
        (lt, ":leaded_party", 1),#if the value is 0, it's a bug, so overlook it
        ##diplomacy end+
        (neg|troop_slot_ge, ":troop_id", slot_troop_prisoner_of_party, 0),
        (call_script, "script_get_kingdom_lady_social_determinants", ":troop_id"),
        (assign, ":location", reg1),
        (troop_set_slot, ":troop_id", slot_troop_cur_center, ":location"),
      (try_end),
	]),


 (2, #Error check for multiple parties on the map
	[
	(eq, "$cheat_mode", 1),
	(assign, ":debug_menu_noted", 0),
	(try_for_parties, ":party_no"),
		(gt, ":party_no", "p_spawn_points_end"),
		(party_stack_get_troop_id, ":commander", ":party_no", 0),
		##diplomacy start+
		(is_between, ":commander", heroes_begin, heroes_end),
		(this_or_next|troop_slot_eq, ":commander", slot_troop_occupation, slto_kingdom_hero),
		##diplomacy end+
		(is_between, ":commander", active_npcs_begin, active_npcs_end),
		(troop_get_slot, ":commander_party", ":commander", slot_troop_leaded_party),
		(neq, ":party_no", ":commander_party"),
		(assign, reg4, ":party_no"),
		(assign, reg5, ":commander_party"),

		(str_store_troop_name, s3, ":commander"),
		(display_message, "@{!}{s3} commander of party #{reg4} which is not his troop_leaded party {reg5}"),
		##diplomacy start+ Make it clear what the error was
		(try_begin),
			(gt, reg4, 0),
			(gt, reg5, 0),
			(str_store_party_name, s3, reg4),
			(str_store_party_name, s65, reg5),
			(display_message, "@{!} Commanded party #{reg4} is {s3}, troop_leaded party #{reg5} is {s65}"),
			(str_store_troop_name, s3, ":commander"),
		(try_end),
		##diplomacy end+
		(str_store_string, s65, "str_party_with_commander_mismatch__check_log_for_details_"),

		(try_begin),
			(eq, ":debug_menu_noted", 0),
			(call_script, "script_add_notification_menu", "mnu_debug_alert_from_s65", 0, 0),
			(assign, ":debug_menu_noted", 1),
		(try_end),
	(try_end),
	]),


 (24, #Kingdom ladies send messages
 [
	(try_begin),
		(neg|check_quest_active, "qst_visit_lady"),
		(neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 1),
		(neg|troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),

		(assign, ":lady_not_visited_longest_time", -1),
		(assign, ":longest_time_without_visit", 120), #five days

		(try_for_range, ":troop_id", kingdom_ladies_begin, kingdom_ladies_end),
            ##diplomacy start not dead, exiled, etc.
			(neg|troop_slot_ge, ":troop_id", slot_troop_occupation, slto_retirement),
            #not already betrothed
            (neg|troop_slot_eq, "trp_player", slot_troop_betrothed, ":troop_id"),
			##diplomacy end
			#set up message for ladies the player is courting
			(troop_slot_ge, ":troop_id", slot_troop_met, 2),
			(neg|troop_slot_eq, ":troop_id", slot_troop_met, 4),

			(troop_slot_eq, ":troop_id", slot_lady_no_messages, 0),
			(troop_slot_eq, ":troop_id", slot_troop_spouse, -1),

			(troop_get_slot, ":location", ":troop_id", slot_troop_cur_center),
			(is_between, ":location", walled_centers_begin, walled_centers_end),
			(call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_id"),
			(gt, reg0, 1),

			(store_current_hours, ":hours_since_last_visit"),
			(troop_get_slot, ":last_visit_hour", ":troop_id", slot_troop_last_talk_time),
			(val_sub, ":hours_since_last_visit", ":last_visit_hour"),

			(gt, ":hours_since_last_visit", ":longest_time_without_visit"),
			(assign, ":longest_time_without_visit", ":hours_since_last_visit"),
			(assign, ":lady_not_visited_longest_time", ":troop_id"),
			(assign, ":visit_lady_location", ":location"),

		(try_end),

		(try_begin),
			(gt, ":lady_not_visited_longest_time", 0),
			(call_script, "script_add_notification_menu", "mnu_notification_lady_requests_visit", ":lady_not_visited_longest_time", ":visit_lady_location"),
		(try_end),

	(try_end),
	]),

	#TEMPERED       chief  #########################  CHECK FOR ENTRENCHMENT FINISHED  ##############################

  (0, [	(party_get_slot,":entrenched","p_main_party",slot_party_entrenched),
		(eq,"$g_camp_mode", 1),
		(eq,":entrenched",-1),
		(store_current_hours,":cur_hour"),
		(try_begin),
			(ge,":cur_hour","$entrench_time"),
			(set_spawn_radius,0),
			(spawn_around_party,"p_main_party","pt_entrench"),
			(assign,"$current_camp_party",reg0),
			(party_set_slot,"$current_camp_party",slot_village_state,1),
			(party_set_slot,"$current_camp_party",slot_party_type,spt_entrenchment),
			(party_set_slot,"p_main_party",slot_party_entrenched,1),
			(display_message,"@_Camp defenses have been completed."),
			(assign,"$entrench_time",0),
			(jump_to_menu,"mnu_camp"),
		(try_end),
       ]),	   

#TEMPERED                    ##########################           CHECK FOR NO LONGER ENTRENCHED    ##########################

  (0, [ (eq,"$g_player_icon_state",pis_normal),
		(eq, "$g_camp_mode", 0),#not camping
		(try_begin),
			(party_slot_eq,"p_main_party",slot_party_entrenched,1), #entrenched			
			(party_set_slot,"p_main_party",slot_party_entrenched,0), #not entrenched
			#(try_begin),
				#(party_slot_eq,"$current_camp_party",slot_village_state,1),#Tempered check to see if player just left entrenchment
				(party_set_slot,"$current_camp_party",slot_village_state,2),
				(store_current_hours,":cur_hour"),
				(val_add,":cur_hour",48),
				(party_set_slot,"$current_camp_party",slot_village_smoke_added,":cur_hour"),
				(party_add_particle_system, "$current_camp_party", "psys_map_village_fire_smoke"),
			#(try_end),
		(else_try),
			(party_slot_eq,"p_main_party",slot_party_entrenched,-1), #working on entrenchment
			(party_set_slot,"p_main_party",slot_party_entrenched,0), #not entrenched
		(try_end),	
		(assign,"$current_camp_party",-1),
       ]),
#TEMPERED                    ##########################         Deteriorate abandoned entrenchments    ##########################

  (3, [ (try_for_parties,":current_party"),
			(party_slot_eq,":current_party",slot_party_type,spt_entrenchment),
			(party_slot_eq,":current_party",slot_village_state,2),
			(party_get_slot,":end_hour",":current_party",slot_village_smoke_added),
			(store_current_hours,":cur_hour"),
			(gt,":cur_hour",":end_hour"),
			(party_clear_particle_systems, ":current_party"),
			(remove_party,":current_party"),
		(try_end),
		#(party_set_flags, ":new_camp", pf_icon_mask, 1),
       ]),   



#Player raiding a village
# This trigger will check if player's raid has been completed and will lead control to village menu.
  (1,
   [
      (ge,"$g_player_raiding_village",1),
      (try_begin),
        (neq, "$g_player_is_captive", 0),
        #(rest_for_hours, 0, 0, 0), #stop resting - abort
        (assign,"$g_player_raiding_village",0),
	 ##Floris - comment out to allow player to cancel ; other part of code in Floris version trigger
      # (else_try),
        # (map_free), #we have been attacked during raid
        # (assign,"$g_player_raiding_village",0),
	 ##Floris - end
      (else_try),
        (this_or_next|party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_looted),
        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_deserted),
        (start_encounter, "$g_player_raiding_village"),
        (rest_for_hours, 0),
        (assign,"$g_player_raiding_village",0),
        (assign,"$g_player_raid_complete",1),
      (else_try),
        (party_slot_eq, "$g_player_raiding_village", slot_village_state, svs_being_raided),
        (rest_for_hours_interactive, 3, 5, 1), ##Floris - change to interactive to allow player to cancel; #rest while attackable
      (else_try),
        (rest_for_hours, 0, 0, 0), #stop resting - abort
        (assign,"$g_player_raiding_village",0),
        (assign,"$g_player_raid_complete",0),
      (try_end),
    ]),


  # Oath fulfilled -- ie, mercenary contract expired?
  (24,
   [
      (le, "$auto_menu", 0),
      (gt, "$players_kingdom", 0),
      (neq, "$players_kingdom", "fac_player_supporters_faction"),
      (eq, "$player_has_homage", 0),

	  (troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),

	  #A player bound to a kingdom by marriage will not have the contract expire. This should no longer be the case, as I've counted wives as having homage, but is in here as a fallback
	  (assign, ":player_has_marriage_in_faction", 0),
	  (try_begin),
		(is_between, ":player_spouse", active_npcs_begin, active_npcs_end),
		(store_faction_of_troop, ":spouse_faction", ":player_spouse"),
		(eq, ":spouse_faction", "$players_kingdom"),
	    (assign, ":player_has_marriage_in_faction", 1),
	  (try_end),
	  (eq, ":player_has_marriage_in_faction", 0),

      (store_current_day, ":cur_day"),
      (gt, ":cur_day", "$mercenary_service_next_renew_day"),
      (jump_to_menu, "mnu_oath_fulfilled"),
    ]),

  # Reducing luck by 1 in every 180 hours
  (180,
   [
     (val_sub, "$g_player_luck", 1),
     (val_max, "$g_player_luck", 0),
    ]),

	#courtship reset
  (72,
   [
     (assign, "$lady_flirtation_location", 0),
    ]),

	#reset time to spare
  (4,
   [
     (assign, "$g_time_to_spare", 1),

    (try_begin),
		(troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
		(assign, "$g_player_banner_granted", 1),
	(try_end),

	 ]),


  # Banner selection menu
  (24,
   [
    (eq, "$g_player_banner_granted", 1),
    (troop_slot_eq, "trp_player", slot_troop_banner_scene_prop, 0),
    (le,"$auto_menu",0),
#normal_banner_begin
    (start_presentation, "prsnt_banner_selection"),
#custom_banner_begin
#    (start_presentation, "prsnt_custom_banner"),
    ]),

  # Party Morale: Move morale towards target value.
  (24,
   [
      (call_script, "script_get_player_party_morale_values"),
      (assign, ":target_morale", reg0),
      (party_get_morale, ":cur_morale", "p_main_party"),
      (store_sub, ":dif", ":target_morale", ":cur_morale"),
      (store_div, ":dif_to_add", ":dif", 5),
      (store_mul, ":dif_to_add_correction", ":dif_to_add", 5),
      (try_begin),#finding ceiling of the value
        (neq, ":dif_to_add_correction", ":dif"),
        (try_begin),
          (gt, ":dif", 0),
          (val_add, ":dif_to_add", 1),
        (else_try),
          (val_sub, ":dif_to_add", 1),
        (try_end),
      (try_end),
      (val_add, ":cur_morale", ":dif_to_add"),
      (party_set_morale, "p_main_party", ":cur_morale"),
    ]),


#Party AI: pruning some of the prisoners in each center (once a week)
  (24*7,
   [
       (try_for_range, ":center_no", centers_begin, centers_end),
         (party_get_num_prisoner_stacks, ":num_prisoner_stacks",":center_no"),
         (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
           (party_prisoner_stack_get_troop_id, ":stack_troop",":center_no",":stack_no"),
           (neg|troop_is_hero, ":stack_troop"),
           (party_prisoner_stack_get_size, ":stack_size",":center_no",":stack_no"),
           (store_random_in_range, ":rand_no", 0, 40),
           (val_mul, ":stack_size", ":rand_no"),
           (val_div, ":stack_size", 100),
           (val_max, ":stack_size", 1), ## CC
           (party_remove_prisoners, ":center_no", ":stack_troop", ":stack_size"),
		   ##diplomacy start+ add prisoner value to center wealth
		   (try_begin),
		      (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_HIGH),#must be explicitly enabled
			  (ge, ":center_no", 1),
			  (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
				(party_slot_eq, ":center_no", slot_party_type, spt_castle),
			  (party_slot_ge, ":center_no", slot_town_lord, 1),#"wealth" isn't used for player garrisons
			  (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
			  (lt, ":cur_wealth", 6000),
			  (store_mul, ":ransom_profits", ":stack_size", 10),#a fraction of what it could be sold for (50 would be a rule of thumb)
			  (val_add, ":cur_wealth", ":ransom_profits"),
			  (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
		   (try_end),
		   ##diplomacy end+
         (try_end),
       (try_end),
    ]),

##CC-C begin
  #Adding net incomes to heroes (once a week)
  #Increasing debts to heroes by 1% (once a week)
  #Adding net incomes to centers (once a week)
#  (24*7,
#   [
		##diplomacy start+ Save register
#		(assign, ":save_reg0", reg0),
		##Change to support kingdom ladies
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
#	   (try_for_range, ":troop_no", heroes_begin, heroes_end),
#	     (this_or_next|is_between, ":troop_no", active_npcs_begin, active_npcs_end),
#		 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	   ##diplomacy end+
#         (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),#Increasing debt
#         (val_mul, ":cur_debt", 101),
#         (val_div, ":cur_debt", 100),
#         (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
#         (call_script, "script_calculate_hero_weekly_net_income_and_add_to_wealth", ":troop_no"),#Adding net income
#       (try_end),

	   ##diplomacy start+
#	   (store_current_hours, ":two_weeks_ago"),
#	   (val_sub, ":two_weeks_ago", 24 * 14),
	   ##diplomacy end+

#       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         #If non-player center, adding income to wealth
#         (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
		 ##diplomacy start+
		 #Defer the ownership check so attrition can still occur for unowned centers.
		 #Give a slight grace period first, though.
#		 (neg|party_slot_eq, ":center_no", slot_town_lord, 0),
#		 (this_or_next|party_slot_ge, ":center_no", dplmc_slot_center_last_transfer_time, ":two_weeks_ago"),
#			(party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
#		 (this_or_next|ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
		 ##diplomacy end+
#		 (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
#         (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
#         (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
#         (store_mul, ":added_wealth", ":prosperity", 15),
#         (val_add, ":added_wealth", 700),
#         (try_begin),
#           (party_slot_eq, ":center_no", slot_party_type, spt_town),
#           (val_mul, ":added_wealth", 3),
#           (val_div, ":added_wealth", 2),
#         (try_end),
#         (val_add, ":cur_wealth", ":added_wealth"),
#         (call_script, "script_calculate_weekly_party_wage", ":center_no"),
         ## CC half wage
#         (assign, ":cur_weekly_wage", reg0),
#         (val_div, ":cur_weekly_wage", 2),
         ## CC half wage
#         (val_sub, ":cur_wealth", reg0),
		 ##diplomacy start+ Allow attrition to occur
#		 (try_begin),
#			(lt, ":cur_wealth", 0),
#			(ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_MEDIUM),
#			(assign, ":cur_weekly_wage", reg0),
#			(store_party_size_wo_prisoners, ":garrison_size", ":center_no"),
#			(call_script, "script_party_get_ideal_size", ":center_no"),#This script has been modified to support this use
#			(val_mul, reg0, 5),
#			(val_div, reg0, 4),
#			(ge, ":garrison_size", reg0),

#			(store_sub, ":percent_under", 0, ":cur_wealth"),
#			(val_mul, ":percent_under", 100),
#			(val_div, ":percent_under", ":cur_weekly_wage"),
#			(val_div, ":percent_under", 5), #Max 20 percent (won't take garrison below ideal size)
#			(call_script, "script_party_inflict_attrition", ":center_no", ":percent_under", 1),
#		 (try_end),
#		 (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
		 ##diplomacy end+
#         (val_max, ":cur_wealth", 0),
#         (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
#       (try_end),
	   ##diplomacy end+
#	   (assign, reg0, ":save_reg0"),
	   ##diplomacy end+
#    ]),

  #Hiring men with hero wealths (once a day)
  #Hiring men with center wealths (once a day)
#  (24,
#   [
     ##diplomacy start+
     ##change to allow promoted kingdom ladies to hire troops
     #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
#     (try_for_range, ":troop_no", active_npcs_begin, kingdom_ladies_end),
     ##diplomacy end+
#       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
#       (ge, ":party_no", 1),
#       (party_is_active, ":party_no"),
#       (party_get_attached_to, ":cur_attached_party", ":party_no"),
#       (is_between, ":cur_attached_party", centers_begin, centers_end),
#       (party_slot_eq, ":cur_attached_party", slot_center_is_besieged_by, -1), #center not under siege

#       (store_faction_of_party, ":party_faction", ":party_no"),
#       (try_begin),
#         (this_or_next|eq, ":party_faction", "fac_player_supporters_faction"),
#         (eq, ":party_faction", "$players_kingdom"),
#         (assign, ":num_hiring_rounds", 1),
#         (store_random_in_range, ":random_value", 0, 2),
#         (val_add, ":num_hiring_rounds", ":random_value"),
#       (else_try),
#         (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
#         (try_begin),
#           (eq, ":reduce_campaign_ai", 0), #hard (2x reinforcing)
#           (assign, ":num_hiring_rounds", 2),
#         (else_try),
#           (eq, ":reduce_campaign_ai", 1), #medium (1x or 2x reinforcing)
#           (assign, ":num_hiring_rounds", 1),
#           (store_random_in_range, ":random_value", 0, 2),
#           (val_add, ":num_hiring_rounds", ":random_value"),
#         (else_try),
#           (eq, ":reduce_campaign_ai", 2), #easy (1x reinforcing)
#           (assign, ":num_hiring_rounds", 1),
#         (try_end),
#       (try_end),

#       (try_begin),
#         (this_or_next|faction_slot_eq,  ":party_faction", slot_faction_leader, ":troop_no"), ## CC
#         (faction_slot_eq,  ":party_faction", slot_faction_marshall, ":troop_no"),
#         (val_add, ":num_hiring_rounds", 1),
#       (try_end),

       ## CC begin
#       (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
#       (store_div, ":num_rounds", ":cur_wealth", 10000),
#       (val_add, ":num_rounds", 1),
       
#       (assign, ":center_score", 0),
#       (store_troop_faction, ":troop_faction", ":troop_no"),
#       (try_for_range, ":cur_center", centers_begin, centers_end),
#         (store_faction_of_party, ":town_faction", ":cur_center"),
#         (eq, ":town_faction", ":troop_faction"),
#         (try_begin),
#           (party_slot_eq, ":cur_center", slot_party_type, spt_village),
#           (val_add, ":center_score", 1),
#         (else_try),
#           (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
#           (val_add, ":center_score", 2),
#         (else_try),
#           (party_slot_eq, ":cur_center", slot_party_type, spt_town),
#           (val_add, ":center_score", 4),
#         (try_end),
#       (try_end),
#       (val_max, ":center_score", 1),
#       (store_div, ":rounds_multi", 9, ":center_score"),
#       (val_add, ":rounds_multi", 1),
#       (val_mul, ":num_rounds", ":rounds_multi"),
#       (val_add, ":num_hiring_rounds", ":num_rounds"),
       # town bonus: *1.5
#       (try_begin),
#         (party_slot_eq, ":cur_attached_party", slot_party_type, spt_town),
#         (val_mul, ":num_hiring_rounds", 3),
#         (val_add, ":num_hiring_rounds", 1),
#         (val_div, ":num_hiring_rounds", 2),
#       (try_end),
       # town bonus
#       (val_min, ":num_hiring_rounds", 8),
       ## CC end

#       (try_for_range, ":unused", 0, ":num_hiring_rounds"),
         ## CC wealth/extra wage > 4
#         (assign, ":cur_weekly_wage", 0),
#         (try_begin),
#           (gt, ":party_no",0),
#           (call_script, "script_calculate_weekly_party_wage", ":party_no"),
#           (assign, ":cur_weekly_wage", reg0),
#         (try_end),
#         (call_script, "script_get_lord_weekly_income", ":troop_no"),
#         (assign, ":weekly_income", reg0),
#         (val_sub, ":cur_weekly_wage", ":weekly_income"),
#         (val_mul, ":cur_weekly_wage", 4),
#         (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
#         (lt, ":cur_weekly_wage", ":cur_wealth"),
         ## CC
#         (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"), #Hiring men with current wealth
#       (try_end),
#     (try_end),

#     (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
#       (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
#       (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.
#       (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege

#       (store_faction_of_party, ":center_faction", ":center_no"),
#       (try_begin),
#         (this_or_next|eq, ":center_faction", "fac_player_supporters_faction"),
#         (eq, ":center_faction", "$players_kingdom"),
#         (assign, ":num_hiring_rounds", 1), ## CC
#         (assign, ":reinforcement_cost", reinforcement_cost_moderate),
#       (else_try),
#         (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
#         (assign, ":reinforcement_cost", reinforcement_cost_moderate),
#         (try_begin),
#           (eq, ":reduce_campaign_ai", 0), #hard (1x or 2x reinforcing)
#           (assign, ":reinforcement_cost", reinforcement_cost_hard),
#           (store_random_in_range, ":num_hiring_rounds", 0, 2),
#           (val_add, ":num_hiring_rounds", 1),
#         (else_try),
#           (eq, ":reduce_campaign_ai", 1), #moderate (1x reinforcing)
#           (assign, ":reinforcement_cost", reinforcement_cost_moderate),
#           (assign, ":num_hiring_rounds", 1),
#         (else_try),
#           (eq, ":reduce_campaign_ai", 2), #easy (none or 1x reinforcing)
#           (assign, ":reinforcement_cost", reinforcement_cost_easy),
#           (store_random_in_range, ":num_hiring_rounds", 0, 2),
#         (try_end),
#       (try_end),
       ## CC begin
#       (try_begin),
#         (is_between, ":center_no", towns_begin, towns_end),
#         (val_add, ":num_hiring_rounds", 1),
#       (try_end),
       ## CC end
#       (try_for_range, ":unused", 0, ":num_hiring_rounds"),
#         (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
#         (assign, ":hiring_budget", ":cur_wealth"),
#         (val_div, ":hiring_budget", 2),
#         (gt, ":hiring_budget", ":reinforcement_cost"),
#         (call_script, "script_cf_reinforce_party", ":center_no"),
#         (val_sub, ":cur_wealth", ":reinforcement_cost"),
#         (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
#       (try_end),
#     (try_end),

     #this is moved up from below , from a 24 x 15 slot to a 24 slot
#     (try_for_range, ":center_no", centers_begin, centers_end),
       #(neg|is_between, ":center_no", castles_begin, castles_end),
#       (store_random_in_range, ":random", 0, 30),
#       (le, ":random", 10),
	   
#       (call_script, "script_get_center_ideal_prosperity", ":center_no"),
#       (assign, ":ideal_prosperity", reg0),
#       (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
#       (try_begin),
#	     (eq, ":random", 0), #with 3% probability it will gain +10/-10 prosperity even it has higher prosperity than its ideal prosperity.
#         (try_begin),
#           (store_random_in_range, ":random", 0, 2),
#           (try_begin),
#             (eq, ":random", 0),
#             (neg|is_between, ":center_no", castles_begin, castles_end), #castles always gain positive prosperity from surprise income to balance their prosperity.
#             (call_script, "script_change_center_prosperity", ":center_no", -10),
#             (val_add, "$newglob_total_prosperity_from_convergence", -10),
#           (else_try),     
#             (call_script, "script_change_center_prosperity", ":center_no", 10),
#             (val_add, "$newglob_total_prosperity_from_convergence", 10),
#           (try_end),
#         (try_end),
#	   (else_try),
#         (gt, ":prosperity", ":ideal_prosperity"),
#         (call_script, "script_change_center_prosperity", ":center_no", -1),
#         (val_add, "$newglob_total_prosperity_from_convergence", -1),
#       (else_try),
#         (lt, ":prosperity", ":ideal_prosperity"),
#         (call_script, "script_change_center_prosperity", ":center_no", 1),
#         (val_add, "$newglob_total_prosperity_from_convergence", 1),
#       (try_end),
#     (try_end),
#    ]),

  #Converging center prosperity to ideal prosperity once in every 15 days
#  (24*15,
#   []),
##CC-C end

  #Checking if the troops are resting at a half payment point
  (6,
   [(store_current_day, ":cur_day"),
    (try_begin),
      (neq, ":cur_day", "$g_last_half_payment_check_day"),
      (assign, "$g_last_half_payment_check_day", ":cur_day"),
      (try_begin),
        (eq, "$g_half_payment_checkpoint", 1),
        (val_add, "$g_cur_week_half_daily_wage_payments", 1), #half payment for yesterday
      (try_end),
      (assign, "$g_half_payment_checkpoint", 1),
    (try_end),
    (assign, ":resting_at_manor_or_walled_center", 0),
    (try_begin),
      (neg|map_free),
      (ge, "$g_last_rest_center", 0),
      (this_or_next|party_slot_eq, "$g_last_rest_center", slot_center_has_manor, 1),
      (is_between, "$g_last_rest_center", walled_centers_begin, walled_centers_end),
      (assign, ":resting_at_manor_or_walled_center", 1),
    (try_end),
    (eq, ":resting_at_manor_or_walled_center", 0),
    (assign, "$g_half_payment_checkpoint", 0),
    ]),

#diplomatic indices
  (24,
   [
   (call_script, "script_randomly_start_war_peace_new", 1),

   (try_begin),
		(store_random_in_range, ":acting_village", villages_begin, villages_end),
		(store_random_in_range, ":target_village", villages_begin, villages_end),
		(store_faction_of_party, ":acting_faction", ":acting_village"),
		(store_faction_of_party, ":target_faction", ":target_village"), #target faction receives the provocation
		(neq, ":acting_village", ":target_village"),
		(neq, ":acting_faction", ":target_faction"),

		(call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":target_faction", ":acting_faction"),
		(eq, reg0, 0),

		(try_begin),
			(party_slot_eq, ":acting_village", slot_center_original_faction, ":target_faction"),

			(call_script, "script_add_notification_menu", "mnu_notification_border_incident", ":acting_village", -1),
		(else_try),
			(party_slot_eq, ":acting_village", slot_center_ex_faction, ":target_faction"),

			(call_script, "script_add_notification_menu", "mnu_notification_border_incident", ":acting_village", -1),

		(else_try),
			(set_fixed_point_multiplier, 1),
			(store_distance_to_party_from_party, ":distance", ":acting_village", ":target_village"),
			(lt, ":distance", 25),

			(call_script, "script_add_notification_menu", "mnu_notification_border_incident", ":acting_village", ":target_village"),
		(try_end),
   (try_end),

   (try_for_range, ":faction_1", kingdoms_begin, kingdoms_end),
		(faction_slot_eq, ":faction_1", slot_faction_state, sfs_active),
		(try_for_range, ":faction_2", kingdoms_begin, kingdoms_end),
			(neq, ":faction_1", ":faction_2"),
			(faction_slot_eq, ":faction_2", slot_faction_state, sfs_active),

			#remove provocations
			(store_add, ":slot_truce_days", ":faction_2", slot_faction_truce_days_with_factions_begin),
			(val_sub, ":slot_truce_days", kingdoms_begin),
			(faction_get_slot, ":truce_days", ":faction_1", ":slot_truce_days"),
			(try_begin),
				(ge, ":truce_days", 1),
				(try_begin),
					(eq, ":truce_days", 1),
					(call_script, "script_update_faction_notes", ":faction_1"),
					(lt, ":faction_1", ":faction_2"),
					## NMCml begin: Diplomacy: Cut reports refer from TinyModPatcher
					(try_begin),
					  (eq, "$g_nmcml_cut_diplomacy_announce_screen", 0),
					  (call_script, "script_add_notification_menu", "mnu_notification_truce_expired", ":faction_1", ":faction_2"),
					(try_end),
					## NMCml end
				##diplomacy begin
		##nested diplomacy start+ Replace "magic numbers" with named constants
        (else_try),
          (eq, ":truce_days", dplmc_treaty_alliance_days_expire + 1),#replaced 61
          (call_script, "script_update_faction_notes", ":faction_1"),
          (lt, ":faction_1", ":faction_2"),
          ## NMCml begin: Diplomacy: Cut reports refer from TinyModPatcher
          (try_begin),
            (eq, "$g_nmcml_cut_diplomacy_announce_screen", 0),
            (call_script, "script_add_notification_menu", "mnu_dplmc_notification_alliance_expired", ":faction_1", ":faction_2"),
          (try_end),
          ## NMCml end
        (else_try),
          (eq, ":truce_days",dplmc_treaty_defense_days_expire + 1),#replaced 41
          (call_script, "script_update_faction_notes", ":faction_1"),
          (lt, ":faction_1", ":faction_2"),
          ## NMCml begin: Diplomacy: Cut reports refer from TinyModPatcher
          (try_begin),
            (eq, "$g_nmcml_cut_diplomacy_announce_screen", 0),
            (call_script, "script_add_notification_menu", "mnu_dplmc_notification_defensive_expired", ":faction_1", ":faction_2"),
          (try_end),
          ## NMCml end
        (else_try),
          (eq, ":truce_days", dplmc_treaty_trade_days_expire + 1),#replaced 21
          (call_script, "script_update_faction_notes", ":faction_1"),
          (lt, ":faction_1", ":faction_2"),
          ## NMCml begin: Diplomacy: Cut reports refer from TinyModPatcher
          (try_begin),
            (eq, "$g_nmcml_cut_diplomacy_announce_screen", 0),
            (call_script, "script_add_notification_menu", "mnu_dplmc_notification_trade_expired", ":faction_1", ":faction_2"),
          (try_end),
          ## NMCml end
  	    ##nested diplomacy end+
        ##diplomacy end
				(try_end),
				(val_sub, ":truce_days", 1),
				(faction_set_slot, ":faction_1", ":slot_truce_days", ":truce_days"),
			(try_end),

			(store_add, ":slot_provocation_days", ":faction_2", slot_faction_provocation_days_with_factions_begin),
			(val_sub, ":slot_provocation_days", kingdoms_begin),
			(faction_get_slot, ":provocation_days", ":faction_1", ":slot_provocation_days"),
			(try_begin),
				(ge, ":provocation_days", 1),
				(try_begin),#factions already at war
					(store_relation, ":relation", ":faction_1", ":faction_2"),
					(lt, ":relation", 0),
					(faction_set_slot, ":faction_1", ":slot_provocation_days", 0),
				(else_try), #Provocation expires
					(eq, ":provocation_days", 1),
					## NMCml begin: Diplomacy: Cut reports refer from TinyModPatcher
					(try_begin),
					  (eq, "$g_nmcml_cut_diplomacy_announce_screen", 0),
					  (call_script, "script_add_notification_menu", "mnu_notification_casus_belli_expired", ":faction_1", ":faction_2"),
					(try_end),
					## NMCml end
					(faction_set_slot, ":faction_1", ":slot_provocation_days", 0),
				(else_try),
					(val_sub, ":provocation_days", 1),
					(faction_set_slot, ":faction_1", ":slot_provocation_days", ":provocation_days"),
				(try_end),
			(try_end),

			(try_begin), #at war
				(store_relation, ":relation", ":faction_1", ":faction_2"),
				(lt, ":relation", 0),
				(store_add, ":slot_war_damage", ":faction_2", slot_faction_war_damage_inflicted_on_factions_begin),
				(val_sub, ":slot_war_damage", kingdoms_begin),
				(faction_get_slot, ":war_damage", ":faction_1", ":slot_war_damage"),
				(val_add, ":war_damage", 1),
				(faction_set_slot, ":faction_1", ":slot_war_damage", ":war_damage"),
			(try_end),

		(try_end),
		(call_script, "script_update_faction_notes", ":faction_1"),
	(try_end),
    ]),

  # Give some xp to hero parties
   (48,
   [
       ##diplomacy start+
       ##change to allow promoted kingdom ladies to hire troops
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
       (try_for_range, ":troop_no", heroes_begin, heroes_end),
       ##diplomacy end+
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

         (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
         (gt, ":hero_party", centers_end),
         (party_is_active, ":hero_party"),

         (store_skill_level, ":trainer_level", skl_trainer, ":troop_no"),
         (val_add, ":trainer_level", 5), #average trainer level is 3 for npc lords, worst : 0, best : 6
         (store_mul, ":xp_gain", ":trainer_level", 1000), #xp gain in two days of period for each lord, average : 8000.

         (assign, ":max_accepted_random_value", 30),
         (try_begin),
           (store_troop_faction, ":cur_troop_faction", ":troop_no"),
           (neq, ":cur_troop_faction", "$players_kingdom"),

           (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
           (try_begin),
             (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
             (assign, ":max_accepted_random_value", 35),
             (val_mul, ":xp_gain", 3),
             (val_div, ":xp_gain", 2),
           (else_try),
             (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
             (assign, ":max_accepted_random_value", 25),
             (val_div, ":xp_gain", 2),
           (try_end),
         (try_end),
         ## CC-D begin: castle train
         (party_get_attached_to, ":cur_center_no", ":hero_party"),
         (try_begin),
           (lt, ":cur_center_no", 0),
           (party_get_cur_town, ":cur_center_no", ":hero_party"),
         (try_end),
         (try_begin),
           (is_between, ":cur_center_no", castles_begin, castles_end),
           (party_slot_eq, ":cur_center_no", slot_town_lord, ":troop_no"),
           
           (val_add, ":max_accepted_random_value", 10),
           (val_mul, ":xp_gain", 6),
           (val_div, ":xp_gain", 5),
         (try_end),
         ## CC-D end

         (store_random_in_range, ":rand", 0, 100),
         (le, ":rand", ":max_accepted_random_value"),

         # (party_upgrade_with_xp, ":hero_party", ":xp_gain"),
         (call_script, "script_upgrade_hero_party", ":hero_party", ":xp_gain"), ## CC
       (try_end),

       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
         (neq, ":center_lord", "trp_player"),

         (assign, ":xp_gain", 3000), #xp gain in two days of period for each center, average : 3000.

         (assign, ":max_accepted_random_value", 30),
         (try_begin),
           (assign, ":cur_center_lord_faction", -1),
           (try_begin),
             (ge, ":center_lord", 0),
             (store_troop_faction, ":cur_center_lord_faction", ":center_lord"),
           (try_end),
           (neq, ":cur_center_lord_faction", "$players_kingdom"),

           (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
           (try_begin),
             (eq, ":reduce_campaign_ai", 0), #hard (1.5x)
             (assign, ":max_accepted_random_value", 35),
             (val_mul, ":xp_gain", 3),
             (val_div, ":xp_gain", 2),
           (else_try),
             (eq, ":reduce_campaign_ai", 2), #easy (0.5x)
             (assign, ":max_accepted_random_value", 25),
             (val_div, ":xp_gain", 2),
           (try_end),
         (try_end),
         ## CC-D begin: castle train
         (try_begin),
           (is_between, ":center_no", castles_begin, castles_end),
           
           (val_add, ":max_accepted_random_value", 10),
           (val_mul, ":xp_gain", 6),
           (val_div, ":xp_gain", 5),
         (try_end),
         ## CC-D end

         (store_random_in_range, ":rand", 0, 100),
         (le, ":rand", ":max_accepted_random_value"),

         (party_upgrade_with_xp, ":center_no", ":xp_gain"),
         (call_script, "script_upgrade_hero_party", ":center_no", ":xp_gain"), ## CC
       (try_end),
    ]),

  # Process sieges
   (24,
   [
       (call_script, "script_process_sieges"),
    ]),

  # Process village raids
   (2,
   [
       (call_script, "script_process_village_raids"),
    ]),


  # Decide vassal ai
   (7,
    [
      (call_script, "script_init_ai_calculation"),
      #(call_script, "script_decide_kingdom_party_ais"),
	  ##diplomacy start+
	  #Also call script_calculate_troop_ai for kingdom ladies who have become slto_kingdom_heroes
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
	  ##diplomacy end+
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (call_script, "script_calculate_troop_ai", ":troop_no"),
      (try_end),
      ]),

##CC-C begin
  # Hold regular marshall elections for players_kingdom
#   (24, #Disabled in favor of new system
#    [
    #  (val_add, "$g_election_date", 1),
    #  (ge, "$g_election_date", 90), #elections holds once in every 90 days.
    #  (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
    #  (neq, "$players_kingdom", "fac_player_supporters_faction"),
    #  (assign, "$g_presentation_input", -1),
    #  (assign, "$g_presentation_marshall_selection_1_vote", 0),
    #  (assign, "$g_presentation_marshall_selection_2_vote", 0),

    #  (assign, "$g_presentation_marshall_selection_max_renown_1", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_2", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_3", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_1_troop", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_2_troop", -10000),
    #  (assign, "$g_presentation_marshall_selection_max_renown_3_troop", -10000),
    #  (assign, ":num_men", 0),
    #  (try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", active_npcs_end),
    #    (assign, ":cur_troop", ":loop_var"),
    #    (assign, ":continue", 0),
    #    (try_begin),
    #      (eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
    #      (assign, ":cur_troop", "trp_player"),
    #      (try_begin),
    #        (eq, "$g_player_is_captive", 0),
    #        (assign, ":continue", 1),
    #      (try_end),
    #    (else_try),
#		  (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
 #         (store_troop_faction, ":cur_troop_faction", ":cur_troop"),
 #         (eq, "$players_kingdom", ":cur_troop_faction"),
  #        #(troop_slot_eq, ":cur_troop", slot_troop_is_prisoner, 0),
  #        (neg|troop_slot_ge, ":cur_troop", slot_troop_prisoner_of_party, 0),
   #       (troop_slot_ge, ":cur_troop", slot_troop_leaded_party, 1),
    #      (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
    #      (neg|faction_slot_eq, ":cur_troop_faction", slot_faction_leader, ":cur_troop"),
    #      (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
    #      (gt, ":cur_party", 0),
    #      (party_is_active, ":cur_party"),
    #      (call_script, "script_party_count_fit_for_battle", ":cur_party"),
    #      (assign, ":party_fit_for_battle", reg0),
    #      (call_script, "script_party_get_ideal_size", ":cur_party"),
    #      (assign, ":ideal_size", reg0),
    #      (store_mul, ":relative_strength", ":party_fit_for_battle", 100),
    #      (val_div, ":relative_strength", ":ideal_size"),
    #      (ge, ":relative_strength", 25),
    #      (assign, ":continue", 1),
    #    (try_end),
    #    (eq, ":continue", 1),
    #    (val_add, ":num_men", 1),
    #    (troop_get_slot, ":renown", ":cur_troop", slot_troop_renown),
    #    (try_begin),
    #      (gt, ":renown", "$g_presentation_marshall_selection_max_renown_1"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3", "$g_presentation_marshall_selection_max_renown_2"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2", "$g_presentation_marshall_selection_max_renown_1"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_1", ":renown"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3_troop", "$g_presentation_marshall_selection_max_renown_2_troop"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2_troop", "$g_presentation_marshall_selection_max_renown_1_troop"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_1_troop", ":cur_troop"),
    #    (else_try),
    #      (gt, ":renown", "$g_presentation_marshall_selection_max_renown_2"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3", "$g_presentation_marshall_selection_max_renown_2"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2", ":renown"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3_troop", "$g_presentation_marshall_selection_max_renown_2_troop"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_2_troop", ":cur_troop"),
    #    (else_try),
    #      (gt, ":renown", "$g_presentation_marshall_selection_max_renown_3"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3", ":renown"),
    #      (assign, "$g_presentation_marshall_selection_max_renown_3_troop", ":cur_troop"),
    #    (try_end),
    #  (try_end),
    #  (ge, "$g_presentation_marshall_selection_max_renown_1_troop", 0),
    #  (ge, "$g_presentation_marshall_selection_max_renown_2_troop", 0),
    #  (ge, "$g_presentation_marshall_selection_max_renown_3_troop", 0),
    #  (gt, ":num_men", 2), #at least 1 voter
    #  (assign, "$g_election_date", 0),
    #  (assign, "$g_presentation_marshall_selection_ended", 0),
    #  (try_begin),
    #    (neq, "$g_presentation_marshall_selection_max_renown_1_troop", "trp_player"),
    #    (neq, "$g_presentation_marshall_selection_max_renown_2_troop", "trp_player"),
    #    (start_presentation, "prsnt_marshall_selection"),
    #  (else_try),
    #    (jump_to_menu, "mnu_marshall_selection_candidate_ask"),
    #  (try_end),
#      ]),#
##CC-C end

   (24,
    [
	##diplomacy start+ Add support for promoted kingdom ladies
	##OLD:
	#(try_for_range, ":kingdom_hero", active_npcs_begin, active_npcs_end),
	##NEW:
	(try_for_range, ":kingdom_hero", heroes_begin, heroes_end),
		(this_or_next|is_between, ":kingdom_hero", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":kingdom_hero", slot_troop_occupation, slto_kingdom_hero),
	##diplomacy end+
		(troop_get_slot, ":impatience", ":kingdom_hero", slot_troop_intrigue_impatience),
		(val_sub, ":impatience", 5),
		(val_max, ":impatience", 0),
		(troop_set_slot, ":kingdom_hero", slot_troop_intrigue_impatience, ":impatience"),
	(try_end),

	(store_random_in_range, ":controversy_deduction", 1, 3),
	(val_min, ":controversy_deduction", 2),
#	(assign, ":controversy_deduction", 1),

	#This reduces controversy by one each round
	##diplomacy start+ Add support for promoted kingdom ladies
	##OLD:
	#(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	##NEW:
	(try_for_range, ":active_npc", heroes_begin, heroes_end),
		(this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
		(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	##diplomacy end+
		(troop_get_slot, ":controversy", ":active_npc", slot_troop_controversy),
		(ge, ":controversy", 1),
		(val_sub, ":controversy", ":controversy_deduction"),
		(val_max, ":controversy", 0),
		(troop_set_slot, ":active_npc", slot_troop_controversy, ":controversy"),
	(try_end),

	(troop_get_slot, ":controversy", "trp_player", slot_troop_controversy),
	(val_sub, ":controversy", ":controversy_deduction"),
	(val_max, ":controversy", 0),
	(troop_set_slot, "trp_player", slot_troop_controversy, ":controversy"),

	]),

    #POLITICAL TRIGGERS
	#POLITICAL TRIGGER #1`
   (8, #increased from 12
    [
	(call_script, "script_cf_random_political_event"),

	#Added Nov 2010 begins - do this twice
	(call_script, "script_cf_random_political_event"),
	#Added Nov 2010 ends

	#This generates quarrels and occasional reconciliations and interventions
	]),

	#Individual lord political calculations
	#Check for lords without fiefs, auto-defections, etc
   (0.5,
    [
	##diplomacy start+
	#This is fairly complicated, and it was getting nearly unreadable so I reformatted it.
	#The old version is visible in version control.
	(assign, ":save_reg0", reg0),
	(val_add, "$g_lord_long_term_count", 1),
	(try_begin),
		(neg|is_between, "$g_lord_long_term_count", active_npcs_including_player_begin, active_npcs_end),
		(assign, "$g_lord_long_term_count", active_npcs_including_player_begin),
	(try_end),

	##Add political calculations for kingdom ladies.  Just extending the range would
	##slow down the political calculations cycle, which would have possibly-unforeseen results.
	##Instead, add a second iteration to deal with extensions.
	(try_for_range, ":iteration", 0, 2),
		(assign, ":troop_no", "$g_lord_long_term_count"),
		(try_begin),
			(eq, ":iteration", 1),
			(val_sub, ":troop_no", active_npcs_including_player_begin),
			(val_add, ":troop_no", active_npcs_end),
		(try_end),
		#Crude check to make sure that a careless modder (i.e. me) didn't decide it
		#would be a good idea to redefine active_npcs to include kingdom_ladies,
		#which would make the second iteration run off the end of the heroes list.
		(is_between, ":troop_no", active_npcs_including_player_begin, heroes_end),

		#Special handling for trp_player, and get the troop's faction
		(try_begin),
			(eq, ":troop_no", "trp_kingdom_heroes_including_player_begin"),
			(assign, ":troop_no", "trp_player"),
			(assign, ":faction", "$players_kingdom"),
		(else_try),
			(store_faction_of_troop, ":faction", ":troop_no"),
		(try_end),

		(try_begin),
			(eq, "$cheat_mode", 1),
			(str_store_troop_name, s9, ":troop_no"),
			(display_message, "@{!}DEBUG -- Doing political calculations for {s9}"),
		(try_end),

        #Tally the fiefs owned by the hero, and cache the value in slot.
		#If a lord owns no fiefs, his relations with his liege may deteriorate.
        (try_begin),
			(assign, reg0, 1),#Center points + 1
			(try_for_range, ":center", centers_begin, centers_end),
				(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
				(try_begin),
					(is_between, ":center", towns_begin, towns_end),
					(val_add, reg0, 3),#3 points per town
				(else_try),
					(is_between, ":center", walled_centers_begin, walled_centers_end),
					(val_add, reg0, 2),#2 points per castle
				(else_try),
					(val_add, reg0, 1),#1 point per village
				(try_end),
			(try_end),
			#Update cached total
			(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
			#If a lord has no fiefs, relation loss potentially results.
			#Do not apply this to the player.
			(eq, reg0, 1),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(neq, ":troop_no", "trp_player"),

			#Don't apply this to the leader
			(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
			(gt, ":faction_leader", -1),
			(neq, ":faction_leader", ":troop_no"),
			(neg|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),
			(neg|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),

			(troop_get_slot, ":troop_reputation", ":troop_no", slot_lord_reputation_type),
			(try_begin),
				(this_or_next|eq, ":troop_reputation", lrep_quarrelsome),
				(this_or_next|eq, ":troop_reputation", lrep_selfrighteous),
				(this_or_next|eq, ":troop_reputation", lrep_cunning),
				(eq, ":troop_reputation", lrep_debauched),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_leader", -4),
				(val_add, "$total_no_fief_changes", -4),
			(else_try),
				(this_or_next|eq, ":troop_reputation", lrep_ambitious),#add support for lady personalities
				(eq, ":troop_reputation", lrep_martial),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":faction_leader", -2),
				(val_add, "$total_no_fief_changes", -2),
			(try_end),
        (try_end),

        #Auto-indictment or defection
        (try_begin),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(eq, ":troop_no", "trp_player"),

			#There must be a valid faction leader.  The faction leader won't defect from his own kingdom.
			#To avoid certain potential complications, also skip the defection/indictment check for the
			#spouse of the faction leader.  (Code to make that possible can be added elsewhere if
			#necessary.)
			(faction_get_slot, ":faction_leader", ":faction", slot_faction_leader),
			(gt, ":faction_leader", -1),
			(neq, ":troop_no", ":faction_leader"),
			(neg|troop_slot_eq, ":troop_no", slot_troop_spouse, ":faction_leader"),
			(neg|troop_slot_eq, ":faction_leader", slot_troop_spouse, ":troop_no"),

          #I don't know why these are necessary, but they appear to be
			(neg|is_between, ":troop_no", "trp_kingdom_1_lord", "trp_knight_1_1"),
			(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),

		  (assign, ":num_centers", 0),		  
		  (try_for_range,":cur_center", walled_centers_begin, walled_centers_end),		    
		    (store_faction_of_party, ":faction_of_center", ":cur_center"),
			(eq, ":faction_of_center", ":faction"),			
			(val_add, ":num_centers", 1),
		  (try_end),

		  #we are counting num_centers to allow defection although there is high relation between faction leader and troop. 
		  #but this rule should not applied for player's faction and player_supporters_faction so thats why here 1 is added to num_centers in that case.
		  (try_begin), 
		    (this_or_next|eq, ":faction", "$players_kingdom"),
			(eq, ":faction", "fac_player_supporters_faction"),
			(val_add, ":num_centers", 1),
		  (try_end),
			
			(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
			(assign, ":cur_relation", reg0),  ## CC-D add: allow defection
          (this_or_next|le, reg0, -50), #was -75
		  (eq, ":num_centers", 0), #if there is no walled centers that faction has defection happens 100%.

			(call_script, "script_cf_troop_can_intrigue", ":troop_no", 0), #Should include battle, prisoner, in a castle with others
      		(store_random_in_range, ":who_moves_first", 0, 2),

			#The more centralized the faction, the greater the chance the liege will indict
			#the lord before he defects.
			(faction_get_slot, reg0, ":faction", dplmc_slot_faction_centralization),
			(val_clamp, reg0, -3, 4),
			(val_add, reg0, 10),#7 minimum, 13 maximum
			(store_random_in_range, ":random", 0, reg0),
			#Random  < 5: The lord defects
			#Random >= 5: The liege indicts the lord for treason

			(try_begin),
	            (this_or_next|eq, ":num_centers", 0), #Thanks Caba`drin & Osviux
	            (this_or_next|le, ":cur_relation", -10),  ## CC-D add: allow defection
	            (neq, ":who_moves_first", 0),
				(lt, ":random", 5),
				(neq, ":troop_no", "trp_player"),
				#do a defection
                        (try_begin), 
                          (neq, ":num_centers", 0), 
						  #Note that I assign the troop number instead of 1 as is done in Native
                          (assign, "$g_give_advantage_to_original_faction", ":troop_no"),
                        (try_end),
			#(assign, "$g_give_advantage_to_original_faction", 1),
        
			(store_faction_of_troop, ":orig_faction", ":troop_no"),
				(call_script, "script_lord_find_alternative_faction", ":troop_no"),
				(assign, ":new_faction", reg0),
				(assign, "$g_give_advantage_to_original_faction", 0),
			(try_begin),
			  (neq, ":new_faction", ":orig_faction"),
				(is_between, ":new_faction", kingdoms_begin, kingdoms_end),
				(str_store_troop_name_link, s1, ":troop_no"),
				(str_store_faction_name_link, s2, ":new_faction"),
				(str_store_faction_name_link, s3, ":faction"),
				(call_script, "script_change_troop_faction", ":troop_no", ":new_faction"),
				(try_begin),
					(ge, "$cheat_mode", 1),
					(str_store_troop_name, s4, ":troop_no"),
					(display_message, "@{!}DEBUG - {s4} faction changed in defection"),
				(try_end),
				(call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
				(assign, reg4, reg0),
				(str_store_string, s4, "str_lord_defects_ordinary"),
				(display_log_message, "@{!}{s4}"),
				(try_begin),
					(eq, "$cheat_mode", 1),
					(this_or_next|eq, ":new_faction", "$players_kingdom"),
					(eq, ":faction", "$players_kingdom"),
					(call_script, "script_add_notification_menu", "mnu_notification_lord_defects", ":troop_no", ":faction"),
				(try_end),
			## CC-D begin: allow defection
			(else_try),
			  (neq, ":new_faction", ":orig_faction"),
			  (str_store_troop_name, s1, ":troop_no"),
			  #(str_store_faction_name, s2, ":new_faction"),
			  (str_store_faction_name, s3, ":faction"),
			  (troop_set_slot, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
			  (troop_get_slot, ":led_party", ":troop_no", slot_troop_leaded_party),
			  (try_begin),
			    (gt, ":led_party", 0),
			    (party_is_active, ":led_party"),
			    (neq, ":led_party", "p_main_party"),
			    (remove_party, ":led_party"),
			    (troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
			  (try_end),
			  (call_script, "script_change_troop_faction", ":troop_no", "fac_outlaws"),
			  (call_script, "script_dplmc_store_troop_is_female", ":troop_no"),
			  (assign, reg4, reg0),
			  (display_log_message, "@{s1} has renounced {reg4?her:his} allegiance to the {s3}, and {reg4?she:he} has gone into exile outside calradia."),
			## CC-D end
			(try_end),
			(else_try),
				(neq, ":faction_leader", "trp_player"),
                (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
			(le, reg0, -50), #was -75
				(call_script, "script_indict_lord_for_treason", ":troop_no", ":faction"),
			(try_end),

			#Update :faction if it has changed
			(try_begin),
				(eq, ":troop_no", "trp_player"),
				(assign, reg0, "$players_kingdom"),
			(else_try),
				(store_faction_of_troop, reg0, ":troop_no"),
			(try_end),
			(neq, reg0, ":faction"),#Fall through if indictment/defection didn't happen
			(assign, ":faction", reg0),
		(else_try),  #Take a stand on an issue
			(neq, ":troop_no", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
			(faction_slot_ge, ":faction", slot_faction_political_issue, 1),
			#This bit of complication is needed for savegame compatibility -- if zero is in the slot, they'll choose anyway
			(neg|troop_slot_ge, ":troop_no", slot_troop_stance_on_faction_issue, 1),
			(this_or_next|troop_slot_eq, ":troop_no", slot_troop_stance_on_faction_issue, -1),
				(neq, "$players_kingdom", ":faction"),

			(call_script, "script_npc_decision_checklist_take_stand_on_issue", ":troop_no"),
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, reg0),
        (else_try),
			#OPTIONAL CHANGE (AI CHANGES HIGH):
			(ge, "$g_dplmc_ai_changes", DPLMC_AI_CHANGES_HIGH),
			#If an AI kingdom has fiefless lords and no free fiefs, the king
			#will consider giving up a village.  The king will not give up fiefs if
			#doing so would give him less territory than another lord of his faction.
			#(For simplicity, the AI will not do this while a marshall appointment
			#is pending.)
			(faction_slot_eq, ":faction", slot_faction_leader, ":troop_no"),
			(neq, ":troop_no", "trp_player"),
			#With fewer than 3 points we don't need to bother continuing, since 2 points means he only owns a single village.
         (troop_get_slot, ":local_temp", ":troop_no", dplmc_slot_troop_center_points_plus_one),
			(ge, ":local_temp", 3),
			#Don't do this while other business is pending
			(neg|faction_slot_ge, ":faction", slot_faction_political_issue, 1),
			#Find the fiefless lord of his faction that the king likes best.
			#Terminate the search early if he finds another lord whose fiefs
			#equal or exceed his own, or a lord whose fief point slot is not
			#initialized.
			(assign, ":end_cond", heroes_end),
			(assign, ":any_found", -200),
			(assign, ":best_active_npc", -1),
			(try_for_range, ":active_npc", heroes_begin, ":end_cond"),
				(neq, ":active_npc", ":troop_no"),
				(troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
				(store_faction_of_troop, reg0, ":active_npc"),
				(eq, reg0, ":faction"),
				(troop_get_slot, reg0, ":active_npc", dplmc_slot_troop_center_points_plus_one),
				(try_begin),
					#Terminate.  The king cannot give up any points without being outfieffed (if he isn't already)
					(ge, reg0, ":local_temp"),
					(assign, ":end_cond", ":active_npc"),
				(else_try),
					#Terminate.  The first pass of political calculations aren't done, or things are in flux.
					(lt, reg0, 1),
					(assign, ":end_cond", ":active_npc"),
				(else_try),
					(eq, reg0, 1),
					(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
					(gt, reg0, ":any_found"),
					(assign, ":any_found", reg0),
					(assign, ":best_active_npc", ":active_npc"),
				(try_end),
			(try_end),
			(eq, ":end_cond", heroes_end),
			(is_between, ":best_active_npc", heroes_begin, heroes_end),
			(gt, ":any_found", -10),
			#Give up the least prosperous fief.
			(assign, ":local_temp", 101),
			(assign, ":any_found", -1),
			(try_for_range, ":center", villages_begin, villages_end),
				(party_slot_eq, ":center", slot_town_lord, ":troop_no"),
				(party_get_slot, reg0, ":center", slot_town_prosperity),
				(this_or_next|eq, ":any_found", -1),
				(lt, reg0, ":local_temp"),
				(assign, ":local_temp", reg0),
				(assign, ":any_found", ":center"),
			(try_end),
			#Clear village's lord
			(is_between, ":any_found", centers_begin, centers_end),
			(party_set_slot, ":any_found", slot_town_lord, -1),
			(troop_get_slot, reg0, ":troop_no", dplmc_slot_troop_center_points_plus_one),
			(val_sub, reg0, 1),
			(troop_set_slot, ":troop_no", dplmc_slot_troop_center_points_plus_one, reg0),
			(str_store_party_name_link, s4, ":any_found"),
			(str_store_troop_name_link, s5, ":troop_no"),
			(str_store_faction_name_link, s7, ":faction"),
			(display_log_message, "@{s5} has decided to grant {s4} to another lord of the {s7}."),
			#Reset faction issue
			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(store_faction_of_troop, reg0, ":active_npc"),
				(eq, reg0, ":faction"),
				(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
			(try_end),
			(store_current_hours, reg0),
			(faction_set_slot, ":faction", slot_faction_political_issue_time, reg0),
			(faction_set_slot, ":faction", slot_faction_political_issue, ":any_found"),
			#Set the liege's position on the issue, since he gave up the village with
			#something specific in mind.
			(troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, ":best_active_npc"),
		(try_end),

		#Reduce grudges over time
		(try_begin),
			#Skip this for the dead
			(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_dead),
			#Do not perform this for kingdom ladies, since it will potentially mess up courtship.
			(neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_lady),

			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(neq, ":active_npc", ":troop_no"),
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_lady),#Don't do for ladies
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, dplmc_slto_dead),#Don't do for the dead

				#Fix: there are some NPCs that have "initial" relations with the player set,
				#but they can decay before ever meeting him, so keep them until the first meeting.
				(this_or_next|neq, ":troop_no", "trp_player"),
				(troop_slot_ge, ":troop_no", slot_troop_met, 1),

				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
				(lt, reg0, 0),
				(store_sub, ":chance_of_convergence", 0, reg0),
				(store_random_in_range, ":random", 0, 300),
				(lt, ":random", ":chance_of_convergence"),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":active_npc", 1),
				(val_add, "$total_relation_changes_through_convergence", 1),
			(try_end),

			#Accelerate forgiveness for lords in exile (with their original faction only)
			(neq, ":troop_no", "trp_player"),
			(troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
			(troop_get_slot, ":original_faction", ":troop_no", slot_troop_original_faction),
			(gt, ":original_faction", 0),

			(try_for_range, ":active_npc", heroes_begin, heroes_end),
				(neq, ":active_npc", ":troop_no"),
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_lady),#Don't do for ladies
				(neg|troop_slot_eq, ":active_npc", slot_troop_occupation, dplmc_slto_dead),#Don't do for the dead
				#Only apply to heroes with the same original faction
				(troop_slot_eq, ":active_npc", slot_troop_original_faction, ":original_faction"),
				(call_script, "script_troop_get_relation_with_troop", ":troop_no", ":active_npc"),
				(lt, reg0, 0),
				(store_sub, ":chance_of_convergence", 0, reg0),
				(store_random_in_range, ":random", 0, 300),
				(lt, ":random", ":chance_of_convergence"),
				(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":active_npc", 1),
				(val_add, "$total_relation_changes_through_convergence", 1),
			(try_end),
		(try_end),
	#Finish loop over the ":iteration" variable.
	(try_end),
	(assign, reg0, ":save_reg0"),
	##diplomacy end+
   ]),

#TEMPORARILY DISABLED, AS READINESS IS NOW A PRODUCT OF NPC_DECISION_CHECKLIST
  # Changing readiness to join army
#   (10,
 #   [
 #     (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
#		(eq, 1, 0),
#	    (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#        (assign, ":modifier", 1),
#        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
#        (try_begin),
#          (gt, ":party_no", 0),
#          (party_get_slot, ":commander_party", ":party_no", slot_party_commander_party),
#          (ge, ":commander_party", 0),
#          (store_faction_of_party, ":faction_no", ":party_no"),
#          (faction_get_slot, ":faction_marshall", ":faction_no", slot_faction_marshall),
#          (ge, ":faction_marshall", 0),
#          (troop_get_slot, ":marshall_party", ":faction_marshall", slot_troop_leaded_party),
#          (eq, ":commander_party", ":marshall_party"),
#          (assign, ":modifier", -1),
#        (try_end),
#        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_join_army),
#        (val_add, ":readiness", ":modifier"),
#        (val_clamp, ":readiness", 0, 100),
#        (troop_set_slot, ":troop_no", slot_troop_readiness_to_join_army, ":readiness"),
#        (assign, ":modifier", 1),
#        (try_begin),
#          (gt, ":party_no", 0),
#          (store_troop_faction, ":troop_faction", ":troop_no"),
#          (eq, ":troop_faction", "fac_player_supporters_faction"),
#          (neg|troop_slot_eq, ":troop_no", slot_troop_player_order_state, spai_undefined),
#          (party_get_slot, ":party_ai_state", ":party_no", slot_party_ai_state),
#          (party_get_slot, ":party_ai_object", ":party_no", slot_party_ai_object),
#          #Check if party is following player orders
#          (try_begin),
#            (troop_slot_eq, ":troop_no", slot_troop_player_order_state, ":party_ai_state"),
#            (troop_slot_eq, ":troop_no", slot_troop_player_order_object, ":party_ai_object"),
#            (assign, ":modifier", -1),
#          (else_try),
#            #Leaving following player orders if the current party order is not the same.
#            (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
#            (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
#          (try_end),
#        (try_end),
#        (troop_get_slot, ":readiness", ":troop_no", slot_troop_readiness_to_follow_orders),
#        (val_add, ":readiness", ":modifier"),
#        (val_clamp, ":readiness", 0, 100),
#        (troop_set_slot, ":troop_no", slot_troop_readiness_to_follow_orders, ":readiness"),
#        (try_begin),
#          (lt, ":readiness", 10),
#          (troop_set_slot, ":troop_no", slot_troop_player_order_state, spai_undefined),
#          (troop_set_slot, ":troop_no", slot_troop_player_order_object, -1),
#        (try_end),
#      (try_end),
 #     ]),

  # Process vassal ai
   (2,
   [
     #(call_script, "script_process_kingdom_parties_ai"), #moved to below trigger (per 1 hour) in order to allow it processed more frequent.
   ]),

  # Process alarms - perhaps break this down into several groups, with a modula
   (1, #this now calls 1/3 of all centers each time, thus hopefully lightening the CPU load
   [
     (call_script, "script_process_alarms"),

	 #occc comment out - It's not necessary anymore with Motomataru's Campaign AI
     #(call_script, "script_allow_vassals_to_join_indoor_battle"),

     (call_script, "script_process_kingdom_parties_ai"),
     ## CC-D begin: extra raider
     (store_current_hours, ":current_time"),
     (try_for_range, ":npc", bandit_npc_begin, bandit_npc_end),
       (store_troop_faction, ":npc_faction", ":npc"),
       (eq, ":npc_faction", "fac_outlaws"),
       (troop_slot_eq, ":npc", slot_troop_occupation, slto_bandit),
       (neg|troop_slot_ge, ":npc", slot_troop_prisoner_of_party, 0),
       (troop_get_slot, ":party_no", ":npc", slot_troop_leaded_party),
       (gt, ":party_no", 0),
       (party_is_active, ":party_no"),
       (party_get_num_companions, ":party_size", ":party_no"),
       (gt, ":party_size", 60),
       (try_begin),
         (party_slot_eq, ":party_no", slot_party_ai_substate, 0),
         (party_get_slot, ":next_raid", ":party_no", slot_party_last_in_any_center),  # slot use aother purpose
         (gt, ":current_time", ":next_raid"),
         (party_set_slot, ":party_no", slot_party_ai_state, spai_raiding_around_center),
       (try_end),
       (call_script, "script_process_raiders_ai", ":npc"),#occc
     (try_end),
     ## CC-D end
   ]),

  # Process siege ai
   (3,
   [
      ##diplomacy start+
	  (assign, ":save_reg0", reg0),#Save registers
	  (assign, ":save_reg1", reg1),
	  ##diplomacy end+
      (store_current_hours, ":cur_hours"),
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_get_slot, ":besieger_party", ":center_no", slot_center_is_besieged_by),
        (gt, ":besieger_party", 0),
        (party_is_active, ":besieger_party"),
        (store_faction_of_party, ":besieger_faction", ":besieger_party"),
        (party_slot_ge, ":center_no", slot_center_is_besieged_by, 1),
        (party_get_slot, ":siege_begin_hours", ":center_no", slot_center_siege_begin_hours),
        (store_sub, ":siege_begin_hours", ":cur_hours", ":siege_begin_hours"),
        (assign, ":launch_attack", 0),
        (assign, ":call_attack_back", 0),
        (assign, ":attacker_strength", 0),
        (assign, ":marshall_attacking", 0),
		
		###ATTENTION OCCC FROM HERE
		
        (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
		  #(try_for_parties, ":party_no"),
          (gt, ":party_no", 0),
          (party_is_active, ":party_no"),

          (store_troop_faction, ":troop_faction_no", ":troop_no"),
		  
		  #(store_faction_of_party, ":troop_faction_no", ":party_no"),
		###ATTENTION OCCC END HERE ITS A KINDA DANGEROUS CHANGE
          (eq, ":troop_faction_no", ":besieger_faction"),
          (assign, ":continue", 0),
          (try_begin),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
            (assign, ":continue", 1),
          (else_try),
            (party_slot_eq, ":party_no", slot_party_ai_state, spai_accompanying_army),
            (party_get_slot, ":commander_party", ":party_no", slot_party_ai_object),
            (gt, ":commander_party", 0),
            (party_is_active, ":commander_party"),
            (party_slot_eq, ":commander_party", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":commander_party", slot_party_ai_object, ":center_no"),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (party_get_battle_opponent, ":opponent", ":party_no"),
          (this_or_next|lt, ":opponent", 0),
          (eq, ":opponent", ":center_no"),
          (party_stack_get_troop_id, ":troop_no", ":party_no", 0),#occc
		  (assign, ":marshal_trp", -1),#occc
          (try_begin),
            (faction_slot_eq, ":besieger_faction", slot_faction_marshall, ":troop_no"),
			#OCCC - if the besieger is a marshall, use his eng skill to process siege
            (assign, ":marshal_trp", ":troop_no"),
            (assign, ":marshall_attacking", 1),
          (try_end),
          (call_script, "script_party_calculate_regular_strength", ":party_no"),
		  ##diplomacy start+ terrain advantage
		  (try_begin),
			(ge, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", ":party_no", dplmc_terrain_code_siege, 0, 0),
          (try_end),
		  ##diplomacy end+
          (val_add, ":attacker_strength", reg0),
        (try_end),
        (try_begin),
          (gt, ":attacker_strength", 0),
          (party_collect_attachments_to_party, ":center_no", "p_collective_enemy"),
          (call_script, "script_party_calculate_regular_strength", "p_collective_enemy"),
		  ##diplomacy start+ terrain advantage
		  (try_begin),
			(ge, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
			(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", dplmc_terrain_code_siege, 0, 0),
          (try_end),
		  ##diplomacy end+
          (assign, ":defender_strength", reg0),
          (try_begin),
            (eq, "$auto_enter_town", ":center_no"),
            (eq, "$g_player_is_captive", 0),
            (call_script, "script_party_calculate_regular_strength", "p_main_party"),
			##diplomacy start+ terrain advantage
			(try_begin),
				(ge, "$g_dplmc_terrain_advantage", DPLMC_TERRAIN_ADVANTAGE_ENABLE),
				(call_script, "script_dplmc_party_calculate_strength_in_terrain", "p_collective_enemy", dplmc_terrain_code_siege, 0, 0),
			(try_end),
			##diplomacy end+
            (val_add, ":defender_strength", reg0),
            (val_mul, ":attacker_strength", 2), #double the power of attackers if the player is in the campaign
          (try_end),
          (party_get_slot, ":siege_hardness", ":center_no", slot_center_siege_hardness),
          (val_add, ":siege_hardness", 100),
          (val_mul, ":defender_strength", ":siege_hardness"),
          (val_div, ":defender_strength", 100),
          (val_max, ":defender_strength", 1),
          (try_begin),
            (eq, ":marshall_attacking", 1),
            (eq, ":besieger_faction", "$players_kingdom"),
            (check_quest_active, "qst_follow_army"),
            (val_mul, ":attacker_strength", 2), #double the power of attackers if the player is in the campaign
          (try_end),
          (store_mul, ":strength_ratio", ":attacker_strength", 100),
          (val_div, ":strength_ratio", ":defender_strength"),
          (store_sub, ":random_up_limit", ":strength_ratio", 250), #was 300 (1.126)

          (try_begin),
            (gt, ":random_up_limit", -100), #never attack if the strength ratio is less than 150%
            (store_div, ":siege_begin_hours_effect", ":siege_begin_hours", 2), #was 3 (1.126)
            (val_add, ":random_up_limit", ":siege_begin_hours_effect"),
          (try_end),

          (val_div, ":random_up_limit", 5),
          (val_max, ":random_up_limit", 0),
          (store_sub, ":random_down_limit", 175, ":strength_ratio"), #was 200 (1.126)
          (val_max, ":random_down_limit", 0),
          (try_begin),
            (store_random_in_range, ":rand", 0, 100),
			#occc begin 
			(assign, ":siege_down_lim_time", 24),
			(try_begin),
				(gt,":marshal_trp",0),
				(store_skill_level, ":sieger_engineer_skl", skl_engineer, ":marshal_trp"),
				(val_max, ":sieger_engineer_skl", 0),
				(val_div, ":sieger_engineer_skl", 2),
				(val_sub, ":siege_down_lim_time", ":sieger_engineer_skl"),
				(val_mul, ":sieger_engineer_skl", 2),
				(val_sub, ":rand", ":sieger_engineer_skl"),
			(try_end),
			#occc end
            (lt, ":rand", ":random_up_limit"),
            (gt, ":siege_begin_hours", ":siege_down_lim_time"),#initial preparation 24->(24-[engineer_skill])
            (assign, ":launch_attack", 1),
          (else_try),
            (store_random_in_range, ":rand", 0, 100),
            (lt, ":rand", ":random_down_limit"),
            (assign, ":call_attack_back", 1),
          (try_end),
        (else_try),
          (assign, ":call_attack_back", 1),
        (try_end),

        #Assault the fortress
        (try_begin),
          (eq, ":launch_attack", 1),
          (call_script, "script_begin_assault_on_center", ":center_no"),
        (else_try),
          (eq, ":call_attack_back", 1),
          (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
            (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
            (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
            (gt, ":party_no", 0),
            (party_is_active, ":party_no"),

            (party_slot_eq, ":party_no", slot_party_ai_state, spai_besieging_center),
            (party_slot_eq, ":party_no", slot_party_ai_object, ":center_no"),
            (party_slot_eq, ":party_no", slot_party_ai_substate, 1),
            (call_script, "script_party_set_ai_state", ":party_no", spai_undefined, -1),
            (call_script, "script_party_set_ai_state", ":party_no", spai_besieging_center, ":center_no"),
            #resetting siege begin time if at least 1 party retreats
            (party_set_slot, ":center_no", slot_center_siege_begin_hours, ":cur_hours"),
          (try_end),
		  #occc risingsun invasion
        (try_end),
      (try_end),
	  ##diplomacy start+
	  #Revert registers
	  (assign, reg0, ":save_reg0"),
	  (assign, reg1, ":save_reg1"),
	  ##diplomacy end+
    ]),

    # Decide faction ais
    (6, #it was 23
    [
      (assign, "$g_recalculate_ais", 1),
    ]),


  # Decide faction ai flag check
   (0,
   [


    (try_begin),
		(ge, "$cheat_mode", 1),

		(try_for_range, ":king", "trp_kingdom_1_lord", "trp_knight_1_1"),
			(store_add, ":proper_faction", ":king", "fac_kingdom_1"),
			(val_sub, ":proper_faction", "trp_kingdom_1_lord"),
			(store_faction_of_troop, ":actual_faction", ":king"),

			(neq, ":proper_faction", ":actual_faction"),
			(neq, ":actual_faction", "fac_commoners"),
			(ge, "$cheat_mode", 2),
			(neq, ":king", "trp_kingdom_2_lord"),

			(str_store_troop_name, s4, ":king"),
			(str_store_faction_name, s5, ":actual_faction"),
			(str_store_faction_name, s6, ":proper_faction"),
			(str_store_string, s65, "@{!}DEBUG - {s4} is in {s5}, should be in {s6}, disabling political cheat mode"),
#			(display_message, "@{s65}"),
			(rest_for_hours, 0, 0, 0),

			#(assign, "$cheat_mode", 1),
			(jump_to_menu, "mnu_debug_alert_from_s65"),
		(try_end),


	(try_end),

     (eq, "$g_recalculate_ais", 1),
     (assign, "$g_recalculate_ais", 0),
     (call_script, "script_recalculate_ais"),
   ]),

    # Count faction armies
    (24,
    [
       (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
         (call_script, "script_faction_recalculate_strength", ":faction_no"),
       (try_end),
	   ##diplomacy start+ Add support for promoted kingdom ladies
	   ##OLD:
	   #(try_for_range, ":active_npc", active_npcs_begin, active_npcs_end),
	   ##NEW:
	   (try_for_range, ":active_npc", heroes_begin, heroes_end),
	    (this_or_next|is_between, ":active_npc", active_npcs_begin, active_npcs_end),
	    (troop_slot_eq, ":active_npc", slot_troop_occupation, slto_kingdom_hero),
	   ##diplomacy end+
		(store_faction_of_troop, ":active_npc_faction", ":active_npc"),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_default),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_feast),
		(neg|faction_slot_eq, ":active_npc_faction", slot_faction_ai_state, sfai_gathering_army),

		(troop_get_slot, ":active_npc_party", ":active_npc", slot_troop_leaded_party),
		(party_is_active, ":active_npc_party"),

		(val_add, "$total_vassal_days_on_campaign", 1),

	    (party_slot_eq, ":active_npc_party", slot_party_ai_state, spai_accompanying_army),
		(val_add, "$total_vassal_days_responding_to_campaign", 1),


	   (try_end),

    ]),

  # Reset hero quest status
  # Change hero relation
   (36,
   [
     (try_for_range, ":troop_no", heroes_begin, heroes_end),
       (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
     (try_end),

     (try_for_range, ":troop_no", village_elders_begin, village_elders_end),
       (troop_set_slot, ":troop_no", slot_troop_does_not_give_quest, 0),
     (try_end),
    ]),

  # Refresh merchant inventories
   (168,
   [
      (try_for_range, ":village_no", villages_begin, villages_end),
        (call_script, "script_refresh_village_merchant_inventory", ":village_no"),
      (try_end),
    ]),

  #Refreshing village defenders
  #Clearing slot_village_player_can_not_steal_cattle flags
   (48,
   [
      (try_for_range, ":village_no", villages_begin, villages_end),
        ## CC-D begin: down prosperity as charge
        (party_get_num_companions, ":past_size", ":village_no"),
        
        (call_script, "script_refresh_village_defenders", ":village_no"),
        (party_set_slot, ":village_no", slot_village_player_can_not_steal_cattle, 0),
        
        (party_get_num_companions, ":cur_size", ":village_no"),
        (try_begin),
          (gt, ":cur_size", ":past_size"),
          (store_sub, ":num", ":past_size", ":cur_size"),
          (val_div, ":num", 2),
          (call_script, "script_change_center_prosperity", ":village_no", ":num"),
        (try_end),
        ## CC-D end
      (try_end),
    ]),

  # Refresh number of cattle in villages
  (24 * 7,
   [
     (try_for_range, ":village_no", centers_begin, centers_end),
	  (neg|is_between, ":village_no", castles_begin, castles_end),
      (party_get_slot, ":num_cattle", ":village_no", slot_center_head_cattle),
      (party_get_slot, ":num_sheep", ":village_no", slot_center_head_sheep),
      (party_get_slot, ":num_acres", ":village_no", slot_center_acres_pasture),
	  (val_max, ":num_acres", 1),

	  (store_mul, ":grazing_capacity", ":num_cattle", 400),
	  (store_mul, ":sheep_addition", ":num_sheep", 200),
	  (val_add, ":grazing_capacity", ":sheep_addition"),
	  (val_div, ":grazing_capacity", ":num_acres"),
	  (try_begin),
		(eq, "$cheat_mode", 1),
	    (assign, reg4, ":grazing_capacity"),
		(str_store_party_name, s4, ":village_no"),
	    #(display_message, "@{!}DEBUG -- Herd adjustment: {s4} at {reg4}% of grazing capacity"),
	  (try_end),


      (store_random_in_range, ":random_no", 0, 100),
      (try_begin), #Disaster
        (eq, ":random_no", 0),#1% chance of epidemic - should happen once every two years
        (val_min, ":num_cattle", 10),

        (try_begin),
#          (eq, "$cheat_mode", 1),
#          (str_store_party_name, s1, ":village_no"),
#          (display_message, "@{!}Cattle in {s1} are exterminated due to famine."),
           ##diplomacy start+ Add display message for the player's own fiefs
		   #(store_distance_to_party_from_party, ":dist", "p_main_party", ":village_no"),
		   #(this_or_next|lt, ":dist", 30),
	          (gt, "$g_player_chamberlain", 0),
		   (party_slot_eq, ":village_no", slot_town_lord, "trp_player"),
		   (party_get_slot, reg4, ":village_no", slot_center_head_cattle),
		   (val_sub, reg4, ":num_cattle"),
		   (gt, reg4, 0),
		   (str_store_party_name_link, s4, ":village_no"),
		   (display_log_message, "@A livestock epidemic has killed {reg4} cattle in {s4}."),
		   ##diplomacy end+
        (try_end),

      (else_try), #Overgrazing
	    (gt, ":grazing_capacity", 100),

         (val_mul, ":num_sheep", 90), #10% decrease at number of cattles
         (val_div, ":num_sheep", 100),

         (val_mul, ":num_cattle", 90), #10% decrease at number of sheeps
         (val_div, ":num_cattle", 100),

       (else_try), #superb grazing
         (lt, ":grazing_capacity", 30),

         (val_mul, ":num_cattle", 120), #20% increase at number of cattles
         (val_div, ":num_cattle", 100),
         (val_add, ":num_cattle", 1),

         (val_mul, ":num_sheep", 120), #20% increase at number of sheeps
         (val_div, ":num_sheep", 100),
         (val_add, ":num_sheep", 1),

       (else_try), #very good grazing
         (lt, ":grazing_capacity", 60),

         (val_mul, ":num_cattle", 110), #10% increase at number of cattles
         (val_div, ":num_cattle", 100),
		(val_add, ":num_cattle", 1),

         (val_mul, ":num_sheep", 110), #10% increase at number of sheeps
         (val_div, ":num_sheep", 100),
		(val_add, ":num_sheep", 1),

     (else_try), #good grazing
	    (lt, ":grazing_capacity", 100),
         (lt, ":random_no", 50),

         (val_mul, ":num_cattle", 105), #5% increase at number of cattles
         (val_div, ":num_cattle", 100),
         (try_begin), #if very low number of cattles and there is good grazing then increase number of cattles also by one
           (le, ":num_cattle", 20),
			(val_add, ":num_cattle", 1),
		(try_end),

         (val_mul, ":num_sheep", 105), #5% increase at number of sheeps
         (val_div, ":num_sheep", 100),
         (try_begin), #if very low number of sheeps and there is good grazing then increase number of sheeps also by one
           (le, ":num_sheep", 20),
			(val_add, ":num_sheep", 1),
		(try_end),


     (try_end),

     (party_set_slot, ":village_no", slot_center_head_cattle, ":num_cattle"),
     (party_set_slot, ":village_no", slot_center_head_sheep, ":num_sheep"),
    (try_end),
    ]),

#CC-C move begin
   #Accumulate taxes
   #(24 * 7,
   #[
      #Adding earnings to town lords' wealths.
      #Moved to troop does business
      #(try_for_range, ":center_no", centers_begin, centers_end),
      #  (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      #  (neq, ":town_lord", "trp_player"),
      #  (is_between, ":town_lord", active_npcs_begin, active_npcs_end),
      #  (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
      #  (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
      #  (troop_get_slot, ":troop_wealth", ":town_lord", slot_troop_wealth),
      #  (val_add, ":troop_wealth", ":accumulated_rents"),
      #  (val_add, ":troop_wealth", ":accumulated_tariffs"),
      #  (troop_set_slot, ":town_lord", slot_troop_wealth, ":troop_wealth"),
      #  (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
      #  (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
      #  (try_begin),
      #    (eq, "$cheat_mode", 1),
      #    (assign, reg1, ":troop_wealth"),
      #    (add_troop_note_from_sreg, ":town_lord", 1, "str_current_wealth_reg1", 0),
      #  (try_end),
      #(try_end),
            
	    #Collect taxes for another week
#      (try_for_range, ":center_no", centers_begin, centers_end),
#        (try_begin),
#          (party_slot_ge, ":center_no", slot_town_lord, 0), #unassigned centers do not accumulate rents	  
#        
#          (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),		  
#		
#          (assign, ":cur_rents", 0),
#          (try_begin),
#            (party_slot_eq, ":center_no", slot_party_type, spt_village),
#            (try_begin),
#              (party_slot_eq, ":center_no", slot_village_state, svs_normal),
#              (assign, ":cur_rents", 1200), 
#            (try_end),
#          (else_try),
#            (party_slot_eq, ":center_no", slot_party_type, spt_castle),
#            (assign, ":cur_rents", 1200),
#          (else_try),  
#            (party_slot_eq, ":center_no", slot_party_type, spt_town),
#            (assign, ":cur_rents", 2400),
#          (try_end),
#		
#          (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity), #prosperty changes between 0..100     
#          (store_add, ":multiplier", 20, ":prosperity"), #multiplier changes between 20..120
#          (val_mul, ":cur_rents", ":multiplier"), 
#          (val_div, ":cur_rents", 120),#Prosperity of 100 gives the default values
#          
#          (try_begin),
#            (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
#            
#            (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
#            (try_begin),
#              (eq, ":reduce_campaign_ai", 0), #hard (less money from rents)
#              (val_mul, ":cur_rents", 3),
#              (val_div, ":cur_rents", 4),
#            (else_try),
#              (eq, ":reduce_campaign_ai", 1), #medium (normal money from rents)
#              #same
#            (else_try),
#              (eq, ":reduce_campaign_ai", 2), #easy (more money from rents)
#              (val_mul, ":cur_rents", 4),
#              (val_div, ":cur_rents", 3),
#            (try_end),                
#          (try_end),  
#                    
#          (val_add, ":accumulated_rents", ":cur_rents"), #cur rents changes between 23..1000
#
#          ##diplomacy begin
#          (try_begin),    
#            (str_store_party_name, s6, ":center_no"),
#             
#            (party_get_slot, ":tax_rate", ":center_no", dplmc_slot_center_taxation),
#            (neq, ":tax_rate", 0),
#            (store_div, ":rent_change", ":accumulated_rents", 100),
#            (val_mul, ":rent_change", ":tax_rate"),
#   
#            (try_begin), #debug
#              (eq, "$cheat_mode", 1),
#              (assign, reg0, ":tax_rate"),
#              (display_message, "@{!}DEBUG : tax rate in {s6}: {reg0}"),
#              (assign, reg0, ":accumulated_rents"),
#              (display_message, "@{!}DEBUG : accumulated_rents  in {s6}: {reg0}"),
#              (assign, reg0, ":rent_change"),
#              (display_message, "@{!}DEBUG : rent_change in {s6}: {reg0}  in {s6}"),
#            (try_end),          
#  
#            (val_add, ":accumulated_rents", ":rent_change"),
#            
#            (val_div, ":tax_rate", -25),
#            
#            (call_script, "script_change_center_prosperity", ":center_no", ":tax_rate"),
#  
#            (try_begin),
#              (lt, ":tax_rate", 0), #double negative values
#              (val_mul, ":tax_rate", 2),
#              
#              (try_begin), #debug
#                (eq, "$cheat_mode", 1),
#                (assign, reg0, ":tax_rate"),
#                (display_message, "@{!}DEBUG : tax rate after modi in {s6}: {reg0}"),
#              (try_end),
#  
#              (try_begin),
#                (this_or_next|is_between, ":center_no", villages_begin, villages_end),
#                (is_between, ":center_no", towns_begin, towns_end),
#                (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),
#  
#                (try_begin), #debug
#                  (eq, "$cheat_mode", 1),
#                  (assign, reg0, ":center_relation"),
#                  (display_message, "@{!}DEBUG : center relation: {reg0}"),
#                (try_end),
#              
#                (le, ":center_relation", -5),
#                (store_random_in_range, ":random",-100, 0),
#                (gt, ":random", ":center_relation"),           
#                
#                (neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
#                (display_message, "@Riot in {s6}!"),
#                (party_set_slot, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"), #trp_peasant_woman used to simulate riot
#                (call_script, "script_change_center_prosperity", ":center_no", -1),     
#                (call_script, "script_add_notification_menu", "mnu_dplmc_notification_riot", ":center_no", 0),         
#  
#                #add additional troops
#                (store_character_level, ":player_level", "trp_player"),
#                (store_div, ":player_leveld2", ":player_level", 2),
#                (store_mul, ":player_levelx2", ":player_level", 2),
#                (try_begin), 
#                  (is_between, ":center_no", villages_begin, villages_end),       
#                  (store_random_in_range, ":random",0, ":player_level"),
#                  (party_add_members, ":center_no", "trp_mercenary_swordsman", ":random"),
#                  (store_random_in_range, ":random", 0, ":player_leveld2"),
#                  (party_add_members, ":center_no", "trp_hired_blade", ":random"),
#                (else_try),
#                  (party_set_banner_icon, ":center_no", 0),   
#                  (party_get_num_companion_stacks, ":num_stacks",":center_no"),
#                  (try_for_range, ":i_stack", 0, ":num_stacks"),
#                    (party_stack_get_size, ":stack_size",":center_no",":i_stack"),                             
#                    (val_div, ":stack_size", 2),
#                    (party_stack_get_troop_id, ":troop_id", ":center_no", ":i_stack"),
#                    (party_remove_members, ":center_no", ":troop_id", ":stack_size"),
#                  (try_end),
#                  (store_random_in_range, ":random",":player_leveld2", ":player_levelx2"),
#                  (party_add_members, ":center_no", "trp_townsman", ":random"),
#                  (store_random_in_range, ":random",0, ":player_level"),
#                  (party_add_members, ":center_no", "trp_watchman", ":random"),
#                (try_end),
#              (end_try),     
#            (try_end),
#            (call_script, "script_change_player_relation_with_center", ":center_no", ":tax_rate"),
#          (try_end),
#          
#          (try_begin), #no taxes for infested villages and towns 
#            (party_slot_ge, ":center_no", slot_village_infested_by_bandits, 1),
#            (assign,":accumulated_rents", 0),
#          (try_end),
#          ##diplomacy end
#
#          (party_set_slot, ":center_no", slot_center_accumulated_rents, ":accumulated_rents"),
#        (try_end),
#        
#        (try_begin),
#          (is_between, ":center_no", villages_begin, villages_end),
#          (party_get_slot, ":bound_castle", ":center_no", slot_village_bound_center),
#          (party_slot_ge, ":bound_castle", slot_town_lord, 0), #unassigned centers do not accumulate rents	  
#          (is_between, ":bound_castle", castles_begin, castles_end),
#          (party_get_slot, ":accumulated_rents", ":bound_castle", slot_center_accumulated_rents), #castle's accumulated rents
#          (val_add, ":accumulated_rents", ":cur_rents"), #add village's rent to castle rents
#          (party_set_slot, ":bound_castle", slot_center_accumulated_rents, ":accumulated_rents"),
#        (try_end),
#      (try_end),
#    ]),
#CC-C move end
##   (7 * 24,
##   [
###       (call_script, "script_get_number_of_unclaimed_centers_by_player"),
###       (assign, ":unclaimed_centers", reg0),
###       (gt, ":unclaimed_centers", 0),
## You are holding an estate without a lord.        
##       (try_for_range, ":troop_no", heroes_begin, heroes_end),
##         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
#         (troop_get_slot, ":relation", ":troop_no", slot_troop_player_relation),
#         (val_sub, ":relation", 1),
#         (val_max, ":relation", -100),
#         (troop_set_slot, ":troop_no", slot_troop_player_relation, ":relation"),
#       (try_end),
# You relation with all kingdoms other than your own has decreased by 1.
#       (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
#         (neq, ":faction_no", "$players_kingdom"),
#         (store_relation,":faction_relation",":faction_no","fac_player_supporters_faction"),
#         (val_sub, ":faction_relation", 1),
#         (val_max, ":faction_relation", -100),
#		  WARNING: Never use set_relation!
#         (set_relation, ":faction_no", "fac_player_supporters_faction", ":faction_relation"),
#       (try_end),
#    ]),


  # Offer player to join faction
  # Only if the player is male -- female characters will be told that they should seek out a faction through NPCs, possibly
   (32,
   [
     (eq, "$players_kingdom", 0),
     (le, "$g_invite_faction", 0),
     (eq, "$g_player_is_captive", 0),
	 ##diplomacy start+ Use script for gender
	 #(troop_get_type, ":type", "trp_player"),
	 (assign, ":type", "$character_gender"),#<-- this should have been set correctly during character creation
	 ##diplomacy end+
	 (try_begin),
	    ##diplomacy start+ In reduced prejudice mode, female players get the same offers.
		(lt, "$g_disable_condescending_comments", 2),
		##diplomacy end+
		(eq, ":type", 1),
		(eq, "$npc_with_sisterly_advice", 0),
		##diplomacy start+  Make the order less predictable (used below)
		(store_random_in_range, ":random", companions_begin, companions_end),
		##diplomacy end+
		(try_for_range, ":npc", companions_begin, companions_end),
			##diplomacy start+ Make the order less predictable
			(val_add, ":npc", ":random"),
			(try_begin),
				(ge, ":npc", companions_end),
				(val_sub, ":npc", companions_end),
				(val_add, ":npc", companions_begin),
			(try_end),
			##diplomacy end+
			(main_party_has_troop, ":npc"),
			##diplmacy start+ Use a script for gender
			##OLD:
			#(troop_get_type, ":npc_type", ":npc"),
			#(eq, ":npc_type", 1),
			##NEW:
			(assign, ":npc_type", 0),
			(try_begin),
				(call_script, "script_cf_dplmc_troop_is_female", ":npc"),
				(assign, ":npc_type", 1),
			(try_end),
			(eq, ":npc_type", ":type"),
			##diplomacy end+
			(troop_slot_ge, "trp_player", slot_troop_renown, 150),
			(troop_slot_ge, ":npc", slot_troop_woman_to_woman_string, 1),
			(assign, "$npc_with_sisterly_advice", ":npc"),
		(try_end),
	 (else_try),
	     (store_random_in_range, ":kingdom_no", npc_kingdoms_begin, npc_kingdoms_end),
	     (assign, ":min_distance", 999999),
	     (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
	       (store_faction_of_party, ":center_faction", ":center_no"),
	       (eq, ":center_faction", ":kingdom_no"),
	       (store_distance_to_party_from_party, ":cur_distance", "p_main_party", ":center_no"),
	       (val_min, ":min_distance", ":cur_distance"),
	     (try_end),
	     (lt, ":min_distance", 30),
	     (store_relation, ":kingdom_relation", ":kingdom_no", "fac_player_supporters_faction"),
	     (faction_get_slot, ":kingdom_lord", ":kingdom_no", slot_faction_leader),
	     (call_script, "script_troop_get_player_relation", ":kingdom_lord"),
	     (assign, ":lord_relation", reg0),
	     #(troop_get_slot, ":lord_relation", ":kingdom_lord", slot_troop_player_relation),
	     (call_script, "script_get_number_of_hero_centers", "trp_player"),
	     (assign, ":num_centers_owned", reg0),
	     (eq, "$g_infinite_camping", 0),

	     (assign, ":player_party_size", 0),
	     (try_begin),
	       (ge, "p_main_party", 0),
	       (store_party_size_wo_prisoners, ":player_party_size", "p_main_party"),
	     (try_end),

	     (try_begin),
	       (eq, ":num_centers_owned", 0),
	       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
	       (ge, ":player_renown", 160),
	       (ge, ":kingdom_relation", 0),
	       (ge, ":lord_relation", 0),
	       (ge, ":player_party_size", 45),
	       (store_random_in_range, ":rand", 0, 100),
	       (lt, ":rand", 50),
	       (call_script, "script_get_poorest_village_of_faction", ":kingdom_no"),
	       (assign, "$g_invite_offered_center", reg0),
	       (ge, "$g_invite_offered_center", 0),
	       (assign, "$g_invite_faction", ":kingdom_no"),
	       (jump_to_menu, "mnu_invite_player_to_faction"),
	     (else_try),
	       (gt, ":num_centers_owned", 0),
	       (neq, "$players_oath_renounced_against_kingdom", ":kingdom_no"),
	       (ge, ":kingdom_relation", -40),
	       (ge, ":lord_relation", -20),
	       (ge, ":player_party_size", 30),
	       (store_random_in_range, ":rand", 0, 100),
	       (lt, ":rand", 20),
	       (assign, "$g_invite_faction", ":kingdom_no"),
	       (assign, "$g_invite_offered_center", -1),
	       (jump_to_menu, "mnu_invite_player_to_faction_without_center"),
	     (try_end),
	 (try_end),
    ]),

    #recalculate lord random decision seeds once in every week
	(24 * 7,
	[
	  ##diplomacy start+ Kingdom ladies should also have their decision seeds updated.
	  ##                 Also, use 10000 instead of 9999, since the upper bound for store_random_in_range is exclusive.
	  ##OLD:
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
      #  (store_random_in_range, ":random", 0, 9999),
	  ##NEW:
	  (try_for_range, ":troop_no", heroes_begin, heroes_end),
	     (store_random_in_range, ":random", 0, 10000),
	  ##diplomacy end+
        (troop_set_slot, ":troop_no", slot_troop_temp_decision_seed, ":random"),
      (try_end),

	  ##diplomacy start+ Also update the temporary seed for the player
	  (store_random_in_range, ":random", 0, 10000),
	  (troop_set_slot, "trp_player", slot_troop_temp_decision_seed, ":random"),
	  ##diplomacy end+
	]),

  # During rebellion, removing troops from player faction randomly because of low relation points
  # Deprecated -- should be part of regular political events



  # Attach Lord Parties to the town they are in
  (0.1,
   [
       (try_for_range, ":troop_no", heroes_begin, heroes_end),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
         (ge, ":troop_party_no", 1),
		 (party_is_active, ":troop_party_no"),

         (party_get_attached_to, ":cur_attached_town", ":troop_party_no"),
         (lt, ":cur_attached_town", 1),
         (party_get_cur_town, ":destination", ":troop_party_no"),
         (is_between, ":destination", centers_begin, centers_end),
         (call_script, "script_get_relation_between_parties", ":destination", ":troop_party_no"),
         (try_begin),
           (ge, reg0, 0),
           (party_attach_to_party, ":troop_party_no", ":destination"),
         ## CC sell prisoners if possible
           (call_script, "script_lord_sell_prisoners", ":troop_no", ":destination"),
         ## CC
         (else_try),
           (party_set_ai_behavior, ":troop_party_no", ai_bhvr_hold),
         (try_end),

         (try_begin),
           (this_or_next|party_slot_eq, ":destination", slot_party_type, spt_town),
           (party_slot_eq, ":destination", slot_party_type, spt_castle),
           (store_faction_of_party, ":troop_faction_no", ":troop_party_no"),
           (store_faction_of_party, ":destination_faction_no", ":destination"),
           (eq, ":troop_faction_no", ":destination_faction_no"),
           (party_get_num_prisoner_stacks, ":num_stacks", ":troop_party_no"),
           (gt, ":num_stacks", 0),
           (assign, "$g_move_heroes", 1),
           (call_script, "script_party_prisoners_add_party_prisoners", ":destination", ":troop_party_no"),#Moving prisoners to the center
           (assign, "$g_move_heroes", 1),
           (call_script, "script_party_remove_all_prisoners", ":troop_party_no"),
         (try_end),
       (try_end),

	   (try_for_parties, ":bandit_camp"),
	 	 (gt, ":bandit_camp", "p_spawn_points_end"),
		 #Can't have party is active here, because it will fail for inactive parties
		 (party_get_template_id, ":template", ":bandit_camp"),
		 (ge, ":template", "pt_forest_bandit_lair"), ## CC fix
		 (lt, ":template", "pt_bandit_lair_templates_end"), ## CC-D fix

		 (store_distance_to_party_from_party, ":distance", "p_main_party", ":bandit_camp"),
	     (lt, ":distance", 3),
	     (party_set_flags, ":bandit_camp", pf_disabled, 0),
	     (party_set_flags, ":bandit_camp", pf_always_visible, 1),
	   (try_end),
    ]),

  # Check escape chances of hero prisoners.
  (48,
   [
       (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", "p_main_party", 50),
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
##         (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
         (assign, ":chance", 30),
         (try_begin),
           (party_slot_eq, ":center_no", slot_center_has_prisoner_tower, 1),
           (assign, ":chance", 5),
         (try_end),
         (call_script, "script_randomly_make_prisoner_heroes_escape_from_party", ":center_no", ":chance"),
       (try_end),
    ]),

  # Asking the ownership of captured centers to the player
#  (3,
#   [
#    (assign, "$g_center_taken_by_player_faction", -1),
#    (try_for_range, ":center_no", centers_begin, centers_end),
#      (eq, "$g_center_taken_by_player_faction", -1),
#      (store_faction_of_party, ":center_faction", ":center_no"),
#      (eq, ":center_faction", "fac_player_supporters_faction"),
#      (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player),
#      (this_or_next|party_slot_eq, ":center_no", slot_town_lord, stl_unassigned),
#      (party_slot_eq, ":center_no", slot_town_lord, stl_rejected_by_player),
#      (assign, "$g_center_taken_by_player_faction", ":center_no"),
#    (try_end),
#    (faction_get_slot, ":leader", "fac_player_supporters_faction", slot_faction_leader),

#	(try_begin),
#		(ge, "$g_center_taken_by_player_faction", 0),

#		(eq, "$cheat_mode", 1),
#		(str_store_party_name, s14, "$g_center_taken_by_player_faction"),
#		(display_message, "@{!}{s14} should be assigned to lord"),
#	(try_end),

#    ]),


  # Respawn hero party after kingdom hero is released from captivity.
  (48,
   [
	   ##diplomacy start+ Support promoted kingdom ladies
	   ##OLD:
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
	   ##NEW:
	    (try_for_range, ":troop_no", heroes_begin, heroes_end),
	   ##diplomacy end+
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),

         (str_store_troop_name, s1, ":troop_no"),

         (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
         (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),

         (store_troop_faction, ":cur_faction", ":troop_no"),
         (try_begin),
           (this_or_next|eq, ":cur_faction", "fac_commoners"),  ## CC-D fix: stop to respawn from commoners
           (eq, ":cur_faction", "fac_outlaws"), #Do nothing
         (else_try),
           (try_begin),
             (eq, "$cheat_mode", 2),
             (str_store_troop_name, s4, ":troop_no"),
             (display_message, "str_debug__attempting_to_spawn_s4"),
           (try_end),

           (call_script, "script_cf_select_random_walled_center_with_faction_and_owner_priority_no_siege", ":cur_faction", ":troop_no"),#Can fail
           (assign, ":center_no", reg0),

           (try_begin),
             (eq, "$cheat_mode", 2),
             (str_store_party_name, s7, ":center_no"),
			 (str_store_troop_name, s0, ":troop_no"),
             (display_message, "str_debug__s0_is_spawning_around_party__s7"),
           (try_end),

           (call_script, "script_create_kingdom_hero_party", ":troop_no", ":center_no"),

		   (try_begin),
		     (eq, "$g_there_is_no_avaliable_centers", 0),
             (party_attach_to_party, "$pout_party", ":center_no"),
           (try_end),

           #new
           #(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
		   #(call_script, "script_npc_decision_checklist_party_ai", ":troop_no"), #This handles AI for both marshal and other parties
		   #(call_script, "script_party_set_ai_state", ":party_no", reg0, reg1),
		   #new end

           (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
           (call_script, "script_party_set_ai_state", ":party_no", spai_holding_center, ":center_no"),

         (else_try),
           (neg|faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
           (try_begin),
             (is_between, ":troop_no", kings_begin, kings_end),
             (troop_set_slot, ":troop_no", slot_troop_change_to_faction, "fac_commoners"),
           (else_try),
             (store_random_in_range, ":random_no", 0, 100),
             (lt, ":random_no", 10),
             (call_script, "script_cf_get_random_active_faction_except_player_faction_and_faction", ":cur_faction"),
             (troop_set_slot, ":troop_no", slot_troop_change_to_faction, reg0),
           (try_end),
         (try_end),
       (try_end),
    ]),

  # Spawn merchant caravan parties
##  (3,
##   [
##       (try_for_range, ":troop_no", merchants_begin, merchants_end),
##         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_merchant),
##         (troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
##         (neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 1),
##
##         (call_script, "script_cf_create_merchant_party", ":troop_no"),
##       (try_end),
##    ]),

  # Spawn village farmer parties
  (24,
   [
       (try_for_range, ":village_no", villages_begin, villages_end),
         (party_slot_eq, ":village_no", slot_village_state, svs_normal),
         (party_get_slot, ":farmer_party", ":village_no", slot_village_farmer_party),
         (this_or_next|eq, ":farmer_party", 0),
         (neg|party_is_active, ":farmer_party"),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 60),
         (call_script, "script_create_village_farmer_party", ":village_no"),
         (party_set_slot, ":village_no", slot_village_farmer_party, reg0),
#         (str_store_party_name, s1, ":village_no"),
#         (display_message, "@Village farmers created at {s1}."),
         ## CC-D begin imported from difor 0.058
         (party_get_slot, ":merchant_troop", ":village_no", slot_town_elder),
         (troop_remove_gold, ":merchant_troop", 250),  # create cost
         ## CC-D end

       (try_end),
    ]),


   (72,
   [
  # Updating trade good prices according to the productions
       (call_script, "script_update_trade_good_prices"),
 # Updating player odds
       (try_for_range, ":cur_center", centers_begin, centers_end),
         (party_get_slot, ":player_odds", ":cur_center", slot_town_player_odds),
         (try_begin),
           (gt, ":player_odds", 1000),
           (val_mul, ":player_odds", 95),
           (val_div, ":player_odds", 100),
           (val_max, ":player_odds", 1000),
         (else_try),
           (lt, ":player_odds", 1000),
           (val_mul, ":player_odds", 105),
           (val_div, ":player_odds", 100),
           (val_min, ":player_odds", 1000),
         (try_end),
         (party_set_slot, ":cur_center", slot_town_player_odds, ":player_odds"),
       (try_end),
       ## CC-D begin
       (try_begin),
         (party_get_slot, ":player_odds", "p_ccc_hide_house", slot_town_player_odds),
         (try_begin),
           (gt, ":player_odds", 1000),
           (val_mul, ":player_odds", 95),
           (val_div, ":player_odds", 100),
           (val_max, ":player_odds", 1000),
         (else_try),
           (lt, ":player_odds", 1000),
           (val_mul, ":player_odds", 105),
           (val_div, ":player_odds", 100),
           (val_min, ":player_odds", 1000),
         (try_end),
         (party_set_slot, "p_ccc_hide_house", slot_town_player_odds, ":player_odds"),
       (try_end),
       ## CC-D end
    ]),


  #Troop AI: Merchants thinking
  (4, #CC-C 8->2 occc 2->4
   [
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
         (party_is_in_any_town, ":party_no"),

         (store_faction_of_party, ":merchant_faction", ":party_no"),
         (faction_get_slot, ":num_towns", ":merchant_faction", slot_faction_num_towns),
         (try_begin),
           (le, ":num_towns", 0),
           (remove_party, ":party_no"),
         (else_try),
           (party_get_cur_town, ":cur_center", ":party_no"),
           
           #CC-C begin
           #(store_random_in_range, ":random_no", 0, 100),                               
           
           #(try_begin),
             #(party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
             
             #(game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
             #(try_begin),
               #(eq, ":reduce_campaign_ai", 0), #hard (less money from tariffs)
               #(assign, ":tariff_succeed_limit", 35),
             #(else_try),
               #(eq, ":reduce_campaign_ai", 1), #medium (normal money from tariffs)
               #(assign, ":tariff_succeed_limit", 45),
             #(else_try),
               #(eq, ":reduce_campaign_ai", 2), #easy (more money from tariffs)
               #(assign, ":tariff_succeed_limit", 60),
             #(try_end),                
           #(else_try),  
             #(assign, ":tariff_succeed_limit", 45),
           #(try_end),
                      
           #(lt, ":random_no", ":tariff_succeed_limit"),
           #CC-C end                  

           (assign, ":can_leave", 1),
           (try_begin),
             (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
             (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
             (assign, ":can_leave", 0),
           (try_end),
           (eq, ":can_leave", 1),

           (assign, ":do_trade", 0),
           (try_begin),
             (party_get_slot, ":cur_ai_state", ":party_no", slot_party_ai_state),
             (eq, ":cur_ai_state", spai_trading_with_town),
             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
             (eq, ":cur_center", ":cur_ai_object"),
             (assign, ":do_trade", 1),
             #CC-C begin occc mildmode
			 (assign, ":total_population", 0),
			 (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
			 (try_for_range, ":i_stack", 0, ":num_stacks"),
				#(party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),#need to fix
				(party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
				(val_add, ":total_population", ":stack_size"),
			 (try_end),
			
			 (try_begin),
				(eq, "$cheat_mode", 1),
				(assign, reg0, ":total_population"),
				(display_message, "@{!}DEBUGS : caravan population : {reg0}"),
			 (try_end),

			 (try_begin),
			  (eq, "$g_occc_mildmode", 0),
			  #(lt,":total_population",1000),#occc cap
              #(party_add_members,":party_no","trp_caravan_guard",3),
              #(store_random_in_range, ":r", 0, 3),
              #(party_add_members,":party_no","trp_caravan_elite_guard",":r"),
				## CC-D begin: expand improvement imported from 0.58
				(assign, ":size_limit", 150),
				(assign, ":top", 4),
				(try_begin),
					(party_slot_eq, ":cur_center", slot_center_has_assembly_hall, 1),
					(assign, ":size_limit", 200),
					(assign, ":top", 6),
				(try_end),
				(party_get_num_companions, ":cur_party_size", ":party_no"),
				(lt, ":cur_party_size", ":size_limit"),
				(store_random_in_range, ":r", 0, ":top"),
				(try_begin),
					(eq, ":r", 0),
					(store_random_in_range, ":r", 1, 3),
					(party_remove_members, ":party_no", "trp_caravan_guard", ":r"),
				(else_try),
					(ge, ":r", 2),
					(party_add_members, ":party_no", "trp_caravan_guard", 3),
					(store_random_in_range, ":r", 0, 2),
					(party_add_members, ":party_no", "trp_caravan_elite_guard", ":r"),
				(try_end),
             ## CC-D end imported from 0.58

             (else_try),
			  (lt,":total_population",48),
              (party_add_members,":party_no","trp_caravan_guard",2),
              (store_random_in_range, ":r", 0, 2),
              (party_add_members,":party_no","trp_caravan_elite_guard",":r"),
			 (try_end),
             #CC-C end
			 #occc caravan training
             (party_upgrade_with_xp, ":party_no", 500),			 
           (try_end),

           (assign, ":target_center", -1),

           (try_begin), #Make sure escorted caravan continues to its original destination.
             (eq, "$caravan_escort_party_id", ":party_no"),
             (neg|party_is_in_town, ":party_no", "$caravan_escort_destination_town"),
             (assign, ":target_center", "$caravan_escort_destination_town"),
           (else_try),
		     ##diplomacy start+ added third parameter "-1" to use the town's location
             (call_script, "script_cf_select_most_profitable_town_at_peace_with_faction_in_trade_route", ":cur_center", ":merchant_faction",
				-1),
			 ##diplomacy end+
             (assign, ":target_center", reg0),
           (try_end),
           (is_between, ":target_center", towns_begin, towns_end),
           (neg|party_is_in_town, ":party_no", ":target_center"),

           (try_begin),
             (eq, ":do_trade", 1),
             (str_store_party_name, s7, ":cur_center"),
             (call_script, "script_do_merchant_town_trade", ":party_no", ":cur_center"),
           (try_end),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":target_center"),
           (party_set_flags, ":party_no", pf_default_behavior, 0),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_slot, ":party_no", slot_party_ai_object, ":target_center"),
         (try_end),
       (try_end),
    ]),

  #Troop AI: Village farmers thinking
  (8,
   [
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_village_farmer),
         (party_is_in_any_town, ":party_no"),
         (party_get_slot, ":home_center", ":party_no", slot_party_home_center),
         (party_get_cur_town, ":cur_center", ":party_no"),

         (assign, ":can_leave", 1),
         (try_begin),
           (is_between, ":cur_center", walled_centers_begin, walled_centers_end),
           (neg|party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
           (assign, ":can_leave", 0),
         (try_end),
         (eq, ":can_leave", 1),

         (try_begin),
           (eq, ":cur_center", ":home_center"),

		   #Peasants trade in their home center
		   (call_script, "script_do_party_center_trade", ":party_no", ":home_center", 3), #this needs to be the same as the center
		   (assign, ":total_change", reg0),  ## CC-D add
		   (store_faction_of_party, ":center_faction", ":cur_center"),
           (party_set_faction, ":party_no", ":center_faction"),
           (party_get_slot, ":market_town", ":home_center", slot_village_market_town),
           (party_set_slot, ":party_no", slot_party_ai_object, ":market_town"),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":market_town"),
           ## CC-D begin imported from difor v 0.058
           (party_get_slot, ":prosperity", ":cur_center", slot_town_prosperity),
           (val_mul, ":total_change", ":prosperity"),
           (val_div, ":total_change", 1000),  # trade profit, ave400 probably
		  #occc start
		   (try_begin),
				(party_slot_eq, ":cur_center", slot_center_has_market, 1),
				(val_mul, ":total_change", 2),
		   (try_end),
		  #occc end
           (val_sub, ":total_change", 50),  # resend cost
           (party_get_slot, ":merchant_troop", ":cur_center", slot_town_elder),
           (troop_add_gold, ":merchant_troop", ":total_change"),
           (call_script, "script_ccd_give_prisoners_as_slave", ":party_no", ":cur_center"),  # get prisoners as slaves
           ## CC-D end
         (else_try),
           (try_begin),
             (party_get_slot, ":cur_ai_object", ":party_no", slot_party_ai_object),
             (eq, ":cur_center", ":cur_ai_object"),

             (call_script, "script_do_party_center_trade", ":party_no", ":cur_ai_object", 3), #raised from 10
             (assign, ":total_change", reg0),
		     #This is roughly 50% of what a caravan would pay

             #Adding tariffs to the town
             (party_get_slot, ":accumulated_tariffs", ":cur_ai_object", slot_center_accumulated_tariffs),
             (party_get_slot, ":prosperity", ":cur_ai_object", slot_town_prosperity),

			 (assign, ":tariffs_generated", ":total_change"),
			 (val_mul, ":tariffs_generated", ":prosperity"),
			 ##diplomacy start+
			 (val_add, ":tariffs_generated", 50),#round properly
			 ##diplomacy end+
			 (val_div, ":tariffs_generated", 100),
			 ##diplomacy start+
			 (val_div, ":tariffs_generated", 5),#round properly
			 ##diplomacy end+
			 (val_div, ":tariffs_generated", 20), #10 for caravans, 20 for villages
			 (val_add, ":accumulated_tariffs", ":tariffs_generated"),
			 ##diplomacy begin
        (try_begin), #no tariffs for infested villages and towns
          (party_slot_ge, ":cur_ai_object", slot_village_infested_by_bandits, 1),
          (assign,":accumulated_tariffs", 0),
        (try_end),
	     ##diplomacy end
			 (try_begin),
				(ge, "$cheat_mode", 3),
				(assign, reg4, ":tariffs_generated"),
				(str_store_party_name, s4, ":cur_ai_object"),
				(assign, reg5, ":accumulated_tariffs"),
				(display_message, "@{!}New tariffs at {s4} = {reg4}, total = {reg5}"),
			 (try_end),

             (party_set_slot, ":cur_ai_object", slot_center_accumulated_tariffs, ":accumulated_tariffs"),

             #Increasing food stocks of the town
             (party_get_slot, ":town_food_store", ":cur_ai_object", slot_party_food_store),
             (call_script, "script_center_get_food_store_limit", ":cur_ai_object"),
             (assign, ":food_store_limit", reg0),
             (val_add, ":town_food_store", 1000),
             (val_min, ":town_food_store", ":food_store_limit"),
             (party_set_slot, ":cur_ai_object", slot_party_food_store, ":town_food_store"),

             #Adding 1 to village prosperity
             (try_begin),
               (store_random_in_range, ":rand", 0, 100),
               (lt, ":rand", 5), #was 35
               (call_script, "script_change_center_prosperity", ":home_center", 1),
			   (val_add, "$newglob_total_prosperity_from_village_trade", 1),
             (try_end),
           (try_end),

           #Moving farmers to their home village
           (party_set_slot, ":party_no", slot_party_ai_object, ":home_center"),
           (party_set_slot, ":party_no", slot_party_ai_state, spai_trading_with_town),
           (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
           (party_set_ai_object, ":party_no", ":home_center"),
         (try_end),
       (try_end),
    ]),

 #Increase castle food stores
  (2,
   [
   ##diplomacy start+ Change to vary with village prosperity
   (try_begin),
       (lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),
       ##OLD:
       #unaltered block begin
       (try_for_range, ":center_no", castles_begin, castles_end),
         (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #castle is not under siege
         (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
         (val_add, ":center_food_store", 100),
         (call_script, "script_center_get_food_store_limit", ":center_no"),
         (assign, ":food_store_limit", reg0),
         (val_min, ":center_food_store", ":food_store_limit"),
         (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
       (try_end),
       #unaltered block end
   (else_try),
       ##NEW:
       (try_for_range, ":village_no", villages_begin, villages_end),
          (neg|party_slot_ge, ":village_no", slot_center_is_besieged_by, 0),
          (party_slot_eq, ":village_no", slot_village_state, svs_normal),
          (party_get_slot, ":center_no", ":village_no", slot_village_bound_center),
          (is_between, ":center_no", castles_begin, castles_end),
          (neg|party_slot_ge, ":center_no", slot_center_is_besieged_by, 0),
          (party_get_slot, ":center_food_store", ":center_no", slot_party_food_store),
          (party_get_slot, reg0, ":village_no", slot_town_prosperity),
          (val_add, reg0, 75),
          (val_mul, reg0, 100),#base addition is 100
          (val_add, reg0, 62),
          (val_div, reg0, 125),#plus or minus 40%
          (val_add, ":center_food_store", reg0),
          (call_script, "script_center_get_food_store_limit", ":center_no"),
          (assign, ":food_store_limit", reg0),
          (val_min, ":center_food_store", ":food_store_limit"),
          (party_set_slot, ":center_no", slot_party_food_store, ":center_food_store"),
       (try_end),
   (try_end),
   ]),

 #cache party strengths (to avoid re-calculating)
##  (2,
##   [
##       (try_for_range, ":cur_troop", heroes_begin, heroes_end),
##         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
##         (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
##         (ge, ":cur_party", 0),
##         (call_script, "script_party_calculate_strength", ":cur_party", 0), #will update slot_party_cached_strength
##       (try_end),
##    ]),
##
##  (6,
##   [
##       (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
##         (call_script, "script_party_calculate_strength", ":cur_center", 0), #will update slot_party_cached_strength
##       (try_end),
##    ]),

##  (1,
##   [
##       (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
##         (store_random_in_range, ":rand", 0, 100),
##         (lt, ":rand", 10),
##         (store_faction_of_party, ":center_faction", ":cur_center"),
##         (assign, ":friend_strength", 0),
##         (try_for_range, ":cur_troop", heroes_begin, heroes_end),
##           (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
##           (troop_get_slot, ":cur_troop_party", ":cur_troop", slot_troop_leaded_party),
##           (gt, ":cur_troop_party", 0),
##           (store_distance_to_party_from_party, ":distance", ":cur_troop_party", ":cur_center"),
##           (lt, ":distance", 10),
##           (store_troop_faction, ":army_faction", ":cur_troop"),
##           (store_relation, ":rel", ":army_faction", ":center_faction"),
##           (try_begin),
##             (gt, ":rel", 10),
##             (party_get_slot, ":str", ":cur_troop_party", slot_party_cached_strength),
##             (val_add, ":friend_strength", ":str"),
##           (try_end),
##         (try_end),
##         (party_set_slot, ":cur_center", slot_party_nearby_friend_strength, ":friend_strength"),
##       (try_end),
##    ]),

  # Make heroes running away from someone retreat to friendly centers
  (0.5,
   [
       (try_for_range, ":cur_troop", heroes_begin, heroes_end),
         (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
         (gt, ":cur_party", 0),
         (try_begin),
           (party_is_active, ":cur_party"),
           (try_begin),
             (get_party_ai_current_behavior, ":ai_bhvr", ":cur_party"),
             (eq, ":ai_bhvr", ai_bhvr_avoid_party),

			 #Certain lord personalities will not abandon a battlefield to flee to a fortress
			 (assign, ":continue", 1),
			 (try_begin),
				(this_or_next|troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_upstanding),
					(troop_slot_eq, ":cur_troop", slot_lord_reputation_type, lrep_martial),
				(get_party_ai_current_object, ":ai_object", ":cur_party"),
				(party_is_active, ":ai_object"),
				(party_get_battle_opponent, ":battle_opponent", ":ai_object"), #CC-C begin
				(party_is_active, ":battle_opponent"), #CC-C begin
				(assign, ":continue", 0),
			 (try_end),
			 (eq, ":continue", 1),


             (store_faction_of_party, ":party_faction", ":cur_party"),
             (party_get_slot, ":commander_party", ":cur_party", slot_party_commander_party),
             (faction_get_slot, ":faction_marshall", ":party_faction", slot_faction_marshall),
             (neq, ":faction_marshall", ":cur_troop"),
             (assign, ":continue", 1),
             (try_begin),
               (ge, ":faction_marshall", 0),
               (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
               (party_is_active, ":faction_marshall_party", 0),
               (eq, ":commander_party", ":faction_marshall_party"),
               (assign, ":continue", 0),
             (try_end),
             #CC-C begin lord reterat
             #(eq, ":continue", 1),
             #(try_begin),
               #(faction_slot_eq, ":party_faction", slot_faction_ai_state, spai_accompanying_army),
               #(ge, ":faction_marshall", 0),
               #(neq,":faction_marshall",":cur_troop"),
               #(troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
               #(party_is_active, ":faction_marshall_party"),
               #(neg|party_slot_eq, ":faction_marshall_party", slot_party_ai_state, spai_retreating_to_center), 
               #(store_distance_to_party_from_party, ":cur_distance", ":cur_party", ":faction_marshall_party"),
               #(le,":cur_distance",lord_retreat_distance),
               #(assign, ":continue", 0),
             #(try_end),
             #CC-C end lord reterat
             (eq, ":continue", 1),
             (assign, ":done", 0),
             (try_for_range, ":cur_center", walled_centers_begin, walled_centers_end),
               (eq, ":done", 0),
               (party_slot_eq, ":cur_center", slot_center_is_besieged_by, -1),
               (store_faction_of_party, ":center_faction", ":cur_center"),
               (store_relation, ":cur_relation", ":center_faction", ":party_faction"),
               (gt, ":cur_relation", 0),
               (store_distance_to_party_from_party, ":cur_distance", ":cur_party", ":cur_center"),
               (lt, ":cur_distance", 20),
               (party_get_position, pos1, ":cur_party"),
               (party_get_position, pos2, ":cur_center"),
               (neg|position_is_behind_position, pos2, pos1),
               (call_script, "script_party_set_ai_state", ":cur_party", spai_retreating_to_center, ":cur_center"),
               (assign, ":done", 1),
             (try_end),
           (try_end),
         (else_try),
           (troop_set_slot, ":cur_troop", slot_troop_leaded_party, -1),
         (try_end),
       (try_end),
    ]),

  # Centers give alarm if the player is around
  (0.5,
   [
     (store_current_hours, ":cur_hours"),
     (store_mod, ":cur_hours_mod", ":cur_hours", 11),
     (store_sub, ":hour_limit", ":cur_hours", 5),
     (party_get_num_companions, ":num_men", "p_main_party"),
     (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
     (val_add, ":num_men", ":num_prisoners"),
     (convert_to_fixed_point, ":num_men"),
     (store_sqrt, ":num_men_effect", ":num_men"),
     (convert_from_fixed_point, ":num_men_effect"),
     (try_begin),
       (eq, ":cur_hours_mod", 0),
       #Reduce alarm by 2 in every 11 hours.
       (try_for_range, ":cur_faction", kingdoms_begin, kingdoms_end),
         (faction_get_slot, ":player_alarm", ":cur_faction", slot_faction_player_alarm),
         (val_sub, ":player_alarm", 1),
         (val_max, ":player_alarm", 0),
         (faction_set_slot, ":cur_faction", slot_faction_player_alarm, ":player_alarm"),
       (try_end),
     (try_end),
     (eq, "$g_player_is_captive", 0),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (store_faction_of_party, ":cur_faction", ":cur_center"),
       (store_relation, ":reln", ":cur_faction", "fac_player_supporters_faction"),
       (lt, ":reln", 0),
       (store_distance_to_party_from_party, ":dist", "p_main_party", ":cur_center"),
       (lt, ":dist", 5),
       (store_mul, ":dist_sqr", ":dist", ":dist"),
       (store_sub, ":dist_effect", 20, ":dist_sqr"),
       (store_sub, ":reln_effect", 20, ":reln"),
       (store_mul, ":total_effect", ":dist_effect", ":reln_effect"),
       (val_mul, ":total_effect", ":num_men_effect"),
       (store_div, ":spot_chance", ":total_effect", 10),
       (store_random_in_range, ":random_spot", 0, 1000),
       (lt, ":random_spot", ":spot_chance"),
       (faction_get_slot, ":player_alarm", ":cur_faction", slot_faction_player_alarm),
       (val_add, ":player_alarm", 1),
       (val_min, ":player_alarm", 100),
       (faction_set_slot, ":cur_faction", slot_faction_player_alarm, ":player_alarm"),
       (try_begin),
         (neg|party_slot_ge, ":cur_center", slot_center_last_player_alarm_hour, ":hour_limit"),
         (str_store_party_name_link, s1, ":cur_center"),
         (display_message, "@Your party is spotted by {s1}."),
         (party_set_slot, ":cur_center", slot_center_last_player_alarm_hour, ":cur_hours"),
       (try_end),
     (try_end),
    ]),

## CC
  # Consuming food at every 14 hours
#CC-C begin food mendoi
  (140,
#CC-C end food mendoi
   [
	(eq, "$g_occc_mildmode", 0),
    (eq, "$g_player_is_captive", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
    (assign, ":num_men", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
      (val_add, ":num_men", ":stack_size"),
    (try_end),
    (val_div, ":num_men", 3),
    (try_begin),
      (eq, ":num_men", 0),
      (val_add, ":num_men", 1),
    (try_end),

    (try_begin),
      (assign, ":number_of_foods_player_has", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (val_add, ":number_of_foods_player_has", 1),
      (try_end),
      (try_begin),
        (ge, ":number_of_foods_player_has", 6),
        (unlock_achievement, ACHIEVEMENT_ABUNDANT_FEAST),
        (call_script, "script_ccd_record_achievement", ACHIEVEMENT_ABUNDANT_FEAST),  ## CC-D add: for local achievement
      (try_end),
    (try_end),

    (assign, ":consumption_amount", ":num_men"),
    (assign, ":no_food_displayed", 0),
    (try_for_range, ":unused", 0, ":consumption_amount"),
      (assign, ":available_food", 0),
      (try_for_range, ":cur_food", food_begin, food_end),
        (item_set_slot, ":cur_food", slot_item_is_checked, 0),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
        (val_add, ":available_food", 1),
      (try_end),
      (try_begin),
        (gt, ":available_food", 0),
        (store_random_in_range, ":selected_food", 0, ":available_food"),
        (call_script, "script_consume_food", ":selected_food"),
      (else_try),
        (eq, ":no_food_displayed", 0),
        (display_message, "@Party has nothing to eat!", 0xFF0000),
        (call_script, "script_change_player_party_morale", -3),
        (assign, ":no_food_displayed", 1),
#NPC companion changes begin
        (try_begin),
            (call_script, "script_party_count_fit_regulars", "p_main_party"),
            (gt, reg0, 0),
            (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_hungry"),
        (try_end),
#NPC companion changes end
      (try_end),
    (try_end),
#    ]),

## CC???
# Party Morale: Move morale towards target value.
#    (call_script, "script_get_player_party_morale_values"),
#    (assign, ":target_morale", reg1),
#    (party_get_morale, ":cur_morale", "p_main_party"),
#    (store_sub, ":dif", ":target_morale", ":cur_morale"),
#    # leadership modifier 
#    (store_skill_level, ":skill", "skl_leadership", "trp_player"),
#    (try_begin),
#      (gt, ":dif", 0),
#      (store_add, ":morale_change_factor", 20, ":skill"),
#    (else_try),
#      (store_sub, ":morale_change_factor", 20, ":skill"),
#    (try_end),
#    (store_mul, ":dif_to_add", ":dif", ":morale_change_factor"),
#    (val_div, ":dif_to_add", 100),
#    (store_mul, ":dif_to_add_correction", ":dif_to_add", 100),
#    (val_div, ":dif_to_add_correction", ":morale_change_factor"),
#    # leadership modifier 
#    (try_begin),#finding ceiling of the value
#      (neq, ":dif_to_add_correction", ":dif"),
#      (try_begin),
#        (gt, ":dif", 0),
#        (val_add, ":dif_to_add", 1),
#      (else_try),
#        (val_sub, ":dif_to_add", 1),
#      (try_end),
#    (try_end),
#    (val_add, ":cur_morale", ":dif_to_add"),
#    (val_clamp, ":cur_morale", 0, 100),
#    (party_set_morale, "p_main_party", ":cur_morale"),
#    (assign, reg1, ":cur_morale"),
#    (display_message, "@Current party morale is {reg1}."),
## CC sort_food
    (call_script, "script_sort_food", "trp_player"),
  ]),
## occc start
  (28,
#occc food hard mode
   [
	(eq, "$g_occc_mildmode", 1),
    (eq, "$g_player_is_captive", 0),
    (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
    (assign, ":num_men", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (party_stack_get_size, ":stack_size","p_main_party",":i_stack"),
      (val_add, ":num_men", ":stack_size"),
    (try_end),
    (val_div, ":num_men", 3),
    (try_begin),
      (eq, ":num_men", 0),
      (val_add, ":num_men", 1),
    (try_end),

    (try_begin),
      (assign, ":number_of_foods_player_has", 0),
      (try_for_range, ":cur_edible", food_begin, food_end),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_edible", imod_rotten),
        (val_add, ":number_of_foods_player_has", 1),
      (try_end),
      (try_begin),
        (ge, ":number_of_foods_player_has", 6),
        (unlock_achievement, ACHIEVEMENT_ABUNDANT_FEAST),
        (call_script, "script_ccd_record_achievement", ACHIEVEMENT_ABUNDANT_FEAST),  ## CC-D add: for local achievement
      (try_end),
    (try_end),

    (assign, ":consumption_amount", ":num_men"),
    (assign, ":no_food_displayed", 0),
    (try_for_range, ":unused", 0, ":consumption_amount"),
      (assign, ":available_food", 0),
      (try_for_range, ":cur_food", food_begin, food_end),
        (item_set_slot, ":cur_food", slot_item_is_checked, 0),
        (call_script, "script_cf_player_has_item_without_modifier", ":cur_food", imod_rotten),
        (val_add, ":available_food", 1),
      (try_end),
      (try_begin),
        (gt, ":available_food", 0),
        (store_random_in_range, ":selected_food", 0, ":available_food"),
        (call_script, "script_consume_food", ":selected_food"),
      (else_try),
        (eq, ":no_food_displayed", 0),
        (display_message, "@Party has nothing to eat!", 0xFF0000),
        (call_script, "script_change_player_party_morale", -3),
        (assign, ":no_food_displayed", 1),
#NPC companion changes begin
        (try_begin),
            (call_script, "script_party_count_fit_regulars", "p_main_party"),
            (gt, reg0, 0),
            (call_script, "script_objectionable_action", tmt_egalitarian, "str_men_hungry"),
        (try_end),
#NPC companion changes end
      (try_end),
    (try_end),

    (call_script, "script_sort_food", "trp_player"),
  ]),
#occc end


  # Setting item modifiers for food
  (48,#occc 24->48 
   [
     (troop_get_inventory_capacity, ":inv_size", "trp_player"),
     (try_for_range, ":i_slot", 0, ":inv_size"),
       (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
       (this_or_next|eq, ":item_id", "itm_cattle_meat"),
       (this_or_next|eq, ":item_id", "itm_chicken"),
		(eq, ":item_id", "itm_pork"),

       (troop_get_inventory_slot_modifier, ":modifier", "trp_player", ":i_slot"),
       (try_begin),
         (ge, ":modifier", imod_fresh),
         (lt, ":modifier", imod_rotten),
         (val_add, ":modifier", 1),
         (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", ":modifier"),
       (else_try),
         (lt, ":modifier", imod_fresh),
         (troop_set_inventory_slot_modifier, "trp_player", ":i_slot", imod_fresh),
       (try_end),
     (try_end),
    ]),

  # Assigning lords to centers with no leaders
  (72,
   [
   #(call_script, "script_assign_lords_to_empty_centers"),
    ]),
  
  # Updating player icon in every frame
  (0,
   [
    (troop_get_inventory_slot, ":cur_horse", "trp_player", 8), #horse slot
    (assign, ":new_icon", -1),
    (try_begin),
      (eq, "$g_player_icon_state", pis_normal),
      (try_begin),
        (ge, ":cur_horse", 0),
        (assign, ":new_icon", "icon_player_horseman"),
      (else_try),
        (assign, ":new_icon", "icon_player"),
      (try_end),
    (else_try),
      (eq, "$g_player_icon_state", pis_camping),
      (assign, ":new_icon", "icon_camp"),
    (else_try),
      (eq, "$g_player_icon_state", pis_ship),
      (assign, ":new_icon", "icon_ship"),
    (try_end),

    #occc test start
    (try_begin),
      (call_script, "script_cf_is_party_on_water", "p_main_party"),
      (assign, ":new_icon", "icon_ship"),#icon_longship
    (try_end),
    ##occc end	

    (neq, ":new_icon", "$g_player_party_icon"),
    (assign, "$g_player_party_icon", ":new_icon"),
    (party_set_icon, "p_main_party", ":new_icon"),
    ]),

 #Update how good a target player is for bandits
  (2,
   [
       (store_troop_gold, ":total_value", "trp_player"),
       (store_div, ":bandit_attraction", ":total_value", (10000/100)), #10000 gold = excellent_target

       (troop_get_inventory_capacity, ":inv_size", "trp_player"),
       (try_for_range, ":i_slot", 0, ":inv_size"),
         (troop_get_inventory_slot, ":item_id", "trp_player", ":i_slot"),
         (ge, ":item_id", 0),
         (try_begin),
           (is_between, ":item_id", trade_goods_begin, trade_goods_end),
           (store_item_value, ":item_value", ":item_id"),
           (val_add, ":total_value", ":item_value"),
         (try_end),
       (try_end),
       (val_clamp, ":bandit_attraction", 0, 100),
       (party_set_bandit_attraction, "p_main_party", ":bandit_attraction"),
    ]),


	#This is a backup script to activate the player faction if it doesn't happen automatically, for whatever reason
  (3,
	[
	(try_for_range, ":center", walled_centers_begin, walled_centers_end),
		(faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_inactive),
		(store_faction_of_party, ":center_faction", ":center"),
		(eq, ":center_faction", "fac_player_supporters_faction"),
		(call_script, "script_activate_player_faction", "trp_player"),
	(try_end),
	##diplomacy start+
	#Piggyback on this: if the minister somehow gets cleared, or wasn't set
	#automatically, reappoint one.
	(try_begin),
		(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
		(le, "$g_player_minister", 0),
		(faction_get_slot, ":faction_leader", "$players_kingdom", slot_faction_leader),
		(ge, ":faction_leader", 0),
		(try_begin),
			(this_or_next|eq, ":faction_leader", "trp_player"),
				(troop_slot_eq, "trp_player", slot_troop_spouse, ":faction_leader"),
			(assign, "$g_player_minister", "trp_temporary_minister"),
			(troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
		(else_try),
			(is_between, ":faction_leader", heroes_begin, heroes_end),
			(troop_slot_eq, ":faction_leader", slot_troop_spouse, "trp_player"),
			(assign, "$g_player_minister", "trp_temporary_minister"),
			(troop_set_faction, "trp_temporary_minister", "fac_player_supporters_faction"),
		(try_end),
	(try_end),
	##diplomacy end+
	]),

  # Checking escape chances of prisoners that joined the party recently.
  (6,
   [(gt, "$g_prisoner_recruit_troop_id", 0),
    (gt, "$g_prisoner_recruit_size", 0),
    (gt, "$g_prisoner_recruit_last_time", 0),
    (is_currently_night),
    (try_begin),
      (store_skill_level, ":leadership", "skl_leadership", "trp_player"),
      (val_mul, ":leadership", 5),
      (store_sub, ":chance", 66, ":leadership"),
      (gt, ":chance", 0),
      (assign, ":num_escaped", 0),
      (try_for_range, ":unused", 0, "$g_prisoner_recruit_size"),
        (store_random_in_range, ":random_no", 0, 100),
        (lt, ":random_no", ":chance"),
        (val_add, ":num_escaped", 1),
      (try_end),
      (party_remove_members, "p_main_party", "$g_prisoner_recruit_troop_id", ":num_escaped"),
      (assign, ":num_escaped", reg0),
      (gt, ":num_escaped", 0),
      (try_begin),
        (gt, ":num_escaped", 1),
        (assign, reg2, 1),
      (else_try),
        (assign, reg2, 0),
      (try_end),
      (assign, reg1, ":num_escaped"),
      (str_store_troop_name_by_count, s1, "$g_prisoner_recruit_troop_id", ":num_escaped"),
      (display_log_message, "@{reg1} {s1} {reg2?have:has} escaped from your party during the night."),
      ## CC begin
      (set_spawn_radius, 3),
      (spawn_around_party, "p_main_party", "pt_deserters"),
      (assign, ":new_party", reg0),
      (party_clear, ":new_party"),
      (party_add_members, ":new_party", "$g_prisoner_recruit_troop_id", ":num_escaped"),
      ## CC end
    (try_end),
    (assign, "$g_prisoner_recruit_troop_id", 0),
    (assign, "$g_prisoner_recruit_size", 0),
    ]),

  # Offering ransom fees for player's prisoner heroes
  (24,
   [(neq, "$g_ransom_offer_rejected", 1),
    (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", "p_main_party"),
    (eq, reg0, 0),#no prisoners offered
    (assign, ":end_cond", walled_centers_end),
    (try_for_range, ":center_no", walled_centers_begin, ":end_cond"),
      (party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
      (call_script, "script_offer_ransom_amount_to_player_for_prisoners_in_party", ":center_no"),
      (eq, reg0, 1),#a prisoner is offered
      (assign, ":end_cond", 0),#break
    (try_end),
    ]),

  # Exchanging hero prisoners between factions and clearing old ransom offers
  (72,
   [(assign, "$g_ransom_offer_rejected", 0),
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
      (gt, ":town_lord", 0),
      (party_get_num_prisoner_stacks, ":num_stacks", ":center_no"),
      (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", ":center_no", ":i_stack"),
        (troop_is_hero, ":stack_troop"),
        (troop_slot_eq, ":stack_troop", slot_troop_occupation, slto_kingdom_hero),
        (store_random_in_range, ":random_no", 0, 100),
        (try_begin),
          (le, ":random_no", 10),
          (call_script, "script_calculate_ransom_amount_for_troop", ":stack_troop"),
          (assign, ":ransom_amount", reg0),
          ##diplomacy start+ Remove the wealth from the stack troop
          (call_script, "script_dplmc_remove_gold_from_lord_and_holdings", ":ransom_amount", ":stack_troop"),
          ##diplomacy end+
          (troop_get_slot, ":wealth", ":town_lord", slot_troop_wealth),
          (val_add, ":wealth", ":ransom_amount"),
          (troop_set_slot, ":town_lord", slot_troop_wealth, ":wealth"),
          (party_remove_prisoners, ":center_no", ":stack_troop", 1),
          (call_script, "script_remove_troop_from_prison", ":stack_troop"),
          (store_troop_faction, ":faction_no", ":town_lord"),
          (store_troop_faction, ":troop_faction", ":stack_troop"),
          (str_store_troop_name, s1, ":stack_troop"),
          (str_store_faction_name, s2, ":faction_no"),
          (str_store_faction_name, s3, ":troop_faction"),
          ## CC begin
          (faction_get_color, ":faction_color", ":troop_faction"),
          (display_log_message, "@{s1} of {s3} has been released from captivity.", ":faction_color"),
          ## CC end
        (try_end),
      (try_end),
    (try_end),
    ]),

  # Adding mercenary troops to the towns
  (72,
   [
#CC-C begin
#     (call_script, "script_update_mercenary_units_of_towns"),
     (call_script, "script_ccc_update_mercenary_units_of_towns"),
#CC-C end
     #NPC changes begin
     # removes   (call_script, "script_update_companion_candidates_in_taverns"),
     #NPC changes end
     (call_script, "script_update_ransom_brokers"),
     (call_script, "script_update_tavern_travellers"),
     (call_script, "script_update_tavern_minstrels"),
     (call_script, "script_update_ranger_master"), ## CC
     (call_script, "script_update_booksellers"),
     (call_script, "script_update_villages_infested_by_bandits"),
     (try_for_range, ":village_no", villages_begin, villages_end),
       (call_script, "script_update_volunteer_troops_in_village", ":village_no"),
       (call_script, "script_update_npc_volunteer_troops_in_village", ":village_no"),
     (try_end),
    ]),

  (24,
   [
    (call_script, "script_update_other_taverngoers"),
	]),

  # Setting random walker types
  (36,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
      (             party_slot_eq, ":center_no", slot_party_type, spt_village),
      (call_script, "script_center_remove_walker_type_from_walkers", ":center_no", walkert_needs_money),
      (call_script, "script_center_remove_walker_type_from_walkers", ":center_no", walkert_needs_money_helped),
      (store_random_in_range, ":rand", 0, 100),
      (try_begin),
        (lt, ":rand", 70),
        (neg|party_slot_ge, ":center_no", slot_town_prosperity, 60),
        (call_script, "script_cf_center_get_free_walker", ":center_no"),
        (call_script, "script_center_set_walker_to_type", ":center_no", reg0, walkert_needs_money),
      (try_end),
    (try_end),
    ]),

  # Checking center upgrades
  (12,
   [(try_for_range, ":center_no", centers_begin, centers_end),
      (party_get_slot, ":cur_improvement", ":center_no", slot_center_current_improvement),
      (gt, ":cur_improvement", 0),
      (party_get_slot, ":cur_improvement_end_time", ":center_no", slot_center_improvement_end_hour),
      (store_current_hours, ":cur_hours"),
      (ge, ":cur_hours", ":cur_improvement_end_time"),
      (party_set_slot, ":center_no", ":cur_improvement", 1),
      (party_set_slot, ":center_no", slot_center_current_improvement, 0),
      (call_script, "script_get_improvement_details", ":cur_improvement"),
	  #occc begin
	  (party_get_slot, ":lord", ":center_no", slot_town_lord),
	  (ge,":lord",0),
	  
      (try_begin),#temple completed
		(eq,":cur_improvement",slot_center_has_temple),
		(troop_get_slot, ":religion", ":lord", slot_troop_religion),
		(try_begin),
			(eq, ":religion",0),
			(store_random_in_range,":religion",reli_saint_cross,reli_oldgods_of_fertility),
		(try_end),
		#occc convert center
		(party_set_slot, ":center_no", slot_center_has_temple, ":religion"),
		#(party_set_slot, ":center_no", slot_center_religion, ":religion"),
      (try_end),
	  
	  #occc end
      (try_begin),
        #(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
		(eq,":lord","trp_player"),
        (str_store_party_name, s4, ":center_no"),
        (display_log_message, "@Building of {s0} in {s4} has been completed."),
        (play_sound, "snd_distant_carpenter"), ## CC-D add
      (try_end),
      (try_begin),
        (is_between, ":center_no", villages_begin, villages_end),
        (eq, ":cur_improvement", slot_center_has_fish_pond),
        (call_script, "script_change_center_prosperity", ":center_no", 5),
      (try_end),
    (try_end),
    ]),

  # Adding tournaments to towns
  # Adding bandits to towns and villages
  (24,
   [(assign, ":num_active_tournaments", 0),
    (try_for_range, ":center_no", towns_begin, towns_end),
      (party_get_slot, ":has_tournament", ":center_no", slot_town_has_tournament),
      (try_begin),
        (eq, ":has_tournament", 1),#tournament ended, simulate
        (call_script, "script_fill_tournament_participants_troop", ":center_no", 0),
        (call_script, "script_sort_tournament_participant_troops"),#may not be needed
        (call_script, "script_get_num_tournament_participants"),
        (store_sub, ":needed_to_remove_randomly", reg0, 1),
        (call_script, "script_remove_tournament_participants_randomly", ":needed_to_remove_randomly"),
        (call_script, "script_sort_tournament_participant_troops"),
        (troop_get_slot, ":winner_troop", "trp_tournament_participants", 0),
        (try_begin),
          (is_between, ":winner_troop", active_npcs_begin, active_npcs_end),
          (str_store_troop_name_link, s1, ":winner_troop"),
          (str_store_party_name_link, s2, ":center_no"),
          (display_message, "@{s1} has won the tournament at {s2}."),
          (call_script, "script_change_troop_renown", ":winner_troop", 20),
          (call_script, "script_ccc_change_troop_wealth", ":winner_troop", 5000),  ## CC-D add: NPC winner get denar
        (try_end),
      (try_end),
      (val_sub, ":has_tournament", 1),
      (val_max, ":has_tournament", 0),
      (party_set_slot, ":center_no", slot_town_has_tournament, ":has_tournament"),
      (try_begin),
        (gt, ":has_tournament", 0),
        (val_add, ":num_active_tournaments", 1),
      (try_end),
    (try_end),

    (try_for_range, ":center_no", centers_begin, centers_end),
      (this_or_next|party_slot_eq, ":center_no", slot_party_type, spt_town),
      (party_slot_eq, ":center_no", slot_party_type, spt_village),
      (party_get_slot, ":has_bandits", ":center_no", slot_center_has_bandits),
      (try_begin),
        (le, ":has_bandits", 0),
        (assign, ":continue", 0),
        (try_begin),
          (check_quest_active, "qst_deal_with_night_bandits"),
          (quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, ":center_no"),
          (neg|check_quest_succeeded, "qst_deal_with_night_bandits"),
          (assign, ":continue", 1),
        (else_try),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", 3),
          (assign, ":continue", 1),
        (try_end),
        (try_begin),
          (eq, ":continue", 1),
          (store_random_in_range, ":random_no", 0, 3),
          (try_begin),
            (eq, ":random_no", 0),
            (assign, ":bandit_troop", "trp_bandit"),
          (else_try),
            (eq, ":random_no", 1),
			(try_begin),
				(eq,"$g_ccc_option_hard_core_mode",1),
				(assign, ":bandit_troop", "trp_mountain_bandit"),#occc tweak...
			(else_try),
				(store_random_in_range, ":random_no", 0, 5),
				(try_begin),
					(eq, ":random_no", 0),
					(store_random_in_range, ":random_no", 0, 50),
					(assign, ":bandit_troop", "trp_mountain_bandit_spartan"),
					(try_begin),
						(eq, ":random_no", 0),
						(assign, ":bandit_troop", "trp_occc_leonidas_copy"),
					(try_end),
				(else_try),
					(assign, ":bandit_troop", "trp_occc_robber_knight"),
				(try_end),
			(try_end),
          (else_try),
            (assign, ":bandit_troop", "trp_forest_bandit"),
          (try_end),
          ## CC-D begin: extra assassin
          (try_begin),
            (this_or_next|neg|check_quest_active, "qst_deal_with_night_bandits"),
            (neg|quest_slot_eq, "qst_deal_with_night_bandits", slot_quest_target_center, ":center_no"),
            
            (store_character_level, ":level", "trp_player"),
            (ge, ":level", 25),
            (store_random_in_range, ":random_no", 0, 100),
            (try_begin),
              (lt, ":random_no", 10),
              (assign, ":bandit_troop", "trp_ccd_assassin"),
            (else_try),
              (lt, ":random_no", 15),
              (ge, ":level", 30),
              (assign, ":bandit_troop", "trp_ccd_komusou"),
            (else_try),
              (lt, ":random_no", 20),
              (ge, ":level", 35),
              (assign, ":bandit_troop", "trp_ccd_shikaku"),
            (else_try),#occc
              (lt, ":random_no", 25),
              (ge, ":level", 35),
              (assign, ":bandit_troop", "trp_occc_cult_assassin"),
            (try_end),
          (try_end),
          ## CC-D end
          (party_set_slot, ":center_no", slot_center_has_bandits, ":bandit_troop"),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s1, ":center_no"),
            (display_message, "@{!}{s1} is infested by bandits (at night)."),
          (try_end),
        (try_end),
      (else_try),
        (try_begin),
          (assign, ":random_chance", 40),
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (assign, ":random_chance", 20),
          (try_end),
          (store_random_in_range, ":random_no", 0, 100),
          (lt, ":random_no", ":random_chance"),
          (party_set_slot, ":center_no", slot_center_has_bandits, 0),
          (try_begin),
            (eq, "$cheat_mode", 1),
            (str_store_party_name, s1, ":center_no"),
            (display_message, "@{s1} is no longer infested by bandits (at night)."),
          (try_end),
        (try_end),
      (try_end),
    (try_end),

    (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
	  (faction_slot_eq, ":faction_no", slot_faction_ai_state, sfai_feast),

	  (faction_get_slot, ":faction_object", ":faction_no", slot_faction_ai_object),
	  (is_between, ":faction_object", towns_begin, towns_end),

	  (party_slot_ge, ":faction_object", slot_town_has_tournament, 1),
	  #continue holding tournaments during the feast
      (party_set_slot, ":faction_object", slot_town_has_tournament, 2),
    (try_end),

	(try_begin),
      #(lt, ":num_active_tournaments", 3), 
      (lt, ":num_active_tournaments", 6),  #CC-C begin add tournaments

      (store_random_in_range, ":random_no", 0, 100),
      #Add new tournaments with a 30% chance if there are less than 3 tournaments going on
      #(lt, ":random_no", 30),
      (lt, ":random_no", 50), #CC-C begin add tournaments
      (store_random_in_range, ":random_town", towns_begin, towns_end),
      (store_random_in_range, ":random_days", 12, 15),
      (party_set_slot, ":random_town", slot_town_has_tournament, ":random_days"),
      (try_begin),
        (eq, "$cheat_mode", 1),
        (str_store_party_name, s1, ":random_town"),
        (display_message, "@{!}{s1} is holding a tournament."),
      (try_end),
    (try_end),
    ]),

  (3,
[
	(assign, "$g_player_tournament_placement", 0),
]),


#(0.1,

#	[
#	(try_begin),
#		(troop_slot_ge, "trp_player", slot_troop_spouse, active_npcs_begin),
#		(troop_get_slot, ":spouse", "trp_player", slot_troop_spouse),
#		(store_faction_of_troop, ":spouse_faction", ":spouse"),
#		(neq, ":spouse_faction", "$players_kingdom"),
#		(display_message, "@{!}ERROR! Player and spouse are separate factions"),
#	(try_end),
#	]
#),

  # Asking to give center to player
  (8,
   [
#    (assign, ":done", 0),
#    (try_for_range, ":center_no", centers_begin, centers_end),
#      (eq, ":done", 0),
#      (party_slot_eq, ":center_no", slot_town_lord, stl_reserved_for_player),
#      (assign, "$g_center_to_give_to_player", ":center_no"),
 #     (try_begin),
  #      (eq, "$g_center_to_give_to_player", "$g_castle_requested_by_player"),
   #     (assign, "$g_castle_requested_by_player", 0),
	#	(try_begin),
	#		(eq, "$g_castle_requested_for_troop", "trp_player"),
	#		(jump_to_menu, "mnu_requested_castle_granted_to_player"),
	#	(else_try),
	#		(jump_to_menu, "mnu_requested_castle_granted_to_player_husband"),
	#	(try_end),
    #  (else_try),
    #    (jump_to_menu, "mnu_give_center_to_player"),
    # (try_end),
    #  (assign, ":done", 1),
    #(else_try),
    #  (eq, ":center_no", "$g_castle_requested_by_player"),
    #  (party_slot_ge, ":center_no", slot_town_lord, active_npcs_begin),
    #  (assign, "$g_castle_requested_by_player", 0),
    #  (store_faction_of_party, ":faction", ":center_no"),
    #  (eq, ":faction", "$players_kingdom"),
    #  (assign, "$g_center_to_give_to_player", ":center_no"),
	#  (try_begin),
#		(eq, "$player_has_homage", 1),
#		(jump_to_menu, "mnu_requested_castle_granted_to_another"),
#	  (else_try),
#		(jump_to_menu, "mnu_requested_castle_granted_to_another_female"),
#	  (try_end),
 #     (assign, ":done", 1),
  #  (try_end),
    ]),

  # Taking denars from player while resting in not owned centers
  (1,
   [(neg|map_free),
    (is_currently_night),
#    (ge, "$g_last_rest_center", 0),
    (is_between, "$g_last_rest_center", centers_begin, centers_end),
    (neg|party_slot_eq, "$g_last_rest_center", slot_town_lord, "trp_player"),

##diplomacy begin
    (party_get_slot, ":town_lord", "$g_last_rest_center", slot_town_lord),
    (assign, reg0, 0),
    (try_begin),
      (is_between, ":town_lord", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":town_lord"),
      (try_begin),
        (neq, reg0, 0),
        (display_message, "@You are within the walls of an affiliated family member and don't have to pay for accommodation."),
      (try_end),
    (try_end),
    (eq, reg0, 0),
##diplomacy end

    (store_faction_of_party, ":last_rest_center_faction", "$g_last_rest_center"),
    (neq, ":last_rest_center_faction", "fac_player_supporters_faction"),
    (store_current_hours, ":cur_hours"),
    (ge, ":cur_hours", "$g_last_rest_payment_until"),
    (store_add, "$g_last_rest_payment_until", ":cur_hours", 24),
    (store_troop_gold, ":gold", "trp_player"),
    (party_get_num_companions, ":num_men", "p_main_party"),
    (store_div, ":total_cost", ":num_men", 4),
    (val_add, ":total_cost", 1),
    (try_begin),
      (ge, ":gold", ":total_cost"),
      (display_message, "@You pay for accommodation."),
      (troop_remove_gold, "trp_player", ":total_cost"),
    (else_try),
      (gt, ":gold", 0),
      (troop_remove_gold, "trp_player", ":gold"),
    (try_end),
    ]),

  # Spawn some bandits.
  (25, #CC-C 36 -> 25
   [
       (call_script, "script_spawn_bandits"),
	  #occc start
       (call_script, "script_cf_occc_lord_parties_daily_check"), 
	   (call_script,"script_cf_occc_subfaction_relation_change"),
	  #occc end
   ]),
   
  #occc  25 ->28
  (28, 
   [
      ## CC begin
       (call_script, "script_bandit_prisoners_convert_to_bandit_party"), 
       (call_script, "script_hostile_troops_of_lord_party_convert_to_deserter_party"), 
       (call_script, "script_combine_parties_of_same_template"),
      ## CC end
   ]),

  # Make parties larger as game progresses.
  (24,
   [
       (call_script, "script_update_party_creation_random_limits"),
    ]),

  # Check if a faction is defeated every day
  (24,
   [
    (assign, ":num_active_factions", 0),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_set_slot, ":cur_kingdom", slot_faction_number_of_parties, 0),
    (try_end),
    (try_for_parties, ":cur_party"),
      (store_faction_of_party, ":party_faction", ":cur_party"),
      (is_between, ":party_faction", kingdoms_begin, kingdoms_end),
      (this_or_next|is_between, ":cur_party", centers_begin, centers_end),
		(party_slot_eq, ":cur_party", slot_party_type, spt_kingdom_hero_party),
      (faction_get_slot, ":kingdom_num_parties", ":party_faction", slot_faction_number_of_parties),
      (val_add, ":kingdom_num_parties", 1),
      (faction_set_slot, ":party_faction", slot_faction_number_of_parties, ":kingdom_num_parties"),
    (try_end),
    (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
      (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
      (val_add, ":num_active_factions", 1),
      (faction_slot_eq, ":cur_kingdom", slot_faction_number_of_parties, 0),
      (assign, ":faction_removed", 0),
      (try_begin),
        (eq, ":cur_kingdom", "fac_player_supporters_faction"),
        (try_begin),
          (le, "$supported_pretender", 0),
          (faction_set_slot, ":cur_kingdom", slot_faction_state, sfs_inactive),
          (assign, ":faction_removed", 1),
        (try_end),
      (else_try),
        (neq, "$players_kingdom", ":cur_kingdom"),
        (faction_set_slot, ":cur_kingdom", slot_faction_state, sfs_defeated),
        (try_for_parties, ":cur_party"),
          (store_faction_of_party, ":party_faction", ":cur_party"),
          (eq, ":party_faction", ":cur_kingdom"),
          (party_get_slot, ":home_center", ":cur_party", slot_party_home_center),
          (store_faction_of_party, ":home_center_faction", ":home_center"),
          (party_set_faction, ":cur_party", ":home_center_faction"),
        (try_end),
        (assign, ":kingdom_pretender", -1),
        (try_for_range, ":cur_pretender", pretenders_begin, pretenders_end),
          (troop_slot_eq, ":cur_pretender", slot_troop_original_faction, ":cur_kingdom"),
          (assign, ":kingdom_pretender", ":cur_pretender"),
        (try_end),
        (try_begin),
          (is_between, ":kingdom_pretender", pretenders_begin, pretenders_end),
          (neq, ":kingdom_pretender", "$supported_pretender"),
          (troop_set_slot, ":kingdom_pretender", slot_troop_cur_center, 0), #remove pretender from the world
        (try_end),
        (assign, ":faction_removed", 1),
        (try_begin),
          (eq, "$players_oath_renounced_against_kingdom", ":cur_kingdom"),
          (assign, "$players_oath_renounced_against_kingdom", 0),
          (assign, "$players_oath_renounced_given_center", 0),
          (assign, "$players_oath_renounced_begin_time", 0),
          (call_script, "script_add_notification_menu", "mnu_notification_oath_renounced_faction_defeated", ":cur_kingdom", 0),
        (try_end),
        #This menu must be at the end because faction banner will change after this menu if the player's supported pretender's original faction is cur_kingdom
        (call_script, "script_add_notification_menu", "mnu_notification_faction_defeated", ":cur_kingdom", 0),
        ## start peace CC
        (try_for_range, ":other_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
          (neq, ":other_kingdom", ":cur_kingdom"),
			(call_script, "script_diplomacy_start_peace_between_kingdoms", ":cur_kingdom", ":other_kingdom", 0),
        (try_end),
        ## CC
      (try_end),
      (try_begin),
        (eq, ":faction_removed", 1),
        (val_sub, ":num_active_factions", 1),
        #(call_script, "script_store_average_center_value_per_faction"),
      (try_end),
      (try_for_range, ":cur_kingdom_2", kingdoms_begin, kingdoms_end),
        (call_script, "script_update_faction_notes", ":cur_kingdom_2"),
      (try_end),
    (try_end),
    (try_begin),
      (eq, ":num_active_factions", 1),
      (eq, "$g_one_faction_left_notification_shown", 0),
      (assign, "$g_one_faction_left_notification_shown", 1),
      (try_for_range, ":cur_kingdom", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":cur_kingdom", slot_faction_state, sfs_active),
        (call_script, "script_add_notification_menu", "mnu_notification_one_faction_left", ":cur_kingdom", 0),
      (try_end),
    (try_end),
    ]),

  (3, #check to see if player's court has been captured
   [
     ##diplomacy start+ The player might be the ruler of another kingdom
     (assign, ":save_reg0", reg0),
	 (assign, ":alt_led_faction", "fac_player_supporters_faction"),
	 (try_begin),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
	    (ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
		(assign, ":alt_led_faction", "$players_kingdom"),
	 (try_end),
	 ##diplomacy end+
     (try_begin), #The old court has been lost
     ##diplomacy begin
       (is_between, "$g_player_court", centers_begin, centers_end),
       (party_slot_eq, "$g_player_court", slot_village_infested_by_bandits, "trp_peasant_woman"),
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (else_try),
     ##diplomacy end
       (is_between, "$g_player_court", centers_begin, centers_end),
       (store_faction_of_party, ":court_faction", "$g_player_court"),
       (neq, ":court_faction", "fac_player_supporters_faction"),
	   ##diplomacy start+ The player might be ruler of a faction other than fac_player_supporters_faction
	   (neq, ":court_faction", ":alt_led_faction"),
	   ##diplomacy end+
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (else_try),	#At least one new court has been found
       (lt, "$g_player_court", centers_begin),
       #Will by definition not active until a center is taken by the player faction
       #Player minister must have been appointed at some point
       (this_or_next|faction_slot_eq, "fac_player_supporters_faction", slot_faction_leader, "trp_player"),
		(gt, "$g_player_minister", 0),

       (assign, ":center_found", 0),
       (try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
         (eq, ":center_found", 0),
         (store_faction_of_party, ":court_faction", ":walled_center"),
		   ##diplomacy start+ The player might be ruler of a faction other than fac_player_supporters_faction
		   (this_or_next|eq, ":court_faction", ":alt_led_faction"),
		   ##diplomacy end+
         (eq, ":court_faction", "fac_player_supporters_faction"),
         (assign, ":center_found", ":walled_center"),
       (try_end),
       (ge, ":center_found", 1),
       (call_script, "script_add_notification_menu", "mnu_notification_court_lost", 0, 0),
     (try_end),
     #Also, piggy-backing on this -- having bandits go to lairs and back
     (try_for_parties, ":bandit_party"),
       (gt, ":bandit_party", "p_spawn_points_end"),
       (party_get_template_id, ":bandit_party_template", ":bandit_party"),
       (is_between, ":bandit_party_template", bandit_party_template_begin, bandit_party_template_end), ## CC
       (party_template_get_slot, ":bandit_lair", ":bandit_party_template", slot_party_template_lair_party),
       (try_begin),#If party is active and bandit is far away, then move to location
         (gt, ":bandit_lair", "p_spawn_points_end"),
         (store_distance_to_party_from_party, ":distance", ":bandit_party", ":bandit_lair"), #this is the cause of the error
         (gt, ":distance", 30),
         #All this needs checking
         (party_set_ai_behavior, ":bandit_party", ai_bhvr_travel_to_point),
         (party_get_position, pos5, ":bandit_lair"),
         (party_set_ai_target_position, ":bandit_party", pos5),
       (else_try), #Otherwise, act freely
         (get_party_ai_behavior, ":behavior", ":bandit_party"),
         (eq, ":behavior", ai_bhvr_travel_to_point),
         (try_begin),
           (gt, ":bandit_lair", "p_spawn_points_end"),
           (store_distance_to_party_from_party, ":distance", ":bandit_party", ":bandit_lair"),
           (lt, ":distance", 3),
           (party_set_ai_behavior, ":bandit_party", ai_bhvr_patrol_party),
           (party_template_get_slot, ":spawnpoint", ":bandit_party_template", slot_party_template_lair_spawnpoint),
           (party_set_ai_object, ":bandit_party", ":spawnpoint"),
           (party_set_ai_patrol_radius, ":bandit_party", 45),
         (else_try),
           (lt, ":bandit_lair", "p_spawn_points_end"),
           (party_set_ai_behavior, ":bandit_party", ai_bhvr_patrol_party),
           (party_template_get_slot, ":spawnpoint", ":bandit_party_template", slot_party_template_lair_spawnpoint),
           (party_set_ai_object, ":bandit_party", ":spawnpoint"),
           (party_set_ai_patrol_radius, ":bandit_party", 45),
         (try_end),
       (try_end),
     (try_end),
     #Piggybacking on trigger:
     (try_begin),
       (troop_get_slot, ":betrothed", "trp_player", slot_troop_betrothed),
       (gt, ":betrothed", 0),
       (neg|check_quest_active, "qst_wed_betrothed"),
       (neg|check_quest_active, "qst_wed_betrothed_female"),
       (str_store_troop_name, s5, ":betrothed"),
       (display_message, "@Betrothal to {s5} expires"),
       (troop_set_slot, "trp_player", slot_troop_betrothed, -1),
       (troop_set_slot, ":betrothed", slot_troop_betrothed, -1),
     (try_end),
	 ##diplomacy start+
	 (assign, reg0, ":save_reg0"),#revert register
	 ##diplomacy end+
     ]),

  # Reduce renown slightly by 0.5% every week
  (7 * 24,
   [
       (troop_get_slot, ":player_renown", "trp_player", slot_troop_renown),
       (store_div, ":renown_decrease", ":player_renown", 200),
       (val_sub, ":player_renown", ":renown_decrease"),
       (troop_set_slot, "trp_player", slot_troop_renown, ":player_renown"),
    ]),

  # Read books if player is resting.
  (1, [(neg|map_free),
       (gt, "$g_player_reading_book", 0),
       (player_has_item, "$g_player_reading_book"),
       (store_attribute_level, ":int", "trp_player", ca_intelligence),
       (item_get_slot, ":int_req", "$g_player_reading_book", slot_item_intelligence_requirement),
       (le, ":int_req", ":int"),
       (item_get_slot, ":book_reading_progress", "$g_player_reading_book", slot_item_book_reading_progress),
       (item_get_slot, ":book_read", "$g_player_reading_book", slot_item_book_read),
       (eq, ":book_read", 0),
      ## CC begin
       (assign, ":read_speed", 0),
       (try_for_range, ":other_troop", companions_begin, companions_end),
         (main_party_has_troop, ":other_troop"),
         (call_script, "script_get_book_read_slot", ":other_troop", "$g_player_reading_book"),
         (assign, ":other_slot_no", reg0),
         (troop_slot_eq, "trp_book_read", ":other_slot_no", 1),
         (val_add, ":read_speed", 1),
       (try_end),
       (val_div, ":read_speed", 4),
       (val_add, ":read_speed", 3),
       (val_add, ":book_reading_progress", ":read_speed"),
      ## CC end
       (item_set_slot, "$g_player_reading_book", slot_item_book_reading_progress, ":book_reading_progress"),
       (ge, ":book_reading_progress", 1000),
       (item_set_slot, "$g_player_reading_book", slot_item_book_read, 1),
       (item_set_slot, "$g_player_reading_book", slot_item_book_reading_progress, 1000), ## CC
       (str_store_item_name, s1, "$g_player_reading_book"),
       (str_clear, s2),
       (try_begin),
         (eq, "$g_player_reading_book", "itm_book_tactics"),
         (troop_raise_skill, "trp_player", "skl_tactics", 1),
         (str_store_string, s2, "@ Your tactics skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_persuasion"),
         (troop_raise_skill, "trp_player", "skl_persuasion", 1),
         (str_store_string, s2, "@ Your persuasion skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_leadership"),
         (troop_raise_skill, "trp_player", "skl_leadership", 1),
         (str_store_string, s2, "@ Your leadership skill has increased by 1."),
      ## CC begin
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_prisoner_management"),
         (troop_raise_skill, "trp_player", "skl_prisoner_management", 1),
         (str_store_string, s2, "@ Your prisoner management skill has increased by 1."),
      ## CC end
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_intelligence"),
         (troop_raise_attribute, "trp_player", ca_intelligence, 1),
         (str_store_string, s2, "@ Your intelligence has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_trade"),
         (troop_raise_skill, "trp_player", "skl_trade", 1),
         (str_store_string, s2, "@ Your trade skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_weapon_mastery"),
         (troop_raise_skill, "trp_player", "skl_weapon_master", 1),
         (str_store_string, s2, "@ Your weapon master skill has increased by 1."),
       (else_try),
         (eq, "$g_player_reading_book", "itm_book_engineering"),
         (troop_raise_skill, "trp_player", "skl_engineer", 1),
         (str_store_string, s2, "@ Your engineer skill has increased by 1."),
       (try_end),

       (unlock_achievement, ACHIEVEMENT_BOOK_WORM),
       (call_script, "script_ccd_record_achievement", ACHIEVEMENT_BOOK_WORM),  ## CC-D add: for local achievement

       (try_begin),
         (eq, "$g_infinite_camping", 0),
         (dialog_box, "@You have finished reading {s1}.{s2}", "@Book Read"),
       (try_end),

       (assign, "$g_player_reading_book", 0),
       ]),

# Removing cattle herds if they are way out of range
  (12, [(try_for_parties, ":cur_party"),
          (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
          (neg|party_slot_eq, ":cur_party", slot_party_ccd_stray_cattle, 1),  ## CC-D
          (store_distance_to_party_from_party, ":dist",":cur_party", "p_main_party"),
          (try_begin),
            (gt, ":dist", 30),
            (remove_party, ":cur_party"),
            (try_begin),
              #Fail quest if the party is the quest party
              (check_quest_active, "qst_move_cattle_herd"),
              (neg|check_quest_concluded, "qst_move_cattle_herd"),
              (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
              (call_script, "script_fail_quest", "qst_move_cattle_herd"),
            (end_try),
          (else_try),
            (gt, ":dist", 10),
            (party_set_slot, ":cur_party", slot_cattle_driven_by_player, 0),
            (party_set_ai_behavior, ":cur_party", ai_bhvr_hold),
          (try_end),
        (try_end),
    ]),


#####!!!!!

# Village upgrade triggers

# School + Temple occc
  (30 * 24,
   [(try_for_range, ":cur_village", villages_begin, villages_end),
      (party_slot_eq, ":cur_village", slot_town_lord, "trp_player"),
      (party_slot_eq, ":cur_village", slot_center_has_school, 1),
      (party_get_slot, ":cur_relation", ":cur_village", slot_center_player_relation),
      (val_add, ":cur_relation", 1),
	  #occc begin
	  (try_begin),
		(party_slot_ge, ":cur_village", slot_center_has_temple, 1),
		(party_get_slot, ":religion", ":cur_village", slot_center_religion),
		(party_slot_eq, ":cur_village", slot_center_has_temple, ":religion"),#same type temple
		(troop_slot_eq,"trp_player",slot_troop_religion,":religion"),#same religion
		(val_add, ":cur_relation", 2),#+2
	  (try_end),
	  #occc end
      (val_min, ":cur_relation", 100),
      (party_set_slot, ":cur_village", slot_center_player_relation, ":cur_relation"),
    (try_end),
    ]),

# Quest triggers:

# Remaining days text update
  (24, [(try_for_range, ":cur_quest", all_quests_begin, all_quests_end),
          (try_begin),
            (check_quest_active, ":cur_quest"),
            (try_begin),
              (neg|check_quest_concluded, ":cur_quest"),
              (quest_slot_ge, ":cur_quest", slot_quest_expiration_days, 1),
              (quest_get_slot, ":exp_days", ":cur_quest", slot_quest_expiration_days),
              (val_sub, ":exp_days", 1),
              (try_begin),
              #CC-C begin
                (is_between,":cur_quest","qst_ccc_cave_quest1","qst_ccc_cave_quest_end"),
                (eq, ":exp_days", 0),
                (call_script, "script_ccc_abort_cave_quest", ":cur_quest"),
              (else_try),
              #CC-C end
                (eq, ":exp_days", 0),
                (call_script, "script_abort_quest", ":cur_quest", 1),
              (else_try),
                (quest_set_slot, ":cur_quest", slot_quest_expiration_days, ":exp_days"),
                (assign, reg0, ":exp_days"),
                (add_quest_note_from_sreg, ":cur_quest", 7, "@You have {reg0} days to finish this quest.", 0),
              (try_end),
            (try_end),
          (else_try),
            (quest_slot_ge, ":cur_quest", slot_quest_dont_give_again_remaining_days, 1),
            (quest_get_slot, ":value", ":cur_quest", slot_quest_dont_give_again_remaining_days),
            (val_sub, ":value", 1),
            (quest_set_slot, ":cur_quest", slot_quest_dont_give_again_remaining_days, ":value"),
          (try_end),
        (try_end),
    ]),

# Report to army quest
  (2,
   [
     (eq, "$g_infinite_camping", 0),
     (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
     (eq, "$g_player_is_captive", 0),

	 (try_begin),
		(check_quest_active, "qst_report_to_army"),
		(faction_slot_eq, "$players_kingdom", slot_faction_marshall, -1),
		(call_script, "script_abort_quest", "qst_report_to_army", 0),
	 (try_end),

	 (faction_get_slot, ":faction_object", "$players_kingdom", slot_faction_ai_object),

     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_feast),

     (assign, ":continue", 1),
     (try_begin),
       (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_attacking_enemies_around_center),
       (this_or_next|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_attacking_center),
       (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_raiding_village),
       (neg|is_between, ":faction_object", walled_centers_begin, walled_centers_end),
       (assign, ":continue", 0),
     (try_end),
     (eq, ":continue", 1),

	 (assign, ":kingdom_is_at_war", 0),
	 (try_for_range, ":faction", kingdoms_begin, kingdoms_end),
		(neq, ":faction", "$players_kingdom"),
		(store_relation, ":relation", ":faction", "$players_kingdom"),
		(lt, ":relation", 0),
		(assign, ":kingdom_is_at_war", 1),
	 (try_end),
	 (eq, ":kingdom_is_at_war", 1),

     (neg|check_quest_active, "qst_report_to_army"),
     (neg|check_quest_active, "qst_follow_army"),

     (neg|quest_slot_ge, "qst_report_to_army", slot_quest_dont_give_again_remaining_days, 1),
     (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
     (gt, ":faction_marshall", 0),
     (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
     (gt, ":faction_marshall_party", 0),
     (party_is_active, ":faction_marshall_party"),

     (store_distance_to_party_from_party, ":distance_to_marshal", ":faction_marshall_party", "p_main_party"),
     (le, ":distance_to_marshal", 96),

     (assign, ":has_no_quests", 1),
     (try_for_range, ":cur_quest", lord_quests_begin, lord_quests_end),
       (check_quest_active, ":cur_quest"),
       (quest_slot_eq, ":cur_quest", slot_quest_giver_troop, ":faction_marshall"),
       (assign, ":has_no_quests", 0),
     (try_end),
     (eq, ":has_no_quests", 1),

     (try_for_range, ":cur_quest", lord_quests_begin_2, lord_quests_end_2),
       (check_quest_active, ":cur_quest"),
       (quest_slot_eq, ":cur_quest", slot_quest_giver_troop, ":faction_marshall"),
       (assign, ":has_no_quests", 0),
     (try_end),
     (eq, ":has_no_quests", 1),

     (try_for_range, ":cur_quest", army_quests_begin, army_quests_end),
       (check_quest_active, ":cur_quest"),
       (assign, ":has_no_quests", 0),
     (try_end),
     (eq, ":has_no_quests", 1),

     (store_character_level, ":level", "trp_player"),
     (ge, ":level", 8),
     (assign, ":cur_target_amount", 2),
     (try_for_range, ":cur_center", centers_begin, centers_end),
       (party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
       (try_begin),
         (party_slot_eq, ":cur_center", slot_party_type, spt_town),
         (val_add, ":cur_target_amount", 3),
       (else_try),
         (party_slot_eq, ":cur_center", slot_party_type, spt_castle),
         (val_add, ":cur_target_amount", 1),
       (else_try),
         (val_add, ":cur_target_amount", 1),
       (try_end),
     (try_end),

     (val_mul, ":cur_target_amount", 4),
     (val_min, ":cur_target_amount", 60),
     (quest_set_slot, "qst_report_to_army", slot_quest_giver_troop, ":faction_marshall"),
     (quest_set_slot, "qst_report_to_army", slot_quest_target_troop, ":faction_marshall"),
     (quest_set_slot, "qst_report_to_army", slot_quest_target_amount, ":cur_target_amount"),
     (quest_set_slot, "qst_report_to_army", slot_quest_expiration_days, 4),
     (quest_set_slot, "qst_report_to_army", slot_quest_dont_give_again_period, 22),
     (jump_to_menu, "mnu_kingdom_army_quest_report_to_army"),
   ]),


# Army quest initializer
  (3,
   [
     (assign, "$g_random_army_quest", -1),
     (check_quest_active, "qst_follow_army", 1),
     (is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
#Rebellion changes begin
#     (neg|is_between, "$players_kingdom", rebel_factions_begin, rebel_factions_end),
#Rebellion changes end
     (neg|faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_default),
     (faction_get_slot, ":faction_marshall", "$players_kingdom", slot_faction_marshall),
     (neq, ":faction_marshall", "trp_player"),
     (gt, ":faction_marshall", 0),
     (troop_get_slot, ":faction_marshall_party", ":faction_marshall", slot_troop_leaded_party),
     (gt, ":faction_marshall_party", 0),
     (party_is_active, ":faction_marshall_party"),
     (store_distance_to_party_from_party, ":dist", ":faction_marshall_party", "p_main_party"),
     (try_begin),
       (lt, ":dist", 15),
       (assign, "$g_player_follow_army_warnings", 0),
       (store_current_hours, ":cur_hours"),
       (faction_get_slot, ":last_offensive_time", "$players_kingdom", slot_faction_last_offensive_concluded),
       (store_sub, ":passed_time", ":cur_hours", ":last_offensive_time"),

       (assign, ":result", -1),
       (try_begin),
         (store_random_in_range, ":random_no", 0, 100),
         (lt, ":random_no", 30),
         (troop_slot_eq, ":faction_marshall", slot_troop_does_not_give_quest, 0),
         (try_for_range, ":unused", 0, 20), #Repeat trial twenty times
           (eq, ":result", -1),
           (store_random_in_range, ":quest_no", army_quests_begin, army_quests_end),
           (neg|quest_slot_ge, ":quest_no", slot_quest_dont_give_again_remaining_days, 1),
           (try_begin),
             (eq, ":quest_no", "qst_deliver_cattle_to_army"),
			# (eq, 1, 0), #disables temporarily
             (try_begin),
               (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_attacking_center),
               (gt, ":passed_time", 120),#5 days
               (store_random_in_range, ":quest_target_amount", 5, 10),
               (assign, ":result","qst_deliver_cattle_to_army"),
               (quest_set_slot, ":result", slot_quest_target_amount, ":quest_target_amount"),
               (quest_set_slot, ":result", slot_quest_expiration_days, 10),
               (quest_set_slot, ":result", slot_quest_dont_give_again_period, 30),
             (try_end),
           (else_try),
             (eq, ":quest_no", "qst_join_siege_with_army"),
			 (eq, 1, 0),
             (try_begin),
               (faction_slot_eq, "$players_kingdom", slot_faction_ai_state, sfai_attacking_center),
               (faction_get_slot, ":ai_object", "$players_kingdom", slot_faction_ai_object),
               (is_between, ":ai_object", walled_centers_begin, walled_centers_end),
               (party_get_battle_opponent, ":besieged_center", ":faction_marshall_party"),
               (eq, ":besieged_center", ":ai_object"),
               #army is assaulting the center
               (assign, ":result", ":quest_no"),
               (quest_set_slot, ":result", slot_quest_target_center, ":ai_object"),
               (quest_set_slot, ":result", slot_quest_expiration_days, 2),
               (quest_set_slot, ":result", slot_quest_dont_give_again_period, 15),
             (try_end),
           (else_try),
             (eq, ":quest_no", "qst_scout_waypoints"),
             (try_begin),
               (assign, ":end_cond", 100),
               (assign, "$qst_scout_waypoints_wp_1", -1),
               (assign, "$qst_scout_waypoints_wp_2", -1),
               (assign, "$qst_scout_waypoints_wp_3", -1),
               (assign, ":continue", 0),
               (try_for_range, ":unused", 0, ":end_cond"),
                 (try_begin),
                   (lt, "$qst_scout_waypoints_wp_1", 0),
                   (call_script, "script_cf_get_random_enemy_center_within_range", ":faction_marshall_party", 50),
                   (assign, "$qst_scout_waypoints_wp_1", reg0),
                 (try_end),
                 (try_begin),
                   (lt, "$qst_scout_waypoints_wp_2", 0),
                   (call_script, "script_cf_get_random_enemy_center_within_range", ":faction_marshall_party", 50),
                   (neq, "$qst_scout_waypoints_wp_1", reg0),
                   (assign, "$qst_scout_waypoints_wp_2", reg0),
                 (try_end),
                 (try_begin),
                   (lt, "$qst_scout_waypoints_wp_3", 0),
                   (call_script, "script_cf_get_random_enemy_center_within_range", ":faction_marshall_party", 50),
                   (neq, "$qst_scout_waypoints_wp_1", reg0),
                   (neq, "$qst_scout_waypoints_wp_2", reg0),
                   (assign, "$qst_scout_waypoints_wp_3", reg0),
                 (try_end),
                 (neq, "$qst_scout_waypoints_wp_1", "$qst_scout_waypoints_wp_2"),
                 (neq, "$qst_scout_waypoints_wp_1", "$qst_scout_waypoints_wp_2"),
                 (neq, "$qst_scout_waypoints_wp_2", "$qst_scout_waypoints_wp_3"),
                 (ge, "$qst_scout_waypoints_wp_1", 0),
                 (ge, "$qst_scout_waypoints_wp_2", 0),
                 (ge, "$qst_scout_waypoints_wp_3", 0),
                 (assign, ":end_cond", 0),
                 (assign, ":continue", 1),
               (try_end),
               (eq, ":continue", 1),
               (assign, "$qst_scout_waypoints_wp_1_visited", 0),
               (assign, "$qst_scout_waypoints_wp_2_visited", 0),
               (assign, "$qst_scout_waypoints_wp_3_visited", 0),
               (assign, ":result", "qst_scout_waypoints"),
               (quest_set_slot, ":result", slot_quest_expiration_days, 7),
               (quest_set_slot, ":result", slot_quest_dont_give_again_period, 25),
             (try_end),
           (try_end),
         (try_end),

         (try_begin),
           (neq, ":result", -1),
           (quest_set_slot, ":result", slot_quest_current_state, 0),
           (quest_set_slot, ":result", slot_quest_giver_troop, ":faction_marshall"),
           (try_begin),
             (eq, ":result", "qst_join_siege_with_army"),
             (jump_to_menu, "mnu_kingdom_army_quest_join_siege_order"),
           (else_try),
             (assign, "$g_random_army_quest", ":result"),
             (quest_set_slot, "$g_random_army_quest", slot_quest_giver_troop, ":faction_marshall"),
             (jump_to_menu, "mnu_kingdom_army_quest_messenger"),
           (try_end),
         (try_end),
       (try_end),
     (else_try),
       (val_add, "$g_player_follow_army_warnings", 1),
       (try_begin),
         (lt, "$g_player_follow_army_warnings", 15),
         (try_begin),
           (store_mod, ":follow_mod", "$g_player_follow_army_warnings", 3),
           (eq, ":follow_mod", 0),
           (str_store_troop_name_link, s1, ":faction_marshall"),
           (try_begin),
             (lt, "$g_player_follow_army_warnings", 8),
#             (display_message, "str_marshal_warning"),
           (else_try),
             (display_message, "str_marshal_warning"),
           (try_end),
         (try_end),
       (else_try),
         (jump_to_menu, "mnu_kingdom_army_follow_failed"),
       (try_end),
     (try_end),
    ]),

# Move cattle herd
  (0.5, [(check_quest_active,"qst_move_cattle_herd"),
         (neg|check_quest_concluded,"qst_move_cattle_herd"),
         (quest_get_slot, ":target_party", "qst_move_cattle_herd", slot_quest_target_party),
         (quest_get_slot, ":target_center", "qst_move_cattle_herd", slot_quest_target_center),
         (store_distance_to_party_from_party, ":dist",":target_party", ":target_center"),
         (lt, ":dist", 3),
         (remove_party, ":target_party"),
         (call_script, "script_succeed_quest", "qst_move_cattle_herd"),
    ]),

  (2, [
       (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		 (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		 (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (ge, ":party_no", 1),
		 (party_is_active, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_following_player, 1),
         (store_current_hours, ":cur_time"),
         (neg|party_slot_ge, ":party_no", slot_party_follow_player_until_time, ":cur_time"),
         (party_set_slot, ":party_no", slot_party_commander_party, -1),
         (party_set_slot, ":party_no", slot_party_following_player, 0),
         (assign,  ":dont_follow_period", 200),
         (store_add, ":dont_follow_time", ":cur_time", ":dont_follow_period"),
         (party_set_slot, ":party_no", slot_party_dont_follow_player_until_time,  ":dont_follow_time"),
       (try_end),
    ]),

# Deliver cattle and deliver cattle to army
  (0.5,
   [
     (try_begin),
       (check_quest_active,"qst_deliver_cattle"),
       (neg|check_quest_succeeded, "qst_deliver_cattle"),
       (quest_get_slot, ":target_center", "qst_deliver_cattle", slot_quest_target_center),
       (quest_get_slot, ":target_amount", "qst_deliver_cattle", slot_quest_target_amount),
       (quest_get_slot, ":cur_amount", "qst_deliver_cattle", slot_quest_current_state),
       (store_sub, ":left_amount", ":target_amount", ":cur_amount"),
       (call_script, "script_remove_cattles_if_herd_is_close_to_party", ":target_center", ":left_amount"),
       (val_add, ":cur_amount", reg0),
       (quest_set_slot, "qst_deliver_cattle", slot_quest_current_state, ":cur_amount"),
       (le, ":target_amount", ":cur_amount"),
       (call_script, "script_succeed_quest", "qst_deliver_cattle"),
     (try_end),
     (try_begin),
       (check_quest_active, "qst_deliver_cattle_to_army"),
       (neg|check_quest_succeeded, "qst_deliver_cattle_to_army"),
       (quest_get_slot, ":giver_troop", "qst_deliver_cattle_to_army", slot_quest_giver_troop),
       (troop_get_slot, ":target_party", ":giver_troop", slot_troop_leaded_party),
       (try_begin),
         (gt, ":target_party", 0),
         (quest_get_slot, ":target_amount", "qst_deliver_cattle_to_army", slot_quest_target_amount),
         (quest_get_slot, ":cur_amount", "qst_deliver_cattle_to_army", slot_quest_current_state),
         (store_sub, ":left_amount", ":target_amount", ":cur_amount"),
         (call_script, "script_remove_cattles_if_herd_is_close_to_party", ":target_party", ":left_amount"),
         (val_add, ":cur_amount", reg0),
         (quest_set_slot, "qst_deliver_cattle_to_army", slot_quest_current_state, ":cur_amount"),
         (try_begin),
           (le, ":target_amount", ":cur_amount"),
           (call_script, "script_succeed_quest", "qst_deliver_cattle_to_army"),
         (try_end),
       (else_try),
         (call_script, "script_abort_quest", "qst_deliver_cattle_to_army", 0),
       (try_end),
     (try_end),
     ]),

# Train peasants against bandits
  (1,
   [
     (neg|map_free),
     (check_quest_active, "qst_train_peasants_against_bandits"),
     (neg|check_quest_concluded, "qst_train_peasants_against_bandits"),
     (eq, "$qst_train_peasants_against_bandits_currently_training", 1),
     (val_add, "$qst_train_peasants_against_bandits_num_hours_trained", 1),
     (call_script, "script_get_max_skill_of_player_party", "skl_trainer"),
     (assign, ":trainer_skill", reg0),
     (store_sub, ":needed_hours", 20, ":trainer_skill"),
     (val_mul, ":needed_hours", 3),
     (val_div, ":needed_hours", 5),
     (ge, "$qst_train_peasants_against_bandits_num_hours_trained", ":needed_hours"),
     (assign, "$qst_train_peasants_against_bandits_num_hours_trained", 0),
     (rest_for_hours, 0, 0, 0), #stop resting
     (jump_to_menu, "mnu_train_peasants_against_bandits_ready"),
     ]),

# Scout waypoints
  (1,
   [
     (check_quest_active,"qst_scout_waypoints"),
     (neg|check_quest_succeeded, "qst_scout_waypoints"),
     (try_begin),
       (eq, "$qst_scout_waypoints_wp_1_visited", 0),
       (store_distance_to_party_from_party, ":distance", "$qst_scout_waypoints_wp_1", "p_main_party"),
       (le, ":distance", 3),
       (assign, "$qst_scout_waypoints_wp_1_visited", 1),
       (str_store_party_name_link, s1, "$qst_scout_waypoints_wp_1"),
       (display_message, "@{s1} is scouted."),
     (try_end),
     (try_begin),
       (eq, "$qst_scout_waypoints_wp_2_visited", 0),
       (store_distance_to_party_from_party, ":distance", "$qst_scout_waypoints_wp_2", "p_main_party"),
       (le, ":distance", 3),
       (assign, "$qst_scout_waypoints_wp_2_visited", 1),
       (str_store_party_name_link, s1, "$qst_scout_waypoints_wp_2"),
       (display_message, "@{s1} is scouted."),
     (try_end),
     (try_begin),
       (eq, "$qst_scout_waypoints_wp_3_visited", 0),
       (store_distance_to_party_from_party, ":distance", "$qst_scout_waypoints_wp_3", "p_main_party"),
       (le, ":distance", 3),
       (assign, "$qst_scout_waypoints_wp_3_visited", 1),
       (str_store_party_name_link, s1, "$qst_scout_waypoints_wp_3"),
       (display_message, "@{s1} is scouted."),
     (try_end),
     (eq, "$qst_scout_waypoints_wp_1_visited", 1),
     (eq, "$qst_scout_waypoints_wp_2_visited", 1),
     (eq, "$qst_scout_waypoints_wp_3_visited", 1),
     (call_script, "script_succeed_quest", "qst_scout_waypoints"),
     ]),

# Kill local merchant

  (3, [(neg|map_free),
       (check_quest_active, "qst_kill_local_merchant"),
       (quest_slot_eq, "qst_kill_local_merchant", slot_quest_current_state, 0),
       (quest_set_slot, "qst_kill_local_merchant", slot_quest_current_state, 1),
       (rest_for_hours, 0, 0, 0), #stop resting
       (assign, "$auto_enter_town", "$qst_kill_local_merchant_center"),
       (assign, "$quest_auto_menu", "mnu_kill_local_merchant_begin"),
       ]),

# Collect taxes
  (1, [(neg|map_free),
       (check_quest_active, "qst_collect_taxes"),
       (eq, "$g_player_is_captive", 0),
       (eq, "$qst_collect_taxes_currently_collecting", 1),
       (quest_get_slot, ":quest_current_state", "qst_collect_taxes", slot_quest_current_state),
       (this_or_next|eq, ":quest_current_state", 1),
       (this_or_next|eq, ":quest_current_state", 2),
       (eq, ":quest_current_state", 3),
       (quest_get_slot, ":left_hours", "qst_collect_taxes", slot_quest_target_amount),
       (val_sub, ":left_hours", 1),
       (quest_set_slot, "qst_collect_taxes", slot_quest_target_amount, ":left_hours"),
       (call_script, "script_get_max_skill_of_player_party", "skl_trade"),

       (try_begin),
         (lt, ":left_hours", 0),
         (assign, ":quest_current_state", 4),
         (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 4),
         (rest_for_hours, 0, 0, 0), #stop resting
         (jump_to_menu, "mnu_collect_taxes_complete"),
       (else_try),
         #Continue collecting taxes
         (assign, ":max_collected_tax", "$qst_collect_taxes_hourly_income"),
         (party_get_slot, ":prosperity", "$g_encountered_party", slot_town_prosperity),
         (store_add, ":multiplier", 30, ":prosperity"),
         (val_mul, ":max_collected_tax", ":multiplier"),
         (val_div, ":max_collected_tax", 80),#Prosperity of 50 gives the default values

         (try_begin),
           (eq, "$qst_collect_taxes_halve_taxes", 1),
           (val_div, ":max_collected_tax", 2),
         (try_end),
         (val_max, ":max_collected_tax", 2),
         (store_random_in_range, ":collected_tax", 1, ":max_collected_tax"),
         (quest_get_slot, ":cur_collected", "qst_collect_taxes", slot_quest_gold_reward),
         (val_add, ":cur_collected", ":collected_tax"),
         (quest_set_slot, "qst_collect_taxes", slot_quest_gold_reward, ":cur_collected"),
         (call_script, "script_troop_add_gold", "trp_player", ":collected_tax"),
       (try_end),
       (try_begin),
         (eq, ":quest_current_state", 1),
         (val_sub, "$qst_collect_taxes_menu_counter", 1),
         (le, "$qst_collect_taxes_menu_counter", 0),
         (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 2),
         (jump_to_menu, "mnu_collect_taxes_revolt_warning"),
       (else_try), #Chance of revolt against player
         (eq, ":quest_current_state", 2),
         (val_sub, "$qst_collect_taxes_unrest_counter", 1),
         (le, "$qst_collect_taxes_unrest_counter", 0),
         (eq, "$qst_collect_taxes_halve_taxes", 0),
         (quest_set_slot, "qst_collect_taxes", slot_quest_current_state, 3),

         (store_div, ":unrest_chance", 10000, "$qst_collect_taxes_total_hours"),
         (val_add, ":unrest_chance",30),

         (store_random_in_range, ":unrest_roll", 0, 1000),
         (try_begin),
           (lt, ":unrest_roll", ":unrest_chance"),
           (jump_to_menu, "mnu_collect_taxes_revolt"),
         (try_end),
       (try_end),
       ]),

#persuade_lords_to_make_peace begin
  (72, [(gt, "$g_force_peace_faction_1", 0),
        (gt, "$g_force_peace_faction_2", 0),
        (try_begin),
          (store_relation, ":relation", "$g_force_peace_faction_1", "$g_force_peace_faction_2"),
          (lt, ":relation", 0),
          (call_script, "script_diplomacy_start_peace_between_kingdoms", "$g_force_peace_faction_1", "$g_force_peace_faction_2", 1),
        (try_end),
        (assign, "$g_force_peace_faction_1", 0),
        (assign, "$g_force_peace_faction_2", 0),
       ]),

#NPC changes begin
#Resolve one issue each hour
(1,
   [
		(str_store_string, s51, "str_no_trigger_noted"),

		# Rejoining party
        (try_begin),
            (gt, "$npc_to_rejoin_party", 0),
            (eq, "$g_infinite_camping", 0),
            (try_begin),
                (neg|main_party_has_troop, "$npc_to_rejoin_party"),
                (neq, "$g_player_is_captive", 1),

				(str_store_string, s51, "str_triggered_by_npc_to_rejoin_party"),

                (assign, "$npc_map_talk_context", slot_troop_days_on_mission),
                (start_map_conversation, "$npc_to_rejoin_party", -1),
			(else_try),
				(troop_set_slot, "$npc_to_rejoin_party", slot_troop_current_mission, npc_mission_rejoin_when_possible),
				(assign, "$npc_to_rejoin_party", 0),
            (try_end),
		# Here do NPC that is quitting
		(else_try),
            (gt, "$npc_is_quitting", 0),
            (eq, "$g_infinite_camping", 0),
            (try_begin),
                (main_party_has_troop, "$npc_is_quitting"),
                (neq, "$g_player_is_captive", 1),
				##diplomacy start+ disable spouse quitting to avoid problems
				(neg|troop_slot_eq, "trp_player", slot_troop_spouse, "$npc_is_quitting"),
				(neg|troop_slot_eq, "$npc_is_quitting", slot_troop_spouse, "trp_player"),
				##diplomacy end+
				(str_store_string, s51, "str_triggered_by_npc_is_quitting"),
                (start_map_conversation, "$npc_is_quitting", -1),
            (else_try),
                (assign, "$npc_is_quitting", 0),
            (try_end),
		#NPC with grievance
        (else_try), #### Grievance
            (gt, "$npc_with_grievance", 0),
            (eq, "$g_infinite_camping", 0),
            (eq, "$disable_npc_complaints", 0),
            (try_begin),
                (main_party_has_troop, "$npc_with_grievance"),
                (neq, "$g_player_is_captive", 1),

				(str_store_string, s51, "str_triggered_by_npc_has_grievance"),

                (assign, "$npc_map_talk_context", slot_troop_morality_state),
                (start_map_conversation, "$npc_with_grievance", -1),
            (else_try),
                (assign, "$npc_with_grievance", 0),
            (try_end),
        (else_try),
            (gt, "$npc_with_personality_clash", 0),
            (eq, "$g_infinite_camping", 0),
            (eq, "$disable_npc_complaints", 0),
            (troop_get_slot, ":object", "$npc_with_personality_clash", slot_troop_personalityclash_object),
            (try_begin),
                (main_party_has_troop, "$npc_with_personality_clash"),
                (main_party_has_troop, ":object"),
                (neq, "$g_player_is_captive", 1),

                (assign, "$npc_map_talk_context", slot_troop_personalityclash_state),
				(str_store_string, s51, "str_triggered_by_npc_has_personality_clash"),
                (start_map_conversation, "$npc_with_personality_clash", -1),
            (else_try),
                (assign, "$npc_with_personality_clash", 0),
            (try_end),
        (else_try), #### Political issue
            (gt, "$npc_with_political_grievance", 0),
            (eq, "$g_infinite_camping", 0),
            (eq, "$disable_npc_complaints", 0),
            (try_begin),
                (main_party_has_troop, "$npc_with_political_grievance"),
                (neq, "$g_player_is_captive", 1),

				(str_store_string, s51, "str_triggered_by_npc_has_political_grievance"),
                (assign, "$npc_map_talk_context", slot_troop_kingsupport_objection_state),
                (start_map_conversation, "$npc_with_political_grievance", -1),
			(else_try),
				(assign, "$npc_with_political_grievance", 0),
            (try_end),
		(else_try),
            (eq, "$disable_sisterly_advice", 0),
            (eq, "$g_infinite_camping", 0),
            (gt, "$npc_with_sisterly_advice", 0),
            (try_begin),
				(main_party_has_troop, "$npc_with_sisterly_advice"),
                (neq, "$g_player_is_captive", 1),

				##diplomacy start+
				(troop_slot_ge, "$npc_with_sisterly_advice", slot_troop_woman_to_woman_string, 1),
				##diplomacy end+
				(assign, "$npc_map_talk_context", slot_troop_woman_to_woman_string), #was npc_with_sisterly advice
	            (start_map_conversation, "$npc_with_sisterly_advice", -1),
			(else_try),
				(assign, "$npc_with_sisterly_advice", 0),
            (try_end),
		(else_try), #check for regional background
            (eq, "$disable_local_histories", 0),
            (eq, "$g_infinite_camping", 0),
            (try_for_range, ":npc", companions_begin, companions_end),
                (main_party_has_troop, ":npc"),
                (troop_slot_eq, ":npc", slot_troop_home_speech_delivered, 0),
                (troop_get_slot, ":home", ":npc", slot_troop_home),
                (gt, ":home", 0),
                (store_distance_to_party_from_party, ":distance", ":home", "p_main_party"),
                (lt, ":distance", 7),
                (assign, "$npc_map_talk_context", slot_troop_home),

				(str_store_string, s51, "str_triggered_by_local_histories"),

                (start_map_conversation, ":npc", -1),
            (try_end),
        (try_end),

		#add pretender to party if not active
		(try_begin),
			(check_quest_active, "qst_rebel_against_kingdom"),
			(is_between, "$supported_pretender", pretenders_begin, pretenders_end),
			(neg|main_party_has_troop, "$supported_pretender"),
			(neg|troop_slot_eq, "$supported_pretender", slot_troop_occupation, slto_kingdom_hero),
			(party_add_members, "p_main_party", "$supported_pretender", 1),
		(try_end),

		#make player marshal of rebel faction
		(try_begin),
			(check_quest_active, "qst_rebel_against_kingdom"),
			(is_between, "$supported_pretender", pretenders_begin, pretenders_end),
			(main_party_has_troop, "$supported_pretender"),
			(neg|faction_slot_eq, "fac_player_supporters_faction", slot_faction_marshall, "trp_player"),
			(call_script, "script_appoint_faction_marshall", "fac_player_supporters_faction", "trp_player"),
		(try_end),


]),
#NPC changes end

(4,
   ##diplomacy start+ Add support for promoted kingdom ladies
   ##OLD:
   #[(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
   ##NEW:
   [(try_for_range, ":troop_no", heroes_begin, heroes_end),
      (this_or_next|is_between, ":troop_no", active_npcs_begin, active_npcs_end),
	  (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
   ##diplomacy end+
      (troop_slot_ge, ":troop_no", slot_troop_change_to_faction, 1),
      (store_troop_faction, ":faction_no", ":troop_no"),
      (troop_get_slot, ":new_faction_no", ":troop_no", slot_troop_change_to_faction),
      (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
      (assign, ":continue", 0),
      (try_begin),
        (le, ":party_no", 0),
        #(troop_slot_eq, ":troop_no", slot_troop_is_prisoner, 0),
        (neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
        (assign, ":continue", 1),
      (else_try),
        (gt, ":party_no", 0),

        #checking if the party is outside the centers
        (party_get_attached_to, ":cur_center_no", ":party_no"),
        (try_begin),
          (lt, ":cur_center_no", 0),
          (party_get_cur_town, ":cur_center_no", ":party_no"),
        (try_end),
        (this_or_next|neg|is_between, ":cur_center_no", centers_begin, centers_end),
        (party_slot_eq, ":cur_center_no", slot_town_lord, ":troop_no"),

        #checking if the party is away from his original faction parties
		##diplomacy start+
		##Add support for promoted kingdom lades.
		##OLD:
        #(assign, ":end_cond", active_npcs_end),
		##NEW:
        (assign, ":end_cond", heroes_end),
		##diplomacy end+
        (try_for_range, ":enemy_troop_no", active_npcs_begin, ":end_cond"),
          (neq, ":enemy_troop_no", ":troop_no"), ## CC
		  (troop_slot_eq, ":enemy_troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":enemy_party_no", ":enemy_troop_no", slot_troop_leaded_party),
          (party_is_active, ":enemy_party_no"),
          (store_faction_of_party, ":enemy_faction_no", ":enemy_party_no"),
          (eq, ":enemy_faction_no", ":faction_no"),
          (store_distance_to_party_from_party, ":dist", ":party_no", ":enemy_party_no"),
          (lt, ":dist", 4),
          (assign, ":end_cond", 0),
        (try_end),
        (neq, ":end_cond", 0),
        (assign, ":continue", 1),
      (try_end),
      (eq, ":continue", 1),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":troop_no"),
			(display_message, "@{!}DEBUG - {s4} faction changed from slot_troop_change_to_faction"),
		(try_end),

      (call_script, "script_change_troop_faction", ":troop_no", ":new_faction_no"),
      (troop_set_slot, ":troop_no", slot_troop_change_to_faction, 0),
      (try_begin),
        (is_between, ":new_faction_no", kingdoms_begin, kingdoms_end),
        (str_store_troop_name_link, s1, ":troop_no"),
        (str_store_faction_name_link, s2, ":faction_no"),
        (str_store_faction_name_link, s3, ":new_faction_no"),
        (display_message, "@{s1} has switched from {s2} to {s3}."),
        (try_begin),
          (eq, ":faction_no", "$players_kingdom"),
          (call_script, "script_add_notification_menu", "mnu_notification_troop_left_players_faction", ":troop_no", ":new_faction_no"),
        (else_try),
          (eq, ":new_faction_no", "$players_kingdom"),
          (call_script, "script_add_notification_menu", "mnu_notification_troop_joined_players_faction", ":troop_no", ":faction_no"),
        (try_end),
      (try_end),
    (try_end),
    ]),


(1,
   [
     (eq, "$cheat_mode", 1),
     (try_for_range, ":center_no", centers_begin, centers_end),
       (party_get_battle_opponent, ":besieger_party", ":center_no"),
       (try_begin),
         (gt, ":besieger_party", 0),
         (str_store_party_name, s2, ":center_no"),
         (str_store_party_name, s3, ":besieger_party"),
         (display_message, "@{!}DEBUG : {s2} is besieging by {s3}"),
       (try_end),
     (try_end),
     ]),

(1,
   [
     (store_current_day, ":cur_day"),
     (gt, ":cur_day", "$g_last_report_control_day"),
     (store_time_of_day, ":cur_hour"),
     (ge, ":cur_hour", 18),

     (store_random_in_range, ":rand_no", 0, 4),
     (this_or_next|ge, ":cur_hour", 22),
     (eq, ":rand_no", 0),

     (assign, "$g_last_report_control_day", ":cur_day"),

     (store_troop_gold, ":gold", "trp_player"),

     (try_begin),
       (lt, ":gold", 0),
       (store_sub, ":gold_difference", 0, ":gold"),
       (troop_add_gold, "trp_player", ":gold_difference"),
     (try_end),

     (party_get_morale, ":main_party_morale", "p_main_party"),

     #(assign, ":swadian_soldiers_are_upset_message_showed", 0),
     #(assign, ":vaegir_soldiers_are_upset_message_showed", 0),
     #(assign, ":khergit_soldiers_are_upset_message_showed", 0),
     #(assign, ":nord_soldiers_are_upset_message_showed", 0),
     #(assign, ":rhodok_soldiers_are_upset_message_showed", 0),

     (try_begin),
       (str_store_string, s1, "str_party_morale_is_low"),
       (str_clear, s2),

       (party_get_num_companion_stacks, ":num_stacks","p_main_party"),
       (assign, ":num_deserters_total", 0),
       (party_clear, "p_temp_party"), # ready to collect all desert troops ## CC
       (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
         (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":i_stack"),
         (neg|troop_is_hero, ":stack_troop"),
         #occc zombies never desert
         (troop_get_type, ":is_undead", ":stack_troop"),
         (assign,":never_runaway",0),
         (try_begin),
            (this_or_next|eq, ":is_undead", 4),#tf_skeleton
            (eq, ":is_undead", 2),#tf_undead
            (neg|is_between, ":stack_troop", customizable_troops_begin,  customizable_troops_end),#NOT custom troops
            (assign,":never_runaway",1),
         (try_end),
         (eq,":never_runaway",0),
         
         (party_stack_get_size, ":stack_size", "p_main_party", ":i_stack"),

         (store_troop_faction, ":faction_no", ":stack_troop"),

         (assign, ":troop_morale", ":main_party_morale"),
         (try_begin),
           (ge, ":faction_no", kingdoms_begin), ## NMC
           (lt, ":faction_no", kingdoms_end), ## NMC

           (faction_get_slot, ":troop_morale_addition", ":faction_no",  slot_faction_morale_of_player_troops),
           (val_div, ":troop_morale_addition", 100),
           (val_add, ":troop_morale", ":troop_morale_addition"),
         (try_end),

         (lt, ":troop_morale", 32),
         (store_sub, ":desert_prob", 36, ":troop_morale"),
         (val_div, ":desert_prob", 4),

         (assign, ":num_deserters_from_that_troop", 0),
         (try_for_range, ":unused", 0, ":stack_size"),
           (store_random_in_range, ":rand_no", 0, 100),
           (lt, ":rand_no", ":desert_prob"),
           (val_add, ":num_deserters_from_that_troop", 1),
           #p.remove_members_from_stack(i_stack,cur_deserters, &main_party_instances);
           (remove_member_from_party, ":stack_troop", "p_main_party"),
           (party_add_members, "p_temp_party", ":stack_troop", 1), ## CC
         (try_end),
         (try_begin),
           (ge, ":num_deserters_from_that_troop", 1),
           (str_store_troop_name, s2, ":stack_troop"),
           (assign, reg0, ":num_deserters_from_that_troop"),
           (try_begin),
             (ge, ":num_deserters_total", 1),
             (str_store_string, s1, "str_s1_reg0_s2"),
           (else_try),
             (str_store_string, s3, s1),
             (str_store_string, s1, "str_s3_reg0_s2"),
           (try_end),
           (val_add, ":num_deserters_total", ":num_deserters_from_that_troop"),
         (try_end),
       (try_end),

       (try_begin),
         (ge, ":num_deserters_total", 1),
      ## CC begin
         (set_spawn_radius, 2),
         (spawn_around_party, "p_main_party", "pt_deserters"),
         (assign, ":new_party", reg0),
         (call_script, "script_party_copy", ":new_party", "p_temp_party"),
      ## CC end
         (try_begin),
           (ge, ":num_deserters_total", 2),
           (str_store_string, s2, "str_have_deserted_the_party"),
         (else_try),
           (str_store_string, s2, "str_has_deserted_the_party"),
         (try_end),

         (str_store_string, s1, "str_s1_s2"),

         (eq, "$g_infinite_camping", 0),

         (tutorial_box, s1, "str_weekly_report"),
       (try_end),
     (try_end),
 ]),
 # reserved for future use. For backward compatibility, we need to use these triggers instead of creating new ones.

  (1,
   [
     (call_script, "script_calculate_castle_prosperities_by_using_its_villages"),

     (store_add, ":fac_kingdom_6_plus_one", "fac_kingdom_6", 1),

     (try_for_range, ":faction_1", "fac_kingdom_1", ":fac_kingdom_6_plus_one"),
       (try_for_range, ":faction_2", "fac_kingdom_1", ":fac_kingdom_6_plus_one"),
         (store_relation, ":faction_relation", ":faction_1", ":faction_2"),
         (str_store_faction_name, s7, ":faction_1"),
         (str_store_faction_name, s8, ":faction_2"),
         (neq, ":faction_1", ":faction_2"),
         (assign, reg1, ":faction_relation"),
         #(display_message, "@{s7}-{s8}, relation is {reg1}"),
       (try_end),
     (try_end),
   ]),

  (1,
   [
     (try_begin),
       (eq, "$g_player_is_captive", 1),
       (neg|party_is_active, "$capturer_party"),
       (rest_for_hours, 0, 0, 0),
     (try_end),

     ##diplomacy begin
      #seems to be a native bug
     (is_between, "$next_center_will_be_fired", villages_begin, villages_end),
     ##diplomacy end
     (assign, ":village_no", "$next_center_will_be_fired"),
     (party_get_slot, ":is_there_already_fire", ":village_no", slot_village_smoke_added),
     (eq, ":is_there_already_fire", 0),


     (try_begin),
       (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
       (party_get_slot, ":last_nearby_fire_time", ":bound_center", slot_town_last_nearby_fire_time),
       (store_current_hours, ":cur_hours"),

	   (try_begin),
		(eq, "$cheat_mode", 1),
		(is_between, ":village_no", centers_begin, centers_end),
		(is_between, ":bound_center", centers_begin, centers_end),
		(str_store_party_name, s4, ":village_no"),
		(str_store_party_name, s5, ":bound_center"),
		(store_current_hours, reg3),
        (party_get_slot, reg4, ":bound_center", slot_town_last_nearby_fire_time),
		(display_message, "@{!}DEBUG - Checking fire at {s4} for {s5} - current time {reg3}, last nearby fire {reg4}"),
	   (try_end),


       (eq, ":cur_hours", ":last_nearby_fire_time"),
       (party_add_particle_system, ":village_no", "psys_map_village_fire"),
       (party_add_particle_system, ":village_no", "psys_map_village_fire_smoke"),
     (else_try),
       (store_add, ":last_nearby_fire_finish_time", ":last_nearby_fire_time", fire_duration),
       (eq, ":last_nearby_fire_finish_time", ":cur_hours"),
       (party_clear_particle_systems, ":village_no"),
     (try_end),


   ]),

  (24,
   [
   (val_sub, "$g_dont_give_fief_to_player_days", 1),
   (val_max, "$g_dont_give_fief_to_player_days", -1),
   (val_sub, "$g_dont_give_marshalship_to_player_days", 1),
   (val_max, "$g_dont_give_marshalship_to_player_days", -1),

   ##diplomacy start+
   ##Add version checking, so the corrections are only applied once.
   ##This allows for more complicated things to be added here in the future
   (troop_get_slot, ":diplomacy_version_code", "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated),#I've arbitrarily picked "when I started tracking this" as 0
   (store_mod, ":verification", ":diplomacy_version_code", 128),
   (assign, ":save_reg0", reg0),
   (assign, ":save_reg1", reg1),
   (try_begin),
		#Detect bad values
		(neq, ":diplomacy_version_code", 0),
		(neq, ":verification", 68),
		(assign, reg0, ":diplomacy_version_code"),
		(display_message, "@{!} A slot had an unexpected value: {reg0}.  This might be because you are using an incompatible troop list, or are using a non-native strange game.  This message will repeat daily."),
		(assign, ":diplomacy_version_code", -1),
	(else_try),
		(val_div, ":diplomacy_version_code", 128),
		#Update if necessary.
		(lt, ":diplomacy_version_code", DPLMC_CURRENT_VERSION_CODE),
		(ge, "$cheat_mode", 1),
		(assign, reg0, ":diplomacy_version_code"),

		(assign, reg1, DPLMC_CURRENT_VERSION_CODE),
		(display_message, "@{!} DEBUG - Detected a new version of diplomacy: previous version was {reg0}, and current version is {reg1}.  Performing updates."),
		(val_mul, reg1, 128),
		(val_add, reg1, DPLMC_VERSION_LOW_7_BITS),
		(troop_set_slot, "trp_dplmc_chamberlain", dplmc_slot_troop_affiliated, reg1),
	(try_end),

	(try_begin),
	(is_between, ":diplomacy_version_code", -1, 1),#-1 or 0
	#Native behavior follows
	##diplomacy end+

   #this to correct string errors in games started in 1.104 or before
   (party_set_name, "p_steppe_bandit_spawn_point", "str_the_steppes"),
   (party_set_name, "p_taiga_bandit_spawn_point", "str_the_tundra"),
   (party_set_name, "p_forest_bandit_spawn_point", "str_the_forests"),
   (party_set_name, "p_mountain_bandit_spawn_point", "str_the_highlands"),
   (party_set_name, "p_sea_raider_spawn_point_1", "str_the_coast"),
   (party_set_name, "p_sea_raider_spawn_point_2", "str_the_coast"),
   (party_set_name, "p_desert_bandit_spawn_point", "str_the_deserts"),


   #this to correct inappropriate home strings - Katrin to Uxkhal, Matheld to Fearichen
   (troop_set_slot, "trp_npc11", slot_troop_home, "p_town_7"),
   (troop_set_slot, "trp_npc8", slot_troop_home, "p_village_35"),

   (troop_set_slot, "trp_npc15", slot_troop_town_with_contacts, "p_town_20"), #durquba

   #this to correct linen production at villages of durquba
   (party_set_slot, "p_village_93", slot_center_linen_looms, 0), #mazigh
   (party_set_slot, "p_village_94", slot_center_linen_looms, 0), #sekhtem
   (party_set_slot, "p_village_95", slot_center_linen_looms, 0), #qalyut
   (party_set_slot, "p_village_96", slot_center_linen_looms, 0), #tilimsal
   (party_set_slot, "p_village_97", slot_center_linen_looms, 0), #shibal zumr
   (party_set_slot, "p_village_102", slot_center_linen_looms, 0), #tamnuh
   (party_set_slot, "p_village_109", slot_center_linen_looms, 0), #habba

   (party_set_slot, "p_village_67", slot_center_fishing_fleet, 0), #Tebandra
   (party_set_slot, "p_village_5", slot_center_fishing_fleet, 15), #Kulum

   ##diplomacy start+
   #End the changes in Native
	(try_end),

   #Behavior specific to a fresh Diplomacy version
	(try_begin),
   (ge, ":diplomacy_version_code", 0),#do not run this if the code is bad
   (lt, ":diplomacy_version_code", 1),
   #Add home centers for claimants (mods not using standard NPCs or map may wish to remove this)
   (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_4"),#Lady Isolle - Suno
   (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_11"),#Prince Valdym - Curaw
   (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_18"),#Dustum Khan - Narra
   (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_12"),#Lethwin Far-Seeker - Wercheg
   (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_3"),#Lord Kastor - Veluca
   (troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_20"),#Arwa the Pearled One - Durquba
   #add ancestral fiefs to home slots (mods not using standard NPCs or map should remove this)
   (troop_set_slot, "trp_knight_2_10", slot_troop_home, "p_castle_29"), #Nelag_Castle
   (troop_set_slot, "trp_knight_3_4", slot_troop_home, "p_castle_30"), #Asugan_Castle
   (troop_set_slot, "trp_knight_1_3", slot_troop_home, "p_castle_35"), #Haringoth_Castle
   (troop_set_slot, "trp_knight_5_11", slot_troop_home, "p_castle_33"), #Etrosq_Castle
   #Also the primary six towns (mods not using standard NPCs or map may wish to remove this)
   (troop_set_slot, "trp_kingdom_1_lord", slot_troop_home, "p_town_6"),#King Harlaus to Praven
   (troop_set_slot, "trp_kingdom_2_lord", slot_troop_home, "p_town_8"),#King Yaroglek to Reyvadin
   (troop_set_slot, "trp_kingdom_3_lord", slot_troop_home, "p_town_10"),#Sanjar Khan to Tulga
   (troop_set_slot, "trp_kingdom_4_lord", slot_troop_home, "p_town_1"),#King Ragnar to Sargoth
   (troop_set_slot, "trp_kingdom_5_lord", slot_troop_home, "p_town_5"),#King Graveth to Jelkala
   (troop_set_slot, "trp_kingdom_6_lord", slot_troop_home, "p_town_19"),#Sultan Hakim to Shariz
   #occc begin
   
   
   #occc end

   #Set the "original lord" values corresponding to the above.
   (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
		(this_or_next|eq, ":troop_no", "trp_knight_2_10"),#Nelag
		(this_or_next|eq, ":troop_no", "trp_knight_3_4"),#Asugan
		(this_or_next|eq, ":troop_no", "trp_knight_1_3"),#Haringoth
		(this_or_next|eq, ":troop_no", "trp_knight_5_11"),#Etrosq
		(this_or_next|is_between, ":troop_no", kings_begin, kings_end),
			(is_between, ":troop_no", pretenders_begin, pretenders_end),

		(troop_get_slot, ":center_no", ":troop_no", slot_troop_home),
		(is_between, ":center_no", centers_begin, centers_end),
		(neg|party_slot_ge, ":center_no", dplmc_slot_center_original_lord, 1),
		(party_set_slot, ":center_no",  dplmc_slot_center_original_lord, ":troop_no"),

		#Also set "ex-lord"
		(neg|is_between, ":troop_no", pretenders_begin, pretenders_end),
		(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
		(neg|party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
		(neg|party_slot_ge, ":center_no", dplmc_slot_center_ex_lord, 1),
		(party_set_slot, ":center_no", dplmc_slot_center_ex_lord, ":troop_no"),
   (try_end),

   #Make sure the affiliation slot is set correctly.
   (try_begin),
	 (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
	 (troop_get_slot, ":slot_val", "$g_player_affiliated_troop", dplmc_slot_troop_affiliated),
	 (is_between, ":slot_val", 0, 3),#0 is default, 1 is asked, in previous versions there was no use of 2
	 (troop_set_slot, "$g_player_affiliated_troop", dplmc_slot_troop_affiliated, 3),#3 is affiliated
   (try_end),

   #Set father/mother slots for the unmarried medium-age lords, so checking for
   #being related will work as expected.
   (try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_slot_eq, ":troop_no", slot_troop_father, -1),
		(troop_slot_eq, ":troop_no", slot_troop_mother, -1),
		(store_mul, ":father", ":troop_no", DPLMC_VIRTUAL_RELATIVE_MULTIPLIER),#defined in module_constants.py
		(val_add, ":father", DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),
		(troop_set_slot, ":troop_no", slot_troop_father, ":father"),
		(store_add, ":mother", ":father", DPLMC_VIRTUAL_RELATIVE_MOTHER_OFFSET - DPLMC_VIRTUAL_RELATIVE_FATHER_OFFSET),
		(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
   (try_end),

   #Fix kingdom lady daughters having "slot_troop_mother" set to themselves.
   #The old fix was in troop_get_family_relation_to_troop, but now we can
   #just do it once here.
   (try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(try_begin),
			(troop_slot_eq, ":troop_no", slot_troop_mother, ":troop_no"),
			(troop_get_slot, ":father", ":troop_no", slot_troop_father),
			(try_begin),
				(is_between, ":father", active_npcs_begin, active_npcs_end),
				(troop_get_slot, ":mother", ":father", slot_troop_spouse),
				(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
				(try_begin),
					#Print a message if desired
					(ge, "$cheat_mode", 1),
					(str_store_troop_name, s0, ":troop_no"),
					(display_message, "@{!}DEBUG - Fixed slot_troop_mother for {s0}."),
				(try_end),
			(else_try),
				(troop_set_slot, ":troop_no", slot_troop_mother, -1),#better than being set to herself
				#Print a message if desired
				(ge, "$cheat_mode", 1),
				(str_store_troop_name, s0, ":troop_no"),
				(display_message, "@{!}DEBUG - When fixing slot_troop_mother for {s0}, could not find a valid mother."),
			(try_end),
	#While we're at it, also give parents to the sisters of the middle-aged lords.
		(else_try),
			(troop_slot_eq, ":troop_no", slot_troop_father, -1),
			(troop_slot_eq, ":troop_no", slot_troop_mother, -1),
			#"Guardian" here means brother
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
			(ge, ":guardian", 1),
			#Has brother's father
			(troop_get_slot, ":father", ":guardian", slot_troop_father),
			(troop_set_slot, ":troop_no", slot_troop_father, ":father"),
			#Has brother's mother
			(troop_get_slot, ":mother", ":guardian", slot_troop_mother),
			(troop_set_slot, ":troop_no", slot_troop_mother, ":mother"),
		(try_end),
   #Also set original factions for ladies.
	   (neg|troop_slot_ge, ":troop_no", slot_troop_original_faction, 1),
		(assign, ":guardian", -1),
		(try_begin),
		   (troop_slot_ge, ":troop_no", slot_troop_father, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_father),
 	   (else_try),
		   (troop_slot_ge, ":troop_no", slot_troop_guardian, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_guardian),
		(else_try),
		   (troop_slot_ge, ":troop_no", slot_troop_spouse, 1),
			(troop_get_slot, ":guardian", ":troop_no", slot_troop_spouse),
	   (try_end),
		(ge, ":guardian", 1),
		(troop_get_slot, ":original_faction", ":guardian", slot_troop_original_faction),
		(troop_set_slot, ":troop_no", slot_troop_original_faction, ":original_faction"),
   (try_end),

	  ##Set relations between kingdom ladies and their relatives.
	  ##Do *not* initialize their relations with anyone they aren't related to:
	  ##that is used for courtship.
	  ##  The purpose of this initialization is so if a kingdom lady gets promoted,
	  ##her relations aren't a featureless slate.  Also, it would be interesting to
	  ##further develop the idea of ladies as pursuing agendas even if they aren't
	  ##leading warbands, which would benefit from giving them relations with other
	  ##people.
	  #
	  #Because relations may already exist, only call this in instances where
	  #they are 0 or 1 (the latter just means "met" between NPCs).
     (try_for_range, ":lady", kingdom_ladies_begin, kingdom_ladies_end),
		(troop_slot_eq, ":lady", slot_troop_occupation, slto_kingdom_lady),
		(troop_get_slot, ":lady_faction", ":lady", slot_troop_original_faction),
		(ge, ":lady_faction", 1),

		(try_for_range, ":other_hero", heroes_begin, heroes_end),
		   (this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(this_or_next|troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_hero),
				(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_inactive_pretender),
			(troop_slot_eq, ":other_hero", slot_troop_original_faction, ":lady_faction"),

			#Because this is not a new game: first check if relations have developed
			(call_script, "script_troop_get_relation_with_troop", ":lady", ":other_hero"),
			(is_between, reg0, 0, 2),#0 or 1

			(try_begin),
				(this_or_next|troop_slot_eq, ":lady", slot_troop_spouse, ":other_hero"),
				(troop_slot_eq, ":other_hero", slot_troop_spouse, ":lady"),
				(store_random_in_range, reg0, 0, 11),
			(else_try),
				#(call_script, "script_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
				(call_script, "script_dplmc_troop_get_family_relation_to_troop", ":lady", ":other_hero"),
			(try_end),

			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", reg0),

			#This relation change only applies between kingdom ladies.
			(troop_slot_eq, ":other_hero", slot_troop_occupation, slto_kingdom_lady),
			(is_between, ":other_hero", kingdom_ladies_begin, kingdom_ladies_end),

			(store_random_in_range, ":random", 0, 11),
			(call_script, "script_troop_change_relation_with_troop", ":lady", ":other_hero", ":random"),
		(try_end),
	  (try_end),

   #Change the occupation of exiled lords (not including pretenders or kings)
   (try_for_range, ":troop_no", lords_begin, lords_end),
		(store_troop_faction, ":faction_no", ":troop_no"),
		#A lord in the outlaw faction
		(eq, ":faction_no", "fac_outlaws"),
		#Possible values for his occupation if he's an exile (but there's some overlap between these and "bandit hero")
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),#<- The default
		(this_or_next|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),#<- This can happen joining the player faction
			(troop_slot_eq, ":troop_no", slot_troop_occupation, 0),#<- This gets set for prisoners
		#(Quick Check) Not leading a party or the prisoner of a party or at a center
		(neg|troop_slot_ge, ":troop_no", slot_troop_leaded_party, 0),
		(neg|troop_slot_ge, ":troop_no", slot_troop_prisoner_of_party, 0),
		(neg|troop_slot_ge, ":troop_no", slot_troop_cur_center, 1),#deliberately 1 instead of 0
		#(Slow check) Does not own any fiefs
		(assign, ":end", centers_end),
		(try_for_range, ":center_no", centers_begin, ":end"),
			(party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
			(assign, ":end", ":center_no"),#stop loop, and also signal failure
		(try_end),
		#(Slow check) Explicitly verify he is not a prisoner anywhere.
		(call_script, "script_search_troop_prisoner_of_party", ":troop_no"),
		(eq, reg0, -1),
		#(Slow check) Explicitly verify he's not a member of any party
		(assign, ":member_of_party", -1),
		(try_for_parties, ":party_no"),
			(eq, ":member_of_party", -1),
			(this_or_next|eq, ":party_no", "p_main_party"),
				(ge, ":party_no", centers_begin),
			(party_count_members_of_type, ":count", ":party_no", ":troop_no"),
			(gt, ":count", 0),
			(assign, ":member_of_party", ":party_no"),
		(try_end),
		(eq, ":member_of_party", -1),
		#Finally verified that he is in exile.  Set the slot value to make
		#this easier in the future.
		(troop_set_slot, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
		(try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s0, ":troop_no"),
			(display_message, "@{!}DEBUG - Changed occupation of {s0} to dplmc_slto_exile"),
		(try_end),
   (try_end),

   #Initialize histories for supported pretenders.
   (try_for_range, ":troop_no", pretenders_begin, pretenders_end),
      (neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (troop_slot_eq, ":troop_no", slot_troop_playerparty_history, 0),
	  (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
   (try_end),

   #Initialize histories for promoted companions
   (try_for_range, ":troop_no", companions_begin, companions_end),
	  (neg|troop_slot_eq, ":troop_no", slot_troop_met, 0),
      (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
	  (neg|troop_slot_eq, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_nonplayer_entry),
	  (troop_set_slot, ":troop_no", slot_troop_playerparty_history, dplmc_pp_history_granted_fief),
   (try_end),

   #For all centers, update new slots
   (try_for_range, ":center_no", centers_begin, centers_end),
	  #Last attacker
	  (try_begin),
	     (party_slot_eq, ":center_no", dplmc_slot_center_last_attacker, 0),
		 (party_slot_eq, ":center_no", dplmc_slot_center_last_attacked_time, 0),
		 (party_set_slot, ":center_no", dplmc_slot_center_last_attacker, -1),
	  (try_end),

      (party_slot_eq, ":center_no", dplmc_slot_center_last_transfer_time, 0),
	  #Ex-lord
	  (try_begin),
  	     (party_slot_eq, ":center_no", dplmc_slot_center_ex_lord, 0),
	     (party_set_slot, ":center_no", dplmc_slot_center_ex_lord, -1),
	  (try_end),
	  #Original lord
	  (try_begin),
		(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, 0),
		(neg|troop_slot_eq, "trp_player", slot_troop_home, ":center_no"),
		(party_set_slot, ":center_no", dplmc_slot_center_original_lord, -1),
	  (try_end),
   (try_end),

   #Don't bother filling in "last caravan arrival" slots with fake values.
   #Right now the scripts check and do that automatically if they aren't
   #set.

   #Fix a mistake I had introduced before, where you could get the wrong
   #"marry betrothed" quest when courting a lady.
   (try_begin),
      (check_quest_active, "qst_wed_betrothed_female"),
	  (quest_get_slot, ":betrothed_troop", "qst_wed_betrothed_female", slot_quest_giver_troop),
	  (is_between, ":betrothed_troop", kingdom_ladies_begin, kingdom_ladies_end),
	  (display_message, "@{!}FIXED PROBLEM - Cancelled erroneous version of qst_wed_betrothed_female.  You should be able to marry normally if you try again."),
	  (call_script, "script_abort_quest", "qst_wed_betrothed_female", 0),#abort with type 0 "event" should give no penalties to the player
   (try_end),
   #End version-checked block.
   (try_end),

   (try_begin),
    (ge, ":diplomacy_version_code", 1),
    (lt, ":diplomacy_version_code", 110615),
    #Fix a bug that was introduced in some version before 2011-06-15 that made
	#all "young unmarried lords" only have half-siblings, with either their own
	#father or mother slot uninitialized.
	(try_begin),
		(lt, 31, heroes_begin),
		(neg|troop_slot_eq, 31, 31, 0),#"slot_troop_father" was 31 in those saved games
		(troop_set_slot, 31, 31, -1),#(it still is 31 as far as I know, but this code should remain the same even if the slot value changes)
	(try_end),
	(try_begin),
		(lt, 32, heroes_begin),
		(neg|troop_slot_eq, 32,32,0),#"slot_troop_mother" was 32 in those saved games
		(troop_set_slot, 32, 32, -1),
	(try_end),
	(try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_get_slot, reg0, ":troop_no", slot_troop_father),
		(troop_get_slot, reg1, ":troop_no", slot_troop_mother),
		(try_begin),
			(is_between, reg0, lords_begin, lords_end),
			(neg|is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(troop_get_slot, reg1, reg0, slot_troop_spouse),
			(is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(troop_set_slot, ":troop_no", slot_troop_mother, reg1),
			(call_script, "script_update_troop_notes", ":troop_no"),#Doesn't actually do anything
		(else_try),
			(is_between, reg1, kingdom_ladies_begin, kingdom_ladies_end),
			(neg|is_between, reg0, lords_begin, lords_end),
			(troop_get_slot, reg0, reg1, slot_troop_spouse),
			(is_between, reg0, lords_begin, lords_end),
			(troop_set_slot, ":troop_no", slot_troop_father, reg0),
			(call_script, "script_update_troop_notes", ":troop_no"),#Doesn't actually do anything
		(try_end),
	(try_end),

	#For old saved games, a reputation bug that was introduced in the release 2011-06-06 and was fixed on 2011-06-07.
	(eq, ":diplomacy_version_code", 1),
	(assign, reg0, 0),
	(try_for_range, ":troop_no", lords_begin, lords_end),
		(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_none),
		(store_random_in_range, reg1, lrep_none, lrep_roguish),
		(val_max, reg1, lrep_none + 1),#So there's an extra chance of getting reputation 1, which is lrep_martial
		(troop_set_slot, ":troop_no", slot_lord_reputation_type, reg1),
		(val_add, reg0, 1),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(store_sub, reg1, reg0, 1),
		(display_message, "@{!} Bug fix: set personality types for {reg0} {reg1?lords:lord}"),
	(try_end),

	(assign, reg0, 0),
	(try_for_range, ":troop_no", kingdom_ladies_begin, kingdom_ladies_end),
		(neq, ":troop_no", "trp_knight_1_1_wife"),#That lady should not appear in the game
		(troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_none),
		(store_random_in_range, reg1, lrep_conventional - 1, lrep_moralist + 1),
		(val_max, reg1, lrep_conventional),#So there's an extra chance of getting lrep_conventional
		(troop_set_slot, ":troop_no", slot_lord_reputation_type, reg1),
		(val_add, reg0, 1),
	(try_end),

	(try_begin),
		(ge, "$cheat_mode", 1),
		(store_sub, reg1, reg0, 1),
		(display_message, "@{!} Bug fix: set personality types for {reg0} {reg1?ladies:lady}"),
	(try_end),
   (try_end),

   #Behavior for an upgrade from Native or pre-Diplomacy 4.0 to Diplomacy 4.0
   (try_begin),
      (is_between, ":diplomacy_version_code", 0, 111001),
      #Fix: slot_faction_leader and slot_faction_marshall should not equal trp_player
      #if the player is not a member of the faction.  (This is initially true because
      #trp_player is 0, and uninitialized slots default to 0.)
      (try_for_range, ":faction_no", 0, dplmc_factions_end),
         (neq, ":faction_no", "fac_player_faction"),
         (neq, ":faction_no", "fac_player_supporters_faction"),
         (this_or_next|neq, ":faction_no", "$players_kingdom"),
         (eq, ":faction_no", 0),
         #The player is not a member of the faction:
         (try_begin),
            (faction_slot_eq, ":faction_no", slot_faction_leader, 0),
            (faction_set_slot, ":faction_no", slot_faction_leader, -1),
         (try_end),
         (try_begin),
            (faction_slot_eq, ":faction_no", slot_faction_marshall, 0),
            (faction_set_slot, ":faction_no", slot_faction_marshall, -1),
         (try_end),
      (try_end),
      #Initialize home slots for town merchants, elders, etc.
      (try_for_range, ":center_no", centers_begin, centers_end),
         (try_for_range, ":troop_no", dplmc_slot_town_merchants_begin, dplmc_slot_town_merchants_end),
            (party_get_slot, ":troop_no", ":center_no", ":troop_no"),
            (gt, ":troop_no", walkers_end),
            (troop_is_hero, ":troop_no"),
            (troop_slot_eq, ":troop_no", slot_troop_home, 0),
            (troop_set_slot, ":troop_no", slot_troop_home, ":center_no"),
         (try_end),
      (try_end),
      #Initialize home slots for startup merchants.  (Merchant of Praven, etc.)
      #This should be done after kings have their home slots initialized.
      (try_for_range, ":troop_no", kings_begin, kings_end),
         (troop_get_slot, ":center_no", ":troop_no", slot_troop_home),
         (val_sub, ":troop_no", kings_begin),
         (val_add, ":troop_no", startup_merchants_begin),
         (is_between, ":troop_no", startup_merchants_begin, startup_merchants_end),#Right now there's a startup merchant for each faction.  Verify this hasn't unexpectedly changed.
         (neg|troop_slot_ge, ":troop_no", slot_troop_home, 1),#Verify that the home slot is not already set
         (troop_set_slot, ":troop_no", slot_troop_home, ":center_no"),
      (try_end),
      #Reset potentially bad value in "slot_troop_stance_on_faction_issue" (i.e. 153) from auto-loot
      (eq, 153, slot_troop_stance_on_faction_issue),
      (try_for_range, ":troop_no", companions_begin, companions_end),
         (try_begin),
            (neg|troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
         (else_try),
            (troop_get_slot, ":slot_val", ":troop_no", slot_troop_stance_on_faction_issue),
            (neg|is_between, ":slot_val", -1, 1),#0 or -1
            (neg|is_between, ":slot_val", heroes_begin, heroes_end),
            (troop_set_slot, ":troop_no", slot_troop_stance_on_faction_issue, -1),
         (try_end),
      (try_end),
   (try_end),

   (assign, reg1, ":save_reg1"),#Revert register
   (assign, reg0, ":save_reg0"),#Revert register

   #Ensure $character_gender is set correctly
   (try_begin),
      (call_script, "script_cf_dplmc_troop_is_female", "trp_player"),
	  (assign, "$character_gender", 1),
   (else_try),
	  (assign, "$character_gender", 0),
   (try_end),
   ##diplomacy end+


   #The following scripts are to end quests which should have cancelled, but did not because of a bug
   (try_begin),
	(check_quest_active, "qst_formal_marriage_proposal"),
	(check_quest_failed, "qst_formal_marriage_proposal"),
    (call_script, "script_end_quest", "qst_formal_marriage_proposal"),
   (try_end),

   (try_begin),
	(check_quest_active, "qst_lend_companion"),
	(quest_get_slot, ":giver_troop", "qst_lend_companion", slot_quest_giver_troop),
	(store_faction_of_troop, ":giver_troop_faction", ":giver_troop"),
    (store_relation, ":faction_relation", ":giver_troop_faction", "$players_kingdom"),
    (this_or_next|lt, ":faction_relation", 0),
    (neg|is_between, ":giver_troop_faction", kingdoms_begin, kingdoms_end),
    (call_script, "script_abort_quest", "qst_lend_companion", 0),
   (try_end),



   (try_begin),
	(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
	(neq, "$players_kingdom", "fac_player_supporters_faction"),
    (faction_slot_eq, "$players_kingdom", slot_faction_marshall, "trp_player"),
    (val_add, "$g_player_days_as_marshal", 1),
   (else_try),
    (assign, "$g_player_days_as_marshal", 0),
   (try_end),

   (try_for_range, ":town", towns_begin, towns_end),
	(party_get_slot, ":days_to_completion", ":town", slot_center_player_enterprise_days_until_complete),
    (ge, ":days_to_completion", 1),
	(val_sub, ":days_to_completion", 1),
	(party_set_slot, ":town", slot_center_player_enterprise_days_until_complete, ":days_to_completion"),
   (try_end),
    ]),
(24,
   [
	  # Setting food bonuses in every 6 hours again and again because of a bug (we could not find its reason) which decreases especially slot_item_food_bonus slots of items to 0.
	  #Staples
      (item_set_slot, "itm_bread", slot_item_food_bonus, 8), #brought up from 4
      (item_set_slot, "itm_grain", slot_item_food_bonus, 2), #new - can be boiled as porridge
	  
	  #Fat sources - preserved
      (item_set_slot, "itm_smoked_fish", slot_item_food_bonus, 4),
      (item_set_slot, "itm_dried_meat", slot_item_food_bonus, 5),
      (item_set_slot, "itm_cheese", slot_item_food_bonus, 5),
      (item_set_slot, "itm_sausages", slot_item_food_bonus, 5),
      (item_set_slot, "itm_butter", slot_item_food_bonus, 4), #brought down from 8

	  #Fat sources - perishable
      (item_set_slot, "itm_chicken", slot_item_food_bonus, 8), #brought up from 7
      (item_set_slot, "itm_cattle_meat", slot_item_food_bonus, 7), #brought down from 7
      (item_set_slot, "itm_pork", slot_item_food_bonus, 6), #brought down from 6
	  
	  #Produce
      (item_set_slot, "itm_raw_olives", slot_item_food_bonus, 1),
      (item_set_slot, "itm_cabbages", slot_item_food_bonus, 2),
      (item_set_slot, "itm_raw_grapes", slot_item_food_bonus, 3),
      (item_set_slot, "itm_apples", slot_item_food_bonus, 4), #brought down from 5

	  #Sweet items
      (item_set_slot, "itm_raw_date_fruit", slot_item_food_bonus, 4), #brought down from 8
      (item_set_slot, "itm_honey", slot_item_food_bonus, 6), #brought down from 12
      
      (item_set_slot, "itm_wine", slot_item_food_bonus, 5),
      (item_set_slot, "itm_ale", slot_item_food_bonus, 4),
   ]),



## CC - npc read book
  (1, [
     (try_for_range, ":troop_no", companions_begin, companions_end),
       (neg|map_free),
       (troop_get_slot, ":item_no", ":troop_no", slot_troop_current_reading_book),
       (gt, ":item_no", 0),
       (call_script, "script_get_troop_item_amount", ":troop_no", ":item_no"),
       (assign, ":continue", 1),
       (try_begin),
         (eq, reg0, 0),
         (troop_set_slot, "$g_talk_troop", slot_troop_current_reading_book, 0),
         (assign, ":continue", 0),
       (try_end),
       (eq, ":continue", 1),
       (store_attribute_level, ":int", ":troop_no", ca_intelligence),
       (item_get_slot, ":int_req", ":item_no", slot_item_intelligence_requirement),
       (le, ":int_req", ":int"),

       (call_script, "script_get_book_read_slot", ":troop_no", ":item_no"),
       (assign, ":slot_no", reg0),
       (troop_get_slot, ":book_read", "trp_book_read", ":slot_no"),
       (troop_get_slot, ":book_reading_progress", "trp_book_reading_progress", ":slot_no"),
       
       (eq, ":book_read", 0),
       (assign, ":read_speed", 0),
       (try_for_range, ":other_troop", companions_begin, companions_end),
         (neq, ":other_troop", ":troop_no"),
         (main_party_has_troop, ":other_troop"),
         (call_script, "script_get_book_read_slot", ":other_troop", ":item_no"),
         (assign, ":other_slot_no", reg0),
         (troop_slot_eq, "trp_book_read", ":other_slot_no", 1),
         (val_add, ":read_speed", 1),
       (try_end),
       (try_begin),
         (item_slot_eq, ":item_no", slot_item_book_read, 1),
         (val_add, ":read_speed", 1),
       (try_end),
       (val_div, ":read_speed", 4),
       (val_add, ":read_speed", 3),
       
       (val_add, ":book_reading_progress", ":read_speed"),
       (troop_set_slot, "trp_book_reading_progress", ":slot_no", ":book_reading_progress"),
       
       (ge, ":book_reading_progress", 1000),
       (troop_set_slot, "trp_book_read", ":slot_no", 1),
       (troop_set_slot, "trp_book_reading_progress", ":slot_no", 1000),
       (troop_set_slot, ":troop_no", slot_troop_current_reading_book, 0),
       
       (str_store_troop_name, s1, ":troop_no"),
       (str_store_item_name, s2, ":item_no"),
       (str_clear, s3),
       (try_begin),
         (eq, ":item_no", "itm_book_tactics"),
         (troop_raise_skill, ":troop_no", "skl_tactics", 1),
         (str_store_string, s3, "@ {s1}'s tactics skill has increased by 1."),
       (else_try),
         (eq, ":item_no", "itm_book_persuasion"),
         (troop_raise_skill, ":troop_no", "skl_persuasion", 1),
         (str_store_string, s3, "@ {s1}'s persuasion skill has increased by 1."),
       (else_try),
         (eq, ":item_no", "itm_book_leadership"),
         (troop_raise_skill, ":troop_no", "skl_leadership", 1),
         (str_store_string, s3, "@ {s1}'s leadership skill has increased by 1."),
## CC begin
       (else_try),
         (eq, ":item_no", "itm_book_prisoner_management"),
         (troop_raise_skill, ":troop_no", "skl_prisoner_management", 1),
         (str_store_string, s3, "@ {s1}'s prisoner management skill has increased by 1."),
## CC end
       (else_try),
         (eq, ":item_no", "itm_book_intelligence"),
         (troop_raise_attribute, ":troop_no", ca_intelligence, 1),
         (str_store_string, s3, "@ {s1}'s intelligence has increased by 1."),
       (else_try),
         (eq, ":item_no", "itm_book_trade"),
         (troop_raise_skill, ":troop_no", "skl_trade", 1),
         (str_store_string, s3, "@ {s1}'s trade skill has increased by 1."),
       (else_try),
         (eq, ":item_no", "itm_book_weapon_mastery"),
         (troop_raise_skill, ":troop_no", "skl_weapon_master", 1),
         (str_store_string, s3, "@ {s1}'s weapon master skill has increased by 1."),
       (else_try),
         (eq, ":item_no", "itm_book_engineering"),
         (troop_raise_skill, ":troop_no", "skl_engineer", 1),
         (str_store_string, s3, "@ {s1}'s engineer skill has increased by 1."),
       (try_end),
       (display_message, "@{s1} have finished reading {s2}.{s3}", 0x88ff88),
       (assign, ":item_no", 0),
     (try_end),
   ]),
   
  (2, [#(call_script, "script_combine_parties_of_same_template"),
   ]),  ## CC-D del: for making the game lighter imported from difor 0.58
   
  (24,
    [
      #(try_for_range, ":loop_var", "trp_kingdom_heroes_including_player_begin", companions_end),
        #(assign, ":cur_troop", ":loop_var"),
        #(try_begin),
          #(eq, ":loop_var", "trp_kingdom_heroes_including_player_begin"),
          #(assign, ":cur_troop", "trp_player"),
        #(try_end),
        #(main_party_has_troop, ":cur_troop"),
        #(assign, ":continue", 0),
        #(try_for_range, ":slot_proficiency_type", slot_one_handed_proficiency_limit, slot_throwing_proficiency_limit+1),
          #(store_sub, ":proficiency_type", ":slot_proficiency_type", slot_one_handed_proficiency_limit),
          #(val_add, ":proficiency_type", wpt_one_handed_weapon),
          #(troop_get_slot, ":slot_proficiency_limit", ":cur_troop", ":slot_proficiency_type"),
          #(troop_get_slot, ":slot_all_proficiency_limit", ":cur_troop", slot_all_proficiency_limit),
          
          #(try_begin),
            #(eq, ":slot_proficiency_limit", 0),
            #(val_add, ":slot_proficiency_limit", proficiency_limit_increase),
          #(else_try),
            #(eq, ":slot_all_proficiency_limit", 0),
            #(val_add, ":slot_all_proficiency_limit", proficiency_limit_increase),
          #(try_end),
          
          #(str_store_troop_name, s1, ":cur_troop"),
          #(str_clear, s2),
          #(store_sub, ":out_string", ":proficiency_type", wpt_one_handed_weapon),
          #(val_add, ":out_string", "str_one_handed_weapon"),
          #(str_store_string, s2, ":out_string"),
          
          #(str_clear, s3),
          #(store_div, ":out_string", ":slot_proficiency_limit", proficiency_limit_increase),
          #(val_sub, ":out_string", 1),
          #(val_add, ":out_string", "str_level_d"),
          #(str_store_string, s3, ":out_string"),
          
          #(store_proficiency_level, ":weapon_proficiency", ":cur_troop", ":proficiency_type"),
          #(try_begin),
            #(ge, ":weapon_proficiency", ":slot_proficiency_limit"),
            #(display_message, "@{s1}'s proficiency in {s2}has reach level {s3}."),
            #(try_begin),
              #(eq, ":slot_proficiency_type", slot_one_handed_proficiency_limit),
              #(troop_raise_attribute, ":cur_troop", ca_agility, 1),
              #(display_message, "@+1 agility."),
            #(else_try),
              #(eq, ":slot_proficiency_type", slot_two_handed_proficiency_limit),
              #(call_script, "script_troop_raise_skill_limit", ":cur_troop", skl_power_strike, 1),
              #(display_message, "@+1 power strike."),
            #(else_try),
              #(eq, ":slot_proficiency_type", slot_polearm_proficiency_limit),
              #(troop_raise_attribute, ":cur_troop", ca_strength, 1),
              #(display_message, "@+1 strength."),
            #(else_try),
              #(eq, ":slot_proficiency_type", slot_archery_proficiency_limit),
              #(call_script, "script_troop_raise_skill_limit", ":cur_troop", skl_power_draw, 1),
              #(display_message, "@+1 power draw."),
            #(else_try),
              #(eq, ":slot_proficiency_type", slot_crossbow_proficiency_limit),
              #(troop_raise_attribute, ":cur_troop", ca_strength, 1),
              #(display_message, "@+1 strength."),
            #(else_try),
              #(eq, ":slot_proficiency_type", slot_throwing_proficiency_limit),
              #(call_script, "script_troop_raise_skill_limit", ":cur_troop", skl_power_throw, 1),
              #(display_message, "@+1 power throw."),
            #(try_end),
            #(val_add, ":slot_proficiency_limit", proficiency_limit_increase),
            #(troop_set_slot, ":cur_troop", ":slot_proficiency_type", ":slot_proficiency_limit"),
          #(else_try),
            #(ge, ":weapon_proficiency", ":slot_all_proficiency_limit"),
            #(val_add, ":continue", 1),
          #(try_end),
          #(try_begin),
            #(eq, ":continue", 6),
            #(call_script, "script_troop_raise_skill_limit", ":cur_troop", skl_weapon_master, 1),
            
            #(str_clear, s3),
            #(store_div, ":out_string", ":slot_all_proficiency_limit", proficiency_limit_increase),
            #(val_sub, ":out_string", 1),
            #(val_add, ":out_string", "str_level_d"),
            #(str_store_string, s3, ":out_string"),
            #(display_message, "@{s1}'s proficiency in all weapons have reach level {s3}."),
            #(display_message, "@+1 weapon_master"),
            #(val_add, ":slot_all_proficiency_limit", proficiency_limit_increase),
            #(troop_set_slot, ":cur_troop", slot_all_proficiency_limit, ":slot_all_proficiency_limit"),
          #(try_end),
        #(try_end),
      #(try_end),
    ]),

   (3,
    [
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
          (ge, ":troop_party_no", 1),
          (party_is_active, ":troop_party_no"),
          (party_get_attached_to, ":cur_attached_town", ":troop_party_no"),
          (ge, ":cur_attached_town", 1),
          (call_script, "script_get_relation_between_parties", ":cur_attached_town", ":troop_party_no"),
          (store_faction_of_party, ":troop_faction_no", ":troop_party_no"),
          (try_begin),
            (this_or_next|lt, reg0, 0),
            (neg|faction_slot_eq, ":troop_faction_no", slot_faction_state, sfs_active),
            (party_detach, ":troop_party_no"),
            (call_script, "script_party_set_ai_state", ":troop_party_no",  spai_patrolling_around_center, ":cur_attached_town"),
          (try_end),
        (try_end),
     ]),
   
  (7,
    [
      (try_for_parties, ":party_no"),
        (neq, ":party_no", "p_main_party"),
        (neq, ":party_no", "p_temp_party"),
        (assign, ":continue", 0),
        (try_begin),
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
          (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
          (party_is_active, ":party_no"),
          (assign, ":continue", 1),
          (try_begin),
            (party_stack_get_troop_id, ":cur_troop", ":party_no", 0),
            (this_or_next|troop_is_hero, ":cur_troop"),
            (eq, ":cur_troop", "trp_caravan_master"),
            (assign, ":first_stack", 1),
          (else_try),
            (assign, ":first_stack", 0),
          (try_end),
        (else_try),
          (this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_castle),
          (party_slot_eq, ":party_no", slot_party_type, spt_town),
          (neg|party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
          (assign, ":first_stack", 0),
          (assign, ":continue", 1),
        (else_try),
          (party_get_template_id, ":party_template", ":party_no"),
          (this_or_next|eq, ":party_template", "pt_looters"),
          (is_between, ":party_template", bandit_party_template_begin, bandit_party_template_end),
          (assign, ":continue", 1),
          (try_begin),
            (party_stack_get_troop_id, ":cur_troop", ":party_no", 0),
            (troop_is_hero, ":cur_troop"),
            (assign, ":first_stack", 1),
          (else_try),
            (assign, ":first_stack", 0),
          (try_end),
        (try_end),
        (eq, ":continue", 1),
        (call_script, "script_sort_party_by_troop_level", ":party_no", ":first_stack"),
      (try_end),
    ]),
   
   (24,
     [
       (try_for_range, ":cur_village", villages_begin, villages_end),
         (party_get_slot, ":cur_bound_center", ":cur_village", slot_village_bound_center),
         (store_faction_of_party, ":village_faction", ":cur_village"),
         (store_faction_of_party, ":town_faction", ":cur_bound_center"),
         (neq,  ":village_faction", ":town_faction"),
         (call_script, "script_give_center_to_faction", ":cur_village", ":town_faction"),
       (try_end),
     ]),
#CC-C begin hp del
#  (24,
#    [
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        #(try_begin),
          #(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          #(call_script, "script_get_troop_backup_hp_times_factor", ":troop_no"),
          #(assign, ":hp_times_factor", reg0),
          #(call_script, "script_get_troop_max_hp", ":troop_no"),
          #(assign, ":max_hp", reg0),
          #(store_mul, ":max_backup_hp", ":max_hp", ":hp_times_factor"),
          #(val_div, ":max_backup_hp", 100),
          #(troop_get_slot, ":backup_hp", ":troop_no", slot_troop_backup_hp),
          #(store_character_level, ":troop_level", ":troop_no"),
          #(store_div, ":refill_speed", ":troop_level", 10),
          #(val_add, ":backup_hp", ":refill_speed"),
          ## refill hp if needed
          #(store_troop_health, ":troop_hp", ":troop_no", 1),
          #(call_script, "script_get_troop_max_hp", ":troop_no"),
          #(assign, ":max_hp", reg0),
          #(store_sub, ":lost_hp", ":max_hp", ":troop_hp"),
          #(val_min, ":lost_hp", ":backup_hp"),
          #(val_add, ":troop_hp", ":lost_hp"),
          #(troop_set_health, ":troop_no", ":troop_hp", 1),
          #(val_sub, ":backup_hp", ":lost_hp"),
          ## set backup_hp
          #(val_min, ":backup_hp", ":max_backup_hp"),
          #(troop_set_slot, ":troop_no", slot_troop_backup_hp, ":backup_hp"),
        #(else_try),
          #(troop_set_slot, ":troop_no", slot_troop_backup_hp, 0),
        #(try_end),
      #(try_end),
#    ]),
##CC-C end

   (1,
     [
       (party_get_morale, ":cur_morale", "p_main_party"),
       (val_clamp, "$g_morale_threshold", 33, 100),
       (try_begin),
         (lt, ":cur_morale", "$g_morale_threshold"),
         (assign, "$g_twice_consum_food", 1),
       (else_try),
         (assign, "$g_twice_consum_food", 0),
       (try_end),
     ]),
   
  (6,
   [
      (try_for_parties, ":party_no"),
        (assign, ":fitful_faction_1", -1),
        (assign, ":fitful_faction_2", -1),
        (party_get_slot, ":party_type", ":party_no", slot_party_type),
        (assign, ":continue", 0),
        (try_begin),
          (this_or_next|eq, ":party_type", spt_town),
          (eq, ":party_type", spt_castle),
          (party_get_slot, ":town_lord", ":party_no", slot_town_lord),
          (neq, ":town_lord", "trp_player"),
          (gt, ":town_lord", 0),  ## CC-D
          (assign, ":continue", 1),
        (else_try),
          (eq, ":party_type", spt_kingdom_hero_party),
          (party_stack_get_troop_id, ":party_leader", ":party_no", 0),
          (neq, ":party_leader", "trp_player"),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        
        (try_begin),
          (party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
          (troop_get_slot, ":fitful_faction_1", ":party_leader", slot_troop_original_faction),
          (store_troop_faction, ":fitful_faction_2", ":party_leader"),
          (try_begin),
            (eq, ":fitful_faction_2", "fac_player_supporters_faction"),
            (assign, ":fitful_faction_2", -1),
          (try_end),
        (else_try),
          (this_or_next|eq, ":party_type", spt_town),
          (eq, ":party_type", spt_castle),
          (party_get_slot, ":fitful_faction_1", ":party_no", slot_center_original_faction),
          (store_faction_of_party, ":fitful_faction_2", ":party_no"),
          (try_begin),
            (store_relation, ":faction_relation", ":fitful_faction_1", ":fitful_faction_2"),
            (lt, ":faction_relation", 0),
            (assign, ":fitful_faction_1", -1),
          (try_end),
          (try_begin),
            (eq, ":fitful_faction_2", "fac_player_supporters_faction"),
            (try_begin),
              (is_between, "$supported_pretender", pretenders_begin, pretenders_end),
              (troop_get_slot, ":fitful_faction_2", "$supported_pretender", slot_troop_original_faction),
            (else_try),
              (gt, ":town_lord", "trp_player"),
              (troop_get_slot, ":fitful_faction_2", ":town_lord", slot_troop_original_faction),
            (else_try),
              (assign, ":fitful_faction_2", -1),
            (try_end),
          (try_end),
        (try_end),
        
        # combine same troops from prisoners
        (call_script, "script_combine_same_troops_from_prisoners", ":party_no"),
        
        # prisoners to members
        (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party_no"),
        (try_for_range_backwards, ":cur_prisoner_stack", 0, ":num_prisoner_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_prisoner_id", ":party_no", ":cur_prisoner_stack"),
          (gt, ":cur_prisoner_id", -1),
          (neg|troop_is_hero, ":cur_prisoner_id"),
          (store_troop_faction, ":troop_faction", ":cur_prisoner_id"),
          (this_or_next|eq, ":troop_faction", ":fitful_faction_1"),
          (this_or_next|eq, ":troop_faction", ":fitful_faction_2"),
          (this_or_next|eq, ":troop_faction", "fac_commoners"),
          (eq, ":troop_faction", "fac_manhunters"),
          (party_get_num_companion_stacks, ":num_companion_stacks", ":party_no"),
          (lt, ":num_companion_stacks", 32),
          (party_prisoner_stack_get_size, ":prisoner_size", ":party_no", ":cur_prisoner_stack"),
          (party_remove_prisoners,":party_no",":cur_prisoner_id", ":prisoner_size"),
          (party_add_members, ":party_no", ":cur_prisoner_id", ":prisoner_size"),
        (try_end),
        
        # members to prisoners
        (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
        (try_for_range_backwards, ":cur_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":cur_troop", ":party_no", ":cur_stack"),
          (gt, ":cur_troop", -1),
          (store_troop_faction, ":troop_faction", ":cur_troop"),
          ## CC-D begin: slave to slave only
          (this_or_next|eq, ":cur_troop", "trp_ccc_slave_man"),
          (eq, ":cur_troop", "trp_ccc_slave_woman"),
          #(eq, ":troop_faction", "fac_outlaws"),
          ## CC-D end
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party_no"),
          (lt, ":num_prisoner_stacks", 32),
          (party_stack_get_size, ":stack_size", ":party_no", ":cur_stack"),
          (party_remove_members, ":party_no", ":cur_troop", ":stack_size"),
          (party_add_prisoners, ":party_no", ":cur_troop", ":stack_size"),
        (try_end),
      (try_end),
      
      # walled centers sell prisoners
      #(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        #(party_get_slot, ":town_lord", ":center_no", slot_town_lord),
        #(gt, ":town_lord", "trp_player"), #center does not belong to player.
        #(neg|is_between, ":town_lord", companions_begin, companions_end), # not companions
        # processing ransom
        #(party_clear, "p_temp_party"),
        #(party_get_num_prisoner_stacks, ":prisoner_stacks", ":center_no"),
        #(try_for_range_backwards, ":prisoner_stack_no", 0, ":prisoner_stacks"),
          #(party_prisoner_stack_get_troop_id, ":prisoner_troop_no", ":center_no", ":prisoner_stack_no"),
          #(neg|troop_is_hero, ":prisoner_troop_no"),
          #(store_troop_faction, ":prisoner_faction", ":prisoner_troop_no"),
          #(neq, ":prisoner_faction", "fac_outlaws"),
          #(party_prisoner_stack_get_size, ":prisoner_stack_size", ":center_no", ":prisoner_stack_no"),
          #(party_remove_prisoners, ":center_no", ":prisoner_troop_no", ":prisoner_stack_size"),
          #(party_add_members, "p_temp_party", ":prisoner_troop_no", ":prisoner_stack_size"),
        #(try_end),
        #(call_script, "script_calculate_ransom_for_party", "p_temp_party"),
        #(assign, ":total_ransom_cost", reg0),
        #(party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
        #(val_add, ":cur_wealth", ":total_ransom_cost"),
        #(party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
        ## upgrade after processing ransom
        #(store_mul, ":xp_gain", ":total_ransom_cost", 5),
        #(party_upgrade_with_xp, ":center_no", ":xp_gain"),
        #(call_script, "script_upgrade_hero_party", ":center_no", ":xp_gain"),
      #(try_end),
   ]),
   
   
   #NPC party's prisoner management trigger
  (7,#occc 3->7 imported from difor 0.058 
   [
    (try_for_parties, ":party_no"),
      (party_get_template_id, ":party_template", ":party_no"),
      (try_begin),
        (is_between, ":party_template", bandit_party_template_begin, bandit_party_template_end),
        (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party_no"),
        # combine outlaws_troops to members
        (try_for_range_backwards, ":cur_prisoner_stack", 0, ":num_prisoner_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_prisoner_id", ":party_no", ":cur_prisoner_stack"),
          (gt, ":cur_prisoner_id", -1),
          (neg|troop_is_hero, ":cur_prisoner_id"),
          (is_between, ":cur_prisoner_id", outlaws_troops_begin, outlaws_troops_end),
          (party_prisoner_stack_get_size, ":prisoner_size", ":party_no", ":cur_prisoner_stack"),
          (party_remove_prisoners,":party_no",":cur_prisoner_id", ":prisoner_size"),
          (party_add_members, ":party_no", ":cur_prisoner_id", ":prisoner_size"),
        (try_end),
        # kingdom-troop prisoners convert to deserters
        (set_spawn_radius, 1),
        (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
          (party_clear, "p_temp_party"),
          (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party_no"),
          (gt, ":num_prisoner_stacks", 0),
          (try_for_range_backwards, ":cur_prisoner_stack", 0, ":num_prisoner_stacks"),
            (party_prisoner_stack_get_troop_id, ":cur_prisoner_id", ":party_no", ":cur_prisoner_stack"),
            (gt, ":cur_prisoner_id", -1),
            (neg|troop_is_hero, ":cur_prisoner_id"),
            (store_troop_faction, ":cur_prisoner_faction", ":cur_prisoner_id"),
            (eq, ":cur_prisoner_faction", ":cur_faction"),
            (party_prisoner_stack_get_size, ":prisoner_size", ":party_no", ":cur_prisoner_stack"),
            (party_remove_prisoners, ":party_no", ":cur_prisoner_id", ":prisoner_size"),
            (party_add_members, "p_temp_party", ":cur_prisoner_id", ":prisoner_size"),
          (try_end),
          (party_get_num_companions, ":num_companions", "p_temp_party"),
          (ge, ":num_companions", 1), # is not empty
          (spawn_around_party, ":party_no", "pt_deserters"),
          (assign, ":new_party", reg0),
          (call_script, "script_party_copy", ":new_party", "p_temp_party"),
        (try_end),
        (call_script, "script_ccd_kill_party_prisoners", ":party_no", 20),  ## CC-D
      (else_try),
        (eq, ":party_template", "pt_kingdom_caravan_party"),
        (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party_no"),
        (try_for_range_backwards, ":cur_prisoner_stack", 0, ":num_prisoner_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_prisoner_id", ":party_no", ":cur_prisoner_stack"),
          (gt, ":cur_prisoner_id", -1),
          (neg|troop_is_hero, ":cur_prisoner_id"),
          (store_troop_faction, ":troop_faction", ":cur_prisoner_id"),
          (store_faction_of_party, ":merchant_faction", ":party_no"),
          (this_or_next|eq, ":troop_faction", ":merchant_faction"),
          (this_or_next|eq, ":cur_prisoner_id", "trp_caravan_master"),
          (is_between, ":cur_prisoner_id", "trp_farmer", "trp_mercenaries_end"),
          (party_prisoner_stack_get_size, ":prisoner_size", ":party_no", ":cur_prisoner_stack"),
          (party_remove_prisoners,":party_no",":cur_prisoner_id", ":prisoner_size"),
          (party_add_members, ":party_no", ":cur_prisoner_id", ":prisoner_size"),
        (try_end),
        (call_script, "script_ccd_kill_party_prisoners", ":party_no", 10),  ## CC-D
      ## OCCC start
      #undeads convert prisoners into zombies
      (else_try),
        (this_or_next|eq, ":party_template", "pt_occc_dark_avengers"),
        (eq, ":party_template", "pt_occc_undead_legion_boss"),
        
        (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party_no"),
        # combine outlaws_troops to members
        (try_for_range_backwards, ":cur_prisoner_stack", 0, ":num_prisoner_stacks"),
          (party_prisoner_stack_get_troop_id, ":cur_prisoner_id", ":party_no", ":cur_prisoner_stack"),
          (gt, ":cur_prisoner_id", -1),
          (neg|troop_is_hero, ":cur_prisoner_id"),
          (store_random_in_range, ":rand_no", 0, 7),
          (le,":rand_no",1),
          (store_character_level, ":victim_level", ":cur_prisoner_id"),
          (try_begin),
            (ge, ":victim_level", 25),
            (assign,":zombie_tier", "trp_occc_fallen_hero"),
          (else_try),
            (ge, ":victim_level", 12),
            (assign,":zombie_tier", "trp_occc_widerganger"),
          (else_try),
            (assign,":zombie_tier", "trp_ccd_zombie"),
          (try_end),
          (party_prisoner_stack_get_size, ":prisoner_size", ":party_no", ":cur_prisoner_stack"),
          (party_remove_prisoners,":party_no",":cur_prisoner_id", ":prisoner_size"),
          (party_add_members, ":party_no", ":zombie_tier", ":prisoner_size"),
        (try_end),
        
        (call_script, "script_ccd_kill_party_prisoners", ":party_no", 50),  ## CC-D
      ## OCCC end

      ## CC-D begin
      (else_try),
        (this_or_next|eq, ":party_template", "pt_manhunters"),
        (eq, ":party_template", "pt_patrol_party"),
        (party_get_slot, ":score", ":party_no", slot_party_ccd_sell_score),
        (call_script, "script_ccd_kill_party_prisoners", ":party_no", 10),
        (gt, reg0, 0),
        (val_add, ":score", reg1),
        (store_div, ":reinf", ":score", 100),
        (try_begin),
          (gt, ":reinf", 0),
          
          (assign, ":reinf_troop", -1),
          (assign, ":most", 0),
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
            (neg|troop_is_hero, ":stack_troop"),
            (party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
            (ge, ":stack_size", ":most", 0),
            (assign, ":reinf_troop", ":stack_troop"),
            (assign, ":most", ":stack_size"),
          (try_end),
          (try_begin),
            (gt, ":reinf_troop", 0),
            (party_add_members, ":party_no", ":reinf_troop", ":reinf"),
            (val_mul, ":reinf", 100),
            (val_sub, ":score", ":reinf"),
          (try_end),
        (try_end),
        (party_set_slot, ":party_no", slot_party_ccd_sell_score, ":score"),
      (else_try),
        (is_between, ":party_template", "pt_looters", "pt_forest_bandits"),  # except pt_manhunters
        (call_script, "script_ccd_kill_party_prisoners", ":party_no", 5),
      ## CC-D end
      (else_try),
        (eq, ":party_template", "pt_deserters"),
        (assign, "$g_move_heroes", 0), 
        (call_script, "script_party_add_party_prisoners", ":party_no", ":party_no"),
        (call_script, "script_party_remove_all_prisoners", ":party_no"),
        
        ## convert neutral faction troop to prisoners
        (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
        (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
          (neg|troop_is_hero, ":stack_troop"),
          (store_troop_faction, ":stack_troop_faction", ":stack_troop"),
          (this_or_next|eq, ":stack_troop_faction", "fac_commoners"),
          (eq, ":stack_troop_faction", "fac_manhunters"),
          (party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
          (party_remove_members, ":party_no", ":stack_troop", ":stack_size"),
          (party_add_prisoners,":party_no", ":stack_troop", ":stack_size"),
        (try_end),
        
        ## convert bandit troops to bandit parties
        (set_spawn_radius, 1),
        (try_for_range, ":bandit_type", outlaws_troops_begin, outlaws_troops_end),
          (party_clear, "p_temp_party"),
          (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
          (try_for_range_backwards, ":cur_stack", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":cur_troop", ":party_no", ":cur_stack"),
            (eq, ":cur_troop", ":bandit_type"),
            (party_stack_get_size, ":stack_size", ":party_no", ":cur_stack"),
            (party_remove_members, ":party_no", ":cur_troop", ":stack_size"),
            (party_add_members, "p_temp_party", ":cur_troop", ":stack_size"),
          (try_end),
          (party_get_num_companions, ":num_companions", "p_temp_party"),
          (ge, ":num_companions", 1), # is not empty
          (call_script, "script_get_party_template_of_bandit", ":bandit_type"),
          (assign, ":dest_pt", reg0),
          (gt,":dest_pt",0),  ## CC-D fix
          (spawn_around_party, ":party_no", ":dest_pt"),
          (assign, ":new_party", reg0),
          (call_script, "script_party_copy", ":new_party", "p_temp_party"),
        (try_end),
        (call_script, "script_ccd_kill_party_prisoners", ":party_no", 20),  ## CC-D
        
        # is empty?
        (try_begin),
          (party_get_num_companions, ":party_size", ":party_no"),
          (eq, ":party_size", 0),
          (party_clear, ":party_no"),
          (remove_party, ":party_no"),
        (try_end),
      (try_end),
    (try_end),
    (call_script, "script_combine_parties_of_same_template"),
   ]),
   
  ## CC player's walled_center recruit troops
  (24,
    [
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center belongs to player.
        (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege
(party_slot_ge, ":center_no", slot_town_recruit_gold, reinforcement_cost_player), ## CC???        
        (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
        (assign, ":reinforcement_cost", 450),
        (try_begin), 
          (eq, ":reduce_campaign_ai", 0), #hard
          (assign, ":reinforcement_cost", 600),
        (else_try), 
          (eq, ":reduce_campaign_ai", 1), #moderate
          (assign, ":reinforcement_cost", 450),
        (else_try), 
          (eq, ":reduce_campaign_ai", 2), #easy
          (assign, ":reinforcement_cost", 300),
        (try_end),
        
        (call_script, "script_get_town_faction_for_recruiting", ":center_no"),
        (assign, ":party_faction", reg0),
        (faction_get_slot, ":party_template_a", ":party_faction", slot_faction_reinforcements_a),
        (faction_get_slot, ":party_template_b", ":party_faction", slot_faction_reinforcements_b),
        (faction_get_slot, ":party_template_c", ":party_faction", slot_faction_reinforcements_c),
        
        (party_get_slot, ":party_type",":center_no", slot_party_type),
        (assign, ":party_template", 0),
        (assign, ":num_hiring_rounds", 1),
        (store_random_in_range, ":rand", 0, 100),
        (try_begin), 
          (party_slot_eq, ":center_no", slot_center_has_barrack, 1),
          (val_sub, ":rand", 15),
          (party_slot_eq, ":center_no", slot_center_has_greater_barrack, 1),
          (val_sub, ":rand", 15),
        (try_end),
        (try_begin),
          (eq, ":party_type", spt_castle),  #CASTLE
          (try_begin),
            (lt, ":rand", 0),
            (assign, ":party_template", ":party_template_c"),
          (else_try),
            (lt, ":rand", 65),
            (assign, ":party_template", ":party_template_b"),
          (else_try),
            (assign, ":party_template", ":party_template_a"),
          (try_end),
        (else_try),
          (eq, ":party_type", spt_town),  #TOWN
          (try_begin),
            (lt, ":rand", 20),
            (assign, ":party_template", ":party_template_c"),
          (else_try),
            (lt, ":rand", 70),
            (assign, ":party_template", ":party_template_b"),
          (else_try),
            (assign, ":party_template", ":party_template_a"),
          (try_end),
          (store_random_in_range, ":random", 0, 2),
          (val_add, ":num_hiring_rounds", ":random"),
        (try_end),

        (try_for_range, ":unused", 0, ":num_hiring_rounds"), 
          (party_slot_ge, ":center_no", slot_town_recruit_gold, ":reinforcement_cost"),
          (party_get_slot, ":recruit_gold", ":center_no", slot_town_recruit_gold),
          (val_sub, ":recruit_gold", ":reinforcement_cost"),
          (party_set_slot, ":center_no", slot_town_recruit_gold, ":recruit_gold"),
          (gt, ":party_template", 0),
          (party_add_template, ":center_no", ":party_template"),
        (try_end),
      (try_end),
    ]),
  
  (24, 
    [
      (eq, "$g_add_bandit_heroes", 1),
      (call_script, "script_centers_init_bandit_leader_quest"),
      (try_for_range, ":pt_no", bandit_party_template_begin, bandit_party_template_end),
        (party_template_set_slot, ":pt_no", slot_party_template_has_hero, 0),
        (try_for_parties, ":party_no"),
          (party_get_template_id, ":party_template", ":party_no"),
          (eq, ":party_template", ":pt_no"),
          (party_stack_get_troop_id, ":leader", ":party_no", 0),
          (troop_is_hero, ":leader"),
          (party_template_set_slot, ":pt_no", slot_party_template_has_hero, 1),
        (try_end),
        (try_begin),
          (party_template_slot_eq, ":pt_no", slot_party_template_has_hero, 1),
          (party_template_set_slot, ":pt_no", slot_party_template_hero_next_spawn_time, 0),
        (else_try),
          (party_template_slot_eq, ":pt_no", slot_party_template_has_hero, 0),
          (party_template_slot_eq, ":pt_no", slot_party_template_hero_next_spawn_time, 0),
          (store_current_hours, ":next_spawn_time"),
          (store_random_in_range, ":added_time", 24*28, 24*42),
          (val_add, ":next_spawn_time", ":added_time"),
          (party_template_set_slot, ":pt_no", slot_party_template_hero_next_spawn_time, ":next_spawn_time"),
        (try_end),
        (party_template_get_slot, ":next_spawn_time", ":pt_no", slot_party_template_hero_next_spawn_time),
        (neq, ":next_spawn_time", 0),
        (store_current_hours, ":cur_time"),
        (gt, ":cur_time", ":next_spawn_time"),
        (party_template_slot_eq, ":pt_no", slot_party_template_has_hero, 0),
        
        (party_template_get_slot, ":spawn_point", ":pt_no", slot_party_template_spawn_point),
        (party_template_get_slot, ":hero_id", ":pt_no", slot_party_template_hero_id),
        (party_template_get_slot, ":hero_name_begin", ":pt_no", slot_party_template_hero_name_begin),
        
        (neq,":hero_id","trp_player"), #CC-C fix
        
        ## compare level 
        (store_character_level, ":player_level", "trp_player"),
        (store_character_level, ":hero_level", ":hero_id"),
        (try_begin),
          (this_or_next|eq, ":pt_no", "pt_steppe_bandits"),
          (eq, ":pt_no", "pt_desert_bandits"),
          (val_mul, ":hero_level", 3),
          (val_div, ":hero_level", 2),
        (try_end),
        (val_div, ":hero_level", 2),
        (ge, ":player_level", ":hero_level"),
        
        (set_spawn_radius, 25),
        (spawn_around_party, ":spawn_point", ":pt_no"),
        (assign, ":new_party", reg0),
        (party_add_template, ":new_party", ":pt_no"),
        (party_add_template, ":new_party", ":pt_no"),
        # new name for hero
        (assign, ":end_cond", 1),
        (try_for_range, ":unused", 0, ":end_cond"),
          (store_random_in_range, ":new_name", 0, 10),
          (val_add, ":new_name", ":hero_name_begin"),
          (party_template_get_slot, ":pre_name", ":pt_no", slot_party_template_hero_pre_name),
          (party_template_get_slot, ":pre_pre_name", ":pt_no", slot_party_template_hero_pre_pre_name),
          (neq, ":new_name", ":pre_name"),
          (neq, ":new_name", ":pre_pre_name"),
          (troop_set_name, ":hero_id", ":new_name"),
          (party_template_set_slot, ":pt_no", slot_party_template_hero_pre_name, ":new_name"),
          (party_template_set_slot, ":pt_no", slot_party_template_hero_pre_pre_name, ":pre_name"),
          (assign, ":end_cond", 0),
        (else_try),
          (val_add, ":end_cond", 1),
        (try_end),
        
        (party_add_leader, ":new_party", ":hero_id"),
        (troop_set_health, ":hero_id", 100), ## refill hp
        (str_store_troop_name, s5, ":hero_id"),
        (party_set_name, ":new_party", "str_s5_s_party"),
        (store_sub, ":cur_banner", ":hero_id", bandit_heroes_begin),
        (val_add, ":cur_banner", "icon_map_flag_bandit_f"),
        (party_set_banner_icon, ":new_party", ":cur_banner"),
        (party_set_flags, ":new_party", pf_label_small, 1),
        (party_set_flags, ":new_party", pf_always_visible, 1),
        (party_template_set_slot, ":pt_no", slot_party_template_has_hero, 1),
        (party_template_set_slot, ":pt_no", slot_party_template_hero_party_id, ":new_party"),
        (party_template_set_slot, ":pt_no", slot_party_template_hero_next_spawn_time, 0),
        (party_template_set_slot, ":pt_no", slot_party_template_hero_spawn_time, ":cur_time"),  ## CC-D
        
        ## NMCml begin: cut announce and disp message
        (str_store_string, s1, ":new_name"),
        (try_begin),
          (eq, ":pt_no", "pt_forest_bandits"),
          (str_store_string, s2, "@Forest Bandits"),
        (else_try),
          (eq, ":pt_no", "pt_taiga_bandits"),
          (str_store_string, s2, "@Tundra Bandits"),
        (else_try),
          (eq, ":pt_no", "pt_steppe_bandits"),
          (str_store_string, s2, "@Steppe Bandits"),
        (else_try),
          (eq, ":pt_no", "pt_sea_raiders"),
          (str_store_string, s2, "@Sea Raiders"),
        (else_try),
          (eq, ":pt_no", "pt_mountain_bandits"),
          (str_store_string, s2, "@Mountain Bandits"),
        (else_try),
          (eq, ":pt_no", "pt_desert_bandits"),
          (str_store_string, s2, "@Desert Bandits"),
        (try_end),
        (display_message, "@{s1} of {s2} has staged a comeback.", 0xff3333),
        
        (try_begin),
          (eq, "$g_nmcml_cut_diplomacy_announce_screen", 0),
          (assign, "$temp", ":pt_no"),
          (jump_to_menu, "mnu_bandit_heroe_spawned"),
        (try_end),
        ## NMCml end
      (try_end),
    ]),
  
  (3, 
    [
      (try_for_range, ":pt_no", bandit_party_template_begin, bandit_party_template_end),
        (party_template_set_slot, ":pt_no", slot_party_template_has_hero, 0),
        (try_for_parties, ":party_no"),
          (party_get_template_id, ":party_template", ":party_no"),
          (eq, ":party_template", ":pt_no"),
          (party_stack_get_troop_id, ":leader", ":party_no", 0),
          (troop_is_hero, ":leader"),
          (party_template_set_slot, ":pt_no", slot_party_template_has_hero, 1),
        (try_end),
        (try_begin),
          (party_template_slot_eq, ":pt_no", slot_party_template_has_hero, 1),
          (party_template_get_slot, ":hero_party", ":pt_no", slot_party_template_hero_party_id),
          (party_is_active, ":hero_party"),
          (assign, ":num_followed", 0),
          (try_for_parties, ":party_no"),
            (party_get_template_id, ":party_template", ":party_no"),
            (eq, ":party_template", ":pt_no"),
            (party_stack_get_troop_id, ":leader", ":party_no", 0),
            (neg|troop_is_hero, ":leader"),
            (get_party_ai_current_object, ":cur_obj", ":party_no"),
            (get_party_ai_current_behavior, ":cur_bhvr", ":party_no"),
            (eq, ":cur_obj", ":hero_party"),
            (eq, ":cur_bhvr", ai_bhvr_escort_party),
            (val_add, ":num_followed", 1),
          (try_end),
          ## CC-D begin: followers increase as time pass
          (party_template_get_slot, ":spawn_time", ":pt_no", slot_party_template_hero_spawn_time),
          (store_current_hours, ":cur_time"),
          (val_min, ":spawn_time", ":cur_time"),
          (val_add, ":spawn_time", 1),
          (val_div, ":spawn_time", 24*7),
          (assign, ":cur_follower", 3),
          (try_begin),
            (lt, ":spawn_time", 1),
            (assign, ":cur_follower", 3),
          (else_try),
            (lt, ":spawn_time", 2),
            (assign, ":cur_follower", 5),
          (else_try),
            (assign, ":cur_follower", 6),
          (try_end),
          ## CC-D end
          (try_for_parties, ":party_no"),
            (party_get_template_id, ":party_template", ":party_no"),
            (eq, ":party_template", ":pt_no"),
            (party_stack_get_troop_id, ":leader", ":party_no", 0),
            (neg|troop_is_hero, ":leader"),
            (try_begin), # skip if :num_followed = 4
              (eq, ":num_followed", ":cur_follower"),  ## CC-D 4->":cur_follower"
            (else_try), # increase num_followed
              (lt, ":num_followed", ":cur_follower"),  ## CC-D 4->":cur_follower"
              (get_party_ai_current_object, ":cur_obj", ":party_no"),
              (get_party_ai_current_behavior, ":cur_bhvr", ":party_no"),
              (neq, ":cur_obj", ":hero_party"),
              (neq, ":cur_bhvr", ai_bhvr_escort_party),
              (party_set_ai_behavior, ":party_no", ai_bhvr_escort_party),
              (party_set_ai_object, ":party_no", ":hero_party"),
              (val_add, ":num_followed", 1),
            (else_try), # decrease num_followed
              (gt, ":num_followed", ":cur_follower"),  ## CC-D 4->":cur_follower"
              (get_party_ai_current_object, ":cur_obj", ":party_no"),
              (get_party_ai_current_behavior, ":cur_bhvr", ":party_no"),
              (eq, ":cur_obj", ":hero_party"),
              (eq, ":cur_bhvr", ai_bhvr_escort_party),
              (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
              (party_set_ai_patrol_radius, ":party_no", 30),
              (party_template_get_slot, ":bandit_template_spawnpoint", ":party_template", slot_party_template_lair_spawnpoint),
              (party_get_position, pos1, ":bandit_template_spawnpoint"),
              (party_set_ai_target_position, ":party_no", pos1),
              (party_set_ai_object, ":party_no", -1),
              (party_set_flags, ":party_no", pf_default_behavior, 0),
              (val_sub, ":num_followed", 1),
            (try_end),
          (try_end),
        (else_try), # bandit hero is defeated
          (try_for_parties, ":party_no"),
            (party_get_template_id, ":party_template", ":party_no"),
            (eq, ":party_template", ":pt_no"),
            (party_stack_get_troop_id, ":leader", ":party_no", 0),
            (neg|troop_is_hero, ":leader"),
            (get_party_ai_object, ":cur_obj", ":party_no"),
            (neg|party_is_active, ":cur_obj"), # reset ai bhvr
            (party_get_position, pos1, ":party_no"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
            (party_set_ai_patrol_radius, ":party_no", 10),
            (party_set_ai_target_position, ":party_no", pos1),
            (party_set_ai_object, ":party_no", -1),
            (party_set_flags, ":party_no", pf_default_behavior, 0),
          (try_end),
        (try_end),
      (try_end),
    ]),

  (24,
    [
      (party_get_num_prisoners, ":num_prisoners", "p_main_party"),
      (call_script, "script_game_get_party_prisoner_limit"),
      (assign, ":limit", reg0),
      (gt, ":num_prisoners", ":limit"),
      (store_mul, ":escape_prob", ":num_prisoners", 10),
      (val_max, ":limit", 1),
      (val_div, ":escape_prob", ":limit"),
      (val_min, ":escape_prob", 50),
      
      (assign, ":kinds_of_escape_troop", 0),
      (assign, ":num_of_escaped", 0),
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_main_party"),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop","p_main_party",":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_prisoner_stack_get_size, ":stack_size","p_main_party",":stack_no"),
        (assign, ":num_removed", 0),
        (try_for_range, ":unused", 0, ":stack_size"),
          (store_random_in_range, ":rand_no", 0, 100),
          (lt, ":rand_no", ":escape_prob"),
          (val_add, ":num_removed", 1),
        (try_end),
        (gt, ":num_removed", 0),
        (party_remove_prisoners, "p_main_party", ":stack_troop", ":num_removed"),
        (val_add, ":kinds_of_escape_troop", 1),
        (val_add, ":num_of_escaped", ":num_removed"),
        (try_begin),
          (eq, ":kinds_of_escape_troop", 1),
          (str_store_troop_name_by_count, s1, ":stack_troop", ":num_removed"),
          (assign, reg1, ":num_removed"),
          (str_store_string, s0, "@{reg1} {s1}"),
        (else_try),
          (eq, ":kinds_of_escape_troop", 2),
          (str_store_troop_name_by_count, s1, ":stack_troop", ":num_removed"),
          (assign, reg1, ":num_removed"),
          (str_store_string, s0, "@{reg1} {s1} and {s0}"),
        (else_try),
          (ge, ":kinds_of_escape_troop", 3),
          (str_store_troop_name_by_count, s1, ":stack_troop", ":num_removed"),
          (assign, reg1, ":num_removed"),
          (str_store_string, s0, "@{reg1} {s1}, {s0}"),
        (try_end),
      (try_end),
      (try_begin),
        (ge, ":kinds_of_escape_troop", 1),
        (try_begin),
          (eq, ":num_of_escaped", 1),
          (str_store_string, s0, "@{s0} has escaped."),
        (else_try),
          (str_store_string, s0, "@{s0} hava escaped."),
        (try_end),
        (str_store_string, s0, "@Number of prisoners exceeds prisoner management limit. {s0}"),
        (tutorial_box, s0, "str_weekly_report"),
      (try_end),
    ]
  ),
  
  ## restoration
  (24,
    [
      (gt, "$g_ccd_faction_restoration", -1),  ## CC-D add
      (try_for_range, ":cur_faction", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_get_slot, ":inactive_days", ":cur_faction", slot_faction_inactive_days),
        (try_begin),
          (neg|faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
          (val_add, ":inactive_days", 1),
        (else_try),
          (assign, ":inactive_days", 0),
        (try_end),
        (faction_set_slot, ":cur_faction", slot_faction_inactive_days, ":inactive_days"),
        (gt, ":inactive_days", "$g_ccd_faction_restoration"),  ## CC-D 20->$g_ccd_faction_restoration
        (troop_get_slot, ":pretender_original_faction", "$supported_pretender",  slot_troop_original_faction),
        (neq, ":pretender_original_faction", ":cur_faction"),
        
        (assign, ":fitful_faction", -1),
        (assign, ":fitful_lords", 0),
        (try_for_range, ":faction_2", npc_kingdoms_begin, npc_kingdoms_end),
          (neq, ":faction_2", ":cur_faction"),
          (neq, ":faction_2", ":pretender_original_faction"),
          (faction_slot_eq, ":faction_2", slot_faction_state, sfs_active),
          (assign, ":fitful_lords_this_faction", 0),
          (try_for_range, ":cur_troop", lords_begin, lords_end),
            (troop_get_slot, ":troop_original_faction", ":cur_troop", slot_troop_original_faction),
            (eq, ":troop_original_faction", ":cur_faction"),
            (store_troop_faction, ":troop_cur_faction", ":cur_troop"),
            (this_or_next|eq, ":troop_cur_faction", ":faction_2"),
            (eq, ":troop_cur_faction", "fac_outlaws"),
            (val_add, ":fitful_lords_this_faction", 1),
          (try_end),
          # centers 
          (assign, ":fitful_centers", 0),
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
            (ge, ":center_lord", 1),
            (store_troop_faction, ":troop_cur_faction", ":center_lord"),
            (eq, ":troop_cur_faction", ":faction_2"),
            (troop_get_slot, ":troop_original_faction", ":center_lord", slot_troop_original_faction),
            (eq, ":troop_original_faction", ":cur_faction"),
            (val_add, ":fitful_centers", 1),
            (try_begin),
              (party_slot_eq, ":center_no", slot_party_type, spt_town),
              (val_add, ":fitful_centers", 1),
            (try_end),
          (try_end),
          (try_begin),
            (ge, ":fitful_centers", 3),
            (gt, ":fitful_lords_this_faction", ":fitful_lords"),
            (assign, ":fitful_lords", ":fitful_lords_this_faction"),
            (assign, ":fitful_faction", ":faction_2"),
          (try_end),
        (try_end),
        (try_begin),
          (lt, ":fitful_lords", 5),
          (assign, ":fitful_faction", -1),
        (try_end),
        
        (gt, ":fitful_faction", -1),
        (faction_get_slot, ":original_king", ":cur_faction", slot_faction_leader),
        ## CC-D begin
        (store_sub, ":kp_offset", pretenders_begin, kings_begin),
        (try_begin),
		## OCCC start Napoleon Hundred Days
          (eq,":original_king","trp_kingdom_2_lord"),#Napoleon returns!
          (neg|troop_slot_eq, "trp_kingdom_2_lord", slot_troop_occupation, dplmc_slto_dead),
		## OCCC end
        (else_try),
          (is_between, ":original_king", pretenders_begin, pretenders_end),
          (store_sub, ":preking", ":original_king", ":kp_offset"),
          (neg|troop_slot_eq, ":preking", slot_troop_occupation, dplmc_slto_dead),
          (assign, ":original_king", ":preking"),
        (else_try),
          (is_between, ":original_king", kings_begin, kings_end),
          (troop_slot_eq, ":original_king", slot_troop_occupation, dplmc_slto_dead),
          (val_add, ":original_king", ":kp_offset"),
        (try_end),
        (neg|troop_slot_eq, ":original_king", slot_troop_occupation, dplmc_slto_dead),
        ## CC-D end
        (call_script, "script_change_troop_faction", ":original_king", ":cur_faction"),
        (troop_set_slot, ":original_king", slot_troop_occupation, slto_kingdom_hero),
        (faction_set_slot, ":cur_faction", slot_faction_leader, ":original_king"),  ## CC-D add
        (call_script, "script_add_notification_menu", "mnu_notification_kingdom_restoration", ":cur_faction", ":fitful_faction"),
      (try_end),
      
      ## CC-D begin: extra restorations:reinvade
      (try_begin),
        #count exiled lord
        #(assign, ":lord_swadia", 0),
        #(assign, ":lord_vaegir", 0),
        (assign, ":lord_khergit", 0),
        (assign, ":lord_nord", 0),
        #(assign, ":lord_rhodok", 0),
        (assign, ":lord_sarran", 0),
        (assign, ":lord_dk", 0),
        (try_for_range, ":cur_troop", lords_begin, lords_end),
          (store_troop_faction, ":troop_cur_faction", ":cur_troop"),
          (eq, ":troop_cur_faction", "fac_outlaws"),
          (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, dplmc_slto_exile),
          (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_inactive),
          (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
          
          (troop_get_slot, ":troop_original_faction", ":cur_troop", slot_troop_original_faction),
          (try_begin),
            (eq, ":troop_original_faction", "fac_kingdom_1"),
            #(val_add, ":lord_swadia", 1),
            (val_add, ":lord_dk", 1),
          (else_try),
            (eq, ":troop_original_faction", "fac_kingdom_2"),
            #(val_add, ":lord_vaegir", 1),
            (val_add, ":lord_dk", 1),
          (else_try),
            (eq, ":troop_original_faction", "fac_kingdom_3"),
            (val_add, ":lord_khergit", 1),
          (else_try),
            (eq, ":troop_original_faction", "fac_kingdom_4"),
            (val_add, ":lord_nord", 1),
          (else_try),
            (eq, ":troop_original_faction", "fac_kingdom_5"),
            #(val_add, ":lord_rhodok", 1),
            (val_add, ":lord_dk", 1),
          (else_try),
            (eq, ":troop_original_faction", "fac_kingdom_6"),
            (val_add, ":lord_sarran", 1),
          (else_try),
            (eq, ":troop_original_faction", "fac_kingdom_7"),
            (val_add, ":lord_dk", 1),
          (try_end),
        (try_end),
        
        #faction check
        (assign, ":fitful_faction", -1),
        (try_begin),
          (ge, ":lord_dk", 3),
          (assign, ":fitful_faction", "fac_kingdom_7"),
        (else_try),
          (ge, ":lord_khergit", 3),
          (assign, ":fitful_faction", "fac_kingdom_3"),
        (else_try),
          (ge, ":lord_nord", 3),
          (assign, ":fitful_faction", "fac_kingdom_4"),
        (else_try),
          (ge, ":lord_sarran", 3),
          (assign, ":fitful_faction", "fac_kingdom_6"),
        (try_end),
        (try_begin),
          (neq, ":fitful_faction", -1),
          (faction_get_slot, ":inactive_days", ":fitful_faction", slot_faction_inactive_days),
          (gt, ":inactive_days", "$g_ccd_faction_restoration"),
          #(neq, ":pretender_original_faction", ":cur_faction"),
        (else_try),
          (assign, ":fitful_faction", -1),
        (try_end),
        
        (gt, ":fitful_faction", -1),
        
        #center check
        (assign, ":fitful_center", -1),
        (assign, ":lowest_str", 3600), # about Lv30 * 200+
        (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
          (assign, ":continue", 0),
          (try_begin),
            (eq, ":fitful_faction", fac_kingdom_7),  #dk
            (this_or_next|eq, ":center_no", "p_town_1"),
            (this_or_next|eq, ":center_no", "p_town_2"),
            (this_or_next|eq, ":center_no", "p_town_5"),
            (this_or_next|eq, ":center_no", "p_town_6"),
            (this_or_next|eq, ":center_no", "p_town_12"),
            (this_or_next|eq, ":center_no", "p_town_13"),
            (this_or_next|eq, ":center_no", "p_town_15"),
            (this_or_next|eq, ":center_no", "p_town_19"),
            (this_or_next|eq, ":center_no", "p_castle_3"),
            (this_or_next|eq, ":center_no", "p_castle_9"),
            (this_or_next|eq, ":center_no", "p_castle_10"),
            (this_or_next|eq, ":center_no", "p_castle_11"),
            (this_or_next|eq, ":center_no", "p_castle_12"),
            (this_or_next|eq, ":center_no", "p_castle_16"),
            (this_or_next|eq, ":center_no", "p_castle_21"),
            (this_or_next|eq, ":center_no", "p_castle_23"),
            (this_or_next|eq, ":center_no", "p_castle_34"),
            (this_or_next|eq, ":center_no", "p_castle_46"),
            (this_or_next|eq, ":center_no", "p_castle_49"),
            (this_or_next|eq, ":center_no", "p_castle_50"),
            (this_or_next|eq, ":center_no", "p_castle_57"),
            (this_or_next|eq, ":center_no", "p_castle_58"),
            (this_or_next|eq, ":center_no", "p_castle_59"),
            (eq, ":center_no", "p_castle_60"),
            (assign, ":continue", 1),
          (else_try),
            (eq, ":fitful_faction", fac_kingdom_3),  #khergit
            (this_or_next|eq, ":center_no", "p_town_10"),
            (this_or_next|eq, ":center_no", "p_town_17"),
            (this_or_next|eq, ":center_no", "p_town_18"),
            (this_or_next|eq, ":center_no", "p_castle_2"),
            (this_or_next|eq, ":center_no", "p_castle_17"),
            (this_or_next|eq, ":center_no", "p_castle_30"),
            (this_or_next|eq, ":center_no", "p_castle_38"),
            (eq, ":center_no", "p_castle_56"),
            (assign, ":continue", 1),
          (else_try),
            (eq, ":fitful_faction", fac_kingdom_4),  #nord
            (this_or_next|eq, ":center_no", "p_town_1"),
            (this_or_next|eq, ":center_no", "p_town_2"),
            (this_or_next|eq, ":center_no", "p_town_6"),
            (this_or_next|eq, ":center_no", "p_town_12"),
            (this_or_next|eq, ":center_no", "p_town_13"),
            (this_or_next|eq, ":center_no", "p_castle_3"),
            (this_or_next|eq, ":center_no", "p_castle_10"),
            (this_or_next|eq, ":center_no", "p_castle_11"),
            (this_or_next|eq, ":center_no", "p_castle_12"),
            (this_or_next|eq, ":center_no", "p_castle_23"),
            (this_or_next|eq, ":center_no", "p_castle_34"),
            (this_or_next|eq, ":center_no", "p_castle_50"),
            (this_or_next|eq, ":center_no", "p_castle_57"),
            (eq, ":center_no", "p_castle_58"),
            (assign, ":continue", 1),
          (else_try),
            (eq, ":fitful_faction", fac_kingdom_6),  #sarran
            (this_or_next|eq, ":center_no", "p_town_19"),
            (this_or_next|eq, ":center_no", "p_town_20"),
            (this_or_next|eq, ":center_no", "p_town_21"),
            (this_or_next|eq, ":center_no", "p_town_22"),
            (this_or_next|eq, ":center_no", "p_castle_42"),
            (this_or_next|eq, ":center_no", "p_castle_43"),
            (this_or_next|eq, ":center_no", "p_castle_44"),
            (this_or_next|eq, ":center_no", "p_castle_45"),
            (this_or_next|eq, ":center_no", "p_castle_46"),
            (this_or_next|eq, ":center_no", "p_castle_48"),
            (this_or_next|eq, ":center_no", "p_castle_62"),
            (this_or_next|eq, ":center_no", "p_castle_63"),
            (eq, ":center_no", "p_castle_64"),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          
          (party_collect_attachments_to_party, ":center_no", "p_collective_enemy"),
          (call_script, "script_party_calculate_strength", "p_collective_enemy", 0),
          (assign, ":cur_str", reg0),
          (lt, ":cur_str", ":lowest_str"),
          (assign, ":fitful_center", ":center_no"),
          (assign, ":lowest_str", ":cur_str"),
        (try_end),
        
        (gt, ":fitful_center", -1),
        
        #king prepare
        (faction_get_slot, ":original_king", ":fitful_faction", slot_faction_leader),
        (store_sub, ":kp_offset", pretenders_begin, kings_begin),
        (try_begin),
          (is_between, ":original_king", pretenders_begin, pretenders_end),
          (store_sub, ":preking", ":original_king", ":kp_offset"),
          (neg|troop_slot_eq, ":preking", slot_troop_occupation, dplmc_slto_dead),
          (assign, ":original_king", ":preking"),
        (else_try),
          (is_between, ":original_king", kings_begin, kings_end),
          (troop_slot_eq, ":original_king", slot_troop_occupation, dplmc_slto_dead),
          (val_add, ":original_king", ":kp_offset"),
        (try_end),
        (neg|troop_slot_eq, ":original_king", slot_troop_occupation, dplmc_slto_dead),
        
        (store_troop_faction, ":troop_cur_faction", ":original_king"),
        (try_begin),
          (troop_slot_eq, ":original_king", slot_troop_occupation, slto_kingdom_hero),
          (is_between, ":troop_cur_faction", kingdoms_begin, kingdoms_end),
          (troop_get_slot, ":cur_wealth", ":original_king", slot_troop_wealth),
          (val_add, ":cur_wealth", 5000),
          (troop_set_slot, ":original_king", slot_troop_wealth, ":cur_wealth"),
        (else_try),
          (troop_get_slot, ":cur_wealth", ":original_king", slot_troop_wealth),
          (val_add, ":cur_wealth", 10000),
          (troop_set_slot, ":original_king", slot_troop_wealth, ":cur_wealth"),
          (troop_set_slot, ":original_king", slot_troop_spawned_before, 0),
        (try_end),
        (call_script, "script_change_troop_faction", ":original_king", ":fitful_faction"),
        (troop_set_slot, ":original_king", slot_troop_occupation, slto_kingdom_hero),
        (faction_set_slot, ":fitful_faction", slot_faction_leader, ":original_king"),
        
        #center prepare
        (party_get_num_attached_parties, ":num_attached_parties",":fitful_center"),
        (try_for_range_backwards, ":iap", 0, ":num_attached_parties"),
          (party_get_attached_party_with_rank, ":attached_party", ":fitful_center", ":iap"),
          (gt, ":attached_party", -1),
          (party_is_active, ":attached_party"),
          (party_detach, ":attached_party"),
          (neq, ":attached_party", "p_main_party"),
          (party_get_slot, ":attached_party_type", ":attached_party", slot_party_type),
          (eq, ":attached_party_type", spt_kingdom_hero_party),
          (store_faction_of_party, ":attached_party_faction", ":attached_party"),
          (call_script, "script_get_closest_walled_center_of_faction", ":attached_party", ":attached_party_faction"),
          (try_begin),
            (gt, reg0, 0),
            (call_script, "script_party_set_ai_state", ":attached_party", spai_holding_center, reg0),
          (else_try),
            (call_script, "script_party_set_ai_state", ":attached_party", spai_patrolling_around_center, ":fitful_center"),
          (try_end),
        (try_end),
        
        (store_faction_of_party, ":center_faction", ":fitful_center"),
        (call_script, "script_give_center_to_faction_aux", ":fitful_center", ":fitful_faction"),
        #(call_script, "script_give_center_to_lord", ":fitful_center", ":original_king", 1),
        
        #lords prepare
        (try_for_range, ":cur_troop", lords_begin, lords_end),
          (assign, ":continue", 0),
          (store_troop_faction, ":troop_cur_faction", ":cur_troop"),
          (try_begin),
            (eq, ":troop_cur_faction", "fac_outlaws"),
            (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, dplmc_slto_exile),
            (this_or_next|troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_inactive),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
            (assign, ":continue", 1),
          (else_try),
            (eq, ":troop_cur_faction", "$players_kingdom"),
            (faction_slot_eq, ":troop_cur_faction", slot_faction_leader, "trp_player"),
            (troop_slot_eq, ":cur_troop", slot_troop_occupation, slto_inactive),
            (assign, ":continue", 1),
          (try_end),
          (eq, ":continue", 1),
          (troop_get_slot, ":troop_original_faction", ":cur_troop", slot_troop_original_faction),
          (eq, ":troop_original_faction", ":fitful_faction"),
          
          (call_script, "script_change_troop_faction", ":cur_troop", ":fitful_faction"),
          (troop_set_slot, ":cur_troop", slot_troop_occupation, slto_kingdom_hero),
          
          # add wealth
          (troop_get_slot, ":cur_wealth", ":cur_troop", slot_troop_wealth),
          (val_add, ":cur_wealth", 5000),
          (troop_set_slot, ":cur_troop", slot_troop_wealth, ":cur_wealth"),
          
          # add relation
          (call_script, "script_troop_get_relation_with_troop", ":cur_troop", ":original_king"),
          (store_add, ":new_relation", reg0, 30),
          (val_clamp, ":new_relation", 10, 101),
          (store_add, ":troop1_slot_for_troop2", ":original_king", slot_troop_relations_begin),
          (troop_set_slot, ":cur_troop", ":troop1_slot_for_troop2", ":new_relation"),
          (store_add, ":troop2_slot_for_troop1", ":cur_troop", slot_troop_relations_begin),
          (troop_set_slot, ":original_king", ":troop2_slot_for_troop1", ":new_relation"),
          
          (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
          (try_begin),
            (gt, ":cur_party", 0),
            (party_is_active, ":cur_party"),
          (else_try),
            (troop_set_slot, ":cur_troop", slot_troop_spawned_before, 0),
            (call_script, "script_create_kingdom_hero_party", ":cur_troop", ":fitful_center"),
            (troop_get_slot, ":cur_party", ":cur_troop", slot_troop_leaded_party),
            (gt, ":cur_party", 0),
            (party_is_active, ":cur_party"),
            (party_attach_to_party, ":cur_party", ":fitful_center"),
          (try_end),
        (try_end),
        
        (call_script, "script_add_notification_menu", "mnu_ccd_notification_reinvade", ":fitful_faction", ":fitful_center"),
        (call_script, "script_diplomacy_start_war_between_kingdoms", ":fitful_faction", ":center_faction", 1),
        (call_script, "script_update_all_notes"),
      (try_end),
      ## CC-D end
    ]),
  
  (1,
    [
      (try_for_range, ":cur_quest", "qst_deal_with_forest_bandit", "qst_quests_end"),
        (check_quest_active, ":cur_quest"),
        (neg|check_quest_succeeded, ":cur_quest"),

        (quest_get_slot, ":dest_pt_no", ":cur_quest", slot_quest_target_party_template),
        (assign, ":has_hero", 0),
        (try_for_parties, ":party_no"),
          (party_get_template_id, ":party_template", ":party_no"),
          (eq, ":party_template", ":dest_pt_no"),
          (party_stack_get_troop_id, ":leader", ":party_no", 0),
          (troop_is_hero, ":leader"),
          (assign, ":has_hero", 1),
        (try_end),
        (eq, ":has_hero", 0),
        (party_template_set_slot, ":dest_pt_no", slot_party_template_has_hero, 0),
        (party_template_set_slot, ":dest_pt_no", slot_party_template_hero_party_id, -1),
        (party_template_get_slot, ":bandit_hero_name", ":dest_pt_no", slot_party_template_hero_pre_name),
        (str_store_string, s1, ":bandit_hero_name"),
        (display_message, "@{s1} has been eliminated by another party.", 0xff3333),
        (call_script, "script_cancel_quest", ":cur_quest"),
      (try_end),
    ]),
  
  # Moving prisoners to the center when a lord in a center
  (3,
   [
       (try_for_range, ":troop_no", heroes_begin, heroes_end),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
         (ge, ":troop_party_no", 1),
         (party_is_active, ":troop_party_no"),

         (party_get_attached_to, ":cur_attached_town", ":troop_party_no"),
         (ge, ":cur_attached_town", 1),
         (party_get_cur_town, ":destination", ":troop_party_no"),
         (is_between, ":destination", centers_begin, centers_end),
       ## CC sell prisoners if possible
         (call_script, "script_lord_sell_prisoners", ":troop_no", ":destination"),
       ## CC
         (this_or_next|party_slot_eq, ":destination", slot_party_type, spt_town),
         (party_slot_eq, ":destination", slot_party_type, spt_castle),
         (store_faction_of_party, ":troop_faction_no", ":troop_party_no"),
         (store_faction_of_party, ":destination_faction_no", ":destination"),
         (eq, ":troop_faction_no", ":destination_faction_no"),
         (party_get_num_prisoner_stacks, ":num_stacks", ":troop_party_no"),
         (gt, ":num_stacks", 0),
         (assign, "$g_move_heroes", 1),
         (call_script, "script_party_prisoners_add_party_prisoners", ":destination", ":troop_party_no"),
         (assign, "$g_move_heroes", 1),
         (call_script, "script_party_remove_all_prisoners", ":troop_party_no"),
       (try_end),
    ]),
  
  # (3,
    # [
      #(call_script, "script_init_commensalism_troops"),
      #(try_for_parties, ":party_no"),
        #(party_get_template_id, ":template_id", ":party_no"),
        #(this_or_next|is_between, ":template_id", "pt_looters", "pt_kidnapped_girl"),
        #(this_or_next|is_between, ":party_no", centers_begin, centers_end),
        #(this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_hero_party),
        #(this_or_next|party_slot_eq, ":party_no", slot_party_type, spt_kingdom_caravan),
        #(eq, ":party_no", "p_main_party"),
        
        #(party_is_active, ":party_no"),
        #(party_get_battle_opponent, ":opponent", ":party_no"),
        #(lt, ":opponent", 0),
        #(assign, ":continue", 0),
        #(try_begin),
          #(party_get_attached_to, ":attached_to", ":party_no"),
          #(lt, ":attached_to", 0),
          #(assign, ":continue", 1),
        #(else_try),
          #(party_get_battle_opponent, ":attached_to_opponent", ":attached_to"),
          #(lt, ":attached_to_opponent", 0),
          #(assign, ":continue", 1),
        #(try_end),
        #(eq, ":continue", 1),
        
        #(call_script, "script_auto_adjust_commensalism_troops" , ":party_no"),
      #(try_end),
    # ]),
  
  # (24,
    # [
      #(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        #(party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        #(call_script, "script_set_top_troop_to_second_class_troop", ":center_no"),
      #(try_end),
      #(call_script, "script_set_top_troop_to_second_class_troop", "p_main_party"),
    # ]),
  
  # exchange troops between lord's party and town/castle
  (3, 
    [
      (try_for_range, ":troop_no", heroes_begin, heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (ge, ":party_no", 1),
        (party_is_active, ":party_no"),
        (party_get_attached_to, ":cur_attached_party", ":party_no"),
        (is_between, ":cur_attached_party", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":cur_attached_party", slot_town_lord, ":troop_no"),
        (store_faction_of_party, ":attached_party_faction", ":cur_attached_party"),
        (faction_get_color, ":faction_color", ":attached_party_faction"),
        
        (call_script, "script_party_get_ideal_size", ":party_no"),
        (assign, ":party_limit", reg0),
        (call_script, "script_party_get_ideal_size", ":cur_attached_party"),
        (assign, ":center_limit", reg0),
        
        # move town/castle troops to lord's party
        (try_begin),
          (party_get_num_companions, ":party_size_begin", ":party_no"),
          (troop_get_slot, ":lord_faction", ":troop_no", slot_troop_original_faction),
          (party_get_slot, ":attached_party_original_faction", ":cur_attached_party", slot_center_original_faction),
          (try_for_range, ":unused", 0, 4),
            (party_get_num_companion_stacks, ":num_stacks", ":cur_attached_party"),
            (try_for_range_backwards, ":cur_stack", 0, ":num_stacks"),
              (try_begin),
                (party_get_num_companions, ":party_size", ":party_no"),
                (party_get_num_companions, ":center_size", ":cur_attached_party"),
                (store_mul, ":center_limit_new", ":center_limit", 11),
                (val_div, ":center_limit_new", 12),
                (this_or_next|lt, ":center_size", ":center_limit_new"),
                (gt, ":party_size", ":party_limit"),
                (assign, ":num_stacks", 0),
              (try_end),
              (gt, ":num_stacks", 0),
              (party_stack_get_troop_id, ":cur_troop", ":cur_attached_party", ":cur_stack"),
              (neg|troop_is_hero, ":cur_troop"),
              (store_troop_faction, ":troop_faction", ":cur_troop"),
              (this_or_next|eq, ":troop_faction", ":lord_faction"),
              (this_or_next|eq, ":troop_faction", ":attached_party_faction"),
              (eq, ":troop_faction", ":attached_party_original_faction"),
              (party_stack_get_size, ":stack_size", ":cur_attached_party", ":cur_stack"),
              (try_begin),
                (eq, ":unused", 0), # the 1st round
                (try_begin),
                  (le, ":stack_size", 5),
                (else_try),
                  (assign, ":stack_size", 0),
                (try_end),
              (else_try),
                (try_begin),
                  (le, ":stack_size", 5),
                (else_try),
                  (store_random_in_range, ":rand_no", 20, 40),
                  (val_mul, ":stack_size", ":rand_no"),
                  (val_div, ":stack_size", 100),
                (try_end),
              (try_end),
              (gt, ":stack_size", 0),
              (party_remove_members, ":cur_attached_party", ":cur_troop", ":stack_size"),
              (party_add_members, ":party_no", ":cur_troop", ":stack_size"),
            (try_end),
          (try_end),
          (party_get_num_companions, ":party_size_end", ":party_no"),
          (store_sub, ":num_moved", ":party_size_end", ":party_size_begin"),
          (ge, ":num_moved", 30), # lt 30 display no message 
          (assign, reg0, ":num_moved"),
          (str_store_troop_name, s3, ":troop_no"),
          (str_store_party_name, s4, ":cur_attached_party"),
          #(display_message, "@{s3} has taken {reg0} troops from {s4}.", ":faction_color"), # NMC - changed to stop spamming messages
        (try_end),
        
        # move lord's troops to town/castle
        (try_begin),
          (party_get_num_companions, ":party_size_begin", ":cur_attached_party"),
          (troop_get_slot, ":lord_faction", ":troop_no", slot_troop_original_faction),
          (party_get_slot, ":attached_party_original_faction", ":cur_attached_party", slot_center_original_faction),
          (try_for_range, ":unused", 0, 4),
            (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
            (try_for_range_backwards, ":cur_stack", 0, ":num_stacks"),
              (try_begin),
                (party_get_num_companions, ":party_size", ":party_no"),
                (party_get_num_companions, ":center_size", ":cur_attached_party"),
                (store_mul, ":center_limit_new", ":center_limit", 3),
                (val_div, ":center_limit_new", 4),
                (store_div, ":party_limit_new", ":party_limit", 2),
                (this_or_next|gt, ":center_size", ":center_limit_new"),
                (lt, ":party_size", ":party_limit_new"),
                (assign, ":num_stacks", 0),
              (try_end),
              (gt, ":num_stacks", 0),
              (party_stack_get_troop_id, ":cur_troop", ":party_no", ":cur_stack"),
              (neg|troop_is_hero, ":cur_troop"),
              (store_troop_faction, ":troop_faction", ":cur_troop"),
              (this_or_next|eq, ":troop_faction", ":lord_faction"),
              (this_or_next|eq, ":troop_faction", ":attached_party_faction"),
              (eq, ":troop_faction", ":attached_party_original_faction"),
              (party_stack_get_size, ":stack_size", ":party_no", ":cur_stack"),
              (try_begin),
                (eq, ":unused", 0), # the 1st round
                (try_begin),
                  (le, ":stack_size", 5),
                (else_try),
                  (assign, ":stack_size", 0),
                (try_end),
              (else_try),
                (try_begin),
                  (le, ":stack_size", 5),
                (else_try),
                  (store_random_in_range, ":rand_no", 20, 40),
                  (val_mul, ":stack_size", ":rand_no"),
                  (val_div, ":stack_size", 100),
                (try_end),
              (try_end),
			  #occc start
			  (try_begin),
				(is_between,":cur_troop","trp_ore_spartanwarrior","trp_occc_amazon_huntress"),#spartan warriors
				(val_min, ":stack_size", 6),
			  (try_end),
			  #occc end
              (gt, ":stack_size", 0),
              (party_remove_members, ":party_no", ":cur_troop", ":stack_size"),
              (party_add_members, ":cur_attached_party", ":cur_troop", ":stack_size"),
            (try_end),
          (try_end),
          (party_get_num_companions, ":party_size_end", ":cur_attached_party"),
          (store_sub, ":num_moved", ":party_size_end", ":party_size_begin"),
          (ge, ":num_moved", 50), #occc lt 30->50 display no message 
          (assign, reg0, ":num_moved"),
          (str_store_troop_name, s3, ":troop_no"),
          (str_store_party_name, s4, ":cur_attached_party"),
          (display_message, "@{s3} has given {reg0} troops to {s4}.", ":faction_color"),
        (try_end),
      (try_end),
    ]),

# exchange cavalry troops in town/castle with non-cavalry troops in lord's party
  (3, 
    [
      (try_for_range, ":troop_no", heroes_begin, heroes_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (ge, ":party_no", 1),
        (party_is_active, ":party_no"),
        (party_get_attached_to, ":cur_attached_party", ":party_no"),
        (is_between, ":cur_attached_party", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":cur_attached_party", slot_town_lord, ":troop_no"),
        
        (party_get_num_companion_stacks, ":center_stacks", ":cur_attached_party"),
        (try_for_range_backwards, ":center_cur_stack", 0, ":center_stacks"),
          (party_stack_get_troop_id, ":center_cur_troop", ":cur_attached_party", ":center_cur_stack"),
          (gt, ":center_cur_troop", -1),
          (neg|troop_is_hero, ":center_cur_troop"),
          (troop_is_guarantee_horse, ":center_cur_troop"), # cavalry
          (party_get_num_companion_stacks, ":party_stacks", ":party_no"),
          (assign, ":end_cond", ":party_stacks"),
          (try_for_range_backwards, ":party_cur_stack", 0, ":end_cond"),
            (party_stack_get_troop_id, ":party_cur_troop", ":party_no", ":party_cur_stack"),
            (gt, ":party_cur_troop", -1),
            (neg|troop_is_hero, ":party_cur_troop"),
            (neg|troop_is_guarantee_horse, ":party_cur_troop"), # non-cavalry
            (party_count_companions_of_type, ":party_stack_size", ":party_no", ":party_cur_troop"),
            (party_count_companions_of_type, ":center_stack_size", ":cur_attached_party", ":center_cur_troop"),
            (try_begin),
              (ge, ":party_stack_size", ":center_stack_size"),
              (assign, ":end_cond", 0),#break
              (assign, ":dest_size", ":center_stack_size"),
            (else_try),
              (assign, ":dest_size", ":party_stack_size"),
            (try_end),
            # ":cavalry_ratio" less than 60%
            (call_script, "script_get_cavalry_ratio_of_party", ":party_no"),
            (assign, ":cavalry_ratio", reg0),
            (assign, ":cavalry_ratio_limit", 60), # by default
            (troop_get_slot, ":troop_original_faction",  ":troop_no", slot_troop_original_faction),
            (try_begin),
              (this_or_next|eq, ":troop_original_faction", "fac_kingdom_4"),
              (eq, ":troop_original_faction", "fac_kingdom_5"),
              (assign, ":cavalry_ratio_limit", 15),
            (else_try),
              (eq, ":troop_original_faction", "fac_kingdom_3"),
              (assign, ":cavalry_ratio_limit", 100),
            (try_end),
            (le, ":cavalry_ratio", ":cavalry_ratio_limit"),
            # start to exchange
            (party_remove_members, ":party_no", ":party_cur_troop", ":dest_size"),
            (party_add_members, ":cur_attached_party", ":party_cur_troop", ":dest_size"),
            (party_remove_members, ":cur_attached_party", ":center_cur_troop", ":dest_size"),
            (party_add_members, ":party_no", ":center_cur_troop", ":dest_size"),
          (try_end),
        (try_end),
        
        ## exchange high-class troops in town/castle with low-class troops in lord's party
        (party_get_num_companion_stacks, ":center_stacks", ":cur_attached_party"),
        (try_for_range_backwards, ":center_cur_stack", 0, ":center_stacks"),
          (party_stack_get_troop_id, ":center_cur_troop", ":cur_attached_party", ":center_cur_stack"),
          (gt, ":center_cur_troop", -1),
          (neg|troop_is_hero, ":center_cur_troop"),
          (party_get_num_companion_stacks, ":party_stacks", ":party_no"),
          (try_for_range_backwards, ":party_cur_stack", 0, ":party_stacks"),
            (party_stack_get_troop_id, ":party_cur_troop", ":party_no", ":party_cur_stack"),
            (gt, ":party_cur_troop", -1),
            (neg|troop_is_hero, ":party_cur_troop"),
            (troop_get_upgrade_troop, ":upgrade_troop_1", ":party_cur_troop", 0),
            (troop_get_upgrade_troop, ":upgrade_troop_2", ":party_cur_troop", 1),
            (this_or_next|eq, ":upgrade_troop_1", ":center_cur_troop"),
            (eq, ":upgrade_troop_2", ":center_cur_troop"),
            (assign, ":continue", 1),
            (try_begin),
              (troop_is_guarantee_horse, ":center_cur_troop"),
              (neg|troop_is_guarantee_horse, ":party_cur_troop"),
              (assign, ":continue", 0),
            (try_end),
            (eq, ":continue", 1),
            # le 1/2 high-class troops in town/castle, ge 1/2 high-class troops in lord's party 
            (party_count_companions_of_type, ":center_higher_troop_size", ":cur_attached_party", ":center_cur_troop"),
            (party_count_companions_of_type, ":party_higher_troop_size", ":party_no", ":center_cur_troop"),
            (store_add, ":num_moved", ":center_higher_troop_size", ":party_higher_troop_size"),
            (val_div, ":num_moved", 2),
            (store_sub, ":num_moved", ":center_higher_troop_size", ":num_moved"),
            (party_count_companions_of_type, ":party_lower_troop_size", ":party_no", ":party_cur_troop"),
            (val_min, ":num_moved", ":party_lower_troop_size"),
            (gt, ":num_moved", 0),
            # start to exchange
            (party_remove_members, ":party_no", ":party_cur_troop", ":num_moved"),
            (party_add_members, ":cur_attached_party", ":party_cur_troop", ":num_moved"),
            (party_remove_members, ":cur_attached_party", ":center_cur_troop", ":num_moved"),
            (party_add_members, ":party_no", ":center_cur_troop", ":num_moved"),
          (try_end),
        (try_end),
      (try_end),
    ]),
  
  # (3, 
    # [
      #(try_for_parties, ":party_no"),
        #(party_is_active, ":party_no"),
        #(store_faction_of_party, ":party_faction", ":party_no"),
        #(this_or_next|eq, ":party_faction", "fac_outlaws"),
        #(eq, ":party_faction", "fac_deserters"),
        #(party_get_battle_opponent, ":opponent", ":party_no"),
        #(try_begin),
          #(ge, ":opponent", 0), # in battle
          #(try_for_parties, ":party_no_2"),
            #(neq, ":party_no_2", ":party_no"),
            #(store_faction_of_party, ":party_faction_2", ":party_no_2"),
            #(eq, ":party_faction_2", ":party_faction"),
            #(party_get_battle_opponent, ":opponent_2", ":party_no_2"),
            #(lt, ":opponent_2", 0),
            #(party_get_attached_to, ":attached_to",":party_no_2"),
            #(lt, ":attached_to", 0),
            #(store_distance_to_party_from_party, ":dist", ":party_no", ":party_no_2"),
            #(le, ":dist", 8),
            #(party_set_ai_behavior, ":party_no_2", ai_bhvr_attack_party),
            #(party_set_ai_object, ":party_no_2", ":opponent"),
            #(party_set_flags, ":party_no_2", pf_default_behavior, 1),
          #(try_end),
        #(else_try), # reset ai bhvr after battle
          #(get_party_ai_current_behavior, ":cur_bhvr", ":party_no"),
          #(neq, ":cur_bhvr", ai_bhvr_escort_party),
          #(get_party_ai_object, ":cur_obj", ":party_no"),
          #(neg|party_is_active, ":cur_obj"), # reset ai bhvr
          #(party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
          #(party_set_ai_patrol_radius, ":party_no", 30),
          #(party_get_template_id, ":party_template", ":party_no"),
          #(party_template_get_slot, ":bandit_template_spawnpoint", ":party_template", slot_party_template_lair_spawnpoint),
          #(party_get_position, pos1, ":bandit_template_spawnpoint"),
          #(party_set_ai_target_position, ":party_no", pos1),
          #(party_set_ai_object, ":party_no", -1),
          #(party_set_flags, ":party_no", pf_default_behavior, 0),
        #(try_end),
      #(try_end),
    # ]),
    
#occc
## CC-D begin: del imported from Difor 0.58
  # lord recruits troops from deserter's party
  # (2,
   # [
   # (try_for_range, ":troop_no", heroes_begin, heroes_end),
     # (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
     # (troop_get_slot, ":troop_party_no", ":troop_no", slot_troop_leaded_party),
     # (ge, ":troop_party_no", 1),
     # (party_is_active, ":troop_party_no"),
     # (store_faction_of_party, ":troop_faction_no", ":troop_party_no"),
     # (troop_get_slot, ":troop_original_faction", ":troop_no", slot_troop_original_faction),
     
     # (try_for_parties, ":party_no"),
       # (party_get_template_id, ":template_id", ":party_no"),
       # (eq, ":template_id", "pt_deserters"),
       # (party_get_battle_opponent, ":opponent", ":party_no"),
       # (lt, ":opponent", 0),
       # (party_get_attached_to, ":attached_to",":party_no"),
       # (lt, ":attached_to", 0),
       # (store_distance_to_party_from_party, ":dist", ":party_no", ":troop_party_no"),
       # (le, ":dist", 5),
       # (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
       # (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
         # (party_stack_get_troop_id, ":stack_troop", ":party_no", ":stack_no"),
         # (neg|troop_is_hero, ":stack_troop"),
         # (store_troop_faction, ":stack_troop_faction", ":stack_troop"),
         # (this_or_next|eq, ":stack_troop_faction", ":troop_faction_no"),
         # (eq, ":stack_troop_faction", ":troop_original_faction"),
         # (party_stack_get_size, ":stack_size", ":party_no", ":stack_no"),
         # (call_script, "script_game_get_join_cost", ":stack_troop"),
         # (assign, ":join_cost", reg0),
         # (val_mul, ":join_cost", ":stack_size"),
         # (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
         # (ge, ":cur_wealth", ":join_cost"),
         # (call_script, "script_party_get_ideal_size", ":troop_party_no"),
         # (assign, ":ideal_size", reg0),
         # (party_get_num_companions, ":party_size", ":troop_party_no"),
         # (lt, ":party_size", ":ideal_size"),
         # (val_sub, ":cur_wealth", ":join_cost"),
         # (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
         # (party_remove_members, ":party_no", ":stack_troop", ":stack_size"),
         # (party_add_members, ":troop_party_no", ":stack_troop", ":stack_size"),
       # (try_end),
       # (try_begin),
         # (party_get_num_companions, ":num_companions", ":party_no"),
         # (eq, ":num_companions", 0), # is empty
         # (remove_party, ":party_no"),
       # (try_end),
     # (try_end),
   # (try_end),
    # ]),
## CC-D end
    
#Custom Troops Begin
# Note: make sure there is a comma in the entry behind this one
  (0,
    [
      (map_free),
      (troop_get_inventory_slot, ":item", "trp_custom_troops_end", 10),
      (eq,":item","itm_velvet"),
      (call_script, "script_reload_custom_troops"),
	  #occc begin
	  (call_script, "script_occc_reload_troop_switching"),#
	  #occc end
      (troop_clear_inventory, "trp_custom_troops_end"),
      
      #(call_script,"script_ccc_game_load_init"), #CC-C begin  ## CC-D del: not use
    ]
  ),
#Custom Troops End

## CC-C begin: Custom Troop Name maintain
  (0, 
    [
      (try_for_range, ":cur_troop", customizable_troops_begin, customizable_troops_end),
        (neg|troop_is_hero, ":cur_troop"),
        (store_add, ":cur_troop_cur_name", ":cur_troop", 1),
        (neq,":cur_troop","trp_player"),
        (str_store_troop_name, s1, ":cur_troop_cur_name"),
        (str_store_troop_name_plural, s2, ":cur_troop_cur_name"),
        (troop_set_name, ":cur_troop", s1),
        (troop_set_plural_name, ":cur_troop", s2),
      (try_end),
    ]
  ),
## CC-C end


  ##diplomacy begin
  #Troop AI Spouse: Spouse thinking
  (3,
   [
	(troop_get_slot, ":player_spouse", "trp_player", slot_troop_spouse),
	(ge, ":player_spouse", active_npcs_begin),#<-- skip the rest of the check when there is no spouse
    (try_for_parties, ":spouse_party"),
      (party_slot_eq, ":spouse_party", slot_party_type, dplmc_spt_spouse),

      (party_get_slot, ":spouse_target", ":spouse_party", slot_party_orders_object),
      (party_get_slot, ":home_center", ":spouse_party", slot_party_home_center),
      (store_distance_to_party_from_party, ":distance", ":spouse_party", ":spouse_target"),

      #Moving spouse to home village
      (try_begin),
        (le, ":distance", 1),
        (try_begin),
          (this_or_next|eq, ":spouse_target", "$g_player_court"),
		      (eq, ":spouse_target", ":home_center"),
          (remove_party, ":spouse_party"),
          (troop_set_slot, ":player_spouse", slot_troop_cur_center, ":spouse_target"),
        (else_try),
          (try_begin),
            (is_between, ":spouse_target", villages_begin, villages_end),
            (party_get_slot,":cur_merchant",":spouse_target", slot_town_elder),
          (else_try),
            (party_get_slot,":cur_merchant",":spouse_target", slot_town_merchant),
          (try_end),
          (troop_get_slot, ":amount", ":player_spouse", dplmc_slot_troop_mission_diplomacy),
          (troop_remove_items, ":cur_merchant", "itm_bread", ":amount"),
          (party_set_ai_behavior, ":spouse_party", ai_bhvr_travel_to_party),
          (try_begin),
            (gt, "$g_player_court", 0),
            (party_set_slot, ":spouse_party", slot_party_ai_object, "$g_player_court"),
            (party_set_ai_object, ":spouse_party", "$g_player_court"),
          (else_try),
            (party_set_slot, ":spouse_party", slot_party_ai_object, ":home_center"),
            (party_set_ai_object, ":spouse_party", ":home_center"),
          (try_end),

          (troop_add_items, "trp_household_possessions", "itm_bread", ":amount"),
        (try_end),
      (try_end),
    (try_end),
    ]),

#Recruiter kit begin
## This trigger keeps the recruiters moving by assigning them targets.
 (0.5,
   [
   (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, dplmc_spt_recruiter),

      (party_get_slot, ":needed", ":party_no", dplmc_slot_party_recruiter_needed_recruits),

      (party_get_num_companion_stacks, ":stacks", ":party_no"),
      (assign, ":destruction", 1),
      (assign, ":quit", 0),

      (try_for_range, ":stack_no", 0, ":stacks"),
         (party_stack_get_troop_id, ":troop_id", ":party_no", ":stack_no"),
         (eq, ":troop_id", "trp_dplmc_recruiter"),
         (assign, ":destruction",0),
      (try_end),
      (try_begin),
         (party_get_battle_opponent, ":opponent", ":party_no"),
         (lt, ":opponent", 0),
         (eq, ":destruction", 1),
         (party_get_slot, ":party_origin", ":party_no", dplmc_slot_party_recruiter_origin),
         (str_store_party_name_link, s13, ":party_origin"),
         (assign, reg10, ":needed"),
         (display_log_message, "@Your recruiter who was commissioned to recruit {reg10} recruits to {s13} has been defeated!", 0xFF0000),
         (remove_party, ":party_no"),
         (assign, ":quit", 1),
      (try_end),

      #waihti
      (try_begin),
        (eq, ":quit", 0),
        (party_get_slot, ":party_origin", ":party_no", dplmc_slot_party_recruiter_origin),
        (store_faction_of_party, ":origin_faction", ":party_origin"),
        (neq, ":origin_faction", "$players_kingdom"),
        (str_store_party_name_link, s13, ":party_origin"),
        (assign, reg10, ":needed"),
        (display_log_message, "@{s13} has been taken by the enemy and your recruiter who was commissioned to recruit {reg10} recruits vanished  without a trace!", 0xFF0000),
        (remove_party, ":party_no"),
        (assign, ":quit", 1),
      (try_end),
      #waihti

      (eq, ":quit", 0),

      (party_get_num_companions, ":amount", ":party_no"),
      (val_sub, ":amount", 1),   #the recruiter himself doesn't count.

   #daedalus begin
      (party_get_slot, ":recruit_faction", ":party_no", dplmc_slot_party_recruiter_needed_recruits_faction),
   #daedalus end
      (lt, ":amount", ":needed"),  #If the recruiter has less troops than player ordered, new village will be set as target.
      (try_begin),
         #(get_party_ai_current_behavior, ":ai_bhvr", ":party_no"),
         #(eq, ":ai_bhvr", ai_bhvr_hold),
         (get_party_ai_object, ":previous_target", ":party_no"),
         (get_party_ai_behavior, ":previous_behavior", ":party_no"),
         (try_begin),
            (neq, ":previous_behavior", ai_bhvr_hold),
            (neq, ":previous_target", -1),
            (party_set_slot, ":previous_target", dplmc_slot_village_reserved_by_recruiter, 0),
         (try_end),
         (assign, ":min_distance", 999999),
         (assign, ":closest_village", -1),
         (try_for_range, ":village", villages_begin, villages_end),
            (store_distance_to_party_from_party, ":distance", ":party_no", ":village"),
            (lt, ":distance", ":min_distance"),
            (try_begin),
               (store_faction_of_party, ":village_current_faction", ":village"),
               (assign, ":faction_relation", 100),
               (try_begin),
                  (neq, ":village_current_faction", "$players_kingdom"),    # faction relation will be checked only if the village doesn't belong to the player's current faction
                  (store_relation, ":faction_relation", "$players_kingdom", ":village_current_faction"),
               (try_end),
               (ge, ":faction_relation", 0),
               (party_get_slot, ":village_relation", ":village", slot_center_player_relation),
               (ge, ":village_relation", 0),
               (party_get_slot, ":volunteers_in_village", ":village", slot_center_volunteer_troop_amount),
               (gt, ":volunteers_in_village", 0),
            #daedalus begin
               #CC-C begin
			   #occc 
			   (try_begin),
					(this_or_next|eq,":recruit_faction","fac_player_supporters_faction"),
					(is_between,":recruit_faction","fac_kingdom_9","fac_kingdom_11"),
					(store_faction_of_party,":village_faction",":village"),
               (else_try),
					(party_get_slot, ":village_faction", ":village", slot_center_original_faction),
			   (try_end),
               #(store_faction_of_party,":village_faction",":village"),
               #CC-C end
               (assign,":stop",1),
               (try_begin),
                  (eq,":recruit_faction",-1),
                  (assign,":stop",0),
               (else_try),
                  (eq, ":village_faction", ":recruit_faction"),
                  (assign,":stop",0),
               (try_end),
               (neq,":stop",1),
            #daedalus end
               (neg|party_slot_eq, ":village", slot_village_state, svs_looted),
               (neg|party_slot_eq, ":village", slot_village_state, svs_being_raided),
               (neg|party_slot_ge, ":village", slot_village_infested_by_bandits, 1),
               (neg|party_slot_eq, ":village", dplmc_slot_village_reserved_by_recruiter, 1),
               (assign, ":min_distance", ":distance"),
               (assign, ":closest_village", ":village"),
            (try_end),
         (try_end),
         (gt, ":closest_village", -1),
         (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
         (party_set_ai_object, ":party_no", ":closest_village"),
         (party_set_slot, ":party_no", slot_party_ai_object, ":closest_village"),
         (party_set_slot, ":closest_village", dplmc_slot_village_reserved_by_recruiter, 1),
      (try_end),
      (party_get_slot, ":target", ":party_no", slot_party_ai_object),
      (gt, ":target", -1),
      (store_distance_to_party_from_party, ":distance_from_target", ":party_no", ":target"),
      (try_begin),
         (store_faction_of_party, ":target_current_faction", ":target"),
         (assign, ":faction_relation", 100),
         (try_begin),
            (neq, ":target_current_faction", "$players_kingdom"),    # faction relation will be checked only if the target doesn't belong to the player's current faction
            (store_relation, ":faction_relation", "$players_kingdom", ":target_current_faction"),
         (try_end),
         (ge, ":faction_relation", 0),
         (party_get_slot, ":target_relation", ":target", slot_center_player_relation),
         (ge, ":target_relation", 0),
      #daedalus begin
            #CC-C begin
			   (try_begin),
					(this_or_next|eq,":recruit_faction","fac_player_supporters_faction"),
					(is_between,":recruit_faction","fac_kingdom_9","fac_kingdom_11"),
					(store_faction_of_party,":target_faction",":target"),
               (else_try),
					(party_get_slot, ":target_faction", ":target", slot_center_original_faction),#occc fix
			   (try_end),
            #(store_faction_of_party,":target_faction",":target"),
            #CC-C end
            (assign,":stop",1),
            (try_begin),
            (eq,":recruit_faction",-1),
            (assign,":stop",0),
        (else_try),
            (eq, ":target_faction", ":recruit_faction"),
            (assign,":stop",0),
            (try_end),
            (neq,":stop",1),
      #daedalus end
         (neg|party_slot_eq, ":target", slot_village_state, svs_looted),
            (neg|party_slot_eq, ":target", slot_village_state, svs_being_raided),
            (neg|party_slot_ge, ":target", slot_village_infested_by_bandits, 1),
         (le, ":distance_from_target", 0),
         (party_get_slot, ":volunteers_in_target", ":target", slot_center_volunteer_troop_amount),
         (party_get_slot, ":target_volunteer_type", ":target", slot_center_volunteer_troop_type),
         ## CC-D begin: add custom troop
         (try_begin),
           (eq, ":recruit_faction", "fac_player_supporters_faction"),
           (assign, ":target_volunteer_type", "trp_custom_recruit"),
         (try_end),
         ## CC-D end
         (assign, ":still_needed", ":needed"),
         (val_sub, ":still_needed", ":amount"),
         (try_begin),
            (gt, ":volunteers_in_target", ":still_needed"),
            (assign, ":santas_little_helper", ":volunteers_in_target"),
            (val_sub, ":santas_little_helper", ":still_needed"),
            (assign, ":amount_to_recruit", ":volunteers_in_target"),
            (val_sub, ":amount_to_recruit", ":santas_little_helper"),
            (assign, ":new_target_volunteer_amount", ":volunteers_in_target"),
            (val_sub, ":new_target_volunteer_amount", ":amount_to_recruit"),
            (party_set_slot, ":target", slot_center_volunteer_troop_amount, ":new_target_volunteer_amount"),
            (party_add_members, ":party_no", ":target_volunteer_type", ":amount_to_recruit"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (else_try),
            (le, ":volunteers_in_target", ":still_needed"),
            (gt, ":volunteers_in_target", 0),
            (party_set_slot, ":target", slot_center_volunteer_troop_amount, -1),
            (party_add_members, ":party_no", ":target_volunteer_type", ":volunteers_in_target"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (else_try),
            (le, ":volunteers_in_target", 0),
            (party_set_ai_behavior, ":party_no", ai_bhvr_hold),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (else_try),
            (display_message, "@ERROR IN THE RECRUITER KIT SIMPLE TRIGGERS!",0xFF2222),
            (party_set_slot, ":target", dplmc_slot_village_reserved_by_recruiter, 0),
         (try_end),
      (try_end),
   (try_end),

   (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, dplmc_spt_recruiter),
      (party_get_num_companions, ":amount", ":party_no"),
      (val_sub, ":amount", 1),   #the recruiter himself doesn't count
      (party_get_slot, ":needed", ":party_no", dplmc_slot_party_recruiter_needed_recruits),
      (eq, ":amount", ":needed"),
      (party_get_slot, ":party_origin", ":party_no", dplmc_slot_party_recruiter_origin),
      (try_begin),
         (neg|party_slot_eq, ":party_no", slot_party_ai_object, ":party_origin"),
         (party_set_slot, ":party_no", slot_party_ai_object, ":party_origin"),
         (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
         (party_set_ai_object, ":party_no", ":party_origin"),
      (try_end),
      (store_distance_to_party_from_party, ":distance_from_origin", ":party_no", ":party_origin"),
      (try_begin),
         (le, ":distance_from_origin", 0),
         (party_get_num_companion_stacks, ":stacks", ":party_no"),
         (try_for_range, ":stack_no", 1, ":stacks"),
            (party_stack_get_size, ":size", ":party_no", ":stack_no"),
            (party_stack_get_troop_id, ":troop_id", ":party_no", ":stack_no"),
            (party_add_members, ":party_origin", ":troop_id", ":size"),
         (try_end),
         (str_store_party_name_link, s13, ":party_origin"),
         (assign, reg10, ":amount"),
         (display_log_message, "@A recruiter has brought {reg10} recruits to {s13}.", 0x00FF00),
         (remove_party, ":party_no"),
      (try_end),
   (try_end),
   ]),

#This trigger makes sure that no village is left reserved forever.
(12,
   [
   (try_for_range, ":village", villages_begin, villages_end),
      (party_set_slot, ":village", dplmc_slot_village_reserved_by_recruiter, 0),
   (try_end),
   ]),
#Recruiter kit end

 #process gift_carvans
 (0.5,
 [
  (eq, "$g_player_chancellor", "trp_dplmc_chancellor"),
  ##nested diplomacy start+
  #These gifts are far too efficient.  To be balanced with Native, they
  #should not (at the best case) exceed an efficiency of 1000 gold per point.
  (assign, ":save_reg0", reg0),
  (assign, ":save_reg1", reg1),
  (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),#store for use below
  ##nested diplomacy end+
  (try_for_parties, ":party_no"),
    (party_slot_eq,":party_no", slot_party_type, dplmc_spt_gift_caravan),
    (party_is_active, ":party_no"),
    (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
    (party_get_slot, ":target_troop", ":party_no", slot_party_orders_object),

    (try_begin),
      (party_is_active, ":target_party"),

      (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
      (str_store_party_name, s14, ":party_no"),
      (str_store_party_name, s15,":target_party"),

      (try_begin), #debug
        (eq, "$cheat_mode", 1),
        (assign, reg0, ":distance_to_target"),
        (display_message, "@Distance between {s14} and {s15}: {reg0}"),
      (try_end),

      (try_begin),
        (le, ":distance_to_target", 1),

        (party_get_slot, ":gift", ":party_no", dplmc_slot_party_mission_diplomacy),
        (str_store_item_name, s12, ":gift"),

        (try_begin),
          (gt, ":target_troop", 0),
          (str_store_troop_name, s13, ":target_troop"),
        (else_try),
          (str_store_party_name, s13, ":target_party"),
        (end_try),
        (display_log_message, "@Your caravan has brought {s12} to {s13}.", 0x00FF00),

        (assign, ":relation_boost", 0),
        (store_faction_of_party, ":target_faction", ":target_party"),

        (try_begin),
          (gt, ":target_troop", 0),
          (faction_slot_eq,":target_faction",slot_faction_leader,":target_troop"),
          (try_begin),
            (eq, ":gift", "itm_wine"),
            (assign, ":relation_boost", 1),
          (else_try),
            (eq, ":gift", "itm_oil"),
            (assign, ":relation_boost", 2),
          (try_end),
        (else_try),
          (store_random_in_range, ":random", 1, 3),
          (try_begin),
            (eq, ":gift", "itm_ale"),
            (val_add, ":relation_boost", ":random"),
          (else_try),
            (eq, ":gift", "itm_wine"),
            (store_add, ":relation_boost", 1, ":random"),
          (else_try),
            (eq, ":gift", "itm_oil"),
            (store_add, ":relation_boost", 2, ":random"),
          (else_try),
            (eq, ":gift", "itm_raw_dyes"),
            (val_add, ":relation_boost", 1),
          (else_try),
            (eq, ":gift", "itm_raw_silk"),
            (val_add, ":relation_boost", 2),
          (else_try),
            (eq, ":gift", "itm_velvet"),
            (val_add, ":relation_boost", 4),
          (else_try),
            (eq, ":gift", "itm_smoked_fish"),
            (try_begin),
              (party_slot_eq, ":target_party", slot_party_type, spt_village),
              (val_add, ":relation_boost", 1),
            (try_end),
          (else_try),
            (eq, ":gift", "itm_cheese"),
            (val_add, ":relation_boost", 1),
            (try_begin),
              (party_slot_eq, ":target_party", slot_party_type, spt_village),
              (val_add, ":relation_boost", 1),
            (try_end),
          (else_try),
            (eq, ":gift", "itm_honey"),
            (val_add, ":relation_boost", 2),
            (try_begin),
              (party_slot_eq, ":target_party", slot_party_type, spt_village),
              (val_add, ":relation_boost", 2),
            (try_end),
          (try_end),
        (try_end),

        (try_begin),
          (this_or_next|eq, ":target_faction", "fac_player_supporters_faction"),
          (eq, ":target_faction", "$players_kingdom"),
          (val_add, ":relation_boost", 1),
        (try_end),

		##nested diplomacy start+
		#Determine the gold cost of the gifts.
		(store_item_value, ":gift_value", ":gift"),
		#Determine how many copies of the gift are used
		(party_get_slot, ":gift_value_factor", ":party_no", dplmc_slot_party_mission_parameter_1),
		(try_begin),
			#This should only fail if the game was saved using an old version while
			#a caravan was en route.
			(gt, ":gift_value_factor", 0),
			(val_mul, ":gift_value", ":gift_value_factor"),
		(else_try),
			#Gifts to ladies had no multiplier.
			#Also, don't do anything for non-trade-goods.
			(this_or_next|is_between, ":target_troop", kingdom_ladies_begin, kingdom_ladies_end),
			(neg|is_between, ":gift", trade_goods_begin, trade_goods_end),
		(else_try),
			 #Gifts to lords used 150 copies of an item
			(is_between, ":target_troop", active_npcs_begin, active_npcs_end),
			(val_mul, ":gift_value", 150),
		(else_try),
			#Gifts to centers used 300 copies of an item
			(is_between, ":target_party", centers_begin, centers_end),
			(val_mul, ":gift_value", 300),
		(try_end),
		(assign, ":gift_value_factor", 100),

		#(store_sub, ":gift_slot_no", ":gift", trade_goods_begin),
		#(val_add, ":gift_slot_no", slot_town_trade_good_prices_begin),

		(try_begin),
			#Gift isn't a trade good: this should never happen
			(neg|is_between, ":gift", trade_goods_begin, trade_goods_end),
			(try_begin),
				(this_or_next|gt, ":target_troop", 0),
					(party_slot_eq, ":target_party", slot_party_type, spt_town),
				(assign, ":gift_value_factor", 115),
			(else_try),
				(assign, ":gift_value_factor", 130),
			(try_end),
		(else_try),
			#Given to a lord.
			(gt, ":target_troop", 0),

			(assign, ":global_price_factor", 0),
			(assign, ":faction_price_factor", 0),
			(assign, ":faction_markets", 0),
			(assign, ":personal_price_factor", 0),
			(assign, ":personal_markets", 0),

			(try_for_range, ":center_no", towns_begin, towns_end),
				(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
				(val_add, ":global_price_factor", reg0),

				(store_faction_of_party, ":center_faction", ":center_no"),
				(eq, ":center_faction", ":target_faction"),
				(val_add, ":faction_price_factor", reg0),
				(val_add, ":faction_markets", 1),

				(party_slot_eq, ":center_no", slot_town_lord, ":target_troop"),
				(val_add, ":personal_price_factor", reg0),
				(val_add, ":personal_markets", 1),
			(try_end),

			(try_begin),
				(eq, ":personal_markets", 0),
				(try_for_range, ":center_no", villages_begin, villages_end),
					(try_begin),
						(party_slot_eq, ":center_no", slot_town_lord, ":target_troop"),
						(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
						(val_add, ":faction_markets", reg0),
						(val_add, ":personal_markets", 1),
					(try_end),
					#Check for castles (deliberately allow multiple-counting)
					(try_begin),
						(party_get_slot, reg1, ":center_no", slot_village_bound_center),
						(gt, reg1, 0),
						(party_slot_eq, reg1, slot_party_type, spt_castle),
						(party_slot_eq, reg1, slot_town_lord, ":target_troop"),
						(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
						(val_add, ":faction_markets", reg0),
						(val_add, ":personal_markets", 1),
					(try_end),
				(try_end),
			(try_end),

			(try_begin),
				#First use any markets at or near the target's fiefs
				(gt, ":personal_markets", 0),
				(store_div, ":gift_value_factor", ":personal_price_factor", ":personal_markets"),
			(else_try),
				#Alternately use any faction markets
				(gt, ":faction_markets", 0),
				(val_mul, ":faction_price_factor", 130),#Convert trade penalty from 115% to 130%
				(val_div, ":faction_price_factor", 115),
				(store_div, ":gift_value_factor", ":faction_price_factor", ":faction_markets"),
			(else_try),
				#As a final option use the global average price
				(gt, towns_end, towns_begin),#should always be true (if not, then the gift price factor stays average)
				(store_sub, reg1, towns_end, towns_begin),
				(val_mul, ":global_price_factor", 130),#Convert trade penalty from 115% to 130%
				(val_div, ":global_price_factor", 115),
				(store_div, ":gift_value_factor", ":global_price_factor", reg1),
			(try_end),
		(else_try),
			#Given to a town or village
			(gt, ":target_party", 0),
			(call_script, "script_dplmc_get_item_buy_price_factor", ":gift", ":center_no", -2, -2),
			(assign, ":gift_value_factor", reg0),
		(else_try),
			#This should never happen
			(assign, ":gift_value_factor", 115),
		(try_end),

		(try_begin),
			(ge, "$cheat_mode", 1),
			(assign, reg0, ":gift_value_factor"),
			(store_mul, reg1, ":gift_value", ":gift_value_factor"),
			(val_add, reg1, 50),
			(val_div, reg1, 100),
			(val_add, reg1, 50),
			(display_message, "@{!} Gift price factor {reg0}/100, effective value {reg1}"),
		(try_end),

		(val_mul, ":gift_value", ":gift_value_factor"),
		(val_add, ":gift_value", 50),
		(val_div, ":gift_value", 100),

		(val_add, ":gift_value", 50),#the cost of the messenger
	    (store_random_in_range, ":random", 0, 1000),#randomly round up or down later, when dividing by 1000
		(assign, reg0, ":gift_value"),#<-- see (1) below, store gold value of gift
		(val_add, ":gift_value", ":random"),
		(val_div, ":gift_value", 1000),

		(try_begin),
		   (eq, ":reduce_campaign_ai", 0), #hard: do not exceed 1/1000 efficiency
		   (val_min, ":relation_boost", ":gift_value"),
		   (try_begin),
			  (eq, ":relation_boost", 0),
			  (store_random_in_range, ":random", 0, 1000),
			  (lt, ":random", reg0),#<-- (1) see above, has gold value of gift
			  (assign, ":relation_boost", 1),
		   (try_end),
		(else_try),
		   (eq, ":reduce_campaign_ai", 1), #medium: use a blend of the two
		   (lt, ":gift_value", ":relation_boost"),
		   (val_add, ":relation_boost", ":gift_value"),
		   (val_add, ":relation_boost", 1),
		   (val_div, ":relation_boost", 2),
	    (else_try),
		   (eq, ":reduce_campaign_ai", 2), #easy: do not use
		(try_end),

		(val_max, ":gift_value", 1),
		(val_min, ":relation_boost", ":gift_value"),
		##nested diplomacy end+

        (try_begin),
		##nested diplomacy start+
		#Write a message so the player doesn't think the lack of relation gain is an error.
			(lt, ":relation_boost", 1),
			(try_begin),
				(gt, ":target_troop", 0),
				(display_message, "@{s13} is unimpressed by your paltry gift."),
			(else_try),
				(display_message, "@The people of {s13} are unimpressed by your paltry gift."),
			(try_end),
		(else_try),
		##nested diplomacy+
          (gt, ":target_troop", 0),
		  (call_script, "script_change_player_relation_with_troop", ":target_troop", ":relation_boost"),
        (else_try),
          (call_script, "script_change_player_relation_with_center", ":target_party", ":relation_boost"),
        (try_end),
        (remove_party, ":party_no"),
      (try_end),
    (else_try),
      (display_log_message, "@Your caravan has lost it's way and gave up your mission!", 0xFF0000),
      (remove_party, ":party_no"),
    (try_end),
  (try_end),
  ##nested diplomacy start+
  (assign, reg0, ":save_reg0"),
  (assign, reg1, ":save_reg1"),
  ##nested diplomacy start+
 ]),

 #process messengers
 (0.5,
 [
  (try_for_parties, ":party_no"),
    (party_slot_eq,":party_no", slot_party_type, spt_messenger),

    (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
    (party_get_slot, ":orders_object", ":party_no", slot_party_orders_object),

    (try_begin),
      (party_is_active, ":target_party"),
      (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
      (str_store_party_name, s14, ":party_no"),
      (str_store_party_name, s15,":target_party"),

      (try_begin), #debug
        (eq, "$cheat_mode", 1),
        (assign, reg0, ":distance_to_target"),
        (display_message, "@Distance between {s14} and {s15}: {reg0}"),
      (try_end),

      (try_begin),
        (le, ":distance_to_target", 1),

        (try_begin), # returning to p_main_party
          (eq, ":target_party", "p_main_party"),
          (party_get_slot, ":party_leader", ":party_no", slot_party_orders_object),
          (party_get_slot, ":success", ":party_no", dplmc_slot_party_mission_diplomacy),
          (call_script, "script_add_notification_menu", "mnu_dplmc_messenger", ":party_leader", ":success"),
          (remove_party, ":party_no"),
        (else_try), # patrols
          (party_slot_eq, ":target_party", slot_party_type, spt_patrol),
          (party_get_slot, ":message", ":party_no", dplmc_slot_party_mission_diplomacy),

          (try_begin),
            (eq, ":message", spai_undefined),
            (remove_party, ":target_party"),
          (else_try),
            (eq, ":message", spai_retreating_to_center),
            (str_store_party_name, s6, ":orders_object"),
            (party_set_name, ":target_party", "@Transfer to {s6}"),
            (party_set_ai_behavior, ":target_party", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":target_party", ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_object, ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_state, spai_retreating_to_center),
            (party_set_aggressiveness, ":target_party", 0),
            (party_set_courage, ":target_party", 3),
            (party_set_ai_initiative, ":target_party", 100),
          (else_try),
            (str_store_party_name, s6, ":orders_object"),
            (party_set_name, ":target_party", "@{s6} patrol"),
            (party_set_ai_behavior, ":target_party", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":target_party", ":orders_object"),
            (party_set_slot, ":target_party", slot_party_ai_object, ":orders_object"),
            (party_set_slot, ":target_party", slot_party_orders_type, ":message"),
          (try_end),

          (remove_party, ":party_no"),
        (else_try), # reached any other target
          (party_stack_get_troop_id, ":party_leader", ":target_party", 0),
          (str_store_troop_name, s13, ":party_leader"),

          (try_begin), #debug
            (eq, "$cheat_mode", 1),
            (display_log_message, "@Your messenger reached {s13}.", 0x00FF00),
            (assign, "$g_talk_troop", ":party_leader"), #debug
          (try_end),

          (party_get_slot, ":message", ":party_no", dplmc_slot_party_mission_diplomacy),
          (assign, ":success", 0),
          (try_begin),
            (party_set_slot, ":target_party", slot_party_commander_party, "p_main_party"),
          	(store_current_hours, ":hours"),
          	(party_set_slot, ":target_party", slot_party_following_orders_of_troop, "trp_kingdom_heroes_including_player_begin"),
          	(party_set_slot, ":target_party", slot_party_orders_object, ":orders_object"),
          	(party_set_slot, ":target_party", slot_party_orders_type, ":message"),

          	(party_set_slot, ":target_party", slot_party_orders_time, ":hours"),
            #CC-C begin
            (gt,":party_leader",0),
            (troop_get_slot, ":party_check", ":party_leader", slot_troop_leaded_party),
            (party_is_active, ":party_check"),
            #CC-C end
            (call_script, "script_npc_decision_checklist_party_ai", ":party_leader"), #This handles AI for both marshal and other parties		
  
            (try_begin), #debug
              (eq, "$cheat_mode", 1),
              (display_message, "@{s14}"), #debug
            (try_end),

            (try_begin),
              (eq, reg0, ":message"),
              (eq, reg1, ":orders_object"),
              (assign, ":success", 1),
            (try_end),
            (call_script, "script_party_set_ai_state", ":target_party", reg0, reg1),
          (try_end),

          (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
          (party_set_ai_object, ":party_no", "p_main_party"),
          (party_set_slot, ":party_no", slot_party_ai_object, "p_main_party"),
          (party_set_slot, ":party_no", slot_party_orders_object, ":party_leader"),
          (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":success"),
        (try_end),
      (try_end),
    (else_try),
      (display_log_message, "@Your messenger has lost it's way and gave up your mission!", 0xFF0000),
      (remove_party, ":party_no"),
    (try_end),
  (try_end),
 ]),


  # Constable training
   (24,
   [
   (eq, "$g_player_constable", "trp_dplmc_constable"),
   (is_between, "$g_constable_training_center", walled_centers_begin, walled_centers_end),
   (party_slot_eq, "$g_constable_training_center", slot_town_lord, "trp_player"),

   (store_skill_level, ":trainer_level", skl_trainer, "trp_player"),
   (val_add, ":trainer_level", 4),
   (store_div, ":xp_gain", ":trainer_level", 2),

   (try_for_parties, ":party_no"),
    (party_slot_eq, ":party_no", slot_town_lord, "trp_player"),
    (eq, ":party_no", "$g_constable_training_center"),
	
	#occc start
	(try_begin),
          (party_slot_eq, ":party_no", slot_center_has_barrack, 1),#if targeted town has a barrack,
		  (store_mul, ":xp_gain",  2),                             #auto training xp gain gets boosted!
		  (store_add, ":xp_gain",  8),
          (party_slot_eq, ":party_no", slot_center_has_greater_barrack, 1),#if targeted town has a greater barrack,
		  (store_mul, ":xp_gain",  2),                             #auto training xp gain moar boosted!!
		  (store_add, ":xp_gain",  50),
	(try_end),
	#occc end
	
    (party_get_num_companion_stacks, ":num_stacks", ":party_no"),

    (assign, ":trained", 0),
    (try_for_range, ":i_stack", 0, ":num_stacks"),
      (eq, ":trained", 0),
      (party_stack_get_troop_id, ":troop_id", ":party_no", ":i_stack"),
      (neg|troop_is_hero, ":troop_id"),

      (troop_get_upgrade_troop, ":upgrade_troop", ":troop_id" , "$g_constable_training_type"),
      (try_begin),
       (le, ":upgrade_troop", 0),
       (troop_get_upgrade_troop, ":upgrade_troop", ":troop_id", 0),
      (try_end),

      #only proceed if troop is upgradable
      (gt, ":upgrade_troop", 0),

      (store_character_level, ":troop_level", ":troop_id"),
      (assign, ":troop_limit" , 6),

      (try_begin),
        (eq, "$g_constable_training_improved", 1),
        (assign, ":troop_limit" , 10),
        (try_begin),
          (le, ":troop_level", 6),
          (val_add, ":xp_gain", 2), #more recruits are trained during improved training
        (try_end),
      (try_end),

      (le, ":troop_level", ":troop_limit"),

      (party_count_members_of_type,":cur_number",":party_no",":troop_id"),
      (val_min, ":xp_gain", ":cur_number"),

      (call_script, "script_game_get_upgrade_cost", ":troop_id"),
      (store_mul, ":upgrade_cost", ":xp_gain", reg0),

      (try_begin),
        (eq, "$g_constable_training_improved", 1),
        (val_add, ":upgrade_cost", 10), #+10 denars during improved training
      (try_end),

      (store_troop_gold, ":gold", "trp_household_possessions"),
      (try_begin),
        (lt, ":gold", ":upgrade_cost"),
        (store_div, ":money_limit", ":gold", reg0),
        (val_min, ":xp_gain", ":money_limit"),
        (store_mul, ":upgrade_cost", ":xp_gain", reg0),
        (display_message, "@Not enough money in treasury to upgrade troops."),
      (try_end),

      (party_remove_members,":party_no",":troop_id",":xp_gain"),
      (party_add_members, ":party_no", ":upgrade_troop", ":xp_gain"),

      (call_script, "script_dplmc_withdraw_from_treasury", ":upgrade_cost"),

      (assign, reg5, ":xp_gain"),
      (str_store_troop_name, s6, ":troop_id"),
      (str_store_troop_name, s7, ":upgrade_troop"),
      (str_store_party_name, s8, ":party_no"),
      (display_message, "@Your constable upgraded {reg5} {s6} to {s7} in {s8}"),
      (assign, ":trained", 1),
    (try_end),
   (try_end),
    ]),

  # Patrol wages
   (24 * 7,
   [

    (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, spt_patrol),



      (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
      (eq, ":ai_state", spai_patrolling_around_center),

      (try_begin),
		(party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"),
        (assign, ":total_wage", 0),
        (party_get_num_companion_stacks, ":num_stacks", ":party_no"),
        (try_for_range, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":stack_troop", ":party_no", ":i_stack"),
          (ge,":stack_troop",0), #CC-C fix
          (party_stack_get_size, ":stack_size", ":party_no", ":i_stack"),
          (call_script, "script_game_get_troop_wage", ":stack_troop", 0),
          (val_mul, reg0, ":stack_size"),
          (val_add, ":total_wage", reg0),
        (try_end),
        (store_troop_gold, ":gold", "trp_household_possessions"),
        (try_begin),
          (lt, ":gold", ":total_wage"),
          (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
          (str_store_party_name, s6, ":target_party"),
          (display_log_message, "@Your soldiers patrolling {s6} disbanded because you can't pay the wages!", 0xFF0000),
          (remove_party, ":party_no"),
        (try_end),
      (try_end),
    (try_end),
    ]),

  #create ai patrols
   (24 * 7,
   [
    (try_for_range, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),

      (assign, ":max_patrols", 0),
      (try_for_range, ":center", towns_begin, towns_end),
        (store_faction_of_party, ":center_faction", ":center"),
        (eq, ":center_faction", ":kingdom"),
        (val_add, ":max_patrols", 1),
      (try_end),

      (assign, ":count", 0),
      (try_for_parties, ":party_no"),
        (party_slot_eq, ":party_no", slot_party_type, spt_patrol),
        (store_faction_of_party, ":party_faction", ":party_no"),
        (eq, ":party_faction", ":kingdom"),
        (neg|party_slot_eq, ":party_no", dplmc_slot_party_mission_diplomacy, "trp_player"), #not player ordered
        (try_begin),
           #Remove patrols above the maximum number allowed.
           (ge, ":count", ":max_patrols"),
           (try_begin),
              (ge, "$cheat_mode", 1),
              (str_store_faction_name, s4, ":kingdom"),
              (str_store_party_name, s5, ":party_no"),
              (display_message, "@{!}DEBUG - Removed {s5} because {s4} cannot support that many patrols"),
           (try_end),
           (remove_party, ":party_no"),
        (else_try),
           (val_add, ":count", 1),
        (try_end),
      (try_end),

      (try_begin),
        (lt, ":count", ":max_patrols"),

        (store_random_in_range, ":random", 0, 10),
        (le, ":random", 3),

        (assign, ":start_center", -1),
        (assign, ":target_center", -1),

        (try_for_range, ":center", towns_begin, towns_end),
          (store_faction_of_party, ":center_faction", ":center"),
          (eq, ":center_faction", ":kingdom"),

          (eq, ":start_center", -1),
          (eq, ":target_center", -1),

          (assign, ":continue", 1),
          (try_for_parties, ":party_no"),
            (party_slot_eq, ":party_no", slot_party_type, spt_patrol),
            (store_faction_of_party, ":party_faction", ":party_no"),
            (eq, ":party_faction", ":kingdom"),
            (party_get_slot, ":target", ":party_no", slot_party_ai_object),
            (eq, ":target", ":center"),
            (assign, ":continue", 0),
          (try_end),
          (eq, ":continue", 1),

          (call_script, "script_cf_select_random_town_with_faction", ":kingdom"),
          (neq, reg0, -1),

          (assign, ":start_center", reg0),
          (assign, ":target_center", ":center"),
        (try_end),

        (try_begin),
          (neq, ":start_center", -1),
          (neq, ":target_center", -1),
          (store_random_in_range, ":random_size", 0, 3),
          (faction_get_slot, ":faction_leader", ":kingdom", slot_faction_leader),
          (call_script, "script_dplmc_send_patrol", ":start_center", ":target_center", ":random_size",":kingdom", ":faction_leader"),
        (try_end),
      (try_end),
    (try_end),
    ]),

  # Patrol ai
   (2,
   [

    (try_for_parties, ":party_no"),
      (party_get_template_id, ":party_template", ":party_no"),
      (this_or_next | eq, ":party_template", "pt_occc_nomad_camp"),#occc
      (party_slot_eq,":party_no", slot_party_type, spt_patrol),

      (call_script, "script_party_remove_all_prisoners", ":party_no"),

      (try_begin),
        (get_party_ai_behavior, ":ai_behavior", ":party_no"),
        (eq, ":ai_behavior", ai_bhvr_travel_to_party),
        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),

        (try_begin),
          (gt, ":target_party", 0),
          (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
          (le, ":distance_to_target", 5),
          (try_begin),
            (party_get_slot, ":ai_state", ":party_no", slot_party_ai_state),
            (eq, ":ai_state", spai_retreating_to_center),
            (try_begin),
			  (neq, ":party_template", "pt_occc_nomad_camp"),#occc
              (le, ":distance_to_target", 1),
              (call_script, "script_party_add_party", ":target_party", ":party_no"),
              (remove_party, ":party_no"),
			(else_try),#nomad camp
              (le, ":distance_to_target", 1),
			  (party_add_template,":party_no","pt_kingdom_3_reinforcements_a"),
            (try_end),
          (else_try),
            (party_get_position, pos1, ":target_party"),
            (party_set_ai_behavior,":party_no", ai_bhvr_patrol_location),
            (party_set_ai_patrol_radius, ":party_no", 1),
            (party_set_ai_target_position, ":party_no", pos1),
          (try_end),
        (else_try),
          #remove party?
        (try_end),

      (try_end),
    ## CC-D begin: expand manhunter
    (else_try),
      (party_get_template_id, ":template", ":party_no"),
      (eq, ":template", "pt_manhunters"),

      (try_begin),
        (get_party_ai_behavior, ":ai_behavior", ":party_no"),
        (eq, ":ai_behavior", ai_bhvr_travel_to_point),
        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),

        (try_begin),
          (gt, ":target_party", 0),
          (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
          (le, ":distance_to_target", 60),
          (party_slot_eq, ":party_no", slot_party_ai_state, spai_patrolling_around_center),
          (party_get_position, pos1, ":target_party"),
          (party_set_ai_behavior,":party_no", ai_bhvr_patrol_location),
          (party_set_ai_patrol_radius, ":party_no", 2),
          (party_set_ai_target_position, ":party_no", pos1),
        (try_end),
      (try_end),
    ## CC-D end
    (try_end),
    ]),

  # Scout ai
   (0.2,
   [

    (try_for_parties, ":party_no"),
      (party_slot_eq,":party_no", slot_party_type, spt_scout),

      (try_begin),
        (get_party_ai_behavior, ":ai_behavior", ":party_no"),
        (this_or_next|eq, ":ai_behavior", ai_bhvr_travel_to_point),
        (eq, ":ai_behavior", ai_bhvr_travel_to_party),

        (party_get_slot, ":target_party", ":party_no", slot_party_ai_object),
        (store_distance_to_party_from_party, ":distance_to_target", ":party_no", ":target_party"),
        (le, ":distance_to_target", 1),

        (try_begin),
          (eq, ":target_party", "p_main_party"),

          (party_get_slot, ":mission_target", ":party_no", dplmc_slot_party_mission_diplomacy),
          (call_script, "script_add_notification_menu", "mnu_dplmc_scout", ":mission_target", 0),

          (remove_party, ":party_no"),
        (else_try),
          (neq, ":target_party", "p_main_party"),
          (party_get_slot, ":hours", ":party_no", dplmc_slot_party_mission_diplomacy),

          (try_begin),
            (le, ":hours", 100),
            (disable_party, ":party_no"),
            (val_add, ":hours", 1),
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":hours"),

            (try_begin),
              (store_random_in_range, ":random", 0, 1000),
              (eq, ":random", 0),
              (str_store_party_name, s11, ":target_party"),
              (display_log_message, "@It is rumoured that a spy has been caught in {s11}.", 0xFF0000),
              (remove_party, ":party_no"),
            (try_end),

          (else_try),
            (enable_party, ":party_no"),
            (party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),
            (party_set_ai_object, ":party_no", "p_main_party"),
            (party_set_slot, ":party_no", slot_party_ai_object, "p_main_party"),
            (party_set_slot, ":party_no", dplmc_slot_party_mission_diplomacy, ":target_party"),
          (try_end),

        (try_end),
      (try_end),
    (try_end),
    ]),

  # Policy
   (30 * 24,
   [
	##nested diplomacy start+
	##If the player is ruler or co-ruler of an NPC kingdom, make sure the
	#policy matches fac_player_supporters_faction.  (It should be synchronized
	#elsewhere, but do it here in case there has been an error.)
	(assign, ":player_is_coruler_of_npc_faction", 0),
	  (try_begin),
		(neq, "$players_kingdom", "fac_player_supporters_faction"),
		(is_between, "$players_kingdom", npc_kingdoms_begin, npc_kingdoms_end),
		(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
		(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),

		(assign, ":player_is_coruler_of_npc_faction", 1),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_serfdom),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_serfdom,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_centralization),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_centralization,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_quality),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_quality,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_aristocracy),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_aristocracy,  reg0),

		(faction_get_slot, reg0, "$players_kingdom", dplmc_slot_faction_mercantilism),
		(faction_set_slot, "fac_player_supporters_faction", dplmc_slot_faction_mercantilism,  reg0),
	(try_end),
	##nested diplomacy end+
  (try_for_range, ":kingdom", kingdoms_begin, kingdoms_end),
    (faction_slot_eq, ":kingdom", slot_faction_state, sfs_active),

    (faction_get_slot, ":centralization", ":kingdom", dplmc_slot_faction_centralization),
    (faction_get_slot, ":aristocracy", ":kingdom", dplmc_slot_faction_aristocracy),
    (faction_get_slot, ":quality", ":kingdom", dplmc_slot_faction_quality),
    (faction_get_slot, ":serfdom", ":kingdom", dplmc_slot_faction_serfdom),
	 ##nested diplomacy start+
    (faction_get_slot, ":mercantilism", ":kingdom", dplmc_slot_faction_mercantilism),
	 ##nested diplomacy end+

    (try_begin),
      (eq, "$cheat_mode", 1),
      (str_store_faction_name, s9, ":kingdom"),
      (assign, reg1, ":centralization"),
      (display_message, "@{!}DEBUG - centralization {reg1}"),
      (assign, reg1, ":aristocracy"),
      (display_message, "@{!}DEBUG - aristocracy {reg1}"),
      (assign, reg1, ":quality"),
      (display_message, "@{!}DEBUG - quality {reg1}"),
      (assign, reg1, ":serfdom"),
      (display_message, "@{!}DEBUG - serfdom {reg1}"),
		##nested diplomacy start+
      (assign, reg1, ":mercantilism"),
      (display_message, "@{!}DEBUG - mercantilism {reg1}"),
		##nested diplomacy end+
    (try_end),

    (try_begin),
      (is_between, ":kingdom", npc_kingdoms_begin, npc_kingdoms_end),
      ##nested diplomacy start+
      ##Ensure the player isn't the kingdom's ruler or co-ruler
      (this_or_next|neq, ":kingdom", "$players_kingdom"),
		(eq, ":player_is_coruler_of_npc_faction", 0),
	  ##Add the chance to move around mercantilism.
      #(store_random_in_range, ":random", 0, 8),
	  (store_random_in_range, ":random", 0, 10),
      ##nested diplomacy end+

      (try_begin),
        (eq,0,1), #CC-C begin unused
		  ##nested diplomacy start+
        #(is_between, ":random", 1, 5),
		  (is_between, ":random", 1, 6),
		  ##nested diplomacy end+
        (store_random_in_range, ":change", -1, 2),

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_faction_name, s12, ":kingdom"),
          (assign, reg1, ":change"),
          (assign, reg2, ":random"),
          (display_message, "@{!}DEBUG - changing {reg1} of {reg2} for {s12}"),
        (try_end),

        (try_begin),
          (eq, ":random", 1),
          (val_add, ":centralization", ":change"),
          (val_max, ":centralization", -3),
          (val_min, ":centralization", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_centralization, ":centralization"),
        (else_try),
          (eq, ":random", 2),
          (val_add, ":aristocracy", ":change"),
          (val_max, ":aristocracy", -3),
          (val_min, ":aristocracy", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_aristocracy, ":aristocracy"),
        (else_try),
          (eq, ":random", 3),
          (val_add, ":quality", ":change"),
          (val_max, ":quality", -3),
          (val_min, ":quality", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_quality, ":quality"),
        (else_try),
          (eq, ":random", 4),
          (val_add, ":serfdom", ":change"),
          (val_max, ":serfdom", -3),
          (val_min, ":serfdom", 3),
          (faction_set_slot, ":kingdom", dplmc_slot_faction_serfdom, ":serfdom"),
		  ##nested diplomacy start+
          (eq, ":random", 5),
          (val_add, ":mercantilism", ":change"),
			 (val_clamp, ":mercantilism", -3, 4),#-3 min, +3 max
          (faction_set_slot, ":kingdom", dplmc_slot_faction_mercantilism, ":mercantilism"),
		  ##nested diplomacy end+
        (try_end),
      (try_end),

    (else_try),

      #only player faction is affected by relation hits
      ##nested diplomacy start+
      ##Don't alter the values of centralization and aristocracy, since that's confusing.
      #(store_mul, ":centralization", ":centralization", -1),
      #(store_mul, ":aristocracy", ":aristocracy", 1),
      #(store_add, ":relation_change", ":centralization", ":aristocracy"),

		(store_sub, ":relation_change", ":aristocracy", ":centralization"),
      ##custodian (merchant) lords like plutocracy, unlike ordinary lords
      (store_mul, ":custodian_change", ":aristocracy", -1),
		(val_sub, ":custodian_change", ":centralization"),
      #benefactor lords like freedom and dislike serfdom
		(store_mul, ":benefactor_change", ":serfdom", -1),
		(val_sub, ":custodian_change", ":centralization"),
      ##nested diplomacy end+
      (try_begin),
        ##nested diplomacy start+
        (this_or_next|neq, ":benefactor_change", 0),
        (this_or_next|neq, ":custodian_change", 0),
        ##nested diplomacy end+
        (neq, ":relation_change", 0),

        (try_begin),
          (eq, "$cheat_mode", 1),
          (str_store_faction_name, s9, ":kingdom"),
          (assign, reg1, ":relation_change"),
          (display_message, "@{!}DEBUG - relation_change =  {reg1} for {s9}"),
        (try_end),

        ##diplomacy start+ also include kingdom ladies who are kingdom heroes
        #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (try_for_range, ":troop_no", heroes_begin, heroes_end),
        ##diplomacy end+
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (store_troop_faction, ":faction_no", ":troop_no"),
          (eq, ":kingdom", ":faction_no"),
          (faction_get_slot, ":faction_leader", ":kingdom", slot_faction_leader),
          ##diplomacy start+
          (neq, ":troop_no", ":faction_leader"),
          (assign, ":change_for_troop", ":relation_change"),
          (try_begin),
             (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_custodian),
             (assign, ":change_for_troop", ":custodian_change"),
          (else_try),
             (troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_benefactor),
             (assign, ":change_for_troop", ":benefactor_change"),
          (try_end),
          ##Extra penalty for going back on a promise, extra bonus for keeping it
          (assign, ":promise_mod", 0),
          (try_begin),
             ##Following are only relevant for companions
				 (is_between, ":troop_no", companions_begin, companions_end),
             (troop_slot_eq, ":troop_no", slot_troop_kingsupport_state, 1),
             (try_begin),
                #Argument: Lords
                (troop_slot_eq, ":troop_no", slot_troop_kingsupport_argument, argument_lords),
                (try_begin),
                  #If more than slightly centralized, or more than slightly balanced against aristocrats
                  (this_or_next|neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),
                     (faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, 2),
                  (val_sub, ":promise_mod", 1),
                (else_try),
                  #If more than slightly decentralized or more than slightly balanced in favor of aristocrats
                  (this_or_next|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, 2),
                  (neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, -2),
                  (faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),#redundant
                  (val_add, ":promise_mod", 1),
                (try_end),
             (else_try),
                  #Argument: Commons
                  (troop_slot_eq, ":troop_no", slot_troop_kingsupport_argument, argument_commons),
                  (try_begin),
                    (faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 2),
                    (val_sub, ":promise_mod", 1),
                  (else_try),
                    (neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 0),
                    (store_add, ":local_temp", ":serfdom", ":aristocracy"),
                    (lt, ":local_temp", 0),
                    (val_add, ":promise_mod", 1),
                  (try_end),
             (try_end),
         (try_end),
         #Check other broken promises
         (try_begin),
             (troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_lords),
             (this_or_next|neg|faction_slot_ge, ":faction_no", dplmc_slot_faction_aristocracy, -1),
                (faction_slot_ge, ":faction_no", dplmc_slot_faction_centralization, 2),
             #Lord must actually have cared about argument
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_upstanding),
             (val_sub, ":promise_mod", 1),
         (else_try),
             (troop_slot_eq, ":troop_no", slot_lord_recruitment_argument, argument_commons),
             (faction_slot_ge, ":faction_no", dplmc_slot_faction_serfdom, 2),
             #Lord must actually have cared about argument
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_quarrelsome),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_selfrighteous),
             (neg|troop_slot_eq, ":troop_no", slot_lord_reputation_type, lrep_debauched),
             (val_sub, ":promise_mod", 1),
         (try_end),
         (val_clamp, ":promise_mod", -1, 2),#-1, 0, or 1
         (val_add, ":change_for_troop", ":promise_mod"),

		 (neq, ":change_for_troop", 0),
		 (call_script, "script_change_player_relation_with_troop", ":troop_no", ":change_for_troop"),
        ##diplomacy end+
        (try_end),
      (try_end),
    (try_end),
  (try_end),
  ]),

  # affilated family ai
   (24 * 7,
   [
	##nested diplomacy start+ (piggyback on this trigger) allow lords to return from exile
	(assign, ":save_reg0", reg0),
	(assign, ":save_reg1", reg1),
	(assign, ":save_reg4", reg4),
	(try_begin),
		#only proceed if setting is enabled
		(ge, "$g_dplmc_lord_recycling", DPLMC_LORD_RECYCLING_ENABLE),
		#Kings/pretenders do not return in this manner (it should be different if it does happen).
		#Companions have a separate mechanism for return.
		(assign, ":chosen_lord", -1),
		(assign, ":best_score", -101),
		(assign, ":num_exiles", 0),
		#iterate over lords from a random start point, wrapping back to zero
		(store_random_in_range, ":rand_no", lords_begin, lords_end),
		(try_for_range, ":index", lords_begin, lords_end),
		  (store_add, ":troop_no", ":rand_no", ":index"),
		  (try_begin),
			 #wrap back around when you go off the end
			  (ge, ":troop_no", lords_end),
			(val_sub, ":troop_no", lords_end),
			(val_add, ":troop_no", lords_begin),
		  (try_end),
		  #Elsewhere we do the bookkeeping of ensuring that when a lord gets exiled
		  #his occupation changes to dplmc_slto_exile, and when loading a Native
		  #saved gamed with diplomacy we make this change for any lords required.
		  (troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),

		  (store_troop_faction, ":faction_no", ":troop_no"),
		  (this_or_next|eq, ":faction_no", -1),
		  (this_or_next|eq, ":faction_no", "fac_commoners"),
			 (eq, ":faction_no", "fac_outlaws"),
		  (val_add, ":num_exiles", 1),
		  (try_begin),
		     #Pick the lord with the best relation with his original liege.
			  #In most cases this will be the lord that has been in exile
			  #the longest.
			  (troop_get_slot, ":new_faction", ":troop_no", slot_troop_original_faction),
			  (is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			  (faction_get_slot, ":faction_leader", ":new_faction", slot_faction_leader),
			  (gt, ":faction_leader", 0),
			  (call_script, "script_troop_get_relation_with_troop", ":troop_no", ":faction_leader"),
			  (this_or_next|eq, ":chosen_lord", -1),
			     (gt, reg0, ":best_score"),
			  (assign, ":chosen_lord", ":troop_no"),
			  (assign, ":best_score", reg0),
		  (else_try),
		     (eq, ":chosen_lord", -1),
			 (assign, ":chosen_lord", ":troop_no"),
		  (try_end),
      (try_end),
		#search is done
		(try_begin),
		 #no lord found
		 (eq, ":chosen_lord", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(display_message, "@{!}DEBUG - no eligible lords in exile"),
		 (try_end),
	    (else_try),
			#If there were fewer than 3 lords in exile, random chance that none will return.
			(lt, ":num_exiles", 3),
			(store_random_in_range, ":random", 0, 256),
			(ge, ":random", 128),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg0, ":num_exiles"),
				(display_message, "@{!}DEBUG - {reg0} lords found in exile; randomly decided not to try to return anyone."),
			(try_end),
		(else_try),
		 #found a lord
		 (neq, ":chosen_lord", -1),
		 (try_begin),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":chosen_lord"),
			(assign, reg0, ":best_score"),
			(assign, reg1, ":num_exiles"),
			(display_message, "@{!}DEBUG - {reg1} lords found in exile; {s4} chosen to return, score was {reg0}"),
		 (try_end),
		 #To decrease the displeasing fragmentation of lord cultures, bias towards assigning
		 #the lord back to his original faction if possible.
		 (troop_get_slot, ":new_faction", ":chosen_lord", slot_troop_original_faction),
		 (try_begin),
			 #If the original faction is not active, or the lord's relation is too low, use a different faction
			 (this_or_next|lt, ":best_score", -50),
			 (this_or_next|neg|is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			    (neg|faction_slot_eq, ":new_faction", slot_faction_state, sfs_active),
		    (call_script, "script_lord_find_alternative_faction", ":chosen_lord"),
			(assign, ":new_faction", reg0),
		 (try_end),
		 (try_begin),
		   (neg|is_between, ":new_faction", kingdoms_begin, kingdoms_end),
			(ge, "$cheat_mode", 1),
			(str_store_troop_name, s4, ":chosen_lord"),
			(display_message, "@{!}DEBUG - {s4} found no faction to return to!"),
		 (try_end),
		 (is_between, ":new_faction", kingdoms_begin, kingdoms_end),
		 (assign, ":num_inactive", 0),
		 (try_begin),
			(eq, ":new_faction", "$players_kingdom"),
			(call_script, "script_dplmc_get_troop_standing_in_faction", "trp_player", "$players_kingdom"),
			(ge, reg0, DPLMC_FACTION_STANDING_LEADER_SPOUSE),
			(assign, ":num_inactive", 0),
			(try_for_range, ":other_lord", lords_begin, lords_end),
			   (store_troop_faction, ":other_lord_faction", ":other_lord"),
			   (this_or_next|eq, ":other_lord_faction", "fac_player_supporters_faction"),
				(eq, ":other_lord_faction", "$players_kingdom"),
			   (troop_slot_eq, ":other_lord", slot_troop_occupation, slto_inactive),
			   (val_add, ":num_inactive", 1),
			(try_end),
			(gt, ":num_inactive", 1),
			(try_begin),
				(ge, "$cheat_mode", 1),
				(assign, reg0, ":num_inactive"),
				(display_message, "@{!}DEBUG - Not returning a lord to the player's kingdom, since there are already {reg0} lords waiting for their petitions to be heard."),
			(try_end),
		 (else_try),
			(call_script, "script_dplmc_lord_return_from_exile", ":chosen_lord", ":new_faction"),
		 (try_end),
		(try_end),
	(try_end),
	##More piggybacking
	##
	(assign, reg0, ":save_reg0"),
	(assign, reg1, ":save_reg1"),
	(assign, reg4, ":save_reg4"),
	##nested diplomacy end+
    (is_between, "$g_player_affiliated_troop", lords_begin, kingdom_ladies_end),
	##nested diplomacy start+
	(assign, ":best_relation", -101),
	(assign, ":worst_relation", 101),

	(assign, ":num_at_least_20", 0),
	(assign, ":num_below_0", 0),

	(assign, ":good_relation", 0),
	##nested diplomacy end+

    (assign, ":bad_relation", 0),
    (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
      (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
      (gt, reg0, 0),
      (call_script, "script_troop_get_player_relation", ":family_member"),
	  ##nested diplomacy start+
	  #(le, reg0, -20),
	  #(assign, ":bad_relation", ":family_member"),
  	  (try_begin),
		(lt, reg0, 0),
		(val_add, ":num_below_0", 1),
		(le, reg0, ":worst_relation"),
		(assign, ":bad_relation", ":family_member"),
	  (else_try),
		(ge, reg0, 20),
		(val_add, ":num_at_least_20", 1),
		(gt, reg0, ":best_relation"),
		(assign, ":good_relation", ":family_member"),
	  (try_end),

	  (val_max, ":best_relation", reg0),
	  (val_min, ":worst_relation", reg0),
	  ##nested diplomacy end+
    (try_end),
	##nested diplomacy start+
	(try_begin),
		(gt, ":worst_relation", -15),
		(assign, ":bad_relation", 0),#suppress with no message
	(else_try),
		(gt, ":worst_relation", -20),
		(str_store_troop_name, s0, ":bad_relation"),
		(display_message, "@{s0} is grumbling against you.  Your affiliation could be jeopardized if this continues."),
		(str_clear, s0),
	(else_try),
		(neq, ":bad_relation", 0),
		(ge, ":num_at_least_20", ":num_below_0"),
		(store_add, reg0, ":worst_relation", ":best_relation"),
		(ge, reg0, 0),
		(str_store_troop_name, s0, ":bad_relation"),
		(str_store_troop_name, s1, ":good_relation"),
		(display_message, "@{s0} is grumbling against you, but with {s1}'s support you remain affiliated for now."),
		(str_clear, s0),
		(str_clear, s1),
		(assign, ":bad_relation", 0),
	(try_end),
	##nested diplomacy end+
    (try_begin),
      (eq, ":bad_relation", 0),

      (try_for_range, ":family_member", lords_begin, kingdom_ladies_end),
        (call_script, "script_dplmc_is_affiliated_family_member", ":family_member"),
        (gt, reg0, 0),
        (try_begin),
           (troop_slot_ge, ":family_member", slot_troop_prisoner_of_party, 0),
           ##diplomacy start+ skip relationship decay for imprisonment when the player himself is imprisoned or wounded
           (neg|troop_slot_ge, "trp_player", slot_troop_prisoner_of_party, 1),
           (neg|troop_is_wounded, "trp_player"),
           ##diplomacy end+
           (call_script, "script_change_player_relation_with_troop", ":family_member", -1),
        (else_try),
          (call_script, "script_change_player_relation_with_troop", ":family_member", 1),
        (try_end),
      (try_end),
    (else_try),
      (call_script, "script_add_notification_menu", "mnu_dplmc_affiliate_end", ":bad_relation", 0),
      (call_script, "script_dplmc_affiliate_end", 1),
    (try_end),
    ##nested diplomacy start+
 	 (assign, reg0, ":save_reg0"),
	 (assign, reg1, ":save_reg1"),
	 (assign, reg4, ":save_reg4"),
    ##nested diplomacy end+
    ]),

   (2,
   [
    (assign, ":has_walled_center", 0),
    (assign, ":has_fief", 0),
    (try_for_range, ":center_no", centers_begin, centers_end),
      (party_get_slot,  ":lord_troop_id", ":center_no", slot_town_lord),
      (eq, ":lord_troop_id", "trp_player"),
      (try_begin),
        (is_between, ":center_no", walled_centers_begin, walled_centers_end),
        (assign, ":has_walled_center", 1),
      (try_end),
      (assign, ":has_fief", 1),
    (try_end),

    (try_begin),
      (eq, ":has_walled_center", 0),
      (this_or_next|neq, "$g_player_constable", 0),
      (neq, "$g_player_chancellor", 0),
      (assign, "$g_player_constable", 0),
      (assign, "$g_player_chancellor", 0),
    (try_end),

    (try_begin),
      (eq, ":has_fief", 0),
      (neq, "$g_player_chamberlain", 0),
      (assign, "$g_player_chamberlain", 0),

      ##nested diplomacy start+
      #Adjust gold loss by difficulty
      (assign, ":save_reg0", reg0),
      (assign, ":save_reg1", reg1),

      (assign, ":loss_numerator", 2),
      (assign, ":loss_denominator", 3),

      (game_get_reduce_campaign_ai, ":reduce_campaign_ai"),
      (try_begin),
         (eq, ":reduce_campaign_ai", 0), #hard, lose 5/6
	 (assign, ":loss_numerator", 5),
	 (assign, ":loss_denominator", 6),
      (else_try),
         (eq, ":reduce_campaign_ai", 1), #medium, lose 2/3
	 (assign, ":loss_numerator", 2),
	 (assign, ":loss_denominator", 3),
      (else_try),
         (eq, ":reduce_campaign_ai", 2), #easy, lose 1/2
	 (assign, ":loss_numerator", 1),
	 (assign, ":loss_denominator", 2),
      (try_end),

      (store_troop_gold, ":cur_gold", "trp_household_possessions"),
      (try_begin),
        (gt, ":cur_gold", 0),
        #(call_script, "script_dplmc_withdraw_from_treasury", ":cur_gold"),
        #(val_div, ":cur_gold", 3),
        #(call_script, "script_troop_add_gold", "trp_player", ":cur_gold"),
        #(display_message, "@Your last fief was captured and you lost 2/3 of your treasury"),
	(store_mul, ":lost_gold", ":cur_gold", ":loss_numerator"),
	(val_div, ":lost_gold", ":loss_denominator"),
	(val_mul, ":lost_gold", -1),
	(call_script, "script_dplmc_withdraw_from_treasury", ":lost_gold"),
	(assign, reg0, ":loss_numerator"),
	(assign, reg1, ":loss_denominator"),
	(display_message, "@Your last fief was captured and you lost {reg0}/{reg1} of your treasury"),
      (try_end),

      (assign, reg0, ":save_reg0"),
      (assign, reg1, ":save_reg1"),
      ##nested diplomacy end+
    (try_end),
    ]),

   (24,
   [
      (try_for_range, ":faction1", npc_kingdoms_begin, npc_kingdoms_end),
        (assign, ":attitude_change", 2), #positive means good attitude
        (try_for_range, ":faction2", kingdoms_begin, kingdoms_end),
          (neq, ":faction1", ":faction2"),
		  ##diplomacy start+
		  #FIX: Stop the attitude change from carrying over from the previous kingdom!
		  (assign, ":attitude_change", 2),
		  #Handling for fac_player_supporters_faction & players_kingdom
		  (assign, ":alt_faction", ":faction2"),
		  (try_begin),
		     (eq, ":faction2", "fac_player_supporters_faction"),
			 (neq, ":faction1", "$players_kingdom"),
			 (assign, ":alt_faction", "$players_kingdom"),
		  (else_try),
		     (eq, ":faction2", "$players_kingdom"),
			 (assign, ":alt_faction", "fac_player_supporters_faction"),
		  (try_end),
		  ##Make loop less wasteful.
		  ##OLD:
          #(try_for_parties, ":party"),
          #  (is_between, ":party", centers_begin, centers_end),
		  ##NEW:
		  (try_for_range, ":party", centers_begin, centers_end),
		  ##diplomacy end+
            (store_faction_of_party, ":party_faction", ":party"),
			##diplomacy start+
			##FIX broken slot check!
			##ADD support for player's faction
			##OLD:
            #(eq, ":party_faction", ":faction2"),
            #(party_slot_eq, ":faction1", ":party", slot_center_original_faction),
			##NEW:
			(this_or_next|eq, ":party_faction", ":faction2"),
				(eq, ":party_faction", ":alt_faction"),
			(party_slot_eq, ":party", slot_center_original_faction, ":faction1"),
			#Don't subtract relation when it would be nonsensical
			(this_or_next|neq, ":faction1", "$players_kingdom"),
			(this_or_next|neq, ":faction2", "fac_player_supporters_faction"),
				(party_slot_ge, ":party", dplmc_slot_center_original_lord, 1),
			##diplomacy end+
            (val_sub, ":attitude_change", 1), #less attitude
          (try_end),

          (try_for_range, ":faction3", kingdoms_begin, kingdoms_end),
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction2", ":faction3"),
            (eq, reg0, -2), #war between 2 and 3
            (call_script, "script_diplomacy_faction_get_diplomatic_status_with_faction", ":faction1", ":faction3"),
            (eq, reg0, -2), #war between 1 and 3
            (val_add, ":attitude_change", 1), #higher attitude
          (try_end),
        (try_end),

        (store_add, ":faction1_to_faction2_slot", ":faction2", dplmc_slot_faction_attitude_begin),
        (party_set_slot, ":faction1", ":faction1_to_faction2_slot", ":attitude_change"),
      (try_end),
    ]),
  ##diplomacy end

################################################################################  
#CC-C begin
################################################################################
   # Add CC-C Give some xp to hero parties
   #party_reinforcements
   #(24,
   #[
       #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         #(troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         #(store_troop_faction, ":cur_troop_faction", ":troop_no"),
         #(neq, ":cur_troop_faction", "$players_kingdom"),
         #(troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
         #(gt, ":hero_party", centers_end),
         #(party_is_active, ":hero_party"),
         
         #get party size
         #(party_get_num_companions, ":party_size", ":hero_party"),
         #(call_script, "script_party_get_ideal_size", ":hero_party"),
         #(assign, ":ideal_size", reg0),

         #sub 15
         #(val_sub, ":ideal_size", 15),
         #(try_begin),
           #(ge,":ideal_size", ":party_size"),
           #(call_script, "script_ccc_party_reinforcements", ":hero_party", ":cur_troop_faction"),
           #(assign,reg0,":hero_party"),
           #(assign,reg1,":ideal_size"),
           #(assign,reg2,":party_size"),
           #(display_message,"@DEBUG add party={reg0} ideal={reg1} size={reg2}"),
         #(try_end),
         
         #(party_upgrade_with_xp, ":hero_party", 1000),
       #(try_end),
   #]),

   #mine 
   (40,
   [
      (try_begin),
        (ge,"$g_ccc_rhodoks_mine_flag",1),

        #
        (call_script, "script_troop_add_gold", "trp_ccc_cave_mineworker_leader", 500),
        #sort
        (call_script, "script_sort_party_by_troop_level", "p_ccc_mineworker_party", 0),
        #training mineworker
        (store_skill_level, ":trainer_skill_level", "skl_trainer", "trp_ccc_cave_mineworker_leader"),
        (store_mul,":xp_gain",":trainer_skill_level", 2000),
        (party_upgrade_with_xp, "p_ccc_mineworker_party", ":xp_gain", 0),
        
        (call_script, "script_ccc_cave_mine_info", "p_ccc_mineworker_party","trp_ccc_cave_mineworker_leader"),
        (assign,":worker",reg0),
        (assign,":good_w",reg1),
        (assign,":slacker_w",reg2),
        (assign,":total",reg3),

        #set point
        (assign,":point",0),
        (store_mul,":add_point",":worker",105),
        (val_add,":point",":add_point"),
        
        (store_mul,":add_point",":good_w",135),
        (val_add,":point",":add_point"),
        
        (store_mul,":add_point",":slacker_w",20),
        (val_add,":point",":add_point"),

        # 4 try to get iron 3->4
		# occc +  stone occc_stone
        (store_div,":iron_point",":point",250),
        (val_min,":iron_point",80),
        (try_for_range, ":unused", 0, 4),
          (store_random_in_range, ":r", 0, 100),
          (try_begin),
            (le,":r",":iron_point"),
			(store_random_in_range, ":r", 0, 100),
			(try_begin),
				(le,":r",60),
				(troop_add_item,"trp_ccc_cave_mineworker_leader","itm_iron",0),
			(else_try),
				(troop_add_item,"trp_ccc_cave_mineworker_leader","itm_occc_stone",0),
			(try_end),
          (try_end),
        (try_end),
        
        # 1 try to get relics
        (store_mul,":add_point",":good_w",100),
        (val_add,":point",":add_point"),

        (store_div,":relics_point",":point",1500),
        (val_min,":relics_point",30),
        (try_for_range, ":unused", 0, 1),
          (store_random_in_range, ":r", 0, 100),
          (try_begin),
            (le,":r",":relics_point"),
            (store_random_in_range, ":r", 0, 7),
            (try_begin),
                         (eq,":r",0),(assign,":get_item","itm_ccc_healing_wine"),
              (else_try),(eq,":r",1),(assign,":get_item","itm_ccc_relics_golden_pistol"),
              (else_try),(eq,":r",2),(assign,":get_item","itm_ccc_relics_1"),
              (else_try),(eq,":r",3),(assign,":get_item","itm_ccc_relics_2"),
              (else_try),(eq,":r",4),(assign,":get_item","itm_ccc_relics_3"),
              (else_try),(eq,":r",5),(assign,":get_item","itm_ccc_relics_4"),
              (else_try),(eq,":r",6),(assign,":get_item","itm_ccc_relics_1"),
              (else_try),(eq,":r",7),(assign,":get_item","itm_ccc_relics_2"),
            (try_end),
            (troop_add_item,"trp_ccc_cave_mineworker_leader",":get_item",0),
          (try_end),
        (try_end),
        
        #stone
        (call_script, "script_ccc_get_stone","trp_ccc_cave_mineworker_leader",12),

        (troop_sort_inventory,"trp_ccc_cave_mineworker_leader"),
        
        #add slacker
        (assign,":total_div", 0),
        (store_random_in_range, ":add_slacker", 0, 3),
        (party_get_num_companion_stacks, ":num_stacks", "p_ccc_mineworker_party"),
        (try_begin),
          (gt, ":add_slacker", 0),
          (gt, ":num_stacks", 0),
          (store_div,":total_div",":total",4),
          (lt,":slacker_w",":total_div"),
          (try_for_range, ":stack_iterator", 0, ":num_stacks"),
            (party_stack_get_troop_id, ":troop_id", "p_ccc_mineworker_party", ":stack_iterator"),
            (party_stack_get_size, ":troop_num", "p_ccc_mineworker_party", ":stack_iterator"),
            
            (try_begin),
              (eq, ":troop_id","trp_ccc_cave_mineworker"),
              (ge, ":troop_num",":add_slacker"),
              (party_remove_members,"p_ccc_mineworker_party","trp_ccc_cave_mineworker",":add_slacker"),
              (party_add_members,"p_ccc_mineworker_party","trp_ccc_cave_slacker_mineworker",":add_slacker"),
              (else_try),
              (eq, ":troop_id","trp_ccc_cave_mineworker"),
              (ge, ":troop_num",1),
              (store_random_in_range, ":r", 0, 4),
              (eq,":r", 0),
              (party_remove_members,"p_ccc_mineworker_party","trp_ccc_cave_good_mineworker",1),
              (party_add_members,"p_ccc_mineworker_party","trp_ccc_cave_slacker_mineworker",1),
            (try_end),
          (try_end),
        (try_end),
        
      (try_end),
   ]),
   
##CC-D begin: cave09 del but keep
   #bandit
   (8,  ## CC-D 5->8
   [
      ## CC-D begin: adjust option the amount of bandits
      (try_begin),
        (eq, "$g_ccd_option_spawn_bandit", 1),
        
        #south
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_south_spawn_point","pt_ccc_south_bandit_party",4),  ## 40->24->4
        (try_begin),
          (gt,reg0, 0),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq,":r", 0),
            (call_script, "script_ccc_make_custom_bandits_party",reg0,1),
            (else_try),
            (call_script, "script_ccc_make_random_bandits_party",reg0,1),
          (try_end),
        (try_end),
        
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_swadia_point","pt_occc_roaming_looter_party",5),  ## CC-D 40->25->5
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_swadia_point","pt_occc_roaming_knights_party",2),#occc
		#occc mountain bandits begin
		  (try_begin),#medieval options
			(eq,"$g_occc_make_factions_medieval",1),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_rhodoks_point","pt_mountain_bandits_classic",6),  ## CC-D 40->25->6
		  (else_try),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_rhodoks_point","pt_mountain_bandits",6),  ## CC-D 40->25->6
		  (try_end),
		#occc mountain bandits end
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_nords_point","pt_sea_raiders",6),  ## CC-D 40->25->6
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_khergit_point","pt_steppe_bandits",6),  ## CC-D 40->25->6
		#occc taiga bandits begin
		  (try_begin),#medieval options
			(this_or_next|eq,"$g_occc_make_factions_medieval",3),
			(eq,"$g_occc_make_factions_medieval",1),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_vaegirs_point","pt_taiga_bandits_classic",6),
		  (else_try),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_vaegirs_point","pt_taiga_bandits",6),## CC-D 40->25->6
		  (try_end),
		#occc taiga bandits end
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_sultanate_point","pt_desert_bandits",6),  ## CC-D 40->25->6
        (call_script,"script_ccc_spawn_bandits","p_albion_bandit_spawn_point","pt_forest_bandits",4),  ## occc
        (call_script,"script_ccc_spawn_bandits","p_amazons_spawn_point","pt_occc_amazon_bandit",4),  ## occc amazons
        (call_script,"script_ccc_spawn_bandits","p_sea_raider_ship_spawn_point","pt_sea_raiders",2),  ## occc
        ## CC-D begin: bandit hero calls extra spawn
        (try_begin),
          (eq, "$g_add_bandit_heroes", 1),
          (try_for_range, ":pt_no", bandit_party_template_begin, bandit_party_template_end),
            (party_template_slot_eq, ":pt_no", slot_party_template_has_hero, 1),
            (try_begin),
              (eq, ":pt_no", "pt_forest_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_swadia_point", "pt_forest_bandits", 8),  ## CC-D 30->8
            (else_try),
              (eq, ":pt_no", "pt_mountain_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_rhodoks_point", "pt_mountain_bandits",8),  ## CC-D 30->8
            (else_try),
              (eq, ":pt_no", "pt_sea_raiders"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_nords_point", "pt_sea_raiders",8),  ## CC-D 30->8
            (else_try),
              (eq, ":pt_no", "pt_steppe_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_khergit_point", "pt_steppe_bandits",8),  ## CC-D 30->8
            (else_try),
              (eq, ":pt_no", "pt_taiga_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_vaegirs_point", "pt_taiga_bandits",8),  ## CC-D 30->8
            (else_try),
              (eq, ":pt_no", "pt_desert_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_sultanate_point", "pt_desert_bandits",8),  ## CC-D 30->8
            (try_end),
          (try_end),
        (try_end),
        ## CC-D end
        
      (else_try),
        (eq, "$g_ccd_option_spawn_bandit", 2),
        
        #south
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_south_spawn_point","pt_ccc_south_bandit_party",24),  ## CC-D 40->24
        (try_begin),
          (gt,reg0, 0),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq,":r", 0),
            (call_script, "script_ccc_make_custom_bandits_party",reg0,1),
            (else_try),
            (call_script, "script_ccc_make_random_bandits_party",reg0,1),
          (try_end),
        (try_end),
		
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_swadia_point","pt_occc_roaming_looter_party",20),  ## CC-D 40->25->5
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_swadia_point","pt_occc_roaming_knights_party",5),#occc
        (call_script,"script_ccc_spawn_bandits","p_albion_bandit_spawn_point","pt_forest_bandits",25),  ## CC-D 40->25
		#occc mountain bandits begin
		  (try_begin),#medieval options
			(eq,"$g_occc_make_factions_medieval",1),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_rhodoks_point","pt_mountain_bandits_classic",25),  ## CC-D 40->25->6
		  (else_try),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_rhodoks_point","pt_mountain_bandits",25),  ## CC-D 40->25->6
		  (try_end),
		#occc mountain bandits end
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_nords_point","pt_sea_raiders",25),  ## CC-D 40->25
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_khergit_point","pt_steppe_bandits",25),  ## CC-D 40->25
		#occc taiga bandits begin
		  (try_begin),#medieval options
			(this_or_next|eq,"$g_occc_make_factions_medieval",3),
			(eq,"$g_occc_make_factions_medieval",1),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_vaegirs_point","pt_taiga_bandits_classic",25),
		  (else_try),
			(call_script,"script_ccc_spawn_bandits","p_ccc_cave_vaegirs_point","pt_taiga_bandits",25),## CC-D 40->25->6
		  (try_end),
		#occc taiga bandits end
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_sultanate_point","pt_desert_bandits",25),  ## CC-D 40->25
        (call_script,"script_ccc_spawn_bandits","p_amazons_spawn_point","pt_occc_amazon_bandit",10),  ## occc amazons
        (call_script,"script_ccc_spawn_bandits","p_sea_raider_ship_spawn_point","pt_sea_raiders",10),  ## occc
        ## CC-D begin: bandit hero calls extra spawn
        (try_begin),
          (eq, "$g_add_bandit_heroes", 1),
          (try_for_range, ":pt_no", bandit_party_template_begin, bandit_party_template_end),
            (party_template_slot_eq, ":pt_no", slot_party_template_has_hero, 1),
            (try_begin),
              (eq, ":pt_no", "pt_forest_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_swadia_point", "pt_forest_bandits", 30),
            (else_try),
              (eq, ":pt_no", "pt_mountain_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_rhodoks_point", "pt_mountain_bandits",30),
            (else_try),
              (eq, ":pt_no", "pt_sea_raiders"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_nords_point", "pt_sea_raiders",30),
            (else_try),
              (eq, ":pt_no", "pt_steppe_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_khergit_point", "pt_steppe_bandits",30),
            (else_try),
              (eq, ":pt_no", "pt_taiga_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_vaegirs_point", "pt_taiga_bandits",30),
            (else_try),
              (eq, ":pt_no", "pt_desert_bandits"),
              (call_script,"script_ccc_spawn_bandits", "p_ccc_cave_sultanate_point", "pt_desert_bandits",30),
            (try_end),
          (try_end),
        (try_end),
        ## CC-D end
        
      (try_end),
      ## CC-D end
    ]),
    
    (20,  ## CC-D 15->20
    [
      ## CC-D begin: adjust option the amount of bandits
      (try_begin),
        (eq, "$g_ccd_option_spawn_bandit", 1),
        
        #north
        (call_script, "script_ccc_spawn_bandits","p_ccc_cave_north_spawn_point","pt_ccc_north_bandit_party",3),  ## CC-D 30->16->3
        (try_begin),
          (gt,reg0, 0),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq,":r", 0),
            (call_script, "script_ccc_make_custom_bandits_party",reg0,2),
            (else_try),
            (call_script, "script_ccc_make_random_bandits_party",reg0,2),
          (try_end),
        (try_end),
        
        #dark
        (call_script, "script_ccc_spawn_bandits","p_ccc_cave_dark_spawn_point","pt_ccc_dark_bandit_party",2),  ## CC-D 14->8->2
        (try_begin),
          (gt,reg0, 0),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq,":r", 0),
            (call_script, "script_ccc_make_custom_bandits_party",reg0,3),
            (else_try),
            (call_script, "script_ccc_make_random_bandits_party",reg0,3),
          (try_end),
        (try_end),#
        
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_khergit_point","pt_black_khergit_raiders",2),  ## CC-D 3->2
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_vaegirs_point","pt_dark_hunters",2),  ## CC-D 3->2
        
      (else_try),
        (eq, "$g_ccd_option_spawn_bandit", 2),
        
        #north
        (call_script, "script_ccc_spawn_bandits","p_ccc_cave_north_spawn_point","pt_ccc_north_bandit_party",16),  ## CC-D 30->16
        (try_begin),
          (gt,reg0, 0),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq,":r", 0),
            (call_script, "script_ccc_make_custom_bandits_party",reg0,2),
            (else_try),
            (call_script, "script_ccc_make_random_bandits_party",reg0,2),
          (try_end),
        (try_end),
        
        #dark
        (call_script, "script_ccc_spawn_bandits","p_ccc_cave_dark_spawn_point","pt_ccc_dark_bandit_party",8),  ## CC-D 14->8
        (try_begin),
          (gt,reg0, 0),
          (store_random_in_range, ":r", 0, 7),
          (try_begin),
            (eq,":r", 0),
            (call_script, "script_ccc_make_custom_bandits_party",reg0,3),
            (else_try),
            (call_script, "script_ccc_make_random_bandits_party",reg0,3),
          (try_end),
        (try_end),
        
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_khergit_point","pt_black_khergit_bandits",3),
        (call_script,"script_ccc_spawn_bandits","p_ccc_cave_vaegirs_point","pt_dark_hunters",3),
        
      (try_end),
      ## CC-D end
    ]),
    
    (71,#additional sub faction troops
    [
	
		#occc nazizombies
		(call_script, "script_ccc_spawn_bandits","p_ccc_cave_kulum_spawn_point","pt_occc_nazi_party",2),
		(try_begin),
		(eq,"$g_occc_additional_subfactions",1),

		
		#occc swadian crusaders
		(store_faction_of_party, ":townfactcheck", "p_town_6"),#praven
		(try_begin),
			(eq, ":townfactcheck", "fac_kingdom_1"),
			(call_script, "script_occc_factional_roaming_party","p_town_6","pt_occc_army_of_the_night","fac_kingdom_1",1),  
		(try_end),#p_town_7 
		
		#occc jomsviking
		(try_begin),
			(call_script, "script_occc_factional_roaming_party","p_occc_jomsborg","pt_occc_jomsviking_raidparty","fac_jomsvikings",3),
			(neq,reg0,0),
			(party_add_leader,reg0,"trp_occc_nord_joms_hersir"),
		(try_end),
		#(call_script, "script_occc_factional_roaming_party","p_jomsviking_ship_spawn_point","pt_occc_jomsviking_raidship","fac_jomsvikings",1),#test trp_occc_nord_joms_hersir
			
		#occc slavers 
		(call_script, "script_occc_factional_roaming_party","p_occc_slaver_camp","pt_occc_slaver_party","fac_slavers",3),
		
		#occc calrador elves
		(call_script, "script_occc_factional_roaming_party","p_calrador_spawn_point","pt_occc_calrador_rangers","fac_calrador",2),

		#occc kara=khergits 
		
		(call_script, "script_occc_factional_roaming_party","p_ccc_cave_dark_knight_point","pt_black_khergit_raiders","fac_black_khergits",2),
		(store_random_in_range, ":r", 0, 10),
		(try_begin),
			(lt, ":r", 2),
			(call_script, "script_occc_factional_roaming_party","p_ccc_cave_dark_knight_point","pt_black_khergit_warband","fac_black_khergits",2),
		(try_end),

		#occc highlanders
		(store_faction_of_party, ":townfactcheck", "p_village_205"),
		(try_begin),
			(this_or_next|eq, ":townfactcheck", "fac_kingdom_4"),
			(eq, ":townfactcheck", "fac_kingdom_14"),
			(call_script, "script_occc_factional_roaming_party","p_village_205","pt_occc_highlander_party",":townfactcheck",1),  
			(gt,reg0,0),
			(store_random_in_range, ":r", 0, 10),
			(lt, ":r", 3),
			(party_add_leader,reg0,"trp_occc_highlander_eternal_champion"),#joke
		(try_end), 

		#occc ghazis
		(store_random_in_range, ":r", 0, 34),
		(store_faction_of_party, ":townfactcheck", "p_town_20"),#droquba
		(try_begin),
			(lt, ":r", 3),
			(eq, ":townfactcheck", "fac_kingdom_6"),
			(eq, "$g_occc_religionsystem", 1),

			(call_script, "script_occc_factional_roaming_party","p_town_20","pt_occc_jihadists","fac_crescent_ghazis",1),  
		(try_end),
		
		#occc valkyries
		(try_begin),
			(eq,"$g_occc_make_factions_medieval",1),#CtA like
			(call_script, "script_occc_factional_roaming_party","p_valkyries_spawn_point","pt_occc_valkyries","fac_valhalla",1),
		(try_end),

		#occc Borchas
		(try_begin),
			(eq,"$g_occc_make_factions_medieval",1),#CtA like
			(call_script, "script_occc_factional_roaming_party","p_borcha_legion_spawn_point","pt_occc_borcha_legion","fac_valhalla",1),
		(try_end),

		
		#occc order knights
		(try_begin),
			(eq,"$g_occc_make_factions_medieval",1),#CtA like
			(store_random_in_range,":spawn_point",towns_begin,towns_end), 
			(store_faction_of_party, ":townfactcheck", ":spawn_point"),
			(neq, ":townfactcheck", "fac_kingdom_6"),
			(call_script, "script_occc_factional_roaming_party",":spawn_point","pt_occc_holy_crusaders","fac_holy_crusaders",4),
		(try_end),
		
		#occc Wardogs
		(try_begin),
			(eq,"$g_occc_make_factions_medieval",1),#CtA like?
			(call_script, "script_occc_factional_roaming_party","p_wardogs_spawn_point","pt_occc_wardogs","fac_manhunters",2),
			(party_add_leader,reg0,"trp_occc_wardog_chef"),
		(else_try),
			(store_faction_of_party, ":townfactcheck", "p_town_26"),#nuovo zendar
			(eq, ":townfactcheck", "fac_kingdom_11"),#zendar rhodok
			(call_script, "script_occc_factional_roaming_party","p_town_26","pt_occc_wardogs","fac_kingdom_11",1),
			(party_add_leader,reg0,"trp_occc_wardog_chef"),
		(try_end),

		#occc undead legio
		(try_begin),
			(eq,"$g_occc_make_factions_medieval",1),#CtA like
			(call_script, "script_occc_factional_roaming_party","p_undead_legio_spawn_point","pt_occc_undead_legion_centuria","fac_revenants",4),
			(neq,reg0,0),
			(party_add_leader,reg0,"trp_occc_undead_centurion"),
		(try_end),

		(try_begin),
		(gt, "$g_ccd_option_spawn_bandit", 0),
		(store_random_in_range, ":r", 0, 100),
			(try_begin),
				(lt, ":r", 10),
				(store_random_in_range, ":r", "p_town_1", "p_town_29"),
				(call_script, "script_ccc_spawn_bandits",":r","pt_occc_mercenary_bandits_warband",2),
				(try_begin),
					(gt,reg0, 0),
					(call_script, "script_ccc_make_custom_bandits_party",reg0,11),
					(str_store_party_name,s1,":r"),
					(display_message, "@You heard jobless Mercenaries started to raid near {s1}", 0xffffff), #
				(try_end),

			(try_end),
		(try_end),

		
		#factional roamers?
		
		#occc imperial legion
		#(store_faction_of_party, ":townfactcheck", "p_town_6"),#Jelkala
		#(try_begin),
		#    (eq, ":townfactcheck", "fac_kingdom_5"),
		#    (call_script, "script_occc_factional_roaming_party","p_town_5","pt_occc_imperial_legion","fac_kingdom_5",2),  ## CC-D 3->1
		#(try_end),

		
		#pop sub-faction groups
		(call_script, "script_occc_factional_roaming_party","p_village_66","pt_occc_riurik_survivors_clan","fac_riurik_clan",1),#test riuriks fisdnar


	(try_end),#p_town_7 
	
		#occc taikou scouter Army
		(store_random_in_range, ":r", 0, 10),
		(try_begin),
			(lt, ":r", 3),
			(eq, "$g_occc_risingsun_invasion", 1),
			(eq, "$occc_risingsun_conquering_process", 1),
			(call_script, "script_occc_factional_roaming_party","p_taikou_scout_spawn_point","pt_occc_taikou_scoutarmy","fac_taikou_scouts",1),
		(try_end),
	#occc end
	
      ## CC-D begin: adjust option the amount of bandits
      (try_begin),
        (eq, "$g_ccd_option_spawn_bandit", 1),
        
        #odasan
        (call_script, "script_ccc_spawn_bandits","p_ccc_cave_odasan_spawn_point","pt_ccc_odasan_bandit_party",1),  ## CC-D 3->1
        (try_begin),
          (gt,reg0, 0),
          (call_script, "script_ccc_make_custom_bandits_party",reg0,4),
        (try_end),
        
      (else_try),
        (eq, "$g_ccd_option_spawn_bandit", 2),
        
      #odasan
      (call_script, "script_ccc_spawn_bandits","p_ccc_cave_odasan_spawn_point","pt_ccc_odasan_bandit_party",3),
      (try_begin),
        (gt,reg0, 0),
        (call_script, "script_ccc_make_custom_bandits_party",reg0,4),
      (try_end),
      
      (try_end),
      (try_begin),
        (gt, "$g_ccd_option_spawn_bandit", 0),
      
        #kulum
        ## CC-D begin
        (try_begin),
          (eq, "$g_ccd_chaos_army", 0),
          (assign, "$g_ccd_chaos_army", 1),
        
        (call_script, "script_ccc_spawn_bandits","p_ccc_cave_kulum_spawn_point","pt_ccc_kuluma_bandit_party",1),
        (try_begin),
          (gt,reg0, 0),
          (call_script, "script_ccc_make_custom_bandits_party",reg0,5),
        (try_end),
        
        (else_try),
          (assign, "$g_ccd_chaos_army", 0),
          (call_script, "script_ccc_spawn_bandits","p_ccc_cave_kulum_spawn_point","pt_ccc_kuluma_bandit_party",1),
          (try_begin),
            (gt,reg0, 0),
            (call_script, "script_ccc_make_custom_bandits_party",reg0,6),
          (try_end),
        (try_end),
        ## CC-D end
      
      (try_end),
      ## CC-D end
      ## CC-D begin: extra raider
      (call_script, "script_ccd_spawn_qb_party", "trp_ccc_bandit_npc_1"),
      (call_script, "script_ccd_spawn_qb_party", "trp_ccc_bandit_npc_2"),
      (call_script, "script_ccd_spawn_qb_party", "trp_ccc_bandit_npc_7"),
      (call_script, "script_ccd_spawn_qb_party", "trp_ccc_bandit_npc_9"),
      (call_script, "script_ccd_spawn_qb_party", "trp_ccc_bandit_npc_10"),
      (call_script, "script_ccd_spawn_qb_party", "trp_quick_battle_troop_11"),
      (call_script, "script_ccd_spawn_qb_party", "trp_occc_bandit_stormtrooper"),
      ## CC-D end
    ]),
## CC-D end
    
    #hide house
    (24,
    [
       #set wedding
       (try_begin),
         (eq,"$g_ccc_wedding_stage",1),
         (assign,"$g_ccc_wedding_stage",2),
       (try_end),
       
       #party menber relation
       (set_show_messages, 0),
       (party_get_num_companion_stacks,":num_stacks", "p_main_party"),
       (try_begin),
         (gt, ":num_stacks", 0),
         (try_for_range, ":stack_iterator", 0, ":num_stacks"),
           (party_stack_get_troop_id,":troop_id", "p_main_party", ":stack_iterator"),
           (gt,":troop_id",0),
           (troop_is_hero,":troop_id"),
           (store_random_in_range, ":r", 0, 7),
           (try_begin),
             (le,":r",1),
             (call_script, "script_troop_change_relation_with_troop", ":troop_id", "trp_player", 1),
           (else_try),
             (eq,":r",6),
             (call_script, "script_troop_change_relation_with_troop", ":troop_id", "trp_player", -1),
           (try_end),
         (try_end),
       (try_end),
       (set_show_messages, 1),
       
       #child
       (try_begin),
        (eq,"$g_child_stage",3),
        (gt,"$g_get_child_day",0),
        (gt,"$g_ccc_wife_troop_no",0),
        (val_sub,"$g_get_child_day",1),
        (le,"$g_get_child_day",1),
        (assign,"$g_child_stage",4),
       (try_end),
    ]),
    
    #ero power and submit
    (24,
    [
      (try_for_range, ":troop_no", active_npcs_begin, kingdom_ladies_end),
        #sex?
        (try_begin),
          (call_script,"script_ccc_check_troop_in_prisoners","p_ccc_hide_house",":troop_no"),
          (gt,reg0,0),
          (troop_get_slot, ":prison_day",":troop_no",slot_troop_days_in_prison),
          (val_add,":prison_day",1),
          (troop_set_slot,":troop_no",slot_troop_days_in_prison,":prison_day"),
          (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party,"p_ccc_hide_house"),
          (troop_set_slot, ":troop_no", slot_troop_cur_center, "p_ccc_hide_house"),
        (else_try),
          (neg|troop_slot_eq,":troop_no",slot_troop_eros_power,-1),
          (neg|troop_slot_eq,":troop_no",slot_troop_cur_center, "p_main_party"),
          (troop_get_slot,":ero",":troop_no",slot_troop_eros_power),
          (store_random_in_range, ":r", -2, 1),
          (val_add,":ero",":r"),
          (val_max,":ero",1),
          (troop_set_slot,":troop_no",slot_troop_eros_power,":ero"),
        (try_end),
        
        #Submit down
        (try_begin),
          (neg|troop_slot_eq,":troop_no",slot_troop_prisoner_of_party, "p_ccc_hide_house"),
          (troop_get_slot,":submit",":troop_no",slot_troop_submit),
          (try_begin),
            (gt,":submit",0),
            (store_random_in_range,":down",1,4),
            (val_sub,":submit",":down"),
            (troop_set_slot,":troop_no",slot_troop_submit, ":submit"),
          (try_end),
        (try_end),
      (try_end),
    ]),
    
    #runaway
    (50,
    [
       (party_get_num_prisoner_stacks, ":num_stacks", "p_main_party"),
       (assign,"$g_ccc_runaway_troop",0),
       (assign,"$g_ccc_runaway_stage",0),
       (assign,"$g_ccc_duel_result",0),

       (try_begin),
         (gt, ":num_stacks", 0),
         (try_for_range, ":stack_iterator", 0, ":num_stacks"),
           (party_prisoner_stack_get_troop_id, ":troop_no", "p_main_party", ":stack_iterator"),
           (troop_set_slot,":troop_no",slot_troop_prisoner_of_party, "p_main_party"),
           (troop_is_hero,":troop_no"),
           (store_random_in_range, ":run", 0, 14),
           (try_begin),
             (eq,":run",0),
             (assign,"$g_ccc_runaway_troop",":troop_no"),
             (assign,"$g_ccc_runaway_stage",1),
             (jump_to_menu,"mnu_ccc_runaway"),
           (try_end),
         (try_end),
       (try_end),
    ]),
    
    #cherry bounus
    (24*52,
    [  
      (try_begin),
        (troop_slot_eq,"trp_player",slot_troop_eros_power,-1),
        (troop_get_slot,":age","trp_player",slot_troop_age),
        (troop_get_type,":type","trp_player"),
        (call_script,"script_ccc_get_ero_string","trp_player"),
        (try_begin),
          (eq,":type",0),
          (try_begin),
            (le,":age",30),
            (troop_raise_attribute,"trp_player",ca_strength,1),
            (display_message,"@{s0} Bounus STR+1",0x33ff33),
          (else_try),
            (troop_raise_attribute,"trp_player",ca_intelligence,1),
            (display_message,"@{s0} Bounus INT+1",0x33ff33),
          (try_end),
          (play_sound, "snd_man_warcry"),
        (else_try),
          (eq,":type",1),
          (try_begin),
            (le,":age",30),
            (troop_raise_attribute,"trp_player",ca_charisma,1),
            (display_message,"@{s0} Bounus CHR+1",0x33ff33),
          (else_try),
            (troop_raise_attribute,"trp_player",ca_strength,1),
            (display_message,"@{s0} Bounus STR+1",0x33ff33),
          (try_end),
          (play_sound, "snd_woman_yell"),
        (try_end),
        
      (try_end),
    ]),
    
    #cherry check
    (12,
    [  
      (try_begin),
        (troop_slot_eq,"trp_player",slot_troop_eros_power,-1),
        (try_begin),
          (troop_slot_ge,"trp_player", slot_troop_spouse,1),
          (store_random_in_range, ":ero", 1, 10),
          (troop_set_slot,"trp_player",slot_troop_eros_power,":ero"),
          (display_message,"@You lost chastity",0xB22222),
        (else_try),
          (eq, "$g_player_is_captive", 1),
		  (lt,"$g_work_for_village_ongoing",1),
          (store_random_in_range, ":r", 0, 100),
          (le,":r",25),
          (store_random_in_range, ":ero", 1, 10),
          (troop_set_slot,"trp_player",slot_troop_eros_power,":ero"),
          (display_message,"@You lost chastity",0xB22222),
          (call_script,"script_ccc_ero_sound_troop","trp_player"),
        (try_end),
      (try_end),
    ]),
    
   (6,
     [
       (try_for_range, ":troop_no", active_npcs_end, active_npcs_end),
         (neq,":troop_no","trp_player"),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
         (store_troop_faction,":faction_no",":troop_no"),
         (neq,":faction_no","fac_player_supporters_faction"),
         (ge, ":party_no", 1),
         (call_script, "script_process_ransom_for_party", ":party_no"),
         (assign, ":total_ransom_cost", reg0),
         (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
         (val_add, ":cur_wealth", ":total_ransom_cost"),
         (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
         (call_script, "script_process_outlaws_for_party", ":party_no"),
         (call_script, "script_update_troop_notes", ":troop_no"),
       (try_end),
       
       #walled centers
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
         (neq, ":town_lord", "trp_player"), #center does not belong to player.
         (ge, ":town_lord", 1), #center belongs to someone.
         (store_troop_faction,":faction_no",":town_lord"),
         (neq,":faction_no","fac_player_supporters_faction"),
         #(neg|is_between, ":town_lord", companions_begin, companions_end), # not companions
         (call_script, "script_process_ransom_for_party", ":center_no"),
         (assign, ":total_ransom_cost", reg0),
         (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
         (val_add, ":cur_wealth", ":total_ransom_cost"),
         (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
         (call_script, "script_process_outlaws_for_party", ":center_no"),
       (try_end),
     ]),
    
    #lords collect taxes
    (24*7,
    [
      #Increasing debts to heroes by 1% (once a week)
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (troop_get_slot, ":cur_debt", ":troop_no", slot_troop_player_debt),#Increasing debt
        (gt,":cur_debt",0),
        (val_mul, ":cur_debt", 101),
        (val_div, ":cur_debt", 100),
        (troop_set_slot, ":troop_no", slot_troop_player_debt, ":cur_debt"),
      (try_end),

      #system fix troop
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
        #report total_income_week
        (troop_set_slot, ":troop_no", slot_troop_total_income_week, ":cur_wealth"),
        
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neq,":troop_no","trp_player"),
        (assign, ":weekly_income", 700), #let every hero receive 750->700 denars by default

		(try_begin),#OCCC Sinan has an extra way to earn money(maybe assassination, hahaha) 
			(eq,":troop_no","trp_knight_6_zed"),
		    (assign, ":weekly_income", 20000),
		(else_try),
			(eq,":troop_no","trp_knight_4_cnut"),#dovahkiin
		    (assign, ":weekly_income", 5000),
		(else_try),#teutonic knights
			(this_or_next|eq,":troop_no","trp_additional_knight_ulrich"),
			(eq,":troop_no","trp_heinrich"),

		    (assign, ":weekly_income", 2400),

		(try_end),
		
		
        #level bounus
        (store_character_level, ":troop_level", ":troop_no"),
        (store_mul, ":level_income", ":troop_level", 10),
        (val_add, ":weekly_income", ":level_income"),
        
        #king bounus
        (store_troop_faction,":faction_no", ":troop_no"),
        (try_begin), #check if troop is kingdom leader
          (faction_slot_eq, ":faction_no", slot_faction_leader, ":troop_no"),
          (val_add, ":weekly_income", 30000),#20000->30000
          (le,":cur_wealth",40000),
          (val_add, ":weekly_income", 40000),
        (try_end),
        
        #marshall bounus
        (try_begin), #check if troop is marshall
          (faction_slot_eq, ":faction_no", slot_faction_marshall, ":troop_no"),
          (val_add, ":weekly_income", 3000),
        (try_end),
        
        (val_add,":cur_wealth",":weekly_income"),
        (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
      (try_end),
      
      #system fix wall
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"),
        (party_slot_ge, ":center_no", slot_town_lord, 1),
        (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
        (store_mul, ":added_wealth", ":prosperity", 20), #15 -> 20
        (val_add, ":added_wealth", 700), 
        (try_begin),
          (party_slot_eq, ":center_no", slot_party_type, spt_town),
          (val_mul, ":added_wealth", 3),
          (val_div, ":added_wealth", 2),
        (try_end),
        (party_get_slot, ":cur_wealth", ":center_no", slot_town_wealth),
        (val_add,":cur_wealth",":added_wealth"),
        (party_set_slot, ":center_no", slot_town_wealth, ":cur_wealth"),
      (try_end),

	    #Collect taxes for another week
      (try_for_range, ":center_no", centers_begin, centers_end),
        (neg|party_slot_eq, ":center_no", slot_party_type, spt_castle),
        (try_begin),
          (party_slot_ge, ":center_no", slot_town_lord, 0), #unassigned centers do not accumulate rents	  
          (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),		  
          (assign, ":cur_rents", 0),
		  (assign, ":pop_bonus", 0),#occc
          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_village),
            (try_begin),
              (party_slot_eq, ":center_no", slot_village_state, svs_normal),
              (assign, ":cur_rents", 1600), #1200->1600 occc
			  
				(try_begin),#occc market
					(party_slot_eq, ":center_no", slot_center_has_market, 1),
					(val_add, ":cur_rents", 500),
				(try_end),#occc market end

            (try_end),
          (else_try),
            (party_slot_eq, ":center_no", slot_party_type, spt_castle),
            (assign, ":cur_rents", 2000),
          (else_try),  
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (assign, ":cur_rents", 2700), #2400->2700
			(party_get_slot, ":pop_bonus",":center_no", slot_center_population),#occc
          (try_end),
		
          (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity), #prosperty changes between 0..100     
          #(store_add, ":multiplier", 20, ":prosperity"), #multiplier changes between 20..120
          (store_mul, ":multiplier", ":prosperity",2),
		  
          (val_mul, ":cur_rents", ":multiplier"), 
		  #occc begin
          (store_sub, ":div", 210,":prosperity"),#Prosperity of 45 gives the default values 75
		  (val_max,":div",10),
		  #occc end
          (val_div, ":cur_rents", ":div"),#occc 120->:div
          
          (val_add, ":accumulated_rents", ":cur_rents"), #cur rents changes between 23..1000

		  #occc begin
		  (val_div, ":pop_bonus",5),#v0.2 10->5
          (val_add, ":accumulated_rents", ":pop_bonus"),
		  #occc end
          ##diplomacy begin
          (try_begin),
            (str_store_party_name, s6, ":center_no"),
             
            (party_get_slot, ":tax_rate", ":center_no", dplmc_slot_center_taxation),
            (neq, ":tax_rate", 0),
            (store_div, ":rent_change", ":accumulated_rents", 100),
            (val_mul, ":rent_change", ":tax_rate"),
   
            (try_begin), #debug
              (eq, "$cheat_mode", 1),
              (assign, reg0, ":tax_rate"),
              (display_message, "@{!}DEBUG : tax rate in {s6}: {reg0}"),
              (assign, reg0, ":accumulated_rents"),
              (display_message, "@{!}DEBUG : accumulated_rents  in {s6}: {reg0}"),
              (assign, reg0, ":rent_change"),
              (display_message, "@{!}DEBUG : rent_change in {s6}: {reg0}  in {s6}"),
            (try_end),          
  
            (val_add, ":accumulated_rents", ":rent_change"),
            
            (val_div, ":tax_rate", -25), #CC-C -25 0
            
            #CC-C begin
            #(assign,":add",":tax_rate"),
            #(val_min,":add",1),
            #(call_script, "script_change_center_prosperity", ":center_no", ":add"),
            #CC-C end
            
            (try_begin),
              (lt, ":tax_rate", 0), #double negative values
              (val_mul, ":tax_rate", 2),
              
              (try_begin), #debug
                (eq, "$cheat_mode", 1),
                (assign, reg0, ":tax_rate"),
                (display_message, "@{!}DEBUG : tax rate after modi in {s6}: {reg0}"),
              (try_end),
  
              (try_begin),
                (this_or_next|is_between, ":center_no", villages_begin, villages_end),
                (is_between, ":center_no", towns_begin, towns_end),
                (party_get_slot, ":center_relation", ":center_no", slot_center_player_relation),
  
                (try_begin), #debug
                  (eq, "$cheat_mode", 1),
                  (assign, reg0, ":center_relation"),
                  (display_message, "@{!}DEBUG : center relation: {reg0}"),
                (try_end),
              
                (le, ":center_relation", -5),
                (store_random_in_range, ":random",-100, 0),
                (gt, ":random", ":center_relation"),           
                
                (neg|party_slot_eq, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"),
                (display_message, "@Riot in {s6}!"),
                (party_set_slot, ":center_no", slot_village_infested_by_bandits, "trp_peasant_woman"), #trp_peasant_woman used to simulate riot
                (call_script, "script_change_center_prosperity", ":center_no", -1),     
                (call_script, "script_add_notification_menu", "mnu_dplmc_notification_riot", ":center_no", 0),         
  
                #add additional troops
                (store_character_level, ":player_level", "trp_player"),
                (store_div, ":player_leveld2", ":player_level", 2),
                (store_mul, ":player_levelx2", ":player_level", 2),
                (try_begin), 
                  (is_between, ":center_no", villages_begin, villages_end),       
                  (store_random_in_range, ":random",0, ":player_level"),
                  (party_add_members, ":center_no", "trp_mercenary_swordsman", ":random"),
                  (store_random_in_range, ":random", 0, ":player_leveld2"),
                  (party_add_members, ":center_no", "trp_hired_blade", ":random"),
                (else_try),
                  (party_set_banner_icon, ":center_no", 0),   
                  (party_get_num_companion_stacks, ":num_stacks",":center_no"),
                  (try_for_range, ":i_stack", 0, ":num_stacks"),
                    (party_stack_get_size, ":stack_size",":center_no",":i_stack"),                             
                    (val_div, ":stack_size", 2),
                    (party_stack_get_troop_id, ":troop_id", ":center_no", ":i_stack"),
                    (party_remove_members, ":center_no", ":troop_id", ":stack_size"),
                  (try_end),
                  (store_random_in_range, ":random",":player_leveld2", ":player_levelx2"),
                  (party_add_members, ":center_no", "trp_townsman", ":random"),
                  (store_random_in_range, ":random",0, ":player_level"),
                  (party_add_members, ":center_no", "trp_watchman", ":random"),
                (try_end),
              (end_try),     
            (try_end),
            (call_script, "script_change_player_relation_with_center", ":center_no", ":tax_rate"),
          (try_end),
          
          (try_begin), #no taxes for infested villages and towns 
            (party_slot_ge, ":center_no", slot_village_infested_by_bandits, 1),
            (assign,":accumulated_rents", 0),
          (try_end),
          ##diplomacy end

          (party_set_slot, ":center_no", slot_center_accumulated_rents, ":accumulated_rents"),
          
          #CC-C begin
          (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
		  #occc tweak mild mode
		  (try_begin),
		  (eq,"$g_occc_mildmode",0),
          (val_mul,":accumulated_tariffs",3),
		  (else_try),
          #(val_mul,":accumulated_tariffs",3),
		  (try_end),

          (party_set_slot, ":center_no", slot_center_accumulated_tariffs, ":accumulated_tariffs"),
          #CC-C end
        (try_end),
        
        #(try_begin),
          #(is_between, ":center_no", villages_begin, villages_end),
          #(party_get_slot, ":bound_castle", ":center_no", slot_village_bound_center),
          #(party_slot_ge, ":bound_castle", slot_town_lord, 0), #unassigned centers do not accumulate rents	  
          #(is_between, ":bound_castle", castles_begin, castles_end),
          #(party_get_slot, ":accumulated_rents", ":bound_castle", slot_center_accumulated_rents), #castle's accumulated rents
          #(val_add, ":accumulated_rents", ":cur_rents"), #add village's rent to castle rents
          #(party_set_slot, ":bound_castle", slot_center_accumulated_rents, ":accumulated_rents"),
        #(try_end),
      ## CC-D begin: castle income
      (else_try),
        (party_slot_eq, ":center_no", slot_party_type, spt_castle),
        
        (party_slot_ge, ":center_no", slot_town_lord, 0), #unassigned centers do not accumulate rents
        (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        (assign, ":cur_rents", 0),
        (assign, ":num_village", 0),
        (store_faction_of_party, ":center_faction", ":center_no"),
        (try_for_range, ":village_no", villages_begin, villages_end),
          (party_slot_eq, ":village_no", slot_village_bound_center, ":center_no"),
          (store_faction_of_party, ":village_faction", ":village_no"),
          (eq, ":village_faction", ":center_faction"),
          
          (neg|party_slot_ge, ":village_no", slot_village_infested_by_bandits, 1),
          (neg|party_slot_eq, ":village_no", slot_village_state, svs_being_raided),
          (neg|party_slot_eq, ":village_no", slot_village_state, svs_looted),
          
          (val_add, ":num_village", 1),
        (try_end),
        
        (store_mul, ":cur_rents", ":num_village", 600),#400->600 occc
        (val_add, ":accumulated_rents", ":cur_rents"),
        (party_set_slot, ":center_no", slot_center_accumulated_rents, ":accumulated_rents"),
      ## CC-D end
      (try_end),

      #auto taxes
      (try_for_range, ":center_no", centers_begin, centers_end),
        (party_get_slot, ":lord", ":center_no", slot_town_lord),
        #(try_begin),
          #(this_or_next|eq,":lord",-1),
          #(neg|troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),
          #(store_faction_of_party, ":cur_faction_no", ":center_no"),
          #(faction_get_slot, ":leader",":cur_faction_no", slot_faction_leader),
          #(assign,":lord",":leader"),
        #(try_end),
        (ge,":lord",0),
        (troop_slot_eq, ":lord", slot_troop_occupation, slto_kingdom_hero),        
        (party_get_slot, ":accumulated_rents", ":center_no", slot_center_accumulated_rents),
        (party_get_slot, ":accumulated_tariffs", ":center_no", slot_center_accumulated_tariffs),
        (party_get_slot, ":town_wealth", ":center_no", slot_town_wealth),
        
        (troop_get_slot, ":troop_wealth", ":lord", slot_troop_wealth),
        (val_add, ":troop_wealth", ":accumulated_rents"),
        (val_add, ":troop_wealth", ":accumulated_tariffs"),
        (val_add, ":troop_wealth", ":town_wealth"),
        
        #report 
        (val_add,":accumulated_rents",":town_wealth"),
        (party_set_slot, ":center_no", slot_center_accumulated_rents_week, ":accumulated_rents"),
        (party_set_slot, ":center_no", slot_center_accumulated_tariffs_week, ":accumulated_tariffs"),
        
        (neq,":lord","trp_player",),
        (troop_set_slot, ":lord", slot_troop_wealth, ":troop_wealth"),
        (party_set_slot, ":center_no", slot_center_accumulated_rents, 0),
        (party_set_slot, ":center_no", slot_center_accumulated_tariffs, 0),
        (party_set_slot, ":center_no", slot_town_wealth, 0),
      (try_end),
      
      #troop army cost imported from difor 0.058
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        #total_income_week
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
        (troop_get_slot, ":old_wealth",":troop_no", slot_troop_total_income_week),
        (store_sub,":troop_total_income_week",":cur_wealth",":old_wealth"),
        (troop_set_slot, ":troop_no", slot_troop_total_income_week, ":troop_total_income_week"),
        
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (neq,":troop_no","trp_player"),
        (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
        (try_begin),
          (gt, ":party_no",0),
          (party_is_active,":party_no"),
          (call_script, "script_calculate_weekly_party_wage", ":party_no"),
          (assign, ":cur_weekly_wage", reg0),
        ## CC-D begin
          (party_get_attached_to, ":attached", ":party_no"),
          (try_begin),
            (is_between, ":attached", centers_begin, centers_end),
            
            (assign, ":feast", 0),
            (store_faction_of_party, ":center_faction", ":attached"),
            (try_begin),
              (faction_slot_eq, ":center_faction", slot_faction_ai_state, sfai_feast),
              (faction_slot_eq, ":center_faction", slot_faction_ai_object, ":attached"),
              (assign, ":feast", 1),
            (try_end),
            
            (party_get_slot, ":lord", ":attached", slot_town_lord),
            (store_troop_faction, ":faction_no", ":troop_no"),
            (try_begin),
              (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
              (faction_get_slot, ":leader", ":faction_no", slot_faction_leader),
            (else_try),
              (assign, ":leader", -1),
            (try_end),
            
            (this_or_next|eq, ":feast", 1),
            (this_or_next|eq, ":leader", ":lord"),
            (eq, ":troop_no", ":lord"),
            
            (val_div, ":cur_weekly_wage", 2),
          (try_end),
        (else_try),
          (assign, ":cur_weekly_wage", 0),
        (try_end),
        
        (try_begin),
          (eq, "$g_ccc_option_npc_hard_training", 1),
          (val_div, ":cur_weekly_wage", 2),
        (try_end),
        ## CC-D end
        (val_sub, ":cur_wealth", ":cur_weekly_wage"),
        
        #(val_max, ":cur_wealth", 0), #CC-C max wealth
        (troop_set_slot, ":troop_no", slot_troop_wealth, ":cur_wealth"),
      (try_end),
      
      #center cost
      (try_for_range, ":center_no", centers_begin, centers_end),  ## CC-D: walled_centers->centers
        (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
        (party_get_slot, ":lord",":center_no", slot_town_lord),
        (gt,":lord",0),
        (call_script, "script_calculate_weekly_party_wage", ":center_no"),
        (assign, ":cur_weekly_wage", reg0),
        ## CC-D begin
        (val_div, ":cur_weekly_wage", 2),
        (try_begin),
          (eq, "$g_ccc_option_npc_hard_training", 1),
          (val_div, ":cur_weekly_wage", 2),
        (try_end),
        ## CC-D end
        (troop_get_slot, ":cur_wealth", ":lord", slot_troop_wealth),
        (val_sub, ":cur_wealth", ":cur_weekly_wage"),
        #(val_max, ":cur_wealth", 0), #CC-C max wealth
        (troop_set_slot, ":lord", slot_troop_wealth, ":cur_wealth"),
      (try_end),
      
      
      #player_supporters_faction fix
      (assign,":support_flag",0),
      (try_begin),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
        (faction_get_slot, ":leader","fac_player_supporters_faction", slot_faction_leader),
        (eq,":leader","trp_player"),
        (store_troop_gold, ":gold","trp_household_possessions"),
        (ge,":gold",30000),
        (troop_remove_gold,"trp_household_possessions",":gold"),
        (troop_get_slot, ":cur_wealth", "trp_player", slot_troop_wealth),
        (val_add,":cur_wealth",":gold"),
        (troop_set_slot, "trp_player", slot_troop_wealth, ":cur_wealth"),
        (assign,":support_flag",1),
      (try_end),
      
      #init
      (try_for_range, ":faction_no",kingdoms_begin,kingdoms_end),
        (faction_set_slot, ":faction_no", slot_faction_support_get, 0),
        (faction_set_slot, ":faction_no", slot_faction_support_send, 0),
      (try_end),

      #king send money
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (store_troop_faction,":faction_no",":troop_no"),
        (is_between,":faction_no",kingdoms_begin,kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_get_slot, ":leader",":faction_no", slot_faction_leader),
        (neq,":leader",":troop_no"),
        (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
        (troop_get_slot, ":leader_wealth", ":leader", slot_troop_wealth),
        (try_begin),
          (lt,":leader_wealth",700000),
          (gt,":troop_wealth",15000),
          (store_sub,":send_max",":troop_wealth",5000),
          (store_random_in_range,":send",3000,":send_max"),
          (val_min, ":send", 100000),
          (val_sub,":troop_wealth",":send"),
          (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
          (val_add, ":leader_wealth", ":send"),
          (troop_set_slot, ":leader", slot_troop_wealth, ":leader_wealth"),
          #support
          (faction_get_slot, ":support",":faction_no", slot_faction_support_get),
          (val_add, ":support", ":send"),
          (faction_set_slot, ":faction_no", slot_faction_support_get, ":support"),
          #(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":leader", 1),
        (else_try),
          (lt,":troop_wealth",2000),
          (troop_get_slot, ":leader_wealth", ":leader", slot_troop_wealth),
          (ge,":leader_wealth",30000),
          (assign,":send_wealth",3000),
          (try_begin),
            (gt,":leader_wealth",600000),
            (assign,":send_wealth",10000),
          (else_try),
            (gt,":leader_wealth",300000),
            (assign,":send_wealth",6000),
          (else_try),
            (gt,":leader_wealth",200000),
            (assign,":send_wealth",4000),
          (try_end),
          (store_sub,":aid_wealth",":send_wealth",":troop_wealth"),
          (val_sub,":leader_wealth",":aid_wealth"),
          (troop_set_slot, ":leader", slot_troop_wealth, ":leader_wealth"),
          
          (troop_get_slot, ":troop_wealth", ":troop_no", slot_troop_wealth),
          (val_add, ":troop_wealth", ":aid_wealth"),
          (troop_set_slot, ":troop_no", slot_troop_wealth, ":troop_wealth"),
          
          #support
          (faction_get_slot, ":support",":faction_no", slot_faction_support_send),
          (val_add, ":support", ":aid_wealth"),
          (faction_set_slot, ":faction_no", slot_faction_support_send, ":support"),
          #(call_script, "script_troop_change_relation_with_troop", ":troop_no", ":leader", 1),
        (else_try), # del army
          (lt, ":troop_wealth", 0),
          (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
          (gt, ":party_no",0),
          (party_is_active,":party_no"),
          (call_script, "script_party_inflict_attrition", ":party_no", 10),
          #(assign,":attrition_num",reg0),
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
            (call_script, "script_party_inflict_attrition", ":center_no", 10),
            #(val_add,":attrition_num",reg0),
          (try_end),
          
          #reset wealth
          #(store_mul,":get_wealth",100,":attrition_num"),
          (troop_set_slot, ":troop_no", slot_troop_wealth, 0),
        (try_end),
      (try_end),
      
      #player_supporters_faction fix
      (try_begin),
        (eq,":support_flag",1),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
        (faction_get_slot, ":leader","fac_player_supporters_faction", slot_faction_leader),
        (eq,":leader","trp_player"),
        (troop_get_slot, ":cur_wealth", "trp_player", slot_troop_wealth),
        (troop_add_gold,"trp_household_possessions",":cur_wealth"),
        (troop_set_slot, "trp_player", slot_troop_wealth, 0),
      (try_end),
      
      #fix
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (neq,":troop_no","trp_player"),
        (troop_get_slot, ":cur_wealth", ":troop_no", slot_troop_wealth),
        (val_min,":cur_wealth",9999999),
        (troop_set_slot, ":troop_no",slot_troop_wealth, ":cur_wealth"),
      (try_end),
      
      (store_current_day,"$g_week_day"),
      (call_script,"script_ccc_faction_report_save"),
    ]),
    
  #Pay day.
  (24 * 7,
   [
     ## CC begin
     (store_current_hours, "$g_next_pay_time"),
     (val_add, "$g_next_pay_time", 168),
     (str_store_date, s1, "$g_next_pay_time"),
     (party_set_name, "p_test_scene", s1),
     #(assign, "$g_presentation_lines_to_display_begin", 0),
     #(assign, "$g_presentation_lines_to_display_end", 15),
     ## CC end
     (assign, "$g_apply_budget_report_to_gold", 1),
     (try_begin),
       (eq, "$g_infinite_camping", 0),
       (start_presentation, "prsnt_budget_report"),
        ##diplomacy begin
        (try_begin),
          (gt, "$g_player_debt_to_party_members", 5000),
          (call_script, "script_add_notification_menu", "mnu_dplmc_deserters",20,0),
        (try_end),
        ##diplomacy end
        ## CC-D begin: expand improvement
        (try_for_range, ":center_no", centers_begin, centers_end),
          (neg|party_slot_eq, ":center_no", slot_center_ccd_last_measure, 0),
          (party_set_slot, ":center_no", slot_center_ccd_last_measure, 0),
        (try_end),
        ## CC-D end
     (try_end),
     
     ## CC-D begin: move to presentations
     ##CC-C begin Cave budget
     ##(assign,":total",0),
     #(call_script,"script_ccc_hide_house_upkeep_weekly"),
     #(val_add,":total",reg0),
     #(call_script,"script_ccc_hide_house_prison_upkeep_weekly"),
     #(val_add,":total",reg0),
     #(call_script,"script_ccc_rhodoks_mine_upkeep_weekly"),
     #(val_add,":total",reg0),

     ##(store_troop_gold,":bef_bank","trp_ccc_chest_bank"),
     ##(store_sub,":aft_bank",":bef_bank",":total"),
     #(try_begin),
     #  (ge,":total",0),
     #  (troop_add_gold,"trp_player",":total"), 
     #(else_try),
     #  (val_mul, ":total", -1),  ## CC-D fix
     #  (troop_remove_gold, "trp_player", ":total"),
     #(try_end),
     ##CC-C end
     ## CC-D end
    ]),
   
#  #Hiring men with hero wealths (once a day)
#  #Hiring men with center wealths (once a day)
  (24,
   [
     (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
       (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
       (troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
       (ge, ":party_no", 1),
       (party_is_active, ":party_no"),
       (party_get_attached_to, ":cur_attached_party", ":party_no"),
       (is_between, ":cur_attached_party", centers_begin, centers_end),
       (party_slot_eq, ":cur_attached_party", slot_center_is_besieged_by, -1), #center not under siege
                       
       (store_faction_of_party, ":party_faction", ":party_no"),
       (assign, ":num_hiring_rounds", 2),
       
       (try_begin),
         (this_or_next|faction_slot_eq,  ":party_faction", slot_faction_leader, ":troop_no"),
         (faction_slot_eq,  ":party_faction", slot_faction_marshall, ":troop_no"),
         (val_add, ":num_hiring_rounds", 2),
       (try_end),

       (try_for_range, ":unused", 0, ":num_hiring_rounds"),         
         (call_script, "script_hire_men_to_kingdom_hero_party", ":troop_no"), #Hiring men with current wealth        
       (try_end),
     (try_end),
       
     (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
       (neg|party_slot_eq, ":center_no", slot_town_lord, "trp_player"), #center does not belong to player.
       (party_slot_ge, ":center_no", slot_town_lord, 1), #center belongs to someone.       
       (party_slot_eq, ":center_no", slot_center_is_besieged_by, -1), #center not under siege
		 
       (assign, ":reinforcement_cost", ccc_reinforcement_cost), #cost
       (assign, ":num_hiring_rounds", 1), #Round
       
       (party_get_slot, ":lord",":center_no", slot_town_lord),
       (try_for_range, ":unused", 0, ":num_hiring_rounds"), 		 
         (troop_get_slot, ":cur_wealth", ":lord", slot_troop_wealth),
         (assign, ":hiring_budget", ":cur_wealth"),
         (val_div, ":hiring_budget", 2),
         (gt, ":hiring_budget", ":reinforcement_cost"),       
         (party_get_num_companions, ":party_size", ":center_no"),
         (call_script,"script_party_get_ideal_size",":center_no"),
         (ge,reg0,":party_size"),
         (call_script, "script_cf_reinforce_party", ":center_no"),       
         (val_sub, ":cur_wealth", ":reinforcement_cost"),
         (troop_set_slot, ":lord", slot_troop_wealth, ":cur_wealth"),
       (try_end),  
     (try_end),

     #this is moved up from below , from a 24 x 15 slot to a 24 slot
     (try_for_range, ":center_no", centers_begin, centers_end),
       (neg|is_between, ":center_no", castles_begin, castles_end),
       (call_script, "script_get_center_ideal_prosperity", ":center_no"),
       (assign, ":ideal_prosperity", reg0),
       (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
       (try_begin),
         (gt, ":prosperity", ":ideal_prosperity"),
         (call_script, "script_change_center_prosperity", ":center_no", -1),
         (val_add, "$newglob_total_prosperity_from_convergence", -1),
       (else_try),
         (lt, ":prosperity", ":ideal_prosperity"),
         (call_script, "script_change_center_prosperity", ":center_no", 1),
         (val_add, "$newglob_total_prosperity_from_convergence", 1),
       (try_end),
     (try_end),
    ]),

#slave prosperity
## CC-D begin: new calculate
# (55,
# [
#    (try_for_range, ":center_no", centers_begin, centers_end),
#      (neg|is_between, ":center_no", castles_begin, castles_end),
#      (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
#
#      (call_script,"script_ccc_check_slave_all_prisoners",":center_no"),
#      (assign,":all_slave",reg2),
#      
#      (gt,":all_slave",5),
#      
#      (assign,":dead",0),
#      (try_begin),
#        (lt,":prosperity",15),
#        (val_mul,":all_slave",4),
#      (else_try),
#        (lt,":prosperity",40),
#        (val_mul,":all_slave",3),
#      (else_try),
#        (lt,":prosperity",60),
#        (val_mul,":all_slave",2),
#      (try_end),
#      
#      (store_div,":dead",":all_slave",10),
#      (val_sub,":dead",-2),
#      (val_max,":dead",0),
#      
#      (store_sub,":rate",":all_slave",":prosperity"),
#      (val_max,":rate",1),
#      
#      (store_random_in_range,":get",0,100),
#      (try_begin),
#        (le,":get",":rate"),
#        (call_script, "script_change_center_prosperity", ":center_no", 1),
#      (try_end),
#      
#      (try_begin),
#        (gt,":dead",0),
#        (store_random_in_range,":r",0,10),
#        (try_begin),
#          (eq,":r",0),
#          (gt,reg0,0),
#          (val_min,":dead",reg0),
#          (party_remove_prisoners,":center_no","trp_ccc_slave_man",":dead"),
#        (try_end),
#          
#        (store_random_in_range,":r",0,15),
#        (try_begin),
#          (eq,":r",0),
#          (gt,reg1,0),
#          (val_min,":dead",reg1),
#          (party_remove_prisoners,":center_no","trp_ccc_slave_man",":dead"),
#        (try_end),
#      (try_end),
#    (try_end),
#  ]),
 (72,
 [
    (try_for_range, ":center_no", centers_begin, centers_end),
      (try_begin),
        (neg|is_between, ":center_no", castles_begin, castles_end),
        
        (party_get_slot, ":prosperity", ":center_no", slot_town_prosperity),
        (party_get_num_companions, ":party_size", ":center_no"),
        
        (gt, ":party_size", 30),
        
        (call_script, "script_ccc_check_slave_all_prisoners", ":center_no"),
        (assign, ":slave_man", reg0),
        (assign, ":slave_woman", reg1),
        (assign, ":slave_all", reg2),
        (assign, ":occc_workers", reg3),

        (gt, ":slave_all", 5),
        
        (store_mul, ":working_max", ":party_size", 2),
        (assign, ":workers", ":slave_all"),
        (val_min, ":workers", ":working_max"),
        (store_mul, ":workers_ratio", ":workers", 100),
        (val_div, ":workers_ratio", ":working_max"),
        
        (store_mul, ":effect", ":workers_ratio", 6),
        (val_div, ":effect", 100),  #max 6 when over 75 prosperity (-3 routine)
        (try_begin),
          (lt, ":prosperity", 25),
          (val_mul, ":effect", 4),
        (else_try),
          (lt, ":prosperity", 50),
          (val_mul, ":effect", 3),
        (else_try),
          (lt, ":prosperity", 75),
          (val_mul, ":effect", 2),
        (else_try),
          (val_mul, ":effect", 1),
        (try_end),
        (call_script, "script_change_center_prosperity", ":center_no", ":effect"),
        
        (call_script, "script_party_get_ideal_size", ":center_no"),
        (store_mul, ":slave_max", reg0, 2),
        (assign, ":dead_rate", 40),
        (try_begin),
          (gt, ":slave_all", ":slave_max"),
          (try_begin),
            (lt, ":workers_ratio", 25),
            (assign, ":dead_rate", 10),
          (else_try),
            (lt, ":workers_ratio", 50),
            (assign, ":dead_rate", 20),
          (else_try),
            (lt, ":workers_ratio", 75),
            (assign, ":dead_rate", 30),
          (else_try),
            (assign, ":dead_rate", 40),
          (try_end),
        (else_try),
          (try_begin),
            (lt, ":workers_ratio", 60),
            (assign, ":dead_rate", 5),
          (else_try),
            (assign, ":dead_rate", 10),
          (try_end),
        (try_end),
        
        (store_mul, ":all_dead_rate", ":workers", ":dead_rate"),
        (val_div, ":all_dead_rate", ":slave_all"),
        
        (try_begin),
          (gt, ":slave_man", 0),
          (store_mul, ":dead", ":slave_man", ":all_dead_rate"),
          (val_div, ":dead", 100),
          (store_random_in_range, ":must_die", 0, 10),
          (val_add, ":dead", ":must_die"),
          (val_min, ":dead", ":slave_man"),
          (party_remove_prisoners, ":center_no", "trp_ccc_slave_man", ":dead"),
        (try_end),
        (try_begin),
          (gt, ":slave_woman", 0),
          (val_div, ":all_dead_rate", 2),  #women have long life
          (store_mul, ":dead", ":slave_woman", ":all_dead_rate"),
          (val_div, ":dead", 100),
          (store_random_in_range, ":must_die", 0, 5),
          (val_add, ":dead", ":must_die"),
          (val_min, ":dead", ":slave_woman"),
          (party_remove_prisoners, ":center_no", "trp_ccc_slave_woman", ":dead"),
        (try_end),
        (try_begin),
          (gt, ":occc_workers", 0),
          (store_random_in_range, ":die_probability", 0, 10),
		  (le,":die_probability",3),#workers have far more longer life
          (val_div, ":all_dead_rate", 2),  
          (store_mul, ":dead", ":occc_workers", ":all_dead_rate"),
          (val_div, ":dead", 100),
          (store_random_in_range, ":must_die", 0, 5),
          (val_add, ":dead", ":must_die"),
          (val_min, ":dead", ":occc_workers"),
          (party_remove_prisoners, ":center_no", "trp_occc_worker", ":dead"),
        (try_end),

      (else_try),
        (call_script, "script_ccc_check_slave_all_prisoners", ":center_no"),
        (assign, ":slave_man", reg0),
        (assign, ":slave_woman", reg1),
        (try_begin),
          (gt, ":slave_man", 0),
          (store_random_in_range, ":must_die", 0, 5),
          (val_min, ":must_die", ":slave_man"),
          (party_remove_prisoners, ":center_no", "trp_ccc_slave_man", ":must_die"),
        (try_end),
        (try_begin),
          (gt, ":slave_woman", 0),
          (store_random_in_range, ":must_die", 0, 3),
          (val_min, ":must_die", ":slave_woman"),
          (party_remove_prisoners, ":center_no", "trp_ccc_slave_woman", ":must_die"),
        (try_end),
      (try_end),
    (try_end),
  ]),
## CC-D end

#make slave caravan
  (47,
  [
    (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
      (store_random_in_range,":true",0,2),
      (eq,":true",0),
      (call_script,"script_ccc_check_slave_all_prisoners",":center_no"),
      (assign,":slave_num",reg0),
      
      (assign,":min",10),
      (try_begin),
        (party_slot_eq, ":center_no", slot_party_type, spt_town),
        (assign,":min",100),
      (try_end),
      (ge,":slave_num",":min"),
      (store_random_in_range,":send_num",10,30),
      (val_min,":send_num",":slave_num"),
      
      #Where go to village?
      (store_faction_of_party, ":cur_faction_no", ":center_no"),
      (assign,":village_num",0),
      (try_for_range, ":village_no", villages_begin, villages_end),
        (store_faction_of_party, ":village_faction_no", ":village_no"),
        (eq,":cur_faction_no",":village_faction_no"),
        (val_add,":village_num",1),
      (try_end),
      (val_add,":village_num",1),
      (store_random_in_range,":set",0,":village_num"),
      (assign,":goto",0),
      (assign,":village_num",0),
      (try_for_range, ":village_no", villages_begin, villages_end),
        (eq,":goto",0),
        (store_faction_of_party, ":village_faction_no", ":village_no"),
        (eq,":cur_faction_no",":village_faction_no"),
        (try_begin),
          (eq,":set",":village_num"),
          (assign,":goto",":village_no"),
        (try_end),
        (val_add,":village_num",1),
      (try_end),
      
      (is_between,":goto",villages_begin,villages_end),
      (set_spawn_radius, 1),
      (spawn_around_party,":center_no","pt_ccc_slave_caravan_party"),
      (assign,":new_party",reg0),
      (gt,reg0,0),
      (party_set_faction,":new_party", ":cur_faction_no"),
      
      (party_set_slot,":new_party", slot_party_type,spt_slave_caravan),
      (party_set_slot,":new_party", slot_party_ai_state, spai_undefined),
      (party_set_slot,":new_party", slot_party_home_center,":center_no"),
      (party_set_slot,":new_party", slot_party_last_traded_center,":center_no"),
      
      (party_set_ai_behavior,":new_party",ai_bhvr_travel_to_party),
      (party_set_ai_object,":new_party",":goto"),
      (party_set_flags,":new_party", pf_default_behavior, 1),
      
      #send slave
      (party_remove_prisoners,":center_no", "trp_ccc_slave_man", ":send_num"),
      (party_add_prisoners, ":new_party", "trp_ccc_slave_man", ":send_num"),
    (try_end),
  ]),


  #Troop AI: Slave caravan thinking
  (8,
   [
       (try_for_parties, ":party_no"),
         (party_slot_eq, ":party_no", slot_party_type, spt_slave_caravan),
         (party_is_in_any_town, ":party_no"),

         (store_faction_of_party, ":cur_faction_no", ":party_no"),
         (try_begin),
           (neg|faction_slot_eq,":cur_faction_no", slot_faction_state, sfs_active),
           (remove_party, ":party_no"),
         (else_try),
           (party_get_cur_town, ":cur_center", ":party_no"),
           (assign,":slave_num",0),
           (party_get_num_prisoner_stacks, ":num_stacks",":party_no"),
           (gt,":num_stacks",0),
           (try_for_range, ":stack_iterator", 0, ":num_stacks"),
             (party_prisoner_stack_get_troop_id, ":troop_id", ":party_no", ":stack_iterator"),
             (eq,":troop_id",slave_begin),
             (party_prisoner_stack_get_size, ":slave_num", ":party_no", ":stack_iterator"),
           (try_end),
           (party_remove_prisoners, ":party_no", "trp_ccc_slave_man",":slave_num"),
           (party_add_prisoners, ":cur_center", "trp_ccc_slave_man",":slave_num"),
           (remove_party,":party_no"),
         (try_end),
       (try_end),
    ]),

  (42,
   [
    #(store_random_in_range,":faction_no",kingdoms_begin,kingdoms_end),
    (try_for_range,":faction_no",kingdoms_begin,kingdoms_end),
      (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
      (call_script, "script_create_kingdom_party_if_below_limit", ":faction_no", spt_kingdom_caravan),
    (try_end),
   ]),

  #faction event
   (24*2,
   [
      (try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
        (faction_get_slot, ":leader",":faction_no", slot_faction_leader),
        (troop_get_slot, ":leader_wealth", ":leader", slot_troop_wealth),
        (str_store_troop_name,s0,":leader"),
		
		#occc begin
        (try_begin),
			(eq,":leader","trp_kingdom_1_lord"),#Harlaus
			(eq,"$g_occc_factional_expantion",1),#swadian factional expantion
			(assign,":bonus_likely",35),#Halraus tends to retribute wealth more
		(else_try),
			(assign,":bonus_likely",10),
		(try_end),
		#occc end
		
        (assign,":pay",0),
        (store_random_in_range,":set_event",0,100),
        (try_begin),
          (lt,":set_event",5),
          (try_begin),
            (ge,":leader_wealth",200000),
            (call_script,"script_ccc_faction_event_training_all",":faction_no",10000),
            (store_mul,reg1,1000,reg0),
            (assign,":pay",reg1),
            (eq,":faction_no","$players_kingdom"),
            (display_message,"@{s0}:All army tarining. pay cost:{reg1}"),
          (try_end),
        (else_try),
          (lt,":set_event",":bonus_likely"),
          (try_begin),
            (ge,":leader_wealth",200000),
            (call_script,"script_ccc_faction_event_bonus_all",":faction_no",2000),
            (store_mul,reg1,2000,reg0),
            (assign,":pay",reg1),
            (eq,":faction_no","$players_kingdom"),
            (display_message,"@{s0}:Good Bonus Day. pay cost:{reg1}"),
          (try_end),
        (else_try),
          (lt,":set_event",70),
          (try_begin),
            (ge,":leader_wealth",100000),
            (call_script,"script_ccc_faction_event_build_village",":faction_no",30),
            (val_add,":pay",reg0),
            (call_script,"script_ccc_faction_event_build_village",":faction_no",30),
            (val_add,":pay",reg0),
          (try_end),
        (else_try),
          (lt,":set_event",80),
          (try_begin),
            (ge,":leader_wealth",200000),
            #(call_script,"script_ccc_faction_event_build_wall",":faction_no",30),
            #(val_add,":pay",reg0),
          (try_end),
        (else_try),
          #no event
        (try_end),
        
        (gt,":pay",0),
        (val_mul,":pay",-1),
        (call_script,"script_ccc_change_troop_wealth",":leader",":pay"),
      (try_end),
   ]),

  #title
  (47,
  [
      (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
        (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
        (store_troop_faction, ":cur_troop_faction", ":troop_no"),
        (call_script, "script_troop_set_title_according_to_faction", ":troop_no",":cur_troop_faction"),
      (try_end),
      
      (try_for_range, ":lady_no", "trp_kingdom_1_lady_1", "trp_heroes_end"),
        (troop_get_slot, ":spouse", ":lady_no", slot_troop_spouse),
        (try_begin),
          (eq,":spouse",-1),
          (str_store_troop_name_plural,s1,":lady_no"),
          (troop_set_name,":lady_no", "str_ccc_add_princess"),
        (else_try),
          (str_store_troop_name_plural,s1,":lady_no"),
          (troop_set_name,":lady_no", "str_ccc_add_lady"),
        (try_end),
      (try_end),
  ]),

   (48,
   [
       (store_current_hours,":h"),
       (val_add,":h",1000),
       (val_min,":h",72000), # 3000day stop
       (assign,":h_xp",":h"),
       (val_div,":h_xp",5),
       
       (try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
         (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
         (store_troop_faction, ":cur_troop_faction", ":troop_no"),
         #(neq, ":cur_troop_faction", "$players_kingdom"),
         (troop_get_slot, ":hero_party", ":troop_no", slot_troop_leaded_party),
         (gt, ":hero_party", centers_end),
         (party_is_active, ":hero_party"),
         
         #time training
         (store_skill_level, ":trainer_level", skl_trainer, ":troop_no"),                  
         (val_add, ":trainer_level", 5),
         (store_mul, ":xp_gain", ":trainer_level", 800), 
         (val_add,":xp_gain",":h_xp"),
         
         #kingdom bounus
         (try_begin),
          (is_between,":troop_no",kings_begin,kings_end),
          (val_mul,":xp_gain",2),
         (try_end),
         
         (try_begin),
           (eq,"$g_ccc_option_npc_hard_training",1),
           (neq, ":cur_troop_faction", "$players_kingdom"),
           (val_add,":xp_gain",500000),
         (try_end),
         
         (party_upgrade_with_xp, ":hero_party", ":xp_gain"),
       (try_end),
       
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),         
         (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
         (ge, ":center_lord", 1),
         (store_troop_faction,":cur_troop_faction",":center_lord"),
         (neq, ":cur_troop_faction", "$players_kingdom"),

          (try_begin),
            (party_slot_eq, ":center_no", slot_party_type, spt_town),
            (assign,":xp_gain",3000),
          (else_try),
            (assign,":xp_gain",10000),
          (try_end),
         
         (try_begin),
           (eq,"$g_ccc_option_npc_hard_training",1),
           (val_add,":xp_gain",500000),
         (try_end),

         (party_upgrade_with_xp, ":center_no", ":xp_gain"),
       (try_end),
    ]),
    
    #raise item set
   (24,
    [
                (try_begin), #debug
                  (eq, "$cheat_mode", 1),
				  (display_message, "@DEBUG!!! raise item set"),
                (try_end),

      (call_script,"script_ccc_set_slot_raise_item","trp_player"),
      ## CC-D begin: add ladies for wife
      #(try_for_range, ":troop_no", active_npcs_begin, active_npcs_end),
      (try_for_range, ":troop_no", heroes_begin, heroes_end),
      ## CC-D end
        (call_script,"script_ccc_set_slot_raise_item",":troop_no"),
      (try_end),
      
      (try_for_range, ":troop_no", customizable_troops_begin, customizable_troops_end),
        (neg|troop_is_hero, ":troop_no"),
        (call_script,"script_ccc_set_slot_raise_item",":troop_no"),
      (try_end),
    ]),
    
   (85,
    [
      (try_for_range, ":troop_no", companions_begin, companions_end),
        (assign, ":flag", 0),  ## CC-D add
        ## CC-D begin: return exiled npc
        (try_begin),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, dplmc_slto_exile),
          (store_troop_faction, ":faction_no", ":troop_no"),
          (eq, ":faction_no", "fac_outlaws"),
          
          (call_script, "script_change_troop_faction", ":troop_no", "fac_commoners"),
          (troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive),
          (troop_set_slot, ":troop_no", slot_troop_days_on_mission, 0),
          (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
          (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
          (troop_set_slot, ":troop_no", slot_troop_banner_scene_prop, 0),
          (troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
          (try_begin),
            (neq, ":party", -1),
            (remove_party, ":party"),
            (troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
          (try_end),
        (try_end),
        ## CC-D end
		#occc default companions not becoming vassal option befin
		(assign, ":try_check", 0), 
        (try_begin),
		 (is_between, ":troop_no", companions_begin, "trp_ccc_random_npc1"),
          (try_begin),
           (eq, "$g_occc_defaultcompanions_novassal", 0),
		   (assign, ":try_check", 0), 
          (else_try),
		   (assign, ":try_check", 1), 
          (try_end),
        (else_try),#Brothers will never be vassals
          (is_between,":troop_no",occc_brothers_npc_begin,occc_brothers_npc_end),
		   (assign, ":try_check", 1), 
        (try_end),
        (eq, ":try_check", 0),
        #(neq, ":troop_no", "trp_occc_random_npc_additional_2"),#king arthur must be seeking holy grail forever

		#occc end
        (try_begin),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_inactive),
          (troop_slot_eq,":troop_no",slot_troop_prisoner_of_party, -1),
          (assign,":max",120),
          (call_script, "script_troop_get_relation_with_troop", "trp_player", ":troop_no"),
          (try_begin),
			(this_or_next|is_between, ":troop_no", mercenary_npc_begin, mercenary_npc_end),#merc heroes often try to officer
            (le,reg0,-30),
            (assign,":max",10),
          (try_end),
          (store_random_in_range,":set",0,":max"),
          (try_begin),
            (le,":set",1),  ## CC-D 5->1
            (store_random_in_range,":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
            (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
            (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
            (call_script,"script_ccc_chenge_knight_item",":faction_no"),
            (troop_equip_items,":troop_no"),
            (str_store_troop_name,s0,":troop_no"),
            (str_store_faction_name,s1,":faction_no"),
            (display_message,"@{s0} officer to {s1}"),
            (call_script, "script_change_troop_faction",":troop_no",":faction_no"),
            (troop_set_note_available, ":troop_no", 1),
            
            (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
            (troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
            (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
            (assign, ":flag", 1),  ## CC-D add
          (try_end),
        (try_end),
        

		##add factional heroes occ?
##        (try_begin),
##            (le,":set",1),  ## CC-D 5->1
##            (assign, ":faction_no", fac_kingdom_4),  ## CC-D add
##            (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
##            (troop_set_slot, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
##            (call_script,"script_ccc_chenge_knight_item",":faction_no"),
##            (troop_equip_items,":troop_no"),
##            (str_store_troop_name,s0,":troop_no"),
##            (str_store_faction_name,s1,":faction_no"),
##            (display_message,"@{s0} officer to {s1}"),
##            (call_script, "script_change_troop_faction",":troop_no",":faction_no"),
##            (troop_set_note_available, ":troop_no", 1),
            
##            (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
##            (troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
##            (troop_set_slot, ":troop_no", slot_troop_prisoner_of_party, -1),
##            (assign, ":flag", 1),  ## CC-D add
##        (try_end),

		
		
		
        (try_begin),
          (troop_slot_eq, ":troop_no", slot_troop_occupation, slto_kingdom_hero),
          (store_troop_faction, ":faction_no", ":troop_no"),
          (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
          (is_between, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),  ## CC-D fix
          (faction_get_slot, ":leader",":faction_no", slot_faction_leader),
          (store_random_in_range,":set",0,100),
		  
		  #occc start
		  (try_begin),
		     (eq, ":troop_no", "trp_occc_random_npc_additional_merc_1"),
			 (eq,":faction_no", "fac_kingdom_14"),#Askeladd will try to serve Albion as long as possible
		     (assign, ":continue", 0), 
          (else_try),
		     (assign, ":continue", 1), 
          (try_end),
		  (eq,":continue", 1),
		  #occc end
          (try_begin),
            (lt,":set",4),  ## CC-D 5->4
            (call_script, "script_troop_change_relation_with_troop", ":troop_no", ":leader", -10),
          (else_try),
            (lt,":set",10),  ## CC-D 30->10
			(try_begin),
				(is_between, ":troop_no", mercenary_npc_begin, mercenary_npc_end),#merc heroes often change factions
				(assign,":hatred",15),
			(else_try),
				(assign,":hatred",-25),
			(try_end),

            (call_script, "script_troop_get_relation_with_troop",":troop_no", ":leader"),
            (lt,reg0,":hatred"),  ## CC-D -15->-25
            ## CC-D begin
            (troop_slot_eq, ":troop_no", slot_troop_prisoner_of_party, -1),
            (troop_get_slot, ":party", ":troop_no", slot_troop_leaded_party),
            (neq, ":party", "$enlisted_party"),  ## CC-D fix for Freelancer
            (try_begin),
              (neq, ":party", -1),
              (party_get_num_prisoner_stacks, ":num_prisoner_stacks", ":party"),
              (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
                (party_prisoner_stack_get_troop_id, ":stack_troop", ":party", ":stack_no"),
                (troop_is_hero, ":stack_troop"),
                (assign, ":flag", 1),
              (try_end),
            (try_end),
            (eq, ":flag", 0),
			#occc fix 
            (try_for_range, ":cur_center", centers_begin, centers_end),
              (party_slot_eq, ":cur_center", slot_town_lord, ":troop_no"),
              (party_set_slot, ":cur_center", slot_town_lord, stl_unassigned),
            (try_end),
            #(call_script, "script_change_troop_faction", ":troop_no", "fac_outlaws"),
            (call_script, "script_change_troop_faction", ":troop_no", "fac_commoners"),
            (str_store_troop_name,s0,":troop_no"),
            (str_store_faction_name,s1,":faction_no"),
            (display_message,"@{s0} go to outside from {s1}"),
            (troop_set_slot, ":troop_no", slot_troop_occupation, slto_inactive),
            #(troop_set_slot,":troop_no",slot_troop_prisoner_of_party, -1),
            (troop_set_slot, ":troop_no", slot_troop_cur_center, -1),
            (troop_set_slot, ":troop_no", slot_troop_banner_scene_prop, 0),
            (try_begin),
              (neq, ":party", -1),
              (remove_party, ":party"),
              (troop_set_slot, ":troop_no", slot_troop_leaded_party, -1),
            (try_end),
            ## CC-D end
          (try_end),
        (try_end),
      (try_end),
    ]),
    
## CC-D begin: use script_ccd_refresh_prison_guard
#   #Gob Store
#   (24*5,
#    [
#      (troop_clear_inventory, "trp_ccc_cave_prison_guard"),
#      
#      (try_for_range,":unused",0,8),
#        (store_random_in_range,":item_id","itm_dagger","itm_ccc_spawn_ghost"),
#        (store_item_value,":cost",":item_id"),
#        (lt,":cost",10000),
#        (troop_add_items, "trp_ccc_cave_prison_guard", ":item_id", 1),
#      (try_end),
#      
#      (try_for_range,":item_id","itm_lady_dress_ruby","itm_sarranid_dress_b"),
#        (store_random_in_range,":get",0,3),
#        (eq,":get",0),
#        (troop_add_items, "trp_ccc_cave_prison_guard", ":item_id", 1),
#      (try_end),
#      
#      (try_for_range,":item_id","itm_turret_hat_ruby","itm_hood_c"),
#        (store_random_in_range,":get",0,3),
#        (eq,":get",0),
#        (troop_add_items, "trp_ccc_cave_prison_guard", ":item_id", 1),
#      (try_end),
#      
#      (try_begin),
#        (store_random_in_range,":get",0,3),
#        (eq,":get",0),
#        (troop_add_items, "trp_ccc_cave_prison_guard", "itm_ccc_throwing_aphrodisiac", 1),
#      (try_end),
#      
#      (call_script, "script_ccc_set_troop_modifier_all_inv_item", "trp_ccc_cave_prison_guard",30),
#      
#      (call_script,"script_ccc_get_stone","trp_ccc_cave_prison_guard",50),
#      (call_script,"script_ccc_get_stone","trp_ccc_cave_prison_guard",10),
#      (call_script,"script_ccc_get_stone","trp_ccc_cave_prison_guard",5),
#      (call_script,"script_ccc_get_stone","trp_ccc_cave_prison_guard",2),
#
#      (troop_sort_inventory, "trp_temp_troop"),
#    ]),
## CC-D end
    
#CC-C bandit quest begin
   (24*14,
   [
    (call_script,"script_ccc_set_cave_quest"),
   ]),
   
   ## CC-D begin: not use
   ##Mate
   #(1,
   #[
   # (try_begin),
   #   (eq,"$g_ccc_temp_flag",3000),
   #   (troop_is_hero,"$g_talk_troop"),
   #   (is_between,"$g_talk_troop",bandit_npc_begin,bandit_npc_end),
   #   (jump_to_menu,"mnu_ccc_troop_meeting"),
   # (try_end),
   #]),
   ## CC-D end
#CC-C bandit quest end
#CC-C begin surgery
   (2,
   [
    (try_begin),
      (gt,"$g_ccc_option_surgery_fix",0),
      (map_free),
      (party_get_num_companion_stacks, ":party_num_stacks", "p_main_party"),
      (try_for_range_backwards,":stacks_index",0,":party_num_stacks"),
        (party_stack_get_troop_id,":troop_no","p_main_party",":stacks_index"),
        (neg|troop_is_hero,":troop_no"),
        (party_stack_get_num_wounded,":wounded_num","p_main_party",":stacks_index"),
        (gt,":wounded_num",0),
        (assign,":dead_cnt",0),
        (try_for_range,":unused",0,":wounded_num"),
          (store_random_in_range,":r",0,100),
          (try_begin),
            (lt,":r","$g_ccc_option_surgery_fix"),
            (val_add,":dead_cnt",1),
          (try_end),
        (try_end),
        (try_begin),
          (gt,":dead_cnt",0),
          (party_remove_members_wounded_first,"p_main_party",":troop_no",":dead_cnt"),
          #(party_remove_members,"p_main_party",":troop_no",":dead_cnt"),  ## CC-D fix
          (str_store_troop_name,s10,":troop_no"),
          (assign,reg10,":dead_cnt"),
          (display_message,"@{reg10} {s10} Dead",0xFFFF0000),
        (try_end),
      (try_end),
    (try_end),
   ]),
#CC-C end surgery
   
#CC-C end

## CC-D begin
  (1,
    [
      (neg|map_free),
      (lt, "$g_ccd_castle_train", 0),
      (val_add, "$g_ccd_castle_train", 1),
      (ge, "$g_ccd_castle_train", 0),
      (assign, "$g_ccd_castle_train", 0),
      (rest_for_hours, 0, 0, 0), #stop resting
      (jump_to_menu, "mnu_ccd_castle_train_maneuver"),
    ]),

  (24,
    [
      (call_script, "script_ccd_work_training_room"),
      (call_script, "script_ccd_create_stray_herd"),
      ## CC begin: Auto-save every 24 hours
      (try_begin),
        (eq, "$g_auto_save", 1),
        (auto_save),
      (try_end),
      ## CC end
    ]),

  (48,
    [
      (call_script, "script_ccd_refresh_prison_guard"),
      (call_script, "script_ccd_charge_barrack_reserve"),
      (call_script, "script_ccd_refresh_blacksmith"),
      (call_script, "script_ccd_refresh_bandit_merchant"),
	  (call_script, "script_occc_refresh_exotic_trader"),#occc
    ]),

  (96,
    [
      (call_script, "script_ccd_refresh_liar_troop"),
      (call_script, "script_ccd_fix_bandit_relation"),
    ]),

  (144,
    [
      (call_script, "script_ccd_refresh_horse_trainer"),
    ]),
## CC-D end

##occc start  
#Floris debt checking
	(24, 																				#Floris seefaring occc 1->24
	[	
   	#	(try_begin),
	#		(party_get_current_terrain, ":terrain", "p_main_party"),
	#		(eq, ":terrain", 0),
	#		(neq, "$g_player_icon_state", pis_ship),
	#		(assign, "$g_player_icon_state", pis_ship),
	#	(else_try),
	#		(party_get_current_terrain, ":terrain", "p_main_party"),
	#		(gt, ":terrain", 0),
	#		(assign, "$g_player_icon_state", pis_normal),		
	#	(try_end),
	#	
	#	(try_begin),
	#		(party_get_slot, ":timer", "p_main_party", slot_ship_time),
	#		(gt, ":timer", 0),
	#		(store_current_hours, ":cur_time"),			
	#		(ge, ":cur_time", ":timer"),
	#		(try_begin),
	#			(party_get_current_terrain, ":terrain", "p_main_party"),
	#			(eq, ":terrain", 0),
	#			(store_skill_level, ":skill", skl_foraging,"trp_player"),
	#			(val_mul, ":skill", 10),
	#			(store_random_in_range, ":luck", 0, 100),
	#			(ge, ":skill", ":luck"),
	#			(store_free_inventory_capacity, ":i_space", "trp_player"),
	#			(try_begin),
	#				(ge, ":i_space", 1),
	#				(display_message, "@You caught some fish."),
	#				(troop_add_item, "trp_player", "itm_trade_smoked_fish"),
	#				#(troop_add_merchandise, "trp_player", "itm_trade_smoked_fish", 1),
	#			(else_try),
	#				(display_message, "@Due to insufficient space, you had to throw the fish back into the ocean"),
	#			(try_end),				
	#			(assign,"$g_camp_mode", 0),
	#			(rest_for_hours_interactive, 0, 5, 1),
	#			(party_set_slot, "p_main_party", slot_ship_time, 0),
	#		(else_try),
	#			(display_message, "@All you caught were some seaweeds."),
	#			(assign,"$g_camp_mode", 0),
	#			(rest_for_hours_interactive, 0, 5, 1),
	#			(party_set_slot, "p_main_party", slot_ship_time, -1),
	#		(try_end),
	#	(try_end),
	#	
	#	(set_fixed_point_multiplier, 10),
	#	(try_for_parties, ":party_no"),													#Floris Get Back to Shore Check
	#		(party_get_template_id,":template",":party_no"),
	#		(this_or_next|eq, ":template", "pt_sea_raiders_ships"),
	#		(this_or_next|eq, ":template", "pt_sea_raiders_ships_r"),
	#		(eq, ":template", "pt_sea_raiders_ships_e"),
	#		(try_begin),
	#			(party_get_position, pos1, ":party_no"),
	#			(position_get_y, ":value_y", pos1),
	#			(position_get_x, ":value_x", pos1),
	#			(val_div, ":value_y", 10),
	#			(val_div, ":value_x", 10),
	#			(this_or_next|gt, ":value_y", 155),
	#			(lt, ":value_x", -180),
	#			(assign, reg1, ":value_y"),
	#			(assign, reg2, ":value_x"),
	#			(get_party_ai_current_behavior, ":behavior", ":party_no"),
	#			(assign, reg3, ":behavior"),
	#			#(display_message, "@Behavior was {reg3}, X is {reg2} and Y is {reg1}"), 
	#			#(party_set_flags, ":party_no", pf_default_behavior, 0),
	#			(party_set_ai_behavior, ":party_no", ai_bhvr_travel_to_party),      ###test if   ai_bhvr_travel_to_point (with the point being the spawn_point location, or a randomized point around it)
	#			(party_set_ai_object, ":party_no", "p_ship_raider_spawn_point_1"),   ##### prevents the ships from going invisible/inactive when they return to the spawn point
	#			#(display_message, "@Get Back to Shore TEST"),
	#		(else_try),
	#			(store_distance_to_party_from_party, ":distance", ":party_no", "p_ship_raider_spawn_point_1"),
	#			(lt, ":distance", 4),
	#			#(party_set_flags, ":party_no", pf_default_behavior, 1),
	#			(party_get_position, pos2, "p_ship_raider_spawn_point_1"),
	#			(party_set_ai_behavior, ":party_no", ai_bhvr_patrol_location),
	#			(party_set_ai_patrol_radius, ":party_no", 10),
	#			(party_set_ai_target_position, ":party_no", pos2),  
				#(party_set_ai_behavior, ":party_no", ai_bhvr_patrol_party),
				#(party_set_ai_patrol_radius, ":party_no", 10),
				#(party_set_ai_object, ":party_no", "p_ship_raider_spawn_point_1"),
				#(party_set_aggressiveness, ":party_no" , 15),
				#(display_message, "@Now get back to sea TEST"),
	#		(try_end),
	#	(try_end),
		
				
		(try_for_range, ":town_no", towns_begin, towns_end),							#	Floris Moneylenders // Not paying debts has consequences
			(party_get_slot, ":debt", ":town_no", slot_town_bank_debt),
			(gt, ":debt", 0),															#	If a debt exists, a deadline exists
			(party_get_slot, ":deadline", ":town_no", slot_town_bank_deadline),
			(store_current_hours, ":date"),
			(ge, ":date", ":deadline"),
			(call_script, "script_change_player_relation_with_center", ":town_no", -5, 0xff3333),
			(try_begin),
				(lt, ":debt", 100000),
				(val_mul, ":debt", 14),
				(val_div, ":debt", 10),
				(try_begin),
					(gt, ":debt", 100000),												#Debt doesnt get higher than 100000 denars
					(assign, ":debt", 100000),
				(try_end),
				(val_add, ":deadline", 24*14),
				(party_set_slot, ":town_no", slot_town_bank_debt, ":debt"),
				(party_set_slot, ":town_no", slot_town_bank_deadline, ":deadline"),
				(str_store_party_name, s1, ":town_no"),
				(display_message, "@You missed the deadline to pay back your debts in {s1}. They now grow at an interest of 50%."),
			(else_try),
				(assign, ":debt", 100000),												#If debt = 100000 denars, then additionally to -5 relation with town, you get -1 relation with Faction.
				(val_add, ":deadline", 24*14),
				(party_set_slot, ":town_no", slot_town_bank_debt, ":debt"),
				(party_set_slot, ":town_no", slot_town_bank_deadline, ":deadline"),
				(store_faction_of_party, ":faction_no", ":town_no"),
				(call_script, "script_change_player_relation_with_faction_ex", ":faction_no", -1),
				(str_store_party_name, s1, ":town_no"),
				(display_message, "@Your debt in {s1} is now so high that the King himself has taken notice. He has frozen your debt, but is displeased with the situation.", 0xff3333),
			(try_end),
		(try_end),			
		
		
	]),
	
	(24*14,
	[
		(try_for_range, ":town_no", towns_begin, towns_end),							#	Floris	//	Adjust Population Depending on Prosperity
			(party_get_slot, ":prosperity", ":town_no", slot_town_prosperity),
			(party_get_slot, ":population", ":town_no", slot_center_population),
			(assign,":change",0),
			(try_begin),#
				(ge, ":prosperity", 57),#occc 60->57
				(store_sub, ":change", ":prosperity",57),#occc 60->57
				(val_div, ":change", 5),#occc 5
				(val_add, ":change", 3),
			(else_try),
				(le, ":prosperity", 42),#occc 40->42
				(store_sub, ":change", ":prosperity", 42),#occc 40->42
				(val_div, ":change", 5),#occc 5
				(val_sub, ":change", 5),
			(else_try),#random change
				(store_random_in_range, ":change", -2, 3),#occc -2~2
			(try_end),

			(store_div,":base",":population",200),										#	Base population change is 0.5% of pop occc 100->200
			(val_mul,":change",":base"),				
			(val_min, ":change", 500),
			
			
			#occc plague system begin
			  (store_random_in_range, ":random_no", 0, 100),
			  (store_div,":sanitation_risk",":population",10000),#every 10000 population, Epidemic Risk rises
			  (val_sub,":random_no",":sanitation_risk"),
			  (try_begin),#Waterworks can decrease plague risk
				(party_slot_eq, ":town_no", slot_center_has_waterworks, 1),
				(val_add, ":random_no", 2),
			  (try_end),
			  
			  (try_begin), #Disaster Chance
				(le, ":random_no", 0),#1% chance of epidemic - should happen once every 4 years
				(try_begin),
				   (str_store_party_name_link, s4, ":town_no"),
				   (display_log_message, "@{s4} was visited by a plague...",0xFF0000),
				   (store_div,":change",":population",4),#25% of people die from plague
				   (val_mul,":change",-1),
				   (call_script, "script_change_center_prosperity", ":town_no", -25),#prosperity penalties
			   (try_end),
			  (try_end),
			#occc plague system end

			(val_add,":population", ":change"),			
			(try_begin),
				(gt, ":population", 100000),
				(assign, ":population", 100000),
				(party_set_slot, ":town_no", slot_center_population, ":population"),
			(else_try),
				(lt, ":population", 5000),
				(assign, ":population", 5000),
				(party_set_slot, ":town_no", slot_center_population, ":population"),
			(else_try),
				(party_set_slot, ":town_no", slot_center_population, ":population"),
			(try_end),
		(try_end),	
	
		(try_for_range, ":town_no", towns_begin, towns_end),							#	Floris	//	Calculating Land Demand and Consequences for supply, pricing and renting
			(party_get_slot, ":population", ":town_no", slot_center_population),
			(party_get_slot, ":land_town", ":town_no", slot_town_acres),
			(party_get_slot, ":land_player", ":town_no", slot_town_player_acres),
			(party_get_slot, ":prosperity", ":town_no", slot_town_prosperity),
			(store_sub, ":revenue", ":prosperity", 50),
			(val_add, ":revenue", 100),
			(try_begin),
				(store_div, ":acres_needed", ":population", 200),						#	200 People warrant 1 acre of cultivated land
				(store_add, ":total_land", ":land_town", ":land_player"),
				(store_sub, ":surplus", ":total_land", ":acres_needed"),
				
				(try_begin),															#	AI Consequences
					(lt, ":total_land", ":acres_needed"),
					(store_sub, ":new_acres", ":acres_needed", ":total_land"),
					(val_add, ":land_town", ":new_acres"),
					(party_set_slot, ":town_no", slot_town_acres, ":land_town"),
				(else_try),
					(ge, ":surplus", 20),
					(ge, ":land_town", 10),
					(val_sub, ":land_town", 10),										#	Changed from 2 / Faster rebalancing in case of player screw up
					(party_set_slot, ":town_no", slot_town_acres, ":land_town"),
				(try_end),
				
				(try_begin),
					(gt, ":land_player", 0),												# 	New Fix / Before it was possible for the towns land to cause the player a deficit
					(try_begin),															#	Player Consequences
						(le, ":total_land", ":acres_needed"),
						(val_mul, ":land_player", ":revenue"),										
						(party_set_slot, ":town_no", slot_town_bank_rent, ":land_player"),
					(else_try),
						(store_mul, ":penalty", ":surplus", -1),
						(val_add, ":penalty", ":revenue"),
						(try_begin),
							(ge, ":penalty", 85),
							(val_mul, ":land_player", ":penalty"),
							(party_set_slot, ":town_no", slot_town_bank_rent, ":land_player"),
						(else_try),
							(store_sub, ":non_rented", ":surplus", 15),
							(val_sub, ":land_player", ":non_rented"),
							(try_begin),													#	Safety check // No penalty on rent should turn rent negative.
								(lt, ":penalty", 0),
								(assign, ":penalty", 0),
							(try_end),
							(val_mul, ":land_player", ":penalty"),
							(party_set_slot, ":town_no", slot_town_bank_rent, ":land_player"),
							(val_mul, ":non_rented", -50),
							(party_set_slot, ":town_no", slot_town_bank_upkeep, ":non_rented"),
						(try_end),
					(try_end),
					(party_get_slot, ":assets", ":town_no", slot_town_bank_assets),						#	Adding/Subtracting profits/losses
					(party_get_slot, ":rent", ":town_no", slot_town_bank_rent),
					(party_get_slot, ":upkeep", ":town_no", slot_town_bank_upkeep),
					(val_add, ":assets", ":rent"),
					(val_add, ":assets", ":upkeep"),
					(party_set_slot, ":town_no", slot_town_bank_assets, ":assets"),	
				(try_end),
				
			(try_end),
		
		(try_end),
	
	]),	
#{BANK OF CALRADIA}		#	Floris Overhaul
  (24 * 7,
   [
	(neq, "$g_infinite_camping", 1),
	(assign, ":end", towns_end),
	(try_for_range, ":center_no", towns_begin, ":end"),
		(this_or_next|party_slot_ge, ":center_no", slot_town_player_acres, 1),
		(this_or_next|party_slot_ge, ":center_no", slot_town_bank_assets, 1),
		(party_slot_ge, ":center_no",slot_town_bank_debt, 1),
		(assign, ":end", towns_begin), #break
	(try_end),
	(eq, ":end", towns_begin), #ONLY DISPLAY BANK PRESENTATION IF THE PLAYER IS USING BANK
	(start_presentation, "prsnt_bank_quickview"),
    ]),
#{BANK OF CALRADIA}

  (24*11,
    [
	
	  #occc noble troop recruiting
     (try_for_range, ":town_no", towns_begin, castles_end),
        (call_script, "script_occc_update_noble_troops_in_towns", ":town_no"),
     (try_end),
      (assign, "$religious_donation", 0),

      (gt, "$hire_religiousknight_constable", 0),
      (val_sub, "$hire_religiousknight_constable", 1),
	  
    ]
  ),
  
 
#rising sun invasion
  (3,#blitzkrieg
    [

    (eq, "$occc_risingsun_conquering_process", 2),
    (call_script, "script_occc_rising_sun_blitzkrieg"),
	(try_for_range, ":troop_id", "trp_knight_9_1", "trp_knight_10_1"),			
		(troop_get_slot, ":leaded_party", ":troop_id", slot_troop_leaded_party),
        (party_is_active, ":leaded_party"),
		(call_script, "script_change_party_morale", ":leaded_party", 8),
	(try_end),#risingsun



    ]  ),
  (3,#blitzkrieg
    [

    (eq, "$occc_sunset_conquering_process", 2),
    (call_script, "script_occc_sunset_blitzkrieg"),
	(try_for_range, ":troop_id", "trp_knight_10_1", "trp_knight_11_1"),			
		(troop_get_slot, ":leaded_party", ":troop_id", slot_troop_leaded_party),
        (party_is_active, ":leaded_party"),
		(call_script, "script_change_party_morale", ":leaded_party", 8),
	(try_end),#sunset
    ]  ),


  (7,#RS party AI
    [
	(eq,"$g_occc_risingsun_invasion",1),
    (ge, "$occc_risingsun_conquering_process", 2),
	(faction_get_slot, ":state","fac_kingdom_9", slot_faction_state),
	(eq,":state",sfs_active),

			(try_for_parties, ":party_no_c"),
				(party_get_template_id, ":template", ":party_no_c"),
				(eq,":template","pt_occc_taikou_conquestarmy"),
				(party_get_slot, ":following_party", ":party_no_c", slot_party_commander_party),
				
				(try_begin),
					(gt, ":following_party", 0),
					(party_is_active, ":following_party"),

					
					(party_get_slot, ":gotstate", ":following_party", slot_party_ai_state),
					(try_begin),
						(neq, ":gotstate", spai_besieging_center),
						(party_set_slot, ":party_no_c", slot_party_ai_substate, spai_accompanying_army),
						(party_set_ai_behavior, ":party_no_c", ai_bhvr_escort_party),
						(party_set_ai_object, ":party_no_c", ":following_party"),

					(else_try),
						(party_slot_eq, ":following_party", slot_party_ai_state, spai_besieging_center),
						(party_slot_eq, ":following_party", slot_party_ai_substate, 1),
						(party_get_slot, ":center_no",":following_party",slot_party_ai_object),
						(call_script, "script_party_set_ai_state", ":party_no_c", spai_undefined, -1),
						(call_script, "script_party_set_ai_state", ":party_no_c", spai_besieging_center, ":center_no"),
						#resetting siege begin time if at least 1 party retreats
					(try_end),
				(else_try),
						(party_set_slot, ":party_no_c", slot_party_commander_party, 0),
						(call_script, "script_party_set_ai_state", ":party_no_c", spai_undefined, -1),
						(party_set_aggressiveness, ":party_no_c", 100),
						(party_set_helpfulness, ":party_no_c", 1000),        

				(try_end),
			(try_end),
		  #occc end

    ]  ),
	
  (7,#SS party AI
    [
	(eq,"$g_occc_sunset_invasion",1),
    (ge, "$occc_sunset_conquering_process", 2),
	(faction_get_slot, ":state","fac_kingdom_10", slot_faction_state),
	(eq,":state",sfs_active),

			(try_for_parties, ":party_no_c"),
				(party_get_template_id, ":template", ":party_no_c"),
				(eq,":template","pt_occc_sunset_conquestarmy"),
				(party_get_slot, ":following_party", ":party_no_c", slot_party_commander_party),
				
				(try_begin),
					(gt, ":following_party", 0),
					(party_is_active, ":following_party"),

					
					(party_get_slot, ":gotstate", ":following_party", slot_party_ai_state),
					(try_begin),
						(neq, ":gotstate", spai_besieging_center),
						(party_set_slot, ":party_no_c", slot_party_ai_substate, spai_accompanying_army),
						(party_set_ai_behavior, ":party_no_c", ai_bhvr_escort_party),
						(party_set_ai_object, ":party_no_c", ":following_party"),

					(else_try),
						(party_slot_eq, ":following_party", slot_party_ai_state, spai_besieging_center),
						(party_slot_eq, ":following_party", slot_party_ai_substate, 1),
						(party_get_slot, ":center_no",":following_party",slot_party_ai_object),
						(call_script, "script_party_set_ai_state", ":party_no_c", spai_undefined, -1),
						(call_script, "script_party_set_ai_state", ":party_no_c", spai_besieging_center, ":center_no"),
						#resetting siege begin time if at least 1 party retreats
					(try_end),
				(else_try),
						(party_set_slot, ":party_no_c", slot_party_commander_party, 0),
						(call_script, "script_party_set_ai_state", ":party_no_c", spai_undefined, -1),
						(party_set_aggressiveness, ":party_no_c", 100),
						(party_set_helpfulness, ":party_no_c", 1000),        
				(try_end),

			(try_end),
		  #occc end

    ]  ),

  (24,
    [
	#risingsun
	(eq, "$g_occc_risingsun_invasion", 1),
	(le, "$occc_risingsun_conquering_process", 3),
    (val_sub, "$occc_risingsun_limitday", 1),
	  
	(try_begin),
	 (eq, "$occc_risingsun_limitday", 0),
     (try_begin),
	  (eq, "$occc_risingsun_conquering_process", 0),
      (store_random_in_range, "$occc_risingsun_limitday", 80, 200),
	  (assign, "$occc_risingsun_conquering_process", 1),
		(jump_to_menu, "mnu_occc_risingsun_rumor"),
	 (else_try),
      (eq, "$occc_risingsun_conquering_process", 1),
	  #rising sun invasion!!!
		(jump_to_menu, "mnu_occc_risingsun_invasion"),
     (try_end),
    (try_end),

     (try_begin),
        (eq, "$occc_risingsun_conquering_process", 2),
        (eq, "$occc_risingsun_limitday", -12),
		(faction_get_slot, ":state","fac_kingdom_9", slot_faction_state),
		(eq,":state",sfs_active),

	(try_for_range, ":troop_id", "trp_knight_9_9", "trp_knight_10_1"),
			(call_script, "script_ccc_chenge_knight_item", ":troop_id"),
			(troop_equip_items,":troop_id"),
			(troop_set_slot, ":troop_id", slot_troop_occupation, slto_kingdom_hero),
			(call_script, "script_troop_change_relation_with_troop", ":troop_id", "trp_kingdom_9_lord", 100),
			(call_script,"script_ccc_change_troop_wealth",":troop_id",300000),
			(call_script, "script_create_kingdom_hero_party", ":troop_id", "p_taikou_scout_spawn_point"),#
			(store_random_in_range, ":renown", 700, 1000),
			(troop_set_slot, ":troop_id", slot_troop_renown, ":renown"),
			(troop_set_note_available, ":troop_id", 1),
			(call_script, "script_update_troop_notes", ":troop_id"),
		(store_random_in_range, ":reputation", 1, 8),

        (troop_set_slot, ":troop_id", slot_lord_reputation_type, ":reputation"),
		(troop_get_slot, ":leaded_party", ":troop_id", slot_troop_leaded_party),

		(spawn_around_party, "p_taikou_scout_spawn_point", "pt_occc_taikou_seeker"),
		(assign,":spawned_party",reg0),
		(party_add_leader,":spawned_party","trp_taikou_umanori_bushou"),
		(party_set_aggressiveness, ":spawned_party", 50),
		(party_set_helpfulness, ":spawned_party", 1000),        
		(party_set_ai_behavior, ":spawned_party", ai_bhvr_escort_party),
		(party_set_ai_object, ":spawned_party", ":leaded_party"),

		
	(try_end),#occc_taikou_conquestarmy

		(troop_get_slot, ":leaded_party", "trp_knight_9_9", slot_troop_leaded_party),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),

		(troop_get_slot, ":leaded_party", "trp_knight_9_10", slot_troop_leaded_party),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),

		(troop_get_slot, ":leaded_party", "trp_knight_9_11", slot_troop_leaded_party),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		
		(troop_get_slot, ":leaded_party", "trp_knight_9_12", slot_troop_leaded_party),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),

		(troop_get_slot, ":leaded_party", "trp_knight_9_13", slot_troop_leaded_party),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),
		(party_add_template, ":leaded_party", "pt_occc_taikou_conquestarmy"),

		(call_script, "script_occc_rising_sun_reinforcement",),
		(display_message, "@Taikonese Reinforcement has arrived! and they have started surprise attack again!", 0xffffff), #
     (try_end),


     (try_begin),
        (eq, "$occc_risingsun_conquering_process", 2),
        (le, "$occc_risingsun_limitday", -24),
        (assign, "$occc_risingsun_conquering_process", 3),
     (try_end),
	
     (try_begin),
        (eq, "$occc_risingsun_conquering_process", 3),
		(val_add,"$occc_risingsun_limitday",2),#need fix
		(ge,"$occc_risingsun_limitday",150),
		(faction_get_slot, ":state","fac_kingdom_9", slot_faction_state),
		(eq,":state",sfs_active),
		
	    (store_random_in_range, ":rand_no", 0, 10),
        (eq, ":rand_no", 0),
		(call_script, "script_occc_rising_sun_reinforcement",),
		(display_message, "@Taikonese Reinforcement has arrived! and they have started surprise attack again!", 0xffffff), #
        (assign, "$occc_risingsun_limitday", 0),

	(try_end),

    ]
  ),


  (24,
    [
	#sunset
	(eq, "$g_occc_sunset_invasion", 1),
	(lt, "$occc_sunset_conquering_process", 3),
    (val_sub, "$occc_sunset_limitday", 1),
	  
	(try_begin),
	 (eq, "$occc_sunset_limitday", 0),
     (try_begin),
	  (eq, "$occc_sunset_conquering_process", 0),
      (store_random_in_range, "$occc_sunset_limitday", 20, 30),
	  (assign, "$occc_sunset_conquering_process", 1),
		(jump_to_menu, "mnu_occc_sunset_encount"),
	 (else_try),
      (eq, "$occc_sunset_conquering_process", 1),
	  #sunset invasion!!!
		(jump_to_menu, "mnu_occc_sunset_invasion"),
     (try_end),
    (try_end),

     (try_begin),
        (eq, "$occc_sunset_conquering_process", 2),
        (le, "$occc_sunset_limitday", -12),
		(try_for_range, ":faction_id", kingdoms_begin, kingdoms_end),
			(neq,":faction_id","fac_kingdom_10"),
			(faction_get_slot, ":state",":faction_id", slot_faction_state),
			(eq,":state",sfs_active),
			(call_script, "script_diplomacy_start_war_between_kingdoms", "fac_kingdom_10", ":faction_id", 1),
		(try_end),
        (assign, "$occc_sunset_conquering_process", 3),
     (try_end),

    ]
  ),
  
  
  
  #


  (24*10,#Hidden companion available/ occc mercenary heroes/ new factional bandits/ and Restoration of Calradic Empire by NPC faction check
    [
	  #(try_begin),
	#	(ge, "$g_ccc_cave_frenzy_top_stage", 5),
	#	(troop_get_slot, ":is_he_dead","trp_occc_random_npc_additional_1", slot_troop_occupation),
	#	(eq, ":is_he_dead", dplmc_slto_dead),#is he deada???
	#	(troop_set_slot, "trp_occc_random_npc_additional_1", slot_troop_occupation, slto_inactive),
	#	(display_message, "@'He' has come back from Avalon."), 
	  #(try_end),
      (store_current_day,":now_day"),

	  (try_begin),
		(ge, "$g_ccc_cave_frenzy_top_stage", 5),
		(troop_get_slot, ":is_he_dead","trp_kingdom_14_lord", slot_troop_occupation),
		(eq, ":is_he_dead", dplmc_slto_dead),#is he deada???
		(troop_set_slot, "trp_kingdom_14_lord", slot_troop_occupation, slto_inactive),
		(display_message, "@'He' has come back from Avalon."), #
	  (try_end),
      (try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),

        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(this_or_next|eq,":faction_no","fac_kingdom_1"),
		(this_or_next|eq,":faction_no","fac_kingdom_4"),
		(this_or_next|eq,":faction_no","fac_kingdom_6"),
		(this_or_next|eq,":faction_no","fac_kingdom_7"),
		(this_or_next|eq,":faction_no","fac_kingdom_11"),
		(eq,":faction_no","fac_kingdom_12"),
        (faction_get_slot, ":leader",":faction_no", slot_faction_leader),
        (troop_get_slot, ":leader_wealth", ":leader", slot_troop_wealth),
        (str_store_troop_name,s0,":leader"),
        (assign,":pay",0),
        (store_random_in_range,":set_event",0,100),

        (try_begin),
          (lt,":set_event",7),#random mercs .... 5% default
          (try_begin),
            (ge,":leader_wealth",80000),
			(assign,":spawn_town",0),
			(try_for_range, ":town_cur", centers_begin, centers_end),
				(eq,":spawn_town",0),
				(this_or_next|party_slot_eq,":town_cur",slot_party_type, spt_town),
				(party_slot_eq,":town_cur",slot_party_type, spt_castle),
				(party_slot_eq, ":town_cur", slot_town_lord, ":leader"),
				(assign,":spawn_town",":town_cur"),#choose a center the leader owns
			(try_end),
			(gt,":spawn_town",0),
			(call_script, "script_occc_factional_roaming_party",":spawn_town","pt_occc_random_mercenaries",":faction_no",6),  #up to 6 party
			(try_begin),
				(gt,reg0, 0),
				(assign,":party_no",reg0),
				#
				(party_add_leader,":party_no","trp_ccd_veteran_hired_blade"),
				(store_random_in_range, ":randomtroops", "trp_watchman", "trp_mercenaries_end"),
				(store_random_in_range, ":randomnum", 18, 55),
				(party_add_members,":party_no",":randomtroops",":randomnum"),
				(store_random_in_range, ":randomtroops", "trp_watchman", "trp_mercenaries_end"),
				(store_random_in_range, ":randomnum", 18, 55),
				(party_add_members,":party_no",":randomtroops",":randomnum"),
				(store_random_in_range, ":randomtroops", "trp_watchman", "trp_mercenaries_end"),
				(store_random_in_range, ":randomnum", 18, 55),
				(party_add_members,":party_no",":randomtroops",":randomnum"),
				(store_random_in_range, ":randomtroops", "trp_watchman", "trp_mercenaries_end"),
				(store_random_in_range, ":randomnum", 18, 55),
				(party_add_members,":party_no",":randomtroops",":randomnum"),
				(store_random_in_range, ":randomtroops", "trp_watchman", "trp_mercenaries_end"),
				(store_random_in_range, ":randomnum", 18, 55),
				(party_add_members,":party_no",":randomtroops",":randomnum"),
				#
				(str_store_party_name,s1,":party_no"),
				(str_store_faction_name,s2,":faction_no"),
				(party_set_name, ":party_no", "@{s2}{s1}"),
				#they follow king
				(troop_get_slot, ":leaded_party", ":leader", slot_troop_leaded_party),
				(party_set_aggressiveness, ":party_no", 20),
				(party_set_helpfulness, ":party_no", 1000),        
				(party_set_ai_behavior, ":party_no", ai_bhvr_escort_party),
				(party_set_ai_object, ":party_no", ":leaded_party"),
				(party_set_slot, ":party_no", slot_party_commander_party, ":leaded_party"),
				(party_set_slot, ":party_no", slot_party_ai_substate, spai_accompanying_army),
				
				(faction_get_color,":color",":faction_no"),
				(display_message, "@{s0} has hired mercenary warband.", ":color"), #
			(try_end),
            (assign,":pay",10000),
          (try_end),
        (try_end),
        
        (gt,":pay",0),
        (val_mul,":pay",-1),
        (call_script,"script_ccc_change_troop_wealth",":leader",":pay"),
      (try_end),

	
	(assign,":spawned",0),
    (store_faction_of_party, ":townfactcheck", "p_town_7"),#praven
	(try_begin),#Arminius
	    (gt, "$g_ccd_option_spawn_bandit", 0),
		(eq, ":spawned", 0),
	    (store_random_in_range, ":rand_no", 0, 10),
        (eq, ":rand_no", 0),
        (eq, ":townfactcheck", "fac_kingdom_5"),
        (troop_slot_eq,"trp_occc_unique_bandit_hero01", slot_troop_occupation, slto_bandit),
        (call_script, "script_occc_new_factional_heroes_party_spawn","p_village_4","pt_occc_rhodok_rebels","fac_outlaws","trp_occc_unique_bandit_hero01"),  
		(neq,reg0,0),
		(assign,":spawned",1),
		(display_message, "@A mighty hero of barbarian, Arminius, has raised a rebellion against Rhodok Imperium!!", 0x57078e), #
    (try_end),
    (store_faction_of_party, ":townfactcheck", "p_town_15"),#Yalen
	(try_begin),#Spartacus
	    (gt, "$g_ccd_option_spawn_bandit", 0),
		(eq, ":spawned", 0),
	    (store_random_in_range, ":rand_no", 0, 10),
        (eq, ":rand_no", 0),
        (eq, ":townfactcheck", "fac_kingdom_5"),
        (troop_slot_eq,"trp_occc_unique_bandit_hero02", slot_troop_occupation, slto_bandit),
        (call_script, "script_occc_new_factional_heroes_party_spawn","p_village_23","pt_occc_rhodok_gladiators","fac_outlaws","trp_occc_unique_bandit_hero02"),  
		(neq,reg0,0),
		(assign,":spawned",1),
		(display_message, "@An ex-gladiator leader, Spartacus, has raised a rebellion against Rhodok Imperium!!", 0x57078e), #
    (try_end),#
	(try_begin),#Stevia, CtA like only
		(eq,"$g_occc_make_factions_medieval",1),#CtA like
	    (gt, "$g_ccd_option_spawn_bandit", 0),
		(eq, ":spawned", 0),
	    (store_random_in_range, ":rand_no", 0, 8),
        (eq, ":rand_no", 0),
		(store_random_in_range,":spawn_point",towns_begin,towns_end), 
		(store_faction_of_party, ":townfactcheck", ":spawn_point"),
		(neq, ":townfactcheck", "fac_kingdom_6"),
        (troop_slot_eq,"trp_occc_unique_bandit_hero04", slot_troop_occupation, slto_bandit),
        (call_script, "script_occc_new_factional_heroes_party_spawn","p_village_23","pt_occc_holy_crusaders_army","fac_holy_crusaders","trp_occc_unique_bandit_hero04"),  
		(neq,reg0,0),
		(str_store_party_name,s1,":spawn_point"),
		(display_message, "@Great army of holy crusaders went on crusade near {s1}!", 0x90ee90), #
	(try_end),
	(try_begin),#undead legion
		(eq,"$g_occc_make_factions_medieval",1),#CtA like
	    (gt, "$g_ccd_option_spawn_bandit", 0),
		(eq, ":spawned", 0),
	    (store_random_in_range, ":rand_no", 0, 6),
        (eq, ":rand_no", 0),
		(call_script, "script_occc_factional_roaming_party","p_undead_legio_spawn_point","pt_occc_undead_legion_legion","fac_revenants",1),
		(neq,reg0,0),
		(party_add_leader,reg0,"trp_occc_undead_legatus"),
		(assign,":spawned",1),
		(display_message, "@Undead Legion of Calradic revenants has risen!", 0x460076), #
	(try_end),
    
	(try_begin),#undead legion army
		(eq,"$g_occc_make_factions_medieval",1),#CtA like
	    (gt, "$g_ccd_option_spawn_bandit", 0),
		(eq, ":spawned", 0),
		(gt, ":now_day", 300),
	    (store_random_in_range, ":rand_no", 0, 20),
        (eq, ":rand_no", 0),
		(call_script, "script_occc_factional_roaming_party","p_undead_legio_spawn_point","pt_occc_undead_legion_boss","fac_revenants",1),
		(neq,reg0,0),
		(assign,":spawned",1),
		(party_add_leader,reg0,"trp_occc_unique_bandit_hero03"),
		(display_message, "@The ancient conqueror has returned, his army also awakens and marches once again!", 0x460076), #
	(try_end),

    (store_faction_of_party, ":townfactcheck", "p_town_23"),#Lirben
	(try_begin),#undead army
		(gt, "$g_ccd_option_spawn_bandit", 0),
		(gt, ":now_day", 180),

		#(eq, ":spawned", 0),
	    (store_random_in_range, ":rand_no", 0, 12),
        (eq, ":rand_no", 0),
        (eq, ":townfactcheck", "fac_kingdom_7"),
        (call_script, "script_occc_new_factional_heroes_party_spawn","p_village_57","pt_occc_dark_avengers","fac_outlaws","trp_occc_lich_king"),  
		(neq,reg0,0),
		(party_add_members,reg0,"trp_occc_skull_knight",12),
		(party_add_members,reg0,"trp_occc_demon_knight",30),
		(assign,":spawned",1),
		(display_message, "@Undead Army has risen near Lirben! They are threatening all mortal beings!", 0x000000), #
    (try_end),
	(try_begin),#black_khergit_army
		(gt, "$g_ccd_option_spawn_bandit", 0),
		(eq, ":spawned", 0),
		(eq,"$g_occc_additional_subfactions",1),
	    (store_random_in_range, ":rand_no", 0, 10),
        (call_script, "script_occc_new_factional_heroes_party_spawn","p_ccc_cave_dark_spawn_point","pt_black_khergit_army","fac_black_khergits","trp_occc_black_khergit_ataman"),  
		(neq,reg0,0),
		(assign,":spawned",1),
		(display_message, "@Black khergit Army has started an invasion into Calradia!!", 0x800000), #
    (try_end),
	(try_begin),#occc_calrador_army
		(gt, "$g_ccd_option_spawn_bandit", 0),
		(eq, ":spawned", 0),
		(eq,"$g_occc_additional_subfactions",1),
	    (store_random_in_range, ":rand_no", 0, 10),
        (call_script, "script_occc_new_factional_heroes_party_spawn","p_calrador_spawn_point","pt_occc_calrador_rangers","fac_calrador","trp_occc_calrador_twilight_knight"),  
		(neq,reg0,0),
		(assign,":spawned",1),
		(display_message, "@Calrador Army has risen, now they are sweeping their territory!!", 0x98FB98), #
    (try_end),

	#Restoration of Calradic Empire check
	(try_begin),
		(eq,"$occc_reclaim_calradic_empire",0),
		(call_script, "script_cf_occc_restortaion_of_calradic_empire_check"),
	(try_end),

    ]
  ),
  
  (24,#occc daily processes 
    [
	  (try_begin),
		  (gt, "$occc_relocate_hide_house_day", 0),
		  (val_sub, "$occc_relocate_hide_house_day", 1),
	  (try_end),

	  (try_begin),
		(gt, "$mobilize_militia_last_time", 0),
		(val_sub, "$mobilize_militia_last_time", 1),
	  (try_end),

	  (try_begin),
		  (gt, "$occc_days_to_supply_items", 0),
		  (val_sub, "$occc_days_to_supply_items", 1),
	  (try_end),

      (try_for_range, ":keeper_no", "trp_town_1_tavernkeeper", "trp_town_1_merchant"),#check tavernkeepers
        (troop_slot_ge, ":keeper_no", slot_troop_town_npc_mobilized, 1),#
		(troop_get_slot, ":cooldown", ":keeper_no", slot_troop_town_npc_mobilized),
        (val_sub, ":cooldown", 1),
		(troop_set_slot, ":keeper_no", slot_troop_town_npc_mobilized, ":cooldown"),
      (try_end),

      (try_for_range, ":keeper_no", companions_begin, companions_end),#check companions
        (troop_slot_ge, ":keeper_no", slot_troop_flirted_with, 1),#
		(troop_set_slot, ":keeper_no", slot_troop_flirted_with, 0),
      (try_end),

    ]
  ),

  (72,#occc 3 day processes
   [
    (call_script, "script_occc_update_exotic_trader"),
	]),

  
#sea flag from Brytenwalda
(.5, [    #trigger rewritten by motomataru occc .2->.5

   #other party icons
   (try_for_parties, ":cur_party"),
		(neq, ":cur_party", "p_main_party"),
		(party_get_template_id, ":cur_template", ":cur_party"),
		(party_get_icon, ":cur_icon", ":cur_party"),
		#(party_get_current_terrain, ":terrain", ":cur_party"),
		(try_begin),
		(call_script, "script_cf_is_party_on_water", ":cur_party"),
			(try_begin),
				(neq, ":cur_icon", "icon_ship"),
				#(neq, ":cur_icon", "icon_castle_snow_a"),
				(party_set_slot, ":cur_party", slot_party_save_icon, ":cur_icon"),
				(try_begin),
					(neq, ":cur_template", "pt_cattle_herd"),
					(party_set_icon, ":cur_party", "icon_ship"),
				(else_try),	#exception for wild animals
					#(party_set_icon, ":cur_party", "icon_castle_snow_a"),	#???
				(try_end),
				
				(this_or_next|eq, ":cur_template", "pt_occc_sea_raider_ship"),	#in case ships had "leaked" onto land
				(eq, ":cur_template", "pt_occc_jomsviking_raidship"),
				#(eq, ":cur_template", "pt_sea_traders"),
				(party_set_flags, ":cur_party", pf_is_ship, 1),
			(try_end),

		#not water terrain
		(else_try),
			(neq, ":cur_template", "pt_occc_sea_raider_ship"),	#hope these guys get in the water! Problem is they spawn on land...
			(neq, ":cur_template", "pt_occc_jomsviking_raidship"),

			#(this_or_next|eq, ":cur_icon", "icon_castle_snow_a"),	#exception for wild animals
			(eq, ":cur_icon", "icon_ship"),
			(try_begin),
				(eq, ":cur_template", "pt_occc_sea_raider_ship"),#temporarily set unused pt
				(party_set_icon, ":cur_party", "icon_gray_knight"),
				(party_set_flags, ":cur_party", pf_is_ship, 0),
			(else_try),
				(party_get_slot, ":new_icon", ":cur_party", slot_party_save_icon),
				(party_set_icon, ":cur_party", ":new_icon"),
			(try_end),
		# (else_try),
# (this_or_next|eq, ":cur_template", "pt_sea_raiders_ships"),
# (this_or_next|eq, ":cur_template", "pt_sea_raiders_ships2"),
# (eq, ":cur_template", "pt_sea_raiders_ships3"),
# (eq, ":cur_icon", "icon_ship"),
# (assign, reg0, ":cur_party"),
# (assign, reg1, ":cur_template"),
# (display_message, "@Party {reg0} type {reg1} sailing on land!"),
			# (try_begin),
				# (eq, ":cur_template", "pt_kingdom_hero_party"),
				# (party_set_icon,":cur_party","icon_flagbearer_a"),
			# (else_try),
				# (this_or_next|eq, ":cur_template", "pt_dplmc_gift_caravan"),
				# (this_or_next|eq, ":cur_template", "pt_player_loot_wagon"),
				# (eq, ":cur_template", "pt_kingdom_caravan_party"),
				# (party_set_icon,":cur_party","icon_mule"),
			# (else_try),
				# (this_or_next|eq, ":cur_template", "pt_dplmc_recruiter"),
				# (this_or_next|eq, ":cur_template", "pt_personal_messenger"),
				# (eq, ":cur_template", "pt_merchant_caravan"),
				# (party_set_icon,":cur_party","icon_gray_knight"),
			# (else_try),
				# (eq, ":cur_template", "pt_skirmish_party"),
				# (party_set_icon,":cur_party","icon_khergit"),
			# (else_try),
				# (this_or_next|eq, ":cur_template", "pt_sacerdotes_party"),
				# (this_or_next|eq, ":cur_template", "pt_paganos_party"),
				# (eq, ":cur_template", "pt_village_farmers"),
				# (party_set_icon,":cur_party","icon_peasant"),
			# (else_try),
				# (this_or_next|eq, ":cur_template", "pt_reinforcements"),
				# (this_or_next|eq, ":cur_template", "pt_manhunters"),
				# (this_or_next|eq, ":cur_template", "pt_new_template"),
				# (this_or_next|eq, ":cur_template", "pt_cado_template"),
				# (this_or_next|eq, ":cur_template", "pt_arrians"),
				# (this_or_next|eq, ":cur_template", "pt_eadfrith"),
				# (this_or_next|eq, ":cur_template", "pt_center_reinforcements"),
				# (this_or_next|eq, ":cur_template", "pt_looters"),
				# (this_or_next|eq, ":cur_template", "pt_forest_bandits"),
				# (this_or_next|eq, ":cur_template", "pt_steppe_bandits"),
				# (this_or_next|eq, ":cur_template", "pt_mountain_bandits"),
				# (this_or_next|eq, ":cur_template", "pt_sea_raiders2"),
				# (this_or_next|eq, ":cur_template", "pt_taiga_bandits"),
				# (this_or_next|eq, ":cur_template", "pt_deserters"),
				# #cambio parties navales
				# # (eq, ":cur_template", "pt_sea_raiders"),
				# (this_or_next|eq, ":cur_template", "pt_sea_raiders"),
				# (this_or_next|eq, ":cur_template", "pt_sea_raiders_ships"),
				# (this_or_next|eq, ":cur_template", "pt_sea_raiders_ships2"),
				# (eq, ":cur_template", "pt_sea_raiders_ships3"),
				# (party_set_icon,":cur_party","icon_axeman"),
			# (else_try),
				# (eq, ":cur_template", "pt_cattle_herd"),
				# (party_set_icon,":cur_party","icon_cattle"),
			# (try_end),
		(try_end),
	(try_end),	#try_for_parties
 ]),

   (24*30,#occc factional Domestic affairs
   [
	  (eq,"$g_occc_factional_expantion",1),
      (try_for_range, ":faction_no", npc_kingdoms_begin, npc_kingdoms_end),
		#(this_or_next|eq,":faction_no","fac_kingdom_7"),
		#################
		#RHODOK IMPERIUM#
		#################
		(eq,":faction_no","fac_kingdom_5"),
        (faction_slot_eq, ":faction_no", slot_faction_state, sfs_active),
		(faction_slot_ge, "fac_kingdom_5", slot_faction_doctrine_level, 0),#not -1
        (faction_get_slot, ":leader",":faction_no", slot_faction_leader),
        (troop_get_slot, ":leader_wealth", ":leader", slot_troop_wealth),
        (ge,":leader_wealth",20000),
        (str_store_troop_name,s0,":leader"),
        (assign,":pay",0),
        (store_random_in_range,":set_event",0,100),
        (try_begin),
          (lt,":set_event",25),
          (try_begin),
            (call_script,"script_ccc_faction_event_build_wall",":faction_no",25),
			(gt,reg0,0),
            (val_add,":pay",reg0),
            #(assign,reg1,":pay"),
			(faction_get_color, ":faction_color", ":faction_no"),
			(str_store_troop_name,s1,":leader"),
            (display_message,"@{s1} funded to build {s0} in {s11}.", ":faction_color"),
          (try_end),
        (else_try),
          #no event
        (try_end),
        
        (gt,":pay",0),
        (val_mul,":pay",-1),
        (call_script,"script_ccc_change_troop_wealth",":leader",":pay"),
      (try_end),
	  
		#Fall of the Empire check
	  (try_begin),
		(eq,"$g_occc_make_factions_medieval",4),#in v0.2fix3, this function is called only in the Fall of the Empire Scenario
		(call_script, "script_cf_occc_transformation_of_rhodok_empire"),
	  (try_end),

   ]),
   
  (48,#occc heroes rejoin check - temporary bug fix
    [
	(try_begin),#if the player character should have gotten slain through bug, this process tries to recover
        (party_stack_get_troop_id, ":mainparty_leader", "p_main_party", 0),
		(neq,":mainparty_leader","trp_player"),
		(eq,"$freelancer_state",0),
		
		#using freelancer backup temporary
       	(call_script, "script_party_copy", "p_freelancer_party_backup", "p_main_party"),
		(remove_member_from_party, "trp_player","p_freelancer_party_backup"),
		
		#clear main party all
        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
        (try_for_range_backwards, ":cur_stack", 0, ":num_stacks"), 
           (party_stack_get_troop_id, ":cur_troops", "p_main_party", ":cur_stack"),
           (party_stack_get_size, ":cur_size", "p_main_party", ":cur_stack"),
           (party_remove_members, "p_main_party", ":cur_troops", ":cur_size"),
        (try_end),

		#make player character rejoin
		#(party_add_leader,"p_main_party","trp_player"),
		(party_add_members, "p_main_party", "trp_player", 1),

		#restore main party
        (party_get_num_companion_stacks, ":num_stacks", "p_freelancer_party_backup"),
        (try_for_range, ":cur_stack", 0, ":num_stacks"),
			(assign, ":stack_amount", 0),
			(party_stack_get_troop_id, ":return_troop", "p_freelancer_party_backup", ":cur_stack"),
			(neq, ":return_troop", "trp_player"),
			(try_begin),
				(troop_is_hero, ":return_troop"), #bugfix for companions (simple, they always return)
				(assign, ":stack_amount", 1),
			(else_try),
				(party_stack_get_size, ":stack_size", "p_freelancer_party_backup", ":cur_stack"),
				(assign, ":stack_amount", ":stack_size"),
			(try_end),
			(ge, ":stack_amount", 1),
			(party_add_members, "p_main_party", ":return_troop", ":stack_amount"),
        (try_end),
		(party_clear, "p_freelancer_party_backup"),
		
		#recover message
        (display_message, "@OCCC RECOVERING:Your player character rejoined your own party."),

	(try_end),
	
   (try_for_range, ":companion", companions_begin, companions_end),
		(try_begin),
			#(troop_get_slot, ":days_left", ":companion", slot_troop_days_on_mission),
			(troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),
			(try_begin),
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_kingsupport),
			(else_try),
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_gather_intel),
			(else_try),	#This covers most diplomatic missions
				(troop_slot_ge, ":companion", slot_troop_current_mission, npc_mission_peace_request),
				##diplomacy begin
				(neg|troop_slot_eq, ":companion", slot_troop_current_mission, 8),
        		##diplomacy end
			(else_try),
				(eq, ":companion", "$g_player_minister"),
			(else_try),
				(main_party_has_troop, ":companion"),
			(else_try),
				(troop_slot_eq, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),
			(else_try),	#Companions who are in a center
				(troop_slot_ge, ":companion", slot_troop_cur_center, 1),
	        (else_try), #Excludes companions who have occupation = retirement
                (try_begin),
                  (check_quest_active, "qst_lend_companion"),
                  (quest_slot_eq, "qst_lend_companion", slot_quest_target_troop, ":companion"),
                (else_try),
                  (check_quest_active, "qst_lend_surgeon"),
                  (quest_slot_eq, "qst_lend_surgeon", slot_quest_target_troop, ":companion"),
                (else_try),
				  (troop_set_slot, ":companion", slot_troop_current_mission, npc_mission_rejoin_when_possible),#rejoin
                (try_end),
                
			(try_end),
		(else_try),
		    #CC-C begin
			#(neg|troop_slot_eq, ":companion", slot_troop_occupation, slto_kingdom_hero),
			(troop_slot_eq, ":companion", slot_troop_occupation, slto_player_companion),
			#CC-C end
			(troop_slot_ge, ":companion", slot_troop_prisoner_of_party, centers_begin),

		(try_end),
   (try_end),

    ]
  ),
  
  
  ## rhodoks check and independence Occc Party_Troop_Ratio_Check
  (24,
    [
        
       #player
	   	(call_script,"script_occc_party_rhodok_percentage","p_main_party"),
        (party_set_slot, "p_main_party", slot_party_rhodok_percentage, reg0),
       #npcs
       (try_for_range, ":troop_no", active_npcs_begin,active_npcs_end),
		(troop_get_slot, ":party_no", ":troop_no", slot_troop_leaded_party),
		(this_or_next|eq,":troop_no","trp_player"),
		(ge,":party_no",1),
		(party_is_active, ":party_no"),
		(call_script,"script_occc_party_rhodok_percentage",":party_no"),
		(party_set_slot, ":party_no", slot_party_rhodok_percentage, reg0),
       (try_end),

      (gt, "$g_ccd_faction_restoration", -1),  ## CC-D add
      (try_for_range, ":cur_faction", "fac_kingdom_14", npc_kingdoms_end),#try only additional sub factions
        (faction_get_slot, ":inactive_days", ":cur_faction", slot_faction_inactive_days),
        (try_begin),
          (neg|faction_slot_eq, ":cur_faction", slot_faction_state, sfs_active),
          (val_add, ":inactive_days", 1),
        (else_try),
          (assign, ":inactive_days", 0),
        (try_end),
        (faction_set_slot, ":cur_faction", slot_faction_inactive_days, ":inactive_days"),
        (gt, ":inactive_days", "$g_ccd_faction_restoration"),  ## CC-D 20->$g_ccd_faction_restoration
        #(troop_get_slot, ":pretender_original_faction", "$supported_pretender",  slot_troop_original_faction),
        #(neq, ":pretender_original_faction", ":cur_faction"),
        
        (assign, ":fitful_faction", -1),
        (assign, ":fitful_lords", 0),
        (try_for_range, ":faction_2", npc_kingdoms_begin, npc_kingdoms_end),
          (neq, ":faction_2", ":cur_faction"),
          #(neq, ":faction_2", ":pretender_original_faction"),
          (faction_slot_eq, ":faction_2", slot_faction_state, sfs_active),
          (assign, ":fitful_lords_this_faction", 0),
          (try_for_range, ":cur_troop", lords_begin, lords_end),
            (troop_get_slot, ":troop_original_faction", ":cur_troop", slot_troop_original_faction),
            (eq, ":troop_original_faction", ":cur_faction"),
            (store_troop_faction, ":troop_cur_faction", ":cur_troop"),
            (this_or_next|eq, ":troop_cur_faction", ":faction_2"),
            (eq, ":troop_cur_faction", "fac_outlaws"),
            (val_add, ":fitful_lords_this_faction", 1),
          (try_end),
          # centers 
          (assign, ":fitful_centers", 0),
          (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
            (party_get_slot, ":center_lord", ":center_no", slot_town_lord),
            (ge, ":center_lord", 1),
            (store_troop_faction, ":troop_cur_faction", ":center_lord"),
            (eq, ":troop_cur_faction", ":faction_2"),
            (troop_get_slot, ":troop_original_faction", ":center_lord", slot_troop_original_faction),
            (eq, ":troop_original_faction", ":cur_faction"),
            (val_add, ":fitful_centers", 1),
            (try_begin),
              (party_slot_eq, ":center_no", slot_party_type, spt_town),
              (val_add, ":fitful_centers", 1),
            (try_end),
          (try_end),
          (try_begin),
            (ge, ":fitful_centers", 3),
            (gt, ":fitful_lords_this_faction", ":fitful_lords"),
            (assign, ":fitful_lords", ":fitful_lords_this_faction"),
            (assign, ":fitful_faction", ":faction_2"),
          (try_end),
        (try_end),
        #(try_begin),
          #(lt, ":fitful_lords", 5),
          #(assign, ":fitful_faction", -1),
        #(try_end),
        
        (gt, ":fitful_faction", -1),
        (faction_get_slot, ":original_king", ":cur_faction", slot_faction_leader),
		(ge,":original_king",1),
        #(store_sub, ":kp_offset", pretenders_begin, kings_begin),
        #(try_begin),
          #(eq,":original_king","trp_kingdom_14_lord"),#Artorius returns!
        #(try_end),
	  	(faction_slot_eq, ":cur_faction", slot_faction_will_independence_event_occur, 1),#only one time the event occurs
        (neg|troop_slot_eq, ":original_king", slot_troop_occupation, dplmc_slto_dead),
        ## CC-D end
        (call_script, "script_change_troop_faction", ":original_king", ":cur_faction"),
        (troop_set_slot, ":original_king", slot_troop_occupation, slto_kingdom_hero),
        (faction_set_slot, ":cur_faction", slot_faction_leader, ":original_king"),  ## CC-D add
		(faction_set_slot, ":cur_faction", slot_faction_will_independence_event_occur, 0),
        (call_script, "script_add_notification_menu", "mnu_notification_kingdom_independence_common", ":cur_faction", ":fitful_faction"),
      (try_end),
    ]),

#imported processes from brytenwalda

######prisioneros acaba
#####Ikaguia chief bardo entretenimiento acaba
   #entertainment party morale bonus
     (24, [

       (assign, ":entertain_bonus", 0),
       #companions
       (store_party_size_wo_prisoners, reg0, "p_main_party"),
       (try_begin),
           (gt, reg0, 1),
           (try_for_range, ":hero", companions_begin, companions_end),
               (main_party_has_troop,":hero"),
               (store_skill_level,":skill","skl_performing",":hero"),
               (store_mul, reg0, ":skill", ":skill"),     #higher skill has bigger effect
               (val_add, ":entertain_bonus", reg0),
           (try_end),
           #player troop
           (store_skill_level,":skill","skl_performing","trp_player"),
           (store_mul, reg0, ":skill", ":skill"),     #higher skill has bigger effect
           (val_add, ":entertain_bonus", reg0),
           #now get the bonus
           (assign, reg0, ":entertain_bonus"),
           (convert_to_fixed_point, reg0),
           (store_sqrt, ":entertain_bonus", reg0),
           (convert_from_fixed_point, ":entertain_bonus"),
           (val_mul, ":entertain_bonus", "$entertainement_on"), #normal kind is 1 but if it is an aewsome entertainement it will get a bonus (like playing lordly/royal musics)
           (val_div, ":entertain_bonus", 2),     #every two skill level gives a morale point (normally)
           #and apply it
           (try_begin),
               (gt, ":entertain_bonus", 0),
               (display_message, "@Your troops enjoy the entertainment you and your companions give them."),
               (call_script, "script_change_player_party_morale", ":entertain_bonus"),
           (else_try),
               #(display_message, "@Your troops wish you and your companions would provide more entertainment."),
               (lt, "$entertainement_on", 1),
              # (call_script, "script_change_player_party_morale", -1), #Moto, if a player wantnt be bard, should we do him have entertain skill?
           (try_end),
       (try_end),    #party size > 1
       (assign, "$entertainement_on", 0),    #init for new day
   ]),

      ( 1, #rigale peasantry timelapse
  [
  (try_begin),
        (this_or_next|eq, "$g_player_is_captive", 1),
        (this_or_next|party_slot_eq, "$current_town", slot_village_state, svs_being_raided),
        (party_slot_ge, "$current_town", slot_village_infested_by_bandits, 1),

        # (gt,"$g_work_for_village_ongoing",1),        
               (gt,"$g_work_for_village_ongoing",0),    #MOTO chief avoid      successful conclusion
  (assign,"$g_work_for_village_ongoing", 0),
		(rest_for_hours,0,0,0),
     	(jump_to_menu,"mnu_village_basic_work"),
  (else_try),
		 (gt,"$g_work_for_village_ongoing",1),
		 (val_sub, "$g_work_for_village_ongoing", 1),
		 (store_random_in_range,":show_overrall_message",1,5),
		 (try_begin),		 
			 (eq,":show_overrall_message",1),
			(display_message,"@You keep working hard for this village...",0x66CC33),		 
		 (try_end),
		 		 (rest_for_hours,2,5,0),
	(else_try), 
		 (eq,"$g_work_for_village_ongoing",1),
		 (display_message,"@Your strenuous village work ends.",),
		 (rest_for_hours,0,0,0),
		 (val_sub, "$g_work_for_village_ongoing", 1),
		(jump_to_menu,"mnu_village_basic_work"),
	 (try_end),	
	]
  ),
###chief acaba rigale


   (240,#nerf for hellas
     [

       #walled centers
       (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
         (party_get_slot, ":town_lord", ":center_no", slot_town_lord),
         (neq, ":town_lord", "trp_knight_8_1"), #center does not belong to leonidas.
         (neq, ":town_lord", "trp_player"), #center does not belong to player.
         (ge, ":town_lord", 1), #center belongs to someone.
         (store_troop_faction,":faction_no",":town_lord"),
         (neq,":faction_no","fac_player_supporters_faction"),
         (party_get_num_companion_stacks, ":num_stacks",":center_no"),
         (try_for_range, ":i_stack", 0, ":num_stacks"),
			 (party_stack_get_troop_id, ":troop_id", ":center_no", ":i_stack"),
			 (is_between,":troop_id","trp_ore_spartanwarrior","trp_occc_amazon_huntress"),#spartan warriors
			 (party_stack_get_size, ":stack_size",":center_no",":i_stack"),                             
			 (party_remove_members, ":center_no", ":troop_id", ":stack_size"),
			 (try_begin),
				(eq,":troop_id","trp_ore_spartanwarrior"),#Hellas_Spartan
				(party_add_members, ":center_no","trp_ccc_swadian_conquistador", ":stack_size"),#perioikoi
			 (else_try),
				(eq,":troop_id","trp_ore_spartanvetwarrior"),#Hellas_Legend_Spartan
				(party_add_members, ":center_no","trp_mountain_bandit_spartan", ":stack_size"),#Young Spartan
			 (try_end),
         (try_end),

       (try_end),
     ]),
	 	 
	#factional expantion!
   (24*5,#Occc nomad_camp_check
     [
		(eq, "$g_occc_factional_expantion", 1),#khergit factional expantion!

		(try_for_parties,":current_party"),
			(party_slot_eq, ":current_party",slot_mongol_camp_status,status_stationed),
			(party_get_template_id, ":template", ":current_party"),
			(eq,":template","pt_occc_nomad_camp"),
            (store_random_in_range, ":rand", 5, 19),
		    (party_set_slot, ":current_party", slot_center_volunteer_troop_amount, ":rand"),
		(try_end),
		
	 	(store_num_parties_of_template, ":num_parties", "pt_occc_nomad_camp"),
		(try_begin),
			(lt,":num_parties", 3),#nomad camps are below 3
			(call_script, "script_occc_spawn_nomads"),#try to spawn nomad camps
		(try_end),
		
		]),

##occc end 
]
# modmerger_start version=201 type=2
try:
    component_name = "simple_triggers"
    var_set = { "simple_triggers" : simple_triggers }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end

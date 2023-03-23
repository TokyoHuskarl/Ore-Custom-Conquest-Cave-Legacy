from header_common import *
from module_constants import *
from header_operations import *
from header_triggers import *

scripts = [

################################################################################
# [OSP] Advanced Soldier Management in Exchange Screens by Leonion
#   https://forums.taleworlds.com/index.php?topic=361448.0
################################################################################
# After Battle
#   LCtrl +A     +[button]  :take all prisoners
#   LCtrl +S     +[button]  :take all soldiers
# Manage Garrison
#   LCtrl +A     +[button]  :take all prisoners
#   LCtrl +D     +[button]  :put all prisoners
#   RCtrl +Right +[button]  :take all soldiers
#   RCtrl +Left  +[button]  :put all soldiers
#   ArrowUp      +[button]  :move selected soldiers up inside garrison
#   ArrowDown    +[button]  :move selected soldiers down inside garrison
#   PageUp       +[button]  :move selected soldiers to the top of garrison
#   PageDown     +[button]  :move selected soldiers to the bottom of garrison
################################################################################

  ("initialize_exchange_screen_extensions",
   [
    (store_script_param, ":troop_id", 1),
    
    ## CC-D begin: cave limit break, and delete the process of covering garrison shift
    (try_begin), #MASS PRISONER TRANSFER AFTER BATTLE
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 10),
      (eq, "$g_adv_transfer_mode", 10),  # after battle
      (key_is_down, key_left_control),
      (key_is_down, key_a),
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_temp_party"),
    #  (assign, ":stop_stack", -1),
    #  (assign, ":stop_no", -1),
      (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
    #    (eq, ":stop_stack", -1),
    #    (party_get_free_prisoners_capacity, ":player_prisoner_capacity", "p_main_party"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_prisoner_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
    #    (try_begin),
    #      (ge, ":player_prisoner_capacity", ":stack_size"),
          (party_add_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
    #    (else_try),
    #      (party_add_prisoners, "p_main_party", ":stack_troop", ":player_prisoner_capacity"),
    #      (assign, ":stop_stack", ":stack_no"),
    #      (assign, ":stop_no", ":player_prisoner_capacity"),
    #    (try_end),
      (try_end),
    #  (try_begin),
    #    (neq, ":stop_stack", -1),
    #    (store_add, ":stop_stack_plus_one", ":stop_stack", 1),
    #  (else_try),
        (assign, ":stop_stack_plus_one", ":num_prisoner_stacks"),
    #  (try_end),
      (try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_prisoner_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
    #    (try_begin),
    #      (neq, ":stop_no", -1),
    #      (eq, ":stack_no", ":stop_stack"),
    #      (party_remove_prisoners, "p_temp_party", ":stack_troop", ":stop_no"),
    #    (else_try),
          (party_remove_prisoners, "p_temp_party", ":stack_troop", ":stack_size"),
    #    (try_end),
      (try_end),
    #(try_end),  # avoid some inputs at the same time
    #++++++++++++++++++++++++++++++++++++++++++++++++ MASS TRANSFER OF RESCUED PRISONERS AFTER BATTLE
    (else_try),  #(try_begin),  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 10),
      (eq, "$g_adv_transfer_mode", 10),  # after battle
      (key_is_down, key_left_control),
      (key_is_down, key_s),
      (party_get_num_companion_stacks, ":num_companion_stacks", "p_temp_party"),
    #  (assign, ":stop_stack", -1),
    #  (assign, ":stop_no", -1),
      (try_for_range, ":stack_no", 0, ":num_companion_stacks"),
    #    (eq, ":stop_stack", -1),
    #    (party_get_free_companions_capacity, ":player_companion_capacity", "p_main_party"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":stack_no"),
    #    (try_begin),
    #      (ge, ":player_companion_capacity", ":stack_size"),
          (party_add_members, "p_main_party", ":stack_troop", ":stack_size"),
          (party_wound_members, "p_main_party", ":stack_troop", ":stack_no_wounded"),
    #    (else_try),
    #      (party_add_members, "p_main_party", ":stack_troop", ":player_companion_capacity"),
    #      (assign, ":stop_stack", ":stack_no"),
    #      (assign, ":stop_no", ":player_companion_capacity"),
    #      (val_add, ":stack_no_wounded", ":player_companion_capacity"),
    #      (store_sub, ":excess", ":stack_no_wounded", ":stack_size"), #party_remove_members first removes healthy members, so we need to find whether any sick members get transfered
    #      (val_max, ":excess", 0),
    #      (party_wound_members, "p_main_party", ":stack_troop", ":excess"),
    #    (try_end),
      (try_end),
    #  (try_begin),
    #    (neq, ":stop_stack", -1),
    #    (store_add, ":stop_stack_plus_one", ":stop_stack", 1),
    #  (else_try),
        (assign, ":stop_stack_plus_one", ":num_companion_stacks"),
    #  (try_end),
      (try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
    #    (try_begin),
    #      (neq, ":stop_no", -1),
    #      (eq, ":stack_no", ":stop_stack"),
    #      (party_remove_members, "p_temp_party", ":stack_troop", ":stop_no"),
    #    (else_try),
          (party_remove_members, "p_temp_party", ":stack_troop", ":stack_size"),
    #    (try_end),
      (try_end),
    (try_end),
    #++++++++++++++++++++++++++++++++++++++++++++++++ SORTING GARRISONS
    (try_begin), #ARROW UP
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      #(troop_slot_eq, "trp_globals_troop", slot_last_requested_troop, ":troop_id"),
      (eq, "$g_last_requested_troop", ":troop_id"),
      (key_is_down, key_up),
      (party_clear, "p_temp_party"),
      (call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
      (party_get_num_companion_stacks, ":num_stacks", "$current_town"),
      (assign, ":key_stack", -1),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (try_begin),
          (eq, ":stack_troop", ":troop_id"),
          (neq, ":stack_no", 0), #key_up can't be used with stack 0
          (assign, ":key_stack", ":stack_no"),
        (try_end),
      (try_end),
      (neq, ":key_stack", -1),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (party_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
        (party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
      (try_end),
      (store_sub, ":key_stack_minus_one", ":key_stack", 1),
      (store_add, ":key_stack_plus_one", ":key_stack", 1),
      (try_for_range, ":stack_no", 0, ":key_stack_minus_one"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":stack_no"),
        (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
        (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_end),
      (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":key_stack"),
      (party_stack_get_size, ":stack_size", "p_temp_party", ":key_stack"),
      (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":key_stack"),
      (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
      (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
    #  (assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
    #  (try_begin),
    #    (ge, ":stack_no_wounded", 1),
    #    (assign, ":first_party_member_was_wounded", 1),
    #  (try_end),
    #  (party_get_num_companion_stacks, ":num_stacks_in_main_party", "p_main_party"),
    #  (try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
    #    (party_stack_get_troop_id, ":stack_troop_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (eq, ":stack_troop_in_main_party", ":troop_id"),
    #    (party_stack_get_size, ":stack_size_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (party_stack_get_num_wounded, ":stack_no_wounded_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (try_begin),
    #      (eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
    #      (gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
    #      (store_sub, ":stack_size_in_main_party_minus_1" , ":stack_size_in_main_party", 1),
    #      (store_sub, ":stack_no_wounded_in_main_party_minus_2" , ":stack_no_wounded_in_main_party", 2),
    #      (party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
    #    (else_try),
    #      (eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
    #      (assign, ":first_party_member_was_wounded", 1),
    #    (try_end), 
    #  (try_end),
      (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":key_stack_minus_one"),
      (party_stack_get_size, ":stack_size", "p_temp_party", ":key_stack_minus_one"),
      (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":key_stack_minus_one"),
      (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
      (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_for_range, ":stack_no", ":key_stack_plus_one", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":stack_no"),
        (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
        (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_end),
    #  (party_remove_members, "p_main_party", ":troop_id", 1),
    #  (party_add_members, "$current_town", ":troop_id", 1),
    #  (try_begin),
    #    (eq, ":first_party_member_was_wounded", 1), #restoring the balance in town
    #    (party_wound_members, "$current_town", ":troop_id", 1),
    #  (try_end),
    #(try_end),  # avoid some inputs at the same time
    
    (else_try),  #(try_begin), #ARROW DOWN  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      #(troop_slot_eq, "trp_globals_troop", slot_last_requested_troop, ":troop_id"),
      (eq, "$g_last_requested_troop", ":troop_id"),
      (key_is_down, key_down),
      (party_clear, "p_temp_party"),
      (call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
      (party_get_num_companion_stacks, ":num_stacks", "$current_town"),
      (store_sub, ":num_stacks_minus_one", ":num_stacks", 1),
      (assign, ":key_stack", -1),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (try_begin),
          (eq, ":stack_troop", ":troop_id"),
          (neq, ":stack_no", ":num_stacks_minus_one"), #key_down can't be used with last stack
          (assign, ":key_stack", ":stack_no"),
        (try_end),
      (try_end),
      (neq, ":key_stack", -1),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (party_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
        (party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
      (try_end),
      (store_add, ":key_stack_plus_one", ":key_stack", 1),
      (store_add, ":key_stack_plus_two", ":key_stack", 2),
      (try_for_range, ":stack_no", 0, ":key_stack"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":stack_no"),
        (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
        (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_end),
      (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":key_stack_plus_one"),
      (party_stack_get_size, ":stack_size", "p_temp_party", ":key_stack_plus_one"),
      (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":key_stack_plus_one"),
      (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
      (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":key_stack"),
      (party_stack_get_size, ":stack_size", "p_temp_party", ":key_stack"),
      (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":key_stack"),
      (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
      (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
    #  (assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
    #  (try_begin),
    #    (ge, ":stack_no_wounded", 1),
    #    (assign, ":first_party_member_was_wounded", 1),
    #  (try_end),
    #  (party_get_num_companion_stacks, ":num_stacks_in_main_party", "p_main_party"),
    #  (try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
    #    (party_stack_get_troop_id, ":stack_troop_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (eq, ":stack_troop_in_main_party", ":troop_id"),
    #    (party_stack_get_size, ":stack_size_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (party_stack_get_num_wounded, ":stack_no_wounded_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (try_begin),
    #      (eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
    #      (gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
    #      (store_sub, ":stack_size_in_main_party_minus_1" , ":stack_size_in_main_party", 1),
    #      (store_sub, ":stack_no_wounded_in_main_party_minus_2" , ":stack_no_wounded_in_main_party", 2),
    #      (party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
    #    (else_try),
    #      (eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
    #      (assign, ":first_party_member_was_wounded", 1),
    #    (try_end), 
    #  (try_end),
      (try_for_range, ":stack_no", ":key_stack_plus_two", ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":stack_no"),
        (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
        (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_end),
    #  (party_remove_members, "p_main_party", ":troop_id", 1),
    #  (party_add_members, "$current_town", ":troop_id", 1),
    #  (try_begin),
    #    (eq, ":first_party_member_was_wounded", 1),
    #    (party_wound_members, "$current_town", ":troop_id", 1),
    #  (try_end),
    #(try_end),  # avoid some inputs at the same time
    
    (else_try),  #(try_begin), #PAGE UP  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      #(troop_slot_eq, "trp_globals_troop", slot_last_requested_troop, ":troop_id"),
      (eq, "$g_last_requested_troop", ":troop_id"),
      (key_is_down, key_page_up),
      (party_clear, "p_temp_party"),
      (call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
      (party_get_num_companion_stacks, ":num_stacks", "$current_town"),
      (assign, ":key_stack", -1),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (try_begin),
          (eq, ":stack_troop", ":troop_id"),
          (neq, ":stack_no", 0), #key_page_up can't be used with stack 0
          (assign, ":key_stack", ":stack_no"),
        (try_end),
      (try_end),
      (neq, ":key_stack", -1),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (party_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
        (party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
      (try_end),
      (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":key_stack"),
      (party_stack_get_size, ":stack_size", "p_temp_party", ":key_stack"),
      (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":key_stack"),
      (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
      (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
    #  (assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
    #  (try_begin),
    #    (ge, ":stack_no_wounded", 1),
    #    (assign, ":first_party_member_was_wounded", 1),
    #  (try_end),
    #  (party_get_num_companion_stacks, ":num_stacks_in_main_party", "p_main_party"),
    #  (try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
    #    (party_stack_get_troop_id, ":stack_troop_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (eq, ":stack_troop_in_main_party", ":troop_id"),
    #    (party_stack_get_size, ":stack_size_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (party_stack_get_num_wounded, ":stack_no_wounded_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (try_begin),
    #      (eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
    #      (gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
    #      (store_sub, ":stack_size_in_main_party_minus_1" , ":stack_size_in_main_party", 1),
    #      (store_sub, ":stack_no_wounded_in_main_party_minus_2" , ":stack_no_wounded_in_main_party", 2),
    #      (party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
    #    (else_try),
    #      (eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
    #      (assign, ":first_party_member_was_wounded", 1),
    #    (try_end), 
    #  (try_end),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (neq, ":stack_no", ":key_stack"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":stack_no"),
        (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
        (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_end),
    #  (party_remove_members, "p_main_party", ":troop_id", 1),
    #  (party_add_members, "$current_town", ":troop_id", 1),
    #  (try_begin),
    #    (eq, ":first_party_member_was_wounded", 1),
    #    (party_wound_members, "$current_town", ":troop_id", 1),
    #  (try_end),
    #(try_end),  # avoid some inputs at the same time
    
    (else_try),  #(try_begin), #PAGE DOWN  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      #(troop_slot_eq, "trp_globals_troop", slot_last_requested_troop, ":troop_id"),
      (eq, "$g_last_requested_troop", ":troop_id"),
      (key_is_down, key_page_down),
      (party_clear, "p_temp_party"),
      (call_script, "script_party_add_party_companions", "p_temp_party", "$current_town"),
      (party_get_num_companion_stacks, ":num_stacks", "$current_town"),
      (store_sub, ":num_stacks_minus_one", ":num_stacks", 1),
      (assign, ":key_stack", -1),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (try_begin),
          (eq, ":stack_troop", ":troop_id"),
          (neq, ":stack_no", ":num_stacks_minus_one"), #key_down can't be used with last stack
          (assign, ":key_stack", ":stack_no"),
        (try_end),
      (try_end),
      (neq, ":key_stack", -1),
      (try_for_range_backwards, ":stack_no", 0, ":num_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (party_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
        (party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
      (try_end),
      (try_for_range, ":stack_no", 0, ":num_stacks"),
        (neq, ":stack_no", ":key_stack"),
        (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":stack_no"),
        (party_stack_get_size, ":stack_size", "p_temp_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":stack_no"),
        (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
        (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_end),
      (party_stack_get_troop_id, ":stack_troop", "p_temp_party", ":key_stack"),
      (party_stack_get_size, ":stack_size", "p_temp_party", ":key_stack"),
      (party_stack_get_num_wounded, ":stack_no_wounded", "p_temp_party", ":key_stack"),
      (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
      (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
    #  (assign, ":first_party_member_was_wounded", 0), #we're trying to understand if the first party member that got transferred by the player (action that launches the script) was wounded
    #  (try_begin),
    #    (ge, ":stack_no_wounded", 1),
    #    (assign, ":first_party_member_was_wounded", 1),
    #  (try_end),
    #  (party_get_num_companion_stacks, ":num_stacks_in_main_party", "p_main_party"),
    #  (try_for_range, ":stack_in_main_party", 0, ":num_stacks_in_main_party"),
    #    (party_stack_get_troop_id, ":stack_troop_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (eq, ":stack_troop_in_main_party", ":troop_id"),
    #    (party_stack_get_size, ":stack_size_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (party_stack_get_num_wounded, ":stack_no_wounded_in_main_party", "p_main_party", ":stack_in_main_party"),
    #    (try_begin),
    #      (eq, ":first_party_member_was_wounded", 1), #restoring the balance in main party
    #      (gt, ":stack_size_in_main_party", ":stack_no_wounded_in_main_party"),
    #      (store_sub, ":stack_size_in_main_party_minus_1" , ":stack_size_in_main_party", 1),
    #      (store_sub, ":stack_no_wounded_in_main_party_minus_2" , ":stack_no_wounded_in_main_party", 2),
    #      (party_remove_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_add_members, "p_main_party", ":troop_id", ":stack_size_in_main_party_minus_1"),
    #      (party_wound_members, "p_main_party", ":stack_troop_in_main_party", ":stack_no_wounded_in_main_party_minus_2"),
    #    (else_try),
    #      (eq, ":stack_no_wounded_in_main_party", ":stack_size_in_main_party"), #the only case when we will remove a sick member, but add (unless it's corrected) a healthy one
    #      (assign, ":first_party_member_was_wounded", 1),
    #    (try_end), 
    #  (try_end),
    #  (party_remove_members, "p_main_party", ":troop_id", 1),
    #  (party_add_members, "$current_town", ":troop_id", 1),
    #  (try_begin),
    #    (eq, ":first_party_member_was_wounded", 1),
    #    (party_wound_members, "$current_town", ":troop_id", 1),
    #  (try_end),
    #(try_end),  # avoid some inputs at the same time
    #++++++++++++++++++++++++++++++++++++++++++++++++ MASSIVE TRANSFERS TO/FROM GARRISON
    (else_try),  #(try_begin), #TROOPS FROM GARRISON TO PLAYER'S PARTY  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      (key_is_down, key_right_control),
      (key_is_down, key_right),
      (party_get_num_companion_stacks, ":num_companion_stacks", "$current_town"),
    #  (assign, ":stop_stack", -1),
    #  (assign, ":stop_no", -1),
      (try_for_range, ":stack_no", 0, ":num_companion_stacks"),
    #    (eq, ":stop_stack", -1),
    #    (party_get_free_companions_capacity, ":player_companion_capacity", "p_main_party"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (party_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "$current_town", ":stack_no"),
    #    (try_begin),
    #      (ge, ":player_companion_capacity", ":stack_size"),
          (party_add_members, "p_main_party", ":stack_troop", ":stack_size"),
          (party_wound_members, "p_main_party", ":stack_troop", ":stack_no_wounded"),
    #    (else_try),
    #      (party_add_members, "p_main_party", ":stack_troop", ":player_companion_capacity"),
    #      (assign, ":stop_stack", ":stack_no"),
    #      (assign, ":stop_no", ":player_companion_capacity"),
    #      (val_add, ":stack_no_wounded", ":player_companion_capacity"),
    #      (store_sub, ":excess", ":stack_no_wounded", ":stack_size"), #party_remove_members first removes healthy members, so we need to find whether any sick members get transfered
    #      (val_max, ":excess", 0),
    #      (party_wound_members, "p_main_party", ":stack_troop", ":excess"),
    #    (try_end),
      (try_end),
    #  (try_begin),
    #    (neq, ":stop_stack", -1),
    #    (store_add, ":stop_stack_plus_one", ":stop_stack", 1),
    #  (else_try),
        (assign, ":stop_stack_plus_one", ":num_companion_stacks"),
    #  (try_end),
      (try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
        (party_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (party_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
    #    (try_begin),
    #      (neq, ":stop_no", -1),
    #      (eq, ":stack_no", ":stop_stack"),
    #      (party_remove_members, "$current_town", ":stack_troop", ":stop_no"),
    #    (else_try),
          (party_remove_members, "$current_town", ":stack_troop", ":stack_size"),
    #    (try_end),
      (try_end),
    #(try_end),  # avoid some inputs at the same time
    
    (else_try),  #(try_begin), #TROOPS FROM PLAYER'S PARTY TO GARRISON  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      (key_is_down, key_right_control),
      (key_is_down, key_left),
      (party_get_num_companion_stacks, ":num_companion_stacks", "p_main_party"),
      (try_for_range, ":stack_no", 0, ":num_companion_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":stack_no"),
        (party_stack_get_num_wounded, ":stack_no_wounded", "p_main_party", ":stack_no"),
        (party_add_members, "$current_town", ":stack_troop", ":stack_size"),
        (party_wound_members, "$current_town", ":stack_troop", ":stack_no_wounded"),
      (try_end),
      (try_for_range_backwards, ":stack_no", 0, ":num_companion_stacks"),
        (party_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_stack_get_size, ":stack_size", "p_main_party", ":stack_no"),
        (party_remove_members, "p_main_party", ":stack_troop", ":stack_size"),
      (try_end),
    #(try_end),  # avoid some inputs at the same time
    
    (else_try),  #(try_begin), #PRISONERS FROM GARRISON TO PLAYER'S PARTY  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      (key_is_down, key_left_control),
      (key_is_down, key_a),
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "$current_town"),
    #  (assign, ":stop_stack", -1),
    #  (assign, ":stop_no", -1),
      (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
    #    (eq, ":stop_stack", -1),
    #    (party_get_free_prisoners_capacity, ":player_prisoner_capacity", "p_main_party"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_prisoner_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
    #    (try_begin),
    #      (ge, ":player_prisoner_capacity", ":stack_size"),
          (party_add_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
    #    (else_try),
    #      (party_add_prisoners, "p_main_party", ":stack_troop", ":player_prisoner_capacity"),
    #      (assign, ":stop_stack", ":stack_no"),
    #      (assign, ":stop_no", ":player_prisoner_capacity"),
    #    (try_end),
      (try_end),
    #  (try_begin),
    #    (neq, ":stop_stack", -1),
    #    (store_add, ":stop_stack_plus_one", ":stop_stack", 1),
    #  (else_try),
        (assign, ":stop_stack_plus_one", ":num_prisoner_stacks"),
    #  (try_end),
      (try_for_range_backwards, ":stack_no", 0, ":stop_stack_plus_one"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", "$current_town", ":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_prisoner_stack_get_size, ":stack_size", "$current_town", ":stack_no"),
    #    (try_begin),
    #      (neq, ":stop_no", -1),
    #      (eq, ":stack_no", ":stop_stack"),
    #      (party_remove_prisoners, "$current_town", ":stack_troop", ":stop_no"),
    #    (else_try),
          (party_remove_prisoners, "$current_town", ":stack_troop", ":stack_size"),
    #    (try_end),
      (try_end),
    #(try_end),  # avoid some inputs at the same time
    
    (else_try),  #(try_begin), #PRISONERS FROM PLAYER'S PARTY TO GARRISON  # avoid some inputs at the same time
      #(troop_slot_eq, "trp_globals_troop", slot_adv_transfer_mode, 12),
      (eq, "$g_adv_transfer_mode", 12),  # manage garrison
      (key_is_down, key_left_control),
      (key_is_down, key_d),
      (party_get_num_prisoner_stacks, ":num_prisoner_stacks", "p_main_party"),
      (try_for_range, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_prisoner_stack_get_size, ":stack_size", "p_main_party", ":stack_no"),
        (party_add_prisoners, "$current_town", ":stack_troop", ":stack_size"),
      (try_end),
      (try_for_range_backwards, ":stack_no", 0, ":num_prisoner_stacks"),
        (party_prisoner_stack_get_troop_id, ":stack_troop", "p_main_party", ":stack_no"),
        (neg|troop_is_hero, ":stack_troop"),
        (party_prisoner_stack_get_size, ":stack_size", "p_main_party", ":stack_no"),
        (party_remove_prisoners, "p_main_party", ":stack_troop", ":stack_size"),
      (try_end),
    (try_end),
    ## CC-D end
  ]),

]


from util_scripts import *
from util_wrappers import *

scripts_directives = [
	#if you change ":unused" in game_get_troop_wage, you need to change next too.
	[SD_OP_BLOCK_INSERT, "game_get_troop_wage", D_SEARCH_FROM_TOP | D_SEARCH_SCRIPTLINE | D_INSERT_AFTER, (store_script_param_2, ":party_no"),0,  ## CC-D: unused->party_no
	[
      (call_script, "script_initialize_exchange_screen_extensions", ":troop_id"),
      #(troop_set_slot, "trp_globals_troop", slot_last_requested_troop, ":troop_id"),
      (assign, "$g_last_requested_troop", ":troop_id"),
	]],
]
                
def modmerge_scripts(orig_scripts):
	# process script directives first
	process_script_directives(orig_scripts, scripts_directives)
	# add remaining scripts
	add_scripts(orig_scripts, scripts, True)
	
def modmerge(var_set):
	try:
		from modmerger_options import module_sys_info
		version = module_sys_info["version"]
	except:
		version = 1166 # version not specified.  assume latest warband at this time

	try:
		var_name_1 = "scripts"
		orig_scripts = var_set[var_name_1]
		
		modmerge_scripts(orig_scripts)
		
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)
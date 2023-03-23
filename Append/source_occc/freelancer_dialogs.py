# Freelancer (1.3) by Taragoth
# Released 11 July 2011
# Edits by Caba'drin 14 Dec 2011
# Mod-Merger'd by Windyplains, Monnikje and Caba'drin

# -*- coding: cp1254 -*-
from header_common import *
from header_dialogs import *
from header_operations import *
from module_constants import *



####################################################################################################################
# During a dialog, the dialog lines are scanned from top to bottom.
# If the dialog-line is spoken by the player, all the matching lines are displayed for the player to pick from.
# If the dialog-line is spoken by another, the first (top-most) matching line is selected.
#
#  Each dialog line contains the following fields:
# 1) Dialogue partner: This should match the person player is talking to.
#    Usually this is a troop-id.
#    You can also use a party-template-id by appending '|party_tpl' to this field.
#    Use the constant 'anyone' if you'd like the line to match anybody.
#    Appending '|plyr' to this field means that the actual line is spoken by the player
#    Appending '|other(troop_id)' means that this line is spoken by a third person on the scene.
#       (You must make sure that this third person is present on the scene)
#
# 2) Starting dialog-state:
#    During a dialog there's always an active Dialog-state.
#    A dialog-line's starting dialog state must be the same as the active dialog state, for the line to be a possible candidate.
#    If the dialog is started by meeting a party on the map, initially, the active dialog state is "start"
#    If the dialog is started by speaking to an NPC in a town, initially, the active dialog state is "start"
#    If the dialog is started by helping a party defeat another party, initially, the active dialog state is "party_relieved"
#    If the dialog is started by liberating a prisoner, initially, the active dialog state is "prisoner_liberated"
#    If the dialog is started by defeating a party led by a hero, initially, the active dialog state is "enemy_defeated"
#    If the dialog is started by a trigger, initially, the active dialog state is "event_triggered"
# 3) Conditions block (list): This must be a valid operation block. See header_operations.py for reference.
# 4) Dialog Text (string):
# 5) Ending dialog-state:
#    If a dialog line is picked, the active dialog-state will become the picked line's ending dialog-state.
# 6) Consequences block (list): This must be a valid operation block. See header_operations.py for reference.
# 7) Voice-over (string): sound filename for the voice over. Leave here empty for no voice over
####################################################################################################################

#+freelancer start
lord_talk_addon = [
# dialog_ask_enlistment

## CC-D begin
    [anyone|plyr,"lord_talk", [
        (eq, "$freelancer_state", 0),
        (check_quest_active, "qst_freelancer_enlisted"),
        (quest_slot_eq, "qst_freelancer_enlisted", slot_quest_giver_troop, "$g_talk_troop"),
        ],
    "My Lord, I would like to recieve the reward about my last service.", "lord_request_reward",[]],
## CC-D end

    [anyone|plyr,"lord_talk", [
        (eq, "$freelancer_state", 0),
		(ge, "$g_talk_troop_faction_relation", 0),
        #(neq, "$players_kingdom", "$g_talk_troop_faction"), occc begin
        (this_or_next|eq, "$players_kingdom", 0),
        (eq, "$players_kingdom", "$g_talk_troop_faction"),#occc end
        (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),  ## NMCml FL: fix situation
        ],
    "My Lord, I would like to like to enlist in your army.", "lord_request_enlistment",[]],
	
	# dialog_advise_retirement
	
## occc begin
    # [anyone|plyr,"lord_talk",[
		# (eq, "$g_talk_troop", "$enlisted_lord"),
		# (eq, "$freelancer_state", 1),
        # (ge, "$g_talk_troop_faction_relation", 0),
        # #(neq, "$players_kingdom", "$g_talk_troop_faction"), occc begin
        # (this_or_next|eq, "$players_kingdom", 0),
        # (eq, "$players_kingdom", "$g_talk_troop_faction"),#occc end
        # ],
        # "My Lord, I would like to request some personal leave", "lord_request_vacation",[]],  

## occc end

    [anyone|plyr,"lord_talk", [
        (eq, "$g_talk_troop", "$enlisted_lord"),
		(neq, "$freelancer_state", 0),
		(neq, "$freelancer_state", 2),  ## NMCml FL: fix situation
        (ge, "$g_talk_troop_faction_relation", 0),
        #(neq, "$players_kingdom", "$g_talk_troop_faction"), occc begin
        (this_or_next|eq, "$players_kingdom", 0),
        (eq, "$players_kingdom", "$g_talk_troop_faction"),#occc end
        ],
    "My Lord, I would like to like to retire from service.", "lord_request_retire",[]],
	
	#dialog_ask_leave
    [anyone|plyr,"lord_talk",[
		(eq, "$g_talk_troop", "$enlisted_lord"),
		(eq, "$freelancer_state", 1),
        (ge, "$g_talk_troop_faction_relation", 0),
        #(neq, "$players_kingdom", "$g_talk_troop_faction"), occc begin
        (this_or_next|eq, "$players_kingdom", 0),
        (eq, "$players_kingdom", "$g_talk_troop_faction"),#occc end
        ],
        "My Lord, I would like to request some personal leave", "lord_request_vacation",[]],  
		
	#dialog_ask_return_from_leave
		[anyone|plyr,"lord_talk",[
		(eq, "$g_talk_troop", "$enlisted_lord"),
		(eq, "$freelancer_state", 2),
        (ge, "$g_talk_troop_faction_relation", 0),
        #(neq, "$players_kingdom", "$g_talk_troop_faction"), occc begin
        (this_or_next|eq, "$players_kingdom", 0),
        (eq, "$players_kingdom", "$g_talk_troop_faction"),#occc end
        (neg|troop_slot_ge, "$g_talk_troop", slot_troop_prisoner_of_party, 0),  ## NMCml FL: fix situation
        ],
        "My Lord, I am ready to return to your command.", "ask_return_from_leave",[]],	
        
    #occc start
    # [anyone|plyr,"lord_talk", [
        # (eq, "$g_talk_troop", "$enlisted_lord"),
		# (eq, "$freelancer_state", 1),
        # (ge, "$g_talk_troop_faction_relation", 0),
        # #(neq, "$players_kingdom", "$g_talk_troop_faction"), occc begin
        # (this_or_next|eq, "$players_kingdom", 0),
        # (eq, "$players_kingdom", "$g_talk_troop_faction"),#occc end
        # ],
    # "My Lord, I would like to reconsider my career.", "lord_request_retire",[]],
    #occc end

        
]
		
dialogs	= [   
# dialog_accept_enlistment

    [anyone,"lord_request_enlistment",
    [
        (ge, "$g_talk_troop_relation", 0),
		(try_begin),
			(neg|faction_slot_eq, "$g_talk_troop_faction", slot_faction_freelancer_troop, 0),
			(faction_get_slot, reg1, "$g_talk_troop_faction", slot_faction_freelancer_troop),
		(else_try),
            #occc start - extra enlistment
            (call_script, "script_occc_freelancer_extra_lord", "$enlisted_lord"),
            #occc end
		(try_end),
		(str_store_troop_name, s1, reg1),
		(store_character_level, reg1, reg1),
		(val_mul, reg1, 10),		
		(str_store_string, s2, "str_reg1_denars"),
    ], "I've got room in my ranks for a {man/woman} of your disposition, {playername}.  I can take you on as a {s1}, with a weekly pay of {s2}. And food, of course.  Plenty of room for promotion and you'll be equipped as befits your rank. You'll have your take of what you can scavange in battle, too.  What do you say?", "lord_request_enlistment_confirm", []],
		
    [anyone|plyr,"lord_request_enlistment_confirm", [],
    "Seems a fair lot and steady work in these lands. I'm with you, my lord.", "close_window",
	[
	    (party_clear, "p_freelancer_party_backup"),
       	(call_script, "script_party_copy", "p_freelancer_party_backup", "p_main_party"),
		(remove_member_from_party, "trp_player","p_freelancer_party_backup"),
        (call_script, "script_event_player_enlists"),
		(assign, "$g_infinite_camping", 1),
        ## CC-D begin: FL double speed refer from CtA
        #(rest_for_hours_interactive, 24 * 365, 5, 1),
        (val_clamp, "$g_nmcml_fl_double_speed", 1, 101),
        (rest_for_hours_interactive, 24 * 365, "$g_nmcml_fl_double_speed", 1),
        ## CC-D end
		(eq,"$talk_context",tc_party_encounter),
		(assign, "$g_leave_encounter", 1),
	]],

	[anyone|plyr,"lord_request_enlistment_confirm",[],
    "Well, on second thought my lord, I might try my luck alone a bit longer. My thanks.", "lord_pretalk",[]],
	
# dialog_reject_enlistment

    [anyone,"lord_request_enlistment", [(lt, "$g_talk_troop_relation", 0)],
    "I do not trust you enough to allow you to serve for me.", "lord_pretalk",[]],

   

# dialog_lord_accept_retire 

##occc start
    [anyone,"lord_request_retire",# hard mode
    [		
		(assign,":continue",0),
		(try_begin),
			(eq,"$g_occc_mildmode",0), #hard mode off
			(assign,":continue",1),
		(else_try),
			(troop_get_slot, ":service_day_start", "trp_player", slot_troop_freelancer_start_date),
			(store_current_day, ":day"),
			(val_sub, ":day", ":service_day_start"),
			(ge,":day",21),
			(assign,":continue",1),
		(try_end),
		(eq,":continue",0),

    ],
    "What? {playername}, it's too short term that you have served for! If you want to retire duty, I demand 4000 denars as compensation for your disloyally.", "lord_request_retire_b",[
	],
	],	
	
	
  [anyone|plyr,"lord_request_retire_b",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", 4000),
    ], "I got it. Then, I'll pay 4000 denars to retire duty.", "lord_pretalk",[
       (troop_remove_gold, "trp_player", 4000),
	   (call_script, "script_troop_change_relation_with_troop", "trp_player", "$g_talk_troop", -5),
	   (call_script, "script_event_player_discharge"),
	   (call_script, "script_party_restore"),
	   (change_screen_map),
        ]],
		
  [anyone|plyr,"lord_request_retire_b",
   [
        (store_troop_gold, ":gold", "trp_player"),
        (ge, ":gold", 4000),
    ],"Hmph, now I have reconsidered. I'll continue to serve you.","lord_pretalk",[]],

  [anyone|plyr,"lord_request_retire_b", [        (store_troop_gold, ":gold", "trp_player"),(lt, ":gold", 4000),
], "I don't have enough denars...", "lord_pretalk",[]],

##occc end
	
	

    [anyone,"lord_request_retire",
    [		

    ],
    "Very well {playername}. You are relieved of duty.", "lord_pretalk",[
	(call_script, "script_event_player_discharge"),
	(call_script, "script_party_restore"),
	(change_screen_map),
	],
	],	

#dialog_accept_leave  
    [anyone,"lord_request_vacation",
        [
        (ge, "$g_talk_troop_relation", 0),
		],
            "Very well {playername}. You shall take some time off from millitary duty. Return in two weeks.", "lord_pretalk",[
		(call_script, "script_event_player_vacation"),
       	(call_script, "script_party_restore"),
		(change_screen_map),
		],
		],
					

				
	
#dialog_accept_ask_return_from_leave
        [anyone,"ask_return_from_leave",
        [
        (ge, "$g_talk_troop_relation", 0),
		],
        "Welcome back {playername}. Your regiment has missed you I daresay, Now return to your post.", "lord_pretalk",[
        (call_script, "script_party_copy", "p_freelancer_party_backup", "p_main_party"),
		(remove_member_from_party, "trp_player","p_freelancer_party_backup"),
        (call_script, "script_event_player_returns_vacation"),
        (assign, "$g_infinite_camping", 1),  ## NMCml FL: fix enlist
		(change_screen_map),
		],
		],	
## CC-D begin
    [anyone,"lord_request_reward",
    [		
    ],
    "Very well {playername}.", "lord_pretalk",[
	(troop_get_slot, ":service_day_start", "trp_player", slot_troop_freelancer_start_date),
	(store_current_day, ":day"),
	(val_sub, ":day", ":service_day_start"),
	(call_script, "script_finish_quest", "qst_freelancer_enlisted", ":day"), #percentage--make based on days served?  ## NMCml FL: quest fix: 100->":day"
	(change_screen_map),
	],
	],	
## CC-D end
#+freelancer end
]
## CC-D begin: caravan guard
caravan_dialog = [
  [anyone|plyr, "merchant_talk", 
    [
      (eq, "$g_encountered_party_type", spt_kingdom_caravan),
      (eq, "$talk_context", tc_party_encounter), 
      (neg|party_slot_ge, "$g_encountered_party", slot_party_last_toll_paid_hours, "$g_current_hours"),
      (ge,"$g_encountered_party_relation",0),
      (eq, "$freelancer_state", 0),
      (ge, "$g_talk_troop_faction_relation", 0),
      (eq, "$players_kingdom", 0),
    ], "Do you want a bouncer?", "merchant_talk_ccd_bauncer", []],
  [anyone, "merchant_talk_ccd_bauncer",
    [
      (store_character_level, reg1, "trp_player"),
      (val_mul, reg1, 10),
      (str_store_string, s2, "str_reg1_denars"),
    ], "If you get our bouncer, I pay {s2} per week, and food. OK?", "merchant_talk_ccd_bauncer_1", []],
  [anyone|plyr, "merchant_talk_ccd_bauncer_1", [
    ], "OK.", "close_window",
    [
      (party_clear, "p_freelancer_party_backup"),
      (call_script, "script_party_copy", "p_freelancer_party_backup", "p_main_party"),
      (remove_member_from_party, "trp_player", "p_freelancer_party_backup"),
      (call_script, "script_event_player_enlists_caravan"),
      (assign, "$g_infinite_camping", 1),
      ## CC-D begin: FL double speed refer from CtA
      #(rest_for_hours_interactive, 24 * 365, 5, 1),
      (val_clamp, "$g_nmcml_fl_double_speed", 1, 101),
      (rest_for_hours_interactive, 24 * 365, "$g_nmcml_fl_double_speed", 1),
      ## CC-D end
      (eq, "$talk_context", tc_party_encounter),
      (assign, "$g_leave_encounter", 1),
    ]],
  [anyone|plyr, "merchant_talk_ccd_bauncer_1", [
    ], "Sorry, my mind change.", "merchant_pretalk", []],
]
## CC-D end

from util_common import *
from util_wrappers import *

def dialogs_addendum(orig_dialogs):
	try:
		dialog = FindDialog(orig_dialogs, anyone|plyr, "lord_talk", "lord_request_mission_ask")
		codeblock = dialog.GetConditionBlock()
		codeblock.InsertBefore(0, not_enlisted)
		dialog = FindDialog(orig_dialogs, anyone|plyr, "lord_talk", "lord_ask_enter_service", "I have come")
		codeblock = dialog.GetConditionBlock()
		codeblock.InsertBefore(0, not_enlisted)
		dialog = FindDialog(orig_dialogs, anyone|plyr, "lord_talk", "lord_ask_enter_service", "I wish to become")
		codeblock = dialog.GetConditionBlock()
		codeblock.InsertBefore(0, not_enlisted)
		## NMCml FL begin: fix situation: need to change under Diplomacy: lady->{lord/lady}
		dialog = FindDialog(orig_dialogs, anyone, "start", "lord_groom_vows", "My {lord/lady}, I")
		codeblock = dialog.GetConditionBlock()
		codeblock.InsertBefore(0, not_enlisted)
		dialog = FindDialog(orig_dialogs, anyone, "start", "lord_groom_vows", "My {lord/lady}, my")
		codeblock = dialog.GetConditionBlock()
		codeblock.InsertBefore(0, not_enlisted)
		## NMCml FL end
	except:
		import sys
		print "Injecton 1 failed:", sys.exc_info()[1]
		raise

# Used by modmerger framework version >= 200 to merge stuff
def modmerge(var_set):
    try:
		var_name_1 = "dialogs"
		orig_dialogs = var_set[var_name_1]
		orig_dialogs.extend(dialogs)
		pos = FindDialog_i(orig_dialogs, anyone|plyr, "lord_talk", "lord_leave_prison")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, lord_talk_addon)
		## CC-D begin: caravan guard
		pos = FindDialog_i(orig_dialogs, anyone|plyr, "merchant_talk", "close_window")
		OpBlockWrapper(orig_dialogs).InsertBefore(pos, caravan_dialog)
		## CC-D end
		##ORIG_DIALOGS is a list, can use OpBlockWrapper and other list operations.
		
		dialogs_addendum(orig_dialogs) #other dialog additions
		
    except KeyError:
        errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
        raise ValueError(errstring)
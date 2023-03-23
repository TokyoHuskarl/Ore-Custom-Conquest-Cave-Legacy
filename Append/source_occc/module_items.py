from module_constants import *
from ID_factions import *
from header_items import  *
from header_operations import *
from header_triggers import *

####################################################################################################################
#  Each item record contains the following fields:
#  1) Item id: used for referencing items in other files.
#     The prefix itm_ is automatically added before each item id.
#  2) Item name. Name of item as it'll appear in inventory window
#  3) List of meshes.  Each mesh record is a tuple containing the following fields:
#    3.1) Mesh name.
#    3.2) Modifier bits that this mesh matches.
#     Note that the first mesh record is the default.
#  4) Item flags. See header_items.py for a list of available flags.
#  5) Item capabilities. Used for which animations this item is used with. See header_items.py for a list of available flags.
#  6) Item value.
#  7) Item stats: Bitwise-or of various stats about the item such as:
#      weight, abundance, difficulty, head_armor, body_armor,leg_armor, etc...
#  8) Modifier bits: Modifiers that can be applied to this item.
#  9) [Optional] Triggers: List of simple triggers to be associated with the item.
#  10) [Optional] Factions: List of factions that item can be found as merchandise.
####################################################################################################################

# Some constants for ease of use.
imodbits_none = 0
imodbits_horse_basic = imodbit_swaybacked|imodbit_lame|imodbit_spirited|imodbit_heavy|imodbit_stubborn|imodbit_timid ## CC
imodbits_cloth  = imodbit_tattered | imodbit_ragged | imodbit_sturdy | imodbit_thick | imodbit_hardened
imodbits_armor  = imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_plate  = imodbit_cracked | imodbit_rusty | imodbit_battered | imodbit_crude | imodbit_thick | imodbit_reinforced |imodbit_lordly
imodbits_polearm = imodbit_cracked | imodbit_bent | imodbit_balanced
imodbits_shield  = imodbit_cracked | imodbit_battered |imodbit_thick | imodbit_reinforced
imodbits_sword   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered
imodbits_sword_high   = imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered|imodbit_masterwork
imodbits_axe   = imodbit_rusty | imodbit_chipped | imodbit_heavy
imodbits_mace   = imodbit_rusty | imodbit_chipped | imodbit_heavy
imodbits_pick   = imodbit_rusty | imodbit_chipped | imodbit_balanced | imodbit_heavy
imodbits_bow = imodbit_cracked | imodbit_bent | imodbit_strong |imodbit_masterwork
imodbits_crossbow = imodbit_cracked | imodbit_bent | imodbit_masterwork
imodbits_missile   = imodbit_bent | imodbit_large_bag
imodbits_thrown   = imodbit_bent | imodbit_heavy| imodbit_balanced| imodbit_large_bag
imodbits_thrown_minus_heavy = imodbit_bent | imodbit_balanced| imodbit_large_bag
## CC-D begin: add champion
#imodbits_horse_good = imodbit_spirited|imodbit_heavy
#occc additional... even good horses can have bad traits
imodbits_horse_good = imodbit_swaybacked|imodbit_stubborn|imodbit_spirited|imodbit_heavy|imodbit_champion
## CC-D end
imodbits_good   = imodbit_sturdy | imodbit_thick | imodbit_hardened | imodbit_reinforced
imodbits_bad    = imodbit_rusty | imodbit_chipped | imodbit_tattered | imodbit_ragged | imodbit_cracked | imodbit_bent
#occc start
imodbits_ancient    = imodbit_rusty | imodbit_chipped | imodbit_tattered | imodbit_ragged | imodbit_cracked | imodbit_bent | imodbit_old

#occc end

## CC begin
missile_distance_trigger = [
  (ti_on_missile_hit, 
    [
      (store_trigger_param_1, ":shooter_agent"),
      
      (eq, "$g_report_shot_distance", 1),
      (get_player_agent_no, ":player_agent"),
      (try_begin),
        (eq, ":shooter_agent", ":player_agent"),
        (agent_get_position, pos2, ":shooter_agent"),
        (agent_get_horse, ":horse_agent", ":player_agent"),
        (try_begin),
          (gt, ":horse_agent", -1),
          (position_move_z, pos2, 220),
        (else_try),
          (position_move_z, pos2, 150),
        (try_end),
        (get_distance_between_positions, ":distance", pos1, pos2),
        (store_div, reg61, ":distance", 100),
        (store_mod, reg62, ":distance", 100),
        (try_begin),
          (lt, reg62, 10),
          (str_store_string, s1, "@{reg61}.0{reg62}"),
        (else_try),
          (str_store_string, s1, "@{reg61}.{reg62}"),
        (try_end),
        (display_message, "@Shot distance: {s1} meters.", 0xCCCCCC),
      (try_end),
    ])]    
## CC end

## CC-D begin: fire arrow from PBOD 0.96.3
fired_arrow_triggers = [
 # (ti_on_init_missile, [
    # (set_position_delta, 0, 100, 0), #change this to move the particle system's local position
    # (particle_system_add_new, "psys_arrow_fire"),
    # (particle_system_add_new, "psys_arrow_smoke"),
    # (particle_system_add_new, "psys_arrow_fire_sparks"),
    # (set_current_color,150, 130, 70),
    # (add_point_light, 10, 30),
   # ]),
  (ti_on_init_item, [
     (set_position_delta, 0, 100, 0), #change this to move the particle system's local position
     (particle_system_add_new, "psys_arrow_fire"),
     (particle_system_add_new, "psys_arrow_smoke"),
     (particle_system_add_new, "psys_arrow_fire_sparks"),
     (set_current_color,150, 130, 70),
     (add_point_light, 10, 30),
   ]),
  (ti_on_missile_hit, [
	(set_position_delta, 0, 100, -300), 
    (particle_system_burst,"psys_arrow_fire", 1, 150),  ## CC-D 20->150
	(particle_system_burst,"psys_arrow_smoke", 1, 160),  ## CC-D 30->160
	(particle_system_burst,"psys_arrow_fire_sparks", 1, 50),  ## CC-D 15->50
	(set_current_color,150, 130, 70),
   ]),
  # (ti_on_missile_dive, [
    # (set_position_delta, 0, 100, -200), 
	# (particle_system_burst,"psys_arrow_smoke", 0, 20),
	# (set_current_color,150, 130, 70),
	# (particle_system_remove, "psys_arrow_fire"),
	# (particle_system_remove, "psys_arrow_fire_sparks"),
   # ]),
]
fired_projectile_triggers = [
 # (ti_on_init_missile, [
    # (set_position_delta, 0, 100, 0), #change this to move the particle system's local position
    # (particle_system_add_new, "psys_arrow_fire"),
    # (particle_system_add_new, "psys_arrow_smoke"),
    # (particle_system_add_new, "psys_arrow_fire_sparks"),
    # (set_current_color,150, 130, 70),
    # (add_point_light, 10, 30),
   # ]),
  (ti_on_init_item, [
     (set_position_delta, 0, 0, 0), #change this to move the particle system's local position
     (particle_system_add_new, "psys_occc_arrow_fire"),
     (particle_system_add_new, "psys_arrow_smoke"),
     (particle_system_add_new, "psys_arrow_fire_sparks"),
     (set_current_color,150, 130, 70),
     (add_point_light, 10, 30),
   ]),
  (ti_on_missile_hit, [
	(set_position_delta, 0, 100, -300), 
    (particle_system_burst,"psys_occc_arrow_fire", 1, 150),  ## CC-D 20->150
	(particle_system_burst,"psys_arrow_smoke", 1, 160),  ## CC-D 30->160
	(particle_system_burst,"psys_arrow_fire_sparks", 1, 50),  ## CC-D 15->50
	(set_current_color,150, 130, 70),
   ]),
  # (ti_on_missile_dive, [
    # (set_position_delta, 0, 100, -200), 
	# (particle_system_burst,"psys_arrow_smoke", 0, 20),
	# (set_current_color,150, 130, 70),
	# (particle_system_remove, "psys_arrow_fire"),
	# (particle_system_remove, "psys_arrow_fire_sparks"),
   # ]),
]
## CC-D end
## CC-D begin: tracer
ccd_tracer_triggers = [
  (ti_on_missile_hit, [
    (copy_position, pos5, pos1),
    (position_move_y, pos5, -10),
    (particle_system_burst, "psys_ccd_tracer_light", pos5, 150),
   ]),
]
## CC-D end
## CC-D begin: magic knife(for psys test)
ccd_magic_knife_trigger = [
  (ti_on_missile_hit, [
    (val_sub, "$temp", 1),
    (try_begin),
      (this_or_next|gt, "$temp", "psys_ccd_tracer_light"),
      (lt, "$temp", 0),
      (assign, "$temp", "psys_ccd_tracer_light"),
    (try_end),
    (particle_system_burst, "$temp", pos1, 150),
    (try_begin),
      (gt, "$cheat_mode", 0),
      (gt, "$g_ccc_option_debug_menu", 0),
      (assign, reg0, "$temp"),
      (display_message, "@{!}{reg0}"),
    (try_end),
  ]),
]
## CC-D end


# Replace winged mace/spiked mace with: Flanged mace / Knobbed mace?
# Fauchard (majowski glaive)
items = [
# item_name, mesh_name, item_properties, item_capabilities, slot_no, cost, bonus_flags, weapon_flags, scale, view_dir, pos_offset
 ["no_item","INVALID ITEM", [("invalid_item",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_longsword, 3,weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(16,blunt)|thrust_damage(10,blunt),imodbits_none],

["tutorial_spear", "Spear", [("spear",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_penalty_with_shield, itc_spear, 0, weight(4.5)|difficulty(0)|spd_rtng(80)|weapon_length(158)|swing_damage(0,cut)|thrust_damage(19,pierce), imodbits_polearm ],
["tutorial_club", "Club", [("club",0)], itp_type_one_handed_wpn|itp_wooden_attack|itp_wooden_parry|itp_primary, itc_scimitar, 0, weight(2.5)|difficulty(0)|spd_rtng(95)|weapon_length(95)|swing_damage(11,blunt)|thrust_damage(0,pierce), imodbits_none ],
["tutorial_battle_axe", "Battle Axe", [("battle_ax",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_axe_back, 0, weight(5)|difficulty(0)|spd_rtng(88)|weapon_length(108)|swing_damage(27,cut)|thrust_damage(0,pierce), imodbits_axe ],
["tutorial_arrows", "Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(3)|abundance(160)|weapon_length(95)|thrust_damage(0,pierce)|max_ammo(20), imodbits_missile, missile_distance_trigger ],
["tutorial_bolts", "Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag",ixmesh_carry),("bolt_bag_b",ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0, weight(2.25)|abundance(90)|weapon_length(55)|thrust_damage(0,pierce)|max_ammo(18), imodbits_missile, missile_distance_trigger ],
["tutorial_short_bow", "Short Bow", [("short_bow",0),("short_bow_carry",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1)|difficulty(0)|spd_rtng(98)|shoot_speed(49)|thrust_damage(12,pierce), imodbits_bow ],
["tutorial_crossbow", "Crossbow", [("crossbow",0)], itp_type_crossbow|itp_cant_reload_on_horseback|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 0, weight(3)|difficulty(0)|spd_rtng(42)|shoot_speed(68)|thrust_damage(32,pierce)|max_ammo(1), imodbits_crossbow ],
["tutorial_throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown|itp_primary, itcf_throw_knife, 0, weight(3.5)|difficulty(0)|spd_rtng(102)|shoot_speed(25)|thrust_damage(16,cut)|max_ammo(14)|weapon_length(0), imodbits_missile, missile_distance_trigger ],
["tutorial_saddle_horse", "Saddle Horse", [("saddle_horse",0)], itp_type_horse, 0, 0, abundance(90)|hit_points(35)|body_armor(0)|difficulty(0)|horse_speed(25)|horse_maneuver(35)|horse_charge(8), imodbits_horse_basic ],
["tutorial_shield", "Kite Shield", [("shield_kite_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 118, weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(150), imodbits_shield ],
["tutorial_staff_no_attack", "Staff", [("wooden_staff",0)], itp_type_polearm|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance, itc_parry_polearm|itcf_carry_sword_back, 9, weight(3.5)|spd_rtng(120)|weapon_length(115)|swing_damage(0,blunt)|thrust_damage(0,blunt), imodbits_none ],
["tutorial_staff", "Staff", [("wooden_staff",0)], itp_type_polearm|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance, itc_staff|itcf_carry_sword_back, 9, weight(3.5)|spd_rtng(120)|weapon_length(115)|swing_damage(16,blunt)|thrust_damage(16,blunt), imodbits_none ],
["tutorial_sword", "Sword", [("long_sword",0),("scab_longsw_a",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 0, weight(1.5)|difficulty(0)|spd_rtng(100)|weapon_length(102)|swing_damage(18,cut)|thrust_damage(15,pierce), imodbits_sword ],
["tutorial_axe", "Axe", [("iron_ax",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_axe_back, 0, weight(4)|difficulty(0)|spd_rtng(91)|weapon_length(108)|swing_damage(19,cut)|thrust_damage(0,pierce), imodbits_axe ],

 ["tutorial_dagger","Dagger", [("practice_dagger",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_longsword, 3,weight(1.5)|spd_rtng(103)|weapon_length(40)|swing_damage(16,blunt)|thrust_damage(10,blunt),imodbits_none],


 ["horse_meat","Horse Meat", [("raw_meat",0)], itp_type_goods|itp_consumable|itp_food, 0, 12,weight(40)|food_quality(30)|max_ammo(40),imodbits_none],
# Items before this point are hardwired and their order should not be changed!

["practice_sword", "Practice Sword", [("practice_sword",0)], itp_type_one_handed_wpn|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_secondary, itc_longsword, 3, weight(1.5)|spd_rtng(103)|weapon_length(90)|swing_damage(22,blunt)|thrust_damage(20,blunt), imodbits_none ],
["heavy_practice_sword", "Heavy Practice Sword", [("heavy_practicesword",0)], itp_type_two_handed_wpn|itp_wooden_attack|itp_wooden_parry|itp_two_handed|itp_primary, itc_greatsword, 21, weight(6.25)|spd_rtng(94)|weapon_length(128)|swing_damage(30,blunt)|thrust_damage(24,blunt), imodbits_none ],
["practice_dagger", "Practice Dagger", [("practice_dagger",0)], itp_type_one_handed_wpn|itp_no_parry|itp_wooden_attack|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_left, 2, weight(0.5)|spd_rtng(110)|weapon_length(47)|swing_damage(16,blunt)|thrust_damage(14,blunt), imodbits_none ],
["practice_axe", "Practice Axe", [("hatchet",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 24, weight(2)|spd_rtng(95)|weapon_length(75)|swing_damage(24,blunt)|thrust_damage(0,pierce), imodbits_axe ],
["arena_axe", "Axe", [("arena_axe",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 137, weight(1.5)|spd_rtng(100)|weapon_length(69)|swing_damage(24,blunt)|thrust_damage(0,pierce), imodbits_axe ],
["arena_sword", "Sword", [("arena_sword_one_handed",0),("sword_medieval_b_scabbard",ixmesh_carry),], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 243, weight(1.5)|spd_rtng(99)|weapon_length(95)|swing_damage(22,blunt)|thrust_damage(20,blunt), imodbits_sword_high ],
["arena_sword_two_handed", "Two Handed Sword", [("arena_sword_two_handed",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 670, weight(2.75)|spd_rtng(93)|weapon_length(110)|swing_damage(30,blunt)|thrust_damage(24,blunt), imodbits_sword_high ],
["arena_lance", "Lance", [("arena_lance",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_staff|itcf_carry_spear, 90, weight(2.5)|spd_rtng(96)|weapon_length(150)|swing_damage(20,blunt)|thrust_damage(25,blunt), imodbits_polearm ],
["practice_staff", "Practice Staff", [("wooden_staff",0)], itp_type_polearm|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance, itc_staff|itcf_carry_sword_back, 9, weight(2.5)|spd_rtng(103)|weapon_length(118)|swing_damage(18,blunt)|thrust_damage(18,blunt), imodbits_none ],
["practice_lance", "Practice Lance", [("joust_of_peace",0)], itp_type_polearm|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_couchable, itc_greatlance, 18, weight(4.25)|spd_rtng(58)|weapon_length(240)|swing_damage(0,blunt)|thrust_damage(15,blunt), imodbits_none ],
["practice_shield", "Practice Shield", [("shield_round_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 20, weight(3.5)|body_armor(1)|hit_points(200)|spd_rtng(100)|shield_width(50), imodbits_none ],
["practice_bow", "Practice Bow", [("hunting_bow",0),("hunting_bow_carry",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(90)|shoot_speed(40)|thrust_damage(21,blunt), imodbits_bow ],
#CC-C begin
["practice_pistol", "Practice Pidtol", [("pistol_revolver_d",0),("pistol_revolver_d_carry",ixmesh_carry)], itp_type_pistol|itp_primary|itp_next_item_as_melee, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol, 25000, weight(2)|difficulty(0)|spd_rtng(92)|shoot_speed(85)|thrust_damage(35,pierce)|max_ammo(4)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])] ],
["practice_pistol_melee", "Practice Pistol Mel", [("pistol_revolver_d",0),("pistol_revolver_d_carry",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_revolver_right, 25000, weight(2)|difficulty(0)|spd_rtng(92)|weapon_length(45)|swing_damage(10, blunt), imodbits_crossbow ],
["practice_rifle", "Practice Musket", [("rifle_musket",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving|itp_next_item_as_melee, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket|itcf_parry_forward_polearm|itcf_parry_up_polearm|itcf_parry_right_polearm|itcf_parry_left_polearm, 1024, weight(2.0)|difficulty(0)|spd_rtng(70)|shoot_speed(120)|thrust_damage(70,pierce)|max_ammo(1)|accuracy(95), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),])] ],
["practice_rifle_melee", "Practice Musket Mel", [("rifle_musket",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_wooden_parry|itp_offset_musket|itp_has_bayonet|itp_no_blur, itc_musket_melee|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear, 1024, weight(2.0)|difficulty(0)|spd_rtng(85)|weapon_length(85)|swing_damage(13, blunt)|thrust_damage(12, blunt), imodbits_crossbow ],
["practice_cartridges", "Practic Cartridges", [("cartridge_a",0),("bullet",ixmesh_flying_ammo)], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield, 0, 41, weight(1)|abundance(90)|weapon_length(3)|thrust_damage(1,pierce)|max_ammo(70), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],
#CC-C end
["practice_crossbow", "Practice Crossbow", [("crossbow_a",0)], itp_type_crossbow|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 0, weight(3)|spd_rtng(42)|shoot_speed(68)|thrust_damage(32,blunt)|max_ammo(1), imodbits_crossbow ],
["practice_javelin", "Practice Javelins", [("javelin",0),("javelins_quiver_new",ixmesh_carry)], itp_type_thrown|itp_primary|itp_next_item_as_melee, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 0, weight(5)|spd_rtng(91)|shoot_speed(28)|thrust_damage(27,blunt)|max_ammo(50)|weapon_length(75), imodbits_thrown, missile_distance_trigger ],
["practice_javelin_melee", "practice_javelin_melee", [("javelin",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_penalty_with_shield, itc_staff, 0, weight(1)|difficulty(0)|spd_rtng(91)|swing_damage(12,blunt)|thrust_damage(14,blunt)|weapon_length(75), imodbits_polearm ],
["practice_throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown|itp_primary, itcf_throw_knife, 0, weight(3.5)|spd_rtng(102)|shoot_speed(25)|thrust_damage(16,blunt)|max_ammo(10)|weapon_length(0), imodbits_thrown, missile_distance_trigger ],
["practice_throwing_daggers_100_amount", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown|itp_primary, itcf_throw_knife, 0, weight(3.5)|spd_rtng(102)|shoot_speed(25)|thrust_damage(16,blunt)|max_ammo(100)|weapon_length(0), imodbits_thrown, missile_distance_trigger ],
# ["cheap_shirt","Cheap Shirt", [("shirt",0)], itp_type_body_armor|itp_covers_legs, 0, 4,weight(1.25)|body_armor(3),imodbits_none],
 ["practice_horse","Practice Horse", [("saddle_horse",0)], itp_type_horse, 0, 37,body_armor(10)|horse_speed(40)|horse_maneuver(37)|horse_charge(14),imodbits_none],
 ["practice_arrows","Practice Arrows", [("arena_arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver", ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0,weight(1.5)|weapon_length(95)|max_ammo(80),imodbits_missile, missile_distance_trigger ],
## ["practice_arrows","Practice Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo)], itp_type_arrows, 0, 31,weight(1.5)|weapon_length(95)|max_ammo(80),imodbits_none],
["practice_bolts", "Practice Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag",ixmesh_carry),("bolt_bag_b",ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0, weight(2.25)|weapon_length(55)|max_ammo(49), imodbits_missile, missile_distance_trigger ],
["practice_arrows_10_amount", "Practice Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(1.5)|weapon_length(95)|max_ammo(10), imodbits_missile, missile_distance_trigger ],
["practice_arrows_100_amount", "Practice Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(1.5)|weapon_length(95)|max_ammo(100), imodbits_missile, missile_distance_trigger ],
["practice_bolts_9_amount", "Practice Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag",ixmesh_carry),("bolt_bag_b",ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0, weight(2.25)|weapon_length(55)|max_ammo(9), imodbits_missile, missile_distance_trigger ],
["practice_boots", "Practice Boots", [("boot_nomad_a",0)], itp_type_foot_armor|itp_attach_armature|itp_civilian, 0, 11, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10), imodbits_cloth ],
["red_tourney_armor", "Red Tourney Armor", [("tourn_armor_a",0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none ],
["blue_tourney_armor", "Blue Tourney Armor", [("mail_shirt",0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none ],
#["green_tourney_armor", "Green Tourney Armor", [("leather_vest",0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none ],
["green_tourney_armor", "Green Tourney Armor", [("celtA",0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none ],
["gold_tourney_armor", "Gold Tourney Armor", [("padded_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 152, weight(15.0)|body_armor(20)|leg_armor(6), imodbits_none ],
["red_tourney_helmet", "Red Tourney Helmet", [("flattop_helmet",0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none ],
["blue_tourney_helmet", "Blue Tourney Helmet", [("segmented_helm",0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none ],
["green_tourney_helmet", "Green Tourney Helmet", [("hood_c",0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none ],
["gold_tourney_helmet", "Gold Tourney Helmet", [("hood_a",0)], itp_type_head_armor, 0, 126, weight(2)|head_armor(16), imodbits_none ],

["arena_shield_red", "Shield", [("arena_shield_red",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 42, weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],
["arena_shield_blue", "Shield", [("arena_shield_blue",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 42, weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],
["arena_shield_green", "Shield", [("arena_shield_green",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 42, weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],
["arena_shield_yellow", "Shield", [("arena_shield_yellow",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 42, weight(2)|hit_points(360)|body_armor(1)|spd_rtng(100)|weapon_length(60), imodbits_shield ],

["arena_armor_white", "Arena Armor White", [("arena_armorW_new",0)], itp_type_body_armor|itp_covers_legs, 0, 650, weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_red", "Arena Armor Red", [("arena_armorR_new",0)], itp_type_body_armor|itp_covers_legs, 0, 650, weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_blue", "Arena Armor Blue", [("arena_armorB_new",0)], itp_type_body_armor|itp_covers_legs, 0, 650, weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_green", "Arena Armor Green", [("arena_armorG_new",0)], itp_type_body_armor|itp_covers_legs, 0, 650, weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_armor_yellow", "Arena Armor Yellow", [("arena_armorY_new",0)], itp_type_body_armor|itp_covers_legs, 0, 650, weight(16)|abundance(100)|head_armor(0)|body_armor(29)|leg_armor(13), imodbits_armor ],
["arena_tunic_white", "Arena Tunic White ", [("arena_tunicW_new",0)], itp_type_body_armor|itp_covers_legs, 0, 47, weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_red", "Arena Tunic Red", [("arena_tunicR_new",0)], itp_type_body_armor|itp_covers_legs, 0, 27, weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_blue", "Arena Tunic Blue", [("arena_tunicB_new",0)], itp_type_body_armor|itp_covers_legs, 0, 27, weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_green", "Arena Tunic Green", [("arena_tunicG_new",0)], itp_type_body_armor|itp_covers_legs, 0, 27, weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
["arena_tunic_yellow", "Arena Tunic Yellow", [("arena_tunicY_new",0)], itp_type_body_armor|itp_covers_legs, 0, 27, weight(2)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(6), imodbits_cloth ],
#headwear
["arena_helmet_red", "Arena Helmet Red", [("arena_helmetR",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_blue", "Arena Helmet Blue", [("arena_helmetB",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_green", "Arena Helmet Green", [("arena_helmetG",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_helmet_yellow", "Arena Helmet Yellow", [("arena_helmetY",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["steppe_helmet_white", "Steppe Helmet White", [("steppe_helmetW",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ], 
["steppe_helmet_red", "Steppe Helmet Red", [("steppe_helmetR",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ], 
["steppe_helmet_blue", "Steppe Helmet Blue", [("steppe_helmetB",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ], 
["steppe_helmet_green", "Steppe Helmet Green", [("steppe_helmetG",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ], 
["steppe_helmet_yellow", "Steppe Helmet Yellow", [("steppe_helmetY",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_plate ], 
["tourney_helm_white", "Tourney Helm White", [("tourney_helmR",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_red", "Tourney Helm Red", [("tourney_helmR",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_blue", "Tourney Helm Blue", [("tourney_helmB",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_green", "Tourney Helm Green", [("tourney_helmG",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["tourney_helm_yellow", "Tourney Helm Yellow", [("tourney_helmY",0)], itp_type_head_armor|itp_covers_head,0, 760 , weight(2.75)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_red", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_blue", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_green", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],
["arena_turban_yellow", "Arena Turban", [("tuareg_open",0)], itp_type_head_armor|itp_fit_to_head ,0, 187 , weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0), imodbits_plate ],


# BOOKS 
## Skill books
## This book must be at the beginning of readable books
["book_tactics", "De Re Militari", [("book_a",0)], itp_type_book, 0, 4000, weight(2)|abundance(100), imodbits_none ],
["book_persuasion", "Rhetorica ad Herennium", [("book_b",0)], itp_type_book, 0, 5000, weight(2)|abundance(100), imodbits_none ],
["book_leadership", "The Life of Alixenus the Great", [("book_d",0)], itp_type_book, 0, 4200, weight(2)|abundance(100), imodbits_none ],
["book_intelligence", "Essays on Logic", [("book_e",0)], itp_type_book, 0, 2900, weight(2)|abundance(100), imodbits_none ],
## CC begin 
["book_prisoner_management", "Ramun's Note", [("book_a",0)], itp_type_book, 0, 5000, weight(2)|abundance(100), imodbits_none ],
## CC end
["book_trade", "A Treatise on the Value of Things", [("book_f",0)], itp_type_book, 0, 3100, weight(2)|abundance(100), imodbits_none ],
["book_weapon_mastery", "On the Art of Fighting with Swords", [("book_d",0)], itp_type_book, 0, 4200, weight(2)|abundance(100), imodbits_none ],
["book_engineering", "Method of Mechanical Theorems", [("book_open",0)], itp_type_book, 0, 4000, weight(2)|abundance(100), imodbits_none ],

## Reference books
## This book must be at the beginning of reference books
["book_wound_treatment_reference", "The Book of Healing", [("book_c",0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none ],
["book_training_reference", "Manual of Arms", [("book_open",0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none ],
["book_surgery_reference", "The Great Book of Surgery", [("book_c",0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none ],
## CC begin
["book_spotting_reference", "The General Knowledge of Spotting", [("book_a",0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none ],
["book_first_aid_reference", "The General Knowledge of First Aid", [("book_f",0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none ],
["book_pathfinding_reference", "The Atlas of Calradia", [("book_b",0)], itp_type_book, 0, 3500, weight(2)|abundance(100), imodbits_none ],
## CC end

#wood_heap_a

# TRADE GOODS
## other trade goods (first one is spice)
["spice", "Spice", [("spice_sack",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 880, weight(40)|abundance(25)|max_ammo(50), imodbit_fine|imodbit_exquisite|imodbit_large_bag ],
["salt", "Salt", [("salt_sack",0)], itp_type_goods|itp_merchandise, 0, 255, weight(50)|abundance(120), imodbit_fine|imodbit_large_bag ],
#["flour","Flour", [("salt_sack",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 40,weight(50)|abundance(100)|food_quality(45)|max_ammo(50),imodbits_none],
["oil", "Oil", [("oil",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 450, weight(50)|abundance(60)|max_ammo(50), imodbit_fine|imodbit_exquisite|imodbit_cheap|imodbit_well_made ],
["pottery", "Pottery", [("jug",0)], itp_type_goods|itp_merchandise, 0, 100, weight(50)|abundance(90), imodbit_cracked|imodbit_crude|imodbit_old|imodbit_cheap|imodbit_fine|imodbit_exquisite|imodbit_masterwork|imodbit_well_made|imodbit_rough|imodbit_sturdy ],

["raw_flax", "Flax Bundle", [("raw_flax",0)], itp_type_goods|itp_merchandise, 0, 150, weight(40)|abundance(90), imodbit_fine|imodbit_exquisite ],
["linen", "Linen", [("linen",0)], itp_type_goods|itp_merchandise, 0, 250, weight(40)|abundance(90), imodbit_cheap|imodbit_fine|imodbit_exquisite|imodbit_masterwork|imodbit_ragged|imodbit_tattered|imodbit_well_made|imodbit_rough|imodbit_sturdy ],

["wool", "Wool", [("wool_sack",0)], itp_type_goods|itp_merchandise, 0, 130, weight(40)|abundance(90), imodbit_fine|imodbit_exquisite ],
["wool_cloth", "Wool Cloth", [("wool_cloth",0)], itp_type_goods|itp_merchandise, 0, 250, weight(40)|abundance(90), imodbit_cheap|imodbit_fine|imodbit_exquisite|imodbit_masterwork|imodbit_ragged|imodbit_tattered|imodbit_well_made|imodbit_rough|imodbit_sturdy ],

["raw_silk", "Raw Silk", [("raw_silk_bundle",0)], itp_type_goods|itp_merchandise, 0, 600, weight(30)|abundance(90), imodbit_fine|imodbit_exquisite ],
["raw_dyes", "Dyes", [("dyes",0)], itp_type_goods|itp_merchandise, 0, 200, weight(10)|abundance(90), imodbit_fine|imodbit_exquisite|imodbit_well_made|imodbit_masterwork ],
["velvet", "Velvet", [("velvet",0)], itp_type_goods|itp_merchandise, 0, 1025, weight(40)|abundance(30), imodbit_fine|imodbit_exquisite|imodbit_well_made|imodbit_masterwork ],

["iron", "Iron", [("iron",0)], itp_type_goods|itp_merchandise, 0, 264, weight(60)|abundance(60), imodbits_none ],
["tools", "Tools", [("iron_hammer",0)], itp_type_goods|itp_merchandise, 0, 410, weight(50)|abundance(90)|max_ammo(50), imodbit_fine|imodbit_exquisite|imodbit_well_made|imodbit_masterwork ],

["raw_leather", "Hides", [("leatherwork_inventory",0)], itp_type_goods|itp_merchandise, 0, 120, weight(40)|abundance(90), imodbit_fine|imodbit_exquisite|imodbit_ragged|imodbit_tattered|imodbit_sturdy|imodbit_thick ],
["leatherwork", "Leatherwork", [("leatherwork_frame",0)], itp_type_goods|itp_merchandise, 0, 220, weight(40)|abundance(90), imodbit_cheap|imodbit_fine|imodbit_exquisite|imodbit_masterwork|imodbit_ragged|imodbit_tattered|imodbit_well_made|imodbit_rough|imodbit_sturdy|imodbit_thick ],
["raw_date_fruit", "Date Fruit", [("date_inventory",0)], itp_type_goods|itp_merchandise|itp_food|itp_consumable, 0, 120, weight(40)|food_quality(10)|max_ammo(10), imodbit_fine|imodbit_exquisite|imodbit_cheap ],
["furs", "Furs", [("fur_pack",0)], itp_type_goods|itp_merchandise, 0, 391, weight(40)|abundance(90), imodbit_fine|imodbit_cheap|imodbit_exquisite|imodbit_ragged|imodbit_tattered|imodbit_sturdy|imodbit_thick ],
#additional trade goods
["occc_timber", "Timber", [("wood_heap_a",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 20, weight(50)|abundance(100)|max_ammo(50), imodbit_fine|imodbit_exquisite|imodbit_cheap ],
["occc_stone", "Stone", [("rock1",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 50, weight(100)|abundance(100)|max_ammo(50), imodbit_fine|imodbit_exquisite|imodbit_cheap ],

["occc_shells", "Arty Cannonball", [("bullet",0)], itp_type_goods|itp_merchandise, 0, 1000, weight(100)|abundance(15), imodbits_none, [], [fac_kingdom_2]  ],

["wine", "Wine", [("amphora_slim",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 220, weight(30)|abundance(60)|max_ammo(50), imodbit_fine|imodbit_exquisite|imodbit_cheap|imodbit_well_made|imodbit_strong ],
["ale", "Ale", [("ale_barrel",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 120, weight(30)|abundance(70)|max_ammo(50), imodbit_fine|imodbit_exquisite|imodbit_cheap|imodbit_well_made|imodbit_strong ],


# FOOD
## foods (first one is smoked_fish)
# ["dry_bread", "wheat_sack", itp_type_goods|itp_consumable, 0, slt_none,view_goods,95,weight(2),max_ammo(50),imodbits_none],
#foods (first one is smoked_fish)
 ["smoked_fish","Smoked Fish", [("smoked_fish",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 65,weight(15)|abundance(110)|food_quality(50)|max_ammo(55),imodbit_fine|imodbit_exquisite|imodbit_cheap],
 ["cheese","Cheese", [("cheese_b",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 75,weight(6)|abundance(110)|food_quality(40)|max_ammo(35),imodbit_fine|imodbit_exquisite|imodbit_cheap|imodbit_well_made],
 ["honey","Honey", [("honey_pot",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 220,weight(5)|abundance(110)|food_quality(40)|max_ammo(35),imodbit_fine|imodbit_exquisite|imodbit_cheap],
 ["sausages","Sausages", [("sausages",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 85,weight(10)|abundance(110)|food_quality(40)|max_ammo(45),imodbit_fine|imodbit_exquisite|imodbit_cheap],
 ["cabbages","Cabbages", [("cabbage",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 30,weight(15)|abundance(110)|food_quality(40)|max_ammo(55),imodbit_fine|imodbit_exquisite|imodbit_cheap],
 ["dried_meat","Dried Meat", [("smoked_meat",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 85,weight(15)|abundance(100)|food_quality(70)|max_ammo(55),imodbit_fine|imodbit_exquisite|imodbit_cheap],
 ["apples","Fruit", [("apple_basket",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 44,weight(20)|abundance(110)|food_quality(40)|max_ammo(55),imodbit_fine|imodbit_exquisite|imodbit_cheap],
 ["raw_grapes","Grapes", [("grapes_inventory",0)], itp_merchandise|itp_consumable|itp_type_goods, 0, 75,weight(40)|abundance(90)|food_quality(10)|max_ammo(15),imodbit_fine|imodbit_exquisite|imodbit_cheap], #x2 for wine
 ["raw_olives","Olives", [("olive_inventory",0)], itp_merchandise|itp_consumable|itp_type_goods, 0, 100,weight(40)|abundance(90)|food_quality(10)|max_ammo(15),imodbit_fine|imodbit_exquisite|imodbit_cheap], #x3 for oil
 ["grain","Grain", [("wheat_sack",0)], itp_merchandise|itp_type_goods|itp_consumable, 0, 30,weight(30)|abundance(110)|food_quality(40)|max_ammo(55),imodbit_fine|imodbit_exquisite|imodbit_cheap],

 ["cattle_meat","Beef", [("raw_meat",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 80,weight(20)|abundance(100)|food_quality(80)|max_ammo(55),imodbits_none],
 ["bread","Bread", [("bread_a",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 50,weight(30)|abundance(110)|food_quality(40)|max_ammo(55),imodbit_fine|imodbit_exquisite|imodbit_cheap|imodbit_well_made],
 ["chicken","Chicken", [("chicken",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 95,weight(10)|abundance(110)|food_quality(40)|max_ammo(55),imodbits_none],
 ["pork","Pork", [("pork",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 75,weight(15)|abundance(100)|food_quality(70)|max_ammo(55),imodbits_none],
 ["butter","Butter", [("butter_pot",0)], itp_merchandise|itp_type_goods|itp_consumable|itp_food, 0, 150,weight(6)|abundance(110)|food_quality(40)|max_ammo(35),imodbit_fine|imodbit_exquisite|imodbit_cheap|imodbit_well_made],

 ["occc_supply_food","Supply Cart", [("winery_wine_cart_loaded",0)], itp_type_goods|itp_consumable|itp_food, 0, 500,weight(60)|abundance(110)|food_quality(40)|max_ammo(250),imodbit_fine|imodbit_exquisite|imodbit_cheap|imodbit_well_made],

 #Would like to remove flour altogether and reduce chicken, pork and butter (perishables) to non-trade items. Apples could perhaps become a generic "fruit", also representing dried fruit and grapes
 # Armagan: changed order so that it'll be easier to remove them from trade goods if necessary.
#************************************************************************************************
# ITEMS before this point are hardcoded into item_codes.h and their order should not be changed!
#************************************************************************************************

# QUEST ITEMS
 ["siege_supply","Supplies", [("ale_barrel",0)], itp_type_goods, 0, 96,weight(40)|abundance(70),imodbits_none],
 ["quest_wine","Wine", [("amphora_slim",0)], itp_type_goods, 0, 46,weight(40)|abundance(60)|max_ammo(50),imodbits_none],
 ["quest_ale","Ale", [("ale_barrel",0)], itp_type_goods, 0, 31,weight(40)|abundance(70)|max_ammo(50),imodbits_none],


# TUTORIAL ITEMS
["tutorial_sword", "Sword", [("long_sword",0),("scab_longsw_a",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 0, weight(1.5)|difficulty(0)|spd_rtng(100)|weapon_length(102)|swing_damage(18,cut)|thrust_damage(15,pierce), imodbits_sword ],
["tutorial_axe", "Axe", [("iron_ax",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_axe_back, 0, weight(4)|difficulty(0)|spd_rtng(91)|weapon_length(108)|swing_damage(19,cut)|thrust_damage(0,pierce), imodbits_axe ],
["tutorial_spear", "Spear", [("spear",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_penalty_with_shield, itc_spear, 0, weight(4.5)|difficulty(0)|spd_rtng(80)|weapon_length(158)|swing_damage(0,cut)|thrust_damage(19,pierce), imodbits_polearm ],
["tutorial_club", "Club", [("club",0)], itp_type_one_handed_wpn|itp_wooden_attack|itp_wooden_parry|itp_primary, itc_scimitar, 0, weight(2.5)|difficulty(0)|spd_rtng(95)|weapon_length(95)|swing_damage(11,blunt)|thrust_damage(0,pierce), imodbits_none ],
["tutorial_battle_axe", "Battle Axe", [("battle_ax",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_axe_back, 0, weight(5)|difficulty(0)|spd_rtng(88)|weapon_length(108)|swing_damage(27,cut)|thrust_damage(0,pierce), imodbits_axe ],
["tutorial_arrows", "Arrows", [("arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(3)|abundance(160)|weapon_length(95)|thrust_damage(0,pierce)|max_ammo(20), imodbits_missile, missile_distance_trigger ],
["tutorial_bolts", "Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag",ixmesh_carry),("bolt_bag_b",ixmesh_carry|imodbit_large_bag)], itp_type_bolts, itcf_carry_quiver_right_vertical, 0, weight(2.25)|abundance(90)|weapon_length(63)|thrust_damage(0,pierce)|max_ammo(18), imodbits_missile, missile_distance_trigger ],
["tutorial_short_bow", "Short Bow", [("short_bow",0),("short_bow_carry",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1)|difficulty(0)|spd_rtng(98)|shoot_speed(49)|thrust_damage(12,pierce), imodbits_bow ],
["tutorial_crossbow", "Crossbow", [("crossbow_a",0)], itp_type_crossbow|itp_cant_reload_on_horseback|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 0, weight(3)|difficulty(0)|spd_rtng(42)|shoot_speed(68)|thrust_damage(32,pierce)|max_ammo(1), imodbits_crossbow ],
["tutorial_throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown|itp_primary, itcf_throw_knife, 0, weight(3.5)|difficulty(0)|spd_rtng(102)|shoot_speed(25)|thrust_damage(16,cut)|max_ammo(14)|weapon_length(0), imodbits_missile, missile_distance_trigger ],
["tutorial_saddle_horse", "Saddle Horse", [("saddle_horse",0)], itp_type_horse, 0, 0, abundance(90)|body_armor(3)|difficulty(0)|horse_speed(40)|horse_maneuver(38)|horse_charge(8), imodbits_horse_basic ],
["tutorial_shield", "Kite Shield", [("shield_kite_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 118, weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(150), imodbits_shield ],
["tutorial_staff_no_attack", "Staff", [("wooden_staff",0)], itp_type_polearm|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance, itc_parry_polearm|itcf_carry_sword_back, 9, weight(3.5)|spd_rtng(120)|weapon_length(115)|swing_damage(0,blunt)|thrust_damage(0,blunt), imodbits_none ],
["tutorial_staff", "Staff", [("wooden_staff",0)], itp_type_polearm|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance, itc_staff|itcf_carry_sword_back, 9, weight(3.5)|spd_rtng(120)|weapon_length(115)|swing_damage(16,blunt)|thrust_damage(16,blunt), imodbits_none ],

["pilgrim_disguise", "Pilgrim Disguise", [("pilgrim_outfit",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|0, 0, 25, weight(2)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["pilgrim_hood", "Pilgrim Hood", [("pilgrim_hood",0)], itp_type_head_armor|itp_civilian|0, 0, 35, weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["torch", "Torch", [("club",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar, 11, weight(2.5)|difficulty(0)|spd_rtng(95)|weapon_length(95)|swing_damage(11,blunt)|thrust_damage(0,pierce), imodbits_none, [(ti_on_init_item,[(set_position_delta,0,60,0),(particle_system_add_new,"psys_torch_fire"),(particle_system_add_new,"psys_torch_smoke"),(set_current_color,150,130,70),(add_point_light,10,30),])] ],

["lyre", "Lyre", [("lyre",0)], itp_type_shield|itp_wooden_parry|itp_civilian, itcf_carry_bow_back, 118, weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90), imodbits_none ],
["lute", "Lute", [("lute",0)], itp_type_shield|itp_wooden_parry|itp_civilian, itcf_carry_bow_back, 118, weight(2.5)|hit_points(480)|body_armor(1)|spd_rtng(82)|weapon_length(90), imodbits_none ],

#instrumentals end
["tunic_with_green_cape", "Tunic with Green Cape", [("peasant_man_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 6, weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["keys", "Ring of Keys", [("throwing_axe_a",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar, 240, weight(5)|spd_rtng(98)|swing_damage(29,cut)|max_ammo(5)|weapon_length(53), imodbits_thrown ],
["bride_dress", "Bride Dress", [("bride_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["bride_crown", "Crown of Flowers", [("bride_crown",0)], itp_type_head_armor|itp_attach_armature|itp_doesnt_cover_hair|itp_civilian, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["bride_shoes", "Bride Shoes", [("bride_shoes",0)], itp_type_foot_armor|itp_attach_armature|itp_civilian, 0, 30, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(8)|difficulty(0), imodbits_cloth ],

["practice_bow_2", "Practice Bow", [("hunting_bow",0),("hunting_bow_carry",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 0, weight(1.5)|spd_rtng(90)|shoot_speed(40)|thrust_damage(21,blunt), imodbits_bow ],
["practice_arrows_2", "Practice Arrows", [("arena_arrow",0),("flying_missile",ixmesh_flying_ammo),("quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back, 0, weight(1.5)|weapon_length(95)|max_ammo(80), imodbits_missile, missile_distance_trigger ],
["mail_boots_for_tableau", "Mail Boots", [("mail_boots_a",0)], itp_type_foot_armor|itp_attach_armature, 0, 1, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(1), imodbits_armor ],

##diplomacy begin
["dplmc_coat_of_plates_red_constable", "Constable Coat of Plates", [("coat_of_plates_red",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 3828, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(0), imodbits_armor ],
##diplomacy end
################################################################################
#CC-C begin
################################################################################
#unused
#dagger
["dagger", "Dagger", [("dagger_b",0),("dagger_b_scabbard",ixmesh_carry),("dagger_b",imodbits_good),("dagger_b_scabbard",ixmesh_carry|imodbits_good)], itp_type_one_handed_wpn|itp_no_parry|itp_merchandise|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn, 37, weight(0.75)|difficulty(0)|spd_rtng(129)|weapon_length(47)|swing_damage(22,cut)|thrust_damage(19,pierce), imodbits_sword_high ],
["ccc_dagger_oreichalkon", "Oreichalkon Dagger", [("sting",0),("sting_scabbard",ixmesh_carry),], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 6545, weight(0.75)|difficulty(0)|spd_rtng(140)|weapon_length(60)|swing_damage(29,cut)|thrust_damage(25,pierce), imodbits_sword_high ],
["ccc_dagger_legolas_knife", "Legolas Knife", [("legolas_knife",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_left|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 300, weight(0.5)|spd_rtng(132)|weapon_length(60)|swing_damage(38,blunt)|thrust_damage(34,blunt), imodbits_none ],
["ccc_dagger_legolas_shield", "Legolas Knife Shield", [("legolas_knife_shield",0)], itp_type_shield, itcf_carry_sword_left_hip, 700, weight(1)|hit_points(540)|head_armor(2)|body_armor(5)|leg_armor(3)|spd_rtng(120)|weapon_length(30), imodbits_shield ],
["ccc_dagger_hadafang", "Hadhafang", [("talak_seax",0),("talak_scab_seax",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_dagger|itcf_carry_dagger_front_left|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 2048, weight(0.5)|spd_rtng(125)|weapon_length(50)|swing_damage(35,blunt)|thrust_damage(34,blunt), imodbits_none ],
["ccc_dagger_ivoryhiltdag", "Ivory Hilt Dagger", [("IvoryHiltDag",0)], itp_type_one_handed_wpn|itp_no_parry|itp_primary, itc_dagger|itcf_carry_dagger_front_right|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 300, weight(0.5)|spd_rtng(125)|weapon_length(65)|swing_damage(36,blunt)|thrust_damage(24,blunt), imodbits_none ],
["ccc_dagger_roma_pugio", "Pugio", [("pugio",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_right|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 80, weight(0.5)|spd_rtng(120)|weapon_length(65)|swing_damage(26,blunt)|thrust_damage(24,blunt), imodbits_none ],
["ccc_dagger_jp_aikuti", "Aikuti", [("aikuchi",0),("aikuchi_with_saya",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary, itc_dagger|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 800, weight(0.5)|spd_rtng(125)|weapon_length(50)|swing_damage(35,blunt)|thrust_damage(34,blunt), imodbits_sword, [],[fac_kingdom_9,fac_bushido_order] ],
["ccc_dagger_jp_aikuti_shield", "Aikuti Shield", [("aikuchishieldb",0),("aikuchi_with_saya",ixmesh_carry)], itp_type_shield, itcf_carry_dagger_front_left, 700, weight(1)|hit_points(240)|body_armor(5)|spd_rtng(120)|weapon_length(30), imodbits_shield ],

#one-hand-sword
["sickle", "Sickle", [("sickle",0)], itp_type_one_handed_wpn|itp_no_parry|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary, itc_cleaver, 9, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(40)|swing_damage(20,cut)|thrust_damage(0,pierce), imodbits_none ],
["military_sickle_a", "Military Sickle", [("military_sickle_a",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary, itc_scimitar|itcf_carry_axe_left_hip, 220, weight(1.0)|difficulty(9)|spd_rtng(100)|weapon_length(75)|swing_damage(26,pierce)|thrust_damage(0,pierce), imodbits_axe ],
["cleaver", "Cleaver", [("cleaver_new",0)], itp_type_one_handed_wpn|itp_no_parry|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary, itc_cleaver, 14, weight(1.5)|difficulty(0)|spd_rtng(103)|weapon_length(35)|swing_damage(24,cut)|thrust_damage(0,pierce), imodbits_none ],
["military_cleaver_b", "Soldier's Cleaver", [("military_cleaver_b",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 193, weight(1.5)|difficulty(0)|spd_rtng(96)|weapon_length(95)|swing_damage(31,cut)|thrust_damage(0,pierce), imodbits_sword_high ],
["military_cleaver_c", "Military Cleaver", [("military_cleaver_c",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 263, weight(1.5)|difficulty(0)|spd_rtng(96)|weapon_length(95)|swing_damage(35,cut)|thrust_damage(0,pierce), imodbits_sword_high ],
["knife", "Knife", [("peasant_knife_new",0)], itp_type_one_handed_wpn|itp_no_parry|itp_merchandise|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_left, 18, weight(0.5)|difficulty(0)|spd_rtng(110)|weapon_length(40)|swing_damage(21,cut)|thrust_damage(13,pierce), imodbits_sword ],
["butchering_knife", "Butchering Knife", [("khyber_knife_new",0)], itp_type_one_handed_wpn|itp_no_parry|itp_merchandise|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_right, 23, weight(0.75)|difficulty(0)|spd_rtng(108)|weapon_length(60)|swing_damage(24,cut)|thrust_damage(17,pierce), imodbits_sword ],
["falchion", "Falchion", [("falchion_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 105, weight(2.5)|difficulty(8)|spd_rtng(98)|weapon_length(73)|swing_damage(30,cut)|thrust_damage(0,pierce), imodbits_sword ],
["sword_medieval_a", "Sword", [("sword_medieval_a",0),("sword_medieval_a_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 163, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(27,cut)|thrust_damage(22,pierce), imodbits_sword_high ],
["sword_medieval_b", "Sword", [("sword_medieval_b",0),("sword_medieval_b_scabbard",ixmesh_carry),("sword_rusty_a",imodbit_rusty),("sword_rusty_a_scabbard",ixmesh_carry|imodbit_rusty)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 243, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(28,cut)|thrust_damage(23,pierce), imodbits_sword_high ],
["sword_medieval_b_small", "Short Sword", [("sword_medieval_b_small",0),("sword_medieval_b_small_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 152, weight(1)|difficulty(0)|spd_rtng(102)|weapon_length(85)|swing_damage(26,cut)|thrust_damage(24,pierce), imodbits_sword_high ],
["sword_medieval_c", "Arming Sword", [("sword_medieval_c",0),("sword_medieval_c_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 410, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(29,cut)|thrust_damage(24,pierce), imodbits_sword_high ],
["sword_medieval_c_small", "Short Arming Sword", [("sword_medieval_c_small",0),("sword_medieval_c_small_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 243, weight(1)|difficulty(0)|spd_rtng(103)|weapon_length(86)|swing_damage(26,cut)|thrust_damage(24,pierce), imodbits_sword_high ],
["sword_medieval_c_long", "Arming Sword", [("sword_medieval_c_long",0),("sword_medieval_c_long_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 480, weight(1.7)|difficulty(0)|spd_rtng(99)|weapon_length(100)|swing_damage(29,cut)|thrust_damage(28,pierce), imodbits_sword_high ],
["sword_medieval_d_long", "Long Arming Sword", [("sword_medieval_d_long",0),("sword_medieval_d_long_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 550, weight(1.8)|difficulty(0)|spd_rtng(96)|weapon_length(105)|swing_damage(33,cut)|thrust_damage(28,pierce), imodbits_sword ],
["sword_viking_1", "Nordic Sword", [("sword_viking_c",0),("sword_viking_c_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 147, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(94)|swing_damage(28,cut)|thrust_damage(20,pierce), imodbits_sword_high ],
["sword_viking_2", "Nordic Sword", [("sword_viking_b",0),("sword_viking_b_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 276, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(29,cut)|thrust_damage(21,pierce), imodbits_sword_high ],
["sword_viking_2_small", "Nordic Short Sword", [("sword_viking_b_small",0),("sword_viking_b_small_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 162, weight(1.25)|difficulty(0)|spd_rtng(103)|weapon_length(85)|swing_damage(28,cut)|thrust_damage(21,pierce), imodbits_sword_high ],
["sword_viking_3", "Nordic War Sword", [("sword_viking_a",0),("sword_viking_a_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 394, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(95)|swing_damage(30,cut)|thrust_damage(21,pierce), imodbits_sword_high ],
["sword_viking_3_small", "Nordic Short War Sword", [("sword_viking_a_small",0),("sword_viking_a_small_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 280, weight(1.25)|difficulty(0)|spd_rtng(103)|weapon_length(86)|swing_damage(29,cut)|thrust_damage(21,pierce), imodbits_sword_high ],
["ncmm_sword_viking_3_small", "Highlander Short Sword", [("dirk",0),("sword_viking_a_small_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 280, weight(1.25)|difficulty(0)|spd_rtng(103)|weapon_length(86)|swing_damage(29,cut)|thrust_damage(21,pierce), imodbits_sword_high ],
["arabian_sword_a", "Sarranid Sword", [("arabian_sword_a",0),("scab_arabian_sword_a",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 108, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(97)|swing_damage(26,cut)|thrust_damage(19,pierce), imodbits_sword_high ],
["arabian_sword_b", "Sarranid Arming Sword", [("arabian_sword_b",0),("scab_arabian_sword_b",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 218, weight(1.7)|difficulty(0)|spd_rtng(99)|weapon_length(97)|swing_damage(28,cut)|thrust_damage(19,pierce), imodbits_sword_high ],
["sarranid_cavalry_sword", "Sarranid Cavalry Sword", [("arabian_sword_c",0),("scab_arabian_sword_c",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 310, weight(1.5)|difficulty(0)|spd_rtng(98)|weapon_length(105)|swing_damage(28,cut)|thrust_damage(19,pierce), imodbits_sword_high ],
["arabian_sword_d", "Sarranid Guard Sword", [("arabian_sword_d",0),("scab_arabian_sword_d",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 420, weight(1.7)|difficulty(0)|spd_rtng(99)|weapon_length(97)|swing_damage(30,cut)|thrust_damage(20,pierce), imodbits_sword_high ],

["ccc_sword_clontarf", "Sting", [("sting_long",0),("sting_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 270, weight(1.5)|difficulty(11)|spd_rtng(110)|weapon_length(80)|swing_damage(36,cut)|thrust_damage(27,pierce), imodbits_sword ],
["ccc_sword_count", "Bastard Count Sword", [("g101",0),("g101_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 270, weight(1.5)|difficulty(14)|spd_rtng(110)|weapon_length(100)|swing_damage(36,cut)|thrust_damage(36,pierce), imodbits_sword ],  ## cave09 g101->bastard_RNC
["ccc_sword_hospitaller", "Hospitaller Sword", [("runico_realblade",0),("runico_realblade_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 300, weight(1.5)|difficulty(11)|spd_rtng(101)|weapon_length(98)|swing_damage(30,cut)|thrust_damage(29,pierce), imodbits_sword ],  ## cave09 runico_realblade->wolfsword
["ccc_sword_templar", "Templar Sword", [("templar_sword",0),("templar_sword_scrab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 400, weight(1.5)|difficulty(11)|spd_rtng(105)|weapon_length(96)|swing_damage(39,cut)|thrust_damage(35,pierce), imodbits_sword ],  ## cave09 templar_sword->sword008
["ccc_sword_brasao", "Brasao Sword", [("brasao_sword",0),("brasao_sword_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 300, weight(2.5)|difficulty(10)|spd_rtng(110)|weapon_length(96)|swing_damage(37,cut)|thrust_damage(33,pierce), imodbits_sword_high ],  ## cave09 brasao_sword->spainsword
["ccc_sword_excalibur", "Excalibur", [("excalibur",0),("excalibur_scrab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 250, weight(2.5)|difficulty(10)|spd_rtng(110)|weapon_length(95)|swing_damage(33,cut)|thrust_damage(33,pierce), imodbits_sword_high ],  ## cave09 excalibur->g102"
["ccc_sword_herugrim", "Herugrim Theoden Sword", [("herugrim_theoden_sword",0),("herugrim_theoden_sword_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 300, weight(2.5)|difficulty(10)|spd_rtng(110)|weapon_length(98)|swing_damage(37,cut)|thrust_damage(33,pierce), imodbits_sword_high ],  ## cave09 del
["ccc_sword_viking1", "Viking Sword", [("viking_runico",0),("viking_runico_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 300, weight(2.5)|difficulty(10)|spd_rtng(115)|weapon_length(90)|swing_damage(32,cut)|thrust_damage(31,pierce), imodbits_sword_high ],
["ccc_sword_viking2", "Viking Blade", [("viking_blade_03",0),("viking_blade_03_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 300, weight(2.5)|difficulty(10)|spd_rtng(108)|weapon_length(95)|swing_damage(32,cut)|thrust_damage(32,pierce), imodbits_sword_high ],  ## cave09 viking_blade_03->viking_runico_02
["ccc_sword_rune", "Rune Sword", [("runic_short",0),("runic_short_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 300, weight(2.5)|difficulty(10)|spd_rtng(125)|weapon_length(85)|swing_damage(36,cut)|thrust_damage(32,pierce), imodbits_sword_high ],  ## cave09 del
["ccc_sword_nobleblade", "Noble Blade", [("nobleblade",0),("nobleblade_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 300, weight(2.5)|difficulty(10)|spd_rtng(115)|weapon_length(90)|swing_damage(34,cut)|thrust_damage(32,pierce), imodbits_sword_high ],  ## cave09 nobleblade->sword006
["ccc_sword_aragorn", "Aragorn Sword", [("aragorn_sword",0),("aragorn_sword_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 300, weight(1.5)|difficulty(11)|spd_rtng(101)|weapon_length(98)|swing_damage(40,cut)|thrust_damage(35,pierce), imodbits_sword ],
["ccc_sword_glamdring", "Glamdring", [("glamdring",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword, 300, weight(1.5)|difficulty(11)|spd_rtng(101)|weapon_length(108)|swing_damage(40,cut)|thrust_damage(35,pierce), imodbits_sword ],
["ccc_sword_ring_wriath", "Ring Wriath Sword", [("ring_wriath_sword",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword, 300, weight(1.5)|difficulty(11)|spd_rtng(101)|weapon_length(97)|swing_damage(40,cut)|thrust_damage(35,pierce), imodbits_sword ],
["ccc_sword_uruk_hai", "Uruk Hai Sword", [("uruk_hai_sword",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_quiver_back, 300, weight(1.5)|difficulty(13)|spd_rtng(98)|weapon_length(99)|swing_damage(45,cut)|thrust_damage(0,pierce), imodbits_sword ],
["ccc_sword_witch_king_sword", "Witch King Sword", [("witch_king_sword",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword, 300, weight(1.5)|difficulty(11)|spd_rtng(101)|weapon_length(98)|swing_damage(42,cut)|thrust_damage(35,pierce), imodbits_sword ],
["ccc_sword_theoden", "Theoden Sword", [("theoden_sword",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword, 300, weight(1.5)|difficulty(11)|spd_rtng(101)|weapon_length(98)|swing_damage(40,cut)|thrust_damage(35,pierce), imodbits_sword ],  ## cave09 del
["ccc_sword_talon_of_akatosh", "Talon Of Akatosh", [("TalonOfAkatosh",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 3000, weight(1.5)|difficulty(10)|spd_rtng(101)|weapon_length(95)|swing_damage(45,cut)|thrust_damage(40,pierce), imodbits_sword ],
["ccc_sword_talon_of_akatosh_imitate", "Talon Of Akatosh Imitate", [("TalonOfAkatosh_fake",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 300, weight(1.5)|difficulty(10)|spd_rtng(99)|weapon_length(95)|swing_damage(39,cut)|thrust_damage(32,pierce), imodbits_sword ],
["ccc_sword_met_scimitar", "MetScimitar", [("MetScimitar",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 3000, weight(1.5)|difficulty(11)|spd_rtng(95)|weapon_length(120)|swing_damage(45,cut)|thrust_damage(0,pierce), imodbits_sword ],
#["ccc_sword_ninjato", "Ninjato", [("demon_sword",0),("demon_sword_scab",ixmesh_carry)], itp_type_one_handed_wpn|itp_two_handed|itp_primary, itc_longsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 1024, weight(3)|difficulty(14)|spd_rtng(110)|weapon_length(90)|swing_damage(41,cut)|thrust_damage(38,pierce), imodbits_sword_high ],
["ccc_sword_roma_falx", "Falx", [("falx",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 200, weight(1.5)|difficulty(11)|spd_rtng(90)|weapon_length(80)|swing_damage(33,cut)|thrust_damage(28,pierce), imodbits_sword ],
#buffed gladius occc
["ccc_sword_roma_gladius_fulham", "Gladius Fulham", [("gladius_fulham",0),("gladius_fulham_scabbard",ixmesh_carry),], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 280, weight(1.5)|difficulty(11)|spd_rtng(123)|weapon_length(80)|swing_damage(33,cut)|thrust_damage(30,pierce), imodbits_sword ],
["ccc_sword_roma_gladius_pompeii", "Gladius Pompeii", [("gladius_pompeii",0),("gladius_pompeii_scabbard",ixmesh_carry),], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 280, weight(1.5)|difficulty(11)|spd_rtng(123)|weapon_length(80)|swing_damage(35,cut)|thrust_damage(32,pierce), imodbits_sword ],
["ccc_sword_roma_spatha3", "Spatha", [("spatha3",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 400, weight(1.5)|difficulty(12)|spd_rtng(95)|weapon_length(105)|swing_damage(41,cut)|thrust_damage(30,pierce), imodbits_sword ],
["ccc_sword_roma_celtsword1", "Celt Sword", [("celtsword1",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 500, weight(1.5)|difficulty(12)|spd_rtng(98)|weapon_length(98)|swing_damage(42,cut)|thrust_damage(32,pierce), imodbits_sword ],
["ccc_sword_roma_celtsword2", "Celt Sword", [("celtsword2",0)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 550, weight(1.5)|difficulty(12)|spd_rtng(98)|weapon_length(98)|swing_damage(44,cut)|thrust_damage(34,pierce), imodbits_sword ],
#occc end
["ccc_sword_glaive_blade", "GlaiveBlade", [("GlaiveBlade",0)], itp_type_one_handed_wpn|itp_primary, itcf_overswing_onehanded|itcf_slashright_onehanded|itcf_slashleft_onehanded|itcf_carry_sword_back|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded|itcf_force_64_bits, 500, weight(1.5)|difficulty(12)|spd_rtng(115)|weapon_length(100)|swing_damage(43,cut)|thrust_damage(0,pierce), imodbits_sword ],
["ccc_shield_glaive_blade", "GlaiveBlade", [("GlaiveShield",0)], itp_type_shield, itcf_carry_round_shield, 500, weight(2.5)|hit_points(600)|body_armor(10)|spd_rtng(120)|shield_width(50), imodbits_shield ],
["khergit_sword", "Khergit Sword", [("khergit_sword",0),("khergit_sword_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 600, weight(1.25)|difficulty(0)|spd_rtng(100)|weapon_length(97)|swing_damage(36,cut)|thrust_damage(21,pierce), imodbits_sword ],
["ccc_sword_king", "King Sword", [("broadswordc",0),("broadswordcscaba",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 2000, weight(2.5)|difficulty(15)|spd_rtng(120)|weapon_length(93)|swing_damage(37,cut)|thrust_damage(33,pierce), imodbits_sword_high ],
["ccc_sword_bk", "Black Knight Sword", [("demon_sword",0),("demon_sword_scab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 3072, weight(2.5)|difficulty(15)|spd_rtng(110)|weapon_length(110)|swing_damage(37,cut)|thrust_damage(34,pierce), imodbits_sword_high ],
["ccc_sword_valkyrie", "Valkyrie Sword", [("g102",0),("g102_scabbard",ixmesh_carry)], itp_merchandise|itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 3072, abundance(500)|weight(2)|difficulty(14)|spd_rtng(120)|weapon_length(93)|swing_damage(34,cut)|thrust_damage(32,pierce), imodbits_sword_high,[],[fac_valkyrie] ],
["ccd_daedricrsword", "Daedricr Sword", [("DaedricrSword",0),("DaedricrSword_scab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 3072, weight(3)|difficulty(15)|spd_rtng(105)|weapon_length(100)|swing_damage(40,blunt)|thrust_damage(38,pierce), imodbits_sword_high ],

#thrust
["ccc_sword_ivory_hilt", "Ivory Hilt", [("IvoryHilt",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_penalty_with_shield|itp_crush_through, itcf_thrust_onehanded|itcf_horseback_thrust_onehanded|itcf_carry_sword_left_hip|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 400, weight(1.5)|difficulty(11)|spd_rtng(130)|weapon_length(100)|swing_damage(0,cut)|thrust_damage(32,pierce), imodbits_sword ],  ## cave09 del
["ccc_sword_rapier", "Rapier", [("rapierec",0),("rapierecscaba",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_can_penetrate_shield|itp_penalty_with_shield|itp_crush_through, itcf_thrust_onehanded|itcf_horseback_thrust_onehanded|itcf_carry_sword_left_hip|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 350, weight(1.5)|difficulty(11)|spd_rtng(140)|weapon_length(100)|swing_damage(0,cut)|thrust_damage(29,pierce), imodbits_sword ],
["ccc_sword_adorn", "Adorn", [("talak_foil",0),("talak_scab_foil",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_can_penetrate_shield|itp_penalty_with_shield|itp_crush_through, itcf_thrust_onehanded|itcf_horseback_thrust_onehanded|itcf_carry_sword_left_hip|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded|itcf_show_holster_when_drawn, 624, weight(1.5)|difficulty(11)|spd_rtng(140)|weapon_length(100)|swing_damage(0,cut)|thrust_damage(29,pierce), imodbits_sword ],
["ccc_sword_plated", "Plated", [("talak_estoc",0),("talak_scab_estoc",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_penalty_with_shield|itp_next_item_as_melee|itp_crush_through, itcf_thrust_onehanded|itcf_carry_sword_left_hip|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded|itcf_show_holster_when_drawn, 400, weight(1.5)|difficulty(11)|spd_rtng(125)|weapon_length(100)|swing_damage(0,cut)|thrust_damage(38,pierce), imodbits_sword ],
["ccc_sword_plated_cut", "Plated_cut", [("talak_estoc",0),("talak_scab_estoc",ixmesh_carry)], itp_type_one_handed_wpn|itp_unique|itp_primary|itp_penalty_with_shield|itp_remove_item_on_use, itcf_overswing_onehanded|itcf_slashright_onehanded|itcf_slashleft_onehanded|itcf_carry_sword_left_hip|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 700, weight(1.5)|difficulty(11)|spd_rtng(110)|weapon_length(100)|swing_damage(30,cut)|thrust_damage(33,pierce), imodbits_sword ],

#Scimitars
["scimitar", "Scimitar", [("scimitar_a",0),("scab_scimeter_a",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 210, weight(1.5)|difficulty(0)|spd_rtng(101)|weapon_length(97)|swing_damage(30,cut)|thrust_damage(0,pierce), imodbits_sword_high ],
["scimitar_b", "Elite Scimitar", [("scimitar_b",0),("scab_scimeter_b",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 290, weight(1.5)|difficulty(0)|spd_rtng(100)|weapon_length(103)|swing_damage(32,cut)|thrust_damage(0,pierce), imodbits_sword_high ],
["ccc_sword_scimitar_sulatn", "Scimitar", [("cimitar",0),("cimitarscaba",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 1024, weight(2.0)|difficulty(0)|spd_rtng(97)|weapon_length(115)|swing_damage(38,cut)|thrust_damage(0,pierce), imodbits_sword_high ],

#Sabel
["sword_khergit_1", "Nomad Sabre", [("khergit_sword_b",0),("khergit_sword_b_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 105, weight(1.25)|difficulty(0)|spd_rtng(100)|weapon_length(97)|swing_damage(29,cut), imodbits_sword_high ],
["sword_khergit_2", "Sabre", [("khergit_sword_c",0),("khergit_sword_c_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 191, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(97)|swing_damage(30,cut), imodbits_sword_high ],
["sword_khergit_3", "Sabre", [("khergit_sword_a",0),("khergit_sword_a_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 294, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(98)|swing_damage(31,cut), imodbits_sword_high ],
["sword_khergit_4", "Heavy Sabre", [("khergit_sword_d",0),("khergit_sword_d_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 384, weight(1.75)|difficulty(0)|spd_rtng(98)|weapon_length(96)|swing_damage(33,cut), imodbits_sword_high ],
["khergit_sword_two_handed_a", "Two Handed Sabre", [("khergit_sword_two_handed_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 523, weight(2.75)|difficulty(10)|spd_rtng(96)|weapon_length(120)|swing_damage(40,cut)|thrust_damage(0,pierce), imodbits_sword_high ],
["khergit_sword_two_handed_b", "Two Handed Sabre", [("khergit_sword_two_handed_b",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 920, weight(2.75)|difficulty(10)|spd_rtng(96)|weapon_length(120)|swing_damage(44,cut)|thrust_damage(0,pierce), imodbits_sword_high ],

["ccc_sword_18_sabre1", "Sabre", [("sabre_hank_2",0),("sabre_hank_2_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 450, weight(1.75)|difficulty(0)|spd_rtng(105)|weapon_length(95)|swing_damage(38,cut), imodbits_sword_high ],  ## cave09 sabre_hank_2->snake_gold
["ccc_sword_18_sabre2", "Sabre", [("Cat-Schiavona1",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 500, weight(1.75)|difficulty(0)|spd_rtng(105)|weapon_length(95)|swing_damage(40,cut)|thrust_damage(35,pierce)|body_armor(4), imodbits_sword_high ],
["ccc_sword_exotic_sabre", "Exotic Sabre", [("exotic_sabre",0),("exotic_sabre_scarab",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 700, weight(2.5)|difficulty(10)|spd_rtng(105)|weapon_length(95)|swing_damage(36,cut)|thrust_damage(0,pierce), imodbits_sword_high ],  ## cave09 del
["ccc_sword_great_sabre", "Great Sabre", [("greatfalchion",0),("greatfalchion_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 880, weight(2.5)|difficulty(10)|spd_rtng(100)|weapon_length(105)|swing_damage(37,cut)|thrust_damage(0,pierce), imodbits_sword_high ],
#katana real_falchion09
["strange_sword", "Strange Sword", [("katana",0),("katana_scabbard",ixmesh_carry)], itp_type_two_handed_wpn|itp_primary, itc_bastardsword|itcf_carry_katana|itcf_show_holster_when_drawn, 679, weight(2.0)|difficulty(9)|spd_rtng(108)|weapon_length(95)|swing_damage(32,cut)|thrust_damage(18,pierce), imodbits_sword, [],[fac_kingdom_9,fac_bushido_order] ],
["strange_great_sword", "Strange Great Sword", [("no_dachi",0),("no_dachi_scabbard",ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back|itcf_show_holster_when_drawn, 920, weight(3.5)|difficulty(11)|spd_rtng(92)|weapon_length(125)|swing_damage(38,cut)|thrust_damage(0,pierce), imodbits_axe, [],[fac_kingdom_9,fac_bushido_order] ],
["strange_short_sword", "Strange Short Sword", [("wakizashi",0),("wakizashi_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn, 321, weight(1.25)|difficulty(0)|spd_rtng(108)|weapon_length(65)|swing_damage(25,cut)|thrust_damage(19,pierce), imodbits_sword, [],[fac_kingdom_9,fac_bushido_order] ],
["ccc_sword_two_jp_no_dachi_samurai10", "Kiku Itimozi", [("no_dachi_samurai10",0),("no_dachi_samurai10_fourreau",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back|itcf_show_holster_when_drawn, 9545, weight(3.5)|difficulty(11)|spd_rtng(92)|weapon_length(125)|swing_damage(41,cut)|thrust_damage(0,pierce), imodbits_axe, [],[fac_kingdom_9,fac_bushido_order] ],  ## cave09 no_dachi_samurai10->dachi_01
["ccc_sword_two_jp_no_dachi_samurai02", "Nodati", [("no_dachi_samurai02",0),("no_dachi_samurai02_fourreau",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back|itcf_show_holster_when_drawn, 6545, weight(3.5)|difficulty(11)|spd_rtng(95)|weapon_length(120)|swing_damage(41,cut)|thrust_damage(0,pierce), imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],  ## cave09 no_dachi_samurai02->dachi_02
["ccc_sword_jp_katana_samurai10", "Katana", [("katana_samurai10",0),("katana_samurai10_fourreau",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_katana|itcf_show_holster_when_drawn, 9545, weight(2.0)|difficulty(9)|spd_rtng(108)|weapon_length(95)|swing_damage(37,cut)|thrust_damage(28,pierce), imodbits_sword, [],[fac_kingdom_9,fac_bushido_order] ],  ## cave09 katana_samurai10->katana_01
["ccc_sword_jp_katana_samurai02", "Samurai Sabre", [("katana_samurai02",0),("katana_samurai02_fourreau",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_katana|itcf_show_holster_when_drawn, 9545, weight(2.0)|difficulty(9)|spd_rtng(105)|weapon_length(100)|swing_damage(41,cut)|thrust_damage(31,pierce), imodbits_sword, [],[fac_kingdom_9,fac_bushido_order] ],  ## cave09 katana_samurai02->katana_02
["ccc_throwing_sword_jp_wakizashi_samurai10", "Wakizasi", [("wakizashi_samurai10",0),("wakizashi_samurai10_fourreau",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary|itp_next_item_as_melee, itcf_throw_axe|itcf_carry_wakizashi|itcf_show_holster_when_drawn, 9545, weight(2)|difficulty(0)|spd_rtng(110)|shoot_speed(20)|thrust_damage(72,cut)|max_ammo(1)|weapon_length(83), imodbits_thrown_minus_heavy, missile_distance_trigger,[fac_kingdom_9,fac_bushido_order] ],  ## cave09 wakizashi_samurai->10katanarr
["ccc_sword_jp_wakizashi_samurai10_fourreau_melee", "Wakizashi Melee", [("wakizashi_samurai10",0),("wakizashi_samurai10_fourreau",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_remove_item_on_use, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn, 9545, weight(1.25)|difficulty(0)|spd_rtng(108)|weapon_length(65)|swing_damage(35,cut)|thrust_damage(29,pierce), imodbits_sword, [],[fac_kingdom_9,fac_bushido_order] ],  ## cave09 wakizashi_samurai->10katanarr
["ccd_kodachi", "Kodachi", [("kodachi_a", 0), ("kodachia_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 1024, weight(1.2)|difficulty(10)|spd_rtng(105)|weapon_length(60)|swing_damage(28, cut)|thrust_damage(16,  pierce), imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["ccd_ninjato", "Yoroi Doshi", [("njbl", 0), ("njbl_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn, 1024, weight(1.5)|difficulty(10)|spd_rtng(106)|weapon_length(90)|swing_damage(29, pierce)|thrust_damage(28,  pierce), imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["ccd_nagamitsu", "Daihannya Nagamitsu", [("ccd_k_nagamitsu", 0),("ccd_k_nagamitsu_saya", ixmesh_carry)], itp_type_two_handed_wpn|itp_next_item_as_melee|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration, itc_nodachi|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 4800, weight(2.3)|difficulty(21)|spd_rtng(115)|weapon_length(120)|swing_damage(56, cut), imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["ccd_nagamitsu_melee", "Daihannya Nagamitsu Melee", [("ccd_k_nagamitsumel", 0),("ccd_k_nagamitsu_saya", ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration, itc_nodachi|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 4800, weight(2.3)|difficulty(21)|spd_rtng(115)|weapon_length(120)|swing_damage(45, blunt), imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],

#two-hand_sword
["two_handed_cleaver", "War Cleaver", [("military_cleaver_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 640, weight(2.75)|difficulty(10)|spd_rtng(93)|weapon_length(120)|swing_damage(45,cut)|thrust_damage(0,cut), imodbits_sword_high ],
["great_sword", "Great Sword", [("bastard_sword",0),("scab_bastardsw",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 423, weight(2.75)|difficulty(10)|spd_rtng(95)|weapon_length(125)|swing_damage(39,cut)|thrust_damage(31,pierce), imodbits_sword_high ],
["sword_of_war", "Sword of War", [("b_bastard_sword",0),("scab_bastardsw_b",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 524, weight(3)|difficulty(11)|spd_rtng(94)|weapon_length(130)|swing_damage(40,cut)|thrust_damage(31,pierce), imodbits_sword_high ],
["ncmm_sword_of_war", "Highlander Great Sword", [("2h_claymore",0),("scab_bastardsw_b",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 524, weight(3)|difficulty(11)|spd_rtng(97)|weapon_length(130)|swing_damage(40,cut)|thrust_damage(31,pierce), imodbits_sword_high ],
["sword_two_handed_b", "Two Handed Sword", [("sword_two_handed_b",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 670, weight(2.75)|difficulty(10)|spd_rtng(97)|weapon_length(110)|swing_damage(40,cut)|thrust_damage(28,pierce), imodbits_sword_high ],
["sword_two_handed_a", "Great Sword", [("sword_two_handed_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 1123, weight(2.75)|difficulty(10)|spd_rtng(96)|weapon_length(120)|swing_damage(42,cut)|thrust_damage(29,pierce), imodbits_sword_high ],
#Bastard Swords
["bastard_sword_a", "Bastard Sword", [("bastard_sword_a",0),("bastard_sword_a_scabbard",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 294, weight(2.0)|difficulty(9)|spd_rtng(98)|weapon_length(101)|swing_damage(35,cut)|thrust_damage(26,pierce), imodbits_sword_high ],
["bastard_sword_b", "Heavy Bastard Sword", [("bastard_sword_b",0),("bastard_sword_b_scabbard",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 526, weight(2.25)|difficulty(9)|spd_rtng(97)|weapon_length(105)|swing_damage(37,cut)|thrust_damage(27,pierce), imodbits_sword_high ],

["ccc_sword_two_narsil", "Narsil", [("narsil",0),], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_sword_back, 1024, weight(3)|difficulty(14)|spd_rtng(98)|weapon_length(120)|swing_damage(49,cut)|thrust_damage(42,pierce), imodbits_sword_high ],
["ccc_sword_two_ssabre", "TwoHandSabre", [("2handsSabre",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 6545, weight(2.75)|spd_rtng(93)|weapon_length(110)|swing_damage(45,cut)|thrust_damage(0,blunt), imodbits_sword_high ],  ## cave09 del
["ccc_sword_two_butcher", "Butcher", [("butcher",0),("butcher_scab",ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_back|itcf_show_holster_when_drawn, 526, weight(2.25)|difficulty(9)|spd_rtng(105)|weapon_length(95)|swing_damage(40,cut)|thrust_damage(27,pierce), imodbits_sword_high ],
["ccc_sword_two_1", "Two Hand Sword", [("zweihanderb",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 1024, weight(2.75)|spd_rtng(88)|weapon_length(145)|swing_damage(38,cut)|thrust_damage(32,pierce), imodbits_sword_high ],
["ccc_sword_two_zweihander1", "Zweihander", [("zweihander",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_staff|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_sword_back, 1024, weight(3)|difficulty(11)|spd_rtng(90)|weapon_length(155)|swing_damage(40,cut)|thrust_damage(31,pierce), imodbits_sword_high ],
["ccc_sword_two_witch_king_sword", "Witch King Sword", [("zweihandere",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_penalty_with_shield, itc_greatsword|itcf_carry_sword_back, 1024, weight(3)|difficulty(14)|spd_rtng(93)|weapon_length(170)|swing_damage(50,cut)|thrust_damage(48,pierce), imodbits_sword_high ],  ## cave09 50->41 48->46
["ccc_sword_two_darkhunterswordb", "Dark Hunter Sword", [("darkhunterswordb",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 1024, weight(2.75)|difficulty(10)|spd_rtng(95)|weapon_length(125)|swing_damage(37,cut)|thrust_damage(24,pierce), imodbits_sword_high ],
["ccc_sword_two_souledge", "Soul Edge", [("SoulEdge",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_can_knock_down, itc_bastardsword|itcf_carry_sword_back|itcf_force_64_bits, 80000, weight(8)|difficulty(25)|spd_rtng(110)|weapon_length(145)|swing_damage(65,cut)|thrust_damage(55,pierce), imodbits_sword_high ],
["ccc_sword_two_blade_of_olympus", "Blade Of Olympus", [("BladeOfOlympus",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration|itp_ignore_friction, itc_bastardsword|itcf_carry_sword_back, 1545, weight(3)|difficulty(20)|spd_rtng(93)|weapon_length(135)|swing_damage(55,cut)|thrust_damage(56,pierce), imodbits_sword_high ],#occc 110->97
["ccc_sword_two_chrome_razor", "Chrome Razor", [("ChromeRazor",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_bastardsword|itcf_thrust_onehanded|itcf_overswing_onehanded|itcf_slashright_onehanded|itcf_slashleft_onehanded|itcf_thrust_twohanded|itcf_carry_sword_back|itcf_force_64_bits, 1545, weight(3)|difficulty(15)|spd_rtng(88)|weapon_length(135)|swing_damage(55,cut)|thrust_damage(44,pierce), imodbits_sword_high ],#occc 105->90 56->44
["ccc_sword_two_frostmourne", "Frostmourne", [("Frostmourne",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_sword_back|itcf_force_64_bits, 1545, weight(2.75)|difficulty(10)|spd_rtng(94)|weapon_length(140)|swing_damage(45,cut)|thrust_damage(39,pierce), imodbits_sword_high ],
["ccd_sword_two_gsw", "GSW", [("GSW1",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_bastardsword|itcf_carry_sword_back|itcf_force_64_bits, 2048, weight(3)|difficulty(16)|spd_rtng(100)|weapon_length(120)|swing_damage(60,cut)|thrust_damage(62,pierce), imodbits_sword_high ],


#one-hand_axe
["hatchet", "Hatchet", [("hatchet",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 13, weight(2)|difficulty(0)|spd_rtng(97)|weapon_length(60)|swing_damage(23,cut)|thrust_damage(0,pierce), imodbits_axe ],
["hand_axe", "Hand Axe", [("talak_bearded_axe",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 24, weight(2)|difficulty(7)|spd_rtng(95)|weapon_length(75)|swing_damage(27,cut)|thrust_damage(0,pierce), imodbits_axe ],
["fighting_axe", "Fighting Axe", [("fighting_ax",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 77, weight(2.5)|difficulty(9)|spd_rtng(92)|weapon_length(90)|swing_damage(31,cut)|thrust_damage(0,pierce), imodbits_axe ],
["one_handed_war_axe_a", "One Handed Axe", [("one_handed_war_axe_a",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 87, weight(1.5)|difficulty(9)|spd_rtng(98)|weapon_length(71)|swing_damage(32,cut)|thrust_damage(0,pierce), imodbits_axe ],
["one_handed_battle_axe_a", "One Handed Battle Axe", [("one_handed_battle_axe_a",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 142, weight(1.5)|difficulty(9)|spd_rtng(98)|weapon_length(73)|swing_damage(34,cut)|thrust_damage(0,pierce), imodbits_axe ],
["one_handed_war_axe_b", "One Handed War Axe", [("one_handed_war_axe_b",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 190, weight(1.5)|difficulty(9)|spd_rtng(98)|weapon_length(76)|swing_damage(34,cut)|thrust_damage(0,pierce), imodbits_axe ],
["one_handed_battle_axe_b", "One Handed Battle Axe", [("one_handed_battle_axe_b",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 230, weight(1.75)|difficulty(9)|spd_rtng(98)|weapon_length(72)|swing_damage(36,cut)|thrust_damage(0,pierce), imodbits_axe ],
["one_handed_battle_axe_c", "One Handed Battle Axe", [("one_handed_battle_axe_c",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 550, weight(2.0)|difficulty(9)|spd_rtng(98)|weapon_length(76)|swing_damage(37,cut)|thrust_damage(0,pierce), imodbits_axe ],
["sarranid_axe_a", "Iron Battle Axe", [("one_handed_battle_axe_g",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 250, weight(1.65)|difficulty(9)|spd_rtng(97)|weapon_length(71)|swing_damage(35,cut)|thrust_damage(0,pierce), imodbits_axe ],
["sarranid_axe_b", "Iron War Axe", [("one_handed_battle_axe_h",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 360, weight(1.75)|difficulty(9)|spd_rtng(97)|weapon_length(71)|swing_damage(38,cut)|thrust_damage(0,pierce), imodbits_axe ],

["ccc_axe_roma_dolabra", "Dolabra", [("dolabra",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar|itcf_carry_sword_left_hip, 220, weight(1.5)|difficulty(11)|spd_rtng(95)|weapon_length(80)|swing_damage(25,cut)|thrust_damage(0,pierce), imodbits_sword ],
["ccc_axe_greatking", "Great King Axe", [("greatking_Axe",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_mace_left_hip, 670, weight(3.5)|difficulty(13)|spd_rtng(95)|weapon_length(85)|swing_damage(39,cut)|thrust_damage(0,pierce), imodbits_axe ],
["ccc_axe_great_doubl", "Great Double Axe", [("great_doubleAxe",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_sword_left_hip, 700, weight(3.5)|difficulty(13)|spd_rtng(95)|weapon_length(85)|swing_damage(44,cut)|thrust_damage(0,pierce), imodbits_axe ],
["ccc_axe_chaos1", "Bloodshed Axe", [("executor_axe",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_force_64_bits|itcf_carry_mace_left_hip, 3064, weight(1.5)|abundance(5)|difficulty(9)|spd_rtng(100)|weapon_length(85)|swing_damage(39,cut)|thrust_damage(0,pierce), imodbits_axe ],
["ccc_axe_chaos2", "Chaos Axe", [("great_axe",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_force_64_bits|itcf_carry_sword_left_hip, 3064, weight(1.5)|abundance(5)|difficulty(9)|spd_rtng(120)|weapon_length(71)|swing_damage(40,pierce)|thrust_damage(0,pierce), imodbits_axe ],
["ccc_axe_chaos3", "Doom Axe", [("2dblhead_ax",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield|itp_crush_through, itc_scimitar|itcf_force_64_bits|itcf_carry_sword_left_hip, 3064, weight(1.5)|abundance(5)|difficulty(9)|spd_rtng(110)|weapon_length(71)|swing_damage(45,cut)|thrust_damage(0,pierce), imodbits_axe ],
["ccd_axe_obsidian", "Obsidian Axe", [("ObsidianAxe",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_mace_left_hip|itcf_force_64_bits, 4096, weight(2.0)|difficulty(15)|spd_rtng(100)|weapon_length(65)|swing_damage(38,pierce)|thrust_damage(0,pierce), imodbits_axe ],
["ccd_axe_dargor", "Dargor Axe", [("dargor_axe",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_force_64_bits|itcf_carry_sword_left_hip, 4096, weight(4.5)|difficulty(18)|spd_rtng(98)|weapon_length(98)|swing_damage(48,cut)|thrust_damage(0,pierce), imodbits_axe ],

#two-hand_axe
["axe", "Axe", [("iron_ax",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 65, weight(4)|difficulty(8)|spd_rtng(88)|weapon_length(108)|swing_damage(35,cut)|thrust_damage(0,pierce), imodbits_axe ],
["battle_axe", "Battle Axe", [("battle_ax",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 240, weight(5)|difficulty(9)|spd_rtng(86)|weapon_length(108)|swing_damage(45,cut)|thrust_damage(0,pierce), imodbits_axe ],
["war_axe", "War Axe", [("war_ax",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 264, weight(5)|difficulty(10)|spd_rtng(83)|weapon_length(110)|swing_damage(46,cut)|thrust_damage(0,pierce), imodbits_axe ],
["two_handed_axe", "Two Handed Axe", [("two_handed_battle_axe_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 90, weight(4.5)|difficulty(10)|spd_rtng(92)|weapon_length(90)|swing_damage(42,cut)|thrust_damage(0,pierce), imodbits_axe ],
["two_handed_battle_axe_2", "Two Handed War Axe", [("two_handed_battle_axe_b",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 152, weight(4.5)|difficulty(10)|spd_rtng(92)|weapon_length(92)|swing_damage(48,cut)|thrust_damage(0,pierce), imodbits_axe ],
["great_axe", "Great Axe", [("two_handed_battle_axe_e",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 316, weight(4.5)|difficulty(10)|spd_rtng(90)|weapon_length(96)|swing_damage(51,cut)|thrust_damage(0,pierce), imodbits_axe ],
["sarranid_two_handed_axe_a", "Sarranid Battle Axe", [("two_handed_battle_axe_g",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 350, weight(2.50)|difficulty(10)|spd_rtng(85)|weapon_length(95)|swing_damage(52,cut)|thrust_damage(0,pierce), imodbits_axe ],
["sarranid_two_handed_axe_b", "Sarranid War Axe", [("two_handed_battle_axe_h",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 280, weight(3.0)|difficulty(10)|spd_rtng(86)|weapon_length(90)|swing_damage(50,cut)|thrust_damage(0,pierce), imodbits_axe ],
["long_axe", "Long Axe", [("long_axe_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_next_item_as_melee|itp_unbalanced, itc_staff|itcf_carry_axe_back, 390, weight(4.75)|difficulty(10)|spd_rtng(89)|weapon_length(120)|swing_damage(57,cut)|thrust_damage(19,blunt), imodbits_axe ],
["long_axe_alt", "Long Axe", [("long_axe_a",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_cut_two_handed|itc_parry_polearm|itcf_carry_axe_back, 390, weight(4.75)|difficulty(10)|spd_rtng(82)|weapon_length(120)|swing_damage(66,cut)|thrust_damage(0,pierce), imodbits_axe ],
["long_axe_b", "Long War Axe", [("long_axe_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_next_item_as_melee|itp_unbalanced, itc_staff|itcf_carry_axe_back, 510, weight(5.0)|difficulty(10)|spd_rtng(89)|weapon_length(125)|swing_damage(53,cut)|thrust_damage(18,blunt), imodbits_axe ],
["long_axe_b_alt", "Long War Axe", [("long_axe_b",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_cut_two_handed|itc_parry_polearm|itcf_carry_axe_back, 510, weight(5.0)|difficulty(10)|spd_rtng(80)|weapon_length(125)|swing_damage(63,cut)|thrust_damage(0,pierce), imodbits_axe ],
["long_axe_c", "Great Long Axe", [("long_axe_c",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_next_item_as_melee|itp_unbalanced, itc_staff|itcf_carry_axe_back, 660, weight(5.5)|difficulty(10)|spd_rtng(88)|weapon_length(127)|swing_damage(57,cut)|thrust_damage(19,blunt), imodbits_axe ],
["long_axe_c_alt", "Great Long Axe", [("long_axe_c",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_cut_two_handed|itc_parry_polearm|itcf_carry_axe_back, 660, weight(5.5)|difficulty(10)|spd_rtng(80)|weapon_length(127)|swing_damage(66,cut)|thrust_damage(0,pierce), imodbits_axe ],
["poleaxe", "Poleaxe", [("pole_ax",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_offset_lance|itp_couchable, itc_staff, 384, weight(4.5)|difficulty(13)|spd_rtng(77)|weapon_length(180)|swing_damage(50,cut)|thrust_damage(15,blunt), imodbits_polearm ],

["voulge", "Voulge", [("voulge",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 129, weight(4.5)|difficulty(8)|spd_rtng(70)|weapon_length(119)|swing_damage(48,cut)|thrust_damage(0,pierce), imodbits_axe ],
["long_voulge", "Long Voulge", [("two_handed_battle_long_axe_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_offset_lance|itp_couchable|itp_crush_through|itp_unbalanced, itc_staff, 120, weight(3.0)|difficulty(10)|spd_rtng(72)|weapon_length(175)|swing_damage(48,cut)|thrust_damage(18,pierce), imodbits_axe ],
["shortened_voulge", "Shortened Voulge", [("two_handed_battle_axe_c",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_cut_two_handed|itc_parry_polearm|itcf_carry_axe_back, 228, weight(4.5)|difficulty(10)|spd_rtng(87)|weapon_length(100)|swing_damage(45,cut)|thrust_damage(12,pierce), imodbits_axe ],

["ccc_axe_gimili_battle", "Gimili Battle Axe", [("gimili_battle_axe",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_axe_back, 1100, weight(4)|difficulty(11)|spd_rtng(92)|weapon_length(108)|swing_damage(49,pierce)|thrust_damage(0,pierce), imodbits_axe ],
["ccc_axe_gimili_walking", "Gimili Walking Axe", [("gimili_walking_axe",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_axe_back, 1500, weight(4)|difficulty(12)|spd_rtng(83)|weapon_length(108)|swing_damage(54,pierce)|thrust_damage(0,pierce), imodbits_axe ],

["ccc_axe_ken_legend_halberd", "Legend Axe", [("legendhalberd",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_axe_back, 9545, weight(5)|difficulty(12)|spd_rtng(75)|weapon_length(180)|swing_damage(48,cut)|thrust_damage(0,pierce), imodbits_axe ],

#Bardiches
["bardiche", "Bardiche", [("two_handed_battle_axe_d",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 291, weight(4.75)|difficulty(10)|spd_rtng(76)|weapon_length(102)|swing_damage(57,cut)|thrust_damage(0,pierce), imodbits_axe ],
["great_bardiche", "Great Bardiche", [("two_handed_battle_axe_f",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_nodachi|itcf_carry_axe_back, 617, weight(5.0)|difficulty(10)|spd_rtng(78)|weapon_length(116)|swing_damage(60,cut)|thrust_damage(0,pierce), imodbits_axe ],
["long_bardiche", "Long Bardiche", [("two_handed_battle_long_axe_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_unbalanced, itc_staff, 390, weight(4.75)|difficulty(11)|spd_rtng(78)|weapon_length(140)|swing_damage(68,cut)|thrust_damage(13,pierce), imodbits_axe ],
["great_long_bardiche", "Great Long Bardiche", [("two_handed_battle_long_axe_c",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_offset_lance|itp_couchable|itp_bonus_against_shield|itp_unbalanced, itc_staff, 660, weight(5.0)|difficulty(12)|spd_rtng(74)|weapon_length(155)|swing_damage(62,cut)|thrust_damage(13,pierce), imodbits_axe ],

#Clubs
["wooden_stick", "Wooden Stick", [("wooden_stick",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_primary, itc_scimitar, 4, weight(2.5)|difficulty(0)|spd_rtng(99)|weapon_length(63)|swing_damage(13,blunt)|thrust_damage(0,pierce), imodbits_none ],
["cudgel", "Cudgel", [("club",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_primary, itc_scimitar, 4, weight(2.5)|difficulty(0)|spd_rtng(99)|weapon_length(70)|swing_damage(13,blunt)|thrust_damage(0,pierce), imodbits_none ],
["club", "Club", [("club",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar, 11, weight(2.5)|difficulty(0)|spd_rtng(98)|weapon_length(70)|swing_damage(20,blunt)|thrust_damage(0,pierce), imodbits_none ],
["spiked_club", "Spiked Club", [("spiked_club",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary, itc_scimitar|itcf_carry_mace_left_hip, 83, weight(3)|difficulty(0)|spd_rtng(97)|weapon_length(70)|swing_damage(21,pierce)|thrust_damage(0,pierce), imodbits_mace ],
["club_with_spike_head", "Spiked Staff", [("mace_e",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_bastardsword|itcf_carry_axe_back, 200, weight(2.80)|difficulty(9)|spd_rtng(95)|weapon_length(117)|swing_damage(24,blunt)|thrust_damage(20,pierce), imodbits_mace ],
["long_spiked_club", "Long Spiked Club", [("mace_long_c",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_staff|itcf_carry_axe_back, 264, weight(3)|difficulty(0)|spd_rtng(96)|weapon_length(126)|swing_damage(23,pierce)|thrust_damage(20,blunt), imodbits_mace ],
#Picks
["pickaxe", "Pickaxe", [("rusty_pick",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary, itc_scimitar|itcf_carry_mace_left_hip, 27, weight(3)|difficulty(0)|spd_rtng(99)|weapon_length(70)|swing_damage(19,pierce)|thrust_damage(0,pierce), imodbits_pick ],
["fighting_pick", "Fighting Pick", [("fighting_pick_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary, itc_scimitar|itcf_carry_mace_left_hip, 108, weight(1.0)|difficulty(0)|spd_rtng(98)|weapon_length(70)|swing_damage(22,pierce)|thrust_damage(0,pierce), imodbits_pick ],
["military_pick", "Military Pick", [("steel_pick_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary, itc_scimitar|itcf_carry_mace_left_hip, 280, weight(1.5)|difficulty(0)|spd_rtng(97)|weapon_length(70)|swing_damage(31,pierce)|thrust_damage(0,pierce), imodbits_pick ],

#one-hand-mace
["ccc_mace_mace1", "Mace", [("maceraptor_1",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_axe_left_hip, 280, weight(3.5)|difficulty(0)|spd_rtng(99)|weapon_length(80)|swing_damage(22,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_mace_mace2", "Mace", [("maceraptor_2",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_axe_left_hip, 280, weight(3.5)|difficulty(0)|spd_rtng(99)|weapon_length(80)|swing_damage(25,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_mace_mace3", "Mace", [("maceraptor_3",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_axe_left_hip, 280, weight(3.5)|difficulty(0)|spd_rtng(99)|weapon_length(80)|swing_damage(32,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_mace_mace4", "Mace", [("maceraptor_4",0)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_axe_left_hip, 280, weight(3.5)|difficulty(0)|spd_rtng(99)|weapon_length(80)|swing_damage(33,blunt)|thrust_damage(0,pierce), imodbits_mace ],

#Occc weight modified begin
["ccc_mace_guardian_mace", "Guardian Mace", [("talak_mace",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 1024, weight(4.0)|difficulty(0)|spd_rtng(105)|weapon_length(85)|swing_damage(39,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_mace_guardian_long_mace", "Guardian Long Mace", [("talak_long_mace",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 6545, weight(4.5)|difficulty(0)|spd_rtng(95)|weapon_length(100)|swing_damage(39,blunt)|thrust_damage(0,pierce), imodbits_mace ],
#Occc weight modified end

["mace_1", "Spiked Club", [("mace_d",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 45, weight(1.5)|difficulty(0)|spd_rtng(99)|weapon_length(70)|swing_damage(19,pierce)|thrust_damage(0,pierce), imodbits_mace ],
["mace_2", "Knobbed_Mace", [("mace_a",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 98, weight(2.5)|difficulty(0)|spd_rtng(98)|weapon_length(70)|swing_damage(21,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["mace_3", "Spiked Mace", [("mace_c",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 152, weight(2.75)|difficulty(0)|spd_rtng(98)|weapon_length(70)|swing_damage(23,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["sarranid_mace_1", "Iron Mace", [("mace_small_d",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 45, weight(2.0)|difficulty(0)|spd_rtng(99)|weapon_length(73)|swing_damage(22,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["mace_4", "Winged_Mace", [("mace_b",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 212, weight(2.75)|difficulty(0)|spd_rtng(98)|weapon_length(70)|swing_damage(24,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["winged_mace", "Flanged Mace", [("flanged_mace",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 122, weight(3.5)|difficulty(0)|spd_rtng(103)|weapon_length(70)|swing_damage(24,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["spiked_mace", "Spiked Mace", [("spiked_mace_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 180, weight(3.5)|difficulty(0)|spd_rtng(98)|weapon_length(70)|swing_damage(28,blunt)|thrust_damage(0,pierce), imodbits_pick ],

#twe-hand-mace
["morningstar", "Morningstar", [("mace_morningstar_new",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_crush_through|itp_unbalanced, itc_morningstar|itcf_carry_mace_left_hip, 305, weight(4.5)|difficulty(13)|spd_rtng(95)|weapon_length(85)|swing_damage(38,pierce)|thrust_damage(0,pierce), imodbits_mace ],
["long_hafted_knobbed_mace", "Long Hafted Knobbed Mace", [("mace_long_a",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_staff|itcf_carry_axe_back, 324, weight(3)|difficulty(0)|spd_rtng(113)|weapon_length(133)|swing_damage(26,blunt)|thrust_damage(23,blunt), imodbits_mace ],
["long_hafted_spiked_mace", "Long Hafted Spiked Mace", [("mace_long_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_staff|itcf_carry_axe_back, 310, weight(3)|difficulty(0)|spd_rtng(110)|weapon_length(140)|swing_damage(28,blunt)|thrust_damage(24,blunt), imodbits_mace ],
["sarranid_two_handed_mace_1", "Iron Mace", [("mace_long_d",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_can_knock_down, itc_greatsword|itcf_carry_axe_back, 470, weight(4.5)|difficulty(0)|spd_rtng(90)|weapon_length(95)|swing_damage(35,blunt)|thrust_damage(22,blunt), imodbits_mace ],
["sarranid_two_handed_mace_2", "Brass Mace", [("mace_long_d_2",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_can_knock_down, itc_greatsword|itcf_carry_axe_back, 530, weight(5)|difficulty(0)|spd_rtng(83)|weapon_length(95)|swing_damage(40,blunt)|thrust_damage(25,blunt), imodbits_mace ],

#morningstar
["ccc_morningstar_guardian", "Guardian Morningstar", [("talak_morningstar",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_primary|itp_crush_through|itp_unbalanced, itc_morningstar|itcf_carry_axe_left_hip, 700, weight(4.5)|difficulty(13)|spd_rtng(100)|weapon_length(85)|swing_damage(43,pierce)|thrust_damage(0,pierce), imodbits_mace ],

#one-hand-hanmmer
["hammer", "Hammer", [("iron_hammer_new",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar, 7, weight(2)|difficulty(0)|spd_rtng(100)|weapon_length(55)|swing_damage(24,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["military_hammer", "Military Hammer", [("military_hammer",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 317, weight(2)|difficulty(0)|spd_rtng(95)|weapon_length(70)|swing_damage(31,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_hammer_military_hammer1", "Military Hammer", [("hammerraptor_1",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_axe_left_hip, 500, weight(4)|difficulty(0)|spd_rtng(92)|weapon_length(90)|swing_damage(21,blunt)|thrust_damage(0,pierce), imodbits_mace ],
#["ccc_hammer_military_hammer2", "Military Hammer", [("hammerraptor_2",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_axe_left_hip, 1024, weight(4)|difficulty(0)|spd_rtng(92)|weapon_length(90)|swing_damage(22,blunt)|thrust_damage(0,pierce), imodbits_mace ],  ## cave09 del

#two-hand-hammer
["maul", "Maul", [("maul_b",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_can_knock_down, itc_nodachi|itcf_carry_spear, 97, weight(6)|difficulty(11)|spd_rtng(83)|weapon_length(79)|swing_damage(36,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["sledgehammer", "Sledgehammer", [("maul_c",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_can_knock_down, itc_nodachi|itcf_carry_spear, 101, weight(7)|difficulty(12)|spd_rtng(81)|weapon_length(82)|swing_damage(39,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["warhammer", "Great Hammer", [("maul_d",0)], itp_type_two_handed_wpn|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_can_knock_down, itc_nodachi|itcf_carry_spear, 290, weight(9)|difficulty(14)|spd_rtng(79)|weapon_length(75)|swing_damage(45,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["bec_de_corbin_a", "War Hammer", [("bec_de_corbin_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_cant_use_on_horseback|itp_unbalanced, itc_cutting_spear|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_carry_spear, 125, weight(3.0)|difficulty(0)|spd_rtng(81)|weapon_length(120)|swing_damage(38,blunt)|thrust_damage(38,pierce), imodbits_polearm ],
["polehammer", "Polehammer", [("pole_hammer",0)], itp_type_polearm|itp_wooden_parry|itp_two_handed|itp_primary|itp_offset_lance, itc_staff, 169, weight(7)|difficulty(18)|spd_rtng(50)|weapon_length(126)|swing_damage(50,blunt)|thrust_damage(35,blunt), imodbits_polearm ],

["ccc_hammer_mallet1", "Mallet", [("malletraptor_1",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_unbalanced, itc_nodachi, 100, weight(10)|difficulty(11)|spd_rtng(65)|weapon_length(115)|swing_damage(26,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_hammer_of", "Big Hammer", [("hammer_of",0)], itp_type_two_handed_wpn|itp_wooden_attack|itp_wooden_parry|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced, itc_nodachi|itcf_carry_spear, 700, weight(7)|difficulty(12)|spd_rtng(81)|weapon_length(110)|swing_damage(42,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_hammer_of_kings", "Hammer of Kings", [("hammer_of_kings",0)], itp_type_two_handed_wpn|itp_wooden_attack|itp_wooden_parry|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_can_knock_down, itc_nodachi|itcf_carry_spear, 900, weight(7)|difficulty(14)|spd_rtng(75)|weapon_length(110)|swing_damage(55,blunt)|thrust_damage(0,pierce), imodbits_mace ],

#staff
#["ccc_staff_waor4", "Chaos Staff", [("WAoRStaffD",0)], itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_covers_head|itp_couchable, itc_staff|itcf_carry_spear|itcf_force_64_bits, 1024, weight(3)|difficulty(15)|spd_rtng(97)|weapon_length(175)|swing_damage(45,blunt)|thrust_damage(45,blunt), imodbits_polearm ],
#["ccc_staff_waor7", "Chaos Staff", [("WAoRStaffG",0)], itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_covers_head|itp_couchable, itc_staff|itcf_carry_spear|itcf_force_64_bits, 1024, weight(3)|difficulty(15)|spd_rtng(85)|weapon_length(190)|swing_damage(43,blunt)|thrust_damage(44,blunt), imodbits_polearm ],

#Scythes
["scythe", "Scythe", [("scythe",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_staff|itcf_carry_spear, 43, weight(3)|difficulty(0)|spd_rtng(82)|weapon_length(182)|swing_damage(19,cut)|thrust_damage(14,pierce), imodbits_polearm ],
["shortened_military_scythe", "Shortened Military Scythe", [("two_handed_battle_scythe_a",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 264, weight(3.0)|difficulty(10)|spd_rtng(90)|weapon_length(112)|swing_damage(45,cut)|thrust_damage(0,pierce), imodbits_sword_high ],
["military_scythe", "Military Scythe", [("spear_e_2-5m",0),("spear_c_2-5m",imodbits_bad)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_carry_spear, 155, weight(2.5)|difficulty(10)|spd_rtng(94)|weapon_length(155)|swing_damage(36,cut)|thrust_damage(25,pierce), imodbits_polearm ],

#Forks
["pitch_fork", "Pitch Fork", [("pitch_fork",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_staff, 19, weight(3.5)|difficulty(0)|spd_rtng(99)|weapon_length(154)|swing_damage(15,blunt)|thrust_damage(18,pierce), imodbits_polearm ],
["military_fork", "Military Fork", [("military_fork",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff, 153, weight(4.5)|difficulty(0)|spd_rtng(102)|weapon_length(135)|swing_damage(15,blunt)|thrust_damage(23,pierce), imodbits_polearm ],
["battle_fork", "Battle Fork", [("battle_fork",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff, 282, weight(4.5)|difficulty(0)|spd_rtng(100)|weapon_length(142)|swing_damage(15,blunt)|thrust_damage(24,pierce), imodbits_polearm ],
["occc_better_battle_fork", "Gladiator Battle Fork", [("battle_fork",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff, 350, weight(4.5)|difficulty(0)|spd_rtng(103)|weapon_length(142)|swing_damage(21,blunt)|thrust_damage(28,pierce), imodbits_polearm ],

#Staves
["staff", "Staff", [("wooden_staff",0)], itp_type_polearm|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance, itc_staff|itcf_carry_sword_back, 36, weight(1.5)|difficulty(0)|spd_rtng(135)|weapon_length(130)|swing_damage(16,blunt)|thrust_damage(17,blunt), imodbits_polearm ],
["quarter_staff", "Quarter Staff", [("quarter_staff",0)], itp_type_polearm|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff|itcf_carry_sword_back, 60, weight(2)|difficulty(0)|spd_rtng(135)|weapon_length(140)|swing_damage(18,blunt)|thrust_damage(17,blunt), imodbits_polearm ],
["iron_staff", "Iron Staff", [("iron_staff",0)], itp_type_polearm|itp_merchandise|itp_primary|itp_offset_lance, itc_staff|itcf_carry_sword_back, 202, weight(2)|difficulty(0)|spd_rtng(117)|weapon_length(140)|swing_damage(25,blunt)|thrust_damage(26,blunt), imodbits_polearm ],
["ccd_maruta", "Maruta", [("ccd_maruta",0)], itp_type_polearm|itp_merchandise|itp_wooden_attack|itp_wooden_parry|itp_two_handed|itp_primary|itp_offset_lance|itp_penalty_with_shield|itp_crush_through|itp_unbalanced|itp_couchable|itp_can_knock_down, itc_parry_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_horseback_slash_polearm|itcf_thrust_musket, 1024, weight(40)|abundance(50)|difficulty(24)|spd_rtng(50)|weapon_length(200)|swing_damage(60,blunt)|thrust_damage(60,blunt), imodbits_polearm, [], [fac_player_supporters_faction] ],

#Glaives
["glaive", "Glaive", [("glaive_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_offset_lance|itp_couchable, itc_staff|itcf_carry_spear, 352, weight(4.5)|difficulty(0)|spd_rtng(90)|weapon_length(157)|swing_damage(39,cut)|thrust_damage(21,pierce), imodbits_polearm ],
["hafted_blade_b", "Hafted Blade", [("khergit_pike_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_guandao|itcf_horseback_thrust_onehanded|itcf_carry_spear, 185, weight(2.75)|difficulty(0)|spd_rtng(95)|weapon_length(135)|swing_damage(37,cut)|thrust_damage(25,pierce), imodbits_polearm ],
["hafted_blade_a", "Hafted Blade", [("khergit_pike_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_guandao|itcf_horseback_thrust_onehanded|itcf_carry_spear, 350, weight(3.25)|difficulty(0)|spd_rtng(93)|weapon_length(153)|swing_damage(39,cut)|thrust_damage(29,pierce), imodbits_polearm ],
#["ccd_naginata", "Naginata", [("long_naginata", 0)], itp_type_polearm|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed, itc_guandao|itcf_carry_spear, 1024, weight(4.75)|difficulty(12)|spd_rtng(83)|weapon_length(190)|swing_damage(42, cut)|thrust_damage(20,  pierce), imodbits_polearm ],  ## cave09  ->ccc_polearm_jp_naginata

#halberd
["ccc_polearm_polehammer1", "Polehammer", [("polehammerraptor_1",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_merchandise, itc_nodachi, 670, weight(13)|difficulty(10)|spd_rtng(66)|weapon_length(150)|swing_damage(32,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["ccc_halberd_polearm1", "Polearm", [("polearmraptor_1",0)], itp_type_polearm|itp_merchandise|itp_two_handed|itp_primary|itp_penalty_with_shield, itc_staff|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear, 750, weight(3)|difficulty(0)|spd_rtng(88)|weapon_length(205)|swing_damage(32,cut)|thrust_damage(32,pierce), imodbits_polearm ],
["ccc_halberd_halberd6", "Halberd", [("halberdraptor_5",0)], itp_type_polearm|itp_merchandise|itp_two_handed|itp_primary|itp_penalty_with_shield, itc_staff|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded, 750, weight(6.0)|abundance(20)|difficulty(8)|spd_rtng(70)|weapon_length(204)|swing_damage(41,cut)|thrust_damage(26,pierce), imodbits_polearm ],
["ccc_halberd_halberd7", "Halberd", [("halberdraptor_2",0)], itp_type_polearm|itp_merchandise|itp_two_handed|itp_primary|itp_penalty_with_shield, itc_staff|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded, 780, weight(6.0)|abundance(20)|difficulty(8)|spd_rtng(70)|weapon_length(190)|swing_damage(44,cut)|thrust_damage(25,pierce), imodbits_polearm ],
["ccc_halberd_guardian", "Guardian Halberd", [("talak_halberd",0)], itp_type_polearm|itp_wooden_parry|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded, 2048, weight(3.0)|difficulty(15)|spd_rtng(75)|weapon_length(170)|swing_damage(46,cut)|thrust_damage(30,pierce), imodbits_polearm ],
["ccc_nord_halberd", "Nord Halberd", [("hallberdh",0)], itp_type_polearm|itp_wooden_parry|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded, 2048, weight(4.0)|difficulty(15)|spd_rtng(68)|weapon_length(240)|swing_damage(48,cut)|thrust_damage(27,pierce), imodbits_polearm ],

#polam
["ccc_polearm_bill1", "Bill hook", [("billraptor_1",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_offset_lance|itp_couchable|itp_merchandise, itc_staff|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded, 450, weight(4)|abundance(20)|difficulty(7)|spd_rtng(68)|weapon_length(230)|swing_damage(35,pierce)|thrust_damage(24,pierce), imodbits_polearm ],
["ccc_polearm_glaive3", "Glaive", [("xpglaiveraptor_3",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable|itp_merchandise, itc_staff|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear, 600, weight(4.5)|difficulty(0)|spd_rtng(74)|weapon_length(245)|swing_damage(34,cut)|thrust_damage(17,pierce), imodbits_polearm ],
["ccc_polearm_darkhunterpolearm", "Dark Polearm", [("darkhunterpolearm",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_carry_spear, 700, weight(3.5)|difficulty(10)|spd_rtng(72)|weapon_length(330)|swing_damage(43,cut)|thrust_damage(42,pierce), imodbits_polearm ],
["ccc_polearm_sword_of_miracles", "Sword Of Miracles", [("SwordOfMiracles",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_nodachi|itcf_carry_sword_back, 1024, weight(6.5)|difficulty(0)|spd_rtng(90)|weapon_length(145)|swing_damage(45,cut)|thrust_damage(31,pierce), imodbits_polearm ],
["ccc_polearm_waor2", "Chaos Polearm", [("WAoRStaffB",0)], itp_type_polearm|itp_primary|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_carry_spear|itcf_force_64_bits, 1500, weight(3)|difficulty(15)|spd_rtng(82)|weapon_length(240)|swing_damage(35,cut)|thrust_damage(38,pierce), imodbits_polearm ],
["ccc_polearm_waor3", "Chaos Polearm", [("WAoRStaffC",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_thrust_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear|itcf_force_64_bits, 1500, weight(3)|difficulty(15)|spd_rtng(80)|weapon_length(250)|swing_damage(45,cut)|thrust_damage(38,pierce), imodbits_polearm ],
["ccc_polearm_waor5", "Chaos Polearm", [("WAoRStaffE",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_penalty_with_shield, itc_staff|itcf_thrust_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear|itcf_parry_forward_polearm|itcf_parry_up_polearm|itcf_parry_right_polearm|itcf_parry_left_polearm|itcf_force_64_bits, 1500, weight(3)|difficulty(15)|spd_rtng(86)|weapon_length(210)|swing_damage(40,cut)|thrust_damage(40,pierce), imodbits_polearm ],
["ccc_polearm_scyth", "Giant Scythe", [("battle_scythe",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_penalty_with_shield, itc_staff|itcf_thrust_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear|itcf_parry_forward_polearm|itcf_parry_up_polearm|itcf_parry_right_polearm|itcf_parry_left_polearm|itcf_force_64_bits, 600, weight(3)|difficulty(15)|spd_rtng(80)|weapon_length(150)|swing_damage(45,cut), imodbits_polearm ],

#JP
["ccc_polearm_jp_kata_spear", "KataKamaYari", [("katakama_yari",0)], itp_type_polearm|itp_primary|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_carry_spear, 1500, weight(3.5)|difficulty(15)|spd_rtng(86)|weapon_length(190)|swing_damage(36,cut)|thrust_damage(33,pierce), imodbits_polearm ],
["ccc_polearm_jp_kiku_spear", "Kiku_Yari", [("kikuchiyari",0)], itp_type_polearm|itp_primary|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_carry_spear, 1500, weight(3)|difficulty(15)|spd_rtng(81)|weapon_length(225)|swing_damage(23,blunt)|thrust_damage(38,pierce), imodbits_polearm ],
["ccc_polearm_jp_kiyomasa_spear", "KiyomasaYari", [("kiyomasa_kamayari",0)], itp_type_polearm|itp_primary|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_carry_spear, 1500, weight(4)|difficulty(16)|spd_rtng(84)|weapon_length(190)|swing_damage(38,cut)|thrust_damage(38,pierce), imodbits_polearm ],
["ccc_polearm_jp_sasaho_spear", "Sasaho_Yari", [("sasaho_yari",0)], itp_type_polearm|itp_primary|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_carry_spear, 1500, weight(3)|difficulty(15)|spd_rtng(85)|weapon_length(207)|swing_damage(23,blunt)|thrust_damage(35,pierce), imodbits_polearm ],
["ccc_polearm_jp_naginata", "Naginata", [("long_naginata",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear|itcf_thrust_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear, 1500, weight(3)|difficulty(12)|spd_rtng(90)|weapon_length(200)|swing_damage(39,cut)|thrust_damage(25,pierce), imodbits_polearm ],

#spear
["bamboo_spear", "Bamboo Spear", [("arabian_spear_a_3m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new|itcf_carry_spear, 80, weight(2.0)|difficulty(0)|spd_rtng(94)|weapon_length(200)|swing_damage(8,blunt)|thrust_damage(15,pierce), imodbits_polearm ],
["boar_spear", "Boar Spear", [("spear",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new|itcf_carry_spear, 76, weight(1.5)|difficulty(0)|spd_rtng(106)|weapon_length(157)|swing_damage(22,cut)|thrust_damage(18,pierce), imodbits_polearm ],
["shortened_spear", "Shortened Spear", [("spear_g_1-9m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_offset_lance, itc_spear_new|itcf_carry_spear, 53, weight(2.0)|difficulty(0)|spd_rtng(125)|weapon_length(120)|swing_damage(12,blunt)|thrust_damage(22,pierce), imodbits_polearm ],
["spear", "Spear", [("spear_h_2-15m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance, itc_spear_new|itcf_carry_spear, 85, weight(2.25)|difficulty(0)|spd_rtng(115)|weapon_length(135)|swing_damage(14,blunt)|thrust_damage(24,pierce), imodbits_polearm ],
["war_spear", "War Spear", [("spear_i_2-3m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new|itcf_carry_spear, 140, weight(2.5)|difficulty(0)|spd_rtng(108)|weapon_length(150)|swing_damage(17,blunt)|thrust_damage(25,pierce), imodbits_polearm ],
["ccc_spear_spear6", "Spear", [("xpspearraptor_5",0)], itp_type_polearm|itp_merchandise|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new|itcf_carry_spear, 200, weight(5)|difficulty(0)|spd_rtng(100)|weapon_length(210)|swing_damage(18,blunt)|thrust_damage(32,pierce), imodbits_polearm ],
["ccc_spear_roma_spear_a", "Roma Spear", [("spearC",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new|itcf_carry_spear, 300, weight(3.0)|difficulty(10)|spd_rtng(103)|weapon_length(200)|swing_damage(20,blunt)|thrust_damage(33,pierce), imodbits_polearm ],
["ccc_spear_uhlan", "Uhlan Lance", [("uhlan_lance",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new, 400, weight(4)|difficulty(11)|spd_rtng(95)|weapon_length(250)|swing_damage(24,blunt)|thrust_damage(38,pierce), imodbits_polearm ],
["ccc_spear_knight", "Knight Spear", [("guisarmeb",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new, 500, weight(4)|difficulty(11)|spd_rtng(98)|weapon_length(330)|swing_damage(24,blunt)|thrust_damage(39,pierce), imodbits_polearm ],

#pike
#occc swing damage addition
["pike", "Pike", [("spear_a_3m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_cant_use_on_horseback|itcf_overswing_polearm, itc_cutting_spear, 125, weight(3.0)|difficulty(0)|spd_rtng(115)|weapon_length(255)|swing_damage(20,blunt)|thrust_damage(27,pierce), imodbits_polearm ],
#["ccc_pike_roma", "Roma Pike", [("pikec",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_cant_reload_on_horseback|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_cant_use_on_horseback|itp_ignore_friction|itcf_overswing_polearm, itc_cutting_spear, 125, weight(3.0)|difficulty(0)|spd_rtng(110)|weapon_length(280)|swing_damage(20,blunt)|thrust_damage(34,pierce), imodbits_polearm ],
["ashwood_pike", "Ashwood Pike", [("pike",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable|itcf_overswing_polearm, itc_cutting_spear, 205, weight(3.5)|difficulty(11)|spd_rtng(118)|weapon_length(170)|swing_damage(20,blunt)|thrust_damage(33,pierce), imodbits_polearm ],
["awlpike", "Awlpike", [("awl_pike_b",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_spear_new|itcf_carry_spear, 345, weight(2.25)|difficulty(0)|spd_rtng(92)|weapon_length(165)|swing_damage(20,blunt)|thrust_damage(33,pierce), imodbits_polearm ],
["awlpike_long", "Long Awlpike", [("awl_pike_a",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_cant_use_on_horseback|itp_offset_lance|itp_couchable, itc_spear_new|itcf_carry_spear, 385, weight(2.25)|difficulty(0)|spd_rtng(89)|weapon_length(185)|swing_damage(20,blunt)|thrust_damage(32,pierce), imodbits_polearm ],
["ccc_pike_darkpike", "Dark Pike", [("darkpike",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_penalty_with_shield|itp_cant_use_on_horseback|itp_offset_lance|itp_couchable, itc_pike, 430, weight(4.5)|difficulty(0)|spd_rtng(114)|weapon_length(330)|swing_damage(20,cut)|thrust_damage(36,pierce), imodbits_polearm ],
["ccc_pike_cavalry_pike", "Cavalry Pike", [("darkhunterpolearm",0)], itp_type_polearm|itp_wooden_parry|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_offset_lance|itp_couchable, itc_greatlance, 490, weight(2.25)|difficulty(0)|spd_rtng(110)|weapon_length(320)|swing_damage(20,blunt)|thrust_damage(40,pierce), imodbits_polearm ],
["occc_merc_short_pike", "Mercenary Pike", [("pikea", 0),], itp_type_polearm|itp_two_handed|itp_merchandise|itp_primary|itp_cant_use_on_horseback|itp_penalty_with_shield, itcf_carry_spear|itc_parry_polearm|itcf_thrust_twohanded|itcf_overswing_polearm, 400, weight(3)|spd_rtng(95)|weapon_length(250)|thrust_damage(30, pierce)|swing_damage(25, blunt), imodbits_polearm ],
["ccc_merc_pike", "Mercenary Long Pike", [("pikeb", 0),], itp_type_polearm|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_penalty_with_shield, itcf_carry_spear|itc_parry_polearm|itcf_thrust_twohanded|itcf_overswing_polearm, 460, weight(4)|spd_rtng(88)|weapon_length(280)|thrust_damage(30, pierce)|swing_damage(25, blunt), imodbits_polearm ],
["occc_helvetia_pike", "Helvetia Pike", [("pikec", 0),], itp_type_polearm|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_penalty_with_shield, itcf_carry_spear|itc_parry_polearm|itcf_thrust_twohanded|itcf_overswing_polearm, 600, weight(5)|spd_rtng(85)|weapon_length(400)|thrust_damage(32, pierce)|swing_damage(29, blunt), imodbits_polearm ],

#lance
["light_lance", "Light Lance", [("spear_b_2-75m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear, 180, weight(2.5)|difficulty(0)|spd_rtng(85)|weapon_length(175)|swing_damage(16,blunt)|thrust_damage(27,pierce), imodbits_polearm ],
["lance", "Lance", [("spear_d_2-8m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear, 270, weight(2.5)|difficulty(0)|spd_rtng(80)|weapon_length(180)|swing_damage(16,blunt)|thrust_damage(29,pierce), imodbits_polearm ],
["double_sided_lance", "Double Sided Lance", [("lance_dblhead",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_staff, 261, weight(4.0)|difficulty(0)|spd_rtng(95)|weapon_length(128)|swing_damage(25,cut)|thrust_damage(27,pierce), imodbits_polearm ],
["ccc_lance_ken_short_silver", "Short Lance", [("short_lance_y2",0)], itp_type_polearm|itp_primary|itp_offset_lance|itp_couchable, itc_greatlance, 340, weight(2.5)|difficulty(0)|spd_rtng(87)|weapon_length(170)|thrust_damage(32,pierce), imodbits_polearm ],

#Great Lance
["heavy_lance", "Heavy Lance", [("spear_f_2-9m",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_offset_lance|itp_couchable, itc_cutting_spear, 360, weight(2.75)|difficulty(10)|spd_rtng(75)|weapon_length(190)|swing_damage(16,blunt)|thrust_damage(31,pierce), imodbits_polearm ],
["jousting_lance", "Jousting Lance", [("joust_of_peace",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_couchable|itp_unbalanced, itc_greatlance, 158, weight(5)|difficulty(0)|spd_rtng(61)|weapon_length(240)|swing_damage(0,cut)|thrust_damage(10,blunt), imodbits_polearm ],
["ccc_lance_heavy_lance_new", "Heavy Lance", [("talak_lance",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_couchable|itp_crush_through|itp_unbalanced, itc_greatlance, 400, weight(4.25)|spd_rtng(50)|weapon_length(240)|swing_damage(0,blunt)|thrust_damage(32,blunt), imodbits_polearm ],
["great_lance", "Great Lance", [("heavy_lance",0)], itp_type_polearm|itp_merchandise|itp_wooden_parry|itp_primary|itp_couchable, itc_greatlance, 410, weight(5)|difficulty(11)|spd_rtng(55)|weapon_length(240)|swing_damage(0,cut)|thrust_damage(41,pierce), imodbits_polearm ],
["ccc_lance_gothic_lance", "Gothic Lance", [("gothic_lance",0)], itp_type_polearm|itp_primary|itp_couchable|itp_crush_through, itc_greatlance, 2000, weight(5)|difficulty(12)|spd_rtng(50)|weapon_length(240)|swing_damage(0,cut)|thrust_damage(65,pierce), imodbits_polearm ],
["ccc_lance_great_bk", "Black Knight Great Lance", [("heavy_lanceb",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_couchable, itc_greatlance, 410, weight(5)|difficulty(11)|spd_rtng(35)|weapon_length(540)|swing_damage(0,cut)|thrust_damage(50,pierce), imodbits_polearm ],
["ccc_lance_color", "Lance", [("vaegir_lance",0)], itp_type_polearm|itp_primary|itp_couchable|itp_crush_through, itc_greatlance, 500, weight(5)|difficulty(11)|spd_rtng(45)|weapon_length(340)|swing_damage(0,cut)|thrust_damage(38,pierce), imodbits_polearm ],
["ccc_lance_black", "Black Lance", [("long_lance_y_black",0)], itp_type_polearm|itp_primary|itp_couchable|itp_crush_through, itc_greatlance, 330, weight(5)|difficulty(11)|spd_rtng(50)|weapon_length(240)|swing_damage(0,cut)|thrust_damage(39,pierce), imodbits_polearm ],
["ccc_lance_silver", "Silver Lance", [("long_lance_y",0)], itp_type_polearm|itp_primary|itp_couchable|itp_crush_through, itc_greatlance, 330, weight(5)|difficulty(11)|spd_rtng(50)|weapon_length(240)|swing_damage(0,cut)|thrust_damage(39,pierce), imodbits_polearm ],
["mm_xyston", "Xyston", [("w_xyston_long", 0),], itp_type_polearm|itp_no_parry|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_unbalanced|itp_couchable, itcf_carry_spear|itc_pike, 1800, weight(3)|spd_rtng(107)|weapon_length(320)|thrust_damage(41, pierce)|swing_damage(19, blunt), imodbits_polearm ],

#bolts
["bolts", "Bolts", [("bolt",0),("flying_bolt",ixmesh_flying_ammo),("bolt_bag",ixmesh_carry),("bolt_bag_b",ixmesh_carry|imodbit_large_bag)], itp_type_bolts|itp_default_ammo|itp_merchandise|itp_can_penetrate_shield, itcf_carry_quiver_right_vertical, 64, weight(2.25)|abundance(90)|weapon_length(63)|thrust_damage(2,pierce)|max_ammo(35), imodbits_missile, missile_distance_trigger ],
["steel_bolts", "Steel Bolts", [("ccd_iron_bolt",0),("flying_bolt",ixmesh_flying_ammo),("bolt_bag_c",ixmesh_carry)], itp_type_bolts|itp_merchandise|itp_can_penetrate_shield|itp_bonus_against_shield, itcf_carry_quiver_right_vertical, 210, weight(2.5)|abundance(20)|weapon_length(63)|thrust_damage(3,pierce)|max_ammo(35), imodbits_missile, missile_distance_trigger ],
["ccc_bomb_bolt", "Bomb Bolts", [("ccd_bomb_bolt",0),("flying_bolt",ixmesh_flying_ammo)], itp_type_bolts|itp_merchandise|itp_no_pick_up_from_ground, 0, 5000, abundance(3)|weight(5)|thrust_damage(105,blunt)|max_ammo(1), imodbits_missile, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"), (call_script, "script_ccd_item_hit_effect_explosion_missile", "itm_ccc_bomb_bolt", ":sa"),])] ],
["ccd_heavy_bolts", "Heavy Bolts", [("ccd_heavy_bolt",0),("flying_bolt",ixmesh_flying_ammo),("bolt_bag_b",ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_bonus_against_shield|itp_can_knock_down, itcf_carry_quiver_right_vertical, 1024, weight(8)|abundance(10)|weapon_length(63)|thrust_damage(20,pierce)|max_ammo(34), imodbits_missile, missile_distance_trigger ],

#firearms occc damage
["cartridges", "Cartridges", [("ccd_ammo_box_a",0),("bullet",ixmesh_flying_ammo),("cartridge_d",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_merchandise|itp_can_penetrate_shield, 0, 41, weight(2.25)|abundance(80)|weapon_length(3)|thrust_damage(6,pierce)|max_ammo(40), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],
["ccc_cartridges_dumdum", "Dumdum Bullet", [("ccd_ammo_box_c",0),("bullet",ixmesh_flying_ammo),("cartridge_c",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_merchandise|itp_bonus_against_shield, 0, 41, weight(2.25)|abundance(90)|weapon_length(3)|thrust_damage(17,pierce)|max_ammo(30), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],
["ccc_cartridges_high_accuracy", "High Accuracy Bullet", [("ccd_ammo_box_e",0),("bullet",ixmesh_flying_ammo),("cartridge_e",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_merchandise|itp_can_knock_down|itp_can_penetrate_shield|itp_ignore_gravity|itp_ignore_friction, 0, 41, weight(2.25)|abundance(90)|weapon_length(1)|thrust_damage(10,pierce)|max_ammo(15), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],
["ccc_shot_shells", "Shot Shell ", [("ccd_ammo_bag_a",0),("bullet_flying",ixmesh_flying_ammo),("bullet",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_merchandise|itp_can_knock_down, 0, 41, weight(2.25)|abundance(90)|weapon_length(3)|thrust_damage(2,pierce)|max_ammo(20), imodbits_missile, [(ti_on_missile_hit,[(call_script, "script_oim_on_bullet_hit"),])] ],  ## CC-D
["ccd_cartridges_tracer", "Tracer Bullet", [("ccd_ammo_bag_b",0),("ccd_tracer",ixmesh_flying_ammo),("cartridge_b",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_merchandise|itp_can_penetrate_shield, 0, 80, weight(3.0)|abundance(60)|weapon_length(3)|thrust_damage(5,pierce)|max_ammo(32), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + ccd_tracer_triggers + missile_distance_trigger ],
["occc_cartridges_blaster_green", "Green Laser", [("ccd_ammo_bag_b",0),("laser_bolt_green",ixmesh_flying_ammo),("laser_bolt_green",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield|itp_ignore_gravity|itp_ignore_friction, 0, 80, weight(3.0)|abundance(60)|weapon_length(3)|thrust_damage(3,pierce)|max_ammo(32), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] +  missile_distance_trigger ],
["occc_cartridges_blaster_red", "Red Laser", [("ccd_ammo_bag_b",0),("laser_bolt_red",ixmesh_flying_ammo),("laser_bolt_red",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield|itp_ignore_gravity|itp_ignore_friction, 0, 80, weight(3.0)|abundance(60)|weapon_length(3)|thrust_damage(3,pierce)|max_ammo(32), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] +  missile_distance_trigger ],
["occc_cartridges_blaster_blue", "Blue Laser", [("ccd_ammo_bag_b",0),("laser_bolt_blue",ixmesh_flying_ammo),("laser_bolt_blue",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield|itp_ignore_gravity|itp_ignore_friction, 0, 80, weight(3.0)|abundance(60)|weapon_length(3)|thrust_damage(3,pierce)|max_ammo(32), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] +  missile_distance_trigger ],
["occc_greater_cartridges", "Heavy Cartridges", [("ccd_ammo_box_a",0),("bullet",ixmesh_flying_ammo),("cartridge_a",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield|itp_can_knock_down, 0, 41, weight(2.25)|abundance(70)|weapon_length(3)|thrust_damage(7,pierce)|max_ammo(35), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],

#arrow- pierce->cut occc damage +7
["arrows", "Arrows", [("arrow",0),("flying_arrow",ixmesh_flying_ammo),("quiver",ixmesh_carry)], itp_type_arrows|itp_default_ammo|itp_merchandise, itcf_carry_quiver_back, 72, weight(3)|abundance(160)|weapon_length(95)|thrust_damage(8,cut)|max_ammo(30), imodbits_missile, missile_distance_trigger ],
["khergit_arrows", "Khergit Arrows", [("arrow_b",0),("flying_arrow",ixmesh_flying_ammo),("quiver_b",ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right, 410, weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(10,cut)|max_ammo(30), imodbits_missile, missile_distance_trigger ],
["barbed_arrows", "Barbed Arrows", [("barbed_arrow",0),("flying_barbed_arrow",ixmesh_flying_ammo),("quiver_d",ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right, 124, weight(3)|abundance(70)|weapon_length(95)|thrust_damage(9,cut)|max_ammo(30), imodbits_missile, missile_distance_trigger ],
["bodkin_arrows", "Bodkin Arrows", [("piercing_arrow",0),("flying_arrow",ixmesh_flying_ammo),("quiver_c",ixmesh_carry)], itp_type_arrows|itp_merchandise, itcf_carry_quiver_back_right, 350, weight(3)|abundance(50)|weapon_length(91)|thrust_damage(10,cut)|max_ammo(28), imodbits_missile, missile_distance_trigger ],
#["ccc_arrow_bear", "Bear Arrow", [("lonely_ar",0),("flying_arrow",ixmesh_flying_ammo),("lonely_quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back_right, 1024, weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(4,pierce)|max_ammo(35), imodbits_missile, missile_distance_trigger ],
["ccc_arrow_gromiteq", "Gromite Arrow", [("gromitearrow",0),("flying_arrow",ixmesh_flying_ammo),("gromiteq",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back_right, 360, weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(13,cut)|max_ammo(43), imodbits_missile, missile_distance_trigger ],
["ccc_arrow_bodkin", "Bodkin Arrows", [("w_arr",0),("flying_piercing_arrow",ixmesh_flying_ammo),("w_qui",ixmesh_carry)], itp_type_arrows|itp_bonus_against_shield, itcf_carry_quiver_back_right, 500, weight(4.5)|abundance(30)|weapon_length(95)|thrust_damage(14,pierce)|max_ammo(32), imodbits_missile, missile_distance_trigger ],
["ccc_arrows_imperials", "Imperial Arrows", [("spak_arrow",0),("flying_arrow",ixmesh_flying_ammo),("spak_quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back_right, 400, weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(15,cut)|max_ammo(40), imodbits_missile, missile_distance_trigger ],
["ccc_arrow_amazon", "Steppe Arrows", [("amazon_arrow",0),("flying_arrow",ixmesh_flying_ammo),("amazon_quiver",ixmesh_carry)], itp_type_arrows, itcf_carry_quiver_back_right, 450, weight(2.5)|abundance(30)|weapon_length(85)|thrust_damage(11,cut)|max_ammo(45), imodbits_missile, missile_distance_trigger ],
["ccc_arrows_valkyrie", "Valkyrie Arrows", [("1steel_arrow",0),("flying_arrow",ixmesh_flying_ammo),("1steel_quiver",ixmesh_carry)], itp_merchandise|itp_type_arrows, itcf_carry_quiver_back_right, 400, abundance(500)|weight(3.5)|abundance(30)|weapon_length(95)|thrust_damage(14,cut)|max_ammo(40), imodbits_missile, missile_distance_trigger,[fac_valkyrie] ],
["ccd_fire_arrows", "Fire Arrows", [("3steel_arrow",0),("fire_arrow_flying_missile",ixmesh_flying_ammo),("arena_quiver",ixmesh_carry)], itp_type_arrows|itp_merchandise|itp_can_penetrate_shield|itp_bonus_against_shield|itp_no_pick_up_from_ground, itcf_carry_quiver_back, 600, weight(3)|abundance(60)|weapon_length(95)|thrust_damage(10,pierce)|max_ammo(30), imodbits_missile, fired_arrow_triggers + missile_distance_trigger ],
["ccd_mind_arrows", "Mind Arrows", [("gohst",0),("ccd_flying_mind_arrow",ixmesh_flying_ammo),("ccd_quiver_mind_arrow",ixmesh_carry),("ccd_flying_mind_arrow",ixmesh_inventory)], itp_type_arrows|itp_no_pick_up_from_ground|itp_ignore_gravity|itp_ignore_friction, itcf_carry_quiver_back_right, 2048, weight(3)|abundance(60)|weapon_length(95)|thrust_damage(3,blunt)|max_ammo(20), imodbits_missile,
  [(ti_on_missile_hit, [
    (store_trigger_param_1, ":agent_id"),
    
    (store_agent_hit_points, ":cur_hp", ":agent_id", 1),
    (try_begin),
      (ge, ":cur_hp", 20),
      
      (assign, ":ammo_all", 0),
      (try_for_range, ":cur_slot", 0, 4),
        (agent_get_item_slot, ":cur_item", ":agent_id", ":cur_slot"),
        (eq, ":cur_item", "itm_ccd_mind_arrows"),
        (agent_get_ammo_for_slot, ":ammo", ":agent_id", ":cur_slot"),
        (store_add, ":ammo_all", ":ammo"),
      (try_end),
      
      (lt, ":ammo_all", 10),
      (agent_set_ammo, ":agent_id", "itm_ccd_mind_arrows", 10),
      (val_sub, ":cur_hp", 2),
      (agent_set_hit_points, ":agent_id", ":cur_hp", 1),
      
      (agent_get_position, pos5, ":agent_id"),
      (play_sound_at_position, "snd_ccd_mind_arrow_charge", pos5),
    (try_end),
  ])] + missile_distance_trigger ],

#RANGED 
#occc thrown weapons' damage all 3/5 - 1
["darts", "Darts", [("dart_b",0),("dart_b_bag",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary, itcf_throw_javelin|itcf_carry_quiver_right_vertical|itcf_show_holster_when_drawn, 155, weight(4)|difficulty(1)|spd_rtng(95)|shoot_speed(28)|thrust_damage(12,pierce)|max_ammo(7)|weapon_length(32), imodbits_thrown, missile_distance_trigger ],
["stones", "Stones", [("throwing_stone",0)], itp_type_thrown|itp_merchandise|itp_primary, itcf_throw_stone, 1, weight(5)|difficulty(0)|spd_rtng(97)|shoot_speed(50)|thrust_damage(6,blunt)|max_ammo(40)|weapon_length(8), imodbit_large_bag, missile_distance_trigger ],
["ccc_stone_good", "Stone Sling", [("dou_stone_mokko",0),("throwing_stone",ixmesh_flying_ammo)], itp_type_thrown|itp_primary|itp_can_knock_down,
 itcf_throw_stone, 2, weight(4)|difficulty(2)|spd_rtng(71)|shoot_speed(65)|thrust_damage(20,blunt)|max_ammo(40)|weapon_length(8), imodbits_thrown_minus_heavy|imodbit_large_bag, missile_distance_trigger ],
["ccc_stone_ultimate", "Ultimate Stone Sling", [("dou_stone_mokko_big",0),("throwing_stone",ixmesh_flying_ammo)],
 itp_type_thrown|itp_merchandise|itp_primary|itp_can_knock_down, itcf_throw_stone, 3, weight(6)|difficulty(3)|spd_rtng(62)|shoot_speed(60)|thrust_damage(24,blunt)|max_ammo(40)|weapon_length(8), imodbit_large_bag, missile_distance_trigger ],
["ccd_rock", "Rocks", [("rock2",0)], itp_type_thrown|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_can_knock_down|itp_no_pick_up_from_ground, itcf_throw_axe, 24, weight(20)|difficulty(5)|spd_rtng(80)|shoot_speed(40)|thrust_damage(29,blunt)|max_ammo(4)|weapon_length(52), imodbit_large_bag, missile_distance_trigger ],
["ccd_grenade", "Grenade", [("ccd_grenade",0)], itp_type_thrown|itp_primary|itp_no_pick_up_from_ground, itcf_throw_stone, 256, weight(2)|difficulty(0)|spd_rtng(95)|shoot_speed(50)|thrust_damage(80,blunt)|max_ammo(2)|weapon_length(6), imodbits_none, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccd_item_hit_effect_explosion_missile", "itm_ccd_grenade", ":sa"),])] + missile_distance_trigger ],
["war_darts", "War Darts", [("dart_a",0),("dart_a_bag",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 285, weight(5)|difficulty(1)|spd_rtng(93)|shoot_speed(42)|thrust_damage(16,pierce)|max_ammo(9)|weapon_length(45), imodbits_thrown, missile_distance_trigger ],

#Throwing Blades
["ccc_throwing_dagger_ivoryhiltdag", "Throwing Dagger", [("daggera",0)], itp_type_thrown|itp_primary, itcf_throw_knife, 512, weight(1.5)|difficulty(0)|spd_rtng(120)|shoot_speed(24)|thrust_damage(26,cut)|max_ammo(8)|weapon_length(15), imodbits_thrown, missile_distance_trigger ],
["throwing_knives", "Throwing Knives", [("throwing_knife",0)], itp_type_thrown|itp_merchandise|itp_primary, itcf_throw_knife, 76, weight(2.5)|difficulty(0)|spd_rtng(121)|shoot_speed(24)|thrust_damage(11,cut)|max_ammo(14)|weapon_length(0), imodbits_thrown, missile_distance_trigger ],
["throwing_daggers", "Throwing Daggers", [("throwing_dagger",0)], itp_type_thrown|itp_merchandise|itp_primary, itcf_throw_knife, 193, weight(2.5)|difficulty(0)|spd_rtng(110)|shoot_speed(24)|thrust_damage(15,cut)|max_ammo(13)|weapon_length(0), imodbits_thrown, missile_distance_trigger ],
#["ccd_syuriken", "Syuriken", [("star_shruiken_A", 0)], itp_type_thrown|itp_primary, itcf_throw_knife|itcf_carry_dagger_front_left, 512, weight(2)|difficulty(4)|spd_rtng(112)|shoot_speed(55)|thrust_damage(28, pierce)|max_ammo(12)|weapon_length(0), imodbits_thrown, missile_distance_trigger ],

#JP
["ccc_jp_syuriken_1", "Syuriken", [("fumastar",0)], itp_type_thrown|itp_primary, itcf_throw_stone, 240, weight(2)|difficulty(4)|spd_rtng(140)|shoot_speed(55)|thrust_damage(18,pierce)|max_ammo(16)|weapon_length(5), imodbits_thrown ],
["ccc_jp_syuriken_2", "Fuuma Syuriken", [("fumastar2",0)], itp_type_thrown|itp_primary, itcf_throw_stone, 512, weight(4)|difficulty(5)|spd_rtng(85)|shoot_speed(45)|thrust_damage(47,pierce)|max_ammo(2)|weapon_length(20), imodbits_thrown ],

#Throwing Axes
["light_throwing_axes", "Light Throwing Axes", [("francisca",0),("francisca_quiver",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary|itp_next_item_as_melee, itcf_throw_axe|itcf_carry_quiver_back_right|itcf_show_holster_when_drawn, 360, weight(5)|difficulty(2)|spd_rtng(99)|shoot_speed(18)|thrust_damage(20,cut)|max_ammo(4)|weapon_length(53), imodbits_thrown_minus_heavy, missile_distance_trigger ],
["light_throwing_axes_melee", "Light Throwing Axe", [("francisca",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar, 360, weight(1)|difficulty(2)|spd_rtng(99)|weapon_length(53)|swing_damage(26,cut), imodbits_thrown_minus_heavy ],
["throwing_axes", "Throwing Axes", [("throwing_axe_a",0),("throwing_axe_a_quiver",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary|itp_next_item_as_melee, itcf_throw_axe|itcf_carry_quiver_back_right|itcf_show_holster_when_drawn, 490, weight(5)|difficulty(3)|spd_rtng(98)|shoot_speed(18)|thrust_damage(25,cut)|max_ammo(4)|weapon_length(53), imodbits_thrown_minus_heavy, missile_distance_trigger ],
["throwing_axes_melee", "Throwing Axe", [("throwing_axe_a",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar, 490, weight(1)|difficulty(3)|spd_rtng(98)|swing_damage(29,cut)|weapon_length(53), imodbits_thrown_minus_heavy ],
["heavy_throwing_axes", "Heavy Throwing Axes", [("throwing_axe_b",0),("throwing_axe_b_quiver",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary|itp_next_item_as_melee, itcf_throw_axe|itcf_carry_quiver_back_right|itcf_show_holster_when_drawn, 620, weight(5)|difficulty(4)|spd_rtng(97)|shoot_speed(18)|thrust_damage(30,cut)|max_ammo(4)|weapon_length(53), imodbits_thrown_minus_heavy, missile_distance_trigger ],
["heavy_throwing_axes_melee", "Heavy Throwing Axe", [("throwing_axe_b",0)], itp_type_one_handed_wpn|itp_primary|itp_bonus_against_shield, itc_scimitar, 620, weight(1)|difficulty(4)|spd_rtng(97)|swing_damage(32,cut)|weapon_length(53), imodbits_thrown_minus_heavy ],

#one-hand_axe_throwing
["ccc_throwing_axe_dunlard1", "Dunlard Axe", [("dunlard_axe",0)], itp_type_thrown|itp_primary|itp_next_item_as_melee, itcf_throw_axe, 800, weight(5)|difficulty(2)|spd_rtng(95)|shoot_speed(18)|thrust_damage(32,cut)|max_ammo(9)|weapon_length(59), imodbits_thrown_minus_heavy, missile_distance_trigger ],#6->9
["ccc_throwing_axe_dunlard1_melee", "Dunlard Axe melee", [("dunlard_axe",0)], itp_type_one_handed_wpn|itp_unique|itp_primary|itp_bonus_against_shield, itc_scimitar, 800, weight(1)|difficulty(3)|spd_rtng(98)|swing_damage(35,cut)|weapon_length(59), imodbits_thrown_minus_heavy ],
["ccc_throwing_axe_dunlard2", "Shadow  Axe", [("dunlardaxe2",0)], itp_type_thrown|itp_primary|itp_can_penetrate_shield|itp_next_item_as_melee, itcf_throw_axe, 1024, weight(5)|difficulty(2)|spd_rtng(95)|shoot_speed(18)|thrust_damage(26,pierce)|max_ammo(12)|weapon_length(59), imodbits_thrown_minus_heavy, missile_distance_trigger ],#6->12
["ccc_throwing_axe_dunlard2_melee", "Shadow Axe", [("dunlardaxe2",0)], itp_type_one_handed_wpn|itp_unique|itp_primary|itp_bonus_against_shield, itc_scimitar, 1024, weight(1)|difficulty(3)|spd_rtng(98)|swing_damage(34,pierce)|weapon_length(59), imodbits_thrown_minus_heavy ],
["ccc_throwing_axe_gim", "Gim Axe", [("doubleAxe",0)], itp_type_thrown|itp_primary|itp_bonus_against_shield|itp_can_knock_down|itp_next_item_as_melee, itcf_throw_axe|itcf_carry_axe_back, 954, weight(5)|difficulty(2)|spd_rtng(110)|shoot_speed(18)|thrust_damage(44,cut)|max_ammo(5)|weapon_length(92), imodbits_thrown_minus_heavy, missile_distance_trigger ],#4->5
["ccc_throwing_axe_gim_melee", "Gim Axe", [("doubleAxe",0)], itp_type_one_handed_wpn|itp_unique|itp_primary|itp_bonus_against_shield|itp_remove_item_on_use, itc_scimitar|itcf_carry_axe_back, 954, weight(1)|difficulty(3)|spd_rtng(98)|swing_damage(35,cut)|weapon_length(92), imodbits_thrown_minus_heavy ],
#
#throwing-spear
["javelin", "Javelins", [("javelin",0),("javelins_quiver_new",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary|itp_next_item_as_melee, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 300, weight(4)|difficulty(1)|spd_rtng(91)|shoot_speed(23)|thrust_damage(21,pierce)|max_ammo(5)|weapon_length(75), imodbits_thrown, missile_distance_trigger ],
["javelin_melee", "Javelin", [("javelin",0)], itp_type_polearm|itp_wooden_parry|itp_primary, itc_staff, 300, weight(1)|difficulty(0)|spd_rtng(120)|swing_damage(12,cut)|thrust_damage(14,pierce)|weapon_length(75), imodbits_polearm ],
["throwing_spears", "Throwing Spears", [("jarid_new_b",0),("jarid_new_b_bag",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary|itp_next_item_as_melee, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 525, weight(3)|difficulty(2)|spd_rtng(87)|shoot_speed(22)|thrust_damage(26,pierce)|max_ammo(4)|weapon_length(65), imodbits_thrown, missile_distance_trigger ],
["throwing_spear_melee", "Throwing Spear", [("jarid_new_b",0),("javelins_quiver",ixmesh_carry)], itp_type_polearm|itp_wooden_parry|itp_primary, itc_staff, 525, weight(1)|difficulty(1)|spd_rtng(117)|swing_damage(18,cut)|thrust_damage(23,pierce)|weapon_length(75), imodbits_thrown ],
["jarid", "Jarids", [("jarid_new",0),("jarid_quiver",ixmesh_carry)], itp_type_thrown|itp_merchandise|itp_primary|itp_next_item_as_melee, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 560, weight(2.75)|difficulty(2)|spd_rtng(89)|shoot_speed(23)|thrust_damage(26,pierce)|max_ammo(4)|weapon_length(65), imodbits_thrown, missile_distance_trigger ],
["jarid_melee", "Jarid", [("jarid_new",0),("jarid_quiver",ixmesh_carry)], itp_type_polearm|itp_wooden_parry|itp_primary, itc_staff, 560, weight(1)|difficulty(2)|spd_rtng(112)|swing_damage(16,cut)|thrust_damage(20,pierce)|weapon_length(65), imodbits_thrown ],

["ccc_throwing_spear_dark", "Dark Spear", [("xpspearraptor_1",0)], itp_type_thrown|itp_primary|itp_next_item_as_melee, itcf_throw_javelin, 800, weight(3)|difficulty(4)|spd_rtng(75)|shoot_speed(22)|thrust_damage(41,pierce)|max_ammo(3)|weapon_length(160), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_spear_dark_melee", "Dark Spear melee", [("xpspearraptor_1",0)], itp_type_polearm|itp_primary|itp_remove_item_on_use, itc_cutting_spear, 800, weight(3)|difficulty(3)|spd_rtng(106)|swing_damage(0,cut)|thrust_damage(40,pierce)|weapon_length(160), imodbits_polearm ],
["ccc_throwing_spear_roma_pilum", "Pilum", [("pilum",0)], itp_type_thrown|itp_primary|itp_bonus_against_shield, itcf_throw_javelin, 600, weight(3)|difficulty(1)|spd_rtng(85)|shoot_speed(22)|thrust_damage(32,pierce)|max_ammo(5)|weapon_length(80), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_spear_roma_pilum_w", "Pilum", [("pilum_w",0)], itp_type_thrown|itp_primary|itp_bonus_against_shield, itcf_throw_javelin, 677, weight(3)|difficulty(1)|spd_rtng(112)|shoot_speed(22)|thrust_damage(38,pierce)|max_ammo(5)|weapon_length(80), imodbits_thrown ],
["ccc_throwing_spear_roma_hasta", "Hasta", [("hasta",0)], itp_type_thrown|itp_primary|itp_bonus_against_shield|itp_next_item_as_melee|itp_remove_item_on_use, itcf_throw_javelin, 750, weight(3)|difficulty(2)|spd_rtng(80)|shoot_speed(22)|thrust_damage(74,pierce)|max_ammo(1)|weapon_length(160), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_spear_roma_hasta_melee", "Hasta Melee", [("hasta",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_unique|itp_remove_item_on_use, itc_cutting_spear, 750, weight(3)|difficulty(3)|spd_rtng(110)|swing_damage(32,cut)|thrust_damage(38,pierce)|weapon_length(160), imodbits_polearm ],
["ccc_throwing_spears_ken", "Throwing Spears", [("throwing_spearwe_ken",0),("throwing_spearwe_ken_quiver",ixmesh_carry)], itp_type_thrown|itp_primary, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 525, weight(4)|difficulty(2)|spd_rtng(87)|shoot_speed(28)|thrust_damage(24,pierce)|max_ammo(9)|weapon_length(65), imodbits_thrown ],
["ccc_throwing_spear_valkyrie", "Valkyrie Spear", [("valspear",0)], itp_merchandise|itp_type_thrown|itp_primary|itp_bonus_against_shield|itp_next_item_as_melee, itcf_throw_javelin, 2048, abundance(500)|weight(4)|difficulty(6)|spd_rtng(100)|shoot_speed(22)|thrust_damage(32,pierce)|max_ammo(6)|weapon_length(140), imodbits_thrown,[],[fac_valkyrie] ],
["ccc_throwing_spear_valkyrie_melee", "Valkyrie Spear melee", [("valspear",0)], itp_type_polearm|itp_unique|itp_primary|itp_offset_lance|itp_couchable, itc_cutting_spear, 2048, weight(4)|difficulty(6)|spd_rtng(110)|swing_damage(37,cut)|thrust_damage(42,pierce)|weapon_length(140), imodbits_polearm ],

#Bows
["hunting_bow", "Hunting Bow", [("hunting_bow",0),("hunting_bow_carry",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 17, weight(1)|difficulty(0)|spd_rtng(100)|shoot_speed(57)|thrust_damage(15,cut), imodbits_bow ],
["short_bow", "Short Bow", [("short_bow",0),("short_bow_carry",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 58, weight(1)|difficulty(1)|spd_rtng(97)|shoot_speed(60)|thrust_damage(18,cut), imodbits_bow ],
["nomad_bow", "Nomad Bow", [("nomad_bow",0),("nomad_bow_case",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 164, weight(1.25)|difficulty(2)|spd_rtng(94)|shoot_speed(60)|thrust_damage(20,cut), imodbits_bow ],
["long_bow", "Long Bow", [("long_bow",0),("long_bow_carry",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 145, weight(1.75)|difficulty(3)|spd_rtng(79)|shoot_speed(60)|thrust_damage(22,cut), imodbits_bow ],
["khergit_bow", "Khergit Bow", [("khergit_bow",0),("khergit_bow_case",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 269, weight(1.25)|difficulty(3)|spd_rtng(90)|shoot_speed(60)|thrust_damage(21,cut), imodbits_bow ],
["strong_bow", "Strong Bow", [("strong_bow",0),("strong_bow_case",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 437, weight(1.25)|difficulty(3)|spd_rtng(88)|shoot_speed(63)|thrust_damage(23,cut), imodbit_cracked|imodbit_bent|imodbit_masterwork ],
["war_bow", "War Bow", [("war_bow",0),("war_bow_carry",ixmesh_carry)], itp_type_bow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 728, weight(1.5)|difficulty(4)|spd_rtng(84)|shoot_speed(64)|thrust_damage(25,cut), imodbits_bow ],
["ccc_bow_imperial", "Imperial Bow", [("imperial_bow",0),("imperial_bow_case",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 1800, weight(1.5)|difficulty(6)|spd_rtng(90)|shoot_speed(64)|thrust_damage(31,cut), imodbits_bow ],
["ccc_bow_amazon", "Composite Bow", [("amazon_bow",0),("amazon_bow_case",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 1500, weight(1.5)|difficulty(4)|spd_rtng(110)|shoot_speed(60)|thrust_damage(26,cut), imodbits_bow ],
["ccc_bow_long_bow", "Nordic Long Bow", [("long_bow",0),("long_bow_carry",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 1800, weight(1.75)|difficulty(6)|spd_rtng(61)|shoot_speed(73)|thrust_damage(31,pierce), imodbits_bow ],
["ccc_bow_saradin", "Saradin Bow", [("fable_bow_4053",0),("fable_bow_4053_carry",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 1800, weight(1.75)|difficulty(4)|spd_rtng(99)|shoot_speed(63)|thrust_damage(30,cut), imodbits_bow ],
["ccc_bow_jp_wa_bow", "Wa Bow", [("heavy_yumi",0),], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 1800, weight(1.75)|difficulty(6)|spd_rtng(55)|shoot_speed(70)|thrust_damage(36,pierce), imodbits_bow ],
["ccc_bow_valkyrie_bow", "Valkyrie Bow", [("lonely",0),("lonely_carry",ixmesh_carry)], itp_merchandise|itp_type_bow|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 3024, abundance(500)|weight(1.75)|difficulty(5)|spd_rtng(110)|shoot_speed(60)|thrust_damage(29,cut), imodbits_bow,[],[fac_valkyrie] ],

#Crossbows
["hunting_crossbow", "Hunting Crossbow", [("light_crossbow",0)], itp_type_crossbow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 22, weight(2.25)|difficulty(0)|spd_rtng(47)|shoot_speed(55)|thrust_damage(37,pierce)|max_ammo(1), imodbits_crossbow ],
["light_crossbow", "Light Crossbow", [("crossbow_b",0)], itp_type_crossbow|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 67, weight(2.5)|difficulty(8)|spd_rtng(45)|shoot_speed(64)|thrust_damage(44,pierce)|max_ammo(1), imodbits_crossbow ],
["crossbow", "Crossbow", [("crossbow_a",0)], itp_type_crossbow|itp_merchandise|itp_cant_reload_on_horseback|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 182, weight(3)|difficulty(8)|spd_rtng(43)|shoot_speed(65)|thrust_damage(49,pierce)|max_ammo(1), imodbits_crossbow ],
["heavy_crossbow", "Heavy Crossbow", [("heavy_crossbow",0)], itp_type_crossbow|itp_merchandise|itp_cant_reload_on_horseback|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 349, weight(3.5)|difficulty(9)|spd_rtng(41)|shoot_speed(70)|thrust_damage(58,pierce)|max_ammo(1), imodbits_crossbow ],
["sniper_crossbow", "Siege Crossbow", [("crossbow_c",0)], itp_type_crossbow|itp_merchandise|itp_cant_reload_on_horseback|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 683, weight(3.75)|difficulty(10)|spd_rtng(37)|shoot_speed(70)|thrust_damage(63,pierce)|max_ammo(1), imodbits_crossbow ],
["ccc_crossbow_sniper", "Sniper Crossbow", [("crossbow_a2_",0)], itp_type_crossbow|itp_cant_reload_on_horseback|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 850, weight(3.75)|difficulty(10)|spd_rtng(43)|shoot_speed(90)|thrust_damage(70,pierce)|max_ammo(1), imodbits_crossbow ],
["ccc_crossbow_roma", "Roman Crossbow", [("crossbow_b2_",0)], itp_type_crossbow|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 780, weight(3.75)|difficulty(10)|spd_rtng(43)|shoot_speed(70)|thrust_damage(65,pierce)|max_ammo(1), imodbits_crossbow ],
["ccd_rendo", "Rendo", [("crossbow_c2_", 0)], itp_type_crossbow|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 2048, weight(4)|difficulty(10)|spd_rtng(64)|shoot_speed(65)|thrust_damage(52,pierce)|max_ammo(8),imodbits_crossbow ],
["ccd_reaping_crossbow", "DD Crossbow", [("r-crossbow_cy", 0)], itp_type_crossbow|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 2048, weight(4)|difficulty(12)|spd_rtng(40)|shoot_speed(96)|thrust_damage(58,pierce)|max_ammo(3),imodbits_crossbow ],
["ccd_fatal_crossbow", "Fatal Crossbow", [("crossbow_cy3",0)], itp_type_crossbow|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 2048, weight(12)|difficulty(12)|spd_rtng(18)|shoot_speed(180)|thrust_damage(190,pierce)|max_ammo(1), imodbits_crossbow ],

#pistols
#occc v0.2 overall damage +30 accuracy -20
["ccc_pistol_pepperbox_a", "The Dirty Dozen", [("pistol_pepperbox_a",0),("pistol_pepperbox_a_carry",ixmesh_carry)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 50000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(40)|shoot_speed(58)|thrust_damage(90,pierce)|max_ammo(12)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_pepperbox_b", "Eight Barrel Pepperbox", [("pistol_pepperbox_b",0),("pistol_pepperbox_b_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 3000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(35)|shoot_speed(52)|thrust_damage(65,pierce)|max_ammo(8)|accuracy(40), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_revolver_b", "Revolver 8", [("pistol_revolver_b",0),("pistol_revolver_b_carry",ixmesh_carry)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 60000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(70)|thrust_damage(90,pierce)|max_ammo(8)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_pepperbox_c", "Six Barrel Pepperbox", [("pistol_pepperbox_c",0),("pistol_pepperbox_c_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 20000, weight(2.2)|abundance(90)|difficulty(0)|spd_rtng(30)|shoot_speed(52)|thrust_damage(90,pierce)|max_ammo(6)|accuracy(55), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_pepperbox_d", "Seven Barrel Pepperbox", [("pistol_pepperbox_d",0),("pistol_pepperbox_d_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 40000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(30)|shoot_speed(52)|thrust_damage(75,pierce)|max_ammo(7)|accuracy(55), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],

["ccc_pistol_revolver_a", "Revolver 6", [("pistol_revolver_a",0),("pistol_revolver_a_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 7800, weight(2)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(70)|thrust_damage(80,pierce)|max_ammo(6)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_revolver_c", "Revolver 5", [("pistol_revolver_c",0),("pistol_revolver_c_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 5000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(70)|thrust_damage(80,pierce)|max_ammo(5)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_revolver_star", "Pistol Of The Moon", [("pistol_revolver_star",0),("pistol_revolver_star_carry",ixmesh_carry)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 1000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(82)|shoot_speed(80)|thrust_damage(80,pierce)|max_ammo(5)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot9"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_revolver_d", "Revolver 4", [("pistol_revolver_d",0),("pistol_revolver_d_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 4000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(70)|thrust_damage(65,pierce)|max_ammo(4)|accuracy(45), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_4barrel", "Quadro Barrel Pistol", [("pistol_4barrel",0),("pistol_4barrel_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 400, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(40)|shoot_speed(65)|thrust_damage(60,pierce)|max_ammo(4)|accuracy(35), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_3barrel", "Triple Barrel Pistol", [("pistol_3barrel",0),("pistol_3barrel_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 4500, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(40)|shoot_speed(65)|thrust_damage(75,pierce)|max_ammo(3)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot10"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_2barrel_star", "Pistol Of The Stars", [("pistol_2barrel_star",0),("pistol_2barrel_star_carry",ixmesh_carry)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 100, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(82)|shoot_speed(80)|thrust_damage(82,pierce)|max_ammo(2)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot10"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_2barrel", "Double Barrel Pistol", [("pistol_2barrel_a",0),("pistol_2barrel_a_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 1000, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(65)|thrust_damage(75,pierce)|max_ammo(2)|accuracy(45), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot9"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_2barrel_carabina", "Double Barrel Carabina", [("pistol_2barrel_carabina",0),("pistol_2barrel_carabina_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 7000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(53)|shoot_speed(100)|thrust_damage(80,pierce)|max_ammo(2)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot5"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_2barrel_revolver", "Double Barrel Revolver", [("pistol_2barrel_revolver",0),("pistol_2barrel_revolver_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 1500, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(65)|thrust_damage(65,pierce)|max_ammo(6)|accuracy(40), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot9"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_lorenzoni", "Lorenzoni Pistol", [("pistol_lorenzoni",0),("pistol_lorenzoni_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 4000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(35)|shoot_speed(51)|thrust_damage(65,pierce)|max_ammo(7)|accuracy(50), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot8"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_lorenzoni_noble", "Noble Lorenzoni Pistol", [("pistol_lorenzoni_noble",0),("pistol_lorenzoni_noble_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 10000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(35)|shoot_speed(51)|thrust_damage(85,pierce)|max_ammo(7)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot8"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_lorenzoni_officer", "Lorenzoni Officer Pistol", [("pistol_lorenzoni_officer",0),("pistol_lorenzoni_officer_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol,
 6500, weight(2)|abundance(90)|difficulty(0)|spd_rtng(40)|shoot_speed(65)|thrust_damage(75,pierce)|max_ammo(7)|accuracy(50), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot8"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_2] ],
["ccc_pistol_ottoman_a", "Ottoman Pistol", [("pistol_ottoman_a",0),("pistol_ottoman_a_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_can_knock_down|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 3500, weight(2)|abundance(90)|difficulty(0)|spd_rtng(75)|shoot_speed(60)|thrust_damage(115,pierce)|max_ammo(1)|accuracy(50), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_6] ],
["ccc_pistol_ottoman_b", "Ottoman Pistol", [("pistol_ottoman_b",0),("pistol_ottoman_b_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_can_knock_down|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 3500, weight(2)|abundance(90)|difficulty(0)|spd_rtng(75)|shoot_speed(60)|thrust_damage(115,pierce)|max_ammo(1)|accuracy(50), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot7"),(call_script, "script_ccd_gun_particle", 0),])], [fac_kingdom_6] ],
["ccc_pistol_rouet_b", "Rouet", [("pistol_rouet_b",0),("pistol_rouet_b_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_merchandise|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 2000, weight(2)|abundance(90)|difficulty(0)|spd_rtng(85)|shoot_speed(65)|thrust_damage(85,pierce)|max_ammo(1)|accuracy(40), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot4"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_rouet_a", "Great Rouet", [("pistol_rouet_a",0),("pistol_rouet_a_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_merchandise|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 5500, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(85)|shoot_speed(65)|thrust_damage(95,pierce)|max_ammo(1)|accuracy(55), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot4"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_blunderbuss_a", "Blunder Pistol", [("pistol_blunderbuss_a",0),("pistol_blunderbuss_a_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 1500, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(100)|shoot_speed(45)|thrust_damage(105,pierce)|max_ammo(1)|accuracy(25), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot3"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_blunderbuss_b", "Blunder Pistol", [("pistol_blunderbuss_b",0),("pistol_blunderbuss_b_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 9000, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(120)|shoot_speed(45)|thrust_damage(135,pierce)|max_ammo(1)|accuracy(15), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot3"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_flintlock_a", "Golden Flintlock Pistol", [("pistol_flintlock_a",0),("pistol_flintlock_a_carry",ixmesh_carry)], itp_type_pistol|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 50000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(100)|shoot_speed(75)|thrust_damage(100,pierce)|max_ammo(1)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_flintlock_b", "Great Flintlock Pistol", [("pistol_flintlock_b",0),("pistol_flintlock_b_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 8000, weight(1.0)|abundance(90)|difficulty(0)|spd_rtng(80)|shoot_speed(65)|thrust_damage(100,pierce)|max_ammo(1)|accuracy(65), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_flintlock_c", "Noble Flintlock Pistol", [("pistol_flintlock_c",0),("pistol_flintlock_c_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 10000, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(80)|shoot_speed(65)|thrust_damage(105,pierce)|max_ammo(1)|accuracy(65), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_flintlock_d", "Flintlock Pistol", [("pistol_flintlock_d",0),("pistol_flintlock_d_carry",ixmesh_carry)], itp_type_pistol|itp_merchandise|itp_primary|itp_can_knock_down, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
 500, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(80)|shoot_speed(65)|thrust_damage(80,pierce)|max_ammo(1)|accuracy(50), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_automatic", "Automatic Pistol", [("flintlock_pistol",30000)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_reload_pistol,
 40000, weight(1.5)|abundance(90)|difficulty(0)|spd_rtng(150)|shoot_speed(85)|thrust_damage(60,pierce)|max_ammo(150)|accuracy(50), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_shot"),(call_script, "script_ccd_gun_particle", 0),])] ],

#["ccc_pistol_shotgun_a", "Shotgun", [("pistol_shotgun_a",0),("pistol_shotgun_b_carry",ixmesh_carry)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
# 0, weight(2)|abundance(90)|difficulty(0)|spd_rtng(70)|shoot_speed(44)|thrust_damage(35,pierce)|max_ammo(1)|accuracy(76), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot6"),(call_script, "script_ccd_gun_particle", 0),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
#["ccc_pistol_shotgun_b", "Shotgun", [("pistol_shotgun_b",0),("pistol_shotgun_b_carry",ixmesh_carry)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol,
# 0, weight(2)|abundance(90)|difficulty(0)|spd_rtng(70)|shoot_speed(44)|thrust_damage(35,pierce)|max_ammo(1)|accuracy(76), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot6"),(call_script, "script_ccd_gun_particle", 0),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],

#rifles
#OCCC rifles and pistols shooting velocity matched difor's version
#...and single load rifles get buffed on its damage... generally +12
#occc additional start
["occc_organ_8barrel", "Eight Barrel Gun", [("rifle_8barrel",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 13000, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(37)|shoot_speed(100)|thrust_damage(92,pierce)|max_ammo(8)|accuracy(74), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),])] ],
#occc additional end 
["ccc_rifle_10shot", "Ten Shot Rifle", [("rifle_10shot",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 50000, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(40)|shoot_speed(120)|thrust_damage(85,pierce)|max_ammo(10)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_4shot_musket", "Four Shot Musket", [("rifle_4shot_musket",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 5000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(110)|thrust_damage(70,pierce)|max_ammo(4)|accuracy(65), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot20"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_4shot_rifle", "Four Shot Rifle", [("rifle_4shot_rifle",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 9000, weight(2.6)|abundance(90)|difficulty(0)|spd_rtng(44)|shoot_speed(120)|thrust_damage(70,pierce)|max_ammo(4)|accuracy(85), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot18"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_6shot", "Six Shot Coachgun", [("rifle_6shot",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 8000, weight(2.7)|abundance(90)|difficulty(0)|spd_rtng(35)|shoot_speed(120)|thrust_damage(70,pierce)|max_ammo(6)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_rifle_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_lorenzoni", "Lorenzoni", [("rifle_lorenzoni",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 15000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(30)|shoot_speed(120)|thrust_damage(70,pierce)|max_ammo(7)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_airgunfire"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_2barrel_hunting", "Double Barrel Hunting Rifle", [("rifle_2barrel_hunting",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 7000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(42)|shoot_speed(120)|thrust_damage(75,pierce)|max_ammo(2)|accuracy(88), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot17"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_2barrel_couchgun", "Double Barel Coachgun", [("rifle_2barrel_couchgun",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 2000, weight(3)|abundance(90)|difficulty(0)|spd_rtng(35)|shoot_speed(120)|thrust_damage(65,pierce)|max_ammo(2)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_cav_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_2barrel_star", "Rifle Of The Dawn", [("rifle_2barrel_star",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 12000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(120)|thrust_damage(80,pierce)|max_ammo(2)|accuracy(85), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot17"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_2barrel_carabina", "Double Barrel Carabine Rifle", [("rifle_2barrel_carabina",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 7000, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(115)|thrust_damage(75,pierce)|max_ammo(2)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_cav_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_ottoman_a", "Ottoman Rifle", [("rifle_ottoman_a",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 4000, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(48)|shoot_speed(130)|thrust_damage(92,pierce)|max_ammo(1)|accuracy(86), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot14"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_6] ],
["ccc_rifle_ottoman_b", "Ottoman Musket", [("rifle_ottoman_b",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 3500, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(56)|shoot_speed(110)|thrust_damage(82,pierce)|max_ammo(1)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot14"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_6] ],
["ccc_rifle_black", "Rifle Of The Dark", [("rifle_black",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 6500, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(130)|thrust_damage(90,pierce)|max_ammo(4)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_7] ],
["ccc_rifle_star_a", "Rifle Of The Stars", [("rifle_star_a",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 1000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(65)|shoot_speed(130)|thrust_damage(79,pierce)|max_ammo(7)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot14"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_star_b", "Rifle Of The Night", [("rifle_star_b",0)], itp_type_musket|itp_two_handed|itp_primary|itp_crush_through|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 1000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(75)|shoot_speed(130)|thrust_damage(95,pierce)|max_ammo(2)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot14"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_star_c", "Rifle Of The Moon", [("rifle_star_c",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 1000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(55)|shoot_speed(130)|thrust_damage(85,pierce)|max_ammo(7)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot14"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_musketair", "Musketair", [("rifle_musketair",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_use_on_horseback, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 1500, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(120)|thrust_damage(60,pierce)|max_ammo(1)|accuracy(95), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot17"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_noble_b", "Noble Rifle", [("rifle_noble_b",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 10000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(130)|thrust_damage(74,pierce)|max_ammo(1)|accuracy(95), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_musketoon_a", "Hunting Musketoon", [("rifle_musketoon_a",0)], itp_type_musket|itp_merchandise|itp_cant_reload_on_horseback|itp_two_handed|itp_primary, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 500, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(55)|shoot_speed(100)|thrust_damage(52,pierce)|max_ammo(1)|accuracy(65), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_musketoon_b", "Noble Musketoon", [("rifle_musketoon_b",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 10000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(65)|shoot_speed(100)|thrust_damage(92,pierce)|max_ammo(1)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_musketoon_c", "Musketoon", [("rifle_musketoon_c",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 4000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(100)|thrust_damage(79,pierce)|max_ammo(1)|accuracy(83), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_couchgun", "Coachgun", [("rifle_couchgun",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 2000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(105)|thrust_damage(67,pierce)|max_ammo(1)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot15"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
#value tweak 1/2 occc start
["ccc_rifle_musketoonpel", "Musketoonpel", [("rifle_musketoonpel",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 1250, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(84)|shoot_speed(120)|thrust_damage(66,pierce)|max_ammo(1)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])] ],
#["ccc_rifle_musketmel", "Musketmel", [("Russian_dragoon_musket",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
# 1000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(68)|thrust_damage(55,pierce)|max_ammo(1)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_musket", "Musket", [("rifle_musket",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_next_item_as_melee|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 2000, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(70)|shoot_speed(110)|thrust_damage(87,pierce)|max_ammo(1)|accuracy(85), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_musket_mel", "Musket", [("rifle_musket",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback, itcf_slashright_twohanded|itcf_slashleft_twohanded|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_carry_spear|itc_parry_polearm,
 2000, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(105)|weapon_length(100)|swing_damage(20,blunt)|thrust_damage(20,blunt), imodbits_crossbow ],
#value tweak 1/2 occc end
 ["ccc_rifle_arquebuse_a", "Great Arquebuse", [("rifle_arquebuse_a",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 7400, weight(3)|abundance(90)|difficulty(0)|spd_rtng(65)|shoot_speed(117)|thrust_damage(82,pierce)|max_ammo(1)|accuracy(83), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_arquebuse_b", "Long Arquebuse", [("rifle_arquebuse_b",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 3000, weight(2.8)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(117)|thrust_damage(77,pierce)|max_ammo(1)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot9"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_arquebuse_c", "Arquebuse", [("rifle_arquebuse_c",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 3000, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(58)|shoot_speed(117)|thrust_damage(69,pierce)|max_ammo(1)|accuracy(67), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot9"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_arquebuse_d", "Short Arquebuse", [("rifle_arquebuse_d",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 3000, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(117)|thrust_damage(69,pierce)|max_ammo(1)|accuracy(55), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot9"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_arquebuse", "Arquebuse", [("rifle_arquebuse_b",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_next_item_as_melee|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 7400, weight(3)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(117)|thrust_damage(82,pierce)|max_ammo(1)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_merc_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_arquebuse_mel", "Arquebuse", [("rifle_arquebuse_b",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_primary|itp_cant_use_on_horseback, itc_poleaxe|itcf_thrust_polearm|itcf_carry_spear,
 7400, weight(3)|abundance(90)|difficulty(0)|spd_rtng(78)|weapon_length(100)|swing_damage(23,blunt)|thrust_damage(18,pierce), imodbits_crossbow ],
["ccc_rifle_short_arquebuse", "Short_Arquebuse", [("rifle_arquebuse_c",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_next_item_as_melee, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 3000, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(65)|shoot_speed(117)|thrust_damage(77,pierce)|max_ammo(1)|accuracy(67), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot9"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_short_arquebuse_mel", "Short Arquebuse", [("rifle_arquebuse_c",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_primary, itcf_thrust_twohanded|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itc_parry_polearm|itcf_carry_spear,
 3000, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(98)|weapon_length(100)|swing_damage(18,cut)|thrust_damage(18,pierce), imodbits_crossbow ],

["ccc_rifle_musket_jp_1", "Hinawazyu", [("tanegashima",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 1524, weight(2.0)|difficulty(0)|spd_rtng(60)|shoot_speed(120)|thrust_damage(97,pierce)|max_ammo(1)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_musket_jp_2", "Hinawazyu Made in Sakai", [("tanegashima3",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 2524, weight(2.0)|difficulty(0)|spd_rtng(58)|shoot_speed(120)|thrust_damage(102,pierce)|max_ammo(1)|accuracy(85), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),])] ],
 
["ccc_rifle_8barrel", "Eight Barrel Shotgun", [("rifle_8barrel",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 20000, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(35)|shoot_speed(75)|thrust_damage(90,pierce)|max_ammo(8)|accuracy(55), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["ccc_rifle_4barrel", "Four Barrel Shotgun", [("rifle_4barrel",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 5500, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(30)|shoot_speed(75)|thrust_damage(80,pierce)|max_ammo(4)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot17"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["ccc_rifle_2barrel_shotgun", "Double Barrel Shotgun", [("rifle_2barrel_shotgun",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 4200, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(40)|shoot_speed(75)|thrust_damage(75,pierce)|max_ammo(2)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot16"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["ccc_rifle_shotgun_a", "Shotgun Rifle", [("rifle_shotgun_a",0)], itp_type_musket|itp_two_handed|itp_primary|itp_next_item_as_melee|itp_can_knock_down|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 8200, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(50)|shoot_speed(80)|thrust_damage(60,pierce)|max_ammo(2)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot16"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["ccc_rifle_shotgun_a_melee", "Shotgun Rifle", [("rifle_shotgun_a",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_primary|itp_can_knock_down, itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_carry_spear,
 8200, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(94)|weapon_length(80)|swing_damage(31,blunt)|thrust_damage(31,blunt), imodbits_crossbow ],
["ccc_rifle_shotgun_b", "Shotgun Rifle", [("rifle_shotgun_b",0)], itp_type_musket|itp_two_handed|itp_primary|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 50000, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(55)|shoot_speed(90)|thrust_damage(105,pierce)|max_ammo(5)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot16"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["ccc_rifle_noble_a", "Noble Shotgun", [("rifle_noble_a",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_use_on_horseback, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 10000, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(65)|shoot_speed(75)|thrust_damage(90,pierce)|max_ammo(1)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot13"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["ccc_rifle_blunderbuss_a", "Long Blunderbuss", [("rifle_blunderbuss_a",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 7500, weight(3.5)|abundance(90)|difficulty(0)|spd_rtng(77)|shoot_speed(80)|thrust_damage(128,pierce)|max_ammo(1)|accuracy(45), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot3"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["ccc_rifle_blunderbuss_b", "Blunderbuss", [("rifle_blunderbuss_b",0)], itp_type_musket|itp_two_handed|itp_primary, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(80)|shoot_speed(80)|thrust_damage(93,pierce)|max_ammo(1)|accuracy(35), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot3"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],

["ccc_rifle_sniper", "Sniper Rifle", [("rifle_sniper",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_cant_use_on_horseback|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 9000, weight(4.0)|abundance(90)|difficulty(0)|spd_rtng(45)|shoot_speed(190)|thrust_damage(107,pierce)|max_ammo(1)|accuracy(99), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot8"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_dark_sniper", "Dark Sniper Rifle", [("Gewehr98",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_crush_through, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 15000, weight(2.0)|abundance(90)|difficulty(0)|spd_rtng(35)|shoot_speed(200)|thrust_damage(117,pierce)|max_ammo(1)|accuracy(99), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot8"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccd_rifle_sniper_scope", "Sniper Rifle with Scope", [("mk12_spr",0)], itp_type_musket|itp_two_handed|itp_merchandise|itp_primary|itp_crush_through|itp_cant_reload_on_horseback|itp_cant_use_on_horseback|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 8192, weight(4.5)|abundance(5)|difficulty(0)|spd_rtng(40)|shoot_speed(250)|thrust_damage(110,pierce)|max_ammo(1)|accuracy(99), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot8"),(store_trigger_param_1, ":agent_id"),(try_begin),(is_presentation_active,"prsnt_ccd_gunsight"),(get_player_agent_no, ":player_agent"),(eq, ":agent_id", ":player_agent"),(mission_cam_get_position, pos5),(play_sound_at_position, "snd_shot8", pos5),(try_end),(call_script, "script_ccd_gun_particle", 1),])], [fac_player_supporters_faction] ],

#bayonet
["ccc_rifle_bayonet", "Bayonet", [("rifle_musketmel",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_next_item_as_melee|itp_crush_through|itp_can_knock_down|itp_has_bayonet|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket|itc_parry_polearm,
 4500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(55)|shoot_speed(120)|thrust_damage(87,pierce)|max_ammo(1)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_rifle_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_bayonet_mel", "Bayonet Melee", [("rifle_musketmel",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback, itcf_thrust_polearm|itcf_overswing_spear|itcf_carry_spear|itc_parry_polearm,
 4500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(95)|weapon_length(120)|thrust_damage(35,pierce), imodbits_crossbow ],
["ccc_rifle_bayonet2", "Bayonet", [("Russian_musket_1808",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_can_knock_down|itp_crush_through|itp_next_item_as_melee|itp_has_bayonet|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 4500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(55)|shoot_speed(120)|thrust_damage(92,pierce)|max_ammo(1)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_rifle_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_bayonet2_mel", "Bayonet Melle", [("Russian_musket_1808",0)], itp_type_polearm|itp_two_handed|itp_primary, itcf_thrust_polearm|itcf_overswing_spear|itcf_carry_spear|itc_parry_polearm, 1024, weight(3)|difficulty(0)|spd_rtng(85)|weapon_length(140)|swing_damage(32,pierce)|thrust_damage(32,pierce), imodbits_polearm ],
["ccc_rifle_bayonet3", "Bayonet", [("LeeEnfield_Bayonet",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback, itcf_thrust_polearm|itcf_overswing_spear|itcf_carry_spear|itc_parry_polearm,
 4500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(95)|weapon_length(120)|thrust_damage(35,pierce), imodbits_crossbow ],
["ccc_rifle_bayonet3_mel", "Bayonet Melee", [("LeeEnfield_Bayonet",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_primary, itc_musket_melee_ccd|itcf_overswing_polearm|itcf_carry_spear, 1024, weight(3)|difficulty(0)|spd_rtng(95)|weapon_length(110)|swing_damage(34,pierce)|thrust_damage(34,pierce), imodbits_polearm ],
["ccc_rifle_bayonet4", "Charleville", [("flintlock_big_with_bayonett",0)], itp_type_musket|itp_merchandise|itp_primary|itp_cant_use_on_horseback|itp_next_item_as_melee|itp_crush_through|itp_can_knock_down|itp_has_bayonet, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket|itc_parry_polearm,
 6500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(58)|shoot_speed(120)|thrust_damage(104,pierce)|max_ammo(1)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_bayonet4_mel", "Charleville Bayonet Melee", [("flintlock_big_with_bayonett",0)], itp_type_polearm|itp_two_handed|itp_unique|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback|itp_crush_through|itp_can_knock_down, itcf_thrust_polearm|itcf_carry_spear|itcf_overswing_spear|itc_parry_polearm,
 12000, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(94)|weapon_length(130)|thrust_damage(42,pierce)|swing_damage(42,pierce), imodbits_crossbow ],
["ccc_rifle_bayonet5", "Brown Bess", [("brown_bess_musket",0)], itp_type_musket|itp_merchandise|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_cant_reload_while_moving|itp_next_item_as_melee|itp_crush_through|itp_can_knock_down, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,  ## CC-D cut: 
 12000, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(70)|shoot_speed(120)|thrust_damage(102,pierce)|max_ammo(1)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_2] ],
["ccc_rifle_bayonet5_mel", "Brown Bess", [("brown_bess_musket",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback, itcf_thrust_polearm|itcf_carry_spear|itcf_overswing_spear|itc_parry_polearm,
 1024, weight(3.0)|difficulty(0)|spd_rtng(85)|weapon_length(135)|thrust_damage(36,pierce)|swing_damage(36,pierce), imodbits_crossbow ],
 #buffed Sister Bayonet occc
["ccc_rifle_bayonet6", "Sister Bayonet", [("Gewehr98_Bayonet",0)], itp_type_musket|itp_two_handed|itp_primary|itp_next_item_as_melee|itp_has_bayonet|itp_crush_through|itp_can_knock_down, itc_staff|itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 1024, weight(3.0)|difficulty(0)|spd_rtng(60)|shoot_speed(120)|thrust_damage(98,pierce)|max_ammo(1)|accuracy(92), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_rifle_shot"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_bayonet6_mel", "Sister Bayonet Melle", [("Gewehr98_Bayonet",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_primary, itc_musket_melee_ccd|itcf_carry_spear, 1024, weight(3)|difficulty(0)|spd_rtng(105)|weapon_length(120)|swing_damage(29,cut)|thrust_damage(24,pierce), imodbits_polearm ],

#shield-wepon
["ccc_dueling_dagger", "Dueling Dagger", [("dueldagger",0)], itp_type_shield, itcf_carry_sword_left_hip, 450, weight(1)|hit_points(620)|body_armor(1)|spd_rtng(150)|shield_width(10), imodbits_shield ],
#["ccd_kodachi_shield", "Kodachi Shield", [("kodachishield_y", 0)], itp_type_shield|itp_force_attach_left_hand, itcf_carry_dagger_front_left, 700, weight(2)|hit_points(400)|spd_rtng(140)|shield_width(10),imodbits_shield ],
["ccd_wakizashi_shield", "Wakizasi Shield", [("wakizashi_samurai10_shield",0),("wakizashi_samurai10_fourreau",ixmesh_carry)], itp_type_shield|itp_force_attach_left_hand, itcf_carry_wakizashi, 2048, weight(2)|hit_points(400)|body_armor(5)|spd_rtng(130)|shield_width(20),imodbits_shield ],
["ccd_torch_shield", "Torch Shield", [("club",0)], itp_type_shield|itp_wooden_parry|itp_force_attach_left_hand, 0, 11, weight(2.5)|hit_points(100)|spd_rtng(120)|shield_width(20), imodbits_shield, [(ti_on_init_item,[(set_position_delta,0,60,0),(particle_system_add_new,"psys_torch_fire"),(particle_system_add_new,"psys_torch_smoke"),(set_current_color,150,130,70),(add_point_light,10,30),])] ],

#shield
["wooden_shield", "Wooden Shield", [("shield_round_a",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 42, weight(4)|hit_points(80)|body_armor(4)|spd_rtng(100)|shield_width(50), imodbits_shield ],
["nordic_shield", "Nordic Shield", [("shield_round_b",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 95, weight(4)|hit_points(100)|body_armor(10)|spd_rtng(100)|shield_width(50), imodbits_shield ],
["fur_covered_shield", "Fur Covered Shield", [("shield_kite_m",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 227, weight(5.5)|hit_points(200)|body_armor(12)|leg_armor(3)|spd_rtng(76)|shield_width(81), imodbits_shield ],
["steel_shield", "Steel Shield", [("shield_dragon",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 697, weight(12)|hit_points(450)|body_armor(20)|spd_rtng(50)|shield_width(40), imodbits_shield ],
["plate_covered_round_shield", "Plate Covered Round Shield", [("shield_round_e",0)], itp_type_shield, itcf_carry_round_shield, 140, weight(10)|hit_points(420)|body_armor(23)|spd_rtng(58)|shield_width(40), imodbits_shield ],
["leather_covered_round_shield", "Leather Covered Round Shield", [("shield_round_d",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 80, weight(6.5)|hit_points(240)|body_armor(9)|spd_rtng(96)|shield_width(40), imodbits_shield ],
["hide_covered_round_shield", "Hide Covered Round Shield", [("shield_round_f",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 40, weight(5)|hit_points(200)|body_armor(4)|spd_rtng(100)|shield_width(40), imodbits_shield ],
["shield_heater_c", "Heater Shield", [("shield_heater_c",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 277, weight(4.5)|hit_points(240)|body_armor(4)|spd_rtng(80)|shield_width(50), imodbits_shield ],

["norman_shield_1", "Kite Shield", [("norman_shield_1",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 118, weight(4.5)|hit_points(240)|body_armor(12)|leg_armor(3)|spd_rtng(82)|shield_width(90), imodbits_shield ],
["norman_shield_2", "Kite Shield", [("norman_shield_2",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 100, weight(4.0)|hit_points(220)|body_armor(10)|leg_armor(2)|spd_rtng(88)|shield_width(90), imodbits_shield ],
["norman_shield_3", "Kite Shield", [("norman_shield_3",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 118, weight(4.5)|hit_points(240)|body_armor(12)|leg_armor(3)|spd_rtng(82)|shield_width(90), imodbits_shield ],
["norman_shield_4", "Kite Shield", [("norman_shield_4",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 121, weight(3.5)|hit_points(250)|body_armor(10)|leg_armor(3)|spd_rtng(86)|shield_width(90), imodbits_shield ],
["norman_shield_5", "Kite Shield", [("norman_shield_5",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 120, weight(4.5)|hit_points(240)|body_armor(13)|leg_armor(3)|spd_rtng(81)|shield_width(90), imodbits_shield ],
["norman_shield_6", "Kite Shield", [("norman_shield_6",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 130, weight(5.5)|hit_points(262)|body_armor(14)|leg_armor(3)|spd_rtng(80)|shield_width(90), imodbits_shield ],
["norman_shield_7", "Kite Shield", [("norman_shield_7",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 118, weight(4.5)|hit_points(240)|body_armor(12)|leg_armor(3)|spd_rtng(82)|shield_width(90), imodbits_shield ],
["norman_shield_8", "Kite Shield", [("norman_shield_8",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 118, weight(4.0)|hit_points(240)|body_armor(11)|leg_armor(3)|spd_rtng(84)|shield_width(90), imodbits_shield ],

["tab_shield_round_a", "Old Round Shield", [("tableau_shield_round_5",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 26, weight(3.5)|hit_points(60)|body_armor(6)|spd_rtng(93)|shield_width(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_round_shield_5",":agent_no",":troop_no")])] ],
["tab_shield_round_b", "Plain Round Shield", [("tableau_shield_round_3",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 65, weight(4)|hit_points(120)|body_armor(9)|spd_rtng(90)|shield_width(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_round_shield_3",":agent_no",":troop_no")])] ],
["tab_shield_round_c", "Round Shield", [("tableau_shield_round_2",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 105, weight(4.5)|hit_points(180)|body_armor(15)|spd_rtng(87)|shield_width(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_round_shield_2",":agent_no",":troop_no")])] ],
["tab_shield_round_d", "Heavy Round Shield", [("tableau_shield_round_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 210, weight(9)|hit_points(400)|body_armor(22)|spd_rtng(84)|shield_width(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_round_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_round_e", "Huscarl's Round Shield", [("tableau_shield_round_4",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 430, weight(8.5)|hit_points(480)|body_armor(25)|spd_rtng(81)|shield_width(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_round_shield_4",":agent_no",":troop_no")])] ],

["tab_shield_kite_a", "Old Kite Shield", [("tableau_shield_kite_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 33, weight(3)|hit_points(45)|body_armor(4)|leg_armor(2)|spd_rtng(75)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_kite_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_kite_b", "Plain Kite Shield", [("tableau_shield_kite_3",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 70, weight(3.5)|hit_points(105)|body_armor(6)|leg_armor(3)|spd_rtng(75)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_kite_shield_3",":agent_no",":troop_no")])] ],
["tab_shield_kite_c", "Kite Shield", [("tableau_shield_kite_2",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 156, weight(4)|hit_points(120)|body_armor(8)|leg_armor(4)|spd_rtng(80)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_kite_shield_2",":agent_no",":troop_no")])] ],
["tab_shield_kite_d", "Heavy Kite Shield", [("tableau_shield_kite_2",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 320, weight(4.5)|hit_points(260)|body_armor(10)|leg_armor(5)|spd_rtng(82)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_kite_shield_2",":agent_no",":troop_no")])] ],
["tab_shield_kite_cav_a", "Horseman's Kite Shield", [("tableau_shield_kite_4",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 205, weight(6)|hit_points(250)|body_armor(8)|leg_armor(6)|spd_rtng(103)|shield_width(30)|shield_height(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_kite_shield_4",":agent_no",":troop_no")])] ],
["tab_shield_kite_cav_b", "Knightly Kite Shield", [("tableau_shield_kite_4",0)], itp_type_shield|itp_merchandise, itcf_carry_kite_shield, 360, weight(7.5)|hit_points(320)|body_armor(13)|leg_armor(10)|spd_rtng(100)|shield_width(30)|shield_height(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_kite_shield_4",":agent_no",":troop_no")])] ],

["tab_shield_heater_a", "Old Heater Shield", [("tableau_shield_heater_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 36, weight(4)|hit_points(55)|body_armor(5)|leg_armor(2)|spd_rtng(96)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heater_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_heater_b", "Plain Heater Shield", [("tableau_shield_heater_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 74, weight(4)|hit_points(110)|body_armor(5)|leg_armor(3)|spd_rtng(93)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heater_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_heater_c", "Heater Shield", [("tableau_shield_heater_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 160, weight(4)|hit_points(120)|body_armor(9)|leg_armor(3)|spd_rtng(90)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heater_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_heater_d", "Heavy Heater Shield", [("tableau_shield_heater_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 332, weight(4)|hit_points(150)|body_armor(12)|leg_armor(7)|spd_rtng(87)|shield_width(36)|shield_height(70), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heater_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_heater_cav_a", "Horseman's Heater Shield", [("tableau_shield_heater_2",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 229, weight(8)|hit_points(190)|body_armor(17)|spd_rtng(103)|shield_width(30)|shield_height(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heater_shield_2",":agent_no",":troop_no")])] ],
["tab_shield_heater_cav_b", "Knightly Heater Shield", [("tableau_shield_heater_2",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_kite_shield, 390, weight(2.5)|hit_points(280)|body_armor(21)|spd_rtng(100)|shield_width(30)|shield_height(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heater_shield_2",":agent_no",":troop_no")])] ],

["tab_shield_pavise_a", "Old Pavise", [("tableau_shield_pavise_2",0)], itp_type_shield|itp_merchandise|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 60, weight(5.5)|hit_points(140)|body_armor(8)|leg_armor(8)|spd_rtng(89)|shield_width(43)|shield_height(100), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_pavise_shield_2",":agent_no",":troop_no")])] ],
["tab_shield_pavise_b", "Plain Pavise", [("tableau_shield_pavise_2",0)], itp_type_shield|itp_merchandise|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 114, weight(6)|hit_points(240)|body_armor(10)|leg_armor(10)|spd_rtng(85)|shield_width(43)|shield_height(100), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_pavise_shield_2",":agent_no",":troop_no")])] ],
["tab_shield_pavise_c", "Pavise", [("tableau_shield_pavise_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 210, weight(7.5)|hit_points(360)|body_armor(14)|leg_armor(14)|spd_rtng(81)|shield_width(43)|shield_height(100), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_pavise_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_pavise_d", "Heavy Pavise", [("tableau_shield_pavise_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 370, weight(8)|hit_points(460)|body_armor(18)|leg_armor(18)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_pavise_shield_1",":agent_no",":troop_no")])] ],
["pavise", "Deployable Pavise", [("pavise_wep",0)], itp_type_shield|itp_merchandise|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 400, weight(13.5)|hit_points(520)|body_armor(20)|leg_armor(20)|spd_rtng(60)|shield_width(57)|shield_height(132), imodbits_shield ],

["tab_shield_small_round_a", "Plain Cavalry Shield", [("tableau_shield_small_round_3",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 96, weight(4)|hit_points(120)|body_armor(12)|spd_rtng(105)|shield_width(40), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_small_round_shield_3",":agent_no",":troop_no")])] ],
["tab_shield_small_round_b", "Round Cavalry Shield", [("tableau_shield_small_round_1",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 195, weight(4.5)|hit_points(160)|body_armor(15)|spd_rtng(103)|shield_width(40), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_small_round_shield_1",":agent_no",":troop_no")])] ],
["tab_shield_small_round_c", "Elite Cavalry Shield", [("tableau_shield_small_round_2",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 370, weight(5)|hit_points(180)|body_armor(20)|spd_rtng(100)|shield_width(40), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_small_round_shield_2",":agent_no",":troop_no")])] ],

["ccc_shield_spak4", "Imperial Shield", [("shield_imperial",0)], itp_type_shield, itcf_carry_round_shield, 500, weight(7.5)|hit_points(380)|body_armor(14)|spd_rtng(88)|shield_width(40), imodbits_shield ],
["ccc_shield_hermitage_shield_1", "Hermitage Shield", [("hermitage_shield_1",0)], itp_type_shield, itcf_carry_round_shield, 500, weight(9.5)|hit_points(410)|body_armor(18)|spd_rtng(81)|shield_width(40), imodbits_shield ],
["ccc_shield_hermitage_shield_2", "Asmoday Shield", [("asmoday_seel",0)], itp_type_shield, itcf_carry_round_shield, 600, weight(9.5)|hit_points(410)|body_armor(19)|spd_rtng(81)|shield_width(40), imodbits_shield ],
["ccc_shield_rune_shield", "Rune Shield", [("alt_sh_run",0)], itp_merchandise|itp_type_shield, itcf_carry_round_shield, 500, abundance(500)|weight(3.5)|hit_points(410)|body_armor(19)|spd_rtng(81)|shield_width(40), imodbits_shield,[],[fac_valkyrie] ],
["ccc_shield_bear_shield", "Bear Shield", [("sh_oval",0)], itp_type_shield, itcf_carry_round_shield, 370, weight(1.5)|hit_points(320)|body_armor(12)|spd_rtng(95)|shield_width(40)|shield_height(50), imodbits_shield ],
["ccc_shield_bk_shield", "Black Knight Shield", [("sp_shr1",0)], itp_type_shield, itcf_carry_round_shield, 440, weight(3.5)|hit_points(410)|body_armor(19)|spd_rtng(81)|shield_width(50), imodbits_shield ],
["ccc_shield_death_shield", "Death Shield", [("shield_round_s3",0)], itp_type_shield, itcf_carry_round_shield, 440, weight(3.5)|hit_points(430)|body_armor(19)|spd_rtng(91)|shield_width(40), imodbits_shield ],
["ccc_shield_heater2", "Heater Shield", [("runico_shield2",0)], itp_type_shield, itcf_carry_kite_shield, 332, weight(5.5)|hit_points(210)|body_armor(8)|leg_armor(1)|spd_rtng(102)|shield_width(60)|shield_height(80), imodbits_shield ],
["ccc_shield_heater4", "Elven Shield", [("runico_shield4",0)], itp_type_shield|itp_wooden_parry,
 itcf_carry_kite_shield, 252, weight(4.5)|hit_points(480)|body_armor(16)|leg_armor(2)|spd_rtng(102)|shield_width(50)|shield_height(70), imodbits_shield ],
["ccc_shield_heater5", "Knight Shield", [("runico_shield5",0)], itp_type_shield, itcf_carry_kite_shield, 332, weight(5.5)|hit_points(280)|body_armor(12)|leg_armor(2)|spd_rtng(102)|shield_width(30)|shield_height(50), imodbits_shield ],
["ccc_shield_arthas_shield", "Arthas Shield", [("ArthasShield",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 500, weight(8)|hit_points(500)|body_armor(18)|spd_rtng(88)|shield_width(50)|shield_height(70), imodbits_shield ],
["ccc_shield_bk_shield_1", "Snake Shield", [("sh_snake",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 500, weight(2)|hit_points(500)|body_armor(18)|spd_rtng(88)|shield_width(40)|shield_height(50), imodbits_shield ],
["ccc_shield_bk_shield_2", "Black Knight Shield", [("sp_newsh",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 500, weight(2)|hit_points(500)|body_armor(18)|spd_rtng(88)|shield_width(40)|shield_height(50), imodbits_shield ],
["ccc_shield_heater6", "King Shield", [("runico_shield6",0)], itp_type_shield, itcf_carry_kite_shield, 5024, weight(7.5)|hit_points(450)|body_armor(26)|spd_rtng(80)|shield_width(60)|shield_height(80), imodbits_shield ],
["ccc_shield_steel_heater1", "Steel Heater", [("steel_heater1",0)], itp_type_shield|itp_merchandise, itcf_carry_kite_shield, 3024, weight(9)|hit_points(320)|body_armor(21)|spd_rtng(91)|shield_width(30)|shield_height(50), imodbits_shield ],
["ccc_shield_steel_heater1_b", "Steel Heater", [("steel_heater1_b",0)], itp_type_shield|itp_merchandise, itcf_carry_kite_shield, 3024, weight(9)|hit_points(320)|body_armor(21)|spd_rtng(91)|shield_width(30)|shield_height(50), imodbits_shield ],
["ccc_shield_steel_kite1", "Steel Kite Shield", [("steel_kite1",0)], itp_type_shield, itcf_carry_kite_shield, 3024, weight(10)|hit_points(320)|body_armor(21)|spd_rtng(92)|shield_width(30)|shield_height(50), imodbits_shield ],
#scutum buffed overall hp +20 occc
["occc_shield_roma_roundscutum", "Round Scutum", [("roundscutum",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 120, weight(1)|hit_points(150)|body_armor(1)|spd_rtng(104)|shield_width(38)|shield_height(38), imodbits_shield ],
["ccc_shield_roma_smallscutum", "Small Scutum", [("smallscutum",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 300, weight(2)|hit_points(250)|body_armor(1)|spd_rtng(98)|shield_width(35)|shield_height(70), imodbits_shield ],
["ccc_shield_roma_scutum", "Scutum", [("scutum",0)], itp_type_shield|itp_cant_use_on_horseback, itcf_carry_board_shield, 550, weight(12)|hit_points(420)|body_armor(25)|leg_armor(25)|spd_rtng(81)|shield_width(65)|shield_height(120), imodbits_shield ],#Prox best shield in this mod
["ccc_shield_roma_clipeus", "Clipeus", [("clipeus",0)], itp_type_shield, itcf_carry_board_shield, 500, weight(8)|hit_points(380)|body_armor(18)|leg_armor(12)|spd_rtng(88)|shield_width(43)|shield_height(110), imodbits_shield ],
["ccc_shield_roma_hexscutum", "Hex Scutum", [("hexscutum",0)], itp_type_shield|itp_wooden_parry|itp_cant_reload_on_horseback|itp_cant_use_on_horseback, itcf_carry_board_shield, 500, weight(5)|hit_points(440)|body_armor(12)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield ],
["ccc_shield_roma_bodyscutum", "Body Scutum", [("bodyscutum",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 500, weight(5)|hit_points(440)|body_armor(12)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield ],
["ccc_shield_roma_ovalscutum", "Oval Scutum", [("ovalscutum",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 500, weight(5)|hit_points(440)|body_armor(12)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield ],
#occc end
["ccc_shield_celt_shield", "Highlander Shield", [("s_h2_1",0)], itp_type_shield|itp_wooden_parry, itcf_carry_board_shield, 300, weight(4)|hit_points(180)|body_armor(9)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield ],
["ccc_shield_tri_shield", "Rosetta Shield", [("s_h2",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 300, weight(4)|hit_points(180)|body_armor(9)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield ],
["ccc_shield_corn_shield", "Highlander Horned Shield", [("s_h1",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 300, weight(5)|hit_points(240)|body_armor(11)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield ],
["ccc_shield_board1", "Board Shield", [("foot_shield",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 300, weight(5)|hit_points(550)|body_armor(8)|spd_rtng(88)|shield_width(43)|shield_height(100), imodbits_shield ],
["ccc_shield_board2", "Board Shield", [("oval_face",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 300, weight(5)|hit_points(550)|body_armor(8)|leg_armor(7)|spd_rtng(88)|shield_width(43)|shield_height(100), imodbits_shield ],  ## cave09 del
["ccc_shield_board3", "Board Shield", [("oval_shield01",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 300, weight(5)|hit_points(550)|body_armor(8)|leg_armor(7)|spd_rtng(88)|shield_width(43)|shield_height(100), imodbits_shield ],  ## cave09 del
#["ccc_shield_board4", "Board Shield", [("oval_shield02",0)], itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_board_shield, 1024, weight(5)|hit_points(550)|body_armor(10)|leg_armor(7)|spd_rtng(88)|shield_width(43)|shield_height(100), imodbits_shield ],  ## cave09 del

#cloth armor
#Cloth
["lady_dress_ruby", "Lady Dress", [("lady_dress_r",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["lady_dress_green", "Lady Dress", [("lady_dress_g",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["lady_dress_blue", "Lady Dress", [("lady_dress_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["red_dress", "Red Dress", [("red_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["brown_dress", "Brown Dress", [("brown_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["green_dress", "Green Dress", [("green_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["khergit_lady_dress", "Khergit Lady Dress", [("khergit_lady_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["khergit_lady_dress_b", "Khergit Leather Lady Dress", [("khergit_lady_dress_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["sarranid_lady_dress", "Sarranid Lady Dress", [("sarranid_lady_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["sarranid_lady_dress_b", "Sarranid Lady Dress", [("sarranid_lady_dress_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["sarranid_common_dress", "Sarranid Dress", [("sarranid_common_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["sarranid_common_dress_b", "Sarranid Dress", [("sarranid_common_dress_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 500, weight(3)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["dress", "Dress", [("dress",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 6, weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["blue_dress", "Blue Dress", [("blue_dress_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 6, weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["peasant_dress", "Peasant Dress", [("peasant_dress_b_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 6, weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["sarranid_dress_a", "Dress", [("woolen_dress",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 33, weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["sarranid_dress_b", "Dress", [("woolen_dress",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 33, weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["woolen_dress", "Woolen Dress", [("woolen_dress",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 10, weight(1.75)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["courtly_outfit", "Courtly Outfit", [("nobleman_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 348, weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["nobleman_outfit", "Nobleman Outfit", [("nobleman_outfit_b_new",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 348, weight(4)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["court_dress", "Court Dress", [("court_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 348, weight(4)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(4)|difficulty(0), imodbits_cloth ],
["rich_outfit", "Rich Outfit", [("merchant_outf",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 348, weight(4)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(4)|difficulty(0), imodbits_cloth ],
["sarranid_cloth_robe", "Worn Robe", [("sar_robe",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 33, weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["sarranid_cloth_robe_b", "Worn Robe", [("sar_robe_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 33, weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["ccd_linen_dress", "Linen Dress", [("linen_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 512, weight(2)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ccd_plaid_dress", "Plaid Dress", [("plaid_dress",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 512, weight(2)|head_armor(0)|body_armor(10)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ccd_kakyu_kunoichi_syozoku_1", "Kakyu Kunoichi Syozoku", [("kunorobe1", 0)], itp_civilian|itp_type_body_armor|itp_merchandise |itp_covers_legs, 0, 300, weight(2)|head_armor(0)|body_armor(26)|leg_armor(5)|difficulty(0), imodbits_armor, [],[fac_kingdom_9,fac_bushido_order]  ],

["shirt", "Shirt", [("shirt",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 3, weight(1)|abundance(100)|head_armor(0)|body_armor(5)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["linen_tunic", "Linen Tunic", [("shirt_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 6, weight(1)|abundance(100)|head_armor(0)|body_armor(6)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["short_tunic", "Red Tunic", [("rich_tunic_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 10, weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["red_shirt", "Red Shirt", [("rich_tunic_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 10, weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["red_tunic", "Red Tunic", [("arena_tunicR_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 10, weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["green_tunic", "Green Tunic", [("arena_tunicG_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 10, weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["blue_tunic", "Blue Tunic", [("arena_tunicB_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 10, weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["robe", "Robe", [("robe",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 31, weight(1.5)|abundance(100)|head_armor(0)|body_armor(8)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["nomad_robe", "Nomad Robe", [("nomad_robe_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 610, weight(15)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["coarse_tunic", "Tunic with vest", [("coarse_tunic_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 47, weight(2)|abundance(100)|head_armor(0)|body_armor(11)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["tabard", "Tabard", [("tabard_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 107, weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["skirmisher_armor", "Skirmisher Armor", [("skirmisher_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 74, weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(9)|difficulty(0), imodbits_cloth ],

#Hide, Fur
["rawhide_coat", "Rawhide Coat", [("coat_of_plates_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 12, weight(5)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["fur_coat", "Fur Coat", [("fur_coat",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 117, weight(6)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(6)|difficulty(0), imodbits_armor ],
["pelt_coat", "Pelt Coat", [("thick_coat_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 14, weight(2)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["nomad_armor", "Nomad Armor", [("nomad_armor_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 25, weight(2)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["khergit_armor", "Khergit Armor", [("khergit_armor_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 38, weight(2)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["steppe_armor", "Steppe Armor", [("lamellar_leather",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 195, weight(5)|abundance(100)|head_armor(0)|body_armor(16)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["nomad_vest", "Nomad Vest", [("nomad_vest_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 360, weight(7)|abundance(50)|head_armor(0)|body_armor(22)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["tribal_warrior_outfit", "Tribal Warrior Outfit", [("tribal_warrior_outfit_a_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 520, weight(14)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0), imodbits_cloth ],

#Leather
["light_leather", "Light Leather", [("light_leather",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 352, weight(5)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(7)|difficulty(0), imodbits_armor ],
["leather_apron", "Leather Apron", [("leather_apron",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 61, weight(3)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["leather_jacket", "Leather Jacket", [("leather_jacket_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 50, weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["leather_vest", "Leather Vest", [("leather_vest_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 146, weight(4)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["leather_armor", "Leather Armor", [("tattered_leather_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 65, weight(7)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["leather_jerkin", "Leather Jerkin", [("ragged_leather_jerkin",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 321, weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["ragged_outfit", "Ragged Outfit", [("ragged_outfit_a_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 390, weight(7)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["archers_vest", "Archer's Padded Vest", [("archers_vest",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 260, weight(6)|abundance(100)|head_armor(0)|body_armor(23)|leg_armor(12)|difficulty(0), imodbits_cloth ],

#Padded Cloth
["gambeson", "Gambeson", [("white_gambeson",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 260, weight(5)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["blue_gambeson", "Blue Gambeson", [("blue_gambeson",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 270, weight(5)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["red_gambeson", "Red Gambeson", [("red_gambeson_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 275, weight(5)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["padded_cloth", "Aketon", [("padded_cloth_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 297, weight(11)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["aketon_green", "Padded Cloth", [("padded_cloth_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 297, weight(11)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(6)|difficulty(0), imodbits_cloth ],

#Padded Leather
["padded_leather", "Padded Leather", [("leather_armor_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 454, weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["sarranid_leather_armor", "Sarranid Leather Armor", [("sarranid_leather_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 650, weight(9)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_armor ],

#["ccc_tunic_blueapron", "Tunic", [("cloth_bur_074",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 130, weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0), imodbits_cloth ],  ## cave09 del
#["ccc_tunic_redapron", "Tunic", [("cloth_orn_104",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 130, weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0), imodbits_cloth ],  ## cave09 del
#["ccc_tunic_bandit", "Bandit Tunic", [("cloth_bur_103",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0), imodbits_cloth ],  ## cave09 del
["ccc_celttish_tunic", "Highlander Tunic", [("celtB",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 160, weight(3)|abundance(100)|head_armor(0)|body_armor(17)|leg_armor(8)|difficulty(0), imodbits_cloth ],
#["ccc_tunic_blueheraldry", "Tunic", [("cloth_orn_232",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 130, weight(3)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(6)|difficulty(0), imodbits_cloth ],  ## cave09 del

#OSP Clothing Vests
["ccc_vest_open_a", "Open Vest", [("vest_open_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 280, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["ccc_vest_open_b", "Open Vest", [("vest_open_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 280, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
#["ccc_vest_open_c", "Open Vest", [("vest_open_c",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],  ## cave09 del
#["ccc_vest_closed_a", "Closed Vest", [("vest_closed_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
#["ccc_vest_closed_b", "Closed Vest", [("vest_closed_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
#["ccc_vest_closed_c", "Closed Vest", [("vest_closed_c",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],  ## cave09 del
["ncm_ccc_celt_armor", "Highlander Aromor", [("celtC",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 280, weight(10)|abundance(50)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["ncm_ccc_vest_closed_b", "Mountainer Shirt", [("a_h1",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 170, weight(2)|abundance(50)|head_armor(0)|body_armor(24)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ncm_ccc_vest_closed_c", "Forrester Shirt", [("a_h1_1",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 170, weight(1.8)|abundance(50)|head_armor(0)|body_armor(22)|leg_armor(8)|difficulty(0), imodbits_cloth ],

#OSP Clothing Jackets
["ccc_jacket_open_a", "Open Jacket", [("jacket_open_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(1), imodbits_cloth ],
#["ccc_jacket_open_b", "Open Jacket", [("jacket_open_b",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
#["ccc_jacket_open_c", "Open Jacket", [("jacket_open_c",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],  ## cave09 del
#["ccc_jacket_closed_a", "Closed Jacket", [("jacket_closed_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
#["ccc_jacket_closed_b", "Closed Jacket", [("jacket_closed_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
#["ccc_jacket_closed_c", "Closed Jacket", [("jacket_closed_c",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 700, weight(2)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],  ## cave09 del
["ccd_business_suit", "Business Suit", [("business_suit_a",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 5000, weight(2)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ncm_ccc_jacket_open_a", "Mountainer Armor", [("a_h2",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 170, weight(4)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(1), imodbits_cloth ],
["ncm_ccc_jacket_open_b", "Forrester Armor", [("a_h2_1",0)], itp_type_body_armor|itp_covers_legs, 0, 170, weight(4)|abundance(50)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["ncm_ccc_jacket_open_c", "Mountainer Heavy Aromor", [("a_h3",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 280, weight(6)|abundance(50)|head_armor(0)|body_armor(32)|leg_armor(14)|difficulty(0), imodbits_cloth ],
["ncm_ccc_jacket_closed_a", "Forrester Heavy Aromor", [("a_h3_1",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 350, weight(8)|abundance(50)|head_armor(0)|body_armor(38)|leg_armor(16)|difficulty(0), imodbits_cloth ],
["ncm_ccc_jacket_closed_b", "Mountainer Cloth", [("a_h4",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 170, weight(1.5)|abundance(50)|head_armor(0)|body_armor(16)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["ncm_ccc_jacket_closed_c", "Forrester Cloth", [("a_h4_1",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 170, weight(2)|abundance(50)|head_armor(0)|body_armor(16)|leg_armor(4)|difficulty(0), imodbits_cloth ],

["ccc_robe_gandalf", "Gandalf Robe", [("sar_robe_b",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(12)|difficulty(0), imodbits_armor ],
#["ccc_cloth_jp_costume_japonais01", "Heifuku", [("costume_japonais01",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(19)|abundance(20)|head_armor(0)|body_armor(26)|leg_armor(5)|difficulty(7), imodbits_cloth ],  ## cave09 del
["ccc_cloth_demonrobe", "Dark Robe", [("demonrobe",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(2)|abundance(85)|head_armor(0)|body_armor(35)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["ccd_cloth_demonrobe_armor", "Dark Robe Armor", [("demonrobe_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 1536, weight(4.5)|abundance(75)|head_armor(0)|body_armor(43)|leg_armor(15)|difficulty(0), imodbits_cloth ],
["ccd_cloth_shadowrobe", "Shadow Robe", [("ccd_shadowrobe",0)], itp_type_body_armor|itp_covers_legs, 0, 4096, weight(4)|head_armor(4)|body_armor(46)|leg_armor(14)|difficulty(18), imodbits_cloth ],

["ccc_uniform_blue", "Uniform Blue", [("nordinf",0)], itp_type_body_armor|itp_covers_legs, 0, 180, weight(6)|abundance(100)|head_armor(0)|body_armor(17)|leg_armor(14)|difficulty(0), imodbits_cloth ],
["ccc_uniform_blue_belt", "Uniform Blue", [("nordoff",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(6)|abundance(100)|head_armor(0)|body_armor(21)|leg_armor(18)|difficulty(0), imodbits_cloth ],
["ccc_uniform_yellow", "Uniform Yellow", [("rhoinf",0)], itp_type_body_armor|itp_covers_legs, 0, 180, weight(6)|abundance(100)|head_armor(0)|body_armor(17)|leg_armor(15)|difficulty(0), imodbits_cloth ],
["ccc_uniform_yellow_belt", "Uniform Yellow", [("rhodoff",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(6)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(25)|difficulty(0), imodbits_cloth ],
["ccc_uniform_white", "Uniform White", [("swadinf",0)], itp_type_body_armor|itp_covers_legs, 0, 180, weight(6)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(16)|difficulty(0), imodbits_cloth ],
["ccc_uniform_white_belt", "Uniform White", [("swadoff",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(6)|abundance(100)|head_armor(0)|body_armor(25)|leg_armor(22)|difficulty(0), imodbits_cloth ],
["ccc_uniform_green", "Uniform Green", [("vaeinf",0)], itp_type_body_armor|itp_covers_legs, 0, 180, weight(5)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ccc_uniform_green_belt", "Uniform Green", [("vaeoff",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(5)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["ccc_uniform_red", "Red Coat", [("red_coat_inf",0)], itp_type_body_armor|itp_covers_legs, 0, 180, weight(6)|abundance(100)|head_armor(0)|body_armor(19)|leg_armor(16)|difficulty(0), imodbits_cloth ],
["ccc_uniform_red_belt", "Red Coat", [("red_coat_ff",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(6)|abundance(100)|head_armor(0)|body_armor(20)|leg_armor(17)|difficulty(0), imodbits_cloth ],
["ccd_uniform_red_cuirassier", "Red Coat with Cuirass", [("red_cuirassier",0)], itp_type_body_armor|itp_covers_legs, 0, 1536, weight(14)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(14)|difficulty(0), imodbits_cloth ],

#JP
["ccc_jp_sinobi_kunobeni", "Beni Kunoiti robe", [("kunorobe2",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 300, weight(12)|abundance(200)|head_armor(0)|body_armor(28)|leg_armor(10)|difficulty(0), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
#["ccc_jp_sinobi_kunokuro", "Kuro Kunoiti robe", [("kunorobe_c3",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 400, weight(12)|abundance(200)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["ccc_jp_miko", "Miko robe", [("mikosyouzoku",0)], itp_type_body_armor|itp_covers_legs, 0, 500, weight(5)|abundance(100)|head_armor(5)|body_armor(30)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ccc_jp_sinobi_robe1", "Sinobi robe", [("kunorobeb2",0)], itp_type_body_armor|itp_covers_legs, 0, 600, weight(12)|abundance(100)|head_armor(0)|body_armor(31)|leg_armor(10)|difficulty(0), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["ccc_jp_sinobi_robe2", "Sinobi robe", [("ninja_robe2",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(13)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(15)|difficulty(0), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["ccd_hakama_blue", "Hakama", [("hakama_blue",0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 512 , weight(2)|abundance(100)|head_armor(0)|body_armor(17)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["ccd_komusou_houi", "Komusou Houi", [("komusou_houi",0)], itp_type_body_armor|itp_covers_legs|itp_civilian ,0, 768 , weight(2.5)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(11)|difficulty(0) ,imodbits_cloth ],

#armor
#woman

#Mail
["mail_with_tunic_red", "Mail with Tunic", [("arena_armorR_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(8), imodbits_armor ],
["mail_with_tunic_green", "Mail with Tunic", [("arena_armorG_new",0)], itp_type_body_armor  |itp_covers_legs ,0, 650 , weight(16)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(8), imodbits_armor ],
["byrnie", "Byrnie", [("byrnie_a_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 795, weight(17)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(6)|difficulty(7), imodbits_armor ],
["studded_leather_coat", "Studded Leather Coat", [("leather_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 690, weight(14)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(10)|difficulty(7), imodbits_armor ],
["mail_shirt", "Mail Shirt", [("mail_shirt_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1040, weight(19)|abundance(100)|head_armor(0)|body_armor(37)|leg_armor(12)|difficulty(7), imodbits_armor ],
["sarranid_cavalry_robe", "Cavalry Robe", [("arabian_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 990, weight(5)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(8)|difficulty(0), imodbits_armor ],
["sarranid_mail_shirt", "Sarranid Mail Shirt", [("sarranian_mail_shirt",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(14)|difficulty(7), imodbits_armor ],
["mail_hauberk", "Mail Hauberk", [("hauberk_a_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1320, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],
["haubergeon", "Haubergeon", [("haubergeon_c",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 863, weight(18)|abundance(100)|head_armor(0)|body_armor(41)|leg_armor(6)|difficulty(6), imodbits_armor ],
["mail_with_surcoat", "Mail with Surcoat", [("mail_long_surcoat_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1544, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(14)|difficulty(7), imodbits_armor ],
["surcoat_over_mail", "Surcoat over Mail", [("surcoat_over_mail_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1720, weight(22)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(14)|difficulty(7), imodbits_armor ],
["brigandine_red", "Brigandine", [("brigandine_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1830, weight(19)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(0), imodbits_armor ],
["banded_armor", "Banded Armor", [("banded_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2710, weight(23)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(14)|difficulty(8), imodbits_armor ],
["cuir_bouilli", "Cuir Bouilli", [("cuir_bouilli_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3100, weight(24)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(15)|difficulty(8), imodbits_armor ],
["heraldic_mail_with_surcoat", "Heraldic Mail with Surcoat", [("heraldic_armor_new_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3454, weight(22)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(17)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heraldic_armor_a",":agent_no",":troop_no")])] ],
["heraldic_mail_with_tunic", "Heraldic Mail", [("heraldic_armor_new_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3520, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(16)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heraldic_armor_b",":agent_no",":troop_no")])] ],
["heraldic_mail_with_tunic_b", "Heraldic Mail", [("heraldic_armor_new_c",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3610, weight(22)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heraldic_armor_c",":agent_no",":troop_no")])] ],
["heraldic_mail_with_tabard", "Heraldic Mail with Tabard", [("heraldic_armor_new_d",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3654, weight(21)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heraldic_armor_d",":agent_no",":troop_no")])] ],
#occc additional heraldic mail
["occc_long_surcoat_new_heraldic", "Heraldic Surcoat over Mail", [("mail_long_surcoat_new_heraldic",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1720, weight(22)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(14)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_long_surcoat_new_heraldic",":agent_no",":troop_no")])] ],#
["occc_heraldic_brigandine", "Heraldic Brigandine", [("brigandine_b_heraldic",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1830, weight(19)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(0), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_brigandine_b_heraldic",":agent_no",":troop_no")])] ],
["occc_heraldic_tunic_new", "Heraldic Mail", [("heraldic_tunic_new",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3520, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(16)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heraldic_tunic_new",":agent_no",":troop_no")])] ],
["occc_heraldic_surcoat_over_mail", "Heraldic Surcoat over Mail", [("heraldic_surcoat_over_mail_short",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1720, weight(22)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(14)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_surcoat_over_mail_short",":agent_no",":troop_no")])]  ],
["occc_heraldic_mail_with_tabard_b", "Heraldic Mail with Tabard", [("tabard_b_heraldic",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3654, weight(21)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(7), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_tabard_b_heraldic",":agent_no",":troop_no")])] ],

#Scale
["scale_armor", "Scale Armor", [("lamellar_armor_e",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2558, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(13)|difficulty(8), imodbits_armor ],
#Lamellar
#["lamellar_cuirass", "Lamellar Cuirass", [("lamellar_armor",0)], itp_type_body_armor  |itp_covers_legs,0, 1020 , weight(25)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(15)|difficulty(9) ,imodbits_armor ],
["arabian_armor_b", "Sarranid Guard Armor", [("arabian_armor_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1200, weight(5)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(8)|difficulty(0), imodbits_armor ],
["lamellar_vest", "Lamellar Vest", [("lamellar_vest_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 970, weight(18)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(7), imodbits_cloth ],
["lamellar_vest_khergit", "Khergit Lamellar Vest", [("lamellar_vest_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 970, weight(18)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(7), imodbits_cloth ],
["lamellar_armor", "Lamellar Armor", [("lamellar_armor_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2410, weight(25)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(0), imodbits_armor ],
["mamluke_mail", "Mamluke Mail", [("sarranid_elite_cavalary",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 2900, weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(8), imodbits_armor ],
["khergit_elite_armor", "Khergit Elite Armor", [("lamellar_armor_d",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3828, weight(20)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(16)|difficulty(8), imodbits_armor ],
["vaegir_elite_armor", "Vaegir Elite Armor", [("lamellar_armor_c",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3828, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8), imodbits_armor ],
["sarranid_elite_armor", "Sarranid Elite Armor", [("tunic_armor_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 3828, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8), imodbits_armor ],

["ccc_mail_yellowleg", "Sarranid Lamellar Mail", [("wei_xiadi_lamellar_armor02",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1800, weight(23)|abundance(40)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(7), imodbits_armor ],  ## cave09 del
#occc["ccc_mail_banditsurcoat", "Mail Hauberk", [("maille_bur_101",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(23)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#occc["ccc_mail_banditapron", "Mail Hauberk", [("maille_bur_104",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
["ccc_roman_scout", "Roman Scout Armor", [("Roman_standard_bearer",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(43)|leg_armor(12)|difficulty(7), imodbits_armor ],
#["ccc_mail_yellowchestplaid", "Mail Hauberk", [("maille_com_014",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#occc["ccc_mail_bluesleeves", "Mail Hauberk", [("maille_mtw_042",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#occc["ccc_mail_bluefull", "Mail Hauberk", [("maille_mtw_121",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_greenwhite", "Mail Hauberk", [("maille_mtw_164",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_redherald", "Mail Hauberk with Surcoat", [("maille_orn_111",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(24)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(13)|difficulty(7), imodbits_armor ],  ## cave09 del
["ccc_mail_sunherald", "Infantry Armor", [("armor_infantry_tripoli_a",0)], itp_type_body_armor|itp_covers_legs, 0, 370, weight(11)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
["ccc_mail_redorangelion", "Infantry Armor", [("armor_infantry_tripoli_b",0)], itp_type_body_armor|itp_covers_legs, 0, 370, weight(11)|abundance(100)|head_armor(0)|body_armor(28)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
["ccc_mail_redlionherald", "Sergeant Mail", [("sergeant_armor_tripoli_a",0)], itp_type_body_armor|itp_covers_legs, 0, 650, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_bronzechest", "Mail Hauberk", [("maille_orn_144",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_redwhitesurcoat", "Mail Hauberk with Surcoat", [("maille_orn_151",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_greychestlion", "Mail Hauberk", [("maille_orn_152",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_yellowsurcoat", "Mail Hauberk with Surcoat", [("maille_orn_221",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(13)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_bluecoat", "Mail Hauberk", [("maille_orn_223",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_bluewhitestripe", "Mail Hauberk", [("maille_orn_224",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
["ccc_mail_fullchain", "Mail Hauberk", [("hauberk2",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
["ccc_mail_fullchain_caped", "Caped Mail Hauberk", [("hauberk2_cape",0)], itp_type_body_armor|itp_covers_legs, 0, 1550, weight(21)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(15)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_bluelion", "Mail Hauberk", [("maille_orn_233",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
#["ccc_mail_bluerose", "Mail Hauberk", [("maille_orn_234",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(19)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(12)|difficulty(7), imodbits_armor ],  ## cave09 del
["ccd_sabe_mail", "Platinum Cuirass", [("sabe_mail", 0)], itp_civilian|itp_type_body_armor|itp_covers_legs, 0, 4096, weight(22)|head_armor(0)|body_armor(53)|leg_armor(16)|difficulty(9), imodbits_armor ],

["ccc_armour_breastplate", "Breast Plate Armor", [("breastplate",0)], itp_type_body_armor|itp_covers_legs, 0, 2000, weight(24)|abundance(100)|head_armor(10)|body_armor(49)|leg_armor(15)|difficulty(9), imodbits_plate ],
#["ccd_armour_mercenary_breastplate", "Breast Plate Armor", [("mercenary_breastplate",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(24)|abundance(100)|head_armor(10)|body_armor(49)|leg_armor(15)|difficulty(9), imodbits_plate ],
["ccc_armour_heavy_breastplate", "Heavy Breast Plate Armor", [("heavy_breastplate",0)], itp_type_body_armor|itp_covers_legs, 0, 2100, weight(26)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(18)|difficulty(11), imodbits_plate ],
#["ccd_armour_mercenary_plate", "Heavy Breast Plate Armor", [("mercenary_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(26)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(18)|difficulty(11), imodbits_plate ],

["ccc_armour_bnw_stripes", "Bnw Stripes Armor ", [("bnw_armour_stripes",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 2100, weight(19)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(12)|difficulty(9), imodbits_plate ],

#Narf
["ccc_armour_early_transitional_blue", "Early Transitional Blue Armour", [("early_transitional_blue",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1700, weight(20)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(7), imodbits_armor ],
["ccc_armour_early_transitional_orange", "Early Transitional Orange Armour", [("early_transitional_orange",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1700, weight(20)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(7), imodbits_armor ],
["ccc_armour_early_transitional_white", "Early Transitional Blue Armour", [("early_transitional_white",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1700, weight(20)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(7), imodbits_armor ],

["ccc_armour_churburg_13", "Full Plate", [("churburg_13",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3000, weight(23)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(20)|difficulty(8), imodbits_armor ],
["ccc_armour_churburg_13_brass", "Ornate Full Plate", [("churburg_13_brass",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3000, weight(23)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(20)|difficulty(8), imodbits_armor ],
["ccc_armour_churburg_13_mail", "Ornate Full Plate", [("churburg_13_mail",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3000, weight(23)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(20)|difficulty(8), imodbits_armor ],
["ccc_armour_churburg_13_bl", "Black Churburg Plate", [("churburg_13_mail_bl",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 3000, weight(23)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(20)|difficulty(8), imodbits_armor ],

["ccc_armour_corrazina_red", "Corrazina", [("corrazina_red",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1800, weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(18)|difficulty(8), imodbits_armor ],
["ccc_armour_corrazina_green", "Corrazina", [("corrazina_green",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1800, weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(18)|difficulty(6), imodbits_armor ],
["ccc_armour_corrazina_grey", "Corrazina", [("corrazina_grey",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 1800, weight(23)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(18)|difficulty(8), imodbits_armor ],

["ccc_armor_roma_cent_hamata", "Centurion Hamata", [("cent_hamata",0)], itp_type_body_armor|itp_covers_legs, 0, 750, weight(21)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(16)|difficulty(11), imodbits_armor ],
["ccc_armor_roma_hamata", "Hamata", [("hamata",0)], itp_type_body_armor|itp_covers_legs, 0, 650, weight(12)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(13)|difficulty(10), imodbits_armor ],
["ccc_armor_roma_squamata", "Squamata", [("squamata",0)], itp_type_body_armor|itp_covers_legs, 0, 780, weight(16)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(12)|difficulty(10), imodbits_armor ],
["ccc_armor_roma_gallicmail", "Gallic Mail", [("gallicmail",0)], itp_type_body_armor|itp_covers_legs, 0, 670, weight(16)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(10)|difficulty(7), imodbits_armor ],
["ccc_armor_roma_praetor_segmentata", "Praetor Segmentata", [("praetor_segmentata",0)], itp_type_body_armor|itp_covers_legs, 0, 1800, weight(22)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(15)|difficulty(10), imodbits_armor ],
["ccc_armor_roma_segmentata", "Segmentata", [("segmentata",0)], itp_type_body_armor|itp_covers_legs, 0, 1700, weight(22)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(15)|difficulty(10), imodbits_armor ],
["ccc_armor_black", "Black Armor", [("4black_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 1700, weight(20)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(19)|difficulty(10), imodbits_armor ],

["ccc_armor_east_saladin", "Saladin Mail", [("saladin",0)], itp_type_body_armor|itp_covers_legs, 0, 2300, weight(20)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(18)|difficulty(10), imodbits_armor ],
["ccc_armor_east_royal_scale_armor", "Royal Scale", [("royal_scale_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 2460, weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(12)|difficulty(10), imodbits_armor ],
["ccc_armor_east_black_lamellar_vest", "Black Lamellar Vest", [("black_lamellar_vest",0)], itp_type_body_armor|itp_covers_legs, 0, 2460, weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(10), imodbits_armor ],
["ccc_armor_east_brass_byrnie", "Brass Byrnie", [("brass_byrnie",0)], itp_type_body_armor|itp_covers_legs, 0, 1600, weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(10), imodbits_armor ],
["ccc_armor_east_brass_haubergeon", "Brass Haubergeon", [("brass_haubergeon",0)], itp_type_body_armor|itp_covers_legs, 0, 1600, weight(18)|abundance(100)|head_armor(1)|body_armor(48)|leg_armor(16)|difficulty(10), imodbits_armor ],
["ccc_armor_east_heavy_lamellar_armor", "Heavy Lamellar Armor", [("heavy_lamellar_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 1600, weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(10), imodbits_armor ],

["ccc_armor_rus_lamellar_a", "Rus lamellar", [("rus_lamellar_a",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs , 0, 2560, weight(18)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(8), imodbits_armor ],
["ccc_armor_rus_lamellar_b", "Rus lamellar", [("rus_lamellar_b",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs , 0, 2560, weight(18)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(8), imodbits_armor ],
["ccc_armor_kuyak_a", "Kuyak", [("kuyak_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1843, weight(16)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(12)|difficulty(6), imodbits_armor ],
["ccc_armor_kuyak_b", "Kuyak", [("kuyak_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2048, weight(16)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(7), imodbits_armor ],
["ccc_armor_rus_scale", "Rus Scale", [("rus_scale",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs , 0, 3072, weight(19)|abundance(100)|head_armor(0)|body_armor(49)|leg_armor(18)|difficulty(8), imodbits_armor ],

#Quest-specific - perhaps can be used for prisoners,
["burlap_tunic", "Burlap Tunic", [("shirt",0)], itp_type_body_armor|itp_covers_legs, 0, 5, weight(1)|abundance(100)|head_armor(0)|body_armor(3)|leg_armor(1)|difficulty(0), imodbits_armor ],

["khergit_guard_armor", "Khergit Guard Armor", [("lamellar_armor_a",0)], itp_type_body_armor|itp_covers_legs, 0, 3048, weight(19)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0), imodbits_armor ],
["mail_and_plate", "Mail and Plate", [("mail_and_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 593, weight(16)|abundance(100)|head_armor(0)|body_armor(34)|leg_armor(12)|difficulty(0), imodbits_armor ],
["light_mail_and_plate", "Light Mail and Plate", [("light_mail_and_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 532, weight(10)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_armor ],

#kengeki
["ccc_armor_sis_robe", "Sister Robe", [("sister_robe",0)], itp_type_body_armor|itp_covers_legs, 0, 1048, weight(6)|abundance(100)|head_armor(0)|body_armor(30)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["ccc_armor_sis_mail", "Sister Mail", [("sister_mail",0)], itp_type_body_armor|itp_covers_legs, 0, 1048, weight(12)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(10)|difficulty(5), imodbits_armor ],
["ccc_armor_valkyrie_armor_1", "Valkyrie Armor", [("valarmor",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 5048, weight(12)|abundance(500)|head_armor(0)|body_armor(47)|leg_armor(17)|difficulty(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_armor_valkyrie_armor_2", "Valkyrie Armor", [("valarmor2",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 5048, weight(12)|abundance(500)|head_armor(0)|body_armor(47)|leg_armor(17)|difficulty(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_armor_valkyrie_armor_3", "Valkyrie Armor", [("valarmor3",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 5048, weight(12)|abundance(500)|head_armor(0)|body_armor(47)|leg_armor(17)|difficulty(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_armor_valkyrie_armor_4", "Valkyrie Armor", [("valarmor4",0)], itp_merchandise|itp_type_body_armor|itp_covers_legs, 0, 5048, weight(12)|abundance(500)|head_armor(0)|body_armor(47)|leg_armor(17)|difficulty(0), imodbits_armor,[],[fac_valkyrie] ],

#plate
["heraldic_mail_with_surcoat_for_tableau", "Heraldic Mail with Surcoat", [("heraldic_armor_new_a",0)], itp_type_body_armor|itp_covers_legs, 0, 1, weight(22)|abundance(100)|head_armor(0)|body_armor(1)|leg_armor(1), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_heraldic_armor_a",":agent_no",":troop_no")])] ],
["coat_of_plates", "Coat of Plates", [("coat_of_plates_a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3828, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8), imodbits_plate ],
["coat_of_plates_red", "Coat of Plates", [("coat_of_plates_red",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3828, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(8), imodbits_plate ],
["plate_armor", "Plate Armor", [("full_plate_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 6553, weight(27)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(17)|difficulty(9), imodbits_plate ],
["black_armor", "Black Armor", [("black_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 9496, weight(28)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(16)|difficulty(10), imodbits_plate ],
["ccc_plate_light_plate", "Light Plate Armor", [("light_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(25)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(16)|difficulty(11), imodbits_plate ],
["ccc_plate_medium_plate", "Medium Plate Armor", [("medium_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(26)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(18)|difficulty(13), imodbits_plate ],

#occc decent armor models replaced
["ccc_plate_steelfull", "Elaborate Cuirass", [("gothic_plate_yb",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2800, weight(24)|abundance(80)|head_armor(0)|body_armor(53)|leg_armor(10)|difficulty(9), imodbits_plate ],
["ccc_plate_redleg", "Elaborate Plate Armor", [("gothic_armour_y",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3072, weight(32)|abundance(80)|head_armor(0)|body_armor(60)|leg_armor(17)|difficulty(9), imodbits_plate ],
["ccc_plate_legcross", "Elaborate Plate Armor", [("gothic_armour_y2",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3072, weight(32)|abundance(80)|head_armor(0)|body_armor(60)|leg_armor(17)|difficulty(9), imodbits_plate ],
["ccc_plate_steelcrossred", "Elaborate Plate Armor", [("gothic_armour_y6_2",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2800, weight(24)|abundance(80)|head_armor(0)|body_armor(60)|leg_armor(17)|difficulty(9), imodbits_plate ],
["ccc_plate_checkeredred", "Elaborate Plate Armor", [("gothic_armour_y6",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3072, weight(32)|abundance(80)|head_armor(0)|body_armor(60)|leg_armor(17)|difficulty(9), imodbits_plate ],

#occc plate armor buffed a bit
["ccc_plate_milanese", "Milanese Plate", [("milanese_armour",0)], itp_type_body_armor|itp_covers_legs, 0, 9496, weight(33)|abundance(30)|head_armor(0)|body_armor(62)|leg_armor(25)|difficulty(16), imodbits_plate ],
["ccc_plate_milanese_b", "Black Milanese Plate", [("milanese_armour_b",0)], itp_type_body_armor|itp_covers_legs, 0, 9496, weight(33)|abundance(30)|head_armor(0)|body_armor(62)|leg_armor(25)|difficulty(16), imodbits_plate ],

["ccc_plate_gothic", "Gothic Plate", [("gothic_armour",0)], itp_type_body_armor|itp_covers_legs, 0, 9496, weight(31)|abundance(30)|head_armor(8)|body_armor(62)|leg_armor(19)|difficulty(12), imodbits_plate ],
["ccc_plate_gothic_b", "Black Gothic Plate", [("gothic_armour_b",0)], itp_type_body_armor|itp_covers_legs, 0, 9496, weight(31)|abundance(30)|head_armor(8)|body_armor(62)|leg_armor(19)|difficulty(12), imodbits_plate ],

#ken
#["ccc_plate_ken_gothic_1", "Gothic Plate", [("gothic_plate_y2",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(19)|difficulty(12), imodbits_plate ],
["ccc_plate_ken_gothic_2", "Sister Plate", [("gothic_plate_y4",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(27)|abundance(100)|head_armor(0)|body_armor(58)|leg_armor(19)|difficulty(12), imodbits_plate ],
["ccc_plate_ken_gothic_3", "Sister Light Plate", [("gothic_plate_y4b",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(21)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(17)|difficulty(12), imodbits_plate ],
#["ccc_plate_ken_gothic_4", "Gothic Plate", [("gothic_plate_y6",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(19)|difficulty(12), imodbits_plate ],
#["ccc_plate_ken_gothic_5", "Gothic Plate", [("gothic_plate_y6b",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(19)|difficulty(12), imodbits_plate ],
#["ccc_plate_ken_gothic_6", "Gothic Plate", [("gothic_plate_ybxx",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(19)|difficulty(12), imodbits_plate ],
["ccc_plate_ken_milanese_1", "Milanese Plate", [("milanese_plate2",0)], itp_type_body_armor|itp_covers_legs, 0, 9496, weight(32)|abundance(100)|head_armor(0)|body_armor(59)|leg_armor(25)|difficulty(16), imodbits_plate ],

["ccc_plate_ken_uwarmor_1", "Death Knight Plate", [("uwarmor",0)], itp_type_body_armor|itp_covers_legs, 0, 5024, weight(30)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(25)|difficulty(16), imodbits_plate ],
["ccc_plate_ken_uwarmor_2", "Death Knight Plate", [("uwarmor2",0)], itp_type_body_armor|itp_covers_legs, 0, 5024, weight(30)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(25)|difficulty(16), imodbits_plate ],

#["ccc_plate_armor", "Plate Armor", [("armor_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(26)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(14)|difficulty(10), imodbits_plate ],
["ccc_plate_black_blazonry_color", "Black Plate", [("black_blazonry_color",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(29)|abundance(100)|head_armor(0)|body_armor(57)|leg_armor(17)|difficulty(10), imodbits_plate ],
["ccc_palte_black_plate", "Black Plate", [("black_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(30)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(17)|difficulty(10), imodbits_plate ],
["ccc_plate_black_ornate", "Black Plate Armor", [("breast_black_ornate",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(30)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(17)|difficulty(10), imodbits_plate ],
#["ccc_plate_black_dragons", "Black Dragons Plate Armor", [("dragons_black_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(27)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(14)|difficulty(10), imodbits_plate ],
["ccc_plate_full1", "Full Plate Armor", [("full_amor",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(27)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(18)|difficulty(12), imodbits_plate ],
["ccc_plate_hospitallar_armor", "Hospitallar Plate Armor", [("hospitallar_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(27)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(18)|difficulty(12), imodbits_plate ],
#["ccc_plate_kings_breast", "Kings Breast Plate Armor", [("kings_breast",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(27)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(18)|difficulty(12), imodbits_plate ],
["ccc_plate_silver_black_ornate", "Black Silver Plate Armor", [("silver_black_ornate",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(33)|abundance(100)|head_armor(0)|body_armor(65)|leg_armor(22)|difficulty(14), imodbits_plate ],
["ccc_plate_silver_blazonry", "Lion Silver Plate Armor", [("silver_blazonry",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(33)|abundance(100)|head_armor(0)|body_armor(65)|leg_armor(22)|difficulty(14), imodbits_plate ],
["ccc_plate_silver_fine_plate", "Silver Fine Plate Armor", [("silver_fine_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(33)|abundance(100)|head_armor(0)|body_armor(65)|leg_armor(22)|difficulty(14), imodbits_plate ],
["ccc_plate_templar_armor", "Templar Plate Armor", [("templar_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(20)|difficulty(14), imodbits_plate ],
["ccc_plate_teutonic_armor", "Teutonic Plate Armor", [("teutonic_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(20)|difficulty(14), imodbits_plate ],
#["ccc_plate_ornate_plate", "Ornate Plate Armor", [("ornate_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(20)|difficulty(14), imodbits_plate ],
["ccc_plate_warrior_breast", "Warrior Plate Armor", [("full_plate_under",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(28)|abundance(100)|head_armor(0)|body_armor(60)|leg_armor(15)|difficulty(12), imodbits_armor ],
#occc end

#spak
["ccc_plate_spak_armor", "Plate Armor", [("2full_plate_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 7168, weight(27)|abundance(100)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9), imodbits_plate ],
["ccc_plate_spak_armor_b", "Black Plate Armor", [("2full_plate_armor_b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 7168, weight(27)|abundance(100)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9), imodbits_plate ],
["ccc_plate_spak_bear_armor", "Bear Armor", [("bear_warrior",0)], itp_type_body_armor|itp_covers_legs, 0, 3072, weight(22)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(17)|difficulty(9), imodbits_plate ],
["ccc_plate_spak_bk", "Black Knight Plate Armor", [("dark_lord_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 6553, weight(27)|abundance(100)|head_armor(0)|body_armor(58)|leg_armor(17)|difficulty(9), imodbits_plate ],

["strange_armor", "Strange Armor", [("samurai_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 3000, weight(18)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(19)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai01_old", "Kattyu", [("armure_samurai01",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(21)|abundance(220)|head_armor(0)|body_armor(50)|leg_armor(19)|difficulty(7), imodbits_plate, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai02_old", "Kattyu", [("armure_samurai02",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(19)|abundance(220)|head_armor(0)|body_armor(50)|leg_armor(17)|difficulty(7), imodbits_plate, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai01", "Haramaki", [("haramaki_ashi",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(13)|abundance(220)|head_armor(0)|body_armor(28)|leg_armor(8), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai02", "Doumaru", [("doumaru_ashi",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(14)|abundance(220)|head_armor(0)|body_armor(37)|leg_armor(10), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai03", "Gusoku", [("gusoku2_ashi",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(15)|abundance(220)|head_armor(0)|body_armor(43)|leg_armor(13)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai04", "Siro Doumaru", [("gusoku2_ashif",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(20)|abundance(220)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_plate_jp_armure_samurai05", "Momo Doumaru", [("sdngusoku_momo",0)], itp_type_body_armor|itp_covers_legs, 0, 1500, weight(19)|abundance(20)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(7), imodbits_armor ],
["ccc_plate_jp_armure_samurai06", "Kuro Doumaru", [("gusoku2_kuro",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(19)|abundance(220)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai07", "Aka Doumaru", [("gusoku_aka",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(19)|abundance(220)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai08", "Ao Kattyu", [("gusoku_ao",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(19)|abundance(220)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai09", "Kuro Kattyu", [("gusoku_black",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(20)|abundance(220)|head_armor(0)|body_armor(49)|leg_armor(17)|difficulty(8), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_plate_jp_armure_samurai10", "Gin Kattyu", [("gusoku_slv",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1700, weight(20)|abundance(220)|head_armor(0)|body_armor(49)|leg_armor(17)|difficulty(8), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccd_gusoku_ashigaru_hatasashi", "Hatasashi Ashigaru Gusoku", [("tableau_gusoku2_ashi_sashi_long",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1756, weight(16)|abundance(220)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(8), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_gusoku2_ashi_sashi_long",":agent_no",":troop_no")])], [fac_kingdom_9,fac_bushido_order] ],
["ccd_gusoku_aka_hatasashi", "Hatasashi Aka Gusoku", [("tableau_gusoku_aka_sashi_long",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1756, weight(20)|abundance(220)|head_armor(0)|body_armor(45)|leg_armor(14)|difficulty(8), imodbits_armor, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_gusoku_aka_sashi_long",":agent_no",":troop_no")])], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_plate_bar_berserk_armors_1", "BerserkArmorSnocape", [("BerserkArmorSnocape",0)], itp_type_body_armor|itp_covers_legs, 0, 25000, weight(28)|abundance(20)|head_armor(0)|body_armor(65)|leg_armor(25)|difficulty(15), imodbits_plate ],
#["ccc_plate_bar_berserk_armors_2", "BerserkArmorWnocape", [("BerserkArmorWnocape",0)], itp_type_body_armor|itp_covers_legs, 0, 25000, weight(28)|abundance(20)|head_armor(0)|body_armor(65)|leg_armor(25)|difficulty(15), imodbits_plate ],
#["ccc_plate_bar_berserk_armors_3", "BerserkArmorS", [("BerserkArmorS",0)], itp_type_body_armor|itp_covers_legs, 0, 25000, weight(28)|abundance(20)|head_armor(0)|body_armor(65)|leg_armor(25)|difficulty(15), imodbits_plate ],
["ccc_plate_bar_berserk_armors_4", "BerserkArmorW", [("BerserkArmorW",0)], itp_type_body_armor|itp_covers_legs, 0, 25000, weight(28)|abundance(20)|head_armor(0)|body_armor(65)|leg_armor(25)|difficulty(15), imodbits_plate ],

#celtbody
["ccc_celtbody_bluepat", "Blue War Paint", [("1celtbody",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(0.5)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_celtbody_germanbody_black", "Black War Paint", [("1germanbody",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(0.5)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_celtbody_bluefade", "Faded War Paint", [("3celtbody",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(0.5)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_celtbody_bluehalf", "Blue War Paint", [("4celtbody",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(0.5)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_celtbody_bluemark", "Blue War Pattern", [("6celtbody",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(0.5)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccd_celtbody", "Pictish_Naked", [("2celtbody",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(0.5)|abundance(10)|head_armor(0)|body_armor(16)|leg_armor(5)|difficulty(0), imodbits_cloth ],

#cloth helm
#Cloak
["ccc_red_cloak", "red cloak", [("cloak1",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_blue_cloak", "blue cloak", [("cloak3",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_grey_cloak", "grey cloak", [("cloak5",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_rough_cloak", "rough cloak", [("cloak7",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_black_cloak", "black cloak", [("cloak9",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_white_cloak", "white cloak", [("cloak11",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_green_cloak", "green cloak", [("cloak13",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_brown_cloak", "brown cloak", [("cloak15",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_blue_cloakm", "worn blue cloak", [("cloak17",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
#["ccc_green_cloakb", "bright green cloak", [("cloak19",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 193 , weight(1)|abundance(50)|head_armor(8)|body_armor(12)|leg_armor(0) ,imodbits_cloth ],
["ccc_red_cloakt", "Red Noble Cloak with trim", [("cloak21",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 500 , weight(2)|abundance(20)|head_armor(10)|body_armor(15)|leg_armor(1) ,imodbits_cloth ],
["ccc_green_cloakt", "Green Noble Cloak with trim", [("cloak22",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 500 , weight(2)|abundance(20)|head_armor(10)|body_armor(15)|leg_armor(1) ,imodbits_cloth ],
["ccc_white_cloakt", "White Noble Cloak", [("cloak23",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 500 , weight(2)|abundance(20)|head_armor(10)|body_armor(15)|leg_armor(1) ,imodbits_cloth ],
["ccc_black_cloakt", "Black Noble Cloak", [("cloak24",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 500 , weight(2)|abundance(20)|head_armor(10)|body_armor(15)|leg_armor(1) ,imodbits_cloth ],
["ccc_black_cloakr", "Black Noble Cloak with red lining", [("cloak25",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 500 , weight(2)|abundance(20)|head_armor(10)|body_armor(15)|leg_armor(1) ,imodbits_cloth ],
["ccc_black_cloakb", "Black Noble Cloak with blue lining", [("cloak26",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 500 , weight(2)|abundance(20)|head_armor(10)|body_armor(15)|leg_armor(1) ,imodbits_cloth ],
["ccc_red_cloak_hood", "red cloak and hood", [("cloak2",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_blue_cloak_hood", "blue cloak and hood", [("cloak4",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
#["ccc_grey_cloak_hood", "grey cloak and hood", [("cloak6",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
#["ccc_rough_cloak_hood", "rough cloak and hood", [("cloak8",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_black_cloak_hood", "black cloak and hood", [("cloak10",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_white_cloak_hood", "white cloak and hood", [("cloak12",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_green_cloak_hood", "green cloak and hood", [("cloak14",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
#["ccc_brown_cloak_hood", "brown cloak and hood", [("cloak16",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_blue_cloak_hoodm", "worn blue cloak and hood", [("cloak18",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_green_cloak_hoodb", "dark red cloak and hood", [("cloak20",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 256 , weight(2)|abundance(50)|head_armor(13)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_green_cloak_hoodc", "green cloak and hood with mask", [("cloak27",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 312 , weight(2)|abundance(100)|head_armor(14)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
#["ccc_brown_cloak_hoodc", "brown cloak and hood with mask", [("cloak28",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 312 , weight(2)|abundance(100)|head_armor(14)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
["ccc_black_cloak_hoodc", "black cloak and hood with mask", [("cloak29",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 312 , weight(2)|abundance(100)|head_armor(14)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],
#["ccc_grey_cloak_hoodc", "grey cloak and hood with mask", [("cloak30",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_attach_armature| itp_doesnt_cover_hair,0, 312 , weight(2)|abundance(100)|head_armor(14)|body_armor(10)|leg_armor(0) ,imodbits_cloth ],

#Headwear 
["turret_hat_ruby", "Turret Hat", [("turret_hat_r",0)], itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 70, weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["turret_hat_blue", "Turret Hat", [("turret_hat_b",0)], itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 80, weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["turret_hat_green", "Barbette", [("barbette_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian|itp_fit_to_head, 0, 70, weight(0.5)|abundance(100)|head_armor(6)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["head_wrappings", "Head Wrapping", [("head_wrapping",0)], itp_type_head_armor|itp_fit_to_head, 0, 16, weight(0.25)|head_armor(3), imodbit_tattered|imodbit_ragged|imodbit_sturdy|imodbit_thick ],
["court_hat", "Turret Hat", [("court_hat",0)], itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 80, weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["wimple_a", "Wimple", [("wimple_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian|itp_fit_to_head, 0, 10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["wimple_with_veil", "Wimple with Veil", [("wimple_b_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian|itp_fit_to_head, 0, 10, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["khergit_lady_hat", "Khergit Lady Hat", [("khergit_lady_hat",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_civilian|itp_fit_to_head, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["khergit_lady_hat_b", "Khergit Lady Leather Hat", [("khergit_lady_hat_b",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_civilian|itp_fit_to_head, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["female_hood", "Lady's Hood", [("ladys_hood_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["sarranid_head_cloth", "Lady Head Cloth", [("tulbent",0)], itp_type_head_armor|itp_attach_armature|itp_doesnt_cover_hair|itp_civilian, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["sarranid_head_cloth_b", "Lady Head Cloth", [("tulbent_b",0)], itp_type_head_armor|itp_attach_armature|itp_doesnt_cover_hair|itp_civilian, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["straw_hat", "Straw Hat", [("straw_hat_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 9, weight(1)|abundance(100)|head_armor(2)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["ccd_headdress", "Head Dress", [("ccd_headdress",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_civilian|itp_fit_to_head, 0, 256, weight(0.5)|head_armor(5)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

#Cloth Helmets 
["sarranid_felt_head_cloth", "Head Cloth", [("common_tulbent",0)], itp_type_head_armor|itp_attach_armature|itp_civilian, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["sarranid_felt_head_cloth_b", "Head Cloth", [("common_tulbent_b",0)], itp_type_head_armor|itp_attach_armature|itp_civilian, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["common_hood", "Hood", [("hood_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["hood_b", "Hood", [("hood_b",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["hood_c", "Hood", [("hood_c",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["hood_d", "Hood", [("hood_d",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 9, weight(1)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["black_hood", "Black Hood", [("hood_black",0)], itp_type_head_armor|itp_merchandise, 0, 193, weight(2)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["headcloth", "Headcloth", [("headcloth_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 1, weight(0.5)|abundance(100)|head_armor(4)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["woolen_hood", "Woolen Hood", [("woolen_hood",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 4, weight(1)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["padded_coif", "Padded Coif", [("padded_coif_a_new",0)], itp_type_head_armor|itp_merchandise, 0, 6, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["woolen_cap", "Woolen Cap", [("woolen_cap_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 2, weight(1)|abundance(100)|head_armor(6)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["felt_hat", "Felt Hat", [("felt_hat_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 4, weight(1)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["felt_hat_b", "Felt Hat", [("felt_hat_b_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 4, weight(1)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["arming_cap", "Arming Cap", [("arming_cap_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 5, weight(1)|abundance(100)|head_armor(7)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

#Fur Helmets
["fur_hat", "Fur Hat", [("fur_hat_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 4, weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["nomad_cap", "Nomad Cap", [("nomad_cap_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 6, weight(0.75)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["nomad_cap_b", "Nomad Cap", [("nomad_cap_b_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 6, weight(0.75)|abundance(100)|head_armor(13)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["steppe_cap", "Steppe Cap", [("steppe_cap_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 14, weight(1)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

#Leather Helmets
["leather_cap", "Leather Cap", [("leather_cap_a_new",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 8, weight(1)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["leather_steppe_cap_a", "Steppe Cap", [("leather_steppe_cap_a_new",0)], itp_type_head_armor|itp_merchandise, 0, 24, weight(1)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["leather_steppe_cap_b", "Steppe Cap ", [("tattered_steppe_cap_b_new",0)], itp_type_head_armor|itp_merchandise, 0, 36, weight(1)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["leather_steppe_cap_c", "Steppe Cap", [("steppe_cap_a_new",0)], itp_type_head_armor|itp_merchandise, 0, 51, weight(1)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["leather_warrior_cap", "Leather Warrior Cap", [("skull_cap_new_b",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 14, weight(1)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

#["ccc_hat_musketeer_hat01", "Musketeer Hat", [("musketeer_hat01",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_hat_musketeer_hat02", "Musketeer Hat", [("musketeer_hat02",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_hat_musketeer_hat03", "Musketeer Hat", [("musketeer_hat03",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_hat_musketeer_hat04", "Musketeer Hat", [("musketeer_hat04",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musketeer_hat05", "Musketeer Hat", [("musketeer_hat05",0)], itp_type_head_armor|itp_merchandise, 0, 36, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_hat_musketeer_hat06", "Musketeer Hat", [("musketeer_hat06",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musketeer_hat07", "Tricorne",      [("musketeer_hat07",0)], itp_type_head_armor|itp_merchandise, 0, 36, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musketeer_hat08", "Musketeer Hat", [("musketeer_hat08",0)], itp_type_head_armor|itp_merchandise, 0, 36, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_hat_musketeer_hat09", "Musketeer Hat", [("musketeer_hat09",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_hat_musketeer_hat10", "Musketeer Hat", [("musketeer_hat10",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musketeer_hat11", "Musketeer Hat", [("musketeer_hat11",0)], itp_type_head_armor|itp_merchandise, 0, 36, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_hat_musketeer_hat12", "Musketeer Hat", [("musketeer_hat12",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musketeer_hat13", "Musketeer Hat", [("musketeer_hat13",0)], itp_type_head_armor|itp_merchandise, 0, 36, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musketeer_hat14", "Musketeer Hat", [("musketeer_hat14",0)], itp_type_head_armor|itp_merchandise, 0, 36, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_bear_hood", "Bear Hood", [("helm_Roman_standard_bearer",0)], itp_type_head_armor|itp_attach_armature, 0, 350, weight(1)|abundance(75)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hilander_cloth_boots", "Hilander Cloth Boots", [("b_h1_1",0)], itp_type_foot_armor, 0, 200, weight(1)|abundance(75)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["ccc_hilander_kelt_boots", "Hilander Kelt Boots", [("b_h1",0)], itp_type_foot_armor, 0, 200, weight(1.5)|abundance(75)|head_armor(0)|body_armor(0)|leg_armor(9)|difficulty(0), imodbits_cloth ],
["ccc_hilander_bear_boots", "Hilander Bear Boots", [("b_h2",0)], itp_type_foot_armor|itp_merchandise, 0, 200, weight(3.5)|abundance(110)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0), imodbits_cloth ],
["ccc_hilander_wolf_boots", "Hilander Wolf Boots", [("b_h2_1",0)], itp_type_foot_armor|itp_attach_armature, 0, 200, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["ccc_mant_red", "Warrior Mant", [("cloak1",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_attach_armature|itp_merchandise|itp_civilian, 0, 1500, weight(1)|abundance(85)|head_armor(8)|body_armor(17)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ccc_mant_black", "Black Mant", [("cloak13",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_attach_armature|itp_merchandise|itp_civilian, 0, 700, weight(1)|abundance(85)|head_armor(2)|body_armor(12)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["mant_food", "Mant and Hood", [("cloak20",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_attach_armature|itp_merchandise, 0, 700, weight(1)|abundance(85)|head_armor(13)|body_armor(13)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_10_mant", "Cross Mant", [("cloak99_2",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_attach_armature|itp_merchandise|itp_civilian, 0, 1500, weight(1)|abundance(85)|head_armor(3)|body_armor(12)|leg_armor(0)|difficulty(0), imodbits_cloth ],
#["ncm_ccc_hat_musketeer_hat11", "White Mant", [("cloak11",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_attach_armature|itp_merchandise|itp_civilian, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_mant_pale", "White Mant", [("cloak11",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_attach_armature|itp_merchandise|itp_civilian, 0, 1500, weight(1)|abundance(85)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["ccc_hat_demon_hood", "Dark Hood", [("demon_hood",0)], itp_type_head_armor|itp_covers_beard, 0, 350, weight(1)|abundance(85)|head_armor(29)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccd_hat_demon_hood_new", "Elite Dark Hood", [("demon_hood_new",0)], itp_type_head_armor|itp_covers_beard, 0, 1536, weight(1)|abundance(75)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccd_hat_shadow_hood", "Shadow Hood", [("ccd_shadowhood",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 4096, weight(1)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["ccc_hat_musket_hat_1", "Musketeer Hat", [("french_artillery_ranker_bearskin",0)], itp_type_head_armor|itp_fit_to_head, 0, 36, weight(1)|abundance(85)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musket_hat_2", "Musketeer Hat", [("french_GaP_ranker_bearskin",0)], itp_type_head_armor|itp_fit_to_head, 0, 36, weight(1)|abundance(85)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_hat_musket_hat_3", "Cavary Hat", [("french_cuirassier_helmet_ranker",0)], itp_type_head_armor, 0, 36, weight(1)|abundance(85)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

#helm
#Helmets
["skullcap", "Skullcap", [("skull_cap_new_a",0)], itp_type_head_armor|itp_merchandise, 0, 60, weight(1.0)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["mail_coif", "Mail Coif", [("mail_coif_new",0)], itp_type_head_armor|itp_merchandise, 0, 71, weight(1.25)|abundance(100)|head_armor(22)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["footman_helmet", "Footman's Helmet", [("skull_cap_new",0)], itp_type_head_armor|itp_merchandise, 0, 95, weight(1.5)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["nasal_helmet", "Nasal Helmet", [("nasal_helmet_b",0)], itp_type_head_armor|itp_merchandise, 0, 121, weight(1.25)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["norman_helmet", "Helmet with Cap", [("norman_helmet_a",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 147, weight(1.25)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["segmented_helmet", "Segmented Helmet", [("segmented_helm_new",0)], itp_type_head_armor|itp_merchandise, 0, 174, weight(1.25)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["helmet_with_neckguard", "Helmet with Neckguard", [("neckguard_helm_new",0)], itp_type_head_armor|itp_merchandise, 0, 190, weight(1.5)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["flat_topped_helmet", "Flat Topped Helmet", [("flattop_helmet_new",0)], itp_type_head_armor|itp_merchandise, 0, 203, weight(1.75)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["kettle_hat", "Kettle Hat", [("kettle_hat_new",0)], itp_type_head_armor|itp_merchandise, 0, 240, weight(1.75)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["spiked_helmet", "Spiked Helmet", [("spiked_helmet_new",0)], itp_type_head_armor|itp_merchandise, 0, 278, weight(2)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["nordic_helmet", "Nordic Helmet", [("helmet_w_eyeguard_new",0)], itp_type_head_armor|itp_merchandise, 0, 340, weight(2)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],

#Sarranid Helmets
["sarranid_felt_hat", "Sarranid Felt Hat", [("sar_helmet3",0)], itp_type_head_armor|itp_merchandise, 0, 16, weight(2)|abundance(100)|head_armor(5)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_cloth ],
["turban", "Turban", [("tuareg_open",0)], itp_type_head_armor|itp_merchandise, 0, 28, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_cloth ],
["desert_turban", "Desert Turban", [("tuareg",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 38, weight(1.50)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_cloth ],
["sarranid_warrior_cap", "Sarranid Warrior Cap", [("tuareg_helmet",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 90, weight(2)|abundance(100)|head_armor(19)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["sarranid_horseman_helmet", "Horseman Helmet", [("sar_helmet2",0)], itp_type_head_armor|itp_merchandise, 0, 180, weight(2.75)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["sarranid_helmet1", "Sarranid Keffiyeh Helmet", [("sar_helmet1",0)], itp_type_head_armor|itp_merchandise, 0, 290, weight(2.50)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["sarranid_mail_coif", "Sarranid Mail Coif", [("tuareg_helmet2",0)], itp_type_head_armor|itp_merchandise, 0, 430, weight(3)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["sarranid_veiled_helmet", "Sarranid Veiled Helmet", [("sar_helmet4",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 810, weight(3.50)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],

#Nordic Helmets
["nordic_archer_helmet", "Nordic Leather Helmet", [("Helmet_A_vs2",0)], itp_type_head_armor|itp_merchandise, 0, 40, weight(1.25)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["nordic_veteran_archer_helmet", "Nordic Leather Helmet", [("Helmet_A",0)], itp_type_head_armor|itp_merchandise, 0, 70, weight(1.5)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["nordic_footman_helmet", "Nordic Footman Helmet", [("Helmet_B_vs2",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 150, weight(1.75)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["nordic_fighter_helmet", "Nordic Fighter Helmet", [("Helmet_B",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head, 0, 240, weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["nordic_huscarl_helmet", "Nordic Huscarl's Helmet", [("Helmet_C_vs2",0)], itp_type_head_armor|itp_merchandise, 0, 390, weight(2)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["nordic_warlord_helmet", "Nordic Warlord Helmet", [("Helmet_C",0)], itp_type_head_armor|itp_merchandise, 0, 880, weight(2.25)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],

#Vaegir Helmets
["vaegir_fur_cap", "Cap with Fur", [("vaeg_helmet3",0)], itp_type_head_armor|itp_merchandise, 0, 50, weight(1)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["vaegir_fur_helmet", "Vaegir Helmet", [("vaeg_helmet2",0)], itp_type_head_armor|itp_merchandise, 0, 110, weight(2)|abundance(100)|head_armor(21)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["vaegir_spiked_helmet", "Spiked Cap", [("vaeg_helmet1",0)], itp_type_head_armor|itp_merchandise, 0, 230, weight(2.50)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["vaegir_lamellar_helmet", "Helmet with Lamellar Guard", [("vaeg_helmet4",0)], itp_type_head_armor|itp_merchandise, 0, 360, weight(2.75)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["vaegir_noble_helmet", "Vaegir Nobleman Helmet", [("vaeg_helmet7",0)], itp_type_head_armor|itp_merchandise, 0, 710, weight(2.75)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["vaegir_war_helmet", "Vaegir War Helmet", [("vaeg_helmet6",0)], itp_type_head_armor|itp_merchandise, 0, 820, weight(3)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["vaegir_mask", "Vaegir War Mask", [("vaeg_helmet9",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 950, weight(3.50)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],

#Khergit Helmets
["felt_steppe_cap", "Felt Steppe Cap", [("felt_steppe_cap",0)], itp_type_head_armor, 0, 237, weight(2)|abundance(100)|head_armor(16)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["khergit_war_helmet", "Khergit War Helmet", [("tattered_steppe_cap_a_new",0)], itp_type_head_armor|itp_merchandise, 0, 200, weight(2)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["khergit_helmet", "Khergit Helmet", [("khergit_guard_helmet",0)], itp_type_head_armor, 0, 361, weight(2)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["khergit_guard_helmet", "Khergit Guard Helmet", [("lamellar_helmet_a",0)], itp_type_head_armor|itp_merchandise, 0, 433, weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["khergit_cavalry_helmet", "Khergit Cavalry Helmet", [("lamellar_helmet_b",0)], itp_type_head_armor|itp_merchandise, 0, 333, weight(2)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0), imodbits_cloth ],

#saradin
["byzantion_helmet_a", "Byzantion Helmet", [("byzantion_helmet_a",0)], itp_type_head_armor, 0, 278, weight(2)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["magyar_helmet_a", "Magyar Helmet", [("magyar_helmet_a",0)], itp_type_head_armor, 0, 278, weight(2)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["rus_helmet_a", "Rus Helmet", [("rus_helmet_a",0)], itp_type_head_armor, 0, 278, weight(2)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["sipahi_helmet_a", "Sipahi Helmet", [("sipahi_helmet_a",0)], itp_type_head_armor, 0, 278, weight(2)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["shahi", "Shahi", [("shahi",0)], itp_type_head_armor, 0, 278, weight(2)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["rabati", "Rabati", [("rabati",0)], itp_type_head_armor, 0, 278, weight(2)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0), imodbits_cloth ],

#Bascinets
["bascinet", "Bascinet", [("bascinet_avt_new",0)], itp_type_head_armor|itp_merchandise, 0, 479, weight(2.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate ],
["bascinet_2", "Bascinet with Aventail", [("bascinet_new_a",0)], itp_type_head_armor|itp_merchandise, 0, 479, weight(2.25)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate ],
["bascinet_3", "Bascinet with Nose Guard", [("bascinet_new_b",0)], itp_type_head_armor|itp_merchandise, 0, 479, weight(2.25)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate ],

["guard_helmet", "Guard Helmet", [("reinf_helmet_new",0)], itp_type_head_armor|itp_merchandise, 0, 555, weight(2.5)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],

#Barbutas
["black_helmet", "Black Helmet", [("black_helm",0)], itp_type_head_armor, 0, 638, weight(2.75)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],

#Great Helmets
["full_helm", "Full Helm", [("great_helmet_new_b",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 811, weight(2.5)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helmet", "Great Helmet", [("great_helmet_new",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["winged_great_helmet", "Winged Great Helmet", [("maciejowski_helmet_new",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 1240, weight(2.75)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],

#["ccc_helm_bascinet_mask", "Masked Bascinet", [("basmask",0)], itp_type_head_armor, 0, 700, weight(2.0)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],  ## cave09 del
["ccc_helm_great_helm_black", "Black Helm", [("blackhelm",0)], itp_type_head_armor, 0, 700, weight(2.75)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(2), imodbits_plate ],
#occc model changed
["ccc_helm_chieftain_helmet", "Valsgarde Helmet", [("x_VALSGARDE2",0)], itp_type_head_armor|itp_merchandise, 0, 1624, weight(2.0)|abundance(1)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_4]  ],
["ccc_helm_great_helm_light", "Great Helm", [("crusaderhelm",0)], itp_type_head_armor, 0, 700, weight(2.75)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_nord_helm_coif_01", "Nordic Helm with Coif", [("helmet_w_eyeguard_new_alt",0)], itp_type_head_armor, 0, 433, weight(2.0)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_kettle_helm_coif", "Kettle Helmet with Coif", [("kettlehelm",0)], itp_type_head_armor, 0, 380, weight(2.0)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_great_helm_cross", "Great Helm", [("maciejowskihelm",0)], itp_type_head_armor, 0, 800, weight(2.75)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_nasal_helm_coif", "Nasal Helm with Coif", [("nasalhelm_coif",0)], itp_type_head_armor|itp_merchandise, 0, 433, weight(2.5)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_nord_helm_coif_02", "Nordic Helm with Coif", [("nordhelm_coif",0)], itp_type_head_armor|itp_merchandise, 0, 443, weight(2.0)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
#["ccc_helm_skullcap_mask", "Masked Skullcap", [("orcmaskcheeks",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(2.0)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],  ## cave09 del
#["ccc_helm_skullcap_coif_01", "Skullcap with Coif", [("orcromanhelm",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1.5)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],  ## cave09 del
#["ccc_helm_barbutte_01", "Barbutte", [("realbarbutteb",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(2.5)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_bascinet_coif", "Bascinet", [("realbascinetc",0)], itp_type_head_armor|itp_merchandise, 0, 520, weight(2.5)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
#["ccc_helm_bascinet_open", "Bascinet", [("realbascinete",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(2.5)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_sallet_helm", "Sallet", [("salade",0)], itp_type_head_armor, 0, 443, weight(2.5)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_sallet_helm_full", "Full Sallet", [("saladec",0)], itp_type_head_armor, 0, 500, weight(3.0)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
#["ccc_helm_skullcap_coif_02", "Skullcap with Coif", [("skullcap_coif",0)], itp_type_head_armor, 0, 700, weight(1.5)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_chieftain_helmet_gold", "Chieftain Helm", [("v_leader_helm",0)], itp_type_head_armor, 0, 443, weight(2.0)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_bascinet_vaegir", "Bascinet", [("vaegirhelm",0)], itp_type_head_armor, 0, 403, weight(2.5)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
#["ccc_helm_spanishpigface", "Pigface Helmet", [("spanishpigface",0)], itp_type_head_armor, 0, 700, weight(1.25)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_spanishsallet", "Sallet", [("spanishsallet",0)], itp_type_head_armor, 0, 980, weight(2.25)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_barbutemdarkmailnew", "Barbutte", [("barbutemdarkmailnew",0)], itp_type_head_armor, 0, 700, weight(1.25)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_reinforcedburgonetnew", "Burgonet", [("reinforcedburgonetnew",0)], itp_type_head_armor, 300, 700, weight(1.25)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["ccc_helm_footmansalletbnew", "Sallet", [("footmansalletbnew",0)], itp_type_head_armor, 0, 700, weight(1.25)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(14), imodbits_plate ],
["ccc_helm_morionreinforcednew", "Morion", [("morionreinforcednew",0)], itp_type_head_armor, 0, 700, weight(2.25)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate ],  ## cave09 del
["ccc_helm_morionnew", "Morion", [("morionnew",0)], itp_type_head_armor, 0, 700, weight(2.25)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(6), imodbits_plate ],
#["ccc_helm_pigfacenew", "Pigface Helmet", [("pigfacenew",0)], itp_type_head_armor, 0, 700, weight(2.25)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_burgonetnew", "Burgonet", [("burgonetnew",0)], itp_type_head_armor, 0, 700, weight(1.25)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate ],
["ccc_helm_openhornedpigfacenew", "Horned Pigface Helmet", [("openhornedpigfacenew",0)], itp_type_head_armor, 0, 1000, weight(1.25)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_hornedpigfacenew", "Horned Pigface Helmet", [("hornedpigfacenew",0)], itp_type_head_armor, 0, 980, weight(1.25)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate ],

["ccc_helm_darkknighthelm", "Dark Knight Helmet", [("darkknighthelm",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 980, weight(2.25)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_plate, [], [fac_kingdom_7] ],
["ccc_helm_darkknighthelmblackhorns", "Horned Dark Knght Helmet", [("darkknighthelmblackhorns",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 1000, weight(1.25)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_7] ],
["ccc_helm_darkknighthelmdragon", "Dragon Helmet", [("darkknighthelmdragon",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 1000, weight(1.25)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_7] ],
["ccc_helm_darkpaladinhelm", "Paladine Helmet", [("darkpaladinhelm",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 1000, weight(2.25)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_7] ],
["ccc_helm_darkhunterhelm", "Hunter Helmet", [("darkhunterhelm",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 880, weight(1.25)|abundance(100)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate, [], [fac_kingdom_7] ],
["ccc_helm_dark_1", "Dark Helm", [("commanderwarhelm",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 2024, weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor, [], [fac_kingdom_7] ],
["ccc_helm_dark_2", "Dark Helm", [("barbutclosedcrow",0)], itp_type_head_armor|itp_fit_to_head|itp_covers_head|itp_covers_beard|itp_merchandise, 0, 780, weight(2.75)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor, [], [fac_kingdom_7] ],

["ccc_helm_chapel_de_fer", "Chapel-de-Fer", [("chapel-de-fer",0)], itp_merchandise| itp_type_head_armor,0, 700 , weight(1.5)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor ],
["ccc_helm_combed_morion_helmet", "Combed Morion", [("combed_morion",0)], itp_merchandise|itp_type_head_armor, 0, 758, weight(2)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor, [], [fac_kingdom_1] ],
["ccc_helm_combed_morion_blued_helmet", "Combed Morion Blued", [("combed_morion_blued",0)], itp_merchandise|itp_type_head_armor, 0, 758, weight(2)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor, [], [fac_kingdom_1] ],

#occc tweak sallet armor buffed +5  slightly more weight +0.25 value +120
["ccc_helm_visored_sallet", "Visored Sallet", [("visored_salet",0)], itp_merchandise| itp_type_head_armor   ,0, 758 , weight(2.25)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor ],
["ccc_helm_visored_sallet_coif", "Visored Sallet with Coif", [("visored_salet_coif",0)], itp_merchandise| itp_type_head_armor   ,0, 1200 , weight(2.5)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["ccc_helm_open_sallet", "Open Sallet", [("open_salet",0)], itp_merchandise| itp_type_head_armor   ,0, 658 , weight(2.0)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor ],
["ccc_helm_open_sallet_coif", "Open Sallet with Coif", [("open_salet_coif",0)], itp_type_head_armor   ,0, 958 , weight(2.25)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
#occc blackened series
["ccc_helm_visored_sallet_b", "Visored Sallet", [("visored_salet_b",0)], itp_merchandise| itp_type_head_armor   ,0, 758 , weight(2.25)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor ],
["ccc_helm_visored_sallet_coif_b", "Visored Sallet with Coif", [("visored_salet_coif_b",0)], itp_merchandise| itp_type_head_armor   ,0, 1200 , weight(2.5)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],
["ccc_helm_open_sallet_b", "Open Sallet", [("open_salet_b",0)], itp_merchandise| itp_type_head_armor   ,0, 658 , weight(2.0)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor ],
["ccc_helm_open_sallet_coif_b", "Open Sallet with Coif", [("open_salet_coif_b",0)], itp_type_head_armor   ,0, 958 , weight(2.25)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate ],

["ccc_helm_2kettle", "Kettle Helm", [("2kettle_hat_new",0)], itp_type_head_armor, 0, 1400, weight(2.0)|abundance(100)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_great_helmet", "Great Helmet", [("2great_helmet_new",0)], itp_type_head_armor, 0, 980, weight(2.0)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_plate ],
#occc tweak 42->56
["ccc_helm_nord_king", "Nord King Helm", [("VALSGARDE8",0)], itp_type_head_armor, 0, 80000, weight(2.0)|abundance(1)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_cloth ],
["ccc_helm_witchking_helmet_large", "Witchking Helmet Large", [("witchking_helmet_large",0)], itp_type_head_armor|itp_unique|itp_covers_head|itp_covers_beard, 0, 90000, weight(2.0)|abundance(5)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_witchking_helmet", "Witchking Helmet", [("witchking_helmet",0)], itp_type_head_armor|itp_unique|itp_covers_head|itp_covers_beard, 0, 90000, weight(2.0)|abundance(5)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_armor ],
#occc tweaked roman helms
["ccc_helm_roma_cent", "Cent Helm", [("cent_helm",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor ],
["ccc_helm_roma_legio", "Legio Helm", [("legio_helm",0)], itp_type_head_armor, 0, 400, weight(2)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor ],
["ccc_helm_roma_praetor", "Praetor Helm", [("praetor_helm",0)], itp_type_head_armor, 0, 600, weight(2)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor ],
["ccc_helm_roma_coolusc", "Coolusc Helm", [("coolusc",0)], itp_type_head_armor, 0, 280, weight(2)|abundance(100)|head_armor(29)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor ],
#occc end
["ccc_helm_lichkinghelm", "Lich King Helm", [("LichKingHelm",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 95000, weight(2.0)|abundance(2)|head_armor(60)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate ],
["ccc_helm_guardian_crown", "Guardian Helm", [("talak_crown",0)], itp_type_head_armor|itp_covers_head, 0, 1000, weight(2)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate ],
["ccc_helm_guardian_crown_ornate", "Guardian Helm", [("talak_crown_ornate",0)], itp_type_head_armor|itp_covers_head, 0, 1020, weight(2)|abundance(100)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate ],
["ccc_helm_scullhead4", "Skull Head", [("scullhead4",0)], itp_type_head_armor|itp_covers_beard, 0, 360, weight(2)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_skull_helmet", "Skull Helmet", [("skull_helmet",0)], itp_type_head_armor|itp_covers_beard, 0, 360, weight(2)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["ccc_helm_monster_1", "Monster Head", [("2cn_hed_disa_0d",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 360, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_monster_2", "Monster Head", [("2cn_hed_cora_0d",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 360, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_viking_1", "Viking Helm", [("qm_hlh_m01a_0",0)], itp_type_head_armor, 0, 360, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_viking_2", "Viking Helm", [("qm_hlh_m01b_0",0)], itp_type_head_armor, 0, 360, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_viking_3", "Viking Light Helm", [("qm_hlh_m04a_0",0)], itp_type_head_armor, 0, 200, weight(2.75)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_viking_4", "Viking Light Helm", [("qm_hlh_m04b_0",0)], itp_type_head_armor, 0, 200, weight(2.75)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_viking_5", "Einherjar Helm", [("helmet1",0)], itp_type_head_armor, 0, 10240, weight(3)|abundance(100)|head_armor(65)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_dao_1", "Calrador Elven Helm", [("2DAO_HELM",0)], itp_type_head_armor|itp_wooden_attack, 0, 7500, weight(2.75)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
#["ccc_helm_dao_2", "Gurdian Helm", [("3DAO_HELM",0)], itp_type_head_armor|itp_merchandise, 0, 1524, weight(2.75)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_dao_3", "Nord Guard Helm", [("6DAO_HELM",0)], itp_type_head_armor|itp_merchandise, 0, 1524, weight(2.75)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
#buffed knights helm occc
["ccc_helm_dao_4", "Knight Helm", [("7DAO_HELM",0)], itp_type_head_armor, 0, 1000, weight(2.75)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_dao_5", "Calrador Knight Helm", [("9DAO_HELM",0)], itp_type_head_armor, 0, 2000, weight(2.75)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_dao_6", "Helm", [("hm_hlh_m02b_0",0)], itp_type_head_armor, 0, 360, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_dao_7", "Helm", [("qm_hlf_t01a_0",0)], itp_type_head_armor, 0, 360, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_dao_8", "Helm", [("pn_hlf_s02a_0d",0)], itp_type_head_armor, 0, 360, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_legion_1", "Legion Helm", [("legion_helmet",0)], itp_type_head_armor, 0, 600, weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
#["ccc_helm_legion_2", "Legion Helm", [("legion_helmet2",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(2.75)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_legion_3", "Legion Helm", [("legiondragon_helmet",0)], itp_type_head_armor, 0, 700, weight(2.75)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],

["ccc_helm_east_black_sar_helmet1", "Black Saradin Helmet", [("black_sar_helmet1",0)], itp_type_head_armor, 0, 300, weight(2)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_east_brass_veil_helm", "Brass Veil Helm", [("brass_veil_helm",0)], itp_type_head_armor, 0, 900, weight(2)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],#buffed
["ccc_helm_east_khergit_kheshig_helmet", "Kheshig Helmet", [("khergit_kheshig_helmet",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_east_khergit_noken_helmet", "Kheshig Helmet", [("khergit_noken_helmet",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_east_sar_helmet2_brass", "Saladin Helmet", [("sar_helmet2_brass",0)], itp_type_head_armor, 0, 700, weight(2)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_east_sar_helmet5", "Saladin Helmet", [("sar_helmet5",0)], itp_type_head_armor, 0, 700, weight(2)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_east_tuareg_helmet_black", "Tuareg", [("tuareg_helmet_black",0)], itp_type_head_armor, 0, 100, weight(2)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_east_tuareg_open_black", "Tuareg", [("tuareg_open_black",0)], itp_type_head_armor, 0, 100, weight(2)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_turban_assassin", "Assassin Turban", [("assassin_helmet",0)], itp_merchandise|itp_type_head_armor|itp_covers_beard, 0, 28, weight(1)|abundance(2)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(6), imodbits_cloth ],
["ccc_helm_turban_assassin_2", "Assassin Turban", [("assassin_helmet2",0)], itp_merchandise|itp_type_head_armor|itp_covers_beard, 0, 28, weight(2)|abundance(3)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_cloth ],
#russian
["ccc_helm_rus_nikolskoe_helm", "Nikolskoe helm", [("nikolskoe_helm",0), ("inv_nikolskoe_helm",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature  ,0, 520 , weight(5)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
["ccc_helm_rus_novogrod_helm", "Novogrod helm", [("novogrod_helm",0), ("inv_novogrod_helm",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 480 , weight(4)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(14) ,imodbits_plate ],
["ccc_helm_rus_gnezdovo_helm_a", "Gnezdovo helm", [("gnezdovo_helm_a",0), ("inv_gnezdovo_helm_a",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 450 , weight(3)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(12) ,imodbits_plate ],
["ccc_helm_rus_gnezdovo_helm_b", "Gnezdovo helm", [("gnezdovo_helm_a",0), ("inv_gnezdovo_helm_b",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 450 , weight(3)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(12) ,imodbits_plate ],
["ccc_helm_rus_tagancha_helm_a", "Tagancha helm", [("tagancha_helm_a",0), ("inv_tagancha_helm_a",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 450 , weight(2)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(12) ,imodbits_plate ],
["ccc_helm_rus_tagancha_helm_b", "Tagancha helm", [("tagancha_helm_b",0), ("inv_tagancha_helm_b",ixmesh_inventory)], itp_merchandise| itp_type_head_armor | itp_attach_armature,0, 450 , weight(5)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_plate ],
#Narf
["ccc_helm_pigface_klappvisor", "Pigface Bascinet", [("pigface_klappvisor",0)], itp_merchandise| itp_type_head_armor|itp_covers_head,0, 1580 , weight(2.75)|abundance(100)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["ccc_helm_pigface_klappvisor_open", "Pigface Bascinet", [("pigface_klappvisor_open",0)], itp_merchandise|itp_type_head_armor   ,0, 1680 , weight(2.75)|abundance(100)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["ccc_helm_hounskull", "Hounskull Bascinet", [("hounskull",0)], itp_merchandise| itp_type_head_armor|itp_covers_head,0, 1380 , weight(2.75)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["occc_helm_pigface_klappvisor_b", "Black Pigface Bascinet", [("pigface_klappvisor_b",0)], itp_merchandise| itp_type_head_armor|itp_covers_head,0, 1580 , weight(2.75)|abundance(100)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["occc_helm_hounskull_b", "Black Hounskull Bascinet", [("hounskull_b",0)], itp_merchandise| itp_type_head_armor|itp_covers_head,0, 1380 , weight(2.75)|abundance(100)|head_armor(58)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],

#spak
["ccc_helm_spack_bk_1", "Twlight Knight helm", [("twilight_helm",0)], itp_type_head_armor|itp_covers_head,0, 2500 , weight(2.75)|abundance(100)|head_armor(67)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["ccc_helm_spack_bk_2", "Twlight Knight helm", [("twilighthelm2",0)], itp_type_head_armor|itp_covers_head,0, 2500 , weight(2.75)|abundance(100)|head_armor(67)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["ccc_helm_spak_bear_1", "White Bear Helm", [("bear2_helmet",0)], itp_type_head_armor, 0, 180, weight(1)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
["ccc_helm_spak_bear_2", "Bear Helm", [("bear_helmet",0)], itp_type_head_armor, 0, 180, weight(1)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],
#kengeki
["ccc_helm_ken_sistercape_1", "Sister Cape", [("sistercape",0)], itp_type_head_armor, 0, 2040, weight(1)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_helm_ken_sistercape_2", "Sister Cape", [("sistercape2",0)], itp_type_head_armor, 0, 2040, weight(1)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["ccc_helm_val_valkyrie_1", "Valkyrie Circlet", [("valhelm1",0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 3024, abundance(500)|weight(1)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_helm_val_valkyrie_2", "Valkyrie Circlet", [("valhelm2",0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 3024, abundance(500)|weight(1)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_helm_val_valkyrie_3", "Valkyrie Circlet", [("valhelm3",0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 3024, abundance(500)|weight(1)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_helm_val_valkyrie_4", "Valkyrie Circlet", [("valhelm5",0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 3024, abundance(500)|weight(1)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_helm_val_valkyrie_5", "Valkyrie Circlet", [("valhelm5b",0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 3024, abundance(500)|weight(1)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_helm_val_valkyrie_6", "Valkyrie Circlet", [("valhelm5c",0)], itp_merchandise|itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 3024, abundance(500)|weight(1)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_armor,[],[fac_valkyrie] ],
["ccc_helm_val_valkyrie_helm", "Valkyrie Helm", [("valhelm4",0)], itp_merchandise|itp_type_head_armor|itp_covers_beard, 0, 2040, abundance(500)|weight(2.75)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate,[],[fac_valkyrie] ],

["ccc_helm_ken_circlet_1", "Circlet", [("circlet",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 170, weight(2)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccc_helm_ken_circlet_2", "Circlet", [("knight_circlet",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 300, weight(2)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_plate ],
["ccc_helm_ken_circlet_3", "Circlet", [("knight_circlet2",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 300, weight(2)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_plate ],
["ccc_helm_ken_circlet_heroine", "Heroine Circlet", [("circlet",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair|itp_unique, 0, 80000, weight(2)|abundance(100)|head_armor(70)|body_armor(10)|leg_armor(10), imodbits_armor ],
["ccc_helm_ken_crown", "Crown", [("crown_y",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 8024, weight(3)|abundance(100)|head_armor(30)|body_armor(1)|leg_armor(1), imodbits_plate ],
#occc model replace
["ccc_helm_ken_silver_knight_1", "Silver Knight Helmet", [("x_burgonet_trim",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 1200, weight(2.75)|abundance(100)|head_armor(59)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["ccc_helm_ken_silver_knight_2", "Silver Knight Helmet", [("x_burgonet2",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 1200, weight(2.75)|abundance(100)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],

#occc end

["ccc_helm_ken_silver_knight_3", "Silver Knight Helmet", [("slv_burgonet_coif",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 1200, weight(2.75)|abundance(100)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["ccc_helm_ken_black_knight_1", "Black Knight Helmet", [("x_burgonet2_b",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 1200, weight(2.75)|abundance(100)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
#["ccc_helm_ken_black_knight_2", "Black Knight Helmet", [("knight_helm_black_Steel",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 2040, weight(2.75)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
#["ccc_helm_ken_black_knight_3", "Black Knight Helmet", [("knightarmet2",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 2040, weight(2.75)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
#["ccc_helm_ken_black_knight_4", "Black Knight Helmet", [("visored_barbutte",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 2040, weight(2.75)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["ccc_helm_ken_dd_1", "Death Knight Helmet", [("uwhelm",0)], itp_type_head_armor|itp_covers_beard, 0, 1000, weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["ccc_helm_ken_dd_2", "Death Knight Helmet", [("uwhelm2",0)], itp_type_head_armor|itp_covers_beard, 0, 1000, weight(2.75)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
#JP
#Sinobi
#["ccc_helm_jp_sinobi_fukumen_b", "Fukumen Black", [("fukumen_black",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 700, weight(2)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0), imodbits_cloth ],
#["ccc_helm_jp_sinobi_hannya_1", "Hannya men", [("hannyamen1",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 700, weight(2)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0), imodbits_cloth ],
["ccc_helm_jp_sinobi_hannya_2", "Hannya men", [("hannyamen2",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 80, weight(2)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0), imodbits_cloth ],
#["ccc_helm_jp_sinobi_kitune_1", "Kitune men", [("kitunemen1",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 700, weight(2)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccc_helm_jp_sinobi_kitune_2", "Kitune men", [("kitunemen2",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 80, weight(2)|abundance(100)|head_armor(15)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccc_helm_jp_headgear_1", "Head Gear", [("headgear",0)], itp_type_head_armor|itp_doesnt_cover_hair|itp_civilian|itp_fit_to_head, 0, 100, weight(2)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_armor ],
#["ccc_helm_jp_headgear_2", "Head Gear", [("headgear2",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 700, weight(2)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccc_helm_jp_headgear_3", "Head Gear", [("armored_headband",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 100, weight(1.5)|abundance(100)|head_armor(23)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccc_helm_jp_headgear_4", "Head Gear", [("armored_headband2",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 100, weight(1.5)|abundance(100)|head_armor(23)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccc_helm_jp_headgear_5", "Happi", [("happuri",0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 100, weight(2)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0), imodbits_armor ],
#["ccc_helm_jp_kasa", "Kasa", [("kasa2",0)], itp_type_head_armor|itp_fit_to_head, 0, 70, weight(1)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccc_helm_jp_kasa", "Jin_Kasa", [("kasa2",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair,0, 65 , weight(1.5)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0) ,imodbits_cloth, [], [fac_kingdom_9,fac_bushido_order] ],
["ccd_kasa_ronin", "Amigasa", [("ccd_kasa_ronin",0)], itp_type_head_armor|itp_doesnt_cover_hair, 0, 65, weight(1)|abundance(100)|head_armor(17)|body_armor(0)|leg_armor(0), imodbits_armor ],
["ccd_kasa_komusou", "Tengai", [("ccd_kasa_komusou",0)], itp_type_head_armor|itp_doesnt_cover_hair, 0, 65, weight(1)|abundance(100)|head_armor(19)|body_armor(0)|leg_armor(0), imodbits_armor ],
#busi
["strange_helmet", "Strange Helmet", [("samurai_helmet",0)], itp_type_head_armor|itp_merchandise, 0, 500, weight(2)|abundance(220)|head_armor(34)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_helm_jp_casque_samurai01n", "Aka Kabuto", [("kabuto1b",0)], itp_type_head_armor|itp_merchandise, 0, 900, weight(2)|abundance(220)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_helm_jp_casque_samurai02n", "Kabuto", [("kabuto3",0)], itp_type_head_armor|itp_merchandise, 0, 500, weight(2)|abundance(220)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_helm_jp_casque_samurai03n", "Kabuto", [("kabuto3b",0)], itp_type_head_armor|itp_merchandise, 0, 500, weight(2)|abundance(220)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_helm_jp_casque_samurai04n", "Siro Kabuto", [("kabuto4_slv",0)], itp_type_head_armor|itp_merchandise, 0, 500, weight(2)|abundance(220)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],

["ccc_helm_jp_casque_samurai01_old", "Kabuto", [("casque_samurai01",0)], itp_type_head_armor, 0, 980, weight(2)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_jp_casque_samurai02_old", "Kabuto", [("casque_samurai02",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],
["ccc_helm_jp_casque_samurai01", "Kabuto", [("kawari_kabuto1",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["ccc_helm_jp_casque_samurai02", "Kabuto", [("kawari_kabuto2",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["ccc_helm_jp_casque_samurai03", "Kabuto", [("kawari_kabuto3",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["ccc_helm_jp_casque_samurai04", "Siro Kabuto", [("kawari_kabuto4",0)], itp_type_head_armor, 0, 600, weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["ccc_helm_jp_casque_samurai05", "Kabuto", [("kawari_kabuto5",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["ccc_helm_jp_casque_samurai06", "Kabuto", [("kawari_kabuto6",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["ccc_helm_jp_casque_samurai07", "Kabuto", [("kawari_kabuto7",0)], itp_type_head_armor, 0, 500, weight(2)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["ccc_helm_bar_berserk_helms", "BerserkHelmS", [("BerserkHelmS",0)], itp_type_head_armor|itp_covers_beard, 0, 25000, weight(3)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(15), imodbits_plate ],
["ccc_helm_bar_berserk_helmw", "BerserkHelmW", [("BerserkHelmW",0)], itp_type_head_armor|itp_covers_beard, 0, 25000, weight(3)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(15), imodbits_plate ],

["ccd_rus_kyiv_dragoons_all", "Russian Dragoon Helmet", [("rus_kyiv_dragoons_all",0)], itp_merchandise| itp_type_head_armor |itp_civilian|itp_fit_to_head ,0, 300, weight(0.5)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_2] ],
["ccd_rus_kyiv_dragoons_trumpeter", "Russian Dragoon Trumpeter Helmet", [("rus_kyiv_dragoons_trumpeter",0)], itp_merchandise| itp_type_head_armor |itp_civilian|itp_fit_to_head ,0, 300, weight(0.5)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_2] ],
["ccd_rus_arty_shako_nco", "Russian Artillery Shako", [("rus_arty_sarge_shako",0)], itp_merchandise| itp_type_head_armor |itp_civilian|itp_fit_to_head ,0, 300, weight(0.5)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_2] ],
["ccd_rus_hussar_shako_officer", "Russian Hussar Shako", [("rus_hussard_captain_shako",0)], itp_merchandise| itp_type_head_armor |itp_civilian|itp_fit_to_head ,0, 400, weight(0.5)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_2] ],
["ccd_rus_opol_hat_ranker", "Opolocheniye Hat", [("rus_opol_hat",0)], itp_merchandise| itp_type_head_armor |itp_civilian|itp_fit_to_head ,0, 300, weight(0.5)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_2] ],

#["ccd_hachigane", "Hachigane", [("headgear", 0)], itp_type_head_armor|itp_doesnt_cover_hair, 0, 512, weight(1)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],  ## cave09  ->ccc_helm_jp_headgear_1
#["ccd_knight_circlet", "Kinght Circlet", [("knight_circlet", 0)], itp_type_head_armor|itp_doesnt_cover_hair,0, 512, weight(1.0)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],  ## cave09  ->ccc_helm_ken_circlet_2
#["ccd_circlet", "Circlet", [("circlet", 0)], itp_type_head_armor|itp_doesnt_cover_hair, 0, 512, weight(1.0)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],  ## cave09  ->ccc_helm_ken_circlet_1
#["ccd_crown_y", "Crown", [("crown_y", 0)], itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair, 0, 10000, weight(1)|head_armor(40)|body_armor(2)|leg_armor(2) ,imodbits_cloth ],  ## cave09  ->ccc_helm_ken_crown
["ccd_crown_coif", "Crown With Coif", [("crown_coif",0)], itp_type_head_armor, 0, 12000, weight(1.5)|head_armor(40)|body_armor(2)|leg_armor(2)|difficulty(7) ,imodbits_armor ],
["ccd_noel_helmet", "Noel Cap", [("noel_helmet", 0)], itp_type_head_armor|itp_civilian|itp_fit_to_head, 0, 70, weight(0.5)|head_armor(5)|body_armor(4)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["ccd_helm_horn_red", "Red Horn Helm with Fur", [("ccd_helm_horn_red",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 4096, weight(3)|head_armor(51)|body_armor(1)|leg_armor(0)|difficulty(4) ,imodbits_plate ],

["ccc_helm_ghost_helm1", "Ghost Helm", [("casque_samurai02",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(2)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_ghost_helm2", "Ghost Helm", [("shahi",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(2)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["ccc_helm_ghost_helm3", "Ghost Helm", [("talak_sutton_hoo",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(2)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_armor ],
["ccc_helm_ghost_helm4", "Ghost Helm", [("talak_spangenhelm",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(2)|abundance(100)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_armor ],

#boots
#Cloth
["wrapping_boots", "Wrapping Boots", [("wrapping_boots_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 3, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["woolen_hose", "Woolen Hose", [("woolen_hose_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 6, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["blue_hose", "Blue Hose", [("blue_hose_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 11, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(3)|difficulty(0), imodbits_cloth ],
["ankle_boots", "Ankle Boots", [("ankle_boots_a_new",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 75, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["sarranid_boots_a", "Sarranid Shoes", [("sarranid_shoes",0)], itp_type_foot_armor|itp_attach_armature|itp_civilian, 0, 30, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(5)|difficulty(0), imodbits_cloth ],

#Hide, Fur
["hunter_boots", "Hunter Boots", [("hunter_boots_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 19, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["hide_boots", "Hide Boots", [("hide_boots_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 34, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["nomad_boots", "Nomad Boots", [("nomad_boots_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 90, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(6)|difficulty(0), imodbits_cloth ],

#Leathers
["light_leather_boots", "Light Leather Boots", [("light_leather_boots",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 91, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["leather_boots", "Leather Boots", [("leather_boots_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 174, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["sarranid_boots_b", "Sarranid Leather Boots", [("sarranid_boots",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 120, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(6)|difficulty(0), imodbits_cloth ],
["khergit_leather_boots", "Khergit Leather Boots", [("khergit_leather_boots",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 120, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ],
#OSP Clothing Boots
["ccc_leather_boots", "Leather Boots", [("boot_slim_brown_L",0)], itp_type_foot_armor|itp_civilian, 0, 91, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["ccc_black_boots", "Black Boots", [("boot_slim_black_L",0)], itp_type_foot_armor|itp_civilian, 0, 91, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["ccc_white_boots", "White Boots", [("boot_slim_white_L",0)], itp_type_foot_armor|itp_civilian, 0, 91, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ],

#Mail
["khergit_guard_boots", "Khergit Guard Boots", [("lamellar_boots_a",0)], itp_type_foot_armor|itp_attach_armature, 0, 254, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["splinted_leather_greaves", "Splinted Leather Greaves", [("leather_greaves_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 310, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(13)|difficulty(0), imodbits_armor ],
["mail_chausses", "Mail Chausses", [("mail_chausses_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 530, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(14)|difficulty(0), imodbits_armor ],
["sarranid_boots_d", "Sarranid Mail Boots", [("sarranid_mail_chausses",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 920, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0), imodbits_armor ],
["mail_boots", "Mail Boots", [("mail_boots_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 1250, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(8), imodbits_armor ],

#Plate
["sarranid_boots_c", "Plated Boots", [("sarranid_camel_boots",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 280, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0), imodbits_plate ],
["splinted_greaves", "Splinted Greaves", [("splinted_greaves_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 853, weight(2.75)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(7), imodbits_armor ],
["iron_greaves", "Iron Greaves", [("iron_greaves_a",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 1470, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(23)|difficulty(9), imodbits_armor ],
["plate_boots", "Plate Boots", [("plate_boots",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 1470, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(23)|difficulty(9), imodbits_plate ],
["black_greaves", "Black Greaves", [("black_greaves",0)], itp_type_foot_armor|itp_attach_armature, 0, 1961, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(25)|difficulty(0), imodbits_armor ],

["ccc_boots_roma_caligae", "Caligae", [("caligae",0)], itp_type_foot_armor|itp_attach_armature|itp_covers_legs, 0, 530, weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0), imodbits_armor ],
["ccc_greaves_roma_greek", "Greek Greaves", [("greek_greaves",0)], itp_type_foot_armor|itp_attach_armature, 0, 1961, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(0), imodbits_armor ],
["ccc_greaves_roma_gutter", "Gutter Greave", [("guttergreave",0)], itp_type_foot_armor|itp_attach_armature, 0, 1270, weight(1.8)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0), imodbits_armor ],

["ccc_greaves_steel", "Steel Greaves", [("steel_greaves",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 2300, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(11), imodbits_plate ],
["ccc_greaves_steel_b", "Black Steel Greaves", [("steel_greaves_b",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 2300, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(11), imodbits_plate ],
["ccc_greaves_shynbaulds", "Shynbaulds", [("shynbaulds",0)], itp_type_foot_armor|itp_attach_armature, 0, 2500, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(12), imodbits_plate ],
["ccc_greaves_black", "Black Greaves", [("black_greaves",0)], itp_type_foot_armor|itp_attach_armature, 0, 2500, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0), imodbits_plate ],

#spak
["ccc_greaves_spak_bear", "Bear Greaves", [("bear_boots",0)], itp_type_foot_armor|itp_attach_armature, 0, 1570, weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(25)|difficulty(0), imodbits_armor ],
["ccc_greaves_spak_silver_plate", "Silver Plate Greaves", [("plate_boots2",0)], itp_type_foot_armor|itp_attach_armature|itp_covers_legs, 0, 2461, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0), imodbits_plate ],
["ccc_greaves_spak_plate", "Plate Greaves", [("plate_boots3",0)], itp_type_foot_armor|itp_attach_armature, 0, 2661, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0), imodbits_plate ],

["ccc_greaves_east_brass_boots", "Saladin Boots", [("brass_boots",0)], itp_type_foot_armor|itp_attach_armature, 0, 2461, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0), imodbits_armor ],
["ccc_greaves_east_brass_mail_boots", "Saladin Boots", [("brass_mail_boots",0)], itp_type_foot_armor|itp_attach_armature, 0, 2361, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(0), imodbits_armor ],
["ccc_greaves_rus_shoes", "Rus Ankle Boots", [("rus_shoes",0)], itp_type_foot_armor |itp_civilian  | itp_attach_armature,0,75 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0) ,imodbits_cloth ],
["ccc_greaves_rus_cav_boots", "Rus Cavalry Boots", [("rus_cav_boots",0)], itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,15 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0) ,imodbits_cloth ],

["ccc_val_greaves_valkyrie_1", "Valkyrie Greaves", [("val_boots",0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0, 2361, abundance(500)|weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0), imodbits_plate,[],[fac_valkyrie] ],
["ccc_val_greaves_valkyrie_2", "Valkyrie Greaves", [("val_boots_2",0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0, 2361, abundance(500)|weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0), imodbits_plate,[],[fac_valkyrie] ],
["ccc_greaves_death_knight", "Death Knight Greaves", [("uw_greaves",0)], itp_type_foot_armor|itp_attach_armature, 0, 5024, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(34)|difficulty(0), imodbits_plate ],
["ccc_greaves_ken_silver_plate", "Silver Plate Greaves", [("slv_greaves",0)], itp_type_foot_armor|itp_attach_armature|itp_covers_legs, 0, 2361, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0), imodbits_plate ],

#JP
["strange_boots", "Strange Boots", [("samurai_boots",0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0, 465, weight(1)|abundance(230)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0), imodbits_cloth, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_greaves_jp_bottes_samurai01", "Suneate", [("bottes_samurai01",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(1)|abundance(10)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0), imodbits_cloth ],
["ccc_greaves_jp_bottes_samurai01", "Suneate", [("suneate1",0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0, 1200, weight(1)|abundance(230)|head_armor(0)|body_armor(0)|leg_armor(24)|difficulty(0), imodbits_cloth, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_greaves_jp_bottes_samurai02", "Suneate", [("bottes_samurai02",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(1)|abundance(10)|head_armor(0)|body_armor(0)|leg_armor(26)|difficulty(0), imodbits_cloth ],
#["ccc_greaves_jp_bottes_samurai02", "Suneate", [("suneate2",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(26)|difficulty(0), imodbits_cloth ],
["ccc_greaves_jp_bottes_samurai03", "Suneate", [("suneate3",0)], itp_merchandise|itp_type_foot_armor|itp_attach_armature, 0, 2461, weight(1)|abundance(230)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0), imodbits_cloth, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_greaves_jp_zinbaori_1", "Zinbaori", [("jinbaori_suneate_1",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(2)|abundance(0)|head_armor(0)|body_armor(6)|leg_armor(28)|difficulty(0), imodbits_cloth ],
["ccc_greaves_jp_zinbaori_1", "Busyo_Jinbaori_with_Suneate", [("jinbaori_suneate_1",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 1770 , weight(5)|abundance(170)|head_armor(0)|body_armor(6)|leg_armor(28)|difficulty(12) ,imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_greaves_jp_zinbaori_2", "Siro Zinbaori", [("jinbaori_suneate_2",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(2)|abundance(0)|head_armor(0)|body_armor(6)|leg_armor(28)|difficulty(0), imodbits_cloth ],
["ccc_greaves_jp_zinbaori_2", "Busyo_Jinbaori_with_Suneate", [("jinbaori_suneate_2",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 1770 , weight(5)|abundance(170)|head_armor(0)|body_armor(6)|leg_armor(28)|difficulty(12) ,imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_greaves_jp_zinbaori_3", "Zinbaori", [("jinbaori_suneate_4",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(2)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(0), imodbits_cloth ],
["ccc_greaves_jp_zinbaori_3", "Jinbaori_with_Suneate", [("jinbaori_suneate_4",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 870 , weight(4)|abundance(180)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(10) ,imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_greaves_jp_zinbaori_4", "Zinbaori", [("jinbaori_suneate_5",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(2)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(0), imodbits_cloth ],
["ccc_greaves_jp_zinbaori_4", "Jinbaori_with_Suneate", [("jinbaori_suneate_5",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 870 , weight(4)|abundance(180)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(10) ,imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_greaves_jp_zinbaori_5", "Zinbaori", [("jinbaori_suneate_6",0)], itp_type_foot_armor|itp_attach_armature, 0, 700, weight(2)|abundance(100)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(0), imodbits_cloth ],
["ccc_greaves_jp_zinbaori_5", "Jinbaori_with_Suneate", [("jinbaori_suneate_6",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 870 , weight(4)|abundance(180)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(10) ,imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["ccc_greaves_jp_warazi", "Warazi", [("waraji",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 54 , weight(0.6)|abundance(250)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccd_waraji", "Waraji", [("waraji", 0)], itp_type_foot_armor|itp_civilian|itp_attach_armature, 0, 128, weight(0.6)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_cloth ],  ## cave09  ->ccc_greaves_jp_warazi

["ccc_greaves_bar_boots", "BerserkBoots", [("BerserkBoots",0)], itp_type_foot_armor|itp_attach_armature, 0, 25000, weight(2)|abundance(10)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0), imodbits_plate ],

#hand
["leather_gloves", "Leather Gloves", [("leather_gloves_L",0)], itp_type_hand_armor|itp_merchandise, 0, 90, weight(0.25)|abundance(120)|body_armor(2)|difficulty(0), imodbits_cloth ],
#heavy hand
["mail_mittens", "Mail Mittens", [("mail_mittens_L",0)], itp_type_hand_armor|itp_merchandise, 0, 350, weight(0.5)|abundance(100)|body_armor(4)|difficulty(0), imodbits_armor ],
["scale_gauntlets", "Scale Gauntlets", [("scale_gauntlets_b_L",0)], itp_type_hand_armor|itp_merchandise, 0, 710, weight(0.75)|abundance(100)|body_armor(5)|difficulty(0), imodbits_armor ],
["lamellar_gauntlets","Lamellar Gauntlets", [("scale_gauntlets_a_L",0)], itp_merchandise|itp_type_hand_armor,0, 910, weight(0.9)|abundance(100)|body_armor(6)|difficulty(0),imodbits_armor],
["gauntlets","Gauntlets", [("gauntlets_L",0),("gauntlets_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor,0, 1040, weight(1.0)|abundance(100)|body_armor(7)|difficulty(0),imodbits_armor],

["ccc_mail_mittens_black", "Black Mail Mittens", [("dmail_mitten_L",0)], itp_type_hand_armor, 0, 350, weight(0.5)|abundance(100)|body_armor(4)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_wisby_gauntlets_black", "Splinted Leather Gauntlets", [("wisby_gauntlets_black_L",0)], itp_type_hand_armor|itp_merchandise, 0, 860, weight(0.75)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_wisby_red", "Splinted Leather Gauntlets", [("wisby_gauntlets_red_L",0)], itp_type_hand_armor|itp_merchandise, 0, 860, weight(0.75)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_hourglass_gauntlets","Hourglass Gauntlets", [("hourglass_gauntlets_L",0)], itp_merchandise|itp_type_hand_armor,0, 990, weight(1.0)|abundance(100)|body_armor(7)|difficulty(0),imodbits_armor],
["ccc_hourglass_gauntlets_ornate","Ornate Hourglass Gauntlets", [("hourglass_gauntlets_ornate_L",0)], itp_merchandise|itp_type_hand_armor,0, 1190, weight(1.0)|abundance(100)|body_armor(7)|difficulty(0),imodbits_armor],
["ccc_gauntlets_mail", "Mail Gauntlets", [("mail_gauntlets_R",0),("mail_gauntlets_L",imodbit_reinforced)], itp_type_hand_armor, 0, 860, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_bnw", "Bnw Gauntlet", [("bnw_gauntlet_R",0),("bnw_gauntlet_L",imodbit_reinforced)], itp_type_hand_armor, 0, 860, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_plate_mittens", "Plate Mittens", [("plate_mittens_R",0),("plate_mittens_L",imodbit_reinforced)], itp_type_hand_armor, 0, 990, weight(2)|abundance(100)|body_armor(8)|difficulty(0), imodbits_plate ],
["ccc_plate_mittens_b", "Black Plate Mittens", [("plate_mittens_b_R",0),("plate_mittens_b_L",imodbit_reinforced)], itp_type_hand_armor, 0, 990, weight(2)|abundance(100)|body_armor(8)|difficulty(0), imodbits_plate ],

#spak
["ccc_gauntlets_spak_dark", "Dark Gauntlet", [("11gauntlets_R",0),("11gauntlets_L",imodbit_reinforced)], itp_type_hand_armor, 0, 860, weight(2)|abundance(100)|body_armor(8)|difficulty(0), imodbits_plate ],
["ccc_gauntlets_spak_bear", "Bear Gauntlet", [("beargauntlets_R",0),], itp_type_hand_armor, 0, 700, weight(2)|abundance(100)|body_armor(7)|difficulty(0), imodbits_plate ],
["ccc_gauntlets_spak_bk", "Black Gauntlet", [("twilight_gloves_R",0),("twilight_gloves_L",imodbit_reinforced)], itp_type_hand_armor, 0, 860, weight(2)|abundance(100)|body_armor(8)|difficulty(0), imodbits_plate ],

#East
["ccc_gauntlets_east_brass_gauntlets", "Saladin Gauntlets", [("brass_l_gauntlets_R",0),("brass_l_gauntlets_L",imodbit_reinforced)], itp_type_hand_armor, 0, 600, weight(1.5)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_east_brass_s_gauntlets", "Saladin Gauntlets", [("brass_s_gauntlets_R",0),("brass_s_gauntlets_L",imodbit_reinforced)], itp_type_hand_armor, 0, 600, weight(1.5)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],

#Kengeki
#["ccc_gauntlets_ken_black", "Black Gauntlet", [("blk_gauntlet_a_R",0),("blk_gauntlet_a_L",imodbit_reinforced)], itp_type_hand_armor, 0, 700, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_ken_black_g", "Black Glove", [("blk_glove_R",0),("blk_glove_L",imodbit_reinforced)], itp_type_hand_armor, 0, 500, weight(1.0)|abundance(100)|body_armor(5)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_ken_blue", "blue Gauntlet", [("blue_gauntlet_a_R",0),("blue_gauntlet_a_L",imodbit_reinforced)], itp_type_hand_armor, 0, 600, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_ken_blue_g", "blue Gauntlet", [("blue_gauntlet_R",0),("blue_gauntlet_L",imodbit_reinforced)], itp_type_hand_armor, 0, 500, weight(1.0)|abundance(100)|body_armor(5)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_ken_slv", "Slv Gauntlet", [("slv_gauntlet_a_R",0),("slv_gauntlet_a_L",imodbit_reinforced)], itp_type_hand_armor, 0, 600, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
#JP
["ccc_gauntlets_jp_tekkou", "Tekkou", [("f_tekkou1R",0),("f_tekkou1L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 400, weight(1.0)|abundance(200)|body_armor(4)|difficulty(0), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_gauntlets_jp_gants_samurai01", "Kote", [("gants_samurai01_R",0),("gants_samurai01_L",imodbit_reinforced)], itp_type_hand_armor, 0, 700, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_jp_gants_samurai01", "Kote", [("kote_y_R",0),("kote_y_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 600, weight(1.0)|abundance(200)|body_armor(6)|difficulty(0), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
#["ccc_gauntlets_jp_gants_samurai02", "Kote", [("gants_samurai02_R",0),("gants_samurai02_L",imodbit_reinforced)], itp_type_hand_armor, 0, 700, weight(1.0)|abundance(100)|body_armor(6)|difficulty(0), imodbits_armor ],
["ccc_gauntlets_jp_gants_samurai02", "Kote", [("tekkou_R",0),("tekkou_L",imodbit_reinforced)], itp_merchandise|itp_type_hand_armor, 0, 500, weight(1.0)|abundance(200)|body_armor(5)|difficulty(0), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],

["ccc_gauntlets_bar_berserk", "BerserkGauntlets", [("BerserkGauntlets_R",0),("BerserkGauntlets_L",imodbit_reinforced)], itp_type_hand_armor, 0, 25000, weight(1.0)|abundance(100)|body_armor(7)|difficulty(8), imodbits_armor ],

#horse
# Horses: sumpter horse/ pack horse, saddle horse, steppe horse, warm blood, geldling, stallion,   war mount, charger,
# Carthorse, hunter, heavy hunter, hackney, palfrey, courser, destrier.
## OCCC tweak - 8 more HP than default cave's HP setting.... this is still weaker than mm's setting
["sumpter_horse", "Sumpter Horse", [("sumpter_horse",0)], itp_type_horse|itp_merchandise, 0, 134, abundance(90)|hit_points(40)|body_armor(14)|difficulty(1)|horse_speed(30)|horse_maneuver(39)|horse_charge(28)|horse_scale(100), imodbits_horse_basic ],
["saddle_horse", "Saddle Horse", [("saddle_horse",0),("horse_c",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 240, abundance(90)|hit_points(40)|body_armor(10)|difficulty(1)|horse_speed(40)|horse_maneuver(54)|horse_charge(35)|horse_scale(104), imodbits_horse_basic ],
["steppe_horse", "Steppe Horse", [("steppe_horse",0)], itp_type_horse|itp_merchandise, 0, 192, abundance(80)|hit_points(40)|body_armor(10)|difficulty(2)|horse_speed(50)|horse_maneuver(61)|horse_charge(33)|horse_scale(98), imodbits_horse_basic, [], [fac_kingdom_2,fac_kingdom_3] ],
["arabian_horse_a", "Desert Horse", [("arabian_horse_a",0)], itp_type_horse|itp_merchandise, 0, 550, abundance(40)|hit_points(40)|body_armor(10)|difficulty(2)|horse_speed(52)|horse_maneuver(50)|horse_charge(47)|horse_scale(100), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_3,fac_kingdom_6] ],
["courser", "Courser", [("courser",0)], itp_type_horse|itp_merchandise, 0, 600, abundance(70)|body_armor(9)|hit_points(40)|difficulty(2)|horse_speed(60)|horse_maneuver(50)|horse_charge(45)|horse_scale(106), imodbits_horse_basic|imodbit_champion ],
["arabian_horse_b", "Sarranid Horse", [("arabian_horse_b",0)], itp_type_horse|itp_merchandise, 0, 700, abundance(80)|hit_points(40)|body_armor(10)|difficulty(3)|horse_speed(52)|horse_maneuver(58)|horse_charge(45)|horse_scale(100), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_6] ],
["hunter", "Hunter", [("hunting_horse",0),("saddle_horse",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 810, abundance(60)|hit_points(40)|body_armor(16)|difficulty(3)|horse_speed(56)|horse_maneuver(52)|horse_charge(55)|horse_scale(108), imodbits_horse_basic|imodbit_champion ],
["ccc_horse_courser_blackwhite", "Courser", [("sumpter_horse",0)], itp_type_horse|itp_merchandise, 0, 2048, abundance(10)|hit_points(40)|body_armor(12)|difficulty(4)|horse_speed(65)|horse_maneuver(70)|horse_charge(60)|horse_scale(108), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_3] ],
["ccc_horse_roma", "Good Saddle Horse", [("saddle_horse",0),("horse_c",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 1024, abundance(10)|hit_points(40)|body_armor(14)|difficulty(4)|horse_speed(60)|horse_maneuver(60)|horse_charge(65)|horse_scale(104), imodbits_horse_basic, [], [fac_kingdom_5] ],
["ccc_horse_valkyrie", "Valkyrie Horse", [("courser",0)], itp_merchandise|itp_type_horse, 0, 3048, abundance(500)|body_armor(10)|hit_points(45)|difficulty(4)|horse_speed(68)|horse_maneuver(68)|horse_charge(40)|horse_scale(140), imodbits_horse_basic|imodbit_champion,[],[fac_valkyrie] ],

#warhorse
## OCCC tweak  less HP than  mm's setting .... this is still stronger than default cave's HP setting
["warhorse", "War Horse", [("warhorse_chain",0),("warhorse",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 3000, abundance(50)|hit_points(49)|body_armor(45)|difficulty(4)|horse_speed(35)|horse_maneuver(38)|horse_charge(85)|horse_scale(110), imodbits_horse_basic|imodbit_champion ],
["charger", "Charger", [("charger_new",0),("charger3_new",imodbit_heavy),("charger",imodbit_spirited)], itp_type_horse|itp_merchandise, 0, 5000, abundance(40)|hit_points(49)|body_armor(35)|difficulty(4)|horse_speed(44)|horse_maneuver(44)|horse_charge(105)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1,fac_kingdom_5] ],
["warhorse_sarranid", "Sarranian War Horse", [("warhorse_sarranid",0)], itp_type_horse, 0, 4000, abundance(10)|hit_points(55)|body_armor(70)|difficulty(5)|horse_speed(27)|horse_maneuver(41)|horse_charge(90)|horse_scale(120), imodbit_heavy, [], [fac_kingdom_6] ],
["warhorse_steppe", "Steppe Charger", [("warhorse_steppe",0)], itp_type_horse|itp_merchandise, 0, 4000, abundance(10)|hit_points(55)|body_armor(50)|difficulty(8)|horse_speed(60)|horse_maneuver(50)|horse_charge(75)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_2,fac_kingdom_3] ],#occc HP 130->80 charge 80->65
["ccc_warhorse_imperial", "Imperial Warhorse", [("barded1W",0)], itp_type_horse, 0, 10000, abundance(10)|hit_points(55)|body_armor(50)|difficulty(5)|horse_speed(32)|horse_maneuver(41)|horse_charge(85), imodbits_horse_basic|imodbit_champion ],
["ccc_warhorse_knigth", "Knight War Horse", [("barded13W",0)], itp_type_horse, 0, 2048, abundance(20)|hit_points(65)|body_armor(40)|difficulty(5)|horse_speed(36)|horse_maneuver(49)|horse_charge(100), imodbits_horse_basic|imodbit_champion ],
["ccc_warhorse_roma", "Roma War Horse", [("Leather1W",0),("spakhorse_03",imodbits_horse_good)], itp_type_horse|itp_merchandise, 0, 4096, abundance(10)|hit_points(50)|body_armor(50)|difficulty(4)|horse_speed(40)|horse_maneuver(40)|horse_charge(95), imodbits_horse_basic|imodbit_champion ],
["ccc_warhorse_guardian", "Guardian War Horse", [("Platedw",0)], itp_type_horse, 0, 2048, abundance(10)|hit_points(65)|body_armor(60)|difficulty(5)|horse_speed(35)|horse_maneuver(25)|horse_charge(80), imodbits_horse_basic|imodbit_champion ],
["ccc_warhorse_warhorse1", "Heavy Charger", [("5warhorse_holy",0)], itp_type_horse, 0, 2048, abundance(10)|hit_points(55)|body_armor(45)|difficulty(5)|horse_speed(45)|horse_maneuver(52)|horse_charge(105), imodbits_horse_basic|imodbit_champion ],
["ccc_warhorse_kher_warhorse", "War Horse", [("MailleW",0)], itp_type_horse|itp_merchandise, 0, 4096, abundance(10)|hit_points(70)|body_armor(65)|difficulty(10)|horse_speed(55)|horse_maneuver(53)|horse_charge(100)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_3] ],
["ccc_warhorse_east_sar_warhorse1", "Saladin War Horse", [("sar_warhorse",0)], itp_type_horse, 0, 2048, abundance(10)|hit_points(65)|body_armor(70)|difficulty(5)|horse_speed(38)|horse_maneuver(55)|horse_charge(90)|horse_scale(122), imodbits_horse_basic|imodbit_champion ],
["ccc_warhorse_dark_knigth_load", "Dark War Horse", [("barded12W",0),("2imperial_warhorse",imodbits_horse_good)], itp_type_horse|itp_ignore_friction, 0, 60000, abundance(1)|hit_points(85)|body_armor(70)|difficulty(6)|horse_speed(38)|horse_maneuver(55)|horse_charge(210), imodbits_horse_good|imodbit_champion ],
["ccc_warhorse_bk_1", "Black Knight War Horse", [("twilight_horse",0)], itp_type_horse, 0, 5000, abundance(1)|hit_points(55)|body_armor(60)|difficulty(5)|horse_speed(55)|horse_maneuver(55)|horse_charge(109), imodbits_horse_good|imodbit_champion ],
["ccc_warhorse_valkyrie", "Valkyrie War Horse", [("war_horse_01",0)], itp_merchandise|itp_type_horse|itp_ignore_friction, 0, 5000, abundance(400)|hit_points(50)|body_armor(40)|difficulty(5)|horse_speed(58)|horse_maneuver(65)|horse_charge(80), imodbits_horse_good|imodbit_champion,[],[fac_valkyrie] ],
["ccc_warhorse_death", "Death War Horse", [("dd_armorcharger",0)], itp_type_horse|itp_ignore_friction, 0, 5000, abundance(1)|hit_points(55)|body_armor(65)|difficulty(5)|horse_speed(51)|horse_maneuver(55)|horse_charge(130), imodbits_horse_good|imodbit_champion ],
["ccd_charger_plate", "Charger Plate", [("charger_plate_1", 0),("horny_charger_plate",imodbits_horse_good)], itp_type_horse, 0, 8192, abundance(40)|hit_points(80)|body_armor(65)|difficulty(5)|horse_speed(47)|horse_maneuver(48)|horse_charge(130)|horse_scale(115), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1,fac_kingdom_5,fac_kingdom_7] ],
["ccd_warhorse_blacksilver", "Silver Head War Horse", [("armored_horse01LP52", 0)], itp_type_horse, 0, 8192, abundance(40)|hit_points(55)|body_armor(45)|difficulty(5)|horse_speed(60)|horse_maneuver(50)|horse_charge(110), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1,fac_kingdom_5,fac_kingdom_7] ],
#occc horses start
["occc_warhorse_knight_additional", "Elite Knight War Horse", [("war_horse_08",0)], itp_type_horse, 0, 2048, abundance(20)|hit_points(68)|body_armor(60)|difficulty(6)|horse_speed(50)|horse_maneuver(29)|horse_charge(110), imodbits_horse_basic|imodbit_champion ],
["occc_charger_new_1", "Swadian Charger", [("barded15W",0),("barded15W",imodbit_heavy),("barded15W",imodbit_spirited)], itp_type_horse|itp_merchandise, 0, 5000, abundance(40)|hit_points(52)|body_armor(45)|difficulty(4)|horse_speed(44)|horse_maneuver(44)|horse_charge(105)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1] ],
["occc_charger_new_2", "Swadian Charger", [("barded16W",0),("barded16W",imodbit_heavy),("barded16W",imodbit_spirited)], itp_type_horse|itp_merchandise, 0, 5000, abundance(40)|hit_points(52)|body_armor(45)|difficulty(4)|horse_speed(44)|horse_maneuver(44)|horse_charge(105)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1] ],
["occc_charger_new_3", "Swadian Charger", [("barded17W",0),("barded17W",imodbit_heavy),("barded17W",imodbit_spirited)], itp_type_horse|itp_merchandise, 0, 5000, abundance(40)|hit_points(52)|body_armor(45)|difficulty(4)|horse_speed(44)|horse_maneuver(44)|horse_charge(105)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1] ],
["occc_charger_new_4", "Swadian Charger", [("barded18W",0),("barded18W",imodbit_heavy),("barded18W",imodbit_spirited)], itp_type_horse|itp_merchandise, 0, 5000, abundance(40)|hit_points(52)|body_armor(45)|difficulty(4)|horse_speed(44)|horse_maneuver(44)|horse_charge(105)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1] ],
["occc_blue_sky_war_horse","Blue Sky War Horse", [("barded6W",0)], itp_merchandise|itp_type_horse, 0, 2200,abundance(20)|hit_points(45)|body_armor(28)|difficulty(4)|horse_speed(50)|horse_maneuver(49)|horse_charge(105)|horse_scale(107),imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_1,fac_kingdom_4]],
["occc_roman_clibanarii_horse", "Imperial Heavy Charger", [("warhorse_steppe_roman",0)], itp_type_horse, 0, 6000,
 abundance(5)|hit_points(60)|body_armor(57)|difficulty(5)|horse_speed(55)|horse_maneuver(46)|horse_charge(75)|horse_scale(112), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_5] ],
["occc_warhorse_teuton1", "Teutonic War Horse", [("heraldic_horse_1",0)], 
  itp_type_horse, 0, 6048, 
  abundance(20)|hit_points(60)|body_armor(46)|difficulty(5)|horse_speed(35)|horse_maneuver(45)|horse_charge(90), imodbits_horse_basic|imodbit_champion ],
["occc_warhorse_teuton2", "Teutonic War Horse", [("heraldic_horse_2",0)], 
  itp_type_horse, 0, 6048, 
  abundance(20)|hit_points(60)|body_armor(43)|difficulty(5)|horse_speed(37)|horse_maneuver(45)|horse_charge(88), imodbits_horse_basic|imodbit_champion ],
["occc_warhorse_teuton3", "Teutonic War Horse", [("heraldic_horse_3",0)], 
  itp_type_horse, 0, 7048, 
  abundance(20)|hit_points(65)|body_armor(50)|difficulty(6)|horse_speed(38)|horse_maneuver(46)|horse_charge(96), imodbits_horse_basic|imodbit_champion ],
["mm_romanhalfcata", "Half Cataphract Horse", [("romanhalfcata", 0),], itp_type_horse, 0, 4000, weight(3)|body_armor(26)|difficulty(3)|hit_points(45)|horse_maneuver(41)|horse_speed(58)|horse_charge(65), imodbits_none ],
["occc_hussar_horse", "Hussar's Horse", [("Hus",0)], itp_type_horse, 0, 4500, abundance(10)|hit_points(47)|body_armor(30)|difficulty(5)|horse_speed(60)|horse_maneuver(50)|horse_charge(120), imodbits_horse_basic|imodbit_champion ],
["occc_ney_hunter", "Ney's Horse", [("hunting_horse",0),("saddle_horse",imodbits_horse_good)], itp_type_horse, 0, 5000, abundance(60)|hit_points(40)|body_armor(5)|difficulty(5)|horse_speed(70)|horse_maneuver(62)|horse_charge(60)|horse_scale(118), imodbits_horse_basic|imodbit_champion,[], [fac_kingdom_3] ],

 #occc horses end

["ccc_camel_camel1", "Camel", [("camel",0)], itp_type_horse|itp_merchandise, 0, 2048, abundance(10)|hit_points(35)|body_armor(16)|difficulty(3)|horse_speed(65)|horse_maneuver(85)|horse_charge(20), imodbits_horse_basic|imodbit_champion, [], [fac_kingdom_6] ],
#horses end
#occc ridable creatures start 
#trample start
["occc_elephant1", "War Elephant", [("yf_daxiang", 0),], itp_type_horse|itp_merchandise, 0, 4000, weight(48)|body_armor(25)|abundance(1)|hit_points(350)|horse_maneuver(18)|horse_speed(38)|horse_charge(230)|horse_scale(150)|difficulty(2), imodbits_horse_basic|imodbit_timid, [], [fac_kingdom_6] ],
["occc_elephant2", "Elephant", [("yf_ydzx", 0),], itp_type_horse|itp_merchandise, 0, 4000, weight(48)|body_armor(15)|abundance(6)|hit_points(330)|horse_maneuver(26)|horse_speed(36)|horse_charge(225)|horse_scale(150)|difficulty(2), imodbits_horse_basic|imodbit_timid, [], [fac_kingdom_6] ],
["mm_mammoth", "Mammoth", [("mammoth", 0),], itp_type_horse, 0, 2000, weight(33)|abundance(90)|hit_points(400)|horse_maneuver(15)|horse_speed(30)|horse_charge(240)|horse_scale(155), imodbits_horse_basic|imodbit_timid ],
["occc_dinosaur_armored", "Armored Dinosaur", [("dark_basilisk", 0),], itp_type_horse, 0, 30000, weight(48)|body_armor(75)|abundance(1)|hit_points(150)|horse_maneuver(35)|horse_speed(42)|horse_charge(80)|horse_scale(114)|difficulty(8), imodbits_horse_basic|imodbit_timid ],
["occc_dinosaur", "Dinosaur", [("basilisk", 0),], itp_type_horse, 0, 25000, weight(48)|body_armor(50)|abundance(1)|hit_points(130)|horse_maneuver(42)|horse_speed(48)|horse_charge(70)|horse_scale(114)|difficulty(7), imodbits_horse_basic|imodbit_timid ],
["occc_trex", "T-REX", [("tirare", 0),], itp_type_horse, 0, 40000, weight(48)|body_armor(80)|abundance(1)|hit_points(500)|horse_maneuver(18)|horse_speed(43)|horse_charge(200)|horse_scale(150)|difficulty(10), imodbits_horse_basic|imodbit_timid ],
["occc_spider", "Spider", [("spider", 0),], itp_type_horse, 0, 2000, weight(33)|abundance(90)|hit_points(80)|horse_maneuver(150)|horse_speed(37)|horse_charge(60)|horse_scale(120)|difficulty(6), imodbits_horse_basic|imodbit_timid ],
#["occc_spider_boss", "Boss Spider", [("spider", 0),], itp_type_horse|itp_unique, 0, 2000, weight(33)|abundance(90)|hit_points(600)|horse_maneuver(150)|horse_speed(38)|horse_charge(150)|horse_scale(150)|difficulty(11), imodbits_horse_basic|imodbit_timid ],
["occc_harley", "Harley", [("harley_2",0)], itp_type_horse, 0, 12000, abundance(10)|hit_points(180)|body_armor(40)|difficulty(6)|horse_speed(75)|horse_maneuver(50)|horse_charge(12)|horse_scale(60), imodbits_none ],

#trample end
["occc_donkey", "Donkey", [("surhorse",0)], itp_type_horse|itp_merchandise, 0, 100, abundance(20)|hit_points(60)|body_armor(10)|difficulty(0)|horse_speed(24)|horse_maneuver(49)|horse_charge(20)|horse_scale(104), imodbits_horse_basic ],
["occc_webknecht", "Webknecht", [("spider", 0),], itp_unique|itp_type_horse, 0, 2000, weight(33)|abundance(90)|hit_points(50)|horse_maneuver(150)|horse_speed(40)|horse_charge(10)|horse_scale(50)|difficulty(6), imodbits_horse_basic|imodbit_timid ],

#########WARGS#########

#first warg in list: warg_1b (see in module_constants)
["occc_warg_1b","Warg",[("warg_1B",0)],itp_type_horse|itp_merchandise,0,1200,hit_points(80)|body_armor(10)|difficulty(2)|horse_speed(33)|horse_maneuver(64)|horse_charge(35),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_warg_1c","Warg",[("warg_1C",0)],itp_type_horse|itp_merchandise,0,1200,hit_points(80)|body_armor(10)|difficulty(2)|horse_speed(33)|horse_maneuver(64)|horse_charge(35),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_warg_1d","Warg",[("warg_1D",0)],itp_type_horse|itp_merchandise,0,1200,hit_points(80)|body_armor(10)|difficulty(2)|horse_speed(33)|horse_maneuver(64)|horse_charge(35),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_wargarmored_1b","Armored_Warg",[("wargArmored_1B",0)],itp_type_horse|itp_merchandise,0,2400,hit_points(100)|body_armor(35)|difficulty(4)|horse_speed(30)|horse_maneuver(61)|horse_charge(38),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_wargarmored_1c","Armored_Warg",[("wargArmored_1C",0)],itp_type_horse|itp_merchandise,0,2400,hit_points(100)|body_armor(35)|difficulty(4)|horse_speed(30)|horse_maneuver(61)|horse_charge(38),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_wargarmored_2b","Armored_Warg",[("wargArmored_2B",0)],itp_type_horse|itp_merchandise,0,2400,hit_points(110)|body_armor(40)|difficulty(4)|horse_speed(30)|horse_maneuver(61)|horse_charge(40),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_wargarmored_2c","Armored_Warg",[("wargArmored_2C",0)],itp_type_horse|itp_merchandise,0,2400,hit_points(120)|body_armor(40)|difficulty(4)|horse_speed(30)|horse_maneuver(61)|horse_charge(40),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_wargarmored_3a","Armored_Warg",[("wargArmored_3A",0)],itp_type_horse|itp_merchandise,0,5000,hit_points(130)|body_armor(45)|difficulty(5)|horse_speed(29)|horse_maneuver(60)|horse_charge(45),imodbits_horse_basic,[],[fac_kingdom_7]],
["occc_warg_reward","Huge_Warg",[("wargArmored_huge",0)],itp_type_horse,0,6000,hit_points(180)|body_armor(45)|difficulty(6)|horse_speed(35)|horse_maneuver(62)|horse_charge(62),imodbits_horse_basic,[],[fac_kingdom_7]],

#occc ridable creatures end

#set skeleton
["ccc_skull_head", "Skull_head", [("skull",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(3)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_plate ],
["ccc_skeleton_cut", "Skeleton Cut", [("skeleton_cut",0)], itp_type_body_armor|itp_covers_legs|itp_covers_head|itp_covers_beard, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(0)|difficulty(4), imodbits_plate ],
["ccc_skeleton_calf", "Skeleton Calf", [("skeleton_calf_L",0)], itp_type_foot_armor|itp_civilian, 0, 700, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(8), imodbits_armor ],
["ccc_skeleton_hand", "Skeleton Hand", [("skeleton_hand_R",0),("skeleton_hand_L",imodbit_reinforced)], itp_type_hand_armor, 0, 700, weight(1.0)|abundance(100)|body_armor(7)|difficulty(0), imodbits_plate ],
["ccd_skeletal_horse", "Skeletal Horse", [("barf_skeletal_horse", 0)], itp_type_horse, 0, 5000, hit_points(60)|body_armor(20)|difficulty(4)|horse_speed(60)|horse_maneuver(80)|horse_charge(40), imodbits_horse_basic|imodbit_champion ],

["ccc_ghost_head", "Ghost_head", [("gohst",0),("ccd_inv_trans_equip_head",ixmesh_inventory),], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(1)|abundance(100)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(1), imodbits_plate ],
["ccc_ghost_body", "Ghost body", [("gohst",0),("ccd_inv_trans_equip_body",ixmesh_inventory),], itp_type_body_armor|itp_covers_legs|itp_covers_head|itp_covers_beard, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(0)|difficulty(1), imodbits_plate ],
["ccc_ghost_calf", "Ghost Calf", [("gohst",0),("ccd_inv_trans_equip_foot",ixmesh_inventory),], itp_type_foot_armor|itp_civilian, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(1), imodbits_armor ],
["ccc_ghost_hand", "Ghost Hand", [("gohst",0),("ccd_inv_trans_equip_hand",ixmesh_inventory),], itp_type_hand_armor, 0, 700, weight(1.0)|abundance(100)|body_armor(7)|difficulty(0), imodbits_plate ],
#["ccc_ghost_horse", "Ghost Horse", [("sumpter_horse",0)], itp_type_horse, 0, 5024, abundance(50)|hit_points(25)|body_armor(5)|horse_speed(89)|horse_maneuver(88)|horse_charge(20)|horse_scale(30), imodbits_horse_basic|imodbit_champion ],

#special item
["ccc_throwing_warp_dagger", "Throwing Warp Dagger", [("dagger_b",0)], itp_type_thrown, itcf_throw_knife, 2024, weight(1)|difficulty(0)|spd_rtng(125)|shoot_speed(15)|thrust_damage(20,cut)|max_ammo(6)|weapon_length(50), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":shooter_agent"),(agent_get_position,pos2,":shooter_agent"),(particle_system_burst,"psys_pistol_smoke",pos2,100),(agent_set_position,":shooter_agent",pos1),(play_sound_at_position, "snd_ccd_ghost", pos1),])] ],
["ccc_throwing_warp_bread", "Throwing Warp Bread", [("bread_b",0)], itp_type_thrown, itcf_throw_axe, 1024, weight(25)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(30,cut)|max_ammo(10)|weapon_length(160), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":shooter_agent"),(agent_get_position,pos2,":shooter_agent"),(particle_system_burst,"psys_pistol_smoke",pos2,100),(agent_set_position,":shooter_agent",pos1),])] ],
["ccc_spawn_ghost", "Throwing Spawn Ghost", [("talak_sutton_hoo",0)], itp_type_thrown|itp_no_pick_up_from_ground, itcf_throw_knife, 2024, weight(1)|difficulty(0)|spd_rtng(150)|shoot_speed(25)|thrust_damage(20,cut)|max_ammo(5)|weapon_length(50), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"),(call_script,"script_ccc_item_hit_effect","itm_ccc_spawn_ghost",":sa"),])] ],
["ccc_throwing_dark_aura", "Dark Aura", [("dagger_b",0)], itp_type_thrown|itp_bonus_against_shield|itp_can_knock_down, itcf_throw_axe, 90000, weight(19)|difficulty(2)|spd_rtng(255)|shoot_speed(15)|thrust_damage(35,blunt)|max_ammo(5)|weapon_length(99), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"),(call_script,"script_ccc_item_hit_effect","itm_ccc_throwing_dark_aura",":sa"),])] ],
["ccc_present_bread", "Present Bread", [("bread_b",0)], itp_type_thrown|itp_default_ammo|itp_bonus_against_shield|itp_remove_item_on_use|itp_can_knock_down, itcf_throw_axe, 500, weight(80)|difficulty(0)|spd_rtng(10)|shoot_speed(1)|thrust_damage(1,blunt)|max_ammo(1)|weapon_length(99), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"),(call_script,"script_ccc_item_hit_effect","itm_ccc_present_bread",":sa"),])] ],

#joke
["ccc_throwing_smoked_meat", "Throwing Smoked Meat", [("smoked_meat",0)], itp_type_thrown, itcf_throw_axe, 400, weight(25)|difficulty(0)|spd_rtng(90)|shoot_speed(30)|thrust_damage(18,cut)|max_ammo(10)|weapon_length(80), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_wine", "Throwing Horse", [("saddle_horse",0)], itp_type_thrown, itcf_throw_axe, 400, weight(35)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(18,cut)|max_ammo(8)|weapon_length(80), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_apple_basket", "Throwing Aplle Basket", [("apple_basket",0)], itp_type_thrown, itcf_throw_javelin, 400, weight(20)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(18,cut)|max_ammo(10)|weapon_length(80), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_wheat", "Throwing Camel", [("camel",0)], itp_type_thrown, itcf_throw_axe, 400, weight(19)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(18,cut)|max_ammo(10)|weapon_length(80), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_cabbage", "Throwing Cabbage", [("cabbage",0)], itp_type_thrown, itcf_throw_axe, 400, weight(35)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(18,cut)|max_ammo(10)|weapon_length(80), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_fish", "Throwing Fish", [("fish_a",0)], itp_type_thrown, itcf_throw_axe, 400, weight(25)|difficulty(8)|spd_rtng(80)|shoot_speed(30)|thrust_damage(18,cut)|max_ammo(10)|weapon_length(200), imodbits_thrown, missile_distance_trigger ],
["ccc_throwing_bread", "Throwing Bread", [("bread_b",0)], itp_type_thrown, itcf_throw_axe, 400, weight(25)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(18,cut)|max_ammo(10)|weapon_length(160), imodbits_thrown, missile_distance_trigger ],

["ccc_cartridges_max", "Catridge", [("cartridge_a",0)], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield, 0, 90000, weight(20.25)|abundance(90)|weapon_length(3)|thrust_damage(99,pierce)|max_ammo(255), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],
["ccc_mini_gun", "Mini Gun", [("rifle_8barrel",0)], itp_type_musket|itp_two_handed|itp_primary|itp_crush_through, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 90000, weight(3.5)|difficulty(0)|spd_rtng(255)|shoot_speed(95)|thrust_damage(150,pierce)|max_ammo(255)|accuracy(0), imodbits_none, [(ti_on_weapon_attack,[(play_sound,"snd_merc_cav_musket_shot"),(position_move_x,pos1,27),(position_move_y,pos1,36),(particle_system_burst,"psys_brazier_fire_1",pos1,15)])] ],
#["ccc_throwing_a_camel", "A-Camel", [("camel",0)], itp_type_thrown, itcf_throw_axe, 1024, weight(19)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(999,cut)|max_ammo(10)|weapon_length(80), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"),(call_script,"script_ccc_item_hit_effect","itm_ccc_throwing_a_camel",":sa"),])] ],
#ccc_throwing_bomb
["ccc_throwing_a_camel", "Bomb", [("stone_9",0)], itp_type_thrown, itcf_throw_axe, 1024, weight(12)|difficulty(0)|spd_rtng(50)|shoot_speed(50)|thrust_damage(100,blunt)|max_ammo(1)|weapon_length(30), imodbits_thrown, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccd_item_hit_effect_explosion_missile", "itm_ccc_throwing_a_camel", ":sa"),])] ],
["ccc_throwing_eros", "Ero Wind", [("dagger_b",0)], itp_type_thrown, itcf_throw_axe, 1024, weight(5)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(1,cut)|max_ammo(10)|weapon_length(80), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"),(call_script,"script_ccc_item_hit_effect","itm_ccc_throwing_eros",":sa"),])] ],
#["ccc_throwing_aphrodisiac", "Aphrodisiac",[("amphora_slim",0)],itp_type_thrown|itp_remove_item_on_use, itcf_throw_axe, 10000, weight(1)|difficulty(0)|spd_rtng(40)|shoot_speed(5)|thrust_damage(1,cut)|max_ammo(1)|weapon_length(80), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"),(call_script,"script_ccc_item_hit_effect","itm_ccc_throwing_aphrodisiac",":sa"),])] ],

#["ccc_horse_joke1", "Mini Horse", [("sumpter_horse",0)], itp_type_horse, 0, 134, abundance(0)|hit_points(35)|body_armor(14)|difficulty(1)|horse_speed(100)|horse_maneuver(100)|horse_charge(25)|horse_scale(10), imodbits_horse_basic ],
#["ccc_horse_joke2", "Mid Horse", [("sumpter_horse",0)], itp_type_horse, 0, 134, abundance(0)|hit_points(999)|body_armor(250)|difficulty(1)|horse_speed(57)|horse_maneuver(50)|horse_charge(25)|horse_scale(300), imodbits_horse_basic ],
#["ccc_horse_joke3", "Big Horse", [("sumpter_horse",0)], itp_type_horse, 0, 134, abundance(0)|hit_points(999)|body_armor(250)|difficulty(1)|horse_speed(57)|horse_maneuver(50)|horse_charge(25)|horse_scale(10000), imodbits_horse_basic ],

["occc_booty", "Booty", [("chest_c",0)], itp_type_goods|itp_consumable, 0, 5000, weight(20)|abundance(20)|max_ammo(1), imodbits_none ],
["occc_booty_2", "Greater Booty", [("chest_b",0)], itp_type_goods|itp_consumable, 0, 10000, weight(20)|abundance(20)|max_ammo(1), imodbits_none ],

# cave item
["ccc_healing_wine", "Healing Wine", [("amphora_slim",0)], itp_type_goods|itp_merchandise|itp_consumable, 0, 700, weight(20)|abundance(5)|max_ammo(3), imodbits_none ],
["ccc_relics_golden_pistol", "Relics Golden Pistol", [("pistol_flintlock_a",0)], itp_type_goods, 0, 100, weight(20)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_relics_1", "Relics", [("oil",0)], itp_type_goods|itp_consumable, 0, 5000, weight(20)|abundance(30)|max_ammo(1), imodbits_none ],
["ccc_relics_2", "Relics", [("jug",0)], itp_type_goods|itp_consumable, 0, 10000, weight(20)|abundance(20)|max_ammo(1), imodbits_none ],
["ccc_relics_3", "Relics", [("sar_warhorse",0)], itp_type_goods|itp_consumable, 0, 20000, weight(20)|abundance(10)|max_ammo(1), imodbits_none ],
["ccc_relics_4", "Relics", [("hermitage_shield_1",0)], itp_type_goods|itp_consumable, 0, 30000, weight(20)|abundance(10)|max_ammo(1), imodbits_none ],
["ccd_relics_a", "Relics", [("mp40",0)], itp_type_goods|itp_consumable, 0, 1000, weight(5)|abundance(10)|max_ammo(1), imodbits_none ],
["ccd_relics_b", "Relics", [("breathmask_with_helmet_grau",0)], itp_type_goods|itp_consumable, 0, 3000, weight(5)|abundance(10)|max_ammo(1), imodbits_none ],
["ccd_relics_c", "Relics", [("MG42",0)], itp_type_goods|itp_consumable, 0, 5000, weight(5)|abundance(10)|max_ammo(1), imodbits_none ],

#Duel
["ccc_warhorse_duel", "Duel Warhorse", [("charger",0)], itp_type_horse, 0, 5000, abundance(40)|hit_points(800)|body_armor(255)|difficulty(0)|horse_speed(150)|horse_maneuver(80)|horse_charge(90)|horse_scale(112), imodbits_horse_basic|imodbit_champion ],
["ccc_lance_duel", "Duel Lance", [("heavy_lanceb",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_couchable, itc_greatlance, 1024, weight(2.25)|spd_rtng(35)|weapon_length(540)|swing_damage(0,blunt)|thrust_damage(50,blunt)|max_ammo(1), imodbits_polearm ],
["ccc_shield_duel", "Duel Shield", [("tableau_shield_kite_4",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 205, weight(2)|hit_points(165)|body_armor(14)|spd_rtng(103)|shield_width(30)|shield_height(50), imodbits_shield, [(ti_on_init_item,[(store_trigger_param_1,":agent_no"),(store_trigger_param_2,":troop_no"),(call_script,"script_shield_item_set_banner","tableau_kite_shield_4",":agent_no",":troop_no")])] ],
["ccc_sword_duel_rapier", "Duel Rapier", [("talak_foil",0),("talak_foil.lod1",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_can_penetrate_shield|itp_penalty_with_shield|itp_crush_through, itcf_thrust_onehanded|itcf_horseback_thrust_onehanded|itcf_carry_sword_left_hip|itcf_parry_forward_onehanded|itcf_parry_up_onehanded|itcf_parry_right_onehanded|itcf_parry_left_onehanded, 1024, weight(1.5)|difficulty(0)|spd_rtng(140)|weapon_length(100)|swing_damage(0,cut)|thrust_damage(15,pierce), imodbits_sword ],
["ccc_sword_duel", "Duel Sword", [("1hsword",0),("1hsword_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 1024, weight(2.5)|difficulty(0)|spd_rtng(100)|weapon_length(90)|swing_damage(38,cut)|thrust_damage(32,pierce), imodbits_sword_high ],
["ccc_pistol_duel", "Duel Pistol", [("pistol_flintlock_d",0),("pistol_flintlock_d_carry",ixmesh_carry)], itp_type_pistol|itp_primary|itp_next_item_as_melee, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_show_holster_when_drawn|itcf_reload_pistol, 1024, weight(1.5)|difficulty(0)|spd_rtng(82)|shoot_speed(85)|thrust_damage(45,pierce)|max_ammo(1)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_pistol_flintlock_shot"),(call_script, "script_ccd_gun_particle", 0),])] ],
["ccc_pistol_duel_melee", "Duel Pistol Mel", [("pistol_flintlock_d",0),("pistol_flintlock_d_carry",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_revolver_right|itcf_show_holster_when_drawn, 1024, weight(1.5)|difficulty(0)|spd_rtng(92)|weapon_length(45)|swing_damage(13, blunt), imodbits_crossbow ],
["ccc_warhorse_duel2", "Duel Warhorse", [("barded1W",0)], itp_type_horse, 0, 250000, abundance(10)|hit_points(45)|body_armor(50)|difficulty(0)|horse_speed(41)|horse_maneuver(41)|horse_charge(110), imodbits_none|imodbit_champion ],
["ccc_system_fixation_ston", "Fixation Ston", [("throwing_stone",0)], itp_type_goods, 0, 1000, weight(20)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rifle_duel_sniper", "Duel Sniper Rifle", [("rifle_sniper",0)], itp_type_musket|itp_two_handed|itp_primary|itp_crush_through|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2048, weight(4.0)|difficulty(0)|spd_rtng(50)|shoot_speed(250)|thrust_damage(150,pierce)|max_ammo(1)|accuracy(99), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_airgunfire"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_duel_bayonet", "Duel Bayonet", [("rifle_musketmel",0)], itp_type_musket|itp_two_handed|itp_primary|itp_next_item_as_melee|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 1024, weight(3.0)|difficulty(0)|spd_rtng(65)|shoot_speed(120)|thrust_damage(20,pierce)|max_ammo(1)|accuracy(60), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),])] ],
["ccc_rifle_duel_bayonet_mel", "Duel Byonet Mel", [("rifle_musketmel",0)], itp_type_polearm|itp_two_handed|itp_primary, itc_musket_melee_ccd|itcf_carry_spear, 1024, weight(3)|difficulty(0)|spd_rtng(95)|weapon_length(120)|swing_damage(15,cut)|thrust_damage(12,pierce), imodbits_polearm ],

["ccc_rais_hp", "HP Stone", [("iron_16",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_str", "Str Stone", [("iron_1",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_agi", "Agi Stone", [("iron_2",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_int", "Int Stone", [("iron_3",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_chr", "chr Stone", [("iron_4",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_one_hand", "One_hand Stone", [("iron_5",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_two_hand", "Two_hand Stone", [("iron_6",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_polearm", "Polearm Stone", [("iron_7",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_archery", "Archery Stone", [("iron_9",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_crossbow", "Crossbow Stone", [("iron_8",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_throwing", "Throwing Stone", [("iron_15",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_firearms", "Firearms Stone", [("iron_10",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_trade", "Trade Stone", [("iron_11",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_leadership", "Leadership Stone", [("iron_12",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_prisoner_management", "Prisoner Management Stone", [("iron_10",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_persuasion", "Persuasion Stone", [("iron_13",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_engineer", "Engineer Stone", [("iron_14",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_first_aid", "First_aid Stone", [("iron_15",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_surgery", "Surgery Stone", [("iron_16",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_wound_treatment", "Wound_treatment Stone", [("iron_17",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_spotting", "Spotting Stone", [("iron_1",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_pathfinding", "Pathfinding Stone", [("iron_2",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_tactics", "Tactics Stone", [("iron_3",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_tracking", "Tracking Stone", [("iron_4",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_trainer", "Trainer Stone", [("iron_5",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
#["ccc_rais_comprehension", "Comprehension Stone", [("iron_6",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_looting", "Looting Stone", [("iron_7",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_horse_archery", "Horse_archery Stone", [("iron_8",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_riding", "Riding Stone", [("iron_9",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_athletics", "Athletics Stone", [("iron_10",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_shield", "Shield Stone", [("iron_11",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_weapon_master", "Weapon Master Stone", [("iron_12",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_power_draw", "Power_draw Stone", [("iron_13",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_power_throw", "Power_throw Stone", [("iron_14",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_power_strike", "Power_strike Stone", [("iron_15",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_ironflesh", "Ironflesh Stone", [("iron_16",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["ccc_rais_end", "Rais_end", [("iron_17",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],

## Tavern Animation Pack by Daedalus
["dedal_kufel","Kufel",[("dedal_kufelL",0)],	itp_type_hand_armor,0,0,weight(1),0],
["dedal_lutnia","Lutnia",[("dedal_lutniaL",0)],	itp_type_hand_armor,0,0,weight(1),0],
["dedal_lira","Lira",[("dedal_liraL",0)],		itp_type_hand_armor,0,0,weight(1),0],
## Tavern Animation Pack end

## CC-D begin
["ccd_lightsaber", "Light Saber", [("ccd_lightsaber",0),("ccd_lightsaber",ixmesh_carry)], itp_type_two_handed_wpn|itp_primary, itc_bastardsword|itcf_carry_dagger_front_left, 50000, weight(2.0)|difficulty(21)|spd_rtng(120)|weapon_length(100)|swing_damage(50,pierce)|thrust_damage(50,pierce), imodbits_sword_high, [(ti_on_init_item,[(try_for_range, ":count", 2, 21),(store_mul, ":pos_y", 5, ":count"),(set_position_delta,0,":pos_y",0),(particle_system_add_new,"psys_ccd_light_spark"),(try_end),]),(ti_on_weapon_attack,[(play_sound, "snd_ccd_lightsaber_swing"),])] ],
["ccd_vicious_heart", "Vicious Heart", [("ViciousHeart",0)], itp_type_two_handed_wpn|itp_primary, itc_bastardsword|itcf_carry_sword_back, 50000, weight(5)|difficulty(30)|spd_rtng(110)|weapon_length(150)|swing_damage(54,cut)|thrust_damage(50,pierce), imodbits_sword_high ],
["ccd_riken", "Kaenken Homura", [( "ccd_riken",0),], itp_type_polearm|itp_offset_lance|itp_couchable|itp_primary|itp_crush_through|itp_bonus_against_shield|itp_next_item_as_melee, itc_staff|itcf_thrust_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_parry_forward_polearm|itcf_parry_up_polearm|itcf_parry_right_polearm|itcf_parry_left_polearm, 8000, weight(12)|difficulty(45)|spd_rtng(82)|weapon_length(200)|thrust_damage(55, pierce)|swing_damage(52, cut), imodbits_sword_high, [(ti_on_init_item,[(set_position_delta, 0, 75, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_position_delta, 0, 130, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_position_delta, 0, 185, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_current_color, 150, 130, 70),(add_point_light, 10, 30),])] ],
["ccd_riken_melee", "Kaenken Homura", [( "ccd_riken",0),], itp_type_two_handed_wpn|itp_couchable|itp_primary|itp_crush_through|itp_bonus_against_shield, itc_bastardsword, 8000, weight(12)|difficulty(45)|spd_rtng(82)|weapon_length(200)|thrust_damage(55, pierce)|swing_damage(52, cut), imodbits_sword_high, [(ti_on_init_item,[(set_position_delta, 0, 75, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_position_delta, 0, 130, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_position_delta, 0, 185, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_current_color, 150, 130, 70),(add_point_light, 10, 30),])] ],
["ccd_valspear", "Throwing Valkyrie Spear", [("valspear", 0)],itp_merchandise|itp_type_thrown|itp_crush_through|itp_primary|itp_bonus_against_shield|itp_next_item_as_melee, itcf_throw_javelin, 10000, abundance(500)|weight(5)|difficulty(8)|spd_rtng(75)|shoot_speed(37)|thrust_damage(33, pierce)|max_ammo(18)|weapon_length(110), imodbits_thrown, missile_distance_trigger,[fac_valkyrie] ],  ## cave09  ->ccc_throwing_spear_valkyrie
["ccd_valspear_melee", "Valkyrie Spear", [("valspear", 0)], itp_crush_through|itp_unique|itp_type_polearm|itp_primary|itp_secondary|itp_bonus_against_shield, itc_cutting_spear, 10000, weight(5)|difficulty(8)|spd_rtng(100)|weapon_length(140)|swing_damage(52, cut)|thrust_damage(48,  pierce), imodbits_polearm ],  ## cave09  ->ccc_throwing_spear_valkyrie_melee
["ccd_valhalberd", "Valkyrie Halberd", [("val_halberd",0)], itp_merchandise|itp_couchable|itp_type_polearm|itp_primary|itp_bonus_against_shield|itp_offset_lance|itp_couchable, itc_staff|itcf_thrust_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear|itcf_parry_forward_polearm|itcf_parry_up_polearm|itcf_parry_right_polearm|itcf_parry_left_polearm|itcf_force_64_bits, 10000, abundance(500)|weight(4)|difficulty(21)|spd_rtng(90)|weapon_length(185)|swing_damage(48,cut)|thrust_damage(45,pierce), imodbits_polearm,[],[fac_valkyrie] ],
["ccd_gungnir_replica", "Throwing Gungnir Replica", [("ccd_gungnir_r", 0)],itp_type_thrown|itp_next_item_as_melee|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration|itp_ignore_friction, itcf_throw_javelin, 4096, weight(4)|difficulty(14)|spd_rtng(200)|shoot_speed(200)|thrust_damage(200, pierce)|max_ammo(1)|weapon_length(200), imodbits_thrown, [(ti_on_weapon_attack,[(play_sound,"snd_ccd_gungnir_shot"),]), (ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccd_item_hit_effect_explosion_missile", "itm_ccd_gungnir_replica", ":sa"),])] + missile_distance_trigger ],
["ccd_gungnir_replica_melee", "Gungnir Replica", [("ccd_gungnir_r", 0)], itp_couchable|itp_unique|itp_type_polearm|itp_primary|itp_two_handed|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration|itp_ignore_friction, itc_guandao|itcf_carry_spear, 4096, weight(4)|difficulty(14)|spd_rtng(110)|weapon_length(200)|swing_damage(54, cut)|thrust_damage(58, pierce), imodbits_polearm ],
["ccd_bangalore", "Bangalore", [("ccd_bangalore",0)], itp_couchable|itp_type_polearm|itp_two_handed|itp_primary|itp_offset_lance, itc_greatlance, 500, weight(4.5)|difficulty(0)|spd_rtng(90)|swing_damage(0, cut)|thrust_damage(20, blunt)|weapon_length(120), imodbits_polearm ],
["ccd_bottle_pink", "Pinky Bottle", [("ccd_bottle_pink", 0)], itp_type_thrown|itp_remove_item_on_use, itcf_throw_knife, 20000, weight(1)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(1, cut)|max_ammo(1)|weapon_length(0), imodbits_missile, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccc_item_hit_effect", "itm_ccd_bottle_pink", ":sa"),])] ],
["ccd_holy_water", "Holy Water", [("ccd_bottle_blue", 0)], itp_type_thrown|itp_remove_item_on_use|itp_no_pick_up_from_ground, itcf_throw_knife, 4096, weight(1)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(1, cut)|max_ammo(2)|weapon_length(0), imodbits_missile, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccc_item_hit_effect", "itm_ccd_holy_water", ":sa"),])] ],
["ccd_magic_knife", "Magic Knife", [("legolas_knife",0)], itp_type_thrown|itp_primary, itcf_throw_knife, 2048, weight(1)|difficulty(0)|spd_rtng(200)|shoot_speed(50)|thrust_damage(5,cut)|max_ammo(200)|weapon_length(0), imodbits_thrown, ccd_magic_knife_trigger + missile_distance_trigger ],
["ccd_sunglass", "Sunglasses", [("ccd_sunglass",0)], itp_type_head_armor|itp_fit_to_head|itp_doesnt_cover_hair|itp_civilian, 0, 512, weight(0.2)|head_armor(16)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
#["ccd_power_punching_gloves", "Power Punching Gloves", [("leather_gloves_L",0)], itp_type_hand_armor, 0, 512, weight(0.5)|body_armor(3)|difficulty(0), imodbits_cloth ],
["ccd_book_human_relations", "The Book of Human Relations", [("book_a",0)], itp_type_goods, 0, 20000, weight(2)|abundance(100), imodbits_none ],
["ccd_return_stone", "Return Stone", [("stone_8",0)], itp_type_goods, 0, 500, weight(0.5)|abundance(0), imodbits_none ],
["ccd_spawn_undead", "Throwing Spawn Undead", [("undead_facemask", 0)], itp_type_thrown|itp_no_pick_up_from_ground, itcf_throw_knife, 1024, weight(2)|difficulty(0)|spd_rtng(120)|shoot_speed(20)|thrust_damage(15, blunt)|max_ammo(4)|weapon_length(50), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1, ":sa"),(call_script, "script_ccc_item_hit_effect", "itm_ccd_spawn_undead",":sa"),])] ],
["ccd_undead_weapon_calf", "Throwing Undead Calf", [("undead_calf_l", 0)], itp_type_thrown|itp_next_item_as_melee, itcf_throw_axe, 256, weight(5)|difficulty(2)|spd_rtng(90)|shoot_speed(50)|thrust_damage(13, blunt)|max_ammo(1)|weapon_length(85), imodbits_thrown, missile_distance_trigger ],
["ccd_undead_weapon_calf_melee", "Hitting Undead Calf", [("undead_calf_l", 0)], itp_type_one_handed_wpn|itp_primary|itp_unique, itc_longsword, 256, weight(5)|difficulty(2)|spd_rtng(95)|swing_damage(27, blunt)|thrust_damage(23, blunt)|weapon_length(85), imodbits_sword_high ],
["ccd_undead_facemask", "Undead Face", [("undead_facemask",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 256, weight(2)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["ccd_undead_bodysuits", "Undead Body", [("undead_bodysuits", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(5)|body_armor(30)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ccd_undead_calfboots", "Undead Calf", [("undead_calfboots", 0)], itp_type_foot_armor|itp_civilian|itp_attach_armature, 0, 256, weight(0.5)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ccd_undead_handgloves", "Undead Hand", [("undead_handgloves_R", 0),("undead_handgloves_L",imodbit_reinforced)], itp_type_hand_armor, 0, 256, weight(1.0)|body_armor(4)|difficulty(0), imodbits_armor ],
["ccd_troll_facemask", "Troll Face", [("trollheadb",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 256, weight(2)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_plate ],
["ccd_troll_bodysuits", "Troll Body", [("trollbodya", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(5)|body_armor(50)|leg_armor(10)|difficulty(0), imodbits_cloth ],
["ccd_troll_calfboots", "Troll Calf", [("trollfoot", 0)], itp_type_foot_armor|itp_civilian|itp_attach_armature, 0, 256, weight(0.5)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0), imodbits_cloth ],
["ccd_troll_handgloves", "Troll Hand", [("troll_hand_R", 0),("troll_hand_L",imodbit_reinforced)], itp_type_hand_armor, 0, 256, weight(1.0)|body_armor(7)|difficulty(0), imodbits_armor ],
["ccd_troll_shield_skin", "Troll Skin Shield", [("empty_mesh",0),("troll_hand_L",ixmesh_inventory),], itp_type_shield, 0, 700, weight(2)|hit_points(300)|body_armor(10)|spd_rtng(100)|shield_width(50)|difficulty(1), imodbits_shield ],
["ccd_dog", "Dog", [("dog_2",0)], itp_type_horse|itp_unique|itp_no_pick_up_from_ground|itp_disable_agent_sounds, 0, 1024, hit_points(45)|body_armor(20)|difficulty(0)|horse_speed(45)|horse_maneuver(90)|horse_charge(30)|horse_scale(55), imodbits_horse_basic|imodbit_champion ],
["ccd_zombiedog", "Zombie Dog", [("dog_2c",0)], itp_type_horse|itp_unique|itp_no_pick_up_from_ground|itp_disable_agent_sounds, 0, 1024, hit_points(45)|body_armor(20)|difficulty(0)|horse_speed(45)|horse_maneuver(90)|horse_charge(30)|horse_scale(80), imodbits_horse_basic|imodbit_champion ],
["ccd_dog_bite", "Bite", [("empty_mesh", 0),("dagger_b",ixmesh_inventory),], itp_type_polearm|itp_primary|itp_can_knock_down|itp_unique|itp_no_pick_up_from_ground, itc_greatlance, 256, weight(1)|spd_rtng(135)|thrust_damage(35,pierce)|weapon_length(75), imodbits_sword_high, [(ti_on_weapon_attack,[(store_trigger_param_1,":cur_agent"),(call_script, "script_ccd_horse_bite_attack",":cur_agent"),])] ],
["occc_animal_attack", "Bite_2", [("empty_mesh", 0),("dagger_b",ixmesh_inventory),], itp_type_one_handed_wpn|itp_primary|itp_unique|itp_no_pick_up_from_ground, itc_longsword, 256, weight(1)|spd_rtng(125)|swing_damage(25,pierce)|thrust_damage(27,pierce)|weapon_length(75), imodbits_sword_high, [(ti_on_weapon_attack,[(store_trigger_param_1,":cur_agent"),(call_script, "script_ccd_horse_bite_attack",":cur_agent"),])] ],
["ccd_lizardman_body", "Lizardman Full Body", [("lizard_body",0),], itp_type_body_armor|itp_unique|itp_covers_legs|itp_civilian|itp_covers_head, 0, 5000, weight(2)|head_armor(25)|body_armor(45)|leg_armor(20), imodbits_none,  ],
["ccd_balrog_sword", "Balrog Sword", [( "balrog_sword",0),], itp_type_one_handed_wpn|itp_primary|itp_crush_through|itp_bonus_against_shield|itp_extra_penetration|itp_no_pick_up_from_ground, itc_scimitar, 5000, weight(15)|difficulty(80)|spd_rtng(90)|weapon_length(217)|thrust_damage(0, pierce)|swing_damage(55, cut), imodbits_sword_high, [(ti_on_init_item,[(set_position_delta, 0, 75, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_position_delta, 0, 130, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_position_delta, 0, 185, 0),(particle_system_add_new, "psys_fireplace_fire_big"),(set_current_color, 150, 130, 70),(add_point_light, 10, 30),])] ],
["ccd_balrog_body", "Balrog Full Body", [("balrog_ignore",0),], itp_type_body_armor|itp_unique|itp_covers_legs|itp_civilian|itp_covers_head, 0, 10000, weight(25)|difficulty(80)|head_armor(40)|body_armor(60)|leg_armor(30), imodbits_none,  ],
["ccd_machinegun", "Short Machine Gun", [("hk_mp5k",0)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol, 8192, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(200)|thrust_damage(65,pierce)|max_ammo(30)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),])], [fac_player_supporters_faction] ],
["ccd_shotshell_night", "Shot Shell(night)", [("ccd_ammo_bag_a",0),("ccd_shotshell_night",ixmesh_flying_ammo),("bullet",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_unique|itp_can_knock_down, 0, 41, weight(2.25)|weapon_length(3)|thrust_damage(5,pierce)|max_ammo(24), imodbits_missile, [(ti_on_missile_hit,[(call_script, "script_oim_on_bullet_hit"),])] ],
["ccd_muttiri_body", "Muttiri Body", [("m_woman_body", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(5)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["ccd_gorgeous_body", "Gorgeous Body", [("body_hd_wet_trans_under_body", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(5)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["ccd_gorgeous_foot", "Gorgeous Foot", [("body_hd_wet_trans_under_foot", 0)], itp_type_foot_armor|itp_civilian|itp_attach_armature, 0, 256, weight(0.5)|head_armor(0)|body_armor(0)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["ccd_dancer_body", "Dancer Body", [("ccd_dancer_body", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(5)|leg_armor(2)|difficulty(0), imodbits_cloth ],
#["ccd_gorgeous_full_body", "Gorgeous Full Body", [("body_hd_wet_trans_under", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(5)|leg_armor(2)|difficulty(0), imodbits_cloth ],
#["ccd_smart_full_body", "Smart Full Body", [("housemaid_body_under", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(4)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["ccd_smart_hand", "Smart Hand", [("norm_handR", 0)], itp_type_hand_armor, 0, 256, weight(1.0)|body_armor(1)|difficulty(0), imodbits_armor ],
## CC-D end


###w-samurai-set BUKI
#w-samurai-set short katana
["aikuchi", "Aikuchi", [("aikuchi",0),("aikuchi_with_saya",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 
 280 , weight(1)|abundance(250)|difficulty(8)|spd_rtng(109) | weapon_length(40)|swing_damage(27 , cut) | thrust_damage(14 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["wazamono_aikuchi", "Wazamono_Aikuchi", [("aikuchi",0),("waikuchi_with_saya2",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 
 460 , weight(1)|abundance(230)|difficulty(10)|spd_rtng(110) | weapon_length(40)|swing_damage(32 , cut) | thrust_damage(14 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["namakura_kodachi", "Namakura_Kodachi", [("wakizashi_y_sk",0),("wakizashi_y_sk_saya",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 
 150 , weight(1.2)|abundance(270)|difficulty(0)|spd_rtng(105) | weapon_length(58)|swing_damage(24 , cut) | thrust_damage(18 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["kodachi", "Kodachi", [("kodachi_a",0),("kodachia_saya",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 
 360 , weight(1.2)|abundance(250)|difficulty(10)|spd_rtng(105) | weapon_length(60)|swing_damage(28 , cut) | thrust_damage(16 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["wazamono_kodachi", "Wazamono_Kodachi", [("kodachiB",0),("kodachiB_with_saya",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 
 490 , weight(1.2)|abundance(230)|difficulty(14)|spd_rtng(106) | weapon_length(60)|swing_damage(33 , cut) | thrust_damage(18 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["namakura_wakizashi", "Namakura_wakizashi", [("wakizashi_y",0),("wakizashi_y_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_merchandise, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn,
 170, weight(1.25)|abundance(270)|difficulty(0)|spd_rtng(103) | weapon_length(85)|swing_damage(24 , cut) | thrust_damage(25 ,  pierce), imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["wakizashi", "Wakizashi", [("kodachiC",0),("kodachiC_with_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_merchandise, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn,
 280 , weight(1.25)|abundance(250)|difficulty(0)|spd_rtng(103) | weapon_length(85)|swing_damage(27 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["wazamono_wakizashi", "Wazamono_wakizashi", [("kodachiD",0),("kodachiD_with_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_merchandise, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn,
 460 , weight(1.25)|abundance(230)|difficulty(0)|spd_rtng(104) | weapon_length(85)|swing_damage(33 , cut) | thrust_damage(27 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["awataguchi_yoshimitsu", "Awataguchi Yoshimitsu", [("kodachiA",0),("kodachiA_with_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_merchandise, itc_longsword|itcf_carry_wakizashi|itcf_show_holster_when_drawn,
 1600 , weight(1.25)|abundance(230)|difficulty(12)|spd_rtng(106) | weapon_length(85)|swing_damage(38 , cut) | thrust_damage(38 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["benisigure", "Benisigure", [("kodachi_by",0),("kodachiby_saya",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 
 880 , weight(1.25)|abundance(200)|difficulty(14)|spd_rtng(106) | weapon_length(65)|swing_damage(40 , cut) | thrust_damage(18 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["zangetsu", "Zangetsu", [("shinobi",0),("shinobiscaba3",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary|itp_no_parry, itc_longsword|itcf_carry_dagger_front_right|itcf_show_holster_when_drawn, 
 900 , weight(1.25)|abundance(200)|difficulty(14)|spd_rtng(104) | weapon_length(70)|swing_damage(36 , cut) | thrust_damage(20 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],

## katana
["mumei_katate_uchigatana", "Mumei_Katate_Uchigatana", [("wkatana_y",0),("wkatana_y_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 160 , weight(1.8)|abundance(250)|difficulty(9)|spd_rtng(97) | weapon_length(103)|swing_damage(30 , cut) | thrust_damage(22 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["namakura_uchigatana", "Namakura_Uchigatana", [("katana_y2",0),("katana_y2_saya", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 250 , weight(2)|abundance(270)|difficulty(10)|spd_rtng(97) | weapon_length(110)|swing_damage(27 , cut) | thrust_damage(25 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["mumei_uchigatana", "Mumei_Uchigatana", [("katana_y2",0),("katana_y2_saya", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 550 , weight(2)|abundance(250)|difficulty(10)|spd_rtng(97) | weapon_length(110)|swing_damage(32 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["masamune", "Masamune", [("katana_y2_e",0),("katana_y2_saya_e", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 6000 , weight(2)|abundance(220)|difficulty(16)|spd_rtng(98) | weapon_length(110)|swing_damage(46 , pierce) | thrust_damage(43 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["oborotsukiyo", "Oborotsukiyo", [("katana_y2_e",0),("katana_y2_saya_e", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 1650 , weight(2)|abundance(200)|difficulty(14)|spd_rtng(98) | weapon_length(110)|swing_damage(37 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["kurenaitennyo", "Kurenaitennyo", [("katana_y2_d",0),("katana_y2_saya_d", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 1650 , weight(1.8)|abundance(200)|difficulty(14)|spd_rtng(101) | weapon_length(110)|swing_damage(40 , cut) | thrust_damage(28 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["sanjyou_munechika", "Sanjyou Munechika", [("katana_y2_f",0),("katana_y2_saya_f", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 2300 , weight(2)|abundance(230)|difficulty(14)|spd_rtng(100) | weapon_length(110)|swing_damage(44 , cut) | thrust_damage(36 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["kacyofugetsu", "Kacyofugetsu", [("katana_y2_f",0),("katana_y2_saya_f", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 1650 , weight(2)|abundance(220)|difficulty(14)|spd_rtng(98) | weapon_length(110)|swing_damage(38 , cut) | thrust_damage(30 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["ginroga", "Ginroga", [("katana_y2_c",0),("katana_y2_saya_c", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 1750 , weight(2)|abundance(200)|difficulty(14)|spd_rtng(96) | weapon_length(110)|swing_damage(36 , cut) | thrust_damage(31 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
 
["rai_kunitoshi", "Rai Kunitoshi", [("katana",0),("katana_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 1900 , weight(1.8)|abundance(230)|difficulty(14)|spd_rtng(98) | weapon_length(105)|swing_damage(34 , cut) | thrust_damage(32 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
 
["kamikaze", "Kamikaze", [("katana",0),("katana_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 1450 , weight(1.8)|abundance(220)|difficulty(12)|spd_rtng(98) | weapon_length(105)|swing_damage(35 , cut) | thrust_damage(26 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["shishiomaru", "Shishiomaru", [("katana_y2_b",0),("katana_y2_saya_b", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 13000 , weight(2.2)|abundance(220)|difficulty(18)|spd_rtng(98) | weapon_length(112)|swing_damage(48 , cut) | thrust_damage(35 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["mumei_nodachi",  "Mumei_Nodachi", [("no_dachiB",0),("no_dachiB_with_saya",ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_merchandise|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_sword_back|itcf_show_holster_when_drawn,
 1100 , weight(3.5)|abundance(200)|difficulty(12)|spd_rtng(88) | weapon_length(130)|swing_damage(41 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["bizen_osafune_nagamitsu",  "Bizen_Osafune_Nagamitsu", [("monohoshi",0),("monohoshi_saya",ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_merchandise|itp_primary|itp_bonus_against_shield, itc_nodachi|itcf_carry_sword_back|itcf_show_holster_when_drawn,
 4500 , weight(3.5)|abundance(230)|difficulty(14)|spd_rtng(95) | weapon_length(150)|swing_damage(45 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["sakabato", "Sakabato", [("sakabatou",0),("sakabatou_saya", ixmesh_carry)], itp_type_two_handed_wpn|itp_merchandise|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 850 , weight(2)|abundance(230)|difficulty(12)|spd_rtng(97) | weapon_length(110)|swing_damage(36 , blunt) | thrust_damage(25 ,  blunt),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],

## nagae buki
["namakura_naginata",  "Namakura_Naginata", [("long_naginata",0)], itp_type_polearm|itp_merchandise|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed, itc_guandao|itcf_carry_spear,
 395 , weight(4.75)|abundance(250)|difficulty(12)|spd_rtng(83) | weapon_length(168)|swing_damage(29 , cut) | thrust_damage(20 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
["naginata",  "Naginata", [("long_naginata",0)], itp_type_polearm|itp_merchandise|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed, itc_guandao|itcf_carry_spear,
 395 , weight(4.75)|abundance(250)|difficulty(12)|spd_rtng(83) | weapon_length(168)|swing_damage(34 , cut) | thrust_damage(25 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
 ["wazamono_naginata",  "Wazamono_Naginata", [("long_naginata",0)], itp_type_polearm|itp_merchandise|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed, itc_guandao|itcf_carry_spear,
 395 , weight(4.75)|abundance(250)|difficulty(12)|spd_rtng(83) | weapon_length(168)|swing_damage(39 , cut) | thrust_damage(30 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
["kagura",  "Kagura", [("bisento",0)], itp_type_polearm|itp_merchandise|itp_primary|itp_penalty_with_shield|itp_wooden_parry|itp_two_handed, itc_guandao|itcf_carry_spear,
 680 , weight(4.25)|abundance(260)|difficulty(12)|spd_rtng(88) | weapon_length(158)|swing_damage(45 , cut) | thrust_damage(36 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
["takeyari", "Takeyari", [("bamboo_spear",0)], itp_type_two_handed_wpn|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_staff|itcf_carry_spear,
 75 , weight(2.0)|difficulty(0)|spd_rtng(97) | weapon_length(160)|swing_damage(19 , blunt) | thrust_damage(21 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
["sasaho_yari", "Sasaho_Yari", [("sasaho_yari",0)], itp_couchable|itp_type_two_handed_wpn|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
 360 , weight(3.0)|abundance(250)|difficulty(0)|spd_rtng(85) | weapon_length(170)|swing_damage(22 , blunt) | thrust_damage(28 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
["kataKama_yari", "KataKama_Yari", [("katakama_yari",0)], itp_couchable|itp_type_two_handed_wpn|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
 610 , weight(3.0)|abundance(250)|difficulty(12)|spd_rtng(85) | weapon_length(170)|swing_damage(25 , blunt) | thrust_damage(30 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
["kikuchi_yari", "Kikuchi_Yari", [("kikuchiyari",0)], itp_couchable|itp_type_two_handed_wpn|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
 700 , weight(3.5)|abundance(240)|difficulty(14)|spd_rtng(80) | weapon_length(200)|swing_damage(22 , blunt) | thrust_damage(34 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
["kiyomasa_kama_yari", "Kiyomasa_Kama_Yari", [("kiyomasa_kamayari",0)], itp_couchable|itp_type_two_handed_wpn|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
 780 , weight(4.5)|abundance(250)|difficulty(14)|spd_rtng(88) | weapon_length(160)|swing_damage(35 , blunt) | thrust_damage(36 ,  pierce),imodbits_polearm, [],[fac_kingdom_9,fac_bushido_order] ],
#["jyuji_yari", "Jyuji_Yari", [("invader_pike",0)], itp_couchable|itp_type_polearm|itp_offset_lance|itp_merchandise| itp_primary|itp_penalty_with_shield|itp_wooden_parry, itc_cutting_spear|itcf_carry_spear,
# 380 , weight(3)|abundance(100)|difficulty(12)|spd_rtng(80) | weapon_length(180)|swing_damage(25 , blunt) | thrust_damage(30 ,  pierce),imodbits_polearm ],

## kanabou
["kanasaibo", "Kanasaibo", [("kanasaibo",0)], itp_crush_through|itp_type_two_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced, itc_nodachi|itcf_carry_spear,
 390 , weight(5)|abundance(230)|difficulty(14)|spd_rtng(80) | weapon_length(135)|swing_damage(35 , blunt) | thrust_damage(21 ,  pierce),imodbits_mace, [],[fac_kingdom_9,fac_bushido_order] ],
["kongo_kanasaibo", "Kongo_Kanasaibo", [("kanabo",0)], itp_crush_through|itp_type_two_handed_wpn|itp_merchandise|itp_can_knock_down|itp_primary|itp_two_handed|itp_wooden_parry|itp_wooden_attack|itp_unbalanced, itc_nodachi|itcf_carry_spear,
 710 , weight(9)|abundance(9)|abundance(200)|difficulty(14)|spd_rtng(70) | weapon_length(120)|swing_damage(45 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace, [],[fac_kingdom_9,fac_bushido_order] ],

## katana shield
["katana_shield", "Katana Shield", [("katanashield_y",0),("katana_y2_saya", ixmesh_carry)], itp_merchandise|itp_type_shield|itp_force_attach_left_hand, itcf_carry_sword_left_hip,
1000 , weight(2)|abundance(180)|hit_points(600)|body_armor(22)|spd_rtng(100)|shield_width(20),imodbits_shield, [],[fac_kingdom_9,fac_bushido_order] ],
["kodachi_shield", "Kodachi Shield", [("kodachishield_y",0),("aikuchi_with_saya",ixmesh_carry)], itp_merchandise|itp_type_shield|itp_force_attach_left_hand, itcf_carry_dagger_front_right,
800 , weight(2)|abundance(190)|hit_points(500)|body_armor(20)|spd_rtng(104)|shield_width(10),imodbits_shield, [],[fac_kingdom_9,fac_bushido_order] ],
["aikuchi_shield", "Aikuchi Shield", [("aikuchishield",0),("kodachia_saya",ixmesh_carry)], itp_merchandise|itp_type_shield|itp_force_attach_left_hand, itcf_carry_dagger_front_right,
460 , weight(2)|abundance(190)|hit_points(380)|body_armor(18)|spd_rtng(110)|shield_width(8),imodbits_shield, [],[fac_kingdom_9,fac_bushido_order] ],


###w-samurai-set BOUGU
## fuku
["tenashi", "Tenashi", [("tenashi",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 10 , weight(0.5)|abundance(250)|head_armor(0)|body_armor(5)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["kinagashi_1", "Kinagashi", [("kinagashi_1",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 220 , weight(1)|abundance(250)|head_armor(0)|body_armor(16)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["kinagashi_2", "Kinagashi", [("kinagashi_2",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 220 , weight(1)|abundance(250)|head_armor(0)|body_armor(16)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["kinagashi_3", "Kinagashi", [("kinagashi_3",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 220 , weight(1)|abundance(250)|head_armor(0)|body_armor(16)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["kinagashi_4", "Kinagashi", [("kinagashi_4",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 220 , weight(1)|abundance(250)|head_armor(0)|body_armor(16)|leg_armor(7)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["hakama_1", "Hakama", [("hakama_1",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 250 , weight(3)|abundance(250)|head_armor(0)|body_armor(19)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["hakama_2", "Hakama", [("hakama_2",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 250 , weight(3)|abundance(250)|head_armor(0)|body_armor(19)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["hakama_3", "Hakama", [("hakama_3",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 250 , weight(3)|abundance(250)|head_armor(0)|body_armor(19)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["hakama_4", "Hakama", [("hakama_4",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 250 , weight(3)|abundance(250)|head_armor(0)|body_armor(19)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["hakama_5", "Hakama", [("hakama_5",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 250 , weight(3)|abundance(250)|head_armor(0)|body_armor(19)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["tasukigake_hakama_1", "Tasukigake_Hakama", [("tasuki_hakama",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 270 , weight(4)|abundance(250)|head_armor(0)|body_armor(21)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["tasukigake_hakama_2", "Tasukigake_Hakama", [("tasuki_hakama2",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 270 , weight(4)|abundance(250)|head_armor(0)|body_armor(21)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],

##touki wo obita fuku
["touki_wo_obita_tenashi", "Touki wo Obita Tenashi", [("tenashi",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2000 , weight(0.5)|abundance(250)|head_armor(0)|body_armor(5)|leg_armor(0)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_kinagashi_1", "Touki wo Obita Kinagashi", [("kinagashi_1",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(1)|abundance(200)|head_armor(0)|body_armor(40)|leg_armor(16)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_kinagashi_2", "Touki wo Obita Kinagashi", [("kinagashi_2",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(1)|abundance(200)|head_armor(0)|body_armor(40)|leg_armor(16)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_kinagashi_3", "Touki wo_Obita Kinagashi", [("kinagashi_3",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(1)|abundance(200)|head_armor(0)|body_armor(40)|leg_armor(16)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_kinagashi_4", "Touki wo Obita Kinagashi", [("kinagashi_4",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(1)|abundance(200)|head_armor(0)|body_armor(40)|leg_armor(16)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_hakama1", "Touki wo Obita Hakama1", [("hakama_1",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(3)|abundance(200)|head_armor(0)|body_armor(41)|leg_armor(14)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_hakama2", "Touki wo_Obita Hakama2", [("hakama_2",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(3)|abundance(200)|head_armor(0)|body_armor(41)|leg_armor(14)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_hakama3", "Touki wo_Obita Hakama3", [("hakama_3",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(3)|abundance(200)|head_armor(0)|body_armor(41)|leg_armor(14)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_hakama4", "Touki wo_Obita Hakama4", [("hakama_4",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(3)|abundance(200)|head_armor(0)|body_armor(41)|leg_armor(14)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_hakama5", "Touki wo_Obita Hakama5", [("hakama_5",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2200 , weight(3)|abundance(200)|head_armor(0)|body_armor(41)|leg_armor(14)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_tasukigake_hakama_1", "Touki_wo_Obita_Tasukigake_Hakama", [("tasuki_hakama",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2300 , weight(4)|abundance(200)|head_armor(0)|body_armor(43)|leg_armor(17)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["touki_wo_obita_tasukigake_hakama_2", "Touki_wo_Obita_Tasukigake_Hakama", [("tasuki_hakama2",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2300 , weight(4)|abundance(200)|head_armor(0)|body_armor(43)|leg_armor(17)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],

["sodenashi_kimono", "Sodenashi Kimono", [("tukurobe",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 300 , weight(4)|abundance(250)|head_armor(0)|body_armor(20)|leg_armor(8)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["sodenashi_kimono_with_mail", "Sodenashi Kimono with mail", [("tukurobe_b",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 520 , weight(14)|abundance(230)|head_armor(0)|body_armor(30)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["miko_syozoku", "Miko_Syozoku", [("mikosyouzoku",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 750 , weight(5)|abundance(240)|head_armor(5)|body_armor(30)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["miko_syozoku_o", "High_Miko_Syozoku", [("mikosyouzoku",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 1950 , weight(6)|abundance(210)|head_armor(5)|body_armor(44)|leg_armor(14)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["sohei_hoi", "Sohei_Hoi", [("sohei_d",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 900 , weight(6)|abundance(240)|head_armor(0)|body_armor(30)|leg_armor(13)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["high_sohei_hoi", "High_Sohei_Hoi", [("sohei_d",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 2300 , weight(6)|abundance(210)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],

## yoroi
["haramaki", "Haramaki", [("haramaki_ashi",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 321 , weight(6)|abundance(260)|head_armor(0)|body_armor(23)|leg_armor(6)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["doumaru", "Doumaru", [("doumaru_ashi",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 440 , weight(10)|abundance(260)|head_armor(0)|body_armor(27)|leg_armor(8)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_sdn", "Gusoku(Sodenashi", [("sdngusoku2_ashi",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 800 , weight(16)|abundance(250)|head_armor(0)|body_armor(37)|leg_armor(8)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku", "Gusoku", [("gusoku2_ashi",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 970 , weight(18)|abundance(250)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["tosei_gusoku_sdn", "Tosei_Gusoku(sodenashi)", [("sdngusoku_ashi",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 1560 , weight(20)|abundance(240)|head_armor(0)|body_armor(41)|leg_armor(14)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["tosei_gusoku", "Tosei_Gusoku", [("gusoku_ashi",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 1750 , weight(22)|abundance(240)|head_armor(0)|body_armor(44)|leg_armor(14)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_aka_sdn", "Akaitoodoshi_Gusoku(sodenashi", [("sdngusoku_aka",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2350 , weight(20)|abundance(230)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_aka", "Akaitoodoshi_Gusoku", [("gusoku_aka",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2790 , weight(22)|abundance(230)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_momo_sdn", "Hiitoodoshi_Gusoku(sodenashi", [("sdngusoku_momo",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2350 , weight(20)|abundance(230)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_momo", "Hiitoodoshi_Gusoku", [("gusoku2_momo",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2790 , weight(22)|abundance(230)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_kon_sdn", "Konitoodoshi_Gusoku(sodenashi", [("sdngusoku_kon",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2350 , weight(20)|abundance(230)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_kon", "Konitoodoshi_Gusoku", [("gusoku2_kon",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2790 , weight(22)|abundance(230)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_kuro_sdn", "Kuroitoodoshi_Gusoku(sodenashi", [("sdngusoku_kuro",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2350 , weight(20)|abundance(230)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_kuro", "Kuroitoodoshi_Gusoku", [("gusoku2_kuro",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2790 , weight(22)|abundance(230)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_ao_sdn", "Aoitoodoshi_Gusoku(sodenashi", [("sdngusoku_ao",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2350 , weight(20)|abundance(230)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_ao", "Aoitoodoshi_Gusoku", [("gusoku_ao",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2790 , weight(22)|abundance(230)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(8) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["nanban_gusoku_sdn", "Nanbando_Gusoku(sodenashi", [("sdngusoku_black",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 3830 , weight(25)|abundance(210)|head_armor(0)|body_armor(52)|leg_armor(16)|difficulty(9) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["nanban_gusoku", "Nanbando_Gusoku", [("gusoku_black",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 5150 , weight(27)|abundance(210)|head_armor(0)|body_armor(55)|leg_armor(16)|difficulty(9) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["nanban_gusoku_slv_sdn", "Ginpakuoshi_Nanbando_Gusoku(sodenashi", [("sdngusoku_slv",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 5530 , weight(26)|abundance(190)|head_armor(0)|body_armor(54)|leg_armor(18)|difficulty(12) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["nanban_gusoku_slv", "Ginpakuoshi_Nanbando_Gusoku", [("gusoku_slv",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 6850 , weight(28)|abundance(190)|head_armor(0)|body_armor(57)|leg_armor(18)|difficulty(12) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["nanban_gusoku_gold_sdn", "Kinpakuoshi_Nanbando_Gusoku(sodenashi", [("sdngusoku_gold",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 5690 , weight(26)|abundance(190)|head_armor(0)|body_armor(55)|leg_armor(18)|difficulty(12) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["nanban_gusoku_gold", "Kinpakuoshi_Nanbando_Gusoku", [("gusoku_gold",0)], itp_type_body_armor |itp_merchandise|itp_covers_legs ,0,
 16150 , weight(28)|abundance(190)|head_armor(0)|body_armor(65)|leg_armor(22)|difficulty(20) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["gusoku_2", "Gusoku", [("gusoku2_ashif",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 650 , weight(16)|abundance(190)|head_armor(0)|body_armor(35)|leg_armor(10)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],

## atama
#["hitai_ate_white", "Hitai_Ate_White", [("armored_headband2",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair,0, 15 , weight(0.5)|abundance(150)|head_armor(10)|body_armor(0)|leg_armor(0) ,imodbits_armor ],
#["hitai_ate_black", "Hitai_Ate_Black", [("armored_headband",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair,0, 50 , weight(1)|abundance(150)|head_armor(14)|body_armor(0)|leg_armor(0) ,imodbits_armor ],
["haganeno_kitunemen_1", "Haganeno_Kitunemen", [("kitunemen1",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair| itp_covers_beard,0, 360 , weight(1.5)|abundance(240)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["haganeno_kitunemen_2", "Haganeno_Kitunemen", [("kitunemen2",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair| itp_covers_beard,0, 360 , weight(1.5)|abundance(240)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["haganeno_hannyamen_1", "Haganeno_Hannyamen", [("hannyamen1",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair| itp_covers_beard,0, 360 , weight(1.5)|abundance(240)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["haganeno_hannyamen_2", "Haganeno_Hannyamen", [("hannyamen2",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair| itp_covers_beard,0, 360 , weight(1.5)|abundance(240)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["shinobi_kabuto", "Shinobi_Kabuto", [("shinobikabuto",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head| itp_covers_beard,0, 950 , weight(1.75)|abundance(250)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(12) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
#["jin_kasa", "Jin_Kasa", [("kasa2",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair,0, 65 , weight(1.5)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["suji_kabuto_1", "Suji_Kabuto", [("shinobikabuto",0)], itp_type_head_armor|itp_merchandise,0, 150 , weight(1.75)|abundance(250)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["suji_kabuto_2", "Suji_Kabuto", [("kabuto1b",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 350 , weight(1.75)|abundance(250)|head_armor(34)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["tosei_suji_kabuto", "Tosei_Suji_Kabuto", [("kabuto2",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 390 , weight(2)|abundance(240)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["menho_with_tosei_suji_kabuto", "Menho_with_Tosei_Suji_Kabuto", [("kabuto2b",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head| itp_covers_beard,0, 750 , weight(2.25)|abundance(230)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["tatemono_with_tosei_suji_kabuto_1", "Tatemono_with_Tosei_Suji_Kabuto", [("kabuto2c",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 690 , weight(2)|abundance(230)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["tatemono_with_tosei_suji_kabuto_2", "Tatemono_with_Tosei_Suji_Kabuto", [("kabuto2d",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 980 , weight(2)|abundance(230)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["tatemono_with_tosei_suji_kabuto_3", "Tatemono_with_Tosei_Suji_Kabuto", [("kabuto3",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 690 , weight(2)|abundance(230)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["tatemono_with_tosei_suji_kabuto_4", "Tatemono_with_Tosei_Suji_Kabuto", [("kabuto3b",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head| itp_covers_beard,0, 1240 , weight(2.5)|abundance(240)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
#["ginpakuoshi_tosei_suji_kabuto", "Ginpakuoshi_Tosei_Suji_Kabuto", [("kabuto4_slv",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 910 , weight(2.25)|abundance()|)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
#["kinpakuoshi_tosei_suji_kabuto", "Kinpakuoshi_Tosei_Suji_Kabuto", [("kabuto3b_gold",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head| itp_covers_beard,0, 980 , weight(2.5)|abundance()|)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate ],
["kawari_kabuto_1", "Kawari_Kabuto", [("kawari_kabuto1",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 690 , weight(2.25)|abundance(210)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["kawari_kabuto_2", "Kawari_Kabuto", [("kawari_kabuto2",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 690 , weight(2.25)|abundance(210)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["kawari_kabuto_3", "Kawari_Kabuto", [("kawari_kabuto3",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 690 , weight(2.25)|abundance(210)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["ginpakuoshi_kawari_kabuto", "Ginpakuoshi_Kawari_Kabuto", [("kawari_kabuto4",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 1240 , weight(2.75)|abundance(140)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["kawari_kabuto_5", "Kawari_Kabuto", [("kawari_kabuto5",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 1240 , weight(2.75)|abundance(210)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["kawari_kabuto_6", "Kawari_Kabuto", [("kawari_kabuto6",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head| itp_covers_beard,0, 1240 , weight(2.75)|abundance(210)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["kawari_kabuto_7", "Kawari_Kabuto", [("kawari_kabuto7",0)], itp_type_head_armor|itp_merchandise|itp_fit_to_head,0, 1240 , weight(2.75)|abundance(210)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["kinpakuoshi_kawari_kabuto", "Kinpakuoshi_Kawari_Kabuto", [("kawari_kabutok",0)], itp_type_head_armor|itp_fit_to_head| itp_covers_beard,0, 13000 , weight(3)|abundance(190)|head_armor(65)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate, [],[fac_kingdom_9,fac_bushido_order] ],
["sohei_zukin", "Sohei_Zukin", [("soheizukin",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_covers_beard,0, 27 , weight(3)|abundance(240)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(13) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["high_sohei_zukin", "High_Sohei_Zukin", [("soheizukin",0)], itp_type_head_armor|itp_merchandise|itp_civilian| itp_covers_beard,0, 200 , weight(3)|abundance(210)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(18) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],


## ashi
#["waraji", "Waraji", [("waraji",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
# 54 , weight(0.6)|abundance(120)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0) ,imodbits_cloth ],
["kyahan", "Kyahan", [("kyahan",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 120 , weight(1)|abundance(260)|head_armor(0)|body_armor(0)|leg_armor(14)|difficulty(0) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["sune_ate_aka", "Sune_Ate_Aka", [("suneate2",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 280 , weight(2.8)|abundance(240)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["sune_ate_kuro", "Sune_Ate_Kuro", [("suneate1",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 460 , weight(2.8)|abundance(230)|head_armor(0)|body_armor(0)|leg_armor(23)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["hagane_no_sune_ate", "Hagane_no_Sune_Ate", [("suneate3",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 1150 , weight(2.8)|abundance(230)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
#["jinbaori_1", "Jinbaori_with_Suneate", [("jinbaori_suneate_6",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
# 870 , weight(4)|abundance(60)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(10) ,imodbits_armor ],
#["jinbaori_2", "Jinbaori_with_Suneate", [("jinbaori_suneate_5",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
# 870 , weight(4)|abundance(60)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(10) ,imodbits_armor ],
#["jinbaori_3", "Jinbaori_with_Suneate", [("jinbaori_suneate_4",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
# 870 , weight(4)|abundance(60)|head_armor(0)|body_armor(4)|leg_armor(23)|difficulty(10) ,imodbits_armor ],
#["busyo_jinbaori_1", "Busyo_Jinbaori_with_Suneate", [("jinbaori_suneate_1",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
# 1770 , weight(5)|abundance(40)|head_armor(0)|body_armor(6)|leg_armor(28)|difficulty(12) ,imodbits_armor ],
#["busyo_jinbaori_2", "Busyo_Jinbaori_with_Suneate", [("jinbaori_suneate_2",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
# 1770 , weight(5)|abundance(40)|head_armor(0)|body_armor(6)|leg_armor(28)|difficulty(12) ,imodbits_armor ],
["busyo_jinbaori_3", "Busyo_Jinbaori_with_Suneate", [("jinbaori_suneate_3",0)], itp_merchandise| itp_type_foot_armor | itp_civilian  | itp_attach_armature,0,
 1770 , weight(5)|abundance(210)|head_armor(0)|body_armor(6)|leg_armor(28)|difficulty(12) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],

## te
["tekko","Tekko", [("f_tekkou1_L",0)], itp_merchandise|itp_type_hand_armor,0, 80, weight(0.25)|abundance(250)|body_armor(2)|difficulty(0),imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["kote","Kote", [("f_tekkou1_L",0)], itp_merchandise|itp_type_hand_armor,0, 710, weight(0.25)|abundance(240)|body_armor(5)|difficulty(0),imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["hagane_no_kote","Hagane_no_Kote", [("kote_y_L",0)], itp_merchandise|itp_type_hand_armor,0, 1000, weight(0.75)|abundance(200)|body_armor(8)|difficulty(0),imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],

## ninja buki
["ninjato", "Ninjato", [("njbl",0),("njbl_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,
 415 , weight(1.5)|abundance(230)|difficulty(10)|spd_rtng(106) | weapon_length(90)|swing_damage(32 , pierce) | thrust_damage(28 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["izayoi", "Izayoi", [("njbl_b",0),("njbl_b_saya", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_back|itcf_show_holster_when_drawn,
 1700 , weight(1.5)|abundance(200)|difficulty(14)|spd_rtng(108) | weapon_length(95)|swing_damage(37 , pierce) | thrust_damage(34 ,  pierce),imodbits_sword_high, [],[fac_kingdom_9,fac_bushido_order] ],
["syuriken", "Syuriken", [("syuriken",0)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_knife|itcf_carry_dagger_front_left,
 260 , weight(2)|abundance(230)|difficulty(0)|spd_rtng(112) | shoot_speed(55) | thrust_damage(15 ,  pierce)|max_ammo(12)|weapon_length(0),imodbits_thrown, [],[fac_kingdom_9,fac_bushido_order] ],
["fuma_syuriken", "Fuma_Syuriken", [("fumastar",0)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_knife|itcf_carry_dagger_front_left,
 510 , weight(2)|abundance(230)|difficulty(2)|spd_rtng(110) | shoot_speed(50) | thrust_damage(18 ,  pierce)|max_ammo(10)|weapon_length(0),imodbits_thrown, [],[fac_kingdom_9,fac_bushido_order] ],
["kunai", "Kunai", [("kunai_ring2",0),("kunai_ring", ixmesh_carry)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_javelin|itcf_carry_quiver_front_right,
 300 , weight(2.5)|abundance(230)|difficulty(0)|spd_rtng(105) | shoot_speed(38) | thrust_damage(21 ,  pierce)|max_ammo(6)|weapon_length(20),imodbits_thrown, [],[fac_kingdom_9,fac_bushido_order] ],
["kunai_melee", "Kunai", [("kunai_ring2",0),("kunai_ring", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary , itc_dagger|itcf_carry_quiver_front_right,
 300 , weight(1)|abundance(230)|difficulty(0)|spd_rtng(108) | swing_damage(19, pierce) | thrust_damage(22 ,  pierce)|weapon_length(35),imodbits_thrown, [],[fac_kingdom_9,fac_bushido_order] ],
["kuro_kunai", "Kuro_Kunai", [("kunai_black2",0),("kunai_black", ixmesh_carry)], itp_type_thrown |itp_merchandise|itp_primary ,itcf_throw_javelin|itcf_carry_dagger_front_right,
 600 , weight(3)|abundance(230)|difficulty(3)|spd_rtng(103) | shoot_speed(40) | thrust_damage(24 ,  pierce)|max_ammo(6)|weapon_length(20),imodbits_thrown, [],[fac_kingdom_9,fac_bushido_order] ],
["kuro_kunai_melee", "Kuro_Kunai", [("kunai_black2",0),("kunai_black", ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary , itc_dagger|itcf_carry_dagger_front_right,
 600 , weight(1)|difficulty(3)|abundance(230)|spd_rtng(103) | swing_damage(24, pierce) | thrust_damage(28 ,  pierce)|weapon_length(35),imodbits_thrown, [],[fac_kingdom_9,fac_bushido_order] ],
["jinpumaru", "Jinpumaru", [("fumastar2",0)], itp_type_thrown |itp_merchandise|itp_primary,itcf_throw_axe|itcf_carry_round_shield,  ## CC-D cut: |itp_next_item_as_melee
 10000 , weight(3)|abundance(200)|difficulty(5)|spd_rtng(70) | shoot_speed(35) | thrust_damage(36 ,  cut)|max_ammo(10)|weapon_length(65),imodbits_thrown_minus_heavy, [],[fac_kingdom_9,fac_bushido_order] ],
#["jinpumaru_melee", "Jinpumaru", [("fumastar2",0)], itp_type_two_handed_wpn |itp_merchandise|itp_primary|itp_bonus_against_shield|itp_two_handed,itc_greatsword|itcf_carry_round_shield,
# 10000 , weight(1)|difficulty(5)|spd_rtng(92) | swing_damage(35, pierce) | thrust_damage(35 ,  pierce)|weapon_length(35),imodbits_thrown_minus_heavy ],
 
## ninja
["kakyu_kunoichi_syozoku_1", "Kakyu_Kunoichi_Syozoku", [("kunosyozoku",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 500 , weight(0.5)|abundance(230)|head_armor(0)|body_armor(30)|leg_armor(5)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["kakyu_kunoichi_syozoku_2", "Kakyu_Kunoichi_Syozoku", [("kunorobe_c2",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 630 , weight(2)|abundance(230)|head_armor(0)|body_armor(32)|leg_armor(7)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["cyukyu_kunoichi_syozoku", "Cyukyu_Kunoichi_Syozoku", [("kunorobeb",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 850 , weight(6)|abundance(220)|head_armor(0)|body_armor(38)|leg_armor(8)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["cyukyu_kunoichi_syozoku", "Cyukyu_Kunoichi_Syozoku", [("kunorobe_c",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 1060 , weight(8)|abundance(220)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["cyukyu_kunoichi_syozoku_with_mail", "Cyukyu_Kunoichi_Syozoku_with_Mail", [("kunosyozoku2",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 1120 , weight(10)|abundance(210)|head_armor(0)|body_armor(42)|leg_armor(10)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["jyokyu_kunoichi_syozoku_with_mail_1", "Jyokyu_Kunoichi_Syozoku_with_Mail", [("kunorobeb2",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 1900 , weight(10)|abundance(200)|head_armor(0)|body_armor(46)|leg_armor(12)|difficulty(10) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["jyokyu_kunoichi_syozoku_with_mail_2", "Jyokyu_Kunoichi_Syozoku_with_Mail", [("kunorobe_c3",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2400 , weight(12)|abundance(200)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(10) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["shinobi_yoroi_f", "Shinobi_Yoroi(kunoichi)", [("kunorobe_c4",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 4000 , weight(16)|abundance(190)|head_armor(0)|body_armor(50)|leg_armor(15)|difficulty(12) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["genin_syozoku_1", "Genin_Syozoku", [("ninja_robe3",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 848 , weight(3)|abundance(230)|head_armor(0)|body_armor(38)|leg_armor(9)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["genin_syozoku_2", "Genin_Syozoku", [("ninja_robe4",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 270 , weight(5)|abundance(230)|head_armor(0)|body_armor(18)|leg_armor(7)|difficulty(0) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["cyunin_syozoku_2", "Cyunin_Syozoku", [("ninja_robe1",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 720 , weight(12)|abundance(220)|head_armor(0)|body_armor(32)|leg_armor(10)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["jyonin_syozoku", "Jyonin_Syozoku", [("ninja_robe2",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 2200 , weight(15)|abundance(210)|head_armor(0)|body_armor(49)|leg_armor(15)|difficulty(10) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["shinobi_yoroi", "Shinobi_Yoroi", [("ninja_yoroi",0)], itp_merchandise| itp_civilian | itp_type_body_armor  |itp_covers_legs ,0,
 4200 , weight(18)|abundance(190)|head_armor(0)|body_armor(51)|leg_armor(16)|difficulty(12) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],

## ninja atama
["hachigane", "Hachigane", [("headgear",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair,0, 80 , weight(1)|abundance(230)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["shinobi_Zukin", "shinobi_Zukin", [("shinobizukin",0)], itp_type_head_armor|itp_merchandise| itp_covers_beard,0, 27 , weight(1)|abundance(230)|head_armor(12)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order] ],
["hachigane_with_shinobi_zukin", "Hachigane_with_Shinobi_Zukin", [("shinobizukin_b",0)], itp_type_head_armor|itp_merchandise| itp_covers_beard,0, 180 , weight(1.5)|abundance(230)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["shinobi_fukumen_1", "Shinobi_Fukumen", [("fukumen_blue",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair| itp_covers_beard,0, 160 , weight(1.25)|abundance(230)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["shinobi_fukumen_2", "Shinobi_Fukumen", [("fukumen_black",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair| itp_covers_beard,0, 160 , weight(1.25)|abundance(230)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["shinobi_fukumen_3", "Shinobi_Fukumen", [("fukumen_brown",0)], itp_type_head_armor|itp_merchandise| itp_doesnt_cover_hair| itp_covers_beard,0, 160 , weight(1.25)|abundance(230)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7) ,imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],


### kantou douran armor
[
 "dou_huku1", "dou_huku1", [("Huku1",0)], 
 itp_merchandise| itp_civilian| itp_type_body_armor| itp_covers_legs, 0, 3, weight(1)
 |abundance(250)| head_armor(0)| body_armor(5)| leg_armor(2)| difficulty(5), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_huku2", "dou_huku2", [("Huku2",0)], 
 itp_type_body_armor| itp_merchandise| itp_covers_legs| itp_civilian, 0, 7, weight(1)
 |abundance(250)| head_armor(0)| body_armor(7)| leg_armor(3)| difficulty(5), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_huku4", "dou_huku4", [("dou_huku4",0)], 
 itp_merchandise| itp_civilian| itp_type_body_armor| itp_covers_legs, 0, 7, weight(1)
 |abundance(250)| head_armor(0)| body_armor(7)| leg_armor(2)| difficulty(5), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "touki_wo_obita_dou_huku1", "Touki wo Obita Huku1", [("Huku1",0)], 
 itp_merchandise| itp_civilian| itp_type_body_armor| itp_covers_legs, 0, 2000, weight(1)
 |abundance(250)| head_armor(0)| body_armor(40)| leg_armor(5)| difficulty(5), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "touki_wo_obita_dou_huku2", "Touki wo Obita Huku2", [("Huku2",0)], 
 itp_type_body_armor| itp_merchandise| itp_covers_legs| itp_civilian, 0, 2000, weight(1)
 |abundance(250)| head_armor(0)| body_armor(38)| leg_armor(10)| difficulty(5), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "touki_wo_obita_dou_huku4", "Touki wo Obita Huku4", [("dou_huku4",0)], 
 itp_merchandise| itp_civilian| itp_type_body_armor| itp_covers_legs, 0, 2000, weight(1)
 |abundance(250)| head_armor(0)| body_armor(38)| leg_armor(10)| difficulty(5), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "cn_sdn_haori_hakama_1", "Sodenashi_Haori_Hakama", [("samurai_civil_a",0)], 
  itp_merchandise| itp_type_body_armor| itp_covers_legs| itp_civilian, 0, 300, weight(1.3)
  |abundance(240)| head_armor(0)| body_armor(21)| leg_armor(17)| difficulty(5), imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "high_sdn_haori_hakama", "high_Sodenashi_Haori_Hakama", [("samurai_civil_a",0)], 
  itp_merchandise| itp_type_body_armor| itp_covers_legs| itp_civilian, 0, 1000, weight(1.3)
  |abundance(200)| head_armor(0)| body_armor(41)| leg_armor(2)| difficulty(5), imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_hachimaki", "Dou_Hachimaki", [("Hachimaki1",0)], 
  itp_merchandise| itp_type_head_armor| itp_doesnt_cover_hair ,0, 40, weight(0.2)
  |abundance(250)| head_armor(5)| body_armor(0)| leg_armor(0)| difficulty(5) ,imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "touki_wo_obita_hachimaki", "Touki_wo_Obita_Hachimaki", [("Hachimaki1",0)], 
  itp_merchandise| itp_type_head_armor| itp_doesnt_cover_hair ,0, 690, weight(0.2)
  |abundance(200)| head_armor(38)| body_armor(0)| leg_armor(0)| difficulty(5) ,imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],

### kantou douran head
[
 "dou_kasa1", "dou_kasa1", [("dou_kasa1",0)], 
 itp_merchandise| itp_type_head_armor|itp_doesnt_cover_hair ,0, 20, weight(0.4)
 |abundance(250)| head_armor(10)| body_armor(0)| leg_armor(0)| difficulty(5), imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "touki_wo_obita_kasa", "Touki_wo_Obita_kasa", [("dou_kasa1",0)], 
 itp_merchandise| itp_type_head_armor|itp_doesnt_cover_hair ,0, 1200, weight(0.4)
 |abundance(200)| head_armor(43)| body_armor(0)| leg_armor(0)| difficulty(5), imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_warazukin1", "dou_warazukin1", [("dou_warazukin1",0)], 
 itp_merchandise| itp_type_head_armor ,0, 36, weight(0.2)
 |abundance(240)| head_armor(14)| body_armor(0)| leg_armor(0)| difficulty(5) ,imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],
### kantou douran ashi
[
 "dou_waraji1", "dou_waraji1", [("dou_waraji1",0)],
 itp_merchandise| itp_type_foot_armor| itp_civilian| itp_attach_armature, 0, 10, weight(0.1)
 |abundance(250)| head_armor(0)| body_armor(0)| leg_armor(1)| difficulty(5) ,imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "touki_wo_obita_waraji", "Touki_wo_Obita_waraji", [("dou_waraji1",0)],
 itp_merchandise| itp_type_foot_armor| itp_civilian| itp_attach_armature, 0, 300, weight(0.1)
 |abundance(200)| head_armor(0)| body_armor(0)| leg_armor(20)| difficulty(5) ,imodbits_cloth , [],[fac_kingdom_9,fac_bushido_order]
],

## kantou douran buki
[
 "dou_tekkoukagi","dou_tekkoukagi", [("dou_tekkoukagi",0)], 
 itp_type_one_handed_wpn| itp_merchandise| itp_primary| itp_secondary, 
 itc_longsword, 140, weight(0.3)
 | abundance(186)| difficulty(3)| spd_rtng(115)| weapon_length(10)| swing_damage(28,cut)| thrust_damage(18, pierce), 
 imodbits_sword_high , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "miyagemono_no_bokutou","Miyagemono_no_Bokutou", [("dou_bokutou2",0)], 
 itp_type_two_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry|itp_wooden_attack, 
 itc_bastardsword, 50, weight(1.3)
 |abundance(210)| spd_rtng(100)| weapon_length(70)| swing_damage(24,blunt)| thrust_damage(19,blunt), imodbits_none, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "kidachi","Kidachi", [("dou_bokutou2",0)], 
 itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry|itp_wooden_attack, 
 itc_bastardsword, 300, weight(1.3)
 |abundance(210)| spd_rtng(104)| weapon_length(70)| swing_damage(28,blunt)| thrust_damage(20,blunt), imodbits_none, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "touyako","Touyako", [("dou_bokutou2",0)], 
 itp_type_two_handed_wpn|itp_merchandise|itp_primary|itp_wooden_parry|itp_wooden_attack, 
 itc_bastardsword, 1750, weight(1.3)
 |abundance(200)| spd_rtng(100)| weapon_length(70)| swing_damage(36,blunt)| thrust_damage(30,blunt), imodbits_none, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "miyagemono_no_bokutou","Miyagemono_no_Bokutou", [("dou_bokutou3",0)], 
 itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary |itp_no_parry|itp_wooden_parry|itp_wooden_attack, 
 itc_longsword, 50, weight(0.3)
 |abundance(240)| spd_rtng(107)| weapon_length(27)| swing_damage(21,blunt)| thrust_damage(16,blunt), imodbits_none, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "mokusei_tantou","Mokusei_Tantou", [("dou_bokutou3",0)], 
 itp_type_one_handed_wpn|itp_merchandise|itp_primary|itp_secondary |itp_no_parry|itp_wooden_parry|itp_wooden_attack|itp_penalty_with_shield, 
 itc_longsword, 300, weight(0.2)
 |abundance(200)| spd_rtng(125)| weapon_length(27)| swing_damage(26,blunt)| thrust_damage(21,blunt), imodbits_none, [],[fac_kingdom_9,fac_bushido_order]
],

[
 "dou_takeyari", "Takeyari", [("dou_takeyari",0)], 
  itp_type_two_handed_wpn| itp_merchandise| itp_primary| itp_penalty_with_shield| itp_wooden_parry| itp_two_handed, 
  itc_staff| itcf_carry_spear, 40, weight(1.5)
  |abundance(250)| difficulty(5)| spd_rtng(89)| weapon_length(160)| swing_damage(18, blunt)| thrust_damage(23, pierce),
  imodbit_bent |imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered| imodbit_masterwork , [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_takeyari_long2", "dou_takeyari_long2", [("dou_takeyari_long2",0)], 
 itp_couchable| itp_type_two_handed_wpn| itp_offset_lance| itp_merchandise| itp_primary| itp_penalty_with_shield| itp_wooden_parry| itp_two_handed, 
 itc_cutting_spear| itcf_carry_spear, 60 , weight(2.2)
 | abundance(250)| difficulty(6)| spd_rtng(73)| weapon_length(250)| swing_damage(20, blunt)| thrust_damage(26, pierce),
 imodbit_bent |imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered| imodbit_masterwork, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_takeyari_long1", "dou_takeyari_long1", [("dou_takeyari_long1",0)], 
  itp_type_two_handed_wpn|itp_merchandise| itp_primary| itp_penalty_with_shield| itp_wooden_parry| itp_two_handed| itp_cant_use_on_horseback,  
  itc_cutting_spear| itcf_carry_spear, 90, weight(3.0)
  |abundance(250)| difficulty(8)| spd_rtng(69)| weapon_length(420)| swing_damage(23, blunt)| thrust_damage(25, pierce), 
  imodbit_bent |imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered| imodbit_masterwork, [],[fac_kingdom_9,fac_bushido_order]
],
["gonbe", "Gonbe", [("dou_takeyari",0)],
 itp_type_polearm|itp_merchandise|itp_primary|itp_penalty_with_shield| itp_wooden_parry|itp_crush_through|itp_two_handed, 
 itc_cutting_spear|itcf_carry_spear, 3000, weight(1.5)|difficulty(1)|spd_rtng(130)|weapon_length(160)|swing_damage(0,cut)|thrust_damage(41,pierce), imodbit_masterwork, [],[fac_kingdom_9,fac_bushido_order]
 ],
[
"tago", "Tago", [("military_sickle_a",0)],
 itp_type_thrown|itp_merchandise|itp_primary,
 itcf_throw_axe, 3000, weight(4)|difficulty(1)|spd_rtng(99)|shoot_speed(30)|thrust_damage(30,cut)|max_ammo(10)|weapon_length(74),
 imodbits_thrown_minus_heavy, [],[fac_kingdom_9,fac_bushido_order]
 ],

[
 "namakura_nagamaki", "namakura_Nagamaki", [("Nagamaki1",0)], 
 itp_type_polearm| itp_merchandise| itp_primary| itp_penalty_with_shield| itp_wooden_parry| itp_two_handed,
 itc_nodachi| itcf_carry_sword_back, 4000 , weight(6.2)
 |abundance(240)| difficulty(14)| spd_rtng(79)| weapon_length(200)| swing_damage(34, cut)| thrust_damage(30,  pierce), 
 imodbit_bent |imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered| imodbit_masterwork, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_nagamaki", "Dou_Nagamaki", [("Nagamaki1",0)], 
 itp_type_polearm| itp_merchandise| itp_primary| itp_penalty_with_shield| itp_wooden_parry| itp_two_handed,
 itc_nodachi| itcf_carry_sword_back, 4000 , weight(6.2)
 |abundance(230)| difficulty(14)| spd_rtng(82)| weapon_length(200)| swing_damage(41, cut)| thrust_damage(35,  pierce), 
 imodbit_bent |imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered| imodbit_masterwork, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "wazamono_nagamaki", "Wazamono_Nagamaki", [("Nagamaki1",0)], 
 itp_type_polearm| itp_merchandise| itp_primary| itp_penalty_with_shield| itp_wooden_parry| itp_two_handed,
 itc_nodachi| itcf_carry_sword_back, 4000 , weight(6.2)
 |abundance(200)| difficulty(14)| spd_rtng(82)| weapon_length(200)| swing_damage(47, cut)| thrust_damage(42,  pierce), 
 imodbit_bent |imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered| imodbit_masterwork, [],[fac_kingdom_9,fac_bushido_order]
],

## tate
[
 "dou_taketaba", "dou_taketaba",   [("dou_taketaba1m_soubi" ,0)], 
 itp_merchandise| itp_type_shield| itp_cant_use_on_horseback| itp_wooden_parry, 
 itcf_carry_board_shield, 200, weight(14.2)
 | abundance(250)| difficulty(0)| hit_points(320)| body_armor(18)| spd_rtng(40)| shield_width(70)| shield_height(100), 
 imodbits_shield, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_kidatel1", "dou_KidateL1", [("KidateL1_Soubi" ,0)], 
 itp_merchandise| itp_type_shield| itp_cant_use_on_horseback| itp_wooden_parry,
 itcf_carry_board_shield, 250, weight(8.0)
 | abundance(260)| difficulty(0)| hit_points(130)| body_armor(12)| spd_rtng(50)| shield_width(76)| shield_height(101),
 imodbits_shield, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_kidates1", "dou_kidateS1", [("KidateS1",0)], 
 itp_type_shield| itp_merchandise| itp_wooden_parry,
 itcf_carry_round_shield, 100, weight(3.0)
 | abundance(250) |difficulty(0)| hit_points(130)| body_armor(9)| spd_rtng(100)| shield_width(40),
 imodbits_shield, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_kidate_practice", "dou_kidate_practice", [("KidateS1",0)], 
 itp_type_shield|itp_merchandise| itp_wooden_parry,
 itcf_carry_round_shield, 100, weight(3.0)
 | abundance(240) | hit_points(130)| body_armor(9)| spd_rtng(100)| shield_width(40),
 imodbits_shield, [],[fac_kingdom_9,fac_bushido_order]
],

#occc buffed japanese bows accuracy and tweaked
#yumi
[
 "dou_marukiyumi", "dou_marukiyumi", [("Douran_Yumi5",0),("Douran_Yumi5_carry",ixmesh_carry)],
 itp_type_bow| itp_merchandise| itp_primary| itp_two_handed,
 itcf_shoot_bow| itcf_carry_bow_back, 30, weight(1)
 | abundance(260)| difficulty(0)| spd_rtng(82)| shoot_speed(61)| accuracy(99)| thrust_damage(24, cut),
 imodbits_bow, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_hankyuu", "Dou_Hankyuu", [("Douran_Yumi4",0),("Douran_Yumi4_carry",ixmesh_carry)], 
 itp_type_bow| itp_merchandise| itp_primary| itp_two_handed,
 itcf_shoot_bow| itcf_carry_bow_back, 370, weight(1.1)
 | abundance(250)| difficulty(2)| spd_rtng(65)| shoot_speed(65)| accuracy(99)| thrust_damage(26, pierce),
 imodbits_bow, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_kurourushinuriyumi", "Dou_KurourushinuriYumi", [("Douran_Yumi2",0),("Douran_Yumi2_carry",ixmesh_carry)],
 itp_type_bow| itp_merchandise| itp_primary| itp_two_handed,
 itcf_shoot_bow| itcf_carry_bow_back, 670, weight(1.45)
 | abundance(240)| difficulty(3)| spd_rtng(63)| shoot_speed(69)| accuracy(99)| thrust_damage(28, pierce),
 imodbits_bow, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "fusetake_yumi", "Fusetake_Yumi", [("yumi",0)], 
 itp_type_bow| itp_merchandise| itp_primary| itp_two_handed,
 itcf_shoot_bow| itcf_carry_bow_back, 670, weight(1.5)
 | abundance(230)| difficulty(4)| spd_rtng(63)| shoot_speed(69)| accuracy(99)| thrust_damage(31, pierce),
 imodbits_bow, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_sanmaiuchiyumi", "Dou_SanmaiuchiYumi", [("Douran_Yumi1",0),("Douran_Yumi1_carry",ixmesh_carry)],
 itp_type_bow| itp_merchandise| itp_primary| itp_two_handed,
 itcf_shoot_bow| itcf_carry_bow_back, 1210, weight(1.75)
 | abundance(220)| difficulty(4)| spd_rtng(61)| shoot_speed(70)| accuracy(99)| thrust_damage(33, pierce), 
 imodbits_bow, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "shigeto_yumi", "Shigeto_Yumi", [("heavy_yumi",0)], 
 itp_type_bow| itp_merchandise| itp_primary| itp_two_handed,
 itcf_shoot_bow| itcf_carry_bow_back, 2200, weight(1.8)
 | abundance(210)| difficulty(6)| spd_rtng(59)| shoot_speed(73)| accuracy(99)| thrust_damage(37, pierce),
 imodbits_bow, [],[fac_kingdom_9,fac_bushido_order]
],
[
 "dou_hazuyari","Dou_Hazuyari", [("Douran_Yumi3",0),("Douran_Yumi3", ixmesh_carry)], 
 itp_type_bow| itp_merchandise| itp_primary| itp_two_handed,  ## CC-D cut: |itp_next_item_as_melee
 itcf_shoot_bow, 2500, weight(1.75)
 | abundance(200)| difficulty(8)| spd_rtng(57)| shoot_speed(73)| accuracy(99)| thrust_damage(39, pierce),
 imodbits_bow, [],[fac_kingdom_9,fac_bushido_order]
],
#[
# "dou_hazuyari_melee","Dou_Hazuyari", [("Douran_Yumi3",0)], 
# itp_type_polearm| itp_primary|itp_merchandise| itp_wooden_parry| itp_penalty_with_shield,
# itc_staff, 2500, weight(1.75)
# | difficulty(0)| spd_rtng(87)| swing_damage(25, cut)| thrust_damage(21, pierce)| weapon_length(165),
# imodbits_polearm 
#],
#occc end

#ya damage occc +6
[
 "so_ya","So_ya", [("dou_arrow_hirane",0),("dou_arrow_hirane_fly",ixmesh_flying_ammo),("dou_utsubo", ixmesh_carry)], 
 itp_type_arrows|itp_merchandise|itp_default_ammo, 
 itcf_carry_quiver_back, 220, weight(1.6)
 |abundance(270)|weapon_length(95)|thrust_damage(10,pierce)|max_ammo(28),imodbits_missile,missile_distance_trigger,[fac_kingdom_9,fac_bushido_order]
],
[
 "karimata_ya","Karimata_ya", [("dou_arrow_karimata",0),("dou_arrow_karimata_fly",ixmesh_flying_ammo),("dou_utsubo", ixmesh_carry)],
 itp_type_arrows|itp_merchandise, 
 itcf_carry_quiver_back, 370, weight(1.6)
 |abundance(240)|weapon_length(95)|thrust_damage(11,pierce)|max_ammo(28),imodbits_missile,missile_distance_trigger,[fac_kingdom_9,fac_bushido_order]
],
[
 "hirae_ya","Hirae_ya", [("dou_arrow_hirane",0),("dou_arrow_hirane_fly",ixmesh_flying_ammo),("dou_utsubo", ixmesh_carry)],
 itp_type_arrows|itp_merchandise, 
 itcf_carry_quiver_back, 610, weight(1.6)
 |abundance(230)|weapon_length(95)|thrust_damage(13,pierce)|max_ammo(28),imodbits_missile,missile_distance_trigger,[fac_kingdom_9,fac_bushido_order]
],
[
 "watakuri_ya","Watakuri_ya", [("dou_arrow_watakuri",0),("dou_arrow_watakuri_fly",ixmesh_flying_ammo),("dou_utsubo", ixmesh_carry)], 
 itp_type_arrows|itp_merchandise, 
 itcf_carry_quiver_back, 1020,weight(1.6)
 |abundance(220)|weapon_length(95)|thrust_damage(15,pierce)|max_ammo(28),imodbits_missile,missile_distance_trigger,[fac_kingdom_9,fac_bushido_order]
],
[
 "hamaya","Hamaya", [("karimata_ya",0),("flying_arrow",ixmesh_flying_ammo),("quiver", ixmesh_carry)], 
 itp_type_arrows|itp_merchandise| itp_default_ammo, 
 itcf_carry_quiver_back, 2000, weight(1.6)
 |abundance(200)| weapon_length(95)| thrust_damage(16, pierce)| max_ammo(28), imodbits_missile, missile_distance_trigger,[fac_kingdom_9,fac_bushido_order]
],

#buffed tanegasimas
[
 "teppou", "Teppou", [("Arquebus",0)],
 itp_type_musket| itp_merchandise| itp_primary| itp_two_handed| itp_bonus_against_shield, itcf_shoot_musket| itcf_reload_musket| itcf_carry_sword_back,
 4200, weight(2.1) |abundance(270)|difficulty(0)|spd_rtng(40) | shoot_speed(90) | thrust_damage(90, pierce)|max_ammo(1)|accuracy(85),imodbits_crossbow,
 [(ti_on_weapon_attack,[(play_sound,"snd_rifle_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_9,fac_bushido_order ] ],

[
 "dou_tanegashima", "dou_tanegashima", [("dou_tanegashima",0)], 
 itp_type_musket| itp_merchandise| itp_primary| itp_two_handed| itp_bonus_against_shield, itcf_shoot_musket| itcf_reload_musket| itcf_carry_sword_back,
 8500, weight(2.5) |abundance(250)|difficulty(0)|spd_rtng(40) | shoot_speed(90) | thrust_damage(110, pierce)|max_ammo(1)|accuracy(90),imodbits_crossbow,
 [(ti_on_weapon_attack,[(play_sound,"snd_rifle_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_9,fac_bushido_order ] ],
 
[
 "wazamono_tanegashima", "Wazamono_Tanegashima", [("dou_tanegashima",0)], itp_type_musket| itp_merchandise| itp_primary| itp_two_handed| itp_bonus_against_shield, itcf_shoot_musket| itcf_reload_musket| itcf_carry_sword_back,
 12000, weight(2.5) |abundance(190)|difficulty(0)|spd_rtng(40) | shoot_speed(140) | thrust_damage(115, pierce)|max_ammo(1)|accuracy(95),imodbits_crossbow,
 [(ti_on_weapon_attack,[(play_sound,"snd_rifle_shot"),(call_script, "script_ccd_gun_particle", 1),])], [fac_kingdom_9,fac_bushido_order ] ],


###new_Musketer
["musketeer_hat1", "Musketeer Hat", [("art_shako_off",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],
["high_musketeer_hat1", "High Musketeer Hat", [("landcav_shako_sarg",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],
["musketeer_hat2", "Musketeer Hat", [("schles_shako_off",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],
["high_musketeer_hat2", "High Musketeer Hat", [("land_shako_ranker",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],

["grenadier_hat", "Grenadier Hat", [("brit_art_rank_shako",0)], itp_type_head_armor|itp_merchandise, 0, 2000, weight(1)|abundance(50)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],
["pope_hat", "Pope Hat", [("rus_pavlovsk_ranker",0)], itp_type_head_armor|itp_merchandise, 0, 2500, weight(1.5)|abundance(75)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],

["chevalier_helmet", "Chevalier Helmet", [("rus_chevalier_hat",0)], itp_type_head_armor|itp_merchandise, 0, 2000, weight(2.0)|abundance(55)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],
["high_chevalier_helmet", "High Chevalier Helmet", [("rus_chevalier_hat_off",0)], itp_type_head_armor|itp_merchandise, 0, 2500, weight(2.0)|abundance(50)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],

["highlander_hat", "Highlander Hat", [("Feather_bonnet_ranker",0)], itp_type_head_armor|itp_merchandise, 0, 2000, weight(1)|abundance(70)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ,[], [fac_kingdom_3]],
["highlander_boots", "Highlander Boots", [("scottish_boots",0)], itp_type_foot_armor|itp_civilian, 0, 2000, weight(1.25)|abundance(70)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ,[], [fac_kingdom_3]],
["highlander_uniform", "Highlander Coat", [("british_highlander",0)], itp_type_body_armor|itp_covers_legs, 0, 2000, weight(12)|abundance(70)|head_armor(0)|body_armor(25)|leg_armor(15)|difficulty(0), imodbits_cloth ,[], [fac_kingdom_3]],

  ["mm_ancieant_mail", "Ancient Mail", [("roman_mail3", 0),], itp_type_body_armor|itp_covers_legs, 0, 700, weight(13.5)|body_armor(31)|leg_armor(9), imodbit_old|imodbit_cheap ],
  ["mm_ancient_scale", "Ancient Scale", [("scale2", 0),], itp_type_body_armor|itp_covers_legs, 0, 1200, weight(15)|body_armor(46)|leg_armor(11), imodbit_old|imodbit_cheap ],

  ["mm_ancient_lame", "Ancient Lamellar", [("lam2", 0),], itp_type_body_armor|itp_covers_legs, 0, 800, weight(19)|abundance(160)|body_armor(47)|leg_armor(14), imodbit_old|imodbit_cheap ],
  ["mm_horse_armor", "Horseman Armor", [("avar_armor", 0),], itp_type_body_armor, 0, 700, weight(14.25)|abundance(90)|body_armor(35)|leg_armor(14), imodbit_old ],
  ["mm_horned_helmet", "Horned Helmet", [("horned_helmet", 0),], itp_type_head_armor, 0, 700, weight(2)|head_armor(22), imodbit_old ],

  ["mm_pagan_spear", "Pagan Spear", [("a_pagan_spear", 0),], itp_type_polearm|itp_wooden_parry|itp_primary|itp_penalty_with_shield|itp_unbalanced, itc_spear_new, 5, weight(5.5)|spd_rtng(80)|weapon_length(185)|thrust_damage(23, pierce), imodbits_polearm ],
  ["mm_iphicrates_doru", "Iphicrates Doru", [("w_iphicrates_doru_2", 0),], itp_type_polearm|itp_no_parry|itp_primary|itp_secondary, itcf_carry_spear|itc_spear_new|itcf_force_64_bits, 800, weight(2.5)|spd_rtng(120)|weapon_length(240)|thrust_damage(26, pierce)|swing_damage(21, pierce), imodbits_none ],
  ["mm_cloth", "Cloth", [("coat1_head", 0),], itp_type_head_armor|itp_doesnt_cover_hair, 0, 20, weight(1)|body_armor(12), imodbits_cloth, [], [fac_kingdom_4]],
  ["mm_pagan_wolfmask", "Berserker Wolfmask", [("cave_m_body_head", 0),], itp_type_head_armor, 0, 15, weight(1)|abundance(160)|head_armor(11)|body_armor(3), imodbits_cloth ],
#  ["ancient_late_helm", "Ancient Late Helm", [("legion_helm_01", 0),], itp_type_head_armor, 0, 700, weight(2.25)|abundance(90)|head_armor(29), imodbit_old ],
  ["mm_ancient_bronze_helm", "Ancient Bronze Helm", [("legion_helm_11", 0),], itp_type_head_armor|itp_merchandise, 0, 700, weight(3)|head_armor(29), imodbit_old ,[], [fac_kingdom_8]],
  ["ancieant_heavy_armor", "Ancieant Heavy Armor", [("legion_armor_2", 0),], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 700, weight(19)|body_armor(27), imodbit_old ,[], [fac_kingdom_8]],
  ["mm_ancient_cloth_armor", "Ancient Cloth Armor", [("legion_armor_1", 0),], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 700, weight(8.5)|body_armor(19), imodbit_old ,[], [fac_kingdom_8]],
  ["mm_ancient_cloth_armor2", "Ancient Cloth Armor", [("legion_armor_5", 0),], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 700, weight(9)|abundance(90)|body_armor(20), imodbit_old ,[], [fac_kingdom_8] ],
  ["mm_sarissa", "Sarissa", [("w_mak_sarissa", 0),], itp_type_polearm|itp_two_handed|itp_primary|itp_crush_through|itp_unbalanced|itp_merchandise|itp_can_knock_down, itcf_carry_spear|itcf_thrust_polearm|itcf_force_64_bits, 3, weight(1.5)|spd_rtng(103)|weapon_length(380)|thrust_damage(28, pierce)|swing_damage(16, blunt), imodbits_none,[], [fac_kingdom_8] ],#sarissa got buffed 18->26
  ["mm_ancient_spear", "Ancient Spear", [("w_greek_spear_doru_steel", 0),], itp_type_polearm|itp_wooden_parry|itp_primary|itp_secondary|itp_penalty_with_shield, itc_spear_new, 2000, weight(4.5)|spd_rtng(152)|weapon_length(125)|swing_damage(16,blunt)|thrust_damage(25, pierce), imodbits_polearm ],
  ["scutum_red_triarii", "Scutum Red", [("scutum_red_triarii", 0),], itp_type_shield|itp_wooden_parry, itcf_carry_board_shield, 1000, weight(5.5)|body_armor(29)|leg_armor(24)|hit_points(330)|spd_rtng(88)|shield_height(100)|shield_width(43), imodbits_none ],
  ["scutum_white", "Scutum White", [("scutum_white", 0),], itp_type_shield, itcf_carry_board_shield, 800, weight(5)|body_armor(28)|leg_armor(22)|hit_points(300)|spd_rtng(92)|shield_height(100)|shield_width(43), imodbits_shield ],
  ["clipeusshield", "Clipeusshield", [("Clipeusshield", 0),], itp_type_shield|itp_merchandise, itcf_carry_board_shield, 400, weight(2)|abundance(160)|body_armor(20)|hit_points(450)|spd_rtng(100)|shield_width(92), imodbits_shield,[], [fac_kingdom_8] ],
  ["pelta", "Pelta", [("pelta", 0),], itp_type_shield|itp_merchandise, itcf_carry_board_shield, 200, weight(2.25)|abundance(90)|body_armor(5)|leg_armor(4)|hit_points(100)|spd_rtng(99)|shield_width(45), imodbits_shield,[], [fac_kingdom_8] ],
  ["snakehoplon", "Snake Hoplon", [("snakehoplon", 0),], itp_type_shield|itp_cant_use_on_horseback|itp_merchandise, itcf_carry_round_shield, 2000, weight(10)|body_armor(20)|leg_armor(20)|difficulty(4)|hit_points(500)|spd_rtng(76)|shield_width(90), imodbits_shield,[], [fac_kingdom_8] ],
  ["spartanhoplon", "Spartan Hoplon", [("spartanhoplon", 0),], itp_type_shield|itp_cant_use_on_horseback, itcf_carry_round_shield, 2500, weight(12)|body_armor(25)|leg_armor(25)|difficulty(4)|hit_points(500)|spd_rtng(73)|shield_width(90), imodbits_shield,[], [fac_kingdom_8] ],
  ["mm_sun_warpaint", "Sun Warpaint", [("sun_warpaint", 0),], itp_type_body_armor|itp_covers_legs, 0, 10, weight(0.5)|head_armor(2)|body_armor(2)|leg_armor(2), imodbit_old ],
  ["mm_ape_body", "Ape Body", [("ape_body", 0),], itp_type_body_armor|itp_covers_legs, 0, 3, weight(0.5)|head_armor(33)|body_armor(33)|leg_armor(33), imodbits_none ],

## CC-D begin
#["ccd_blank1", "blank for edit", [("stone_6", 0)], 0, 0, 1, 0, 0 ],
#["ccd_blank2", "blank for edit", [("stone_6", 0)], 0, 0, 1, 0, 0 ],
#["ccd_blank3", "blank for edit", [("stone_6", 0)], 0, 0, 1, 0, 0 ],
#["ccd_blank4", "blank for edit", [("stone_6", 0)], 0, 0, 1, 0, 0 ],
## CC-D end

 ##Project Age Of Machinery begin-----------------------------------------------
 ["mangonel","Mangonel", [("mangonel",0)], itp_unique|itp_type_goods, 0,1000,weight(60)|abundance(60),imodbits_none],
 ["onager","Onager", [("Catapult",0)], itp_unique|itp_type_goods, 0,1000,weight(60)|abundance(60),imodbits_none],
 ["trebuchet","Trebuchet", [("trebuchet_new",0)], itp_unique|itp_type_goods, 0,1000,weight(60)|abundance(60),imodbits_none],
 ["rocks","Rocks", [("rus_helmet_a",0)], itp_unique|itp_type_goods, 0,150,weight(60)|abundance(60),imodbits_none],
 ["rocks_odd","rocks", [("rus_helmet_a",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["unused","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
 ["end","unused", [("stone_6",0)], itp_unique|itp_type_goods, 0,0,weight(60)|abundance(60),imodbits_none],
#Project Age Of Machinery end-----------------------------------------------


##################################
#Items imported from Firearm05
##################################
["maid_wear", "Maid_Wear", [("maid_wear", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(5)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["maid_shoes", "Maid_Shoes", [("maid_shoes", 0)], itp_type_foot_armor|itp_civilian|itp_attach_armature, 0, 256, weight(0.5)|head_armor(0)|body_armor(0)|leg_armor(1)|difficulty(0), imodbits_cloth ],
["maid_shoes2", "Maid_Shoes", [("maid_shoes2", 0)], itp_type_foot_armor|itp_civilian|itp_attach_armature, 0, 256, weight(0.5)|head_armor(0)|body_armor(0)|leg_armor(1)|difficulty(0), imodbits_cloth ],

["combat_maid_wear1", "Combat_Maid_Wear", [("combat_maid_wear1", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(5)|body_armor(25)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["combat_maid_wear2", "Combat_Maid_Socks", [("combat_maid_wear2", 0)], itp_type_foot_armor|itp_civilian|itp_attach_armature, 0, 256, weight(0.5)|head_armor(0)|body_armor(5)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["maid_helmet_a", "Maid_Stahl_Helm", [("maid_helmet_a",0)], itp_merchandise| itp_type_head_armor |itp_civilian|itp_fit_to_head ,0, 700, weight(0.5)|abundance(30)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],
["maid_helmet_b", "Maid_Reinforced_Stahl_Helm", [("maid_helmet_b",0)], itp_merchandise| itp_type_head_armor |itp_civilian|itp_fit_to_head ,0, 700, weight(0.5)|abundance(30)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_cloth ],

##################################
#Items imported from Firearm05 end
##################################


###################
##FROM SW conquest!
###################
["darth_vader_helmet", "Darth Vader's Helmet", [("dvader_helm",0)], itp_type_head_armor|itp_civilian|itp_covers_head ,0, 2000 , weight(2)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_none ],
["darth_vader_armor", "Darth Vader's Armor",   [("dvader_body",0)], itp_type_body_armor |itp_covers_legs |itp_civilian  ,0, 3000 , weight(27)|head_armor(0)|body_armor(50)|leg_armor(18)|difficulty(0) ,imodbits_none ],
["darth_vader_feet", "Darth Vader's Feet", [("gohst",0),("transparent_helmet_inv",ixmesh_inventory)], itp_unique|itp_type_foot_armor|itp_civilian,0, 1 , weight(0.25)|abundance(0)|difficulty(63)|head_armor(18)|body_armor(23)|leg_armor(69)|difficulty(0) ,imodbits_none ],
["transparent_hands", "Transparent Hands", [("gohst",0),("transparent_helmet_inv",ixmesh_inventory)], itp_unique|itp_type_hand_armor|itp_civilian,0, 1 , weight(0.25)|abundance(0)|head_armor(0)|body_armor(1)|leg_armor(0)|difficulty(0) ,imodbits_none ], 
["occc_battle_droid_body", "Battle_Droid_Body", [("battledroid",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_covers_head, 0, 
 720 , weight(10)|abundance(10)|head_armor(34)|body_armor(34)|leg_armor(34)|difficulty(0) ,imodbits_armor ],#Stormtrooper_body

["imperial_stormtrooper_helmet", "Imperial Stormtrooper Helmet", [("Stormtrooper_helm",0)],itp_type_head_armor|itp_covers_head|itp_civilian ,0, 
 195 , weight(1)|abundance(100)|head_armor(14)|body_armor(0)|leg_armor(0)|difficulty(2) ,imodbits_armor ],#"Stormtrooper_helm"
["imperial_stormtrooper_boots", "Imperial Stormtrooper Boots", [("Stormtrooper_legs_L",0)], itp_type_foot_armor  |itp_civilian,0, 
 210 , weight(2.0)|abundance(50)|head_armor(0)|body_armor(0)|leg_armor(16)|difficulty(0) ,imodbits_armor ], #Stormtrooper_legs_L
["imperial_stormtrooper_armor", "Imperial Stormtrooper Armor", [("Stormtrooper_body",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 
 720 , weight(10)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(18)|difficulty(0) ,imodbits_armor ],#Stormtrooper_body
["imperial_stormtrooper_gloves","Imperial Stormtrooper Gloves", [("slv_gauntlet_a_R",0),("slv_gauntlet_a_L",imodbit_reinforced)], itp_type_hand_armor|itp_civilian,0, 
 28, weight(0.25)|abundance(80)|body_armor(3)|difficulty(0),imodbits_cloth], #stormie_glov_L
#zantei ban
 ["occc_stormtrooperblaster", "Stormtrooper Blaster", [("HeavyRepeater",0),("HeavyRepeater_inv",ixmesh_inventory)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_next_item_as_melee|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 6500, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(80)|thrust_damage(60,pierce)|max_ammo(15)|accuracy(55), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_blaster_shot"),])] ],
 ["occc_stormtrooperblaster_mel", "Stormtrooper Blaster", [("HeavyRepeater",0)], itp_type_polearm|itp_unique|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback, itcf_thrust_polearm|itcf_carry_spear|itcf_overswing_polearm|itc_parry_polearm,
 6500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(90)|weapon_length(130)|swing_damage(20,blunt)|thrust_damage(15,blunt), imodbits_crossbow ],
 ["occc_novatrooperblaster", "Novatrooper Blaster", [("DC15A",0),("DC15A_inv",ixmesh_inventory)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_next_item_as_melee|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket,
 6500, weight(2.5)|abundance(90)|difficulty(0)|spd_rtng(60)|shoot_speed(80)|thrust_damage(70,pierce)|max_ammo(15)|accuracy(70), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_blaster_shot"),])] ],
 ["occc_novatrooperblaster_mel", "Novatrooper Blaster", [("DC15A",0)], itp_type_polearm|itp_unique|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback, itcf_thrust_polearm|itcf_carry_spear|itcf_overswing_polearm|itc_parry_polearm,
 6500, weight(3.0)|abundance(90)|difficulty(0)|spd_rtng(90)|weapon_length(130)|swing_damage(20,blunt)|thrust_damage(15,blunt), imodbits_crossbow ],
 ["imperial_stormtrooper_boots_novatrooper", "Novatrooper Boots", [("Novatrooper_legs_L",0)],  itp_type_foot_armor  |itp_civilian,0, 
 250 , weight(2.4)|abundance(40)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(4) ,imodbits_armor ], 
["imperial_stormtrooper_helmet_novatrooper", "Novatrooper Helmet", [("Novatrooper_helm",0)],  itp_type_head_armor|itp_covers_head|itp_civilian ,0, 
 226 , weight(2)|abundance(50)|head_armor(15)|body_armor(0)|leg_armor(0)|difficulty(3) ,imodbits_armor ],
["imperial_stormtrooper_armor_novatrooper", "Novatrooper Armor", [("Novatrooper_body",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 
 840 , weight(10)|abundance(40)|head_armor(0)|body_armor(43)|leg_armor(19)|difficulty(6) ,imodbits_armor ],
["imperial_stormtrooper_boots_novatrooper", "Novatrooper Boots", [("Novatrooper_legs_L",0)],  itp_type_foot_armor  |itp_civilian,0, 
 250 , weight(2.4)|abundance(40)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(4) ,imodbits_armor ], 
["novatrooper_gloves","Novatrooper Gloves", [("slv_gauntlet_a_R",0)], itp_type_hand_armor|itp_civilian,0, 
 38, weight(0.25)|abundance(40)|body_armor(4)|difficulty(4),imodbits_cloth],
["imperial_stormtrooper_armor_officer", "Imperial Stormtrooper Officer Armor", [("Sandtrooper_body_orangepauldron",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 
 825 , weight(12)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(22)|difficulty(0) ,imodbits_armor ], 
 
 ["occc_force_bow", "Force Shot", [("gohst",0),("gohst",ixmesh_carry),("dvader_body",ixmesh_inventory),], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 1000, weight(1.75)|difficulty(7)|spd_rtng(61)|shoot_speed(45)|thrust_damage(31,blunt), imodbits_bow ],
 ["occc_force_push", "Force Push", [("gohst",0),("dvader_helm",ixmesh_inventory),], itp_type_thrown|itp_remove_item_on_use|itp_no_pick_up_from_ground|itp_ignore_gravity|itp_ignore_friction, itcf_throw_knife, 1000, weight(1)|difficulty(0)|spd_rtng(70)|shoot_speed(50)|accuracy(100)|thrust_damage(1, cut)|max_ammo(8)|weapon_length(0), imodbits_missile, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccc_item_hit_effect", "itm_occc_force_push", ":sa"),])] ],

#######
#swadia
#######


["great_helm_goldcross", "Great Helmet", [("maciejowski_helmet_new5",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_1", "Great Helmet", [("maciejowski_helmet_new3",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_2", "Great Helmet", [("x_great_helmet_new_4",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_3", "Great Helmet", [("x_bolzanobucket",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_4", "Great Helmet", [("x_crusaderbucket1",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_5", "Great Helmet", [("x_gotlandbucket",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_6", "Great Helmet", [("x_madelnbucket2",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],

["great_helm_new_occ_colored_1", "Great Helmet", [("x_bolzanobucket2",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_colored_2", "Great Helmet", [("x_crusaderbucket2",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_colored_3", "Great Helmet", [("x_crusaderbucket3",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["great_helm_new_occ_colored_4", "Great Helmet", [("x_gotlandbucket2",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],

["occc_zendar_greathelm", "Zendar Great Helmet", [("rhodok_great_helmet",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate,[],[fac_kingdom_11] ],
["occc_hooded_great_helm_1", "Hooded Great Helmet", [("shadowhood_with_helm",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],


["great_helm_goldcross_caped", "Great Helmet and Cape", [("great_helm_with_cape1",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 1980, weight(3.75)|abundance(30)|head_armor(52)|body_armor(12)|leg_armor(0)|difficulty(10), imodbits_plate ],
#["occc_sugarloaf1", "Sugarloaf Helmet", [("talak_sugarloaf_helm",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 980, weight(2.75)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],

["occc_crusader_helm", "Crusader Helm", [("crusader_hard_helm_ord",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 760, weight(2.0)|abundance(80)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["occc_crusader_helm_colored_1", "Crusader Helm", [("crusader_knight_helm_a",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 760, weight(2.0)|abundance(80)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["occc_crusader_helm_colored_2", "Crusader Helm", [("crusader_knight_helm_b",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 760, weight(2.0)|abundance(80)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["occc_crusader_helm_colored_3", "Crusader Helm", [("crusader_knight_helm_c",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 760, weight(2.0)|abundance(80)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["occc_crusader_helm_colored_4", "Crusader Helm", [("crusader_knight_helm_d",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 760, weight(2.0)|abundance(80)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
#["occc_crusader_helm_colored_5", "Crusader Helm", [("crusader_knight_helm_e",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 760, weight(2.0)|abundance(80)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],
["occc_crusader_helm_colored_6", "Crusader Helm", [("crusader_knight_helm_f",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 760, weight(2.0)|abundance(80)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate ],

#papal
["occc_pope_cap", "Pope Cap", [("cardinal",0)], itp_type_head_armor|itp_civilian, 0, 8000, weight(1)|abundance(100)|head_armor(7)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["occc_helm_combed_morion_plumed", "Plumed Combed Morion", [("combed_morion_helvetia",0)], itp_type_head_armor|itp_attach_armature, 0, 800, weight(2)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_armor ],

#landsknecht
["occc_burgonet_lord_x", "Open Burgonet", [("burgonet_lord",0)], itp_type_head_armor    ,0,
 720 , weight(2.3)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["occc_landsknecht_hat_a_x", "Landsknecht Hat", [("beret_plumes_brown",0)], itp_type_head_armor |itp_doesnt_cover_hair|itp_merchandise   ,0,
 300 , weight(1.0)|abundance(40)|head_armor(13)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["occc_landsknecht_hat_b_x", "Landsknecht Hat", [("beret_plumes_brown2",0)], itp_type_head_armor |itp_doesnt_cover_hair|itp_merchandise   ,0,
 300 , weight(1.0)|abundance(40)|head_armor(13)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
 ["occc_landsknecht_beret_a_x", "Landsknecht Beret", [("x_beret_a",0)], itp_type_head_armor |itp_doesnt_cover_hair|itp_merchandise   ,0,
 300 , weight(0.5)|abundance(40)|head_armor(8)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["occc_landsknecht_beret_b_x", "Landsknecht Beret", [("x_beret_b",0)], itp_type_head_armor |itp_doesnt_cover_hair|itp_merchandise   ,0,
 300 , weight(0.5)|abundance(40)|head_armor(8)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],

["occc_add_kettle_hat_light_1", "Kettle Cap", [("flattop_kettle_hat_a",0)], itp_type_head_armor|itp_merchandise, 0, 170, weight(1.5)|abundance(25)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_light_2", "Kettle Cap", [("four_plated_kettle_hat_w_cap",0)], itp_type_head_armor|itp_merchandise, 0, 170, weight(1.5)|abundance(25)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_light_3", "Kettle Cap", [("rhodok_kettle_hat_a",0)], itp_type_head_armor|itp_merchandise, 0, 170, weight(1.5)|abundance(25)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_medium_1", "Kettle Hat", [("rhodok_kettle_hat_c",0)], itp_type_head_armor|itp_merchandise, 0, 250, weight(1.6)|abundance(25)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_medium_2", "Kettle Hat", [("four_plated_kettle_hat",0)], itp_type_head_armor|itp_merchandise, 0, 250, weight(1.6)|abundance(25)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_medium_3", "Kettle Hat", [("flattop_kettle_hat",0)], itp_type_head_armor|itp_merchandise, 0, 250, weight(1.6)|abundance(25)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_medium_4", "Kettle Hat", [("flattop_kettle_hat_b",0)], itp_type_head_armor|itp_merchandise, 0, 250, weight(1.6)|abundance(25)|head_armor(35)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_heavy_1", "Kettle Hat with Coif", [("rhodok_kettle_hat_d",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(1.8)|abundance(25)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_heavy_2", "Chapel_De_Fer", [("rhodok_chapel_de_fer",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(1.8)|abundance(25)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
["occc_add_kettle_hat_heavy_3", "Chapel_De_Fer", [("rhodok_chapel_de_fer_b",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(1.8)|abundance(25)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate,[],[fac_kingdom_11] ],
#
["occc_weimar_helm", "Weimar Helm", [("x_weimarhelm2",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(2.75)|abundance(30)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(15), imodbits_plate, [], [fac_kingdom_1] ],
["occc_weimar_helm_b", "Black Weimar Helm", [("x_weimarhelm2_b",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(2.75)|abundance(30)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(15), imodbits_plate, [], [fac_kingdom_1] ],

["occc_splend_armet1", "Knight Armet", [("splend_armet",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(2.75)|abundance(20)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(13), imodbits_plate, [], [fac_kingdom_1] ],
["occc_splend_armet2", "Knight Armet", [("splend_armet_ph",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(3.0)|abundance(20)|head_armor(65)|body_armor(0)|leg_armor(0)|difficulty(15), imodbits_plate, [], [fac_kingdom_1] ],
["occc_splend_armet3", "Knight Armet", [("splendorous_flemish_armet",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(3.0)|abundance(20)|head_armor(64)|body_armor(0)|leg_armor(0)|difficulty(15), imodbits_plate, [], [fac_kingdom_1] ],
["occc_x_classichelm", "Knight Helm", [("x_classichelm",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(2.75)|abundance(20)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_1] ],
["occc_x_classichelm2", "Knight Helm", [("x_classichelm2",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(2.75)|abundance(20)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_1] ],
["occc_x_classichelm_b", "Black Knight Helm", [("x_classichelm_b",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 3072, weight(2.75)|abundance(20)|head_armor(62)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_1] ],

["occc_striped_burgonet", "Striped Burgonet", [("x_burgonet_bw",0)], itp_type_head_armor, 0, 700, weight(2.75)|abundance(100)|head_armor(61)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate ],


["occc_faceover_coif", "Face Over Coif", [("facecovermail",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 100, weight(1.5)|abundance(100)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["occc_faceover_coif_banded", "Banded Face Over Coif", [("facecovermail_headband",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 120, weight(1.5)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["occc_full_coif", "Full Coif", [("fullmailcoif",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 100, weight(1.4)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],
["occc_full_coif_banded", "Banded Full Coif", [("fullmailcoif_headband",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 100, weight(1.4)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor ],

["occc_cataphract_helm", "Eastern Cataphract Helmet", [("facecovermail_plume",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 810, weight(3.50)|abundance(10)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_5] ],
["occc_eastern_kettle_hat", "Eastern Kettle Hat", [("facecovermail_kettlehat",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(1.75)|abundance(10)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_5] ],
["occc_eastern_helmet", "Eastern Infantry Helmet", [("facecovermail_helmet",0)], itp_type_head_armor|itp_merchandise, 0, 270, weight(1.75)|abundance(10)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_5] ],




["occc_new_surcoat_01", "Swadian Surcoat", [("rathos_surcoat_english",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1600, weight(22)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(16)|difficulty(7), imodbits_armor,[],[fac_kingdom_1] ],
["occc_new_surcoat_02", "Mail with Surcoat", [("rathos_surcoat_halfblue",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1544, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(14)|difficulty(7), imodbits_armor,[],[fac_kingdom_1] ],
["occc_new_surcoat_03", "Mail with Surcoat", [("rathos_surcoat_halfred",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1544, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(14)|difficulty(7), imodbits_armor,[],[fac_kingdom_1] ],
["occc_new_surcoat_04", "Mail with Surcoat", [("rathos_surcoat_redyellow",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1544, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(14)|difficulty(7), imodbits_armor,[],[fac_kingdom_1] ],
["occc_new_surcoat_05", "Mail with Surcoat", [("rathos_surcoat_white",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1544, weight(22)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(14)|difficulty(7), imodbits_armor,[],[fac_kingdom_1] ],

["occc_plate_ken_gothic_4", "Elaborate Plate Armor", [("gothic_plate_y2b",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 9496, weight(30)|abundance(20)|head_armor(0)|body_armor(60)|leg_armor(17)|difficulty(9), imodbits_plate ],
["occc_bnw_armour_stripes_r", "Landsknecht Armor", [("x_bnw_armour_stripes_r",0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise ,0,
 1800 , weight(15)|abundance(30)|head_armor(0)|body_armor(46)|leg_armor(10)|difficulty(7) ,imodbits_armor , [], [fac_kingdom_1]],
["occc_bnw_armour_stripes_r2", "Landsknecht Armor", [("x_bnw_armour_stripes_r2",0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise ,0,
 1800 , weight(15)|abundance(30)|head_armor(0)|body_armor(46)|leg_armor(10)|difficulty(7) ,imodbits_armor , [], [fac_kingdom_1]],
["occc_bnw_armour_stripes_d", "Landsknecht Armor", [("x_bnw_armour_stripes_D",0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise ,0,
 2100 , weight(18)|abundance(30)|head_armor(0)|body_armor(51)|leg_armor(12)|difficulty(9) ,imodbits_plate , [], [fac_kingdom_1]],
["occc_bnw_armour_stripes_ro", "Landsknecht Armor", [("x_bnw_armour_stripes_RO",0)],  itp_type_body_armor  |itp_covers_legs|itp_merchandise ,0,
 2100 , weight(18)|abundance(30)|head_armor(0)|body_armor(51)|leg_armor(12)|difficulty(9) ,imodbits_plate , [], [fac_kingdom_1]],


["occc_additional_plate1", "Plate Armor", [("full_plate",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 9496, weight(33)|abundance(40)|head_armor(0)|body_armor(62)|leg_armor(25)|difficulty(16), imodbits_plate, [], [fac_kingdom_1] ],
["occc_additional_plate2", "Plate Armor", [("full_plate_2",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 9496, weight(33)|abundance(40)|head_armor(0)|body_armor(62)|leg_armor(25)|difficulty(16), imodbits_plate, [], [fac_kingdom_1] ],


["occc_landsknect_shoes_d", "Landsknecht Shoes", [("x_bear_paw_shoes_black",0)], itp_type_foot_armor|itp_attach_armature|itp_civilian|itp_merchandise, 0, 100, weight(1)|abundance(30)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ],
["occc_landsknect_shoes_ro", "Landsknecht Shoes", [("x_bear_paw_shoes",0)], itp_type_foot_armor|itp_attach_armature|itp_civilian|itp_merchandise, 0, 100, weight(1)|abundance(30)|head_armor(0)|body_armor(0)|leg_armor(7)|difficulty(0), imodbits_cloth ],


["occc_flamberge_x",  "Zweihander", [("flamberge",0)], itp_type_two_handed_wpn|itp_merchandise|itp_two_handed|itp_cant_use_on_horseback|itp_primary, itc_staff|itcf_horseback_thrust_onehanded|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_sword_back,
 3000 , weight(4)|abundance(30)|difficulty(8)|spd_rtng(92) | weapon_length(170)|swing_damage(50 , cut) | thrust_damage(38 ,  pierce),imodbits_polearm , []],
["occc_flamberge", "Flamberge Zweihander", [("zweihanderc",0)], itp_type_two_handed_wpn|itp_two_handed|itp_merchandise|itp_primary, itc_greatsword|itcf_carry_sword_back,
 4000 , weight(3.5)|abundance(10)|difficulty(12)|spd_rtng(92) | weapon_length(150)|swing_damage(52 , cut) | thrust_damage(32 ,  pierce),imodbits_sword_high , []], ##### ADD MP

["occc_sword_of_war_x", "Sword of War", [("grandeepeed",0)], itp_merchandise|itp_type_two_handed_wpn| itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back,
 2500 , weight(3)|abundance(30)|difficulty(11)|spd_rtng(94) | weapon_length(135)|swing_damage(48 , cut) | thrust_damage(37 ,  pierce),imodbits_sword_high ],

["occc_bastard_sword_1", "Noble Bastard Sword", [("mackie_bastard",0)], itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_sword_back,
 2500 , weight(2.7)|abundance(30)|difficulty(13)|spd_rtng(92) | weapon_length(127)|swing_damage(47 , cut) | thrust_damage(36 ,  pierce),imodbits_sword_high , [], [fac_kingdom_1,fac_kingdom_11]],
["occc_bastard_sword_2", "Dark Bastard Sword", [("s_sword",0),("s_sword_scab",ixmesh_carry)], itp_type_two_handed_wpn|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 720, weight(2.25)|difficulty(11)|spd_rtng(91)|weapon_length(113)|swing_damage(40,cut)|thrust_damage(30,pierce), imodbits_sword_high ],

["occc_kriegsmesser", "Kriegsmesser", [("mackie_kriegsmesser",0)], itp_merchandise|itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_sword_back,
 980 , weight(2.5)|abundance(30)|difficulty(9)|spd_rtng(98) | weapon_length(113)|swing_damage(41 , cut) | thrust_damage(32 ,  pierce),imodbits_sword_high ],

 
["occc_military_hammer_talak", "Noble Military Hammer", [("talak_warhammer",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 450, weight(2)|difficulty(0)|spd_rtng(97)|weapon_length(68)|swing_damage(34,blunt)|thrust_damage(0,pierce), imodbits_mace ],

["occc_morningstar_mackie_long", "Great Morningstar", [("mackie_morning_star_long",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_primary|itp_crush_through|itp_unbalanced|itp_two_handed|itp_cant_use_on_horseback, itc_morningstar|itcf_carry_sword_back, 1800, weight(5)|difficulty(18)|spd_rtng(83)|weapon_length(135)|swing_damage(49,pierce)|thrust_damage(0,pierce), imodbits_mace ],
["occc_morningstar_mackie", "Short Morningstar", [("mackie_morning_star",0)], itp_type_one_handed_wpn|itp_merchandise|itp_wooden_parry|itp_primary|itp_can_knock_down, itc_scimitar|itcf_carry_mace_left_hip, 370, weight(4.0)|difficulty(0)|spd_rtng(100)|weapon_length(60)|swing_damage(29,pierce)|thrust_damage(0,pierce), imodbits_pick ],

["occc_knechten_hallberd_1", "Landsknecht Halberd", [("hallberdc",0)], itp_type_polearm|itp_wooden_parry|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_offset_lance|itp_cant_use_on_horseback|itp_merchandise, itc_cutting_spear|itcf_slashright_polearm|itcf_slashleft_polearm, 1200, weight(4.0)|difficulty(15)|spd_rtng(78)|weapon_length(240)|swing_damage(48,cut)|thrust_damage(27,pierce), imodbits_polearm ],
["occc_knechten_hallberd_2", "Landsknecht Halberd", [("hallberde",0)], itp_type_polearm|itp_wooden_parry|itp_two_handed|itp_primary|itp_can_penetrate_shield|itp_offset_lance|itp_cant_use_on_horseback|itp_merchandise, itc_cutting_spear|itcf_slashright_polearm|itcf_slashleft_polearm, 1200, weight(4.0)|difficulty(15)|spd_rtng(78)|weapon_length(240)|swing_damage(48,cut)|thrust_damage(27,pierce), imodbits_polearm ],



# FromPerisno Begin
["sunsword", "Weird Knight Blade", [("SwordOfDarkness",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_sword_back, 15000, weight(3.3)|difficulty(15)|spd_rtng(110)|weapon_length(136)|swing_damage(55,cut)|thrust_damage(42,pierce), imodbits_sword_high ],
["sunswordcopy", "Sun Sword Imitate", [("SwordOfDarkness",0)], itp_type_two_handed_wpn|itp_primary, itc_bastardsword|itcf_carry_sword_back, 2000, weight(3.3)|difficulty(15)|spd_rtng(103)|weapon_length(132)|swing_damage(50,cut)|thrust_damage(28,pierce), imodbits_sword_high|imodbit_rusty|imodbit_tempered|imodbit_masterwork ],
#From Perisno End

["occc_katzbalger", "Katzbalger", [("talak_katzbalger",0),("talak_scab_katzbalger",ixmesh_carry)], itp_type_one_handed_wpn|itp_merchandise|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 200, weight(1)|difficulty(0)|spd_rtng(108)|weapon_length(82)|swing_damage(34,cut)|thrust_damage(28,pierce), imodbits_sword_high ],
["occc_sword_baron", "Baron Sword", [("baron",0),("baron_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
  700, weight(1.5)|difficulty(11)|spd_rtng(93)|weapon_length(109)|swing_damage(36,cut)|thrust_damage(28,pierce), imodbits_sword ],  ## cave09 templar_sword->sword008


["horned_great_helmet", "Horned Great Helmet", [("maciejowski_helmet5b",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 7070, weight(3.6)|abundance(7)|head_armor(60)|body_armor(0)|leg_armor(0)|difficulty(19), imodbits_plate|imodbit_cracked|imodbit_rusty|imodbit_battered|imodbit_crude|imodbit_thick|imodbit_reinforced|imodbit_lordly,[], [fac_kingdom_1] ],

["occc_horned_great_helmet_1", "Horned Great Helmet", [("maciejowski_helmet_new4",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 5070, weight(3.6)|abundance(10)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(14), imodbits_plate|imodbit_cracked|imodbit_rusty|imodbit_battered|imodbit_crude|imodbit_thick|imodbit_reinforced|imodbit_lordly,[], [fac_kingdom_1] ],
["occc_horned_great_helmet_2", "Horned Great Helmet", [("maciejowski_helmet5b_black",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 5070, weight(3.6)|abundance(10)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(14), imodbits_plate|imodbit_cracked|imodbit_rusty|imodbit_battered|imodbit_crude|imodbit_thick|imodbit_reinforced|imodbit_lordly,[], [fac_kingdom_1] ],
["occc_horned_great_helmet_3", "Horned Great Helmet", [("maciejowski_helmet5b_bronze",0)], itp_type_head_armor|itp_merchandise|itp_covers_head|itp_covers_beard, 0, 5070, weight(3.6)|abundance(10)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(14), imodbits_plate|imodbit_cracked|imodbit_rusty|imodbit_battered|imodbit_crude|imodbit_thick|imodbit_reinforced|imodbit_lordly,[], [fac_kingdom_1] ],

## ADD CounterPoint391's Start
["tabard_hospitaller", "Tabard of Hospitaller", [("tabard_hospitaller",0)], itp_merchandise|itp_type_body_armor| itp_covers_legs |itp_civilian,0,
 380 , weight(3)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(8)|difficulty(0) ,imodbits_cloth , [], [fac_kingdom_1,fac_kingdom_5]],
["padded_leather_hospitaller", "Padded Leather of Hospitaller", [("padded_cloth_hospitaller",0)], itp_merchandise|itp_type_body_armor| itp_covers_legs|itp_civilian,0,
 800 , weight(12)|abundance(100)|head_armor(0)|body_armor(36)|leg_armor(12)|difficulty(0) ,imodbits_cloth , [], [fac_kingdom_1,fac_kingdom_5]],
["mail_with_surcoat_hospitaller", "Mail with Surcoat of Hospitaller", [("mail_long_surcoat_hospitaller",0)], itp_merchandise|itp_type_body_armor| itp_civilian  |itp_covers_legs ,0,
 1800 , weight(20)|abundance(50)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(8) ,imodbits_armor , [], [fac_kingdom_1,fac_kingdom_5]],
["surcoat_over_mail_hospitaller", "Surcoat over Mail of Hospitaller", [("surcoat_over_mail_hospitaller",0)], itp_merchandise|itp_type_body_armor| itp_civilian  |itp_covers_legs ,0,
 2200 , weight(21)|abundance(50)|head_armor(0)|body_armor(46)|leg_armor(15)|difficulty(9) ,imodbits_armor , [], [fac_kingdom_1,fac_kingdom_5]],
## ADD CounterPoint391's End


["teutonic_gambeson1", "Teutonic Gambeson", [("armor_15",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 260, weight(5)|abundance(30)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["teutonic_gambeson2", "Teutonic Gambeson", [("armor_16",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 260, weight(5)|abundance(30)|head_armor(0)|body_armor(20)|leg_armor(5)|difficulty(0), imodbits_cloth ],

["teutonicmail_cape1", "Teutonic Mail with Cape", [("armor_11",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 860, weight(14)|abundance(15)|head_armor(2)|body_armor(42)|leg_armor(5)|difficulty(9), imodbits_armor,],
["teutonicmail_cape2", "Teutonic Mail with Cape", [("armor_12",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 860, weight(14)|abundance(15)|head_armor(2)|body_armor(42)|leg_armor(5)|difficulty(9), imodbits_armor,],

["teutonicsurcoatmail_halb1", "Teutonic Halbbruder Mail", [("armor_14",0)], itp_type_body_armor|itp_covers_legs, 0, 860, weight(14)|abundance(30)|head_armor(0)|body_armor(42)|leg_armor(8)|difficulty(9), imodbits_armor,],
["teutonicsurcoatmail_halb2", "Teutonic Halbbruder Mail", [("armor_13",0)], itp_type_body_armor|itp_covers_legs, 0, 860, weight(14)|abundance(30)|head_armor(0)|body_armor(42)|leg_armor(8)|difficulty(9), imodbits_armor,],

["teutonicsurcoatmail_withoutcape", "Teutonic Mail with Surcoat", [("knight_armor_tevton_c",0)], itp_type_body_armor|itp_covers_legs, 0, 6400, weight(14)|abundance(30)|head_armor(0)|body_armor(44)|leg_armor(10)|difficulty(9), imodbits_armor,],
["teutonicsurcoatmail", "Caped Teutonic Mail with Surcoat", [("knight_armor_tevton_c_cloak",0)], itp_type_body_armor|itp_covers_legs, 0, 11960, weight(16)|abundance(10)|head_armor(0)|body_armor(54)|leg_armor(24)|difficulty(18), imodbits_armor,[], [fac_kingdom_1]],

#teutonic
["teutonichelm_x1", "Teutonic Helm", [("x_helmet_21",0)], itp_type_head_armor|itp_covers_head   ,0,
 5400 , weight(2.75)|abundance(50)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["teutonichelm_x2", "Teutonic Helm", [("x_maciejowski_helmet_new_bnw",0)], itp_type_head_armor|itp_covers_head   ,0,
 5400 , weight(2.75)|abundance(50)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["teutonichelm_x3", "Teutonic Helm", [("x_teutonichelm",0)], itp_type_head_armor|itp_covers_head   ,0,
 5400 , weight(2.75)|abundance(50)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["caped_teutonic_helm1", "Teutonic Helm and Cape", [("x_maciejowski_helmet_new_bnw_caped",0)], itp_type_head_armor|itp_covers_head   ,0,
 7000 , weight(4.75)|abundance(50)|head_armor(55)|body_armor(12)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["crusader_greathelm1", "Crusader Great Helm", [("greathelm1_crusader",0)], itp_type_head_armor|itp_covers_head|itp_merchandise   ,0,
 2500 , weight(2.75)|abundance(50)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["crusader_greathelm2", "Crusader Great Helm", [("greathelmwhat",0)], itp_type_head_armor|itp_covers_head   ,0,
 4000 , weight(2.75)|abundance(50)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],

["shield_teutonic_halb1", "Heater Shield", [("shield_2",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
 480 , weight(3.25)|abundance(20)|hit_points(280)|body_armor(18)|spd_rtng(96)|shield_width(31)|shield_height(52),imodbits_shield ],
["shield_teutonic_halb2", "Heater Shield", [("shield_3",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
 480 , weight(3.25)|abundance(20)|hit_points(280)|body_armor(18)|spd_rtng(96)|shield_width(31)|shield_height(52),imodbits_shield ],
["shield_teutonic_halb3", "Heater Shield", [("shield_4",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
 480 , weight(3.25)|abundance(20)|hit_points(280)|body_armor(18)|spd_rtng(96)|shield_width(31)|shield_height(52),imodbits_shield ],
["shield_teutonic_halb4", "Heater Shield", [("shield_5",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
 480 , weight(3.25)|abundance(20)|hit_points(280)|body_armor(18)|spd_rtng(96)|shield_width(31)|shield_height(52),imodbits_shield ],
["shield_teutonic_halb5", "Heater Shield", [("shield_6",0)], itp_type_shield|itp_wooden_parry|itp_merchandise, itcf_carry_kite_shield, 
 480 , weight(3.25)|abundance(20)|hit_points(280)|body_armor(18)|spd_rtng(96)|shield_width(31)|shield_height(52),imodbits_shield ],

["shield_teutonic_x1", "Heater Shield", [("shield_10",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
 600 , weight(3.25)|abundance(50)|hit_points(320)|body_armor(18)|spd_rtng(96)|shield_width(31)|shield_height(52),imodbits_shield ],
["shield_teutonic_x2", "Heater Shield", [("shield_7",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield, 
 660 , weight(3.25)|abundance(50)|hit_points(350)|body_armor(18)|spd_rtng(96)|shield_width(31)|shield_height(52),imodbits_shield ],

["occc_helm_sp_pigface_1", "Feathered Bascinet", [("sprend_pigface",0)], itp_type_head_armor|itp_covers_head,0, 1180 , weight(3)|abundance(100)|head_armor(59)|body_armor(0)|leg_armor(0)|difficulty(9) ,imodbits_plate ],
["occc_helm_sp_pigface_2", "Feathered Bascinet", [("sprend_pigface2",0)], itp_type_head_armor|itp_covers_head,0, 1180 , weight(3)|abundance(100)|head_armor(59)|body_armor(0)|leg_armor(0)|difficulty(13) ,imodbits_plate ],
["occc_helm_sp_pigface_open", "Hochmeister's Open Bascinet", [("sprend_pigface_open",0)], itp_type_head_armor,0, 20000 , weight(3)|abundance(100)|head_armor(63)|body_armor(0)|leg_armor(0)|difficulty(15) ,imodbits_plate ],

["occc_dejawolf_greatbascinet_a", "Great Bascinet", [("x_dejawolf_greatbascinet_a",0)], itp_type_head_armor|itp_covers_head|itp_merchandise   ,0,
 1400 , weight(2.75)|abundance(30)|head_armor(59)|body_armor(0)|leg_armor(0)|difficulty(12) ,imodbits_plate ],
["occc_dejawolf_greatbascinet_a_b", "Black Great Bascinet", [("x_dejawolf_greatbascinet_a_b",0)], itp_type_head_armor|itp_covers_head|itp_merchandise   ,0,
 1400 , weight(2.75)|abundance(30)|head_armor(59)|body_armor(0)|leg_armor(0)|difficulty(12) ,imodbits_plate ],
["occc_dejawolf_milanese_sallet", "Milanese Sallet", [("x_dejawolf_milanese_sallet",0)],itp_type_head_armor|itp_covers_head   ,0,
 1400 , weight(2.75)|abundance(50)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(12) ,imodbits_plate ],
["occc_dejawolf_barbuta_a", "Barbuta", [("x_dejawolf_barbuta_a",0)], itp_type_head_armor|itp_merchandise   ,0,
 800 , weight(2.2)|abundance(50)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["occc_dejawolf_barbuta_b", "Barbuta", [("x_dejawolf_barbuta_b",0)], itp_type_head_armor|itp_merchandise   ,0,
 800 , weight(2.2)|abundance(50)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],

 
########
#vaegir
########
["occc_emperor_bicorne", "Hero's Bicorne",[("french_hat_boney",0)], itp_type_head_armor|itp_doesnt_cover_hair, 0, 80000, weight(1)|abundance(0)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["occc_michelle_bicorne", "Michelle's Bicorne",[("mich_fr_rev_bicorn",0)], itp_type_head_armor, 0, 1000, weight(1)|abundance(0)|head_armor(30)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["occc_french_bicorne", "Revolutional Bicorne",[("fr_rev_bicorn",0)], itp_type_head_armor, 0, 30, weight(1)|abundance(0)|head_armor(8)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["occc_hat_musketeer_hat01", "Outlaw Hat", [("musketeer_hat01",0)], itp_type_head_armor|itp_merchandise, 0, 34, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],
["occc_hat_musketeer_hat02", "Outlaw Hat", [("musketeer_hat02",0)], itp_type_head_armor|itp_merchandise, 0, 34, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],
["occc_shako_french", "Shako Hat", [("french_shako_line",0)], itp_type_head_armor|itp_merchandise, 0, 40, weight(1)|abundance(75)|head_armor(20)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth,[], [fac_kingdom_3] ],

["occc_napoleon_coat", "Hero's Coat", [("french_coat_napoleon",0)], itp_type_body_armor|itp_covers_legs, 0, 80000, weight(6)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["occc_cuirassier_french", "French Cuirass", [("french_cuirassier",0)], itp_type_body_armor|itp_covers_legs, 0, 1536, weight(14)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(14)|difficulty(0), imodbits_cloth ],

["occc_line_captain_uniform", "Captain Uniform", [("french_coat_linecaptain",0)], itp_type_body_armor|itp_covers_legs, 0, 400, weight(6)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["occc_old_guards_uniform", "Old Guards Uniform", [("frenchcoat",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(6)|abundance(100)|head_armor(0)|body_armor(26)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["occc_artillery_officer_uniform", "Artillery Uniform", [("french_coat_artilleryofficer",0)], itp_type_body_armor|itp_covers_legs, 0, 550, weight(6)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["occc_musician_uniform", "Musician Uniform", [("french_coat_musician",0)], itp_type_body_armor|itp_covers_legs, 0, 350, weight(6)|abundance(100)|head_armor(0)|body_armor(18)|leg_armor(8)|difficulty(0), imodbits_cloth ],
["occc_grande_armee_uniform", "Grande Armee Uniform", [("french_coat_light",0)], itp_type_body_armor|itp_covers_legs, 0, 150, weight(6)|abundance(100)|head_armor(0)|body_armor(14)|leg_armor(8)|difficulty(0), imodbits_cloth ],

#["occc_revolutional_troop_uniform", "Revolutional Troop Uniform", [("fr_rev_uniform",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(6)|abundance(100)|head_armor(0)|body_armor(38)|leg_armor(12)|difficulty(0), imodbits_cloth ],

["occc_musician_gloves", "Musician Gloves", [("gloves_drummer_R",0)], itp_type_hand_armor, 0, 90, weight(0.25)|abundance(120)|body_armor(2)|difficulty(0), imodbits_cloth ],

["occc_napoleon_boots", "Old Guards Boots", [("french_boots_lineofficer",0)], itp_type_foot_armor|itp_civilian, 0, 150, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0), imodbits_cloth ],
["occc_french_gaiters", "French Line Boots", [("french_gaiters",0)], itp_type_foot_armor|itp_civilian, 0, 91, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0), imodbits_cloth ],
["occc_french_boots", "Grande Armee Boots", [("french_boots_lightofficer",0)], itp_type_foot_armor|itp_civilian, 0, 91, weight(1.25)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0), imodbits_cloth ],

["occc_old_guard_sabre", "Old Guards Sabre", [("lui_dussack",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 1000, weight(1.75)|difficulty(0)|spd_rtng(115)|weapon_length(98)|swing_damage(41,cut)|thrust_damage(0,pierce)|body_armor(4), imodbits_sword_high ],
#
["occc_handgun_cartridges", "Handgun Cartridges", [("ccd_ammo_box_a",0),("bullet",ixmesh_flying_ammo),("cartridge_a",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_merchandise, 0, 20, weight(1.25)|abundance(80)|weapon_length(3)|thrust_damage(1,pierce)|max_ammo(60), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],
["occc_gatling_cartridges", "Gatling Catridge", [("ccd_ammo_box_a",0),("bullet",ixmesh_flying_ammo),("cartridge_a",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield, 0, 100000, weight(125.25)|abundance(0)|weapon_length(3)|thrust_damage(5,pierce)|max_ammo(150), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + missile_distance_trigger ],

["occc_gatling_gun", "Proto Type Gatling Gun", [("rifle_8barrel",0)], itp_type_musket|itp_two_handed|itp_primary|itp_crush_through, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 100000, weight(80)|abundance(0)|difficulty(0)|spd_rtng(180)|shoot_speed(95)|thrust_damage(90,pierce)|max_ammo(150)|accuracy(0), imodbits_none, [(ti_on_weapon_attack,[(play_sound,"snd_merc_cav_musket_shot"),(call_script, "script_ccd_gun_particle", 1),])] ],
["occc_artillery_operation", "Artillery Operation", [("gohst",0),("leather_gloves_L",ixmesh_inventory),], itp_type_thrown|itp_remove_item_on_use|itp_no_pick_up_from_ground|itp_ignore_friction, itcf_throw_knife, 8000, weight(1)|difficulty(0)|spd_rtng(56)|shoot_speed(230)|accuracy(100)|thrust_damage(1, cut)|max_ammo(1)|weapon_length(0), imodbits_missile, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccc_item_hit_effect", "itm_occc_artillery_operation", ":sa"),])] ],
["occc_artillery_projectile", "Explosive_Shell", [("gohst",0),("ccd_grenade",ixmesh_inventory)], itp_type_thrown|itp_primary|itp_no_pick_up_from_ground, itcf_throw_stone, 256, weight(2)|difficulty(0)|spd_rtng(95)|shoot_speed(50)|thrust_damage(200,pierce)|max_ammo(1)|weapon_length(6), imodbits_none, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccd_item_hit_effect_explosion_missile", "itm_occc_artillery_projectile", ":sa"),])] + missile_distance_trigger ],

["occc_rus_kettle_hat", "Russian Kettle Hat", [("western_rus_kettle_hat",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(1.75)|abundance(10)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_12] ],
["occc_rus_inf_helm_1", "Russian Infantry Helmet", [("rus_helmet_c_coif",0)], itp_type_head_armor|itp_merchandise, 0, 320, weight(1.75)|abundance(10)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_12] ],
["occc_rus_inf_helm_2", "Russian Infantry Helmet", [("rus_helmet_c_brass",0)], itp_type_head_armor|itp_merchandise, 0, 320, weight(1.75)|abundance(10)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_12] ],

["occc_rus_cav_helm_1", "Russian Cavalry Helmet", [("east_cav_helmet",0)], itp_type_head_armor|itp_merchandise, 0, 360, weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_12] ],
["occc_rus_cav_helm_2", "Russian Cavalry Helmet", [("rus_plain_helmet",0)], itp_type_head_armor|itp_merchandise, 0, 360, weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_12] ],
["occc_rus_cav_helm_3", "Russian Cavalry Helmet", [("rus_plain_helmet_b",0)], itp_type_head_armor|itp_merchandise, 0, 360, weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_12] ],

["occc_vaeg_warmask1", "Vaegir Elite War Mask", [("vaeg_helmet9_additional",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 1000, weight(3.50)|abundance(100)|head_armor(53)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_12] ],


########
#samurai
########
["occc_kamikazekabuto", "KAMIKAZE KABUTO", [("kabuto_inv",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 2200, weight(2)|abundance(200)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["occc_kamikazeyoroi", "KAMIKAZE YOROI", [("yoroi",0)], itp_type_body_armor|itp_merchandise, 0, 11960, weight(18)|abundance(200)|head_armor(0)|body_armor(52)|leg_armor(24)|difficulty(18), imodbits_armor, [],[fac_kingdom_9,fac_bushido_order]],
["occc_kamikazekote","KAMIKAZE KOTE", [("kote_L",0)], itp_merchandise|itp_type_hand_armor,0, 3300, weight(0.25)|abundance(200)|body_armor(5)|difficulty(0),imodbits_armor , [],[fac_kingdom_9,fac_bushido_order]],
["occc_kamikazegusoku", "KAMIKAZE GUSOKU", [("suneate",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 700, weight(1)|abundance(200)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0), imodbits_cloth, [],[fac_kingdom_9,fac_bushido_order]  ],
["occc_kamikazekabuto_r", "RED KAMIKAZE KABUTO", [("copy_kabuto_inv",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 2200, weight(2)|abundance(200)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [],[fac_kingdom_9,fac_bushido_order]  ],
["occc_kamikazeyoroi_r", "RED KAMIKAZE YOROI", [("copy_yoroi",0)], itp_type_body_armor|itp_merchandise, 0, 11960, weight(18)|abundance(200)|head_armor(0)|body_armor(52)|leg_armor(24)|difficulty(18), imodbits_armor, [],[fac_kingdom_9,fac_bushido_order] ],
["occc_kamikazekote_r","RED KAMIKAZE KOTE", [("copy_kote_L",0)], itp_merchandise|itp_type_hand_armor,0, 3300, weight(0.25)|abundance(200)|abundance(9)|body_armor(5)|difficulty(0),imodbits_armor, [],[fac_kingdom_9,fac_bushido_order]],
["occc_kamikazegusoku_r", "RED KAMIKAZE GUSOKU", [("copy_suneate",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 700, weight(1)|abundance(200)|head_armor(0)|body_armor(0)|leg_armor(30)|difficulty(0), imodbits_cloth, [], [fac_kingdom_9,fac_bushido_order]  ],


["occc_kenseikabuto", "Kensei's Kabuto", [("kensei_kabuto",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 4000, weight(2)|abundance(80)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["occc_kamakura_kabuto_1", "Kamakura Kabuto", [("samurai_kamakura_helm_a",0)], itp_type_head_armor|itp_merchandise, 0, 600, weight(2)|abundance(150)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["occc_kamakura_kabuto_2", "Kamakura Kabuto", [("samurai_kamakura_helm_b",0)], itp_type_head_armor|itp_merchandise, 0, 600, weight(2)|abundance(150)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["occc_kamakura_kabuto_3", "Kamakura Kabuto", [("samurai_kamakura_helm_c",0)], itp_type_head_armor|itp_merchandise, 0, 600, weight(2)|abundance(150)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],

#anti-arrow armors begin
["occc_doumaru_horo_w", "Doumaru with Horo", [("dou_doumaru_horo_shiro",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(20)|abundance(80)|head_armor(0)|body_armor(53)|leg_armor(16)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],
["occc_doumaru_horo_y", "Doumaru with Horo", [("copy_dou_doumaru_horo_shiro",0)], itp_type_body_armor|itp_covers_legs, 0, 1500, weight(20)|abundance(20)|head_armor(0)|body_armor(54)|leg_armor(16)|difficulty(7), imodbits_armor, [], [fac_kingdom_9,fac_bushido_order] ],

#anti-arrow armors end
#imported from kanto doran!
["occc_dou_takeda_nagae", "Nagae Yari", [("dou_takeda_nagae",0)], 
 itp_merchandise| itp_type_polearm| itp_wooden_parry| itp_two_handed| itp_primary| itp_penalty_with_shield| itp_cant_use_on_horseback, 
 itc_cutting_spear| itcf_carry_spear, 2000, weight(4.9)
 | abundance(150)| difficulty(11)| spd_rtng(67)| weapon_length(500)| swing_damage(44, blunt)| thrust_damage(23, pierce), 
 imodbit_bent |imodbit_rusty | imodbit_chipped | imodbit_balanced |imodbit_tempered| imodbit_masterwork
 , [], [fac_kingdom_9,fac_bushido_order ]
],


#["occc_bow_jp_wa_bow_improved", "Kitunetuki Bow", [("heavy_yumi",0),], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 2048, weight(1.75)|difficulty(9)|spd_rtng(40)|shoot_speed(66)|thrust_damage(43,pierce), imodbits_bow ],

#####
#Nord
#####
["viking_byrnie", "Huscarl Caped Mail", [("dejawolf_vikingbyrnie",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 6140, weight(20)|abundance(35)|head_armor(0)|body_armor(52)|leg_armor(24)|difficulty(10), imodbits_armor ,[], [fac_kingdom_4]],
["viking_byrnie_2", "Huscarl Caped Mail", [("dejawolf_vikingbyrnie_blue",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 8400, weight(22)|abundance(35)|head_armor(0)|body_armor(54)|leg_armor(22)|difficulty(12), imodbits_armor ,[], [fac_kingdom_4]],
["occc_einherjar_armor", "Einherjar Armor", [("x_banded_armor_heavy2",0)],  itp_type_body_armor  |itp_covers_legs ,0,
 9200 , weight(28)|abundance(2)|head_armor(0)|body_armor(58)|leg_armor(20)|difficulty(12) ,imodbits_plate , [], [fac_kingdom_4]],
["occc_joms_viking_hersir_armor", "Hersir's Armor", [("copy_ssh_huscarl_armour",0)], itp_type_body_armor|itp_covers_legs, 0, 9500, weight(31)|abundance(5)|head_armor(0)|body_armor(61)|leg_armor(20)|difficulty(15), imodbits_plate ],

["occc_nordic_light_armor", "Nordic Light Armor", [("nordiclightarmor12",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 532, weight(10)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_armor, [], [fac_kingdom_4] ],
["occc_nordic_banded_armor", "Banded Armor", [("banded_armor3",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2710, weight(23)|abundance(100)|head_armor(0)|body_armor(46)|leg_armor(14)|difficulty(8), imodbits_armor, [], [fac_kingdom_4] ],
["occc_nordic_heavy_banded_armor", "Banded Heavy Armor", [("banded_armor_heavy1",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 5500, weight(28)|abundance(100)|head_armor(0)|body_armor(54)|leg_armor(14)|difficulty(8), imodbits_plate, [], [fac_kingdom_4] ],
["occc_barbarian_armor1", "Barbarian Armor", [("barbar_body",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(1)|abundance(50)|head_armor(0)|body_armor(8)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["occc_barbarian_armor2", "Barbarian Armor", [("barbar_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 24, weight(2)|abundance(50)|head_armor(0)|body_armor(23)|leg_armor(5)|difficulty(0), imodbits_cloth ],
["occc_nordic_rawhide_coat", "Nordic Rawhide Coat", [("coat_of_plates1",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 12, weight(5)|abundance(100)|head_armor(0)|body_armor(10)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_4] ],

["occc_nordic_chieftain_mail", "Nordic Huscarl Mail", [("x_huscarl_mail",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1500, weight(19)|abundance(30)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(0), imodbits_armor, [], [fac_kingdom_4] ],
["occc_mail_hauberk_caped", "Caped Mail Hauberk", [("hauberk_a_new_cape",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1360, weight(19)|abundance(100)|head_armor(0)|body_armor(42)|leg_armor(13)|difficulty(7), imodbits_armor ],
["occc_mail_shirt_caped", "Caped Mail Shirt", [("mail_shirt_a_caped",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 1070, weight(19)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(12)|difficulty(7), imodbits_armor ],
["occc_nordic_light_mail1", "Nordic Light Mail", [("mail_coat_c",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1000, weight(12.5)|abundance(40)|head_armor(0)|body_armor(37)|leg_armor(10)|difficulty(0), imodbits_armor, [], [fac_kingdom_4] ],
["occc_nordic_light_mail2", "Nordic Light Mail", [("mail_coat_b",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1000, weight(12.5)|abundance(40)|head_armor(0)|body_armor(37)|leg_armor(10)|difficulty(0), imodbits_armor, [], [fac_kingdom_4] ],
["occc_nordic_light_mail3", "Nordic Light Mail", [("kuwras",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1000, weight(12.5)|abundance(40)|head_armor(0)|body_armor(37)|leg_armor(10)|difficulty(0), imodbits_armor, [], [fac_kingdom_4] ],
["occc_nordic_raider_mail", "Nordic Raider Mail", [("kuwra",0)], itp_type_body_armor|itp_covers_legs, 0, 1400, weight(40)|abundance(14)|head_armor(0)|body_armor(44)|leg_armor(10)|difficulty(0), imodbits_armor, [], [fac_kingdom_4] ],
["occc_nordic_fenrir_mail", "Fenrir Brigandine", [("bers_armor",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1800, weight(16)|abundance(4)|head_armor(0)|body_armor(48)|leg_armor(11)|difficulty(0), imodbits_plate, [], [fac_kingdom_4] ],
["occc_viking_konungr_armor", "Konungr's Armor", [("ssh_huscarl_armour",0)], itp_type_body_armor|itp_covers_legs, 0, 3064, weight(28)|abundance(100)|head_armor(0)|body_armor(61)|leg_armor(15)|difficulty(12), imodbits_plate ],

#
["occc_goat_cap", "Goat Cap", [("goat_cap", 0),], itp_type_head_armor, 0, 15, weight(1)|abundance(160)|head_armor(8), imodbits_cloth ],#occc 

["occc_helm_spangenhelm", "Spangen Helm", [("talak_spangenhelm",0)], itp_type_head_armor|itp_merchandise, 0, 360, weight(2)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_armor, [], [fac_kingdom_14] ],
["occc_helm_spangenhelm_goat", "Goat Spangen Helm", [("talak_spangenhelm_goat",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(3)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_armor, [], [fac_kingdom_14] ],
["occc_helm_sutton_hoo", "Sutton Hoo", [("talak_sutton_hoo",0)], itp_type_head_armor, 0, 600, weight(2)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_armor ],

["occc_pointedhelmet_x", "Pointed Helmet", [("pointedhelmet",0)], itp_type_head_armor|itp_merchandise   ,0,
 300 , weight(2.0)|abundance(100)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(5) ,imodbits_plate ],
["occc_normanhelmet_x", "Norman Helmet", [("x_normanhelmet",0)], itp_type_head_armor|itp_merchandise   ,0,
 340 , weight(2.0)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(5) ,imodbits_plate ],
["occc_normanhelmcoif_x", "Norman Helm Coif", [("normanhelmcoif",0)], itp_type_head_armor|itp_merchandise   ,0,
 479 , weight(2.75)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(5) ,imodbits_plate ],
 
["occc_helm_valsgarde", "Valsgarde Helm", [("VALSGARDE8",0)], itp_type_head_armor|itp_covers_head, 0, 760, weight(2.0)|abundance(1)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_4]  ],
["occc_helm_valsgarde_cloth", "Valsgarde Helm", [("BL_03_Valsgarde01",0)], itp_type_head_armor|itp_merchandise, 0, 620, weight(2)|abundance(1)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_4]  ],
["occc_helm_valsgarde_small", "Valsgarde Helm", [("Valsgarde_small",0)], itp_type_head_armor|itp_merchandise, 0, 380, weight(1.5)|abundance(1)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_4]  ],
["occc_nordic_chieftain_helmet", "Elite Huscarl's Helmet", [("x_chieftainhelm",0)], itp_type_head_armor, 0, 700, weight(2)|abundance(20)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_4] ],
["occc_nordic_huscarl_warhelmet1", "Elite Huscarl's Helmet", [("copy_x_chieftainhelm",0)], itp_type_head_armor|itp_covers_beard, 0, 700, weight(2)|abundance(20)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_4] ],
["occc_nordic_raider_helmet", "Nordic Raider's Helmet", [("BL_04_Valsgarde07BOAR",0)], itp_type_head_armor|itp_merchandise, 0, 390, weight(1.5)|abundance(20)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_4] ],
["occc_nordic_raider_warhelmet1", "Raider's Helmet", [("BL_03_Valsgarde09",0)], itp_type_head_armor, 0, 300, weight(1.5)|abundance(20)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_4] ],

["occc_fenrir_helmet_close", "Fenrir Helmet", [("bers_helm",0),("bers_helm_inventory",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 2048, weight(2)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_4]],
["occc_fenrir_helmet_open", "Opened Fenrir Helmet", [("bers_helm_open",0),("bers_helm_inventory",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 2048, weight(2)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_4]],

["occc_helm_dovahkiin", "Dovahkiin Helm", [("dragonborn_helm_renew",0)], itp_type_head_armor, 0, 80000, weight(2.75)|abundance(4)|head_armor(70)|body_armor(0)|leg_armor(0)|difficulty(50), imodbits_armor ],
["occc_helm_konungr", "Konungr's Winged Helm", [("xenoargh_gold_winged_viking_helm_eyepiece",0)], itp_type_head_armor, 0, 80000, weight(2.75)|abundance(4)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate ],

#["occc_cnut_crownhelm1", "Nordic Ruler's Helm", [("amade_bronze_winged_helm_plain",0)], itp_type_head_armor|itp_civilian, 0, 80000, weight(1.5)|head_armor(52)|body_armor(2)|leg_armor(2)|difficulty(7) ,imodbits_armor ],
["occc_cnut_crownhelm2", "Nordic Ruler's War Helm", [("amade_bronze_winged_helm_store",0)], itp_type_head_armor, 0, 80000, abundance(4)|weight(2)|head_armor(62)|body_armor(2)|leg_armor(2)|difficulty(7) ,imodbits_plate ],
["occc_wingedhelm", "Winged Helm", [("winged_helm_y2",0)], itp_merchandise|itp_type_head_armor|itp_doesnt_cover_hair, 0, 15000, abundance(100)|weight(1.5)|head_armor(55)|body_armor(2)|leg_armor(2)|difficulty(7) ,imodbits_plate, [], [fac_valkyrie] ],

#imported from CtA
["occc_einhendi_trondrox_x", "Jomsviking Axe", [("x_einhendi_trondrox",0)], itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
 870 , weight(2.5)|abundance(7)|difficulty(9)|spd_rtng(96) | weapon_length(75)|swing_damage(42 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_4] ],
["occc_einhendi_breithofudox_x", "Jomsviking Axe", [("x_einhendi_breithofudox",0)], itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield|itp_wooden_parry, itc_scimitar|itcf_carry_axe_left_hip,
 1500 , weight(3.5)|abundance(7)|difficulty(9)|spd_rtng(95) | weapon_length(82)|swing_damage(43 , pierce) | thrust_damage(0 ,  pierce),imodbits_axe, [], [fac_kingdom_4] ],
["occc_tveirhendr_hedmarkox_x", "Jomsviking Great Axe", [("x_tveirhendr_hedmarkox",0)], itp_type_polearm| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry,
  itc_parry_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_axe_back,
 1800 , weight(5.7)|abundance(3)|difficulty(10)|spd_rtng(85) | weapon_length(123)|swing_damage(65 , pierce) | thrust_damage(0 ,  blunt),imodbits_axe, [], [fac_kingdom_4] ],
["occc_tveirhendr_danox_x", "Jomsviking Great Axe", [("x_tveirhendr_danox",0)], itp_type_polearm| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry,
  itc_parry_polearm|itcf_overswing_polearm|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_axe_back,
 1800 , weight(5.8)|abundance(3)|difficulty(10)|spd_rtng(83) | weapon_length(123)|swing_damage(66 , pierce) | thrust_damage(0 ,  blunt),imodbits_axe, [], [fac_kingdom_4] ],
["occc_langr_bryntvari",  "Nordic Spear", [("x_langr_bryntvari",0)], itp_couchable|itp_merchandise|itp_type_polearm| itp_primary|itp_offset_lance|itp_wooden_parry|itp_penalty_with_shield|itp_primary|itp_secondary, itc_spear_new|itcf_carry_spear,
 560 , weight(2.5)|difficulty(0)|spd_rtng(90) | weapon_length(203)|swing_damage(24, blunt) | thrust_damage(32 ,  pierce),imodbits_polearm, [], [fac_kingdom_4] ],
["occc_sviar",  "Nordic Spear", [("x_sviar",0)], itp_couchable|itp_merchandise|itp_type_polearm| itp_primary|itp_offset_lance|itp_wooden_parry|itp_penalty_with_shield|itp_primary|itp_secondary, itc_spear_new|itcf_carry_spear,
 560 , weight(2.5)|difficulty(0)|spd_rtng(90) | weapon_length(203)|swing_damage(24, blunt) | thrust_damage(32 ,  pierce),imodbits_polearm, [], [fac_kingdom_4] ],

 
["occc_ulfberht", "Ulfberht", [("jarl",0),("jarl_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip,
 1260 , weight(1.25)|abundance(50)|difficulty(11)|spd_rtng(94) | weapon_length(96)|swing_damage(40 , cut) | thrust_damage(27 ,  pierce),imodbit_masterwork],

["occc_hrunting", "Hrunting", [("wolfsword",0),("wolfsword_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip,
 1500 , weight(1.25)|difficulty(12)|spd_rtng(89) | weapon_length(100)|swing_damage(44 , cut) | thrust_damage(30 ,  pierce),imodbit_masterwork],

 
["occc_heathen_great_sword", "Heathen Great Sword", [("kingslayer",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 2048, weight(2)|difficulty(11)|spd_rtng(110)|weapon_length(117)|swing_damage(47,cut)|thrust_damage(42,pierce), imodbits_sword_high ],

["occc_jomsviking_shield_x", "Jomsviking Shield", [("x_talak_jomsviking_shield",0)], itp_type_shield |itp_wooden_parry|itp_cant_use_on_horseback, itcf_carry_round_shield,
 600 , weight(4.5)|abundance(50)|hit_points(480)|body_armor(24)|spd_rtng(89)|shield_width(55)|difficulty(5),imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_01", "Nord Round Shield", [("ad_viking_shield_round_04",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_02", "Nord Round Shield", [("ad_viking_shield_round_05",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_03", "Nord Round Shield", [("ad_viking_shield_round_06",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_04", "Nord Round Shield", [("ad_viking_shield_round_07",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_05", "Nord Round Shield", [("ad_viking_shield_round_08",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_06", "Nord Round Shield", [("ad_viking_shield_round_09",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_07", "Nord Round Shield", [("ad_viking_shield_round_10",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_08", "Nord Round Shield", [("ad_viking_shield_round_11",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_09", "Nord Round Shield", [("ad_viking_shield_round_12",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_10", "Nord Round Shield", [("ad_viking_shield_round_14",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
["occc_viking_shield_11", "Nord Round Shield", [("ad_viking_shield_round_15",0)], itp_type_shield|itp_merchandise|itp_wooden_parry, itcf_carry_round_shield, 170, weight(6)|hit_points(350)|body_armor(20)|spd_rtng(84)|shield_width(50), imodbits_shield, [], [fac_kingdom_4] ],
 #axe shield axeshield01
["occc_einhendi_shield", "Axe Shield", [("axeshield01",0)], itp_type_shield|itp_merchandise, itcf_carry_sword_left_hip, 700, weight(2.5)|hit_points(400)|body_armor(5)|spd_rtng(120)|weapon_length(30), imodbits_shield, [], [fac_kingdom_4] ],

##################
#Rhodok and Hellas
##################
#mid roman
["occc_helm_roma_praetor_masked", "Masked Praetor Helm", [("catafract_helmet_2",0)], itp_type_head_armor|itp_covers_beard, 0, 740, weight(3)|abundance(100)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor, [], [fac_kingdom_5] ],
["occc_helm_roma_legio_masked", "Masked Legio Helm", [("catafract_helmet_1",0)], itp_type_head_armor|itp_covers_beard, 0, 500, weight(3)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor, [], [fac_kingdom_5] ],
["occc_helm_roma_cent_masked", "Masked Centurion Helm", [("catafract_helmet_3",0)], itp_type_head_armor|itp_covers_beard, 0, 600, weight(3)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor, [], [fac_kingdom_5] ],
["occc_g_helm_spak2", "Provocator Helm", [("x_g_helm_spak2",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise    ,0,
 187 , weight(2.75)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate, [], [fac_kingdom_5] ],
["occc_gradiator_arena_helmet_red", "Arena Helmet Red", [("roman_tourney_helmR",0)], itp_type_head_armor|itp_fit_to_head|itp_covers_beard ,0, 187 , weight(1.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0), imodbits_plate ],
["occc_gradiator_arena_helmet_blue", "Arena Helmet Blue", [("roman_tourney_helmB",0)], itp_type_head_armor|itp_fit_to_head|itp_covers_beard ,0, 187 , weight(1.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0), imodbits_plate ],
["occc_gradiator_arena_helmet_green", "Arena Helmet Green", [("roman_tourney_helmG",0)], itp_type_head_armor|itp_fit_to_head|itp_covers_beard ,0, 187 , weight(1.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0), imodbits_plate ],
["occc_gradiator_arena_helmet_yellow", "Arena Helmet Yellow", [("roman_tourney_helmY",0)], itp_type_head_armor|itp_fit_to_head|itp_covers_beard ,0, 187 , weight(1.25)|abundance(100)|head_armor(32)|body_armor(0)|leg_armor(0), imodbits_plate ],

["occc_ancient_bronze_helm1", "Ancient Bronze Helm", [("mrmasters_corintiah_helmet_steel", 0),], itp_type_head_armor|itp_merchandise, 0, 320, weight(3)|head_armor(33), imodbit_old,[], [fac_kingdom_8] ],
["occc_ancient_bronze_helm2", "Ancient Bronze Helm", [("mrmasters_corintiah_helmet", 0),], itp_type_head_armor|itp_merchandise, 0, 320, weight(3)|head_armor(33), imodbit_old,[], [fac_kingdom_8] ],
["occc_helm_roma_tribune1", "Legatus Helm", [("h_tribune",0), ("h_tribune_inventory",ixmesh_inventory)], itp_type_head_armor|itp_attach_armature, 0, 2048, weight(2)|abundance(30)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor ],
["occc_helm_roma_tribune2", "Legatus Helm", [("h_tribune2",0), ("h_tribune2_inventory",ixmesh_inventory)], itp_type_head_armor|itp_attach_armature, 0, 2048, weight(2)|abundance(30)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],
["occc_helm_roma_tribune3", "Black Legatus Helm", [("h_tribune4",0)], itp_type_head_armor|itp_attach_armature, 0, 2048, weight(2.25)|abundance(30)|head_armor(55)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor ],
["occc_helm_roma_tribune4", "Legatus Helm", [("h_tribune_steel",0), ("h_tribune_steel_inv",ixmesh_inventory)], itp_type_head_armor|itp_attach_armature, 0, 2048, weight(2)|abundance(30)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor ],
["occc_helm_roma_imperator", "Imperator Helm", [("imperator_helm",0)], itp_type_head_armor|itp_attach_armature, 0, 10000, weight(2.25)|abundance(0)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate ],

#early roman helms
["occc_gaelic_helm", "Gaelic Helm", [("gallicmontefortinob", 0),], itp_type_head_armor, 0, 230, weight(2)|head_armor(30), imodbit_old ],

#late roman helms
["occc_roman_ridge_1", "Late Imperial Ridge Helm", [("dux_ridge_helm", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 350, weight(1.5)|head_armor(38), imodbits_armor,[],[fac_kingdom_5] ],
["occc_roman_ridge_2", "Late Imperial Elite Helm", [("dux_ridge_helm_gold", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 360, weight(1.5)|head_armor(39), imodbits_armor,[],[fac_kingdom_5] ],
["occc_roman_ridge_plumed_1", "Late Imperial Ridge Helm", [("dux_ridge_helm_plume", 0),], itp_type_head_armor|itp_fit_to_head, 0, 450, weight(1.5)|head_armor(41), imodbits_armor,[],[fac_kingdom_5] ],
["occc_roman_ridge_plumed_2", "Late Imperial Elite Helm", [("copy_dux_ridge_helm_plume", 0),], itp_type_head_armor|itp_fit_to_head, 0, 450, weight(1.5)|head_armor(43), imodbits_armor,[],[fac_kingdom_5] ],
["occc_mm_horse_helm_masked", "Masked Imperial Horseman Helm", [("late_roman_cav_helm", 0),], itp_type_head_armor|itp_covers_beard, 0, 400, weight(1.5)|head_armor(46), imodbits_armor,[],[fac_kingdom_5] ],

["occc_laurel_gold", "Laurel Gold", [("laurel_gold",0)],itp_type_head_armor|itp_civilian|itp_doesnt_cover_hair,0,65000, weight(1)|abundance(1)|head_armor(30)|body_armor(8)|leg_armor(8)|difficulty(0),imodbits_cloth],
##mm
["mm_horse_helm", "Late Imperial Horseman Helm", [("avar_horse_helm", 0),], itp_type_head_armor|itp_merchandise, 0, 400, weight(1.5)|head_armor(40), imodbits_armor,[],[fac_kingdom_5] ],
["mm_romanspangenhelm", "Ancient Helm", [("old_spangenhelm", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 300, weight(1.5)|head_armor(32), imodbits_armor,[],[fac_kingdom_5] ],
["mm_romanelitehelm", "Late Imperial Elite Helmet", [("romanelitehelm", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 350, weight(2)|abundance(90)|head_armor(42), imodbits_armor,[],[fac_kingdom_5] ],
["mm_romanplumedhelm", "Late Imperial Plumed Helm", [("romanplumedhelm", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 350, weight(1.5)|head_armor(39), imodbits_armor,[],[fac_kingdom_5] ],
["occc_romanspangenhelm_1", "Ancient Spangen Helm", [("old_spangenhelmcheek", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 350, weight(1.5)|abundance(90)|head_armor(39), imodbits_armor,[],[fac_kingdom_5] ],
["occc_romanspangenhelm_2", "Ancient Spangen Helm", [("old_spangenhelmaven", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 350, weight(2)|head_armor(42), imodbits_armor,[],[fac_kingdom_5] ],
["occc_romanspangenhelm_3", "Ancient Spangen Helm", [("old_spangenhelm_masked", 0),], itp_type_head_armor|itp_fit_to_head|itp_covers_beard, 0, 450, weight(2)|head_armor(47), imodbits_armor,[],[fac_kingdom_5] ],

["occc_romanspangenhelm_4", "Imperial Spangen Helm", [("spangenhelm_a", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 450, weight(2)|head_armor(44), imodbits_armor,[],[fac_kingdom_5] ],
["occc_romanspangenhelm_5", "Ornament Spangen Helm", [("spangenhelm_a_ornate", 0),], itp_type_head_armor|itp_fit_to_head|itp_merchandise, 0, 450, weight(2)|head_armor(46), imodbits_armor,[],[fac_kingdom_5] ],


["occc_armor_roma_light", "Veteris Armor", [("roman_light_armor",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 100, weight(6)|abundance(100)|head_armor(0)|body_armor(22)|leg_armor(0)|difficulty(6), imodbits_cloth,[],[fac_kingdom_5] ],


["occc_toga", "Tunica", [("roman_shirt",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 3, weight(1)|abundance(100)|head_armor(0)|body_armor(5)|leg_armor(0)|difficulty(0), imodbits_cloth,[],[fac_kingdom_5] ],

["occc_armor_roman_chain", "Centurion Hamata", [("a_roman_chain",0)], itp_type_body_armor|itp_covers_legs, 0, 1200, weight(20)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(10), imodbits_armor ],
["occc_rolica_musculata1", "Lorica Musculata", [("tribune_b",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(24)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(15)|difficulty(10), imodbits_plate ],
["occc_rolica_musculata2", "Lorica Musculata", [("a_tribune",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(23)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(15)|difficulty(10), imodbits_plate ],
["occc_rolica_musculata_black", "Lorica Musculata", [("black_musculata",0)], itp_type_body_armor|itp_covers_legs, 0, 4000, weight(24)|abundance(100)|head_armor(0)|body_armor(53)|leg_armor(15)|difficulty(10), imodbits_plate ],
["occc_rolica_musculata_imperator", "Imperator Musculata", [("imperator_musculata_caped",0)], itp_type_body_armor|itp_covers_legs, 0, 20000, weight(24)|abundance(100)|head_armor(0)|body_armor(56)|leg_armor(15)|difficulty(10), imodbits_plate ],
["occc_germanicus_musculata", "Germanicus's Musculata", [("copy_tribune_b",0)], itp_type_body_armor|itp_covers_legs, 0, 15000, weight(25)|abundance(100)|head_armor(2)|body_armor(55)|leg_armor(15)|difficulty(10), imodbits_plate ],

["occc_roman_chiseled_armor", "Chiseled Musculata", [("aqs_gold_roman",0)], itp_type_body_armor|itp_covers_legs, 0, 25000, weight(24)|abundance(100)|head_armor(0)|body_armor(56)|leg_armor(15)|difficulty(10), imodbits_plate ],

["occc_armor_centurion_chain_caped", "Caped Centurion Hamata", [("a_roman_chain_caped",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(22)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(15)|difficulty(10), imodbits_armor ],
["occc_armor_roma_caped_segmentata", "Caped Segmentata", [("caped_segmentata",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(22)|abundance(100)|head_armor(0)|body_armor(53)|leg_armor(17)|difficulty(10), imodbits_armor ],

#late roman armors
["occc_late_roman_mail", "Late Imperial Mail", [("lateromanmail", 0),], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1150, weight(16.5)|body_armor(39)|leg_armor(13), imodbits_armor,[],[fac_kingdom_5] ],
["occc_late_roman_scale", "Late Imperial Scale", [("lateromanscale", 0),], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 1800, weight(17)|body_armor(48)|leg_armor(14), imodbits_armor,[],[fac_kingdom_5] ],
["occc_late_roman_elite_armor", "Late Imperial Elite Scale", [("bizans_armor_c", 0),], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 3828, weight(25)|body_armor(54)|leg_armor(16), imodbits_armor,[],[fac_kingdom_5] ],
["occc_armor_roman_royal_scale_armor_caped", "Caped Royal Scale", [("late_roman_royal_scale",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 2460, weight(19)|abundance(100)|head_armor(0)|body_armor(51)|leg_armor(14)|difficulty(10), imodbits_armor,[],[fac_kingdom_5] ],
["occc_late_imperial_lamellar", "Imperial Lamellar", [("lam_calradic", 0),], itp_type_body_armor|itp_covers_legs, 0, 2558, weight(24)|abundance(160)|body_armor(54)|leg_armor(19), imodbits_armor,[],[fac_kingdom_5] ],
["occc_late_imperial_scale_armor", "Imperial Scale", [("calradic_scale_armor_e",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2558, weight(25)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(13)|difficulty(8), imodbits_armor,[],[fac_kingdom_5] ],

#boots
["occc_greaves_roma_gutter_single", "Single Gutter Greave", [("roman_greaves_gutter_single",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 900, weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(18)|difficulty(0), imodbits_armor,[],[fac_kingdom_5] ],
["occc_roman_sandal_female", "Female Roman Sandal", [("sandal_girl",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise|itp_civilian, 0, 10, weight(0.1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(2)|difficulty(0), imodbits_armor,[],[fac_kingdom_5] ],

#shields
["occc_shield_roma_cav", "Roman Cavalry Scutum", [("roman_shield_cav_2",0)], itp_type_shield, itcf_carry_board_shield, 600, weight(6)|hit_points(320)|body_armor(18)|leg_armor(12)|spd_rtng(85)|shield_width(50)|shield_height(95), imodbits_shield ],
["occc_shield_roma_ovalscutum", "Oval Scutum", [("ovalga",0)], itp_type_shield|itp_wooden_parry, itcf_carry_board_shield, 500, weight(5)|hit_points(280)|body_armor(13)|spd_rtng(90)|shield_width(45)|shield_height(94), imodbits_shield ],

#items
["occc_signum", "Rhodok Signum", [("signum_a", 0),], itp_type_two_handed_wpn|itp_no_parry|itp_two_handed|itp_primary, itcf_carry_spear|itcf_force_64_bits, 10000, weight(1.5)|spd_rtng(103)|weapon_length(200)|thrust_damage(0, blunt)|swing_damage(0, blunt), imodbits_none ],

["occc_spartan_xiphos", "Spartan Xiphos", [("spartan_xiphos",0),("spartan_xiphosscaba",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 1500 , weight(1.8)|abundance(40)|difficulty(15)|spd_rtng(110) | weapon_length(96)|swing_damage(40 , cut) | thrust_damage(34 ,  pierce),imodbits_sword_high , [], [fac_kingdom_8]],
["occc_sword_roma_spatha1", "Late Spatha", [("spatha1",0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip, 400, weight(1.5)|difficulty(12)|spd_rtng(95)|weapon_length(105)|swing_damage(35,cut)|thrust_damage(25,pierce), imodbits_sword ,[],[fac_kingdom_5]],
["occc_sword_roma_spatha2", "Late Spatha", [("spatha2",0)], itp_type_one_handed_wpn|itp_primary|itp_merchandise, itc_longsword|itcf_carry_sword_left_hip, 400, weight(1.5)|difficulty(12)|spd_rtng(95)|weapon_length(105)|swing_damage(37,cut)|thrust_damage(28,pierce), imodbits_sword ,[],[fac_kingdom_5]],


["occc_yattuke_cloth_white_robe", "White Robe", [("white_robe",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 24, weight(2)|abundance(85)|head_armor(0)|body_armor(5)|leg_armor(2)|difficulty(0), imodbits_cloth ],

#bronze series... bronze? no theyre made of gold haha...
["occc_bronze_plate", "Golden Muscle Plate", [("amade_bronze_plate",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(23)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(15)|difficulty(10), imodbits_plate ],
["occc_steel_plate", "Steel Muscle Plate", [("amade_steel_plate",0)], itp_type_body_armor|itp_covers_legs|itp_merchandise, 0, 2048, weight(23)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(15)|difficulty(10), imodbits_plate,[], [fac_kingdom_8] ],
["occc_champion_plate", "Hero's Muscle Plate", [("amade_bronze_plate_champion",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(23)|abundance(100)|head_armor(0)|body_armor(55)|leg_armor(15)|difficulty(10), imodbits_plate ],

["occc_bronze_plate_greaves", "Golden Greaves", [("amade_bronze_greaves",0)], itp_type_foot_armor|itp_attach_armature, 0, 3300, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(27)|difficulty(10), imodbit_old ],
["occc_steel_plate_greaves", "Steel Greaves", [("amade_steel_greaves",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 3300, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(27)|difficulty(10), imodbit_old,[], [fac_kingdom_8] ],


["occc_ancient_plate_mitten1", "Golden Plate Gauntlet", [("amade_bronze_gauntlet_R",0),("amade_bronze_gauntlet_L",imodbit_reinforced)], itp_type_hand_armor, 0, 700, weight(2)|abundance(100)|body_armor(8)|difficulty(0), imodbits_plate ],
["occc_ancient_plate_mitten2", "Steel Plate Gauntlet", [("amade_steel_gauntlet_R",0),("amade_steel_gauntlet_L",imodbit_reinforced)], itp_type_hand_armor|itp_merchandise, 0, 700, weight(2)|abundance(100)|body_armor(8)|difficulty(0), imodbits_plate,[], [fac_kingdom_8] ],


#old Rhodok
["occc_crossbow_arbalest", "Arbalest", [("we_rho_crossbow_arbalest",0)], itp_type_crossbow|itp_merchandise|itp_primary|itp_two_handed|itp_cant_reload_on_horseback,itcf_shoot_crossbow|itcf_carry_crossbow_back,1253,
 weight(4.25)|abundance(60)|difficulty(17)|spd_rtng(34)|shoot_speed(80)|thrust_damage(95,pierce)|max_ammo(1)|accuracy(99),imodbits_crossbow,[],[fac_kingdom_11]],

#imperial
["occc_crossbow_imperial", "Imperial Crossbow", [("spak_crsb01",0)], itp_type_crossbow|itp_primary|itp_merchandise,
 itcf_shoot_crossbow|itcf_carry_crossbow_back, 820, weight(3.75)|difficulty(8)|spd_rtng(56)|shoot_speed(85)|thrust_damage(61,pierce)|max_ammo(1), imodbits_crossbow, [], [fac_kingdom_5,fac_kingdom_7] ],
["occc_crossbow_sniper_roman", "Imperium Scorpio", [("spak_crsb02",0)], itp_type_crossbow|itp_cant_reload_on_horseback|itp_two_handed|itp_primary|itp_can_knock_down,
 itcf_shoot_crossbow|itcf_carry_crossbow_back, 2000, weight(8.75)|difficulty(21)|spd_rtng(20)|shoot_speed(118)|thrust_damage(165,pierce)|max_ammo(1)|accuracy(99), imodbits_crossbow ],#this may multiple hit

#barrel
["occc_greek_fire_thrower", "Flamethrower", [("occc_greek_fire",0)], itp_type_musket|itp_primary|itp_two_handed|itp_cant_reload_on_horseback|itp_cant_reload_while_moving ,itcf_shoot_musket|itcf_reload_musket|itcf_carry_spear, 
1500 , weight(14)|abundance(50)|difficulty(0)|spd_rtng(30) | shoot_speed(36) | thrust_damage(55 ,pierce)|max_ammo(50)|accuracy(65),imodbits_crossbow,
 [(ti_on_weapon_attack,[(play_sound,"snd_ccd_fire_burning")])] , [fac_kingdom_5]],
 ["occc_greek_fire","Greek Fire", [("ale_barrel",0),("occc_fire_projectile",ixmesh_flying_ammo), ("ale_barrel",ixmesh_inventory)], itp_type_bullets|itp_default_ammo|itp_can_penetrate_shield, 0, 920,weight(3.5)|abundance(80)|weapon_length(95)|thrust_damage(5,pierce)|max_ammo(100),imodbits_missile,
fired_projectile_triggers,
 
 # [(ti_on_init_item, [
    # (set_position_delta, 0, 100, 0), #change this to move the particle system's local position
    # (particle_system_add_new, "psys_arrow_fire"),
    # (particle_system_add_new, "psys_smoke"),
    # (particle_system_add_new, "psys_fire_sparks"),
    # (set_current_color,150, 130, 70),
    # (add_point_light, 10, 30),
# ])]
],

#["occc_scorpio_bolts", "Scorpio Bolts", [("ccd_heavy_bolt",0),("flying_bolt",ixmesh_flying_ammo),("bolt_bag_b",ixmesh_carry)], itp_type_bolts|itp_can_penetrate_shield|itp_bonus_against_shield, itcf_carry_quiver_right_vertical, 1024, weight(20)|abundance(10)|weapon_length(63)|thrust_damage(40,pierce)|max_ammo(16), 
# imodbits_missile, missile_distance_trigger, imodbits_missile, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"), (call_script, "script_occc_item_hit_pen_wp_set", "itm_occc_crossbow_sniper_roman", ":sa"),])] ],
#Scorpio
 

# Kengeki Spartan
["ore_ancient_spartan_helm", "Spartan Legend Helm", [("spartan_helm_y", 0),], itp_type_head_armor, 0, 2000, weight(2)|head_armor(31), imodbit_old ],
["ore_ancient_great_spartan_helm", "Great Spartan Legend Helm", [("great_spartan_helm_y", 0),], itp_type_head_armor, 0, 2700, weight(2)|head_armor(35), imodbit_old ],
["ore_spartan_cloak", "Spartan Legend Cloak", [("spartan_cloak2",0)], itp_type_body_armor|itp_covers_legs, 0, 10000, weight(0.5)|abundance(100)|head_armor(5)|body_armor(12)|leg_armor(5)|difficulty(0), imodbit_old ],
["ore_spartan_greaves", "Spartan Legend Greaves", [("spartan_greaves",0)], itp_type_foot_armor|itp_attach_armature, 0, 3300, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(25)|difficulty(10), imodbit_old ],
["occc_300spartanhoplon", "300 Legend Hoplon", [("300hoplon", 0),], itp_type_shield|itp_cant_use_on_horseback, itcf_carry_round_shield, 3000, weight(12)|body_armor(50)|leg_armor(25)|difficulty(8)|hit_points(550)|spd_rtng(77)|shield_width(90), imodbits_shield ],

 




#########
#sarranid
######### wei_xiadi_lamellar_armor02
["occc_armor_brass_mamluke", "Mamluke Mail", [("brass_mamluk_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 3400, weight(22)|abundance(20)|head_armor(0)|body_armor(48)|leg_armor(16)|difficulty(10), imodbits_armor,[], [fac_kingdom_6] ],
# ["occc_sarranid_platedchain", "Mamluke Mail", [("chain_tab",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 2900, weight(21)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(8), imodbits_armor, [], [fac_kingdom_6] ],
["occc_yeni_uniform", "Yeniceli Uniform", [("janichareteksiz",0)], itp_type_body_armor|itp_covers_legs, 0, 50, weight(1)|abundance(100)|head_armor(0)|body_armor(12)|leg_armor(9)|difficulty(0), imodbits_cloth ],

["occc_sarranid_leather_armor", "Sarranid Leather Armor", [("arab_padded_leather_3",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 650, weight(9)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_armor, [], [fac_kingdom_6] ],
["occc_sarranid_plated_mail1", "Sarranid Plated Mail", [("arab_mail_plate_1",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 1900, weight(21)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(7), imodbits_armor, [], [fac_kingdom_6] ],
["occc_sarranid_plated_mail2", "Sarranid Plated Mail", [("arab_mail_plate_red",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 1900, weight(21)|abundance(100)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(7), imodbits_armor, [], [fac_kingdom_6] ],



["occc_armor_guard_mamluke_1", "Guard Mamluke Mail", [("tyrk_armor_heavi_a",0)], itp_type_body_armor|itp_covers_legs, 0, 4500, weight(20)|abundance(20)|head_armor(0)|body_armor(54)|leg_armor(16)|difficulty(10), imodbits_plate,[], [fac_kingdom_6] ],
["occc_armor_guard_mamluke_2", "Guard Mamluke Mail", [("tyrk_armor_heavi_b",0)], itp_type_body_armor|itp_covers_legs, 0, 4500, weight(20)|abundance(20)|head_armor(0)|body_armor(54)|leg_armor(16)|difficulty(10), imodbits_plate,[], [fac_kingdom_6] ],
["occc_armor_guard_mamluke_3", "Guard Mamluke Mail", [("tyrk_armor_heavi_c",0)], itp_type_body_armor|itp_covers_legs, 0, 4500, weight(20)|abundance(20)|head_armor(0)|body_armor(54)|leg_armor(16)|difficulty(10), imodbits_plate,[], [fac_kingdom_6] ],

#["occc_armor_noble_sarranid_1", "Sarranid Noble Mail", [("Ghulam_heavy_cavalryman_1",0)], itp_type_body_armor|itp_covers_legs, 0, 4000, weight(19)|abundance(20)|head_armor(0)|body_armor(53)|leg_armor(14)|difficulty(9), imodbits_plate,[], [fac_kingdom_6] ],
["occc_armor_noble_sarranid_2", "Sarranid Noble Mail", [("Ghulam_heavy_cavalryman_2",0)], itp_type_body_armor|itp_covers_legs, 0, 4000, weight(19)|itp_merchandise|abundance(20)|head_armor(0)|body_armor(53)|leg_armor(14)|difficulty(9), imodbits_armor,[], [fac_kingdom_6] ],
["occc_armor_noble_sarranid_3", "Sarranid Noble Mail", [("Ghulam_heavy_cavalryman_3",0)], itp_type_body_armor|itp_covers_legs, 0, 4000, weight(19)|itp_merchandise|abundance(20)|head_armor(0)|body_armor(53)|leg_armor(14)|difficulty(9), imodbits_armor,[], [fac_kingdom_6] ],

["occc_sarranid_guard_helmet_1", "Sarranid Guard Helmet", [("helm_tyrk_a",0),("helm_tyrk_a_market",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 1024, weight(2)|abundance(10)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_6]],
["occc_sarranid_guard_helmet_2", "Sarranid Guard Helmet", [("helm_tyrk_b",0),("helm_tyrk_b_market",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 1024, weight(2)|abundance(10)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_6]],
["occc_sarranid_guard_helmet_3", "Sarranid Guard Helmet", [("helm_tyrk_c",0),("helm_tyrk_c_market",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 1024, weight(2)|abundance(10)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_6]],
["occc_sarranid_guard_helmet_4", "Sarranid Guard Helmet", [("helm_tyrk_d",0),("helm_tyrk_d_market",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 1024, weight(2)|abundance(10)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_6]],
["occc_sarranid_guard_helmet_5", "Sarranid Guard Helmet", [("helm_tyrk_e",0),("helm_tyrk_e_market",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 1024, weight(2)|abundance(10)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_6]],
["occc_sarranid_guard_helmet_6", "Sarranid Guard Helmet", [("helm_tyrk_f",0),("helm_tyrk_f_market",ixmesh_inventory)], 
 itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 1024, weight(2)|abundance(10)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_armor, [], [fac_kingdom_6]],


 
["occc_sarranid_h_guard_helmet_1", "Sarranid Heavy Guard Helmet", [("helm_tyrk_heavi_a",0)], 
 itp_type_head_armor|itp_covers_beard, 0, 2048, weight(3)|abundance(10)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6]],
["occc_sarranid_h_guard_helmet_2", "Sarranid Heavy Guard Helmet", [("helm_tyrk_heavi_c",0)], 
 itp_type_head_armor|itp_covers_beard, 0, 2048, weight(3)|abundance(10)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6]],

["occc_sarranid_ghulam_helm_1", "Ghulam Helmet", [("ghulss",0)], itp_type_head_armor|itp_covers_beard, 0, 700, weight(2)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],
["occc_sarranid_ghulam_helm_2", "Ghulam Helmet", [("ghulssss",0)], itp_type_head_armor|itp_covers_beard, 0, 500, weight(2)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor ],

#["occc_sarranid_noble_helm_1", "Sarranid Noble Helmet", [("gulam_helm_a",0)], itp_type_head_armor, 0, 800, weight(2)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_armor, [], [fac_kingdom_6] ],
["occc_sarranid_noble_helm_2", "Sarranid Noble Helmet", [("gulam_helm_d",0),("gulam_helm_d_market",ixmesh_inventory)],
  itp_type_head_armor|itp_attach_armature|itp_covers_beard|itp_merchandise, 0, 800, weight(2)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate, [], [fac_kingdom_6]],
["occc_sarranid_noble_helm_3", "Sarranid Noble Helmet", [("gulam_helm_f",0),("gulam_helm_f_market",ixmesh_inventory)],
  itp_type_head_armor|itp_covers_beard|itp_attach_armature|itp_merchandise, 0, 800, weight(2)|abundance(100)|head_armor(46)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate, [], [fac_kingdom_6]],

 
["occc_kuffiya", "Kuffiya", [("kuffiya",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 28, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_cloth,[], [fac_kingdom_6] ],
["occc_kuffiya_b", "Kuffiya", [("kuffiya_b",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 28, weight(1)|abundance(100)|head_armor(11)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_cloth,[], [fac_kingdom_6] ],

["occc_yeni_cap_1", "Yeniceli Cap", [("bork1",0)], itp_type_head_armor|itp_covers_beard, 0, 60, weight(1.50)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["occc_yeni_cap_2", "Yeniceli Cap", [("bork2",0)], itp_type_head_armor|itp_covers_beard, 0, 60, weight(1.50)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],
["occc_yeni_cap_3", "Yeniceli Cap", [("bork3",0)], itp_type_head_armor|itp_covers_beard, 0, 60, weight(1.50)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth ],

["occc_sarranid_sultan_helmet", "Sultan's Helmet", [("helm_Sultan_saracens",0),("helm_Sultan_saracens_market",ixmesh_inventory)], itp_type_head_armor|itp_covers_beard|itp_attach_armature, 0, 80000, weight(2)|abundance(100)|head_armor(56)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6]],
["occc_sarranid_sultan_mail1", "Sultan's Mail", [("armor_Sultan_saracens",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 80000, weight(21)|abundance(100)|head_armor(0)|body_armor(56)|leg_armor(16)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],

#["occc_sarranid_black_robe", "Black Robe", [("blackrobe",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 33, weight(1)|abundance(100)|head_armor(0)|body_armor(9)|leg_armor(9)|difficulty(0), imodbits_cloth ],

["occc_slave_body1", "Slave Body", [("skin_bumi", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 10, weight(0.5)|head_armor(1)|body_armor(1)|leg_armor(1)|difficulty(0), imodbits_cloth, [], [fac_kingdom_6] ],
["occc_slave_body2", "Slave Body", [("skin_veddah", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 10, weight(0.5)|head_armor(1)|body_armor(1)|leg_armor(1)|difficulty(0), imodbits_cloth, [], [fac_kingdom_6] ],

["occc_tuareg_helmet1", "Sarranid Tuareg Helmet", [("tuareg_helmet_additional",0)], itp_type_head_armor|itp_merchandise, 0, 290, weight(2.50)|abundance(100)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],
["occc_tuareg_helmet2", "Sarranid Tuareg Helmet", [("tuareg_helmet2_additional",0)], itp_type_head_armor|itp_merchandise, 0, 430, weight(3)|abundance(100)|head_armor(33)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],
["occc_sarranid_veiled_helmet", "Sarranid Veiled Helmet", [("sar_helmet4_additional",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 810, weight(3.30)|abundance(100)|head_armor(41)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6]],

#
["occc_assawira_helm", "Assawira Helmet", [("Assawira_helmet",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(2)|abundance(30)|head_armor(31)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],
["occc_ansar_helm", "Ansar Helmet", [("Ansar",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 460, weight(3)|abundance(30)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],
["occc_mujahidin_helm", "Mujahidin Helmet", [("Muslim_leader",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 550, weight(3)|abundance(30)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],
["occc_eastern_fullmail_helm", "Eastern Fullmail Helm", [("Full_mail_helmet",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 400, weight(1.75)|abundance(10)|head_armor(37)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_5] ],
["occc_eastern_conical_helm", "Eastern Conical Helm", [("Conical_helmet",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 420, weight(2)|abundance(10)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_5] ],

["occc_sarranid_horseman_helm_1", "Sarranid Horseman Helm", [("Mail_coif_helmet",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(1.75)|abundance(10)|head_armor(34)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_5] ],
["occc_sarranid_horseman_helm_2", "Sarranid Horseman Helm", [("Mail_spangenhelm",0)], itp_type_head_armor|itp_merchandise, 0, 300, weight(1.75)|abundance(10)|head_armor(34)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_5] ],


["occc_sarranid_heavy_turban_1", "Sarranid Mailed Turban", [("facecovermail_turban_1",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 480, weight(3)|abundance(100)|head_armor(43)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],
["occc_sarranid_heavy_turban_2", "Sarranid Mailed Turban", [("facecovermail_turban_2",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 600, weight(3)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_6] ],
["occc_seljuk_helmet_x", "Seljuk Helmet", [("seljuk_helmet",0)], itp_type_head_armor |itp_covers_beard    ,0,
 1200 , weight(3)|abundance(70)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],

["occc_hood_assassin1", "Assassin's Hood", [("youhou_assassin_hood",0)], itp_type_head_armor|itp_covers_beard, 0, 1000, weight(1)|abundance(2)|head_armor(28)|body_armor(0)|leg_armor(0), imodbits_cloth, [], [fac_kingdom_6] ],
["occc_hood_assassin2", "Assassin's Hood", [("youhou_assassin_hood_red",0)], itp_type_head_armor|itp_covers_beard, 0, 1000, weight(1)|abundance(2)|head_armor(28)|body_armor(0)|leg_armor(0), imodbits_cloth, [], [fac_kingdom_6] ],

["occc_armor_assassin1", "Assassin's Armor", [("youhou_assassin_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 6165, weight(6)|abundance(25)|head_armor(0)|body_armor(43)|leg_armor(12)|difficulty(0), imodbits_armor, [], [fac_kingdom_6] ],
["occc_armor_assassin2", "Assassin's Red Armor", [("youhou_assassin_armor_red",0)], itp_type_body_armor|itp_covers_legs, 0, 6165, weight(6)|abundance(25)|head_armor(0)|body_armor(44)|leg_armor(12)|difficulty(0), imodbits_armor, [], [fac_kingdom_6] ],

["occc_blade_assassin", "Assassin's Sword", [("youhou_assassin_sword",0),("youhou_assassin_sword_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_cleaver|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 6000 , weight(1.8)|abundance(15)|difficulty(12)|spd_rtng(105) | weapon_length(108)|swing_damage(47 , cut) | thrust_damage(0 ,  pierce),imodbits_sword_high ],
["occc_mamluke_throwing_scimitar", "Mamluke Scimitar", [("cimitar",0),("cimitarscaba",ixmesh_carry)], itp_type_thrown|itp_primary, itcf_throw_axe|itcf_carry_wakizashi|itcf_show_holster_when_drawn, 2000, weight(2)|difficulty(0)|spd_rtng(110)|shoot_speed(43)|thrust_damage(50,cut)|max_ammo(1)|weapon_length(115), imodbits_thrown_minus_heavy, missile_distance_trigger ],

########
#khergit
########
["occc_nomad_warmask1", "Nomad War Mask", [("vaeg_helmet8_additional",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 600, weight(3.50)|abundance(100)|head_armor(48)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_3] ],
["occc_nomad_warmask2", "Nomad War Mask", [("helm_tyrk_heavi_b",0)], itp_type_head_armor|itp_merchandise|itp_covers_beard, 0, 950, weight(3.50)|abundance(100)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_plate, [], [fac_kingdom_3] ],
["occc_khergit_warmask1", "Khergit War Mask", [("khergit_warmask_a",0)], itp_type_head_armor|itp_covers_beard, 0, 2048, weight(3.50)|abundance(10)|head_armor(50)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_3] ],
["occc_khergit_warmask2", "Khergit War Mask", [("khergit_warmask_b",0)], itp_type_head_armor|itp_covers_beard, 0, 2048, weight(3.50)|abundance(10)|head_armor(49)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_3] ],
["occc_khergit_warhelm1", "Khergit War Helm", [("khergit_warhelm_a",0)], itp_type_head_armor|itp_merchandise, 0, 700, weight(2.50)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate, [], [fac_kingdom_3] ],
["occc_khergit_warhelm2", "Khergit Helm", [("surcoat_dav_03a_helmet_b",0)], itp_type_head_armor|itp_merchandise, 0, 560, weight(1.50)|abundance(100)|head_armor(38)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate, [], [fac_kingdom_3] ],
["occc_khergit_warhelm3", "Khergit War Helm", [("mon_helmet_07_lam1",0)], itp_type_head_armor|itp_merchandise, 0, 800, weight(2.50)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(8), imodbits_plate, [], [fac_kingdom_3] ],

["occc_nomad_cap", "Nomad Cap", [("skin_helmet",0)], itp_type_head_armor|itp_merchandise|itp_civilian, 0, 6, weight(0.75)|abundance(100)|head_armor(10)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_3] ],

["occc_khergit_khan_armor", "Khan's Armor", [("surcoat_dav_02b",0)], itp_type_body_armor|itp_covers_legs, 0, 6000, weight(20)|abundance(1)|head_armor(0)|body_armor(54)|leg_armor(15)|difficulty(0), imodbits_armor ],
["occc_nomad_armor_lammellar1", "Nomad Lamellar Vest", [("armor_lam",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs|itp_civilian, 0, 970, weight(18)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(8)|difficulty(7), imodbits_armor, [], [fac_kingdom_3] ],
["occc_nomad_armor_lammellar2", "Nomad Lamellar Armor", [("chain_tab_2",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 970, weight(21)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(12)|difficulty(7), imodbits_armor, [], [fac_kingdom_3] ],

["occc_nomad_armor_heavy_1", "Nomad Heavy Armor", [("aqs_merchant_outf",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2048, weight(23)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(12)|difficulty(7), imodbits_armor, [], [fac_kingdom_3] ],
["occc_nomad_noble_armor_1", "Nomad Noble Armor", [("aqs_nobleman_outf",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 2048, weight(16)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(12)|difficulty(7), imodbits_armor, [], [fac_kingdom_3] ],

["occc_khergit_armor_heavy_1", "Khergit Heavy Armor", [("surcoat_dav_03a",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3928, weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(7), imodbits_armor, [], [fac_kingdom_3] ],
#["occc_khergit_armor_heavy_2", "Khergit Heavy Armor", [("surcoat_dav_03b_withSA",0)], itp_type_body_armor|itp_merchandise|itp_covers_legs, 0, 3928, weight(24)|abundance(100)|head_armor(0)|body_armor(48)|leg_armor(14)|difficulty(7), imodbits_cloth, [], [fac_kingdom_3] ],

["occc_khergit_lammellar_boots", "Khergit Lamellar Boots", [("surcoat_dav_03a_boots",0)], itp_type_foot_armor|itp_attach_armature|itp_merchandise, 0, 200, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_armor, [], [fac_kingdom_3] ],

["occc_rocket_bow", "Rocket Bow", [("nomad_bow",0),("nomad_bow_case",ixmesh_carry)], itp_type_bow|itp_cant_use_on_horseback|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 1000, weight(1.25)|difficulty(7)|spd_rtng(94)|accuracy(70)|shoot_speed(70)|thrust_damage(5,cut), imodbits_bow, [(ti_on_weapon_attack, [(play_sound,"snd_occc_rocket")])],[fac_kingdom_3] ],
["occc_explosive_arrow", "Explosive Arrows", [("ccd_bomb_bolt",0),("fire_arrow_flying_missile",ixmesh_flying_ammo),("arena_quiver",ixmesh_carry)], itp_type_arrows|itp_no_pick_up_from_ground, 0, 6000, weight(12)|thrust_damage(1,blunt)|max_ammo(15), imodbits_missile, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"), (call_script, "script_cf_occc_item_hit_effect_explosion_missile_set", "itm_occc_explosive_arrow", ":sa"),])] ],#occc_rocket
["ccd_tetuhau", "Khergit Grenade", [("throwing_stone",0)], itp_type_thrown|itp_primary|itp_no_pick_up_from_ground, itcf_throw_stone, 256, weight(2)|difficulty(0)|spd_rtng(95)|shoot_speed(80)|thrust_damage(30,cut)|max_ammo(12)|weapon_length(6), imodbits_none, [(ti_on_missile_hit, [(store_trigger_param_1,":sa"), (call_script, "script_ccd_item_hit_effect_explosion_missile", "itm_ccd_tetuhau", ":sa"),])] + missile_distance_trigger ],

["occc_khergit_heavy_machete", "Khergit Machete", [("mongol_heavy_sword",0)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip, 600, abundance(35)|weight(2.5)|difficulty(17)|spd_rtng(82)|weapon_length(115)|swing_damage(48,cut)|thrust_damage(0,pierce), imodbits_sword_high,[],[fac_kingdom_3] ],

["occc_khergit_pike_a_x", "Khergit Poleblade", [("x_khergit_pike_a",0)], itp_couchable|itp_type_polearm|itp_offset_lance| itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_two_handed|itp_merchandise, itc_guandao, 
 2200 , weight(4.5)|abundance(10)|difficulty(15)|spd_rtng(90) | weapon_length(200)|swing_damage(46 , cut) | thrust_damage(30 ,  pierce),imodbits_polearm , [], [fac_kingdom_3]],
["occc_khergit_pike_b_x", "Khergit Poleblade", [("x_khergit_pike_b",0)], itp_couchable|itp_type_polearm|itp_offset_lance| itp_primary|itp_bonus_against_shield|itp_wooden_parry|itp_two_handed|itp_merchandise, itc_guandao, 
 2200 , weight(4.5)|abundance(10)|difficulty(15)|spd_rtng(91) | weapon_length(200)|swing_damage(47 , cut) | thrust_damage(28 ,  pierce),imodbits_polearm , [], [fac_kingdom_3]],

########
#Dark Knights
########
["occc_helm_asmoday", "Asmoday Helmet", [("asmoday_helmet2",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 3642, weight(3.5)|abundance(5)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate , [], [fac_kingdom_7] ],
["occc_helm_asmoday_skull", "Asmoday Skull Head", [("asmoday_skull",0)], itp_type_head_armor|itp_covers_beard|itp_covers_head, 0, 3642, weight(3.5)|abundance(5)|head_armor(57)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate , [], [fac_kingdom_7] ],
["occc_helm_asmoday_zombie", "Asmoday Head", [("asmoday_ghoul",0)], itp_type_head_armor|itp_covers_beard|itp_covers_head, 0, 3642, weight(3.5)|abundance(5)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate , [], [fac_kingdom_7] ],

["occc_skull_crown", "Lich Crown", [("lich_crownskull",0)], itp_type_head_armor|itp_covers_beard|itp_covers_head, 0, 12000, weight(1.5)|head_armor(40)|body_armor(2)|leg_armor(2)|difficulty(7) ,imodbits_armor ],

["occc_dark_great_helm_1", "Dark Great Helmet", [("spak_helmet_k",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 2300, weight(2.5)|abundance(10)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate , [], [fac_kingdom_7] ],
["occc_dark_great_helm_2", "Dark Great Helmet", [("spak_helmet_k2",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise, 0, 2300, weight(2.5)|abundance(10)|head_armor(51)|body_armor(0)|leg_armor(0)|difficulty(12), imodbits_plate , [], [fac_kingdom_7] ],
["occc_demon_coat_of_plates_1", "Dreadful Coat of Plates", [("spak_coat_of_plates_b",0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 3828, weight(25)|abundance(20)|head_armor(0)|body_armor(56)|leg_armor(16)|difficulty(0), imodbits_plate, [], [fac_kingdom_7] ],
["occc_demon_coat_of_plates_2", "Dreadful Coat of Plates", [("spak_coat_of_plates_d",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 3828, weight(25)|abundance(20)|head_armor(0)|body_armor(55)|leg_armor(16)|difficulty(0), imodbits_plate, [], [fac_kingdom_7] ],
["occc_demon_coat_of_plates_3", "Dreadful Coat of Plates", [("spak_coat_of_plates_e",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 3828, weight(25)|abundance(20)|head_armor(0)|body_armor(56)|leg_armor(16)|difficulty(0), imodbits_plate, [], [fac_kingdom_7] ],
["occc_demon_coat_of_plates_4", "Dreadful Coat of Plates", [("spak_coat_of_plates_f",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 0, 3828, weight(25)|abundance(20)|head_armor(0)|body_armor(56)|leg_armor(16)|difficulty(0), imodbits_plate, [], [fac_kingdom_7] ],

["occc_dark_cuir_bouilli", "Dark Cuir_Bouilli", [("cuir_bouilli_sp",0)], itp_type_body_armor|itp_covers_legs|itp_civilian|itp_merchandise, 
  0, 3100, weight(24)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(15)|difficulty(8), imodbits_armor, [], [fac_kingdom_7] ],

["occc_sauron_helm", "Sauron Helm", [("sauron_helmet",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard|itp_unique, 0, 95000, weight(2.0)|abundance(2)|head_armor(70)|body_armor(0)|leg_armor(0)|difficulty(40), imodbits_plate ],
["occc_sauron_armor", "Sauron Armor", [("sauron_armour",0)], itp_type_body_armor|itp_covers_legs|itp_unique, 0, 95000, weight(33)|abundance(100)|head_armor(0)|body_armor(70)|leg_armor(32)|difficulty(40), imodbits_plate ],
["occc_sauron_boots", "Sauron Greaves", [("sauron_boots",0)], itp_type_foot_armor|itp_attach_armature|itp_unique, 0, 95000, weight(3.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(38)|difficulty(40), imodbits_plate ],


["occc_sauron_mace", "Doom Mace", [("sauron_mace",0)], itp_type_one_handed_wpn|itp_primary|itp_can_knock_down|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration|itp_ignore_friction, itc_scimitar|itcf_carry_mace_left_hip,
  30000, weight(4.5)|difficulty(20)|spd_rtng(100)|weapon_length(96)|swing_damage(48,blunt)|thrust_damage(0,pierce), imodbits_mace ],

["occc_dark_hunter_crossbow", "Dark Hunter Crossbow", [("van_helsing_crossbow_01", 0),("van_helsing_crossbow_scabbard",ixmesh_carry)], itp_type_crossbow|itp_two_handed|itp_primary, itcf_shoot_crossbow|itcf_carry_crossbow_back, 8000, weight(6)|abundance(9)|difficulty(8)|spd_rtng(40)|shoot_speed(88)|thrust_damage(54,pierce)|max_ammo(15),imodbits_crossbow ],
["occc_dark_hunter_bolts", "Dark Hunter Cartridge", [("van_helsing_crossbow_bolt",0),("flying_bolt",ixmesh_flying_ammo),("van_helsing_crossbow_bolt_bag",ixmesh_carry),("van_helsing_crossbow_bolt_bag",ixmesh_inventory)], itp_type_bolts|itp_default_ammo, 0, 1000, weight(4.25)|abundance(9)|weapon_length(63)|thrust_damage(1,pierce)|max_ammo(60), imodbits_missile, missile_distance_trigger ],

["occc_shield_dragon_1", "Drachen Shield", [("round_dragon_shield",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 600, weight(6.5)|hit_points(300)|body_armor(19)|spd_rtng(84)|shield_width(34), imodbits_shield, [], [fac_kingdom_7] ],
["occc_shield_dragon_2", "Drachen Shield", [("round_dragon_shield2",0)], itp_type_shield|itp_merchandise, itcf_carry_round_shield, 600, weight(6.5)|hit_points(300)|body_armor(19)|spd_rtng(84)|shield_width(34), imodbits_shield, [], [fac_kingdom_7] ],

#######
#sunset
#######

["occc_monchan_helm", "Tezcatlipoca Helm", [("skull_helmet_aztec",0)], itp_type_head_armor|itp_covers_beard, 0, 80000, weight(2)|abundance(100)|head_armor(40)|body_armor(0)|leg_armor(0)|difficulty(9), imodbits_plate, [], [fac_kingdom_10] ],
["occc_cuahchiqueh_helm_1", "Cuahchiqueh Helm", [("cuahchiqueh_helmet_b",0)], itp_type_head_armor, 0, 700, weight(1)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_cuahchiqueh_helm_2", "Cuahchiqueh Helm", [("cuahchiqueh_helmet_g",0)], itp_type_head_armor, 0, 700, weight(1)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_cuahchiqueh_helm_3", "Cuahchiqueh Helm", [("cuahchiqueh_helmet_r",0)], itp_type_head_armor, 0, 700, weight(1)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_cuahchiqueh_helm_4", "Cuahchiqueh Helm", [("cuahchiqueh_helmet_w",0)], itp_type_head_armor, 0, 700, weight(1)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_eagle_helm_1", "Eagle Helm", [("eagle_helmet1_1",0)], itp_type_head_armor, 0, 500, weight(1)|abundance(100)|head_armor(23)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_eagle_helm_2", "Eagle Helm", [("eagle_helmet1_2",0)], itp_type_head_armor, 0, 500, weight(1)|abundance(100)|head_armor(23)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_helm_1", "Jaguar Helm", [("jaguar_helmet_1",0)], itp_type_head_armor, 0, 700, weight(1.5)|abundance(100)|head_armor(29)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_helm_2", "Jaguar Helm", [("jaguar_helmet_2",0)], itp_type_head_armor, 0, 700, weight(1.5)|abundance(100)|head_armor(29)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_helm_3", "Jaguar Helm", [("jaguar_helmet_3",0)], itp_type_head_armor, 0, 700, weight(1.5)|abundance(100)|head_armor(29)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_helm_4", "Jaguar Helm", [("jaguar_helmet_4",0)], itp_type_head_armor, 0, 700, weight(1.5)|abundance(100)|head_armor(29)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_coyote_helm_1", "Coyote Helm", [("coyote_helmet1",0)], itp_type_head_armor, 0, 300, weight(1)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_coyote_helm_2", "Coyote Helm", [("coyote_helmet3",0)], itp_type_head_armor, 0, 300, weight(1)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_coyote_helm_3", "Coyote Helm", [("coyote_helmet4",0)], itp_type_head_armor, 0, 300, weight(1)|abundance(100)|head_armor(26)|body_armor(0)|leg_armor(0)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],


["occc_monchan_armor", "Tezcatlipoca Body", [("natives_cloth_b",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(1)|abundance(50)|head_armor(0)|body_armor(11)|leg_armor(3)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_cuahchiqueh_armour_1", "Cuahchiqueh Armor", [("cuahchiqueh_armour4",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(10)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_cuahchiqueh_armour_2", "Cuahchiqueh Armor", [("cuahchiqueh_armour3",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(10)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_eagle_armour_1", "Eagle Armor", [("eagle_armour2",0)], itp_type_body_armor|itp_covers_legs, 0, 500, weight(8)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_eagle_armour_2", "Eagle Armor", [("eagle_armour3",0)], itp_type_body_armor|itp_covers_legs, 0, 500, weight(8)|abundance(100)|head_armor(0)|body_armor(24)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_armour_1", "Jaguar Armor", [("jaguar_armour2",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(13)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_armour_2", "Jaguar Armor", [("jaguar_armour2",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(13)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_armour_3", "Jaguar Armor", [("jaguar_armour4",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(13)|abundance(100)|head_armor(0)|body_armor(32)|leg_armor(12)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_coyote_armour_1", "Coyote Armor", [("coyote_armour2",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(15)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(14)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_coyote_armour_2", "Coyote Armor", [("coyote_armour3",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(15)|abundance(100)|head_armor(0)|body_armor(35)|leg_armor(14)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_native_body_1", "Native Body", [("native_armor_f", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(0.5)|head_armor(1)|body_armor(1)|leg_armor(1)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_native_body_2", "Native Body", [("native_armor_e", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(0.5)|head_armor(1)|body_armor(1)|leg_armor(1)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_native_body_3", "Native Body", [("native_armor_c", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(0.5)|head_armor(1)|body_armor(1)|leg_armor(1)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],

["occc_cuahchiqueh_boots_1", "Cuahchiqueh Foot", [("cuahchiqueh_boots",0)], itp_type_foot_armor|itp_covers_legs, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_cuahchiqueh_boots_2", "Cuahchiqueh Foot", [("cuahchiqueh_boots3",0)], itp_type_foot_armor|itp_covers_legs, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_eagle_boots_1", "Eagle Foot", [("eagle_boots",0)], itp_type_foot_armor|itp_covers_legs, 0, 500, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(10)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_boots_1", "Jaguar Foot", [("jaguar_boots",0)], itp_type_foot_armor|itp_covers_legs, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_jaguar_boots_2", "Jaguar Foot", [("jaguar_boots2",0)], itp_type_foot_armor|itp_covers_legs, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(12)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_coyote_boots_1", "Coyote Foot", [("coyote_boots",0)], itp_type_foot_armor|itp_covers_legs, 0, 256, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(14)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],
["occc_coyote_boots_2", "Coyote Foot", [("coyote_boots3",0)], itp_type_foot_armor|itp_covers_legs, 0, 256, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(14)|difficulty(0), imodbits_cloth, [], [fac_kingdom_10] ],


["occc_macuahuitl", "One Hand Macuahuitl", [("maquahuitl",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip, 83, weight(1.5)|difficulty(0)|spd_rtng(115)|weapon_length(73)|swing_damage(24,blunt)|thrust_damage(0,pierce), imodbits_mace, [], [fac_kingdom_10] ],
["occc_pole_macuahuitl", "Pole Macuahuitl", [("maquahuitl_two_handed",0)], itp_type_two_handed_wpn|itp_wooden_parry|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_unbalanced|itp_merchandise, itc_cutting_spear|itcf_slashright_polearm|itcf_slashleft_polearm|itcf_carry_spear, 125, weight(3.0)|difficulty(0)|spd_rtng(106)|weapon_length(119)|swing_damage(36,blunt)|thrust_damage(10,blunt), imodbits_polearm, [], [fac_kingdom_10] ],
["occc_elite_macuahuitl_1", "Jaguar Macuahuitl", [("mackie_basehuitl",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip, 120, weight(2)|difficulty(0)|spd_rtng(115)|weapon_length(93)|swing_damage(31,blunt)|thrust_damage(0,pierce), imodbits_mace, [], [fac_kingdom_10] ],
["occc_elite_macuahuitl_2", "Elite Macuahuitl", [("mackie_basehuitl_plain",0)], itp_type_one_handed_wpn|itp_wooden_parry|itp_primary|itp_merchandise, itc_scimitar|itcf_carry_mace_left_hip, 98, weight(2)|difficulty(0)|spd_rtng(113)|weapon_length(93)|swing_damage(29,blunt)|thrust_damage(0,pierce), imodbits_mace, [], [fac_kingdom_10] ],
["occc_pole_tepoztopilli", "Tepoztopilli", [("mackie_tepoztopilli",0)], itp_type_polearm|itp_two_handed|itp_primary|itp_penalty_with_shield|itp_merchandise, itc_staff|itcf_horseback_overswing_right_onehanded|itcf_horseback_overswing_left_onehanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded, 1024, weight(6.0)|abundance(20)|difficulty(8)|spd_rtng(102)|weapon_length(157)|swing_damage(35,cut)|thrust_damage(27,blunt), imodbits_polearm, [], [fac_kingdom_10] ],

["occc_aztec_wardarts", "Atlatl", [("dart_a",0),("dart_a_bag",ixmesh_carry)], itp_type_thrown|itp_primary, itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 285, weight(5)|difficulty(1)|spd_rtng(93)|shoot_speed(55)|thrust_damage(15,pierce)|max_ammo(30)|weapon_length(45), imodbits_thrown, missile_distance_trigger ],


["occc_shield_aztec_1", "Aztec Shield", [("aztec_shield2",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 102, weight(2)|hit_points(150)|body_armor(8)|spd_rtng(78)|shield_width(30), imodbits_shield, [], [fac_kingdom_10] ],
["occc_shield_aztec_2", "Aztec Shield", [("aztec_shield3",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 102, weight(2)|hit_points(150)|body_armor(8)|spd_rtng(78)|shield_width(30), imodbits_shield, [], [fac_kingdom_10] ],
#["occc_shield_aztec_3", "Aztec Shield", [("aztec_shield4",0)], itp_type_shield|itp_wooden_parry, itcf_carry_board_shield, 1024, weight(3)|hit_points(150)|body_armor(8)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield, [], [fac_kingdom_10] ],
["occc_shield_aztec_4", "Aztec Shield", [("aztec_shield4",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 102, weight(2)|hit_points(150)|body_armor(8)|spd_rtng(78)|shield_width(30), imodbits_shield, [], [fac_kingdom_10] ],
["occc_shield_aztec_5", "Aztec Shield", [("aztec_shield6",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield, 102, weight(2)|hit_points(150)|body_armor(8)|spd_rtng(78)|shield_width(30), imodbits_shield, [], [fac_kingdom_10] ],
#["occc_shield_aztec_6", "Aztec Shield", [("aztec_shield7",0)], itp_type_shield|itp_wooden_parry, itcf_carry_board_shield, 1024, weight(3)|hit_points(150)|body_armor(8)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield, [], [fac_kingdom_10] ],
#["occc_shield_aztec_7", "Aztec Shield", [("aztec_shield8",0)], itp_type_shield|itp_wooden_parry, itcf_carry_board_shield, 1024, weight(3)|hit_points(150)|body_armor(8)|spd_rtng(78)|shield_width(43)|shield_height(100), imodbits_shield, [], [fac_kingdom_10] ],



 ######
 #Minka
 ######
["minka_lady_outfit_1", "Minka Lady Outfit", [("diaochan",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 200 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3] ],
["minka_lady_outfit_2", "Minka Lady Outfit", [("womancloth1",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 200 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3] ],
["minka_noble_lady_outfit_1", "Minka Noble Lady Outfit", [("woman_a_1",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 200 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3] ],
["minka_noble_lady_outfit_2", "Minka Noble Lady Outfit", [("diaochan_a",0)], itp_merchandise| itp_type_body_armor | itp_covers_legs  |itp_civilian ,0, 200 , weight(3)|abundance(100)|head_armor(0)|body_armor(15)|leg_armor(10)|difficulty(0) ,imodbits_cloth, [], [fac_kingdom_3] ],

["minka_general_armor_1", "Minka General Armor", [("mcshen_a",0)],  itp_merchandise|itp_type_body_armor |itp_covers_legs ,0, 
4000 , weight(25)|abundance(10)|head_armor(0)|body_armor(54)|leg_armor(18)|difficulty(10) ,imodbits_armor, [], [fac_kingdom_3] ],
["minka_general_armor_2", "Minka General Armor", [("lbshen_a",0)],  itp_merchandise|itp_type_body_armor |itp_covers_legs ,0, 
4000 , weight(25)|abundance(10)|head_armor(0)|body_armor(54)|leg_armor(18)|difficulty(10) ,imodbits_armor, [], [fac_kingdom_3] ],
["minka_general_armor_3", "Minka General Armor", [("zyshen_a",0)],  itp_merchandise|itp_type_body_armor |itp_covers_legs ,0, 
4800 , weight(25)|abundance(10)|head_armor(0)|body_armor(54)|leg_armor(18)|difficulty(10) ,imodbits_armor, [], [fac_kingdom_3] ],
["minka_general_armor_4", "Minka General Armor", [("lxshen_a",0)],  itp_merchandise|itp_type_body_armor |itp_covers_legs ,0, 
6000 , weight(25)|abundance(10)|head_armor(0)|body_armor(54)|leg_armor(20)|difficulty(12) ,imodbits_armor, [], [fac_kingdom_3] ],

["occc_eastern_falchion", "Eastern Falchion", [("falchion1hand",0),("falchion1hand_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 400, weight(2.5)|difficulty(10)|spd_rtng(107)|weapon_length(102)|swing_damage(39,cut)|thrust_damage(0,pierce), imodbits_sword_high ],



#######
#others
#######
#["occc_simple_armor", "Simple Armor", [("simple_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 3828, weight(25)|abundance(100)|head_armor(0)|body_armor(47)|leg_armor(16)|difficulty(8), imodbits_armor ],

["occc_normanpepperpot_x", "Norman Pepperpot", [("x_normanpepperpot",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise    ,0,
 450 , weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["occc_normanpepperpot", "Norman Pepperpot", [("normanpepperpot",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise    ,0,
 450 , weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["occc_munitionshelm1", "Munitions Helm", [("munitionshelm1",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise    ,0,
 450 , weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["occc_munitionshelm2", "Munitions Helm", [("munitionshelm2",0)], itp_type_head_armor|itp_covers_beard|itp_merchandise    ,0,
 450 , weight(2.75)|abundance(100)|head_armor(39)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],

["occc_early_hand_cannon", "Hand_Cannon", [("rrr_handgonne",0)], itp_type_musket|itp_merchandise|itp_primary|itp_two_handed|itp_cant_reload_on_horseback|itp_next_item_as_melee |itp_cant_reload_while_moving ,itcf_shoot_musket|itcf_reload_musket|itcf_carry_spear, 
850 , weight(4)|abundance(50)|difficulty(0)|spd_rtng(25) | shoot_speed(100) | thrust_damage(72 ,pierce)|max_ammo(1)|accuracy(45),imodbits_crossbow,
 [(ti_on_weapon_attack,[(play_sound,"snd_shot3"),(call_script, "script_ccd_gun_particle", 1),])] , [fac_kingdom_1,fac_kingdom_11,fac_kingdom_6]],
["occc_early_hand_cannon_melee", "Hand_Cannon", [("rrr_handgonne",0)],itp_type_polearm|itp_primary|itp_unique|itp_wooden_parry|itp_two_handed|itp_wooden_attack , itc_staff|itcf_carry_sword_back, 
850 , weight(4)|difficulty(0)|spd_rtng(90) | swing_damage(16, blunt) | thrust_damage(14 ,  blunt)|weapon_length(64),imodbits_crossbow ],
["occc_early_arquebuse", "Arquebuse", [("rrr_arquebuse",0)], itp_type_musket|itp_merchandise|itp_primary|itp_two_handed|itp_cant_reload_on_horseback|itp_can_penetrate_shield|itp_next_item_as_melee |itp_cant_reload_while_moving ,itcf_shoot_musket|itcf_reload_musket|itcf_carry_spear, 
990 , weight(4)|abundance(50)|difficulty(0)|spd_rtng(28) | shoot_speed(110) | thrust_damage(88 ,pierce)|max_ammo(1)|accuracy(65),imodbits_crossbow,
 [(ti_on_weapon_attack,[(play_sound,"snd_shot3"),(call_script, "script_ccd_gun_particle", 1),])] , [fac_kingdom_1,fac_kingdom_11,fac_kingdom_6]],
["occc_early_arquebuse_melee", "Arquebuse", [("rrr_arquebuse",0)],itp_type_polearm|itp_primary|itp_wooden_parry|itp_two_handed|itp_wooden_attack , itc_staff|itcf_carry_sword_back, 
990 , weight(4)|difficulty(0)|spd_rtng(88) | swing_damage(16, blunt) | thrust_damage(12 ,  blunt)|weapon_length(70),imodbits_crossbow ],
["occc_early_matchlock_musket", "Matchlock_Musket", [("rrr_matchlock_musket",0)], itp_type_musket|itp_merchandise|itp_primary|itp_two_handed|itp_cant_reload_on_horseback|itp_can_penetrate_shield |itp_cant_reload_while_moving ,itcf_shoot_musket|itcf_reload_musket|itcf_carry_sword_back, 
1500 , weight(4)|abundance(30)|difficulty(0)|spd_rtng(30) | shoot_speed(120) | thrust_damage(100 ,pierce)|max_ammo(1)|accuracy(75),imodbits_crossbow,
 [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),])] , [fac_kingdom_1,fac_kingdom_11,fac_kingdom_6]], ##### ADD MP

["occc_gewehr98", "Gewehr98", [("Gewehr98_Bayonet",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_use_on_horseback|itp_next_item_as_melee|itp_crush_through|itp_can_knock_down|itp_has_bayonet, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket|itc_parry_polearm,
 8000, weight(3.0)|abundance(5)|difficulty(0)|spd_rtng(30)|shoot_speed(250)|thrust_damage(105,pierce)|max_ammo(5)|accuracy(95), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_hyb_musket"),(call_script, "script_ccd_gun_particle", 1),])] ],
["occc_gewehr98_mel", "Gewehr98", [("Gewehr98_Bayonet",0)], itp_type_polearm|itp_unique|itp_wooden_parry|itp_primary|itp_cant_use_on_horseback, itcf_thrust_polearm|itcf_carry_spear|itcf_overswing_spear|itc_parry_polearm,
 1000, weight(3.0)|abundance(5)|difficulty(0)|spd_rtng(90)|weapon_length(130)|swing_damage(20,blunt)|thrust_damage(32,pierce), imodbits_crossbow ],

 
 

["occc_ebony_strong_bow",         "Ebony Composite Bow", [("strong_bow_2",0),("strong_bow_case_2", ixmesh_carry)], itp_type_bow |itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bowcase_left|itcf_show_holster_when_drawn, 
1500 , weight(1.5)|abundance(50)|difficulty(5)|spd_rtng(102) | shoot_speed(60) | thrust_damage(30 ,cut),imodbit_cracked | imodbit_bent | imodbit_masterwork , [], [fac_kingdom_3]],
["occc_ebony_war_bow",         "Ebony War Bow", [("war_bow_2",0),("war_bow_carry_2",ixmesh_carry)],itp_type_bow|itp_merchandise|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 
2200 , weight(2)|abundance(50)|difficulty(6)|spd_rtng(81) | shoot_speed(65) | thrust_damage(35 ,cut),imodbits_bow , [], [fac_kingdom_12]],
["occc_bow_chosen", "Chosen's Bow", [("amade_latticed_flatbow",0),("amade_latticed_flatbow_carry",ixmesh_carry)], itp_type_bow|itp_two_handed|itp_primary, itcf_shoot_bow|itcf_carry_bow_back, 6000, weight(1.5)|difficulty(7)|spd_rtng(100)|shoot_speed(78)|thrust_damage(37,cut), imodbits_bow ],

["occc_shield_hermitage_shield_additional_1", "Hermitage Shield", [("hermitage_shield_2",0)], itp_type_shield, itcf_carry_round_shield, 500, weight(9.5)|hit_points(410)|body_armor(18)|spd_rtng(81)|shield_width(40), imodbits_shield ],
["occc_shield_hermitage_shield_additional_2", "Hermitage Shield", [("hermitage_shield_3",0)], itp_type_shield, itcf_carry_round_shield, 500, weight(9.5)|hit_points(410)|body_armor(18)|spd_rtng(81)|shield_width(40), imodbits_shield ],
["occc_shield_hermitage_shield_additional_3", "Hermitage Shield", [("hermitage_shield_4",0)], itp_type_shield, itcf_carry_round_shield, 500, weight(9.5)|hit_points(410)|body_armor(18)|spd_rtng(81)|shield_width(40), imodbits_shield ],

["occc_kiai_shield", "Elan vital", [("gohst",0),("book_a",ixmesh_inventory)], itp_type_shield|itp_force_attach_left_hand|itp_unique, itcf_carry_round_shield,
50 , weight(0.1)|abundance(8)|hit_points(250)|body_armor(2)|spd_rtng(100)|shield_width(20),imodbits_shield ],

 #unique items
["occc_agilulfo_helm", "Nonexistent Helm", [("agilulfo_armet",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard,
 0, 8000, weight(2.75)|abundance(30)|head_armor(68)|body_armor(0)|leg_armor(0)|difficulty(15), imodbits_plate],
["occc_helm_arminius", "Arminius Helm", [("arminius_helm",0)], itp_type_head_armor|itp_covers_beard, 0, 10000, weight(3)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_armor, [], [fac_kingdom_5] ],
["occc_asmoday_sword", "Muramasa Blade", [("asmoday_sword",0),("asmoday_sword_scab", ixmesh_carry)], itp_type_two_handed_wpn|itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 80000 , weight(2)|abundance(18)|difficulty(10)|spd_rtng(120) | weapon_length(112)|swing_damage(52 , pierce) | thrust_damage(42 ,  pierce),imodbits_sword_high ],
["occc_imagin_sword", "Imaginary Sword", [("g103",0),("g103_scabbard",ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip, 
 12000, weight(2)|difficulty(0)|spd_rtng(132)|weapon_length(102)|swing_damage(45,cut)|thrust_damage(37,pierce), imodbits_sword_high ],
["occc_darger", "Darger", [("mackie_dagger",0),("mackie_dagger_scabbard",ixmesh_carry),("mackie_dagger_scabbard",imodbits_good),("mackie_dagger_scabbard",ixmesh_carry|imodbits_good)], itp_type_one_handed_wpn|itp_no_parry|itp_primary|itp_secondary, itc_dagger|itcf_carry_dagger_front_left|itcf_show_holster_when_drawn, 80000, weight(0.75)|difficulty(0)|spd_rtng(139)|weapon_length(47)|swing_damage(46,cut)|thrust_damage(44,pierce), imodbits_sword_high ],
["occc_highlander_masamune", "MASAMUNE", [("katana_y2_e",0),("katana_y2_saya_e", ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
 6000 , weight(2)|abundance(7)|difficulty(16)|spd_rtng(107) | weapon_length(110)|swing_damage(55 , pierce) | thrust_damage(52 ,  pierce),imodbits_sword_high ],
["occc_holy_grenade", "Holy Hand Grenade", [("holy_bible",0)], itp_type_thrown, itcf_throw_axe, 100000, weight(19)|difficulty(0)|spd_rtng(80)|shoot_speed(30)|thrust_damage(999,cut)|max_ammo(1)|weapon_length(80), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1,":sa"),(call_script,"script_ccc_item_hit_effect","itm_occc_holy_grenade",":sa"),])] ],
#legendary two handed swords (these can deflect missiles)
["occc_moonlight", "Moon Light", [("holy_brand",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration|itp_ignore_friction, itc_greatsword|itcf_carry_sword_back,
 20000 , weight(4.0)|abundance(1)|difficulty(23)|spd_rtng(102) | weapon_length(138)|swing_damage(58 , pierce) | thrust_damage(50 ,  pierce),imodbits_sword_high],#(ti_on_init_item,[(try_for_range, ":count", 2, 24),(store_mul, ":pos_y", 5, ":count"),(set_position_delta,0,":pos_y",0),(particle_system_add_new,"psys_occc_moonlight"),(try_end),
["occc_hoshitsubaki", "Hoshitsubaki", [("Aurorablade",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_greatsword|itcf_carry_sword_back, 80000, weight(2)|difficulty(15)|spd_rtng(125)|weapon_length(143)|swing_damage(70,cut)|thrust_damage(47,pierce), imodbits_sword_high ],
["occc_ultima_weapon", "Ultima Weapon", [("Ultima",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_extra_penetration|itp_ignore_friction, itc_greatsword|itcf_carry_sword_back, 80000, weight(3)|difficulty(20)|spd_rtng(110)|weapon_length(135)|swing_damage(55,pierce)|thrust_damage(56,pierce), imodbits_sword_high ],
["occc_lightsaber_red", "Red Light Saber", [("lightsaber_red_2h",0),("lightsaber_red_2hoff",ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_dagger_front_left, 5000, weight(2.0)|difficulty(21)|spd_rtng(120)|weapon_length(130)|swing_damage(50,pierce)|thrust_damage(50,pierce), imodbits_sword_high, [(ti_on_init_item,[(try_for_range, ":count", 3, 28),(store_mul, ":pos_y", 5, ":count"),(set_position_delta,0,":pos_y",0),(particle_system_add_new,"psys_ccd_light_spark"),(try_end),]),(ti_on_weapon_attack,[(play_sound, "snd_ccd_lightsaber_swing"),])] ],
["occc_lightsaber_green", "Green Light Saber", [("lightsaber_green_2h",0),("lightsaber_green_2hoff",ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_dagger_front_left, 5000, weight(2.0)|difficulty(21)|spd_rtng(120)|weapon_length(130)|swing_damage(50,pierce)|thrust_damage(50,pierce), imodbits_sword_high, [(ti_on_init_item,[(try_for_range, ":count", 3, 28),(store_mul, ":pos_y", 5, ":count"),(set_position_delta,0,":pos_y",0),(particle_system_add_new,"psys_ccd_light_spark_g"),(try_end),]),(ti_on_weapon_attack,[(play_sound, "snd_ccd_lightsaber_swing"),])] ],
["occc_lightsaber_blue", "Blue Light Saber", [("lightsaber_blue_2h",0),("lightsaber_blue_2hoff",ixmesh_carry)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_dagger_front_left, 5000, weight(2.0)|difficulty(21)|spd_rtng(120)|weapon_length(130)|swing_damage(50,pierce)|thrust_damage(50,pierce), imodbits_sword_high, [(ti_on_init_item,[(try_for_range, ":count", 3, 28),(store_mul, ":pos_y", 5, ":count"),(set_position_delta,0,":pos_y",0),(particle_system_add_new,"psys_ccd_light_spark_b"),(try_end),]),(ti_on_weapon_attack,[(play_sound, "snd_ccd_lightsaber_swing"),])] ],
#kengeki
["ccc_sword_two_ken_dragon_slayer", "Dragon Slayer", [("dragon_slayer_long",0)], itp_type_two_handed_wpn|itp_bonus_against_shield|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_sword_back, 2545, weight(4)|difficulty(18)|spd_rtng(80)|weapon_length(150)|swing_damage(50,cut)|thrust_damage(40,pierce), imodbits_sword_high ],
["ccc_sword_two_bar_dragon_slayer", "Black Dragon Slayer", [("DragonSlayer",0)], itp_type_two_handed_wpn|itp_crush_through|itp_two_handed|itp_primary, itc_bastardsword|itcf_carry_sword_back|itcf_force_64_bits, 25000, weight(5)|difficulty(25)|spd_rtng(75)|weapon_length(175)|swing_damage(65,cut)|thrust_damage(45,pierce), imodbits_sword_high ],




["occc_ccd_smart_full_body_test", "Test Smart Full Body", [("housemaid_body_under", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(4)|leg_armor(2)|difficulty(0), imodbits_cloth ],

#female armors imported from BoS
["occc_vanadis_fullarmor1", "Vanadis Armor", [("xenoargh_new_female_armor02",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor2", "Vanadis Armor", [("xenoargh_new_female_armor04",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor3", "Vanadis Sapphire Armor", [("xenoargh_new_female_armor_blue02",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor4", "Vanadis Sapphire Armor", [("xenoargh_new_female_armor_blue04",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor5", "Vanadis Emerald Armor", [("xenoargh_new_female_armor_green01",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor6", "Vanadis Emerald Armor", [("xenoargh_new_female_armor_green03",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor7", "Vanadis Garnet Armor", [("xenoargh_new_female_armor_orange03",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor8", "Vanadis Garnet Armor", [("xenoargh_new_female_armor_orange04",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(16)|abundance(10)|head_armor(0)|body_armor(52)|leg_armor(19)|difficulty(8), imodbits_armor ],

["occc_vanadis_fullarmor_sister1", "Vanadis Black Sister Armor", [("xenoargh_female_armor_sisters_of_mercy1",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(18)|abundance(10)|head_armor(0)|body_armor(56)|leg_armor(19)|difficulty(8), imodbits_armor ],
["occc_vanadis_fullarmor_sister2", "Vanadis Black Sister Armor", [("xenoargh_female_armor_sisters_of_mercy4",0)], itp_type_body_armor|itp_covers_legs, 0, 5048, weight(18)|abundance(10)|head_armor(0)|body_armor(56)|leg_armor(19)|difficulty(8), imodbits_armor ],

["occc_female_cloth_1", "Female Dress", [("anar2_dress", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(8)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["occc_female_cloth_2", "Female Dress", [("anar_dress", 0)], itp_type_body_armor|itp_covers_legs|itp_civilian, 0, 256, weight(5)|head_armor(2)|body_armor(8)|leg_armor(2)|difficulty(0), imodbits_cloth ],
["occc_amazon_armor", "Amazon Armor", [("aribeth_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 860, weight(7)|abundance(10)|head_armor(0)|body_armor(32)|leg_armor(8)|difficulty(8), imodbits_armor ],
["occc_bikini_armor_1", "Bikini Armor", [("rogue_armor1",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(4)|abundance(10)|head_armor(0)|body_armor(20)|leg_armor(2)|difficulty(8), imodbits_armor ],
["occc_bikini_armor_2", "Bikini Armor", [("rogue_armor2",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(3)|abundance(10)|head_armor(0)|body_armor(18)|leg_armor(1)|difficulty(8), imodbits_armor ],
["occc_warmistress_armor", "War Mistress Armor", [("xena_armor",0)], itp_type_body_armor|itp_covers_legs, 0, 860, weight(3)|abundance(10)|head_armor(0)|body_armor(22)|leg_armor(0)|difficulty(8), imodbits_armor ],

["occc_mail_with_surcoat_xf", "Mail with Blue Surcoat", [("x_mail_long_surcoat_new_f",0)],  itp_type_body_armor  |itp_covers_legs ,0,
 1850 , weight(24)|abundance(80)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(7) ,imodbits_armor ],

#Onna kishi
["occc_onnakishi_hair", "Female Commander's Hair", [("onnna_kishi_hair",0)], itp_type_head_armor, 0, 300, weight(0.1)|abundance(10)|head_armor(25)|body_armor(0)|leg_armor(0)|difficulty(7), imodbits_cloth, []],
["occc_onnakishi_yoroi", "Female Commander's Armor", [("onnna_kishi", 0)], itp_civilian|itp_type_body_armor|itp_covers_legs, 0, 8000, weight(22)|head_armor(0)|body_armor(53)|leg_armor(16)|difficulty(9), imodbits_armor ],
["occc_onnakishi_boots", "Female Commander's Boots", [("onnna_kishi_kutu",0)], itp_type_foot_armor|itp_covers_legs, 0, 700, weight(2)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(23)|difficulty(0), imodbits_cloth, []],


#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#Hunting Mod begin#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
 #["deer","Deer", [("deer",0)], itp_unique|itp_type_horse, 0, 1411,abundance(40)|hit_points(20)|body_armor(0)|difficulty(11)|horse_speed(40)|horse_maneuver(50)|horse_charge(10),imodbits_horse_basic],
 ["boar","Boar", [("boar",0)], itp_type_horse|itp_merchandise, 0, 500,abundance(2)|hit_points(100)|body_armor(10)|difficulty(2)|horse_speed(37)|horse_maneuver(20)|horse_charge(100),imodbits_horse_basic, [], [fac_kingdom_4]],
 
 #["deer_meat","Deer Meat", [("raw_meat",0)], itp_type_goods|itp_consumable|itp_food, 0, 10,weight(30)|abundance(100)|food_quality(40)|max_ammo(30),imodbits_none],
 ["boar_meat","Boar Meat", [("raw_meat",0)], itp_type_goods|itp_consumable|itp_food, 0, 20,weight(30)|abundance(100)|food_quality(80)|max_ammo(50),imodbits_none],
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#
#-#-#-#Hunting Mod end#-#-#-#
#-#-#-#-#-#-#-#-#-#-#-#-#-#-#


###############


#joke items
["occc_odinhelm", "Alfather's Winged Helm", [("valhelm2", 0)], itp_type_head_armor|itp_doesnt_cover_hair, 0, 2048, weight(1.5)|head_armor(80)|body_armor(0)|leg_armor(0)|difficulty(8) ,imodbits_plate ],
["occc_ban_hammer", "BAN HAMMER!", [("ban_hammer",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_crush_through|itp_unbalanced, itc_nodachi, 30, weight(30)|difficulty(55)|spd_rtng(53)|weapon_length(217)|swing_damage(64,blunt)|thrust_damage(0,pierce), imodbits_mace ],
["occc_blunt_chicken", "Blunt Chicken", [("chicken_montypython",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary, itc_scimitar, 90, weight(0.5)|spd_rtng(100)|weapon_length(65)|swing_damage(10,blunt)|thrust_damage(0,blunt), imodbits_none ],


##shadow_skull
["occc_shadow_skull_head", "Shadow_head", [("copy_skull",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(3)|abundance(100)|head_armor(28)|body_armor(0)|leg_armor(0)|difficulty(11), imodbits_plate ],
["occc_shadow_skeleton_cut", "Shadow Cut", [("copy_skeleton_cut",0)], itp_type_body_armor|itp_covers_legs|itp_covers_head|itp_covers_beard, 0, 700, weight(1)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(0)|difficulty(4), imodbits_plate ],
["occc_shadow_skeleton_calf", "Shadow Calf", [("copy_skeleton_calf_L",0)], itp_type_foot_armor|itp_civilian, 0, 700, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(31)|difficulty(8), imodbits_armor ],
["occc_shadow_skeleton_hand", "Shadow Hand", [("copy_skeleton_hand_R",0),("copy_skeleton_hand_L",imodbit_reinforced)], itp_type_hand_armor, 0, 700, weight(1.0)|abundance(100)|body_armor(7)|difficulty(0), imodbits_plate ],

##Monsters
#Demon Lord
#["occc_shadow_demonlord_head", "Demon_Shadow_head", [("demon_warlordhead",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard|itp_fit_to_head|itp_unique, 0, 1000, weight(3)|abundance(100)|head_armor(75)|body_armor(0)|leg_armor(0)|difficulty(63), imodbits_plate ],
#["occc_shadow_demonlord_cut", "Demon_Shadow body", [("demon_warlordbody",0)], itp_type_body_armor|itp_covers_legs|itp_covers_head|itp_covers_beard|itp_unique, 0, 1000, weight(1)|abundance(100)|head_armor(0)|body_armor(75)|leg_armor(0)|difficulty(63), imodbits_plate ],
#["occc_shadow_demonlord_calf", "Demon_Shadow boots", [("demonwarlordfoot",0)], itp_type_foot_armor|itp_civilian|itp_unique, 0, 1000, weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(75)|difficulty(63), imodbits_armor ],
#Minotaur
["occc_minotaur_head", "Minotaur_head", [("minotaur",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard|itp_fit_to_head, 0, 700, weight(1)|abundance(100)|head_armor(54)|body_armor(0)|leg_armor(0)|difficulty(1), imodbits_plate ],


##Undead Legions
["occc_helm_roma_cent_undead", "Undead Cent Head", [("undead_cent_helm",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 700, weight(2)|abundance(100)|head_armor(42)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_ancient ],
["occc_helm_roma_legio_undead", "Undead Legio Head", [("undead_legio_helm",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 400, weight(2)|abundance(100)|head_armor(36)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_ancient ],
["occc_helm_roma_praetor_undead", "Undead Tribune Head", [("h_undead_tribune",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard|itp_attach_armature, 0, 800, weight(2)|abundance(100)|head_armor(47)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_ancient ],
["occc_helm_roma_coolusc_undead", "Undead Coolusc Head", [("copy_undead_legio_helm",0)], itp_type_head_armor|itp_covers_head|itp_covers_beard, 0, 280, weight(2)|abundance(100)|head_armor(29)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_ancient ],
["occc_helm_ancient_honorguard_1", "Ancient Honor Guard Helm", [("VALSGARDE8_honorguard",0)], itp_type_head_armor|itp_covers_head, 0, 1024, weight(2.5)|abundance(1)|head_armor(52)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_5]  ],
["occc_helm_ancient_honorguard_2", "Ancient Honor Guard Helm", [("talak_sutton_hoo_honorguard",0)], itp_type_head_armor, 0, 1030, weight(2.2)|abundance(1)|head_armor(44)|body_armor(0)|leg_armor(0)|difficulty(10), imodbits_plate, [], [fac_kingdom_5]  ],

["occc_rolica_musculata_undead", "Ancient Lorica Musculata", [("undead_tribune",0)], itp_type_body_armor|itp_covers_legs, 0, 2048, weight(24)|abundance(100)|head_armor(0)|body_armor(52)|leg_armor(15)|difficulty(10), imodbits_ancient ],
["occc_armor_roman_chain_undead", "Ancient Centurion Hamata", [("undead_a_roman_chain",0)], itp_type_body_armor|itp_covers_legs, 0, 700, weight(20)|abundance(100)|head_armor(0)|body_armor(45)|leg_armor(15)|difficulty(10), imodbits_ancient ],
["occc_armor_segmentata_undead", "Ancient Segmentata", [("undead_legio_segmentata",0)], itp_type_body_armor|itp_covers_legs, 0, 1800, weight(22)|abundance(100)|head_armor(0)|body_armor(50)|leg_armor(15)|difficulty(10), imodbits_ancient ],
["occc_ancient_honorguard_armor_1", "Ancient Honor Guard Armor", [("bizans_armor_c_honorguard", 0),], itp_type_body_armor|itp_covers_legs, 0, 3828, weight(27)|body_armor(54)|leg_armor(16), imodbits_armor,[],[fac_kingdom_5] ],
["occc_ancient_honorguard_armor_2", "Ancient Honor Guard Armor", [("lam_calradic_ancient", 0),], itp_type_body_armor|itp_covers_legs, 0, 3828, weight(27)|body_armor(54)|leg_armor(16), imodbits_armor,[],[fac_kingdom_5] ],

["occc_skeleton_foot", "Skelton Foot", [("skelton_foot",0)], itp_type_foot_armor|itp_attach_armature|itp_covers_legs, 0, 530, weight(1.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(15)|difficulty(0), imodbits_ancient ],
["occc_skeleton_greaves", "Skelton Greaves", [("undead_legio_foot",0)], itp_type_foot_armor|itp_attach_armature, 0, 2461, weight(2.5)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(28)|difficulty(0), imodbits_ancient ],

["occc_ancient_war_scythe", "Ancient War Scythe", [("warscythe_honorguard",0)], itp_type_two_handed_wpn|itp_two_handed|itp_primary, itc_nodachi|itcf_carry_sword_back, 1250, weight(4.0)|difficulty(18)|spd_rtng(91)|weapon_length(128)|swing_damage(41,cut)|thrust_damage(0,pierce), imodbits_sword_high ],

["occc_spawn_legio", "Throwing Spawn Legionary", [("undead_legio_helm", 0)], itp_type_thrown|itp_unique|itp_no_pick_up_from_ground, itcf_throw_knife, 1024, weight(2)|difficulty(0)|spd_rtng(120)|shoot_speed(20)|thrust_damage(15, blunt)|max_ammo(6)|weapon_length(50), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1, ":sa"),(call_script, "script_ccc_item_hit_effect", "itm_occc_spawn_legio",":sa"),])] ],
["occc_spawn_honorguard", "Throwing Spawn Honorguard", [("talak_sutton_hoo_honorguard", 0)], itp_type_thrown|itp_unique|itp_no_pick_up_from_ground, itcf_throw_knife, 1024, weight(2)|difficulty(0)|spd_rtng(120)|shoot_speed(18)|thrust_damage(15, blunt)|max_ammo(4)|weapon_length(50), imodbits_thrown, [(ti_on_missile_hit,[(store_trigger_param_1, ":sa"),(call_script, "script_ccc_item_hit_effect", "itm_occc_spawn_honorguard",":sa"),])] ],

#occc system items
["occc_transparent_foot", "sys_transparent Feet", [("gohst",0),("transparent_helmet_inv",ixmesh_inventory)], itp_unique|itp_type_foot_armor|itp_civilian,0, 1 , weight(0.25)|abundance(0)|head_armor(0)|body_armor(0)|leg_armor(1)|difficulty(0) ,imodbits_none ],
#["occc_system_onehand_pole_spear", "Onehand Fix Spear", [("spear_g_1-9m",0)], itp_type_polearm|itp_wooden_parry|itp_primary|itp_offset_lance, itc_staff|itcf_carry_spear, 53, weight(2.0)|difficulty(0)|spd_rtng(125)|weapon_length(120)|swing_damage(12,blunt)|thrust_damage(20,cut), imodbits_polearm ],

#Horn From Brytenwalda
["occc_horn", "Horn", [("horn",0),("gohst",ixmesh_flying_ammo)], itp_type_thrown |itp_primary|itp_no_pick_up_from_ground, itcf_throw_knife, 420 , weight(1.5)|difficulty(0)|spd_rtng(50) | shoot_speed(45) | thrust_damage(3 ,  cut)|max_ammo(3)|weapon_length(0),imodbits_thrown,
   [(ti_on_weapon_attack, [(store_trigger_param_1,":sa"),(agent_get_team, ":user_team", ":sa"),(agent_set_animation, ":sa", "anim_cheer", 1),#yeahh!!

       (play_sound,"snd_occc_horn"),(try_for_agents,":agent"),
                              (agent_is_alive,":agent"),
                              (agent_is_human,":agent"),
							  (agent_get_team, ":cur_team", ":agent"),
							  (neg|teams_are_enemies, ":user_team", ":cur_team"),
       (agent_get_slot, ":agent_courage_score", ":agent", slot_agent_courage_score),
       (val_add, ":agent_courage_score", 200),#gaining courage
       (agent_set_slot, ":agent", slot_agent_courage_score, ":agent_courage_score"),           
       (store_agent_hit_points,":life",":agent",0),
##       (try_begin),
##       (agent_set_animation, ":troop", "anim_horn_blow"),
###                           (agent_set_animation, ":agent", "anim_cheer"),
##       (try_end),
       (val_add,":life",3),
       (agent_set_hit_points,":agent",":life",0),
		(agent_get_troop_id, ":p_id", ":agent"),	   
		(troop_get_type, ":is_female", ":p_id"),
		(try_begin),
		  (this_or_next|eq,":is_female",  12),#tf_elf_female
		  (this_or_next|eq, ":is_female", 10),#tf_gaolu_female
		  (this_or_next|eq, ":is_female", 9),#tf_girl
		  (eq, ":is_female", 1),#tf_female
		  (agent_play_sound, ":agent", "snd_woman_victory"),
		(else_try),
		  (agent_play_sound, ":agent", "snd_man_victory"),
		(try_end),
       (try_end),           
       (store_add,":recovery",3),
       (assign,reg1,":recovery"),
     #  (display_message,"@Horn rally men! (wounded troops recover 5 hitpoints)",0x6495ed),            (agent_play_sound, ":player_agent", "snd_woman_victory"),

                              ],)]],
							  
# ["occc_marchsong", "Play March Song", [("gohst",0),("occc_musician_gloves",ixmesh_inventory),("gohst",ixmesh_flying_ammo)], itp_type_thrown |itp_primary|itp_no_pick_up_from_ground|itp_unique, itcf_throw_knife, 1450 , weight(1.5)|difficulty(0)|spd_rtng(100) | shoot_speed(80) | thrust_damage(3 ,  cut)|max_ammo(1)|weapon_length(0),imodbits_thrown,
   # [(ti_on_weapon_attack, [(store_trigger_param_1,":sa"),(agent_get_team, ":user_team", ":sa"),(agent_play_sound, ":sa", "snd_occc_marchsong"),#yeahh!!
        # (agent_get_position,pos1,":sa"),

							  # (try_for_agents,":agent"),
                              # (agent_is_alive,":agent"),
                              # (agent_is_human,":agent"),
							  # (agent_get_position,pos2,":agent"),
							  # (get_distance_between_positions,":dist",pos1,pos2),
							  # (lt,":dist",5000),#50m
							  # (agent_get_team, ":cur_team", ":agent"),
							  # (neg|teams_are_enemies, ":user_team", ":cur_team"),
       # (agent_get_slot, ":agent_courage_score", ":agent", slot_agent_courage_score),
       # (val_add, ":agent_courage_score", 500),#gaining courage
       # (agent_set_slot, ":agent", slot_agent_courage_score, ":agent_courage_score"),           
       # (store_agent_hit_points,":life",":agent",0),
       # (val_add,":life",4),
       # (agent_set_hit_points,":agent",":life",0),
       # (store_add,":recovery",4),
       # (assign,reg1,":recovery"),

                              # ],)]],

							  
							  
							  


["occc_necronomicon", "Necronomicon", [("necronomicon",0)], itp_type_goods, 0, 10000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_1", "Christianity Bible", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_2", "Norse Saga", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_3", "Tengri Bible", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_4", "Quran", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_5", "Roman-Greece Bible", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_6", "Shinto Bible", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_7", "Quetzalcoatl Bible", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],
["occc_bible_8", "Baal Bible", [("holy_bible",0)], itp_type_goods, 0, 5000, weight(2)|abundance(100)|max_ammo(1), imodbits_none ],



#firearms 05
["occc_drum_magazine", "Drum_Magazine", [("Drum_Magazine",0),("ccd_tracer",ixmesh_flying_ammo),("Drum_Magazine",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_bonus_against_shield|itp_unique, 0, 80, weight(3.0)|abundance(60)|weapon_length(3)|thrust_damage(10,pierce)|max_ammo(250), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + ccd_tracer_triggers + missile_distance_trigger ],
["occc_normal_magazine", "Magazine", [("Magazine",0),("ccd_tracer",ixmesh_flying_ammo),("Magazine",ixmesh_inventory),], itp_type_bullets|itp_default_ammo|itp_bonus_against_shield|itp_unique, 0, 30, weight(2.0)|abundance(60)|weapon_length(3)|thrust_damage(10,pierce)|max_ammo(90), imodbits_missile, [(ti_on_missile_hit,[(call_script,"script_oim_on_bullet_hit"),])] + ccd_tracer_triggers + missile_distance_trigger ],

["occc_m37", "M37", [("M37",0)], itp_type_musket|itp_unique|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_can_knock_down|itp_cant_reload_while_moving|itp_next_item_as_melee, itcf_shoot_musket|itc_parry_polearm|itcf_carry_spear|itcf_reload_musket, 1024, weight(2.0)|difficulty(0)|spd_rtng(90)|shoot_speed(120)|thrust_damage(57,pierce)|max_ammo(8)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot16"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["occc_m37_b", "M37", [("M37",0)], itp_type_polearm|itp_unique|itp_two_handed|itp_primary|itp_wooden_parry, itc_parry_polearm|itcf_overswing_musket|itcf_slashright_twohanded|itcf_slashleft_twohanded|itcf_horseback_slashright_onehanded|itcf_horseback_slashleft_onehanded|itcf_carry_spear, 1024, weight(2.0)|difficulty(0)|spd_rtng(98)|weapon_length(100)|swing_damage(27, blunt)|thrust_damage(25, blunt), imodbits_crossbow ],

["occc_m37_t", "M37_T", [("M37_T",0)], itp_type_musket|itp_two_handed|itp_primary|itp_bonus_against_shield|itp_can_knock_down|itp_cant_reload_while_moving|itp_next_item_as_melee, itcf_shoot_musket|itc_parry_polearm|itcf_carry_spear|itcf_reload_musket, 1024, weight(2.0)|difficulty(0)|spd_rtng(90)|shoot_speed(120)|thrust_damage(57,pierce)|max_ammo(8)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot16"),(call_script, "script_ccd_gun_particle", 1),(store_trigger_param_1, ":agent_id"),(call_script, "script_ccd_shotgun_fire", ":agent_id"),])] ],
["occc_m37_t_b", "M37_T", [("M37_T",0)], itp_type_polearm|itp_two_handed|itp_primary, itc_musket_melee_ccd|itcf_carry_spear, 4545, weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(130)|swing_damage(38,cut)|thrust_damage(28,pierce), imodbits_polearm ],



["occc_fn1949bayonet", "FN1949bayonet", [("FN1949bayonet",0)], itp_type_musket|itp_two_handed|itp_primary|itp_next_item_as_melee|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 1024, weight(3.0)|difficulty(0)|spd_rtng(60)|shoot_speed(500)|thrust_damage(150,pierce)|max_ammo(10)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot7"),(call_script, "script_ccd_gun_particle", 1),])] ],
["occc_fn1949bayonet", "FN1949bayonet", [("FN1949bayonet",0)], itp_type_polearm|itp_two_handed|itp_primary, itc_musket_melee_ccd|itcf_carry_spear, 4545, weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(130)|swing_damage(38,cut)|thrust_damage(28,pierce), imodbits_polearm ],

["occc_gew43", "Gew43", [("Gew43",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 1024, weight(3.0)|difficulty(0)|spd_rtng(60)|shoot_speed(200)|thrust_damage(100,pierce)|max_ammo(10)|accuracy(93), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot7"),(call_script, "script_ccd_gun_particle", 1),])] ],
["occc_mas49", "MAS49", [("MAS49",0)], itp_type_musket|itp_two_handed|itp_primary|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 1024, weight(3.0)|difficulty(0)|spd_rtng(60)|shoot_speed(200)|thrust_damage(100,pierce)|max_ammo(10)|accuracy(92), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot7"),(call_script, "script_ccd_gun_particle", 1),])] ],

#######################
#autofire weapons start
#######################
["autofire_weapons_begin", "AUTOFIRE WEAPONS BEGIN!", [("bullet",0),("bullet",ixmesh_carry)], itp_type_crossbow|itp_two_handed|itp_primary, itcf_shoot_musket|itcf_carry_crossbow_back|itcf_show_holster_when_drawn|itcf_reload_musket, 600, weight(1.25)|difficulty(0)|spd_rtng(67)|shoot_speed(399)|thrust_damage(29,pierce)|max_ammo(32)|accuracy(58), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),])], [fac_player_supporters_faction] ],

["occc_hk_mp5k", "Short Machine Gun", [("hk_mp5k",0)], itp_type_pistol|itp_primary, itcf_shoot_pistol|itcf_carry_revolver_right|itcf_reload_pistol, 8192, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(88)|thrust_damage(55,pierce)|max_ammo(30)|accuracy(95), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),(call_script, "script_ccd_gun_particle", 2),])], [fac_player_supporters_faction] ],
#["MP34", "MP34", [("MP34",0)],  itp_type_musket|itp_primary,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 8192, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(500)|thrust_damage(65,pierce)|max_ammo(32)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),])], [fac_player_supporters_faction] ],
["occc_mp34bayonet", "MP34bayonet.1", [("MP34bayonet.1",0)], itp_type_musket|itp_two_handed|itp_primary|itp_next_item_as_melee|itp_cant_reload_while_moving, itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 1024, weight(3.0)|difficulty(0)|spd_rtng(60)|shoot_speed(80)|thrust_damage(60,pierce)|max_ammo(32)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound,"snd_shot7"),(call_script, "script_ccd_gun_particle", 1),])] ],
["occc_mp34bayonet_mel", "MP34bayonet.1", [("MP34bayonet.1",0)], itp_type_polearm|itp_two_handed|itp_primary, itc_musket_melee_ccd|itcf_carry_spear, 4545, weight(3)|difficulty(0)|spd_rtng(90)|weapon_length(130)|swing_damage(38,cut)|thrust_damage(28,pierce), imodbits_polearm ],
["occc_mp35", "MP35", [("MP35",0)],  itp_type_musket|itp_primary,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2800, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(85)|thrust_damage(60,pierce)|max_ammo(32)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),(call_script, "script_ccd_gun_particle", 2),])], [fac_player_supporters_faction] ],
["occc_Thompson", "Thompson", [("Thompson",0)],  itp_type_musket|itp_primary,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2800, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(85)|thrust_damage(90,pierce)|max_ammo(30)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),(call_script, "script_ccd_gun_particle", 2),])], [fac_player_supporters_faction] ],
["occc_madsenM1945", "madsenM1945", [("madsenM1945",0)],  itp_type_musket|itp_primary,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2800, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(100)|thrust_damage(90,pierce)|max_ammo(30)|accuracy(80), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),(call_script, "script_ccd_gun_particle", 2),])], [fac_player_supporters_faction] ],

["occc_mp40", "MP40", [("mp40",0)],  itp_type_musket|itp_primary|itp_unique,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2800, weight(2)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(85)|thrust_damage(65,pierce)|max_ammo(32)|accuracy(90), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_shot7"),(call_script, "script_ccd_gun_particle", 2),])], [fac_player_supporters_faction] ],

#Heavy Machinegun(or assault rifle)s
["occc_bar", "BAR", [("BAR",0)],  itp_type_musket|itp_primary,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket|itp_cant_reload_while_moving, 2800, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(250)|thrust_damage(90,pierce)|max_ammo(20)|accuracy(85), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_ccd_shot_mg0815"),(call_script, "script_ccd_gun_particle", 3),])], [fac_player_supporters_faction] ],
["occc_mg42", "MG42", [("MG42",0)], itp_type_musket|itp_primary|itp_unique,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket|itp_cant_reload_while_moving, 8192, weight(11)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(350)|thrust_damage(85,pierce)|max_ammo(250)|accuracy(98), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_ccd_shot_mg0815"),(call_script, "script_ccd_gun_particle", 2),])], [fac_player_supporters_faction] ],
["occc_mg08_15", "MG08_15", [("MG08_15",0)], itp_type_musket|itp_primary,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket|itp_cant_reload_while_moving, 8192, weight(15)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(300)|thrust_damage(85,pierce)|max_ammo(250)|accuracy(98), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_ccd_shot_mg0815"),(call_script, "script_ccd_gun_particle", 3),])], [fac_player_supporters_faction] ],
["occc_stg44", "Stg44", [("mp44",0)],  itp_type_musket|itp_primary|itp_unique,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2800, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(200)|thrust_damage(90,pierce)|max_ammo(30)|accuracy(85), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_ccd_shot_mg0815"),(call_script, "script_ccd_gun_particle", 3),])], [fac_player_supporters_faction] ],
["occc_ak47", "AK47", [("KK_44",0)],  itp_type_musket|itp_primary|itp_unique,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2800, weight(3)|abundance(5)|difficulty(0)|spd_rtng(100)|shoot_speed(200)|thrust_damage(95,pierce)|max_ammo(30)|accuracy(75), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_ccd_shot_mg0815"),(call_script, "script_ccd_gun_particle", 3),])], [fac_player_supporters_faction] ],
["occc_m4a1", "M4A1", [("m4a1",0)],  itp_type_musket|itp_primary,  itcf_shoot_musket|itcf_carry_spear|itcf_reload_musket, 2800, weight(3)|abundance(5)|difficulty(0)|spd_rtng(110)|shoot_speed(200)|thrust_damage(80,pierce)|max_ammo(30)|accuracy(92), imodbits_crossbow, [(ti_on_weapon_attack,[(play_sound, "snd_ccd_shot_mg0815"),(call_script, "script_ccd_gun_particle", 3),])], [fac_player_supporters_faction] ],

#######################
#autofire weapons end
#######################
["occc_bat_1", "Bat", [("mackie_bat",0)], itp_type_two_handed_wpn|itp_primary, itc_morningstar|itcf_carry_sword_back, 50, weight(1)|difficulty(0)|spd_rtng(110)|weapon_length(116)|swing_damage(19,blunt)|thrust_damage(0,blunt), imodbits_mace ],
["occc_bat_2", "Nailed Bat", [("mackie_bat_nailed",0)], itp_type_two_handed_wpn|itp_primary, itc_morningstar|itcf_carry_sword_back, 80, weight(1)|difficulty(0)|spd_rtng(107)|weapon_length(116)|swing_damage(20,pierce)|thrust_damage(0,blunt), imodbits_mace ],
["occc_guitar", "Electric Guitar", [("electric_guitar",0)], itp_type_two_handed_wpn|itp_primary, itc_morningstar|itcf_carry_sword_back, 2000, weight(3)|difficulty(27)|spd_rtng(150)|weapon_length(135)|swing_damage(26,blunt)|thrust_damage(0,blunt), imodbits_mace ],

["occc_shovel", "Shovel", [("lapio",0),("lapio_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip,
 163 , weight(1.5)|difficulty(0)|spd_rtng(70) | weapon_length(65)|swing_damage(27 , cut) | thrust_damage(22 ,  pierce),imodbits_sword_high,[], [fac_kingdom_3] ],
["occc_police_shield", "Strange Shield", [("riotshieldus",0)], itp_type_shield|itp_cant_use_on_horseback, itcf_carry_board_shield, 400, weight(3)|hit_points(360)|body_armor(30)|leg_armor(30)|spd_rtng(100)|shield_width(43)|shield_height(90), imodbits_shield ],

["occc_helmet_supersoldat", "Supersoldat Helmet", [("breathmask_with_helmet_grau",0)], itp_type_head_armor|itp_covers_beard   ,0, 278 , weight(2)|abundance(100)|head_armor(45)|body_armor(0)|leg_armor(0) ,imodbits_armor ],
["occc_m35_helmet", "M35 Helmet", [("kypara1_grey",0)], itp_type_head_armor   ,0, 278 , weight(1)|abundance(100)|head_armor(24)|body_armor(0)|leg_armor(0) ,imodbits_armor ],
["occc_german_field_cap", "Field Cap", [("lakki_2",0)], itp_type_head_armor   ,0, 278 , weight(0.5)|abundance(100)|head_armor(8)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
["occc_gas_mask", "Strange Mask", [("gasmask",0)], itp_type_head_armor|itp_covers_beard   ,0, 278 , weight(1)|abundance(100)|head_armor(18)|body_armor(0)|leg_armor(0) ,imodbits_armor ],
["occc_special_force_helm", "Strange Helmet", [("blackhelmet",0)], itp_type_head_armor|itp_covers_beard|itp_covers_head   ,0, 600 , weight(1)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0) ,imodbits_armor ],
["occc_american_helm", "Strange Helmet", [("Helmet_with_glasses",0)], itp_type_head_armor   ,0, 600 , weight(1)|abundance(100)|head_armor(44)|body_armor(0)|leg_armor(0) ,imodbits_armor ],



["occc_german_stoss", "M36 Uniform", [("nco",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,
 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["occc_german_schutze", "M36 Uniform", [("shutze",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,
 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(13)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["occc_guerilla", "Strange Vest", [("guerilla",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,
 10 , weight(1)|abundance(100)|head_armor(0)|body_armor(7)|leg_armor(5)|difficulty(0) ,imodbits_cloth ],
["occc_special_force_armor", "Strange Armor", [("blackarmor",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,
 500 , weight(2)|abundance(100)|head_armor(0)|body_armor(40)|leg_armor(15)|difficulty(0) ,imodbits_cloth ],
["occc_american_armor", "Strange Armor", [("desertkevlar",0)], itp_type_body_armor |itp_civilian |itp_covers_legs ,0,
 500 , weight(2)|abundance(100)|head_armor(0)|body_armor(39)|leg_armor(19)|difficulty(0) ,imodbits_cloth ],

 
 
#Elven Items

["occc_lorien_sword_a","Elven_Longsword",[("lorien_sword_long",0),("scab_lorien_sword_long",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,900,weight(2)|difficulty(0)|spd_rtng(120)|weapon_length(100)|swing_damage(30,cut)|thrust_damage(20,pierce),imodbits_sword],
["occc_lorien_sword_b","Elven_Shortsword",[("lorien_sword_short",0),("scab_lorien_sword_short",ixmesh_carry)],itp_type_one_handed_wpn|itp_primary,itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,700,weight(1.5)|difficulty(0)|spd_rtng(130)|weapon_length(65)|swing_damage(28,cut)|thrust_damage(25,pierce),imodbits_sword],
["occc_lorien_sword_c","Elven_War_Sword",[("lorien_sword_hand_and_half",0),("scab_lorien_sword_hand_and_half",ixmesh_carry)],itp_type_two_handed_wpn|itp_primary,itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,1100,weight(2.5)|difficulty(0)|spd_rtng(118)|weapon_length(103)|swing_damage(33,cut)|thrust_damage(23,pierce),imodbits_sword],

["occc_riv_bow","Elven_Bow",[("rivendellbow",0),("rivendellbow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back,11000,weight(1.8)|difficulty(4)|shoot_speed(99)|spd_rtng(96)|thrust_damage(27,pierce)|accuracy(99),imodbits_bow],
["occc_lorien_bow","Galadhrim_Bow",[("Elfbow",0),("Elfbow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed,itcf_shoot_bow|itcf_carry_bow_back,13000,weight(1.5)|difficulty(7)|shoot_speed(105)|spd_rtng(93)|thrust_damage(29,pierce)|accuracy(99),imodbits_bow ],

["occc_elven_arrows","Elven_Arrows",[("white_elf_arrow",0),("white_elf_arrow_flying",ixmesh_flying_ammo),("lothlorien_quiver",ixmesh_carry)],itp_type_arrows,itcf_carry_quiver_back,500,weight(3)|thrust_damage(15,pierce)|max_ammo(31)|weapon_length(91),imodbits_missile,[]],

###########LORIEN ARMORS########
["occc_lorien_archer","Elven_Archer_Armor",[("lorien_archer",0)],itp_type_body_armor|itp_covers_legs,0,500,weight(8)|head_armor(0)|body_armor(36)|leg_armor(16)|difficulty(0),imodbits_cloth,],
["occc_lorien_armor_a","Elven_Infantry_Armor",[("lorien_infantry",0)],itp_type_body_armor|itp_covers_legs,0,800,weight(12)|head_armor(0)|body_armor(40)|leg_armor(18)|difficulty(0),imodbits_cloth,],
["occc_lorien_armor_b","Elven_Heavy_Infantry_Armor",[("lorien_vetinfantry",0)],itp_type_body_armor|itp_covers_legs,0,1000,weight(12)|head_armor(0)|body_armor(45)|leg_armor(18)|difficulty(0),imodbits_cloth,],
["occc_lorien_armor_c","Elven_Royal_Archer_Armor",[("lorien_royalarcher",0)],itp_type_body_armor|itp_covers_legs,0,1500,weight(12)|head_armor(0)|body_armor(55)|leg_armor(20)|difficulty(0),imodbits_cloth,],
["occc_lorien_armor_d","Elven_Royal_Swordsman_Armor",[("lorien_royalswordsman",0)],itp_type_body_armor|itp_covers_legs,0,2400,weight(12)|head_armor(0)|body_armor(55)|leg_armor(20)|difficulty(0),imodbits_cloth,],
["occc_lorien_armor_e","Elven_Warden_Cloak",[("lorien_warden_cloak",0)],itp_type_body_armor|itp_covers_legs,0,700,weight(12)|head_armor(0)|body_armor(58)|leg_armor(20)|difficulty(0),imodbits_cloth,],
["occc_lorien_armor_f","Elven_Elite_Armor",[("lorien_royal",0)],itp_type_body_armor|itp_covers_legs,0,2000,weight(12)|head_armor(0)|body_armor(60)|leg_armor(20)|difficulty(0),imodbits_cloth,],
#
["occc_lorien_boots","Elven_Boots",[("lorien_boots",0)],itp_type_foot_armor|itp_attach_armature,0,1500,weight(1)|leg_armor(28)|difficulty(0),imodbits_cloth],
########LORIEN SHIELDS#####
["occc_lorien_shield_b","Elven_Tower_Shield",[("lorien_kite",0)],itp_type_shield|itp_wooden_parry|itp_cant_use_on_horseback,itcf_carry_kite_shield,700,weight(2)|hit_points(1000)|body_armor(18)|spd_rtng(82)|difficulty(9)|weapon_length(90),imodbits_shield,],
["occc_lorien_shield_c","Elven_Kite_Shield",[("lorien_kite_small",0)],itp_type_shield|itp_wooden_parry,itcf_carry_round_shield,500,weight(2)|hit_points(800)|body_armor(15)|spd_rtng(92)|difficulty(7)|weapon_length(70),imodbits_shield,],
["occc_lorien_round_shield","Elven_Round_Shield",[("lorien_round_shield",0)],itp_type_shield|itp_wooden_parry,itcf_carry_round_shield,400,weight(1)|hit_points(700)|body_armor(12)|spd_rtng(96)|difficulty(7)|weapon_length(50),imodbits_shield,],
# 
########LORIEN HELMS#######
["occc_lorien_helm_a","Elven_Archer_Helm",[("lorienhelmetarcherlow",0)],itp_type_head_armor,0,1300,weight(1)|head_armor(52)|difficulty(0),imodbits_armor],
["occc_lorien_helm_b","Elven_Archer_Helm",[("lorienhelmetarcherhigh",0)],itp_type_head_armor,0,1800,weight(1)|head_armor(57)|difficulty(0),imodbits_armor],
["occc_lorien_helm_c","Elven_Infantry_Helm",[("lorienhelmetinf",0)],itp_type_head_armor,0,1900,weight(1.2)|head_armor(59)|difficulty(0),imodbits_armor],




 ["items_end", "Items End", [("shield_round_a",0)], 0, 0, 1, 0, 0],

## NMCml NativeAdFix begin: scene fix
["nordic_sword", "{!}Nordic Sword", [("viking_sword",0),("scab_vikingsw", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 142 , weight(1.5)|difficulty(0)|spd_rtng(99) | weapon_length(98)|swing_damage(27 , cut) | thrust_damage(19 ,  pierce),imodbits_sword ],
["arming_sword", "{!}Arming Sword", [("b_long_sword",0),("scab_longsw_b", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 156 , weight(1.5)|difficulty(0)|spd_rtng(101) | weapon_length(100)|swing_damage(25 , cut) | thrust_damage(22 ,  pierce),imodbits_sword ],
["sword",         "{!}Sword", [("long_sword",0),("scab_longsw_a", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 148 , weight(1.5)|difficulty(0)|spd_rtng(100) | weapon_length(102)|swing_damage(26 , cut) | thrust_damage(23 ,  pierce),imodbits_sword ],
["broadsword",         "{!}Broadsword", [("broadsword",0),("scab_broadsword", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_scimitar|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 122 , weight(2.5)|difficulty(8)|spd_rtng(91) | weapon_length(101)|swing_damage(27 , cut) | thrust_damage(0 ,  pierce),imodbits_sword ],
["bastard_sword", "{!}Bastard Sword", [("bastard_sword",0),("scab_bastardsw", ixmesh_carry)], itp_type_two_handed_wpn| itp_primary, itc_bastardsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 279 , weight(2.25)|difficulty(9)|spd_rtng(102) | weapon_length(120)|swing_damage(33 , cut) | thrust_damage(27 ,  pierce),imodbits_sword ],
["double_axe",         "{!}Double Axe", [("dblhead_ax",0)], itp_type_two_handed_wpn| itp_two_handed|itp_primary|itp_bonus_against_shield|itp_wooden_parry, itc_nodachi|itcf_carry_axe_back, 359 , weight(6.5)|difficulty(12)|spd_rtng(85) | weapon_length(95)|swing_damage(43 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["one_handed_war_axe", "{!}One Handed War Axe", [("one_handed_war_axe_a",0),("one_handed_war_axe_b",imodbits_good)], itp_type_one_handed_wpn| itp_primary|itp_secondary|itp_bonus_against_shield, itc_scimitar|itcf_carry_axe_left_hip, 77 , weight(2.5)|difficulty(11)|spd_rtng(92) | weapon_length(90)|swing_damage(28 , cut) | thrust_damage(0 ,  pierce),imodbits_axe ],
["sword_medieval_a_long", "{!}Sword", [("sword_medieval_a_long",0),("sword_medieval_a_long_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn, 156 , weight(1.5)|difficulty(0)|spd_rtng(97) | weapon_length(105)|swing_damage(25 , cut) | thrust_damage(22 ,  pierce),imodbits_sword ],
["battle_shield", "{!}Battle Shield", [("shield_kite_d",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  196 , weight(3)|hit_points(560)|body_armor(1)|spd_rtng(78)|shield_width(94),imodbits_shield ],
["heater_shield", "{!}Heater Shield", [("shield_heater_a",0)], itp_type_shield|itp_wooden_parry, itcf_carry_kite_shield,  477 , weight(3.5)|hit_points(710)|body_armor(4)|spd_rtng(80)|shield_width(60),imodbits_shield ],
["nomad_shield", "{!}Nomad Shield", [("shield_wood_b",0)], itp_type_shield|itp_wooden_parry, itcf_carry_round_shield,  12 , weight(2)|hit_points(260)|body_armor(6)|spd_rtng(110)|shield_width(30),imodbits_shield ],
["shield_round_e", "{!}Round Shield", [("shield_round_e",0)], itp_type_shield , itcf_carry_round_shield,  12 , weight(2)|hit_points(260)|body_armor(6)|spd_rtng(110)|weapon_length(30),imodbits_shield ],
## NMCml NativeAdFix end
##INVASION MODE START
["javelin_bow",         "Javelin Bow", [("war_bow",0),("war_bow_carry",ixmesh_carry)],itp_type_bow|itp_primary|itp_two_handed ,itcf_shoot_bow|itcf_carry_bow_back, 
0 , weight(1.5)|difficulty(0)|spd_rtng(84) | shoot_speed(59) | thrust_damage(25 ,pierce), 0, [(ti_on_weapon_attack, [(play_sound,"snd_throw_javelin")])] ],
["knockdown_mace",         "Knockdown Mace", [("flanged_mace",0)], itp_type_one_handed_wpn|itp_can_knock_down| itp_primary|itp_wooden_parry, itc_scimitar|itcf_carry_mace_left_hip, 
0 , weight(3.5)|difficulty(0)|spd_rtng(103) | weapon_length(70)|swing_damage(24 , blunt) | thrust_damage(0 ,  pierce),imodbits_mace ],
["blood_drain_throwing_knives", "Blood Drain Throwing Knives", [("throwing_knife",0)], itp_type_thrown |itp_primary ,itcf_throw_knife, 0 , weight(2.5)|difficulty(0)|spd_rtng(121) | shoot_speed(25) | thrust_damage(25 ,  pierce)|max_ammo(5)|weapon_length(0),imodbits_thrown ],
["doom_javelins",         "Doom Javelins", [("jarid_new_b",0),("jarid_new_b_bag", ixmesh_carry)], itp_type_thrown |itp_primary ,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 
0 , weight(3)|difficulty(0)|spd_rtng(87) | shoot_speed(22) | thrust_damage(44 ,  pierce)|max_ammo(2)|weapon_length(65),imodbits_thrown ],
#["unblockable_morningstar",         "Unblockable Morningstar", [("mace_morningstar_new",0)], itp_crush_through|itp_type_two_handed_wpn|itp_primary|itp_wooden_parry|itp_unbalanced, itc_morningstar|itcf_carry_mace_left_hip, 
#305 , weight(20)|difficulty(13)|spd_rtng(95) | weapon_length(85)|swing_damage(38 , pierce) | thrust_damage(0 ,  pierce),imodbits_mace ],
["disarming_throwing_axe", "Disarming Throwing Axe", [("throwing_axe_a",0)], itp_type_thrown |itp_primary,itcf_throw_axe,
0, weight(1)|difficulty(0)|spd_rtng(98) | shoot_speed(18) | thrust_damage(10,cut)|max_ammo(1)|weapon_length(53),imodbits_thrown_minus_heavy ],
["instakill_knife",         "Instakill Knife", [("peasant_knife_new",0)], itp_type_one_handed_wpn|itp_primary|itp_secondary|itp_no_parry|itp_two_handed, itc_dagger|itcf_carry_dagger_front_left, 
0 , weight(0.5)|difficulty(0)|spd_rtng(101) | weapon_length(40)|swing_damage(21 , cut) | thrust_damage(13 ,  pierce),imodbits_sword ],
["backstabber", "Backstabber", [("sword_viking_a_small",0),("sword_viking_a_small_scabbard", ixmesh_carry)], itp_type_one_handed_wpn|itp_primary, itc_longsword|itcf_carry_sword_left_hip|itcf_show_holster_when_drawn,
0 , weight(1.25)|difficulty(0)|spd_rtng(103) | weapon_length(86)|swing_damage(20 , cut) | thrust_damage(13 ,  pierce),imodbits_sword_high ],
["weak_beserker_dart",         "Weak Beserker Dart", [("dart_b",0),("dart_b_bag", ixmesh_carry)], itp_type_thrown |itp_primary ,itcf_throw_javelin|itcf_carry_quiver_right_vertical|itcf_show_holster_when_drawn, 
0 , weight(4)|difficulty(0)|spd_rtng(95) | shoot_speed(28) | thrust_damage(5 ,  pierce)|max_ammo(1)|weapon_length(32),imodbits_thrown ],
["team_change_dart",         "Team Change Dart", [("dart_a",0),("dart_a_bag", ixmesh_carry)], itp_type_thrown |itp_primary ,itcf_throw_javelin|itcf_carry_quiver_back|itcf_show_holster_when_drawn, 
0 , weight(5)|difficulty(0)|spd_rtng(93) | shoot_speed(27) | thrust_damage(5 ,  pierce)|max_ammo(1)|weapon_length(45),imodbits_thrown ],
["awesome_spear",         "Awesome Spear", [("spear",0)], itp_type_polearm| itp_primary|itp_penalty_with_shield|itp_wooden_parry,itc_staff|itcf_carry_spear, 
0 , weight(1.5)|difficulty(0)|spd_rtng(110) | weapon_length(157)|swing_damage(41 , cut) | thrust_damage(33 ,  pierce),imodbits_polearm ],


["running_boots",  "Running Boots", [("samurai_boots",0)], itp_type_foot_armor | itp_attach_armature,0, 0 , weight(1)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(21)|difficulty(0) ,imodbits_cloth ],
["power_gloves","Power Gloves", [("scale_gauntlets_a_L",0)], itp_type_hand_armor,0, 0, weight(0.9)|abundance(100)|body_armor(6)|difficulty(0),imodbits_armor],
#["wielding_gloves","Wielding Gloves", [("scale_gauntlets_b_L",0)], itp_type_hand_armor,0, 0, weight(0.75)|abundance(100)|body_armor(5)|difficulty(0),imodbits_armor],
["invulnerable_helmet", "Invulnerable Helmet", [("maciejowski_helmet_new",0)], itp_type_head_armor|itp_covers_head,0, 1240 , weight(2.75)|abundance(100)|head_armor(63)|body_armor(0)|leg_armor(0)|difficulty(0) ,imodbits_plate ],
["kicking_boots", "Kicking Boots", [("sarranid_camel_boots",0)],  itp_type_foot_armor |itp_civilian | itp_attach_armature ,0,
 0 , weight(3)|abundance(100)|head_armor(0)|body_armor(0)|leg_armor(20)|difficulty(0) ,imodbits_plate ],
["restore_health_armour",  "Restore Health Armour", [("samurai_armor",0)], itp_type_body_armor  |itp_covers_legs ,0, 0 , weight(12)|abundance(100)|head_armor(0)|body_armor(27)|leg_armor(11)|difficulty(0) ,imodbits_armor ],
#["extra_life_helmet", "Extra Life Helmet", [("byzantion_helmet_a",0)], itp_type_head_armor   ,0, 0 , weight(2)|abundance(100)|head_armor(20)|body_armor(0)|leg_armor(0) ,imodbits_cloth ],
#["scatter_crossbow", "Scatter Crossbow", [("crossbow_c",0)], itp_type_crossbow |itp_primary|itp_two_handed|itp_cant_reload_on_horseback ,itcf_shoot_crossbow|itcf_carry_crossbow_back, 
#0 , weight(3.75)|spd_rtng(20) | shoot_speed(90) | thrust_damage(90 ,pierce)|max_ammo(1),imodbits_crossbow ],

#additional items for coop
["javelin_bow_ammo",         "Shooting Javelins", [("javelin_bow_ammo",0),("javelins_quiver_new", ixmesh_carry)], itp_type_arrows|itp_default_ammo ,itcf_carry_quiver_back, 
0, weight(4) | thrust_damage(34 ,  pierce)|max_ammo(15)|weapon_length(75),0 ],
#["scatter_bolts","Scatter Bolts", [("bolt",0),("flying_missile",ixmesh_flying_ammo),("bolt_bag", ixmesh_carry),("bolt_bag_b", ixmesh_carry|imodbit_large_bag)], itp_type_bolts|itp_merchandise|itp_default_ammo|itp_can_penetrate_shield, itcf_carry_quiver_right_vertical, 
#0,weight(2.25)|abundance(90)|weapon_length(63)|thrust_damage(1,pierce)|max_ammo(4),imodbits_missile],
["ccoop_new_items_end", "Items End", [("shield_round_a",0)], 0, 0, 1, 0, 0],
#INVASION MODE END

]
# modmerger_start version=201 type=2
try:
    component_name = "items"
    var_set = { "items" : items }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end

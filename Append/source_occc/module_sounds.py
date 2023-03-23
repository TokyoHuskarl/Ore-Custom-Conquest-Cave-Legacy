from header_sounds import *

sounds = [
 ("click", sf_2d|sf_vol_3,["click_01.ogg"]),
 ("tutorial_1", sf_2d|sf_vol_7,["tutorial_1.ogg"]),
 ("tutorial_2", sf_2d|sf_vol_7,["tutorial_2.ogg"]),
 ("gong", sf_2d|sf_priority_9|sf_vol_7, ["cymbal_01.ogg"]),
 ("quest_taken", sf_2d|sf_priority_9|sf_vol_10, ["get_quest_01.ogg"]),
 ("quest_completed", sf_2d|sf_priority_9|sf_vol_8, ["quest_completed.ogg"]),
 ("quest_succeeded", sf_2d|sf_priority_9|sf_vol_7, ["quest_succeeded.ogg"]),
 ("quest_concluded", sf_2d|sf_priority_9|sf_vol_7, ["quest_concluded.ogg"]),
 ("quest_failed", sf_2d|sf_priority_9|sf_vol_7, ["quest_failed.ogg"]),
 ("quest_cancelled", sf_2d|sf_priority_9|sf_vol_7, ["quest_cancelled.ogg"]),
 ("rain",sf_2d|sf_priority_10|sf_vol_4|sf_looping, ["rain_1.ogg"]),
 ("money_received",sf_2d|sf_priority_10|sf_vol_4, ["coins_dropped_1.ogg"]),
 ("money_paid",sf_2d|sf_priority_10|sf_vol_10, ["coins_dropped_2.ogg"]),
 ("sword_clash_1", sf_priority_5|sf_vol_8,["sword_clank_metal_09.ogg","sword_clank_metal_09b.ogg","sword_clank_metal_10.ogg","sword_clank_metal_10b.ogg","sword_clank_metal_12.ogg","sword_clank_metal_12b.ogg","sword_clank_metal_13.ogg","sword_clank_metal_13b.ogg"]),
 ("sword_clash_2", sf_priority_5|sf_vol_9,["s_swordClash2.wav"]),
 ("sword_clash_3", sf_priority_5|sf_vol_9,["s_swordClash3.wav"]),
 ("sword_swing", sf_vol_8|sf_priority_2,["weapon_swing_01.ogg","weapon_swing_02.ogg","weapon_swing_03.ogg","weapon_swing_04.ogg","weapon_swing_05.ogg"]),
 ("footstep_grass", sf_vol_4|sf_priority_1,["footstep_grass_light_01.ogg","footstep_grass_light_02.ogg","footstep_grass_light_03.ogg","footstep_grass_light_04.ogg","footstep_grass_light_05.ogg","footstep_grass_light_06.ogg","footstep_grass_light_07.ogg","footstep_grass_light_08.ogg","footstep_grass_light_09.ogg","footstep_grass_light_10.ogg","footstep_grass_light_11.ogg","footstep_grass_light_12.ogg","footstep_grass_light_13.ogg","footstep_grass_light_14.ogg","footstep_grass_light_15.ogg"]),
 ("footstep_wood", sf_vol_6|sf_priority_1,["footstep_wood_light_01.ogg","footstep_wood_light_02.ogg","footstep_wood_light_03.ogg","footstep_wood_light_04.ogg","footstep_wood_light_05.ogg","footstep_wood_light_06.ogg","footstep_wood_light_07.ogg","footstep_wood_light_08.ogg","footstep_wood_light_09.ogg","footstep_wood_light_10.ogg"]),
# ("footstep_wood", sf_vol_3|sf_priority_1,["footstep_stone_1.ogg","footstep_stone_3.ogg","footstep_stone_4.ogg"]),
 ("footstep_water", sf_vol_7|sf_priority_3,["footstep_water_01.ogg","footstep_water_02.ogg","footstep_water_03.ogg","footstep_water_04.ogg","footstep_water_05.ogg","footstep_water_06.ogg","footstep_water_07.ogg","footstep_water_08.ogg","footstep_water_09.ogg","footstep_water_10.ogg"]),
 ("footstep_horse",sf_priority_3|sf_vol_8, ["footstep_horse_5.ogg","footstep_horse_2.ogg","footstep_horse_3.ogg","footstep_horse_4.ogg"]),
# ("footstep_horse",0, ["s_footstep_horse_4b.wav","s_footstep_horse_4f.wav","s_footstep_horse_5b.wav","s_footstep_horse_5f.wav"]),
 ("footstep_horse_1b",sf_priority_3|sf_vol_8, ["s_footstep_horse_4b.wav","s_footstep_horse_4f.wav","s_footstep_horse_5b.wav","s_footstep_horse_5f.wav"]),
 ("footstep_horse_1f",sf_priority_3|sf_vol_8, ["s_footstep_horse_2b.wav","s_footstep_horse_2f.wav","s_footstep_horse_3b.wav","s_footstep_horse_3f.wav"]),
# ("footstep_horse_1f",sf_priority_3|sf_vol_8, ["footstep_horse_5.ogg","footstep_horse_2.ogg","footstep_horse_3.ogg","footstep_horse_4.ogg"]),
 ("footstep_horse_2b",sf_priority_3|sf_vol_8, ["s_footstep_horse_2b.wav"]),
 ("footstep_horse_2f",sf_priority_3|sf_vol_8, ["s_footstep_horse_2f.wav"]),
 ("footstep_horse_3b",sf_priority_3|sf_vol_8, ["s_footstep_horse_3b.wav"]),
 ("footstep_horse_3f",sf_priority_3|sf_vol_8, ["s_footstep_horse_3f.wav"]),
 ("footstep_horse_4b",sf_priority_3|sf_vol_8, ["s_footstep_horse_4b.wav"]),
 ("footstep_horse_4f",sf_priority_3|sf_vol_8, ["s_footstep_horse_4f.wav"]),
 ("footstep_horse_5b",sf_priority_3|sf_vol_8, ["s_footstep_horse_5b.wav"]),
 ("footstep_horse_5f",sf_priority_3|sf_vol_8, ["s_footstep_horse_5f.wav"]),
 ("jump_begin", sf_vol_6|sf_priority_9,["jump_light_b_01.ogg","jump_light_b_02.ogg","jump_light_b_03.ogg"]),
 ("jump_end", sf_vol_5|sf_priority_9,["jump_light_e_01.ogg","jump_light_e_02.ogg"]),
 ("jump_begin_water", sf_vol_9|sf_priority_9,["water_jump_01.ogg","water_jump_02.ogg","water_jump_03.ogg"]),
 ("jump_end_water", sf_vol_8|sf_priority_9,["water_splash_01.ogg","water_splash_02.ogg","water_splash_03.ogg","water_splash_04.ogg","water_splash_05.ogg"]),
 ("horse_jump_begin", sf_vol_10|sf_priority_9,["horse_jump_b_01.ogg","horse_jump_b_02.ogg"]),
 ("horse_jump_end", sf_vol_10|sf_priority_9,["horse_jump_e_01.ogg","horse_jump_e_02.ogg"]),
 ("horse_jump_begin_water", sf_vol_10|sf_priority_9,["water_jump_large_01.ogg","water_jump_large_02.ogg","water_jump_large_03.ogg"]),
 ("horse_jump_end_water", sf_vol_10|sf_priority_9,["water_splash_large_01.ogg","water_splash_large_02.ogg","water_splash_large_03.ogg","water_splash_large_04.ogg","water_splash_large_05.ogg"]),

 ("release_bow",sf_vol_8, ["bow_shoot_01.ogg","bow_shoot_02.ogg","bow_shoot_03.ogg","bow_shoot_04.ogg","bow_shoot_05.ogg","bow_shoot_06.ogg","bow_shoot_07.ogg","bow_shoot_08.ogg","bow_shoot_09.ogg","bow_shoot_10.ogg"]),
 ("release_crossbow",sf_vol_7, ["crossbow_shoot_01.ogg","crossbow_shoot_02.ogg","crossbow_shoot_03.ogg","crossbow_shoot_04.ogg","crossbow_shoot_05.ogg","crossbow_shoot_06.ogg"]),
 ("throw_javelin",sf_vol_5, ["throw_javelin_2.ogg","throw_javelin_01.ogg","throw_javelin_02.ogg","throw_javelin_03.ogg"]),
 ("throw_axe",sf_vol_7, ["throw_axe_1.ogg"]),
 ("throw_knife",sf_vol_5, ["throw_knife_01.ogg","throw_knife_02.ogg","throw_knife_03.ogg","throw_knife_04.ogg"]),
 ("throw_stone",sf_vol_5, ["throw_stone_01.ogg","throw_stone_02.ogg","throw_stone_03.ogg"]),

 ("reload_crossbow",sf_vol_3, ["pull_crossbow_string_01.ogg","pull_crossbow_string_02.ogg","pull_crossbow_string_03.ogg","pull_crossbow_string_04.ogg","pull_crossbow_string_05.ogg"]),
 ("reload_crossbow_continue",sf_vol_6, ["put_back_dagger.ogg"]),
 ("pull_bow",sf_vol_6, ["pull_bow_string_01.ogg","pull_bow_string_02.ogg","pull_bow_string_03.ogg","pull_bow_string_04.ogg","pull_bow_string_05.ogg"]),
 ("pull_arrow",sf_vol_5, ["draw_arrow_01.ogg","draw_arrow_02.ogg","draw_arrow_03.ogg"]),

 ("arrow_pass_by",sf_priority_7, ["arrow_pass_01.ogg","arrow_pass_02.ogg","arrow_pass_03.ogg","arrow_pass_04.ogg","arrow_pass_05.ogg","arrow_pass_06.ogg","arrow_pass_07.ogg","arrow_pass_08.ogg","arrow_pass_09.ogg","arrow_pass_10.ogg"]),
 ("bolt_pass_by",sf_priority_7, ["bolt_pass_01.ogg","bolt_pass_02.ogg","bolt_pass_03.ogg","bolt_pass_04.ogg","bolt_pass_05.ogg","bolt_pass_06.ogg","bolt_pass_07.ogg","bolt_pass_08.ogg"]),
 ("javelin_pass_by",sf_priority_7, ["javelin_pass_by_1.ogg","javelin_pass_by_2.ogg"]),
 ("stone_pass_by",sf_vol_9|sf_priority_7, ["stone_pass_01.ogg","stone_pass_02.ogg","stone_pass_03.ogg"]),
 ("axe_pass_by",sf_priority_7, ["axe_pass_by_1.ogg"]),
 ("knife_pass_by",sf_priority_7, ["knife_pass_01.ogg","knife_pass_02.ogg","knife_pass_03.ogg","knife_pass_04.ogg"]),
 ("bullet_pass_by",sf_priority_7, ["bullet_pass_01.ogg","bullet_pass_02.ogg","bullet_pass_03.ogg","bullet_pass_04.ogg","bullet_pass_05.ogg","bullet_pass_06.ogg","bullet_pass_07.ogg","bullet_pass_08.ogg","bullet_pass_09.ogg","bullet_pass_10.ogg","bullet_pass_11.ogg","bullet_pass_12.ogg"]),
 
 ("incoming_arrow_hit_ground",sf_priority_7|sf_vol_7, ["arrow_ground_01.ogg","arrow_ground_02.ogg","arrow_ground_03.ogg","arrow_ground_04.ogg","arrow_ground_05.ogg","arrow_ground_06.ogg","arrow_ground_07.ogg","arrow_ground_08.ogg"]),
 ("incoming_bolt_hit_ground",sf_priority_7|sf_vol_7, ["bolt_ground_01.ogg","bolt_ground_02.ogg","bolt_ground_03.ogg","bolt_ground_04.ogg","bolt_ground_05.ogg","bolt_ground_06.ogg","bolt_ground_07.ogg","bolt_ground_08.ogg"]),
 ("incoming_javelin_hit_ground",sf_priority_7|sf_vol_7, ["javelin_ground_01.ogg","javelin_ground_02.ogg","javelin_ground_03.ogg"]),
 ("incoming_stone_hit_ground",sf_priority_7|sf_vol_7, ["stone_ground_01.ogg","stone_ground_02.ogg","stone_ground_03.ogg"]),
 ("incoming_axe_hit_ground",sf_priority_7|sf_vol_7, ["axe_ground_01.ogg","axe_ground_02.ogg","axe_ground_03.ogg"]),
 ("incoming_knife_hit_ground",sf_priority_7|sf_vol_7, ["knife_ground_01.ogg","knife_ground_02.ogg","knife_ground_03.ogg"]),
 ("incoming_bullet_hit_ground",sf_priority_7|sf_vol_7, ["bullet_ric_01.ogg","bullet_ric_02.ogg","bullet_ric_03.ogg","bullet_ric_04.ogg","bullet_ric_05.ogg","bullet_ric_06.ogg","bullet_ric_07.ogg","bullet_ric_08.ogg"]),

 ("outgoing_arrow_hit_ground",sf_priority_7|sf_vol_7, ["arrow_ground_01.ogg","arrow_ground_02.ogg","arrow_ground_03.ogg","arrow_ground_04.ogg","arrow_ground_05.ogg","arrow_ground_06.ogg","arrow_ground_07.ogg","arrow_ground_08.ogg"]),
 ("outgoing_bolt_hit_ground",sf_priority_7|sf_vol_7,  ["bolt_ground_01.ogg","bolt_ground_02.ogg","bolt_ground_03.ogg","bolt_ground_04.ogg","bolt_ground_05.ogg","bolt_ground_06.ogg","bolt_ground_07.ogg","bolt_ground_08.ogg"]),
 ("outgoing_javelin_hit_ground",sf_priority_7|sf_vol_10, ["javelin_ground_01.ogg","javelin_ground_02.ogg","javelin_ground_03.ogg"]),
 ("outgoing_stone_hit_ground",sf_priority_7|sf_vol_7, ["stone_ground_01.ogg","stone_ground_02.ogg","stone_ground_03.ogg"]),
 ("outgoing_axe_hit_ground",sf_priority_7|sf_vol_7, ["axe_ground_01.ogg","axe_ground_02.ogg","axe_ground_03.ogg"]),
 ("outgoing_knife_hit_ground",sf_priority_7|sf_vol_7, ["knife_ground_01.ogg","knife_ground_02.ogg","knife_ground_03.ogg"]),
 ("outgoing_bullet_hit_ground",sf_priority_7|sf_vol_7, ["bullet_ric_01.ogg","bullet_ric_02.ogg","bullet_ric_03.ogg","bullet_ric_04.ogg","bullet_ric_05.ogg","bullet_ric_06.ogg","bullet_ric_07.ogg","bullet_ric_08.ogg"]),


 ("draw_sword",sf_priority_2|sf_vol_4, ["draw_sword_02.ogg","draw_sword_03.ogg"]),
 ("put_back_sword",sf_priority_1|sf_vol_4, ["put_away_sword_01.ogg"]),
 ("draw_greatsword",sf_priority_2|sf_vol_4, ["draw_greatsword_01.ogg","draw_greatsword_03.ogg"]),
 ("put_back_greatsword",sf_priority_1|sf_vol_4, ["put_away_greatsword_01.ogg"]),
 ("draw_axe",sf_priority_2|sf_vol_4, ["draw_axe_01.ogg","draw_axe_02.ogg"]),
 ("put_back_axe",sf_priority_1|sf_vol_4, ["put_away_axe_01.ogg"]),
 ("draw_greataxe",sf_priority_2|sf_vol_4, ["draw_greataxe_01.ogg","draw_greataxe_02.ogg"]),
 ("put_back_greataxe",sf_priority_1|sf_vol_4, ["put_away_greataxe_01.ogg"]),
 ("draw_spear",sf_priority_2|sf_vol_4, ["draw_spear_01.ogg","draw_spear_02.ogg"]),
 ("put_back_spear",sf_priority_1|sf_vol_4, ["put_away_spear_01.ogg"]),
 ("draw_crossbow",sf_priority_2|sf_vol_6, ["draw_crossbow_01.ogg","draw_crossbow_02.ogg"]),
 ("put_back_crossbow",sf_priority_1|sf_vol_4, ["put_away_crossbow_01.ogg"]),
 ("draw_revolver",sf_priority_2|sf_vol_4, ["draw_from_holster.ogg"]),
 ("put_back_revolver",sf_priority_2|sf_vol_4, ["put_back_to_holster.ogg"]),
 ("draw_dagger",sf_priority_2|sf_vol_4, ["draw_dagger_01.ogg","draw_dagger_02.ogg"]),
 ("put_back_dagger",sf_priority_1|sf_vol_4, ["put_away_dagger_01.ogg"]),
 ("draw_bow",sf_priority_2|sf_vol_4, ["draw_bow_01.ogg","draw_bow_02.ogg"]),
 ("put_back_bow",sf_priority_1|sf_vol_4, ["put_away_bow_01.ogg"]),
 ("draw_shield",sf_priority_2|sf_vol_4, ["draw_shield_01.ogg","draw_shield_02.ogg"]),
 ("put_back_shield",sf_priority_1|sf_vol_7, ["put_away_shield_01.ogg"]),
 ("draw_other",sf_priority_2|sf_vol_4, ["draw_other.ogg"]),
 ("put_back_other",sf_priority_1|sf_vol_4, ["draw_other2.ogg"]),

 ("body_fall_small",sf_priority_5|sf_vol_9, ["body_fall_small_01.ogg","body_fall_small_02.ogg","body_fall_small_03.ogg","body_fall_small_04.ogg","body_fall_small_05.ogg","body_fall_small_06.ogg","body_fall_small_07.ogg","body_fall_small_08.ogg"]),
 ("body_fall_big",sf_priority_6|sf_vol_10, ["body_fall_large_01.ogg","body_fall_large_02.ogg","body_fall_large_03.ogg","body_fall_large_04.ogg","body_fall_large_05.ogg","body_fall_large_06.ogg","body_fall_large_07.ogg","body_fall_large_08.ogg"]),
# ("body_fall_very_big",sf_priority_9|sf_vol_10, ["body_fall_very_big_1.ogg"]),
 ("horse_body_fall_begin",sf_priority_7|sf_vol_10, ["horse_fall_b_01.ogg","horse_fall_b_02.ogg","horse_fall_b_03.ogg"]),
 ("horse_body_fall_end",sf_priority_7|sf_vol_10, ["horse_fall_e_01.ogg","horse_fall_e_02.ogg","horse_fall_e_03.ogg"]),
 
## ("clang_metal",sf_priority_9, ["clang_metal_1.ogg","clang_metal_2.ogg","s_swordClash1.wav","s_swordClash2.wav","s_swordClash3.wav"]),
 ("hit_wood_wood",sf_priority_7|sf_vol_10, ["wood_on_wood_01.ogg","wood_on_wood_02.ogg","wood_on_wood_03.ogg","wood_on_wood_04.ogg","wood_on_wood_05.ogg","wood_on_wood_06.ogg","wood_on_wood_07.ogg","wood_on_wood_08.ogg"]),#dummy
 ("hit_metal_metal",sf_priority_7|sf_vol_10, ["Sword_clash_01.ogg","Sword_clash_02.ogg","Sword_clash_03.ogg","Sword_clash_04.ogg","Sword_clash_05.ogg","Sword_clash_06.ogg","Sword_clash_07.ogg","Sword_clash_08.ogg","Sword_clash_09.ogg","Sword_clash_10.ogg","Sword_clash_11.ogg","Sword_clash_12.ogg","Sword_clash_13.ogg","Sword_clash_14.ogg","Sword_clash_15.ogg","Sword_clash_16.ogg","Sword_clash_17.ogg","Sword_clash_18.ogg","Sword_clash_19.ogg","Sword_clash_20.ogg","Sword_clash_21.ogg","Sword_clash_22.ogg","Sword_clash_23.ogg","Sword_clash_24.ogg","Sword_clash_25.ogg","Sword_clash_26.ogg","Sword_clash_27.ogg"]),
 ("hit_wood_metal",sf_priority_7|sf_vol_10, ["metal_on_wood_01.ogg","metal_on_wood_02.ogg","metal_on_wood_03.ogg","metal_on_wood_04.ogg","metal_on_wood_05.ogg","metal_on_wood_06.ogg","metal_on_wood_07.ogg","metal_on_wood_08.ogg","metal_on_wood_09.ogg","metal_on_wood_10.ogg"]),
# ("clang_metal", sf_priority_9,["sword_clank_metal_09.ogg","sword_clank_metal_10.ogg","sword_clank_metal_12.ogg","sword_clank_metal_13.ogg"]),
## ("shield_hit_cut",sf_priority_5, ["shield_hit_cut_3.ogg","shield_hit_cut_4.ogg","shield_hit_cut_5.ogg"]),
 ("shield_hit_wood_wood",sf_priority_7|sf_vol_10, ["shield_wood_wood_01.ogg","shield_wood_wood_02.ogg","shield_wood_wood_03.ogg","shield_wood_wood_04.ogg","shield_wood_wood_05.ogg","shield_wood_wood_06.ogg","shield_wood_wood_07.ogg","shield_wood_wood_08.ogg","shield_wood_wood_09.ogg","shield_wood_wood_10.ogg","shield_wood_wood_11.ogg","shield_wood_wood_12.ogg"]),
 ("shield_hit_metal_metal",sf_priority_7|sf_vol_10, ["shield_metal_metal_01.ogg","shield_metal_metal_02.ogg","shield_metal_metal_03.ogg","shield_metal_metal_04.ogg","shield_metal_metal_05.ogg","shield_metal_metal_06.ogg","shield_metal_metal_07.ogg","shield_metal_metal_08.ogg","shield_metal_metal_09.ogg","shield_metal_metal_10.ogg","shield_metal_metal_11.ogg","shield_metal_metal_12.ogg"]),
 ("shield_hit_wood_metal",sf_priority_7|sf_vol_10, ["shield_metal_wood_01.ogg","shield_metal_wood_02.ogg","shield_metal_wood_03.ogg","shield_metal_wood_04.ogg","shield_metal_wood_05.ogg","shield_metal_wood_06.ogg","shield_metal_wood_07.ogg","shield_metal_wood_08.ogg","shield_metal_wood_09.ogg","shield_metal_wood_10.ogg"]), #(shield is wood)
 ("shield_hit_metal_wood",sf_priority_7|sf_vol_10, ["shield_wood_metal_01.ogg","shield_wood_metal_02.ogg","shield_wood_metal_03.ogg","shield_wood_metal_04.ogg","shield_wood_metal_05.ogg","shield_wood_metal_06.ogg","shield_wood_metal_07.ogg","shield_wood_metal_08.ogg"]),#(shield is metal)
 ("shield_broken",sf_priority_9, ["shield_break_01.ogg","shield_break_02.ogg"]),
 ("man_hit",sf_priority_2|sf_vol_10, ["man_grunt_pain_01.ogg","man_grunt_pain_02.ogg","man_grunt_pain_03.ogg","man_grunt_pain_04.ogg","man_grunt_pain_05.ogg","man_grunt_pain_06.ogg","man_grunt_pain_07.ogg","man_grunt_pain_08.ogg","man_grunt_pain_09.ogg","man_grunt_pain_10.ogg","man_grunt_pain_11.ogg","man_grunt_pain_12.ogg","man_grunt_pain_13.ogg","man_grunt_pain_14.ogg","man_grunt_pain_15.ogg","man_grunt_pain_16.ogg","man_grunt_pain_17.ogg","man_grunt_pain_18.ogg","man_grunt_pain_19.ogg","man_grunt_pain_20.ogg"]),
 ("man_die",sf_priority_10|sf_vol_10,  ["man_death_1.ogg","man_death_8.ogg","man_death_8b.ogg","man_death_11.ogg","man_death_14.ogg","man_death_16.ogg","man_death_18.ogg","man_death_21.ogg","man_death_22.ogg","man_death_29.ogg","man_death_40.ogg","man_death_44.ogg","man_death_46.ogg","man_death_48.ogg","man_death_64.ogg","man_die_03.ogg","man_die_04.ogg","man_die_05.ogg","man_die_06.ogg","man_die_08.ogg","man_die_09.ogg","man_die_10.ogg","man_die_11.ogg","man_die_14.ogg","man_die_15.ogg","man_die_17.ogg","man_die_18.ogg","man_die_20.ogg","man_die_24.ogg","man_die_27.ogg","man_die_29.ogg","man_die_30.ogg"]),
 ("woman_hit",sf_priority_3, ["woman_hit_2.ogg","woman_hit_3.ogg","woman_hit_b_2.ogg","woman_hit_b_4.ogg","woman_hit_b_6.ogg","woman_hit_b_7.ogg","woman_hit_b_8.ogg","woman_hit_b_11.ogg","woman_hit_b_14.ogg","woman_hit_b_16.ogg"]),
 ("woman_die",sf_priority_10, ["woman_fall_1.ogg","woman_hit_b_5.ogg"]),
 ("woman_yell",sf_priority_10|sf_vol_10, ["woman_yell_1.ogg","woman_yell_2.ogg"]),
 ("hide",0, ["s_hide.wav"]),
 ("unhide",0, ["s_unhide.wav"]),
 ("neigh",0, ["horse_exterior_whinny_01.ogg","horse_exterior_whinny_02.ogg","horse_exterior_whinny_03.ogg","horse_exterior_whinny_04.ogg","horse_exterior_whinny_05.ogg","horse_whinny.ogg"]),
 ("gallop",sf_vol_4, ["horse_gallop_3.ogg","horse_gallop_4.ogg","horse_gallop_5.ogg"]),
 ("battle",sf_vol_4, ["battle.ogg"]),
# ("bow_shoot_player",sf_priority_10|sf_vol_10, ["bow_shoot_4.ogg"]),
# ("bow_shoot",sf_priority_4, ["bow_shoot_4.ogg"]),
# ("crossbow_shoot",sf_priority_4, ["bow_shoot_2.ogg"]),
 ("arrow_hit_body",sf_priority_4, ["missile_flesh_01.ogg","missile_flesh_02.ogg","missile_flesh_03.ogg","missile_flesh_04.ogg","missile_flesh_05.ogg","missile_flesh_06.ogg","missile_flesh_07.ogg","missile_flesh_08.ogg"]),
 ("metal_hit_low_armor_low_damage",sf_priority_5|sf_vol_9, ["metal_low_low_01.ogg","metal_low_low_02.ogg","metal_low_low_03.ogg","metal_low_low_04.ogg","metal_low_low_05.ogg","metal_low_low_06.ogg","metal_low_low_07.ogg","metal_low_low_08.ogg"]),
 ("metal_hit_low_armor_high_damage",sf_priority_5|sf_vol_9, ["metal_low_high_01.ogg","metal_low_high_02.ogg","metal_low_high_03.ogg","metal_low_high_04.ogg","metal_low_high_05.ogg","metal_low_high_06.ogg","metal_low_high_07.ogg","metal_low_high_08.ogg","metal_low_high_09.ogg","metal_low_high_10.ogg","metal_low_high_11.ogg","metal_low_high_12.ogg","metal_low_high_13.ogg","metal_low_high_14.ogg","metal_low_high_15.ogg","metal_low_high_16.ogg","metal_low_high_17.ogg","metal_low_high_18.ogg","metal_low_high_19.ogg","metal_low_high_20.ogg","metal_low_high_21.ogg","metal_low_high_22.ogg","metal_low_high_23.ogg","metal_low_high_24.ogg","metal_low_high_25.ogg","metal_low_high_26.ogg","metal_low_high_27.ogg"]),
 ("metal_hit_high_armor_low_damage",sf_priority_5|sf_vol_9, ["metal_high_low_01.ogg","metal_high_low_02.ogg","metal_high_low_03.ogg","metal_high_low_04.ogg","metal_high_low_05.ogg","metal_high_low_06.ogg","metal_high_low_07.ogg","metal_high_low_08.ogg","metal_high_low_09.ogg","metal_high_low_10.ogg","metal_high_low_11.ogg","metal_high_low_12.ogg","metal_high_low_13.ogg","metal_high_low_14.ogg","metal_high_low_15.ogg","metal_high_low_16.ogg","metal_high_low_17.ogg","metal_high_low_18.ogg","metal_high_low_19.ogg","metal_high_low_20.ogg","metal_high_low_21.ogg","metal_high_low_22.ogg","metal_high_low_23.ogg","metal_high_low_24.ogg","metal_high_low_25.ogg"]),
 ("metal_hit_high_armor_high_damage",sf_priority_5|sf_vol_9, ["metal_high_high_01.ogg","metal_high_high_02.ogg","metal_high_high_03.ogg","metal_high_high_04.ogg","metal_high_high_05.ogg","metal_high_high_06.ogg","metal_high_high_07.ogg","metal_high_high_08.ogg","metal_high_high_09.ogg","metal_high_high_10.ogg","metal_high_high_11.ogg","metal_high_high_12.ogg","metal_high_high_13.ogg","metal_high_high_14.ogg","metal_high_high_15.ogg","metal_high_high_16.ogg","metal_high_high_17.ogg","metal_high_high_18.ogg","metal_high_high_19.ogg","metal_high_high_20.ogg","metal_high_high_21.ogg","metal_high_high_22.ogg","metal_high_high_23.ogg","metal_high_high_24.ogg","metal_high_high_25.ogg","metal_high_high_26.ogg","metal_high_high_27.ogg","metal_high_high_28.ogg","metal_high_high_29.ogg","metal_high_high_30.ogg","metal_high_high_31.ogg","metal_high_high_32.ogg"]),
 ("wooden_hit_low_armor_low_damage",sf_priority_5|sf_vol_9, ["blunt_low_low_01.ogg","blunt_low_low_02.ogg","blunt_low_low_03.ogg","blunt_low_low_04.ogg","blunt_low_low_05.ogg","blunt_low_low_06.ogg","blunt_low_low_07.ogg","blunt_low_low_08.ogg","blunt_low_low_09.ogg","blunt_low_low_10.ogg"]),
 ("wooden_hit_low_armor_high_damage",sf_priority_5|sf_vol_9, ["blunt_low_high_01.ogg","blunt_low_high_02.ogg","blunt_low_high_03.ogg","blunt_low_high_04.ogg","blunt_low_high_05.ogg","blunt_low_high_06.ogg","blunt_low_high_07.ogg","blunt_low_high_08.ogg","blunt_low_high_09.ogg","blunt_low_high_10.ogg","blunt_low_high_11.ogg","blunt_low_high_12.ogg","blunt_low_high_13.ogg"]),
 ("wooden_hit_high_armor_low_damage",sf_priority_5|sf_vol_9, ["blunt_high_low_01.ogg","blunt_high_low_02.ogg","blunt_high_low_03.ogg","blunt_high_low_04.ogg","blunt_high_low_05.ogg","blunt_high_low_06.ogg","blunt_high_low_07.ogg","blunt_high_low_08.ogg","blunt_high_low_09.ogg","blunt_high_low_10.ogg"]),
 ("wooden_hit_high_armor_high_damage",sf_priority_5|sf_vol_9, ["blunt_high_high_01.ogg","blunt_high_high_02.ogg","blunt_high_high_03.ogg","blunt_high_high_04.ogg","blunt_high_high_05.ogg","blunt_high_high_06.ogg","blunt_high_high_07.ogg","blunt_high_high_08.ogg","blunt_high_high_09.ogg","blunt_high_high_10.ogg","blunt_high_high_11.ogg","blunt_high_high_12.ogg","blunt_high_high_13.ogg","blunt_high_high_14.ogg","blunt_high_high_15.ogg","blunt_high_high_16.ogg","blunt_high_high_17.ogg","blunt_high_high_18.ogg","blunt_high_high_19.ogg","blunt_high_high_20.ogg","blunt_high_high_21.ogg","blunt_high_high_22.ogg"]),
 ("mp_arrow_hit_target",sf_2d|sf_priority_15|sf_vol_9, ["mp_arrow_hit_target.ogg"]),
 ("blunt_hit",sf_priority_5|sf_vol_10, ["horse_charge_01.ogg","horse_charge_02.ogg","horse_charge_03.ogg","horse_charge_04.ogg","horse_charge_05.ogg","horse_charge_06.ogg","horse_charge_07.ogg","horse_charge_08.ogg"]),
 ("player_hit_by_arrow",sf_priority_10|sf_vol_10, ["player_hit_by_arrow.ogg"]),
 ("pistol_shot",sf_priority_10|sf_vol_10, ["gun_shoot_01.ogg","gun_shoot_02.ogg","gun_shoot_03.ogg","gun_shoot_04.ogg","gun_shoot_05.ogg","gun_shoot_06.ogg","gun_shoot_07.ogg","gun_shoot_08.ogg","gun_shoot_09.ogg","gun_shoot_10.ogg","gun_shoot_11.ogg"]),
 ("man_grunt",sf_priority_3|sf_vol_4, ["man_heavy_grunt_01.ogg","man_heavy_grunt_02.ogg","man_heavy_grunt_03.ogg","man_heavy_grunt_04.ogg","man_heavy_grunt_05.ogg","man_heavy_grunt_06.ogg","man_heavy_grunt_07.ogg","man_heavy_grunt_08.ogg","man_heavy_grunt_09.ogg","man_heavy_grunt_10.ogg","man_heavy_grunt_11.ogg","man_heavy_grunt_12.ogg","man_heavy_grunt_13.ogg","man_heavy_grunt_14.ogg","man_heavy_grunt_15.ogg"]),
 ("man_breath_hard",sf_priority_3|sf_vol_8, ["man_heavy_grunt_01.ogg","man_heavy_grunt_02.ogg","man_heavy_grunt_03.ogg","man_heavy_grunt_04.ogg","man_heavy_grunt_05.ogg","man_heavy_grunt_06.ogg","man_heavy_grunt_07.ogg","man_heavy_grunt_08.ogg","man_heavy_grunt_09.ogg","man_heavy_grunt_10.ogg","man_heavy_grunt_11.ogg","man_heavy_grunt_12.ogg","man_heavy_grunt_13.ogg","man_heavy_grunt_14.ogg","man_heavy_grunt_15.ogg"]),
 ("man_stun",sf_priority_3|sf_vol_9, ["man_short_grunt_01.ogg","man_short_grunt_02.ogg"]),
 ("man_grunt_long",sf_priority_3|sf_vol_8, ["man_heavy_grunt_01.ogg","man_heavy_grunt_02.ogg","man_heavy_grunt_03.ogg","man_heavy_grunt_04.ogg","man_heavy_grunt_05.ogg","man_heavy_grunt_06.ogg","man_heavy_grunt_07.ogg","man_heavy_grunt_08.ogg","man_heavy_grunt_09.ogg","man_heavy_grunt_10.ogg","man_heavy_grunt_11.ogg","man_heavy_grunt_12.ogg","man_heavy_grunt_13.ogg","man_heavy_grunt_14.ogg","man_heavy_grunt_15.ogg"]),
 ("man_yell",sf_priority_3|sf_vol_7, ["man_yell_4.ogg","man_yell_7.ogg","man_yell_9.ogg","man_yell_11.ogg","man_yell_13.ogg","man_yell_15.ogg","man_yell_16.ogg","man_yell_17.ogg","man_yell_20.ogg","man_shortyell_4.ogg","man_shortyell_5.ogg","man_shortyell_6.ogg","man_shortyell_9.ogg","man_shortyell_11.ogg","man_shortyell_11b.ogg","man_yell_b_18.ogg","man_yell_b_21.ogg","man_yell_b_22.ogg","man_yell_b_23.ogg","man_yell_c_20.ogg","man_yell_01.ogg","man_yell_02.ogg","man_yell_03.ogg","man_yell_04.ogg","man_yell_05.ogg","man_yell_06.ogg","man_yell_07.ogg","man_yell_08.ogg","man_yell_09.ogg","man_yell_10.ogg","man_yell_11b.ogg","man_yell_12.ogg"]),
## not adequate, removed: "man_yell_b_21.ogg","man_yell_b_22.ogg","man_yell_b_23.ogg"]),
#TODONOW:
 ("man_warcry",sf_priority_5, ["man_insult_2.ogg","man_insult_3.ogg","man_insult_7.ogg","man_insult_9.ogg","man_insult_13.ogg","man_insult_15.ogg","man_insult_16.ogg","man_insult_nv16.ogg","man_insult_nv16_3.ogg","man_insult_nv17.ogg","man_insult_nv18.ogg","man_insult_nv19.ogg","man_insult_nv20.ogg","man_insult_nv21.ogg","man_insult_nv22.ogg","man_insult_nv23.ogg","man_insult_nv24.ogg"]),  ## CC-D add man_insult_nv*

 ("encounter_looters",sf_2d|sf_vol_8, ["encounter_river_pirates_5.ogg","encounter_river_pirates_6.ogg","encounter_river_pirates_9.ogg","encounter_river_pirates_10.ogg","encounter_river_pirates_4.ogg","encounter_river_pirates_nv5.ogg"]),  ## CC-D add encounter_river_pirates_nv5.ogg

 ("encounter_bandits",sf_2d|sf_vol_8, ["encounter_bandit_2.ogg","encounter_bandit_9.ogg","encounter_bandit_12.ogg","encounter_bandit_13.ogg","encounter_bandit_15.ogg","encounter_bandit_16.ogg","encounter_bandit_10.ogg",]),
 ("encounter_farmers",sf_2d|sf_vol_8, ["encounter_farmer_2.ogg","encounter_farmer_5.ogg","encounter_farmer_7.ogg","encounter_farmer_9.ogg","encounter_farmer_nv2.ogg"]),  ## CC-D add encounter_farmer_nv2.ogg
 ("encounter_sea_raiders",sf_2d|sf_vol_8, ["encounter_sea_raider_5.ogg","encounter_sea_raider_9.ogg","encounter_sea_raider_9b.ogg","encounter_sea_raider_10.ogg","encounter_sea_raider_nv5.ogg","encounter_sea_raider_nv10.ogg"]),  ## CC-D add encounter_sea_raider_nv*
 ("encounter_steppe_bandits",sf_2d|sf_vol_8, ["encounter_steppe_bandit_3.ogg","encounter_steppe_bandit_3b.ogg","encounter_steppe_bandit_8.ogg","encounter_steppe_bandit_10.ogg","encounter_steppe_bandit_12.ogg","encounter_steppe_bandit_nv8.ogg","encounter_steppe_bandit_nv10.ogg","encounter_steppe_bandit_nv12.ogg"]),  ## CC-D add encounter_steppe_bandit_nv*
 ("encounter_nobleman",sf_2d|sf_vol_8, ["encounter_nobleman_1.ogg"]),
 ("encounter_vaegirs_ally",sf_2d|sf_vol_8, ["encounter_vaegirs_ally.ogg","encounter_vaegirs_ally_2.ogg"]),
 ("encounter_vaegirs_neutral",sf_2d|sf_vol_8, ["encounter_vaegirs_neutral.ogg","encounter_vaegirs_neutral_2.ogg","encounter_vaegirs_neutral_3.ogg","encounter_vaegirs_neutral_4.ogg"]),
 ("encounter_vaegirs_enemy",sf_2d|sf_vol_8, ["encounter_vaegirs_neutral.ogg","encounter_vaegirs_neutral_2.ogg","encounter_vaegirs_neutral_3.ogg","encounter_vaegirs_neutral_4.ogg"]),
 ("sneak_town_halt",sf_2d, ["sneak_halt_1.ogg","sneak_halt_2.ogg"]),
 ("horse_walk",sf_priority_3|sf_vol_10, ["horse_walk_01.ogg","horse_walk_02.ogg","horse_walk_03.ogg","horse_walk_04.ogg","horse_walk_05.ogg","horse_walk_06.ogg","horse_walk_07.ogg","horse_walk_08.ogg"]),
 ("horse_trot",sf_priority_4|sf_vol_10, ["horse_trot_01.ogg","horse_trot_02.ogg","horse_trot_03.ogg","horse_trot_04.ogg","horse_trot_05.ogg","horse_trot_06.ogg","horse_trot_07.ogg","horse_trot_08.ogg","horse_trot_09.ogg","horse_trot_10.ogg"]),
 ("horse_canter",sf_priority_4|sf_vol_13, ["horse_canter_01.ogg","horse_canter_02.ogg","horse_canter_03.ogg","horse_canter_04.ogg","horse_canter_05.ogg","horse_canter_06.ogg","horse_canter_07.ogg","horse_canter_08.ogg"]),
 ("horse_gallop",sf_priority_5|sf_vol_13, ["horse_gallop_01.ogg","horse_gallop_02.ogg","horse_gallop_03.ogg","horse_gallop_04.ogg","horse_gallop_05.ogg","horse_gallop_06.ogg","horse_gallop_07.ogg","horse_gallop_08.ogg","horse_gallop_09.ogg","horse_gallop_10.ogg"]),
 ("horse_breath",sf_priority_1|sf_vol_4, ["horse_breath_4.ogg","horse_breath_5.ogg","horse_breath_6.ogg","horse_breath_7.ogg"]),
 ("horse_snort",sf_priority_1|sf_vol_2, ["horse_snort_1.ogg","horse_snort_2.ogg","horse_snort_3.ogg","horse_snort_4.ogg","horse_snort_5.ogg"]),
 ("horse_low_whinny",sf_vol_12, ["horse_whinny-1.ogg","horse_whinny-2.ogg"]),
 ("block_fist",0, ["block_fist_3.ogg","block_fist_4.ogg"]),
 ("man_hit_blunt_weak",sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_blunt_strong",sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_pierce_weak",sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_pierce_strong",sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_cut_weak",sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_hit_cut_strong",sf_priority_5|sf_vol_10, ["man_hit_13.ogg","man_hit_29.ogg","man_hit_32.ogg","man_hit_47.ogg","man_hit_57.ogg"]),
 ("man_victory",sf_priority_5|sf_vol_9, ["man_victory_3.ogg","man_victory_4.ogg","man_victory_5.ogg","man_victory_8.ogg","man_victory_15.ogg","man_victory_49.ogg","man_victory_52.ogg","man_victory_54.ogg","man_victory_57.ogg","man_victory_71.ogg","man_victory_01.ogg","man_victory_02.ogg","man_victory_03.ogg"]),
 ("fire_loop",sf_priority_9|sf_vol_4|sf_looping|sf_start_at_random_pos, ["Fire_Torch_Loop3.ogg"]),
 ("torch_loop",sf_priority_9|sf_vol_4|sf_looping|sf_start_at_random_pos, ["Fire_Torch_Loop3.ogg"]),
 ("dummy_hit",sf_priority_9, ["dummy_hit_01.ogg","dummy_hit_02.ogg","dummy_hit_03.ogg"]),
 ("dummy_destroyed",sf_priority_9, ["dummy_break_01.ogg","dummy_break_02.ogg","dummy_break_03.ogg","dummy_break_04.ogg","dummy_break_05.ogg"]),
 ("gourd_destroyed",sf_priority_9, ["dummy_break_01.ogg","dummy_break_02.ogg","dummy_break_03.ogg","dummy_break_04.ogg","dummy_break_05.ogg"]),#TODO
 ("cow_moo", sf_2d|sf_priority_9|sf_vol_8, ["cow_moo_1.ogg"]),
 ("cow_slaughter", sf_2d|sf_priority_9|sf_vol_8, ["cow_slaughter_01.ogg","cow_slaughter_02.ogg"]),
 ("distant_dog_bark", sf_2d|sf_priority_3|sf_vol_8, ["d_dog1.ogg","d_dog2.ogg","d_dog3.ogg","d_dog7.ogg"]),
 ("distant_owl", sf_2d|sf_priority_3|sf_vol_9, ["d_owl2.ogg","d_owl3.ogg","d_owl4.ogg"]),
 ("distant_chicken", sf_2d|sf_priority_3|sf_vol_8, ["d_chicken1.ogg","d_chicken2.ogg"]),
 ("distant_carpenter", sf_2d|sf_priority_3|sf_vol_3, ["d_carpenter1.ogg","d_saw_short3.ogg"]),
 ("distant_blacksmith", sf_2d|sf_priority_3|sf_vol_4, ["d_blacksmith2.ogg"]),
 ("arena_ambiance", sf_2d|sf_priority_8|sf_vol_3|sf_looping, ["arena_loop11.ogg"]),
 ("town_ambiance", sf_2d|sf_priority_8|sf_vol_3|sf_looping, ["town_loop_3.ogg"]),
 ("tutorial_fail", sf_2d|sf_vol_7,["cue_failure.ogg"]),
 ("your_flag_taken", sf_2d|sf_priority_10|sf_vol_10, ["your_flag_taken.ogg"]),
 ("enemy_flag_taken", sf_2d|sf_priority_10|sf_vol_10, ["enemy_flag_taken.ogg"]),
 ("flag_returned", sf_2d|sf_priority_10|sf_vol_10, ["your_flag_returned.ogg"]),
 ("team_scored_a_point", sf_2d|sf_priority_10|sf_vol_10, ["you_scored_a_point.ogg"]),
 ("enemy_scored_a_point", sf_2d|sf_priority_10|sf_vol_10, ["enemy_scored_a_point.ogg"]),
 #INVASION MODE START
 ("ccoop_spawn_companion_0",sf_2d|sf_vol_8, ["encounter_farmer_2.ogg"]),
 ("ccoop_spawn_companion_1",sf_2d|sf_vol_8, ["encounter_farmer_5.ogg"]),
 ("ccoop_spawn_companion_2",sf_2d|sf_vol_8, ["encounter_farmer_7.ogg"]),
 ("ccoop_spawn_companion_3",sf_2d|sf_vol_8, ["encounter_farmer_9.ogg"]),
 ("ccoop_nobleman_taunt",sf_2d|sf_vol_8, ["encounter_nobleman_1.ogg"]),
 ("ccoop_looter_taunt_0",sf_2d|sf_vol_8, ["encounter_river_pirates_5.ogg"]),
 ("ccoop_looter_taunt_1",sf_2d|sf_vol_8, ["encounter_river_pirates_6.ogg"]),
 ("ccoop_looter_taunt_2",sf_2d|sf_vol_8, ["encounter_river_pirates_9.ogg"]),
 ("ccoop_looter_taunt_3",sf_2d|sf_vol_8, ["encounter_river_pirates_10.ogg"]),
 ("ccoop_looter_taunt_4",sf_2d|sf_vol_8, ["encounter_river_pirates_4.ogg"]),
 ("ccoop_bandit_taunt_0",sf_2d|sf_vol_8, ["encounter_bandit_2.ogg"]),
 ("ccoop_bandit_taunt_1",sf_2d|sf_vol_8, ["encounter_bandit_9.ogg"]),
 ("ccoop_bandit_taunt_2",sf_2d|sf_vol_8, ["encounter_bandit_12.ogg"]),
 ("ccoop_bandit_taunt_3",sf_2d|sf_vol_8, ["encounter_bandit_13.ogg"]),
 ("ccoop_bandit_taunt_4",sf_2d|sf_vol_8, ["encounter_bandit_15.ogg"]),
 ("ccoop_bandit_taunt_5",sf_2d|sf_vol_8, ["encounter_bandit_16.ogg"]),
 ("ccoop_bandit_taunt_6",sf_2d|sf_vol_8, ["encounter_bandit_10.ogg"]),
 ("ccoop_sea_raider_taunt_0",sf_2d|sf_vol_8, ["encounter_sea_raider_5.ogg"]),
 ("ccoop_sea_raider_taunt_1",sf_2d|sf_vol_8, ["encounter_sea_raider_9.ogg"]),
 ("ccoop_sea_raider_taunt_2",sf_2d|sf_vol_8, ["encounter_sea_raider_9b.ogg"]),
 ("ccoop_sea_raider_taunt_3",sf_2d|sf_vol_8, ["encounter_sea_raider_10.ogg"]),
 ("sounds_end", sf_2d|sf_priority_10|sf_vol_10, ["enemy_scored_a_point.ogg"]),
 #INVASION MODE END
 
 #Ore Custom
 ("blaster_shot",sf_priority_10|sf_vol_9, ["fswcblaster04_long.ogg"]), 
 #
 
 #CC-C begin
 ("pistol_flintlock_shot",sf_priority_10|sf_vol_9, ["pistol_flintlock_c.wav","pistol_flintlock_b.wav","pistol_cav_flintlock_a.wav","pistol_cav_flintlock_ba.wav"]),
 ("rifle_shot",sf_priority_9|sf_vol_9, ["rifle_musket.wav","rifle_musketmel.wav","rifle_musketoon_a.wav","rifle_musketoon_b.wav","rifle_musketoon_c.wav","rifle_musketoonpel.wav","rifled_musket.wav","gun_shoot_10.ogg","gun_shoot_11.ogg"]),
 ("merc_musket_shot",sf_priority_10|sf_vol_9, ["merc_musket_a.wav","merc_musket_b.wav"]),
 ("merc_cav_musket_shot",sf_priority_10|sf_vol_9, ["merc_cav_musket_a.wav","merc_cav_musket_b.wav","gun_shoot_10.ogg","gun_shoot_11.ogg"]),
 ("shot1",sf_priority_10|sf_vol_9, ["shot001.ogg"]),
 ("shot2",sf_priority_10|sf_vol_9, ["shot002.ogg"]),
 ("shot3",sf_priority_10|sf_vol_8, ["shot003.ogg"]),
 ("shot4",sf_priority_10|sf_vol_8, ["shot004.ogg"]),
 ("shot5",sf_priority_10|sf_vol_8, ["shot005.ogg"]),
 ("shot6",sf_priority_10|sf_vol_8, ["shot006.ogg"]),
 ("shot7",sf_priority_10|sf_vol_8, ["shot007.ogg"]),
 ("shot8",sf_priority_10|sf_vol_8, ["shot008.ogg"]),
 ("shot9",sf_priority_10|sf_vol_7, ["shot009.ogg"]),
 ("shot10",sf_priority_10|sf_vol_9, ["shot010.ogg"]), 
 ("shot11",sf_priority_10|sf_vol_7, ["shot011.ogg"]),
 ("shot12",sf_priority_10|sf_vol_9, ["shot012.ogg"]),

 ("shot13",sf_priority_10|sf_vol_8, ["shot013.ogg"]),
 ("shot14",sf_priority_10|sf_vol_9, ["shot014.ogg"]),
 ("shot15",sf_priority_10|sf_vol_8, ["shot015.ogg"]),
 ("shot16",sf_priority_10|sf_vol_9, ["shot016.ogg"]),
 ("shot17",sf_priority_10|sf_vol_9, ["shot017.ogg"]),
 ("shot18",sf_priority_10|sf_vol_9, ["shot018.ogg"]),
 ("shot19",sf_priority_10|sf_vol_9, ["shot019.ogg"]),
 ("shot20",sf_priority_10|sf_vol_9, ["shot020.ogg"]),
 
 ("airgunfire",sf_priority_10|sf_vol_9, ["air_1.wav","air_2.wav","air_3.wav","air_4.wav","air_5.wav","air_6.wav","air_7.wav"]),
 ("hyb_musket",sf_priority_10|sf_vol_9, ["hmusk01.wav","hmusk02.wav","hmusk03.wav","hmusk04.wav","hmusk05.wav","hmusk06.wav","hmusk07.wav","hmusk08.wav","hmusk09.wav","hmusk10.wav","hmusk11.wav","hmusk12.wav","hmusk13.wav","hmusk14.wav","hmusk15.wav"]),

 ## CC-D begin
 #("woman_ero",sf_priority_2|sf_vol_10, ["woman_hit_2.ogg","woman_hit_3.ogg","woman_hit_b_2.ogg","woman_hit_b_4.ogg","woman_hit_b_6.ogg","woman_hit_b_7.ogg","woman_hit_b_8.ogg","woman_hit_b_11.ogg","woman_hit_b_14.ogg","woman_hit_b_16.ogg"]),
 ("woman_ero",sf_priority_2|sf_vol_10, ["eros_woman_01.ogg","eros_woman_02.ogg","eros_woman_03.ogg","eros_woman_04.ogg","eros_woman_05.ogg","eros_woman_06.ogg","eros_woman_07.ogg","eros_woman_08.ogg"]),
 #("man_ero",sf_priority_2|sf_vol_10, ["man_grunt_pain_01.ogg","man_grunt_pain_02.ogg","man_grunt_pain_03.ogg","man_grunt_pain_04.ogg","man_grunt_pain_05.ogg","man_grunt_pain_06.ogg","man_grunt_pain_07.ogg","man_grunt_pain_08.ogg","man_grunt_pain_09.ogg","man_grunt_pain_10.ogg","man_grunt_pain_11.ogg","man_grunt_pain_12.ogg","man_grunt_pain_13.ogg","man_grunt_pain_14.ogg","man_grunt_pain_15.ogg","man_grunt_pain_16.ogg","man_grunt_pain_17.ogg","man_grunt_pain_18.ogg","man_grunt_pain_19.ogg","man_grunt_pain_20.ogg"]),
 ("man_ero",sf_priority_2|sf_vol_10, ["eros_man_01.ogg","eros_man_02.ogg","eros_man_03.ogg","eros_man_04.ogg"]),
 ("eros_fire", sf_priority_2|sf_vol_10, ["eros_fire_01.ogg","eros_fire_02.ogg"]),
 ## CC-D end
 
 ("woman_grunt",sf_priority_2|sf_vol_10, ["femgrunt1.ogg","femgrunt2.ogg","femgrunt9.ogg","femgrunt10.ogg"]),
 ("woman_warcry",sf_priority_2|sf_vol_10, ["wwarcry.mp3","wwarcry1.mp3","wwarcry2.mp3","wwarcry2a.mp3","wwarcry3.mp3","wwarcry4.mp3","wwarcry5.mp3","wwarcry6.mp3"]),  ## CC-D add
 ("woman_victory",sf_priority_2|sf_vol_10, ["wvictory1.ogg","wvictory2.ogg","wvictory3.ogg","wvictory4.ogg","wvictory5.ogg"]),  ## CC-D mp3->ogg
 ("woman_stun",sf_priority_2|sf_vol_10, ["femgrunt6.ogg"]),  ## CC-D add
 
 ("man_attack_talk",sf_priority_10|sf_vol_10, ["man_insult_15.ogg","man_insult_16.ogg","man_insult_7.ogg","man_insult_13.ogg","man_insult_9.ogg","man_yell_4.ogg","man_yell_11.ogg"]),
# ("man_die_shout",sf_priority_10|sf_vol_5, ["man_insult_15.ogg"]),  ## CC-D del: not use
#CC-C end

## NMCml begin: horse whistle
 ("whistle", sf_priority_5|sf_vol_8, ["whistle.ogg"]),
## NMCml end
## Tavern Animation Pack by Daedalus
 ("dedal_tavern_lute",	sf_priority_6|sf_vol_8|sf_looping, ["dedal_tavern_lute_1.ogg","dedal_tavern_lute_2.ogg","dedal_tavern_lute_3.ogg"]),
 ("dedal_tavern_lyre",	sf_priority_6|sf_vol_9|sf_looping, ["dedal_tavern_lyre_1.ogg","dedal_tavern_lyre_2.ogg","dedal_tavern_lyre_3.ogg"]),
## Tavern Animation Pack end
## CC-D begin

 ("ccd_raise_troop", sf_2d|sf_priority_9|sf_vol_7, ["ccd_heyhey.ogg"]),

 ("ccd_dog_bark", sf_priority_10|sf_vol_15, ["ccd_dog_bark.ogg"]),
 ("ccd_dog_whine", sf_priority_10|sf_vol_15, ["ccd_dog_die.ogg"]),
 ("ccd_dog_growl", sf_priority_10|sf_vol_15, ["ccd_dog_growl.ogg"]),
 ("ccd_healpot", sf_priority_5|sf_vol_8, ["ccd_healpot.ogg"]),
 ("ccd_souledge", sf_priority_10|sf_vol_14, ["ccd_souledge.ogg"]),
 ("ccd_lightsaber_swing", sf_priority_10|sf_vol_10, ["ccd_lightsaber_01.ogg","ccd_lightsaber_02.ogg"]),
 ("ccd_bash_earth", sf_priority_10|sf_vol_14, ["ccd_bash_earth.ogg"]),
 ("ccd_get_lair", sf_2d|sf_priority_9|sf_vol_7, ["quest_completed2.ogg"]),
 ("ccd_destroy_lair", sf_2d|sf_priority_7|sf_vol_10, ["ccd_destroy_lair.ogg"]),
 ("ccd_raided", sf_2d|sf_priority_9|sf_vol_7, ["quest_cancelled2.ogg"]),
 ("ccd_ghost", sf_priority_7|sf_vol_10, ["horse_fall_b_03.ogg"]),
 ("ccd_undead", sf_priority_7|sf_vol_10, ["cow_slaughter.ogg"]),
 ("ccd_throwing_eros_hit", sf_priority_7|sf_vol_10, ["arrow_pass_by_1.ogg"]),
 ("ccd_pinkdrug", sf_priority_7|sf_vol_10, ["nw_water_walk_2.wav"]),
 ("ccd_gungnir_shot", sf_priority_7|sf_vol_10, ["nw_shell3.ogg"]),
 ("ccd_fire_burning",sf_priority_10|sf_vol_10, ["ccd_fire_burning.ogg"]),
 ("ccd_explosion",sf_priority_15|sf_vol_15, ["nw_shell1.ogg","nw_shell2.ogg","nw_shell3.ogg"]),
 ("ccd_mind_arrow_charge", sf_priority_5|sf_vol_15, ["ccd_aura_charge.ogg"]),

 
 
 ("ccd_undead_die",sf_priority_3|sf_vol_10, ["ccd_zombie_death_1.ogg","ccd_zombie_death_2.ogg"]),
 ("ccd_undead_grunt",sf_priority_3|sf_vol_10, ["ccd_zombie_grunt_1.ogg"]),
 ("ccd_undead_hit",sf_priority_3|sf_vol_10, ["ccd_zombie_hit_1.ogg","ccd_zombie_hit_2.ogg"]),
 ("ccd_undead_yell",sf_priority_3|sf_vol_10, ["ccd_zombie_grunt_1.ogg"]),
 ("ccd_undead_victory",sf_priority_3|sf_vol_10, ["ccd_zombie_grunt_1.ogg"]),
 ("ccd_troll_die",sf_priority_3|sf_vol_10, ["ccd_troll_death_1.ogg"]),
 ("ccd_troll_grunt",sf_priority_3|sf_vol_10, ["ccd_troll_grunt_1.ogg"]),
 ("ccd_troll_hit",sf_priority_3|sf_vol_10, ["ccd_troll_hit_1.ogg","ccd_troll_hit_2.ogg","ccd_troll_hit_3.ogg"]),
 ("ccd_troll_yell",sf_priority_3|sf_vol_10, ["ccd_troll_grunt_1.ogg"]),
 ("ccd_troll_victory",sf_priority_3|sf_vol_10, ["ccd_troll_grunt_1.ogg"]),
 ("balrog_yell", sf_priority_10|sf_vol_15, ["balrog_yell_1.ogg", "balrog_yell_2.ogg", "balrog_yell_3.ogg", "balrog_yell_4.ogg", "balrog_yell_5.ogg", "balrog_yell_6.ogg", "balrog_yell_7.ogg", "balrog_yell_8.ogg", "balrog_yell_9.ogg", "balrog_yell_10.ogg", "balrog_yell_11.ogg", "balrog_yell_12.ogg",]),
 ("balrog_die", sf_priority_10|sf_vol_15, ["balrog_die_1.ogg", "balrog_die_2.ogg", "balrog_die_3.ogg",]),
 ("balrog_hit", sf_priority_10|sf_vol_15, ["balrog_hit_1.ogg", "balrog_hit_2.ogg", "balrog_hit_3.ogg", "balrog_hit_4.ogg", "balrog_hit_5.ogg", "balrog_hit_6.ogg", "balrog_hit_7.ogg", "balrog_hit_8.ogg", "balrog_hit_9.ogg", "balrog_hit_10.ogg",]),
 ("ccd_lizard_die",sf_priority_3|sf_vol_10, ["ccd_lizard_die.ogg"]),
 ("ccd_lizard_grunt",sf_priority_3|sf_vol_10, ["ccd_lizard_grunt.ogg"]),
 ("ccd_lizard_hit",sf_priority_3|sf_vol_10, ["ccd_lizard_hit.ogg"]),
 ("ccd_lizard_yell",sf_priority_3|sf_vol_10, ["ccd_lizard_yell.ogg"]),
 
 ("ccd_shot_mg0815",sf_priority_10|sf_vol_9, ["ccd_gun_shoot_mg0815.ogg"]),

## CC-D end
#occc start
 ("occc_decapitation",sf_priority_9|sf_vol_11, ["decap1.ogg","decap2.ogg","decap3.ogg","decap4.ogg"]),
 ("occc_rocket",sf_priority_10|sf_vol_11, ["argh_explosive_arrow01.wav","argh_explosive_arrow02.wav","argh_explosive_arrow03.wav","argh_explosive_arrow04.wav","argh_explosive_arrow05.wav"]),
 ("occc_shell",sf_priority_10|sf_vol_15, ["shell_incoming1.wav"]),
 ("occc_horn", sf_2d|sf_priority_9|sf_vol_7,["horn.wav"]),
 ("occc_marchsong",	sf_priority_6|sf_vol_15, ["La_ChargeMarche_des_Grenadiers_a_Cheval.ogg"]),
 ("occc_saber_hit",sf_priority_7|sf_vol_10, ["saber_hit1.mp3","saber_hit2.mp3","saber_hit3.mp3"]),

 ("occc_mino_moo", sf_priority_3|sf_vol_10, ["cow_moo_1.ogg"]),
 ("occc_mino_slaughter", sf_priority_10|sf_vol_15, ["cow_slaughter_01.ogg","cow_slaughter_02.ogg"]),

#occc additional v0.21
 ("occc_skeleton_die",sf_priority_3|sf_vol_10, ["skeleton_die_1.ogg","skeleton_die_2.ogg"]),
 ("occc_skeleton_grunt",sf_priority_3|sf_vol_10, ["skeleton_grunt_1.ogg","skeleton_grunt_2.ogg"]),
 ("occc_skeleton_hit",sf_priority_3|sf_vol_10, ["skeleton_hit_1.ogg","skeleton_hit_2.ogg","skeleton_hit_3.ogg"]),
 ("occc_skeleton_yell",sf_priority_3|sf_vol_10, ["skeleton_grunt_1.ogg","skeleton_grunt_2.ogg"]),
 ("occc_skeleton_victory",sf_priority_3|sf_vol_10, ["skeleton_victory_2.ogg"]),

#occc end
 #Project Age Of Machinery start-----------------------------------------------
 ("cannon_shot1", sf_priority_10|sf_vol_10, ["CannonShot1.wav"]),
 ("cannon_shot2", sf_priority_10|sf_vol_10, ["CannonShot2.wav"]),
 ("cannon_shot3", sf_priority_10|sf_vol_10, ["CannonShot3.wav"]),
 ("cannon_shot4", sf_priority_10|sf_vol_10, ["CannonShot4.wav"]),
 ("groundhit1", sf_priority_10|sf_vol_10, ["GroundHit1.wav"]),
 ("groundhit2", sf_priority_10|sf_vol_10, ["GroundHit3.wav"]),
 ("groundhit3", sf_priority_10|sf_vol_10, ["GroundHit4.wav"]),
 ("catapult", sf_priority_10|sf_vol_10, ["Catapult_Attack.wav"]), #occc

#Project Age Of Machinery end-----------------------------------------------#



]
# modmerger_start version=201 type=2
try:
    component_name = "sounds"
    var_set = { "sounds" : sounds }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end

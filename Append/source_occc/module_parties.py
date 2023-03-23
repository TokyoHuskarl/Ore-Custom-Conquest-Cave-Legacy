from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_party_templates import *
from ID_map_icons import *

####################################################################################################################
#  Each party record contains the following fields:
#  1) Party id: used for referencing parties in other files.
#     The prefix p_ is automatically added before each party id.
#  2) Party name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Party-template. ID of the party template this party belongs to. Use pt_none as the default value.
#  6) Faction.
#  7) Personality. See header_parties.py for an explanation of personality flags.
#  8) Ai-behavior
#  9) Ai-target party
# 10) Initial coordinates.
# 11) List of stacks. Each stack record is a triple that contains the following fields:
#   11.1) Troop-id. 
#   11.2) Number of troops in this stack. 
#   11.3) Member flags. Use pmf_is_prisoner to note that this member is a prisoner.
# 12) Party direction in degrees [optional]
####################################################################################################################

no_menu = 0
#pf_town = pf_is_static|pf_always_visible|pf_hide_defenders|pf_show_faction
pf_town = pf_is_static|pf_always_visible|pf_show_faction|pf_label_large
pf_castle = pf_is_static|pf_always_visible|pf_show_faction|pf_label_medium
##CC-C begin
#pf_village = pf_is_static|pf_always_visible|pf_hide_defenders|pf_label_small
pf_village = pf_is_static|pf_always_visible|pf_show_faction|pf_label_small
##CC-C end
#sample_party = [(trp_swadian_knight,1,0), (trp_swadian_peasant,10,0), (trp_swadian_crossbowman,1,0), (trp_swadian_man_at_arms, 1, 0), (trp_swadian_footman, 1, 0), (trp_swadian_militia,1,0)]

# NEW TOWNS:
# NORMANDY: Rouen, Caen, Bayeux, Coutances, Evreux, Avranches
# Brittany: Rennes, Nantes,
# Maine: Le Mans
# Anjou: Angers


parties = [
  ("main_party","Main Party",icon_player, no_menu, pt_none,fac_player_faction,0,ai_bhvr_hold,0,(17, 52.5),[(trp_player,1,0)]),
  ("temp_party","{!}temp_party",pf_disabled, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
  ("camp_bandits","{!}camp_bandits",pf_disabled, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(1,1),[(trp_temp_troop,3,0)]),
#parties before this point are hardwired. Their order should not be changed.

  ("temp_party_2","{!}temp_party_2",pf_disabled, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
#Used for calculating casulties.
  ("temp_casualties","{!}casualties",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_casualties_2","{!}casualties",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_casualties_3","{!}casualties",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_wounded","{!}enemies_wounded",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("temp_killed", "{!}enemies_killed", pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("main_party_backup","{!}_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("encountered_party_backup","{!}_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
#  ("ally_party_backup","_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("collective_friends_backup","{!}_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("player_casualties","{!}_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("enemy_casualties","{!}_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("ally_casualties","{!}_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),

  ("collective_enemy","{!}collective_enemy",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  #TODO: remove this and move all to collective ally
  ("collective_ally","{!}collective_ally",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
  ("collective_friends","{!}collective_ally",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),
   
  ("total_enemy_casualties","{!}_",  pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]), #ganimet hesaplari icin #new:
  ("routed_enemies","{!}routed_enemies",pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]), #new:  
################################################################################
#CC-C begin
################################################################################
  ("ccc_cave_swadia_point" ,"Swadia Cave",icon_bandit_lair|pf_is_static|pf_always_visible|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(-76.71,20.06),[],340),
  ("ccc_cave_rhodoks_point" ,"Rhodoks Cave",icon_bandit_lair|pf_is_static|pf_always_visible|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(-20.14,-42.86),[],140),
  ("ccc_cave_nords_point" ,"Nords Cave",icon_bandit_lair|pf_is_static|pf_always_visible|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(3.15,50.27),[],60),
  ("ccc_cave_khergit_point" ,"Khergit Cave",icon_bandit_lair|pf_is_static|pf_always_visible|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(111.93,-8.63),[],330),
  ("ccc_cave_vaegirs_point" ,"Vaegirs Cave",icon_bandit_lair|pf_is_static|pf_always_visible|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(72.33,37.46),[],340),
  ("ccc_cave_sultanate_point" ,"Sultanate Cave",icon_bandit_lair|pf_is_static|pf_always_visible|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(72.46,-57.73),[],150),
  ("occc_cave_albion_point" ,"Balion Cave",icon_bandit_lair|pf_is_static|pf_always_visible|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(-216.54,22.27),[],287), #[swycartographr] prev. coords: (36.46, -57.73) rot: 150

  ("ccc_cave_dark_knight_point" ,"Dark Knight Cave",icon_bandit_lair|pf_is_static|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(165.82,-8.95),[],60),
  ("ccc_cave_dark_spawn_point","{!}dark bandit",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(173.56,47.60),[(trp_looter,15,0)]),
  
  ("ccc_cave_north_point" ,"North Cave",icon_bandit_lair|pf_is_static|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(129.75,92.72),[],340),
  ("ccc_cave_north_spawn_point","{!}north bandit",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(137.75,101.72),[(trp_looter,15,0)]),

  ("ccc_cave_south_point" ,"South Cave",icon_bandit_lair|pf_is_static|pf_hide_defenders,no_menu,pt_ccc_cave_1,fac_neutral,0,ai_bhvr_hold,0,(106.12,-120.22),[],140),
  ("ccc_cave_south_spawn_point","{!}south bandit",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(107.12,-132.22),[]),

  ("ccc_cave_kulum_spawn_point","kulum near",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-230, 82),[]),#occc -128.13,113.93
  ("ccc_cave_odasan_spawn_point","{!}odasan near",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-30.77,121.41),[]),

  ("ccc_mineworker_party","Mineworker",pf_disabled, no_menu,pt_none,fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  ("ccc_troop_table","{!}temp_party",pf_disabled, no_menu,pt_ccc_temp_party, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
  
  ("ccc_hide_house" ,"Hide_house",icon_village_a|pf_is_static|pf_hide_defenders|pf_label_small,no_menu,pt_none,fac_neutral,0,ai_bhvr_hold,0,(-1.20,8.97),[],140),
  ("ccc_slave_merchant","{!}Slave Market",pf_disabled, no_menu,pt_none,fac_neutral,0,ai_bhvr_hold,0,(0,0),[]),
  
  #system party
  ("ccc_temp_party","{!}temp_party",pf_disabled, no_menu,pt_ccc_temp_party, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
  ("ccc_stand_party","Stand_party",pf_disabled, no_menu,pt_ccc_temp_party, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
  ("ccc_stop_party","Stop_party",pf_disabled, no_menu,pt_ccc_temp_party, fac_commoners,0,ai_bhvr_hold,0,(0,0),[]),
################################################################################
#CC-C End
################################################################################
#  ("village_reinforcements","village_reinforcements",pf_is_static|pf_disabled, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1,1),[]),

###############################################################  
  ("zendar","Zendar",pf_disabled|icon_town|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(18,60),[]),

  ("town_1","Sargoth",  icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-17.6, 79.7),[], 170),
  ("town_2","Tihr",     icon_town_tihr|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-53.5, 78.4),[], 120),
  ("town_3","Veluca",   icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-57.4, -44.5),[], 80),
  ("town_4","Suno",     icon_town_big|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-70, 15.4),[], 290),
  ("town_5","Jelkala",  icon_town_rome|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-74.6, -79.7),[], 90),
  ("town_6","Praven",   icon_town_big|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-96, 26.4),[], 155),
  ("town_7","Uxkhal",   icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-50, -8.5),[], 240),

  ("town_8","Reyvadin", icon_town_big|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(48.44, 39.3),[], 175),
  ("town_9","Khudan",   icon_town_snow|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(94, 65.2),[], 90),
  ("town_10","Tulga",   icon_town_steppe|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(135.5, -22),[], 310),
  ("town_11","Curaw",   icon_town_snow|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(43, 67.5),[], 150),
  ("town_12","Wercheg", icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-1.2, 108.9),[], 25),
  ("town_13","Rivacheg",icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(64.8, 113.7),[], 60),
  ("town_14","Halmar",  icon_town_steppe|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(55.5, -45),[], 135),

  ("town_15","Yalen",  icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-132.8, -47.3),[], 45),
  ("town_16","Dhirim",  icon_town_big|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(14, -2),[], 0),
  ("town_17","Ichamur",  icon_town_steppe|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(121.8, 8.6),[], 90),
  ("town_18","Narra",  icon_town_steppe|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(88, -26.5),[], 135),

  ("town_19","Shariz", icon_town_desert|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(15, -107),[], 45),
  ("town_20","Durquba", icon_town_desert|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(90, -95.1),[], 270),
  ("town_21","Ahmerrad", icon_town_desert|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(130.5, -78.5),[], 330),
  ("town_22","Bariyye", icon_town_desert|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(165, -106.7),[], 225),

#CC-C begin add town
  ("town_23","Lirben",   icon_town_big|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(40.49, -19.70),[], 310), ## Base town_10 Tulga
  ("town_24","Rehmen",  icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-0.95, -39.19),[], 135), ## Base town_18 Narra
#CC-C End
##occc start
  #hellas
  ("town_25","Athenai",  icon_town_desert|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-7.43, -155.56),[], 312), ##  
  ("town_26","Nuovo Zendar",  icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-142.67, 28.26),[], 207), ## Base town_5 Jelkala  #[swycartographr] prev. coords: (-10.43, -155.56) rot: 312 #[swycartographr] prev. coords: (-143.43, 27.35)
  ("town_27","Murom",  icon_town_big_snowy|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(106.07, 103.1),[], 155), ##     #[swycartographr] prev. coords: (-12.43, -155.56) rot: 312
  ("town_28","Camelot",  icon_town|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-180.5, 75.67),[], 204), ## Albion  Base     #[swycartographr] prev. coords: (-12.43, -155.56) rot: 312 #[swycartographr] prev. coords: (-184.044, 76.438) rot: 155 #[swycartographr] prev. coords: (-181, 75.47)
  ("town_29","Lundein",  icon_town_tihr|pf_town, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-198.56, -3.54),[], 355), ## Albion  Base     #[swycartographr] prev. coords: (-12.43, -155.56) rot: 312 #[swycartographr] prev. coords: (-184.044, 76.438) rot: 155 #[swycartographr] prev. coords: (-198, -2.47) rot: 60 #[swycartographr] prev. coords: (-197.92, -2.8) rot: 127 #[swycartographr] prev. coords: (-197.92, -2.8) rot: 299

  
  
##occc end
#   Aztaq_Castle       
#  Malabadi_Castle
  ("castle_1","Culmarr_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-101.3, -21),[],50),
  ("castle_2","Malayurg_Castle",icon_castle_b|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(97.5, -2.2),[],75),
  ("castle_3","Bulugha_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(47.5, 111.3),[],100),
  ("castle_4","Radoghir_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(32.5, 47.8),[],180),
  ("castle_5","Tehlrog_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-4.8, 63.7),[],90),
  ("castle_6","Tilbaut_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(37.6, 17.1),[],55),
  ("castle_7","Sungetche_Castle",icon_castle_snow_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(109.5, 41.5),[],45),
  ("castle_8","Jeirbe_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(35.2, 89),[],30),
  ("castle_9","Jamiche_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-7.5, -82.6),[],100),
  ("castle_10","Alburq_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(24.2, 96.85),[],110), ## CC change from icon_castle_a
  ("castle_11","Curin_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-27.50, 83.46),[],75),
  ("castle_12","Chalbek_Castle",icon_castle_b|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-84.75, 105.5),[],95),
  ("castle_13","Kelredan_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-10.6, 17.6),[],115),
  ("castle_14","Maras_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-122.4, -18.1),[],90),
  ("castle_15","Ergellon_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-52.5, -28),[],235),
  ("castle_16","Almerra_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-10.6, -65.6),[],45),
  ("castle_17","Distar_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(140.3, -10.8),[],15),
  ("castle_18","Ismirala_Castle",icon_castle_snow_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(14.4, 70.1),[],300),
  ("castle_19","Yruma_Castle",icon_castle_snow_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(69.5, 55.6),[],280),
  ("castle_20","Derchios_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(16, 11.5),[],260),
  ("castle_21","Ibdeles_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-73, -89.5),[],260),
  ("castle_22","Unuzdaq_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(33, -64),[],260),
  ("castle_23","Tevarin_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-124.8, 44.3),[],80),
  ("castle_24","Reindi_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(24.9, -35.6),[],260),
  ("castle_25","Ryibelet_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-57, 30.6),[],260),
  ("castle_26","Senuzgda_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-2.5, -9.5),[],260),
  ("castle_27","Rindyar_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(63.3, -2),[],260),
  ("castle_28","Grunwalder_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-36.4, -39.3),[],260),

  ("castle_29","Nelag_Castle",icon_castle_snow_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(147.7, 50.4),[],280),
  ("castle_30","Asugan_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(176, -47),[],260),
  ("castle_31","Vyincourd_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-65.7, -12.5),[],260),
  ("castle_32","Knudarr_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(2, 30.1),[],260),
  ("castle_33","Etrosq_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-101.4, -32.1),[],80),
  ("castle_34","Hrus_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-72.5, 78.6),[],260),
  ("castle_35","Haringoth_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-110, 0),[],260),
  ("castle_36","Jelbegi_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-47.3, 53.2),[],260),
  ("castle_37","Dramug_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(55.3, 23),[],260),
  ("castle_38","Tulbuk_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(141.7, 33.3),[],260),
  ("castle_39","Slezkh_Castle",icon_castle_snow_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(56.8, 74.5),[],280),
  ("castle_40","Uhhun_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(62.9, -26),[],260),

  ("castle_41","Jameyyed_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(71.3, -71.1),[],260),
  ("castle_42","Teramma_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(70, -96),[],80),
  ("castle_43","Sharwa_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(172, -65),[],260),
  ("castle_44","Durrin_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(128, -87),[],260),
  ("castle_45","Caraf_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(30.6, -110.6),[],260),
  ("castle_46","Weyyah_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(13.3, -84.4),[],260),
  ("castle_47","Samarra_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(116, -74),[],260),
  ("castle_48","Bardaq_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(157, -80),[],260),

## CC new castles
  # Swadia
  ("castle_49","Deglan_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-140.3, 12.1),[],100),
  ("castle_50","Tredian_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-77.3, 47.9),[],110),
  ("castle_51","Grainwad_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-20.8, 27.3),[],75),
  ("castle_52","Ryis_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-21.6, 0.5),[],95),
  ("castle_53","Stamar_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(40.8, -10),[],115),
  # Vaegirs
  ("castle_54","Doru_Castle",icon_castle_snow_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(88.3, 84.1),[],90),
  ("castle_55","Gastya_Castle",icon_castle_snow_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(119.6, 67.9),[],235),
  # Khergit
  ("castle_56","Sebula_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(168.8, 21.7),[],260),
  # Nords
  ("castle_57","Turegor_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(2.4, 88.9),[],260),
  ("castle_58","Rayeck_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-119.4, 100.4),[],260),
  # Rhodoks
  ("castle_59","Reland_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-134.7, -0.6),[],280),
  ("castle_60","Falsevor_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-35.4, -77.4),[],260),
  ("castle_61","Reichsin_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-78.3, -44),[],80),
  # Sarranid
  ("castle_62","Ghulassen_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(51.3, -98.9),[],260),
  ("castle_63","Muhnir_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(59.4, -110),[],260),
  ("castle_64","Biliya_Castle",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(116.8, -99.6),[],260),
  
  ##occc begin 
  #Hellas Lakedaimon
  ("castle_65","Lakedaimon",icon_castle_d|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-5.89, -141.57),[],355),  
  #Albibon 
  ("castle_66","Castle_Anthrax",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-193.25, 44.62),[],46),            #[swycartographr] prev. coords: (-185.89, 76.57) rot: 355 #[swycartographr] prev. coords: (-194.94, 82.82) rot: 300 #[swycartographr] prev. coords: (-199.04, 58.59) #[swycartographr] prev. coords: (-188.82, 63.38) #[swycartographr] prev. coords: (-194.22, 61.69) rot: 50 #[swycartographr] prev. coords: (-197.95, 52.48) #[swycartographr] prev. coords: (-195.54, 52.19)
  ("castle_67","Aarrgh_Castle",icon_castle_a|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-177.09, 89.79),[],115),             #[swycartographr] prev. coords: (-175.89, 76.57) rot: 355 #[swycartographr] prev. coords: (-176.24, 86.68)
  ("castle_68","Camulodun_Castle",icon_castle_c|pf_castle, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-196.73, 18.34),[],287),          #[swycartographr] prev. coords: (-177.5, -82.6) rot: 100 #[swycartographr] prev. coords: (-198.16, 19.41)

  #Camulodun
  ##occc end
## CC

#     Rinimad      
#              Rietal Derchios Gerdus
# Tuavus   Pamir   vezona 
  
  ("village_1", "Yaragar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-60, -9.5),[], 100),
  ("village_2", "Burglen",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-13.5, 3.5),[], 110),
  ("village_3", "Azgad",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-97.4, 36),[], 120),
  ("village_4", "Nomar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-36.6, -13.2),[], 130),
  ("village_5", "Kulum",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-122.7, 106.3),[], 170),
  ("village_6", "Emirin",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(5.5, -2.5),[], 100),
  ("village_7", "Amere",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(39.3, -5.25),[], 110),
  ("village_8", "Haen",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-49.7, 74),[], 120),
  ("village_9", "Buvran",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-85, -75.35),[], 130),
  ("village_10","Mechin",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(8.8, 34.75),[], 170),

  ("village_11","Dusturil",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(137.2, -36.5),[], 100),
  ("village_12","Emer",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-45.8, -58.5),[], 110),
  ("village_13","Nemeja",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-119, 3),[], 120),
  ("village_14","Sumbuja",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(40,52),[], 130),
  ("village_15","Ryibelet",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-49.3, 26.25),[], 170),
  ("village_16","Shapeshte",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(74, 86.8),[], 170),
  ("village_17","Mazen",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(44.7, 91.4),[], 35),
  ("village_18","Ulburban",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(73.7, 30.1),[], 170),
  ("village_19","Hanun",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(152.3, 53.5),[], 170),
  ("village_20","Uslum",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(116, 80.3),[], 170),

  ("village_21","Bazeck",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(60.4, 85),[], 100),
  ("village_22","Shulus",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(125.4, 64),[], 110),
  ("village_23","Ilvia",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-133.3, -37.6),[], 120),
  ("village_24","Ruldi",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-57.6, -73),[], 130),
  ("village_25","Dashbigha",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(125.2, -8),[], 170),
  ("village_26","Pagundur",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-58.5, -30.8),[], 170),
  ("village_27","Glunmar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-146.3, -16.6),[], 170),
  ("village_28","Tash_Kulun",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(95, -11.4),[], 170),
  ("village_29","Buillin",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-90.6, 110.9),[], 170),

  ("village_30","Ruvar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(29.2, 114.3),[], 170),
  ("village_31","Ambean",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-24, 53),[], 100),
  ("village_32","Tosdhar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(8.3 , 14.5 ),[], 110),
  ("village_33","Ruluns",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-59, 10.6),[], 120),
  ("village_34","Ehlerdah",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(34.15, -30),[], 130),
  ("village_35","Fearichen",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(2.14, 86.9),[], 170),
  ("village_36","Jayek",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(17.4, 100.7),[], 170),
  ("village_37","Ada_Kulun",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(164.4, 26),[], 170),
  ("village_38","Ibiran",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-42.8, 11.25),[], 170),
  ("village_39","Reveran",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-124.3, -29.5),[], 170),
  ("village_40","Saren",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-12, -53),[], 170),

  ("village_41","Dugan",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(175, -39.5),[], 100),
  ("village_42","Dirigh_Aban",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(115.4, 21.6),[], 110),
  ("village_43","Zagush",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(99.4, -21.3),[], 120),
  ("village_44","Peshmi",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(51.8, -50),[], 130),
  ("village_45","Bulugur",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(151.5, -3),[], 170),
  ("village_46","Fedner",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-82.4, -48.8),[], 170),
  ("village_47","Epeshe",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-101.2, -53.7),[], 170),
  ("village_48","Veidar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-103, 15.3),[], 170),
  ("village_49","Tismirr",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(90.8, 60.5),[], 10),
  ("village_50","Karindi",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(64.1, 55.9),[], 170),

  ("village_51","Jelbegi",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-40, 62),[], 100),
  ("village_52","Amashke",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(38.2, -67.7),[], 110),
  ("village_53","Balanli",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-130.3, 42),[], 120),
  ("village_54","Chide",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-19, 15.5),[], 130),
  ("village_55","Tadsamesh",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(37.3, 23.7),[], 170),
  ("village_56","Fenada",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-5.55, 75.5),[], 170),
  ("village_57","Ushkuru",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(24.75, -7.7),[], 170),
  ("village_58","Vezin",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(78.50, 118.3),[], 170),
  ("village_59","Dumar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-101, -45),[], 170),
  ("village_60","Tahlberl",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-26.6, 30),[], 170),

  ("village_61","Aldelen",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-99.8, 85.65),[], 100),
  ("village_62","Rebache",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(36.7, 59.5),[], 100),
  ("village_63","Rduna",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(70.75, 1.6),[], 100),
  ("village_64","Serindiar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-41.5, -35.8),[], 100),
  ("village_65","Iyindah",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-86.3, 12.4),[], 100),
  ("village_66","Fisdnar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(109, 127.5),[], 100),
  ("village_67","Tebandra",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(65, 23),[], 100),
  ("village_68","Ibdeles",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-72.6, -97.5),[], 100),
  ("village_69","Kwynn",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-26.5, 77.6),[], 100),
  ("village_70","Dirigsene",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-94, -27),[], 100),

  ("village_71","Tshibtin",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-9, -20),[], 20),
  ("village_72","Elberl",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-144, 16.15),[], 60),
  ("village_73","Chaeza",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-63.2, -51.4),[], 55),
  ("village_74","Ayyike",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(49, 31),[], 15),
  ("village_75","Bhulaban",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(110.2, 48.8),[], 10),
  ("village_76","Kedelke",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(91.5, -34.8),[], 35),
  ("village_77","Rizi",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-64.8, 81.5),[], 160),
  ("village_78","Sarimish",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-30.2, -53.3),[], 180),
  ("village_79","Istiniar",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-134.1, -5.5),[], 0),
  ("village_80","Vayejeg",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-1.5, 56),[], 40),

  ("village_81","Odasan",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-17.2, 123.6),[], 20),
  ("village_82","Yalibe",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(12, -26),[], 60),
  ("village_83","Gisim",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-79.9, 55.2),[], 55),
  ("village_84","Chelez",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-45.6, -83),[], 15),
  ("village_85","Ismirala",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(22.8, 71.7),[], 10),
  ("village_86","Slezkh",  icon_village_snow_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(60.5, 68.2),[], 35),
  ("village_87","Udiniad",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(52.3, 111.8),[], 160),
  ("village_88","Tulbuk",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(135.8, 24.7),[], 180),
  ("village_89","Uhhun",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(70.1, -27.9),[], 0),
  ("village_90","Jamiche",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-12.7, -85.5),[], 40),

  ("village_91","Ayn Assuadi",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(21.6, -95.3),[], 20),
  ("village_92","Dhibbain",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(42.5, -111.6),[], 60),
  ("village_93","Qalyut",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(50, -94.8),[], 55),
  ("village_94","Mazigh",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(75.4, -61.65),[], 15),
  ("village_95","Tamnuh",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(99, -90.5),[], 10),
  ("village_96","Habba",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(107, -75),[], 35),
  ("village_97","Sekhtem",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(82.3, -76.8),[], 160),
  ("village_98","Mawiti",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(117.7, -62.2),[], 180),
  ("village_99","Fishara",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(158.35, -98),[], 0),
  ("village_100","Iqbayl",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(150, -106.5),[], 40),

  ("village_101","Uzgha",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(154, -69.5),[], 20),
  ("village_102","Shibal Zumr",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(77.2, -91),[], 60),
  ("village_103","Mijayet",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(121, -95.6),[], 55),
  ("village_104","Tazjunat",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(159, -58.5),[], 15),
  ("village_105","Aab",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(135, -88.5),[], 10),
  ("village_106","Hawaha",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(10.3, -91.0),[], 35),
  ("village_107","Unriya",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(156.6, -84),[], 160),
  ("village_108","Mit Nun",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(28.8, -107.3),[], 180),
  ("village_109","Tilimsal",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(53, -114.5),[], 0),
  ("village_110","Rushdigh",  icon_village_c|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(38, -104),[], 40),
  
#CC-C begin add village
  ("village_111","Aken",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(30.74, -20.55),[], 100), 
  ("village_112","Busingen",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(51.40, -23.91),[], 170), 
  ("village_113","Cottbus",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(8.20, -42.85),[], 110), 
  ("village_114","Leer",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-15.33, -31.72),[], 35), 
  ("village_115","Neustadt",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-21.40, -27.93),[], 170), 
  ("village_116","Pyritz",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(5.53, -51.49),[], 110), 
  ("village_117","Zerbst",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(52.63, -12.11),[], 35), 
  
  #Sw
  ("village_118","Amberg",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(29.51, 0.23),[], 110), 
  ("village_119","Ansbach",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(31.28, 9.03),[], 35), 
  ("village_120","Bamberg",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(22.80, -22.65),[], 170), 
  ("village_121","Breslau",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(8.38, -8.51),[], 110), 
  ("village_122","Dessau",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(21.25, -14.11),[], 35), 
  ("village_123","Demmin",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(8.20, -16.24),[], 110), 
  ("village_124","Emden",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-18.15, -7.70),[], 35), 
  ("village_125","Erfurt",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-30.49, -3.84),[], 170), 
  ("village_126","Freiburg",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-41.98, -0.39),[], 110), 
  ("village_127","Gera",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(19.71, 22.70),[], 35), 
  ("village_128","Giessen",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-55.82, 20.87),[], 35), 
  ("village_129","Greiz",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-64.77, 48.40),[], 170), 
  ("village_130","Konigsberg",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-85.87, -30.32),[], 110), 
  ("village_131","Lorbach",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-92.98, 19.83),[], 35), 
  ("village_132","Rheyot",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-124, 18.63),[], 35), 
  ("village_133","Saratoga",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-80.65, 39.58),[], 110), 
  ("village_134","Ulm",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-87.84, 0.53),[], 35), 
  ("village_135","Worth",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-106.24, 34.14),[], 170), 
  ("village_136","Zeitz",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-53.68, 40.60),[], 110), 
  ("village_137","Torgau",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(2.32, 6.31),[], 35), 
  
  #rd
  ("village_138","Emilia",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-107.13, -9.98),[], 170), 
  ("village_139","Arpino",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-113, -16.58),[], 110), 
  ("village_140","Arpinum",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-126.02, -9.52),[], 35), 
  ("village_141","Caserta",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-148.25, -31.61),[], 110), 
  ("village_142","Genoa",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-157.89, -33.58),[], 35), 
  ("village_143","Genova",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-124.65, -58.94),[], 170), 
  ("village_144","Italia",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-91.56, -85.06),[], 110), 
  ("village_145","Napole",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-68.89, -38.54),[], 35), 
  ("village_146","Torino",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-47.10, -98.10),[], 147),              #[swycartographr] prev. coords: (-47.78, -98.33) rot: 35 #[swycartographr] prev. coords: (-46.52, -95.48) rot: 84 #[swycartographr] prev. coords: (-45.26, -95.34) #[swycartographr] prev. coords: (-21.1, -76.1)
  ("village_147","Bergamo",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-4.75, -61.07),[], 170), 
  ("village_148","Milano",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-73.99, -58.30),[], 110), 

  #nd
  ("village_149","Bristol",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-105.97, 73.01),[], 170), 
  ("village_150","Northwood",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-106.81, 113.09),[], 110), 
  ("village_151","Harbey",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-20.79, 63.61),[], 35), 
  ("village_152","Anglie",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-19.14, 40.16),[], 110), 
  ("village_153","Argyll",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-33.52, 79.23),[], 35), 
  ("village_154","Edina",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-16.60, 75.62),[], 170), 
  ("village_155","Edinburgh",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-38.72, 110.38),[], 110), 
  ("village_156","Exeter",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-12.49, 49.48),[], 35), 
  ("village_157","Windsor",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-34.69, 49.42),[], 35), 
  ("village_158","Omagh",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(7.81, 65.72),[], 170), 
  ("village_159","Ulster",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-1.02, 116.26),[], 110), 

  #vg
  ("village_160","Aisne",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(92.04, 69.14),[], 110), 
  ("village_161","Albiga",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(98.31, 68.40),[], 35), 
  ("village_162","Autun",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(70.63, 95.79),[], 110), 
  ("village_163","Auvergne",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(62.58, 109.52),[], 35), 
  ("village_164","Auxerre",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(69.70, 110.47),[], 170), 
  ("village_165","Cahors",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(58.52, 43.72),[], 110), 
  ("village_166","Loire",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(36.84, 38.95),[], 35), 
  ("village_167","Marne",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(13.87, 50.88),[], 35), 
  ("village_168","Savoie",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(15.09, 59.64),[], 170), 
  ("village_169","Seine",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(55.14, 49.35),[], 110), 

  #kh
  ("village_170","Cadix",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(48.60, -40.38),[], 110), 
  ("village_171","Cadiz",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(57.87, -37.69),[], 35), 
  ("village_172","Conca",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(64.28, -47.05),[], 110), 
  ("village_173","Hoei",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(84.15, -19.78),[], 35), 
  ("village_174","Huy",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(77.73, -39.79),[], 170), 
  ("village_175","Jerez",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(129.54, 10.51),[], 110), 
  ("village_176","Liegi",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(127.44, -19.42),[], 35), 
  ("village_177","Malaca",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(154.81, -22.03),[], 35), 
  ("village_178","Urci",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(89.13, -3.93),[], 170), 
  ("village_179","Znaim",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(103.79, -37.86),[], 110), 

  #sa
  ("village_180","Hattusa",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(7.76, -112.96),[], 110), 
  ("village_181","Jericho",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(7.45, -100.63),[], 35), 
  ("village_182","Petra",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(18.65, -113.53),[], 110), 
  ("village_183","Ugarit",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(30.62, -121.06),[], 35), 
  ("village_184","Qadesh",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(89.12, -102.54),[], 170), 
  ("village_185","Sidon",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(97.72, -99.83),[], 110), 
  ("village_186","Saida",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(130.25, -70.14),[], 35), 
  ("village_187","Byblos",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(172.28, -97.70),[], 35), 
  ("village_188","Tyre",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(60.37, -67.70),[], 170), 
  ("village_189","Megiddo",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(95.16, -73.54),[], 110), 

#CC-C end

#occc start
  ("village_190","Thebai",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-12.37, -160.48),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-3.93, -136.04)
  ("village_191","Micene",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-3.62, -162.24),[], 22),              #[swycartographr] prev. coords: (-4.16, -180.54) rot: 110
#old vaegir
  ("village_192","Neva",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(102.94, 94.39),[], 166),                 #[swycartographr] prev. coords: (-5.62, -162.24) #[swycartographr] prev. coords: (97.87, 96.65) rot: 170
  ("village_193","Volga",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(98.51, 105.67),[], 108),                 #[swycartographr] prev. coords: (-5.62, -162.24) #[swycartographr] prev. coords: (112.87, 96.65) rot: 170
#old rhodok
  ("village_194","Shylock",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-139.69, 31.21),[], 170),            #[swycartographr] prev. coords: (-8.62, -162.24)
  ("village_195","Venicia",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-146.03, 24.68),[], 217),            #[swycartographr] prev. coords: (-8.62, -162.24) #[swycartographr] prev. coords: (-120.69, 31.21) rot: 170
#hellas additional villages
  ("village_196","Macedon",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-4, -150.04),[], 170),             #[swycartographr] prev. coords: (-2, -148.7)
  ("village_197","Constanty",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-3.62, -139.24),[], 22),              #[swycartographr] prev. coords: (-4.16, -180.54) rot: 110
  ("village_198","Salonica",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-21.15, -148.22),[], 232),              #[swycartographr] prev. coords: (-4.16, -180.54) rot: 110 #[swycartographr] prev. coords: (-21.15, -148.22) #[swycartographr] prev. coords: (-1.62, -139.24) rot: 22
  ("village_199","Ionis",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-20.45, -133.81),[], 140),              #[swycartographr] prev. coords: (-4.16, -180.54) rot: 110 #[swycartographr] prev. coords: (-20.45, -133.81) #[swycartographr] prev. coords: (-1.62, -134.24) rot: 22
#Albion
  ("village_200","Aberlessic",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-177.03, 79.02),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-177.55, 77.97)
  ("village_201","Baer",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-193.33, 24.54),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-174.78, 70.65) #[swycartographr] prev. coords: (-175.42, 71.72)
  ("village_202","Dinypas",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-194.84, 56.59),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-183.49, 60.8) #[swycartographr] prev. coords: (-181.52, 61.21) #[swycartographr] prev. coords: (-186.58, 61.92)
  ("village_203","Ludeu",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-179.03, 67.77),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-190.42, 71.73) #[swycartographr] prev. coords: (-192.89, 70.96) #[swycartographr] prev. coords: (-186.07, 69.92)
  ("village_204","Cluana",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-189.63, 79.97),[], 311),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) rot: 170 #[swycartographr] prev. coords: (-192.12, 87.69)
  ("village_205","Bertha",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-184.59, 87.62),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-184.99, 87.65) #[swycartographr] prev. coords: (-183.84, 81.63)
  ("village_206","Casislen Credi",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-187.32, 96.14),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04)
  ("village_207","Duin",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-189.68, 63.16),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-190.79, 79.8) #[swycartographr] prev. coords: (-193.89, 78.72) #[swycartographr] prev. coords: (-179.56, 63.92)
  ("village_208","Uaine",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-190.44, 47.63),[], 170),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-196.68, 66.25) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-195.69, 62.84) #[swycartographr] prev. coords: (-197.18, 67.63) #[swycartographr] prev. coords: (-203.04, 71.07) #[swycartographr] prev. coords: (-196, 59.69) #[swycartographr] prev. coords: (-194.4, 57.68)
  ("village_209","Lann Abae",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-204.27, 54.29),[], 221),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-192.86, 50.1) #[swycartographr] prev. coords: (-198.46, 58.85) #[swycartographr] prev. coords: (-197.61, 55.72) rot: 170 #[swycartographr] prev. coords: (-203.23, 45.77) #[swycartographr] prev. coords: (-195.95, 44.11) #[swycartographr] prev. coords: (-192.23, 33.9)
  ("village_210","Ad Cluanan",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-189.91, 35.72),[], 133),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-206.56, 56.98) #[swycartographr] prev. coords: (-182.28, 67.18) #[swycartographr] prev. coords: (-184.54, 66.7) rot: 170 #[swycartographr] prev. coords: (-186.55, 42.52)
  ("village_211","Thames",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-198.61, -11.61),[], 180),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-206.56, 56.98) #[swycartographr] prev. coords: (-182.28, 67.18) #[swycartographr] prev. coords: (-184.54, 66.7) rot: 170 #[swycartographr] prev. coords: (-209.55, -9.52)
  ("village_212","Heli",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-192.57, 4.55),[], 60),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-206.56, 56.98) #[swycartographr] prev. coords: (-182.28, 67.18) #[swycartographr] prev. coords: (-184.54, 66.7) rot: 170 #[swycartographr] prev. coords: (-209.55, -9.52)
  ("village_213","Cair",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-188.35, 14.81),[], 150),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-206.56, 56.98) #[swycartographr] prev. coords: (-182.28, 67.18) #[swycartographr] prev. coords: (-184.54, 66.7) rot: 170 #[swycartographr] prev. coords: (-209.55, -9.52) #[swycartographr] prev. coords: (-201.01, 4.73) rot: 133
  ("village_214","Vicus",  icon_village_a|pf_village, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-201.01, 4.73),[], 133),             #[swycartographr] prev. coords: (-2, -148.7) #[swycartographr] prev. coords: (-184, 70.04) #[swycartographr] prev. coords: (-206.56, 56.98) #[swycartographr] prev. coords: (-182.28, 67.18) #[swycartographr] prev. coords: (-184.54, 66.7) rot: 170 #[swycartographr] prev. coords: (-209.55, -9.52)

  
  #occc end

##CC-C begin
  #("salt_mine","Salt_Mine",icon_village_a|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(14.2, -31),[]),
  ("salt_mine","Salt_Mine",icon_village_a|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(1, 1),[]),
##CC-C end

  ("four_ways_inn","Four_Ways_Inn",icon_village_a|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(4.8, -39.6),[]),
  ("test_scene","test_scene",icon_village_a|pf_disabled|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(10.8, -19.6),[]),
  #("test_scene","test_scene",icon_village_a|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(10.8, -19.6),[]),
  ("battlefields","battlefields",pf_disabled|icon_village_a|pf_is_static|pf_always_visible|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(10.8, -16.6),[]),
  ("dhorak_keep","Dhorak_Keep",icon_town|pf_disabled|pf_is_static|pf_always_visible|pf_no_label|pf_hide_defenders, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-50,-58),[]),

  ("training_ground","Training Ground",  pf_disabled|icon_training_ground|pf_hide_defenders|pf_is_static|pf_always_visible, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(3, -7),[]),

  ("training_ground_1", "Mercenary Camp",  icon_training_ground|pf_hide_defenders|pf_is_static|pf_always_visible|pf_label_medium, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(37.4, 102.8),[], 100),
  ("training_ground_2", "Mercenary Camp",  icon_training_ground|pf_hide_defenders|pf_is_static|pf_always_visible|pf_label_medium, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-12.8, 33),[], 100),
  ("training_ground_3", "Mercenary Camp",  icon_training_ground|pf_hide_defenders|pf_is_static|pf_always_visible|pf_label_medium, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(70.5, 72.0),[], 100),
  ("training_ground_4", "Mercenary Camp",  icon_training_ground|pf_hide_defenders|pf_is_static|pf_always_visible|pf_label_medium, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(11.5, -75.2),[], 100),
  ("training_ground_5", "Mercenary Camp",  icon_training_ground|pf_hide_defenders|pf_is_static|pf_always_visible|pf_label_medium, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-125.8, 12.5),[], 100),


#  bridge_a
  ("Bridge_1","{!}1",icon_bridge_snow_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(39.37, 65.10),[], -44.8),
  ("Bridge_2","{!}2",icon_bridge_snow_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(56.44, 77.88),[], 4.28),
  ("Bridge_3","{!}3",icon_bridge_snow_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(70.87, 87.95),[], 64.5),
  ("Bridge_4","{!}4",icon_bridge_snow_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(93.71, 62.13),[], -2.13),
  ("Bridge_5","{!}5",icon_bridge_snow_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(11.02, 72.61),[], 21.5),
  ("Bridge_6","{!}6",icon_bridge_b|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-8.83, 52.24),[], -73.5),
  ("Bridge_7","{!}7",icon_bridge_b|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-29.79, 76.84),[], -64),
  ("Bridge_8","{!}8",icon_bridge_b|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-64.05, -6),[], 1.72),
  ("Bridge_9","{!}9",icon_bridge_b|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-64.95, -9.60),[], -33.76),
  ("Bridge_10","{!}10",icon_bridge_b|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-75.32, -75.27),[], -44.07),
  ("Bridge_11","{!}11",icon_bridge_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-24.39, 67.82),[], 81.3),
  ("Bridge_12","{!}12",icon_bridge_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-114.33, -1.94),[], -35.5),
  ("Bridge_13","{!}13",icon_bridge_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-84.02, -7),[], -17.7),
  ("Bridge_14","{!}14",icon_bridge_a|pf_is_static|pf_always_visible|pf_no_label, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(-23.36, 75.8),[], 66.6),

  ("looter_spawn_point"   ,"{!}looter_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(26, 77),[(trp_looter,15,0)]),
  ("steppe_bandit_spawn_point"  ,"the steppes",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(125, 9),[(trp_looter,15,0)]),
  ("taiga_bandit_spawn_point"   ,"the tundra",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(78, 84),[(trp_looter,15,0)]),
##  ("black_khergit_spawn_point"  ,"black_khergit_sp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(47.1, -73.3),[(trp_looter,15,0)]),
  ("forest_bandit_spawn_point"  ,"the forests",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-35, 18),[(trp_looter,15,0)]),
  ("mountain_bandit_spawn_point","the highlands",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-90, -26.8),[(trp_looter,15,0)]),
## CC begin
  ("sea_raider_spawn_point_1"   ,"the coast",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(13.5, 91.1),[(trp_looter,15,0)]),
  ("sea_raider_spawn_point_2"   ,"the coast",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-12.5, 110),[(trp_looter,15,0)]),
## CC end
  ("desert_bandit_spawn_point"  ,"the deserts",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(110, -100),[(trp_looter,15,0)]),
 # add extra towns before this point
 #occc
  ("sea_raider_ship_spawn_point"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(-171, 13),[(trp_looter,15,0)]),
  ("albion_bandit_spawn_point"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(-224, 9),[(trp_looter,15,0)]),
  ("taikou_scout_spawn_point"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(173, -32),[(trp_looter,15,0)]),
  ("amazons_spawn_point"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0, -123),[(trp_looter,15,0)]),
  ("calrador_spawn_point"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(-220, 58),[(trp_looter,15,0)]),
  ("undead_legio_spawn_point"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(-96, -64),[(trp_looter,15,0)]),
  ("wardogs_spawn_point"  ,"wardogs",pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(-158, -32),[]),
  ("valkyries_spawn_point"  ,"valkyries",pf_disabled|pf_is_static, no_menu, pt_none, fac_valhalla,0,ai_bhvr_hold,0,(116, 101),[]), ##### ADD MP
  ("borcha_legion_spawn_point"  ,"borcha_legion",pf_disabled|pf_is_static, no_menu, pt_none, fac_valhalla,0,ai_bhvr_hold,0,(-158, -32),[]), ##### ADD MP

  ("spawn_points_end"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("reserved_1"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("reserved_2"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("reserved_3"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("reserved_4"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("reserved_5"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  
##occc start
  ("occc_jomsborg" ,"Jomsborg",icon_castle_c|pf_is_static|pf_hide_defenders,no_menu,pt_none,fac_commoners,0,ai_bhvr_hold,0,(-140.50,121),[],340),
  ("occc_slaver_camp", "Slave Market",  icon_training_ground|pf_hide_defenders|pf_is_static, no_menu, pt_none, fac_neutral,0,ai_bhvr_hold,0,(150.0, -129.49),[], 176), #[swycartographr] prev. coords: (150, -128) rot: 100
  ("occc_rhodok_legio_camp"  ,"Rhodok Legion Camp",pf_disabled|pf_is_static, no_menu, pt_none, fac_outlaws,0,ai_bhvr_hold,0,(-35, 18),[(trp_looter,15,0)]),

#religions buildings
  ("occc_reli_1"                  ,"Saint Cross Religious House",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("occc_reli_2"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("occc_reli_3"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("occc_reli_4"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("occc_reli_5"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("occc_reli_6"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("occc_reli_7"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  ("occc_reli_8"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(0., 0),[(trp_looter,15,0)]),
  
  #("occc_island_nazis"                  ,"{!}last_spawn_point",    pf_disabled|pf_is_static, no_menu, pt_none, fac_commoners,0,ai_bhvr_hold,0,(-230, 82),[(trp_looter,15,0)]),

##occc end
  ]
# modmerger_start version=201 type=2
try:
    component_name = "parties"
    var_set = { "parties" : parties }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end

from header_common import *
from header_parties import *
from ID_troops import *
from ID_factions import *
from ID_map_icons import *

pmf_is_prisoner = 0x0001
#pf_manor = icon_manor_icon|pf_label_small|pf_is_static|pf_hide_defenders

####################################################################################################################
#  Each party template record contains the following fields:
#  1) Party-template id: used for referencing party-templates in other files.
#     The prefix pt_ is automatically added before each party-template id.
#  2) Party-template name.
#  3) Party flags. See header_parties.py for a list of available flags
#  4) Menu. ID of the menu to use when this party is met. The value 0 uses the default party encounter system.
#  5) Faction
#  6) Personality. See header_parties.py for an explanation of personality flags.
#  7) List of stacks. Each stack record is a tuple that contains the following fields:
#    7.1) Troop-id. 
#    7.2) Minimum number of troops in the stack. 
#    7.3) Maximum number of troops in the stack. 
#    7.4) Member flags(optional). Use pmf_is_prisoner to note that this member is a prisoner.
#     Note: There can be at most 6 stacks.
####################################################################################################################


party_templates = [
  ("none","none",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("rescued_prisoners","Rescued Prisoners",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
  ("enemy","Enemy",icon_gray_knight,0,fac_undeads,merchant_personality,[]),
  ("hero_party","Hero Party",icon_gray_knight,0,fac_commoners,merchant_personality,[]),
####################################################################################################################
# Party templates before this point are hard-wired into the game and should not be changed. 
####################################################################################################################
##  ("old_garrison","Old Garrison",icon_vaegir_knight,0,fac_neutral,merchant_personality,[]),
  ("village_defenders","Village Defenders",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,10,20),(trp_peasant_woman,0,4)]),
  ("cattle_herd","Cattle Herd",icon_cattle|carries_goods(10),0,fac_neutral,merchant_personality,[(trp_cattle,80,120)]),

##  ("vaegir_nobleman","Vaegir Nobleman",icon_vaegir_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_vaegir_knight,2,6),(trp_vaegir_horseman,4,12)]),
##  ("swadian_nobleman","Swadian Nobleman",icon_gray_knight|carries_goods(10)|pf_quest_party,0,fac_commoners,merchant_personality,[(trp_nobleman,1,1),(trp_swadian_knight,2,6),(trp_swadian_man_at_arms,4,12)]),
# Ryan BEGIN
  ("looters","Looters",icon_axeman|carries_goods(8),0,fac_outlaws,bandit_personality,[(trp_looter,3,45)]),
# Ryan END
#Riurik_survivors_clan
  ("manhunters","Manhunters",icon_gray_knight,0,fac_manhunters,soldier_personality,[(trp_slaver_chief,1,1), (trp_slave_hunter,3,10), (trp_manhunter,9,40)]),
##  ("peasant","Peasant",icon_peasant,0,fac_commoners,merchant_personality,[(trp_farmer,1,6),(trp_peasant_woman,0,7)]),

## CC begin
#occc start kara khergits

  ("black_khergit_nomads","Black Khergit Nomads",icon_khergit_horseman_b|carries_goods(2),0,fac_black_khergits,merchant_personality,[(trp_black_khergit_lancer,1,6),(trp_black_khergit_guard,2,15),(trp_black_khergit_horseman,2,18),(trp_occc_black_khergit_nomad,6,28)]),
  ("black_khergit_bandits","Black Khergit Bandits",icon_khergit_horseman_b|carries_goods(2),0,fac_black_khergits,bandit_personality,[(trp_occc_black_khergit_baatur,1,6),(trp_black_khergit_guard,2,15),(trp_black_khergit_lancer,2,18),(trp_black_khergit_horseman,6,28)]),
  ("black_khergit_raiders","Black Khergit Raiders",icon_khergit_horseman_b|carries_goods(2),0,fac_black_khergits,bandit_personality,[(trp_occc_black_khergit_baatur,1,6),(trp_black_khergit_guard,2,15),(trp_black_khergit_lancer,2,18),(trp_black_khergit_horseman,6,28)]),
  ("black_khergit_warband","Black Khergit Warband",icon_khergit_horseman_b|carries_goods(2),0,fac_black_khergits,bandit_personality,[(trp_occc_black_khergit_ataman,1,3),(trp_occc_black_khergit_baatur,2,5),(trp_occc_black_khergit_mergen,2,5),(trp_black_khergit_guard,2,15),(trp_black_khergit_lancer,2,15),(trp_black_khergit_horseman,12,48)]),
  ("black_khergit_army","Black Khergit Army",icon_khergit_horseman_b|carries_goods(2),0,fac_black_khergits,bandit_personality,[(trp_occc_black_khergit_ataman,1,12),(trp_occc_black_khergit_baatur,25,50),(trp_occc_black_khergit_mergen,25,50),(trp_black_khergit_guard,1,12),(trp_black_khergit_lancer,100,220),(trp_black_khergit_horseman,180,420)]),

#occc end

  ("dark_hunters","Dark Hunters",icon_gray_knight,0,fac_dark_knights,soldier_personality,[(trp_dark_knight,4,42),(trp_dark_sniper,10,20),(trp_dark_hunter,13,25)]),
  #normal bandits begin
#  ("forest_bandits","Forest Bandits",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_forest_bandit,2,10), (trp_forest_bandit,12,52)]),
  ("forest_bandits","Forest Bandits",icon_archer_bandit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_forest_bandit,2,10),(trp_forest_bandit,4,75)]),
  ("taiga_bandits","Tundra Bandits",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_taiga_bandit,4,90)]),
#  ("steppe_bandits","Steppe Bandits",icon_khergit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_steppe_bandit,2,11), (trp_steppe_bandit,12,58)]),
  ("steppe_bandits","Steppe Bandits",icon_khergit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_steppe_bandit,2,11),(trp_steppe_bandit,4,80)]),
#  ("sea_raiders","Sea Raiders",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_sea_raider,3,10), (trp_sea_raider,15,50)]),
  ("sea_raiders","Sea Raiders",icon_sea_raider|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_sea_raider,3,10),(trp_sea_raider,5,60)]),
  ("mountain_bandits","Mountain Bandits",icon_horse_bandit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_mountain_bandit_rhodok,5,70)]),
#  ("desert_bandits","Desert Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_desert_bandit,2,11), (trp_desert_bandit,12,58)]),
  ("desert_bandits","Desert Bandits",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_desert_bandit,8,95), (trp_ccc_swadian_musket,1,30)]),
## CC end
  ("deserters","Deserters",icon_vaegir_knight|carries_goods(3),0,fac_deserters,bandit_personality,[]),
#occc start
  ("occc_roaming_looter_party", "Outlaws", icon_axeman, 0, fac_outlaws, 0, [(trp_brigand,2,6),(trp_looter,5,12),(trp_bandit,9,11),]),
  ("occc_roaming_knights_party", "Robber Knights", icon_gray_knight, 0, fac_outlaws, 0, [(trp_occc_robber_knight,2,6),(trp_ccd_bandit_cavelry,5,12),(trp_brigand,9,11),]),
  ("occc_amazon_bandit","Amazons",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_occc_amazon_archer_cavalry,3,6),(trp_occc_amazon_archer,5,15),(trp_occc_amazon_huntress,10,38)]),
  ("taiga_bandits_classic","Tundra Bandits",icon_horse_bandit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_taiga_bandit_classic,2,11), (trp_taiga_bandit_classic,12,58)]),
  ("mountain_bandits_classic","Mountain Bandits",icon_horse_bandit|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_mountain_bandit_classic,2,12), (trp_mountain_bandit,12,60)]),

  #normal bandits end
  ("occc_slaver_party","Slavers",icon_gray_knight,0,fac_slavers,bandit_personality,[(trp_occc_elite_slaver,1,1),(trp_slaver_chief,2,3), (trp_slave_hunter,3,10), (trp_manhunter,9,40),(trp_ccc_slave_man,2,10,pmf_is_prisoner),(trp_ccc_slave_woman,2,5,pmf_is_prisoner)]),
  ("occc_sea_raider_ship","Sea Raiders Ship",icon_ship|pf_is_ship|carries_goods(2),0,fac_outlaws,bandit_personality,[(trp_chief_sea_raider,3,10),(trp_sea_raider,5,60)]),#unused
#occc end
#CC-C begin
  #("merchant_caravan","Merchant Caravan",icon_gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,6,15),(trp_watchman,4,10)]), ## CC
  ("merchant_caravan","Merchant Caravan",icon_gray_knight|carries_goods(20)|pf_auto_remove_in_town|pf_quest_party,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,20),(trp_watchman,5,12)]),#occc 25->20 15->12
#CC-C end
  ("troublesome_bandits","Troublesome Bandits",icon_axeman|carries_goods(9)|pf_quest_party,0,fac_outlaws,bandit_personality,[(trp_bandit,14,55)]),
  ("bandits_awaiting_ransom","Bandits Awaiting Ransom",icon_axeman|carries_goods(9)|pf_auto_remove_in_town|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_bandit,24,58),(trp_kidnapped_girl,1,1,pmf_is_prisoner)]),
  ("kidnapped_girl","Kidnapped Girl",icon_woman|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_kidnapped_girl,1,1)]),
#CC-C begin
  #("village_farmers","Village Farmers",icon_peasant|pf_civilian,0,fac_innocents,merchant_personality,[(trp_farmer,5,10),(trp_peasant_woman,3,8)]),
  ("village_farmers","Village Farmers",icon_peasant|pf_civilian,0,fac_innocents,merchant_personality,[(trp_farmer,5,25),(trp_peasant_woman,5,18)]),
#CC-C end
  ("spy_partners", "Unremarkable Travellers", icon_gray_knight|carries_goods(10)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy_partner,1,1),(trp_caravan_guard,5,11)]),
  ("runaway_serfs","Runaway Serfs",icon_peasant|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_farmer,6,7), (trp_peasant_woman,3,3)]),
  ("spy", "Ordinary Townsman", icon_gray_knight|carries_goods(4)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_spy,1,1)]),
  ("sacrificed_messenger", "Sacrificed Messenger", icon_gray_knight|carries_goods(3)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[]),
##  ("conspirator", "Conspirators", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator,3,4)]),
##  ("conspirator_leader", "Conspirator Leader", icon_gray_knight|carries_goods(8)|pf_default_behavior|pf_quest_party,0,fac_neutral,merchant_personality,[(trp_conspirator_leader,1,1)]),
##  ("peasant_rebels", "Peasant Rebels", icon_peasant,0,fac_peasant_rebels,bandit_personality,[(trp_peasant_rebel,33,97)]),
##  ("noble_refugees", "Noble Refugees", icon_gray_knight|carries_goods(12)|pf_quest_party,0,fac_noble_refugees,merchant_personality,[(trp_noble_refugee,3,5),(trp_noble_refugee_woman,5,7)]),

  ("forager_party","Foraging Party",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("scout_party","Scouts",icon_gray_knight|carries_goods(1)|pf_show_faction,0,fac_commoners,bandit_personality,[]),
  ("patrol_party","Patrol",icon_gray_knight|carries_goods(2)|pf_show_faction,0,fac_commoners,soldier_personality,[]),
#  ("war_party", "War Party",icon_gray_knight|carries_goods(3),0,fac_commoners,soldier_personality,[]),
  ("messenger_party","Messenger",icon_gray_knight|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("raider_party","Raiders",icon_gray_knight|carries_goods(16)|pf_quest_party,0,fac_commoners,bandit_personality,[]),
  ("raider_captives","Raider Captives",0,0,fac_commoners,0,[(trp_peasant_woman,6,30,pmf_is_prisoner)]),
  ("kingdom_caravan_party","Caravan",icon_mule|carries_goods(25)|pf_show_faction,0,fac_commoners,merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,15,30)]), #CC-C 50->80
  ("prisoner_train_party","Prisoner Train",icon_gray_knight|carries_goods(5)|pf_show_faction,0,fac_commoners,merchant_personality,[]),
  ("default_prisoners","Default Prisoners",0,0,fac_commoners,0,[(trp_bandit,5,10,pmf_is_prisoner)]),

  ("routed_warriors","Routed Enemies",icon_vaegir_knight,0,fac_commoners,soldier_personality,[]),


# Caravans
  ("center_reinforcements","Reinforcements",icon_axeman|carries_goods(16),0,fac_commoners,soldier_personality,[(trp_townsman,5,30),(trp_watchman,4,20)]),  

  ("kingdom_hero_party","{!}War Party",icon_flagbearer_a|pf_show_faction|pf_default_behavior,0,fac_commoners,soldier_personality,[]),
  
# Reinforcements
  # each faction includes three party templates. One is less-modernised, one is med-modernised and one is high-modernised
  # less-modernised templates are generally includes 7-14 troops in total, 
  # med-modernised templates are generally includes 5-10 troops in total, 
  # high-modernised templates are generally includes 3-5 troops in total

#CC-C begin
################################################################################
#Player Faction
################################################################################
  ("player_supporters_faction_reinforcements_a", "{!}psf_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_custom_recruit,3,14),(trp_custom_infantry,2,5)]),
  ("player_supporters_faction_reinforcements_b", "{!}psf_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_custom_sharpshooter,2,5),(trp_custom_skirmisher,4,6)]),
  ("player_supporters_faction_reinforcements_c", "{!}psf_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_custom_squire,2,4),(trp_custom_knight,1,2)]),

## NMC
  ("player_supporters_faction_lord_reinf_a", "{!}player_supporters_faction_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_custom_recruit,3,8),(trp_custom_infantry,3,5)]),
  ("player_supporters_faction_lord_reinf_b", "{!}player_supporters_faction_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_custom_sharpshooter,2,4),(trp_custom_skirmisher,2,5)]),
  ("player_supporters_faction_lord_reinf_c", "{!}player_supporters_faction_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_custom_squire,1,2),(trp_custom_knight,2,3)]),
## NMC
################################################################################
#Swadian
################################################################################
  ("kingdom_1_reinforcements_a", "{!}kingdom_1_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_swadian_militia,6,10),(trp_swadian_infantry,3,8)],),  ## CC-D 5->6 OCCC 3->2->3
  #("kingdom_1_reinforcements_b", "{!}kingdom_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_swadian_man_at_arms,3,5),(trp_swadian_skirmisher,3,5)]),  ## CC-D (trp_swadian_crossbowman,3,5),->(trp_swadian_man_at_arms,3,5),
  ("kingdom_1_reinforcements_b", "{!}kingdom_1_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_swadian_man_at_arms,1,2),(trp_swadian_skirmisher,3,6),(trp_swadian_crossbowman,1,2),]),	#occc
  ("kingdom_1_reinforcements_c", "{!}kingdom_1_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_swadian_man_at_arms,1,2),(trp_swadian_knight,2,4),(trp_ccc_swadian_lancer_knight,0,1)]),

## CC-D begin: +CC
  ("kingdom_1_lord_reinf_a", "{!}kingdom_1_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_swadian_recruit,3,8),(trp_swadian_militia,3,5)]),
  ("kingdom_1_lord_reinf_b", "{!}kingdom_1_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_swadian_crossbowman,2,4),(trp_swadian_footman,2,5)]),
  ("kingdom_1_lord_reinf_c", "{!}kingdom_1_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_swadian_man_at_arms,3,5)]),
## CC-D end

  ("el_trp_kingdom_1_lord","{!}EL",0,0,fac_commoners,0,[(trp_ccc_swadian_lancer_knight,1,3),(trp_swadian_knight,1,3),(trp_occc_swadian_elite_foot_knight,1,2),(trp_swadian_infantry,1,2),(trp_swadian_militia,5,12),(trp_ccc_swadian_guards_knight,1,1),]),
  ("el_trp_knight_1_2","{!}EL",0,0,fac_commoners,0,[(trp_ccc_swadian_musket_cave,2,6),(trp_occc_swadian_landsknecht,3,7),(trp_occc_swadian_doppelsoldnar,1,3)]),
  ("el_trp_knight_1_7","{!}EL",0,0,fac_commoners,0,[(trp_swadian_man_at_arms,2,3),(trp_swadian_knight,2,3),(trp_ccc_swadian_elite_knight,1,2),(trp_ccc_swadian_lancer_knight,1,2)]),
  ("el_trp_knight_1_8","{!}EL",0,0,fac_commoners,0,[(trp_occc_swadian_jinete,1,2),(trp_ccc_swadian_conquistador_cave,1,3),(trp_ccc_swadian_musket_cave,4,8),(trp_ccc_swadian_heavy_musket_cave,2,4)]),  ## cdnCavemm 
  

  ("heinrich_party", "{!}EL", 0, 0, fac_commoners, 0, [(trp_ritterbruder,1,2),(trp_occc_ironcross_sergeant,3,8),(trp_occc_ironcross_crossbowman,3,8),(trp_swadian_ironcross_foot_knight,2,3),(trp_swadian_veteran_ironcross_knight,2,3)] ),
  ("occc_ulrich_party", "{!}EL", 0, 0, fac_commoners, 0, [(trp_ritterbruder,1,3),(trp_occc_ironcross_sergeant,3,8),(trp_occc_ironcross_crossbowman,3,8),(trp_swadian_ironcross_squire,2,7),(trp_swadian_ironcross_knight,2,4)] ),

  ("occc_helvetia_guards", "{!}kingdom_1_reinforcements_ex", 0, 0, fac_commoners, 0, [(trp_occc_helvetia_guard,2,3)]),

################################################################################
#Vaegir
################################################################################
  ("kingdom_2_reinforcements_a", "{!}kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_line_inf,6,10),(trp_ccc_vaegir_recruit,4,8)]),  ## CC-D 5->6 8->9
  ("kingdom_2_reinforcements_b", "{!}kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_recruit,4,5),(trp_ccc_vaegir_elite_support_inf,1,2),(trp_ccc_vaegir_sniper,1,2)]),  ## cdnCavemm
  ("kingdom_2_reinforcements_c", "{!}kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_sabre_cavalry,3,4),(trp_ccc_vaegir_red_coat_cavalry,1,2)]),

## CC-D begin: +CC
  ("kingdom_2_lord_reinf_a", "{!}kingdom_2_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_line_inf,3,8),(trp_ccc_vaegir_recruit,3,5)]),
  ("kingdom_2_lord_reinf_b", "{!}kingdom_2_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_support_inf,2,4),(trp_ccc_vaegir_sniper,2,5)]),  ## cdnCavemm
  ("kingdom_2_lord_reinf_c", "{!}kingdom_2_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_sabre_cavalry,3,5)]),
## CC-D end

  ("el_trp_kingdom_2_lord","{!}EL",0,0,fac_commoners,0,[(trp_ccc_vaegir_red_coat_line_inf,15,30),(trp_ccc_vaegir_grenadier_inf,5,12),(trp_occc_vaegir_dragoon_de_la_garde,2,5),(trp_occc_vaegir_cavalry_grenadier,6,9),]),
  ("el_trp_knight_2_1","{!}EL",0,0,fac_commoners,0,[(trp_occc_vaegir_red_coat,15,30),(trp_occc_vaegir_red_coat_cav,8,12)]),  ## OCCC 
  ("el_trp_knight_2_2","{!}EL",0,0,fac_commoners,0,[(trp_ccc_vaegir_legend_gunman_2,8,15),(trp_occc_vaegir_red_coat_cav,2,3),(trp_ccc_vaegir_western_people_2,1,2),(trp_ccc_vaegir_gunman_2,8,15),]),  ## OCCC
  ("el_trp_knight_2_3","{!}EL",0,0,fac_commoners,0,[(trp_vaegir_footman,5,6),(trp_vaegir_archer,3,4),(trp_vaegir_horseman,1,2),(trp_ccc_vaegir_guardian,2,3),(trp_ccc_vaegir_guardian_halberd,1,3),(trp_ccc_vaegir_guardian_knight,1,2),]),
  ("el_trp_knight_2_ney","{!}EL",0,0,fac_commoners,0,[(trp_occc_vaegir_cavalry_grenadier,10,20)]),  ## OCCC 
  ("el_trp_knight_2_21","{!}EL",0,0,fac_commoners,0,[(trp_ccc_vaegir_elite_support_inf,8,15),(trp_ccc_vaegir_cowboy_2,2,3),(trp_ccc_vaegir_shotgun_man,2,3),(trp_ccc_vaegir_legend_gunman,2,3),(trp_ccc_vaegir_support_inf,8,15),]),  ## cdnCavemm
################################################################################
#Khergit
################################################################################
  ("kingdom_3_reinforcements_a", "{!}kingdom_3_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_khergit_skirmisher,2,6),(trp_khergit_tribesman,6,13)]),
  ("kingdom_3_reinforcements_b", "{!}kingdom_3_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_khergit_horse_archer,2,5),(trp_khergit_skirmisher,4,5)]),
  ("kingdom_3_reinforcements_c", "{!}kingdom_3_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_khergit_lancer,2,4),(trp_ccc_khergit_manghit,0,1),(trp_khergit_veteran_horse_archer,2,3)]),
  
## CC-D begin: +CC
  ("kingdom_3_lord_reinf_a", "{!}kingdom_3_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_khergit_tribesman,3,8),(trp_khergit_skirmisher,3,5)]),
  ("kingdom_3_lord_reinf_b", "{!}kingdom_3_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_khergit_horseman,3,6),(trp_khergit_horse_archer,2,4)]),
  ("kingdom_3_lord_reinf_c", "{!}kingdom_3_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_khergit_lancer,1,2),(trp_khergit_horseman,1,2),(trp_khergit_veteran_horse_archer,1,2)]),
## CC-D end

  ("el_trp_kingdom_3_lord","{!}EL",0,0,fac_commoners,0,[(trp_ccc_khergit_manghit,3,5),(trp_occc_khergit_khorchen,3,5),(trp_ccc_khergit_elite_lancer,3,5),(trp_khergit_veteran_horse_archer,4,5),]),
################################################################################
#Nords
################################################################################
  ("kingdom_4_reinforcements_a", "{!}kingdom_4_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_nord_footman,4,14),(trp_nord_recruit,4,12),]),
  ("kingdom_4_reinforcements_b", "{!}kingdom_4_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_nord_archer,1,3),(trp_nord_veteran,1,4),(trp_ccc_nord_long_bow,2,3)]),
  ("kingdom_4_reinforcements_c", "{!}kingdom_4_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_ccc_nord_barbarian_great,2,2),(trp_ccc_nord_barbarian_legend,1,2),(trp_nord_champion,2,4),(trp_ccc_nord_elite_huscarl,1,1)]),  ## OCCC 5->2 8->4
  
## CC-D begin: +CC
  ("kingdom_4_lord_reinf_a", "{!}kingdom_4_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_nord_footman,4,8),(trp_nord_huntsman,2,5)]),
  ("kingdom_4_lord_reinf_b", "{!}kingdom_4_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_nord_trained_footman,3,7),(trp_nord_archer,2,3)]),
  ("kingdom_4_lord_reinf_c", "{!}kingdom_4_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_nord_veteran,1,3),(trp_nord_warrior,2,4)]),
## CC-D end ccc_nord_elite_huscarl


  ("el_trp_knight_dovahkiin","{!}EL",0,0,fac_commoners,0,[(trp_ccc_valkyrie_knight,2,5),(trp_ccc_nord_einherjar,4,6),(trp_ccc_valkyrie_recruit,2,5),(trp_nord_recruit,6,9),(trp_ccc_valkyrie_archer,2,4)]),
  ("el_trp_knight_4_19","{!}EL",0,0,fac_commoners,0,[(trp_occc_nord_veteran_long_bow,1,2),(trp_ccc_nord_long_bow,1,5),(trp_nord_footman,2,3),(trp_nord_recruit,4,8),(trp_occc_nord_shieldmaiden,1,4)]),
  ("el_trp_knight_4_5a6a7","{!}EL",0,0,fac_commoners,0,[(trp_ccc_nord_barbarian_great_cave,14,28),(trp_ccc_nord_barbarian_legend_cave,4,8),(trp_occc_nord_berserk,2,3),]),
################################################################################
#Rhodok
################################################################################
  ("kingdom_5_reinforcements_a", "{!}kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes,1,2),(trp_ccc_rhodok_hastati,1,3),(trp_ccc_rhodok_tribesman,4,16)]),
  ("kingdom_5_reinforcements_b", "{!}kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes_spear,1,2),(trp_ccc_rhodok_principes,1,3),(trp_ccc_rhodok_equites,1,2),(trp_ccc_rhodok_trained_crossbowman,2,4),(trp_ccc_rhodok_principes_archar,1,2)]),
  ("kingdom_5_reinforcements_c", "{!}kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_triarii,3,4),(trp_ccc_rhodok_triarii_knight,1,3),(trp_occc_rhodok_scorpio,1,1)]),

## CC-D begin: +CC
  ("kingdom_5_lord_reinf_a", "{!}kingdom_5_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes,4,8),(trp_ccc_rhodok_tribesman,2,5)]),
  ("kingdom_5_lord_reinf_b", "{!}kingdom_5_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes,2,4),(trp_ccc_rhodok_trained_crossbowman,3,6)]),
  ("kingdom_5_lord_reinf_c", "{!}kingdom_5_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_triarii,1,2),(trp_ccc_rhodok_triarii_knight,2,3)]),
## CC-D end

  ("el_trp_knight_5_18","{!}EL",0,0,fac_commoners,0,[(trp_occ_rhodok_gladiator,1,3),(trp_ccc_rhodok_principes,1,4),(trp_ccc_rhodok_tribesman,4,14),(trp_ccc_rhodok_crossbowman,2,4),(trp_ccc_rhodok_equites,1,2)]),
  ("el_trp_knight_5_21","{!}EL",0,0,fac_commoners,0,[(trp_ccd_rhodok_praetoriani,3,5),(trp_ccc_rhodok_triarii,5,8),(trp_ccc_rhodok_triarii_knight,1,3),(trp_ccc_rhodok_hastati,1,3),(trp_occc_rhodok_scorpio,1,2)]),
  ("occc_germanicus_party","{!}EL",0,0,fac_commoners,0,[(trp_ccd_rhodok_praetoriani,3,5),(trp_ccc_rhodok_hastati,5,8),(trp_ccc_rhodok_principes,1,3),(trp_ccc_rhodok_principes_spear,1,3),(trp_ccc_rhodok_principes_archar,2,4)]),
  
###Late romans start
  ("el_beli_cataphracts","{!}EL",0,0,fac_commoners,0,[(trp_occc_rhodok_late_palatina_guard,1,2),(trp_occc_rhodok_late_elite_legio,2,4),(trp_ccc_rhodok_principes_pistol,6,10),(trp_occc_rhodok_late_legio,5,6),(trp_occc_rhodok_clibanarii,2,4)]),
  ("el_stilicho_late_western_roman","{!}EL",0,0,fac_commoners,0,[(trp_occc_rhodok_herculiani_seniores,2,4),(trp_occc_rhodok_late_scholae_palatinae,2,3),(trp_ccc_rhodok_principes_pistol,2,3),(trp_occc_rhodok_late_ballistarii,2,4),(trp_occc_rhodok_late_legio,2,4),(trp_nord_trained_footman,3,5)]),
  ("el_aetius_late_western_roman","{!}EL",0,0,fac_commoners,0,[(trp_occc_rhodok_late_palatina_guard,2,3),(trp_occc_rhodok_late_scholae_palatinae,2,3),(trp_occc_rhodok_late_skirmisher,2,4),(trp_occc_rhodok_late_legio,2,4),(trp_occc_rhodok_late_spearman,4,6),(trp_khergit_horseman,3,4),]),
###Late romans end
  
  ("kingdom_5_praetorianguards", "{!}kingdom_5_reinforcements_ex", 0, 0, fac_commoners, 0, [(trp_ccd_rhodok_praetoriani,1,3),(trp_occc_rhodok_varanger,1,2),(trp_occc_rhodok_greekfireman,0,1)]),

  ("kingdom_5_late_reinforcements_a", "{!}kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_occc_rhodok_late_legio,1,2),(trp_occc_rhodok_late_cohors,1,3),(trp_occc_rhodok_late_tribesman,4,16)]),
  ("kingdom_5_late_reinforcements_b", "{!}kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_hastati_rifle,1,2),(trp_occc_rhodok_late_legio,1,3),(trp_occc_rhodok_late_equites_promoti,1,2),(trp_occc_rhodok_late_skirmisher,2,4),(trp_occc_rhodok_late_ballistarii_lesser,1,2)]),
  ("kingdom_5_late_reinforcements_c", "{!}kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_occc_rhodok_late_elite_legio,2,3),(trp_occc_rhodok_clibanarii,1,1),(trp_occc_rhodok_late_scholae_palatinae,1,3),(trp_ccc_rhodok_principes_pistol,1,2)]),

################################################################################
#Sarranid
################################################################################
  ("kingdom_6_reinforcements_a", "{!}kingdom_6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sarranid_komono,3,7),(trp_sarranid_recruit,3,10)]),                ## cdnCavemm
  ("kingdom_6_reinforcements_b", "{!}kingdom_6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sarranid_yumi_ashigaru,4,6),(trp_sarranid_sanpei_ashigaru,4,7)]),  ## cdnCavemm
  ("kingdom_6_reinforcements_c", "{!}kingdom_6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sarranid_bushi,3,6),(trp_occc_kamikazewarrior,1,2),(trp_occc_masuraowarrior,1,2)]),                                             ## cdnCavemm

## CC-D begin: +CC
  ("kingdom_6_lord_reinf_a", "{!}kingdom_6_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_sarranid_recruit,3,8),(trp_sarranid_footman,3,5)]),
  ("kingdom_6_lord_reinf_b", "{!}kingdom_6_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_sarranid_archer,2,4),(trp_sarranid_veteran_footman,2,5)]),
  ("kingdom_6_lord_reinf_c", "{!}kingdom_6_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_sarranid_mamluke,2,3),(trp_ccc_sarranid_amir,1,2),(trp_ccc_rhodok_triarii_revolver,1,1)]),
## CC-D end

  ("kingdom_6_lord_naffatun", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_sarranid_naffatun,1,3),(trp_occc_sarranid_ghulam,2,3),(trp_occc_sarranid_camel_archer,2,3),(trp_sarranid_master_archer,3,5),(trp_sarranid_recruit2,5,8)]),
  ("kingdom_6_lord_ghulam", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_sarranid_loyal_rider,3,4),(trp_occc_sarranid_ghulam,4,6),(trp_occc_sarranid_camel_archer,2,3),(trp_sarranid_veteran_footman,3,5),(trp_sarranid_recruit2,8,15)]),

  ("kingdom_6_lord_baibars", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_sarranid_amir,3,4),(trp_occc_sarranid_loyal_rider,4,6),(trp_occc_sarranid_ghulam,2,3),(trp_ccc_rhodok_triarii_revolver,3,5),(trp_sarranid_recruit2,8,15)]),
  # trp_occc_sarranid_naffatun
  
  ("kingdom_6_lord_ninjas", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_sarranid_mounted_assassin,3,6),]),
  
################################################################################
#Classic Sarranid
################################################################################
 ("kingdom_6b_reinforcements_a", "{!}kingdom_6_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sarranid_footman,3,7),(trp_sarranid_recruit2,3,10)]),
 ("kingdom_6b_reinforcements_b", "{!}kingdom_6_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_ccc_sarranid_yeniceri,3,5),(trp_sarranid_archer,3,5),(trp_sarranid_skirmisher,3,6)]),
 ("kingdom_6b_reinforcements_c", "{!}kingdom_6_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_ccc_sarranid_elite_yeniceri,1,2),(trp_sarranid_mamluke,2,5),(trp_ccc_sarranid_amir,0,1),(trp_ccc_rhodok_triarii_revolver,1,1)]),#

################################################################################
#Dark knight
################################################################################
  ("kingdom_7_reinforcements_a", "{!}kingdom_7_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_recruit_troop,3,5),(trp_ccc_dark_knight_tribesman,5,12)]),
  ("kingdom_7_reinforcements_b", "{!}kingdom_7_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_militia,4,7),(trp_ccc_dark_knight_rifle,2,3),(trp_ccc_dark_knight_skirmishers,1,1)]),
  ("kingdom_7_reinforcements_c", "{!}kingdom_7_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_black_rider,1,2),(trp_ccc_dark_knight_monster_rider,1,2)]),

## CC-D begin: +CC
  ("kingdom_7_lord_reinf_a", "{!}kingdom_7_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_recruit_troop,3,8),(trp_ccc_dark_knight_tribesman,3,5)]),
  ("kingdom_7_lord_reinf_b", "{!}kingdom_7_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_militia,2,4),(trp_ccc_dark_knight_rifle,2,5)]),
  ("kingdom_7_lord_reinf_c", "{!}kingdom_7_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_black_rider,3,5),(trp_ccd_dark_knight_shadow,1,2)]),  ## CC-D
## CC-D end

  ("el_trp_knight_7_1","{!}EL",0,0,fac_kingdom_7,0,[(trp_ccc_dark_knight_skeleton,5,8),(trp_ccc_dark_knight_black_rider,1,2),(trp_ccc_dark_knight_ghost,4,8),(trp_ccc_dark_knight_monster_rider,1,2)]),
  ("el_ccc_random_npc14","{!}EL",0,0,fac_kingdom_7,0,[(trp_ccc_dark_knight_skeleton,5,8),(trp_ccc_dark_knight_black_rider,1,1),(trp_ccc_dark_knight_ghost,2,3),(trp_ccc_dark_knight_monster_rider,0,1)]),
  
  ("el_trp_kingdom_7_lord","{!}EL",0,0,fac_kingdom_7,0,[(trp_ccc_dark_knight_recruit_troop,4,6),(trp_ccc_dark_knight_militia,4,6),(trp_ccc_dark_knight_black_rider,1,2),(trp_ccc_dd_knight,1,2),(trp_ccc_dd_guard,1,2),(trp_ccc_dd_sucut,1,2),]),
  ("el_trp_knight_7_13","{!}EL",0,0,fac_kingdom_7,0,[(trp_ccc_dark_knight_tribesman,5,10),(trp_ccc_dd_knight,1,2),(trp_ccc_dd_sucut,1,2),(trp_ccc_dd_guard,1,2),]),
  
  ("occc_vader_party", "{!}EL", 0, 0, fac_commoners, 0, [(trp_occc_novatrooper,3,9),(trp_occc_imperial_stormtrooper,5,18),] ),

#Other
  ("el_samurai_1","{!}EL",0,0,fac_commoners,0,[(trp_sarranid_yari_taishou,5,8),(trp_sarranid_bushou,1,2),(trp_sarranid_umanori_bushou,1,2)]),  ## cdnCavemm
  
  ("el_valkyrie_normal","{!}EL",0,0,fac_commoners,0,[(trp_ccc_valkyrie_recruit,3,6),(trp_ccc_valkyrie_warrior,1,3),(trp_ccc_valkyrie_archer,2,4),]),
  ("el_sister_normal", "{!}EL", 0, 0, fac_commoners, 0, [(trp_ccc_sister_recruit,3,6),(trp_ccc_sister_swordsman,2,3),(trp_ccc_sister_bayonet,1,3),(trp_ccc_sister_elite_bayonet,1,3),(trp_ccc_sister_knight,1,2)]),
  ("el_yamato_normal","{!}EL",0,0,fac_commoners,0,[(trp_ccc_yamato_asigaru_recruit,5,7),(trp_ccc_yamato_nodati_asigaru,1,2),(trp_ccc_yamato_yari_asigaru,1,2),(trp_ccc_yamato_musket_asigaru,1,2),(trp_ccc_yamato_kiba_samurai,1,2)]),
  ("el_ninjas", "{!}n", 0, 0, fac_commoners, 0, [(trp_ore_shadow_tyuunin,5,12),(trp_ccc_yamato_kunoiti_tyuu,2,6),(trp_ore_shadow_twilightedge,2,4),(trp_ccc_yamato_miko_kagura,2,5),(trp_ccc_yamato_kunoiti,2,10),]),

################################################################################
#Hellas
################################################################################
  ("kingdom_8_reinforcements_a", "{!}kingdom_8_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_occc_hellas_tribesman,3,5),(trp_occc_hellas_spearman,5,12)]),
  ("kingdom_8_reinforcements_b", "{!}kingdom_8_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_khergit_peltastai,4,7),(trp_khergit_thuros_spear,2,3),(trp_khergit_sarissailoi,1,1)]),
  ("kingdom_8_reinforcements_c", "{!}kingdom_8_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_occc_hellas_hypaspists,1,3),(trp_ccc_khergit_hetailoi,1,2)]),

  ("kingdom_8_lord_reinf_a", "{!}kingdom_8_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_occc_hellas_tribesman,3,8),(trp_khergit_peltastai,3,5)]),
  ("kingdom_8_lord_reinf_b", "{!}kingdom_8_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_khergit_thuros_spear,2,4),(trp_khergit_sarissailoi,2,5)]),
  ("kingdom_8_lord_reinf_c", "{!}kingdom_8_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_occc_hellas_hypaspists,3,5),(trp_ccc_khergit_hetailoi,1,2)]),  ## CC-D

 ("el_trp_hellas","{!}EL",0,0,fac_commoners,0,[(trp_khergit_thuros_spear,3,4),(trp_occc_alexander_hetailoi,1,4),(trp_khergit_sarissailoi,2,4),(trp_occc_hellas_spearman,6,9)]),
 ("occc_leonidas_party", "{!}EL", 0, 0, fac_commoners, 0, [(trp_ore_spartanvetwarrior,2,6),(trp_ore_spartanwarrior,4,12),] ),
 ("occc_cynane_party", "{!}EL", 0, 0, fac_commoners, 0, [(trp_occc_hellas_toxotai,3,5),(trp_occc_hellas_cretan,8,12),(trp_occc_hellas_tribesman,4,10),] ),

################################################################################
#Taikou 
################################################################################
  ("kingdom_9_reinforcements_a", "{!}kingdom_9_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_taikou_komono,3,7),(trp_taikou_recruit,3,10),(trp_taikou_yari_ashigaru,1,3)]),                ## cdnCavemm
  ("kingdom_9_reinforcements_b", "{!}kingdom_9_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_taikou_yumi_ashigaru,4,6),(trp_taikou_sanpei_ashigaru,4,7),(trp_taikou_teppou_ashigaru,2,3),]),  ## cdnCavemm
  ("kingdom_9_reinforcements_c", "{!}kingdom_9_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_taikou_bushi,3,6),(trp_taikou_umanori_musha,1,2),(trp_taikou_musha,1,3)]),                                             ## cdnCavemm

## CC-D begin: +CC
  ("kingdom_9_lord_reinf_a", "{!}kingdom_9_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_taikou_recruit,3,8),(trp_taikou_komono,3,5)]),
  ("kingdom_9_lord_reinf_b", "{!}kingdom_9_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_taikou_yumi_ashigaru,2,4),(trp_taikou_yari_ashigaru,2,5)]),
  ("kingdom_9_lord_reinf_c", "{!}kingdom_9_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_taikou_bushi,2,4),(trp_taikou_umanori_musha,2,3)]),
################################################################################
#Sunset 
################################################################################

  ("kingdom_10_reinforcements_a", "{!}kingdom_10_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_sunset_spearman,4,14),(trp_sunset_peasant,4,12),]),
  ("kingdom_10_reinforcements_b", "{!}kingdom_10_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_sunset_archer,1,3),(trp_sunset_warrior,1,4),(trp_sunset_skirmisher,2,3)]),
  ("kingdom_10_reinforcements_c", "{!}kingdom_10_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_sunset_eagle,2,3),(trp_sunset_el_eagle,1,2),(trp_sunset_coyote,2,3),(trp_sunset_jaguar,1,2)]),
  
## CC-D begin: +CC
  ("kingdom_10_lord_reinf_a", "{!}kingdom_10_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_sunset_spearman,4,8),(trp_sunset_huntsman,2,5)]),
  ("kingdom_10_lord_reinf_b", "{!}kingdom_10_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_sunset_warrior,3,7),(trp_sunset_skirmisher,2,3)]),
  ("kingdom_10_lord_reinf_c", "{!}kingdom_10_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_sunset_priest,1,3),(trp_sunset_eagle,2,4)]),
## CC-D end ccc_nord_elite_huscarl

################################################################################
#Classic Rhodok (Zendar=Rhodok)
################################################################################
 ("kingdom_5b_reinforcements_a", "{!}kingdom_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_rhodok_trained_spearman,3,5),(trp_rhodok_spearman,3,6),(trp_rhodok_tribesman,3,6)]),
 ("kingdom_5b_reinforcements_b", "{!}kingdom_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_rhodok_veteran_crossbowman,2,5),(trp_rhodok_trained_crossbowman,2,4),(trp_rhodok_crossbowman,4,6)]),
 ("kingdom_5b_reinforcements_c", "{!}kingdom_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_occc_rhodok_elite_sergeant,1,2),(trp_rhodok_sergeant,2,4),(trp_rhodok_sharpshooter,1,2),(trp_occc_rhodok_arbalester,0,1)]),

  ("kingdom_11_lord_reinf_a", "{!}kingdom_8_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_rhodok_tribesman,3,8),(trp_rhodok_spearman,3,5)]),
  ("kingdom_11_lord_reinf_b", "{!}kingdom_8_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_rhodok_trained_spearman,2,4),(trp_rhodok_trained_crossbowman,2,5)]),
  ("kingdom_11_lord_reinf_c", "{!}kingdom_8_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_rhodok_veteran_crossbowman,3,5),(trp_occc_rhodok_arbalester,1,2)]),  ## OCCC

  ("kingdom11_elite_party", "{!}EL", 0, 0, fac_commoners, 0, [(trp_occc_rhodok_steel_arbalest,3,5),(trp_rhodok_veteran_crossbowman,8,12),(trp_rhodok_spearman,4,10),] ),
  ("kingdom11_wardog_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_wardog_soldier,2,6),(trp_occc_wardog_veteran_soldier,1,3),(trp_occc_wardog_sergeant,1,2),(trp_occc_wardog_archer_sergeant,1,2),(trp_occc_wardog_archer,1,5),]),

 
################################################################################
#Classic Vaegir (Murom=Vaegir)
################################################################################
 ("kingdom_2b_reinforcements_a", "{!}kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_vaegir_veteran,3,5),(trp_vaegir_footman,3,6),(trp_vaegir_recruit,3,6)]),
 ("kingdom_2b_reinforcements_b", "{!}kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_vaegir_marksman,2,5),(trp_vaegir_archer,2,4),(trp_vaegir_skirmisher,4,6)]),
 ("kingdom_2b_reinforcements_c", "{!}kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_vaegir_horseman,2,5),(trp_vaegir_knight,1,2),(trp_occc_vaegir_boyar_sons,1,2)]),

 ("kingdom_12_lord_reinf_a", "{!}kingdom_12_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_vaegir_recruit,3,8),(trp_vaegir_footman,3,5)]),
 ("kingdom_12_lord_reinf_b", "{!}kingdom_12_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_vaegir_marksman,2,4),(trp_vaegir_veteran,2,5)]),
 ("kingdom_12_lord_reinf_c", "{!}kingdom_12_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_vaegir_knight,3,5),(trp_occc_vaegir_boyar_sons,1,2),(trp_occc_vaegir_master_shooter,1,1)]),  ## OCCC

################################################################################
#Kingdom of the Ring
################################################################################
 ("kingdom_13_reinforcements_a", "{!}kingdom_2_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_vaegir_veteran,3,5),(trp_vaegir_footman,3,6),(trp_vaegir_recruit,3,6)]),
 ("kingdom_13_reinforcements_b", "{!}kingdom_2_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_vaegir_marksman,2,5),(trp_vaegir_archer,2,4),(trp_vaegir_skirmisher,4,6)]),
 ("kingdom_13_reinforcements_c", "{!}kingdom_2_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_vaegir_horseman,2,5),(trp_vaegir_knight,1,2),(trp_occc_vaegir_master_shooter,0,1),(trp_occc_vaegir_boyar_sons,1,2)]),

 ("kingdom_13_lord_reinf_a", "{!}kingdom_12_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_vaegir_recruit,3,8),(trp_vaegir_footman,3,5)]),
 ("kingdom_13_lord_reinf_b", "{!}kingdom_12_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_vaegir_marksman,2,4),(trp_vaegir_veteran,2,5)]),
 ("kingdom_13_lord_reinf_c", "{!}kingdom_12_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_vaegir_knight,3,5),(trp_occc_vaegir_boyar_sons,1,2),(trp_occc_vaegir_master_shooter,1,2)]),  ## OCCC

################################################################################
#Kingdom of Albion (Nord's minor faction)
################################################################################
  ("kingdom_14_reinforcements_a", "{!}kingdom_14_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_albion_footman,4,14),(trp_albion_recruit,4,12),]),
  ("kingdom_14_reinforcements_b", "{!}kingdom_14_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_albion_archer,1,3),(trp_albion_veteran,1,4),(trp_albion_veteran_archer,2,3)]),
  ("kingdom_14_reinforcements_c", "{!}kingdom_14_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_albion_cavalry,1,2),(trp_albion_champion,2,4)]),  ## OCCC 5->2 8->4
  
## CC-D begin: +CC
  ("kingdom_14_lord_reinf_a", "{!}kingdom_14_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_albion_footman,4,8),(trp_albion_skirmisher,2,5)]),
  ("kingdom_14_lord_reinf_b", "{!}kingdom_14_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_albion_warrior,3,7),(trp_albion_archer,2,3)]),
  ("kingdom_14_lord_reinf_c", "{!}kingdom_14_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_albion_champion,1,3),(trp_albion_veteran,2,4)]),
## CC-D end ccc_nord_elite_huscarl

  ("montypython_party", "{!}EL", 0, 0, fac_commoners, 0, [(trp_occc_montypython_blackknight,1,2),(trp_occc_montypython_frenchman,4,8),(trp_occc_montypython_ni_knight,2,5),(trp_occc_montypython_ni_squire,3,7)] ),
################################################################################
#Restored Calradic Empire
#Last Boss Faction?
################################################################################

#based on rhodok empire

  ("nova_imperium_calradium_reinforcements_a", "{!}empire_5_reinforcements_a", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes,1,4),(trp_swadian_militia,2,4),(trp_sarranid_footman,2,4),(trp_ccc_rhodok_tribesman,3,5),(trp_khergit_skirmisher,2,4)]),
  ("nova_imperium_calradium_reinforcements_b", "{!}empire_5_reinforcements_b", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes_spear,1,2),(trp_ccc_rhodok_principes,1,4),(trp_rhodok_sharpshooter,2,4),(trp_khergit_veteran_horse_archer,1,2)]),
  ("nova_imperium_calradium_reinforcements_c", "{!}empire_5_reinforcements_c", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_triarii,3,4),(trp_ccc_swadian_lancer_knight,1,2),(trp_ccc_sarranid_amir,1,2),(trp_occc_vaegir_master_shooter,1,2)]),

## CC-D begin: +CC
  ("nova_imperium_calradium_lord_reinf_a", "{!}empire_5_lord_reinf_a", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes,4,8),(trp_ccc_rhodok_tribesman,2,5)]),
  ("nova_imperium_calradium_lord_reinf_b", "{!}empire_5_lord_reinf_b", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_principes,2,4),(trp_rhodok_sharpshooter,3,6)]),
  ("nova_imperium_calradium_lord_reinf_c", "{!}empire_5_lord_reinf_c", 0, 0, fac_commoners, 0, [(trp_ccc_rhodok_triarii,1,2),(trp_ccc_swadian_lancer_knight,2,3)]),


################################################################################
# empty place for expantion
################################################################################
#type
  ("ccc_quest_bandit_camp","Bandit",icon_axeman|carries_goods(1)|pf_quest_party|pf_always_visible,0, fac_neutral,bandit_personality,[]),  
  ("ccc_quest_bandit_fortress","Bandit Fortress",icon_castle_c|pf_is_static|pf_always_visible|pf_show_faction|pf_label_medium,0, fac_neutral,bandit_personality,[]),  
#obj
  ("ccc_faction_bandits", "{!}n", 0, 0, fac_commoners, 0, []),
  ("ccc_faction_straggler", "{!}n", 0, 0, fac_commoners, 0, []),

################################################################################
# occc expantion
################################################################################
 ("mercs_nordic","{!}EL",0,0,fac_commoners,0,[(trp_nord_veteran_archer,1,4),(trp_ccc_nord_barbarian_veteran,4,8),(trp_nord_recruit,4,8),(trp_nord_veteran,1,5)]),
 ("mercs_old_rhodok","{!}EL",0,0,fac_commoners,0,[(trp_rhodok_tribesman,5,8),(trp_rhodok_veteran_crossbowman,8,12),(trp_rhodok_spearman,4,10),(trp_rhodok_trained_spearman,3,6),]),
 ("mercs_landsknecht","{!}EL",0,0,fac_commoners,0,[(trp_mercenary_musketeer,8,16),(trp_mercenary_swordsman,4,8),(trp_mercenary_horseman,5,10),(trp_watchman,5,8)]),
 ("occc_holy_crusaders_companion","{!}",0,0,fac_commoners,0,
  [(trp_occc_order_squire,4,9),(trp_occc_order_sergeant,3,7),(trp_occc_order_standard_bearer,2,4),(trp_occc_order_knight,1,2)]),


  #Sw
 ("occc_army_of_the_night", "Army of the Night", icon_gray_knight, 0, fac_commoners, 0, [(trp_ritterbruder,3,4),(trp_swadian_veteran_ironcross_knight,2,5),(trp_swadian_ironcross_knight,8,10),(trp_occc_ironcross_crossbowman,5,15)] ),
 ("occc_holy_crusaders","Holy Knights Order",icon_gray_knight|carries_goods(20),0,fac_holy_crusaders,soldier_personality,
  [(trp_occc_order_master_knight,3,10),(trp_occc_order_squire,10,50),(trp_occc_order_sergeant,15,60),(trp_occc_order_standard_bearer,5,20),(trp_occc_order_knight,10,40)]),
#Vg
 ("occc_vaegir_volunteer_army", "{!}n", 0, 0, fac_commoners, 0, [(trp_vaegir_footman,8,15),(trp_vaegir_archer,8,15),(trp_vaegir_horseman,3,5)]),
 ("occc_riurik_survivors_clan","Riurik_Survivors_Clan",icon_vaegir_knight,0,fac_riurik_clan,soldier_personality,[(trp_ccc_sarranid_elite_archer,5,50), (trp_ccc_sarranid_samurai,3,45), (trp_ccc_sarranid_syougun,1,24), (trp_ccc_sarranid_kiba_musya,1,25), (trp_ccc_swadian_heavy_musket,4,24)]),
 ("occc_nomad_scouts", "{!}n", 0, 0, fac_commoners, 0, [(trp_black_khergit_guard,4,5),(trp_black_khergit_lancer,3,6),(trp_black_khergit_horseman,5,5)]),
#invaders
 ("occc_taikou_scoutarmy", "Foreign Scouters", icon_taikou_lord, 0, fac_taikou_scouts, soldier_personality, [(trp_taikou_umanori_bushou,10,15),(trp_taikou_buhen_sha,30,50),(trp_taikou_umanori,20,30),(trp_taikou_buhen_teppou_ashigaru,20,40),(trp_taikou_buhen_yari_ashigaru,30,70),(trp_taikou_buhen_yumi_ashigaru,20,30),]),
 ("occc_taikou_conquestarmy", "Rising Sun Invaders", icon_taikou_lord, 0, fac_kingdom_9, soldier_personality, [(trp_taikou_umanori_bushou,50,90),(trp_taikou_musha,150,240),(trp_taikou_umanori_musha,100,150),(trp_taikou_teppou_ashigaru,150,250),(trp_taikou_yari_ashigaru,180,300),(trp_taikou_yumi_ashigaru,80,180),]),
 ("occc_taikou_seeker", "Rising Sun Cavalry Seekers", icon_taikou_lord, 0, fac_kingdom_9, soldier_personality, [(trp_taikou_umanori_musha,40,60),(trp_taikou_umanori,70,120)]),
 ("occc_sunset_conquestarmy", "Sunset Invaders", icon_axeman, 0, fac_kingdom_10, soldier_personality, [(trp_sunset_jaguar,80,160),(trp_sunset_el_eagle,80,180),(trp_sunset_eagle,80,150),(trp_sunset_skirmisher,120,200),(trp_sunset_coyote,120,270),(trp_sunset_atlatl,100,190),]),
 ("occc_sunset_seeker", "Sunset Seekers", icon_axeman, 0, fac_kingdom_10, soldier_personality, [(trp_sunset_el_eagle,40,60),(trp_sunset_eagle,60,120)]),

 #Nd
 ("occc_jomsviking_raidparty", "Jomsviking Raiders", icon_sea_raider, 0, fac_jomsvikings, bandit_personality, [(trp_ccc_nord_elite_halberd_huscarl,10,20),(trp_ccc_nord_halberd_huscarl,16,50),(trp_occc_nord_joms_archer,12,20),(trp_occc_nord_berserk,12,18)]),
 ("occc_jomsviking_raidship", "Jomsviking Raid Ship", icon_ship|pf_is_ship, 0, fac_jomsvikings, 0, [(trp_ccc_nord_elite_halberd_huscarl,35,50),(trp_ccc_nord_halberd_huscarl,75,100),]),
 ("occc_highlander_party", "Highlanders", icon_axeman, 0, fac_kingdom_4, 0, [(trp_ccc_nord_highland_army,24,30),(trp_occc_nord_highlander,20,30),(trp_ccc_nord_wolves,10,13),]),
 ("occc_calrador_rangers", "Calrador Rangers", icon_axeman, 0, fac_calrador, 0, [(trp_occc_calrador_noble,2,24),(trp_occc_calrador_ranger,4,36),(trp_occc_calrador_warrior,12,36),]),
 ("occc_calrador_army", "Calrador Army", icon_gray_knight, 0, fac_calrador, 0, [(trp_occc_calrador_twilight_knight,12,35),(trp_occc_calrador_noble,12,24),(trp_occc_calrador_warrior,12,60),(trp_occc_calrador_ranger,120,300),(trp_occc_calrador_maiden_ranger,120,240),]),
 ("emp21", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bear_wahite_warrior,10,15),(trp_ccc_bear_warrior,10,15),]),
#Rd
 ("occc_imperial_legion", "{!}n", 0, 0, fac_commoners, 0, [(trp_rhodok_spearman,10,15),(trp_rhodok_crossbowman,10,15),(trp_rhodok_tribesman,3,5)]),
 ("occc_rhodok_rebels", "Rhodok Barbarian Rebels", icon_axeman, 0, fac_commoners, 0, [(trp_chief_forest_bandit,190,260),(trp_ccc_bear_wahite_warrior,100,160),(trp_ccc_nord_barbarian_great_cave,100,180),(trp_ccc_nord_barbarian_veteran_cave,100,180),(trp_occc_barbarian_warrior,120,250)]),
 ("occc_rhodok_gladiators", "Rhodok Gradiator Rebels", icon_axeman, 0, fac_commoners, 0, [(trp_occ_rhodok_gladiator,220,260),(trp_ccc_rhodok_hastati_rifle,100,160),(trp_ccc_rhodok_hastati_archar,100,180),(trp_occc_rebel_gladiator,100,180),(trp_occc_slave_gladiator,120,250)]),
 ("occc_undead_legion_centuria", "Calradic Revenants Centuria", icon_rhodok_lord, 0, fac_commoners, 0, [(trp_occc_undead_legionary,40,45),(trp_occc_undead_auxilia,30,50)]),
 ("occc_undead_legion_legion", "Calradic Revenants Legion", icon_rhodok_lord, 0, fac_commoners, 0, [(trp_occc_undead_equites,15,25),(trp_occc_undead_centurion,20,30),(trp_occc_undead_legionary,70,90),(trp_occc_undead_auxilia,100,150)]),
 ("occc_undead_legion_boss", "Calradic Revenants Army", icon_rhodok_king, 0, fac_commoners, 0, [(trp_occc_undead_legatus,5,10),(trp_occc_undead_equites,80,120),(trp_occc_undead_centurion,40,60),(trp_occc_undead_legionary,280,340),(trp_occc_undead_auxilia,100,180)]),
 ("emp28", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bear_wahite_warrior,10,15),(trp_ccc_bear_warrior,10,15),]),
 #cta
 ("occc_wardogs","WarDogs",icon_gray_knight|carries_goods(20),0,fac_manhunters,soldier_personality,
  [(trp_occc_wardog_soldier,40,80),(trp_occc_wardog_archer,25,45),(trp_occc_wardog_archer_sergeant,5,15),(trp_occc_wardog_veteran_soldier,20,40),(trp_occc_wardog_sergeant,10,20)]), ##### ADD MP
 ("occc_valkyries","Valkyries",icon_gray_knight|carries_goods(20),0,fac_valhalla,soldier_personality, [(trp_ccd_valkyrie,100,120)]),  ##### ADD MP
 ("occc_borcha_legion","Borcha Legion",icon_axeman|carries_goods(2),0,fac_valhalla,soldier_personality, [(trp_occc_borcha_clone,2000,3000),(trp_ccd_valkyrie,5,5,pmf_is_prisoner),(trp_occc_nazi_supersoldat,1,1,pmf_is_prisoner)]),  ##### ADD MP 

#Sa
 ("occc_jihadists", "Crescent Ghazis", icon_axeman, 0, fac_crescent_ghazis, 0, [(trp_occc_crescent_ghazi,50,80),(trp_occc_crescent_dervish,20,40),]),
 ("emp29", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bandit_scorpion,20,30),]),
 ("emp30", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_yamato_kunoiti_zyou,10,15),(trp_ccc_yamato_miko_kagura,20,25),(trp_ccc_yamato_kiba_samurai_taisyou,20,30),(trp_ccc_yamato_musket_samurai_taisyou,20,40),(trp_ccc_yamato_nodati_samurai_taisyou,10,20),(trp_ccc_yamato_yari_samurai_taisyou,10,20),]),
#Dk
 ("occc_dark_avengers", "Lich King Undead Army", 0, 0, fac_commoners, 0, [(trp_occc_widerganger,150,250),(trp_ccc_dark_knight_ghost,100,120),(trp_occc_dullahan,20,40),(trp_ccc_dark_knight_skeleton,140,180),(trp_occc_shadow_skeleton,80,120),]),#
 ("occc_nazi_party", "Letzte Bataillon", icon_axeman,0,fac_outlaws, bandit_personality, [(trp_occc_nazi_supersoldat,2,10),(trp_occc_nazi_zombie,10,40),(trp_occc_nazi_schutze,8,20),(trp_occc_nazi_stosstruppen,8,20),]),
 ("occc_true_chaos_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_skeleton,10,15),(trp_ccc_dark_knight_ghost,10,15),(trp_ccc_dark_knight_black_rider,1,2),(trp_ccc_dark_knight_monster_rider,1,2)]),
 ("occc_nazi_surprise_party", "Letzte Bataillon", 0, 0, fac_commoners, 0, [(trp_occc_nazi_supersoldat,1,3),(trp_occc_nazi_zombie,5,12),(trp_occc_nazi_schutze,2,5),(trp_occc_nazi_stosstruppen,2,5),]),
 ("occc_drifters_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_american_troop,10,15),(trp_occc_special_force_troop,5,12),]),
 ("occc_junkies_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_apocalyptic_wraith,1,3),(trp_occc_apocalyptic_heavymetal,2,8),(trp_occc_apocalyptic_junkie,10,15),(trp_occc_apocalyptic_riot,20,25),]),#
 ("occc_borcha_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_borcha_clone,18,25),]),

 ("occc_holy_crusaders_army","Holy Knights Army",icon_swadia_lord|carries_goods(20),0,fac_holy_crusaders,soldier_personality,
  [(trp_occc_order_master_knight,10,30),(trp_occc_order_squire,30,150),(trp_occc_order_sergeant,45,180),(trp_occc_order_standard_bearer,15,60),(trp_occc_order_knight,30,120)]),
#end
 ("occc_mercenary_bandits_warband","Outlaw Mercenary Warband",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[]),
 ("occc_random_mercenaries","Mercenary Warband",icon_vaegir_knight,0,fac_commoners,soldier_personality,[]),

################################################################################
# Caravan
################################################################################
 ("ccc_slave_caravan_party","Slave Caravan",icon_slave_caravan|carries_goods(25)|pf_show_faction,0,fac_commoners,merchant_personality,[(trp_slaver_chief,1,1),(trp_slave_crusher,6,10),(trp_slave_hunter,6,15),(trp_slave_driver,6,25)]),
 ("ccc_caravan_guard_a_party", "{!}caravan_guard_a", 0, 0, fac_commoners, 0, [(trp_mercenary_horseman,5,15),(trp_mercenary_cavalry,2,5),]),
 ("ccc_caravan_guard_b_party", "{!}caravan_guard_b", 0, 0, fac_commoners, 0, [(trp_sword_sister,3,8),(trp_ccc_white_knight,1,2),]),
################################################################################
#CC-C end
################################################################################

#  ("forest_bandit_lair" ,"Forest Bandit Camp",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_forest_bandit,15,58),(trp_chief_forest_bandit,5,14)]),
  ("forest_bandit_lair" ,"Forest Bandit Camp",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_forest_bandit,15,92),]),
  ("taiga_bandit_lair","Tundra Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_taiga_bandit,15,58),(trp_chief_taiga_bandit,5,14)]),
  ("steppe_bandit_lair" ,"Steppe Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_steppe_bandit,15,58),(trp_chief_steppe_bandit,5,14)]),
  ("sea_raider_lair","Sea Raider Landing",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_sea_raider,15,50),(trp_chief_sea_raider,3,12)]),
#  ("mountain_bandit_lair" ,"Mountain Bandit Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_mountain_bandit,15,58),(trp_chief_mountain_bandit,5,14)]),
  ("mountain_bandit_lair" ,"Mountain Bandit Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_mountain_bandit_rhodok,30,90)]),
  ("desert_bandit_lair" ,"Desert Bandit Lair",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_desert_bandit,15,58),(trp_chief_desert_bandit,5,14)]),
  ("looter_lair","Kidnappers' Hideout",icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders,0,fac_neutral,bandit_personality,[(trp_looter,15,25)]),
  ("bandit_lair_templates_end","{!}bandit_lair_templates_end",icon_axeman|carries_goods(2)|pf_is_static,0,fac_outlaws,bandit_personality,[(trp_sea_raider,15,50)]),

  ("leaded_looters","Band of robbers",icon_axeman|carries_goods(8)|pf_quest_party,0,fac_neutral,bandit_personality,[(trp_looter_leader,1,1),(trp_looter,3,3)]),

   ##diplomacy begin
  ("dplmc_spouse","Your spouse",icon_woman|pf_civilian|pf_show_faction,0,fac_neutral,merchant_personality,[]),

  ("dplmc_gift_caravan","Your Caravan",icon_mule|carries_goods(25)|pf_show_faction,0,fac_commoners,escorted_merchant_personality,[(trp_caravan_master,1,1),(trp_caravan_guard,5,25)]),
#recruiter kit begin
   ("dplmc_recruiter","Recruiter",icon_gray_knight|pf_show_faction,0,fac_neutral,merchant_personality,[(trp_dplmc_recruiter,1,1)]),
#recruiter kit end
   ##diplomacy end
##occc start
   ("entrench","Entrenchment",icon_last_entrench|pf_is_static|pf_always_visible|pf_no_label,0, fac_neutral,bandit_personality,[]),  #icon_last_entrench
   ("occc_reinforcement_party","Reinforcement",icon_gray_knight|pf_show_faction,0,fac_neutral,merchant_personality,[]),

##occc end
#CC-C begin
 ("ccc_cave_1", "{!}ccc_cave_1", icon_bandit_lair|carries_goods(2)|pf_is_static|pf_hide_defenders, 0,fac_neutral, bandit_personality, []),
 ("ccc_temp_party", "{!}ccc_temp_party", 0, 0, fac_commoners, 0, [] ),
 ## CC-D begin: keep(cave09 delete)
 ("ccc_north_bandit_party","North Bandit",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[]),
 ("ccc_south_bandit_party","South Bandit",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[]),
 ("ccc_dark_bandit_party","Dark Bandit",icon_gray_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[]),
 ("ccc_odasan_bandit_party","Odasan Bandit",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[]),
 ("ccc_kuluma_bandit_party","Chaos Bandit",icon_vaegir_knight|carries_goods(2),0,fac_outlaws,bandit_personality,[]),
 ("ccc_bandit_party","Bandit",icon_axeman|carries_goods(2),0,fac_outlaws,bandit_personality,[]),
 ## CC-D end
 #("ccc_temp_party", "{!}ccc_temp_party", 0, 0, fac_commoners, 0, [] ),  ## CC-D del
#CC-C End

## CC-D begin
 ("ccd_rodorigo_party", "Rodorigo Family", icon_vaegir_knight|carries_goods(3), 0, fac_outlaws, bandit_personality, [(trp_ccd_bandit_cavelry, 15, 25), (trp_chief_steppe_bandit, 7, 13), (trp_steppe_bandit, 25, 35), (trp_chief_forest_bandit, 7, 13), (trp_chief_mountain_bandit, 7, 13)]),
 ("ccd_usiatra_party", "Usiatra Party", icon_vaegir_knight|carries_goods(3), 0, fac_outlaws, bandit_personality, [(trp_ccd_bandit_cavelry, 7, 13), (trp_chief_mountain_bandit, 25, 35), (trp_chief_taiga_bandit, 15, 25), (trp_chief_forest_bandit, 25, 35)]),
 ("ccd_stavros_party","Stavros Party",icon_gray_knight,0,fac_manhunters,soldier_personality,[(trp_ccd_veteran_hired_blade, 30, 40), (trp_ccd_mercenary_sharpshooter, 30, 40), (trp_slave_crusher, 15, 25)]),
 ("ccd_aethrod_party", "Aethrod Party", icon_axeman|carries_goods(3), 0, fac_outlaws, bandit_personality, [(trp_vaegir_marksman, 45, 55), (trp_vaegir_archer, 15, 25), (trp_ccd_mercenary_sharpshooter, 25, 35), (trp_mercenary_crossbowman, 15, 25)]),
 ("ccd_zaira_party", "Fox Bandit", icon_vaegir_knight|carries_goods(3), 0, fac_outlaws, bandit_personality, [(trp_ccc_bandit_sand_fox_drgoon,10,20),(trp_ccc_bandit_sand_fox_hunter,10,20),]),
 ("ccd_argo_party","Argo Party",icon_gray_knight,0,fac_manhunters,soldier_personality,[(trp_caravan_elite_guard, 15, 25), (trp_mercenary_cavalry, 25, 35), (trp_caravan_guard, 15, 25), (trp_slaver_chief, 15, 25), (trp_slave_crusher, 15, 25)]),

 ("occc_galactic_deserters", "Galactic Deserters", icon_axeman|carries_goods(3), 0, fac_outlaws, bandit_personality, [(trp_occc_novatrooper,10,20),(trp_occc_imperial_stormtrooper,25,50),] ),

 ("occc_ordensrittern_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_ironcross_sergeant,5,10),(trp_swadian_ironcross_knight,2,5),(trp_swadian_ironcross_foot_knight,3,5),(trp_occc_ironcross_crossbowman,5,8)]),

 #Sw
  ("ccc_dragoon_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_sarranid_camel_dragoon,15,20),(trp_ccc_vaegir_red_coat_dragoon,15,20),]),  ## cdnCavemm
  ("ccc_quickbattle_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_quickbattle_infantry,2,7),(trp_quickbattle_skirmisher,5,8),]),
  ("ccc_elite_quickbattle_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_quickbattle_sharpshooter,5,7),(trp_quickbattle_warrior,5,8),(trp_quickbattle_squire,2,3),(trp_quickbattle_knight,2,3),]),
  ("ccc_sister_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_sister_elite_bayonet,5,8),(trp_ccc_sister_armor_bayonet,5,7),(trp_ccc_sister_swordsman,5,8),(trp_ccc_sister_knight,5,8),(trp_ccc_sister_swordmaster,2,3),(trp_ccc_sister_guard_knight,2,3),]),
  ("occc_teutonic", "{!}n", 0, 0, fac_commoners, 0, [(trp_swadian_veteran_ironcross_knight,3,6),(trp_swadian_ironcross_squire,8,10),(trp_swadian_ironcross_knight,5,8),(trp_swadian_ironcross_foot_knight,5,9)]),
  ("occc_brigands_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_brigand_raider,1,2),(trp_looter,5,12),(trp_brigand,9,11),(trp_occc_brigand_poacher,2,6),]),#occc
#Vg
  ("ccc_old_vg", "{!}n", 0, 0, fac_commoners, 0, [(trp_vaegir_footman,8,15),(trp_vaegir_archer,8,15),(trp_vaegir_horseman,3,5)]),
  ("ccc_line_inf_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_line_inf,25,35),]),
  ("ccc_gunman_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_cowboy,13,18),(trp_ccc_vaegir_rifle_gunman,13,18),]),  ## cdnCavemm
  ("ccc_guardian_vg", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_guardian,8,20),(trp_ccc_vaegir_guardian_halberd,8,20),(trp_ccc_vaegir_guardian_knight,6,9)]),
  ("occc_hus", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_vaegir_cowboy_2,14,18)]),
#Kg
  ("ccc_black_khergit_raiders", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_black_khergit_mergen,0,2),(trp_occc_black_khergit_baatur,0,2),(trp_black_khergit_guard,4,5),(trp_black_khergit_lancer,3,6),(trp_black_khergit_horseman,5,5)]),
  ("ccc_slave_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_slaver_chief,1,1),(trp_slave_crusher,4,8),(trp_slave_hunter,6,7),(trp_slave_driver,6,12)]),
  ("ccc_looter_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_looter,5,12),(trp_brigand,9,11),(trp_brigand,2,6),(trp_occc_robber_knight,1,3),]),
  ("occc_looter_doom_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_brigand,5,12),(trp_occc_robber_knight,9,11),(trp_occc_doom_knight,2,6),]),
  ("ccc_yamato_iga_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_yamato_kunoiti_tyuu,5,12),(trp_ccc_yamato_kunoiti_zyou,2,6),(trp_ore_shadow_twilightedge,2,4),(trp_ccc_yamato_miko_kagura,2,5),(trp_ore_shadow_zyounin,2,10),]),
#Nd
  ("ccc_chaos_party", "{!}n", 0, 0, fac_commoners, 0, []),
  ("ccc_farmer_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_farmer,15,35),(trp_peasant_woman,15,35),(trp_ccc_farmer,1,10),(trp_ccc_farmer_woman,1,7),]),
  ("occc_barbarian_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_nord_barbarian_veteran_cave,10,15),(trp_ccc_nord_barbarian_great_cave,10,15),(trp_ccc_nord_barbarian_legend_cave,5,8),]),
  ("ccc_viking_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bandit_viking,10,15),(trp_ccc_bandit_viking_axe,10,15),]),
  ("ccc_valkyrie_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_valkyrie_recruit,10,15),(trp_ccc_valkyrie_warrior,5,15),(trp_ccc_valkyrie_archer,5,15),(trp_ccc_valkyrie_knight,3,5),(trp_ccc_valkyrie_paladin,3,5),]),
  ("ccc_bear_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bear_wahite_warrior,10,15),(trp_ccc_bear_warrior,10,15),]),
#Rd
  ("ccc_old_rd", "{!}n", 0, 0, fac_commoners, 0, [(trp_rhodok_spearman,10,15),(trp_rhodok_crossbowman,10,15),(trp_rhodok_tribesman,3,5)]),
  ("ccc_mine_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_cave_mineworker,2,3),(trp_ccc_cave_good_mineworker,1,2),(trp_ccc_cave_slacker_mineworker,15,20),]),
  ("ccc_yamato_1_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_yamato_nodati_samurai,3,8),(trp_ccc_yamato_nodati_asigaru,2,8),(trp_ccc_yamato_asigaru_recruit,2,8),(trp_ccc_yamato_asigaru,3,12),(trp_ccc_yamato_yari_samurai,3,12),(trp_ccc_yamato_yari_samurai_taisyou,3,5),]),
  ("ccc_yamato_2_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_yamato_nodati_samurai_taisyou,3,8),(trp_ccc_yamato_yari_samurai_taisyou,3,8),(trp_ccc_yamato_nodati_samurai,3,8),(trp_ccc_yamato_musket_samurai_taisyou,3,8),(trp_ccc_yamato_kiba_samurai,1,8),]),
  ("occc_ancient_dead_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_undead_legionary,15,18),(trp_occc_undead_auxilia,10,14)]),
  ("ccc_mercenary_guard_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_mercenary_guard,10,15),(trp_ccc_mercenary_guard_light,10,15),(trp_ccc_mercenary_guard_heavy,5,10),]),
#Sa
  ("ccc_samurai_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_yamato_yari_samurai,10,15),(trp_ccc_yamato_nodati_samurai,2,3),(trp_ccc_yamato_kiba_samurai,2,3),]),
  ("ccc_sister_woman_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_sword_sister,1,2),(trp_fighter_woman,2,4),(trp_hunter_woman,5,8),(trp_follower_woman,10,12),]),
  ("ccc_scorpion_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bandit_scorpion,20,30),]),
  #("ccc_bandit_sand_fox", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bandit_sand_fox_drgoon,10,20),(trp_ccc_bandit_sand_fox_hunter,10,20),]),  ## CC-D del: avoid difor qb party
  ("ccc_yamato_syougun_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_masuraowarrior,10,15),(trp_occc_kamikazewarrior,20,25),(trp_ccc_yamato_kiba_samurai_taisyou,20,30),(trp_ccc_yamato_musket_samurai_taisyou,20,40),(trp_ccc_yamato_nodati_samurai_taisyou,10,20),(trp_ccc_yamato_yari_samurai_taisyou,10,20),]),
#Dk
  ("ccc_dark_hunters", "{!}n", 0, 0, fac_commoners, 0, [(trp_dark_knight,10,12),(trp_dark_sniper,10,12),(trp_dark_hunter,5,6)]),
  ("ccc_dark_skirmishers_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_skirmishers,25,35),]),
  ("ccc_undead_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_skeleton,10,15),(trp_ccc_dark_knight_ghost,10,15),(trp_ccc_dark_knight_black_rider,1,2),(trp_ccc_dark_knight_monster_rider,1,2)]),
  ("ccc_bk_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_bk_black_man_at_arms,15,30),(trp_ccc_bk_black_north_man_at_arms,15,30),]),
  ("occc_galactic_storm_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_novatrooper,7,14),(trp_occc_imperial_stormtrooper,15,30),]),
  ("ccc_dd_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_dd_knight,10,20),(trp_ccc_dd_guard,15,30),(trp_ccc_dd_sucut,15,30),]),
#hellas
  ("occc_spartan_bd", "{!}n", 0, 0, fac_commoners, 0, [(trp_ore_spartanvetwarrior,10,15),(trp_ore_spartanwarrior,15,20),]),##ore plus
  ("occc_persians", "{!}n", 0, 0, fac_commoners, 0, [(trp_desert_bandit,100,200), (trp_ccc_swadian_musket,40,80),]),##ore plus
  ("occc_amazons", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_amazon_archer_cavalry,3,6),(trp_occc_amazon_archer,5,15),(trp_occc_amazon_huntress,10,38)]),##ore plus
  ("occc_amazon_army", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_amazon_guardwoman,3,8),(trp_occc_amazon_warrior,3,8),(trp_occc_amazon_archer_cavalry,3,8),(trp_occc_amazon_archer,3,8),(trp_occc_amazon_knight,1,8),]),##ore plus
  ("occc_young_spartan", "{!}n", 0, 0, fac_commoners, 0, [(trp_mountain_bandit_spartan,10,15),(trp_ccc_swadian_conquistador,15,20),]),##ore plus
  ("occc_phalanx_army", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_khergit_pezetaioloi,10,20),(trp_ccc_khergit_pezetaioloi,5,10),(trp_ccc_khergit_iphicrates_hoplitai,10,15),(trp_occc_hellas_toxotai,10,15)]),##ore plus 

#old rhodokj 
  ("occc_tercios", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_swadian_landsknecht,10,16),(trp_ccc_swadian_heavy_musket_cave,3,6),(trp_ccc_swadian_conquistador_cave,3,6),(trp_ccc_swadian_musket_cave,6,9)]),
  ("occc_random_mercs", "{!}n", 0, 0, fac_commoners, 0, []),
  ("occc_militias", "{!}n", 0, 0, fac_commoners, 0, [(trp_militia,25,30),(trp_militia_veteran,15,30),(trp_militia_corporal,8,12)]),
  ("occc_crazy_elephants_bd", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_war_elephant,10,20)]),##ore plus
  ("occc_wardog_platoon", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_wardog_veteran_soldier,10,12),(trp_occc_wardog_archer,10,12),(trp_occc_wardog_soldier,5,6)]),
  ("occc_wardog_squad", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_wardog_soldier,5,12),(trp_occc_wardog_veteran_soldier,2,6),(trp_occc_wardog_sergeant,2,4),(trp_occc_wardog_archer,2,5),(trp_occc_wardog_archer_sergeant,2,10),]),

#Old vaegir
  ("occc_zombie_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_widerganger,10,20),(trp_ccd_zombie,40,60),]),
  ("occc_hades_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_dullahan,10,15),(trp_ccd_zombiedog,10,20),(trp_occc_shadow_skeleton,20,30),(trp_occc_demon_knight,10,20),(trp_ccc_dark_knight_monster_rider,10,20),(trp_occc_widerganger,30,40)]),
  ("occc_riuriks", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_sarranid_elite_archer,10,30), (trp_ccc_sarranid_samurai,10,25), (trp_ccc_sarranid_syougun,6,16), (trp_ccc_sarranid_kiba_musya,6,16), (trp_ccc_swadian_heavy_musket,6,16)]),
  ("occc_freedom_fighters", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_western_western_gunman,7,21), (trp_occc_western_gunman,5,18)]),
  ("occc_deadly_gunmen", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_western_unforgiven,3,5), (trp_occc_western_legend_gunman,10,25), (trp_occc_western_shotgun_man,6,16)]),

#Balion
  ("occc_calrador_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_calrador_warrior,10,26),(trp_occc_calrador_ranger,10,20),(trp_occc_calrador_noble,3,5),]),
  ("ccc_barbarian_party", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_nord_highland_army,8,13),(trp_occc_nord_highlander,10,15),(trp_ccc_nord_wolves,5,8),]),
  ("occc_montypython_1", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_montypython_ni_knight,10,15),(trp_occc_montypython_ni_squire,15,20),]),##ore plus
  ("occc_montypython_2", "{!}n", 0, 0, fac_commoners, 0, [(trp_occc_montypython_blackknight,3,5),(trp_occc_montypython_frenchman,20,30),]),##ore plus
  ("occc_highlander_heroes", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_nord_wolves,8,10),(trp_ccc_nord_beard,15,20),]),##ore plus

#end
  ("ccc_skeleton_bandit", "{!}n", 0, 0, fac_commoners, 0, [(trp_ccc_dark_knight_skeleton,8,12),(trp_occc_shadow_skeleton,2,4),]),#(trp_ccd_zombie,50,75),

  #occc_
  #Nomad Horde from AD1257
  ("occc_nomad_camp","Nomad horde",icon_khergit|carries_goods(5)|pf_show_faction,0,fac_commoners,soldier_personality,[(trp_khergit_veteran_horse_archer,1,5),(trp_ccc_khergit_elite_lancer,1,3),(trp_khergit_skirmisher,10,14),(trp_khergit_tribesman,8,13)]),


 ("ccd_end_party", "{!}ccd_end_party", 0, 0, fac_commoners, 0, [] ),
## CC-D end
]
# modmerger_start version=201 type=2
try:
    component_name = "party_templates"
    var_set = { "party_templates" : party_templates }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end

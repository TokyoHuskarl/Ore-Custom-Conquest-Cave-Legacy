from header_factions import *

####################################################################################################################
#  Each faction record contains the following fields:
#  1) Faction id: used for referencing factions in other files.
#     The prefix fac_ is automatically added before each faction id.
#  2) Faction name.
#  3) Faction flags. See header_factions.py for a list of available flags
#  4) Faction coherence. Relation between members of this faction.
#  5) Relations. This is a list of relation records.
#     Each relation record is a tuple that contains the following fields:
#    5.1) Faction. Which other faction this relation is referring to
#    5.2) Value: Relation value between the two factions.
#         Values range between -1 and 1.
#  6) Ranks
#  7) Faction color (default is gray)
####################################################################################################################

## CC begin
default_kingdom_relations = [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("dark_knights", -0.04),("black_khergits", -0.04),("valhalla",0.1)]

## CC end
#occc start
hating_every_faction = [("kingdom_1", -0.1),("kingdom_2", -0.1),("kingdom_3", -0.1),("kingdom_4", -0.1),("kingdom_5", -0.1),("kingdom_6", -0.1),("kingdom_7", -0.9),("kingdom_8", -0.1),("kingdom_9", -0.1),("kingdom_10", -0.1),("kingdom_11", -0.1),("kingdom_12", -0.1),("kingdom_13", -0.1),("kingdom_14", -0.1),("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("commoners",-0.6),("valhalla",0.1)]

#occc end

factions = [
  ("no_faction","No Faction",0, 0.9, [], []),
  ("commoners","Commoners",0, 0.1,[("player_faction",0.1)], []),
  ("outlaws","Outlaws", max_player_rating(-30), 0.5,[("commoners",-0.6),("player_faction",-0.15),("jomsvikings",-0.15),("valhalla",0.1)], [], 0xCC66CC), ## CC
# Factions before this point are hardwired into the game end their order should not be changed.

  ("neutral","Neutral",0, 0.1,[("player_faction",0.0)], [],0xFFFFFF),
  ("innocents","Innocents", ff_always_hide_label, 0.5,[("outlaws",-0.05)], []),
  ("merchants","Merchants", ff_always_hide_label, 0.5,[("outlaws",-0.5),], []),
#CC-C begin new faction
  ("yamato","Yamato",0, 0.1,[("player_faction",0.1)], []),
  ("valkyrie","Valkyrie",0, 0.1,[("player_faction",0.1)], []),
  ("sister","Sister",0, 0.1,[("player_faction",0.1)], []),
  ("minka","Minka",0, 0.1,[("player_faction",0.1)], []),
#CC-C end

## CC begin
  ("dark_knights","Wandering Dark Knights", 0, 0.5,[("player_faction",-0.4),("player_supporters_faction",-0.4),("outlaws", 0.1),("valhalla",0.1)], [], 0x800000),
  ("black_khergits","Black Khergits", 0, 0.5,[("commoners",-0.1),("outlaws", 0.1),("valhalla",0.1)], [], 0x800000),
## CC end
  ("culture_1",  "{!}culture_1", 0, 0.9, [], []), #swadian
  ("culture_2",  "{!}culture_2", 0, 0.9, [], []), #revolutionary vaegir
  ("culture_3",  "{!}culture_3", 0, 0.9, [], []), #khergit
  ("culture_4",  "{!}culture_4", 0, 0.9, [], []), #nords
  ("culture_5",  "{!}culture_5", 0, 0.9, [], []), #rhodok
  ("culture_6",  "{!}culture_6", 0, 0.9, [], []), #sarranid
  ("culture_7",  "{!}culture_7", 0, 0.9, [], []), ## NMC
#CC-C begin add faction
  ("culture_8",  "{!}culture_8", 0, 0.9, [], []),#dark
#CC-C end add faction
#occc start
  ("culture_9",  "{!}culture_9", 0, 0.9, [], []),#hellas
  ("culture_10",  "{!}culture_10", 0, 0.9, [], []),#taikou
  ("culture_11",  "{!}culture_11", 0, 0.9, [], []),#sunset
  ("culture_12",  "{!}culture_12", 0, 0.9, [], []),#old rhodok
  ("culture_13",  "{!}culture_13", 0, 0.9, [], []),#old vaegir
  ("culture_14",  "{!}culture_14", 0, 0.9, [], []),#kingdom of the ring
  ("culture_15",  "{!}culture_15", 0, 0.9, [], []),#Kingdom of Balion

#occc end

#  ("swadian_caravans","Swadian Caravans", 0, 0.5,[("outlaws",-0.8), ("dark_knights",-0.2)], []),
#  ("vaegir_caravans","Vaegir Caravans", 0, 0.5,[("outlaws",-0.8), ("dark_knights",-0.2)], []),

  ("player_faction","Player Faction",0, 0.9, [], []),
## CC begin
  ("player_supporters_faction","Player's Supporters",0, 0.9, [("player_faction",1.00),("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("valhalla",0.1)], [], 0xFF4433), #changed name so that can tell difference if shows up on map
  ("kingdom_1",  "Kingdom of Swadia",   0, 0.9, default_kingdom_relations, [], 0xEE7744),
  ("kingdom_2",  "Revolutionary Empire Vaegir",  0, 0.9, default_kingdom_relations, [], 0x0072bb),#  3344FF
  ("kingdom_3",  "Khergit Khanate",     0, 0.9, default_kingdom_relations, [], 0xCC99FF),#
  ("kingdom_4",  "Kingdom of Nords",    0, 0.9, default_kingdom_relations, [], 0x33DDDD),
  ("kingdom_5",  "Imperium Rhodok",  0, 0.9, default_kingdom_relations, [], 0x660aa8),# 0x460076
  ("kingdom_6",  "Sarranid Sultanate",  0, 0.9, default_kingdom_relations, [], 0xDDDD33),
## CC end
#CC-C begin add faction
  ("kingdom_7",  "Dark Knights",0, 0.9, default_kingdom_relations, [], 0x000000),
#CC-C end add faction
##occc start additional faction
  ("kingdom_8",  "Hellas City States",0, 0.9, default_kingdom_relations, [], 0x7f715e),#occc  
  ("kingdom_9",  "Taikou Conquest Army",0, 0.9, default_kingdom_relations, [], 0xC41A41),#occc
  ("kingdom_10",  "Sunset Empire",0, 0.9, default_kingdom_relations, [], 0xf4418e),#occc
  ("kingdom_11",  "Zendar=Rhodok Republic",  0, 0.9, default_kingdom_relations, [], 0x33DD33),
  ("kingdom_12",  "Murom=Vaegir Principality",  0, 0.9, default_kingdom_relations, [], 0xCCBB99),
  ("kingdom_13",  "Kingdom of The Ring",  0, 0.9, default_kingdom_relations, [], 0x800000),
  ("kingdom_14",  "Kingdom of Balion",  0, 0.9, default_kingdom_relations, [], 0x000080),#minor faction of nord

#occc rebels

##  ("kingdom_1_rebels",  "Swadian rebels", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_2_rebels",  "Vaegir rebels",    0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_3_rebels",  "Khergit rebels", 0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_4_rebels",  "Nord rebels",    0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", -0.05)], [], 0xCC2211),
##  ("kingdom_5_rebels",  "Rhodok rebels",  0, 0.9, [("outlaws",-0.05),("peasant_rebels", -0.1),("deserters", -0.02),("mountain_bandits", -0.05),("forest_bandits", -0.05)], [], 0xCC2211),

##occc end additional faction

  ("kingdoms_end","{!}kingdoms_end", 0, 0,[], []),
  ("robber_knights",  "{!}robber_knights", 0, 0.1, [], []),
  ("khergits","{!}Khergits", 0, 0.5,[("player_faction",0.0)], []),
##  ("rebel_peasants","Rebel Peasants", 0, 0.5,[("vaegirs",-0.5),("player_faction",0.0)], []),

#occc Religions
  ("christians","Christian", 0, 0.5,[("outlaws",-0.05),], []),
  ("pagans","Norse Pagan", 0, 0.5,[("outlaws",-0.05),], []),
  ("tengri","Tengri", 0, 0.5,[("outlaws",-0.05),], []),
  ("muslims","Muslims", 0, 0.5,[("outlaws",-0.05),], []),
  ("olympians","Olympians", 0, 0.5,[("outlaws",-0.05),], []),
  ("shinto","Shinto", 0, 0.5,[("outlaws",-0.05),], []),#
  ("nahuatl","Quetzalcoatl", 0, 0.5,[("outlaws",-0.05),], []),
  ("baal","Baal", 0, 0.5,[("outlaws",-0.05),], []),
#occc

## CC begin
  ("manhunters","Manhunters", 0, 0.5,[("outlaws",-0.6),("player_faction",0.1),("valhalla",0.1)], [], 0x80ff80),
  ("deserters","Deserters", 0, 0.5,[("manhunters",-0.6),("merchants",-0.5),("player_faction",-0.1),("valhalla",0.1)], [], 0xff8080),
  #("mountain_bandits","Mountain Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),
  #("forest_bandits","Forest Bandits", 0, 0.5,[("commoners",-0.2),("merchants",-0.5),("manhunters",-0.6),("player_faction",-0.15)], [], 0x888888),
## CC end

  ("undeads","{!}Undeads", max_player_rating(-30), 0.5,[("commoners",-0.7),("player_faction",-0.5),("valhalla",0.1)], []),
#  ("undeads","{!}Undeads", max_player_rating(-30), 0.5,[("commoners",-0.7),("player_faction",-0.5),("kingdom_1",-0.5),("kingdom_2",-0.5),("kingdom_3",-0.5),("kingdom_4",-0.5),("kingdom_5",-0.5),("kingdom_6",-0.5),("kingdom_7",0.5)], []),
  ("slavers","Slavers", 0, 0.5, [("outlaws",0.6),("commoners",-0.6),("deserters", -0.02),("valhalla",0.1)], [],0x2a542a),
  ("peasant_rebels","{!}Peasant Rebels", 0, 1.0,[("noble_refugees",-1.0)], []),
  ("noble_refugees","{!}Noble Refugees", 0, 0.5,[], []),
#INVASION MODE START
  ("ccoop_all_stars","All Stars", 0, 0.5,[], []),
#INVASION MODE END

# occc start
  ("mercenary","Mercenaries",0, 0.1,[("player_faction",0.1)], []),
  ("valhalla","Army of Valhalla", 0, 0.5, [("commoners",0.1),("manhunters",0.1),("outlaws",0.1),("merchants",0.1),("player_faction",-0.05),("deserters", 0.1),("jomsvikings", 0.1)], [],0x800080),
  #("rhodok_rebel","Rhodok Rebel", max_player_rating(-30), 0.5,[("commoners",-0.6),("player_faction",-0.15)], [], 0xCC66CC), ## CC

  # knight orders?
  #riuriks
  ("riurik_clan","Riurik Survivors Clan", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_12", 0.1),("valhalla",0.1)], [], 0x42f4ad),#salvage from cave-mm manhunters
   #SAMURAI!?
  ("bushido_order","Calradic Blades", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_6", 0.1),("kingdom_5", 0.1),("kingdom_9", 0.1),], [], 0xDDDD33),#
   #tengger
  ("tengger_cavalry","Tengger Cavalry", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_3", 0.1),], [], 0xc1eeff),#
   #teutons
  ("teutonic_order","Order of the Ironcross", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_1", 0.1),("crescent_ghazis", -0.6),], [], 0x232323),#
   #sisters and knight order
  ("holy_crusaders","Holy Crusaders", 0, 0.5,[("commoners",0.5),("outlaws",-0.6),("player_faction",0.1),("deserters", -0.5),("crescent_ghazis", -0.6),("valhalla",0.1)], [], 0x90ee90),#
   #valkyrie
  ("asgaard","Guardians of Asgaard", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_4", 0.1),("valhalla",0.1)], [], 0x38b1c1),#
  # ("kamibito","Shrine Guards", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   # ("black_khergits", -0.04),("kingdom_9", 0.1),("valhalla",0.1)], [], 0xff69b4),#
   #crescent ghazis
  ("crescent_ghazis","Crescent Zealots", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_6", 0.1),("valhalla",0.1)], [], 0xFFD700),#
  ("assassin_cult","Assassin Cult", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_6", 0.1),("valhalla",0.1)], [], 0x8B008B),#
   #jomsviking
  ("jomsvikings","Jomsviking", 0, 0.5,[("outlaws", 0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("commoners",-0.6),("valhalla",0.1)], [], 0x06146d),#
   #playerownorder
  ("player_own_order","Your own order", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("valhalla",0.1)], [], 0xDDDD33),#

	#sub factions
  ("taikou_scouts","Conquest Army Scouts", 0, 0.5,[("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("kingdom_9", 0.1),("kingdom_1", -0.1),("kingdom_2", -0.1),("kingdom_3", -0.1),("kingdom_4", -0.1),("kingdom_5", -0.1),("kingdom_6", -0.1),("kingdom_7", -0.1),("kingdom_8", -0.1),("kingdom_10", -0.1),("kingdom_11", -0.1),("kingdom_12", -0.1),("kingdom_13", -0.1),("kingdom_14", -0.1),("valhalla",0.1)], [], 0xC41A41),#
  ("calrador","Calrador Elves", 0, 0.5,[("kingdom_1", -0.1),("kingdom_2", -0.1),("kingdom_3", -0.1),("kingdom_4", -0.1),("kingdom_5", -0.1),("kingdom_6", -0.1),("kingdom_7", -0.9),("kingdom_8", -0.1),("kingdom_9", -0.1),("kingdom_10", -0.1),("kingdom_11", -0.1),("kingdom_12", -0.1),("kingdom_13", 0.1),("kingdom_14", -0.1),("outlaws", -0.1),("deserters", -0.02),("dark_knights", -0.04),
   ("black_khergits", -0.04),("valhalla",0.1)], [], 0x98FB98),#
  ("revenants","Calradic Revenants", max_player_rating(-30), 0.5,hating_every_faction, [],0x460076),

#occc end

]

##diplomacy start+ Define these for convenience
dplmc_factions_begin = 1 #As mentioned in the notes above, this is hardcoded and shouldn't be altered.  Deliberately excludes "no faction".
dplmc_non_generic_factions_begin = [x[0] for x in enumerate(factions) if x[1][0] == "merchants"][0] + 1
dplmc_factions_end   = len(factions)
##diplomacy end+
# modmerger_start version=201 type=4
try:
    component_name = "factions"
    var_set = { "factions":factions,"default_kingdom_relations":default_kingdom_relations, }
    from modmerger import modmerge
    modmerge(var_set, component_name)
except:
    raise
# modmerger_end

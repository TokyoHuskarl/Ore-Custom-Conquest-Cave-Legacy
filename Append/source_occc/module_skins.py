from header_skins import *
from ID_particle_systems import *
####################################################################################################################
#  Each skin record contains the following fields:
#  1) Skin id: used for referencing skins.
#  2) Skin flags. Not used yet. Should be 0.
#  3) Body mesh.
#  4) Calf mesh (left one).
#  5) Hand mesh (left one).
#  6) Head mesh.
#  7) Face keys (list)
#  8) List of hair meshes.
#  9) List of beard meshes.
# 10) List of hair textures.
# 11) List of beard textures.
# 12) List of face textures.
# 13) List of voices.
# 14) Skeleton name
# 15) Scale (doesn't fully work yet)
# 16) Blood particles 1 (do not add this if you wish to use the default particles)
# 17) Blood particles 2 (do not add this if you wish to use the default particles)
# 17) Face key constraints (do not add this if you do not wish to use it)
####################################################################################################################

man_face_keys = [
(20,0, 0.7,-0.6, "Chin Size"),
(260,0, -0.6,1.4, "Chin Shape"),
(10,0,-0.5,0.9, "Chin Forward"),
(240,0,0.9,-0.8, "Jaw Width"),
(210,0,-0.5,1.0, "Jaw Position"),
(250,0,0.8,-1.0, "Mouth-Nose Distance"),
(200,0,-0.3,1.0, "Mouth Width"),
(50,0,-1.5,1.0, "Cheeks"),

(60,0,-0.4,1.35, "Nose Height"),
(70,0,-0.6,0.7, "Nose Width"),
(80,0,1.0,-0.1, "Nose Size"),
(270,0,-0.5,1.0, "Nose Shape"),
(90,0,-0.2,1.4, "Nose Bridge"),

(100,0,-0.3,1.5, "Cheek Bones"),
(150,0,-0.2,3.0, "Eye Width"),
(110,0,1.5,-0.9, "Eye to Eye Dist"),
(120,0,1.9,-1.0, "Eye Shape"),
(130,0,-0.5, 1.1, "Eye Depth"),
(140,0,1.0,-1.2, "Eyelids"),

(160,0,1.3,-0.2, "Eyebrow Position"),
(170,0,-0.1,1.9, "Eyebrow Height"),
(220,0,-0.1,0.9, "Eyebrow Depth"),
(180,0,-1.1,1.6, "Eyebrow Shape"),
(230,0,1.2,-0.7, "Temple Width"),

(30,0,-0.6,0.9, "Face Depth"),
(40,0,0.9,-0.6, "Face Ratio"),
(190,0,0.0,0.95, "Face Width"),

(280,0,0.0,1.0, "Post-Edit"),
]

man_face_keys_new = [
(240,0, -0.4,0.3, "Chin Size"),
(230,0, -0.4,0.8, "Chin Shape"),
(250,0,-0.25,0.55, "Chin Forward"),#
(130,0,-0.5,1.0, "Jaw Width"),
(120,0,-0.5,0.6, "Lower_Lip"),
(110,0,-0.2,0.6, "Upper_Lip"),
(100,0,0.2,-0.2, "Mouth-Nose_Distance"),
(90,0,0.55,-0.55, "Mouth_Width"),#

(30,0,-0.3,0.3, "Nostril_Size"),
(60,0,0.25,-0.25, "Nose_Height"),
(40,0,-0.2,0.3, "Nose_Width"),
(70,0,-0.3,0.4, "Nose_Size"),
(50,0,0.2,-0.3, "Nose_Shape"),

(80,0,-0.2,0.65, "Nose_Bridge"),
(160,0,-0.2,0.25, "Eye_Width"),
(190,0,-0.25,-0.15, "Eye_to_Eye_Dist"),
(170,0,-0.85,0.85, "Eye Shape"),
(200,0,-0.3, 0.7, "Eye Depth"),
(180,0,-1.5,-1.5, "Eyelids"),

(20,0,0.6,-0.25, "Cheeks"),
(260,0,-0.6,0.5, "Cheek_Bones"),
(220,0,-0.1,0.9, "Eyebrow_Height"),
(210,0,-0.75,0.75, "Eyebrow_Shape"),
(10,0,-0.6,0.5, "Temple_Width"),

(270,0,-0.3,1.0, "Face Depth"),
(150,0,-0.25,-0.45, "Face Ratio"),
(140,0,-0.4,0.5, "Face Width"),

(280,0,1.0,1.0, "Post-Edit"),
]

# Face width-Jaw width Temple width
woman_face_keys = [
(230,0,0.8,-1.0, "Chin Size"), 
(220,0,-1.0,1.0, "Chin Shape"), 
(10,0,-1.2,1.0, "Chin Forward"),
(20,0, -0.6, 1.2, "Jaw Width"), 
(40,0,-0.7,1.0, "Jaw Position"),
(270,0,0.9,-0.9, "Mouth-Nose Distance"),
(30,0,-0.5,1.0, "Mouth Width"),
(50,0, -0.5,1.0, "Cheeks"),

(60,0,-0.5,1.0, "Nose Height"),
(70,0,-0.5,1.1, "Nose Width"),
(80,0,1.5,-0.3, "Nose Size"),
(240,0,-1.0,0.8, "Nose Shape"),
(90,0, 0.0,1.1, "Nose Bridge"),

(100,0,-0.5,1.5, "Cheek Bones"),
(150,0,-0.4,1.0, "Eye Width"),
(110,0,1.0,0.0, "Eye to Eye Dist"),
(120,0,-0.2,1.0, "Eye Shape"),
(130,0,-0.1,1.6, "Eye Depth"),
(140,0,-0.2,1.0, "Eyelids"),


(160,0,-0.2,1.2, "Eyebrow Position"),
(170,0,-0.2,0.7, "Eyebrow Height"),
(250,0,-0.4,0.9, "Eyebrow Depth"),
(180,0,-1.5,1.2, "Eyebrow Shape"),
(260,0,1.0,-0.7, "Temple Width"),

(200,0,-0.5,1.0, "Face Depth"),
(210,0,-0.5,0.9, "Face Ratio"),
(190,0,-0.4,0.8, "Face Width"),

(280,0,0.0,1.0, "Post-Edit"),
]
undead_face_keys = []

##### ADD OCCC

new_woman_face_keys = [
#(250,0,-1.0,1.0, "Chin Shape3"),
#(230,0,-1.0,1.0, "Chin Shape2"),
#(220,0,-1.0,1.0, "Chin Shape1"),
(180,0,-0.4,0.5, "Chin Size"),
#(260,0,0.3,-1.4, "Chin Shape"),
(240,0,-0.7,1.0, "Chin Shape"),
(190,0,-1.2,1.0, "Chin Forward"),

(200,0,-1.0,1.0, "Jaw Width"),#Jaw Width
(210,0,-0.9,0.6, "Jaw Position"),

(150,0,-0.5,1.0, "Mouth Width"),
(110,0,-0.5,1.0, "Cheeks"),


(160,0,-0.5,0.5, "Under Lip"),#
(170,0,-0.5,0.5, "Upper Lip"),



(90,0, -0.6,1.4, "Eye Width"),
(100,0,1.0,0.0, "Eye to Eye Dist"),
(80,0,-0.2,1.0, "Eye Shape"),


(140,0,-0.5,1.0, "Nose Height"),
(120,0,1.5,-0.3, "Nose Size"),
(130,0,-1.0,0.8, "Nose Shape"),



(50,0, -0.2,1.2, "Eyebrow Position"),
(70,0,-0.2,0.7, "Eyebrow Height"),
(60,0,-1.5,1.2, "Eyebrow Shape"),

(30,0,-0.5,1.0, "Face Depth"),
(10,0,-0.5,0.9, "Face Ratio"),
(20,0, -0.8, 0.8, "Head Height"),
(40,0,-0.8, 0.8, "Head Width"),

(280,0,0.0,1.0, "Post-Edit"),
]

##### ADD OCCC end


chin_size = 0
chin_shape = 1
chin_forward = 2
jaw_width = 3
jaw_position = 4
mouth_nose_distance = 5
mouth_width = 6
cheeks = 7
nose_height = 8
nose_width = 9
nose_size = 10
nose_shape = 11
nose_bridge = 12
cheek_bones = 13
eye_width = 14
eye_to_eye_dist = 15
eye_shape = 16
eye_depth = 17
eyelids = 18
eyebrow_position = 19
eyebrow_height = 20
eyebrow_depth = 21
eyebrow_shape = 22
temple_width = 23
face_depth = 24
face_ratio = 25
face_width = 26

comp_less_than = -1;
comp_greater_than = 1;

skins = [
  (#0
    "man", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head", man_face_keys,
#    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
#CC-C begin
    ["man_hair_yu20","man_hair_yu19","man_hair_yu7","man_hair_yu2","man_hair_yu1","man_hair_yu3","man_hair_p","man_hair_r","man_hair_q","man_hair_yu10","man_hair_y6","man_hair_y12","man_hair_yu18","man_hair_y4","man_hair_u","man_hair_yu6","man_hair_yu8","man_hair_yu9","man_hair_yu12","man_hair_yu17","man_hair_yu11","man_hair_yu13","man_hair_yu14","man_hair_v","man_hair_yu15","man_hair_yu16","man_hair_yu4","man_hair_yu21","man_hair_yu22","hair_punk","man_hair_yu5","hairmessy","longshoulder","ponytail","longstraight","courthair","slickedback","shortbob","shortlayer","shortcut","man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10","man_hair_t","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_y","man_hair_y2"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",  ## CC-D add
#CC-C end
    ["beard_e","beard_d","beard_k","beard_l","beard_i","beard_j","beard_z","beard_m","beard_n","beard_y","beard_p","beard_o",   "beard_v", "beard_f", "beard_b", "beard_c","beard_t","beard_u","beard_r","beard_s","beard_a","beard_h","beard_g","accessory_glasses_simple","accessory_monocle","accessory_cigar_simple","accessory_pipe_simple","accessory_pipe_russian","accessory_eyepatch_simple","accessory_grashalm_simple","accessory_single_earing","accessory_flower_daisy","accessory_Rich_german_pipe_3",], #beard meshes ,"beard_q"  ## CC-D add
    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    ["beard_blonde","beard_red","beard_brunette","beard_black","beard_white"], #beard_materials
    [("manface_young_2",0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19]),
     ("manface_midage",0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("manface_young",0xffd0e0e0,["hair_blonde"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
#     ("manface_old",0xffd0d0d0,["hair_white","hair_brunette","hair_red","hair_blonde"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
     ("manface_young_3",0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff007080c]),
     ("manface_7",0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff007080c]),
     ("manface_midage_2",0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("manface_rugged",0xffb0aab5,["hair_blonde"],[0xff171313, 0xff007080c]),
#     ("manface_young_4",0xffe0e8e8,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff007080c]),
     ("manface_african",0xff807c8a,["hair_blonde"],[0xff120808, 0xff007080c]),     
#     ("manface_old_2",0xffd5d5c5,["hair_white"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
## CC-D begin: extra man faces
     ("imf_manface_asian1",0xffe3e8e1,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_asian2",0xffe3e8e1,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_asian3",0xffbbb6ae,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_mideast1",0xffaeb0a6,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_mideast2",0xffd0c8c1,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_mideast3",0xffe0e8e8,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_black1",0xff87655c,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_black2",0xff5a342d,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_black3",0xff634d3e,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_white1",0xffe0e8e8,["hair_blonde"],[0xffffffff,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("imf_manface_white2",0xffe0e8e8,["hair_blonde"],[0xffffffff,0xffb04717,0xff632e18,0xff502a19,0xff19100c,0xff0c0d19]),
     ("imf_manface_white3",0xffe0e8e8,["hair_blonde"],[0xff83301a,0xff502a19,0xff19100c,0xff0c0d19]),
     ("rus_asian_manface_young_2",0xffd0e0e0,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_asian_manface_young_3",0xffd0e0e0,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_asian_manface_young_5",0xffd0e0e0,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_manface_1",0xffdfefe1,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_manface_2",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_3",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_5",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_6",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_7",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_8",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_9",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_11",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
## CC-D end
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_man_yell"),(voice_stun,"snd_man_stun"),(voice_victory,"snd_man_victory"),
     (voice_warcry, "snd_man_warcry"),  ## CC-D add
     ], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),
  
  (#1
    "woman", skf_use_morph_key_10,
#CC-C begin
    "woman_body_y",  "woman_calf_l", "f_handL",
    "female_head2", woman_face_keys,
#CC-C begin
    ["woman_hair_yu1","woman_hair_yu2","woman_hair_yu3","woman_hair_yu4","woman_hair_yu5","woman_hair_yu6","woman_hair_yu6b","woman_hair_yu7","woman_hair_yu8","woman_hair_yu9","woman_hair_yu10","woman_hair_yu11","woman_hair_yu12","woman_hair_yu13","woman_hair_yu13b","woman_hair_yu14","woman_hair_yu15","woman_hair_yu20","woman_hair_yu17","woman_hair_yu18","woman_hair_yu19","woman_hair_yu16","woman_hair_yu21","woman_hair_yu22","woman_hair_yu23","woman_hair_yu23x","sib_leia","rensibhair2","sib_curly","hair_ren05","hair_ren03","woman_hair_q2","hair_punk","twintale_roll","maidenhair","hairmessy","longshoulder","ponytail","longstraight","courthair","slickedback","shortbob","shortlayer","woman_hair_p","woman_hair_n","woman_hair_o","woman_hair_q","woman_hair_r","woman_hair_t","woman_hair_s","onnna_kishi_hair"], #woman_hair_meshes  ## CC-D add
#    ["woman_hair_a","woman_hair_b","woman_hair_c","woman_hair_d","woman_hair_e","woman_hair_f","woman_hair_g"], #woman_hair_meshes
    ["acc1","acc2","acc3","acc4","acc5","acc6","acc7","acc8","acc9","acc10","acc11","acc12","acc13", "acc14","accessory_cigar_simple","accessory_pipe_simple","accessory_grashalm_simple","accessory_single_earing","accessory_flower_daisy",],  ## CC-D add
#    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    [],
    [("womanface_young3y",0xffeafcec,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),  ## CC-D 0xffe3e8ef->0xffeafcec
     ("womanface_by",0xffdfdfdf,["hair_blonde"],[0xffa5481f, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_a",0xffe8dfe5,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_brown",0xffaf9f7e,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]),#wimanface_brown2
     ("womanface_african2y",0xff808080,["hair_blonde"],[0xff120808, 0xff007080c]),
     ("womanface_b2",0xffe3e8ef,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),
     ("womanface_young2y_x",0xffabd8ff,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]),  ## CC-D 0xffaf9f7e->0xffabd8ff
     ("womanface_young_grey2",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]), ##### occc imported from MP 
     ("womanface_young2y",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]), ##### occc imported from MP 
	 ("wimanface_brown2",0xffaf9f7e,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]), ##### occc imported from MP 
#     ("womanface_midage",0xffe5eaf0,["hair_black","hair_brunette","hair_red","hair_white"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
     ],#woman_face_textures
    [(voice_die,"snd_woman_die"),(voice_hit,"snd_woman_hit"),(voice_grunt,"snd_woman_grunt"),(voice_grunt_long,"snd_woman_grunt"),(voice_yell,"snd_woman_yell"),(voice_victory,"snd_woman_victory"),
     (voice_warcry, "snd_woman_warcry"), (voice_stun, "snd_woman_stun"),  ## CC-D add
     ], #voice sounds
#CC-C end
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
  ),
  
## CC-D begin
  (#2
    "undead", 0,
    "undead_body", "undead_calf_l", "undead_handgloves_L",
    "undead_skin_occc", undead_face_keys,
    ["man_hair_p"], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("undeadface_a",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [(voice_die,"snd_ccd_undead_die"),(voice_hit,"snd_ccd_undead_hit"),(voice_grunt,"snd_ccd_undead_grunt"),(voice_yell,"snd_ccd_undead_yell"),(voice_victory,"snd_ccd_undead_victory")], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
  ),

  (#3
    "troll", 0,
    "trollbodya", "trollfootL", "troll_hand_L",
    "troll_head_skin", undead_face_keys,
    ["man_hair_p"], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("troll_head_skin",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [(voice_die,"snd_ccd_troll_die"),(voice_hit,"snd_ccd_troll_hit"),(voice_grunt,"snd_ccd_troll_grunt"),(voice_grunt_long,"snd_ccd_troll_grunt"),(voice_yell,"snd_ccd_troll_yell"),(voice_victory,"snd_ccd_troll_victory")], #voice sounds
    "skel_human", 1.5,
    psys_game_blood,psys_game_blood_2,
  ),

  (#4
    "skeleton", 0,
    "skeleton_body", "skeleton_body_calf_L", "skeleton_hand_L",
    "skull_skin", undead_face_keys,
    ["man_hair_p"], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("skull_skin",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [
    (voice_die,"snd_occc_skeleton_die"),(voice_hit,"snd_occc_skeleton_hit"),(voice_grunt,"snd_occc_skeleton_grunt"),(voice_grunt_long,"snd_occc_skeleton_grunt"),(voice_yell,"snd_occc_skeleton_yell"),(voice_victory,"snd_occc_skeleton_victory")
    ], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
  ),

  (#5
    "dog", 0,
    "empty_mesh", "empty_mesh", "empty_mesh",
    "empty_mesh", undead_face_keys,
    [], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("manface_young_2",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [(voice_die,"snd_ccd_dog_whine"),(voice_hit,"snd_ccd_dog_whine"),(voice_grunt,"snd_ccd_dog_whine"),(voice_grunt_long,"snd_ccd_dog_whine"),(voice_yell,"snd_ccd_dog_growl"),(voice_stun,"snd_ccd_dog_bark"),(voice_victory,"snd_ccd_dog_bark")], #voice sounds
    "skel_human_reduced", 0.55,
    psys_game_blood,psys_game_blood_2,
  ),

  (#6
    "lizardman", 0,
    "lizard_body", "empty_mesh", "empty_mesh",
    "empty_mesh", undead_face_keys,
    [], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("manface_young_2",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [(voice_die,"snd_ccd_lizard_die"),(voice_hit,"snd_ccd_lizard_hit"),(voice_grunt,"snd_ccd_lizard_grunt"),(voice_grunt_long,"snd_ccd_lizard_grunt"),(voice_yell,"snd_ccd_lizard_yell"),(voice_victory,"snd_ccd_lizard_yell"),(voice_stun,"snd_ccd_lizard_hit"),], #voice sounds
    "skel_human", 1.1,
    psys_game_blood,psys_game_blood_2,
  ),

  (#7
    "balrog", 0,
    "balrog_ignore", "empty_mesh", "empty_mesh",
    "empty_mesh", undead_face_keys,
    [], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("manface_young_2",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [(voice_die,"snd_balrog_die"),(voice_hit,"snd_balrog_hit"),(voice_yell,"snd_balrog_yell"),(voice_victory,"snd_balrog_yell"),(voice_stun,"snd_balrog_hit"),], #voice sounds
    "skel_balrog_big", 1.5,
    psys_game_blood,psys_game_blood_2,
  ),
    (#8
    "nordic_man", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head", man_face_keys,
#    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
#CC-C begin
    ["man_hair_yu20","man_hair_yu19","man_hair_yu7","man_hair_yu2","man_hair_yu1","man_hair_yu3","man_hair_p","man_hair_r","man_hair_q","man_hair_yu10","man_hair_y6","man_hair_y12","man_hair_yu18","man_hair_y4","man_hair_u","man_hair_yu6","man_hair_yu8","man_hair_yu9","man_hair_yu12","man_hair_yu17","man_hair_yu11","man_hair_yu13","man_hair_yu14","man_hair_v","man_hair_yu15","man_hair_yu16","man_hair_yu4","man_hair_yu21","man_hair_yu22","hair_punk","man_hair_yu5","hairmessy","longshoulder","ponytail","longstraight","courthair","slickedback","shortbob","shortlayer","shortcut","man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10","man_hair_t","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_y","man_hair_y2"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",  ## CC-D add
#CC-C end
    ["beard_e","beard_d","beard_k","beard_l","beard_i","beard_j","beard_z","beard_m","beard_n","beard_y","beard_p","beard_o",   "beard_v", "beard_f", "beard_b", "beard_c","beard_t","beard_u","beard_r","beard_s","beard_a","beard_h","beard_g","accessory_glasses_simple","accessory_monocle","accessory_cigar_simple","accessory_pipe_simple","accessory_pipe_russian","accessory_eyepatch_simple","accessory_grashalm_simple","accessory_single_earing","accessory_flower_daisy","accessory_Rich_german_pipe_3",], #beard meshes ,"beard_q"  ## CC-D add
    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    ["beard_blonde","beard_red","beard_brunette","beard_black","beard_white"], #beard_materials
    [("manface_young_2",0xffcbe0e0,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19]),
     ("manface_midage",0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("manface_young",0xffd0e0e0,["hair_blonde"],[0xff83301a, 0xff502a19, 0xff19100c, 0xff0c0d19]),     
#     ("manface_old",0xffd0d0d0,["hair_white","hair_brunette","hair_red","hair_blonde"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
     ("manface_young_3",0xffdceded,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff007080c]),
     ("manface_7",0xffc0c8c8,["hair_blonde"],[0xff171313, 0xff007080c]),
     ("manface_midage_2",0xfde4c8d8,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("manface_rugged",0xffb0aab5,["hair_blonde"],[0xff171313, 0xff007080c]),
#     ("manface_young_4",0xffe0e8e8,["hair_blonde"],[0xff2f180e, 0xff171313, 0xff007080c]),
     ("manface_african",0xff807c8a,["hair_blonde"],[0xff120808, 0xff007080c]),     
#     ("manface_old_2",0xffd5d5c5,["hair_white"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
## CC-D begin: extra man faces
     ("imf_manface_asian1",0xffe3e8e1,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_asian2",0xffe3e8e1,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_asian3",0xffbbb6ae,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_mideast1",0xffaeb0a6,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_mideast2",0xffd0c8c1,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_mideast3",0xffe0e8e8,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_black1",0xff87655c,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_black2",0xff5a342d,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_black3",0xff634d3e,["hair_blonde"],[0xff171313,0xff007080c]),
     ("imf_manface_white1",0xffe0e8e8,["hair_blonde"],[0xffffffff,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("imf_manface_white2",0xffe0e8e8,["hair_blonde"],[0xffffffff,0xffb04717,0xff632e18,0xff502a19,0xff19100c,0xff0c0d19]),
     ("imf_manface_white3",0xffe0e8e8,["hair_blonde"],[0xff83301a,0xff502a19,0xff19100c,0xff0c0d19]),
     ("rus_asian_manface_young_2",0xffd0e0e0,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_asian_manface_young_3",0xffd0e0e0,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_asian_manface_young_5",0xffd0e0e0,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_manface_1",0xffdfefe1,["hair_blonde"],[0xff19100c,0xff0c0d19]),
     ("rus_manface_2",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_3",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_5",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_6",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_7",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_8",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_9",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
     ("rus_manface_11",0xffdfefe1,["hair_blonde"],[0xffddd6b3,0xff997d29,0xffb04717,0xff632e18,0xff502a19,0xff19100c]),
## CC-D end
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_man_yell"),(voice_stun,"snd_man_stun"),(voice_victory,"snd_man_victory"),
     (voice_warcry, "snd_man_warcry"),  ## CC-D add
     ], #voice sounds
    "skel_human", 1.08,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),
  
  
  (#concept from CtAMP option (applying to fatima and camile) 9
    "girl", skf_use_morph_key_10,
#CC-C begin
    "woman_body_y",  "woman_calf_l", "f_handL",
    "female_head2", woman_face_keys,
#CC-C begin
    ["woman_hair_yu1","woman_hair_yu2","woman_hair_yu3","woman_hair_yu4","woman_hair_yu5","woman_hair_yu6","woman_hair_yu6b","woman_hair_yu7","woman_hair_yu8","woman_hair_yu9","woman_hair_yu10","woman_hair_yu11","woman_hair_yu12","woman_hair_yu13","woman_hair_yu13b","woman_hair_yu14","woman_hair_yu15","woman_hair_yu20","woman_hair_yu17","woman_hair_yu18","woman_hair_yu19","woman_hair_yu16","woman_hair_yu21","woman_hair_yu22","woman_hair_yu23","woman_hair_yu23x","sib_leia","rensibhair2","sib_curly","hair_ren05","hair_ren03","woman_hair_q2","hair_punk","twintale_roll","maidenhair","hairmessy","longshoulder","ponytail","longstraight","courthair","slickedback","shortbob","shortlayer","woman_hair_p","woman_hair_n","woman_hair_o","woman_hair_q","woman_hair_r","woman_hair_t","woman_hair_s"], #woman_hair_meshes  ## CC-D add
#    ["woman_hair_a","woman_hair_b","woman_hair_c","woman_hair_d","woman_hair_e","woman_hair_f","woman_hair_g"], #woman_hair_meshes
    ["acc1","acc2","acc3","acc4","acc5","acc6","acc7","acc8","acc9","acc10","acc11","acc12","acc13", "acc14","accessory_cigar_simple","accessory_pipe_simple","accessory_grashalm_simple","accessory_single_earing","accessory_flower_daisy",],  ## CC-D add
#    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    [],
    [("womanface_young3y",0xffeafcec,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),  ## CC-D 0xffe3e8ef->0xffeafcec
     ("womanface_by",0xffdfdfdf,["hair_blonde"],[0xffa5481f, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_a",0xffe8dfe5,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_brown",0xffaf9f7e,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]),
     ("womanface_african2y",0xff808080,["hair_blonde"],[0xff120808, 0xff007080c]),
     ("womanface_b2",0xffe3e8ef,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),
     ("womanface_young2y_x",0xffabd8ff,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]),  ## CC-D 0xffaf9f7e->0xffabd8ff
     ("womanface_young_grey2",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]), ##### occc imported from MP 
     ("womanface_young2y",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]), ##### occc imported from MP 
	 ("wimanface_brown2",0xffaf9f7e,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]), ##### occc imported from MP 

#     ("womanface_midage",0xffe5eaf0,["hair_black","hair_brunette","hair_red","hair_white"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
     ],#woman_face_textures
    [(voice_die,"snd_woman_die"),(voice_hit,"snd_woman_hit"),(voice_grunt,"snd_woman_grunt"),(voice_grunt_long,"snd_woman_grunt"),(voice_yell,"snd_woman_yell"),(voice_victory,"snd_woman_victory"),
     (voice_warcry, "snd_woman_warcry"), (voice_stun, "snd_woman_stun"),  ## CC-D add
     ], #voice sounds
#CC-C end
    "skel_human", 0.95,
    psys_game_blood,psys_game_blood_2,
  ),

  
##### FROM MP

########### _gaolu 10
 
    ("woman_gaolu", skf_use_morph_key_10,
    "woman_body_y",  "woman_calf_l", "f_handL",
    "xcorprus_female_head", new_woman_face_keys,
    ["woman_hair_yu1","woman_hair_yu2","woman_hair_yu3","woman_hair_yu4","woman_hair_yu5","woman_hair_yu6","woman_hair_yu6b","woman_hair_yu7","woman_hair_yu8","woman_hair_yu9","woman_hair_yu10","woman_hair_yu11","woman_hair_yu12","woman_hair_yu13","woman_hair_yu13b","woman_hair_yu14","woman_hair_yu15","woman_hair_yu20","woman_hair_yu17","woman_hair_yu18","woman_hair_yu19","woman_hair_yu16","woman_hair_yu21","woman_hair_yu22","woman_hair_yu23","woman_hair_yu23x","sib_leia","rensibhair2","sib_curly","hair_ren05","hair_ren03","woman_hair_q2","hair_punk","twintale_roll","maidenhair","hairmessy","longshoulder","ponytail","longstraight","courthair","slickedback","shortbob","shortlayer","woman_hair_p","woman_hair_n","woman_hair_o","woman_hair_q","woman_hair_r","woman_hair_t","woman_hair_s"], #woman_hair_meshes  ## CC-D add
#    ["woman_hair_a","woman_hair_b","woman_hair_c","woman_hair_d","woman_hair_e","woman_hair_f","woman_hair_g"], #woman_hair_meshes
    ["acc1","acc2","acc3","acc4","acc5","acc6","acc7","acc8","acc9","acc10","acc11","acc12","acc13", "acc14","accessory_cigar_simple","accessory_pipe_simple","accessory_grashalm_simple","accessory_single_earing","accessory_flower_daisy",],  ## CC-D add
#    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    [],
    [("womanface_young_gaolu",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_young_gaolu_a",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_young_gaolu_b",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_b_gaolu2",0xffdfdfdf,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_b_gaolu",0xffdfdfdf,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_caucas_gaolu",0xffe8dfe5,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19, 0xff007080c]), 
     ("womanface_brown_gaolu",0xffaf9f7e,["hair_blonde"],[0xffa5481f, 0xff502a19, 0xff19100c, 0xff0c0d19, 0xff007080c]), 
     ("womanface_african_gaolu",0xff808080,["hair_blonde"],[0xffa5481f, 0xff502a19, 0xff19100c, 0xff0c0d19, 0xff007080c]),
     ("womanface_young_gaolu_a2",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     

#     ("womanface_midage",0xffe5eaf0,["hair_black","hair_brunette","hair_red","hair_white"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
     ],#woman_face_textures
    [(voice_die,"snd_woman_die"),(voice_hit,"snd_woman_hit"),(voice_yell,"snd_woman_yell"),(voice_grunt,"snd_woman_grunt"),(voice_grunt_long,"snd_woman_grunt_long"),(voice_victory,"snd_woman_victory")], #voice sounds

    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
  ),

  
## CC-D end
  (#11
    "elven_man", 0,
    "man_body", "man_calf_l", "m_handL",
    "male_head_elven", man_face_keys,
#    ["man_hair_s","man_hair_m","man_hair_n","man_hair_o", "man_hair_y10", "man_hair_y12","man_hair_p","man_hair_r","man_hair_q","man_hair_v","man_hair_t","man_hair_y6","man_hair_y3","man_hair_y7","man_hair_y9","man_hair_y11","man_hair_u","man_hair_y","man_hair_y2","man_hair_y4"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",
    ["elf_hair_1","elf_hair_2","elf_hair_3","elf_hair_4","elf_hair_5","elf_hair_6","elf_hair_7","elf_hair_8"], #man_hair_meshes ,"man_hair_y5","man_hair_y8",  ## CC-D add
    [], #beard meshes ,"beard_q"  ## CC-D add
    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    ["beard_blonde","beard_red","beard_brunette","beard_black","beard_white"], #beard_materials
    [
     ("elfface_young",0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("elfface_young2",0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("elfface_young3",0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),
     ("elfface_young4",0xffdfefe1,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff632e18, 0xff502a19, 0xff19100c]),

## CC-D end
     ], #man_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_man_yell"),(voice_stun,"snd_man_stun"),(voice_victory,"snd_man_victory"),
     (voice_warcry, "snd_man_warcry"),  ## CC-D add
     ], #voice sounds
    "skel_human", 1.05,
    psys_game_blood,psys_game_blood_2,
    [[1.7, comp_greater_than, (1.0,face_width), (1.0,temple_width)], #constraints: ex: 1.7 > (face_width + temple_width)
     [0.3, comp_less_than, (1.0,face_width), (1.0,temple_width)],
     [1.7, comp_greater_than, (1.0,face_width), (1.0,face_depth)],
     [0.3, comp_less_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [1.7, comp_greater_than, (1.0,eyebrow_height), (1.0,eyebrow_position)],
     [-0.7, comp_less_than, (1.0,nose_size), (-1.0,nose_shape)],
     [0.7, comp_greater_than, (1.0,nose_size), (-1.0,nose_shape)],
     [2.7, comp_greater_than, (1.0,chin_size), (1.0,mouth_nose_distance), (1.0,nose_height), (-1.0,face_width)],
     ]
  ),
  
  (#12
    "elven_woman", skf_use_morph_key_10,
#CC-C begin
    "woman_body_y",  "woman_calf_l", "f_handL",
    "female_head_elven", woman_face_keys,
#CC-C begin
    ["woman_hair_yu1","woman_hair_yu2","woman_hair_yu3","woman_hair_yu4","woman_hair_yu5","woman_hair_yu6","woman_hair_yu6b","woman_hair_yu7","woman_hair_yu8","woman_hair_yu9","woman_hair_yu10","woman_hair_yu11","woman_hair_yu12","woman_hair_yu13","woman_hair_yu13b","woman_hair_yu14","woman_hair_yu15","woman_hair_yu20","woman_hair_yu17","woman_hair_yu18","woman_hair_yu19","woman_hair_yu16","woman_hair_yu21","woman_hair_yu22","woman_hair_yu23","woman_hair_yu23x","sib_leia","rensibhair2","sib_curly","hair_ren05","hair_ren03","woman_hair_q2","hair_punk","twintale_roll","maidenhair","hairmessy","longshoulder","ponytail","longstraight","courthair","slickedback","shortbob","shortlayer","woman_hair_p","woman_hair_n","woman_hair_o","woman_hair_q","woman_hair_r","woman_hair_t","woman_hair_s","onnna_kishi_hair"], #woman_hair_meshes  ## CC-D add
#    ["woman_hair_a","woman_hair_b","woman_hair_c","woman_hair_d","woman_hair_e","woman_hair_f","woman_hair_g"], #woman_hair_meshes
    ["acc1","acc2","acc3","acc4","acc5","acc6","acc7","acc8","acc9","acc10","acc11","acc12","acc13", "acc14","accessory_cigar_simple","accessory_pipe_simple","accessory_grashalm_simple","accessory_single_earing","accessory_flower_daisy",],  ## CC-D add
#    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    ["hair_blonde", "hair_red", "hair_brunette", "hair_black", "hair_white"], #hair textures
    [],
    [("womanface_young3y",0xffeafcec,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),  ## CC-D 0xffe3e8ef->0xffeafcec
     ("womanface_by",0xffdfdfdf,["hair_blonde"],[0xffa5481f, 0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_a",0xffe8dfe5,["hair_blonde"],[0xff502a19, 0xff19100c, 0xff0c0d19]),
     ("womanface_brown",0xffaf9f7e,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]),#wimanface_brown2
     ("womanface_african2y",0xff808080,["hair_blonde"],[0xff120808, 0xff007080c]),
     ("womanface_b2",0xffe3e8ef,["hair_blonde"],[0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c]),
     ("womanface_young2y_x",0xffabd8ff,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]),  ## CC-D 0xffaf9f7e->0xffabd8ff
     ("womanface_young_grey2",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]), ##### occc imported from MP 
     ("womanface_young2y",0xffdfefe1,["hair_blonde"],[0xffbbcded, 0xffffffff, 0xffb04717, 0xff502a19, 0xff19100c, 0xff0c0d19]), ##### occc imported from MP 
	 ("wimanface_brown2",0xffaf9f7e,["hair_blonde"],[0xff19100c, 0xff0c0d19, 0xff007080c]), ##### occc imported from MP 
#     ("womanface_midage",0xffe5eaf0,["hair_black","hair_brunette","hair_red","hair_white"],[0xffffcded, 0xffbbcded, 0xff99eebb]),
     ],#woman_face_textures
    [(voice_die,"snd_woman_die"),(voice_hit,"snd_woman_hit"),(voice_grunt,"snd_woman_grunt"),(voice_grunt_long,"snd_woman_grunt"),(voice_yell,"snd_woman_yell"),(voice_victory,"snd_woman_victory"),
     (voice_warcry, "snd_woman_warcry"), (voice_stun, "snd_woman_stun"),  ## CC-D add
     ], #voice sounds
#CC-C end
    "skel_human", 1.05,
    psys_game_blood,psys_game_blood_2,
  ),
  
## CC-D begin
#occc 
  (#13
    "ghost", 0,
    "gohst", "gohst", "gohst",
    "gohst", undead_face_keys,
    ["man_hair_p"], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("undeadface_a",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [(voice_die,"snd_man_die"),(voice_hit,"snd_man_hit"),(voice_grunt,"snd_man_grunt"),(voice_grunt_long,"snd_man_grunt_long"),(voice_yell,"snd_man_yell"),(voice_stun,"snd_man_stun"),(voice_victory,"snd_man_victory"),
     (voice_warcry, "snd_man_warcry"),], #voice sounds
    "skel_human", 1.0,
    psys_game_blood,psys_game_blood_2,
  ),
  (#14
    "joke_minotaur", 0,
    "gohst", "gohst", "gohst",
    "gohst", undead_face_keys,
    ["man_hair_p"], #man_hair_meshes ,
    [], #beard meshes ,
    ["hair_blonde"], #hair textures
    [], #beard_materials
    [("undeadface_a",0xffffffff,["hair_blonde"],[0xffffffff, 0xffffffff]),
     ], #undead_face_textures,
    [(voice_die,"snd_occc_mino_slaughter"),(voice_hit,"snd_occc_mino_moo"),(voice_grunt,"snd_occc_mino_moo"),(voice_grunt_long,"snd_occc_mino_moo"),(voice_yell,"snd_occc_mino_moo"),(voice_stun,"snd_occc_mino_moo"),(voice_victory,"snd_occc_mino_moo"),
     (voice_warcry, "snd_occc_mino_moo"),], #voice sounds
    "skel_human", 1.4,#1.25
    psys_game_blood,psys_game_blood_2,
  ),

##  (
##    "undead", 0,
##    "undead_body", "undead_calf_l", "undead_handL",
##    "undead_head", undead_face_keys,
##    [],
##    [],
##    [],
##    [],
##    [("undeadface_a",0xffffffff,[]),
##     ("undeadface_b",0xffcaffc0,[]),
##     ], #undead_face_textures
##    [], #voice sounds
##    "skel_human", 1.0,
##  ),
]

# modmerger_start version=201 type=2
try:
    component_name = "skins"
    var_set = { "skins" : skins }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end

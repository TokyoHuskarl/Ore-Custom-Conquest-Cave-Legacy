from header_common import *

###################################################
# header_troops.py
# This file contains declarations for troops
# DO NOT EDIT THIS FILE!
###################################################

#Troop flags
tf_male           = 0
tf_female         = 1
tf_undead         = 2
## CC-D begin: add extra races
tf_troll          = 3
tf_skeleton       = 4
tf_dog            = 5
tf_lizardman      = 6
tf_balrog         = 7
## CC-D end
## occc start
tf_nordic_man     = 8
tf_girl			  = 9
tf_gaolu_female	  = 10
tf_elf_male       = 11
tf_elf_female     = 12
tf_ghost     	  = 13
tf_joke_minotaur  = 14
## occc end

troop_type_mask   = 0x0000000f
tf_hero              = 0x00000010
tf_inactive          = 0x00000020
tf_unkillable        = 0x00000040
tf_allways_fall_dead = 0x00000080
tf_no_capture_alive  = 0x00000100
tf_mounted           = 0x00000400 #Troop's movement speed on map is determined by riding skill.
tf_is_merchant       = 0x00001000 #When set, troop does not equip stuff he owns
tf_randomize_face    = 0x00008000 #randomize face at the beginning of the game.

tf_guarantee_boots            = 0x00100000
tf_guarantee_armor            = 0x00200000
tf_guarantee_helmet           = 0x00400000
tf_guarantee_gloves           = 0x00800000
tf_guarantee_horse            = 0x01000000
tf_guarantee_shield           = 0x02000000
tf_guarantee_ranged           = 0x04000000
tf_guarantee_polearm          = 0x08000000
tf_unmoveable_in_party_window = 0x10000000

# Character attributes...
ca_strength     = 0
ca_agility      = 1
ca_intelligence = 2
ca_charisma     = 3

wpt_one_handed_weapon = 0
wpt_two_handed_weapon = 1
wpt_polearm           = 2
wpt_archery           = 3
wpt_crossbow          = 4
wpt_throwing          = 5
wpt_firearm           = 6


#personality modifiers:
# courage 8 means neutral
courage_4  = 0x0004
courage_5  = 0x0005
courage_6  = 0x0006
courage_7  = 0x0007
courage_8  = 0x0008
courage_9  = 0x0009
courage_10 = 0x000A
courage_11 = 0x000B
courage_12 = 0x000C
courage_13 = 0x000D
courage_14 = 0x000E
courage_15 = 0x000F

aggresiveness_1  = 0x0010
aggresiveness_2  = 0x0020
aggresiveness_3  = 0x0030
aggresiveness_4  = 0x0040
aggresiveness_5  = 0x0050
aggresiveness_6  = 0x0060
aggresiveness_7  = 0x0070
aggresiveness_8  = 0x0080
aggresiveness_9  = 0x0090
aggresiveness_10 = 0x00A0
aggresiveness_11 = 0x00B0
aggresiveness_12 = 0x00C0
aggresiveness_13 = 0x00D0
aggresiveness_14 = 0x00E0
aggresiveness_15 = 0x00F0

is_bandit        = 0x0100
#-----------------------------------
#these also in sentences.py
tsf_site_id_mask = 0x0000ffff
tsf_entry_mask   = 0x00ff0000
tsf_entry_bits   = 16

def entry(n):
  return (((n) << tsf_entry_bits) & tsf_entry_mask)
#-------------------------------------

str_1            = bignum | 0x00000001
str_2            = bignum | 0x00000002
str_3            = bignum | 0x00000003
str_4            = bignum | 0x00000004
str_5            = bignum | 0x00000005
str_6            = bignum | 0x00000006
str_7            = bignum | 0x00000007
str_8            = bignum | 0x00000008
str_9            = bignum | 0x00000009
str_10           = bignum | 0x0000000a
str_11           = bignum | 0x0000000b
str_12           = bignum | 0x0000000c
str_13           = bignum | 0x0000000d
str_14           = bignum | 0x0000000e
str_15           = bignum | 0x0000000f
str_16           = bignum | 0x00000010
str_17           = bignum | 0x00000011
str_18           = bignum | 0x00000012
str_19           = bignum | 0x00000013
str_20           = bignum | 0x00000014
str_21           = bignum | 0x00000015
str_22           = bignum | 0x00000016
str_23           = bignum | 0x00000017
str_24           = bignum | 0x00000018
str_25           = bignum | 0x00000019
str_26           = bignum | 0x0000001a
str_27           = bignum | 0x0000001b
str_28           = bignum | 0x0000001c
str_29           = bignum | 0x0000001d
str_30           = bignum | 0x0000001e
str_31           = bignum | 0x0000001f
str_32           = bignum | 0x00000020
str_33           = bignum | 0x00000021
str_34           = bignum | 0x00000022
str_35           = bignum | 0x00000023
str_36           = bignum | 0x00000024
str_37           = bignum | 0x00000025
str_38           = bignum | 0x00000026
str_39           = bignum | 0x00000027
str_40           = bignum | 0x00000028
str_41           = bignum | 0x00000029
str_42           = bignum | 0x0000002a
str_43           = bignum | 0x0000002b
str_44           = bignum | 0x0000002c
str_45           = bignum | 0x0000002d
str_46           = bignum | 0x0000002e
str_47           = bignum | 0x0000002f
str_48           = bignum | 0x00000030
str_49           = bignum | 0x00000031
str_50           = bignum | 0x00000032
str_51           = bignum | 0x00000033
str_52           = bignum | 0x00000034
str_53           = bignum | 0x00000035
str_54           = bignum | 0x00000036
str_55           = bignum | 0x00000037
str_56           = bignum | 0x00000038
str_57           = bignum | 0x00000039
str_58           = bignum | 0x0000003a
str_59           = bignum | 0x0000003b
str_60           = bignum | 0x0000003c
str_61           = bignum | 0x0000003d
str_62           = bignum | 0x0000003e
str_63           = bignum | 0x0000003f
str_64           = bignum | 0x00000040
str_65           = bignum | 0x00000041
str_66           = bignum | 0x00000042
str_67           = bignum | 0x00000043
str_68           = bignum | 0x00000044
str_69           = bignum | 0x00000045
str_70           = bignum | 0x00000046
str_71           = bignum | 0x00000047
str_72           = bignum | 0x00000048
str_73           = bignum | 0x00000049
str_74           = bignum | 0x0000004a
str_75           = bignum | 0x0000004b
str_76           = bignum | 0x0000004c
str_77           = bignum | 0x0000004d
str_78           = bignum | 0x0000004e
str_79           = bignum | 0x0000004f
str_80           = bignum | 0x00000050
str_81           = bignum | 0x00000051
str_82           = bignum | 0x00000052
str_83           = bignum | 0x00000053
str_84           = bignum | 0x00000054
str_85           = bignum | 0x00000055
str_86           = bignum | 0x00000056
str_87           = bignum | 0x00000057
str_88           = bignum | 0x00000058
str_89           = bignum | 0x00000059
str_90           = bignum | 0x0000005a
str_91           = bignum | 0x0000005b
str_92           = bignum | 0x0000005c
str_93           = bignum | 0x0000005d
str_94           = bignum | 0x0000005e
str_95           = bignum | 0x0000005f
str_96           = bignum | 0x00000060
str_97           = bignum | 0x00000061
str_98           = bignum | 0x00000062
str_99           = bignum | 0x00000063
str_100          = bignum | 0x00000064
str_101          = bignum | 0x00000065
str_102          = bignum | 0x00000066
str_103          = bignum | 0x00000067
str_104          = bignum | 0x00000068
str_105          = bignum | 0x00000069
str_106          = bignum | 0x0000006a
str_107          = bignum | 0x0000006b
str_108          = bignum | 0x0000006c
str_109          = bignum | 0x0000006d
str_110          = bignum | 0x0000006e
str_111          = bignum | 0x0000006f
str_112          = bignum | 0x00000070
str_113          = bignum | 0x00000071
str_114          = bignum | 0x00000072
str_115          = bignum | 0x00000073
str_116          = bignum | 0x00000074
str_117          = bignum | 0x00000075
str_118          = bignum | 0x00000076
str_119          = bignum | 0x00000077
str_120          = bignum | 0x00000078
str_121          = bignum | 0x00000079
str_122          = bignum | 0x0000007a
str_123          = bignum | 0x0000007b
str_124          = bignum | 0x0000007c
str_125          = bignum | 0x0000007d
str_126          = bignum | 0x0000007e
str_127          = bignum | 0x0000007f
str_128          = bignum | 0x00000080
str_129          = bignum | 0x00000081
str_130          = bignum | 0x00000082
str_131          = bignum | 0x00000083
str_132          = bignum | 0x00000084
str_133          = bignum | 0x00000085
str_134          = bignum | 0x00000086
str_135          = bignum | 0x00000087
str_136          = bignum | 0x00000088
str_137          = bignum | 0x00000089
str_138          = bignum | 0x0000008a
str_139          = bignum | 0x0000008b
str_140          = bignum | 0x0000008c
str_141          = bignum | 0x0000008d
str_142          = bignum | 0x0000008e
str_143          = bignum | 0x0000008f
str_144          = bignum | 0x00000090
str_145          = bignum | 0x00000091
str_146          = bignum | 0x00000092
str_147          = bignum | 0x00000093
str_148          = bignum | 0x00000094
str_149          = bignum | 0x00000095
str_150          = bignum | 0x00000096
str_151          = bignum | 0x00000097
str_152          = bignum | 0x00000098
str_153          = bignum | 0x00000099
str_154          = bignum | 0x0000009a
str_155          = bignum | 0x0000009b
str_156          = bignum | 0x0000009c
str_157          = bignum | 0x0000009d
str_158          = bignum | 0x0000009e
str_159          = bignum | 0x0000009f
str_160          = bignum | 0x000000a0
str_161          = bignum | 0x000000a1
str_162          = bignum | 0x000000a2
str_163          = bignum | 0x000000a3
str_164          = bignum | 0x000000a4
str_165          = bignum | 0x000000a5
str_166          = bignum | 0x000000a6
str_167          = bignum | 0x000000a7
str_168          = bignum | 0x000000a8
str_169          = bignum | 0x000000a9
str_170          = bignum | 0x000000aa
str_171          = bignum | 0x000000ab
str_172          = bignum | 0x000000ac
str_173          = bignum | 0x000000ad
str_174          = bignum | 0x000000ae
str_175          = bignum | 0x000000af
str_176          = bignum | 0x000000b0
str_177          = bignum | 0x000000b1
str_178          = bignum | 0x000000b2
str_179          = bignum | 0x000000b3
str_180          = bignum | 0x000000b4
str_181          = bignum | 0x000000b5
str_182          = bignum | 0x000000b6
str_183          = bignum | 0x000000b7
str_184          = bignum | 0x000000b8
str_185          = bignum | 0x000000b9
str_186          = bignum | 0x000000ba
str_187          = bignum | 0x000000bb
str_188          = bignum | 0x000000bc
str_189          = bignum | 0x000000bd
str_190          = bignum | 0x000000be
str_191          = bignum | 0x000000bf
str_192          = bignum | 0x000000c0
str_193          = bignum | 0x000000c1
str_194          = bignum | 0x000000c2
str_195          = bignum | 0x000000c3
str_196          = bignum | 0x000000c4
str_197          = bignum | 0x000000c5
str_198          = bignum | 0x000000c6
str_199          = bignum | 0x000000c7
str_200          = bignum | 0x000000c8
str_201          = bignum | 0x000000c9
str_202          = bignum | 0x000000ca
str_203          = bignum | 0x000000cb
str_204          = bignum | 0x000000cc
str_205          = bignum | 0x000000cd
str_206          = bignum | 0x000000ce
str_207          = bignum | 0x000000cf
str_208          = bignum | 0x000000d0
str_209          = bignum | 0x000000d1
str_210          = bignum | 0x000000d2
str_211          = bignum | 0x000000d3
str_212          = bignum | 0x000000d4
str_213          = bignum | 0x000000d5
str_214          = bignum | 0x000000d6
str_215          = bignum | 0x000000d7
str_216          = bignum | 0x000000d8
str_217          = bignum | 0x000000d9
str_218          = bignum | 0x000000da
str_219          = bignum | 0x000000db
str_220          = bignum | 0x000000dc
str_221          = bignum | 0x000000dd
str_222          = bignum | 0x000000de
str_223          = bignum | 0x000000df
str_224          = bignum | 0x000000e0
str_225          = bignum | 0x000000e1
str_226          = bignum | 0x000000e2
str_227          = bignum | 0x000000e3
str_228          = bignum | 0x000000e4
str_229          = bignum | 0x000000e5
str_230          = bignum | 0x000000e6
str_231          = bignum | 0x000000e7
str_232          = bignum | 0x000000e8
str_233          = bignum | 0x000000e9
str_234          = bignum | 0x000000ea
str_235          = bignum | 0x000000eb
str_236          = bignum | 0x000000ec
str_237          = bignum | 0x000000ed
str_238          = bignum | 0x000000ee
str_239          = bignum | 0x000000ef
str_240          = bignum | 0x000000f0
str_241          = bignum | 0x000000f1
str_242          = bignum | 0x000000f2
str_243          = bignum | 0x000000f3
str_244          = bignum | 0x000000f4
str_245          = bignum | 0x000000f5
str_246          = bignum | 0x000000f6
str_247          = bignum | 0x000000f7
str_248          = bignum | 0x000000f8
str_249          = bignum | 0x000000f9
str_250          = bignum | 0x000000fa
str_251          = bignum | 0x000000fb
str_252          = bignum | 0x000000fc
str_253          = bignum | 0x000000fd
str_254          = bignum | 0x000000fe
str_255          = bignum | 0x000000ff

agi_1            = bignum | 0x00000100
agi_2            = bignum | 0x00000200
agi_3            = bignum | 0x00000300
agi_4            = bignum | 0x00000400
agi_5            = bignum | 0x00000500
agi_6            = bignum | 0x00000600
agi_7            = bignum | 0x00000700
agi_8            = bignum | 0x00000800
agi_9            = bignum | 0x00000900
agi_10           = bignum | 0x00000a00
agi_11           = bignum | 0x00000b00
agi_12           = bignum | 0x00000c00
agi_13           = bignum | 0x00000d00
agi_14           = bignum | 0x00000e00
agi_15           = bignum | 0x00000f00
agi_16           = bignum | 0x00001000
agi_17           = bignum | 0x00001100
agi_18           = bignum | 0x00001200
agi_19           = bignum | 0x00001300
agi_20           = bignum | 0x00001400
agi_21           = bignum | 0x00001500
agi_22           = bignum | 0x00001600
agi_23           = bignum | 0x00001700
agi_24           = bignum | 0x00001800
agi_25           = bignum | 0x00001900
agi_26           = bignum | 0x00001a00
agi_27           = bignum | 0x00001b00
agi_28           = bignum | 0x00001c00
agi_29           = bignum | 0x00001d00
agi_30           = bignum | 0x00001e00
agi_31           = bignum | 0x00001f00
agi_32           = bignum | 0x00002000
agi_33           = bignum | 0x00002100
agi_34           = bignum | 0x00002200
agi_35           = bignum | 0x00002300
agi_36           = bignum | 0x00002400
agi_37           = bignum | 0x00002500
agi_38           = bignum | 0x00002600
agi_39           = bignum | 0x00002700
agi_40           = bignum | 0x00002800
agi_41           = bignum | 0x00002900
agi_42           = bignum | 0x00002a00
agi_43           = bignum | 0x00002b00
agi_44           = bignum | 0x00002c00
agi_45           = bignum | 0x00002d00
agi_46           = bignum | 0x00002e00
agi_47           = bignum | 0x00002f00
agi_48           = bignum | 0x00003000
agi_49           = bignum | 0x00003100
agi_50           = bignum | 0x00003200
agi_51           = bignum | 0x00003300
agi_52           = bignum | 0x00003400
agi_53           = bignum | 0x00003500
agi_54           = bignum | 0x00003600
agi_55           = bignum | 0x00003700
agi_56           = bignum | 0x00003800
agi_57           = bignum | 0x00003900
agi_58           = bignum | 0x00003a00
agi_59           = bignum | 0x00003b00
agi_60           = bignum | 0x00003c00
agi_61           = bignum | 0x00003d00
agi_62           = bignum | 0x00003e00
agi_63           = bignum | 0x00003f00
agi_64           = bignum | 0x00004000
agi_65           = bignum | 0x00004100
agi_66           = bignum | 0x00004200
agi_67           = bignum | 0x00004300
agi_68           = bignum | 0x00004400
agi_69           = bignum | 0x00004500
agi_70           = bignum | 0x00004600
agi_71           = bignum | 0x00004700
agi_72           = bignum | 0x00004800
agi_73           = bignum | 0x00004900
agi_74           = bignum | 0x00004a00
agi_75           = bignum | 0x00004b00
agi_76           = bignum | 0x00004c00
agi_77           = bignum | 0x00004d00
agi_78           = bignum | 0x00004e00
agi_79           = bignum | 0x00004f00
agi_80           = bignum | 0x00005000
agi_81           = bignum | 0x00005100
agi_82           = bignum | 0x00005200
agi_83           = bignum | 0x00005300
agi_84           = bignum | 0x00005400
agi_85           = bignum | 0x00005500
agi_86           = bignum | 0x00005600
agi_87           = bignum | 0x00005700
agi_88           = bignum | 0x00005800
agi_89           = bignum | 0x00005900
agi_90           = bignum | 0x00005a00
agi_91           = bignum | 0x00005b00
agi_92           = bignum | 0x00005c00
agi_93           = bignum | 0x00005d00
agi_94           = bignum | 0x00005e00
agi_95           = bignum | 0x00005f00
agi_96           = bignum | 0x00006000
agi_97           = bignum | 0x00006100
agi_98           = bignum | 0x00006200
agi_99           = bignum | 0x00006300
agi_100          = bignum | 0x00006400
agi_101          = bignum | 0x00006500
agi_102          = bignum | 0x00006600
agi_103          = bignum | 0x00006700
agi_104          = bignum | 0x00006800
agi_105          = bignum | 0x00006900
agi_106          = bignum | 0x00006a00
agi_107          = bignum | 0x00006b00
agi_108          = bignum | 0x00006c00
agi_109          = bignum | 0x00006d00
agi_110          = bignum | 0x00006e00
agi_111          = bignum | 0x00006f00
agi_112          = bignum | 0x00007000
agi_113          = bignum | 0x00007100
agi_114          = bignum | 0x00007200
agi_115          = bignum | 0x00007300
agi_116          = bignum | 0x00007400
agi_117          = bignum | 0x00007500
agi_118          = bignum | 0x00007600
agi_119          = bignum | 0x00007700
agi_120          = bignum | 0x00007800
agi_121          = bignum | 0x00007900
agi_122          = bignum | 0x00007a00
agi_123          = bignum | 0x00007b00
agi_124          = bignum | 0x00007c00
agi_125          = bignum | 0x00007d00
agi_126          = bignum | 0x00007e00
agi_127          = bignum | 0x00007f00
agi_128          = bignum | 0x00008000
agi_129          = bignum | 0x00008100
agi_130          = bignum | 0x00008200
agi_131          = bignum | 0x00008300
agi_132          = bignum | 0x00008400
agi_133          = bignum | 0x00008500
agi_134          = bignum | 0x00008600
agi_135          = bignum | 0x00008700
agi_136          = bignum | 0x00008800
agi_137          = bignum | 0x00008900
agi_138          = bignum | 0x00008a00
agi_139          = bignum | 0x00008b00
agi_140          = bignum | 0x00008c00
agi_141          = bignum | 0x00008d00
agi_142          = bignum | 0x00008e00
agi_143          = bignum | 0x00008f00
agi_144          = bignum | 0x00009000
agi_145          = bignum | 0x00009100
agi_146          = bignum | 0x00009200
agi_147          = bignum | 0x00009300
agi_148          = bignum | 0x00009400
agi_149          = bignum | 0x00009500
agi_150          = bignum | 0x00009600
agi_151          = bignum | 0x00009700
agi_152          = bignum | 0x00009800
agi_153          = bignum | 0x00009900
agi_154          = bignum | 0x00009a00
agi_155          = bignum | 0x00009b00
agi_156          = bignum | 0x00009c00
agi_157          = bignum | 0x00009d00
agi_158          = bignum | 0x00009e00
agi_159          = bignum | 0x00009f00
agi_160          = bignum | 0x0000a000
agi_161          = bignum | 0x0000a100
agi_162          = bignum | 0x0000a200
agi_163          = bignum | 0x0000a300
agi_164          = bignum | 0x0000a400
agi_165          = bignum | 0x0000a500
agi_166          = bignum | 0x0000a600
agi_167          = bignum | 0x0000a700
agi_168          = bignum | 0x0000a800
agi_169          = bignum | 0x0000a900
agi_170          = bignum | 0x0000aa00
agi_171          = bignum | 0x0000ab00
agi_172          = bignum | 0x0000ac00
agi_173          = bignum | 0x0000ad00
agi_174          = bignum | 0x0000ae00
agi_175          = bignum | 0x0000af00
agi_176          = bignum | 0x0000b000
agi_177          = bignum | 0x0000b100
agi_178          = bignum | 0x0000b200
agi_179          = bignum | 0x0000b300
agi_180          = bignum | 0x0000b400
agi_181          = bignum | 0x0000b500
agi_182          = bignum | 0x0000b600
agi_183          = bignum | 0x0000b700
agi_184          = bignum | 0x0000b800
agi_185          = bignum | 0x0000b900
agi_186          = bignum | 0x0000ba00
agi_187          = bignum | 0x0000bb00
agi_188          = bignum | 0x0000bc00
agi_189          = bignum | 0x0000bd00
agi_190          = bignum | 0x0000be00
agi_191          = bignum | 0x0000bf00
agi_192          = bignum | 0x0000c000
agi_193          = bignum | 0x0000c100
agi_194          = bignum | 0x0000c200
agi_195          = bignum | 0x0000c300
agi_196          = bignum | 0x0000c400
agi_197          = bignum | 0x0000c500
agi_198          = bignum | 0x0000c600
agi_199          = bignum | 0x0000c700
agi_200          = bignum | 0x0000c800
agi_201          = bignum | 0x0000c900
agi_202          = bignum | 0x0000ca00
agi_203          = bignum | 0x0000cb00
agi_204          = bignum | 0x0000cc00
agi_205          = bignum | 0x0000cd00
agi_206          = bignum | 0x0000ce00
agi_207          = bignum | 0x0000cf00
agi_208          = bignum | 0x0000d000
agi_209          = bignum | 0x0000d100
agi_210          = bignum | 0x0000d200
agi_211          = bignum | 0x0000d300
agi_212          = bignum | 0x0000d400
agi_213          = bignum | 0x0000d500
agi_214          = bignum | 0x0000d600
agi_215          = bignum | 0x0000d700
agi_216          = bignum | 0x0000d800
agi_217          = bignum | 0x0000d900
agi_218          = bignum | 0x0000da00
agi_219          = bignum | 0x0000db00
agi_220          = bignum | 0x0000dc00
agi_221          = bignum | 0x0000dd00
agi_222          = bignum | 0x0000de00
agi_223          = bignum | 0x0000df00
agi_224          = bignum | 0x0000e000
agi_225          = bignum | 0x0000e100
agi_226          = bignum | 0x0000e200
agi_227          = bignum | 0x0000e300
agi_228          = bignum | 0x0000e400
agi_229          = bignum | 0x0000e500
agi_230          = bignum | 0x0000e600
agi_231          = bignum | 0x0000e700
agi_232          = bignum | 0x0000e800
agi_233          = bignum | 0x0000e900
agi_234          = bignum | 0x0000ea00
agi_235          = bignum | 0x0000eb00
agi_236          = bignum | 0x0000ec00
agi_237          = bignum | 0x0000ed00
agi_238          = bignum | 0x0000ee00
agi_239          = bignum | 0x0000ef00
agi_240          = bignum | 0x0000f000
agi_241          = bignum | 0x0000f100
agi_242          = bignum | 0x0000f200
agi_243          = bignum | 0x0000f300
agi_244          = bignum | 0x0000f400
agi_245          = bignum | 0x0000f500
agi_246          = bignum | 0x0000f600
agi_247          = bignum | 0x0000f700
agi_248          = bignum | 0x0000f800
agi_249          = bignum | 0x0000f900
agi_250          = bignum | 0x0000fa00
agi_251          = bignum | 0x0000fb00
agi_252          = bignum | 0x0000fc00
agi_253          = bignum | 0x0000fd00
agi_254          = bignum | 0x0000fe00
agi_255          = bignum | 0x0000ff00

int_3            = bignum | 0x00030000
int_4            = bignum | 0x00040000
int_5            = bignum | 0x00050000
int_6            = bignum | 0x00060000
int_7            = bignum | 0x00070000
int_8            = bignum | 0x00080000
int_9            = bignum | 0x00090000
int_10           = bignum | 0x000a0000
int_11           = bignum | 0x000b0000
int_12           = bignum | 0x000c0000
int_13           = bignum | 0x000d0000
int_14           = bignum | 0x000e0000
int_15           = bignum | 0x000f0000
int_16           = bignum | 0x00100000
int_17           = bignum | 0x00110000
int_18           = bignum | 0x00120000
int_19           = bignum | 0x00130000
int_20           = bignum | 0x00140000
int_21           = bignum | 0x00150000
int_22           = bignum | 0x00160000
int_23           = bignum | 0x00170000
int_24           = bignum | 0x00180000
int_25           = bignum | 0x00190000
int_26           = bignum | 0x001a0000
int_27           = bignum | 0x001b0000
int_28           = bignum | 0x001c0000
int_29           = bignum | 0x001d0000
int_30           = bignum | 0x001e0000


cha_3            = bignum | 0x03000000
cha_4            = bignum | 0x04000000
cha_5            = bignum | 0x05000000
cha_6            = bignum | 0x06000000
cha_7            = bignum | 0x07000000
cha_8            = bignum | 0x08000000
cha_9            = bignum | 0x09000000
cha_10           = bignum | 0x0a000000
cha_11           = bignum | 0x0b000000
cha_12           = bignum | 0x0c000000
cha_13           = bignum | 0x0d000000
cha_14           = bignum | 0x0e000000
cha_15           = bignum | 0x0f000000
cha_16           = bignum | 0x10000000
cha_17           = bignum | 0x11000000
cha_18           = bignum | 0x12000000
cha_19           = bignum | 0x13000000
cha_20           = bignum | 0x14000000
cha_21           = bignum | 0x15000000
cha_22           = bignum | 0x16000000
cha_23           = bignum | 0x17000000
cha_24           = bignum | 0x18000000
cha_25           = bignum | 0x19000000
cha_26           = bignum | 0x1a000000
cha_27           = bignum | 0x1b000000
cha_28           = bignum | 0x1c000000
cha_29           = bignum | 0x1d000000
cha_30           = bignum | 0x1e000000

level_mask       = 0x000000FF
level_bits       = 32

def level(v):
  if (v > level_mask):
    v = level_mask
  return (bignum|v) << level_bits
  
def_attrib = str_5 | agi_5 | int_4 | cha_4

# Weapon proficiencies:
one_handed_bits = 0
two_handed_bits = 10
polearm_bits    = 20
archery_bits    = 30
crossbow_bits   = 40
throwing_bits   = 50
firearm_bits    = 60

## CC
num_weapon_proficiencies = 7
def wp_one_handed(x):
  return (((bignum |(x*3/2)) & 0x3FF) << one_handed_bits)
def wp_two_handed(x):
  return (((bignum |(x*3/2)) & 0x3FF) << two_handed_bits)
def wp_polearm(x):
  return (((bignum |(x*3/2)) & 0x3FF) << polearm_bits)
def wp_archery(x):
  return (((bignum |(x*3/2)) & 0x3FF) << archery_bits)
def wp_crossbow(x):
  return (((bignum |(x*3/2)) & 0x3FF) << crossbow_bits)
def wp_throwing(x):
  return (((bignum |(x*3/2)) & 0x3FF) << throwing_bits)
def wp_firearm(x):
  return (((bignum |(x*3/2)) & 0x3FF) << firearm_bits)
## CC

def find_troop(troops,troop_id):
  result = -1
  num_troops = len(troops)
  i_troop = 0
  while (i_troop < num_troops) and (result == -1):
    troop = troops[i_troop]
    if (troop[0] == troop_id):
      result = i_troop
    else:
      i_troop += 1
  return result



def upgrade(troops,troop1_id,troop2_id):
  troop1_no = find_troop(troops,troop1_id)
  troop2_no = find_troop(troops,troop2_id)
  if (troop1_no == -1):
    print "Error with upgrade def: Unable to find troop1-id: " + troop1_id
  elif (troop2_no == -1):
    print "Error with upgrade def: Unable to find troop2-id: " + troop2_id
  else:
    cur_troop = troops[troop1_no]
    cur_troop_length = len(cur_troop)
    if cur_troop_length == 11:
      cur_troop[11:11] = [0, 0, 0, troop2_no, 0]
    elif cur_troop_length == 12:
      cur_troop[12:12] = [0, 0, troop2_no, 0]
    elif cur_troop_length == 13:
      cur_troop[13:13] = [0, troop2_no, 0]
    else:
      cur_troop[14:14] = [troop2_no, 0]
      

def upgrade2(troops,troop1_id,troop2_id,troop3_id):
  troop1_no = find_troop(troops,troop1_id)
  troop2_no = find_troop(troops,troop2_id)
  troop3_no = find_troop(troops,troop3_id)
  if (troop1_no == -1):
    print "Error with upgrade2 def: Unable to find troop1-id: " + troop1_id
  elif (troop2_no == -1):
    print "Error with upgrade2 def: Unable to find troop2-id: " + troop2_id
  elif (troop3_no == -1):
    print "Error with upgrade2 def: Unable to find troop3-id: " + troop3_id
  else:
    cur_troop = troops[troop1_no]
    cur_troop_length = len(cur_troop)
    if cur_troop_length == 11:
      cur_troop[11:11] = [0, 0, 0, troop2_no, troop3_no]
    elif cur_troop_length == 12:
      cur_troop[12:12] = [0, 0, troop2_no, troop3_no]
    elif cur_troop_length == 13:
      cur_troop[13:13] = [0, troop2_no, troop3_no]
    else:
      cur_troop[14:14] = [troop2_no, troop3_no]

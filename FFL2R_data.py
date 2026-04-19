class GameData:
    TREASURES = [
        0x1D, 0x17, 0x00, 0x15, 0x48, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x1D, 0x44, 0x3B, 0x02, 0x10, 0x4C, 0x18, 0x45, 
        0x43, 0x32, 0x03, 0x19, 0x65, 0x43, 0x05, 0x26, 0x3F, 0x71, 0x41, 0x43, 0x3D, 0x28, 0x6C, 0x14, 0xFF, 0xFF, 0xFF, 0xFF, 
        0xFF, 0x44, 0x6E, 0x73, 0x41, 0x0a, 0x45, 0x5F, 0x2D, 0x1A, 0x46, 0x3E, 0x60, 0x08, 0x1C, 0x23, 0x6F, 0x5E, 0x40, 0x0d, 
        0x2E, 0x34, 0x0e, 0x30, 0x54, 0x09, 0x39, 0x72, 0x76, 0x47, 0x22, 0x61, 0x43, 0x46, 0x38, 0x07, 0x44, 0x45, 0x11, 0x5D, 
        0x41, 0x6F, 0x53, 0x08, 0x47, 0x34, 0x5E, 0x60, 0x2E, 0x0d, 0x23, 0x7E, 0x6A, 0x39, 0x76, 0x72, 0x12, 0x47, 0x54, 0x09, 
        0x74, 0x30, 0x61, 0x13, 0x6B
        ]
    
    MAGI = [
        # 76 total. TrueEye (0x0A) is not a real Magi but instead a plot event that flips a script variable to make the Light Cave visible.
        # It is not included in this list and not shuffled.
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, #power
        0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, #speed
        0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, #mana
        0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03, 0x03,       #defense
        0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04, #Fire
        0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, 0x05, #Ice
        0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, 0x06, #Thunder
        0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, 0x07, #Poison
        0x08, #Masmune
        0x09, #Aegis
        0x0b, #Heart
        0x0c, #Pegasus
        0x0d  #Prism 		
        ]

    newItemPrices = {
        #prices are stored in three hex, addresses read right to left.
        67 : 2500,  #stat boosting potions, changed to 2.5k each up from 1k
        68 : 2500,
        69 : 2500,
        70 : 2500,
        18 : 50000, #vampic, changed to 50,000
        126 : 25000, #selfix, changed to 25,000,
        127 : 77777, #seven sword, changed to 77,777
        }

    #tier 1 x 3 = 24 slots, 14 items
    #tier 2 x 3 = 24 slots, 16 items
    #tier 3 x 3 = 24 slots, 16 items
    #tier 4 x 4 = 32 slots, 15 items
    #tier 5 x 3 = 24 slots, 15 items
    #tier 6 x 4 = 32 slots, 15 items
    #tier 7 x 1 = 8 slots, 13 items
    #two specials
    #w/six filler items

    shopTiers = [
        [0x47, 0x24, 0x2F, 0x43, 0x44, 0x45, 0x46], #tent, cureb, healstaff, powerp, speedp, magicp, bodyp
        [0x35, 0x31, 0x3A, 0x17, 0x00, 0x01, 0x15, 0x48, 0x4F, 0x6D, 0x2A, 0x4C, 0x56, 0x67], #bronze, hammer, longs, bow, whip, punch, psi knife, sleepb, colt, stung, coin
        [0x18, 0x32, 0x36, 0x3B, 0x68, 0x02, 0x03, 0x21, 0x0f, 0x50, 0x26, 0x27, 0x28, 0x29, 0x4D, 0x71], #silver, kimono, axe, battles, abacus, rapier, kick, fireb, iceb, thunderb, fogb, musket, rocket]
        [0x19, 0x37, 0x3C, 0x64, 0x33, 0x04, 0x05, 0x55, 0x49, 0x16, 0x51, 0x25, 0x2B, 0x5A, 0x5F, 0x60], #gold, armybody, katana, golds, temptat, blitzw, goldbow, headbutt, prayerb, stoneb, smg, fireg, missle]
        [0x62, 0x3D, 0x63, 0x65, 0x0c, 0x0a, 0x0b, 0x07, 0x06, 0x10, 0x4B, 0x6E, 0x5B, 0x5C, 0x4A], #giant, armyhelm, geta, thunderaxe, flames, ices, ogreaxe, corals, sabre, counter, psis, grenade, bazooka, chainsaw
        [0x38, 0x3F, 0x73, 0x1A, 0x1B, 0x0e, 0x66, 0x08, 0x14, 0x6C, 0x52, 0x2C, 0x2D, 0x4E, 0x5D], #dragonbody, hermes, gianthelm, flameshield, iceshield, runeaxe, sypha, dragons, revenge, lasers, x-kick, deathb, magestaff, magnum, vulcan
        [0x75, 0x40, 0x3E, 0x34, 0x1C, 0x69, 0x0d, 0x6A, 0x09, 0x11, 0x53, 0x2E, 0x30, 0x6F, 0x5E], #battlebody, hecate, ninjahand, dragonshield, samuraishield, defends, muramas, suns, catclaw, jyudo, wizardstaff, flareb, laserg, tankc
        [0x39, 0x76, 0x7E, 0x7F, 0x6B, 0x22, 0x13, 0x23, 0x54, 0x72, 0x12, 0x61, 0x74], #arthur, parasuit, selffix, sevens, gungnir, xcalibr, glass, samuraibow, karate, psig, vampic, nukebomb, hyper
        [0x1D, 0x1E, 0x1F, 0x20, 0x41, 0x42, 0x70, 0x77] #cure, xcure, curse, eyedrop, elixier, soft, speedup, door
        ]

    #not-a-comprehensive list of all char encodes
    dteLookup = {
            0x00:"(end)",
            0x05:"\n",
            0x06:"\n\n",
            0x3C:"○",
            0x3D:"×",
            0x4E:"e ",
            0x4F:" t",
            0x50:"th",
            0x51:"he",
            0x52:"s ",
            0x53:"er",
            0x54:"t ",
            0x55:"ou",
            0x56:"in",
            0x57:"d ",
            0x58:" a",
            0x59:"an",
            0x5A:"re",
            0x5B:"o ",
            0x5C:" i",
            0x5D:"to",
            0x5E:" w",
            0x5F:"is",
            0x60:"at",
            0x61:" h",
            0x62:" g",
            0x63:" s",
            0x64:" m",
            0x65:"on",
            0x66:"or",
            0x67:"ll",
            0x68:"r ",
            0x69:" o",
            0x6A:"ha",
            0x6B:"ng",
            0x6C:"me",
            0x6D:"yo",
            0x6E:"ar",
            0x6F:" y",
            0x70:"hi",
            0x71:"go",
            0x72:"y ",
            0x73:"n ",
            0x74:" b",
            0x75:"ea",
            0x76:"ve",
            0x77:"'s",
            0x78:"st",
            0x79:"I ",
            0x7A:" c",
            0x7B:"a ",
            0x7C:"nd",
            0x7D:"ur",
            0x7E:" f",
            0x7F:"te",
            0x80:"se",
            0x81:"om",
            0x82:"ra",
            0x83:" d",
            0x84:"ow",
            0x85:"et",
            0x86:"ut",
            0x87:"it",
            0x88:"no",
            0x89:"as",
            0x8A:" l",
            0x8B:"en",
            0x8C:" I",
            0x8D:"of",
            0x8E:"us",
            0x8F:"ed",
            0x90:" n",
            0x91:"ro",
            0x92:"ne",
            0x93:"sh",
            0x94:"nt",
            0x95:"be",
            0x96:"l ",
            0x97:"ca",
            0x98:"le",
            0x99:"Th",
            0x9A:"u ",
            0x9B:"g ",
            0x9C:" M",
            0x9D:"lo",
            0x9E:"(Magi)",
            0x9F:"(Whip)",
            0xA0:"(Cannon)",
            0xA1:"(Gun)",
            0xA2:"©",
            0xA3:"(Shield)",
            0xA4:"(Knife)",
            0xA5:"(Staff)",
            0xA6:"(Spear)",
            0xA7:"(Sword)",
            0xA8:"(Axe)",
            0xA9:"(Bow)",
            0xAA:"(Helm)",
            0xAB:"(Glove)",
            0xAC:"(Armor)",
            0xAD:"(Boot)",
            0xAE:"(Book)",
            0xAF:"(Potion)",
            0xB0:"0",
            0xB1:"1",
            0xB2:"2",
            0xB3:"3",
            0xB4:"4",
            0xB5:"5",
            0xB6:"6",
            0xB7:"7",
            0xB8:"8",
            0xB9:"9",
            0xBA:"A",
            0xBB:"B",
            0xBC:"C",
            0xBD:"D",
            0xBE:"E",
            0xBF:"F",
            0xC0:"G",
            0xC1:"H",
            0xC2:"I",
            0xC3:"J",
            0xC4:"K",
            0xC5:"L",
            0xC6:"M",
            0xC7:"N",
            0xC8:"O",
            0xC9:"P",
            0xCA:"Q",
            0xCB:"R",
            0xCC:"S",
            0xCD:"T",
            0xCE:"U",
            0xCF:"V",
            0xD0:"W",
            0xD1:"X",
            0xD2:"Y",
            0xD3:"Z",
            0xD4:"a",
            0xD5:"b",
            0xD6:"c",
            0xD7:"d",
            0xD8:"e",
            0xD9:"f",
            0xDA:"g",
            0xDB:"h",
            0xDC:"i",
            0xDD:"j",
            0xDE:"k",
            0xDF:"l",
            0xE0:"m",
            0xE1:"n",
            0xE2:"o",
            0xE3:"p",
            0xE4:"q",
            0xE5:"r",
            0xE6:"s",
            0xE7:"t",
            0xE8:"u",
            0xE9:"v",
            0xEA:"w",
            0xEB:"x",
            0xEC:"y",
            0xED:"z",
            0xEE:"'",
            0xEF:",",
            0xF0:".",
            0xF1:"..",
            0xF2:"-",
            0xF3:"!",
            0xF4:"?",
            0xF5:":",
            0xF6:"/",
            0xFF:" "
        }

    ITEMS = {
        0x00 : "Hammer",
        0x01 : "Long Sword",
        0x02 : "Axe",
        0x03 : "Battle Sword",
        0x04 : "Katana",
        0x05 : "Gold Sword",
        0x06 : "Coral Sword",
        0x07 : "Ogre Axe",
        0x08 : "Dragon Sword",
        0x09 : "Sun Sword",
        0x0a : "Flame Sword",
        0x0b : "Ice Sword",
        0x0c : "Thunder Axe",
        0x0d : "Defend Sword",
        0x0e : "Rune Axe",
        0x0f : "Rapier",
        0x10 : "Sabre",
        0x11 : "Cat Claw",
        0x12 : "Vampric Sword",
        0x13 : "Glass Sword",
        0x14 : "Revenge Sword",
        0x15 : "Bow",
        0x16 : "Gold Bow",
        0x17 : "Bronze Shield",
        0x18 : "Silver Shield",
        0x19 : "Gold Shield",
        0x1A : "Flame Shield",
        0x1B : "Ice Shield",
        0x1C : "Dragon Shield",
        0x1D : "Cure Potion",
        0x1E : "X-Cure Potion",
        0x1F : "Curse Potion",
        0x20 : "Eye Drop",
        0x21 : "Abacus",
        0x22 : "Excalibur",
        0x23 : "Samurai Bow",
        0x24 : "Cure Book",
        0x25 : "Prayer Book",
        0x26 : "Fire Book",
        0x27 : "Ice Book",
        0x28 : "Thunder Book",
        0x29 : "Fog Book",
        0x2A : "Sleep Book",
        0x2B : "Stone Book",
        0x2C : "Death Book",
        0x2D : "Mage Staff",
        0x2E : "Wizard Staff",
        0x2F : "Heal Staff",
        0x30 : "Flare Book",
        0x31 : "Bronze Helm",
        0x32 : "Silver Helm",
        0x33 : "Gold Helm",
        0x34 : "Dragon Helm",
        0x35 : "Bronze Armor",
        0x36 : "Silver Armor",
        0x37 : "Gold Armor",
        0x38 : "Dragon Armor",
        0x39 : "Arthur Armor",
        0x3A : "Bronze Gauntlets",
        0x3B : "Silver Gauntlets",
        0x3C : "Gold Gauntlets",
        0x3D : "Giant Gauntlets",
        0x3E : "Ninja Gauntlets",
        0x3F : "Hermes Shoes",
        0x40 : "Hecate Shoes",
        0x41 : "Elixir",
        0x42 : "Soft Potion",
        0x43 : "Power Potion",
        0x44 : "Speed Potion",
        0x45 : "Magic Potion",
        0x46 : "Body Potion",
        0x47 : "Tent",
        0x48 : "Whip",
        0x49 : "Blitz Whip",
        0x4A : "Chainsaw",
        0x4B : "Counter",
        0x4C : "Colt",
        0x4D : "Musket",
        0x4E : "Magnum",
        0x4F : "Punch",
        0x50 : "Kick",
        0x51 : "Headbutt",
        0x52 : "X-Kick",
        0x53 : "Jyudo",
        0x54 : "Karate",
        0x55 : "Temptat",
        0x56 : "Stun Gun",
        0x57 : "Heat",
        0x5A : "SMG",
        0x5B : "Grenade",
        0x5C : "Bazooka",
        0x5D : "Vulcan Cannon",
        0x5E : "Tank Cannon",
        0x5F : "Fire Gun",
        0x60 : "Missile",
        0x61 : "NukeBomb",
        0x62 : "Giant Armor",
        0x63 : "Army Helm",
        0x64 : "Army Armor",
        0x65 : "Geta Shoes",
        0x66 : "Sypha",
        0x67 : "Coin",
        0x68 : "Kimono",
        0x69 : "Samurai Shield",
        0x6A : "Muramasa",
        0x6B : "Gungnir",
        0x6C : "Laser Sword",
        0x6D : "Psi Knife",
        0x6E : "Psi Sword",
        0x6F : "Laser Gun",
        0x70 : "Speed Up",
        0x71 : "Rocket",
        0x72 : "Psi Gun",
        0x73 : "Giant Helm",
        0x74 : "Hyper Cannon",
        0x75 : "Battle Armor",
        0x76 : "Parasuit",
        0x77 : "Door",
        0x7E : "Selfix",
        0x7F : "Seven Sword"
        }

    #exclude no-header entries
    noMemoCalls = (
        0, 1, 2, 3, 4, 5, 8, 9, 10, 11, 14, 15, 20, 21, 22, 23, 26, 27, 28, 29, 
        30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 45, 47, 48, 49, 
        50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 64, 65, 66, 67, 70, 71, 73, 
        74, 75, 76, 77, 84, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 
        99, 100, 102, 103, 104, 107, 108, 110, 111, 112, 113, 114, 115, 116, 117, 
        119, 120, 122, 124, 125, 126, 128, 131, 134, 135, 137, 138, 140, 141, 142, 
        143, 144, 145, 146, 147, 148, 149, 150, 151, 153, 154, 155, 156, 157, 158, 
        159, 160, 161, 162, 163, 164, 165, 166, 168, 169, 170, 171, 173, 174, 176, 
        177, 180, 183, 184, 185, 186, 187, 191, 192, 193, 194, 195, 196, 198, 199, 
        200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 
        215, 216, 217, 218, 219, 224, 225, 227, 228, 229, 230, 231, 232, 233, 234, 
        235, 236, 237
        )

# switch WarMach treasure chest flag w/ TrueEye!

# Opening Cutscene, [0, 1, 172]
# Char 2's Parent [0, 275, 39] (Will always award an Item)
# First Cave, First Platform, Left 	[5, 2, '80 00 2b e7 1d f9']
# First Cave, First Platform, Right 	[5, 3, '80 01 2d e7 17 f9']
# First Cave, Near Exit, North 	[5, 4, '80 02 3c d3 00 f9']
# First Cave, Near Exit, South 	[5, 5, '80 03 3c d4 15 f9']
# Ruins of the Ancient Gods, Floor 2 [13, 0, '80 27 24 e0 48 f9']
# Ruins of the Ancient Gods, Floor 3, Northwest  [14, 0, '80 04 11 db ff f9']
# Ruins of the Ancient Gods, Floor 3, Southwest  [14, 1, '80 05 11 dc ff f9']
# Ruins of the Ancient Gods, Floor 3, Northeast  [14, 2, '80 06 22 db ff f9']
# Ruins of the Ancient Gods, Floor 3, Southeast  [14, 3, '80 07 22 dc ff f9']
# Ruins of the Ancient Gods, Floor 4, Main North [15, 5, '80 08 1c e0 ff f9']
# Ruins of the Ancient Gods, Floor 4, Main West [15, 6, '80 09 1b e1 ff f9']
# Ruins of the Ancient Gods, Floor 4, Main East [15, 7, '80 0a 1d e1 ff f9']
# Ruins of the Ancient Gods, Floor 4, Vault West [15, 11, '80 40 29 d9 1d f9']
# Ruins of the Ancient Gods, Floor 4, Vault Northeast [15, 8, '80 0b 19 d3 00 fa']
# Ruins of the Ancient Gods, Floor 4, Vault Southeast [15, 9, '80 0c 1e d3 01 fa']
# Ruins of the Ancient Gods, Floor 4, West by Entrance [15, 10, '80 0d 1e d4 02 fa']
# Ashura's Base, Floor 3 [18, 4, '80 41 01 c3 44 f9']
# Ashura's Base, Floor 4 [19, 4, '80 42 01 c3 3b f9']
# Ashura's Base, Floor 5 [20, 0, '80 28 06 c8 02 f9']
# Ashura's Base, Exit Southeast [20, 5, '80 0e 26 dc 03 fa']
# Ashura's Base, Exit Northeast [20, 6, '80 0f 27 db 04 fa']
# Ashura's Base, Exit West [20, 7, '80 10 21 db 05 fa']
# Ashura's Tower, Floor 4 [32, 0, '80 29 10 c8 10 f9']
# Ashura's Tower, Floor 7 [35, 0, '80 2a 13 c6 4c f9']
# Ashura's Tower, Floor 9 [37, 0, '80 2b 13 d3 18 f9']
# Ashura's Tower, Ashura's Floor Southwest [38, 4, '80 43 11 da 45 f9']
# Ashura's Tower, Ashura's Floor Southeast [38, 5, '80 44 19 da 43 f9']
# Ashura's Tower, Ashura's Floor Northwest [38, 6, '80 45 13 d4 32 f9']
# Ashura's Tower, Ashura's Floor Northeast [38, 7, '80 46 18 d5 03 f9']
# Ashura Drop 1 [0, 192, 0]
# Ashura Drop 2 [0, 192, 3]
# Ashura Drop 3 [0, 192, 6]
# Ashura Drop 4 [0, 192, 9]
# Ashura Drop 5 [0, 192, 12]
# Ashura Drop 6 [0, 192, 15]
# Ashura Drop 7 [0, 192, 18]
# Dad in Giant's World [0, 339, 303]
# Giant Town, Magi House North [45, 0, '80 11 10 d5 00 fa']
# Giant Town, Magi House South [45, 1, '80 12 10 d7 07 fa']
# Giant Town, Micron House West [46, 0, '80 2c 24 ea 19 f9']
# Giant Town, Micron House East [46, 1, '80 47 2c ec 65 f9']
# Giant Town, Micron Potion Location [0, 29, 11]
# Ki's Assistant [0, 308, 34]
# Ki's Stomach [0, 31, 0]
# Ki's Heart [0, 32, 0]
# Ki's Left Hand [0, 33, 0]
# Ki's Right Hand [0, 34, 0]
# Ki's Left Foot [0, 35, 0]
# Ki's Right Foot [0, 36, 0]
# Ki's Brain [0, 37, 0]
# Meeting Apollo [0, 350, 76]
# Undersea Volcano, Floor 3 West [63, 0, '80 48 0e d0 43 f9']
# Undersea Volcano, Floor 3 East [63, 1, '80 49 0f d0 05 f9']
# Undersea Volcano, Floor 4 [64, 1, '80 2d 20 de 26 f9']
# Undersea Volcano, Exit West [65, 0, '80 13 1f da 04 fa']
# Undersea Volcano, Exit East [65, 1, '80 14 21 da 07 fa']
# Undersea Volcano, Exit TrueEye 
# Dunatis Cave, Entrance [70, 0, '80 4a 34 df 3f f9']
# Dunatis Cave, Floor 3 [72, 0, '80 2e 14 d8 71 f9']
# Dunatis Cave, Dunatis Floor [74, 2, '80 2f 1a d1 41 f9']
# Cave of Light, Floor 3 [78, 0, '80 30 0b c3 43 f9']
# Cave of Light, Floor 4 West [79, 0, '80 4b 08 c3 3d f9']
# Cave of Light, Floor 4 East [79, 1, '80 4c 15 c3 28 f9']
# Cave of Light, Floor 5 [80, 0, '80 4d 0f cf 6c f9']
# Cave of Light, Floor 6 [81, 0, '80 31 0d c3 14 f9']
# Cave of Light, Final Floor North [82, 0, '80 16 14 c5 02 fa']
# Cave of Light, Final Floor East [82, 1, '80 17 1d c9 05 fa']
# Cave of Light, Final Floor West [82, 2, '80 18 12 cc 06 fa']
# Dunatis Drop 1 [0, 492, 59]
# Dunatis Drop 2 [0, 492, 62]
# Dunatis Drop 3 [0, 492, 65]
# Dunatis Drop 4 [0, 492, 68]
# Guardian Base Storage, North-center [97, 0, '80 19 1d c3 ff f9']
# Guardian Base Storage, Northwest  [97, 1, '80 1a 1f c3 ff f9']
# Guardian Base Storage, Center  [97, 2, '80 1b 1e c6 ff f9']
# Guardian Base Storage, Northeast  [97, 3, '80 1c 19 c3 ff f9']
# Guardian Base Storage, South [97, 4, '80 1d 1c c8 ff f9']
# Guardian Base Commando [0, 400, 59]
# Guardian Base Magician [0, 401, 7]
# Guardian Base Manticore [0, 402, 7]
# Guardian Base Ogre [0, 404, 7]
# Dad's Death, Final Gift [3, 244, 282]
# Dad's Death, Ninja [3, 244, 745]
# Dad's Death, Lynn's Mom [3, 244, 1185]]
# Sewer, Entrance [110, 0, '80 4e 10 c8 44 f9']
# Hermit Crab Drop [0, 438, 14]
# Sewer, Floor 2 [111, 0, '80 32 0e c9 6e f9']
# Sewer, Floor 5 West [114, 0, '80 33 0d c6 73 f9']
# Sewer, Floor 5 East [114, 1, '80 4f 01 c3 41 f9']
# Sewer, Locked Room 1, Northwest [116, 0, '80 1e 31 c3 00 fa']
# Sewer, Locked Room 1, Southwest [116, 1, '80 1f 31 c4 01 fa']
# Sewer, Locked Room 1, Northeast [116, 2, '80 20 39 c3 02 fa']
# Sewer, Locked Room 2, Northwest [116, 4, '80 21 31 d3 03 fa']
# Sewer, Locked Room 2, Northeast [116, 5, '80 22 33 d3 05 fa']
# Sewer, Locked Room 2, Southwest [116, 6, '80 23 32 d5 06 fa']
# Venus Volcano, Floor 5, Lava [121, 1, '80 34 13 ca 0a f9']
# Venus Volcano, Floor 5, Land [121, 2, '80 50 13 cd 45 f9']
# Venus Volcano, Floor 6, West [122, 1, '80 51 05 c6 5f f9']
# Venus Volcano, Floor 6, East [122, 2, '80 52 06 c6 2d f9']
# Venus Volcano, Exit, Isolated [123, 4, '80 35 15 e4 1a f9']
# Venus Volcano, Exit, West [123, 1, '80 24 1c e2 04 fa']
# Venus Volcano, Exit, East [123, 2, '80 25 1e e2 07 fa']
# Leon's Theft [0, 420, 28] (Should always Steal a Magi)
# Venus Drop 1 [0, 193, 0]
# Venus Drop 2 [0, 193, 3]
# Venus Drop 3 [0, 193, 6]
# Venus Drop 4 [0, 193, 9]
# Venus Drop 5 [0, 193, 12]
# Venus Drop 6 [0, 193, 15]
# Venus Drop 7 [0, 193, 18]
# Venus Drop 8 [0, 43, 106]
# Race - Adamant [0, 457, 36]
# Race - Tortoise [0, 458, 36]
# Race - Lamia [0, 459, 36]
# Race - Watcher  [0, 460, 24]
# Race - Watcher (Lamia) [0, 460, 30]
# Race - Watcher (Tortoise) [0, 460, 37]
# Race - Watcher (Adamant) [0, 460, 44]
# Edo Castle, Floor 3, Center [142, 0, '80 38 22 cb 46 f9']
# Edo Castle, Floor 3, West [142, 1, '80 55 20 cb 3e f9']
# Edo Castle, Floor 3, East [142, 2, '80 56 24 cb 60 f9']
# Edo Castle, Floor 4 [143, 0, '80 39 18 cc 08 f9']
# Edo Castle, Floor 5 [144, 0, '80 57 1f d3 1c f9']
# Edo Castle, Shogun Floor [145, 5, '80 37 12 cd 23 f9']
# Banana Smuggling Boat, Middle Deck [150, 0, '80 53 2d e5 6f f9']
# Banana Smuggling Boat, Lower Deck, West [151, 2, '80 54 09 d8 5e f9']
# Banana Smuggling Boat, Lower Deck, East [151, 3, '80 36 11 d2 40 f9']
# Magnate Drop 1 [0, 468, 107]
# Magnate Drop 2 [0, 468, 110]
# Magnate Drop 3 [0, 468, 113]
# Magnate Drop 4 [0, 468, 116]
# Nasty Dungeon, Entrance, Chest 1 [202, 3, '80 60 22 c1 43 f9']
# Nasty Dungeon, Entrance, Chest 2 [202, 4, '80 61 24 c2 46 f9']
# Nasty Dungeon, Entrance, Chest 3 [202, 5, '80 62 0e c2 38 f9']
# Nasty Dungeon, Entrance, Chest 4 [202, 6, '80 63 07 c1 07 f9']
# Nasty Dungeon, Floor 2, Chest 1 [203, 0, '80 64 1d cd 44 f9']
# Nasty Dungeon, Floor 2, Chest 2 [203, 1, '80 65 24 cb 45 f9']
# Nasty Dungeon, Floor 2, Chest 3 [203, 2, '80 66 24 c5 11 f9']
# Nasty Dungeon, Floor 2, Chest 4 [203, 3, '80 67 24 c6 5d f9']
# Nasty Dungeon, Floor 3, Chest 1 [204, 0, '80 68 0e cd 41 f9']
# Nasty Dungeon, Floor 3, Chest 2 [204, 1, '80 69 0e ce 6f f9']
# Nasty Dungeon, Floor 3, Chest 3 [204, 2, '80 6a 0c dc 53 f9']
# Nasty Dungeon, Floor 3, Chest 4 [204, 3, '80 6b 0c dd 08 f9']
# Nasty Dungeon, Floor 4, Chest 1 [205, 0, '80 6c 13 e1 47 f9']
# Nasty Dungeon, Floor 4, Chest 2 [205, 1, '80 6d 13 ee 34 f9']
# Nasty Dungeon, Floor 4, Chest 3 [205, 2, '80 6e 0d d1 5e f9']
# Nasty Dungeon, Floor 4, Chest 4 [205, 3, '80 6f 23 d8 60 f9']
# Nasty Dungeon, Floor 5, Chest 1 [206, 0, '80 70 14 d4 2e f9']
# Nasty Dungeon, Floor 5, Chest 2 [206, 1, '80 71 0c d4 0d f9']
# Nasty Dungeon, Floor 5, Chest 3 [206, 2, '80 72 08 d4 23 f9']
# Nasty Dungeon, Floor 5, Chest 4 [206, 3, '80 3f 10 d4 7e f9']
# Nasty Dungeon, Floor 5, Chest 5 [206, 4, '80 73 08 ca 6a f9']
# Nasty Dungeon, Floor 5, Chest 1 [207, 0, '80 74 30 cb 39 f9']
# Nasty Dungeon, Floor 5, Chest 2 [207, 1, '80 75 19 d9 76 f9']
# Nasty Dungeon, Floor 5, Chest 3 [207, 2, '80 76 19 dd 72 f9']
# Nasty Dungeon, Floor 5, Chest 4 [207, 3, '80 77 1c dd 12 f9']
# Nasty Dungeon, Floor 6, Chest 1 [208, 0, '80 78 18 d4 47 f9']
# Nasty Dungeon, Floor 6, Chest 2 [208, 1, '80 79 1a d5 54 f9']
# Nasty Dungeon, Floor 6, Chest 3 [208, 2, '80 7a 1a d3 09 f9']
# Nasty Dungeon, Floor 6, Chest 4 [208, 3, '80 7b 10 c2 74 f9']
# Nasty Dungeon, Exit, Chest 1 [209, 1, '80 7c 09 ce 30 f9']
# Nasty Dungeon, Exit, Chest 2 [209, 2, '80 7d 2e dd 61 f9']
# Nasty Dungeon, Exit, Chest 3 [209, 3, '80 7e 18 e2 13 f9']
# Nasty Dungeon, Exit, Chest 4 [209, 4, '80 7f 22 e7 6b f9']
# Vahalla, Entrance [164, 0, '80 3a 05 c3 0d f9']
# Vahalla, Floor 2 [165, 0, '80 58 0b c8 2e f9']
# Vahalla, Floor 4 [167, 0, '80 3b 10 c3 34 f9']
# Vahalla, Floor 5 [168, 0, '80 59 08 cc 0e f9']
# Vahalla, Floor 6 [169, 0, '80 5a 05 c3 30 f9']
# Odin Drop 1 [0, 14, 0]
# Odin Drop 2 [0, 14, 3]
# Odin Drop 3 [0, 14, 6]
# Odin Drop 4 [0, 14, 9]
# Odin Drop 5 [0, 14, 12]
# Odin Drop 6 [0, 14, 15]
# Odin Drop 7 [0, 14, 18]
# Odin Drop 8 [0, 132, 15]
# Final Dungeon, Entrance [177, 0, '80 5b 22 c4 54 f9']
# Final Dungeon, Floor 2 [178, 0, '80 5c 09 c5 09 f9']
# Final Dungeon, Floor 4 [180, 0, '80 5d 15 ce 39 f9']
# Final Dungeon, Floor 5 [181, 0, '80 5e 24 d1 72 f9']
# Final Dungeon, Floor 6 [182, 0, '80 3c 20 c7 76 f9']
# Final Dungeon, Floor 7 [183, 0, '80 5f 22 c4 47 f9']
# Final Dungeon, Floor 9 [185, 0, '80 3d 15 c3 22 f9']
# Final Dungeon, Floor 10 [186, 0, '80 3e 25 ce 61 f9']
# Final World, WarMach Chest [0, 71, 7]
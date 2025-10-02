class GameData:
    treasures = [
        0x1D,
        0x17,
        0x00,
        0x15,
        0x48,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0x1D,
        0x44,
        0x3B,
        0x02,
        0x10,
        0x4C,
        0x18,
        0x45,
        0x43,
        0x32,
        0x03,
        0x19,
        0x65,
        0x43,
        0x05,
        0x26,
        0x3F,
        0x71,
        0x41,
        0x43,
        0x3D,
        0x28,
        0x6C,
        0x14,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0xFF,
        0x44,
        0x6E,
        0x73,
        0x41,
        0x0A,
        0x45,
        0x5F,
        0x2D,
        0x1A,
        0x46,
        0x3E,
        0x60,
        0x08,
        0x1C,
        0x23,
        0x6F,
        0x5E,
        0x40,
        0x0D,
        0x2E,
        0x34,
        0x0E,
        0x30,
        0x54,
        0x09,
        0x39,
        0x72,
        0x76,
        0x47,
        0x22,
        0x61,
        0x43,
        0x46,
        0x38,
        0x07,
        0x44,
        0x45,
        0x11,
        0x5D,
        0x41,
        0x6F,
        0x53,
        0x08,
        0x47,
        0x34,
        0x5E,
        0x60,
        0x2E,
        0x0D,
        0x23,
        0x7E,
        0x6A,
        0x39,
        0x76,
        0x72,
        0x12,
        0x47,
        0x54,
        0x09,
        0x74,
        0x30,
        0x61,
        0x13,
        0x6B
        ]
    
    magi = [
        # 76 total. TrueEye (OA) is not a real Magi but instead a plot event that flips a script variable to make the Light Cave visible.
        # It is not included in this list and not shuffled.
        0x00, # Power, 9
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x01, # Speed, 9
        0x01,
        0x01,
        0x01,
        0x01,
        0x01,
        0x01,
        0x01,
        0x01,
        0x02, # Mana, 9
        0x02,
        0x02,
        0x02,
        0x02,
        0x02,
        0x02,
        0x02,
        0x02,
        0x03, # Defense, 8
        0x03,
        0x03,
        0x03,
        0x03,
        0x03,
        0x03,
        0x03,
        0x04, # Fire, 9
        0x04,
        0x04,
        0x04,
        0x04,
        0x04,
        0x04,
        0x04,
        0x04,
        0x05, # Ice, 9
        0x05,
        0x05,
        0x05,
        0x05,
        0x05,
        0x05,
        0x05,
        0x05,
        0x06, # Thunder, 9 
        0x06,
        0x06,
        0x06,
        0x06,
        0x06,
        0x06,
        0x06,
        0x06,
        0x07, # Poison, 9
        0x07,
        0x07,
        0x07,
        0x07,
        0x07,
        0x07,
        0x07,
        0x07,
        0x08, # Masmune, 1
        0x09, # Aegis, 1
        0x0B, # Heart, 1
        0x0C, # Pegasus, 1
        0x0D # Prism, 1 
        ]

    newItemPrices = {
        #prices are stored in three hex, addresses read right to left.
        0x3f929 : 0xC4,  #stat boosting potions, changed to 2.5k each up from 1k
        0x3f92a : 0x09,
        0x3f92b : 0x00,
        0x3f92c : 0xC4,
        0x3f92d : 0x09,
        0x3f92e : 0x00,
        0x3f92f : 0xC4,
        0x3f930 : 0x09,
        0x3f931 : 0x00,
        0x3f932 : 0xC4,
        0x3f933 : 0x09,
        0x3f934 : 0x00,
        0x3f896 : 0x50, #vampic, changed to 50,000
        0x3f897 : 0xC3,
        0x3f898 : 0x00,
        0x3f9da : 0x50, #selfix, changed to 50,000
        0x3f9db : 0xC3,
        0x3f9dc : 0x00,
        0x3f9dd : 0xD1, #seven sword, changed to 77,777
        0x3f9de : 0x2F,
        0x3f9df : 0x01
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
        [0x18, 0x32, 0x36, 0x3B, 0x68, 0x02, 0x03, 0x21, 0x0F, 0x50, 0x26, 0x27, 0x28, 0x29, 0x4D, 0x71], #silver, kimono, axe, battles, abacus, rapier, kick, fireb, iceb, thunderb, fogb, musket, rocket]
        [0x19, 0x37, 0x3C, 0x64, 0x33, 0x04, 0x05, 0x55, 0x49, 0x16, 0x51, 0x25, 0x2B, 0x5A, 0x5F, 0x60], #gold, armybody, katana, golds, temptat, blitzw, goldbow, headbutt, prayerb, stoneb, smg, fireg, missle]
        [0x62, 0x3D, 0x63, 0x65, 0x0C, 0x0A, 0x0B, 0x07, 0x06, 0x10, 0x4B, 0x6E, 0x5B, 0x5C, 0x4A], #giant, armyhelm, geta, thunderaxe, flames, ices, ogreaxe, corals, sabre, counter, psis, grenade, bazooka, chainsaw
        [0x38, 0x3F, 0x73, 0x1A, 0x1B, 0x0E, 0x66, 0x08, 0x14, 0x6C, 0x52, 0x2C, 0x2D, 0x4E, 0x5D], #dragonbody, hermes, gianthelm, flameshield, iceshield, runeaxe, sypha, dragons, revenge, lasers, x-kick, deathb, magestaff, magnum, vulcan
        [0x75, 0x40, 0x3E, 0x34, 0x1C, 0x69, 0x0D, 0x6A, 0x09, 0x11, 0x53, 0x2E, 0x30, 0x6F, 0x5E], #battlebody, hecate, ninjahand, dragonshield, samuraishield, defends, muramas, suns, catclaw, jyudo, wizardstaff, flareb, laserg, tankc
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

    itemList = (
        0x00, #Hammer
        0x01, #Long Sword
        0x02, #Axe
        0x03, #Battle Sword
        0x04, #Katana
        0x05, #Gold Sword
        0x06, #Coral Sword
        0x07, #Ogre Axe
        0x08, #Dragon Sword
        0x09, #Sun Sword
        0x0A, #Flame Sword
        0x0B, #Ice Sword
        0x0C, #Thunder Axe
        0x0D, #Defend Sword
        0x0E, #Rune Axe
        0x0F, #Rapier
        0x10, #Sabre
        0x11, #Cat Claw
        0x12, #Vampric Sword
        0x13, #Glass Sword
        0x14, #Revenge Sword
        0x15, #Bow
        0x16, #Gold Bow
        0x17, #Bronze Shield
        0x18, #Silver Shield
        0x19, #Gold Shield
        0x1A, #Flame Shield
        0x1B, #Ice Shield
        0x1C, #Dragon Shield
        0x1D, #Cure Potion
        0x1E, #X-Cure Potion
        0x1F, #Curse Potion
        0x20, #Eye Drop
        0x21, #Abacus
        0x22, #Excalibur
        0x23, #Samurai Bow
        0x24, #Cure Book
        0x25, #Prayer Book
        0x26, #Fire Book
        0x27, #Ice Book
        0x28, #Thunder Book
        0x29, #Fog Book
        0x2A, #Sleep Book
        0x2B, #Stone Book
        0x2C, #Death Book
        0x2D, #Mage Staff
        0x2E, #Wizard Staff
        0x2F, #Heal Staff
        0x30, #Flare Book
        0x31, #Bronze Helm
        0x32, #Silver Helm
        0x33, #Gold Helm
        0x34, #Dragon Helm
        0x35, #Bronze Armor
        0x36, #Silver Armor
        0x37, #Gold Armor
        0x38, #Dragon Armor
        0x39, #Arthur Armor
        0x3A, #Bronze Gauntlets
        0x3B, #Silver Gauntlets
        0x3C, #Gold Gauntlets
        0x3D, #Giant Gauntlets
        0x3E, #Ninja Gauntlets
        0x3F, #Hermes Shoes
        0x40, #Hecate Shoes
        0x41, #Elixir
        0x42, #Soft Potion
        0x43, #Power Potion
        0x44, #Speed Potion
        0x45, #Magic Potion
        0x46, #Body Potion
        0x47, #Tent
        0x48, #Whip
        0x49, #Blitz Whip
        0x4A, #Chainsaw
        0x4B, #Counter
        0x4C, #Colt
        0x4D, #Musket
        0x4E, #Magnum
        0x4F, #Punch
        0x50, #Kick
        0x51, #Headbutt
        0x52, #X-Kick
        0x53, #Jyudo
        0x54, #Karate
        0x55, #Temptat
        0x56, #Stun Gun
        0x57, #Heat
        0x5A, #SMG
        0x5B, #Grenade
        0x5C, #Bazooka
        0x5D, #Vulcan Cannon
        0x5E, #Tank Cannon
        0x5F, #Fire Gun
        0x60, #Missile
        0x61, #NukeBomb
        0x62, #Giant Armor
        0x63, #Army Helm
        0x64, #Army Armor
        0x65, #Geta Shoes
        0x66, #Sypha
        0x67, #Coin
        0x68, #Kimono
        0x69, #Samurai Shield
        0x6A, #Muramasa
        0x6B, #Gungnir
        0x6C, #Laser Sword
        0x6D, #Psi Knife
        0x6E, #Psi Sword
        0x6F, #Laser Gun
        0x70, #Speed Up
        0x71, #Rocket
        0x72, #Psi Gun
        0x73, #Giant Helm
        0x74, #Hyper Cannon
        0x75, #Battle Armor
        0x76, #Parasuit
        0x77, #Door
        0x7E, #Selfix
        0x7F #Seven Sword
        )

    #exclude no-header entries
    noMemoCalls = (
        0,
        1,
        2,
        3,
        4,
        5,
        8,
        9,
        10,
        11,
        14,
        15,
        20,
        21,
        22,
        23,
        26,
        27,
        28,
        29,
        30,
        31,
        32,
        33,
        34,
        35,
        36,
        37,
        38,
        39,
        40,
        41,
        42,
        43,
        45,
        47,
        48,
        49,
        50,
        51,
        52,
        53,
        54,
        55,
        56,
        57,
        58,
        59,
        62,
        64,
        65,
        66,
        67,
        70,
        71,
        73,
        74,
        75,
        76,
        77,
        84,
        86,
        87,
        88,
        89,
        90,
        91,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99,
        100,
        102,
        103,
        104,
        107,
        108,
        110,
        111,
        112,
        113,
        114,
        115,
        116,
        117,
        119,
        120,
        122,
        124,
        125,
        126,
        128,
        131,
        134,
        135,
        137,
        138,
        140,
        141,
        142,
        143,
        144,
        145,
        146,
        147,
        148,
        149,
        150,
        151,
        153,
        154,
        155,
        156,
        157,
        158,
        159,
        160,
        161,
        162,
        163,
        164,
        165,
        166,
        168,
        169,
        170,
        171,
        173,
        174,
        176,
        177,
        180,
        183,
        184,
        185,
        186,
        187,
        191,
        192,
        193,
        194,
        195,
        196,
        198,
        199,
        200,
        201,
        202,
        203,
        204,
        205,
        206,
        207,
        208,
        209,
        210,
        211,
        212,
        213,
        214,
        215,
        216,
        217,
        218,
        219,
        224,
        225,
        227,
        228,
        229,
        230,
        231,
        232,
        233,
        234,
        235,
        236,
        237
        )

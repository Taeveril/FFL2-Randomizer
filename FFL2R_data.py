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

    treasureAddresses = [
        0x1c8f3,
        0x1c8f9,
        0x1c8ff,
        0x1c905,
        0x1cab2,
        0x1cac5,
        0x1cacb,
        0x1cad1,
        0x1cad7,
        0x1cb0d,
        0x1cb13,
        0x1cb19,
        0x1cb31,
        0x1cba5,
        0x1cbd1,
        0x1cbea,
        0x1cd8f,
        0x1cdca,
        0x1cde8,
        0x1ce12,
        0x1ce18,
        0x1ce1e,
        0x1ce24,
        0x1cf2c,
        0x1cf32,
        0x1d10e,
        0x1d114,
        0x1d12e,
        0x1d21e,
        0x1d23c,
        0x1d268,
        0x1d29a,
        0x1d2ad,
        0x1d2b3,
        0x1d2c6,
        0x1d2d9,
        0x1d4dc,
        0x1d4e2,
        0x1d4e8,
        0x1d4ee,
        0x1d4f4,
        0x1d7c1,
        0x1d7d8,
        0x1d819,
        0x1d81f,
        0x1d8e5,
        0x1d8eb,
        0x1d907,
        0x1d90d,
        0x1d93a,
        0x1dbdb,
        0x1dbe1,
        0x1dbe7,
        0x1dbfa,
        0x1dc0f,
        0x1dc42,
        0x1dd0a,
        0x1dd35,
        0x1dd3b,
        0x1df64,
        0x1df77,
        0x1df95,
        0x1dfa8,
        0x1dfbb,
        0x1e0bc,
        0x1e0cf,
        0x1e0ed,
        0x1e100,
        0x1e113,
        0x1d93a,
        0x1dbdb,
        0x1dbe1,
        0x1dbe7,
        0x1dbfa,
        0x1dc0f,
        0x1dc42,
        0x1dd0a,
        0x1dd35,
        0x1dd3b,
        0x1df64,
        0x1df77,
        0x1df95,
        0x1dfa8,
        0x1dfbb,
        0x1e0bc,
        0x1e0cf,
        0x1e0ed,
        0x1e100,
        0x1e113,
        0x1e126,
        0x1e144,
        0x1e157,
        0x1e3d6,
        0x1e3dc,
        0x1e3e2,
        0x1e3e8,
        0x1e3fb,
        0x1e401,
        0x1e407,
        0x1e40d,
        0x1e420,
        0x1e426,
        0x1e42c,
        0x1e432,
        0x1e445,
        0x1e44b,
        0x1e451,
        0x1e457,
        0x1e46a,
        0x1e470,
        0x1e476,
        0x1e47c,
        0x1e482,
        0x1e495,
        0x1e49b,
        0x1e4a1,
        0x1e4a7,
        0x1e4ba,
        0x1e4c0,
        0x1e4c6,
        0x1e4cc,
        0x1e4e6,
        0x1e4ec,
        0x1e4f2,
        0x1e4f8
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

    magiAddresses = [
        0x1cb1f, #chests
        0x1cb25,
        0x1cb2b,
        0x1cc08,
        0x1cc0e,
        0x1cc14,
        0x1cf14,
        0x1cf1a,
        0x1d141,
        0x1d147,
        0x1d2ec,
        0x1d2f2,
        0x1d2f8,
        0x1d840,
        0x1d846,
        0x1d84c,
        0x1d858,
        0x1d85e,
        0x1d864,
        0x1d928,
        0x1d92e,
        0x1e171,
        # Addresses from 20000-2EB7F could be affected with any scripting changes
        # as these addresses are MAGI rewarded via script.
        0x2892a, # Ki Assistant
        0x2913a, # Dad Giant World
        0x29454, # Apollo First
        0x29e7e, # Guardian World
        0x29ea4,	 
        0x29eaf,	 
        0x29f39,	 
        0x2993c, # Ninja Cut Scenes
        0x2a0a6,	 
        0x2a275,	 
        0x2a459, # Nils's Return
        0x2ab50, # Race  
        0x2ab55, # NOTE: There are alternate drop methods dependent on dragon choice.
        0x2ab5b, # These three must be matched to their counterpart.
        0x2ab61, #
        0x2ad20, # Magnate
        0x2ad23,
        0x2ad26,
        0x2ad29,
        0x2ba53, # Dunatis
        0x2ba56,	 
        0x2ba59,	 
        0x2c233, # Opening.      
        0x2caa6, # Ki's Body.    
        0x2caaf,
        0x2cab8,
        0x2cac1,
        0x2caca,
        0x2cad3,
        0x2cadc,
        0x2c874, # Odin
        0x2c877,
        0x2c87a,
        0x2c87d,
        0x2c880,
        0x2c883,
        0x2c886,
        0x2dc58,
        0x2d27b, #Nasty Dungeon
        0x2e9e7, #Ashura
        0x2e9ea,
        0x2e9ed,
        0x2e9f0,
        0x2e9f3,
        0x2e9f6,
        0x2e9f9,
        0x2cc74, #Venus
        0x2e9fd, 
        0x2ea00, 
        0x2ea03,
        0x2ea06,
        0x2ea09,
        0x2ea0c,
        0x2ea0f
        ]

    #magiAddressesAlternate = [
    #    0x2aae0, # 2ab55
    #    0x2ab07, # 2ab5b
    #    0x2ab2f  # 2ab61
    #    ]

    newItemPrices = {
        #prices are stored in three hex, addresses read right to left.
        0x3f929 : 0x88,  #stat boosting potions, changed to 5k each up from 1k
        0x3f92a : 0x13,
        0x3f92b : 0x00,
        0x3f92c : 0x88,
        0x3f92d : 0x13,
        0x3f92e : 0x00,
        0x3f92f : 0x88,
        0x3f930 : 0x13,
        0x3f931 : 0x00,
        0x3f932 : 0x88,
        0x3f933 : 0x13,
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

    shopAddresses = [
        (1, 0x3f9e0), # 3f9e0-3f9e7 - First Town, Weapon Shop (tier 1)
        (2, 0x3f9e8), # 3f9e8-3f9ef - Desert Town, Weapon Shop (tier 2)
        (2, 0x3f9f0), # 3f9f0-3f9f7 - Ashura Town, Weapon Shop (tier 2)
        (3, 0x3f9f8), # 3f9f8-3f9ff - Giant Town, Weapon Shop (tier 3)
        (1, 0x3fa00), # 3fa00-3fa07 - Second Town, Weapon Shop (tier 1)
        (3, 0x3fa08), # 3fa08-3fa0f - Apollo Town, Weapon Shop (tier 3)
        (4, 0x3fa10), # 3fa10-3fa17 - Lynn Town, Weapon Shop (tier 4)
        (4, 0x3fa18), # 3fa18-3fa1f - Guardian Town, Weapon Shop (tier 4)
        (5, 0x3fa20), # 3fa20-3fa27 - Venus Town, Weapon Shop (tier 5)
        (5, 0x3fa28), # 3fa28-3fa2f - Race Town, Weapon Shop (tier 5)
        (6, 0x3fa30), # 3fa30-3fa37 - Edo Town, Weapon Shop (tier 6)
        (6, 0x3fa38), # 3fa38-3fa3f - Final Town, Weapon Shop (tier 6)
        (1, 0x3fa40), # 3fa40-3fa47 - First Town, Item Shop (tier 1)
        (2, 0x3fa48), # 3fa48-3fa4f - Desert Town, Item Shop (tier 2)
        (3, 0x3fa50), # 3fa50-3fa57 - Giant Town, Item Shop (tier 3)
        (4, 0x3fa58), # 3fa58-3fa5f - Apollo Town, Item Shop (tier 4)
        (4, 0x3fa60), # 3fa60-3fa67 - Guardian Town, Item Shop (tier 4)
        (5, 0x3fa68), # 3fa68-3fa6f - Venus Town, Item Shop (tier 5)
        (6, 0x3fa70), # 3fa70-3fa77 - Race Town, Item Shop (tier 6)
        (6, 0x3fa78)  # 3fa78-3fa7f - Edo Town, Item Shop (tier 6)
                      # 3fa80-3fa87 - Final Town, Item Shop (tier 7)
                      # 3fa88-3fa8f - Recurring Item Shop (Second Town, Ashura Town, etc.) (tier 0)
                      # 3fa90-3fa97 - Echigoya
                      # 3fa98-3fa9f - Giant Town Giant Gear Seller
        ]

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
        [0x39, 0x76, 0x7E, 0x7F, 0x6B, 0x22, 0x13, 0x23, 0x54, 0x72, 0x12, 0x61, 0x74], #arthur, parasuit, selffix, sevens, gungnir, xcalibr, glasss, samuraibow, karate, psig, vampic, nukebomb, hyper
        [0x1D, 0x1E, 0x1F, 0x20, 0x41, 0x42, 0x70, 0x77] #cure, xcure, curse, eyedrop, elixier, soft, speedup, door
        ]
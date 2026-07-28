import random
import argparse
import mmap

import FFL2R_asm
import FFL2R_manager_base
from FFL2R_utils import Utility
from FFL2R_io import File
from FFL2R_data import GameData
from FFL2R_manager_scripts import ScriptManager
from FFL2R_manager_maps import MapManager
from FFL2R_manager_monsters import MonsterManager
from FFL2R_manager_economy import ShopManager
from FFL2R_manager_economy import GoldManager
from FFL2R_manager_economy import ItemManager
from FFL2R_manager_world import WorldManager

VERSION = 3.22
DEBUG = False

def main(fromWeb:bool, romData:mmap.mmap|None, rom_path:str|None, seed:int|None, encounterRate:int|None, goldDrops:int|None, 
         worldType:int|None, shuffleType:int|None, dadMagiType:int|None)->tuple:
    if not fromWeb:
        if not rom_path:
            gameFile = str(input("First, please path to the FFL2 rom. \n>>"))
        else:
            gameFile = rom_path
        romData = File.readInRom(gameFile, DEBUG)

    #  seeding
    if not seed:
        if not fromWeb:
            gameSeed_str = str(input("Seed please. Blank will generate a random number. \n>>"))
        try:
            gameSeed = int(gameSeed_str)
            gameSeed = abs(gameSeed)
        except:
            gameSeed = random.randint(0, 4294967296)
    else:
        gameSeed = seed
    random.seed(gameSeed)    

    if not encounterRate:
        encounterRate = int(input("Encounter rate please, 20-200. >>"))          

    if not goldDrops:
        goldDrops = int(input("Gold adjustment please, 50-500. (Gold dropped is currently capped at 65535.)\n>>"))

    if not worldType:
        worldType = int(input("Choose a world order type: 1 = Vanilla, 2 = Shuffle, 3 = Open\n>>"))
        
    if worldType < 1 or worldType > 3:
        raise Exception("Invalid World Order Selection.")

    if not shuffleType:
        shuffleType = int(input("""Choose a treasure shuffle type:
        1 = Shuffle Treasures, Shuffle Magi, Don't Mix
        2 = Shuffle Treasures, Shuffle Magi, Mix
        3 = Random Treasures, Shuffle Magi, Don't Mix
        4 = Random Treasures, Shuffle Magi, Mix
        5 = Shuffle Treasures, Random Magi, Don't Mix
        6 = Shuffle Treasures, Random Magi, Mix
        7 = Random Treasures, Random Magi, Don't Mix
        8 = Random Treasures, Random Magi, Mix
        >>"""))
        
    if shuffleType < 1 or worldType > 8:
        raise Exception("Invalid Shuffle Selection.")

    # List is in game data order
    if not (dadMagiType):
        dadMagiType = int(input("""Please choose what Magi Dad gives you at the beginning:
        1 = Masmune
        2 = Aegis
        3 = Heart
        4 = Pegasus
        5 = Prism
        6 = Random                                 
        >>>"""))
        
    if dadMagiType not in range(1,7):
        raise Exception("Invalid Dad Magi Selection.")

    dadMagi:int
    match dadMagiType:
        case 1: dadMagi = 0x08
        case 2: dadMagi = 0x09
        case 3: dadMagi = 0x0b
        case 4: dadMagi = 0x0c
        case 5: dadMagi = 0x0d
        case 6: dadMagi = 0x00

    FFL2R_asm.Fixes.fixPoison(romData)
    FFL2R_asm.Fixes.missingTrigger(romData)
    FFL2R_asm.Fixes.magiFix(romData)
    FFL2R_asm.Fixes.mutantStr(romData)
    FFL2R_asm.Fixes.forceRaceDismount(romData)
    FFL2R_asm.Fixes.goldDropFix(romData)

    FFL2R_asm.QOL.moveHax(romData)
    FFL2R_asm.QOL.textHax(romData)
    FFL2R_asm.QOL.betterGrowth(romData)

    scripts = ScriptManager(romData)
    maps = MapManager(romData)
    monsters = MonsterManager(romData)
    shops = ShopManager(romData)
    gold = GoldManager(romData)
    items = ItemManager(romData)
    worlds = WorldManager()

    FFL2R_manager_base.ScriptedFixes.moveMrS(scripts, maps)
    FFL2R_manager_base.ScriptedFixes.fixTheRace(scripts, maps)

    FFL2R_manager_base.GamePrep.newTitleScreen(scripts, gameSeed, VERSION)
    FFL2R_manager_base.GamePrep.newDropScripts(scripts)
    FFL2R_manager_base.GamePrep.kiShrineCleanup(scripts, maps)
    FFL2R_manager_base.GamePrep.memoRemove(scripts, romData)
    FFL2R_manager_base.GamePrep.venusWorldCleanup(scripts, maps)
    FFL2R_manager_base.GamePrep.dadDeathCutscenes(scripts)
    FFL2R_manager_base.GamePrep.warMachAdjust(scripts, maps)
    FFL2R_manager_base.GamePrep.nastyChest(scripts, maps)
    FFL2R_manager_base.GamePrep.guardianBaseLogic(maps)
    FFL2R_manager_base.GamePrep.betterPrism(scripts, romData)
    FFL2R_manager_base.GamePrep.newCredits(scripts)
    FFL2R_manager_base.GamePrep.convertTrueEyeChest(scripts, maps)

    FFL2R_manager_base.ScriptedQOL.newNPCHelpers(scripts, maps)

    randomization(worlds, shuffleType, scripts, maps, romData, dadMagi)
    shopRando(shops, GameData.shopTiers)
    worldShuffle(romData, maps, scripts, worlds, worldType)

    newStarters(monsters, scripts)

    if encounterRate != 100:
        encounterRate = Utility.setBoundaries(encounterRate, 20, 200)
        encounterRateAdjustment(maps, encounterRate)

    if goldDrops != 100:
        goldDrops = Utility.setBoundaries(goldDrops, 50, 500)
        goldAdjustment(gold, goldDrops)
    
    for k,v in GameData.newItemPrices.items():
         items.item[k].setPrice(v)

    # if DEBUG == True:
    #     prismCounts = [0 for _ in range(16)]
    #     for k,v in worlds.locations.items():
    #         treasuretype = ""
    #         treasurevalue = ""
    #         if v.lType.value > 4:
    #             if v.data[0] == 0:
    #                 if scripts.main[v.data[1]][v.data[2]+1] == 0xa:
    #                     treasuretype = "MAGI"
    #                     treasurevalue = GameData.MAGIVALUES[scripts.main[v.data[1]][v.data[2]+2]]
    #                     prismCounts[v.pType.value]+=1
    #                 else:
    #                     treasuretype = "Item"
    #                     treasurevalue = GameData.ITEMS[scripts.main[v.data[1]][v.data[2]+2]]
    #             else:
    #                 treasuretype = ""
    #                 treasurevalue = ""
    #                 if scripts.memo[v.data[1]][v.data[2]+1] == 0xa:
    #                     treasuretype = "MAGI"
    #                     treasurevalue = GameData.MAGIVALUES[scripts.memo[v.data[1]][v.data[2]+2]]
    #                     prismCounts[v.pType.value]+=1
    #                 else:
    #                     treasuretype = "Item"
    #                     treasurevalue = GameData.ITEMS[scripts.memo[v.data[1]][v.data[2]+2]]
    #         else:
    #             if maps.map[v.data[0]].npcs[v.data[1]][5] == 0xfa:
    #                 treasuretype = "MAGI"
    #                 treasurevalue = GameData.MAGIVALUES[maps.map[v.data[0]].npcs[v.data[1]][4]]
    #                 prismCounts[v.pType.value]+=1
    #             else:
    #                 treasuretype = "Item"
    #                 treasurevalue = GameData.ITEMS[maps.map[v.data[0]].npcs[v.data[1]][4]]
    #         if treasuretype == "MAGI":
    #             print(f"{k} - {treasuretype}: {treasurevalue}")
    #     print(f"{prismCounts} = Total: {sum(prismCounts) - 3}")

    romData = File.editRom(romData, scripts, maps, shops, monsters, gold, items)

    worldMode = ""
    match worldType:
        case 1: worldMode = "Vanilla"
        case 2: worldMode = "Shuffled"
        case 3: worldMode = "Open"
    shuffleMode = ""
    match shuffleType:
        case 1: shuffleMode = "Shuffle Treasures, Shuffle Magi, Don't Mix"
        case 2: shuffleMode = "Shuffle Treasures, Shuffle Magi, Mix"
        case 3: shuffleMode = "Random Treasures, Shuffle Magi, Don't Mix"
        case 4: shuffleMode = "Random Treasures, Shuffle Magi, Mix"
        case 5: shuffleMode = "Shuffle Treasures, Random Magi, Don't Mix"
        case 6: shuffleMode = "Shuffle Treasures, Random Magi, Mix"
        case 7: shuffleMode = "Random Treasures, Random Magi, Don't Mix"
        case 8: shuffleMode = "Random Treasures, Random Magi, Mix"
    dadMode = ""
    if dadMagi != 0x00:
        dadMode = GameData.MAGIVALUES.get(dadMagi)
    else:
        dadMode = "Random"
    print(f"""        Final Fantasy Legend 2 Randomizer Settings:
        Seed is: {str(gameSeed)}
        Encounter rate adjustment is: {str(encounterRate)}%
        Gold adjustment is: {str(goldDrops)}%
        World type is: {worldMode}
        Treasure Distribution is: {shuffleMode}
        Magi that Dad gives you is: {dadMode}""")
    if fromWeb == True:
        return romData, gameSeed
    else:
        File.writeOutRom(romData, gameSeed)
        print("            Randomizer finished successfully. Right on!")
        return 0


def goldAdjustment(gold:GoldManager, rate:int):
    percent = rate / 100

    for v in gold.dropValue.values():
        g = int(v.actualValue * percent)
        #10% stack bonus causes overflow issues, so capped at 59578
        if g > 59578:
            g = 59578
        v.actualValue = g
        v.updateGold(g)

def encounterRateAdjustment(maps:MapManager, rate:int):
    percent = rate / 100

    #if a map's encounter rate is 0, it winds up for a default encounter rate somehow. So it floors at 1.
    for v in maps.map.values():
        if v.isDangerous == True:
            v.encounterRate = int(v.encounterRate * percent)
            if v.encounterRate == 0:
                v.encounterRate = 1

def randomization(worlds:WorldManager, shuffleType:int, scripts:ScriptManager, maps:MapManager, romData:mmap, dadMagi:int):
    def _char2Parent(scripts:ScriptManager):
        startGift = random.choice(list(GameData.ITEMS.keys()))
        scripts.main[275][26] = startGift
        scripts.main[275][41] = startGift
    def _placeInChest(mapID:int, npcIndex:int, value:int, tType:int, maps:MapManager):
        if tType == 1: #magi
            maps.map[mapID].npcs[npcIndex][4] = value
            maps.map[mapID].npcs[npcIndex][5] = 0xfa
        else: #item
            maps.map[mapID].npcs[npcIndex][4] = value
            maps.map[mapID].npcs[npcIndex][5] = 0xf9
            if value == 0xff:
                maps.map[mapID].npcs[npcIndex][2]+=0x40
    def _placeInScript(bankID:int, scriptID:int, byteIndex: int, value:int, tType:int, scripts:ScriptManager):
        if bankID == 3:
            scripts.memo[scriptID][byteIndex] = 0x19
            if tType == 1:
                scripts.memo[scriptID][byteIndex+1] = 0x0a
            else: 
                scripts.memo[scriptID][byteIndex+1] = 0x0b
            scripts.memo[scriptID][byteIndex+2] = value
        else:
            scripts.main[scriptID][byteIndex] = 0x19
            if tType == 1:
                scripts.main[scriptID][byteIndex+1] = 0x0a
            else: 
                scripts.main[scriptID][byteIndex+1] = 0x0b
            scripts.main[scriptID][byteIndex+2] = value

    #determine items
    items = []
    magi = []
    prismCounts = [0 for _ in range(16)]
    if shuffleType in (1, 2, 5, 6):
        items = GameData.TREASURES
        random.shuffle(items)
    else:
        allItems = list(GameData.ITEMS.keys())
        for _ in range(106):
            items.append(random.choice(allItems))
    if shuffleType < 5:
        for m, c in GameData.MAGI.items():
            for _ in range(c):
                magi.append(m)
        random.shuffle(magi)
    else:
        magiTypes = list(GameData.MAGI.keys())
        for _ in range(76):
            magi.append(random.choice(magiTypes))
    if dadMagi != 0x00: # If the selected magi for Dad is Random, skip.
        magi.remove(dadMagi) # Remove Dad's magi from the list.
        magi.append(dadMagi) # Move Dad's new magi to last to avoid having it allocated early.
    keyListShuffled = []
    keyListPrioritized = []
    for k, v in worlds.locations.items():
        if v.lType.value in (2,4,6,8) or k == "Final Dungeon, WarMach Chest":
            match k:
                case "Opening Cutscene":
                    if dadMagi != 0x00: # Skip magi swap if random.
                        magi[magi.index(dadMagi)] = magi[0] # Swap the magi he was originally going to give us with the new magi.
                        magi[0] = dadMagi
                    
                    #Put the magi in the script for the opening cutscene.
                    _placeInScript(v.data[0], v.data[1], v.data[2], magi[0], 1, scripts)
                    magi.pop(0)
                    prismCounts[v.pType.value]+=1
                case "Char 2's Parent":
                    _char2Parent(scripts)
                case "Undersea Volcano, Exit TrueEye":
                     #TrueEye stays put, currently not in dict
                    _placeInChest(v.data[0], v.data[1], 0x0a, 1, maps)
                    prismCounts[v.pType.value]+=1
                case "Leon's Theft":
                    scripts.replaceScript(0, 54, FFL2R_manager_base.GamePrep.leonsText(magi[0]))
                    _placeInScript(v.data[0], v.data[1], v.data[2], magi[0], 1, scripts)
                    magi.pop(0)
                    prismCounts[v.pType.value]+=1
                case "Hermit Crab Drop" | "Giant Town, Micron Potion Location" | "Race - Watcher (Adamant)" | "Race - Watcher (Tortoise)" | "Race - Watcher (Lamia)":
                    pass
                case "Final Dungeon, WarMach Chest":
                     _placeInScript(v.data[0], v.data[1], v.data[2], magi[0], 1, scripts)
                     magi.pop(0)
                     prismCounts[v.pType.value]+=1
                case _:
                    keyListPrioritized.append(k)
        else:
            match k:
               case k if 'Final Dungeon' in k:
                     _placeInChest(v.data[0], v.data[1], items[0], 0, maps)
                     items.pop(0)
               case _:
                    keyListShuffled.append(k)
    random.shuffle(keyListShuffled)
    keyList = keyListPrioritized + keyListShuffled
    if shuffleType % 2 == 0:
        activeList = magi
        listBool = 1
        for k in keyList:
            if not activeList:
                activeList = items
                listBool = 0
            locData = worlds.locations[k]
            if locData.lType.value <= 4:
                _placeInChest(locData.data[0], locData.data[1], activeList[0], listBool, maps)
            else:
                _placeInScript(locData.data[0], locData.data[1], locData.data[2], activeList[0], listBool, scripts)
                s=""
                match k:
                    case "Race - Adamant":
                        s = "Race - Watcher (Adamant)"
                    case "Race - Tortoise":
                        s = "Race - Watcher (Tortoise)"
                    case "Race - Lamia":
                        s = "Race - Watcher (Lamia)"
                if s:
                    _placeInScript(worlds.locations[s].data[0], worlds.locations[s].data[1], worlds.locations[s].data[2], activeList[0], listBool, scripts)                        
            if listBool == 1:
                prismCounts[locData.pType.value]+=1
            activeList.pop(0)
    else:
        for k in keyList:
            locData = worlds.locations[k]
            match locData.lType.value:
                case 0 | 1:
                    _placeInChest(locData.data[0], locData.data[1], items[0], 0, maps)
                    items.pop(0)
                case 5:
                    _placeInScript(locData.data[0], locData.data[1], locData.data[2], items[0], 0, scripts)
                    items.pop(0)
                case 3:
                    _placeInChest(locData.data[0], locData.data[1], magi[0], 1, maps)
                    prismCounts[locData.pType.value]+=1
                    magi.pop(0)
                case 7 | 8:
                    _placeInScript(locData.data[0], locData.data[1], locData.data[2], magi[0], 1, scripts)
                    prismCounts[locData.pType.value]+=1
                    s=""
                    match k:
                        case "Race - Adamant":
                            s = "Race - Watcher (Adamant)"
                        case "Race - Tortoise":
                            s = "Race - Watcher (Tortoise)"
                        case "Race - Lamia":
                            s = "Race - Watcher (Lamia)"
                    if s:
                        _placeInScript(worlds.locations[s].data[0], worlds.locations[s].data[1], worlds.locations[s].data[2], magi[0], 1, scripts)                        
                    magi.pop(0)
                case _:
                    print(f"{k} - err")
    for x in range (0, len(prismCounts)):
        romData[worlds.PRISMADDR+x] = prismCounts[x]
    #account for the NPC removal
    if DEBUG == True:
        for k, v in worlds.locations.items():
            if "Ruins of the Ancient Gods, Floor 4" in k:
                v.data[1]-=1


def shopRando(shops:ShopManager, tiers:list):
    def _mixTier(tierData:list)->list:
        random.shuffle(tierData)
        return tierData
    def _populateShop(currentShop:list, count:int, availableItems:list, *bonusItems:list):
        for i in range(0, count):
            if random.randint(0,3) == 3 and bonusItems:
                currentShop[i] = bonusItems[0][i]
            else:
                currentShop[i] = availableItems[i]
        return currentShop

    for v in shops.shop.values():
        currentShop = bytearray.fromhex('FF FF FF FF FF FF FF FF')
        length = random.randint(6,8)
        match v.tier:
            case 0: #recurring
                currentShop = tiers[8]
            case 7: #final shop
                currentShop = tiers[0]
                items = _mixTier(tiers[7])
                currentShop.append(items[0])
            case 8: #Echigoya will always have a full stock of eight items
                items = _mixTier(tiers[7])
                currentShop = _populateShop(currentShop, 8, items)             
            case 9: #giant town special, grab from 0 first then 6/7
                items = _mixTier(tiers[6]+tiers[7])
                currentShop = _populateShop(currentShop, length, items)
            case _: #most other shops
                items = _mixTier(tiers[v.tier])
                bonusItems = _mixTier(tiers[v.tier+1])
                currentShop = _populateShop(currentShop, length, items, bonusItems)
        v.wares = currentShop

def newStarters(monsters:MonsterManager, scripts:ScriptManager):
    randoMonsters = random.sample(range(180),3)
    for starter in randoMonsters:
        starterIndex = randoMonsters.index(starter)
        monsters.monster[245+starterIndex].family = monsters.monster[starter].family
        monsters.monster[245+starterIndex].ai = monsters.monster[starter].ai
        monsters.monster[245+starterIndex].gfx= monsters.monster[starter].gfx
        monsters.monster[245+starterIndex].npc = monsters.monster[starter].npc
        monsters.monster[245+starterIndex].stats = monsters.monster[starter].stats
        monsters.monster[245+starterIndex].skillsLength = monsters.monster[starter].skillsLength
        monsters.monster[245+starterIndex].skills = monsters.monster[starter].skills
        monsters.monster[245+starterIndex].name = monsters.monster[starter].name
        monsters.monster[245+starterIndex].goldIndex = monsters.monster[starter].goldIndex

        if monsters.monster[starter].dslevel < 10:
            hexLevel = 'FF FF' + f"{0xB0 + monsters.monster[starter].dslevel:02x}"
        else:
            hexLevel = 'FF B1' + f"{(0xB0 + (monsters.monster[starter].dslevel - 10)):02x}"
        match starterIndex:
            case 0:
                pos = 69
            case 1:
                pos = 83
            case 2:
                pos = 97
        scripts.insertIntoScript(2, 21, pos, hexLevel)

def worldShuffle(romData:mmap, maps:MapManager, scripts:ScriptManager, worlds:WorldManager, worldType:int):
    warpScripts = {}
    startaddr = worlds.WORLD_NAME_STARTADDR
    warpNames = {}
    scriptIndex = 0
    teleCounter = 2
    finalStore = list(worlds.finalStore.values())
    worlds.magiCheckRedo(scripts, maps, worldType)
    if worldType != 1:
        maps.map[finalStore[0][1]].npcs[finalStore[0][2]][0] = 0x10
        maps.map[finalStore[0][1]].npcs[finalStore[0][2]][1] = 0x1f
        maps.map[finalStore[1][1]].npcs[finalStore[1][2]][0] = 0x10
        maps.map[finalStore[1][1]].npcs[finalStore[1][2]][1] = 0x1f
        if worldType == 3:
            for k, v in worlds.world.items():
                for x in finalStore:
                    if x[0] == v.index:
                        maps.map[x[1]].npcs[x[2]][0] = 0x00
                        maps.map[x[1]].npcs[x[2]][1] = 0x0F
                if v.scriptTeleportUnlockByte:
                    scripts.main[v.scriptTeleportUnlockByte[0]][v.scriptTeleportUnlockByte[1]+2] = 0x0D
    newWorldOrder = list(worlds.world.values())
    if worldType == 2:
        for world in newWorldOrder:
            if world.teleportScripts:
                for s in world.teleportScripts:
                    warpScripts[s] = scripts.main[s]
            if world.nameAddr:
                for loc in world.nameAddr:
                    name = []
                    for x in range(0, 16):
                       name.append(romData[loc+x])
                    warpNames[loc] = name
        random.shuffle(newWorldOrder)
        for v in worlds.pillar.values():
            gWorld = False
            if newWorldOrder[0].isScript:
                gWorld = True
                trigger = [87,0]
            elif newWorldOrder[0].doorIn > 255:
                trigger = [newWorldOrder[0].doorIn-256, 6]
            else:
                trigger = [newWorldOrder[0].doorIn, 5]
            maps.map[v.mapPillarID].triggers[v.doorInMapIndex] = trigger
            maps.map[v.mapPillarID].triggers[v.mapPillarTriggerIndexPrism] = [newWorldOrder[0].prismScript ,0]
            if v.doorOut > 255:
                trigger = [v.doorOut - 256, 6]
            else:
                trigger = [v.doorOut, 5]
            maps.map[newWorldOrder[0].mapID].triggers[newWorldOrder[0].doorOutMapIndex] = trigger
            if gWorld == True:
                maps.map[90].triggers[0] = trigger
            if newWorldOrder[0].teleportScripts:
                for s in newWorldOrder[0].teleportScripts:
                    scripts.replaceScript(0, 99+scriptIndex, warpScripts[s].hex(" "))
                    scriptIndex+=1
            if newWorldOrder[0].nameAddr:
                for loc in newWorldOrder[0].nameAddr:
                    for x in range(0,16):
                        romData[startaddr] = warpNames[loc][x]
                        startaddr+=1
            if newWorldOrder[0].scriptTeleportUnlockByte:
                teleCounter+=newWorldOrder[0].scriptTeleportUnlockByte[2]
                scripts.main[newWorldOrder[0].scriptTeleportUnlockByte[0]][newWorldOrder[0].scriptTeleportUnlockByte[1]+2] = teleCounter
            for x in finalStore:
                if x[0] == newWorldOrder[0].index:
                    maps.map[x[1]].npcs[x[2]][0] = 0x10
                    maps.map[x[1]].npcs[x[2]][1] = (v.order*16)+15
            newWorldOrder.pop(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int) # todo - pathlib
    parser.add_argument('-r', '--rom_path', type=str, dest="rom_path")
    parser.add_argument('-e', '--encounter_rate', type=int)
    parser.add_argument('-g', '--gold', type=int)
    parser.add_argument('-w', '--world', type=int)
    parser.add_argument('-sh', '--shuffle', type=int)
    parser.add_argument('-d', '--dad_magi', type=int)
    args = parser.parse_args()
    main(False, None, rom_path = args.rom_path, seed=args.seed, encounterRate=args.encounter_rate, goldDrops=args.gold, worldType=args.world, shuffleType=args.shuffle, dadMagiType=args.dad_magi)

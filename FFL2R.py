import random
import FFL2R_data
import FFL2R_utils
import FFL2R_io
import FFL2R_bugfixes
import FFL2R_qol
import argparse
import mmap
from tkinter import Menu, Tk
from tkinter.filedialog import askopenfilename

VERSION = 1.0

def main(rom_path:str|None, seed:int|None, encounterRate:int|None, goldDrops:int|None):
    Tk().withdraw()
    if not rom_path:
        gameFile = askopenfilename(title="First, please point to the FFL2 rom.")
    else:
        gameFile = rom_path

    #  seeding
    if not seed:
        gameSeed_str = str(input("Seed please. Blank will generate a random number."))
        try:
            gameSeed = int(gameSeed_str)
            gameSeed = abs(gameSeed)
        except:
            gameSeed = random.randint(0, 4294967296)
    else:
        gameSeed = seed
    random.seed(gameSeed)    

    if not encounterRate:
        encounterRate = int(input("Encounter rate please, 20-200. "))          

    if not goldDrops:
        goldDrops = int(input("Gold adjustment please, 50-500. (Gold dropped is currently capped at 65535.) "))

    treasureFlagReclaim = []
    
    romData = FFL2R_io.File.readInRom(gameFile)

    FFL2R_bugfixes.AssemblyFixes.missingTrigger(romData)
    FFL2R_bugfixes.AssemblyFixes.magiFix(romData)
    FFL2R_bugfixes.AssemblyFixes.mutantStr(romData)
    FFL2R_bugfixes.AssemblyFixes.forceRaceDismount(romData)
    FFL2R_bugfixes.AssemblyFixes.goldDropFix(romData)

    FFL2R_qol.AssemblyQOL.moveHax(romData)
    FFL2R_qol.AssemblyQOL.textHax(romData)
    FFL2R_qol.AssemblyQOL.betterGrowth(romData)

    maps = FFL2R_io.MapData(romData, 0x1c800, 0x1e5f8,0x1e6ff, 0x1c000, 0x1ef80, 0x1efff)
    scriptingBlock1 = FFL2R_io.ScriptBlock(romData, 0x2c000, 0x2eb7f, 0x28000)
    scriptingBlock2 = FFL2R_io.ScriptBlock(romData, 0x28000, 0x2be3e, 0x24000)
    battleBlock = FFL2R_io.ScriptBlock(romData, 0x2eb80, 0x2f3ff, 0x28000)
    menuBlock = FFL2R_io.ScriptBlock(romData, 0x2f400, 0x2ffcf, 0x28000)
    shops = FFL2R_io.ShopData(romData, 0x3f9e0, 0x3fa9f)
    goldTable = FFL2R_io.GoldData(romData, 0x33e50, 0x33e7f)
    monsterTable = FFL2R_io.MonsterData(romData, 0x33800, 0x33d50, 0x36400, 0x36b70, 0x36f80, 0x3eec0, 0x33c50)
    memoBlock = FFL2R_io.ScriptBlock(romData, 0x3c250, 0x3e07f, 0x38000)
    memoBlock.headerData.blockStart = 0x3c270
    memoBlock.headerData.blockEnd = 0x3c46f
    memoBlock.headerData.addr = memoBlock.headerData.getAddr(romData)
    memoBlock.script = memoBlock.getData(romData)

    FFL2R_bugfixes.ScriptedFixes.moveMrS(scriptingBlock1, maps)
    FFL2R_bugfixes.ScriptedFixes.fixTheRace(scriptingBlock1, scriptingBlock2, maps)

    FFL2R_utils.GamePrep.newTitleScreen(menuBlock, VERSION, gameSeed)
    FFL2R_utils.GamePrep.magiCheckRedo(scriptingBlock1, scriptingBlock2, maps, treasureFlagReclaim)
    FFL2R_utils.GamePrep.newDropScripts(scriptingBlock1, scriptingBlock2)
    FFL2R_utils.GamePrep.kiShrineCleanup(scriptingBlock1, scriptingBlock2, maps)
    FFL2R_utils.GamePrep.memoRemove(scriptingBlock1, scriptingBlock2, menuBlock, memoBlock, romData)
    FFL2R_utils.GamePrep.venusWorldCleanup(scriptingBlock1, scriptingBlock2, memoBlock, maps)
    FFL2R_utils.GamePrep.dadDeathCutscenes(scriptingBlock1, scriptingBlock2, memoBlock)
    FFL2R_utils.GamePrep.nastyChest(scriptingBlock1, maps) 
    FFL2R_utils.GamePrep.prismDummy(menuBlock)
    FFL2R_utils.GamePrep.newCredits(memoBlock)

    FFL2R_qol.ScriptedQOL.newNPCHelpers(scriptingBlock1, scriptingBlock2, maps)

    magiShuffle(scriptingBlock1, scriptingBlock2, memoBlock, maps, FFL2R_data.GameData.magi)
    treasureShuffle(maps, scriptingBlock2, FFL2R_data.GameData.treasures, treasureFlagReclaim)
    shopRando(shops, FFL2R_data.GameData.shopTiers)
    worldShuffle(romData, maps, scriptingBlock1, scriptingBlock2, FFL2R_data.GameData.pillarsWorlds)

    FFL2R_utils.GamePrep.convertToRealChests(scriptingBlock1, maps, treasureFlagReclaim)

    newStarters(monsterTable, menuBlock)

    if encounterRate != 100:
        encounterRate = FFL2R_utils.Utility.setBoundaries(encounterRate, 20, 200)
        encounterRateAdjustment(maps, encounterRate)

    if goldDrops != 100:
        goldDrops = FFL2R_utils.Utility.setBoundaries(goldDrops, 50, 500)
        goldAdjustment(goldTable, goldDrops)
    
    for k,v in FFL2R_data.GameData.newItemPrices.items():
         romData[k] = v

    romData = FFL2R_io.File.editRom(romData, scriptingBlock1, scriptingBlock2, menuBlock, memoBlock, maps, shops, goldTable, 
                                    monsterTable)

    FFL2R_io.File.writeOutRom(romData, gameSeed, encounterRate, goldDrops)
    print("Done!")

def goldAdjustment(goldTable:FFL2R_io.GoldData, rate:int):
    percent = rate / 100

    for v in goldTable.table.values():
        gold = int(v.actualValue * percent)
        #10% stack bonus causes overflow issues, so capped at 59578
        if gold > 59578:
            gold = 59578
        v.actualValue = gold
        v.updateGold(gold)

def encounterRateAdjustment(maps:FFL2R_io.MapData, rate:int):
    percent = rate / 100

    #if a map's encounter rate is 0, it winds up for a default encounter rate somehow. So it floors at 1.
    for v in maps.header.values():
        if v.isDangerous == True:
            v.encounterRate = int(v.encounterRate * percent)
            if v.encounterRate == 0:
                v.encounterRate = 1

def treasureShuffle(mapHeaders:FFL2R_io.MapData, scriptingBlock2:FFL2R_io.ScriptBlock, treasures:list, treasureFlagReclaim:list):
    treasuresList = treasures
    random.shuffle(treasuresList)
    #0=npc, 1=treasures, 2=magi
    treasureChests = mapHeaders.findNPCs(1)
    for chest in treasureChests:
        chest[2][4] = treasuresList[0]
        if treasuresList[0] == 0xFF:
            x = FFL2R_utils.Utility.findCoordinate(chest[2][2])
            y = FFL2R_utils.Utility.findCoordinate(chest[2][3])
            treasureFlagReclaim.append(chest[2][1])
            chest[2] = [0x0, 0xf, x+0x40, y+0xc0, 0x3, 0xf1]
        treasuresList.pop(0)
        mapHeaders.header[chest[0]].npcs[chest[1]] = chest[2]
    startGift = random.randint(0, len(FFL2R_data.GameData.itemList))
    scriptingBlock2.script[19].scriptData[26] = FFL2R_data.GameData.itemList[startGift]
    scriptingBlock2.script[19].scriptData[41] = FFL2R_data.GameData.itemList[startGift]

def magiShuffle(scriptingBlock1:FFL2R_io.ScriptBlock, scriptingBlock2:FFL2R_io.ScriptBlock, memoBlock:FFL2R_io.ScriptBlock, mapHeaders:FFL2R_io.MapData, magi:list):
    magiList = magi
    random.shuffle(magiList)
    magiChests = mapHeaders.findNPCs(2)
    raceMagi = []
    leonsMagi = 0x00 #in bank 2
    for chest in magiChests:
        chest[2][4] = magiList[0]
        magiList.pop(0)
        mapHeaders.header[chest[0]].npcs[chest[1]] = chest[2]
    scriptList = scriptingBlock1.findScriptsByBytes([0x19, 0x0A])
    for script in scriptList:
        if script[0] != 86: #skip trueeye script
            scriptingBlock1.script[script[0]].scriptData[script[1]+2] = magiList[0]
            magiList.pop(0)
    scriptList = scriptingBlock2.findScriptsByBytes([0x19, 0x0A])
    for script in scriptList:
        scriptingBlock2.script[script[0]].scriptData[script[1]+2] = magiList[0]
        if script[0] == 164: #leon's return cutscene
            leonsMagi = magiList[0] #leon's theft
            scriptingBlock1.replaceScript(54, FFL2R_utils.GamePrep.leonsText(leonsMagi))
        if script[0] in (201, 202, 203): #race scripts
            raceMagi.append(magiList[0])
        magiList.pop(0)
        if script[0] == 204 and raceMagi: #slow dragon race script
            magiList.insert(0, raceMagi[0])
            raceMagi.pop(0)
    scriptList = memoBlock.findScriptsByBytes([0x19, 0x0A])
    for script in scriptList:
        memoBlock.script[script[0]].scriptData[script[1]+2] = magiList[0]
        magiList.pop(0)

def shopRando(shops:FFL2R_io.ShopData, tiers:list):
    def mixTier(tierData:list)->list:
        random.shuffle(tierData)
        return tierData
    def populateShop(currentShop:list, count:int, availableItems:list, *extraItems:list):
        for i in range(0, count):
            if random.randint(0,3) == 3 and len(extraItems) > 0:
                currentShop[i] = extraItems[0][i]
            else:
                currentShop[i] = availableItems[i]
            i+=1
        if count < 8 and random.randint(0,2) >= 1 and len(extraItems) > 1:
                currentShop[i] = extraItems[1][0]
        return currentShop

    for v in shops.data.values():
        currentShop = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
        length = random.randint(6,8)
        match v.tier:
            case 0: #recurring
                currentShop = tiers[8]
            case 7: #final shop
                items = mixTier(tiers[7])
                currentShop = populateShop(currentShop, 8, items)
            case 8: #Echigoya will always have a full stock of eight items
                items = mixTier(tiers[7]+tiers[0])
                currentShop = populateShop(currentShop, 8, items)             
            case 9: #giant town special, grab from 0 first then 6/7
                items = mixTier(tiers[0])
                bonusItems = mixTier(tiers[6]+tiers[7])
                items = items + bonusItems
                currentShop = populateShop(currentShop, length, items)
            case _: #most other shops
                items = mixTier(tiers[v.tier])
                bonusItems = mixTier(tiers[v.tier+1])
                specialItems = mixTier(tiers[0])
                currentShop = populateShop(currentShop, length, items, bonusItems, specialItems)
        v.wares = currentShop

def newStarters(monsterBlock:FFL2R_io.MonsterData, menuBlock:FFL2R_io.ScriptBlock):
    randoMonsters = random.sample(range(180),3)
    for starter in randoMonsters:
        starterIndex = randoMonsters.index(starter)
        monsterBlock.data[245+starterIndex].monsterFamily = monsterBlock.data[starter].monsterFamily
        monsterBlock.data[245+starterIndex].monsterAI = monsterBlock.data[starter].monsterAI
        monsterBlock.data[245+starterIndex].monsterGFX = monsterBlock.data[starter].monsterGFX
        monsterBlock.data[245+starterIndex].monsterNPC = monsterBlock.data[starter].monsterNPC
        monsterBlock.data[245+starterIndex].statArray = monsterBlock.data[starter].statArray
        monsterBlock.data[245+starterIndex].skillLength = monsterBlock.data[starter].skillLength
        monsterBlock.data[245+starterIndex].skillList = monsterBlock.data[starter].skillList
        monsterBlock.data[245+starterIndex].name = monsterBlock.data[starter].name
        monsterBlock.data[245+starterIndex].goldIndex = monsterBlock.data[starter].goldIndex

        if monsterBlock.data[starter].dslevel < 10:
            hexLevel = [0xFF, 0xFF, 0xB0 + monsterBlock.data[starter].dslevel]
        else:
            hexLevel = [0xFF, 0xB1, (0xB0 + (monsterBlock.data[starter].dslevel - 10))]
        match starterIndex:
            case 0:
                pos = 69
            case 1:
                pos = 83
            case 2:
                pos = 97
        menuBlock.insertIntoScript(21, pos, hexLevel)

def worldShuffle(romData:mmap, mapHeaders:FFL2R_io.MapData, scriptingBlock1:FFL2R_io.ScriptBlock, scriptingBlock2:FFL2R_io.ScriptBlock, pillarsWorlds:dict):
    warpScripts = {}
    warpNames = {}
    newWorldOrder = list(pillarsWorlds.values())
    for world in newWorldOrder:
        if world[3]:
            for s in world[3]:
                warpScripts[s] = scriptingBlock1.script[s].scriptData
        if world[4]:
            for loc in world[4]:
                name = []
                for x in range(0, 16):
                   name.append(romData[loc+x])
                warpNames[loc] = name
    random.shuffle(newWorldOrder)
    scriptIndex = 0
    prismArray = []
    prismLoc = 0x3e600
    teleCounter = 2
    j = 0x3f6f0
    for k in pillarsWorlds.keys():
        gWorld = False
        if newWorldOrder[0][0] == 87:
            gWorld = True
            trigger = [87,0]
        elif newWorldOrder[0][0] > 255:
            trigger = [newWorldOrder[0][0]-256, 6]
        else:
            trigger = [newWorldOrder[0][0], 5]
        mapHeaders.header[k[0]].triggerRef[k[1]] = trigger
        mapHeaders.header[k[0]].triggerRef[k[3]] = [newWorldOrder[0][6],0]
        if k[2] > 255:
            trigger = [k[2] - 256, 6]
        else:
            trigger = [k[2], 5]
        mapHeaders.header[newWorldOrder[0][1]].triggerRef[newWorldOrder[0][2]] = trigger
        if gWorld == True:
            mapHeaders.header[90].triggerRef[0] = trigger
        if newWorldOrder[0][3]:
            for s in newWorldOrder[0][3]:
                scriptingBlock1.replaceScript(99+scriptIndex, warpScripts[s])
                scriptIndex+=1
        if newWorldOrder[0][4]:
            for loc in newWorldOrder[0][4]:
                for x in range(0,16):
                    romData[j] = warpNames[loc][x]
                    j+=1
        if newWorldOrder[0][5]:
            teleCounter+=newWorldOrder[0][5][3]
            if newWorldOrder[0][5][0] == 1:
                scriptingBlock2.script[newWorldOrder[0][5][1]].scriptData[newWorldOrder[0][5][2]+2] = teleCounter
            else:
                scriptingBlock1.script[newWorldOrder[0][5][1]].scriptData[newWorldOrder[0][5][2]+2] = teleCounter
        prismArray.append(newWorldOrder[0][7])
        newWorldOrder.pop(0)
    # for x in range(0,14):
    #     match x:
    #         case 0:
    #             romData[prismLoc] = 7
    #         case 2:
    #             romData[prismLoc + 2] = romData[prismLoc + 1] + 1
    #         case 4:
    #             romData[prismLoc + 4] = romData[prismLoc + 3] + 7
    #         case 8:
    #             romData[prismLoc + 8] = romData[prismLoc + 7] + 1
    #         case _:
    #             romData[prismLoc + x] = romData[prismLoc + x - 1] + prismArray[0]
    #             prismArray.pop(0)





            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int) # todo - pathlib
    parser.add_argument('-r', '--rom_path', type=str, dest="rom_path")
    parser.add_argument('-e', '--encounter_rate', type=int)
    parser.add_argument('-g', '--gold_drops', type=int)
    args = parser.parse_args()
    main(rom_path = args.rom_path, seed=args.seed, encounterRate=args.encounter_rate, goldDrops=args.gold_drops)


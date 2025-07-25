import random
import FFL2R_data
import FFL2R_utils
import FFL2R_io
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename

VERSION = 0.7

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

    romData = FFL2R_io.File.readInRom(gameFile)

    romData = FFL2R_utils.Utility.bugFixQOL(romData)

    mapHeaders = FFL2R_io.MapHeaderData(romData, 0x1c800, 0x1e5f8)
    scriptingBlock1 = FFL2R_io.ScriptBlock(romData, 0x2c000, 0x2eb7f, 0x28000)
    scriptingBlock2 = FFL2R_io.ScriptBlock(romData, 0x28000, 0x2be3e, 0x24000)
    battleBlock = FFL2R_io.ScriptBlock(romData, 0x2eb80, 0x2f3ff, 0x28000)
    menuBlock = FFL2R_io.ScriptBlock(romData, 0x2f400, 0x2ffcf, 0x28000)
    shops = FFL2R_io.ShopData(romData, 0x3f9e0, 0x3fa9f)
    goldTable = FFL2R_io.GoldData(romData, 0x33e50, 0x33e7f)
    monsterTable = FFL2R_io.MonsterData(romData, 0x33800, 0x33d50, 0x36400, 0x36b70, 0x36f80, 0x3eec0, 0x33c50)

    preGame(scriptingBlock1, scriptingBlock2, menuBlock, mapHeaders, gameSeed)

    magiShuffle(scriptingBlock1, scriptingBlock2, mapHeaders, FFL2R_data.GameData.magi)
    treasureShuffle(mapHeaders, FFL2R_data.GameData.treasures)
    shopRando(shops, FFL2R_data.GameData.shopTiers)

    newStarters(monsterTable, menuBlock)

    if encounterRate != 100:
        encounterRate = FFL2R_utils.Utility.setBoundaries(encounterRate, 20, 200)
        encounterRateAdjustment(mapHeaders, encounterRate)

    if goldDrops != 100:
        goldDrops = FFL2R_utils.Utility.setBoundaries(goldDrops, 50, 500)
        goldAdjustment(goldTable, goldDrops)
    
    for key, value in FFL2R_data.GameData.newItemPrices.items():
         romData[key] = value
    
    romData = FFL2R_io.File.editRom(romData, scriptingBlock1, scriptingBlock2, menuBlock, mapHeaders, shops, goldTable, monsterTable)

    FFL2R_io.File.writeOutRom(romData, gameSeed, encounterRate, goldDrops)

    print ("Done!")


def preGame(scriptingBlock1:FFL2R_io.ScriptBlock, scriptingBlock2:FFL2R_io.ScriptBlock, menuBlock:FFL2R_io.ScriptBlock, mapHeaders:FFL2R_io.MapHeaderData, seed:int):
    #giving Ashura and Venus unique drop scripts
    scriptingBlock1.addNewScript([0x19, 0x0A, 0x00, 0x19, 0x0A, 0x01, 0x19, 0x0A, 0x02, 0x19, 0x0A, 0x04, 0x19, 0x0A, 0x05, 0x19, 0x0A, 
                                  0x06, 0x19, 0x0A, 0x07, 0x00])
    scriptingBlock1.addNewScript([0x19, 0x0A, 0x00, 0x19, 0x0A, 0x01, 0x19, 0x0A, 0x02, 0x19, 0x0A, 0x04, 0x19, 0x0A, 0x05, 0x19, 0x0A, 
                                  0x06, 0x19, 0x0A, 0x07, 0x00])
    #ashura
    scriptingBlock2.script[77].scriptData[348] = 0xC0
    #venus
    scriptingBlock1.script[43].scriptData[105] = 0xC1

    #title screen mod
    titleInfo = FFL2R_utils.Utility.infoPatchList(VERSION, seed)
    menuBlock.addBytes(20, 29)
    menuBlock.script[20].scriptData = [0x00, 0x0A, 0x14, 0x08] + titleInfo + [0x2E, 0xFF, 0xBC, 0x65, 0xE7, 0x56, 0xE8, 0xD8, 
                                                                            0x06, 0xFF, 0xA2, 0xB1, 0xB9, 0xB9, 0xB1, 0xFF, 
                                                                            0xCC, 0xCA, 0xCE, 0xBA, 0xCB, 0xBE, 0xFF, 0xCC, 
                                                                            0xC8, 0xBF, 0xCD, 0x05, 0xC5, 0xC2, 0xBC, 0xBE, 
                                                                            0xC7, 0xCC, 0xBE, 0xBD, 0xFF, 0xBB, 0xD2, 0xFF, 
                                                                            0xC7, 0xC2, 0xC7, 0xCD, 0xBE, 0xC7, 0xBD, 0xC8, 
                                                                            0x00]
    #safeunlocks
    # All MAGI checks are an invisible npc that otherwise halts the player if they fail to meet the requirement -- "We need more MAGI to open this door!"
    # this can put the player in a rough state if the player Teleports/Pegasus/ItemDoor's to a world where they cannot escape, usually happens when 
    # Apollo steals MAGI. This function makes it so that once the magi check passes, the NPC vanishes and does not respawn.
    # Functionally, all these checks use script variable 16. The "opened" script increments the state, pulls the player through into the door,
    # and then decrements the state. This edits the script to not decrement while putting a max state on these NPCs so they do not respawn.
    scriptingBlock1.script[47].scriptData = [0x12, 0x10, 0x10, 0x06, 0x36, 0x05, 0xC8, 0xE3, 0x8B, 0x8F, 0xF3, 0x0B, 0x0D, 0x19, 0xF0, 
                                        0x01, 0xFF, 0x00]
    scriptingBlock1.addBytes(47, -2)
    doorLocks = {
            23 : 0x01, #to giant world, map 23
            39 : 0x02, #giant house, map 39 npc1
            40 : 0x04, #to apollo world 40
            47 : 0x03, #to Ki's head, wholly unnecessary but nice to be consistent map 47
            56 : 0x05, #to guardian world map 56
            84 : 0x06, #to ninja world map 84
            100 : 0x07, #to venus world map 100
            103 : 0x08, #to race world map 103
            125 : 0x09, #to edo map 125
            136 : 0x0A, #to nasty dungeon world map 136
            161 : 0x0B, #to valhalla map 161
            174 : 0x0C, #to central world map 174 npc14
            175 : 0x0A  #map 175 back to valhalla. Maybe a bug since it checks for 66 Magi (to Edo) which is script 76, rather than 76 MAGI; but all irrelevant since it's meant to block you into final world.
            }

    for k,v in doorLocks.items():
        match k:
            case 39:
                npcTarget = 1
            case 174:
                npcTarget = 14
            case _:
                npcTarget = 0
        mapHeaders.header[k].npcs[npcTarget][1] = v
    #ki's variables from 16 to 5 just for cleanliness
    scriptingBlock1.script[37].scriptData[4] = 0x05
    scriptingBlock1.script[37].scriptData[23] = 0x05
    mapHeaders.header[54].npcs[1][0] = 0x05 #head magi tc

    #Adjusting var1 usage lets us move Mr.S and prevent him from blocking the first cave.
    scriptingBlock1.script[19].scriptData[1:3] = [0x01, 0x1F]
    scriptingBlock1.insertIntoScript(19, 20, [0x12, 0x01])
    scriptingBlock1.addBytes(19, 2)
    scriptingBlock2.script[249].scriptData[2] = 0x2F
    scriptingBlock1.script[20].scriptData[5] = 0x3F
    scriptingBlock1.script[20].scriptData[125] = 0x03
    scriptingBlock2.script[47].scriptData[350] = 0x04
    scriptingBlock1.script[18].scriptData[2] = 0x03
    scriptingBlock1.script[22].scriptData[2] = 0x5F
    scriptingBlock1.script[22].scriptData[56] = 0x05
    scriptingBlock1.script[23].scriptData[2] = 0x6F
    scriptingBlock1.script[23].scriptData[28] = 0x06
    mapHeaders.header[4].npcs[0][0] = 0x01
    mapHeaders.header[5].npcs[0][1] = 0x01
    mapHeaders.header[5].npcs[1] = [0x01, 0x3F, 0xEF, 0x0A, 0x18, 0xA1]
    mapHeaders.header[11].npcs[10][1] = 0x03
    mapHeaders.header[11].npcs[11][1] = 0x45
    mapHeaders.header[11].npcs[12][1] = 0x66
    mapHeaders.header[12].npcs[1][1] = 0x66
    mapHeaders.header[12].npcs[2][1] = 0x7F
    mapHeaders.header[15].npcs[0][1] = 0x04
    mapHeaders.header[15].npcs[1][1] = 0x04
    mapHeaders.header[15].npcs[2][1] = 0x55
    mapHeaders.header[15].npcs[3][1] = 0x55

def goldAdjustment(goldTable:FFL2R_io.GoldData, rate:int):
    percent = rate / 100

    for k,v in goldTable.table.items():
        gold = int(v.actualValue * percent)
        #10% stack bonus causes overflow issues, so capped at 59578
        if gold > 59578:
            gold = 59578
        v.actualValue = gold
        v.updateGold(gold)

def encounterRateAdjustment(mapHeaders:FFL2R_io.MapHeaderData, rate:int):
    percent = rate / 100

    #if a map's encounter rate is 0, it winds up for a default encounter rate somehow. So it floors at 1.
    for k,v in mapHeaders.header.items():
        if v.isDangerous == True:
            v.encounterRate = int(v.encounterRate * percent)
            if v.encounterRate == 0:
                v.encounterRate = 1

def treasureShuffle(mapHeaders:FFL2R_io.MapHeaderData, treasures:list):
    treasuresList = treasures
    random.shuffle(treasuresList)
    #0=npc, 1=treasures, 2=magi
    treasureChests = mapHeaders.findNPCs(1)
    for chest in treasureChests:
        chest[2][4] = treasuresList[0]
        if treasuresList[0] == 0xFF:
            #show empty
            chest[2][2]+=64
        treasuresList.pop(0)
        mapHeaders.header[chest[0]].npcs[chest[1]] = chest[2]

def magiShuffle(scriptingBlock1:FFL2R_io.ScriptBlock, scriptingBlock2:FFL2R_io.ScriptBlock, mapHeaders:FFL2R_io.MapHeaderData, magi:list):
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
        print(script)
        scriptingBlock2.script[script[0]].scriptData[script[1]+2] = magiList[0]
        if script[0] == 164: #leon's return cutscene
            leonsMagi = magiList[0] #leon's theft
            #any script edits should all equally be the same 106 bytes, so no byte update necessary
            scriptingBlock1.script[54].scriptData = FFL2R_utils.Utility.leonsText(leonsMagi)
        if script[0] in (201, 202, 203): #race scripts
            raceMagi.insert(0, magiList[0])
        magiList.pop(0)
        if script[0] == 204 and raceMagi: #slow dragon race script
            magiList.insert(0, raceMagi[0])
            raceMagi.pop(0)  

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

    for k,v in shops.data.items():
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
                currentShop = populateShop(currentShop, length, items, bonusItems)
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
        menuBlock.addBytes(21, 3)
        menuBlock.insertIntoScript(21, pos, hexLevel)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=int) # todo - pathlib
    parser.add_argument('-r', '--rom_path', type=str, dest="rom_path")
    parser.add_argument('-e', '--encounter_rate', type=int)
    parser.add_argument('-g', '--gold_drops', type=int)
    args = parser.parse_args()
    main(rom_path = args.rom_path, seed=args.seed, encounterRate=args.encounter_rate, goldDrops=args.gold_drops)


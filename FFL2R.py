import random
import argparse
import mmap

from tkinter import Tk
from tkinter.filedialog import askopenfilename

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

VERSION = 2.0


def main(rom_path:str|None, seed:int|None, encounterRate:int|None, goldDrops:int|None, worldType:int|None):
    Tk().withdraw()
    if not rom_path:
        gameFile = askopenfilename(title="First, please point to the FFL2 rom.")
    else:
        gameFile = rom_path

    #  seeding
    if not seed:
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


    treasureFlagReclaim = []

    romData = File.readInRom(gameFile)

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

    FFL2R_manager_base.GamePrep.newTitleScreen(scripts, gameSeed)
    FFL2R_manager_base.GamePrep.newDropScripts(scripts)
    FFL2R_manager_base.GamePrep.kiShrineCleanup(scripts, maps)
    FFL2R_manager_base.GamePrep.memoRemove(scripts, romData)
    FFL2R_manager_base.GamePrep.venusWorldCleanup(scripts, maps)
    FFL2R_manager_base.GamePrep.dadDeathCutscenes(scripts)
    FFL2R_manager_base.GamePrep.warMachAdjust(scripts, maps, treasureFlagReclaim)
    FFL2R_manager_base.GamePrep.nastyChest(scripts, maps)
    FFL2R_manager_base.GamePrep.prismDummy(scripts)
    FFL2R_manager_base.GamePrep.guardianBaseLogic(maps)
    FFL2R_manager_base.GamePrep.newCredits(scripts)

    FFL2R_manager_base.ScriptedQOL.newNPCHelpers(scripts, maps)

    magiShuffle(scripts, maps, GameData.MAGI)
    treasureShuffle(maps, scripts, GameData.TREASURES, treasureFlagReclaim)
    shopRando(shops, GameData.shopTiers)
    worldShuffle(romData, maps, scripts, worlds, worldType)

    FFL2R_manager_base.GamePrep.convertToRealChests(scripts, maps, treasureFlagReclaim)

    newStarters(monsters, scripts)

    if encounterRate != 100:
        encounterRate = Utility.setBoundaries(encounterRate, 20, 200)
        encounterRateAdjustment(maps, encounterRate)

    if goldDrops != 100:
        goldDrops = Utility.setBoundaries(goldDrops, 50, 500)
        goldAdjustment(gold, goldDrops)
    
    for k,v in GameData.newItemPrices.items():
         items.item[k].setPrice(v)

    romData = File.editRom(romData, scripts, maps, shops, monsters, gold, items)

    File.writeOutRom(romData, gameSeed, encounterRate, goldDrops, worldType)
    print("            Randomizer finished successfully. Right on!")


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

def treasureShuffle(maps:MapManager, scripts:ScriptManager, treasures:list, treasureFlagReclaim:list):
    treasuresList = treasures
    random.shuffle(treasuresList)
    #0=treasures, 1=magi
    treasureChests = maps.findNPCs(0)
    for chest in treasureChests:
        newChest = bytearray.fromhex(chest[2][0:12] + f"{treasuresList[0]:02x}" + chest[2][15:17])
        if treasuresList[0] == 0xFF:
            x, y = Utility.findCoordinate(int(chest[2][6:8], 16)), Utility.findCoordinate(int(chest[2][9:11], 16))
            treasureFlagReclaim.append(chest[2][1])
            newChest = bytearray.fromhex('00 0f ' + f"{x+0x40:02x}" + f"{y+0xc0:02x}" + '03 f1')
        treasuresList.pop(0)
        maps.map[chest[0]].npcs[chest[1]] = newChest
    startGift = random.choice(list(GameData.ITEMS.keys()))
    scripts.main[275][26] = startGift
    scripts.main[275][41] = startGift

def magiShuffle(scripts:ScriptManager, maps:MapManager, magi:list):
    def _newMagi(scripts:ScriptManager, magiList:list, x:int, y:int):
        scripts.main[x][y] = magiList[0]
        magiList.pop(0)
    magiList = magi
    random.shuffle(magiList)
    magiChests = maps.findNPCs(1)
    raceMagi = []
    leonsMagi = 0x00
    for chest in magiChests:
        newChest = bytearray.fromhex(chest[2][0:12] + f"{magiList[0]:02x}" + chest[2][15:17])
        magiList.pop(0)
        maps.map[chest[0]].npcs[chest[1]] = newChest
    scriptList = scripts.findScriptByBytes('19 0a')
    for script in scriptList:
        if script[0] == 3:
            scripts.memo[script[1]][script[2]+2] = magiList[0]
            magiList.pop(0)
        else:
            match script[1]:
                case 86: #skip trueeye script
                    pass
                case 420: #leon's return cutscene
                    leonsMagi = magiList[0] #leon's theft
                    scripts.replaceScript(0, 54, FFL2R_manager_base.GamePrep.leonsText(leonsMagi))
                    _newMagi(scripts, magiList, script[1], script[2]+2)
                case 457|458|459:
                    raceMagi.append(magiList[0])
                    _newMagi(scripts, magiList, script[1], script[2]+2)
                case 460:
                    if script[2] != 24:#position 24 signifies the first magi reward and should avoid using racemagi
                        magiList.insert(0, raceMagi[0])
                        raceMagi.pop(0)
                    _newMagi(scripts, magiList, script[1], script[2]+2)
                case _:
                    _newMagi(scripts, magiList, script[1], script[2]+2)

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
    #prismArray = []
    #prismLoc = 0x3e600
    teleCounter = 2
    finalStore = list(worlds.finalStore.values())
    worlds.magiCheckRedo(scripts, maps, worldType)
    if worldType != 1:
        maps.map[finalStore[0][1]].npcs[finalStore[0][2]][0] = 0x10
        maps.map[finalStore[0][1]].npcs[finalStore[0][2]][1] = 0x1f
        maps.map[finalStore[1][1]].npcs[finalStore[1][2]][0] = 0x10
        maps.map[finalStore[1][1]].npcs[finalStore[1][2]][1] = 0x1f
        if worldType == 3:
            for world in worlds.world.values():
                for x in finalStore:
                    if x[0] == world.index:
                        maps.map[x[1]].npcs[x[2]][0] = 0x00
                        maps.map[x[1]].npcs[x[2]][1] = 0x0F
                if world.scriptTeleportUnlockByte:
                    scripts.main[world.scriptTeleportUnlockByte[0]][world.scriptTeleportUnlockByte[1]+2] = 0x0D
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
        #    prismArray.append(newWorldOrder[0].prismCount)
            for x in finalStore:
                if x[0] == newWorldOrder[0].index:
                    maps.map[x[1]].npcs[x[2]][0] = 0x10
                    maps.map[x[1]].npcs[x[2]][1] = (v.order*16)+15
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
    parser.add_argument('-g', '--gold', type=int)
    parser.add_argument('-w', '--world', type=int)
    args = parser.parse_args()
    main(rom_path = args.rom_path, seed=args.seed, encounterRate=args.encounter_rate, goldDrops=args.gold, worldType=args.world)


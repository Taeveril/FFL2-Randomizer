import mmap
import hashlib
import FFL2R_utils

class ScriptBlock:
    def __init__(self, rom:mmap, startAddr:int, endAddr:int, bankOffset:int):
        self.startAddr = startAddr
        self.endAddr = endAddr
        self.bankOffset = bankOffset
        self.headerEnd = self.getHeaderEnd(rom)
        self.headerBlock = self.getHeaderBlock(rom)
        self.newScriptPlacement = 0x00000
        self.script = self.getData(rom)
        self.currentOffset = 0

    def getHeaderEnd(self, rom:mmap)->int:
        return (rom[self.startAddr+1] << FFL2R_utils.MAXINT.bit_length() | rom[self.startAddr]) + self.bankOffset

    def getHeaderBlock(self, rom:mmap)->dict:
        header = {}
        i=self.startAddr
        while i<self.headerEnd:
            header[i] = rom[i+1] << FFL2R_utils.MAXINT.bit_length() | rom[i]
            i+=2
        return header

    def getData(self, rom:mmap)->dict:
        blockLast = self.endAddr
        d = {}
        indexer=0
        for k,v in self.headerBlock.items():
            if k != self.headerEnd - 2:
                length = self.headerBlock[k+2] - v
            else:
                while rom[blockLast] == 0x00:
                    blockLast-=1
                #all scripts must end with a 0x00
                length = blockLast - (v+self.bankOffset) +2
                self.newScriptPlacement = blockLast + 2
            scriptData = self.getScriptData(rom, v, length)
            script = Script(scriptData, k, v, self.bankOffset)
            d[indexer] = script
            indexer+=1
        return d

    def getScriptData(self, rom:mmap, addr:int, length:int)->list:
        data = []
        i=0
        while i < length:
            data.append(rom[addr + self.bankOffset + i])
            i+=1
        return data
    
    #provide list, add script at the end
    def addNewScript(self, hexes:list):
        lastIndex = 0
        for k in self.script.keys():
            if k > lastIndex:
                lastIndex = k
            self.script[k].addr+=2
            self.script[k].relAddr+=2
        newIndexer = lastIndex + 1
        newHeaderAddr = self.script[k].headerAddr + 2
        newRelAddr = self.script[k].relAddr + len(self.script[k].scriptData)
        self.script[newIndexer] = Script(hexes, newHeaderAddr, newRelAddr, self.bankOffset)
        self.currentOffset + 2

    def addBytes(self, targetScriptIndex:int, amount:int):
        for k in self.script.keys():
            if k > targetScriptIndex:
                self.script[k].relAddr += amount
                self.script[k].addr += amount

    def findScriptsByBytes(self, matchList:list)->list:
        scriptList = []
        for k, v in self.script.items():
            i=0
            while i < (len(v.scriptData) - len(matchList) + 1):
                if v.scriptData[i:len(matchList)+i] == matchList:
                    scriptList.append([k, i])
                i+=1
        return scriptList

    def insertIntoScript(self, index:int, position:int, insertion:list):
        self.script[index].scriptData = self.script[index].scriptData[:position] + insertion + self.script[index].scriptData[position:]

class Script:
    def __init__(self, array:list, header:int, location:int, bank:int):
        self.headerAddr = header
        self.relAddr = location
        self.addr = self.relAddr + bank
        self.scriptData = array


class MapHeaderData:
    def __init__(self, rom:mmap, startAddr:int, endAddr:int):
        self.startAddr = startAddr
        self.endAddr = endAddr
        self.header = self.getHeaderData(rom)

    def getHeaderData(self, rom:mmap)->dict:
        i = self.startAddr
        hd = {}
        index = 0
        while i <= self.endAddr:
            k=i
            tileMap = rom[i+1]<< FFL2R_utils.MAXINT.bit_length() | rom[i]
            i+=2
            tileSet = rom[i]
            i+=1
            #high nibble: first two bits are animspeed, third bit isDangerous, fourth bit isNPCs
            flagsAndTriggerTiles = rom[i]
            nh = (rom[i] & 0xf0) >> 4
            nl = (rom[i] & 0x0f) #trigger tile count
            animSpeed = nh % 4
            if nh & 4 == 4:
                isDangerous = True
            else:
                isDangerous = False
            if nh & 8 == 8:
                isNPCs = True
            else:
                isNPCs = False
            i+=1
            if isDangerous:
                encounterSet = rom[i]
                i+=1
                encounterRate = rom[i]
                i+=1
            else:
                encounterSet = None
                encounterRate = None
            triggerCount = rom[i]
            i+=1
            if triggerCount > 0:
                ref = 0
                triggerRef = []
                while ref < triggerCount:
                    trigger = [rom[i], rom[i+1]]
                    triggerRef.append(trigger)
                    i+=2
                    ref+=1
            else:
                triggerRef = None
            if isNPCs:
                npcArray = []
                npcgfx = []
                while (rom[i] != 0xFF) and (len(npcgfx) <= 5):
                    npcgfx.append(rom[i])
                    i+=1
                else:
                    if len(npcgfx) != 6:
                        npcgfx.append(0xFF)
                        i+=1
                while(rom[i] != 0xFF):
                    npc = [rom[i], rom[i+1], rom[i+2], rom[i+3], rom[i+4], rom[i+5]]
                    npcArray.append(npc)
                    i+=6
                npcArray.append(0xFF)
                i+=1
            else:
                npcgfx = None
                npcArray = None
            hd[index] = MapHeader(k, tileMap, tileSet, flagsAndTriggerTiles, nl, animSpeed, isDangerous, encounterSet, encounterRate, isNPCs, 
                                      triggerCount, triggerRef, npcgfx, npcArray)
            index+=1
        return hd

    def findNPCs(self, findType:int, *varCheck:int)->list:
        npcList = []
        for k, v in self.header.items():
            if v.isNPCs:
                for npc in v.npcs:
                    match findType:
                        case 0:
                            if isinstance(npc, list) and ((npc[0] & 0x0f) | (((npc[0] & 0x10) >> 4) << 4)) == varCheck[0]:
                                npcList.append([k, v.npcs.index(npc), npc])
                        case 1:
                            if isinstance(npc, list) and npc[0] == 0x80 and npc[5] == 0xF9:
                                npcList.append([k, v.npcs.index(npc), npc])
                        case 2: 
                            if isinstance(npc, list) and npc[0] == 0x80 and npc[5] == 0xFA:
                                npcList.append([k, v.npcs.index(npc), npc])
                        case 3:
                            if isinstance(npc, list) and k == varCheck[0]:
                                print(f"{k} - {FFL2R_utils.Utility.listToHex(npc)}")
        return npcList
    
    def headerInfo(self, match:int):
        for k,v in self.header.items():
            if k == match or v.addr == match:
                print(f"""
    Index: {k}
    Addr: {hex(v.addr)}
    Tilemap: {hex(v.tileMap)}
    Tileset: {v.tileSet}
    FlagsTriggers: {hex(v.flagsAndTriggerTiles)}
    Tile Count: {v.triggerTileCount}
    Anim Speed: {v.animSpeed}
    Is Dangerous: {v.isDangerous}
    Encounter Set: {v.encounterSet}
    Encounter Rate: {v.encounterRate}
    Is NPCs: {v.isNPCs}
    Trigger Count: {v.triggerCount}
    Triggers: {v.triggerRef}
    NPCGFX: {v.npcgfx}
    NPCs: {v.npcs}"""
                )

class MapHeader:
    def __init__(self, addr:int, tileMap:int, tileSet:int, flagsAndTriggerTiles:int, triggerTileCount:int, animSpeed: int, isDangerous:bool, encounterSet:int|None, encounterRate:int|None ,isNPCs:bool, 
                 triggerCount:int, triggerRef:list|None, npcgfx:list|None, npcs:list|None):
        self.addr = addr
        self.tileMap = tileMap
        self.tileSet = tileSet
        self.flagsAndTriggerTiles = flagsAndTriggerTiles
        self.triggerTileCount = triggerTileCount
        self.animSpeed = animSpeed
        self.isDangerous = isDangerous
        self.encounterSet = encounterSet
        self.encounterRate = encounterRate
        self.isNPCs = isNPCs
        self.triggerCount = triggerCount
        self.triggerRef = triggerRef
        self.npcgfx = npcgfx
        self.npcs = npcs

class MonsterData:
    def __init__ (self, rom:mmap, monFamAddr:int, monAIAddr:int, monGFXAddr:int, monNPCAddr:int, monStatAddr:int, monNameAddr:int, 
                  monGoldAddr:int):
        self.monFamAddr = monFamAddr
        self.monAIAddr = monAIAddr
        self.monGFXAddr = monGFXAddr
        self.monNPCAddr = monNPCAddr
        self.monStatAddr = monStatAddr
        self.monNameAddr = monNameAddr
        self.monGoldAddr = monGoldAddr
        self.data = self.getData(rom)

    def getData(self, rom:mmap)->dict:
        md = {}
        for i in range(0,256):
            stats = []
            name = []
            skills = []
            for j in range(0,10):
                stats.append(rom[self.monStatAddr+(i*10)+j])
                j+=1
            for k in range(0,8):
                name.append(rom[self.monNameAddr+((i*8)+k)])
                k+=1
            skillLoc = (stats[9]<< FFL2R_utils.MAXINT.bit_length() | stats[8]) + 0x30000
            skillLength = (stats[0] & 0x0F) + 1
            for l in range(0, skillLength):
                skills.append(rom[skillLoc + l])
                l+=1
            md[i] = Monster(rom[self.monFamAddr+i], rom[self.monAIAddr+i], rom[self.monGFXAddr+i], rom[self.monNPCAddr+i], 
                            self.monStatAddr + (i * 10),
                            stats, self.monNameAddr+(i*8), name, skillLoc, skillLength,
                            skills, rom[self.monGoldAddr+i])
            i+=1
        return md
       
class Monster:
    def __init__(self, monsterFamily:int, monsterAI:int, monsterGFX:int, monsterNPC:int, statAddr:int, stats:list, nameAddr:int, name:list, skillLoc:int, skillLength:int, 
                 skills:list, goldIndex:int):
        self.monsterFamily = monsterFamily
        self.monsterAI = monsterAI
        self.monsterGFX = monsterGFX
        self.monsterNPC = monsterNPC
        self.statAddr = statAddr
        self.statArray = stats
        self.skillListLoc = skillLoc
        self.skillLength = skillLength
        self.skillList = skills
        self.nameAddr = nameAddr
        self.name = name
        self.dslevel = self.getdsLevel()
        self.goldIndex = goldIndex #low nibble is the reference, plus first bit of high nibble (24 entries)
                                   #high nibble: 2nd bit = rare drop, 3rd bit = common drop, 4th bit = meat flag

    def getdsLevel(self):
        return self.monsterAI & 0x0f

class ShopData:
    def __init__(self, rom:mmap, startAddr:int, endAddr:int):
        self.startAddr = startAddr
        self.endAddr = endAddr
        self.data = self.getShopData(rom)

    def getShopData(self, rom:mmap)->dict:
        sd = {}
        indexer = 0
        name = ""
        tier = 0
        i = self.startAddr
        while i <= self.endAddr:
            shopArray = []
            j = 0
            k = i
            for j in range (0,8):
                shopArray.append(rom[i+j])
                j+=1
            match k:
                #strings here are internal-facing only in an effort to better show shop data
                case 0x3f9e0:
                    tier = 1
                    name = "First Town, Weapon Shop"
                case 0x3f9e8:
                    tier = 2
                    name = "Desert Town, Weapon Shop"
                case 0x3f9f0:
                    tier = 2
                    name = "Ashura Town, Weapon Shop"
                case 0x3f9f8:
                    tier = 3
                    name = "Giant Town, Weapon Shop"
                case 0x3fa00:
                    tier = 1
                    name = "Second Town, Weapon Shop"
                case 0x3fa08:
                    tier = 3
                    name = "Apollo Town, Weapon Shop"
                case 0x3fa10:
                    tier = 4
                    name = "Lynn Town, Weapon Shop"
                case 0x3fa18:
                    tier = 4
                    name = "Guardian Town, Weapon Shop"
                case 0x3fa20:
                    tier = 5
                    name = "Venus Town, Weapon Shop"
                case 0x3fa28:
                    tier = 5 
                    name = "Race Town, Weapon Shop"
                case 0x3fa30:
                    tier = 6
                    name = "Edo Town, Weapon Shop"
                case 0x3fa38:
                    tier = 6
                    name = "Final Town, Weapon Shop"
                case 0x3fa40:
                    tier = 1
                    name = "First Town, Item Shop"
                case 0x3fa48:
                    tier = 2
                    name = "Desert Town, Item Shop"
                case 0x3fa50:
                    tier = 3
                    name = "Giant Town, Item Shop"
                case 0x3fa58:
                    tier = 4
                    name = "Apollo Town, Item Shop"
                case 0x3fa60:
                    tier = 4
                    name = "Guardian Town, Item Shop"
                case 0x3fa68:
                    tier = 5
                    name = "Venus Town, Item Shop"
                case 0x3fa70:
                    tier = 6
                    name = "Race Town, Item Shop"
                case 0x3fa78:
                    tier = 6
                    name = "Edo Town, Item Shop"
                case 0x3fa80:
                    tier = 7
                    name = "Final Town, Item Shop"
                case 0x3fa88:
                    tier = 0
                    name = "Recurring Item Shop"
                case 0x3fa90:
                    tier = 8
                    name = "Echigoya"
                case 0x3fa98:
                    tier = 9
                    name = "Giant Town Giant Gear Seller"
                case _:
                    print("shop err.")
            sd[k] = Shop(indexer, name, tier, shopArray)
            i+=8
            indexer+=1
        return sd
        
class Shop:
    def __init__(self, index:int, name:str, tier:int, wares:list):
        self.index = index
        self.name = name
        self.tier = tier
        self.wares = wares

class GoldData:
    def __init__ (self, rom:mmap, startAddr:int, endAddr:int):
        self.startAddr = startAddr
        self.endAddr = endAddr
        self.table = self.getGold(rom)

    def getGold(self, rom:mmap)->dict:
        indexer = 0
        gt = {}
        i = self.startAddr
        while i <= self.endAddr:
            gt[indexer] = GoldEntry(i, rom[i], rom[i+1])
            indexer+=1
            i+=2
        return gt

class GoldEntry:
    def __init__(self, addr:int, firstByte:int, secondByte:int):
        self.addr = addr
        self.firstByte = firstByte
        self.secondByte = secondByte
        self.actualValue = self.getActualValue()

    def getActualValue(self)->int:
        return self.secondByte << FFL2R_utils.MAXINT.bit_length() | self.firstByte

    def updateGold(self, newValue:int):
        self.secondByte = (newValue >> FFL2R_utils.MAXINT.bit_length()) & FFL2R_utils.MAXINT
        self.firstByte = newValue & FFL2R_utils.MAXINT

class File:
    def __init__(self):
        pass

    def readInRom(file:str)->mmap:
        with open(file, 'rb') as f:
            rom = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_COPY,offset=0)
            hashCheck = hashlib.md5(rom)
            if hashCheck.hexdigest() != "2bb0df1b672253aaa5f9caf9aab78224":
                raise Exception("MD5 hash mismatch. Invalid Final Fantasy Legend 2 ROM file.")
        return rom

    def writeOutRom(rom:mmap, seed:int, encounter:int, gold:int):
        print(f"""        Final Fantasy Legend 2 Randomizer Settings:
            Seed is: {str(seed)}
            Encounter rate adjustment is: {str(encounter)}%
            Gold adjustment is: {str(gold)}%""")
        with open('Final Fantasy Legend 2 - ' + str(seed) + '.gb', 'xb') as f:
            f.write(rom)

    def editRom(rom:mmap, script1:ScriptBlock, script2:ScriptBlock, menu:ScriptBlock, maps:MapHeaderData, 
               shops:ShopData, goldTable:GoldData, monsters:MonsterData)->mmap:
        def writeDataBlocks(rom:mmap, block:ScriptBlock):
            for v in block.script.values():
                #header write first
                rom[v.headerAddr] = v.relAddr & FFL2R_utils.MAXINT
                rom[v.headerAddr+1] = (v.relAddr >> FFL2R_utils.MAXINT.bit_length()) & FFL2R_utils.MAXINT
                i=0
                for byte in v.scriptData:
                    rom[v.addr + i] = byte
                    i+=1
            finalIndex = list(block.script.keys())[-1]
            finalEntry = block.script[finalIndex].addr + len(block.script[finalIndex].scriptData)
            while finalEntry < block.endAddr:
                 rom[finalEntry] = 0x00
                 finalEntry+=1

        def writeMapHeaders(rom:mmap, maps:MapHeaderData):
            for v in maps.header.values():
                i=0
                rom[v.addr] = v.tileMap & FFL2R_utils.MAXINT
                i+=1
                rom[v.addr+i] = (v.tileMap >> FFL2R_utils.MAXINT.bit_length()) & FFL2R_utils.MAXINT
                i+=1
                rom[v.addr+i] = v.tileSet
                i+=1
                rom[v.addr+i] = v.flagsAndTriggerTiles
                i+=1
                if v.isDangerous:
                    rom[v.addr+i] = v.encounterSet
                    i+=1
                    rom[v.addr+i] = v.encounterRate
                    i+=1
                rom[v.addr+i] = v.triggerCount
                i+=1    
                if v.triggerCount > 0x00:
                    ref = 0x00
                    while ref < v.triggerCount:
                        rom[v.addr+i] = v.triggerRef[ref][0]
                        i+=1
                        rom[v.addr+i] = v.triggerRef[ref][1]
                        i+=1
                        ref+=1
                if v.isNPCs:
                    for gfx in v.npcgfx:
                        rom[v.addr+i] = gfx
                        i+=1
                    for npcs in v.npcs:
                        if type(npcs) == list:
                            rom[v.addr+i] = npcs[0]
                            rom[v.addr+i+1] = npcs[1]
                            rom[v.addr+i+2] = npcs[2]
                            rom[v.addr+i+3] = npcs[3]
                            rom[v.addr+i+4] = npcs[4]
                            rom[v.addr+i+5] = npcs[5]
                            i+=6
                        else:
                            rom[v.addr+i] = npcs
                            i+=1
        
        def writeShops(rom:mmap, shops:ShopData):
            for k,v in shops.data.items():
                for x in range(0,8):
                    rom[k+x] = v.wares[x]

        def writeGoldTable(rom:mmap, goldTable:GoldData):
            for v in goldTable.table.values():
                rom[v.addr] = v.firstByte
                rom[v.addr+1] = v.secondByte

        def writeMonsters(rom:mmap, monsters:MonsterData):
            for k,v in monsters.data.items():
                rom[monsters.monFamAddr + k] = v.monsterFamily
                rom[monsters.monAIAddr + k] = v.monsterAI
                rom[monsters.monGFXAddr + k] = v.monsterGFX
                rom[monsters.monNPCAddr + k] = v.monsterNPC
                for x in range(0,10):
                    rom[v.statAddr + x] = v.statArray[x]
                for x in range(0, v.skillLength):
                    rom[v.skillListLoc + x] = v.skillList[x]
                for x in range(0,8):
                    rom[v.nameAddr + x] = v.name[x]
                rom[monsters.monGoldAddr + k] = v.goldIndex

        writeDataBlocks(rom, script1)
        writeDataBlocks(rom, script2)
        writeDataBlocks(rom, menu)

        writeMapHeaders(rom, maps)

        writeShops(rom, shops)

        writeGoldTable(rom, goldTable)

        writeMonsters(rom, monsters)
        return rom


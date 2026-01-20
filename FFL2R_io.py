import mmap
import hashlib
from FFL2R_utils import Utility

FFL2_HASH = "2bb0df1b672253aaa5f9caf9aab78224"

class File:
    def __init__(self):
        pass

    def readInRom(file:str)->mmap:
        with open(file, 'rb') as f:
            rom = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_COPY,offset=0)
            hashCheck = hashlib.md5(rom)
            if hashCheck.hexdigest() != FFL2_HASH:
                raise Exception("MD5 hash mismatch. Invalid Final Fantasy Legend 2 ROM file.")
        return rom

    def writeOutRom(rom:mmap, seed:int, encounter:int, gold:int, world:int):
        mode = ""
        match world:
            case 1:
                mode = "Vanilla"
            case 2:
                mode = "Shuffled"
            case 3:
                mode = "Open"
        print(f"""        Final Fantasy Legend 2 Randomizer Settings:
            Seed is: {str(seed)}
            Encounter rate adjustment is: {str(encounter)}%
            Gold adjustment is: {str(gold)}%
            World type is: {mode}""")
            
        with open('Final Fantasy Legend 2 - ' + str(seed) + '.gb', 'xb') as f:
            f.write(rom)

    def editRom(rom:mmap, scripts, maps, shops, monsters, gold, items)->mmap:
        def _scriptsToRom(rom, addrs, block):
            if len(addrs) > 4:
                headerAddr = 0x44e2
                codeAddr = addrs[4] + 0x73 #skip over the memo names
            else:
                headerAddr = addrs[0] - addrs[2] + (len(block)*2)
                codeAddr = addrs[0] + (len(block)*2)
            for k,v in block.items():
                rom[addrs[0]+(k*2)], rom[addrs[0]+(k*2)+1] = Utility.byteizeTwo(headerAddr)
                l = len(v)
                for x in range (0, l): rom[codeAddr+x] = v[x]
                headerAddr+=l
                codeAddr+=l
            if (addrs[1] - codeAddr) > 0:
                for x in range(codeAddr, addrs[1]):
                    rom[x] = 0x00
        def _mapsToRom(rom, maps):
            i = maps.MAP_STARTADDR
            for v in maps.map.values():
                rom[i], rom[i+1] = Utility.byteizeTwo(v.tileMap)
                i+=2
                rom[i] = v.tileSet
                i+=1
                rom[i] = v.flagsAndTriggerTiles
                i+=1
                if v.isDangerous:
                    rom[i] = v.encounterSet
                    i+=1
                    rom[i] = v.encounterRate
                    i+=1
                rom[i] = v.triggerCount
                i+=1    
                if v.triggerCount > 0x00:
                    for x in range (0, v.triggerCount):
                        rom[i] = v.triggers[x][0]
                        i+=1
                        rom[i] = v.triggers[x][1]
                        i+=1
                if v.isNPCs:
                    for gfx in v.npcgfx:
                        rom[i] = gfx
                        i+=1
                    for npcs in v.npcs:
                        if len(npcs) == 6:
                            rom[i] = npcs[0]
                            rom[i+1] = npcs[1]
                            rom[i+2] = npcs[2]
                            rom[i+3] = npcs[3]
                            rom[i+4] = npcs[4]
                            rom[i+5] = npcs[5]
                            i+=6
                        else:
                            rom[i] = npcs[0]
                            i+=1
            for x in range (i, maps.MAP_ENDADDR+1):
                rom[x] = 0x00
            for v in maps.door.values():
                rom[v.loc], rom[v.loc+1] = Utility.byteizeTwo(v.addr)
                rom[v.loc+2] = v.x
                match v.dirEnum:
                    case 0: #south
                        pass
                    case 1: #north
                        rom[v.loc+2]+=0x40
                    case 2: #west
                        rom[v.loc+2]+=0x80
                    case 3: #east
                        rom[v.loc+2]+=0xc0
                rom[v.loc+3] = v.y
                if v.mysteryFlag == True:
                    rom[v.loc+3]+=0x40
                if v.doorSound == True:
                    rom[v.loc+3]+=0x80
        def _shopsToRom(rom, shops):
            for v in shops.shop.values():
                for x in range(0,8):
                    rom[v.addr+x] = v.wares[x]
        def _monstersToRom(rom, monsters):
            for k,v in monsters.monster.items():
                rom[monsters.FAMILY + k] = v.family
                rom[monsters.AI + k] = v.ai
                rom[monsters.GFX + k] = v.gfx
                rom[monsters.NPC + k] = v.npc
                for x in range(0,10):
                    rom[v.statAddr + x] = v.stats[x]
                for x in range(0, v.skillsLength):
                    rom[v.skillsLoc + x] = v.skills[x]
                for x in range(0,8):
                    rom[v.nameAddr + x] = v.name[x]
                rom[monsters.GOLD + k] = v.goldIndex
        def _itemsToRom(rom, items):
            for k,v in items.item.items():
                for x in range(0,8):
                    rom[items.FLAGS+(k*8)+x] = v.flags[x]
                for x in range(0,8):
                    rom[items.NAME+(k*8)+x] = v.name[x]
                if v.price:
                    for x in range(0,3):
                        rom[items.PRICE+(k*3)+x] = v.price[x]
                rom[items.AFFINITIES+k] = v.affinities
        def _goldToRom(rom, gold):
            for v in gold.dropValue.values():
                rom[v.addr] = v.firstByte
                rom[v.addr+1] = v.secondByte

        for block in scripts.banks:
            block = dict(sorted(block.items()))
            match scripts.banks.index(block):
                case 0:
                    first = {}
                    second = {}
                    for k,v in block.items():
                        if k < 256:
                            first[k] = v
                        else:
                            second[k-256] = v
                    addrs = scripts.SCRIPT_BLOCK_1
                    _scriptsToRom(rom, addrs, first)
                    addrs = scripts.SCRIPT_BLOCK_2
                    _scriptsToRom(rom, addrs, second)
                case 1:
                    addrs = scripts.BATTLE_BLOCK
                    _scriptsToRom(rom, addrs, block)
                case 2:
                    addrs = scripts.MENU_BLOCK
                    _scriptsToRom(rom, addrs, block)
                case 3:
                    addrs = scripts.MEMO_BLOCK
                    _scriptsToRom(rom, addrs, block)
        _mapsToRom(rom, maps)
        _shopsToRom(rom, shops)
        _monstersToRom(rom, monsters)
        _goldToRom(rom, gold)
        _itemsToRom(rom, items)

        return rom
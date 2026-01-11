import mmap
from FFL2R_utils import Utility

class MapManager:
    def __init__(self, rom:mmap):
        self.MAP_STARTADDR = 0x1c800
        self.MAP_ENDADDR = 0x1e6ff
        self._EMPTY_SPACE = 0x1e5f8
        self.map = self._populateMaps(rom)
        self._DOOR_STARTADDR_1 = 0x1c000
        self._DOOR_STARTADDR_2 = 0x1ef80
        self._DOOR_ENDADDR = 0x1efff
        self.door = self._populateDoors(rom)

    def _populateMaps(self, rom:mmap)->dict:
        i = self.MAP_STARTADDR
        d = {}
        index = 0
        while i <= self._EMPTY_SPACE:
            k=i
            tileMap = Utility.twoBytes(rom[i], rom[i+1])
            i+=2
            tileSet = rom[i]    
            i+=1
            #high nibble: first two bits are animspeed, third bit isDangerous, fourth bit isNPCs
            flagsAndTriggerTiles = rom[i]
            nh = Utility.highNibble(rom[i])
            nl = Utility.lowNibble(rom[i]) #trigger tile count
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
                encounterSet, encounterRate = None, None
            triggerCount = rom[i]
            i+=1
            if triggerCount > 0:
                triggers = []
                for x in range(0, triggerCount):
                    triggers.append([rom[i], rom[i+1]])
                    i+=2
            else:
                triggers = None
            if isNPCs:
                npcArray = []
                npcgfx = bytearray()
                while (rom[i] != 0xFF) and (len(npcgfx) <= 5):
                    npcgfx.append(rom[i])
                    i+=1
                else:
                    if len(npcgfx) != 6:
                        npcgfx.extend(bytearray.fromhex('ff'))
                        i+=1
                while(rom[i] != 0xFF):
                    npc = bytearray()
                    for x in range(0,6):
                        npc.append(rom[i+x])
                    npcArray.append(npc)
                    i+=6
                npcArray.append(bytearray.fromhex('ff'))
                i+=1
            else:
                npcgfx = None
                npcArray = None
            d[index] = self.Map(k, tileMap, tileSet, flagsAndTriggerTiles, nl, animSpeed, isDangerous, encounterSet, encounterRate, isNPCs, 
                                      triggerCount, triggers, npcgfx, npcArray)
            index+=1
        return d

    class Map:
        def __init__(self, addr:int, tileMap:int, tileSet:int, flagsAndTriggerTiles:int, triggerTileCount:int, animSpeed: int, isDangerous:bool, 
                    encounterSet:int|None, encounterRate:int|None ,isNPCs:bool, triggerCount:int, triggers:list|None, npcgfx:list|None, 
                    npcs:list|None):
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
            self.triggers = triggers
            self.npcgfx = npcgfx
            self.npcs = npcs

        def info(self):
            print(f"""
            Addr:           {hex(self.addr)}
            Tilemap:        {hex(self.tileMap)}
            Tileset:        {self.tileSet}
            FlagsTriggers:  {hex(self.flagsAndTriggerTiles)}
            Tile Count:     {self.triggerTileCount}
            Anim Speed:     {self.animSpeed}
            Is Dangerous:   {self.isDangerous}
            Encounter Set:  {self.encounterSet}
            Encounter Rate: {self.encounterRate}
            Is NPCs:        {self.isNPCs}
            Trigger Count:  {self.triggerCount}
            Triggers:       {self.triggers}
            NPCGFX:         {self.npcgfx.hex(" ") if self.npcgfx else "None"}
            NPCs:           {[x.hex(" ") for x in self.npcs if type(x) == bytearray] if self.npcs else "None"}
            """
            )

    def _populateDoors(self, rom:mmap)->dict:
        def _populate(rom:mmap, start:int, stop:int, indexer:int, dataBlock:int, d:dict):
            for doorBytes in range(start, stop, 4):
                mapAddr = Utility.twoBytes(rom[doorBytes], rom[doorBytes+1])
                xval = Utility.findCoordinate(rom[doorBytes+2])
                #south = 0, north = 1, west = 2, east = 3
                direction = Utility.remainingBytes(rom[doorBytes+2], xval)
                yval = Utility.findCoordinate(rom[doorBytes+3])
                soundAndFlag = Utility.remainingBytes(rom[doorBytes+3], yval)
                mysteryFlag = bool(soundAndFlag % 2)
                doorSound = bool(soundAndFlag >> 1)
                mapIndex = self.getMapForDoor(mapAddr)
                d[indexer] = self.Door(indexer, mapAddr, mapIndex, xval, direction, yval, mysteryFlag, doorSound, dataBlock, doorBytes)
                indexer+=1
        d = {}
        _populate(rom, self._DOOR_STARTADDR_1, self.MAP_STARTADDR, 0, 1, d)
        _populate(rom, self._DOOR_STARTADDR_2, self._DOOR_ENDADDR, 512, 2, d)
        return d

    def getMapForDoor(self, loc:int)->int:
        for k, v in self.map.items():
            if v.addr == (loc + 0x18000):
                return k
        return 0


    class Door:
        def __init__(self, index:int, addr:int, mapIndex:int, x:int, dirEnum:int, y:int, flag:bool, sound:bool, block:int, loc:int):
            self.index = index
            self.addr = addr
            self.map = mapIndex
            self.x = x
            self.dirEnum = dirEnum
            self.direction = self.getDirection(self.dirEnum)
            self.y = y
            self.mysteryFlag = flag
            self.doorSound = sound
            self.dataBlock = block
            self.loc = loc

        def getDirection(self, direction:int)->str:
            match direction:
                case 0:
                    return "South"
                case 1:
                    return "North"
                case 2:
                    return "West"
                case 3:
                    return "East"
                case _:
                    return "Err"

        def info(self):
            print(f"""
            Addr:           {hex(self.addr)}
            Map:            {self.map}
            X:              {self.x}
            Y:              {self.y}
            Direction:      {self.direction}
            Mystery Flag:   {self.mysteryFlag}
            Door Sound:     {self.doorSound}
            Data Block:     {self.dataBlock}
            Loc in ROM:     {hex(self.loc)}
            """
            )

    def findNPCs(self, findType:int)->list:
        npcList = []
        for k, v in self.map.items():
            if v.isNPCs:
                for npc in v.npcs:
                    match findType:
                        case 0: #chests
                            if isinstance(npc, bytearray) and npc[0] == 0x80 and npc[5] == 0xF9:
                                npcList.append([k, v.npcs.index(npc), npc.hex(" ")])
                        case 1: #magi
                            if isinstance(npc, bytearray) and npc[0] == 0x80 and npc[5] == 0xFA:
                                npcList.append([k, v.npcs.index(npc), npc.hex(" ")])
                        case _:
                            print("FindNPC error. Invalid findtype.")
        return npcList

    def addNPC(self, index:int, gfx: int, npc:str):
        npc = bytearray.fromhex(npc)
        totalShift = 6
        if self.map[index].isNPCs:
            self.map[index].npcs.pop()
            self.map[index].npcs.append(npc)
        else:
            self.map[index].isNPCs = True
            self.map[index].npcgfx = bytearray.fromhex('ff')
            self.map[index].npcs = [npc]
            self.map[index].flagsAndTriggerTiles+=0x80
            totalShift+=2
        self.map[index].npcs.append((bytearray.fromhex('ff')))
        if gfx != 0:
            self.map[index].npcgfx.pop()
            self.map[index].npcgfx.append(gfx)
            if len(self.map[index].npcgfx) < 6:
                self.map[index].npcgfx.append(0xff)
                totalShift+=1
        for v in self.door.values():
            if v.map > index:
                v.addr+=totalShift
        
    def remNPC(self, index:int, target:int):
        totalShift = 6
        self.map[index].npcs.pop(target)
        if self.map[index].npcs[0] == bytearray.fromhex('ff'):
            self.map[index].npcs, self.map[index].npcgfx = None, None
            self.map[index].isNPCs = False
            self.map[index].flagsAndTriggerTiles-=0x80
            totalShift = 8
        for v in self.door.values():
            if v.map > index:
                v.addr-=totalShift

    def delNPC(self, index:int, amount:list):
        self.map[index].npcs.pop() #pop the 0xff!
        for i in range(amount):
            self.map[index].npcs.pop()
        self.map[index].npcs.append(bytearray.fromhex('ff'))
        for v in self.door.values():
            if v.map > index:
                v.addr-=(amount*6)
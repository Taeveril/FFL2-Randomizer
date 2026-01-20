from FFL2R_manager_scripts import ScriptManager
from FFL2R_manager_maps import MapManager

# World here doesn't mean any unique technical data, but rather
# a design. FFL2 has around a dozen or so "Worlds" that use specific
# data. This file exists as a way to manage and edit easily.
class WorldManager():
    def __init__(self):
        self.WORLD_NAME_STARTADDR = 0x3f6f0

        #pillar world, map index in door, out door, map index trigger set prism
        #in door, world, map index out door, teleport scripts, name addr, teleport unlock script location, prism count
        self.pillar = {
            "Ashura"   :    self.Pillar(2, 23, 6, 98, 5, 1),
            "Giant"    :    self.Pillar(3, 40, 6, 104, 5, 2),
            "Apollo"   :    self.Pillar(4, 56, 6, 193, 5, 3),
            "Guardian" :    self.Pillar(5, 84, 6, 230, 5, 4),
            "Monster"  :    self.Pillar(6, 100, 9, 235, 8, 5),
            "Venus"    :    self.Pillar(7, 103, 6, 280, 5, 6),
            "Race"     :    self.Pillar(8, 125, 6, 286, 5, 7),
            "Edo"      :    self.Pillar(9, 136, 6, 315, 5, 8),
            "Nasty"    :    self.Pillar(10, 161, 6, 134, 5, 9),
            "Valhalla" :    self.Pillar(11, 163, 5, 391, 4, None)
            }

        self.world = {
            "Ashura's World"   : self.World(2, 99, False, 22, 0, [99,100], [0x3f6f0, 0x3f700], (330, 134, 2), 147, 7),
            "Giant World"      : self.World(3, 105, False, 39, 3, [101], [0x3f710], (339, 502, 1), 148, 3),
            "Apollo's World"   : self.World(4, 194, False, 55, 1, [102, 103], [0x3f720, 0x3f730], (492, 339, 2), 149, 10),
            "Guardian Base"    : self.World(5, 87, True, 83, 0, [104], [0x3f740], (10, 41, 1), 150, 4),    
            "Monster World"    : self.World(6, 237, False, 99, 1, None, None, None, 151, 2),
            "Venus' World"     : self.World(7, 281, False, 210, 2, [105], [0x3f750], (412, 105, 1), 152, 11),
            "Race World"       : self.World(8, 287, False, 124, 0, [106], [0x3f760], (78, 77, 1), 153, 4),
            "Edo"              : self.World(9, 316, False, 135, 0, [107], [0x3f770], (117, 273, 1), 154, 4),
            "Nasty Dungeon"    : self.World(None, 387, False, 160, 0, [108], [0x3f780], (94, 12, 1), 155, 1),
            "Valhalla Palace"  : self.World(None, 390, False, 162, 1, [109], [0x3f790], (132, 25, 1), 156, 8)
            }

        self.finalStore = {
            "First Town"    :   (1, 7, 6),
            "Second Town"   :   (1, 10, 4),
            "Desert Town"   :   (2, 25, 4),
            "Ashura Town"   :   (2, 28, 4),
            "Giant Town"    :   (3, 42, 4),
            "Port Town"     :   (4, 59, 4),
            "Lynn Town"     :   (4, 67, 4),
            "Guardian Base" :   (5, 85, 4),
            "Monster World" :   (6, 101, 4),
            "Venus World 1" :   (7, 107, 4),
            "Venus World 2" :   (7, 107, 12),
            "Race World"    :   (8, 127, 4),
            "Edo 1"         :   (9, 153, 2),
            "Edo 2"         :   (9, 159, 2)
            }

    class Pillar:
        def __init__(self, order:int, mapPillarID:int, doorInMapIndex:int, doorOut:int, mapPillarTriggerIndexPrism:int, nextPillarVar16Check:int|None):
            self.order = order
            self.mapPillarID = mapPillarID
            self.doorInMapIndex = doorInMapIndex
            self.doorOut = doorOut
            self.mapPillarTriggerIndexPrism = mapPillarTriggerIndexPrism
            self.nextPillarVar16Check = nextPillarVar16Check

    class World:
        def __init__(self, index:int, doorIn:int, isScript:bool, mapID:int, doorOutMapIndex:int, teleportScripts:list|None, 
                     nameAddr:list|None, scriptTeleportUnlockByte:tuple|None, prismScript:int, prismCount:int):
            self.index = index
            self.doorIn = doorIn
            self.isScript = isScript
            self.mapID = mapID
            self.doorOutMapIndex = doorOutMapIndex
            self.teleportScripts = teleportScripts
            self.nameAddr = nameAddr
            self.scriptTeleportUnlockByte = scriptTeleportUnlockByte
            self.prismScript = prismScript
            self.prismCount = prismCount

    def magiCheckRedo(self, scripts:ScriptManager, maps:MapManager, worldType:int):
        #most var16 incs are in the respective rescript events. 
        #repurpose 72/73 to teleport to appropriate guardian world
        maps.remNPC(15,4)
        scripts.replaceScript(0, 24, '00')
        maps.remNPC(39,1)
        scripts.replaceScript(0, 68, '00')
        scripts.insertIntoScriptAtEnd(0, 400, '12 10')
        scripts.insertIntoScriptAtEnd(0, 468, '12 10')
        scripts.insertIntoScriptAtEnd(0, 132, '12 10')
        maps.addNPC(172, 0, '50 0a e0 c1 35 f0')
        maps.remNPC(175, 0)
        scripts.replaceScript(0, 53, '1a 4b 19 00 44 00 19 00 45 00')
        scripts.replaceScript(0, 68, 'ff 36 03 d0 4e 92 8f ff b7 b6 06 36 03 c6 ba c0 79 5d 69 e3 8b 06 36 04 50 5f 83 e2 66 f3 00')
        scripts.replaceScript(0, 69, '14 10 0b 10 06 36 05 c8 e3 8b 8f f3 0b 0d 19 f0 01 ff 00 00')
        scripts.replaceScript(0, 70, 'ff d0 4e e0 8e 54 d6 81 e3 98 7f 06 58 67 69 50 53 5e 66 df d7 e6 06 5d 69 e3 8b 4f 70 52 d7 e2 66 f3 00')
        scripts.replaceScript(0, 72, '00')
        scripts.replaceScript(0, 104, '19 00 5f 14 0e 06 15 06 02 19 05 e5 0e 19 05 ec 00')
        scripts.replaceScript(0, 74, '00')
        scripts.replaceScript(0, 75, '00')
        scripts.replaceScript(0, 76, '00')
        scripts.replaceScript(0, 77, '00')
 
        for v in self.pillar.values():
            if (v.nextPillarVar16Check):
                if worldType != 2:
                    maps.map[v.mapPillarID].npcs[0][1] = v.nextPillarVar16Check
                else:
                    maps.map[v.mapPillarID].npcs[0][1] = 0x00
                maps.map[v.mapPillarID].npcs[0][4] = 0x00
                maps.map[v.mapPillarID].npcs[0][5]+=0x01
 
        maps.map[174].npcs[14] = bytearray.fromhex('4c 04 e0 dc 00 f1')
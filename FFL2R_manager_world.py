from enum import Enum
import mmap
from FFL2R_manager_scripts import ScriptManager
from FFL2R_manager_maps import MapManager

# World here doesn't mean any unique technical data, but rather
# a design. FFL2 has around a dozen or so "Worlds" that use specific
# data. This file exists as a way to manage and edit easily.
class WorldManager:
    def __init__(self):
        self.PRISMADDR = 0x3e600

        self.pillar = {
            "Ashura"   :    self.PillarData(23, (410, 0x4c28), '1e', 2),
            "Giant"    :    self.PillarData(40, (411, 0x4e20), '1f', 3),
            "Apollo"   :    self.PillarData(56, (45, 0x4fdf), '20', 5),
            "Guardian" :    self.PillarData(84, (522, 0x5307), '21', 6),
            "Monster"  :    self.PillarData(100, None, '22', 7),
            "Venus"    :    self.PillarData(103, (523, 0x5593), '23', 8),
            "Race"     :    self.PillarData(125, (524, 0x5949), '24', 25),
            "Edo"      :    self.PillarData(136, (525, 0x5b32), '25', 10),
            "Nasty"    :    self.PillarData(161, (526, 0x5f19), '26', 29),
            "Valhalla" :    self.PillarData(163, (527, 0x5f5e), '27', 28)
        }

        self.world = {
            #index, map ID, teleport scripts, teleport triggers, pillar
            "First World"       :   self.WorldData(1, 1, (0, 273, 89, '1'), None),
            "Ashura's World"    :   self.WorldData(2, 22, (0, 330, 134, '3'), self.pillar["Ashura"]),
            "Giant World"       :   self.WorldData(3, 39, (0, 339, 502, '4'), self.pillar["Giant"]),
            "Apollo's World"    :   self.WorldData(4, 55, (0, 492, 339, '6'), self.pillar["Apollo"]),
            "Guardian Base"     :   self.WorldData(5, 83, (0, 10, 41, '7'), self.pillar["Guardian"]),
            "Monster World"     :   self.WorldData(6, 99, None, self.pillar["Monster"]),
            "Venus' World"      :   self.WorldData(7, 210, (0, 412, 105, '8'), self.pillar["Venus"]),
            "Race World"        :   self.WorldData(8, 124, (0, 78, 77, '9'), self.pillar["Race"]),
            "Edo"               :   self.WorldData(9, 135, (3, 245, 273, 'a'), self.pillar["Edo"]),
            "Nasty Dungeon"     :   self.WorldData(10, 160, (0, 94, 12, 'b'), self.pillar["Nasty"]),
            "Valhalla"          :   self.WorldData(11, 162, (0, 132, 25, 'c'), self.pillar["Valhalla"])
        }

        self.finalStore = {
            '01 cf 18 1e 14 44'     :   [(7, 6)],
            '01 cf 18 1e 14 34'     :   [(10, 4)],
            '02 5f 18 1e 14 34'     :   [(25, 4), (28, 4)],
            '03 5f 18 1e 14 34'     :   [(42, 4)],
            '05 5f 18 1e 14 34'     :   [(59, 4), (67, 4)],
            '06 8f 1d 07 14 24'     :   [(85, 4)],
            '07 7f 18 1e 14 34'     :   [(101, 4)],
            '08 af 07 07 14 54'     :   [(107, 4)],
            '08 af 20 08 14 54'     :   [(107, 12)],
            '19 6f 18 1e 14 34'     :   [(127, 4)],
            '0a 4f 04 08 14 44'     :   [(153, 2)],
            '0a 4f 04 08 14 34'     :   [(159, 2)]
            }

        #key: script, value: memoscript
        self.gameEvents = {
           25  : '14',  #"Ashura Base Collapse"  
           333 : '15',  #"Ashura's Death"        
           37  : '16',  #"Ki's Body All Magi"    
           86  : '17',  #"Apollo's World Check"   cannot be insert into end, must be [6] directly
           400 : '18',  #"Last Monster Guardian" 
           244 : '19',  #"Dad Death"            
           241 : '1a',  #"Venus Death"           
           80  : '1b',  #"Finished Race"         
           468 : '1c',  #"Magnate Death"         
           94  : '1d',  #"Nasty Cave"            
           132 : None   #"Odin Death"            
        }

        self.locations = {
            "Opening Cutscene"                                      : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 1, 172], self.PrismIndex.FIRST_WORLD),
            "Char 2's Parent"                                       : self.Location(self.LocationType.SCRIPT_ITEM_SPECIAL, [0, 275, 39], self.PrismIndex.FIRST_WORLD),
            "First Cave, First Platform, Left"                      : self.Location(self.LocationType.NPC_ITEM, [5, 2], self.PrismIndex.FIRST_WORLD),
            "First Cave, First Platform, Right"                     : self.Location(self.LocationType.NPC_ITEM, [5, 3], self.PrismIndex.FIRST_WORLD),
            "First Cave, Near Exit, North"                          : self.Location(self.LocationType.NPC_ITEM, [5, 4], self.PrismIndex.FIRST_WORLD),
            "First Cave, Near Exit, South"                          : self.Location(self.LocationType.NPC_ITEM, [5, 5], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 2"                    : self.Location(self.LocationType.NPC_ITEM, [13, 0], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Northwest"         : self.Location(self.LocationType.NPC_ITEM, [14, 0], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Southwest"         : self.Location(self.LocationType.NPC_ITEM, [14, 1], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Northeast"         : self.Location(self.LocationType.NPC_ITEM, [14, 2], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 3, Southeast"         : self.Location(self.LocationType.NPC_ITEM, [14, 3], self.PrismIndex.FIRST_WORLD),
            #the npc removal happens after, uses original npc counts
            "Ruins of the Ancient Gods, Floor 4, Main North"        : self.Location(self.LocationType.EMPTY, [15, 5], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Main West"         : self.Location(self.LocationType.EMPTY, [15, 6], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Main East"         : self.Location(self.LocationType.EMPTY, [15, 7], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Vault Northeast"   : self.Location(self.LocationType.NPC_MAGI, [15, 8], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Vault Southeast"   : self.Location(self.LocationType.NPC_MAGI, [15, 9], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, Vault West"        : self.Location(self.LocationType.NPC_MAGI, [15, 10], self.PrismIndex.FIRST_WORLD),
            "Ruins of the Ancient Gods, Floor 4, North of Entrance" : self.Location(self.LocationType.NPC_ITEM, [15, 11], self.PrismIndex.FIRST_WORLD),
            #Ashura's Base, Wanderers
            "Ashura's Base, Floor 3"                                : self.Location(self.LocationType.NPC_ITEM, [18, 4], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Floor 4"                                : self.Location(self.LocationType.NPC_ITEM, [19, 4], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Floor 5"                                : self.Location(self.LocationType.NPC_ITEM, [20, 0], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Exit Southeast"                         : self.Location(self.LocationType.NPC_MAGI, [20, 5], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Exit Northeast"                         : self.Location(self.LocationType.NPC_MAGI, [20, 6], self.PrismIndex.FIRST_WORLD),
            "Ashura's Base, Exit West"                              : self.Location(self.LocationType.NPC_MAGI, [20, 7], self.PrismIndex.FIRST_WORLD),
            "Ashura's Tower, Floor 4"                               : self.Location(self.LocationType.NPC_ITEM, [32, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Floor 7"                               : self.Location(self.LocationType.NPC_ITEM, [35, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Floor 9"                               : self.Location(self.LocationType.NPC_ITEM, [37, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Southwest"              : self.Location(self.LocationType.NPC_ITEM, [38, 4], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Southeast"              : self.Location(self.LocationType.NPC_ITEM, [38, 5], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Northwest"              : self.Location(self.LocationType.NPC_ITEM, [38, 6], self.PrismIndex.ASHURA_WORLD),
            "Ashura's Tower, Ashura's Floor Northeast"              : self.Location(self.LocationType.NPC_ITEM, [38, 7], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 1"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 0], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 2"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 3], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 3"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 6], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 4"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 9], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 5"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 12], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 6"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 15], self.PrismIndex.ASHURA_WORLD),
            "Ashura Drop 7"                                         : self.Location(self.LocationType.SCRIPT_MAGI, [0, 192, 18], self.PrismIndex.ASHURA_WORLD),
            "Dad in Giant's World"                                  : self.Location(self.LocationType.SCRIPT_MAGI, [0, 339, 303], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Magi House North"                          : self.Location(self.LocationType.NPC_MAGI, [45, 0], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Magi House South"                          : self.Location(self.LocationType.NPC_MAGI, [45, 1], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Micron House West"                         : self.Location(self.LocationType.NPC_ITEM, [46, 0], self.PrismIndex.GIANT_WORLD),
            "Giant Town, Micron House East"                         : self.Location(self.LocationType.NPC_ITEM, [46, 1], self.PrismIndex.GIANT_WORLD),
            #"Giant Town, Micron Potion Location"                    : self.Location(self.LocationType.SCRIPT_ITEM_FORCED, [0, 29, 11], self.PrismIndex.GIANT_WORLD),
            "Ki's Assistant"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 308, 34], self.PrismIndex.FIRST_WORLD_RETURN),
            "Ki's Stomach"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 31, 0], self.PrismIndex.KIS_BODY),
            "Ki's Heart"                                            : self.Location(self.LocationType.SCRIPT_MAGI, [0, 32, 0], self.PrismIndex.KIS_BODY),
            "Ki's Left Hand"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 33, 0], self.PrismIndex.KIS_BODY),
            "Ki's Right Hand"                                       : self.Location(self.LocationType.SCRIPT_MAGI, [0, 34, 0], self.PrismIndex.KIS_BODY),
            "Ki's Left Foot"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 35, 0], self.PrismIndex.KIS_BODY),
            "Ki's Right Foot"                                       : self.Location(self.LocationType.SCRIPT_MAGI, [0, 36, 0], self.PrismIndex.KIS_BODY),
            "Ki's Brain"                                            : self.Location(self.LocationType.SCRIPT_MAGI, [0, 37, 0], self.PrismIndex.KIS_BODY),
            "Meeting Apollo"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 350, 76], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Floor 3 West"                        : self.Location(self.LocationType.NPC_ITEM, [63, 0], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Floor 3 East"                        : self.Location(self.LocationType.NPC_ITEM, [63, 1], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Floor 4"                             : self.Location(self.LocationType.NPC_ITEM, [64, 1], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Exit West"                           : self.Location(self.LocationType.NPC_MAGI, [65, 0], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Exit East"                           : self.Location(self.LocationType.NPC_MAGI, [65, 1], self.PrismIndex.APOLLOS_WORLD),
            "Undersea Volcano, Exit TrueEye"                        : self.Location(self.LocationType.NPC_MAGI_SPECIAL, [65, 2], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Cave, Entrance"                                : self.Location(self.LocationType.NPC_ITEM, [70, 0], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Cave, Floor 3"                                 : self.Location(self.LocationType.NPC_ITEM, [72, 0], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Cave, Dunatis Floor"                           : self.Location(self.LocationType.NPC_ITEM, [74, 2], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 3"                                : self.Location(self.LocationType.NPC_ITEM, [78, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 4 West"                           : self.Location(self.LocationType.NPC_ITEM, [79, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 4 East"                           : self.Location(self.LocationType.NPC_ITEM, [79, 1], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 5"                                : self.Location(self.LocationType.NPC_ITEM, [80, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Floor 6"                                : self.Location(self.LocationType.NPC_ITEM, [81, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Final Floor North"                      : self.Location(self.LocationType.NPC_MAGI, [82, 0], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Final Floor East"                       : self.Location(self.LocationType.NPC_MAGI, [82, 1], self.PrismIndex.APOLLOS_WORLD),
            "Cave of Light, Final Floor West"                       : self.Location(self.LocationType.NPC_MAGI, [82, 2], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 1"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 492, 59], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 2"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 492, 62], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 3"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 492, 65], self.PrismIndex.APOLLOS_WORLD),
            "Dunatis Drop 4"                                        : self.Location(self.LocationType.SCRIPT_ITEM, [0, 492, 68], self.PrismIndex.APOLLOS_WORLD),
            "Guardian Base Storage, North-center"                   : self.Location(self.LocationType.EMPTY, [97, 0], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, Northwest"                      : self.Location(self.LocationType.EMPTY, [97, 1], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, Center"                         : self.Location(self.LocationType.EMPTY, [97, 2], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, Northeast"                      : self.Location(self.LocationType.EMPTY, [97, 3], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Storage, South"                          : self.Location(self.LocationType.EMPTY, [97, 4], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Commando"                                : self.Location(self.LocationType.SCRIPT_MAGI, [0, 400, 59], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Magician"                                : self.Location(self.LocationType.SCRIPT_MAGI, [0, 401, 7], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Manticore"                               : self.Location(self.LocationType.SCRIPT_MAGI, [0, 402, 7], self.PrismIndex.GUARDIAN_WORLD),
            "Guardian Base Ogre"                                    : self.Location(self.LocationType.SCRIPT_MAGI, [0, 404, 7], self.PrismIndex.GUARDIAN_WORLD),
            "Dad's Death, Final Gift"                               : self.Location(self.LocationType.SCRIPT_MAGI, [3, 244, 282], self.PrismIndex.MONSTER_WORLD),
            "Dad's Death, Ninja"                                    : self.Location(self.LocationType.SCRIPT_MAGI, [3, 244, 745], self.PrismIndex.MONSTER_WORLD),
            "Dad's Death, Lynn's Mom"                               : self.Location(self.LocationType.SCRIPT_MAGI, [3, 244, 1185], self.PrismIndex.APOLLOS_WORLD_RETURN),
            "Sewer, Entrance"                                       : self.Location(self.LocationType.NPC_ITEM, [110, 0], self.PrismIndex.VENUS_WORLD),
            #"Hermit Crab Drop"                                      : self.Location(self.LocationType.SCRIPT_ITEM, [0, 438, 14], self.PrismIndex.VENUS_WORLD),
            "Sewer, Floor 2"                                        : self.Location(self.LocationType.NPC_ITEM, [111, 0], self.PrismIndex.VENUS_WORLD),
            "Sewer, Floor 5 West"                                   : self.Location(self.LocationType.NPC_ITEM, [114, 0], self.PrismIndex.VENUS_WORLD),
            "Sewer, Floor 5 East"                                   : self.Location(self.LocationType.NPC_ITEM, [114, 1], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 1, Northwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 0], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 1, Southwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 1], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 1, Northeast"                       : self.Location(self.LocationType.NPC_MAGI, [116, 2], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 2, Northwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 4], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 2, Northeast"                       : self.Location(self.LocationType.NPC_MAGI, [116, 5], self.PrismIndex.VENUS_WORLD),
            "Sewer, Locked Room 2, Southwest"                       : self.Location(self.LocationType.NPC_MAGI, [116, 6], self.PrismIndex.VENUS_WORLD),
            #Sewer, Monster-in-a-box
            "Venus Volcano, Floor 5, Lava"                          : self.Location(self.LocationType.NPC_ITEM, [121, 1], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Floor 5, Land"                          : self.Location(self.LocationType.NPC_ITEM, [121, 2], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Floor 6, West"                          : self.Location(self.LocationType.NPC_ITEM, [122, 1], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Floor 6, East"                          : self.Location(self.LocationType.NPC_ITEM, [122, 2], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Exit, Isolated"                         : self.Location(self.LocationType.NPC_ITEM, [123, 4], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Exit, West"                             : self.Location(self.LocationType.NPC_MAGI,[123, 1], self.PrismIndex.VENUS_WORLD),
            "Venus Volcano, Exit, East"                             : self.Location(self.LocationType.NPC_MAGI,[123, 2], self.PrismIndex.VENUS_WORLD),
            "Leon's Theft"                                          : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 420, 28], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 1"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 0], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 2"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 3], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 3"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 6], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 4"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 9], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 5"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 12], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 6"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 15], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 7"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 193, 18], self.PrismIndex.VENUS_WORLD),
            "Venus Drop 8"                                          : self.Location(self.LocationType.SCRIPT_MAGI, [0, 43, 106], self.PrismIndex.VENUS_WORLD),
            "Race - Adamant"                                        : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 457, 36], self.PrismIndex.RACE_WORLD),
            "Race - Tortoise"                                       : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 458, 36], self.PrismIndex.RACE_WORLD),
            "Race - Lamia"                                          : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 459, 36], self.PrismIndex.RACE_WORLD),
            "Race - Watcher"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 460, 24], self.PrismIndex.RACE_WORLD),
            "Race - Watcher (Lamia)"                                : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 460, 30], self.PrismIndex.RACE_WORLD),
            "Race - Watcher (Tortoise)"                             : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 460, 37], self.PrismIndex.RACE_WORLD),
            "Race - Watcher (Adamant)"                              : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 460, 44], self.PrismIndex.RACE_WORLD),
            "Edo Castle, Floor 3, Center"                           : self.Location(self.LocationType.NPC_ITEM, [142, 0], self.PrismIndex.EDO),
            "Edo Castle, Floor 3, West"                             : self.Location(self.LocationType.NPC_ITEM, [142, 1], self.PrismIndex.EDO),
            "Edo Castle, Floor 3, East"                             : self.Location(self.LocationType.NPC_ITEM, [142, 2], self.PrismIndex.EDO),
            "Edo Castle, Floor 4"                                   : self.Location(self.LocationType.NPC_ITEM, [143, 0], self.PrismIndex.EDO),
            "Edo Castle, Floor 5"                                   : self.Location(self.LocationType.NPC_ITEM, [144, 0], self.PrismIndex.EDO),
            "Edo Castle, Shogun Floor"                              : self.Location(self.LocationType.NPC_ITEM, [145, 5], self.PrismIndex.EDO),
            "Banana Smuggling Boat, Middle Deck"                    : self.Location(self.LocationType.NPC_ITEM, [150, 0], self.PrismIndex.EDO),
            "Banana Smuggling Boat, Lower Deck, West"               : self.Location(self.LocationType.NPC_ITEM, [151, 2], self.PrismIndex.EDO),
            "Banana Smuggling Boat, Lower Deck, East"               : self.Location(self.LocationType.NPC_ITEM, [151, 3], self.PrismIndex.EDO),
            #Edo, Hatamotos
            "Magnate Drop 1"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 103], self.PrismIndex.EDO),
            "Magnate Drop 2"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 106], self.PrismIndex.EDO),
            "Magnate Drop 3"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 109], self.PrismIndex.EDO),
            "Magnate Drop 4"                                        : self.Location(self.LocationType.SCRIPT_MAGI, [0, 468, 112], self.PrismIndex.EDO),
            "Nasty Dungeon, Entrance, MAGI Chest"                   : self.Location(self.LocationType.SCRIPT_MAGI, [0, 94, 9], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 1"                      : self.Location(self.LocationType.NPC_ITEM, [202, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 2"                      : self.Location(self.LocationType.NPC_ITEM, [202, 4], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 3"                      : self.Location(self.LocationType.NPC_ITEM, [202, 5], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Entrance, Chest 4"                      : self.Location(self.LocationType.NPC_ITEM, [202, 6], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [203, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [203, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [203, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 2, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [203, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [204, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [204, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [204, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 3, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [204, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [205, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [205, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [205, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 4, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [205, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [206, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [206, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [206, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [206, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 5, Chest 5"                       : self.Location(self.LocationType.NPC_ITEM, [206, 4], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [207, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [207, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [207, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 6, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [207, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 1"                       : self.Location(self.LocationType.NPC_ITEM, [208, 0], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 2"                       : self.Location(self.LocationType.NPC_ITEM, [208, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 3"                       : self.Location(self.LocationType.NPC_ITEM, [208, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Floor 7, Chest 4"                       : self.Location(self.LocationType.NPC_ITEM, [208, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 1"                          : self.Location(self.LocationType.NPC_ITEM, [209, 1], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 2"                          : self.Location(self.LocationType.NPC_ITEM, [209, 2], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 3"                          : self.Location(self.LocationType.NPC_ITEM, [209, 3], self.PrismIndex.NASTY_DUNGEON),
            "Nasty Dungeon, Exit, Chest 4"                          : self.Location(self.LocationType.NPC_ITEM, [209, 4], self.PrismIndex.NASTY_DUNGEON),
            "Vahalla, Entrance"                                     : self.Location(self.LocationType.NPC_ITEM, [164, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 2"                                      : self.Location(self.LocationType.NPC_ITEM, [165, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 4"                                      : self.Location(self.LocationType.NPC_ITEM, [167, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 5"                                      : self.Location(self.LocationType.NPC_ITEM, [168, 0], self.PrismIndex.VALHALLA),
            "Vahalla, Floor 6"                                      : self.Location(self.LocationType.NPC_ITEM, [169, 0], self.PrismIndex.VALHALLA),
            "Odin Drop 1"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 0], self.PrismIndex.VALHALLA),
            "Odin Drop 2"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 3], self.PrismIndex.VALHALLA),
            "Odin Drop 3"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 6], self.PrismIndex.VALHALLA),
            "Odin Drop 4"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 9], self.PrismIndex.VALHALLA),
            "Odin Drop 5"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 12], self.PrismIndex.VALHALLA),
            "Odin Drop 6"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 15], self.PrismIndex.VALHALLA),
            "Odin Drop 7"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 14, 18], self.PrismIndex.VALHALLA),
            "Odin Drop 8"                                           : self.Location(self.LocationType.SCRIPT_MAGI, [0, 132, 15], self.PrismIndex.VALHALLA),
            "Final Dungeon, Entrance"                               : self.Location(self.LocationType.NPC_ITEM, [177, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 2"                                : self.Location(self.LocationType.NPC_ITEM, [178, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 4"                                : self.Location(self.LocationType.NPC_ITEM, [180, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 5"                                : self.Location(self.LocationType.NPC_ITEM, [181, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 6"                                : self.Location(self.LocationType.NPC_ITEM, [182, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 7"                                : self.Location(self.LocationType.NPC_ITEM, [183, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 9"                                : self.Location(self.LocationType.NPC_ITEM, [185, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, Floor 10"                               : self.Location(self.LocationType.NPC_ITEM, [186, 0], self.PrismIndex.FINAL_WORLD),
            "Final Dungeon, WarMach Chest"                          : self.Location(self.LocationType.SCRIPT_MAGI_SPECIAL, [0, 71, 7], self.PrismIndex.FINAL_WORLD)
            #"Central Pillar, Tian-Lung drop"                          :
            #"Central Pillar, Fenrir drop"                             :
            }
    
    class WorldData:
        #WEB ERRORS PASSING IN TYPE CLASS WITH PILLAR WHY
        def __init__(self, index:int, mapID:int, teleportTriggers:tuple|None, pillar):
            self.index = index
            self.mapID = mapID
            self.teleportTriggers = teleportTriggers
            self.pillar = pillar

    class PillarData:
        def __init__(self, mapID:int, newDoor:tuple|None, memoCall:int, worldVar:int):
            self.mapID = mapID
            self.newDoor = newDoor
            self.memoCall = memoCall
            self.worldVar = worldVar

    class Location:
        def __init__(self, lType:Enum, data:list, pType:Enum):
            self.lType = lType
            self.data = data
            self.pType = pType

    class LocationType(Enum):
        EMPTY = 0
        NPC_ITEM = 1
        NPC_ITEM_SPECIAL = 2
        NPC_MAGI = 3
        NPC_MAGI_SPECIAL = 4
        SCRIPT_ITEM = 5
        SCRIPT_ITEM_SPECIAL = 6
        SCRIPT_MAGI = 7
        SCRIPT_MAGI_SPECIAL = 8

    class PrismIndex(Enum):
        FIRST_WORLD = 0
        ASHURA_WORLD = 1
        FIRST_WORLD_RETURN = 2
        GIANT_WORLD = 3
        KIS_BODY = 4
        APOLLOS_WORLD = 5
        GUARDIAN_WORLD = 6
        MONSTER_WORLD = 7
        APOLLOS_WORLD_RETURN = 8
        VENUS_WORLD = 9
        RACE_WORLD = 10
        EDO = 11
        NASTY_DUNGEON = 12
        VALHALLA = 13
        FINAL_WORLD = 14

    def worldBuilder(self, scripts:ScriptManager, maps:MapManager, worldType:int, worldOrder:dict):
        maps.remNPC(15,4)
        scripts.replaceScript(0, 24, '00')
        maps.remNPC(39,1)
        maps.addNPC(172, 0, '4c 02 e0 c1 35 f0') #Valhalla right pillar
        maps.remNPC(175, 0) #final world map
        scripts.replaceScript(0, 53, '1a 4b 19 00 44 00 19 00 45 00')
        scripts.replaceScript(0, 68, 'ff 36 03 d0 4e 92 8f ff b7 b6 06 36 03 c6 ba c0 79 5d 69 e3 8b 06 36 04 50 5f 83 e2 66 f3 00')
        scripts.replaceScript(0, 69, '10 06 36 05 c8 e3 8b 8f f3 0b 0d 19 f0 01 ff 00 00')
        scripts.replaceScript(0, 70, 'ff d0 4e e0 8e 54 d6 81 e3 98 7f 06 58 67 69 50 53 5e 66 df d7 e6 06 5d 69 e3 8b 4f 70 52 d7 e2 66 f3 00')
        scripts.replaceScript(0, 72, '00')
        scripts.replaceScript(0, 73, '00')
        scripts.replaceScript(0, 74, '00')
        scripts.replaceScript(0, 75, '00')
        scripts.replaceScript(0, 76, '00')
        scripts.replaceScript(0, 77, '00')

        scripts.removeFromScript(0, 142, 307, 310)
        if worldType != 3:
            scripts.insertIntoScriptAtEnd(0, 1, '14 02 0f 14 03 0f 14 05 0f 14 06 0f 14 07 0f 14 08 0f 14 19 0f 14 0a 0f 14 1d 0f 14 1c 0f')
            #14 18 0d to add var24 at end, different function
 
        maps.map[174].npcs[14] = bytearray.fromhex('4c 04 e0 dc 00 f1')

        # #world keys, placed in memo
        scripts.replaceScript(3, 20,'0d 19 07 a2 14 02 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c ba 93 7d d4 77 ff d0 66 df d7 f3 0b 0d 00')
        scripts.replaceScript(3, 21,'0d 19 07 a2 14 03 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c c0 dc 59 e7 77 ff d0 66 df d7 f3 0b 0d 00')
        scripts.replaceScript(3, 22,'0d 19 07 a2 14 05 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c ba e3 e2 67 e2 77 ff d0 66 df d7 f3 0b 0d 00')
        scripts.replaceScript(3, 23,'0d 19 07 a2 14 06 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c c0 e8 6e d7 dc 59 77 ff bb 89 d8 f3 0b 0d 00')
        scripts.replaceScript(3, 24,'0d 19 07 a2 14 07 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c c6 65 78 53 ff d0 66 df d7 f3 0b 0d 00')
        scripts.replaceScript(3, 25,'0d 19 07 a2 14 08 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c cf 8b 8e ee ff d0 66 df d7 f3 0b 0d 00')
        scripts.replaceScript(3, 26,'0d 19 07 a2 14 19 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c cb d4 d6 4e d0 66 df d7 f3 0b 0d 00')
        scripts.replaceScript(3, 27,'0d 19 07 a2 14 0a 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c be d7 e2 f3 0b 0d 00')
        scripts.replaceScript(3, 28,'0d 19 07 a2 14 1d 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c c7 89 e7 72 bd e8 6b d8 65 f3 0b 0d 00')
        scripts.replaceScript(3, 29,'0d 19 07 a2 14 1c 00 05 cb d8 d6 d8 dc 76 57 20 06 07 9c cf d4 df 6a 67 7b c9 d4 df d4 d6 d8 f3 0b 0d 00')

        scripts.addNewScript(0, 'd2 55 7a 7d 5a 94 df 72 d7 5b 06 88 54 e3 e2 e6 80 e6 52 50 4e 05 ff 05 07 9c 4f 5b 8b 7f e5 f0 00')
        for v in self.pillar.values():
            scripts.addNewScript(0, '4b' + v.memoCall + '40' + v.memoCall + '00')
        scripts.replaceScript(3, 30, '99 5f 5c 52 ba 93 7d d4 77 ff 06 d0 66 df d7 f0 06 15 02 ff 19 00 c7 31 00')
        scripts.replaceScript(3, 31, '99 5f 5c 52 c0 dc 59 e7 77 ff 06 d0 66 df d7 f0 06 15 03 ff 19 00 c7 31 00')
        scripts.replaceScript(3, 32, '99 5f 5c 52 ba e3 e2 67 e2 77 ff 06 d0 66 df d7 f0 06 15 05 ff 19 00 c7 31 00')
        scripts.replaceScript(3, 33, '99 5f 5c 52 06 c0 e8 6e d7 dc 59 77 ff bb 89 d8 f0 06 15 06 ff 19 00 c7 31 00')
        scripts.replaceScript(3, 34, '99 5f 5c 52 c6 65 78 53 ff 06 d0 66 df d7 f0 06 15 07 ff 19 00 c7 31 00')
        scripts.replaceScript(3, 35, '99 5f 5c 52 cf 8b 8e ee 06 d0 66 df d7 f0 06 15 08 ff 19 00 c7 31 00')
        scripts.replaceScript(3, 36, '99 5f 5c 52 cb d4 d6 d8 06 d0 66 df d7 f0 06 15 19 ff 19 00 c7 31 00')
        scripts.replaceScript(3, 37, '99 5f 5c 52 be d7 e2 f0 06 15 0a ff 19 00 c7 31 00')
        scripts.replaceScript(3, 38, '99 5f 5c 52 c7 89 e7 72 06 bd e8 6b d8 65 f0 06 15 1d ff 19 00 c7 31 00')
        scripts.replaceScript(3, 39, '99 5f 5c 52 cf d4 df 6a 67 d4 06 c9 d4 df d4 d6 d8 f0 06 15 1c ff 19 00 c7 31 00')

        scripts.replaceScript(0, 99, '19 00 5f 15 02 ff 19 06 9a 00 19 0e 13 14 0e 01 00')
        scripts.replaceScript(0, 100, '19 00 5f 15 02 ff 19 06 9a 00 19 0e 14 14 0e 01 00')
        scripts.replaceScript(0, 101, '19 00 5f 15 03 ff 19 06 9b 00 19 0e 15 14 0e 03 00')
        scripts.replaceScript(0, 102, '19 00 5f 15 05 ff 19 05 2d 00 19 0e 16 15 04 06 14 0e 05 00 14 0e 08 00')
        scripts.replaceScript(0, 103, '19 00 5f 15 05 ff 19 05 2d 00 19 0e 17 15 04 06 14 0e 05 00 14 0e 08 00')
        scripts.replaceScript(0, 104, '19 00 5f 15 06 ff 19 0e 0a 00 14 0e 06 15 06 02 19 05 e5 00 19 05 ec 00')
        scripts.replaceScript(0, 105, '19 00 5f 15 08 ff 19 0e 0b 00 19 0e 19 14 0e 09 00')
        scripts.replaceScript(0, 106, '19 00 5f 15 19 ff 19 0e 0c 00 19 0e 1a 14 0e 0a 00')
        scripts.replaceScript(0, 107, '19 00 5f 15 0a ff 19 0e 0d 00 19 0e 1b 14 0e 0b 00')
        scripts.replaceScript(0, 108, '19 00 5f 15 1d ff 19 0e 0e 00 19 0e 1c 14 0e 0c 00')
        scripts.replaceScript(0, 109, '19 00 5f 15 0d ff 19 0e 0f 00 19 0e 1d 14 0e 0d 00')

        #figure out why only one door fucks up when using only one for loop later
        for v in self.world.values():
            if v.pillar:
                if maps.map[v.pillar.mapID].npcs:
                    maps.map[v.pillar.mapID].npcs[0] = bytearray.fromhex('40 ff e0 c6 00 f1')
                else:
                    maps.addNPC(v.pillar.mapID, 0x00,'40 ff e0 c6 00 f1')
                maps.addNPC(v.pillar.mapID, 0x3c, '00 0f df 85 c6 90')
                maps.map[v.pillar.mapID].npcs[0][0] += v.pillar.worldVar
                maps.map[v.pillar.mapID].npcs[1][4] += v.index
        for v in self.world.values():
            if v.pillar:
                if v.pillar.newDoor:
                    maps.door[v.pillar.newDoor[0]].addr = v.pillar.newDoor[1]
                    maps.door[v.pillar.newDoor[0]].map = v.mapID
                    maps.door[v.pillar.newDoor[0]].x = 32
                    maps.door[v.pillar.newDoor[0]].y = 5
                    maps.door[v.pillar.newDoor[0]].dirEnum = 2
            if v.teleportTriggers:
                scripts.insertIntoScript(v.teleportTriggers[0], v.teleportTriggers[1], v.teleportTriggers[2], ('15180' + str(v.teleportTriggers[3])))
                scripts.insertIntoScript(v.teleportTriggers[0], v.teleportTriggers[1], v.teleportTriggers[2]+6, '31')

        print(worldOrder)
        for k,v in worldOrder.items():
            if v:
                memo = '4b' + v + '40' + v
                match k:
                    case 241:
                        scripts.insertIntoScriptAtEnd(3, k, memo)
                    case 244:
                        scripts.insertIntoScriptAtEnd(3, k, memo)
                    case 25:
                        scripts.insertIntoScript(0, 25, 73, memo)
                    case _:
                        scripts.insertIntoScriptAtEnd(0, k, memo)

        for k,v in self.finalStore.items():
            if k != '06 8f 1d 07 14 24': #we're gonna move Guardian Base Final Store to outside map 90
                for _ in v:
                    maps.map[_[0]].npcs[_[1]] = bytearray.fromhex(k)
            else:
                maps.addNPC(90, 28, k)
                maps.remNPC(85, 4)

    def getPrismCounts(self, rom:mmap)->list:
        magiCounts = []
        for x in range (0,16):
            magiCounts.append(rom[self.PRISMADDR+x])
        return magiCounts


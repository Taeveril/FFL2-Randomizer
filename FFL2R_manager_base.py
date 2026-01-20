import mmap
from FFL2R_manager_scripts import ScriptManager
from FFL2R_manager_maps import MapManager
from FFL2R_data import GameData
from FFL2R import VERSION

class ScriptedFixes:
    def __init__(self):
        pass

    def moveMrS(scripts:ScriptManager, maps:MapManager):
        #MrS blocks the first cave exit due to some poor scripting. Fixing the scripting lets us move MrS out of the way. 
        scripts.insertIntoScript(0, 19, 0, '15 01 1f 19 05 16 0e')
        maps.map[4].npcs[0][0] = 0x01
        maps.map[5].npcs[1] = bytearray.fromhex('01 2F EF 0a 18 A1')

    def fixTheRace(scripts:ScriptManager, maps:MapManager):
        #Puts a dismount on the teleport scripts. Also changes var usage around to be cleaner.
        scripts.replaceScript(0, 55, '33 e8 03 19 f0 08 19 00 4e 00')
        scripts.replaceScript(0, 56, '33 20 03 19 f0 09 19 00 4e 00')
        scripts.replaceScript(0, 57, '33 58 02 19 f0 0a 19 00 4e 00')
        scripts.replaceScript(0, 58, '19 f0 0b 19 00 4e 00')
        scripts.replaceScript(0, 59, '15 19 01 19 01 c7 00 19 01 c8 00')
        scripts.replaceScript(0, 78, """0d 19 06 2d 19 07 00 cb 75 d7 ec f1 f1 06 c0 85 63 85 f1 f1 0b 0d 12 11 10 19 f1 53 ff 36 06 19 07 a8 c0 c8 f3 19 f6 53 
                                     00 f6 53 01 f6 53 02 ff 0d 13 11 10 c8 e2 e2 e2 e3 e6 f3 06 bf d8 67 58 74 87 74 d8 70 7c f3 11 10 0d 19 07 0b 14 18 0a
                                     15 19 00 14 19 01 31 00""")
        scripts.replaceScript(0, 80, """15 1f 00 19 01 db 00 19 f1 30 ff 19 07 03 c0 c8 ba c5 f3 f3 06 99 4e ea 56 92 68 5f 06 20 1f 00 77 ff cd 75 e0 f3 0b 0d 
                                     19 f0 05 bc 65 da 82 e7 e8 df 60 dc 65 e6 f3 0b 0d 14 12 00 14 19 06 19 06 3a 19 07 0c 12 10 00""")
        scripts.replaceScript(0, 95, '15 11 02 19 00 5d 31 14 0f 03 19 f0 10 19 07 8b 19 07 0c 00')
        scripts.replaceScript(0, 449, '4b 55 f3 00')
        scripts.replaceScript(0, 457, """15 1f 00 19 01 db 00 15 19 2f 19 06 37 00 15 1f 2f 19 06 37 00 12 11 10 11 10 09 06 13 11 12 12 14 19 02 10 19 0a 01 0d 
                                      19 06 37 00""")
        scripts.replaceScript(0, 458, """15 1f 00 19 01 db 00 15 19 3f 19 06 38 00 15 1f 3f 19 06 38 00 12 11 10 11 10 09 37 13 11 12 12 14 19 03 10 19 0a 02 0d 
                                      19 06 38 00""")
        scripts.replaceScript(0, 459, """15 1f 00 19 01 db 00 15 19 4f 19 06 39 00 15 1f 4f 19 06 39 00 12 11 10 11 10 09 07 13 11 12 12 14 19 04 10 19 0a 05 0d 
                                      19 06 39 00""")
        scripts.replaceScript(0, 460, """15 1f 00 19 01 db 00 15 19 5f 19 00 00 00 12 11 10 11 10 09 87 13 11 10 19 0a 06 15 12 02 19 0a 01 31 15 12 01 19 0a 02 
                                      31 15 12 00 19 0a 05 31 14 19 05 00""")
        scripts.replaceScript(0, 461, '19 01 ed 15 1f 3f 19 01 ee 00 00')
        scripts.replaceScript(0, 462, '19 01 ed 15 1f 4f 19 01 ee 00 00')
        scripts.replaceScript(0, 463, '00')
        maps.map[129].npcs[1] = bytearray.fromhex('19 6f 05 8a 8f a1')
        maps.map[129].npcs[2] = bytearray.fromhex('19 01 05 8a c2 a1')
        maps.map[129].npcs[4] = bytearray.fromhex('19 6f 0d 8a 8f b1')
        maps.map[129].npcs[5] = bytearray.fromhex('19 02 0d 8a c3 b1')
        maps.map[129].npcs[7] = bytearray.fromhex('19 6f 15 0a 8f c1')
        maps.map[129].npcs[8] = bytearray.fromhex('19 03 15 0a c4 c1')
        maps.map[129].npcs[10] = bytearray.fromhex('19 6f 1d 0a 8f d1')
        maps.map[129].npcs[11] = bytearray.fromhex('19 05 1d 0a c5 d1')
        maps.map[130].npcs[0] = bytearray.fromhex('12 00 8c 41 3b 90')
        maps.map[130].npcs[1] = bytearray.fromhex('12 00 0c c2 3b 90')
        maps.map[130].npcs[2] = bytearray.fromhex('12 00 4c c3 3b 90')
        maps.map[131].npcs[3] = bytearray.fromhex('11 11 ba 23 c9 a1')
        maps.map[132].npcs[0] = bytearray.fromhex('5f 2f af 47 00 90')
        maps.map[132].npcs[1] = bytearray.fromhex('5f 2f 2e c7 cd a1')
        maps.map[132].npcs[2] = bytearray.fromhex('11 11 2d 05 ca b1')
        maps.map[133].npcs[0] = bytearray.fromhex('5f 3f 47 57 00 90')
        maps.map[133].npcs[1] = bytearray.fromhex('5f 3f 07 d6 ce a1')
        maps.map[133].npcs[2] = bytearray.fromhex('11 11 c5 15 cb b1')
        maps.map[134].npcs[0] = bytearray.fromhex('5f 4f d6 56 00 90')
        maps.map[134].npcs[1] = bytearray.fromhex('5f 4f 17 d5 ed a1')
        maps.map[134].npcs[2] = bytearray.fromhex('11 11 99 14 cc b1')

class ScriptedQOL:
    def __init__(self):
        pass

    def newNPCHelpers(scripts:ScriptManager, maps:MapManager):
        #echigoya's new clerk
        maps.addNPC(154, 60, '09 BF 22 23 16 C4')
        #ashura's base guardian
        maps.addNPC(1, 66, '01 DF 1F 05 C3 A0')
        scripts.addNewScript(0, 'bd 5b 6d 9a 92 8f 4f 5b da 85 63 81 85 70 6b 69 86 69 d9 ff ba 93 7d d4 77 ff bb 89 d8 f4 16 19 05 33 31 0d 00')
        scripts.removeFromScript(0, 25, 0, 6)
        scripts.insertIntoScript(0, 25, 0, '12 10 15 01 bf 19 05 3f 00')
        #Ki's Body Guardian
        scripts.addNewScript(0, """79 6a 76 63 81 4e d8 eb e7 82 ff 22 ff 78 51 5a 5c d9 ff 06 6d 9a 92 8f 4f 5b da 85 06 d5 d4 d6 de 5c 94 5b c4 
                                   dc 77 06 bb e2 d7 ec 16 19 01 24 31 0d 00""")
        maps.map[11].npcgfx[3] = 0x3c
        maps.map[11].npcs[8] = bytearray.fromhex('03 5f 11 0c c4 c0')
        scripts.replaceScript(0, 299, '00')
        scripts.replaceScript(0, 300, '00')
        #Valhalla teleporters
        maps.addNPC(162, 66, '0b 1f 03 0a c5 90')
        maps.addNPC(162, 60, '0b 1f 38 07 c6 a0')
        scripts.addNewScript(0, 'd0 55 df 57 6d 9a df dc de 4e 5d ff 06 da 85 4f 5b 50 4e 75 78 53 e1 06 e3 dc 67 6e f4 16 19 06 8c 31 0d 00')
        scripts.addNewScript(0, 'd0 55 df 57 6d 9a df dc de 4e 5d ff 06 da 85 4f 5b 50 4e ea d8 78 53 e1 06 e3 dc 67 6e f4 16 19 06 86 31 0d 00')

class GamePrep:
    def __init__(self):
        pass

    def newTitleScreen(scripts:ScriptManager, seed:int):
        def _infoPatchList(seed:int)->str:
            def _hexList(info:str, maxLength:int)->str:
                hexes = ''
                for digit in info:
                    if digit.isdigit():
                        hexes+=f"{(int(digit) + 0xB0):02x}"
                    else: #float w/ dot
                        hexes+='F0'
                while len(hexes) < maxLength:
                    hexes = 'FF' + hexes
                return hexes

            finalList = '36 03 CB 59 D7 81 DC ED 53 FF' #"Randomizer "
            finalList+=(_hexList(str(VERSION), 8))
            finalList+= '05 36 03 CC D8 8F FF' #"Seed "
            finalList+=(_hexList(str(seed), 20))
            finalList+= '06 FF FF 2E FF CC E7 6E 54' #truncate start/continue
            return finalList


        titleInfo = _infoPatchList(seed)
        scripts.replaceScript(2, 20, '00 0a 14 08' + titleInfo + """2E FF BC 65 E7 56 E8 D8 06 FF A2 B1 B9 B9 B1 FF CC CA CE BA CB BE FF CC C8 BF
                                      CD 05 C5 C2 BC BE C7 CC BE BD FF BB D2 FF C7 C2 C7 CD BE C7 BD C8 00""")
        
    def leonsText(magi:int) -> list:
        match magi:
            case 0x00:
                magiString='C98453' #power
            case 0x01:
                magiString='CCE3D88F' #speed
            case 0x02:
                magiString='C659D4' #mana
            case 0x03:
                magiString='BDD8D98B80' #defense
            case 0x04:
                magiString='BFDC5A' #fire
            case 0x05:
                magiString='C2D6D8' #ice
            case 0x06:
                magiString='CDDBE87C53' #thunder
            case 0x07:
                magiString='C9E25F65' #poison
            case 0x08:
                magiString='C689E0E892' #masmune
            case 0x09:
                magiString='BAD8DA5F' #aegis
            case 0x0b:
                magiString='C175E5E7' #heart
            case 0x0c:
                magiString='C9D8DA898E' #pegasus
            case 0x0d:
                magiString='C9E55FE0' #prism
        magiString+='F3'
        while len(magiString) < 12:
            magiString+='FF'
        newScriptText = '06 CB D8 D6 D8 DC 76 57 9E' + magiString + """0b 0d 12 11 10 19 F6 33 00 FF 19 F6 11 00 F1 02 FF 19 F6 03 00 FF C5 D8 65 
                         F5 C9 98 89 D8 F1 F1 06 FF BF 66 DA DC 76 64 4E F1 F3 F3 11 04 0d 19 F0 12 19 F6 13 00 F2 13 FF 19 F6 21 00 FF 13 11 14 
                         08 06 10 20 1F 00 F5 C5 D8 65 63 5D 98 06 50 4E 9E""" + magiString + '00'

        return newScriptText

    def newDropScripts(scripts:ScriptManager):
        #gives Ashura and Venus new magi drop scripts
        scripts.addNewScript(0, '19 0a 00 19 0a 01 19 0a 02 19 0a 04 19 0a 05 19 0a 06 19 0a 07 00')
        scripts.addNewScript(0, '19 0a 00 19 0a 01 19 0a 02 19 0a 04 19 0a 05 19 0a 06 19 0a 07 00')
        #ashura
        scripts.main[333][348] = 0xC0
        #venus
        scripts.main[43][105] = 0xC1

    def memoRemove(scripts:ScriptManager, romData:mmap):
        blocks = ((0x54c4, 4), (0x3e038,72))
        for addr in blocks:
            for i in range(0,addr[1]):
                romData[addr[0]+i] = 0x00
        scripts.removeFromScript(2,1,31,37)
        scripts.menu[1][3]=0x0d
        for x in GameData.noMemoCalls:
            scripts.replaceScript(3, x, '00')
        c1 = scripts.findScriptByBytes('18')
        c2 = [x for x in c1 if x[0] == 0 and scripts.main[x[1]][x[2]-1] not in range(0x00, 0x3c)]
        c2.reverse()
        for x in c2:
            scripts.removeFromScript(0, x[1], x[2], x[2]+2)

    def kiShrineCleanup(scripts:ScriptManager, maps:MapManager):
        scripts.addNewScript(0, 'ba e6 e6 5f e7 59 e7 f5 8c 61 d4 76 06 e6 81 85 70 6b 7e 66 6f 55 f3 00')
        scripts.insertIntoScript(0, 306, 0, '15 0c 00 19 00 c2 00')
        maps.delNPC(11, 7)
        maps.map[11].npcs = [bytearray.fromhex('00 0e 24 25 25 11'), bytearray.fromhex('00 0e 28 25 27 21'), bytearray.fromhex('00 0e 24 a2 29 31'), 
                             bytearray.fromhex('01 0c 14 13 2d 51'), bytearray.fromhex('01 de 13 0c 2e d1'), bytearray.fromhex('01 06 12 cc 38 e1'), 
                             bytearray.fromhex('01 de 52 cc 32 e1'), bytearray.fromhex('03 5f 12 cc 33 e1'), bytearray.fromhex('01 0e 10 11 2b 41'), 
                             bytearray.fromhex('ff')]
        scripts.insertIntoScript(0, 293, 0, '15 01 de 19 01 26 00')
        scripts.insertIntoScript(0, 295, 0, '15 01 de 19 01 28 00')
        scripts.insertIntoScript(0, 297, 0, '15 01 de 19 01 2a 00')
        scripts.insertIntoScript(0, 299, 0, '15 01 de 19 01 2c 00')
        scripts.replaceScript(0, 305, '00')
        maps.map[47].npcs[0] =  bytearray.fromhex('4c 06 db c5 00 f1')
        scripts.replaceScript(0, 30, '00') 
        scripts.insertIntoScript(0, 31, 5, '12 0c')
        scripts.insertIntoScript(0, 32, 5, '12 0c')
        scripts.insertIntoScript(0, 33, 5, '12 0c')
        scripts.insertIntoScript(0, 34, 5, '12 0c')
        scripts.insertIntoScript(0, 35, 5, '12 0c')
        scripts.insertIntoScript(0, 36, 5, '12 0c')
        scripts.replaceScript(0, 37, '19 0a 03 12 03 12 0c 12 10 14 01 0f 10 14 0c 00 0b 0d 19 05 b0 19 07 03 00')
        scripts.main[345][37] = 0x0c
        maps.map[54].npcs = [bytearray.fromhex('4c 77 1a 12 59 91'), bytearray.fromhex('0c 78 5a cf 25 a0'), bytearray.fromhex('ff')]
        maps.map[22].npcs[0][1] = 0x55
        maps.map[38].npcs[0] = bytearray.fromhex('42 04 15 c5 4d 91')
        maps.map[38].npcs[1] = bytearray.fromhex('42 04 56 c5 4d 91')
        maps.map[38].npcs[2] = bytearray.fromhex('42 04 95 c6 4d 91')
        maps.map[38].npcs[3] = bytearray.fromhex('42 04 d6 c6 4d 91')
        scripts.replaceScript(0, 333, """19 07 12 ba 93 7d d4 f5 c1 ba f3 ff c1 ba f3 06 ff d0 d8 67 ef 61 d8 67 e2 f0 06 8c 5e 89 58 d5 55 54 5d 06 63 8b 
                                         57 e6 81 d8 65 4e 5d 06 4f d8 67 6f 55 f1 4f 6a e7 f1 06 9c 72 e0 59 58 df 5a d4 d7 ec 06 64 dc d6 91 e1 dc ed 8f 
                                         58 7c 06 5e 8b 54 56 5d ff c4 dc 77 06 74 e2 d7 ec f3 06 20 1f 00 f5 d0 6a 54 d7 dc 57 6d e8 06 83 5b 5d 61 53 f4 
                                         f3 06 ba 93 7d d4 f5 c4 dc 5e 89 74 66 73 ea 87 db 9c ba c0 79 56 61 53 06 74 e2 d7 72 ea 70 d6 db 62 d4 76 06 61 
                                         53 4f 51 ff e3 84 53 69 d9 06 61 75 df 56 da f0 06 8c 62 85 4f db e2 80 9c ba c0 c2 06 58 7c 63 51 7e d4 dc df e6 
                                         f3 f3 06 ff f1 f1 c4 dc 67 56 9b b2 74 dc e5 d7 52 ea 87 db ff b1 63 5d 92 f1 f1 06 ff d0 d8 67 f1 f1 ff c7 84 8c 
                                         62 85 06 6f 55 e5 52 59 57 50 60 ee 67 64 d4 de 4e 87 ff b3 74 dc e5 d7 e6 f3 f3 20 1f 00 f5 f1 f1 ff c7 d8 76 e5 
                                         f3 f3 0b 0d 09 83 37 19 07 0c 3e ba 93 7d d4 f5 c7 e2 f1 ff c7 e2 f3 f3 06 ff f1 8c ff f1 83 65 ee 54 f1 06 ff ff 
                                         f1 5e 59 e1 7b f1 83 dc d8 f1 ff f1 11 30 ba cb cb c0 c1 f3 11 01 0d 14 02 05 10 19 00 c0 0d 19 05 4a 10 19 f1 03 
                                         ff 1f 04 f5 c2 ee 76 83 65 d8 06 5e 6a 54 79 ea 59 7f 57 5d f0 06 ff cc d8 4e 6d e8 f3 06 06 36 03 1f 04 8a d8 d9 
                                         e7 f0 0b 0d 14 02 06 14 00 00 10 19 f1 00 ff 20 1f 05 f5 c4 dc 64 8e 54 95 06 5c 73 7b e7 91 e8 d5 98 f3 06 ff c5 
                                         85 77 62 5b 5d 61 53 f3 0b 0d 12 10 00""")
        maps.map[41].npcs[4] = bytearray.fromhex('03 00 5f 8b 53 d1')
        scripts.replaceScript(0, 339, """46 20 1f 05 f5 bd f1 ff bd d4 d7 f3 f3 06 19 07 0a bf 60 51 e5 f5 ce db f4 ff 20 1f 05 ff f1 f4 06 20 1f 05 f5 d2 
                                         75 db f3 f3 06 ff cb d8 6c e0 95 68 6c f4 f3 06 bf 60 51 e5 f5 c8 d9 7a 55 e5 80 f3 06 ff f1 ff c8 db ef ff 20 1f 
                                         05 ff f1 f1 06 ff c1 84 77 9c 81 f4 06 20 1f 05 f5 cc 51 77 7e 56 d8 f3 06 ff f1 ff d0 d4 87 56 9b db 81 d8 f0 06 
                                         ff c5 85 77 62 5b db 81 d8 06 4f e2 da 85 51 e5 ef ff bd d4 d7 f3 06 bf 60 51 e5 f5 ff f1 ff c7 5b f1 06 8c 7a 59 
                                         ee 54 ec 85 f0 06 20 1f 05 f5 bf 66 9c ba c0 c2 f4 06 ff bb 86 ff f1 ff d0 4e d7 d8 d9 75 7f 57 ba 93 7d d4 f3 06 
                                         bf 60 51 e5 f5 99 53 4e 6e d8 06 64 66 4e 8d 4f db e2 80 06 8a dc de 4e ba 93 7d 7b f1 06 62 e2 56 9b d4 d9 7f 68 
                                         c6 ba c0 c2 f0 20 1f 05 f5 c6 ba c0 c2 f1 ff d0 d8 ee 76 06 62 e2 54 e6 81 d8 f3 ff c1 53 d8 f3 f3 06 bf 60 51 e5 
                                         f5 d2 55 ee 5a 06 62 60 51 e5 56 9b 50 d8 e0 ef 06 4f e2 e2 f4 f3 06 ff 99 8b ef 4f d4 de 4e 50 5f f3 06 0b 0d 19 
                                         0a 00 06 bf 60 51 e5 f5 c7 e2 d5 e2 d7 ec 06 5e 55 df 57 dc e0 d4 da 56 d8 06 4f 6a 54 de dc d7 52 df dc de d8 06 
                                         6f 55 61 d4 76 63 e8 d6 db 06 58 4f 70 6b f0 06 20 1f 05 f5 c2 ee e0 90 e2 e7 06 58 ff de dc 57 59 ec e0 66 d8 f0 
                                         06 bf 60 51 e5 f5 d0 d8 ee 67 64 d8 85 06 58 da d4 56 58 52 9d 6b 58 e6 06 5e 4e 71 58 d9 7f 68 c6 ba c0 c2 f0 8c 
                                         ee 67 7a 81 4e db 81 d8 06 5e 87 db 6f 55 4f 51 e1 f0 06 20 1f 05 f5 c9 91 e0 5f d8 f4 06 bf 60 51 e5 f5 f1 f1 ff 
                                         d2 d8 e6 f0 06 8c ff c9 91 e0 5f d8 f0 06 14 03 01 10 20 1f 05 f5 c8 de d4 ec ef ff bd d4 57 f1 f1 06 ff f1 f1 ff 
                                         e3 91 e0 5f 4e f1 f1 06 14 18 05 00""")
        scripts.main[343][209] = 0x2f
        scripts.main[79][2] = 0x01
        scripts.main[79][9] = 0x22
        scripts.main[79][11] = 0x03
        scripts.main[79][12] = 0x03
        maps.map[39].npcs[0][1] = 0x03
        scripts.main[28][2] = 0x33
        scripts.main[334][17] = 0x04
        scripts.replaceScript(0, 302, '4b b3 f3 06 c0 dc 59 e7 52 93 55 df d7 06 de 88 ea 61 84 f0 ff 15 0c 00 19 01 34 00 00')
        scripts.replaceScript(0, 303, """20 1f 05 f5 bd 5b 6d 9a de 88 ea 06 58 e1 ec 50 56 9b d4 d5 55 e7 06 4f 51 9c ba c0 c2 f4 06 c4 dc f5 d0 
                                                 6a 54 ea dc 67 6f 55 06 83 5b ea 87 db 4f 51 e0 f4 06 ff bb 4e 7b 71 d7 f4 06 20 1f 06 f5 c7 5b ea d4 ec 
                                                 f3 06 ff 20 1f 05 77 7e 60 51 68 5f 06 62 e2 56 9b d4 d9 7f 68 c6 ba c0 c2 f0 ff d0 d8 ee 5a 8a e2 e2 de 
                                                 56 da 06 7e 66 61 dc e0 f0 06 c4 dc f5 99 60 64 59 5e 87 db 06 58 61 60 69 e1 f4 06 20 1f 05 f5 bd 5b 6d 
                                                 9a de 88 ea f4 06 ff d0 51 5a 83 dc 57 51 62 e2 f4 06 c4 dc f5 c1 4e d7 91 e3 e3 8f 5c e1 ef 06 58 e6 de 
                                                 8f 64 4e d4 d5 55 e7 06 9c ba c0 c2 ef 58 7c 8a d8 d9 e7 f0 06 20 1f 05 f5 c8 db f1 f1 ff c8 de d4 ec f0 
                                                 06 ff 99 59 de e6 f1 0b 0d 19 f1 10 ff c4 dc f5 d0 d4 87 f3 06 19 f1 11 ff 11 08 c4 dc f5 c9 d8 e2 e3 98 
                                                 63 d4 72 50 60 4f 51 5a 58 5a 9c ba c0 c2 06 5c 73 50 4e 5a df dc d6 52 8d 06 4f 51 58 e1 d6 dc 8b 54 71 
                                                 d7 e6 f0 8c e7 77 ff b4 4f 5b 50 d8 06 ff 75 78 58 7c ff b3 4f 5b 50 d8 06 63 55 50 7e 91 e0 4f 51 06 ff 
                                                 bb dc 9b cb e2 d6 de 5c 73 50 d8 06 ff cc 55 50 53 73 bf 66 d8 78 f0 0b 14 01 03 10 00""")
        scripts.replaceScript(0, 304, """06 ff d0 6a e7 f4 06 ff ba 93 7d d4 77 64 8b 4f e2 e2 de 06 4f 51 9c ba c0 c2 f4 06 20 1f 05 f5 d0 4e 6e 
                                                 4e 71 56 da 06 4f 5b 50 4e ba 93 7d d4 77 06 ff bb 89 d8 f0 06 c4 dc f5 c2 ee e0 7a 81 56 9b ea 87 db 6f 
                                                 55 f0 8c 64 8e 54 e6 d4 76 06 4f 70 52 ea 66 df 57 d9 91 e0 06 ff ba 93 7d d4 f0 0b 0d 14 01 07 14 00 02 
                                                 10 19 00 0f 00""")
        scripts.replaceScript(0, 312, """c4 dc f5 c2 ee 67 61 75 96 6d e8 f3 06 19 01 7c ff c8 de d4 ec f3 ff ba 67 83 65 d8 f3 f3 06 15 01 56 19 
                                                 01 30 00 15 01 02 19 01 2f 00 00""")
        scripts.insertIntoScript(0, 308, 0, '12 0c')
 
    def convertToRealChests(scripts:ScriptManager, maps:MapManager, treasureFlags:list):
        scripts.replaceScript(0, 38, """1b 0a 19 00 5b 00 19 05 b4 19 07 0e c2 e7 77 4f e2 5b d5 e5 dc da db e7 f3 06 79 97 e1 88 54 80 d8 06 59 
                                                ec 50 56 da f3 f3 00""")
        scripts.replaceScript(0, 91, '19 05 b5 19 f0 12 19 07 0b 36 03 cc d8 4e ea d8 67 5e 87 db 06 36 03 9e ff cd e5 e8 4e be ec 4e f3 f3 00')
        maps.map[65].npcs[2] = bytearray.fromhex('80' + f"{treasureFlags[0]:02x}" + '20 d9 0a fa')
        treasureFlags.pop(0)
        scripts.replaceScript(0, 86, '00')

    def venusWorldCleanup(scripts:ScriptManager, maps:MapManager):
        scripts.insertIntoScript(0, 165, 0, '15 08 01 14 08 02 31')
        scripts.removeFromScript(0, 432, 91, 94)
        maps.map[102].npcs[0][1] = 0x00
        scripts.removeFromScript(0, 421, 0, 2)
        scripts.insertIntoScript(0, 421, 0, '15 08 01')
        scripts.removeFromScript(0, 413, 6, 13)
        scripts.insertIntoScript(0, 413, 6, '00 15 08 11 19 01 f6 00')
        scripts.removeFromScript(3, 241, 390, 392)
        scripts.insertIntoScript(3, 241, 390, '15 11 00')
        scripts.insertIntoScript(3, 241, 504, '13 11 12 10')
        scripts.insertIntoScript(0, 420, 0, '12 11')
        scripts.removeFromScript(0, 415, 51, 53)
        scripts.insertIntoScript(0, 415, 51, '15 11 00')
        scripts.main[47][1] = 0x11
        scripts.main[47][18] = 0x11
        maps.map[112].npcs[0][0] = 0x51
        maps.map[113].npcs[0][0] = 0x51

#     #stitches together Dad's death cutscene by putting it all into memo, also adds a var4 check
    def dadDeathCutscenes(scripts:ScriptManager):
        scripts.insertIntoScript(0, 390, 34, '15 04 55')
        scripts.insertIntoScript(0, 390, 40, '31')
        scripts.replaceScript(3, 244, scripts.main[408].hex(" "))
        scripts.removeFromScript(0, 372, 211, 218)
        scripts.insertIntoScript(0, 372, 0, '10')
        scripts.insertIntoScriptAtEnd(3, 244, scripts.main[372].hex(" "))
        scripts.removeFromScript(3, 244, len(scripts.memo[244])-5, len(scripts.memo[244]))
        scripts.insertIntoScriptAtEnd(0, 371, '14 0e 07 12 10 19 05 ed 0d 15 05 00 14 04 00 00 15 05 11 14 04 01 00 15 05 33 14 04 01 00 00')
        scripts.insertIntoScriptAtEnd(3, 244, scripts.main[371].hex(" "))
        #+ 
        scripts.replaceScript(0, 371, '00')
        scripts.replaceScript(0, 372, '00')
        scripts.replaceScript(0, 408, '4b f4 40 f4 00')
        scripts.insertIntoScriptAtEnd(0, 492, '12 05 15 05 44 12 10 12 05 00')
        scripts.insertIntoScriptAtEnd(0, 89, '15 05 12 12 05 12 05 15 05 44 12 10 12 05 00')
        scripts.insertIntoScriptAtEnd(0, 350, '12 05')

    def guardianBaseLogic(maps:MapManager):
            maps.map[90].npcs[0][1] = 0x77
            maps.map[92].npcs[0][1] = 0x66
            maps.map[93].npcs[0][1] = 0x55
            maps.map[93].npcs[1][1] = 0x44
            maps.map[94].npcs[0][1] = 0x33

    def nastyChest(scripts:ScriptManager, maps:MapManager):
        #29
        scripts.replaceScript(0, 82, '15 11 11 19 00 53 0e 19 f0 00 ff 14 11 01 14 1e 02 19 07 0d 00')
        scripts.replaceScript(0, 93, '14 1e 03 14 11 00 15 0d 28 14 1e 01 31 00')
        scripts.removeFromScript(0, 142, 313, 315)
        maps.map[202].npcs[1] = bytearray.fromhex('1d 00 04 c6 5e f0')
        scripts.replaceScript(0, 94, '12 1d 12 10 12 11 10 13 11 19 0a 0c 14 18 0c 00')

    def warMachAdjust(scripts:ScriptManager, maps:MapManager, treasureFlagReclaim:list):
        treasureFlagReclaim.append(38)
        maps.map[187].npcs[1] = bytearray.fromhex('0c 04 0c cc 47 f0')
        maps.addNPC(187, 0, '11 11 4c cc 03 f1')
        scripts.replaceScript(0, 71, '12 0c 12 11 10 13 11 19 0a 0b 00')

    def prismDummy(scripts:ScriptManager):
        scripts.replaceScript(2, 64, '09 0d 02 02 f2 f2 00')

    def newCredits(scripts:ScriptManager):
        scripts.replaceScript(3, 240, """46 19 07 0f 4a 20 1f 05 f5 bd d4 d7 f3 f3 06 bf 60 51 e5 f5 c3 59 d8 77 06 ff e9 e2 dc d6 4e 5d df 57 6c 4f e2
                                         06 63 e7 d4 72 51 5a 58 7c 06 5e d4 87 7e 66 6f 55 f0 06 ff f1 8c 83 dc d7 e1 ee 54 de 88 ea 06 4f 6a 54 c6 ba 
                                         c0 79 ea 89 06 63 e8 d6 db 4f 70 6b ff f1 06 20 1f 05 f5 79 d9 d8 d8 96 df dc de d8 06 8c ee 76 63 d8 8b 64 66 
                                         d8 06 4f 6a 73 d8 76 e5 ec d5 e2 d7 ec 06 ff d8 df 80 f3 06 bf 60 51 e5 f5 c1 7b c1 d4 06 ff d2 55 68 ea 66 df 
                                         57 5f e1 ee e7 06 4f 6a 54 e6 e0 d4 67 f0 06 8c 61 d4 76 4f 5b 71 58 7c 06 63 d8 4e 87 58 67 f3 06 20 1f 05 f5 
                                         ce db f2 e8 db f3 06 ff bb d8 d9 66 4e 50 60 ef ff bd d4 d7 f3 bf 60 51 e5 f5 c8 db ef 6f d8 e6 f3 06 8c ff de 
                                         88 ea f1 f3 06 ff c5 85 77 62 5b db 81 d8 f3 11 08 0d 14 11 00 19 f0 15 19 0e 00 11 08 19 0e 01 19 f0 16 11 10 
                                         c9 91 da 82 e0 05 ff c7 d4 e2 de dc ff c8 de d4 95 05 ff cd 81 e2 de dc ff ba e1 d4 ed d4 ea d4 11 18 0d 19 f1 
                                         10 ff 11 18 12 11 10 13 11 10 12 11 10 13 11 10 12 11 10 c6 d4 56 ff bd 60 d4 05 ff c1 dc 91 e0 dc d6 70 ff cd 
                                         59 d4 de d4 06 bb 60 e7 98 ff bd 60 d4 05 ff ba de 87 e2 93 dc ff c4 d4 ea d4 ed e8 11 18 0d 13 11 10 12 11 10 
                                         13 11 10 12 11 10 13 11 10 11 18 19 0e 02 10 11 18 c6 d4 e3 ff bd 60 d4 05 ff cd e2 93 dc ec e8 de dc 8c 88 e8 
                                         d8 05 c0 82 e3 70 d6 e6 05 ff c1 dc 91 e0 dc ff c7 d4 de d4 d7 d4 05 ff c1 dc 91 e0 dc 8c 5d db 11 18 0d 14 11 
                                         02 10 19 f6 10 00 f1 01 ff 11 18 cc 55 7c ff c9 91 da 82 e0 05 ff c4 d8 87 6e 55 ff ba d7 d4 d6 70 05 c6 8e dc 
                                         d6 ff bc 81 e3 e2 80 05 ff c7 e2 d5 e8 5b ce d8 e0 60 e6 e8 05 ff c4 8b dd dc 8c 5d db 11 18 0d 19 f6 53 02 f1 
                                         02 ff 11 18 cd 82 e1 e6 df 60 dc 65 05 ff c4 d4 66 9a c6 66 dc ec d4 e0 d4 05 bd dc 5a d6 e7 dc 65 58 7c 05 cc 
                                         d6 8b 6e dc 5b d5 ec 05 ff ba de 87 e2 93 dc ff c4 d4 ea d4 ed e8 11 18 0d 19 f6 00 02 ff 11 04 19 f6 02 02 ff 
                                         11 04 19 f6 01 02 ff 11 04 19 f6 03 02 ff 11 04 19 f6 00 02 ff 11 04 19 f6 02 02 ff 11 04 19 f6 01 02 ff 11 04 
                                         19 f6 03 02 ff 11 18 19 0e 03 10 11 18 19 f1 53 ff 19 f7 00 19 f1 33 ff cb 59 d7 81 dc ed 53 74 ec 05 ff cd d4 
                                         d8 76 e5 dc df 11 18 0d 11 18 19 0e 04 10 11 18 19 f6 00 00 f6 00 01 ff bd d8 e6 dc da 73 d5 ec 05 ff bd d8 78 
                                         dc df 05 ff cd d4 d8 76 e5 dc df 05 ff cd 5a d5 98 05 ff d0 dc df d7 cf e8 df e7 7d d8 11 18 0d 19 f6 82 02 f6 
                                         82 03 ff 19 0e 05 10 11 18 be 6b 56 d8 53 56 9b d5 ec 05 ff bd d8 78 dc df 05 ff cd d4 d8 76 e5 dc df 05 4f d8 
                                         db e7 e0 dc 11 18 0d 12 11 10 19 f6 21 02 f1 03 f6 10 00 f1 10 f6 10 01 ff 19 f1 03 ff 11 18 cc e3 d8 d6 dc d4 
                                         96 99 59 de e6 05 4f d8 db e7 e0 dc 05 ff ba e0 8e d8 e8 e0 05 ff ba 98 eb ff c3 d4 d6 de e6 65 05 19 f6 02 02 
                                         ff ff c0 d4 6c bf ba ca e6 ee ff bf bf c5 b2 ff 05 ff 9c d8 e6 e6 d4 da 4e bb e2 6e d7 11 18 0d 11 18 19 0e 06 
                                         10 11 18 be 76 e5 6d 92 5e db e2 05 61 d8 df e3 8f 64 d4 e3 4f 70 52 05 ff cb c8 c6 4f 5b e0 d4 de d8 05 4f 70 
                                         52 82 7c 81 dc ed 53 05 ff e3 e2 e6 e6 dc d5 98 f0 11 18 0d 11 18 19 0e 07 10 11 18 19 f6 10 01 ff f1 59 d7 ef 
                                         69 d9 ff 05 7a 55 e5 80 ef ff d2 c8 ce f3 06 99 59 de 52 d9 66 ff 05 ff e3 df d4 ec 56 da f3 11 18 0d 11 18 bc 
                                         e2 e3 ec e5 dc da db e7 06 ff b1 b9 b9 b0 ff cc ca ce ba cb be 06 ff b1 b9 b9 b1 ff cc ca ce ba cb be ff cc c8 
                                         bf cd 11 18 0d 19 f0 15 19 0e 00 11 40 11 08 0d 19 0e 08 10 19 f0 16 20 1f 05 f5 c6 e0 e0 f1 db e0 f1 ff bd d4 
                                         d7 06 ff f1 ff d0 6a 54 5f 5c e7 f4 06 bf 60 51 e5 f5 79 6a 76 4f e2 06 8a 75 76 90 84 f0 06 20 1f 05 f5 ba da 
                                         d4 56 f4 06 ff d0 6a 54 5f 5c 54 50 5f 06 4f dc 6c ef ff bd d4 d7 f4 06 bf 60 51 e5 f5 c2 e7 77 4f 51 06 ff c5 
                                         e2 78 ff ba e5 de ef ff 20 1f 05 f3 06 19 f7 00 19 f1 10 ff 19 f1 12 ff 19 f1 01 f6 00 02 ff 20 1f 05 f5 c2 ee 
                                         e0 7a 81 56 da 06 5e 87 db 6f 55 ef ff bd d4 d7 f3 06 bf 60 51 e5 f5 ba 67 ff e5 dc da db e7 f3 06 ff bc 81 4e 
                                         65 f3 11 10 0d 19 f6 11 02 f1 11 ff 06 d0 d4 87 58 64 56 86 d8 f3 06 11 04 0d 19 07 01 19 f6 51 03 f6 10 02 f1 
                                         10 ff 19 f6 03 03 f1 02 ff c6 81 f5 c2 ee e0 4f dc 5a 57 8d 06 63 e7 d4 ec 56 9b db 81 4e 59 d7 06 5e 66 e5 ec 
                                         56 da f3 06 ff cd d4 de 4e 6c 5e 87 db 6f 55 f3 bd d4 d7 f5 bd 75 e5 f1 f3 f4 06 20 1f 05 f5 c0 5a 60 f3 06 ff 
                                         c5 85 77 62 e2 f3 11 10 0d 19 f6 11 02 f3 11 f6 13 03 ff 19 f6 61 02 f3 61 f6 61 03 ff 19 f0 15 11 70 19 0e 09 
                                         11 30 4d 00""")

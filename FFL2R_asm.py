import mmap
       
class Fixes:
    def __init__(self):
        pass

    #map 193 has a badly-defined trigger that this fixes
    def missingTrigger(rom:mmap):
        rom[0x1e292] = 0x09

    #elemental magi fix, mana magi affinity enable
    def magiFix(rom:mmap):
        adjustments = {
            0x32e29 : 0x0c, #elemental magi fix
            0x337ac : 0x40,
            0x337ad : 0x40,
            0x337b4 : 0x20,
            0x337b5 : 0x20,
            0x33c42 : 0x2A
        }
        for k,v in adjustments.items():
            rom[k] = v

    #fixes mutants so they can gain str
    def mutantStr(rom:mmap):
        rom[0x3119c] = 0x08

    #the warp call normally sets var29 to 0. this instead inserts var31, which forces a dismount when warping, fixing the race bug
    def forceRaceDismount(rom:mmap):
        warpVar =  bytearray.fromhex('1f 00 00 00 00 00')

        for x in range(0, len(warpVar)):
            rom[0x5cb3+x] = warpVar[x]

    #fixes gold drops when there is mutliple groups of enemies, written by tehtmi
    def goldDropFix(rom:mmap):
        asmmove = {
            0x30d0d: bytearray.fromhex('02 12 4D 06 06'),
            0x30d30: bytearray.fromhex('02 53 4D 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06 06'),
            0x34292: bytearray.fromhex('CD CC 45 00 00 00 00 00'),
            0x345cc: bytearray.fromhex("""21 77 CF AF 22 22 77 06 05 3E D0 80 67 2E 00 7E B7 28 50 4F 2E 0A 7E 21 50 7C C7 3E 0C CD D2 00 E6 1F 07 
                                        21 50 7E C7 3E 0C CD D2 00 23 5F 3E 0C CD D2 00 6B 67 AF 57 5F D5 E5 57 1E 0A CD 5F 01 57 59 CD 5C 01 E5 D5 
                                        F8 04 54 5D F8 00 CD 62 01 E8 04 E1 57 59 CD 5C 01 D5 11 77 CF F8 00 CD 62 01 E8 04 04 78 FE 08 38 A0 3E 08 
                                        CD 7D 01 61 43 0D FA 45 D8 C9"""),
            }

        for k,v in asmmove.items():
            for i in range(len(v)):
                rom[k+i] = v[i]

class QOL:
    def __init__(self):
        pass

    #There is a specific player movement speed variable. This sets it to 0x02 rather than 0x01, which is basically double speed.
    #increasing it higher than that starts messing up the loaded graphics. So without an overhaul, this will have to do for the
    #time being.
    def moveHax(rom:mmap):
        moveAddr = (
            0x01e43,
            0x01e54
           )
        for address in moveAddr:
            rom[address] = 0x02

    #this will speed text up without the a button as a default.
    #0x06 is default speed, 0x00 is fastest (as if a were pressed). Increasing value slows text down.
    def textHax(rom:mmap):
        textHax = (
             0x01470,
             0x067a0
             )

        for address in textHax:
             rom[address] = 0x00

    #better stat growth, written by tehtmi
    def betterGrowth(rom:mmap):
        asm = {
            0x30ffa : bytearray.fromhex('05'),
            0x31020 : bytearray.fromhex('05'),
            0x31001 : bytearray.fromhex('E3 4D D8 1F 00 38 6C 36 1F 02 14 50 06 06 06 06 06 06 06'),
            0x31160 : bytearray.fromhex('06 27 0E'),
            0x31194 : bytearray.fromhex('06 06 06'),
            0x311c0 : bytearray.fromhex('06 07 B3'),
            0x311e8 : bytearray.fromhex('06 06 06'),
            0x31215 : bytearray.fromhex('06 06 06'),
            0x340ca : bytearray.fromhex('00 00 00'),
            0x34196 : bytearray.fromhex('21 4D D8 C7 00 00'),
            0x341c0 : bytearray.fromhex('CD B5 45 00 00 00'),
            0x345b5 : bytearray.fromhex('E5 21 40 7B 1A 4F 1C 1A 47 09 3E 0C CD D2 00 E6 F0 E1 B6 77 78 C9'),
            }
        for k,v in asm.items():
            for i in range(len(v)):
                rom[k+i] = v[i]

        #this doubles or triples growth chances
        for i in range(0,32):
            if i == 16 or i == 17:
                rom[0x33f90+i]*=2
            else:
                rom[0x33f90+i]*=3
       






import binascii
import random
import FFL2R_data
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def main(rom_path:str|None, seed:int|None):
    Tk().withdraw()
    if not rom_path:
        gameFile = askopenfilename(title="First, please point to the FFL2 rom.")
    else:
        gameFile = rom_path

    romData = {}

    #  seeding
    if not seed:
        gameSeed_str = str(input("And now a seed please. Blank will generate a random number."))
        try:
            gameSeed=int(gameSeed_str)
            gameSeed = abs(gameSeed)
        except:
            gameSeed = random.randint(0, 4294967296)
        random.seed()
    else:
        gameSeed = seed
    print("Seed is: " + str(gameSeed))

    with open(gameFile, 'rb') as f:
        hexData = binascii.hexlify(f.read())

    i = 0
    # init of address with hex
    while i*2 < len(hexData):
        # script patching-in code
        if i >= 180224 and i <= 180606 and i % 2 == 0:
            # this can probably be generalized if there's more bit overflow with additional scripts
            # but right now it only happens once so it's done by hardcoding
            if hexData[i*2:i*2+2].upper() == b"FF":
                romData.update({ ("{:08X}".format(i)) : b"03" })
                i+=1
                romData.update({ ("{:08X}".format(i)) : b"53" })
            else:
                romData.update({ ("{:08X}".format(i)) : bytes(hex(int((hexData[i*2:i*2+2]),16)+4)[2:].zfill(2).upper(), encoding='utf-8') })
        # insertion of new scripts
        # Ashura, Venus, and Odin all use the same drop script (one of each MAGI), with Venus + Odin dropping Aegis / Masmune in the post-battle script.
        # To increase randomization possibilities, new scripts for Ashura and Venus have been added.
        # Odin keeps the original script. All non-TrueEye MAGI can be randomized.
        elif i >= 180607 and i <= 190948:
            if i == 180607 or i == 180609:
                romData.update({ ("{:08X}".format(i)) : b"69" })
            elif i == 180608:
                romData.update({ ("{:08X}".format(i)) : b"E5" })
            elif i == 180610:
                romData.update({ ("{:08X}".format(i)) : b"FB" })
            else:
                romData.update({ ("{:08X}".format(i)) : hexData[(i-4)*2:(i-4)*2+2].upper() })
        # Ashura's new custom MAGI drop script
        elif i >= 190949 and i<=190969:
            match i % 3:
                case 0:
                    romData.update({ ("{:08X}".format(i)) : b"0A" })
                case 1:
                    romData.update({ ("{:08X}".format(i)) : b"09" })
                case 2:
                    romData.update({ ("{:08X}".format(i)) : b"19" })
        elif i == 190970:
            romData.update({ ("{:08X}".format(i)) : b"00" })
            romData.update({ "00028EDB" : b"C0"})
        # Venus' new custom MAGI drop script
        elif i >= 190971 and i<=190991:
            match i % 3:
                case 0:
                    romData.update({ ("{:08X}".format(i)) : b"19" })
                case 1:
                    romData.update({ ("{:08X}".format(i)) : b"0A" })
                case 2:
                    romData.update({ ("{:08X}".format(i)) : b"09" })   
        elif i == 190992:
            romData.update({ ("{:08X}".format(i)) : b"00" })
            romData.update({ "0002CC71" : b"C1"}) #addr +4 offset
        else:
            romData.update({ ("{:08X}".format(i)) : hexData[i*2:i*2+2].upper() })
        i+=1

    game = FFL2R_data.GameData
    
    random.shuffle(game.treasures)


    j=0
    for address in game.treasureAddresses:
        romData.update({ address : game.treasures[j] })
        if game.treasures[j] == b"FF":
            k = "{:08X}".format(int("0x" + address,16)-2)
            romData[k] = bytes(hex(int(romData[k], 16)+64)[2:].upper(), encoding='utf-8')
        j+=1

    random.shuffle(game.magi)
    j=0
    for address in game.magiAddresses:
        romData.update({ address : game.magi[j] })
        #race MAGI duplication
        if address == "0002AB55":
            romData.update ({ "0002AAE0" : game.magi[j] })
        elif address == "0002AB5B":
            romData.update ({ "0002AB07"  : game.magi[j] })
        elif address == "0002AB61":
            romData.update ({"0002AB2F" : game.magi[j] })
        j+=1
    
    for prices in game.newItemPrices:
        romData.update(prices)

    with open('Final Fantasy Legend 2 - ' + str(gameSeed) + '.gb', 'xb') as f:
        for key, value in romData.items():
            f.write(binascii.unhexlify(value))

    print ("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=str) # todo - pathlib
    parser.add_argument('-r', '--rom_path', type=int, dest="rom_path")
    args = parser.parse_args()
    main(rom_path = args.rom_path, seed=args.seed)

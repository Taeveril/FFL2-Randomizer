import binascii
import random
from re import M
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
        random.seed(gameSeed)
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
                romData.update({ hex(i) : b"03" })
                i+=1
                romData.update({ hex(i) : b"53" })
            else:
                romData.update({ hex(i) : bytes(hex(int((hexData[i*2:i*2+2]),16)+4)[2:].zfill(2).upper(), encoding='utf-8') })
        # insertion of new scripts
        # Ashura, Venus, and Odin all use the same drop script (one of each MAGI), with Venus + Odin dropping Aegis / Masmune in the post-battle script.
        # To increase randomization possibilities, new scripts for Ashura and Venus have been added.
        # Odin keeps the original script. All non-TrueEye MAGI can be randomized.
        elif i >= 180607 and i <= 190948:
            if i == 180607 or i == 180609:
                romData.update({ hex(i) : b"69" })
            elif i == 180608:
                romData.update({ hex(i) : b"E5" })
            elif i == 180610:
                romData.update({ hex(i) : b"FB" })
            else:
                romData.update({ hex(i) : hexData[(i-4)*2:(i-4)*2+2].upper() })
        # Ashura's new custom MAGI drop script
        elif i >= 190949 and i<=190969:
            match i % 3:
                case 0:
                    romData.update({ hex(i) : b"0A" })
                case 1:
                    romData.update({ hex(i) : b"09" })
                case 2:
                    romData.update({ hex(i) : b"19" })
        elif i == 190970:
            romData.update({ hex(i) : b"00" })
            romData.update({ hex(167643) : b"C0"}) #0x28edb
        # Venus' new custom MAGI drop script
        elif i >= 190971 and i<=190991:
            match i % 3:
                case 0:
                    romData.update({ hex(i) : b"19" })
                case 1:
                    romData.update({ hex(i) : b"0A" })
                case 2:
                    romData.update({ hex(i) : b"09" })   
        elif i == 190992:
            romData.update({ hex(i) : b"00" })
            romData.update({ hex(183409) : b"C1"}) #addr +4 offset #0x2cc71
        else:
            romData.update({ hex(i) : hexData[i*2:i*2+2].upper() })
        i+=1
     

    game = FFL2R_data.GameData

    random.shuffle(game.treasures)
    j=0
    for address in game.treasureAddresses:
        romData.update({ hex(address) : game.treasures[j] })
        if game.treasures[j] == b"FF":
            k = hex(address - 0x2)
            romData[k] = bytes(hex(int(romData[k], 16)+64)[2:].upper(), encoding='utf-8')
        j+=1


    random.shuffle(game.magi)
    k=0
    for address in game.magiAddresses:
        romData.update({ hex(address) : game.magi[k] })
        #race MAGI duplication
        if address == 0x2ab55:
            romData.update({ hex(174816) : game.magi[k] }) #0x2aae0
        elif address == 0x2ab5b:
            romData.update({ hex(174855) : game.magi[k] }) #0x2ab07
        elif address == 0x2ab61:
            romData.update({ hex(174895): game.magi[k] }) #0x2ab2f
        k+=1
        
    for key, value in game.newItemPrices.items():
        romData.update({hex(key) : value})

    #shopshuffle
    l=1
    while l <= 10:
        match l:
            #final town
            case 7:
                a=0
                t7 = list(game.shopTiers[7])
                random.shuffle(t7)
                while a < 8:
                    romData.update({hex(260736+a) : t7[a]})
                    a+=1
            #recurring
            case 8:
                a=0
                while a < 8:
                    romData.update({hex(260744+a) : game.shopTiers[8][a]})
                    a+=1
            #echigoya
            case 9:
                echigoya = []
                t0 = list(game.shopTiers[0])
                t7 = list(game.shopTiers[7])
                random.shuffle(t0)
                random.shuffle(t7)
                a = random.randint(0,5)
                b = 6 - a
                c = 0
                while a >= 0:
                    echigoya.append(t0[a])
                    a-=1
                while b >= 0:
                    echigoya.append(t7[b])
                    b-=1
                while c < 8:
                    romData.update({hex(260752+c) : echigoya[c]})
                    c+=1
            #giant town special
            case 10:
                gianttown = []
                t0 = list(game.shopTiers[0])
                t6 = list(game.shopTiers[6])
                t7 = list(game.shopTiers[7])
                random.shuffle(t0)
                random.shuffle(t6)
                random.shuffle(t7)
                a = random.randint(3,6)
                b = random.randint(0,2)
                c = random.randint(0,2)
                d = 0
                while a > 0:
                    gianttown.append(t0[a-1])
                    a-=1
                while b > 0 and len(gianttown) < 8:
                    gianttown.append(t6[b-1])
                    b-=1
                while c > 0 and len(gianttown) < 8:
                    gianttown.append(t7[c-1])
                    c-=1
                while d < 8:
                    if d+1 <= len(gianttown):
                        romData.update({hex(260760+d) : gianttown[d]})
                    else:
                        romData.update({hex(260760+d) : b"FF"})
                    d+=1
            case _:
                addresses = []
                for tierCheck in game.shopAddresses:
                    if tierCheck[0] == l:
                        addresses.append(tierCheck[1])
                tier = list(game.shopTiers[l])
                t0 = list(game.shopTiers[0])
                nexttier = list(game.shopTiers[l+1])
                random.shuffle(tier)
                random.shuffle(t0)
                t0 = t0[0:3]
                random.shuffle(nexttier)
                totalItems = random.randint((len(tier)+2), ((len(addresses)*8)))
                currentShop = 0
                positionTracker = 0
                while totalItems > 0:
                    if len(tier) > 0:
                        romData.update({hex(addresses[currentShop]+positionTracker) : tier[0] })
                        tier.pop(0)
                    elif len(t0) > 0:
                        romData.update({hex(addresses[currentShop]+positionTracker) : t0[0] })
                        t0.pop(0)
                    elif len(nexttier) > 0:
                        romData.update({hex(addresses[currentShop]+positionTracker) : nexttier[0] })
                        nexttier.pop(0)
                    currentShop+=1
                    if (currentShop > len(addresses)-1):
                        currentShop = 0
                        positionTracker+=1
                    totalItems-=1
                while positionTracker < 8:
                    romData.update({hex(addresses[currentShop]+positionTracker) : b"FF" })
                    currentShop+=1
                    if (currentShop > len(addresses)-1):
                        currentShop = 0
                        positionTracker+=1
        l+=1

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

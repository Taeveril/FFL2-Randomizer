import mmap
import random
from re import M
import FFL2R_data
import FFL2R_utils
import argparse
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def main(rom_path:str|None, seed:int|None):
    Tk().withdraw()
    if not rom_path:
        gameFile = askopenfilename(title="First, please point to the FFL2 rom.")
    else:
        gameFile = rom_path

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
        romData = mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_COPY,offset=0)  

    romData = treasureShuffle(romData, FFL2R_data.GameData)
    romData = magiShuffle(romData, FFL2R_data.GameData)
    
    romData = FFL2R_utils.GameUtility.safeUnlocks(romData)
    romData = FFL2R_utils.GameUtility.magiFix(romData)
    romData = FFL2R_utils.GameUtility.mutantFix(romData)

    for key, value in FFL2R_data.GameData.newItemPrices.items():
         romData[key] = value

    romData = shopShuffle(romData, FFL2R_data.GameData)

    with open('Final Fantasy Legend 2 - ' + str(gameSeed) + '.gb', 'xb') as f:
            f.write(romData)

    print ("Done!")

def treasureShuffle(rom:mmap, data:FFL2R_data) -> mmap:
    random.shuffle(data.treasures)
    i=0
    for address in data.treasureAddresses:
        rom[address] = data.treasures[i]
        if data.treasures[i] == 0xFF:
            j = address - 2
            rom[j] = rom[j]+64
        i+=1
    return rom

def magiShuffle(rom:mmap, data:FFL2R_data) -> mmap:
    rom = FFL2R_utils.GameUtility.scriptPatch(rom)
    random.shuffle(data.magi)
    i=0
    for address in data.magiAddresses:
        rom[address] = data.magi[i]
        #race MAGI duplication
        if address == 0x2ab55:
            rom[0x2aae0] = data.magi[i]
        elif address == 0x2ab5b:
            rom[0x2ab07] = data.magi[i]
        elif address == 0x2ab61:
            rom[0x2ab2f] = data.magi[i]
        i+=1
    return rom

def shopShuffle(rom:mmap, data:FFL2R_data) -> mmap:
    i=1
    while i <= 10:
        match i:
            #final town
            case 7:
                a=0
                t7 = list(data.shopTiers[7])
                random.shuffle(t7)
                while a < 8:
                    rom[0x3fa80+a] = t7[a]
                    a+=1
            #recurring
            case 8:
                a=0
                while a < 8:
                    rom[0x3fa88+a] = data.shopTiers[8][a]
                    a+=1
            #echigoya
            case 9:
                echigoya = []
                t0 = list(data.shopTiers[0])
                t7 = list(data.shopTiers[7])
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
                    rom[0x3fa90+c] = echigoya[c]
                    c+=1
            #giant town special
            case 10:
                gianttown = []
                t0 = list(data.shopTiers[0])
                t6 = list(data.shopTiers[6])
                t7 = list(data.shopTiers[7])
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
                        rom[0x3fa98+d] = gianttown[d]
                    else:
                        rom[0x3fa98+d] = 0xFF
                    d+=1
            case _:
                addresses = []
                for tierCheck in data.shopAddresses:
                    if tierCheck[0] == i:
                        addresses.append(tierCheck[1])
                tier = list(data.shopTiers[i])
                t0 = list(data.shopTiers[0])
                nexttier = list(data.shopTiers[i+1])
                random.shuffle(tier)
                random.shuffle(t0)
                t0 = t0[0:3]
                random.shuffle(nexttier)
                totalItems = random.randint((len(tier)+2), ((len(addresses)*8)))
                currentShop = 0
                positionTracker = 0
                while totalItems > 0:
                    if len(tier) > 0:
                        rom[addresses[currentShop]+positionTracker] = tier[0]
                        tier.pop(0)
                    elif len(t0) > 0:
                        rom[addresses[currentShop]+positionTracker] = t0[0]
                        t0.pop(0)
                    elif len(nexttier) > 0:
                        rom[addresses[currentShop]+positionTracker] = nexttier[0]
                        nexttier.pop(0)
                    currentShop+=1
                    if (currentShop > len(addresses)-1):
                        currentShop = 0
                        positionTracker+=1
                    totalItems-=1
                while positionTracker < 8:
                    rom[addresses[currentShop]+positionTracker] = 0xFF
                    currentShop+=1
                    if (currentShop > len(addresses)-1):
                        currentShop = 0
                        positionTracker+=1
        i+=1
    return rom

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--seed', type=str) # todo - pathlib
    parser.add_argument('-r', '--rom_path', type=int, dest="rom_path")
    args = parser.parse_args()
    main(rom_path = args.rom_path, seed=args.seed)

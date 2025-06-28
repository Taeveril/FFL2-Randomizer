import mmap

class GameUtility:

    def titlePatch(VERSION:float, seed:int, rom:mmap) -> mmap:
        i=0x2f42a
        while i<=0x2f498:
            if i % 2 == 0:
                if (rom[i] + 29) > 255:
                    carryOver = rom[i]
                    carryOver +=29
                    carryOver -=256
                    rom[i] = carryOver
                    i+=1
                    rom[i]+=1
                else:
                    rom[i]+=29
            i+=1

        titleUpdate = GameUtility.infoPatchList(VERSION, seed)
        dataShift = []
        j=0x2f8c8
        k=0

        while j<=0x2ffeb:
            if j >=0x2f8c8 and j<=0x2f8ef:
                if j >= 0x2f8d3:
                    dataShift.append(rom[j])
                rom[j] = titleUpdate[k]
                k+=1
            else:
                dataShift.append(rom[j])
                rom[j] = dataShift[0]
                dataShift.pop(0)
                if j == 0x2f90b:
                    rom[j] = 0x05
            j+=1
        return rom

    def infoPatchList(VERSION:float, seed:int) -> list:
        finalList = [0x36, 0x03, 0xCB, 0x59, 0xD7, 0x81, 0xDC, 0xED, 0x53, 0xFF] #"Randomizer "
        finalList.extend(GameUtility.hexList(str(VERSION), 4))
        finalList.extend([0x05, 0x36, 0x03, 0xCC, 0xD8, 0x8F, 0xFF]) #"Seed "
        finalList.extend(GameUtility.hexList(str(seed), 10))
        finalList.extend([0x06, 0xFF, 0xFF, 0x2E, 0xFF, 0xCC, 0xE7, 0x6E, 0x54]) #truncate start/continue
        return finalList

    def hexList(info:str, maxLength:int)-> list:
        hexes = []
        for digit in info:
            if digit.isdigit():
                hexes.append(int(digit) + 0xB0)
            else: #float w/ dot
                hexes.append(0xF0)
        while len(hexes) < maxLength:
            hexes.insert(0, 0xFF)
        return hexes

    def magiScriptPatch(rom:mmap) -> mmap:
        i=0x2c000
        insertion = []
        while i <= 0x2ea10:
            if i >= 0x2c000 and i <= 0x2c17e and i % 2 == 0:
            # this can probably be generalized if there's more bit overflow with additional scripts
            # but right now it only happens once so it's done by hardcoding
                if rom[i] == 0xFF:
                    rom[i] = 0x03
                    i+=1
                    rom[i] = 0x53
                else:
                    rom[i]+=4
        # insertion of new scripts
        # Ashura, Venus, and Odin all use the same drop script (one of each MAGI), with Venus + Odin dropping Aegis / Masmune in the post-battle script.
        # To increase randomization possibilities, new scripts for Ashura and Venus have been added.
        # Odin keeps the original script. All non-TrueEye MAGI can be randomized.
            elif i >= 0x2c17f and i <= 0x2e9e4:
                insertion.append(rom[i])
                if i == 0x2c17f or i == 0x2c181:
                    rom[i] = 0x69
                elif i == 0x2c180:
                    rom[i] = 0xE5
                elif i == 0x2c182:
                    rom[i] = 0xFB
                else:
                    rom[i] = insertion[0]
                    insertion.pop(0)
            # Ashura's new custom MAGI drop script
            elif i >= 0x2e9e5 and i<=0x2e9f9:
                match i % 3:
                    case 0:
                        rom[i] = 0x0A
                    case 1:
                        rom[i] = 0x09
                    case 2:
                        rom[i] = 0x19
            elif i == 0x2e9fa:
                rom[i] = 0x00
                rom[0x28edb] = 0xC0
                # Venus' new custom MAGI drop script
            elif i >= 0x2e9fb and i<=0x2ea0f:
                match i % 3:
                    case 0:
                        rom[i] = 0x19
                    case 1:      
                        rom[i] = 0x0A
                    case 2:      
                        rom[i] = 0x09 
            elif i == 0x2ea10:
                rom[i] = 0x00
                rom[0x2cc71] = 0xC1 #addr +4 offset #0x2cc71
            i+=1
        return rom

    def leonsText(magi:int, rom:mmap) -> mmap:
        match magi:
            case 0x00:
                magiString=[0xC9, 0x84, 0x53] #power
            case 0x01:
                magiString=[0xCC, 0xE3, 0xD8, 0x8F] #speed
            case 0x02:
                magiString=[0xC6, 0x59, 0xD4] #mana
            case 0x03:
                magiString=[0xBD, 0xD8, 0xD9, 0x8B, 0x80] #defense
            case 0x04:
                magiString=[0xBF, 0xDC, 0x5A] #fire
            case 0x05:
                magiString=[0xC2, 0xD6, 0xD8] #ice
            case 0x06:
                magiString=[0xCD, 0xDB, 0xE8, 0x7C, 0x53] #thunder
            case 0x07:
                magiString=[0xC9, 0xE2, 0x5F, 0x65] #poison
            case 0x08:
                magiString=[0xC6, 0x89, 0xE0, 0xE8, 0x92] #masmune
            case 0x09:
                magiString=[0xBA, 0xD8, 0xDA, 0x5F] #aegis
            case 0x0B:
                magiString=[0xC1, 0x75, 0xE5, 0xE7] #heart
            case 0x0C:
                magiString=[0xC9, 0xD8, 0xDA, 0x89, 0x8E] #pegasus
            case 0x0D:
                magiString=[0xC9, 0xE5, 0x5F, 0xE0] #prism
        magiString.append(0xF3)
        while len(magiString) < 6:
            magiString.append(0xFF)
        newScriptText = magiString + [0x0B, 0x0D, 0x12, 0x11, 0x10, 0x19, 0xF6, 0x33, 0x00, 0xFF, 0x19, 0xF6, 0x11, 0x00, 0xF1, 0x02,
                         0xFF, 0x19, 0xF6, 0x03, 0x00, 0xFF, 0xC5, 0xD8, 0x65, 0xF5, 0xC9, 0x98, 0x89, 0xD8, 0xF1, 0xF1,
                         0x06, 0xFF, 0xBF, 0x66, 0xDA, 0xDC, 0x76, 0x64, 0x4E, 0xF1, 0xF3, 0xF3, 0x11, 0x04, 0x0D, 0x19,
                         0xF0, 0x12, 0x19, 0xF6, 0x13, 0x00, 0xF2, 0x13, 0xFF, 0x19, 0xF6, 0x21, 0x00, 0xFF, 0x13, 0x11,
                         0x14, 0x08, 0x06, 0x10, 0x20, 0x1F, 0x00, 0xF5, 0xC5, 0xD8, 0x65, 0x63, 0x5D, 0x98, 0x58, 0xFF,
                         0x06, 0x9E] + magiString
        i=0x2ce28 #should be 2ce26 but some odd offset thing isn't making it work right, prob mmap and using adding scripts in the same function
        while i <= 0x2ce85: #should be 2ce83
            rom[i] = newScriptText[0]
            newScriptText.pop(0)
            i+=1
        j=0
        while j <= 5:
            if magiString[j] == 0xF3:
                magiString[j] = 0xF0
            j+=1
        newMemoText = [0x63, 0x5D, 0x98, 0x58, 0xFF, 0xFF, 0x06, 0x9E] + magiString + [0xFF, 0xFF]
        k=0x3ca6b
        while k <= 0x3ca7a:
            rom[k] = newMemoText[0]
            newMemoText.pop(0)
            k+=1
        return rom

    def safeUnlocks(rom:mmap) -> mmap:
        # All MAGI checks are an invisible npc that otherwise halts the player if they fail to meet the requirement -- "We need more MAGI to open this door!"
        # this can put the player in a rough state if the player Teleports/Pegasus/ItemDoor's to a world where they cannot escape, usually happens when 
        # Apollo steals MAGI. This function makes it so that once the magi check passes, the NPC vanishes and does not respawn.
        # Functionally, all these checks use script variable 16. The "opened" script increments the variable, pulls the player through into the door,
        # and then decrements the variable. This edits the script not decrement while putting a max var on these NPCs so they do not respawn.
        doorLocks = {
            0x1cc66 : 0x01, #to giant world
            0x1ce42 : 0x02, #giant house
            0x1ce5d : 0x04, #to apollo world
            0x1cf54 : 0x03, #to Ki's head, wholly unnecessary but nice to be consistent
            0x2cada : 0x05, #   these are not unlocks but changes the script variables for Ki's MAGI from using 16 to 5, the TrueEye MAGI plot event. 
            0x2caed : 0x05, #   Again kind of unnecessary, but just cleaning up Script Variable 16 to be consistent.
            0x1cfd8 : 0x05,
            0x1d015 : 0x05, #to guardian world
            0x1d336 : 0x06, #to ninja world
            0x1d54e : 0x07, #to venus world
            0x1d5b4 : 0x08, #to race world
            0x1d963 : 0x09, #to edo
            0x1db45 : 0x0A, #to nasty dungeon world
            0x1df1e : 0x0B, #to valhalla
            0x1e078 : 0x0C, #to central world
            0x1e091 : 0x0A  #back to valhalla. Maybe a bug since it checks for 66 Magi (to Edo) which is script 76, rather than 76 MAGI; but all irrelevant since it's meant to block you into final world.
            }

        for key, value in doorLocks.items():
            if key >= 0x2c000: #2c000
                rom[key + 4] = value
            else:
                rom[key] = value

        #recalc scripting block
        
        i=0x2c060
        while i<= 0x2c183:
            if i % 2 == 0:
                rom[i]-=2
            i+=1

        j=0x2ccec
        while j<= 0x2ea10:
            rom[j] = rom[j+2]
            j+=1

        return rom

    def monsterSelect(monsters:list, rom:mmap) -> mmap:
        shiftList = []
        dslist = []
        #shift the rest of the monster ability array
        remainingAddr = 0x37e8b
        currentAddr = remainingAddr
        while currentAddr <= 0x37eb4:
            shiftList.append(rom[currentAddr])
            currentAddr+=1
        c=0

        for monster in monsters:
            currentMonster = RandomMonster(monster)
            monstersIndex = monsters.index(monster)
            rom[0x338f5+monstersIndex] = rom[currentMonster.monFamAddr]
            rom[0x33e45+monstersIndex] = rom[currentMonster.monAIAddr]
            rom[0x364f5+monstersIndex] = rom[currentMonster.monGFXAddr]
            rom[0x36c65+monstersIndex] = rom[currentMonster.monNPCAddr]

            #calc DS level from monAIAddr low nibble, put it on the select screen
            dslist.append(rom[currentMonster.monAIAddr] & 0x0f)

            for stat in currentMonster.statArray:
                statIndex = currentMonster.statArray.index(stat)
                match statIndex:
                    case 8:
                        currentMonster.skillListAddr.append(rom[currentMonster.monStatAddr + 8])
                        rom[0x37912 + (monstersIndex * 10) + 8] = 0x8b + c
                    case 9:
                        currentMonster.skillListAddr.append(rom[currentMonster.monStatAddr + 9])
                        rom[0x37912 + (monstersIndex * 10) + 9] = 0x7e
                    case _:
                        rom[0x37912 + (monstersIndex * 10) + statIndex] = rom[stat]
                        rom[0x3f668 + (monstersIndex * 8) + statIndex] = rom[currentMonster.name[statIndex]]
                        if statIndex == 0:
                            currentMonster.skillListLength = rom[currentMonster.statArray[0]] - 31

            currentMonster.skillListLoc = currentMonster.getSkillListLoc(currentMonster.skillListAddr)            
            
            i = 0
            while i < currentMonster.skillListLength:               
                currentMonster.skillList.append(rom[currentMonster.skillListLoc + i])
                i+=1

            for skill in currentMonster.skillList:
                rom[remainingAddr] = skill
                remainingAddr+=1

            c = c + currentMonster.skillListLength

        j = 0
        while j <= 7:
           rom[0x37938 + (j*10)] = rom[0x37938 + (j*10)] + c
           j+=1

        for value in shiftList:
            rom[remainingAddr] = value
            remainingAddr+=1

        #recalc menu addr block 9 more bytes:       
        hexlevels = []
        for level in dslist:
            if level < 10:
                hexlevels.append(0xff)
                hexlevels.append(0xb0 + level)
            else:
                hexlevels.append(0xb1)
                hexlevels.append(0xb0 + (level - 10))
        
        i = 0x2f42c
        while i <= 0x2f499:
            if i % 2 == 0:
                if (rom[i] + 9) > 255:
                    carryOver = rom[i]
                    carryOver +=9
                    carryOver -=256
                    rom[i] = carryOver
                    i+=1
                    rom[i]+=1
                else:
                    rom[i]+=9
            i+=1

        shiftedList = []
        j = 0x2f966
        while j <= 0x2ffff:
            shiftedList.append(rom[j])
            match j:
                case 0x2f966 | 0x2f974 | 0x2f982:
                    rom[j] = 0xff #space
                    j+=1
                    shiftedList.append(rom[j])
                    rom[j] = hexlevels[0]
                    hexlevels.pop(0)
                    j+=1
                    shiftedList.append(rom[j])
                    rom[j] = hexlevels[0]
                    hexlevels.pop(0)
                case _:
                    rom[j] = shiftedList[0]
                    shiftedList.pop(0)
            j+=1
        return rom          

    def magiFix(rom:mmap) -> mmap:
        fix = {
            0x32e29 : 0x0C, #elemental magi fix
            0x337ac : 0x40,
            0x337ad : 0x40,
            0x337b4 : 0x20,
            0x337b5 : 0x20,
            0x33c42 : 0x2A  #mana magi affinity enable
            }

        for key, value in fix.items():
            rom[key] = value

        return rom

    def mutantFix(rom:mmap) -> mmap:
        rom[0x3119C] = 0x08
        return rom

    #There is a specific player movement speed variable. This sets it to 0x02 rather than 0x01, which is basically double speed.
    #increasing it higher than that starts messing up the loaded graphics. So without an overhaul, this will have to do for the
    #time being.
    def speedHax(rom:mmap) -> mmap:
        moveHax = (
            #movement
            0x01e3e,
            0x01e43,
            0x01e54
            )
        
        for address in moveHax:
            rom[address] = 0x02

    #this will speed text up without the a button as a default.
    #0x06 is default speed, 0x00 is fastest (as if a were pressed). Increasing value slows text down.
        textHax = (
             0x01470,
             0x067A0
             )
        for address in textHax:
             rom[address] = 0x00

        return rom


class RandomMonster:
    def __init__(self, monster:int):
        self.monster = monster
        self.monFamAddr = 0x33800 + self.monster
        self.monAIAddr = 0x33d50 + self.monster
        self.monGFXAddr = 0x36400 + self.monster
        self.monNPCAddr = 0x36b70 + self.monster
        self.monStatAddr = 0x36f80 + (self.monster * 10) #len 10
        self.statArray = self.getStatArray(self.monStatAddr)
        self.skillListLength = 0
        self.skillList = []
        self.skillListAddr = []
        self.skillListLoc = 0
        self.nameAddr = 0x3eec0 + (self.monster * 8)
        self.name = self.getName(self.nameAddr)

    def getStatArray(self, addr:int)->list:
        stats = []
        i=0
        while i < 10:
            stats.append(addr + i)
            i+=1
        return stats

    def getSkillListLoc(self, statArrayAddr:list)->int:
        MAXINT = 255
        location = statArrayAddr[1]<< MAXINT.bit_length() | statArrayAddr[0] + 0x30000
        return location

    def getName(self, addr:int)->list:
        name = []
        i=0
        while i < 8:
            name.append(addr + i)
            i+=1
        return name

    # def lockInfo(MAXINT:int, rom:mmap) -> mmap:
    #     i=0x2c032
    #     while i <= 0x2c183:
    #         if (rom[i] + 11) > MAXINT:
    #             carryOver = rom[i]
    #             carryOver +=11
    #             carryOver -=256
    #             rom[i] = carryOver
    #             i+=1
    #             rom[i]+=1
    #         else:
    #             rom[i]+=11
    #         i+=1

    #     lock0 = [0xBE, 0xEB, 0x87, 0xF5, 0x06, 0x9E, 0xFF, 0xB4, 0xF5, 0x2C, 0x06, 0x1A, 0x03, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #Exit, but lets repurpose this for Ashura
    #     lock1 = [0xC4, 0xDC, 0x77, 0xFF, 0xC1, 0x75, 0xD7, 0xF5, 0x06, 0x9E, 0xB2, 0xB4, 0xF5, 0x2C, 0x06, 0x1A, 0x17, 0x19, 0x01, 0x10, 0x00, 0x19, 0x00, 0x2F, 0x00] #Ki's Head
    #     lock2 = [0xCF, 0xD4, 0xDF, 0x6A, 0x67, 0xD4, 0xF5, 0x06, 0x9E, 0xB6, 0xB8, 0xF5, 0x2C, 0x06, 0x1A, 0x43, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #Valhalla
    #     lock3 = [0xC1, 0x55, 0x80, 0xF5, 0x06, 0x9E, 0xB1, 0xB8, 0xF5, 0x2C, 0x06, 0x1A, 0x11, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #House
    #     lock4 = [0xC0, 0xDC, 0x59, 0xE7, 0x77, 0xFF, 0xD0, 0x66, 0xDF, 0xD7, 0xF5, 0x06, 0x9E, 0xB1, 0xB5, 0xF5, 0x2C, 0x06, 0x1A, 0x0E, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #Giant's World
    #     lock5 = [0xBA, 0xE3, 0xE2, 0x67, 0xE2, 0x77, 0xFF, 0xD0, 0x66, 0xDF, 0xD7, 0xF5, 0x06, 0x9E, 0xB2, 0xB5, 0xF5, 0x2C, 0x06, 0x1A, 0x18, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #Apollo's World
    #     lock6 = [0xC0, 0xE8, 0x6E, 0xD7, 0xDC, 0x59, 0x77, 0xFF, 0xBB, 0x89, 0xD8, 0xF5, 0x06, 0x9E, 0xB3, 0xB5, 0xF5, 0x2C, 0x06, 0x1A, 0x22, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #Guardian's Base
    #     lock7 = [0xC7, 0x56, 0xDD, 0xD4, 0xF5, 0x06, 0x9E, 0xB3, 0xB9, 0xF5, 0x2C, 0x06, 0x1A, 0x26, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #ninja
    #     lock8 = [0xCF, 0x8B, 0x8E, 0xEE, 0xFF, 0xD0, 0x66, 0xDF, 0xD7, 0xF5, 0x06, 0x9E, 0xB4, 0xB1, 0xF5, 0x2C, 0x06, 0x1A, 0x29, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #Venus' World
    #     lock9 = [0xCB, 0xD4, 0xD6, 0x4E, 0xD0, 0x66, 0xDF, 0xD7, 0xF5, 0x06, 0x9E, 0xB5, 0xB9, 0xF5, 0x2C, 0x06, 0x1A, 0x3A, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #Race World
    #     locka = [0xBE, 0xD7, 0xE2, 0xF5, 0x06, 0x9E, 0xB6, 0xB3, 0xF5, 0x2C, 0x06, 0x1A, 0x3E, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #edo
    #     lockb = [0xC7, 0x89, 0xE7, 0x72, 0xBD, 0xE8, 0x6B, 0xD8, 0x65, 0xF5, 0x06, 0x9E, 0xB6, 0xB7, 0xF5, 0x2C, 0x06, 0x1A, 0x42, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #nasty dungeon
    #     lockc = [0xBC, 0x8B, 0xE7, 0x82, 0x96, 0xC9, 0xDC, 0x67, 0x6E, 0xF5, 0x06, 0x9E, 0xFF, 0xB1, 0xF5, 0x2C, 0x06, 0x1A, 0x00, 0x19, 0x01, 0x37, 0x00, 0x19, 0x00, 0x2F, 0x00] #central pillar

        #j=0x2ca18
        #while j <= 0x2eae0:


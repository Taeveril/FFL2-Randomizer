import mmap

class GameUtility:

    def titlePatch(vers:float, seed:int, rom:mmap) -> mmap:
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

        titleUpdate = GameUtility.infoPatchList(vers, seed)
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

    def infoPatchList(vers:float, seed:int) -> list:
        finalList = [0x36, 0x03, 0xCB, 0x59, 0xD7, 0x81, 0xDC, 0xED, 0x53, 0xFF] #"Randomizer "
        finalList.extend(GameUtility.hexList(str(vers), 4))
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






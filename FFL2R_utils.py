import mmap

class GameUtility:

    def scriptPatch(rom:mmap) -> mmap:
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






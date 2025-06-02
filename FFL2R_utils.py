def create(dict1, bytes1):
    i=0
    while i*2 < len(bytes1):
        dict1.update({ hex(i) : bytes1[i*2:i*2+2].upper() })
        i+=1
    return dict1

def scriptPatch(dict1):
    i=180224
    insertion = []
    while i <= 190992:
        if i >= 180224 and i <= 180606 and i % 2 == 0:
        # this can probably be generalized if there's more bit overflow with additional scripts
        # but right now it only happens once so it's done by hardcoding
            if dict1[hex(i)] == b"FF":
                dict1.update({ hex(i) : b"03" })
                i+=1
                dict1.update({ hex(i) : b"53" })
            else:
                dict1.update({ hex(i) : bytes(hex(int((dict1[hex(i)]),16)+4)[2:].zfill(2).upper(), encoding='utf-8') })
    # insertion of new scripts
    # Ashura, Venus, and Odin all use the same drop script (one of each MAGI), with Venus + Odin dropping Aegis / Masmune in the post-battle script.
    # To increase randomization possibilities, new scripts for Ashura and Venus have been added.
    # Odin keeps the original script. All non-TrueEye MAGI can be randomized.
        elif i >= 180607 and i <= 190948:
            insertion.append(dict1[hex(i)])
            if i == 180607 or i == 180609:
                dict1.update({ hex(i) : b"69" })
            elif i == 180608:
                dict1.update({ hex(i) : b"E5" })
            elif i == 180610:
                dict1.update({ hex(i) : b"FB" })
            else:
                dict1.update({ hex(i) : insertion[0] })
                insertion.pop(0)
        # Ashura's new custom MAGI drop script
        elif i >= 190949 and i<=190969:
            match i % 3:
                case 0:
                    dict1.update({ hex(i) : b"0A" })
                case 1:
                    dict1.update({ hex(i) : b"09" })
                case 2:
                    dict1.update({ hex(i) : b"19" })
        elif i == 190970:
            dict1.update({ hex(i) : b"00" })
            dict1.update({ hex(167643) : b"C0"}) #0x28edb
            # Venus' new custom MAGI drop script
        elif i >= 190971 and i<=190991:
            match i % 3:
                case 0:
                    dict1.update({ hex(i) : b"19" })
                case 1:
                    dict1.update({ hex(i) : b"0A" })
                case 2:
                    dict1.update({ hex(i) : b"09" })   
        elif i == 190992:
            dict1.update({ hex(i) : b"00" })
            dict1.update({ hex(183409) : b"C1"}) #addr +4 offset #0x2cc71
        i+=1
    return dict1

def safeUnlocks(dict1):
    # All MAGI checks are an invisible npc that otherwise halts the player if they fail to meet the requirement -- "We need more MAGI to open this door!"
    # this can put the player in a rough state if the player Teleports/Pegasus/ItemDoor's to a world where they cannot escape, usually happens when 
    # Apollo steals MAGI. This function makes it so that once the magi check passes, the NPC vanishes and does not respawn.
    # Functionally, all these checks use script variable 16. The "opened" script increments the variable, pulls the player through into the door,
    # and then decrements the variable. This edits the script not decrement while putting a max var on these NPCs so they do not respawn.
    doorLocks = {
        0x1cc66 : b"01", #to giant world
        0x1ce42 : b"02", #giant house
        0x1ce5d : b"04", #to apollo world
        0x1cf54 : b"03", #to Ki's head, wholly unnecessary but nice to be consistent
        0x2cade : b"05", #   these are not unlocks but changes the script variables for Ki's MAGI from using 16 to 5, the TrueEye MAGI plot event. 
        0x2caf1 : b"05", #   Again kind of unnecessary, but just cleaning up Script Variable 16 to be consistent.
        0x1cfd8 : b"05",
        0x1d015 : b"05", #to guardian world
        0x1d336 : b"06", #to ninja world
        0x1d54e : b"07", #to venus world
        0x1d5b4 : b"08", #to race world
        0x1d963 : b"09", #to edo
        0x1db45 : b"0A", #to nasty dungeon world
        0x1df1e : b"0B", #to valhalla
        0x1e078 : b"0C", #to central world
        0x1e091 : b"0A" #back to valhalla. Maybe a bug since it checks for 66 Magi (to Edo) which is script 76, rather than 76 MAGI; but all irrelevant since it's meant to block you into final world.
        }

    for key, value in doorLocks.items():
        dict1.update({hex(key) : value})

    i=180320
    while i<=180611:
        if i % 2 == 0:
            dict1.update({ hex(i) : bytes(hex(int((dict1[hex(i)]),16)-2)[2:].zfill(2).upper(), encoding='utf-8') })
        i+=1

    j=183532
    while j<= 190992:
        dict1.update({ hex(j) : dict1[hex(j+2)]})
        j+=1

    return dict1







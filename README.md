# Final Fantasy Legend 2 Randomizer

## Features:
- Treasure shuffle.
- Magi shuffle.
- Shop shuffle.
- Starting monsters randomized.
- World shuffle.
- QoL Features:
  - Empty chests will appear open.
  - Encounter rate adjustment.
  - Gold drop adjustment.
  - Central pillar worlds stay unlocked once MAGI threshold met.
  - Double movement speed.
  - Default fast text speed.
  - Mr. S will no longer block the first cave entrance upon completion.
  - Better stat growth.
  - NPCs added to help access one-time or limited-time areas.
  - Game bug fixes:
    - Gold/Meat/Item drops now calculate correctly.
    - Elemental MAGI behaves appropriately.
    - Mana MAGI affinity enabled.
    - Mutant stat growth behaves as expected.
    - Dooring/Pegasus/Teleporting during the race will now force a dismount.

## Version 2.0.0 (1/11/2026):
- Rewrote entire codebase again, trying to adopt pythonic principles...sort of.
- Redid Final Shop logic. The NPC will now appear after world completion.
- Lowered the price of Selfix from 50,000 to 25,000
- Fixed a bug where the Key in Venus' world was not required to open doors.
- Fixed a bug where the teleport unlock for Ashura's World would set to an incorrect value.
- Fixed a bug where uring teleport would remove the guest character.

## How to:
- Download the Python scripts (and install Python if you don't have it).
- Run FFL2R.py
- Will prompt for a GB ROM, seed, encounter rate.
  - will also take command line arguments -s for seed, -r for rom path, and -e for encounter rate.
- Will generate a ROM.

## Credits and thank yous:
This project really stands on the shoulders of giants. Over two decades of people poking and
mapping the ROM have made this possible.

- tehtmi - Author of Saga2Edit: https://www.romhacking.net/utilities/1546/ and for answering questions.
- Amuseum - Building spreadsheets filled with relevant data. (https://www.geocities.ws/kattdood/ffl2/ffl2.htm,
  other domain shenafu has been lost to time but findable on archive.org)
- Alex Jackson - Gamefaqs poster that originally dove into hexediting the ROM.
- Friends Destil and Treble, for contributing and listening.

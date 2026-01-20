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

## Version 2.1.0 (1/19/2026):
- Added an "open world" option to the randomizer. Generating seeds will now require an input on how worlds should be shuffled (-w).
- Fixed an issue where teleporting during Guardian Base could break logic and put players in a bad state.
- Made it so teleporting to Guardian Base will now check where you are in that world's progression.

## How to:
- Download the Python scripts (and install Python if you don't have it).
- Run FFL2R.py
- Will prompt for a GB ROM, seed, encounter rate, and world mode.
  - will also take command line arguments -s for seed, -r for rom path, -e for encounter rate, -w for world mode.
- Will generate a ROM.

## Credits and thank yous:
This project really stands on the shoulders of giants. Over two decades of people poking and
mapping the ROM have made this possible.

- tehtmi - Author of Saga2Edit: https://www.romhacking.net/utilities/1546/ and for answering questions.
- Amuseum - Building spreadsheets filled with relevant data. (https://www.geocities.ws/kattdood/ffl2/ffl2.htm,
  other domain shenafu has been lost to time but findable on archive.org)
- Alex Jackson - Gamefaqs poster that originally dove into hexediting the ROM.
- Friends Destil and Treble, for contributing and listening.

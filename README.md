# Final Fantasy Legend 2 Randomizer

## Features:
- Treasure shuffle.
- Magi shuffle.
- Shop shuffle.
- Starting monsters randomized.
- QoL Features:
  - Empty chests will appear open.
  - Encounter rate adjustment.
  - Gold drop adjustment.
  - Central pillar worlds stay unlocked once MAGI threshold met.
  - Double movement speed.
  - Default fast text speed.
  - Game bug fixes:
    - Elemental MAGI behaves appropriately.
    - Mana MAGI affinity enabled.
    - Mutant stat growth behaves as expected.


## Version 0.6.0 (6/28/2025):
- Randomized monsters in the starting character select screen. Will also show hidden DS level to give players an idea of how good they are at the start.
- Text speed will default to fastest, pressing a button unnecessary.
- Fixed an issue where encounter rate adjustment would create a game-fatal treasure chest in the Nasty Dungeon if interacted with.

## How to:
- Download the Python scripts (and install Python if you don't have it).
- Run FFL2R.py
- Will prompt for a GB ROM, seed, encounter rate.
  - will also take command line arguments -s for seed, -r for rom path, and -e for encounter rate.
- Will generate a ROM.

## Plans:
- World randomizer.
- Ttrying to fix the if meats drop then no additional gold bug.
- Increase growth chance for humans/mutants.

## Credits and thank yous:
This project really stands on the shoulders of giants. Over two decades of people poking and
mapping the ROM have made this possible.

- tehtmi - Author of Saga2Edit: https://www.romhacking.net/utilities/1546/ and for answering questions.
- Amuseum - Building spreadsheets filled with relevant data. (https://www.geocities.ws/kattdood/ffl2/ffl2.htm,
  other domain shenafu has been lost to time but findable on archive.org)
- Alex Jackson - Gamefaqs poster that originally dove into hexediting the ROM.
- Friends Destil and Treble, for contributing and listening.

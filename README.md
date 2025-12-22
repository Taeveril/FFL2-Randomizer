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

## Version 0.9.1 (12/22/2025):
- Teleport unlocks have been fixed.
- Fixed a bug where a world shuffle could cause Apollo not to appear in his world.
- Fixed an issue where new scripts with yes/no prompts would require a button press to advance rather than automate.
- Added Guardians to Valhalla that will teleport you to the other pillar once Odin is defeated.
- Prism magi count is a lot harder to fix. Turns out that magi checks a number against your total magi count to give the appearance of telling you how many magi are left in the world.
  - Its fixable, but remains as a known bug for now as Prism usage is not mandatory to complete the game.

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

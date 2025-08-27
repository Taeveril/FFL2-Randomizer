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
  - Mr. S will no longer block the first cave entrance upon completion.
  - Better stat growth.
  - Game bug fixes:
    - Gold/Meat/Item drops now calculate correctly.
    - Elemental MAGI behaves appropriately.
    - Mana MAGI affinity enabled.
    - Mutant stat growth behaves as expected.
    - Dooring/Pegasus/Teleporting during the race will now force a dismount.

## Version 0.7.3 (8/27/2025):
   - The Race has been reworked:
      - If you teleport/door out during the race, you will now be dismounted.
      	- The dragon will remain on the track when you return.
        - It is not encouraged to switch mounts while racing, or you could end up with off-magi counts or other weirdness.
      - When returning, dragon availability will depend on which magi have been acquired.
   - Fixed the graphical issue introduced with the movement speed boost.


## How to:
- Download the Python scripts (and install Python if you don't have it).
- Run FFL2R.py
- Will prompt for a GB ROM, seed, encounter rate.
  - will also take command line arguments -s for seed, -r for rom path, and -e for encounter rate.
- Will generate a ROM.

## Plans:
- World randomizer.

## Credits and thank yous:
This project really stands on the shoulders of giants. Over two decades of people poking and
mapping the ROM have made this possible.

- tehtmi - Author of Saga2Edit: https://www.romhacking.net/utilities/1546/ and for answering questions.
- Amuseum - Building spreadsheets filled with relevant data. (https://www.geocities.ws/kattdood/ffl2/ffl2.htm,
  other domain shenafu has been lost to time but findable on archive.org)
- Alex Jackson - Gamefaqs poster that originally dove into hexediting the ROM.
- Friends Destil and Treble, for contributing and listening.

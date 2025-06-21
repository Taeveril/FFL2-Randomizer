# Final Fantasy Legend 2 Randomizer

## Features:
- Treasure shuffle.
- Magi shuffle.
- Shop shuffle.
- QoL Features:
  - Empty chests will appear open.
  - Encounter rate adjustment.
  - Gold drop adjustment.
  - Central pillar worlds stay unlocked once MAGI threshold met.
  - Game bug fixes:
    - Elemental MAGI behaves appropriately.
    - Mana MAGI affinity enabled.
    - Mutant stat growth behaves as expected.


## Version 0.5.0 (6/21/2025):
- Gold rate adjustment introduced. Will prompt for a number between 50-500 and will turn into a percentage to adjust.
   - Gold will currently cap at 65535. 10% bonus for all monsters defeated still there.
   - Have not yet fixed the meat/gold drop bug. Learning assembly (and translating it to hex) as fast as I can to try and get this fixed.
- The Magi Leon steals from you will now appropriately display.
- Fixed an issue where the title screen may not always show the seed number.

## Version 0.4.0 (6/14/2025):
- Encounter rate adjustment introduced. Will prompt for a number between 20-200 and will turn into a percentage to adjust.
- Title screen will now display version and seed.
- Misc bug cleanup:
  - Retroduced seed inconsistency by accident.
  - Fixed issue where some treasure items and locations were referenced more than once.

## How to:
- Download the Python scripts (and install Python if you don't have it).
- Run FFL2R.py
- Will prompt for a GB ROM, seed, encounter rate.
  - will also take command line arguments -s for seed, -r for rom path, and -e for encounter rate.
- Will generate a ROM.

## Plans:
- Increase gold drops.
  - This includes trying to fix the if meats drop then no additional gold bug.
- Increase growth chance for humans/mutants.
- Movement speed increase.

## Credits and thank yous:
This project really stands on the shoulders of giants. Over two decades of people poking and
mapping the ROM have made this possible.

- tehtmi - Author of Saga2Edit: https://www.romhacking.net/utilities/1546/
- Amuseum - Building spreadsheets filled with relevant data. (https://www.geocities.ws/kattdood/ffl2/ffl2.htm,
  other domain shenafu has been lost to time but findable on archive.org)
- Alex Jackson - Gamefaqs poster that originally dove into hexediting the ROM.
- Friends Destil and Treble, for contributing and listening.

### Complete version history

#### Version 0.3.2 (6/11/2025):
- Yet Even More code cleanup. Maybe someday I'll be a proper engineer. Today is not that day.
- Mutant stat growth in-game bug fixed.

#### Version 0.3.1 (6/9/2025):
- Further code cleanup.
- Fixed some in-game bugs related to MAGI:
  - Elemental MAGI all work how they're expected.
  - Mana MAGI affinity has been enabled.

#### Version 0.3.0 (6/2/2025):
- When you break a door locked by magi, it is permanent (will be optionized in the future). No more potentially getting stuck when Apollo steals your magi.
- Slight code cleanup.

#### Version 0.2.0 (5/27/2025):
- Shop rando is completed (Thanks Treble!).

#### Version 0.1.3 (5/24/2025):
- Fixed issue with seeding not producing consistent results.

#### Version 0.1.2 (5/23/2025):
- Treasure Chests, if empty, will be open.
- Some code cleanup, improvements.

#### Version 0.1.1 (5/22/2025):
- Cleaned up some usability issues (Thanks Destil!).

#### Version 0.1.0 (5/21/2025):
- Initial commit

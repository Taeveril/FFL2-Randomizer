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

Known issue: Race sequence will be graphically odd, but does not do anything adverse. Fixed by simply dismounting/remounting the dragon for each leg. 

## Version 0.7.2 (8/9/2025):
- Some more quality of life bugfixing (thank you tehtmi!):
	-	Gold will now calculate correctly when multiple groups of enemies are defeated and meat/an item drops.
	-	Multiple stats can grow after battle for a single character.
			- The chance to grow has also drastically increased.
			- The chance for mutants to change skills has also slightly increased.
-	Will now check for a correct rom.


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

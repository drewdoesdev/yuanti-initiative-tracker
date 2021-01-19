# Yuanti Initiative Tracker 

**Version 1.0.0**

Yuanti is a lightweight,  command line initiative  tracker for 5e written in python.  

## How to use

- Download this repository and, in the encounter.txt file, list your encounter info in the following format, each on a new line:
    - {pc for player charaters or allies, or mon for monsters},{Name},{initiative modifier if monster},{*optional*: True if the monster has Advantage}
- Run the script with the following command: 
    - ```python {Your Path}/app.py```
- The app will ask for your player's initiative rolls, then it will randomly generate the monster's initiative.

## Commands
- **n (next)**: Moves to next line in initiative
- **d (damage) {Name}**: Adds to the monster or PC's running Damage total.
- **k (kill) {Name}**: Crosses the specified combatant's name in initiative, inidicating that the are unconcious.
- **x (exit)**: Ends initiatiative and exits application 
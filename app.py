import random
from pathlib import Path

class Character:
    def __init__(self, name):
        self.name = name
        self.initiative = -1
        self.health = 0
        self.isDead = False

class Monster:
    def __init__(self, name, initModifier, hasAdvantage=False):
        self.name = name
        self.initiative = rollInitiative(initModifier, hasAdvantage)
        self.health = 0
        self.isDead = False

def printLogo():
    logo = """                                                                                                                           
    ______      _ _   _____      _ _   _       _   _           
    | ___ \    | | | |_   _|    (_) | (_)     | | (_)          
    | |_/ /___ | | |   | | _ __  _| |_ _  __ _| |_ ___   _____ 
    |    // _ \| | |   | || '_ \| | __| |/ _` | __| \ \ / / _ \\
    | |\ \ (_) | | |  _| || | | | | |_| | (_| | |_| |\ V /  __/
    \_| \_\___/|_|_|  \___/_| |_|_|\__|_|\__,_|\__|_| \_/ \___|

    """               
    print(logo)              


def printVictory():
    text = """
     _   _ _      _                   _ 
    | | | (_)    | |                 | |
    | | | |_  ___| |_ ___  _ __ _   _| |
    | | | | |/ __| __/ _ \| '__| | | | |
    \ \_/ / | (__| || (_) | |  | |_| |_|
     \___/|_|\___|\__\___/|_|   \__, (_)
                                __/ |  
                                |___/   
    
    """
    print(text)

def strike(text):
    i = 0
    new_text = ''
    while i < len(text):
        new_text = new_text + (text[i] + u'\u0336')
        i = i + 1
    return(new_text)

def printInitiative(initiative):
    for turn in range(len(initiative)):
        line = ""
        if initiative[turn].isDead:
            line = strike(initiative[turn].name + " - " + str(initiative[turn].initiative))
        else:    
            if turn == currentTurn:
                line = "\033[1m\033[4m" + initiative[turn].name + " - " + str(initiative[turn].initiative) + " - " + '\033[91m' + str(initiative[turn].health) + "\033[0m"
            else:
                line = initiative[turn].name + " - " + str(initiative[turn].initiative) + " - " + '\033[91m' + str(initiative[turn].health) + "\033[0m"
        
        print(line)

    print("\n\n")


def rollInitiative(mod, hasAdvantage):
    modifier = int(mod)
    if(hasAdvantage == True):
        diceRolls = [random.randint(1,20), random.randint(1,20)].sort()
        return diceRolls[0] + modifier
    else:
        diceRoll = random.randint(1, 20)
        return diceRoll + modifier

def setPartyInitiative(party):
    print("Enter your party's initiative as they appear")
    for character in party:
        while character.initiative == -1:
            initiative = input(character.name + ": ")
            character.initiative = int(initiative)

    return party


def adjustHealth(currentInitiative, effectedCharacter, damageToAdd):
    for combatant in currentInitiative:
        if(combatant.name == effectedCharacter):
            combatant.health += damageToAdd
    
    return currentInitiative

def adjustDeath(currentInitiative, effectedCharacter, newVal):
    for combatant in currentInitiative:
        if(combatant.name == effectedCharacter):
            combatant.isDead = newVal
    
    return currentInitiative

#init
isRunning = True

printLogo()

party = []
monsters = []

filePath = Path(__file__).parent / "encounter.txt"
with filePath.open() as f:
    for line in f:
        parsedLine = line.rstrip('\n').split(",")
        parsedLine[1]
        if(parsedLine[0] == "pc"):
            character = Character(parsedLine[1])
            party.append(character)
        elif(parsedLine[0] == "mon"):
            hasAdvantage = False
            try:
                hasAdvantage = parsedLine[3]
            except  IndexError:
                hasAdvantage = False
            monster = Monster(parsedLine[1], parsedLine[2], hasAdvantage)
            monsters.append(monster)

rolledParty = setPartyInitiative(party)

initiative = rolledParty + monsters

initiative.sort(key=lambda x: x.initiative, reverse=True)

currentTurn = 0
currentRound = 1
while isRunning == True:
    print("\n\n == Round " + str(currentRound) + " ==")
    print("\nInitiative")
    print("--------------")

    printInitiative(initiative)

    nextCommand = input("Enter 'n' to continue initiative.  Enter 'x' to end combat: ")
    if nextCommand == 'n': #Next
        if currentTurn + 1 == len(initiative):
            currentTurn = 0
            currentRound += 1
        else:
            currentTurn += 1
    elif nextCommand[0] == 'd': #Damage
        commands = nextCommand.split(' ')
        initiative = adjustHealth(initiative, commands[1], int(commands[2]))
    elif nextCommand[0] == 'k': #Kill
        commands = nextCommand.split(' ')
        initiative = adjustDeath(initiative, commands[1], True)
    elif nextCommand[0] == 'r': #Resurect
        commands = nextCommand.split(' ')
        initiative = adjustDeath(initiative, commands[1], False)
    elif nextCommand == 'x':  #Exit
        isRunning = False
        printVictory()
    else:
        print("\nInvalid command.  enter 'h' for a list of commands.\n")
# following should be ordered in a txt, read by computer to set up a dictionary
# (tuple(string bodypart,int hardness)-> tuple waysofstimulation)
# => > import json <

# better list of dictionaries
# [{'name':'Hand','active':True,'softStimulation'=[...],'strong...},{...},...]

# chooses an action that fits on both body parts

import random  # REQUIRED for random.choice()

parts = {}
activeParts = {}
passiveParts = {}
players = []


# reading the extern file of included items
def reading():
    print('Insert a .txt-file name (without ending) of a file inside the folder of spoongame.')
    print('Or just press >enter<')
    fileName = input()

    if fileName == '':  # default file name
        fileName = 'action2'

    try:
        file = open(fileName + '.txt')
        document = file.readlines()
        file.close()
    except:
        print('Opening of actions.txt failed')
        return

    for documentLine in document:
        try:
            partRead(documentLine)
        except SyntaxError:
            print('Syntax Error in following:')
            print(documentLine)
            print()
        except:
            print('File reading went wrong.')
            print('Error at:')
            print(documentLine)
            print()
    print(f'Reading data file <{fileName}.txt> was successful.')
    input()


def partRead(line):
    if line.startswith('#') or line == '\n':  # ignore comments and empty lines
        return

    elif ':' in line:  # headline
        headline = line.split(':')[0]
        parts.update({headline: {}})

    elif '(' in line:  # content
        if not parts:
            print('parts is still empty.')
            raise SyntaxError

        if '#' in line:
            line = line.split('#')[0]

        headline = list(parts.keys())[-1]

        items = line.split(';')
        for item in items:
            itemName = item.split('(')[0].strip()
            itemActions = (
                item.split('(')[1]
                .replace(')', '')
                .replace('\n', '')
                .split(',')
            )
            itemActions = [a.strip() for a in itemActions]
            parts[headline].update({itemName: itemActions})

    else:
        raise SyntaxError


def begin():
    for _ in range(30):
        print()

    print(' _____ ')
    print(' _______________/ \\ ')
    print(' / XX \\ ')
    print(' \\___________XX__ ) ')
    print(' \\_____/ ')
    print()

    print(' Welcome to the Spoongame!')
    for _ in range(6):
        print()
    input()

    print('You will need a spoon for it.')
    input()

    print('...and maybe some other stuff.')
    input()

    print('You have to be at least two persons.')
    input()

    print('...or just pretend this, it´s just a dumb computer.')
    input()

    print('All genders and body forms are welcome.')
    input()

    print('Be careful, aware and look for each other.')
    input()

    print('Remember: This is a game.')
    input()


def menu(players, parts, activeParts, passiveParts):
    print('MENU:')
    print('-----------------------------------------------')
    print('>S< Start the game')
    print('>P< add new Players')
    print('>R< Remove a player')
    print('>I< choose Interactions')
    print('>T< add a Tool')
    print('>X< Refresh all settings')
    print('>Q< Quit')
    print()

    choice = input().casefold()

    if choice.startswith('s'):
        game(players, activeParts, passiveParts, '')
    elif choice.startswith('p'):
        players = setNames(players)
        menu(players, parts, activeParts, passiveParts)
    elif choice.startswith('r'):
        players = removePlayer(players)
        menu(players, parts, activeParts, passiveParts)
    elif choice.startswith('i'):
        activeParts, passiveParts = setInteractions(parts)
        menu(players, parts, activeParts, passiveParts)
    elif choice.startswith('t'):
        activeParts = setTool()
        menu(players, parts, activeParts, passiveParts)
    elif choice.startswith('x'):
        parts, activeParts, passiveParts = refresh(parts, activeParts, passiveParts)
        menu(players, parts, activeParts, passiveParts)
    elif choice.startswith('q'):
        return
    else:
        print('Please retry.')
        menu(players, parts, activeParts, passiveParts)


def game(players, activeParts, passiveParts, lastPlayer):
    try:
        if len(players) < 2:
            print('There are not enough players chosen. Please get or imagine a friend.')
            print('')
            menu(players, parts, activeParts, passiveParts)

        if not parts:
            print('<parts> is empty. Please refresh.')
            input()
            raise ValueError

        elif not passiveParts or not activeParts:
            print('There are no active parts or no passive parts chosen. There must be both.')
            print('Please do this first!')
            menu(players, parts, activeParts, passiveParts)
            return

        activePlayer = random.choice(players)
        passivePlayer = random.choice(players)

        if activePlayer == passivePlayer or activePlayer == lastPlayer:
            if activeParts and passiveParts:
                game(players, activeParts, passiveParts, lastPlayer)
            return

        if activeParts:
            activeItem = random.choice(list(activeParts.keys()))
        else:
            print('There are no active parts chosen.')
            input('Press enter to continue.')
            menu(players, parts, activeParts, passiveParts)
            return

        if passiveParts:
            passiveItem = random.choice(list(passiveParts.keys()))
        else:
            print('There are no passive parts chosen.')
            input('Press enter to continue.')
            menu(players, parts, activeParts, passiveParts)
            return
            
        possibleActions = list(
            set(activeParts[activeItem]) & set(passiveParts[passiveItem])
        )

        if not possibleActions:
            game(players, activeParts, passiveParts, lastPlayer)
            return

        action = random.choice(possibleActions)

        print()
        print(f'{activePlayer}, would you like to {action} '
              f'{passivePlayer}´s {passiveItem} with your {activeItem}?')
        print()
        print(f'{passivePlayer}, are you ok with it?')
        print()

        quit=input().casefold()
        if quit.startswith('m'):
            menu(players, parts, activeParts, passiveParts)
            return
        elif quit.startswith('q'):
            return
            
        if activeParts and passiveParts:
            game(players, activeParts, passiveParts, activePlayer)

    except ValueError:
        menu(players, parts, activeParts, passiveParts)
    except:
        print('Something went wrong.')
        print(Exception)
        input('Press enter to continue.')
        menu(players, parts, activeParts, passiveParts)


def setNames(players):
    printPlayers(players)

    try:
        while True:
            print('Name of new Player or press >return< when done:')
            newPlayer = input()
            if newPlayer:
                players.append(newPlayer)
                printPlayers(players)
            else:
                break

        if len(players) < 2:
            raise ValueError

        if players[0] == players[1]:
            raise KeyError

    except ValueError:
        print('There are not enough players.')
        setNames(players)

    except KeyError:
        print('Players must have different names.')
        players.pop()
        #players = [players[0]]
        setNames(players)

    return players


def removePlayer(players):
    printPlayers(players)
    if not players:
        return players

    print('Which player number should leave?')
    try:
        playnum = int(input())-1
        if 0 <= playnum < len(players):
            players.pop(playnum)
    except:
        print('No player removed')
    printPlayers(players)
    return players


def setInteractions(parts):
    activeParts = {}
    passiveParts = {}

    for category in parts:
        print(f'Do you like to use {category.title()}?')
        wish = input().casefold()
        if wish.startswith('y'):
            print('Category chosen.')
            print()
            if category.startswith('active'):
                for item in parts[category]:
                    activeParts.setdefault(item, []).extend(parts[category][item])
            else:
                for item in parts[category]:
                    passiveParts.setdefault(item, []).extend(parts[category][item])
        else:
            print("This won't bother you.")
    input('Interaction items are chosen.')
    return activeParts, passiveParts


def setTool():
    print('What is your added tool?')
    toolName = input()
    toolActions = []

    print('What actions can it perform? (empty line to finish)')
    while True:
        action = input()
        if not action:
            break
        toolActions.append(action)

    activeParts[toolName] = toolActions
    return activeParts


def refresh(parts, activeParts, passiveParts):
    print('Do you want to refresh data?')
    answer = input().casefold()

    if answer in 'yes':
        parts.clear()
        activeParts.clear()
        passiveParts.clear()
        reading()

    return parts, activeParts, passiveParts


def printPlayers(players):
    if not players:
        print('At the moment there are no players chosen.')
    else:
        for i, p in enumerate(players):
            print(f'Player number {i+1} is {p}.')
    print()

def credits():
    print()
    print('I hope, that was fun. If not, do something else!')
    print('If you found some bugs, feel free to improve the code.')
    print('Improve the code anyway if you want or give it to a coding nerd.')
    print('Thank for the nerds on earth! They are great and keep it running.')
    print('Thanks for Errno Lokkila, of Turun Yliopista, who teached me coding python.')
    print('This game started as "Interaction Game" in his coding course in 2024.')
    

# main program
reading()
begin()
menu(players, parts, activeParts, passiveParts)
credits()

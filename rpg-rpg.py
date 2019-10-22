#!/bin/python3
import random
# Replace RPG starter project with this code when new instructions are live


def showInstructions():
    # print a main menu and the commands
    print('''

RPG Game
========
Get to the garden with the key and the potion
Avoid the evil schmubbel!
Commands:
  go [direction]
  get [item]
''')


# player stats:
player = {
    'health': 20,
    'attack': 10,
    'defence': 10
    }


def showStatus():
    # print the player's current status
    print('---------------------------')
    print('You are in the ' + currentRoom)
    # print the current inventory
    print('Inventory : ' + str(inventory))
    # print an item if there is one
    if "item" in rooms[currentRoom]:
        print('You see a ' + rooms[currentRoom]['item'])
    print("---------------------------")


# initialise monster
def initMonster(HP, ATK, DEF):
    Monster = {
        'health': HP,
        'attack': ATK,
        'defence': DEF
        }
    return(Monster)


# an inventory, which is initially empty
inventory = []

# a dictionary linking a room to other rooms
rooms = {

            'Hall': {
                'south': 'Kitchen',
                'west': 'Dining Room',
                'east': 'Living Room',
                'north': 'Chamber'
                },
            'Chamber': {
                'south': 'Hall',
                'item': 'sword'
                },
            'Living Room': {
                'west': 'Hall',
                'item': 'map'
                },
            'Kitchen': {
                'north': 'Hall',
                'item': 'monster'
                },
            'Dining Room': {
                'east': 'Hall',
                'south': 'Garden',
                'item': 'potion'
                },
            'Garden': {
                'north': 'Dining Room'
                }

         }

# house map
map = '''
      \tCh\t  \n
      \t||\t  \n
    Di----Lr\n
    ||\t||\t  \n
    Ga\tKi\t  \n
    '''
# start the player in the Hall
currentRoom = 'Hall'

showInstructions()

# loop forever
while True:

    showStatus()

    # get the player's next 'move'
    # .split() breaks it up into an list array
    # eg typing 'go east' would give the list:
    # ['go','east']
    move = ''
    while move == '':
        move = input('>')

    move = move.lower().split()

    # if they type 'go' first
    if move[0] == 'go':
        # check that they are allowed wherever they want to go
        if move[1] in rooms[currentRoom]:
            # set the current room to the new room
            currentRoom = rooms[currentRoom][move[1]]
            # there is no door (link) to the new room
        else:
            print('You can\'t go that way!')

    # if they type 'get' first
    if move[0] == 'get':
        # if the room contains an item, and the item is the one they want to get
        if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
            # add the item to their inventory
            inventory += [move[1]]
            # display a helpful message
            print(move[1] + ' got!')
            # delete the item from the room
            del rooms[currentRoom]['item']
            # otherwise, if the item isn't there to get
        else:
            # tell them they can't get it
            print('Can\'t get ' + move[1] + '!')

    # if they type 'use' first
    if move[0] == 'use':
        if move[1] == 'map' and 'map' in inventory:
            print(map)

        elif move[1] in inventory and move[1] is not 'map':
            print('you can\'t use' + move[1] + 'now!')

        else:
            print('you don\'t have that in your inventory!')

    # player loses if they they enter a room with a monster
    if 'item' in rooms[currentRoom] and 'monster' in rooms[currentRoom]['item']:
        if 'sword' in inventory:
            # fight loop
            monster = initMonster(15, 5, 5)
            fight = True
            while fight is True:
                # Players turn starts
                print('''
You stand against the monster.. what are you going to do?
Type fight to attack
Type block to defend
Type run to escape
''')
                valid = False
                action = input('>')
                if action == 'fight':
                    # player damage output varies a little bit
                    dmgOut = random.randrange(player['attack']-2, player['attack']+2, 1)
                    defOut = player['defence']
                    valid = True

                elif action == 'block':
                    defOut = player['defence']+5
                    dmgOut = 0
                    valid = True

                elif action == 'run':
                    fight = False

                elif action == quit:
                    exit()
                if valid is True:
                    # calculating damage
                    player['health'] -= abs(monster['attack'] - defOut)
                    print(defOut, monster['attack'])
                    monster['health'] -= abs(dmgOut - monster['defence'])

                    # win condition
                    if monster['health'] <= 0:
                        print('You slayed the monster! Take the loot...')
                        del rooms[currentRoom]['item']
                        inventory += ['key']
                        fight = False

                    # loosing condition
                    elif player['health'] <= 0:
                        print('The monste has won... GAME OVER!')
                        exit()

                    print('HP: ', player['health'], '\nMonster HP:', monster['health'])
                    print('---------------------------')

                # in case of invalid input
                else:
                    print('you cannot do that action')
                    print('---------------------------')

        else:
            print('The evil schmubbel has got you... GAME OVER!')
            break

    # player wins if they get to the garden with a key and a potion
    if currentRoom == 'Garden' and 'key' in inventory and 'potion' in inventory:
        print('You ecaped the house... YOU WIN!')
        break

    if move[0] == 'quit':
        exit()

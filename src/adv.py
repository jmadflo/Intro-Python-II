from room import Room
from player import Player
from item import Item

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons"),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air."""),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

# Put some items into some of the rooms to start with

room['outside'].items = [Item('ball', 'a fun spherical toy'), Item('bug', 'a creepy crawly creature'), Item('stick', 'a thin wooden rod')]
room['overlook'].items = [Item('binoculars', 'a tool for observing far away objects'), Item('mat', "a small square on the floor which can be used to clean the bottom of one's shoes")]
room['narrow'].items = [Item('torch', 'a rod with fire at the top that can be used as a portable light'), Item('coin', 'a flat round piece of metal that is used as money')]
room['treasure'].items = [Item('empty_chest', 'a container that seems to have had treasure in the past, but no longer'), Item('shard_of_glass', 'a sharp piece of glass that seems to have been part of a glass cup')]

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

player_name = input("Tell us your name!\n")

player = Player(player_name, room['outside'], [Item('phone', 'a device for communicating with others'), Item('wallet', 'a place to store money and identification')])

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.

next_step = 'not yet decided'

def room_greeting():
    print(f"-------Hey {player.name}! You are currently at the {player.current_room.name}!------\n")

room_greeting()

while True:
    print(f'{player.current_room.description}\n')

    # Print items for the current room
    room_items_names = [x.name for x in player.current_room.items]
    if len(player.current_room.items) > 0:
        print(f'The items in this room are the following: {room_items_names}\n')
    else:
        print('There are no items in this room')
    
    # Print items for the current player
    player_items_names = [x.name for x in player.items]
    if len(player.items) > 0:
        print(f'The items that you currently hold are the following: {player_items_names}\n')
    else:
        print('You have no items.')

    next_step = input(f"If you want to enter another room type: n for north, s for south, e for east, w for west, i or inventory to review your items, or q for quit.\n").split(' ')
    if len(next_step) == 1: # Move player
        direction = next_step[0]
        if direction == "n" or direction == "s" or direction == "e" or direction == "w":
            next_room = getattr(player.current_room, f"{direction}_to")
            if next_room == 'wall':
                print(f"You can't move this way. It's a wall!\n")
            else: 
                player.current_room = next_room
                room_greeting()
        elif direction == "q": # quitting
            print(f"You are a traitor {player.name}! You have made a terrible mistake in leaving. You will regret your heinous decision to leave!.")
            break
        elif direction == 'i' or direction == 'inventory':
            print(f'My items: {player_items_names}')
        else:
            print("This doesn't make sense. Try again!\n")
    elif len(next_step) == 2: # deal with items
        action = next_step[0]
        item_name = next_step[1]
        item = Item('placeholder', 'placeholder')
        if action == 'get' or action == 'take':
            for i in player.current_room.items:
                if item_name == i.name:
                    item = i
                    break
            if item == '':
                print(f'There is no {item} in this room.\n')
            elif item_name in room_items_names:
                player.current_room.items.remove(item)
                player.items.append(item)
                item.on_take()
                
        elif action == 'drop':
            for i in player.items:
                if item_name == i.name:
                    item = i
                    break
            if item == '':
                print(f'You do not have a {item_name} with you.')

            elif item.name in player_items_names:
                player.items.remove(item)
                player.current_room.items.append(item)
                item.on_drop()
    else: 
        print("This doesn't make sense. Try again!\n")
    print('\n\n -------------------- \n\n')

# Python3 adv.py
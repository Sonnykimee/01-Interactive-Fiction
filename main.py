#!/usr/bin/env python3

'''
    Important Note:
    Please DON’T run this game on VS Code. Run the game on the native OS terminal.
    I’ve experienced multiple errors on VS Code terminal that does not
    happen on the native terminal.
'''

from modules.game_helper import GameHelper
from modules.player import Player
from modules.item import Item
from modules.npc import NPC
from pathlib import Path
import sys,os,json,time, csv

class NoThankYou(Exception):
    pass


def get_script(filename, id):
    with open(Path("npc/"+ filename +".csv"), "r") as f:
        reader = csv.reader(f)
        for line in reader:
            if line[0] == id:
                return line[1]

VERSION = "0.2.0"

do_render = True # This variable determines wheter to render the world again or not.

def load(l):
    f = open(os.path.join(sys.path[0], l))
    data = f.read()
    j = json.loads(data)
    return j


def find_passage(game_desc, pid):
    for p in game_desc["passages"]:
        if p["pid"] == pid:
            return p
    return {}


def run_game():
    # Load map
    game_desc = load("game.json")
    current = find_passage(game_desc, game_desc["startnode"])

    # Show intro
    show_intro()

    # Ask user to initialize player
    player = init_player()
    npcs = {
        "oldlady": NPC("The Old Lady", 0),
        "ianne": NPC("Ianne", 0),
        "tybalt": NPC("Tybalt", 0),
        "myrce": NPC("Myrce", 0),
        "gypsy": NPC("Gypsy", 0)
    }
    
    world = {
        "Player": player,
        "Current": current,
        "Map": game_desc,
        "NPC": npcs
    }

    # Show intro
    # show_intro()

    # Game Loop
    choice = ""

    run = True
    while (run):

        if choice != "quit":
            world = update(world, choice)
            render(world)
            choice = get_input()
        else:
            # End Game Loop
            run = False


def get_input():
    '''Handles player input and returns the input.'''
    choice = input("What would you like to do?: ")
    choice = choice.lower()
    if choice in ["quit","q","exit"]:
        return "quit"
    return choice


def update(world, choice):
    global do_render

    if choice == "":
        do_render = True
        return world
    else:
        args = choice.split(" ")

        if args[0] == "goto": # Go to a place
            if len(args) == 1:
                print("Type the direction's number! ex) goto 0")
            else:
                try:
                    goto = int(args[1])

                    current = world["Current"]
                    links = current["links"]
                    p = world["Player"]

                    if (goto >= 0 and goto < len(links)):
                        
                        l = links[goto]
                        new_current = find_passage(world["Map"], l["pid"])
                        world["Current"] = new_current
                        p.talking = None
                        do_render = True

                        return world
                    else:
                        print("You have chosen an invalid path!")
                        
                except ValueError:
                    print("Cannot go there!")

        elif args[0] == "talk": # Talk to an NPC
            p = world["Player"]

            if (len(args) == 0):
                print("Type the person's name. Type \"people\" to see the people around you!")
            else:
                current = world["Current"]

                for npc_id in current["npcs"]:
                    if npc_id == args[1]:
                        npc = world["NPC"][npc_id]
                        p.talking = npc
                        print("You have selected " + npc.name + "!")
                        print(npc.name + ": " + get_script(npc_id, "100"))
                        return world
                print("You have chosen an invalid person's name. Type \"people\" to see the people around you!")
        elif args[0] == "give": # Give item to an NPC
            p = world["Player"]
            
            if (p.talking):
                if len(args) == 0:
                    print("Type the item's number. Type \"inv\" to see your inventory!")
                else:
                    try:
                        item_num = int(args[1])
                        items = p.items
                        target = p.talking

                        if (item_num >= 0 and item_num < len(items)):
                            item = items[item_num]
                            print("[You gave " + item.name + " to " + target.name + "]")

                            try:
                                world = handle_give(world, target, item)
                                p.remove_item(item)
                                return world
                            except NoThankYou:
                                print(target.name + ": No thank you. I have no use of that.\n[" + target.name + " gave " + item.name + " back to you]")
                        else:
                            print("You don't have item with that number. Type \"inv\" to see your inventory!")
                    except ValueError:
                        print("Type the item's number. Type \"inv\" to see your inventory!")
            else:
                print("You cannot give item because you are not talking to anyone. Type \"talk [name]\" to start talking!")
        elif args[0] == "inv": # Show inventory
            p = world["Player"]
            p.see_items()
        elif args[0] == "people": # Show NPCs
            current = world["Current"]
            if len(current["npcs"]) == 0:
                print("No one is here.")
            else:
                print("[People]")
                for npc in current["npcs"]:
                    print(npc, end=", ")
                print("")
        else:
            print("You cannot do such thing!")
        
        return world


def render(world):
    global do_render
    
    if do_render:
        current = world["Current"]
        links = current["links"]
        count = 0

        GameHelper.cls()
        print(current["text"])
        for l in links:
            print("[goto " + str(count) + "] " + l["name"])
            count += 1

        do_render = False


def init_player():
    '''Ask for player's name and returns a player object with that name.'''
    while True:
        name = input("What is your name?: ")

        recheck = input("Your name is " + name + ". Is that correct? (Y/N): ")

        if recheck.lower() == "y":
            print("Great!")
            return Player(name)
        else:
            print("Oh, I am sorry. Could you tell me your name once more?")


def show_intro():
    '''Shows the intro of the game.'''
    time.sleep(0.3)
    print(".")
    time.sleep(0.3)
    print(".")
    time.sleep(0.3)
    print(".")
    time.sleep(0.3)
    print("VERSION: " + VERSION)
    time.sleep(0.3)
    print(".")
    time.sleep(0.3)
    print("Created by Sonny Kim")
    time.sleep(0.3)
    print(".")
    time.sleep(0.3)
    print("It's Saturday night. You are relaxing on your sofa watching a movie. "
    + "The movie is rather boring. When you reached out your hand for a bag of chips, " 
    + "suddenly you started to feel dizzy. Through your blurred vision, "
    + "you see a mysterious circle that has appeared in the middle of the room. "
    + "Beyond the circle, you see a place where you have never been. "
    + "The circle is growing larger, and now it's devouring you.\n")
    
    time.sleep(1)
    input("Press Enter to Continue...")
    GameHelper.cls()


def handle_give(world, npc, item):
    global do_render

    current_pid = world["Current"]["pid"]

    if current_pid == "2": # At the Bonefire
        if npc.name == "The Old Lady" and item.item_id == 103: # If the npc is oldlady and the item is edible type
            ianne = world["NPC"]["ianne"]
            player = world["Player"]

            ianne.relationship += 10
            player.mercy += 10
            player.add_item(Item(104, "Golden Whistle"))

            new_current = find_passage(world["Map"], "4")
            world["Current"] = new_current
            player.talking = None
            do_render = True
            return world
    elif current_pid == "9": # At the Shrine of Compassion
        if npc.name == "Myrce" and item.item_id == 104:
            ianne = world["NPC"]["myrce"]
            player = world["Player"]

            ianne.relationship += 10
            player.mercy += 5

            print("Myrce:" + get_script("myrce", "101"))
            print("Myrce" + get_script("myrce", "102"))
            return world


    raise NoThankYou


if __name__ == "__main__":
    run_game()

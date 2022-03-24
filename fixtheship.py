# Fix the Ship v0.5.0
# Timothy Goode (telimektar3)
from threading import Thread
import time

# Global variables
player_functions = {}
locations = {}
prompt = ""
thread_running = True
# Player Class here
class Player:
    def __init__(self, name, hp, max_hp):
        # Biographical attributes
        self.name = name
        self.location = []
        
        # Health system attributes
        self.healthpoints = hp
        self.maxhealthpoints = max_hp
        self.unconscious = False
        self.dead = False
        
        # Inventory system attributes
        self.inv = {} # needs to be {item.name: item}
        self.eq = [["head", ""], ["chest", ""], ["weapon", ""],["tool", ""]]

        # Skill system attributes
        self.repair_skill = 0
        self.repair_prac = 0
        self.search_skill = 0
        self.search_prac = 0

    # Run this with "score" input   
    def __repr__(self):
        return "Your health is {hp}/{max_hp}.".format(hp = self.healthpoints, max_hp = self.maxhealthpoints)



    # Run this with "i" or "inventory" input
    def inventory(self):
        parsed_inventory = ""
        if self.inv != {}:
            for item in self.inv:
                parsed_inventory += " " + item + ","
        else:
            parsed_inventory = "There is nothing in your inventory"
        if parsed_inventory != "There is nothing in your inventory":
            parsed_inventory = "You see the following items in your inventory:" + parsed_inventory
        parsed_inventory = parsed_inventory.strip(",") + "."
        return parsed_inventory

    # Run this with "equip" input; it should without argument list equipped items, and with argument attempt to equip an item
    def equip(self, item=""): # when equipping an item it will add the following list to the appropriate equip slot [item.name, item.weight, item.condition]
        equipped_items_desc = []
        equipped_items_string = "" 
        if item == "": # this will show what is equipped if there is no item arg
            equipped_items_desc.append("You have the following items equipped:")
            if self.eq[0][1] == "":
                equipped_items_desc.append("\n         Head:  nothing")
            else:
                equipped_items_desc.append("\n         Head:  {head}".format(head = self.eq[0][1]))
            if self.eq[1][1] == "":
                equipped_items_desc.append("        Chest:  nothing")
            else:
                equipped_items_desc.append("        Chest:  {chest}".format(chest = self.eq[1][1]))
            if self.eq[2] == ["weapon", ""] and self.eq[3] == ["tool", ""]:
                equipped_items_desc.append("        Hands:  nothing")
            elif self.eq[2][1] != "" and self.eq[3][1] != "":
                equipped_items_desc.append("   Right hand:  {right_hand}\n    Left hand:  {left_hand}".format(right_hand = self.eq[2][1], left_hand = self.eq[3][1]))
            elif self.eq[2][1] != "" and self.eq[3][1] == "":
                equipped_items_desc.append("   Right hand:  {right_hand}\n    Left hand:  nothing".format(right_hand = self.eq[2][1]))
            elif self.eq[2][1] == "" and self.eq[3][1] != "":
                equipped_items_desc.append("   Right hand:  nothing\n    Left hand:  {left_hand}".format(left_hand = self.eq[3][1]))
            for item in equipped_items_desc:
                equipped_items_string += item + "\n"
            return equipped_items_string
        if item != "": # this will check to see if the item specified can be equipped, and if it can places it in the correct slot in self.eq
            if item in self.inv:
                item_to_eq = self.inv[item]
                retrieved_id = getattr(item_to_eq, 'id')
                new_self_eq = []
                response = ""
                id_list = next(zip(*self.eq))
                if item_to_eq.in_inventory == False:
                    response = "You don't have that!"
                elif retrieved_id not in id_list:
                    response = "You can't equip that!"
                else:
                    for list in self.eq:
                        if list[0] == retrieved_id and list[1] == "": # if the open slot matches the item type, places it in the open slot
                            new_self_eq.append([list[0], item]) # appending .name rather than item because there won't be more than one of an item, and (frankly) I don't want to figure out how to convert "item stored @ somewhere" into it's .name right now
                            response = "You equip {item}.".format(item = item)
                            item_to_eq.is_equipped = True
                        elif list[1] == item:
                            new_self_eq.append([list[0], list[1]])
                            response = "You already have that equipped!"
                        elif list[0] == retrieved_id and list[1] != "":
                            new_self_eq.append([list[0], list[1]])
                            response = "You have already equipped {item} there. Try removing it first.".format(item = list[1])
                        else:
                            new_self_eq.append([list[0], list[1]])
                    self.eq = new_self_eq
            else:
                response = "You don't have that!"
            return response



   # Removes equipment on player.eq slots
    def remove(self, item = ""):
        response_remove = ""
        if item != "": # this will check to see if the item can be removed, and if it can removes it from the correct slot in self.eq
            # retrieved_id = getattr(item, "id")
            new_self_eq = []
            response = ""
            if item not in player.inv:
                response = "You don't have that!"
            else:
                item_object = player.inv[item]
                for list in self.eq:
                    count = 0
                    if list[1] == item: # if a slot matches the item name, removes it from self.eq
                        eq_id = list[0]
                        new_self_eq.append([eq_id, ""])
                        response_remove = "You remove {item}.".format(item = item)
                        count += 1
                        item_object.is_equipped = False
                        # print(player.eq)
                    else:
                        new_self_eq.append([list[0], list[1]])
                        response = "You don't have that equipped"
                        # print("The remove else case")
                self.eq = new_self_eq
                # print(player.eq)
            if response_remove != "":
                    return response_remove
            else:
                return response
        else:
            return "Remove what?"

 
    # Run this with "search" input
    def search(self, item = ""):
        pass
    # "Search" should have a case that looks for parts where it finds parts necessary to repair the ship
    # in the current room. Need to create an attribute that includes a list of the necessary repair items.
    # this search function should only be usable if the player has talked to the droid about what parts are
    # necessary.

    # Run this with "look" input
    def look(self, place = ""):
        room_desc = player.location[0]
        if place == "":
            return room_desc.describe_self()
        elif place != "" and place in room_desc.items:
            items_here = room_desc.items.keys()
            for item in items_here:
                if place == item and room_desc.items[item].is_hidden == False:
                     return "You see {item}".format(item = item)
                elif room_desc[item].is_hidden == True:
                    for item in player.inv:
                        return "Nope"
                else:
                    return "You don't see that here."
            # location_object = player.location[0]
            # print(location_object.look_desc)
        elif place != "" and place.capitalize() in str(room_desc.occupants):
            return droid.describe_droid()
        else:
            return "What?"

    # Run this with "get" input
    
    def get_here(self, item=""):
        current_room = self.location
        here = current_room[0]
        here_objects = getattr(here, 'items')
        if item in here_objects.keys():
            new_item = here_objects[item]
            del here.items[item]
            # print(here.items) 
            return player.get(new_item)
        elif item == "":
            return "Get what?"
        else:
            return "That isn't here."
    
    def get(self, item):
        if self.inv == {} and item != None:
            self.inv = {item.name: item}
            item.in_inventory = True
            item.is_hidden = False
            # print(item.in_inventory)
        elif item != None:
            self.inv[item.name] = item
            item.in_inventory = True
            # print(item.in_inventory)
        return "You get " + item.name

    # Need player function that removes items from inventory
    def drop(self, item = ""):
        # pass # implement; make sure that this calls a function in Item that sets item.in_inventory to False
        if item == "":
            return "Drop what?"
        else:
            current_room = self.location
            here = current_room[0]
            if item in self.inv.keys():
                item_object = self.inv[item]
                if item_object.is_equipped == True:
                    Player.remove(player, item)
                    print("You unequip " + item)
                    item_object.is_equipped = False
                here.items[item] = item_object
                # print(here.items)
                item_object.in_inventory = False
                del self.inv[item]
                # print(self.inv)
                # print(here.items)
                # print(item_object.in_inventory)
                return "You drop " + item + "."
            else:
                return "You don't have " + item + "!"
            
    def give(self, string = ""):
        if string == "":
            return "Give <what> to <who>?"
        else:
            new_split = string.split(" to ", 1)
            print(new_split)
            if not len(new_split) > 1:
                return "Give <what> to <who>?"
            else:
                item = new_split[0]
                target = new_split[1].capitalize
                current_room = self.location
                here = current_room[0]
                new_target = []
                if target in here.occupants:
                    new_target.append(here.occupants[target])
                    if item in self.inv.keys():
                        item_object = self.inv[item]
                        if item_object.is_equipped == True:
                            Player.remove(player, item)
                            print("You unequip " + item)
                            item_object.is_equipped = False
                        here.items[item] = item_object
                        item_object.in_inventory = False
                        del self.inv[item]
                        # print(self.inv)
                        # print(here.items)
                        # print(item_object.in_inventory)
                        return "You give " + item + " to {target}.".format(target = target)
                    else:
                        return "You don't have " + item + "!"
                else:
                    return "They aren't here."
            

    # Need player function for "help" that lists commands: maybe help(blank,[command from list inside function])
    def help(self, topic = ""):
        pass

    def check_move(self, input):
        if input in locations.keys():
            value = locations[input]
            return Player.move(input, value)
        else:
            return "What?"   

    def move(input, value):
        exit = value.room_id
        current_location = player.location[0].room_id
        if current_location != exit:
            new_player_location = [value]
            print("You move to the {location}".format(location = value.examine_desc.lower()))
            player.location = new_player_location
            return player.look()
        else:
            return "You can't go that way."

    def turn_on(self, string = ""):
        current_room = self.location
        here = current_room[0]
        occupant = here.occupants
        new_string = string.split("on ", 1)
        if new_string == "":
            return "Turn on who?"
        if len(new_string) > 1: 
            if new_string[1].capitalize() == "Robbie":
                key = new_string[1].capitalize()
                occupant_new = occupant[new_string[1].capitalize()]
                if key.capitalize() in occupant:
                    if occupant_new.plugged_in == False:
                        return "You should <plug Robbie in> first."
                    elif occupant_new.plugged_in == True and occupant_new.unconscious == True:
                        occupant_new.unconscious = False
                        print("\nThe green light on Robbie's chest glows a bit brighter, and you hear a soft 'click'.")
                        time.sleep(5)
                        print("\nRobbie's eyes brigthen and there is a whirring noise.")
                        time.sleep(5)
                        return "\nRobbie says: 'It has been two-hundred days since I last was activated. Oh my.'\n"
                    else:
                        return "\nRobbie stops you from touching his power cord. 'I'm all juiced up.'\n"
                else:
                    return "Turn on who?"
            else:
                return "Turn on who?"
        else:
            return "Turn on who?"
    
    def plug_in(self, string = ""):
        current_room = self.location
        here = current_room[0]
        occupant = here.occupants
        new_string = string.split(" ", 1)
        if occupant != {"": ""}:
            if len(new_string) > 1:
                new_string2 = new_string[0]
                if new_string2.capitalize() == "Robbie":
                    key = new_string2.capitalize()
                    occupant_new = occupant[new_string2.capitalize()]
                    if key.capitalize() in occupant and occupant_new.unconscious == True:
                         return occupant_new.plug_in()
                    elif key.capitalize() in occupant and occupant_new.unconscious == False:
                        return "Robbie says: 'I don't require any more power, thank you.'\n"
                    else:
                        return "That person isn't here."
                else:
                    return "Plug <who> in?"
            else:
                return "Plug <who> in?"
        else:
            return "That person isn't here."

    def say(self, string = ""):
        if string == "":
            return "You mumble to yourself."
        else:
            player_speech = "You say: {string}".format(string = string)
            droid_output = droid.listen(string)
            if droid_output == None:
                return player_speech
            else:
                print(player_speech)
                time.sleep(0.5)
                return droid_output

    def ask(self, string = ""):
        current_room = self.location
        here = current_room[0]
        occupant = here.occupants
        if string == "":
            return "Ask <who> about <what>?"
        else:
            lower_string = string.lower()
            robot = "Robbie"
            if "robbie" in lower_string:
                occupant_new = occupant[robot]
            if "robbie about" not in lower_string:
                return "Ask <who> about <what>?"
            elif occupant != {"": ""}:
                if robot in occupant and occupant_new.unconscious == True:
                    return "Robbie can't answer questions. You should try turning Robbie on."
                elif robot in occupant and occupant_new.unconscious == False:
                    parsed_string = lower_string.split("robbie about ", 1)
                    if parsed_string[1] in occupant_new.dialogue: # See if the asked about item is a key of the Droid.dialoge dict
                        pass
                    else:
                        pass
                else:
                    return "What?"
            else:
                return "There isn't anyone here to ask."

    def quit(self): # need a save function so that progress on game can be made, perhaps with a yes/no prompt?
        global thread_running
        thread_running = False
        return "See you later."

# Room Class here
class Room:
    room_id_count = 0

    def __init__(self, desc, ex_desc, exits, room_items, occupants_name, occupant):
        # Room sensorium
        self.look_desc = desc
        self.examine_desc = ex_desc
        # Environmental system attributes
        # self.oxygen_level = oxy_level
        # Direction
        self.exits = exits
        # Occupants
        self.items = room_items # use a dictionary {"item name": object}
        self.occupants = {occupants_name: occupant}
        locations[self.examine_desc.lower()] = self
        Room.room_id_count += 1
        self.room_id = Room.room_id_count
         

    def describe_self(self):
        occupants = ""
        if self.occupants != {"": ""}:
            for key in self.occupants.keys():
                occupants_key = self.occupants[key]
                occupants += occupants_key.name
        occupants = occupants.strip(", ")
        if self.items != {}:
            items_here = list(self.items.keys())
            for item in items_here:
                items_here_new = ""
                item_scan = self.items[item]
                if item_scan.is_hidden == False:
                    items_here_new = items_here_new + item + ", "
            items_here_new = items_here_new.strip(", ")
            if items_here_new != "":
                look_at_me = "\n" + self.examine_desc + ":\n" + self.look_desc + "\n\n" + "In the room there are the folowing: " + items_here_new + "\n\n" + "You can see the following exits:\n------------------------------\n" + self.exits + "\n\n" + occupants +"\n"
            else:
                look_at_me = "\n" + self.examine_desc + ":\n" + self.look_desc + "\n\n" + "You can see the following exits:\n------------------------------\n" + self.exits + "\n\n" + occupants +"\n"
        else:
            look_at_me = "\n" + self.examine_desc + ":\n" + self.look_desc + "\n\n" + "You can see the following exits:\n------------------------------\n" + self.exits + "\n\n" + occupants +"\n"
        return look_at_me


# Droid Class here
class Droid:
    def __init__(self, name, inventory, location):
        # Biographical attributes
        self.name = name
        self.location = location
        # Health system attributes
        self.unconscious = True # droid starts out in a powered down state
        self.plugged_in = False
        # Inventory system attributes
        self.inventory = inventory
        # Relationship system attributes
        self.dialogue = {} # need to add topics of conversation here; may benefit from creating a method in Droid that will be called to process

    def listen(self, input = ""):    
        current_room = player.location[0]
        if input != None:
                hi = input.lower()
        if current_room != self.location:
            return
        elif droid.unconscious == False:
            if "hi" in hi:
                return "\nRobbie says: 'Hello, {player_name}. Please <ask> me about anything you want to know.'".format(player_name = player.name)
            else:
                pass
        else:
            return
            
    
    def describe_droid(self):
        if self.unconscious:
            return "This droid has the word 'Robbie' painted across his chest. He appears to be powered off. Maybe you should <turn on Robbie>?"
        else:
            return "This droid has the word 'Robbie' painted across his chest. His eyes are two glowing pink orbs in a mechanical face.\n He looks friendly. \n Maybe you could say 'Hi'?"

    def plug_in(self):
        self.plugged_in = True
        print("You plug Robbie's cord into an outlet in the wall.")
        time.sleep(2)
        print("\nA green light begins to blink on Robbie's chest.")
        time.sleep(2)
        print("\nThe light continues to blink")
        time.sleep(1)
        print("\nblink")
        time.sleep(1)
        print("\nblink")
        time.sleep(1)
        print("\nblink")
        time.sleep(0.5)
        print("\nblink")
        time.sleep(0.5)
        print("\nblink")
        time.sleep(0.1)
        print("\nblink")        
        time.sleep(0.1)
        print("\nblink")       
        time.sleep(0.1)
        print("\nblink")
        time.sleep(0.1)
        print("\n\nThe green light glows brightly on Robbie's chest.")
        time.sleep(2)
        return "\nYou can <turn on Robbie> now."


# Item class here
class Item:
    def __init__(self, name, item_id, location):
        # Biographical attributes
        self.name = name
        self.id = item_id # Can be "head", "chest" "hand" 
        self.in_inventory = False
        self.is_equipped = False
        self.is_hidden = False
        self.location = location
        # Health system attributes
        # self.condition = condition_item

# Function Dictionary for Parser
# player_functions["repair"] = Player.repair
player_functions["remove"] = Player.remove     
player_functions["eq"] = Player.equip
player_functions["equip"] = Player.equip 
player_functions["i"] = Player.inventory
player_functions["inventory"] = Player.inventory
player_functions["get"] = Player.get_here
player_functions["drop"] = Player.drop
player_functions["l"] = Player.look
player_functions["look"] = Player.look
player_functions["quit"] = Player.quit
player_functions["give"] = Player.give
player_functions["turn"] = Player.turn_on
player_functions["plug"] = Player.plug_in
player_functions["say"] = Player.say
player_functions["ask"] = Player.ask

# Parser here
def parse(input):
    input_list = input.split(" ", 1)
    # print(input_list)
    input_long = input
    input = input_list[0]
    function_output = ""
    for key in player_functions.keys():
        if input_list[0] == key:
            function = player_functions.get(key)
            # print(function)
            if len(input_list) > 1:
                command_arg = input_list[1]
                print(input_long)
                function_output = function(player, command_arg)
            elif len(input_list) == 1:
                print(input_long)
                function_output = function(player)
            return function_output
    else:
        print(input_long)
        return Player.check_move(player, input_long)


# Game Code

# Game Thread Setup

# Create initial items & Hide hidden items
space_suit_1 = Item("a spacesuit", "chest", "")
space_helmet_1 = Item("a helmet", "head", "")
battery_1 = Item("a battery", "", "")
circuit_board_1 = Item("a circuit board", "", "")
wiring_harness_1 = Item("a wiring harness", "", "")
processor_1 = Item("a processor", "", "")

battery_1.is_hidden = True
circuit_board_1.is_hidden = True
wiring_harness_1.is_hidden = True
processor_1.is_hidden = True

# Create initial rooms
engine_room = Room("This is the engine room. There are all sorts of blinking lights and various other things here.\nOddly enough, there isn't any sound here.", "Engine Room", "galley, hallway", {space_suit_1.name: space_suit_1}, "", "")
hallway = Room("This is a long hallway that runs the length of the ship. There are several doors on either side of the hallway. At the ends of the hallway are heavy doors. ", "Hallway", "bridge, medical room, dormitory, workshop, utility closet, engine room, hangar bay", {}, "", "")
medical_room = Room("This is a small medical room. There is a bed for the patient to lay on. There are various kinds of medical equipment on the walls.", "Medical Room", "hallway",{space_helmet_1.name: space_helmet_1}, "", "")
bridge = Room("", "Bridge", "hallway", {circuit_board_1.name: circuit_board_1}, "", "") # need to add description
dormitory = Room("", "Dormitory", "hallway", {processor_1.name: processor_1}, "", "") # need to add description
workshop = Room("", "Workshop", "hallway", {wiring_harness_1.name: wiring_harness_1}, "", "") # need to add description
utility_closet = Room("", "Utility Closet", "hallway", {battery_1.name: battery_1}, "", "") # need to add description
hangar_bay = Room("", "Hangar Bay", "hallway", {}, "", "") # need to add description
galley = Room("", "Galley", "engine room", {}, "", "") # need to add description

# Create Player instance
player = Player("blank", 100, 100)
player.location = [medical_room]

# Create initial Droids
droid = Droid("Robbie", {}, engine_room)
engine_room.occupants = {droid.name: droid}

# Create prompt
prompt = "hp: " + str(player.healthpoints) + "/" + str(player.maxhealthpoints) + ": "

# Intro Script
print("\n\n\n\n\n\n\n    _______  __  ___   ___    .___________. __    __   _______         _______. __    __   __  .______")   
print("   |   ____||  | \  \ /  /    |           ||  |  |  | |   ____|       /       ||  |  |  | |  | |   _  \\")
print("   |  |__   |  |  \  V  /     `---|  |----`|  |__|  | |  |__         |   (----`|  |__|  | |  | |  |_)  |") 
print("   |   __|  |  |   >   <          |  |     |   __   | |   __|         \   \    |   __   | |  | |   ___/")  
print("   |  |     |  |  /  .  \         |  |     |  |  |  | |  |____    .----)   |   |  |  |  | |  | |  |")      
print("   |__|     |__| /__/ \__\        |__|     |__|  |__| |_______|   |_______/    |__|  |__| |__| | _|\n\n\n")

time.sleep(5)

initial_name = input(str("What is your name? "))
player.name = initial_name
time.sleep(1)
print("\n\nHello, {player}".format(player = player.name))
time.sleep(1)
print("\n\nWelcome to your very own adventure. You will use your reading, typing and puzzle skills to fix a spaceship. You will find a robot on the ship that you can interact with. There will be items to pick up and use.\n\n\n")

input(str("Press ENTER to continue "))
print("\nIf you ever need help you can type the word 'help'\n")

begin_now = "Press ENTER to begin your adventure.\n\n"

input(str(begin_now))
print("\n\n\n\n\n\n\n\n")
time.sleep(1)
print("..........\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print(".........\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print("........\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print(".......\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print("......\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print(".....\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print("....\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print("...\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print("..\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(1)
print(".\n\n\n\n\n\n\n\n\n\n\n\n")
time.sleep(3)
print("\n\n\n\n\n\n\n\n\n\n\n\n")
print("You open your eyes. There is a bright light that makes it hard to see.\n\n")
time.sleep(4)
print("You rub your eyes. After a little bit you can see that you are in the medical room of a spaceship.")

input(str("\n\n\nPress ENTER to continue "))
print("\n\n\n\n\n\nYou can hear an alarm sounding, and the lights are flickering. You remember flying your ship through space\n when you suddenly flew into an asteroid belt. The last thing you remember is a big asteroid slamming into the side of your ship.\n\n")

input(str("Press ENTER to continue "))
print("\n\n\n\n\n\nYou wonder who brought you the medical room. Maybe it was Robbie?\n\n")

input(str("Press ENTER to continue"))
print("\n\n\n\n\n\n")
print(medical_room.describe_self())

# Game Threads

def my_forever_while():
    global thread_running
    
    # start_time = time.time()

    # # run this while there is no input
    # while thread_running:
    #     time.sleep(0.1)

    #     if time.time() - start_time >= 5:
    #         start_time = time.time()
    #         print('Another 5 seconds has passed')


def take_input():
    global thread_running
    while thread_running:
        what_was_typed = []
        player_input = input(str(prompt))
        # doing something with the input
        if player_input == "score":
            print(player_input)
            print(player)
        else:
            what_was_typed = parse(player_input)
            print(what_was_typed)

if __name__ == '__main__':
    t1 = Thread(target=my_forever_while)
    t2 = Thread(target=take_input)

    t1.start()
    t2.start()

    t2.join()  # interpreter will wait until your process get completed or terminated
    # thread_running = False
    print('Good-bye.') # maybe change this

# Outro Text
print("\n\n\n    _______  __  ___   ___    .___________. __    __   _______         _______. __    __   __  .______")   
print("   |   ____||  | \  \ /  /    |           ||  |  |  | |   ____|       /       ||  |  |  | |  | |   _  \\")
print("   |  |__   |  |  \  V  /     `---|  |----`|  |__|  | |  |__         |   (----`|  |__|  | |  | |  |_)  |") 
print("   |   __|  |  |   >   <          |  |     |   __   | |   __|         \   \    |   __   | |  | |   ___/")  
print("   |  |     |  |  /  .  \         |  |     |  |  |  | |  |____    .----)   |   |  |  |  | |  | |  |")      
print("   |__|     |__| /__/ \__\        |__|     |__|  |__| |_______|   |_______/    |__|  |__| |__| | _|\n\n\n\n")      
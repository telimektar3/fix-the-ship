# Fix the Ship
# Timothy Goode (telimektar3)
import random
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
        # self.sex = sex
        # self.height = height # in inches
        # self.weight = weight # in pounds
        self.location = []
        
        # Health system attributes
        # self.oxygen = oxygen # input as [effort, available% (100 - 0)]
        self.healthpoints = hp
        self.maxhealthpoints = max_hp
        self.unconscious = False
        self.dead = False
        
        # Inventory system attributes
        self.inv = {} # needs to be {item.name: item}
        self.eq = [["head", ""], ["chest", ""], ["weapon", ""],["tool", ""]]
        
        # Relationship system attributes
        # self.droid_relationship = 0
        
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



    # Run this with "skills" input
    # def skills(self, skill=""):
    #     skill_list = ["repair", "search"]
    #     if skill == "":
    #         return "\nYour skills are:\n\n                repair: {repair}%\n                search: {search}%\n".format(repair = self.repair_skill, search = self.search_skill)
    #     elif skill not in skill_list:
    #         return "\nThat's not a skill. Try 'repair' or 'search' instead.\n"
    #     elif skill == "repair":
    #         repair_skill = "\nThis is a person's ability to 'repair' items or systems.\nYour repair skill is at {repair}% mastery at this time.\n".format(repair = self.repair_skill)
    #         return repair_skill
    #     else:
    #         search_skill = "\nThis is a person's ability to find hidden items or 'search' through computer systems for needed information.\nYour search skill is at {search}% mastery at this time.\n".format(search = self.search_skill)
    #         return search_skill



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



    # def repair_item(self, item):
    #     repair_skill = self.repair_skill
    #     initial_condition = item.condition
    #     repair_skill_number = (repair_skill + random.randint(0, 100)) * .70
    #     repair_outcome = repair_skill_number - initial_condition
    #     skill_use_outcome = ""
    #     skill_increase = ""
    #     if repair_skill_number >= initial_condition:
    #         if repair_outcome >= 10:
    #             item.condition = item.condition + random.randint(10, 20)
    #         elif repair_outcome >= 5:
    #             item.condition = item.condition + random.randint(5, 10)
    #         else:
    #             item.condition = item.condition + random.randint(1, 5)
    #         skill_use_outcome = "You repaired {item}.".format(item = item.name)
    #     elif repair_skill_number < initial_condition:
    #         if repair_outcome <= -15:
    #             item.condition = item.condition - random.randint(1, 5)
    #             skill_use_outcome =  "That didn't work. You might have made it worse."
    #         elif repair_outcome > -15:
    #             skill_use_outcome = "Your repair fails, but you don't seem to have made it worse."
    #     self.repair_prac += 1
    #     if self.repair_prac > (self.repair_skill + 1) * 0.5:
    #         self.repair_skill += 1
    #         skill_increase =  "Your skill at repairing increased!"
    #     final_repair_msg = skill_use_outcome + "\n" + skill_increase
    #     return final_repair_msg

    # # Run this with "repair" input
    # def repair(self, item = ""):
    #     if item == None:
    #         return "You should input: repair 'item name'."
    #     elif item not in player.inv:
    #         return "You don't have that in your possession."
    #     elif item.condition >= 90:
    #         item_name = item.name
    #         return item_name.capitalize() + " is already in perfect condition."
    #     else:
    #         item_name = item.name
    #         print(self.repair_item(item))
    #         if item.condition <= 10:
    #             return item_name.capitalize() + " is in very bad condition."
    #         elif item.condition > 10 and item.condition <= 40:
    #             return item_name.capitalize() + " is in bad condition."
    #         elif item.condition > 40 and item.condition <= 60:
    #             return item_name.capitalize() + " is in okay condition."
    #         elif item.condition > 60 and item.condition <= 80:
    #             return item_name.capitalize() + " is in good condition."
    #         else:
    #             return item_name.capitalize() + " is in very good condition."

 

            


 
    # Run this with "search" input
    # def search(self, item = ""):
    #     pass
    # "Search" should have a case that looks for parts where it finds parts necessary to repair the ship
    # in the current room. Need to create an attribute that includes a list of the necessary repair items.
    # this search function should only be usable if the player has talked to the droid about what parts are
    # necessary.

    # Run this with "rest" input
    # def rest(self):
    #     pass # make sure that you complete this

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
            print(str(room_desc.occupants))
            return droid.describe_droid()

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
            



    # needs to also edit player.inv and remove item.name from that list

 
    # Need player function for "help" that lists commands: maybe help(blank,[command from list inside function])
    # def help(self, topic = ""):
    #     pass

    # Need player function that uses oxygen based on weight of items and body size/weight: 
        # "Air Consumption Rate All other factors being equal, a diver’s air consumption rate, also called his Surface Air Consumption Rate (SAC rate) 
        # or Respiratory Minute Volume (RMV), will determine how long the air in his tank will last compared to the average diver. A diver with large 
        # lung volume (tall or large people) will require more air than a petite or short person with a smaller lung volume and will usually have a higher 
        # air consumption rate. A variety of factors effect an individual’s air consumption rate, including stress, experience level, buoyancy control, and 
        # the amount of exercise the diver does on a dive. Relaxed, slow, and deep breathing is usually the best way for a diver to reduce his air consumption rate." 
        # - https://www.omegadivers.com/how-long-does-a-scuba-tank-last/
    # def air_usage(self):
    #     pass

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
        print(new_string)
        if new_string == "":
            return "Turn on who?"
        if len(new_string) > 1: 
            print(new_string[1])
            if new_string[1].capitalize() == "Robbie":
                key = new_string[1].capitalize()
                occupant_new = occupant[new_string[1].capitalize()]
                if key.capitalize() in occupant:
                    if occupant_new.plugged_in == False:
                        return "You should <plug Robbie in> first."
                    else:
                        occupant_new.unconscious = False
                        return occupant_new.plug_in()
                else:
                    return "Turn on who?"
            else:
                return "Turn on who?"
        else:
            return "Turn on who?"

    def quit(self): # need a save function so that progress on game can be made, perhaps with a yes/no prompt?
        global thread_running
        thread_running = False
        return "See you later."
        
# Player functions dictionary to use with Parser
# need a player functions function that initializes these


# Player Class testing below

# print(player)
# print(player.inventory())
# print(player.skills())





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
        if self.occupants != {}:
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
                look_at_me = "\n" + self.examine_desc + ":\n" + self.look_desc + "\n" + "In the room there are the folowing: " + items_here_new + "\n\n" + "You can see the following exits:\n------------------------------\n" + self.exits + "\n\n" + occupants + " is here.\n"
            else:
                look_at_me = "\n" + self.examine_desc + ":\n" + self.look_desc + "\n\n" + "You can see the following exits:\n------------------------------\n" + self.exits + "\n\n" + occupants + " is here.\n"
        else:
            look_at_me = "\n" + self.examine_desc + ":\n" + self.look_desc + "\n\n" + "You can see the following exits:\n------------------------------\n" + self.exits + "\n\n" + occupants + " is here.\n"
        return look_at_me


        

    # def check_occupants(self):
    #     if self.occupants == []:


    # def check_oxygen(self):
    #     if player.location == self and self.oxygen_level == 0:
    #         if player.eq[1][1] == "" and player.eq[0][1] == "":
    #             if player.oxygen > 50:
    #                 print("You gasp... there's no oxygen in here!!!")
    #                 self.drain_oxygen()
    #             else:
    #                 self.drain_oxygen()
    #         else:
    #             return
    #     else:
    #         return
            
    # def drain_oxygen(self):
    #     if player.oxygen == 0:
    #         player.healthpoints = player.healthpoints - 5
    #         print("It's hard to focus on anything, and the world is going gray.")
    #     elif 30 < player.oxygen <= 50:
    #         print("Your worries just seem to be slipping away...")
    #         player.oxygen = player.oxygen - 10
    #     else:
    #         print("Who knew life could be so great?")
    #         player.oxygen = player.oxygen - 10


# Droid Class here
class Droid:
    def __init__(self, name, inventory, location):
        # Biographical attributes
        self.name = name
        # self.sex = "Robot"
        # self.height = height # in inches
        # self.weight = weight # in pounds
        self.location = location
        # Health system attributes
        # self.healthpoints = hp
        # self.movepoints = mp
        self.unconscious = True # droid starts out in a powered down state
        self.plugged_in = False
        # Inventory system attributes
        self.inventory = inventory
        # Relationship system attributes
        # self.droid_relationship = droid_relate
        # Skill system attributes
        # self.repair_skill = 100
        # self.medical_skill = 100
    
    def describe_droid(self):
        if self.unconscious:
            return "This droid has the word 'Robbie' painted across his chest. He appears to be powered off. Maybe you should <turn on Robbie>?"
        else:
            return "This droid has the word 'Robbie' painted across his chest. His eyes are two glowing pink orbs in a mechanical face./n He looks friendly. /n Maybe you could say 'Hi'?"

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
        time.sleep(9)
        print("\nRobbie says: 'Thank you for powering me up.")
        time.sleep(5)
        return "\nRobbie says: 'It has been two-hundred days since I last was activated. Oh my.\n"

# Item class here
class Item:
    def __init__(self, name, item_id, location):
        # Biographical attributes
        self.name = name
        self.id = item_id # Can be "head", "chest" "hand" 
        # self.length_item = length_item # in inches
        # self.weight = weight # in pounds
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
# player_functions["skills"] = Player.skills  
player_functions["i"] = Player.inventory
player_functions["inventory"] = Player.inventory
player_functions["get"] = Player.get_here
player_functions["drop"] = Player.drop
player_functions["l"] = Player.look
player_functions["look"] = Player.look
# player_functions["skills"] = Player.skills
# player_functions["skill"] = Player.skills
player_functions["quit"] = Player.quit
player_functions["give"] = Player.give
player_functions["turn"] = Player.turn_on

# print(player_functions)


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
viking_armor_1 = Item("a set of viking armor", "chest", "")
engine_room = Room("This is the engine room. There are all sorts of blinking lights and various other things here.\nOddly enough, there isn't any sound here.", "Engine Room", "galley, hallway", {viking_armor_1.name: viking_armor_1}, "", "")
hallway = Room("This is a long hallway that runs the length of the ship. There are several doors on either side of the hallway. At the ends of the hallway are heavy doors. ", "Hallway", "bridge, medical room, dormitory, workshop, utility closet, engine room, hangar bay", {}, "", "")
player = Player("Tim", 100, 100)
player.location = [engine_room]
droid = Droid("Robbie", {}, engine_room)
droid.plugged_in = True
engine_room.occupants = {droid.name: droid}
print(engine_room.describe_self())
prompt = "hp: " + str(player.healthpoints) + "/" + str(player.maxhealthpoints) + ": "


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
    print('Good-bye.')

# Actual Game

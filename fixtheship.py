# Fix the Ship
# Timothy Goode (telimektar3)
import random
# Player Class here
class Player:
    def __init__(self, name, sex, height, weight, location, oxygen, hp, max_hp, mp, max_mp, mp_string):
        # Biographical attributes
        self.name = name
        self.sex = sex
        self.height = height # in inches
        self.weight = weight # in pounds
        self.location = location
        
        # Health system attributes
        self.oxygen = oxygen # input as [effort, available% (100 - 0)]
        self.healthpoints = hp
        self.maxhealthpoints = max_hp
        self.movepoints_string = mp_string
        self.movepoints = mp
        self.maxmovepoints = max_mp
        self.unconscious = False
        self.dead = False
        
        # Inventory system attributes
        self.inv = []
        self.eq = [["head", ""], ["chest", ""], ["weapon", ""],["tool", ""]]
        
        # Relationship system attributes
        self.droid_relationship = 0
        
        # Skill system attributes
        self.repair_skill = 0
        self.repair_prac = 0
        self.search_skill = 0
        self.search_prac = 0

    # Run this with "condition" input   
    def __repr__(self):
        return "Your health is {hp}/{max_hp} and you are {mp_string}.".format(hp = self.healthpoints, max_hp = self.maxhealthpoints, mp_string = self.movepoints_string)

    # Run this with "inv" input
    def inventory(self):
        parsed_inventory = ""
        if self.inv != []:
            for item in self.inv:
                parsed_inventory += " " + item + ","
        else:
            parsed_inventory = "There is nothing in your inventory"
        if parsed_inventory != "There is nothing in your inventory":
            parsed_inventory = "You see the following items in your inventory:" + parsed_inventory
        parsed_inventory = parsed_inventory.strip(",") + "."
        return parsed_inventory

    # Run this with "skills" input
    def skills(self, skill=""):
        skill_list = ["repair", "search"]
        if skill == "":
            return "Your skills are:\n\n                repair: {repair}%\n                search: {search}%\n".format(repair = self.repair_skill, search = self.search_skill)
        elif skill not in skill_list:
            return "That's not a skill. Try 'repair' or 'search' instead."
        elif skill == "repair":
            repair_skill = "This a person's ability to 'repair' items or systems.\nYour repair skill is at {repair}% mastery at this time.".format(repair = self.repair_skill)
            return repair_skill
        else:
            search_skill = "This is a person's ability to find hidden items or 'search' through computer systems for needed information.\nYour search skill is at {search}% mastery at this time.".format(search = self.search_skill)
            return search_skill

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
            retrieved_id = getattr(item, "id")
            new_self_eq = []
            response = ""
            id_list = next(zip(*self.eq))
            if item.in_inventory == False:
                response = "You don't have that!"
            elif retrieved_id not in id_list:
                response = "You can't equip that!"
            else:
                for list in self.eq:
                    if list[0] == retrieved_id and list[1] == "": # if the open slot matches the item type, places it in the open slot
                        new_self_eq.append([list[0], item.name]) # appending .name rather than item because there won't be more than one of an item, and (frankly) I don't want to figure out how to convert "item stored @ somewhere" into it's .name right now
                        response = "You equip {item}.".format(item = item.name)
                    elif list[1] == item:
                        new_self_eq.append([list[0], list[1]])
                        response = "You already have that equipped!"
                    elif list[0] == retrieved_id and list[1] != "":
                        new_self_eq.append([list[0], list[1]])
                        response = "You have already equipped {item} there. Try removing it first.".format(item = list[1])
                    else:
                        new_self_eq.append([list[0], list[1]])
                self.eq = new_self_eq
            return response

   # Removes equipment on player.eq slots
    def remove(self, item):
        if item != "": # this will check to see if the item can be removed, and if it can removes it from the correct slot in self.eq
            retrieved_id = getattr(item, "id")
            new_self_eq = []
            response = ""
            if item.in_inventory == False:
                response = "You don't have that!"
            else:
                for list in self.eq:
                    if list[0] == retrieved_id and list[1] == item.name: # if a slot matches the item name, removes it from self.eq
                        new_self_eq.append([list[0], ""]) 
                        response = "You remove {item}.".format(item = item.name)
                    else:
                        new_self_eq.append([list[0], list[1]])
                self.eq = new_self_eq
            return response


    def repair_item(self, item):
        repair_skill = self.repair_skill
        initial_condition = item.condition
        repair_skill_number = (repair_skill + random.randint(0, 100)) * .70
        repair_outcome = repair_skill_number - initial_condition
        skill_use_outcome = ""
        skill_increase = ""
        if repair_skill_number >= initial_condition:
            if repair_outcome >= 10:
                item.condition = item.condition + random.randint(10, 20)
            elif repair_outcome >= 5:
                item.condition = item.condition + random.randint(5, 10)
            else:
                item.condition = item.condition + random.randint(1, 5)
            skill_use_outcome = "You repaired {item}.".format(item = item.name)
        elif repair_skill_number < initial_condition:
            if repair_outcome <= -15:
                item.condition = item.condition - random.randint(1, 5)
                skill_use_outcome =  "That didn't work. You might have made it worse."
            elif repair_outcome > -15:
                skill_use_outcome = "Your repair fails, but you don't seem to have made it worse."
        self.repair_prac += 1
        if self.repair_prac > (self.repair_skill + 1) * 0.5:
            self.repair_skill += 1
            skill_increase =  "Your skill at repairing increased!"
        final_repair_msg = skill_use_outcome + "\n" + skill_increase
        return final_repair_msg

    # Run this with "repair" input
    def repair(self, item = ""):
        item_name = item.name
        if item == "":
            return "You should input: repair 'item name'."
        elif item.condition >= 90:
            return item_name.capitalize() + " is already in perfect condition."
        else:
            print(self.repair_item(item))
            if item.condition <= 10:
                return item_name.capitalize() + " is in very bad condition."
            elif item.condition > 10 and item.condition <= 40:
                return item_name.capitalize() + " is in bad condition."
            elif item.condition > 40 and item.condition <= 60:
                return item_name.capitalize() + " is in okay condition."
            elif item.condition > 60 and item.condition <= 80:
                return item_name.capitalize() + " is in good condition."
            else:
                return item_name.capitalize() + " is in very good condition."

 
                
            


 
    # Run this with "search" input
    # "Search" should have a case that looks for parts where it finds parts necessary to repair the ship
    # in the current room. Need to create an attribute that includes a list of the necessary repair items.
    # this search function should only be usable if the player has talked to the droid about what parts are
    # necessary.

    # Run this with "rest" input
    def rest(self):
        pass # make sure that you complete this

    # Run this with "look" input
    def look(self, place = ""):
        pass # remember to implement

    # Run this with "get" input
    def get(self, item):
        pass # implement; make sure that this sets item.in_inventory to True
    # needs to also edit player.inv and add item.name to that list

    # Need player function that removes items from inventory
    def drop(self, item):
        pass # implement; make sure that this calls a function in Item that sets item.in_inventory to False
    # needs to also edit player.inv and remove item.name from that list

 
    # Need player function for "help" that lists commands: maybe help(blank,[command from list inside function])
    def help(self, topic = ""):
        pass

    # Need player function that uses oxygen based on weight of items and body size/weight: 
        # "Air Consumption Rate All other factors being equal, a diver’s air consumption rate, also called his Surface Air Consumption Rate (SAC rate) 
        # or Respiratory Minute Volume (RMV), will determine how long the air in his tank will last compared to the average diver. A diver with large 
        # lung volume (tall or large people) will require more air than a petite or short person with a smaller lung volume and will usually have a higher 
        # air consumption rate. A variety of factors effect an individual’s air consumption rate, including stress, experience level, buoyancy control, and 
        # the amount of exercise the diver does on a dive. Relaxed, slow, and deep breathing is usually the best way for a diver to reduce his air consumption rate." 
        # - https://www.omegadivers.com/how-long-does-a-scuba-tank-last/
    def air_usage(self):
        pass

    # Output hp/hpmax  mp/mpmax  oxygen%  at each prompt
    def prompt(self):
        pass


# Player Class testing below

# print(player)
# print(player.inventory())
# print(player.skills())





# Room Class here
class Room:
    def __init__(self, desc, ex_desc, smell, sound, oxy_level, temperature, exits, room_items):
        # Room sensorium
        self.look_desc = desc
        self.examine_desc = ex_desc
        self.smell = smell
        self.sounds = sound
        # Environmental system attributes
        self.oxygen_level = oxy_level
        self.light = ["none", "low", "normal", "bright"] # Bright, Normal, Low, None
        self.temperature = temperature # Celsius
        # Direction
        self.exits = exits
        # Occupants
        self.items = room_items



# Droid Class here
class Droid:
    def __init__(self, name, height, weight, hp, mp, inventory, droid_relate):
        # Biographical attributes
        self.name = name
        self.sex = "Robot"
        self.height = height # in inches
        self.weight = weight # in pounds
        # Health system attributes
        self.healthpoints = hp
        self.movepoints = mp
        self.unconscious = True # droid starts out in a powered down state
        self.dead = False
        # Inventory system attributes
        self.inventory = inventory
        # Relationship system attributes
        self.droid_relationship = droid_relate
        # Skill system attributes
        self.repair_skill = 100
        self.medical_skill = 100


# Item class here
class Item:
    def __init__(self, name, item_id, length_item, weight, condition_item):
        # Biographical attributes
        self.name = name
        self.id = item_id # Can be "head", "chest" "hand" 
        self.length_item = length_item # in inches
        self.weight = weight # in pounds
        self.in_inventory = False
        # Health system attributes
        self.condition = condition_item

        
# Game Code

# Testing functions interacting classes
player = Player("Tim", "male", 72, 220, "", 100, 100, 100, 100, 100, "well rested")
player.eq = [["head", ""], ["chest", ""], ["weapon", ""],["tool", ""]]
viking_helm_1 = Item("a viking helm", "head", 10, 1, 100)
viking_armor_1 = Item("a set of viking armor", "chest", 10, 1, 39)
viking_hammer_1 = Item("a viking hammer", "weapon", 14, 20, 100)
viking_caliper_1 = Item("a viking caliper", "tool", 12, 5, 100)
banana_1 = Item("a green banana", "food", 5, 0.5, 100)

viking_armor_1.in_inventory = True
player.inv = [viking_armor_1.name]
print(player.equip(viking_hammer_1))
# print(player.equip(viking_armor_1))
# print(player.equip())
# print(player.inventory())
print(player.equip())
print(player.remove(viking_armor_1))
print(player.inventory())
print(player.equip())
print(player.equip(viking_armor_1))
print(player.equip())
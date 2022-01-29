# Fix the Ship
# Timothy Goode (telimektar3)

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
        self.head_eq = ["","","",""]
        self.chest_eq = ["","","",""]
        self.hands_eq = ["", ""] #currently using this to hold items, [0] is right hand, [1] is left hand
        
        # Relationship system attributes
        self.droid_relationship = 0
        
        # Skill system attributes
        self.repair_skill = 0
        self.search_skill = 0

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
    def skills(self):
        return "Your skills are:\n\n                repair: {repair}\n                search: {search}\n".format(repair = self.repair_skill, search = self.search_skill)

    # Run this with "equip" input; it should without argument list equipped items, and with argument attempt to equip an item
    def equip(self, item): # when equipping an item it will add the following list to the appropriate equip slot [item.name, item.weight, item.condition]
        equipped_items_desc = []
        equipped_items_string = "" 
        if item == "": # this will show what is equipped if there is no item arg
            equipped_items_desc.append("You have the following items equipped:")
            if self.head_eq == []:
                equipped_items_desc.append("\n         Head:  Nothing")
            else:
                equipped_items_desc.append("\n         Head:  {head}".format(head = self.head_eq[0]))
            if self.chest_eq == []:
                equipped_items_desc.append("        Chest:  Nothing")
            else:
                equipped_items_desc.append("        Chest:  {chest}".format(chest = self.chest_eq[0]))
            if self.hands_eq == ["",""]:
                equipped_items_desc.append("        Hands:  Nothing")
            elif self.hands_eq[0] != "" and self.hands_eq[1] != "":
                equipped_items_desc.append("   Right hand:  {right_hand}\n    Left hand:  {left_hand}".format(right_hand = self.hands_eq[0], left_hand = self.hands_eq[1]))
            elif self.hands_eq[0] != "" and self.hands_eq[1] == "":
                equipped_items_desc.append("   Right hand:  {right_hand}\n    Left hand:  Nothing".format(right_hand = self.hands_eq[0]))
            elif self.hands_eq[0] == "" and self.hands_eq[1] != "":
                equipped_items_desc.append("   Right hand:  Nothing\n    Left hand:  {left_hand}".format(left_hand = self.hands_eq[1]))
            for item in equipped_items_desc:
                equipped_items_string += item + "\n"
            return equipped_items_string
        if item != "":
            retrieved_id = getattr(item, "id")
            


            # Check for head equipment
            # retrieved_id = getattr(item, "id")
            # if retrieved_id == "head" and self.head_eq == ["","","",""]:
            #     self.head_eq = []
            #     self.head_eq.append(item.name)
            #     self.head_eq.append(item.weight)
            #     self.head_eq.append(item.condition)
            #     self.head_eq.append(item)
            #     return "You put {helmet} on your head.".format(helmet = item.name)
            if item == self.head_eq[3]:
                return "You are already wearing that, silly."
            elif retrieved_id == "head" and self.head_eq != ["","","",""]:
                return "You are already wearing " + self.head_eq[0] + "! Try removing it first"
            # Check for chest equipment
            if retrieved_id == "chest" and self.chest_eq == ["","","",""]:
                self.chest_eq = []
                self.chest_eq.append(item.name)
                self.chest_eq.append(item.weight)
                self.chest_eq.append(item.condition)
                self.chest_eq.append(item)
                return "You wriggle into {space_suit}.".format(space_suit = item.name)
            elif item == self.chest_eq[3]:
                return "You are already wearing that, silly."
            elif retrieved_id == "chest" and self.chest_eq != ["","","",""]:
                return "You are already wearing " + self.chest_eq[0] + "! Try removing it first"


    # Run this with "repair" input

    # Run this with "search" input

    # Run this with "rest" input

    # Run this with "look" input

    # Need player function that puts items into inventory

    # Need player function that removes items from inventory

    # Need player function that removes equipment on head, body or hand(s);  anything equipped to self.hands must take two arguments every time, even if one is ""

    # Need player function for "help" that lists commands: maybe help(blank,[command from list inside function])

    # Need player function that uses oxygen based on weight of items and body size/weight: 
        # "Air Consumption Rate All other factors being equal, a diver’s air consumption rate, also called his Surface Air Consumption Rate (SAC rate) 
        # or Respiratory Minute Volume (RMV), will determine how long the air in his tank will last compared to the average diver. A diver with large 
        # lung volume (tall or large people) will require more air than a petite or short person with a smaller lung volume and will usually have a higher 
        # air consumption rate. A variety of factors effect an individual’s air consumption rate, including stress, experience level, buoyancy control, and 
        # the amount of exercise the diver does on a dive. Relaxed, slow, and deep breathing is usually the best way for a diver to reduce his air consumption rate." 
        # - https://www.omegadivers.com/how-long-does-a-scuba-tank-last/
        
    # Output hp/hpmax  mp/mpmax  oxygen%  at each prompt


# Player Class testing below

# print(player)
# print(player.inventory())
# print(player.skills())





# Room Class here
class Room:
    def __init__(self):
        # Room sensorium
        self.look_desc = desc
        self.examine_desc = ex_desc
        self.smell = smell
        self.sounds = sound
        # Environmental system attributes
        self.oxygen_level = oxy_level
        self.light = light # Bright, Normal, Low, None
        self.temperature = temperature # Celsius
        # Direction
        self.exits = exits


# Droid Class here
class Droid:
    def __init__(self):
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
        self.repair_skill = repair_skill
        self.medical_skill = first_aid
        self.search_skill = search_skill


# Item class here
class Item:
    def __init__(self, name, item_id, length_item, weight, condition_item):
        # Biographical attributes
        self.name = name
        self.id = item_id # Can be "head", "chest" "hand" 
        self.length_item = length_item # in inches
        self.weight = weight # in pounds
        # Health system attributes
        self.condition = condition_item
        
# Game Code

# Testing functions interacting classes
player = Player("Tim", "male", 72, 220, "", 100, 100, 100, 100, 100, "well rested")
viking_helm_1 = Item("a viking helm", "head", 10, 1, 100)
viking_helm_2 = Item("a viking helm", "chest", 10, 1, 100)




print(player.equip(viking_helm_1))
# print(player.chest_eq)

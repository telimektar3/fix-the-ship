# Fix the Ship
# Timothy Goode (telimektar3)

# Player Class here
class Player:
    def __init__(self, name, sex, height, weight, location, oxygen, hp, max_hp, mp, max_mp, mp_string, xp, inventory, helmet, suit, boots, gloves, legs, droid_relate, self_esteem, repair_skill, first_aid, search_skill):
        # Biographical attributes
        self.name = name
        self.sex = sex
        self.height = height # in inches
        self.weight = weight # in pounds
        self.location = location
        # Health system attributes
        self.oxygen = oxygen
        self.healthpoints = hp
        self.maxhealthpoints = max_hp
        self.movepoints_string = mp_string
        self.movepoints = mp
        self.maxmovepoints = max_mp
        self.unconscious = False
        self.dead = False
        # Inventory system attributes
        self.inv = inventory
        self.head_eq = helmet
        self.chest_eq = suit
        self.feet_eq = boots
        self.hands_eq = gloves #currently using this to hold items, [0] is right hand, [1] is left hand
        self.legs_eq = legs
        # Relationship system attributes
        self.droid_relationship = droid_relate
        self.self_esteem = self_esteem
        # Skill system attributes
        self.repair_skill = repair_skill
        self.medical_skill = first_aid
        self.search_skill = search_skill
        self.experience = xp
    # Player Functions
    # Need player function to calculate self.movepoints_string
    # Need player function to increase skill levels
    # Need player function to change self.droid_relationship
    # Need player function to change self.self_esteem

    # Run this with "condition" input   
    def __repr__(self):
        return "Your health is {hp}/{max_hp}, you are {mp_string}, and you have {xp} experience.".format(hp = self.healthpoints, max_hp = self.maxhealthpoints, mp_string = self.movepoints_string, xp = self.experience)

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
        return "Your skills are: repair: {repair}, first aid: {first_aid}, search: {search}.".format(repair = self.repair_skill, first_aid = self.medical_skill, search = self.search_skill)

    # Run this with "equip" input; it should without argument list equipped items, and with argument attempt to equip an item
    def equip(self, item):
        equipped_items = []
        equipped_items_string = ""
        if item == "":
            equipped_items.append("You have the following items equipped:")
        if self.head_eq == []:
            equipped_items.append("\n         Head:  Nothing")
        else:
            equipped_items.append("\n         Head:  {head}".format(head = self.head_eq[0]))
        if self.chest_eq == []:
            equipped_items.append("        Chest:  Nothing")
        else:
            equipped_items.append("        Chest:  {chest}".format(chest = self.chest_eq[0]))
        if self.hands_eq == []:
            equipped_items.append("        Hands:  Nothing")
        elif self.hands_eq[0] != [] and self.hands_eq[1] != "":
            equipped_items.append("   Right hand:  {right_hand}\n    Left hand:  {left_hand}".format(right_hand = self.hands_eq[0], left_hand = self.hands_eq[1]))
        elif self.hands_eq[0] != [] and self.hands_eq[1] == "":
            equipped_items.append("   Right hand:  {right_hand}\n    Left hand:  Nothing".format(right_hand = self.hands_eq[0]))
        if self.feet_eq == []:
            equipped_items.append("         Feet:  Nothing")
        else:
            equipped_items.append("         Feet:  {feet}".format(feet = self.feet_eq[0]))
        for item in equipped_items:
            equipped_items_string += item + "\n"
        return equipped_items_string
    # Run this with "repair" input
    # Run this with "first aid" input
    # Run this with "search" input
    # Run this with "rest" input
    # Need player function that puts items into inventory
    # Need player function that removes items from inventory
    # Need player function that places equipment on head, chest, hands, feet;  anything equipped to self.hands must take two arguments every time, even if one is ""
    # Need player function for "help" that lists commands: maybe help(blank,[command from list inside function])

player = Player("Tim", "male", 72, 220, "", 100, 50, 50, 50, 50, "", 0, ["old banana", "apple"],["Viking helm"],[],[],[],[], 0, 0, 0, 0, 0)
player.movepoints_string = "well rested"
print(player)
print(player.inventory())
print(player.skills())
print(player.equip(""))

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
    def __init__(self):
        # Biographical attributes
        self.name = name
        self.length_item = length_item # in inches
        self.weight = weight # in pounds
        # Health system attributes
        self.condition = condition_item
        # Inventory system attributes
        self.inventory = inventory
        
# Game Code
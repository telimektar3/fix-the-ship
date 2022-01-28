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
        self.hands_eq = gloves
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
        parsed_inventory = "".join(str(item) for item in self.inventory)
        return "You see the following items in your inventory:" + parsed_inventory

    # Run this with "skills" input
    # Run this with "equip" input
    # Run this with "repair" input
    # Run this with "first aid" input
    # Run this with "search" input
    # Run this with "rest" input
    # Need player function that puts items into inventory
    # Need player function that removes items from inventory
    # Need player function that places equipment on head, chest, hands, feet
    # Need player function for "help" that lists commands: maybe help(blank,[command from list inside function])

player = Player("Tim", "male", 72, 220, "", 100, 50, 50, 50, 50, "", 0, [],[],[],[],[],[], 0, 0, 0, 0, 0)
player.movepoints_string = "well rested"
print(player)
# player.inventory() this throws an error, obviously not ready for prime time


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
        

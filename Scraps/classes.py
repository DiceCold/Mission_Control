python3
import random
 
Startup = True
Current_Location = "Void"
 
class Pilot:
    def __init__(self, name, battlesuit, battlesuit_damaged, injured, alive, weapons, attack, defence, location):
            self.name = name
            self.battlesuit = battlesuit
            self.battlesuit_damaged = battlesuit_damaged
            self.injured = injured
            self.alive = alive
            self.weapons = weapons
            self.attack = attack
            self.defence = defence
            self.location = location
 
class Battlesuit:
    def __init__(self, name, powercells_max, mobility, generator, refresh, shields):
            self.name = name
            self.powercells_max = powercells_max
            self.mobility = mobility
            self.generator = generator
            self.refresh = refresh
            self.shields = shields
 
class Weapon:
    def __init__(self, name, attack, distance, cost_use, cost_maintain):
            self.name = name
            self.attack = attack
            self.distance = distance
            self.cost_use = cost_use
            self.cost_maintain = cost_maintain
 
class Shield:
    def __init__(self, name, cost_use, cost_maintain):
            self.name = name
            self.cost_use = cost_use
            self.cost_maintain = cost_maintain
 
class Location:
    def __init__(self, name, Distance_From_City, Danger_Level, Hazards):
            self.name = name
            self.Distance_From_City = Distance_From_City
            self.Danger_Level = Danger_Level
            self.Hazards = Hazards
 
if Startup == True:
        #Battlesuits
        Majestic = Battlesuit("Majestic", 5, "Quick", "Fusion Core", 3, "Light Shields")
        Leviathan = Battlesuit("Leviathan", 12, "Slow", "Fusion Core", 1, "Heavy Shields")
        #Pilots                                         
        Rose = Pilot("Intrepid Rose", Majestic, False, False, True, ["powersword"], 3, 2, "Void")
        Nighthawk = Pilot("Nighthawk", Majestic, False, False, True, ["burst cannon"], 2, 3, "Void")
        Scorpion = Pilot("Scorpion", Leviathan, False, False, True, ["burst cannon", "powersword"], 1, 4, "Void")
        AzureKite = Pilot("Azure Kite", Leviathan, False, False, True, ["burst cannon", "powersword"], 4, 1, "Void")
        #Shields
        Aegis = Shield("Aegis", 2, 1)
        #Weapons
        Powersword = Weapon("Powersword", 3, "melee", 0, 1)
        Burst_Cannon = Weapon("Burst Cannon", 3, "Close", 2, 0)
        n = 1
        #Locations
        Crashsite = Location("Crashsite", "Far", "High Danger", ["killbots"])
        Bayport = Location("Bayport", "Close", "Low Danger", [])
        Resource_Types = ["Scrap", "Drone Constructors", "Fuel Rods", "Credits"]
        City = "Bayport City"
        Zone_List = ["spaceport", "mineral extractor", "residential housing", "broadcast tower", "entertainment stadium", "standard template constructor", "shipyard", "medical facility", "research lab", "greenhouses", "supply depot", "armory", "desalination plant", "shopping center", "crematorium", "schools", "university", "data archives", "public transit hub"]
        #Generate current location
        if Current_Location == "Void":
            if City == "Bayport City":
                n = random.randint(0,15)
                Current_Location = Zone_List[n]
        Distance_From_City = 0
        Danger_Level = "Low"
        Hazards = []
        Attacker = Rose
        Defender = Scorpion
        Startup = False
 
#Actions
def Travel_Random():
    n = random.randint(0,15)
    Current_Location = Zone_List[n]
    print(Current_Location)
    return Current_Location
 
def Roll_to_hit():
    Attacker = Rose
    Defender = Scorpion
    # print("Attacker: ")
    # Attacker = input()
    # if Attacker == "": Attacker = Rose
    # if Attacker == "Rose": Attacker = Rose
    # print("Defender: ")
    # Defender = input()
    # if Defender == "": Defender = Scorpion
    # if Defender == "Scorpion": Defender = Scorpion
    Hit_Roll = (Attacker.attack + random.randint(0,20))
    if "powersword" in Attacker.weapons:
        Hit_Roll = (Attacker.attack + random.randint(0,20) + Powersword.attack)
    Target_Number = Defender.defence + 10
    if Hit_Roll >= Target_Number or Hit_Roll == 20:
        if Defender.injured == True:
            Defender.alive = False
        if Defender.injured == False:
            Defender.injured = True
            print("Target Injured:" + str(Defender.injured))
    else: print("miss")
    Outcome = ["Hit:" + str(Hit_Roll), "Target Injured:" + str(Defender.injured), "Target Alive:" + str(Defender.alive)]
    print(Outcome)
    return Outcome

def Locate_Me():
    print(Current_Location)
 
def Save_Game():
    savegame = open("Documents/Python_Exploration/Mission_Control/savegame.txt", "w")
    savegame.write(str(Rose.name) + " piloting: battlesuit " + str(Rose.battlesuit.name) + " " + str(Roll_to_hit_outcome))
    savegame.close()
    savegame = open("Documents/Python_Exploration/Mission_Control/savegame.txt", "r")
    print(savegame.read())
 
Random_Location = Travel_Random()
My_Location = Locate_Me()
Roll_to_hit_outcome = Roll_to_hit()
 
GPS_Position = [North = 0, South = 0, East = 0, West = 0]

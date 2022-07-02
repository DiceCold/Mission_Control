import pygame
import random
from sys import exit
import pygame

Startup = True

#Classes
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
class Mission:
    def __init__(self, name, location, threat_level, Hazards, active):
            self.name = name
            self.location = location
            self.threat_level = threat_level
            self.Hazards = Hazards

if Startup == True: #Load Data
    if Startup == True: #Load Battlesuits
        Majestic = Battlesuit("Majestic", 5, "Quick", "Fusion Core", 3, "Light Shields")
        Leviathan = Battlesuit("Leviathan", 12, "Slow", "Fusion Core", 1, "Heavy Shields")
    if Startup == True: #Load Pilots
        Rose = Pilot("Intrepid Rose", Majestic, False, False, True, ["powersword"], 3, 2, "Void")
        Nighthawk = Pilot("Nighthawk", Majestic, False, False, True, ["burst cannon"], 2, 3, "Void")
        Scorpion = Pilot("Scorpion", Leviathan, False, False, True, ["burst cannon", "powersword"], 1, 4, "Void")
        AzureKite = Pilot("Azure Kite", Leviathan, False, False, True, ["burst cannon", "powersword"], 4, 1, "Void")
        Lightbringer = Pilot("Lightbringer", Leviathan, False, False, True, ["burst cannon", "powersword"], 4, 1, "Void")
    if Startup == True: #Load Weapons
        Powersword = Weapon("Powersword", 3, "melee", 0, 1)
        Burst_Cannon = Weapon("Burst Cannon", 3, "Close", 2, 0)
    if Startup == True: #Load Shields
        Aegis = Shield("Aegis", 2, 1)
        Light_shield = Shield("Light Shield", 1, 1)
    if Startup == True: #Load Locations
        Current_Location = "Void"
        Crashsite = Location("Crashsite", [600,400], "High Danger", ["killbots"])
        Bayport = Location("Bayport", "Close", "Low Danger", [])
        Resource_Types = ["Scrap", "Drone Constructors", "Fuel Rods", "Credits"]
        City = "Bayport City"
        Zone_List = ["spaceport", "mineral extractor", "residential housing", "broadcast tower", "entertainment stadium", "standard template constructor", "shipyard", "medical facility", "research lab", "greenhouses", "supply depot", "armory", "desalination plant", "shopping center", "crematorium", "schools", "university", "data archives", "public transit hub"]#Load Locations#Load Locations
        if Current_Location == "Void":
                if City == "Bayport City":
                    n = random.randint(0,15)
                    Current_Location = Zone_List[n]
        Distance_From_City = 0
    if Startup == True: #Load Missions
        Mission_Active = False
        Mission_1 = Mission("Train Robbery", Crashsite, 1, ["Raiders"], False)
    if Startup == True: #Load Other
        n = 1
        Danger_Level = "Low"
        Hazards = []
        Attacker = Rose
        Defender = Scorpion
        pygame.init()
        screen = pygame.display.set_mode((1920,1080))
        pygame.display.set_caption("Mission_Control")
        clock = pygame.time.Clock()
        test_font = pygame.font.Font('/Users/Graeme/Mission_Control/font/Pixeltype.ttf', 50)
        game_active = True
        map_active = False
        mission_screen_Active = False
        pause = False
        Mission_1_Active = False
        Pilot_Select = False
        player_y_pos = 300
        #text_surface = test_font.render('Mission Control', True, 'Black')
        Mission_1_Dialogue = 0
        player_surface = pygame.image.load('/Users/Graeme//Mission_Control/graphics/player/player_walk_1.png').convert_alpha()
        player_rect = player_surface.get_rect(midbottom = (80,player_y_pos))
        #snail_rect = snail_surface.get_rect(midbottom = (600,300))
        Mission_Screen_Frame_Black_Grey_BG = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Mission_Assignment_Screen_Black_Grey.png').convert_alpha()
        player_gravity = 0
        Pilot_Selected = "None"
        Mission_Screen_Active = False

        #Skills = [perception, mobility, armor, weapons, science, social, engineering]   
    if Startup == True: #Load Images    
        map_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/green_map_framed_icons.png').convert_alpha()
        map_rect = map_surf.get_rect(center = (960,540))
        pause_menu_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/pause_menu.png').convert()
        pause_menu_rect = pause_menu_surf.get_rect(topleft = (0,0))
        quit_button_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/quit_button.png').convert()
        quit_button_rect = quit_button_surf.get_rect(topleft = (0,540))
        X_Button_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/X_Button.png').convert_alpha()
        X_Button_rect = X_Button_surf.get_rect(topleft = (100,50))
        dashboard_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/Cockpit1.png').convert_alpha()
        dashboard_rect = dashboard_surf.get_rect(midbottom = (960,810))
        mission_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Story/Mission_Screen1_1.png').convert_alpha()
        mission_rect = mission_surf.get_rect(center = (960,540))
        planet_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/Planet1.png').convert_alpha()
        planet_rect = planet_surf.get_rect(topleft = (0,0))
        clickablemap_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/clickscreen.png').convert_alpha()
        clickablemap_rect = clickablemap_surf.get_rect(topleft = (0,0))
        Mission_Icon_1_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/bionic_eye_lowres_green.png').convert_alpha()
        Mission_Icon_1_rect = Mission_Icon_1_surf.get_rect(topleft = (960,540))
        Nighthawk_Pilot_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Pilots/Nighthawk_Standing_Default.png').convert_alpha()
        Nighthawk_Pilot_rect = Nighthawk_Pilot_surf.get_rect(topleft = (1500,200))
        Intrepid_Rose_Pilot_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Pilots/Intrepid_Rose_Standing_Default.png').convert_alpha()
        Intrepid_Rose_Pilot_rect = Intrepid_Rose_Pilot_surf.get_rect(topleft = (1500,200))
        Lightbringer_Pilot_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Pilots/Lightbringer_Standing_Default.png').convert_alpha()
        Lightbringer_Pilot_rect = Lightbringer_Pilot_surf.get_rect(topleft = (1500,200))
    if Startup == True: #Load Mission 1
        Mission_Screen_Frame_Black_BG_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/White_Frame_Black_BG.png').convert_alpha()
        Mission_Screen_Text_1_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Story/Mission_Text_1.png').convert_alpha()
        Mission_Screen_Pilot_List_Right_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Mission_Pilot_List_Right.png').convert_alpha()
        Pilot_List_Name_Nighthawk_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Pilot_List_Name_Nighthawk.png').convert_alpha()
        Pilot_List_Name_Intrepid_Rose_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Pilot_List_Name_Intrepid_Rose.png').convert_alpha()
        Pilot_List_Name_Lightbringer_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Pilot_List_Name_Lightbringer.png').convert_alpha()
        Pilot_List_Name_Nighthawk_Assigned_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Pilot_List_Name_Nighthawk_Assigned.png').convert_alpha()
        Mission_Screen_Green_Filter = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Mission_Filter_Green.png')
        Mission_Screen_Frame_White_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/White_Frame.png').convert_alpha()
        Pilot_List_Name_Nighthawk_rect = Pilot_List_Name_Nighthawk_surf.get_rect(topleft = (1400,250))
        Pilot_List_Name_Intrepid_Rose_rect = Pilot_List_Name_Intrepid_Rose_surf.get_rect(topleft = (1400,350))
        Pilot_List_Name_Lightbringer_rect = Pilot_List_Name_Lightbringer_surf.get_rect(topleft = (1400,450))
        Text_Continue_Button_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Interface/Text_Continue.png').convert_alpha()
        Text_Continue_Button_rect = Text_Continue_Button_surf.get_rect(topleft = (100,100))
        Mission_1_Nighthawk_Dialogue_1_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Story/Mission_1_Nighthawk_Dialogue.png').convert_alpha()
        Mission_1_Nighthawk_Dialogue_1_rect = Mission_1_Nighthawk_Dialogue_1_surf.get_rect(topleft = (200,200))
        Mission_1_Intrepid_Rose_Dialogue_1_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Story/Mission_1_Intrepid_Rose_Dialogue.png').convert_alpha()
        Mission_1_Intrepid_Rose_Dialogue_1_rect = Mission_1_Intrepid_Rose_Dialogue_1_surf.get_rect(topleft = (200,200))
        Mission_1_Lightbringer_Dialogue_1_surf = pygame.image.load('/Users/Graeme/Mission_Control/Art_assets/Story/Mission_1_Lightbringer_Dialogue.png').convert_alpha()
        Mission_1_Lightbringer_Dialogue_1_rect = Mission_1_Lightbringer_Dialogue_1_surf.get_rect(topleft = (200,200))
        screen.blit(planet_surf,(0,0))
    if Startup == True: #End Startup
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
    #print(Outcome)
    return Outcome
def Locate_Me():
    print(Current_Location)
    #pass
def Save_Game():
    savegame = open("Documents/Python_Exploration/Mission_Control/savegame.txt", "w")
    savegame.write(str(Rose.name) + " piloting: battlesuit " + str(Rose.battlesuit.name) + " " + str(Roll_to_hit_outcome))
    savegame.close()
    savegame = open("Documents/Python_Exploration/Mission_Control/savegame.txt", "r")
    print(savegame.read())

Random_Location = Travel_Random()
My_Location = Locate_Me()
Roll_to_hit_outcome = Roll_to_hit()
#GPS_Position = [North = 0, South = 0, East = 0, West = 0]

while True: #Game Cycle
    for event in pygame.event.get(): #Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active == True:
            # if event.type == pygame.KEYDOWN: #Player Jump
            #     if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
            #         player_gravity = -20
            if event.type == pygame.KEYDOWN: #Toggle Map
                if event.key == pygame.K_m:
                    if map_active == True:
                        map_active = False
                    else:
                        map_active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click dashboard map for full map
                if clickablemap_rect.collidepoint(event.pos):
                    #player_gravity = -20
                    map_active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click mission icon 1
                if Mission_Icon_1_rect.collidepoint(event.pos) and Mission_1_Active == False:
                    map_active = False
                    Mission_Screen_Active = True
                    Mission_1_Dialogue = 1
                    Mission_1_Active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Continue to pilot select
                if Text_Continue_Button_rect.collidepoint(event.pos) and Mission_1_Active == True:
                    Mission_1_Dialogue = 0
                    Pilot_Select = True
                    map_active = False
            if Pilot_Select == True:
                if event.type == pygame.MOUSEBUTTONDOWN: #Select a Pilot
                    # if Pilot_List_Name_Nighthawk_rect.collidepoint(event.pos) and Pilot_Select == True:
                    #     Pilot_Selected = Nighthawk
                    #     Pilot_Select = False
                    if Pilot_List_Name_Intrepid_Rose_rect.collidepoint(event.pos) and Pilot_Select == True:
                        Pilot_Selected = Rose
                        Pilot_Select = False
                        Mission_1_Dialogue = 2
                    if Pilot_List_Name_Lightbringer_rect.collidepoint(event.pos) and Pilot_Select == True:
                        Pilot_Selected = Lightbringer
                        Pilot_Select = False
                        Mission_1_Dialogue = 3
            if event.type == pygame.MOUSEBUTTONDOWN: #Close mission window
                if X_Button_rect.collidepoint(event.pos):
                    if Mission_Screen_Active == True:
                        Mission_Screen_Active = False
                        Mission_1_Dialogue = 0
                        Mission_1_Active = False
                        map_active = False
                    if Mission_1_Dialogue == 1:
                        Mission_1_Dialogue = 0
                        Mission_1_Active = False
                        map_active = False
                    if Pilot_Select == True:
                        Pilot_Select = False
                        Mission_1_Active = False
                        map_active = False
            if event.type == pygame.KEYDOWN: #Pause Menu
                if event.key == pygame.K_ESCAPE:
                    if pause == False:
                        pause = True
                    else:
                        pause = False
            if event.type == pygame.MOUSEBUTTONDOWN: #Quit the game
                if pause == True:
                    if quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        exit()

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                #snail_rect.x = 800
    if game_active == True: #Render Screen
        #screen.blit(text_surface,(300,50))
        #display_score()
        screen.blit(planet_surf,(0,0))
        screen.blit(dashboard_surf,(0,0))
        screen.blit(clickablemap_surf,(0,0))
    
        #snail_rect.x -= 4
        #if snail_rect.right <= 0: snail_rect.left = 800
        #screen.blit(snail_surface,snail_rect)
        player_gravity += 1
        #screen.blit(player_surface,player_rect)
        player_rect.y += player_gravity
        if player_rect.bottom >= 300: player_rect.bottom = 300
        #if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            #map_active = True
            #if snail_rect.colliderect(player_rect):
            #game_active = False
    else: #Render Black Screen
        screen.fill('Black')
        #screen.blit(map_surf,(0,-50))
    if map_active == True: #Show Map + Mission Icons
        screen.blit(map_surf,(map_rect))
        screen.blit(Mission_Icon_1_surf,(Mission_Icon_1_rect)) 
    # if mission_screen == True: #Show Mission Screen
    #     screen.blit(mission_surf,(mission_rect))
    #     screen.blit(Text_Continue_Button_surf,(Text_Continue_Button_rect))
    if Mission_Screen_Active == True:   
        screen.blit(Mission_Screen_Frame_Black_BG_surf,(0,0))
        # screen.blit(Mission_Screen_Text_1_surf,(0,0))
        screen.blit(X_Button_surf,(X_Button_rect))
        screen.blit(Mission_Screen_Frame_White_surf,(0,0))
    if Mission_1_Dialogue == 1:
        screen.blit(Mission_1_Nighthawk_Dialogue_1_surf,(Mission_1_Nighthawk_Dialogue_1_rect))
        screen.blit(Nighthawk_Pilot_surf,(Nighthawk_Pilot_rect))
        screen.blit(Mission_Screen_Green_Filter,(0,150))
        screen.blit(Mission_Screen_Frame_White_surf,(0,0))
        screen.blit(Text_Continue_Button_surf,(Text_Continue_Button_rect))
        screen.blit(X_Button_surf,(X_Button_rect))
    if Pilot_Select == True:
        screen.blit(Mission_Screen_Pilot_List_Right_surf,(0,0))
        screen.blit(Pilot_List_Name_Nighthawk_surf,(Pilot_List_Name_Nighthawk_rect))
        screen.blit(Pilot_List_Name_Intrepid_Rose_surf,(Pilot_List_Name_Intrepid_Rose_rect))
        screen.blit(Pilot_List_Name_Lightbringer_surf,(Pilot_List_Name_Lightbringer_rect))
        screen.blit(Mission_Screen_Green_Filter,(0,150))
        screen.blit(Mission_Screen_Frame_White_surf,(0,0))
        screen.blit(X_Button_surf,(X_Button_rect))
    if Mission_1_Dialogue == 2:
        screen.blit(Mission_1_Intrepid_Rose_Dialogue_1_surf,(Mission_1_Intrepid_Rose_Dialogue_1_rect))
        screen.blit(Intrepid_Rose_Pilot_surf,(Intrepid_Rose_Pilot_rect))
        screen.blit(Mission_Screen_Green_Filter,(0,150))
        screen.blit(Mission_Screen_Frame_White_surf,(0,0))
        screen.blit(Text_Continue_Button_surf,(Text_Continue_Button_rect))
        screen.blit(X_Button_surf,(X_Button_rect))
    if Mission_1_Dialogue == 3:
        screen.blit(Mission_1_Lightbringer_Dialogue_1_surf,(Mission_1_Lightbringer_Dialogue_1_rect))
        screen.blit(Lightbringer_Pilot_surf,(Lightbringer_Pilot_rect))
        screen.blit(Mission_Screen_Green_Filter,(0,150))
        screen.blit(Mission_Screen_Frame_White_surf,(0,0))
        screen.blit(Text_Continue_Button_surf,(Text_Continue_Button_rect))
        screen.blit(X_Button_surf,(X_Button_rect))

    if pause == True: #Show Pause Screen
        screen.blit(pause_menu_surf, (0,0))
        screen.blit(quit_button_surf, (0,540))

    pygame.display.update()
    clock.tick(60)


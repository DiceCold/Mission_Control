import pygame
import random
from sys import exit
import os


Startup = True
Invuln_timer = 0
Shadowstalker_Shields = True
Shadowstalker_Armor_Damaged = False
Shadowstalker_Armor_Heavilly_Damaged = False
Shadowstalker_Pilot_Injured = False
Hit_Successful = False


#Classes
class Pilot:
    def __init__(self, name, battlesuit, shields_up, battlesuit_damaged, battlesuit_heavilly_damaged, injured, alive, weapons, attack, defence, location):
            self.name = name
            self.battlesuit = battlesuit
            self.shields_up = shields_up
            self.battlesuit_damaged = battlesuit_damaged
            self.battlesuit_heavilly_damaged = battlesuit_heavilly_damaged
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
    def __init__(self, name, attack, distance, cost_use, cooldown):
            self.name = name
            self.attack = attack
            self.distance = distance
            self.cost_use = cost_use
            self.cooldown = cooldown
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
    def __init__(self, name, location, threat_level, Hazards, Active):
            self.name = name
            self.location = location
            self.threat_level = threat_level
            self.Hazards = Hazards
            self.Active = Active

if Startup == True: #Load Data
    if Startup == True: #Load Battlesuits
        Majestic = Battlesuit("Majestic", 5, "Quick", "Fusion Core", 3, "Light Shields")
        Leviathan = Battlesuit("Leviathan", 12, "Slow", "Fusion Core", 1, "Heavy Shields")
    if Startup == True: #Load Pilots
        Rose = Pilot("Intrepid Rose", Majestic, True, False, False, False, True, ["powersword"], 3, 2, "Void")
        Nighthawk = Pilot("Nighthawk", Majestic, True, False, False, False, True, ["burst cannon"], 2, 3, "Void")
        Scorpion = Pilot("Scorpion", Leviathan, True, False, False, False, True, ["burst cannon", "powersword"], 1, 4, "Void")
        AzureKite = Pilot("Azure Kite", Leviathan, True, False, False, False, True, ["burst cannon", "powersword"], 4, 1, "Void")
        Lightbringer = Pilot("Lightbringer", Leviathan, True, False, False, False, True, ["burst cannon", "powersword"], 4, 1, "Void")
        Unassigned = Pilot("Unassigned", Majestic, True, False, False, False, True, ["powersword"], 3, 2, "Void")
    if Startup == True: #Load Weapons
        Powersword = Weapon("Powersword", 3, "melee", 0, 100)
        Burst_Cannon = Weapon("Burst Cannon", 3, "Close", 2, 200)
        Beam_Cannon = Weapon("Beam Cannon", 3, "Close", 0, 200)
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
        Screen_Width = 1920
        Screen_Height = 1080
        pygame.init()
        screen = pygame.display.set_mode((Screen_Width,Screen_Height))
        pygame.display.set_caption("Mission_Control")
        clock = pygame.time.Clock()
        test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
        Game_Active = True
        Map_Active = False
        pause = False
        Mission_1_Active = False
        Pilot_Select = False
        player_y_pos = 300
        #text_surface = test_font.render('Mission Control', True, 'Black')
        Mission_1_Dialogue = 0
        Mission_Screen_Frame_Black_Grey_BG = pygame.image.load('Art_assets/Interface/Mission_Assignment_Screen_Black_Grey_75.png').convert_alpha()
        player_gravity = 0
        Pilot_Selected = "None"
        Draw_Mission_Page = False

        #Skills = [perception, mobility, armor, weapons, science, social, engineering]   
    if Startup == True: #Load Images    
        map_surf = pygame.image.load('Art_assets/Interface/green_map_framed_icons_75.png').convert_alpha()
        map_rect = map_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        pause_menu_surf = pygame.image.load('Art_assets/Interface/pause_menu.png').convert()
        pause_menu_rect = pause_menu_surf.get_rect(topleft = (0,0))
        quit_button_surf = pygame.image.load('Art_assets/Interface/quit_button.png').convert()
        quit_button_rect = quit_button_surf.get_rect(topleft = (0,540))
        X_Button_surf = pygame.image.load('Art_assets/Interface/X_Button_75.png').convert_alpha()
        X_Button_rect = X_Button_surf.get_rect(topleft = (300,150))
        dashboard_surf = pygame.image.load('Art_assets/Interface/Cockpit1.png').convert_alpha()
        dashboard_rect = dashboard_surf.get_rect(midbottom = (960,810))
        #mission_surf = pygame.image.load('Art_assets/Story/Mission_Screen1_1.png').convert_alpha()
        #mission_rect = mission_surf.get_rect(center = (960,540))
        planet_surf = pygame.image.load('Art_assets/Interface/Planet1.png').convert_alpha()
        planet_rect = planet_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        clickablemap_surf = pygame.image.load('Art_assets/Interface/clickscreen.png').convert_alpha()
        clickablemap_rect = clickablemap_surf.get_rect(topleft = (0,0))
        Mission_Icon_1_surf = pygame.image.load('Art_assets/Interface/bionic_eye_lowres_green.png').convert_alpha()
        Mission_Icon_1_rect = Mission_Icon_1_surf.get_rect(topleft = (960,540))
        Nighthawk_Pilot_surf = pygame.image.load('Art_assets/Pilots/Nighthawk_Standing_Default_75.png').convert_alpha()
        Nighthawk_Pilot_rect = Nighthawk_Pilot_surf.get_rect(topleft = (1350,300))
        Intrepid_Rose_Pilot_surf = pygame.image.load('Art_assets/Pilots/Intrepid_Rose_Standing_Default_75.png').convert_alpha()
        Intrepid_Rose_Pilot_rect = Intrepid_Rose_Pilot_surf.get_rect(topleft = (1350,300))
        Lightbringer_Pilot_surf = pygame.image.load('Art_assets/Pilots/Lightbringer_Standing_Default_75.png').convert_alpha()
        Lightbringer_Pilot_rect = Lightbringer_Pilot_surf.get_rect(topleft = (1350,300))
    if Startup == True: #Load Air Battle
        Dogfight_Screen = False
        Jet_pos_x = 750
        Jet_pos_y = 500
        Jet_momentum_x = -1.5
        Jet_momentum_y = -0.5
        Radio_pos_x = 600
        Radio_pos_y = 550
        Jet2_pos_x = random.randint(250,500)
        Jet2_pos_y = random.randint(250,500)
        Jet2_momentum_x = 0.5
        Jet2_momentum_y = 0.5
        test_surf = pygame.Surface((100,200))
        test_surf.fill("Red")
        Map_surf = pygame.image.load('Art_assets/Interface/green_map_framed_icons_75.png').convert_alpha()
        Jet_surf = pygame.image.load('Art_assets/Pilots/red_dot_icon.png').convert_alpha()
        Jet_surf = pygame.transform.scale(Jet_surf, (10,10))
        Jet_rect = Jet_surf.get_rect(center = (Jet_pos_x, Jet_pos_y))
        pilot1_surf = pygame.image.load('Art_assets/Pilots/red_dot_icon.png').convert_alpha()
        pilot1_surf = pygame.transform.scale(Jet_surf, (10,10))
        pilot1_rect = Jet_surf.get_rect(center = (800, 800))
        Jet2_surf = pygame.image.load('Art_assets/Pilots/blue_dot_icon.png').convert_alpha()
        Jet2_surf = pygame.transform.scale(Jet2_surf, (10,10))
        Jet2_rect = Jet2_surf.get_rect(center = (Jet2_pos_x, Jet_pos_y))
        Jet2_Radio_Distance_x = 0
        Jet2_Radio_Distance_y = 0
        Radio_surf = pygame.image.load('Art_assets/Interface/radio.png').convert_alpha()
        Radio_surf = pygame.transform.scale(Radio_surf, (40,40))
        Radio_rect = Radio_surf.get_rect(center = (Radio_pos_x, Radio_pos_y))
        Pilot_1_Health_surf = pygame.image.load('Art_assets/Interface/Pilot_Systems_Full.png')
        Pilot_1_Health_rect = Pilot_1_Health_surf.get_rect(topleft = (1300,375))
        Pilot_1_Shields_Down_surf = pygame.image.load('Art_assets/Interface/Shield_Hidden.png')
        Pilot_1_Shields_Down_rect = Pilot_1_Shields_Down_surf.get_rect(topleft = (1310,390))
        Pilot_1_Health_Current_surf = pygame.image.load('Art_assets/Interface/Pilot_Health_Full.png')
        Pilot_1_Health_Current_rect = Pilot_1_Health_Current_surf.get_rect(topleft = (1397,375))
        pilot1_momentum_x = 0
        pilot1_momentum_y = 0
        global Combat_Pilot_1
        global Combat_Pilot_2
        global Combat_Pilot_3
        Combat_Pilot_1 = Unassigned
        Combat_Pilot_2 = Unassigned
        Combat_Pilot_3 = Unassigned

        Dogfight_Screen = True


    if Startup == True: #Load Mission 1
        Mission_Screen_Frame_Black_BG_surf = pygame.image.load('Art_assets/Interface/White_Frame_Black_BG_75.png').convert_alpha()
        Mission_Screen_Frame_Black_BG_rect = Mission_Screen_Frame_Black_BG_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        Mission_Screen_Green_Filter_surf = pygame.image.load('Art_assets/Interface/Mission_Filter_Green.png').convert_alpha()
        Mission_Screen_Green_Filter_rect = Mission_Screen_Green_Filter_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        Mission_Screen_Frame_White_surf = pygame.image.load('Art_assets/Interface/White_Frame_75.png').convert_alpha()
        Mission_Screen_Frame_White_rect = Mission_Screen_Frame_White_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        Mission_Screen_Text_1_surf = pygame.image.load('Art_assets/Story/Mission_Text_1.png').convert_alpha()
        Mission_Screen_Text_1_rect = Mission_Screen_Text_1_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        Mission_Screen_Pilot_List_Right_surf = pygame.image.load('Art_assets/Interface/Mission_Pilot_List_Right_75.png').convert_alpha()
        Mission_Screen_Pilot_List_Right_rect = Mission_Screen_Pilot_List_Right_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        Pilot_List_Name_Nighthawk_surf = pygame.image.load('Art_assets/Interface/Pilot_List_Name_Nighthawk_75.png').convert_alpha()
        Pilot_List_Name_Intrepid_Rose_surf = pygame.image.load('Art_assets/Interface/Pilot_List_Name_Intrepid_Rose_75.png').convert_alpha()
        Pilot_List_Name_Lightbringer_surf = pygame.image.load('Art_assets/Interface/Pilot_List_Name_Lightbringer_75.png').convert_alpha()
        Pilot_List_Name_Nighthawk_Assigned_surf = pygame.image.load('Art_assets/Interface/Pilot_List_Name_Nighthawk_Assigned.png').convert_alpha()
        Pilot_List_Name_Nighthawk_rect = Pilot_List_Name_Nighthawk_surf.get_rect(topleft = (1300,325))
        Pilot_List_Name_Intrepid_Rose_rect = Pilot_List_Name_Intrepid_Rose_surf.get_rect(topleft = (1300,400))
        Pilot_List_Name_Lightbringer_rect = Pilot_List_Name_Lightbringer_surf.get_rect(topleft = (1300,475))
        Text_Continue_Button_surf = pygame.image.load('Art_assets/Interface/Text_Continue_75.png').convert_alpha()
        Text_Continue_Button_rect = Text_Continue_Button_surf.get_rect(topleft = (300,200))
        Mission_1_Nighthawk_Dialogue_1_surf = pygame.image.load('Art_assets/Story/Mission_1_Nighthawk_Dialogue.png').convert_alpha()
        Mission_1_Nighthawk_Dialogue_1_rect = Mission_1_Nighthawk_Dialogue_1_surf.get_rect(topleft = (300,275))
        Mission_1_Intrepid_Rose_Dialogue_1_surf = pygame.image.load('Art_assets/Story/Mission_1_Intrepid_Rose_Dialogue.png').convert_alpha()
        Mission_1_Intrepid_Rose_Dialogue_1_rect = Mission_1_Intrepid_Rose_Dialogue_1_surf.get_rect(topleft = (300,275))
        Mission_1_Lightbringer_Dialogue_1_surf = pygame.image.load('Art_assets/Story/Mission_1_Lightbringer_Dialogue.png').convert_alpha()
        Mission_1_Lightbringer_Dialogue_1_rect = Mission_1_Lightbringer_Dialogue_1_surf.get_rect(topleft = (300,275))
        screen.blit(planet_surf,(0,0))
    if Startup == True: #End Startup
        Startup = False
 
#Actions

def draw_screen():
    if Game_Active == True:    
        screen.blit(planet_surf,(0,0))
        screen.blit(dashboard_surf,(0,0))
        screen.blit(clickablemap_surf,(0,0))
    else: screen.fill('Black')
    if Map_Active == True: #Show Map + Mission Icons
        screen.blit(map_surf,(map_rect))
        screen.blit(Mission_Icon_1_surf,(Mission_Icon_1_rect))
        screen.blit(X_Button_surf,(X_Button_rect))
    if Draw_Mission_Page == True:
        screen.blit(Mission_Screen_Frame_Black_BG_surf,(Mission_Screen_Frame_Black_BG_rect))
    if Mission_1_Dialogue == 1:
        screen.blit(Mission_1_Nighthawk_Dialogue_1_surf,(Mission_1_Nighthawk_Dialogue_1_rect))
        screen.blit(Nighthawk_Pilot_surf,(Nighthawk_Pilot_rect))
    if Mission_1_Dialogue == 2:
        screen.blit(Mission_1_Intrepid_Rose_Dialogue_1_surf,(Mission_1_Intrepid_Rose_Dialogue_1_rect))
        screen.blit(Intrepid_Rose_Pilot_surf,(Intrepid_Rose_Pilot_rect))
    if Mission_1_Dialogue == 3:
        screen.blit(Mission_1_Lightbringer_Dialogue_1_surf,(Mission_1_Lightbringer_Dialogue_1_rect))
        screen.blit(Lightbringer_Pilot_surf,(Lightbringer_Pilot_rect))
    if Pilot_Select == True:
        screen.blit(Mission_Screen_Pilot_List_Right_surf,(Mission_Screen_Pilot_List_Right_rect))
        screen.blit(Pilot_List_Name_Nighthawk_surf,(Pilot_List_Name_Nighthawk_rect))
        screen.blit(Pilot_List_Name_Intrepid_Rose_surf,(Pilot_List_Name_Intrepid_Rose_rect))
        screen.blit(Pilot_List_Name_Lightbringer_surf,(Pilot_List_Name_Lightbringer_rect))
    if Draw_Mission_Page == True:
        screen.blit(Mission_Screen_Green_Filter_surf,(Mission_Screen_Green_Filter_rect))
        screen.blit(Mission_Screen_Frame_White_surf,(Mission_Screen_Frame_White_rect))
        screen.blit(X_Button_surf,(X_Button_rect))
        screen.blit(Text_Continue_Button_surf,(Text_Continue_Button_rect))
        #text_surface = test_font.render('Mission Control', True, 'Black')
        #screen.blit(text_surface,(1000,500))
    if Dogfight_Screen == True: #Aerial Combat
        (screen.blit(Map_surf,(map_rect)))
        screen.blit(Radio_surf,(Radio_rect))
        screen.blit(Jet_surf,(Jet_rect))
        screen.blit(Jet2_surf,(Jet2_rect))
        screen.blit(Mission_Screen_Frame_White_surf,(Mission_Screen_Frame_White_rect))
        screen.blit(X_Button_surf,(X_Button_rect))
        screen.blit(Mission_Screen_Pilot_List_Right_surf,(Mission_Screen_Pilot_List_Right_rect))
        screen.blit(Pilot_List_Name_Nighthawk_surf,(Pilot_List_Name_Nighthawk_rect))
        screen.blit(Pilot_1_Health_surf,(Pilot_1_Health_rect))
        screen.blit(Pilot_1_Health_Current_surf,(Pilot_1_Health_Current_rect))

def Save_Game():
    savegame = open("Documents/Python_Exploration/Mission_Control/savegame.txt", "w")
    savegame.write(str(Rose.name) + " piloting: battlesuit " + str(Rose.battlesuit.name) + " " + str(Roll_to_hit_outcome))
    savegame.close()
    savegame = open("Documents/Python_Exploration/Mission_Control/savegame.txt", "r")
    print(savegame.read())
def Roll_to_hit():
    Attacker = Combat_Pilot_1
    Defender = Scorpion
    global Hit_Successful
    Hit_Roll = (Attacker.attack + random.randint(0,20))
    if "powersword" in Attacker.weapons:
        Hit_Roll = (Attacker.attack + random.randint(0,20) + Powersword.attack)
    Target_Number = Defender.defence + 10
    if Hit_Roll >= Target_Number or Hit_Roll == 20:
        print("Hit")
        Hit_Successful = True
    else: print("miss")
def Register_Hit():
    global Hit_Successful
    global Nighthawk
    if Hit_Successful == True:
        if Combat_Pilot_1.shields_up == True:
            Combat_Pilot_1.shields_up = False
            Hit_Successful = False
        else:
            if Combat_Pilot_1.battlesuit_damaged == False:
                Combat_Pilot_1.battlesuit_damaged = True
                Hit_Successful = False
            else: 
                if Combat_Pilot_1.battlesuit_heavilly_damaged == False:
                    Combat_Pilot_1.battlesuit_heavilly_damaged = True
                    Hit_Successful = False
                else:
                    Combat_Pilot_1.injured = True
                    Hit_Successful = False
        # print("Shields On: " + str(Shadowstalker_Shields))
        # print("Armor Damaged: " + str(Shadowstalker_Armor_Damaged))
        # print("Armor Heavily Damaged: " + str(Shadowstalker_Armor_Heavilly_Damaged))
        # print("Pilot Injured: " + str(Shadowstalker_Pilot_Injured))
    if Combat_Pilot_1.shields_up == False:
        print("Shields down!")
    if Combat_Pilot_1.battlesuit_damaged:
        print("Battlesuit is damaged!")
    if Combat_Pilot_1.battlesuit_heavilly_damaged == True:
        print("!!! PILOT IN DANGER !!!")

#GPS_Position = [North = 0, South = 0, East = 0, West = 0]

while True: #Game Cycle
    for event in pygame.event.get(): #Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if Game_Active == True: #Buttons/clicking
            if event.type == pygame.KEYDOWN: #Toggle Map
                if event.key == pygame.K_m:
                    if Map_Active == True:
                        Map_Active = False
                    else:
                        Map_Active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click dashboard map for full map
                if clickablemap_rect.collidepoint(event.pos):
                    Map_Active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click mission icon 1
                if Mission_Icon_1_rect.collidepoint(event.pos) and Mission_1_Active == False:
                    Map_Active = False
                    Draw_Mission_Page = True
                    Mission_1_Dialogue = 1
                    Mission_1_Active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Continue to pilot select
                if Text_Continue_Button_rect.collidepoint(event.pos) and Mission_1_Active == True:
                    Mission_1_Dialogue = 0
                    Pilot_Select = True
                    Map_Active = False
            if event.type == pygame.MOUSEBUTTONDOWN: #Start dogfight
                if Text_Continue_Button_rect.collidepoint(event.pos) and Mission_1_Active == True:
                    if Pilot_Selected == Rose:
                        Mission_1_Dialogue = 0
                        Pilot_Select = False
                        Map_Active = False
                        Draw_Mission_Page = False
                        Dogfight_Screen = True
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
            if event.type == pygame.MOUSEBUTTONDOWN: #Close window
                if X_Button_rect.collidepoint(event.pos):
                    if Draw_Mission_Page == True:
                        Draw_Mission_Page = False
                        Mission_1_Dialogue = 0
                        Mission_1_Active = False
                        Map_Active = False
                    if Mission_1_Dialogue == 1:
                        Mission_1_Dialogue = 0
                        Mission_1_Active = False
                        Draw_Mission_Page = False
                        Map_Active = False
                    if Pilot_Select == True:
                        Pilot_Select = False
                        Mission_1_Active = False
                        Map_Active = False
                        Draw_Mission_Page = False
                    if Map_Active == True:
                        Map_Active = False
                    if Dogfight_Screen == True:
                        Dogfight_Screen = False
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

    draw_screen()
    if Dogfight_Screen == True: #Aerial Combat
        if Dogfight_Screen == True: #Pilot health display
            if Combat_Pilot_1.shields_up == False:
                screen.blit(Pilot_1_Shields_Down_surf,(Pilot_1_Shields_Down_rect))
            if Combat_Pilot_1.battlesuit_damaged:
                Pilot_1_Health_Current_surf = pygame.image.load('Art_assets/Interface/Pilot_Health_Half.png')
            if Combat_Pilot_1.battlesuit_heavilly_damaged:
                Pilot_1_Health_Current_surf = pygame.image.load('Art_assets/Interface/Pilot_Health_None.png')
            # if Dogfight_Screen == True: #Aerial maneuvering
        if Dogfight_Screen == True: #Jet position updating
            Jet_pos_y = (Jet_pos_y + Jet_momentum_y*0.1)
            Jet_pos_x = (Jet_pos_x + Jet_momentum_x*0.1)
            Jet_rect = Jet_surf.get_rect(center = (Jet_pos_x, Jet_pos_y))
            Jet2_pos_y = (Jet2_pos_y + Jet2_momentum_y*0.1)
            Jet2_pos_x = (Jet2_pos_x + Jet2_momentum_x*0.1)
            Jet2_rect = Jet2_surf.get_rect(center = (Jet2_pos_x, Jet2_pos_y))
            Invuln_timer += 1
        if Dogfight_Screen == True: #Jet targeting
            #Jet1 primary target distance
            Jet_target1 = "Radio_Tower"
            Jet_target2 = "Radio_Tower"
            Jet2_target1 = "Jet1"
            Jet2_target2 = "Jet1"
            if Jet_target1 == "Radio_Tower":
                Jet1_target1_distance_x = Jet_pos_x - Radio_pos_x
                Jet1_target1_distance_y = Jet_pos_y - Radio_pos_y
            if Jet_target1 == "Jet2":
                Jet1_target1_distance_x = Jet_pos_x - Jet2_pos_x
                Jet1_target1_distance_y = Jet_pos_y - Jet2_pos_y 
            #Jet1 secondary target distance
            if Jet_target2 == "Radio_Tower":
                Jet1_target2_distance_x = Jet_pos_x - Radio_pos_x
                Jet1_target2_distance_y = Jet_pos_y - Radio_pos_y
            if Jet_target2 == "Jet2":
                Jet1_target2_distance_x = Jet_pos_x - Jet2_pos_x
                Jet1_target2_distance_y = Jet_pos_y - Jet2_pos_y 

            #Jet2 primary target distance
            Jet2_target1 = "Radio_Tower"
            if Jet2_target1 == "Jet1":
                Jet2_target1_distance_x = Jet2_pos_x - Jet_pos_x
                Jet2_target1_distance_y = Jet2_pos_y - Jet_pos_y
            if Jet2_target1 == "Radio_Tower":
                Jet2_target1_distance_x = Jet2_pos_x - Radio_pos_x
                Jet2_target1_distance_y = Jet2_pos_y - Radio_pos_y
            #Jet2 secondary target distance
            Jet2_target1 = "Radio_Tower"
            if Jet2_target2 == "Jet1":
                Jet2_target2_distance_x = Jet2_pos_x - Jet_pos_x
                Jet2_target2_distance_y = Jet2_pos_y - Jet_pos_y
            if Jet2_target2 == "Radio_Tower":
                Jet2_target2_distance_x = Jet2_pos_x - Radio_pos_x
                Jet2_target2_distance_y = Jet2_pos_y - Radio_pos_y
        if Dogfight_Screen == True: #Control velocity
            #Speed limit
            if Jet2_momentum_x > 10:
                Jet2_momentum_x = 10
            if Jet2_momentum_y >10:
                Jet2_momentum_y = 10
            if Jet2_momentum_x < -10:
                Jet2_momentum_x = -10
            if Jet2_momentum_y < -10:
                Jet2_momentum_y = -10
            #Speed Boost
            if Jet2_momentum_x > -2 and Jet2_momentum_x < 2:
                Jet2_momentum_x = Jet2_momentum_x*1.05

            #Jet1 movement target
            if Jet1_target1_distance_x >= 0:
                Jet_momentum_x -= 0.01
                Jet_momentum_x -= 0.0002*Jet1_target1_distance_x
            else:
                Jet_momentum_x += 0.01
                Jet_momentum_x += 0.0002*abs(Jet1_target1_distance_x) 
            if Jet1_target1_distance_y >= 0:
                Jet_momentum_y -= 0.01
                Jet_momentum_y -= 0.001*Jet1_target1_distance_y
            else:
                Jet_momentum_y += 0.001*abs(Jet1_target1_distance_y)
                Jet_momentum_y += 0.01
            
            #Jet2 movement target
            if Jet2_target1_distance_x >= 0:
                Jet2_momentum_x -= 0.001*abs(Jet2_target1_distance_x)
                Jet2_momentum_x -= 0.01
            else:
                Jet2_momentum_x += 0.001*abs(Jet2_target1_distance_x)
                Jet2_momentum_x += 0.01
            if Jet2_target2_distance_y >= 0:
                Jet2_momentum_y -= 0.001*abs(Jet2_Radio_Distance_y)
                Jet2_momentum_y -= 0.01
            else:
                Jet2_momentum_y += 0.001*abs(Jet2_Radio_Distance_y)
                Jet2_momentum_y += 0.01
            #Jet2 attack target
            if abs(Jet2_target1_distance_x) < 30 and abs(Jet2_target1_distance_y) <30:
                pygame.draw.line(screen, (200,0,0), (Jet2_pos_x,Jet2_pos_y), (Jet_pos_x,Jet_pos_y), 5)
                print("Target Acquired")
                if Invuln_timer > 200:
                    Roll_to_hit()
                    Invuln_timer = 0
                if Hit_Successful == True:
                    Register_Hit()
                    print(Invuln_timer)
            
        # if Jet_rect.collidepoint(Jet2_rect.x, Jet2_rect.y): #Detect Melee Contact
        #     if Invuln_timer > 200:
        #         print("Contact")
        #         Roll_to_hit()
        #         Register_Hit()
        #         print(Invuln_timer)
        #         Jet2_momentum_y = Jet2_momentum_y * 2
        #         Invuln_timer = 0

    if pause == True: #Show Pause Screen
            screen.blit(pause_menu_surf, (0,0))
            screen.blit(quit_button_surf, (0,540))

    pygame.display.update()
    clock.tick(60)


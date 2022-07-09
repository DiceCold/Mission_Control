import pygame
import random
from sys import exit
import os
import copy


startup = True

if startup == True: #load Data
    if startup == True: #load classes
        class pilot:
            def __init__(self, name, battlesuit, injured, alive, location):
                    self.name = name
                    self.battlesuit = battlesuit
                    self.injured = injured
                    self.alive = alive
                    self.location = location
        class battlesuit:
            def __init__(self, name, refresh, mobility, shields, weapons, battlesuit_damaged, battlesuit_heavilly_damaged):
                    self.name = name
                    self.refresh = refresh
                    self.mobility = mobility
                    self.shields = shields
                    self.weapons = weapons
                    self.battlesuit_damaged = battlesuit_damaged
                    self.battlesuit_heavilly_damaged = battlesuit_heavilly_damaged
        class weapon:
            def __init__(self, name, attack, distance, cooldown):
                    self.name = name
                    self.attack = attack
                    self.distance = distance
                    self.cooldown = cooldown
        class shields:
            def __init__(self, name, cooldown, charged):
                    self.name = name
                    self.cooldown = cooldown
                    self.charged = charged
        class location:
            def __init__(self, name, Distance_From_City, danger_level, hazards):
                    self.name = name
                    self.Distance_From_City = Distance_From_City
                    self.danger_level = danger_level
                    self.hazards = hazards
        class mission:
            def __init__(self, name, location, threat_level, hazards, active):
                    self.name = name
                    self.location = location
                    self.threat_level = threat_level
                    self.hazards = hazards
                    self.active = active
        class jet
            def __init__(self, name, target, pos_x, pos_y, momentum_x, momentum_y, surf, rect)
                self.name = name
                self.target = target
                self.pos_x = pos_x
                self.pos_y = pos_y
                self.momentum_x = momentum_x
                self.momentum_y = momentum_y
                self.surf
                self.rect
    if startup == True: #load Weapons
        powersword = weapon("Powersword", 3, "melee", 100)
        burst_cannon = weapon("Burst cannon", 3, "Close", 200)
        beam_cannon = weapon("beam cannon", 3, "Close", 200)
        majestic_beam_cannon = copy.copy(beam_cannon)
    if startup == True: #load shields
        light_shield = shields("Light shields", 18, True)
        majestic_shield1 = copy.copy(light_shield)
        majestic_shield2 = copy.copy(light_shield)
        majestic_shield1.name = "Primary shield"
        majestic_shield2.name = "Secondary shield"
    if startup == True: #load Battlesuits
        Majestic = battlesuit("Majestic", 3, "Quick", [majestic_shield1, majestic_shield2], majestic_beam_cannon, False, False)
        Leviathan = battlesuit("Leviathan", 4, "Slow", light_shield, beam_cannon, False, False)
    if startup == True: #load pilots
        rose = pilot("Intrepid Rose", Majestic, False, True, "Void")
        rose_flyer = jet("Intrepid Rose", unassigned_flyer, 0, 0, 0, 0, copy.deepcopy(jet_surf),copy.deepcopy(jet_rect))
        nighthawk = pilot("Nighthawk", Majestic, False, True, "Void")
        nighthawk_flyer = jet("Nighthawk", unassigned_flyer, 0, 0, 0, 0, copy.deepcopy(jet_surf),copy.deepcopy(jet_rect))
        scorpion = pilot("Scorpion", Majestic, False, True, "Void")
        scorpion_flyer = jet("Scorpion", unassigned_flyer, 0, 0, 0, 0, copy.deepcopy(jet_surf),copy.deepcopy(jet_rect))
        azure = pilot("Azure Kite", Majestic, False, True, "Void")
        azure_flyer = jet("Azure Kite", unassigned_flyer, 0, 0, 0, 0, copy.deepcopy(jet_surf),copy.deepcopy(jet_rect))
        lightbringer = pilot("Lightbringer", Majestic, False, True, "Void")
        lightbringer_flyer = jet("Lightbringer", unassigned_flyer, 0, 0, 0, 0, copy.deepcopy(jet_surf),copy.deepcopy(jet_rect))
        unassigned = pilot("unassigned", Majestic, False, True, "Void")
        unassigned_flyer = jet("unassigned", unassigned_flyer, 0, 0, 0, 0, copy.deepcopy(jet_surf),copy.deepcopy(jet_rect))
        radio_flyer = jet("unassigned", unassigned_flyer, 0, 0, 0, 0, copy.deepcopy(jet_surf),copy.deepcopy(jet_rect))
    if startup == True: #load locations
        current_location = "Void"
        Crashsite = location("Crashsite", [600,400], "High danger", ["killbots"])
        Bayport = location("Bayport", "Close", "Low danger", [])
        Resource_Types = ["Scrap", "Drone Constructors", "Fuel Rods", "Credits"]
        City = "Bayport City"
        Zone_list = ["spaceport", "mineral extractor", "residential housing", "broadcast tower", "entertainment stadium", "standard template constructor", "shipyard", "medical facility", "research lab", "greenhouses", "supply depot", "armory", "desalination plant", "shopping center", "crematorium", "schools", "university", "data archives", "public transit hub"]#load locations#load locations
        if current_location == "Void":
                if City == "Bayport City":
                    n = random.randint(0,15)
                    current_location = Zone_list[n]
        Distance_From_City = 0
    if startup == True: #load missions
        mission_active = False
        mission_1 = mission("Train Robbery", Crashsite, 1, ["Raiders"], False)
        hazards = []
    if startup == True: #load Other
        danger_level = "Low"
        attacker = unassigned
        defender = unassigned
        pilot_selected = unassigned
        screen_width = 1920
        screen_height = 1080
        pygame.init()
        screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption("mission_control")
        clock = pygame.time.Clock()
        test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
        game_active = True
        map_active = False
        pause = False
        mission_1_active = False
        pilot_select = False
        mission_1_dialogue = 0
        draw_mission_page = False
        global target
        target = unassigned
        global hit_successful
        hit_successful = False
        global hit_roll
        hit_roll = 0
        global difficulty
        difficulty = 10
        interface_screen = False
        invuln_timer = 0
        #Skills = [perception, mobility, armor, weapons, science, social, engineering]   
    if startup == True: #load Images
        interface_screen_back_surf = pygame.image.load('art_assets/interface/interface_back_75.png').convert_alpha()
        interface_screen_back_rect = interface_screen_back_surf.get_rect(center = (screen_width/2,screen_height/2))
        green_filter_surf = pygame.image.load('art_assets/interface/green_filter.png').convert_alpha()
        green_filter_rect = green_filter_surf.get_rect(center = (screen_width/2,screen_height/2))
        interface_frame_surf = pygame.image.load('art_assets/interface/white_frame_75.png').convert_alpha()
        interface_frame_rect = interface_frame_surf.get_rect(center = (screen_width/2,screen_height/2))    
        map_surf = pygame.image.load('art_assets/interface/basic_map_75.png').convert_alpha()
        map_rect = map_surf.get_rect(center = (screen_width/2,screen_height/2))
        pause_menu_surf = pygame.image.load('art_assets/interface/pause_menu.png').convert()
        pause_menu_rect = pause_menu_surf.get_rect(topleft = (0,0))
        quit_button_surf = pygame.image.load('art_assets/interface/quit_button.png').convert()
        quit_button_rect = quit_button_surf.get_rect(topleft = (0,540))
        x_button_surf = pygame.image.load('art_assets/interface/x_button_75.png').convert_alpha()
        x_button_rect = x_button_surf.get_rect(topleft = (300,150))
        dashboard_surf = pygame.image.load('art_assets/interface/cockpit1.png').convert_alpha()
        dashboard_rect = dashboard_surf.get_rect(midbottom = (960,810))
        planet_surf = pygame.image.load('art_assets/interface/planet1.png').convert_alpha()
        planet_rect = planet_surf.get_rect(center = (screen_width/2,screen_height/2))
        clickablemap_surf = pygame.image.load('art_assets/interface/clickscreen.png').convert_alpha()
        clickablemap_rect = clickablemap_surf.get_rect(topleft = (0,0))
        mission_icon_1_surf = pygame.image.load('art_assets/interface/bionic_eye_lowres_green.png').convert_alpha()
        mission_icon_1_rect = mission_icon_1_surf.get_rect(topleft = (960,540))
        nighthawk_pilot_surf = pygame.image.load('art_assets/pilots/nighthawk_standing_default_75.png').convert_alpha()
        nighthawk_pilot_rect = nighthawk_pilot_surf.get_rect(topleft = (1350,300))
        intrepid_rose_pilot_surf = pygame.image.load('art_assets/pilots/intrepid_rose_standing_default_75.png').convert_alpha()
        intrepid_rose_pilot_rect = intrepid_rose_pilot_surf.get_rect(topleft = (1350,300))
        lightbringer_pilot_surf = pygame.image.load('art_assets/pilots/lightbringer_standing_default_75.png').convert_alpha()
        lightbringer_pilot_rect = lightbringer_pilot_surf.get_rect(topleft = (1350,300))
        jet_surf = pygame.image.load('art_assets/pilots/red_dot_icon.png').convert_alpha()
        jet_surf = pygame.transform.scale(jet_surf, (10,10))
        jet_rect = jet_surf.get_rect(center = (jet_pos_x, jet_pos_y))
        pilot1_surf = pygame.image.load('art_assets/pilots/red_dot_icon.png').convert_alpha()
        pilot1_surf = pygame.transform.scale(jet_surf, (10,10))
        pilot1_rect = jet_surf.get_rect(center = (800, 800))
        jet2_surf = pygame.image.load('art_assets/pilots/blue_dot_icon.png').convert_alpha()
        jet2_surf = pygame.transform.scale(jet2_surf, (10,10))
        jet2_rect = jet2_surf.get_rect(center = (jet2_pos_x, jet2_pos_y))
        radio_surf = pygame.image.load('art_assets/interface/radio.png').convert_alpha()
        radio_surf = pygame.transform.scale(radio_surf, (40,40))
        radio_rect = radio_surf.get_rect(center = (radio_pos_x, radio_pos_y))
        pilot_list_name_nighthawk_surf = pygame.image.load('art_assets/interface/pilot_list_name_nighthawk_75.png').convert_alpha()
        pilot_list_name_intrepid_rose_surf = pygame.image.load('art_assets/interface/pilot_list_name_intrepid_rose_75.png').convert_alpha()
        pilot_list_name_lightbringer_surf = pygame.image.load('art_assets/interface/pilot_list_name_lightbringer_75.png').convert_alpha()
        pilot_list_name_nighthawk_assigned_surf = pygame.image.load('art_assets/interface/pilot_list_name_nighthawk_assigned.png').convert_alpha()
        pilot_list_name_nighthawk_rect = pilot_list_name_nighthawk_surf.get_rect(topleft = (1300,325))
        pilot_list_name_intrepid_rose_rect = pilot_list_name_intrepid_rose_surf.get_rect(topleft = (1300,400))
        pilot_list_name_lightbringer_rect = pilot_list_name_lightbringer_surf.get_rect(topleft = (1300,475))
        text_continue_button_surf = pygame.image.load('art_assets/interface/text_continue_75.png').convert_alpha()
        text_continue_button_rect = text_continue_button_surf.get_rect(topleft = (300,200))

    if startup == True: #load Air Battle
        dogfight_screen = False
        target = unassigned_flyer

    if startup == True: #load mission 1
        mission_screen_text_1_surf = pygame.image.load('art_assets/Story/mission_text_1.png').convert_alpha()
        mission_screen_text_1_rect = mission_screen_text_1_surf.get_rect(center = (screen_width/2,screen_height/2))
        mission_screen_pilot_list_Right_surf = pygame.image.load('art_assets/interface/mission_pilot_list_Right_75.png').convert_alpha()
        mission_screen_pilot_list_Right_rect = mission_screen_pilot_list_Right_surf.get_rect(center = (screen_width/2,screen_height/2))
        mission_1_nighthawk_dialogue_1_surf = pygame.image.load('art_assets/Story/mission_1_nighthawk_dialogue.png').convert_alpha()
        mission_1_nighthawk_dialogue_1_rect = mission_1_nighthawk_dialogue_1_surf.get_rect(topleft = (300,275))
        mission_1_intrepid_rose_dialogue_1_surf = pygame.image.load('art_assets/Story/mission_1_intrepid_rose_dialogue.png').convert_alpha()
        mission_1_intrepid_rose_dialogue_1_rect = mission_1_intrepid_rose_dialogue_1_surf.get_rect(topleft = (300,275))
        mission_1_lightbringer_dialogue_1_surf = pygame.image.load('art_assets/Story/mission_1_lightbringer_dialogue.png').convert_alpha()
        mission_1_lightbringer_dialogue_1_rect = mission_1_lightbringer_dialogue_1_surf.get_rect(topleft = (300,275))
        screen.blit(planet_surf,(0,0))
    if startup == True: #End startup
        startup = False
 
#Actions

def draw_dashboard_screen():
    if game_active == True:    
        screen.blit(planet_surf,(0,0))
        screen.blit(dashboard_surf,(0,0))
        screen.blit(clickablemap_surf,(0,0))
    else: screen.fill('black')
def draw_interface_screen_back():
    if interface_screen == True:
        screen.blit(interface_screen_back_surf,(interface_screen_back_rect))
def draw_interface_screen_front():
    screen.blit(green_filter_surf,(green_filter_rect))
    screen.blit(interface_frame_surf,(interface_frame_rect))
    screen.blit(x_button_surf,(x_button_rect))
def draw_map_screen():    
    if map_active == True: #Show map + mission icons
        screen.blit(map_surf,(map_rect))
        screen.blit(mission_icon_1_surf,(mission_icon_1_rect))
def draw_mission_page():
    if mission_1_dialogue == 1:
        screen.blit(mission_1_nighthawk_dialogue_1_surf,(mission_1_nighthawk_dialogue_1_rect))
        screen.blit(nighthawk_pilot_surf,(nighthawk_pilot_rect))
    if mission_1_dialogue == 2:
        screen.blit(mission_1_intrepid_rose_dialogue_1_surf,(mission_1_intrepid_rose_dialogue_1_rect))
        screen.blit(intrepid_rose_pilot_surf,(intrepid_rose_pilot_rect))
    if mission_1_dialogue == 3:
        screen.blit(mission_1_lightbringer_dialogue_1_surf,(mission_1_lightbringer_dialogue_1_rect))
        screen.blit(lightbringer_pilot_surf,(lightbringer_pilot_rect))
    screen.blit(text_continue_button_surf,(text_continue_button_rect))
def draw_pilot_select():
    if pilot_select == True:
        screen.blit(mission_screen_pilot_list_Right_surf,(mission_screen_pilot_list_Right_rect))
        screen.blit(pilot_list_name_nighthawk_surf,(pilot_list_name_nighthawk_rect))
        screen.blit(pilot_list_name_intrepid_rose_surf,(pilot_list_name_intrepid_rose_rect))
        screen.blit(pilot_list_name_lightbringer_surf,(pilot_list_name_lightbringer_rect))
def draw_dogfight_screen():
    if dogfight_screen == True: #Aerial combat
        screen.blit(map_surf,(map_rect))
        screen.blit(radio_surf,(radio_rect))
        screen.blit(jet_surf,(jet_rect))
        screen.blit(jet2_surf,(jet2_rect))
def save_game():
    savegame = open("mission_control/savegame.txt", "w")
    savegame.write(str(rose.name) + " piloting: battlesuit " + str(rose.battlesuit.name) + " " + str(Roll_to_hit_outcome))
    savegame.close()
    savegame = open("Documents/Python_Exploration/mission_control/savegame.txt", "r")
    print(savegame.read())
def roll_to_hit():
    global hit_roll
    global hit_successful
    global attacker
    hit_roll = random.randint(9,20)
    if hit_roll > difficulty:
        hit_successful = True
        print("hit")
    else: 
        hit_successful = False
        print("Miss")
def register_hit():
    global hit_successful
    global Target
    if hit_successful == True:
        if combat_pilot_1.shields_up == True:
            combat_pilot_1.shields_up = False
            hit_successful = False
        else:
            if combat_pilot_1.battlesuit_damaged == False:
                combat_pilot_1.battlesuit_damaged = True
                hit_successful = False
            else: 
                if combat_pilot_1.battlesuit_heavilly_damaged == False:
                    combat_pilot_1.battlesuit_heavilly_damaged = True
                    hit_successful = False
                else:
                    combat_pilot_1.injured = True
                    hit_successful = False
        # print("shields On: " + str(Shadowstalker_shields))
        # print("Armor Damaged: " + str(Shadowstalker_Armor_Damaged))
        # print("Armor Heavily Damaged: " + str(Shadowstalker_Armor_Heavilly_Damaged))
        # print("pilot Injured: " + str(Shadowstalker_pilot_Injured))
    if combat_pilot_1.shields_up == False:
        print("shields down!")
    if combat_pilot_1.battlesuit_damaged:
        print("Battlesuit is damaged!")
    if combat_pilot_1.battlesuit_heavilly_damaged == True:
        print("!!! pilot IN DANGER !!!")

def jet_maneuver():
    #change velocity
    if jet_target_distance_x >= 0:
        jet.momentum_x -= 0.01
        jet.momentum_x -= 0.0002*jet_target_distance_x
    else:
        jet.momentum_x += 0.01
        jet.momentum_x += 0.0002*abs(jet_target_distance_x) 
    if jet_target1_distance_y >= 0:
        jet.momentum_y -= 0.01
        jet.momentum_y -= 0.001*jet_target_distance_y
    else:
        jet.momentum_y += 0.001*abs(jet_target_distance_y)
        jet.momentum_y += 0.01
    #speed limit
    if jet.momentum_x > 10: #speed limit
                jet2_momentum_x = 10
            if jet2_momentum_y >10:
                jet2_momentum_y = 10
            if jet2_momentum_x < -10:
                jet2_momentum_x = -10
            if jet2_momentum_y < -10:
                jet2_momentum_y = -10
    if jet.momentum_x > -2 and jet.momentum_x < 2: #Speed Boost
        jet.momentum_x = jet.momentum_x*1.05
        jet.momentum_x = jet.momentum_x*1.05
    #update positions
    jet.pos_y = (jet.pos_y + jet.momentum_y*0.1)
    jet.pos_x = (jet.pos_x + jet.momentum_x*0.1)




def jet_targeting_distance():
    jet_target_distance_x = jet.pos_x - target.pos_x
    jet_target_distance_y = jet.pos_y - target.pos_y


while True: #game Cycle
    draw_interface_screen_back()
    draw_dashboard_screen()
    draw_mission_page()
    draw_map_screen()
    draw_pilot_select()
    draw_dogfight_screen()
    draw_interface_screen_front()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
        if game_active == True: #User imputs
            if event.type == pygame.KEYDOWN: #Toggle map
                if event.key == pygame.K_m:
                    if map_active == True:
                        map_active = False
                    else:
                        map_active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click dashboard map for full map
                if clickablemap_rect.collidepoint(event.pos):
                    map_active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click mission icon 1
                if mission_icon_1_rect.collidepoint(event.pos) and mission_1_active == False:
                    map_active = False
                    draw_mission_page = True
                    mission_1_dialogue = 1
                    mission_1_active = True
            if event.type == pygame.MOUSEBUTTONDOWN: #continue to pilot select
                if text_continue_button_rect.collidepoint(event.pos) and mission_1_active == True:
                    mission_1_dialogue = 0
                    pilot_select = True
                    map_active = False
            if event.type == pygame.MOUSEBUTTONDOWN: #Start dogfight
                if text_continue_button_rect.collidepoint(event.pos) and mission_1_active == True:
                    if pilot_selected == rose:
                        mission_1_dialogue = 0
                        pilot_select = False
                        map_active = False
                        draw_mission_page = False
                        dogfight_screen = True
            if pilot_select == True:
                if event.type == pygame.MOUSEBUTTONDOWN: #select a pilot
                    # if pilot_list_name_nighthawk_rect.collidepoint(event.pos) and pilot_select == True:
                    #     pilot_selected = nighthawk
                    #     pilot_select = False
                    if pilot_list_name_intrepid_rose_rect.collidepoint(event.pos) and pilot_select == True:
                        pilot_selected = rose
                        pilot_select = False
                        mission_1_dialogue = 2
                    if pilot_list_name_lightbringer_rect.collidepoint(event.pos) and pilot_select == True:
                        pilot_selected = lightbringer
                        pilot_select = False
                        mission_1_dialogue = 3
            if event.type == pygame.MOUSEBUTTONDOWN: #Close window
                if x_button_rect.collidepoint(event.pos):
                    if draw_mission_page == True:
                        draw_mission_page = False
                        mission_1_dialogue = 0
                        mission_1_active = False
                        map_active = False
                    if mission_1_dialogue == 1:
                        mission_1_dialogue = 0
                        mission_1_active = False
                        draw_mission_page = False
                        map_active = False
                    if pilot_select == True:
                        pilot_select = False
                        mission_1_active = False
                        map_active = False
                        draw_mission_page = False
                    if map_active == True:
                        map_active = False
                    if dogfight_screen == True:
                        dogfight_screen = False
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

    if dogfight_screen == True: #Aerial combat
        invuln_timer += 1
        #placeholder
        jet = nighthawk_flyer
        target = radio_flyer
        jet_maneuver()
        jet = rose_flyer
        target = nighthawk_flyer
        jet_maneuver()
        
        if dogfight_screen == True: #control velocity
            #Speed limit
            
            #jet1 movement target

            
            #jet2 movement target
            if jet2_target1_distance_x >= 0:
                jet2_momentum_x -= 0.001*abs(jet2_target1_distance_x)
                jet2_momentum_x -= 0.01
            else:
                jet2_momentum_x += 0.001*abs(jet2_target1_distance_x)
                jet2_momentum_x += 0.01
            if jet2_target2_distance_y >= 0:
                jet2_momentum_y -= 0.001*abs(jet2_radio_Distance_y)
                jet2_momentum_y -= 0.01
            else:
                jet2_momentum_y += 0.001*abs(jet2_radio_Distance_y)
                jet2_momentum_y += 0.01
            #jet2 attack target
            if abs(jet2_target1_distance_x) < 30 and abs(jet2_target1_distance_y) <30:
                pygame.draw.line(screen, (200,0,0), (jet2_pos_x,jet2_pos_y), (jet_pos_x,jet_pos_y), 5)
                print("Target Acquired")
                if invuln_timer > 200:
                    Roll_to_hit()
                    invuln_timer = 0
                if hit_successful == True:
                    register_hit()
                    print(invuln_timer)
            
        # if jet_rect.collidepoint(jet2_rect.x, jet2_rect.y): #Detect Melee Contact
        #     if invuln_timer > 200:
        #         print("Contact")
        #         Roll_to_hit()
        #         register_hit()
        #         print(invuln_timer)
        #         jet2_momentum_y = jet2_momentum_y * 2
        #         invuln_timer = 0

    if pause == True: #Show Pause screen
            screen.blit(pause_menu_surf, (0,0))
            screen.blit(quit_button_surf, (0,540))

    pygame.display.update()
    clock.tick(60)


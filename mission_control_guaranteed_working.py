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
            def __init__(self, name, refresh, mobility, shields, weapons, battlesuit_damaged, battlesuit_heavilly_damaged, target, pos_x, pos_y, momentum_x, momentum_y, surf, rect):
                    self.name = name
                    self.refresh = refresh
                    self.mobility = mobility
                    self.shields = shields
                    self.weapons = weapons
                    self.battlesuit_damaged = battlesuit_damaged
                    self.battlesuit_heavilly_damaged = battlesuit_heavilly_damaged
                    self.target = target
                    self.pos_x = pos_x
                    self.pos_y = pos_y
                    self.momentum_x = momentum_x
                    self.momentum_y = momentum_y
                    self.surf = surf
                    self.rect = rect
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

    if startup == True: #load Images
        screen_width = 1920
        screen_height = 1080
        centerpoint = ((screen_width)/2, (screen_height)/2)
        pygame.init()
        screen = pygame.display.set_mode((screen_width,screen_height))
        pygame.display.set_caption("mission_control")
        interface_screen_back_surf = pygame.image.load('graphics/interface/interface_back_75.png').convert_alpha()
        interface_screen_back_rect = interface_screen_back_surf.get_rect(center = (screen_width/2,screen_height/2))
        green_filter_surf = pygame.image.load('graphics/interface/green_filter.png').convert_alpha()
        green_filter_rect = green_filter_surf.get_rect(center = (screen_width/2,screen_height/2))
        interface_frame_surf = pygame.image.load('graphics/interface/white_frame_75.png').convert_alpha()
        interface_frame_rect = interface_frame_surf.get_rect(center = (screen_width/2,screen_height/2))    
        map_surf = pygame.image.load('graphics/interface/basic_map_75.png').convert_alpha()
        map_rect = map_surf.get_rect(center = (screen_width/2,screen_height/2))
        pause_menu_surf = pygame.image.load('graphics/interface/pause_menu.png').convert()
        pause_menu_rect = pause_menu_surf.get_rect(topleft = (0,0))
        quit_button_surf = pygame.image.load('graphics/interface/quit_button.png').convert()
        quit_button_rect = quit_button_surf.get_rect(topleft = (0,540))
        x_button_surf = pygame.image.load('graphics/interface/x_button_75.png').convert_alpha()
        x_button_rect = x_button_surf.get_rect(topleft = (300,150))
        dashboard_surf = pygame.image.load('graphics/interface/cockpit1.png').convert_alpha()
        dashboard_rect = dashboard_surf.get_rect(midbottom = (960,810))
        planet_surf = pygame.image.load('graphics/interface/planet1.png').convert_alpha()
        planet_rect = planet_surf.get_rect(center = (screen_width/2,screen_height/2))
        clickablemap_surf = pygame.image.load('graphics/interface/clickscreen.png').convert_alpha()
        clickablemap_rect = clickablemap_surf.get_rect(topleft = (0,0))
        mission_icon_1_surf = pygame.image.load('graphics/interface/bionic_eye_lowres_green.png').convert_alpha()
        mission_icon_1_rect = mission_icon_1_surf.get_rect(topleft = (960,540))
        nighthawk_pilot_surf = pygame.image.load('graphics/pilots/nighthawk_standing_default_75.png').convert_alpha()
        nighthawk_pilot_rect = nighthawk_pilot_surf.get_rect(topleft = (1350,300))
        intrepid_rose_pilot_surf = pygame.image.load('graphics/pilots/intrepid_rose_standing_default_75.png').convert_alpha()
        intrepid_rose_pilot_rect = intrepid_rose_pilot_surf.get_rect(topleft = (1350,300))
        lightbringer_pilot_surf = pygame.image.load('graphics/pilots/lightbringer_standing_default_75.png').convert_alpha()
        lightbringer_pilot_rect = lightbringer_pilot_surf.get_rect(topleft = (1350,300))
        jet_red_surf = pygame.image.load('graphics/pilots/red_dot_icon.png').convert_alpha()
        jet_red_surf = pygame.transform.scale(jet_red_surf, (10,10))
        jet_red_rect = jet_red_surf.get_rect(center = (0,0))
        jet_blue_surf = pygame.image.load('graphics/pilots/blue_dot_icon.png').convert_alpha()
        jet_blue_surf = pygame.transform.scale(jet_blue_surf, (10,10))
        jet_blue_rect = jet_blue_surf.get_rect(center = (900,900))
        radio_surf = pygame.image.load('graphics/interface/radio.png').convert_alpha()
        radio_surf = pygame.transform.scale(radio_surf, (40,40))
        radio_rect = radio_surf.get_rect(center = (800,500))
        pilot_list_name_nighthawk_surf = pygame.image.load('graphics/interface/pilot_list_name_nighthawk_75.png').convert_alpha()
        pilot_list_name_intrepid_rose_surf = pygame.image.load('graphics/interface/pilot_list_name_intrepid_rose_75.png').convert_alpha()
        pilot_list_name_lightbringer_surf = pygame.image.load('graphics/interface/pilot_list_name_lightbringer_75.png').convert_alpha()
        pilot_list_name_nighthawk_assigned_surf = pygame.image.load('graphics/interface/pilot_list_name_nighthawk_assigned.png').convert_alpha()
        pilot_list_name_nighthawk_rect = pilot_list_name_nighthawk_surf.get_rect(topleft = (1300,325))
        pilot_list_name_intrepid_rose_rect = pilot_list_name_intrepid_rose_surf.get_rect(topleft = (1300,400))
        pilot_list_name_lightbringer_rect = pilot_list_name_lightbringer_surf.get_rect(topleft = (1300,475))
        text_continue_button_surf = pygame.image.load('graphics/interface/text_continue_75.png').convert_alpha()
        text_continue_button_rect = text_continue_button_surf.get_rect(topleft = (300,200))
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
        Majestic = battlesuit("Majestic", 3, "Quick", [majestic_shield1, majestic_shield2], majestic_beam_cannon, False, False, "unassigned.battlesuit", 300, 300, 0, 0, copy.copy(jet_red_surf), copy.copy(jet_red_rect))
        Leviathan = battlesuit("Leviathan", 4, "Slow", light_shield, beam_cannon, False, False, "unassigned.battlesuit", 300, 300, 0, 0, copy.copy(jet_red_surf), copy.copy(jet_red_rect))
        Tower = battlesuit("Tower", 4, "none", light_shield, beam_cannon, False, False, "unassigned.battlesuit", 800, 800, 0, 0, copy.copy(radio_surf), copy.copy(radio_rect))
    if startup == True: #load pilots
        rose = pilot("Intrepid Rose", copy.copy(Majestic), False, True, "Void")
        nighthawk = pilot("Nighthawk", copy.copy(Majestic), False, True, "Void")
        scorpion = pilot("Scorpion", copy.copy(Majestic), False, True, "Void")
        azure = pilot("Azure Kite", copy.copy(Majestic), False, True, "Void")
        lightbringer = pilot("Lightbringer", copy.copy(Majestic), False, True, "Void")
        unassigned = pilot("unassigned", copy.copy(Majestic), False, True, "Void")
        radio_tower = pilot("unassigned", Tower, False, True, "Void")
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
        clock = pygame.time.Clock()
        test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
        game_active = True
        map_active = False
        pause = False
        mission_1_active = False
        pilot_select = False
        mission_1_dialogue = 0
        mission_page = False
        global target
        target = radio_tower.battlesuit
        global hit_successful
        hit_successful = False
        global hit_roll
        hit_roll = 0
        global difficulty
        difficulty = 10
        interface_screen = False
        invuln_timer = 0
        continue_button = False
        d6 = random.randint(0,6)
        #Skills = [perception, mobility, armor, weapons, science, social, engineering]   
    if startup == True: #load Air Battle
        dogfight_screen = False
        target = radio_tower.battlesuit
        nighthawk.battlesuit.pos_y = random.randint(0,500)
        lightbringer.battlesuit.pos_y = random.randint(0,500)
        azure.battlesuit.pos_y = random.randint(0,500)
        rose.battlesuit.surf = copy.copy(jet_blue_surf)
        target_hostile = True

    if startup == True: #load mission 1
        mission_screen_text_1_surf = pygame.image.load('graphics/Story/mission_text_1.png').convert_alpha()
        mission_screen_text_1_rect = mission_screen_text_1_surf.get_rect(center = (screen_width/2,screen_height/2))
        mission_screen_pilot_list_Right_surf = pygame.image.load('graphics/interface/mission_pilot_list_Right_75.png').convert_alpha()
        mission_screen_pilot_list_Right_rect = mission_screen_pilot_list_Right_surf.get_rect(center = (screen_width/2,screen_height/2))
        mission_1_nighthawk_dialogue_1_surf = pygame.image.load('graphics/Story/mission_1_nighthawk_dialogue.png').convert_alpha()
        mission_1_nighthawk_dialogue_1_rect = mission_1_nighthawk_dialogue_1_surf.get_rect(topleft = (300,275))
        mission_1_intrepid_rose_dialogue_1_surf = pygame.image.load('graphics/Story/mission_1_intrepid_rose_dialogue.png').convert_alpha()
        mission_1_intrepid_rose_dialogue_1_rect = mission_1_intrepid_rose_dialogue_1_surf.get_rect(topleft = (300,275))
        mission_1_lightbringer_dialogue_1_surf = pygame.image.load('graphics/Story/mission_1_lightbringer_dialogue.png').convert_alpha()
        mission_1_lightbringer_dialogue_1_rect = mission_1_lightbringer_dialogue_1_surf.get_rect(topleft = (300,275))
        jet = unassigned.battlesuit
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
    if interface_screen == True:
        screen.blit(green_filter_surf,(green_filter_rect))
        screen.blit(interface_frame_surf,(interface_frame_rect))
        screen.blit(x_button_surf,(x_button_rect))
    if continue_button == True:
        screen.blit(text_continue_button_surf,(text_continue_button_rect))
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
        # screen.blit(jet_red_surf,(jet_red_rect))
def draw_jet():
    global jet
    if dogfight_screen == True:
        screen.blit(jet.surf,(jet.rect))

def draw_pause_screen():
    if pause == True: #Show Pause screen
            screen.blit(pause_menu_surf, (0,0))
            screen.blit(quit_button_surf, (0,540))

def save_game():
    savegame = open("mission_control/savegame.txt", "w")
    savegame.write(str(rose.name) + " piloting: battlesuit " + str(rose.battlesuit.name) + " " + str(roll_to_hit_outcome))
    savegame.close()
    savegame = open("Documents/Python_Exploration/mission_control/savegame.txt", "r")
    print(savegame.read())
def roll_to_hit():
    global hit_roll
    global hit_successful
    global attacker
    hit_roll = random.randint(1,20)
    if hit_roll > difficulty:
        hit_successful = True
        print("hit")
    else: 
        hit_successful = False
        print("Miss")
def register_hit():
    global hit_successful
    global target
    print(target.name)
    if hit_successful == True:
        if target.shields == True:
            target.shields = False
            hit_successful = False
        else:
            if target.battlesuit_damaged == False:
                target.battlesuit_damaged = True
                hit_successful = False
            else: 
                if target.battlesuit_heavilly_damaged == False:
                    target.battlesuit_heavilly_damaged = True
                    hit_successful = False
                else:
                    target.injured = True
                    hit_successful = False
def jet_targeting_distance():
    global jet_target_distance_x
    global jet_target_distance_y
    global jet
    global target
    jet_target_distance_x = jet.pos_x - target.pos_x
    jet_target_distance_y = jet.pos_y - target.pos_y
def jet_maneuver():
    #change velocity
    global jet_target_distance_x
    global jet_target_distance_y
    global jet
    global jet_red_rect
    global jet_red_surf
    global jet_blue_surf
    global jet_blue_rect
    if jet.battlesuit_damaged == True:
        jet.momentum_x += 0.01*jet_target_distance_x
    if jet_target_distance_x >= 0:
        jet.momentum_x -= 0.01
        jet.momentum_x -= 0.002*jet_target_distance_x
    else:
        jet.momentum_x += 0.01
        jet.momentum_x += 0.002*abs(jet_target_distance_x) 
    if jet_target_distance_y >= 0:
        jet.momentum_y -= 0.001
        jet.momentum_y -= 0.01*jet_target_distance_y
    else:
        jet.momentum_y += 0.002*abs(jet_target_distance_y)
        jet.momentum_y += 0.01
    #speed limit
    if abs(jet.momentum_x) > 10: #speed limit
        jet.momentum_x *= 0.9
    if abs(jet.momentum_y) >10:
        jet.momentum_y *= 0.9
    if abs(jet.momentum_x) < 2 and abs(jet.momentum_y) < 2: #Speed Boost
        jet.momentum_x *= 1.1
        jet.momentum_y *= 1.1
    #update positions
    jet.pos_y = (jet.pos_y + jet.momentum_y*0.1)
    jet.pos_x = (jet.pos_x + jet.momentum_x*0.1)
    jet.rect = jet.surf.get_rect(center = (int(jet.pos_x), int(jet.pos_y)))
def jet_attack():
    global jet
    global target
    global invuln_timer
    global hit_successful
    if target_hostile == True:
        if abs(jet_target_distance_x) < 30 and abs(jet_target_distance_y) <30:
            pygame.draw.line(screen, (200,0,0), (jet.pos_x,jet.pos_y), (target.pos_x,target.pos_y), 5)
            if invuln_timer > 200:
                roll_to_hit()
                invuln_timer = 0
            if hit_successful == True:
                register_hit()

def jet_sequence():
    jet_targeting_distance()
    jet_maneuver()
    # jet_maneuver()
    jet_attack()
    draw_jet()

dogfight_screen = True
interface_screen = True
while True: #game Cycle
    draw_dashboard_screen()
    draw_interface_screen_back()
    draw_mission_page()
    draw_map_screen()
    draw_pilot_select()
    draw_dogfight_screen()
    draw_jet()
    draw_interface_screen_front()
    draw_pause_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
        if game_active == True: #User imputs
            if event.type == pygame.KEYDOWN: #Toggle map
                if event.key == pygame.K_m:
                    if map_active == True:
                        map_active = False
                        interface_screen = False
                    else:
                        map_active = True
                        interface_screen = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click dashboard map for full map
                if clickablemap_rect.collidepoint(event.pos):
                    if interface_screen == False:
                        map_active = True
                        interface_screen = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Click mission icon 1
                if mission_icon_1_rect.collidepoint(event.pos) and mission_1_active == False:
                    map_active = False
                    interface_screen = True
                    mission_page = True
                    mission_1_dialogue = 1
                    mission_1_active = True
                    continue_button = True
            if event.type == pygame.MOUSEBUTTONDOWN: #continue to pilot select
                if text_continue_button_rect.collidepoint(event.pos) and mission_1_active == True:
                    mission_1_dialogue = 0
                    pilot_select = True
                    interface_screen = True
                    map_active = False
                    continue_button = True
            if event.type == pygame.MOUSEBUTTONDOWN: #Start dogfight
                if text_continue_button_rect.collidepoint(event.pos) and mission_1_active == True:
                    if pilot_selected == rose:
                        mission_1_dialogue = 0
                        pilot_select = False
                        map_active = False
                        mission_page = False
                        dogfight_screen = True
                        interface_screen = True
                        continue_button = False
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
                    interface_screen = False
                    continue_button = False
                    mission_page = False
                    if mission_page == True:
                        mission_1_dialogue = 0
                        mission_1_active = False
                        map_active = False
                    if mission_1_dialogue == 1:
                        mission_1_dialogue = 0
                        mission_1_active = False
                        map_active = False
                    if pilot_select == True:
                        pilot_select = False
                        mission_1_active = False
                        map_active = False
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
        jet = rose.battlesuit
        target = radio_tower.battlesuit
        jet_sequence()
        jet = nighthawk.battlesuit
        if rose.battlesuit.battlesuit_damaged == False:
            target = rose.battlesuit
            target_hostile = True
        else: 
            target = radio_tower.battlesuit
            target_hostile = False
        jet_sequence()
        jet = lightbringer.battlesuit
        target = rose.battlesuit
        jet_sequence()
        jet = azure.battlesuit
        target = rose.battlesuit
        jet_sequence()



        # if jet_red_rect.collidepoint(jet_red_rect.x, jet_red_rect.y): #Detect Melee Contact
        #     if invuln_timer > 200:
        #         print("Contact")
        #         roll_to_hit()
        #         register_hit()
        #         print(invuln_timer)
        #         jet_momentum_y = jet_momentum_y * 2
        #         invuln_timer = 0



    pygame.display.update()
    clock.tick(60)


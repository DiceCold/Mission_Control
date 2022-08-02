import pygame
import os

game_active = True
interface_screen = False
mission_1_dialogue = False
pilot_select = False
dogfight_screen = False
continue_button = False
pause = False


#load visuals
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
map_surf = pygame.image.load('graphics/maps/basic_map_75.png').convert_alpha()
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
radio_surf = pygame.image.load('graphics/interface/shield_blank.png').convert_alpha()
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

def draw_dashboard_screen():
    if game_active == True:    
        screen.blit(planet_surf,(0,0))
        screen.blit(dashboard_surf,(0,0))
        screen.blit(clickablemap_surf,(0,0))
    else: screen.fill('black')
def draw_interface_screen_back():
    screen.blit(interface_screen_back_surf,(interface_screen_back_rect))
def draw_interface_screen_front():
        screen.blit(green_filter_surf,(green_filter_rect))
        screen.blit(interface_frame_surf,(interface_frame_rect))
        screen.blit(x_button_surf,(x_button_rect))
        if continue_button == True:
            screen.blit(text_continue_button_surf,(text_continue_button_rect))
def draw_map_screen():    
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
def draw_jet():
    global jet
    if dogfight_screen == True:
        screen.blit(jet.image,(jet.rect))
        
def draw_pause_screen():
    if pause == True: #Show Pause screen
            screen.blit(pause_menu_surf, (0,0))
            screen.blit(quit_button_surf, (0,540))
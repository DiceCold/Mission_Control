#clean version to test from
import pygame
import random
from sys import exit
import os
import copy

none = "none"
window_display = "none"
selected_pilot_row= -1
selected_loadout_row = 0
selected_loadout_column = 0

startup = True

if startup == True: #load screen
    screen_width = 1280
    screen_height = 720
    centerpoint = ((screen_width)/2, (screen_height)/2)
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("mission_control")
    text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
    clock = pygame.time.Clock()

if startup == True: #load images
    interface_back_surf = pygame.image.load('graphics/interface/interface_back.png').convert_alpha()
    interface_back_surf = pygame.transform.scale(interface_back_surf, (screen_width*0.8,screen_height*0.8))
    interface_back_rect = interface_back_surf.get_rect(center = (screen_width/2,screen_height/2))
    green_filter_surf = pygame.image.load('graphics/interface/green_filter.png').convert_alpha()
    green_filter_surf = pygame.transform.scale(green_filter_surf, (screen_width*0.8,screen_height*0.8))
    green_filter_rect = green_filter_surf.get_rect(center = (screen_width/2,screen_height/2))
    interface_frame_surf = pygame.image.load('graphics/interface/white_frame_large.png').convert_alpha()
    interface_frame_surf = pygame.transform.scale(interface_frame_surf, (screen_width*0.8,screen_height*0.8))
    interface_frame_rect = interface_frame_surf.get_rect(center = (screen_width/2,screen_height/2))    
    map_surf = pygame.image.load('graphics/interface/shield_blank.png').convert_alpha()
    map_rect = map_surf.get_rect(center = (screen_width/2,screen_height/2))
    pause_menu_surf = pygame.image.load('graphics/interface/pause_menu.png').convert()
    pause_menu_rect = pause_menu_surf.get_rect(topleft = (0,0))
    quit_button_surf = pygame.image.load('graphics/interface/quit_button.png').convert()
    quit_button_rect = quit_button_surf.get_rect(topleft = (0,540))
    x_button_surf = pygame.image.load('graphics/interface/x_button_75.png').convert_alpha()
    x_button_rect = x_button_surf.get_rect(topleft = (screen_width*0.15,screen_height*0.15))
    small_frame_1_surf = pygame.image.load('graphics/interface/small_frame.png').convert_alpha()
    small_frame_1_surf = pygame.transform.scale(small_frame_1_surf, (screen_width*0.25,screen_height*0.8))
    small_frame_2_surf = pygame.image.load('graphics/interface/small_frame_flipped.png').convert_alpha()
    small_frame_2_surf = pygame.transform.scale(small_frame_2_surf, (screen_width*0.25,screen_height*0.8))
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
    blueprint_surf = pygame.image.load('graphics/interface/blueprint_labeled.png').convert_alpha()
    blueprint_surf = pygame.transform.scale(blueprint_surf, (screen_width*0.3,screen_height*0.3))
    blueprint_rect = blueprint_surf.get_rect(center = (screen_width/2,screen_height/2))
   
class Power_Core:
    def __init__(self, type):
        if type == "fusion_core":
            self.name = "Fusion Core"
        if type == "null_core":
            self.name = " "
            
fusion_core = Power_Core("fusion_core")
null_core = Power_Core("null_core")
   
class Weapon:
    def __init__(self, type):
        if type == "unassigned_weapon":
            self.name = "Unassigned"
        if type == "beam_cannon":
            self.name = "Beam Cannon"
            self.accuracy = 1
            self.distance = "mid"
            self.cooldown = 200
            self.damage_type = "thermal"
            self.apply_status = "overheated"
        if type == "cryo_shot":
            self.name = "Cryo Shot"
            self.accuracy = 1
            self.distance = "close"
            self.cooldown = 200
            self.damage_type = "cold"
            self.apply_status = "frozen"
        if type == "powersword":
            self.name = "Powersword"
            self.accuracy = 1
            self.distance = "melee"
            self.cooldown = 200
            self.damage_type = "pierce"
            self.apply_status = "knockback"
        if type == "flame_lance":
            self.name = "Flame Lance"
            self.accuracy = 1
            self.distance = "melee"
            self.cooldown = 200
            self.damage = "thermal"
            self.apply_status = "knockback" + "overheated"
        if type == "lightning_chain":
            self.name = "Lightning Chain"
            self.accuracy = 1
            self.distance = "melee"
            self.cooldown = 200
            self.damage = "shock"
            self.apply_status = "disrupted" + "tethered"
        if type == "null_weapon":
            self.name = " "
            
beam_cannon = Weapon("beam_cannon")
unassigned_weapon = Weapon("unassigned_weapon")
null_weapon = Weapon("null_weapon")

class Shield:
    def __init__(self, type):
        if type == "light_shield":
            self.name = "Light Shield"
            self.cooldown = 200
            self.charged = True
            
light_shield = Shield("light_shield")

class Battlesuit(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.item_1 = beam_cannon
        self.item_2 = unassigned_weapon
        self.item_3 = light_shield
        self.item_4 = unassigned_weapon
        if type == "majestic":
            self.name = "Majestic"
            self.mobility = 1
            self.refresh = 4
            self.size = 1
            self.loadout = [fusion_core,beam_cannon,unassigned_weapon,light_shield,unassigned_weapon]
        if type == "leviathan":
            self.name = "Leviathan"
            self.mobility = 0.5
            self.refresh = 4
            self.power_core = "dirty_fission_core"
            self.size = 2
        if type == "tower":
            self.name = "Tower"
            self.mobility = 0
        if type == "javelin":
            self.name = "Javelin"
            self.mobility = 2
            self.refresh = 3
            self.power_core = fusion_core
            self.size = 0.5
        if type == "drone":
            self.name = "Drone"
            self.mobility = 2
            self.refresh = 1
            self.power_core = fusion_core
            self.size = 0.3
        if type == "null_suit":
            self.name = " "
            self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
        self.damaged = False
        self.severely_damaged = False
        
        
    def update(self):
        self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        self.invuln_timer -= 1
        if self.invuln_timer > 0:
            self.invuln_timer = 0

majestic = Battlesuit("majestic")
leviathan = Battlesuit("leviathan")
tower = Battlesuit("tower")
javelin = Battlesuit("javelin")
drone = Battlesuit("drone")
null_suit = Battlesuit("null_suit")


class Pilot:
    def __init__(self, name, battlesuit):
            self.name = name
            self.battlesuit = copy.copy(battlesuit)
            self.injured = False
            self.alive = True

unassigned_pilot = Pilot("Unassigned",tower)
nighthawk = Pilot("Nighthawk",majestic)
rose = Pilot("Intrepid_Rose",majestic)
lightbringer = Pilot("Lightbringer",majestic)
deadlift = Pilot("Deadlift",majestic)
kite = Pilot("Azure_Kite",majestic)
null_pilot = Pilot(" ",null_suit)
pilot_list = [unassigned_pilot, nighthawk, rose, lightbringer, deadlift, kite]
inventory_list = [beam_cannon]
selected_pilot = null_pilot

enemy_drone = Pilot("Enemy_Drone",drone)

class Loadout_Names(pygame.sprite.Sprite):
    def __init__(self, loadout_number, column_number, row_number):
        super().__init__()
        self.column_number = column_number
        self.row_number = row_number
        self.loadout_number = loadout_number
        text_surf = text_font_small.render(f"{selected_pilot.battlesuit.loadout[self.loadout_number].name}",False,(0,0,0))
        self.image = text_surf
        self.rect = self.image.get_rect(topleft = (screen_width*0.05 + column_number*100, screen_height*0.215 + row_number*40))     
        self.selected = False
    def update(self):
        self.image = text_font_small.render(f"{selected_pilot.battlesuit.loadout[self.loadout_number].name}",False,(0,0,0))

class Pilot_Names(pygame.sprite.Sprite):
    def __init__(self, name, column_number, row_number):
        super().__init__()
        self.name = name
        name_surf = text_font_small.render(f'{self.name}',False,(111,196,169))
        self.frames = [name_surf]
        self.animation_index = 0
        self.row_number = row_number
        self.image = self.frames[self.animation_index]
        self.name = name
        self.rect = self.image.get_rect(topleft = (screen_width*0.05 + column_number*100, screen_height*0.215 + row_number*40))  
        self.rect = pygame.Rect(screen_width*0.05 + column_number*100, screen_height*0.215 + self.row_number*40,300,40) 
 
        # self.selected = False
        # self.cooldown = 10
    def update(self):
        # global selected_pilot
        # self.click_button()
        self.image = text_font_small.render(f'{self.name}',False,(111,196,169))
        # if self.cooldown > 0:
            # self.cooldown -= 1
        # if self.selected == True:
            # selected_pilot = self.name
    # def click_button(self):
        # global selected_pilot
        # if event.type == pygame.MOUSEBUTTONDOWN: #Click
           # if self.cooldown == 0:
                # if self.rect.collidepoint(event.pos): #Toggle select
                    # self.cooldown = 10
                    # if self.selected == False:
                        # self.selected = True
                    # else:
                        # self.selected = False
                # else: self.selected = False

class Nameplates(pygame.sprite.Sprite):
    def __init__(self,type,column_number,row_number,name):
        super().__init__()
        if type == "standard":
            nameplate_1 = pygame.image.load('graphics/interface/interface_panel_name.png').convert_alpha()
            nameplate_1 = pygame.transform.scale(nameplate_1, (300,40))
            nameplate_2 = pygame.image.load('graphics/interface/interface_panel_name_green.png').convert_alpha()
            nameplate_2 = pygame.transform.scale(nameplate_2, (300,40))
            self.height = 40
        if type == "card":
            nameplate_1 = pygame.image.load('graphics/interface/interface_panel_name.png').convert_alpha()
            nameplate_1 = pygame.transform.scale(nameplate_1, (400,100))
            nameplate_2 = pygame.image.load('graphics/interface/interface_panel_name_green.png').convert_alpha()
            nameplate_2 = pygame.transform.scale(nameplate_2, (400,100))
            self.height = 100
        if type == "inventory_line_item":
            nameplate_1 = pygame.image.load('graphics/interface/interface_panel_name.png').convert_alpha()
            nameplate_1 = pygame.transform.scale(nameplate_1, (300,40))
            nameplate_2 = pygame.image.load('graphics/interface/interface_panel_name_green.png').convert_alpha()
            nameplate_2 = pygame.transform.scale(nameplate_2, (300,40))
            self.height = 40
        if type == "pilot_line_item":
            nameplate_1 = pygame.image.load('graphics/interface/interface_panel_name.png').convert_alpha()
            nameplate_1 = pygame.transform.scale(nameplate_1, (300,40))
            nameplate_2 = pygame.image.load('graphics/interface/interface_panel_name_green.png').convert_alpha()
            nameplate_2 = pygame.transform.scale(nameplate_2, (300,40))
            self.height = 40
        if type == "loadout_label":
            nameplate_1 = pygame.image.load('graphics/interface/label_white_lowres.png')
            nameplate_1 = pygame.transform.scale(nameplate_1, (150,30))
            nameplate_2 = pygame.image.load('graphics/interface/label_grey_lowres.png')
            nameplate_2 = pygame.transform.scale(nameplate_2, (150,30))
            self.height = 40
        
        self.frames = [nameplate_1,nameplate_2]
        self.animation_index = 0
        self.row_number = row_number
        self.column_number = column_number
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(topleft = (screen_width*0.1 +self.column_number*100, screen_height*0.25 + self.row_number*self.height))
        self.selected = False
        self.cooldown = 0
        self.name = name
        self.type = type
    def destroy(self):
        self.kill()
    def update(self):
        self.click_button()
        if self.type == "pilot_line_item":
            if self.row_number == selected_pilot_row:
                self.selected = True
            else:
                self.selected = False
        if self.type == "loadout_label":
            if self.row_number == selected_loadout_row and self.column_number == selected_loadout_column:
                self.selected = True
            else: self.selected = False
        if self.selected == True:
            self.animation_index = 1
        else: self.animation_index = 0
        self.image = self.frames[self.animation_index]
        if self.cooldown > 0:
            self.cooldown -= 1
    def click_button(self):
        global selected_pilot_row
        global selected_pilot
        global selected_inventory_column
        global selected_inventory_row
        global selected_loadout_column
        global selected_loadout_row
        if event.type == pygame.MOUSEBUTTONDOWN: #Click
           if self.cooldown == 0:
                if self.rect.collidepoint(event.pos): #Toggle select
                    self.cooldown = 10
                    if self.type == "pilot_line_item":
                        if selected_pilot_row == self.row_number:
                            selected_pilot = null_pilot
                            selected_pilot_row = -1
                        else:
                            selected_pilot_row = self.row_number
                            selected_pilot = self.name
                    if self.type == "loadout_label":
                        if self.column_number == selected_loadout_column and self.row_number == selected_loadout_row:
                            selected_loadout_column = 0
                            selected_loadout_row = 0
                        else:
                            selected_loadout_column = self.column_number
                            selected_loadout_row = self.row_number
                        

if startup == True: #create sprite groups       
    nameplates_group = pygame.sprite.Group()
    pilot_names_group = pygame.sprite.Group()
    inventory_names_group = pygame.sprite.Group()
    loadout_names_group = pygame.sprite.Group()

def create_nameplate(type, column_number, row_number,name):
    nameplates_group.add(Nameplates(type,column_number,row_number,name))


create_nameplate("pilot_line_item",0,0,pilot_list[1])
create_nameplate("pilot_line_item",0,1,pilot_list[2])
create_nameplate("pilot_line_item",0,2,pilot_list[3])
create_nameplate("pilot_line_item",0,3,pilot_list[4])
create_nameplate("pilot_line_item",0,4,pilot_list[5])

create_nameplate("inventory_line_item",7.2,0,inventory_list[0].name)

create_nameplate("loadout_label", 3.2,2,"item_1")
create_nameplate("loadout_label", 3.2,6.3,"item_3")
create_nameplate("loadout_label", 5.6,2,"item_2")
create_nameplate("loadout_label", 5.6,4.1,"power_core")
create_nameplate("loadout_label", 5.6,6.3,"item_4")


# create_nameplate("line_item",7.2,1)
# create_nameplate("line_item",7.2,2)
# create_nameplate("line_item",7.2,3)
# create_nameplate("line_item",7.2,4)
# create_nameplate("line_item",7.2,5)
# create_nameplate("line_item",7.2,6)
# create_nameplate("line_item",7.2,7)
# create_nameplate("line_item",7.2,8)
# create_nameplate("line_item",7.2,9)
# create_nameplate("line_item",7.2,10)

selected_pilot = null_pilot

# pilot_names_group.add(Pilot_Names(pilot.name,1,1))

pilot_names_group.add(Pilot_Names(pilot_list[1].name,1,1))
pilot_names_group.add(Pilot_Names(pilot_list[2].name,1,2))
pilot_names_group.add(Pilot_Names(pilot_list[3].name,1,3))
pilot_names_group.add(Pilot_Names(pilot_list[4].name,1,4))
pilot_names_group.add(Pilot_Names(pilot_list[5].name,1,5))

loadout_names_group.add(Loadout_Names(1,4,2.8))
loadout_names_group.add(Loadout_Names(2,6.37,2.8))
loadout_names_group.add(Loadout_Names(3,4,7.1))
loadout_names_group.add(Loadout_Names(4,6.37,7.1))
loadout_names_group.add(Loadout_Names(0,6.37,4.9))


def draw_selected_pilot_name():
    selected_pilot_name_surf = text_font.render(f"{selected_pilot.name}",False,(111,196,169))
    selected_pilot_name_rect = selected_pilot_name_surf.get_rect(center = (screen_width*0.5,screen_height*0.3))
    screen.blit(selected_pilot_name_surf,(selected_pilot_name_rect))


def draw_dashboard_screen():
    if game_active == True:    
        screen.blit(planet_surf,(0,0))
        screen.blit(dashboard_surf,(0,0))
        screen.blit(clickablemap_surf,(0,0))
def draw_interface_back():
    screen.blit(interface_back_surf,(interface_back_rect))
def draw_interface_screen_front():
    screen.blit(green_filter_surf,(green_filter_rect))
    screen.blit(interface_frame_surf,(interface_frame_rect))
def draw_ui_buttons():
    if x_button == True:
        screen.blit(x_button_surf,(x_button_rect))
    if continue_button == True:
        screen.blit(text_continue_button_surf,(text_continue_button_rect))
def draw_map_screen():    
    screen.blit(map_surf,(map_rect))
    screen.blit(mission_icon_1_surf,(mission_icon_1_rect))       
def draw_pause_screen():
    screen.blit(pause_menu_surf, (0,0))
    screen.blit(quit_button_surf, (0,540))
def draw_small_frame(side):
    if side == "left":
        screen.blit(small_frame_1_surf,(screen_width*0.1,screen_height*0.17))
    if side == "right":
        screen.blit(small_frame_2_surf,(screen_width*0.66,screen_height*0.17))
def draw_blueprint():
    screen.blit(blueprint_surf,(blueprint_rect))


while True: #game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN: #Toggle map
            if event.key == pygame.K_i:
                window_display = "inventory"
                x_button = True
                continue_button = False
                
    if window_display == "inventory":
        pilot = selected_pilot
        draw_interface_back()
        draw_blueprint()
        nameplates_group.update()
        nameplates_group.draw(screen)
        pilot_names_group.update()
        pilot_names_group.draw(screen)
        loadout_names_group.update()
        loadout_names_group.draw(screen)
        draw_selected_pilot_name()
        draw_interface_screen_front()
        draw_small_frame("left")
        draw_small_frame("right")
        draw_ui_buttons()
    
    pygame.display.update()
    clock.tick(60)
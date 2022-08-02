#clean version to test from
import pygame
import random
from sys import exit
import os
import copy

none = "none"
window_display = "none"

damage_types = ["thermal","cold","piercing","concussive","magnetic","shock"]
status_effects = ["frozen","overheated","disrupted","blinded","knockback","energized","supressed","tethered"]
available_missions = [False,True,False,False,False,False]

startup = True

if startup == True: #load notes
    power_core_list = {"01":"trapped_combustion_core", "02":"dirty_fission_core", "04":"solar_array_core", "06":"cold_fusion_core", "07":"entropy_core", "08":"black_pinhole_core", "10":"wave_collapse_core", "11":"phantom_pinnacle_core", "0x":"alien_crystal_core", "00":"no_core"}
    #suit code is size class, power core type , power core capacity, product generation
    #086403 = 08.6.4.03 = size 8, fusion core, capacity 4, generation 3
    #core type determines what kind of fuel the suit needs to operate
    #can replace core with high capacity battery that does not recharge outside of base. Each unit of stored charge = 60 seconds of powercore output
    pass
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
    blank_frame = pygame.image.load('graphics/blank.png')
    interface_back_surf = pygame.image.load('graphics/interface/interface_back.png').convert_alpha()
    interface_back_surf = pygame.transform.scale(interface_back_surf, (screen_width*0.8,screen_height*0.8))
    interface_back_rect = interface_back_surf.get_rect(center = (screen_width/2,screen_height/2))
    green_filter_surf = pygame.image.load('graphics/interface/green_filter.png').convert_alpha()
    green_filter_surf = pygame.transform.scale(green_filter_surf, (screen_width*0.8,screen_height*0.8))
    green_filter_rect = green_filter_surf.get_rect(center = (screen_width/2,screen_height/2))
    interface_frame_surf = pygame.image.load('graphics/interface/frames/white_frame_large.png').convert_alpha()
    interface_frame_surf = pygame.transform.scale(interface_frame_surf, (screen_width*0.8,screen_height*0.8))
    interface_frame_rect = interface_frame_surf.get_rect(center = (screen_width/2,screen_height/2))    
    pause_menu_surf = pygame.image.load('graphics/interface/pause_menu.png').convert()
    pause_menu_rect = pause_menu_surf.get_rect(topleft = (0,0))
    quit_button_surf = pygame.image.load('graphics/interface/quit_button.png').convert()
    quit_button_rect = quit_button_surf.get_rect(topleft = (0,540))
    x_button_surf = pygame.image.load('graphics/interface/icons/x_button_75.png').convert_alpha()
    x_button_rect = x_button_surf.get_rect(topleft = (screen_width*0.15,screen_height*0.15))
    small_frame_1_surf = pygame.image.load('graphics/interface/frames/small_frame.png').convert_alpha()
    small_frame_1_surf = pygame.transform.scale(small_frame_1_surf, (screen_width*0.25,screen_height*0.8))
    small_frame_2_surf = pygame.image.load('graphics/interface/frames/small_frame_flipped.png').convert_alpha()
    small_frame_2_surf = pygame.transform.scale(small_frame_2_surf, (screen_width*0.25,screen_height*0.8))
    dashboard_surf = pygame.image.load('graphics/interface/cockpit/cockpit1.png').convert_alpha()
    dashboard_rect = dashboard_surf.get_rect(midbottom = (960,810))
    planet_surf = pygame.image.load('graphics/interface/cockpit/planet1.png').convert_alpha()
    planet_rect = planet_surf.get_rect(center = (screen_width/2,screen_height/2))
    clickablemap_surf = pygame.image.load('graphics/interface/cockpit/clickscreen.png').convert_alpha()
    clickablemap_rect = clickablemap_surf.get_rect(topleft = (0,0))
    mission_icon_1_surf = pygame.image.load('graphics/interface/icons/bionic_eye_lowres_green.png').convert_alpha()
    mission_icon_1_rect = mission_icon_1_surf.get_rect(topleft = (960,540))
    nighthawk_pilot_surf = pygame.image.load('graphics/pilots/nighthawk_standing_default_75.png').convert_alpha()
    nighthawk_pilot_rect = nighthawk_pilot_surf.get_rect(topleft = (1350,300))
    intrepid_rose_pilot_surf = pygame.image.load('graphics/pilots/intrepid_rose_standing_default_75.png').convert_alpha()
    intrepid_rose_pilot_rect = intrepid_rose_pilot_surf.get_rect(topleft = (1350,300))
    lightbringer_pilot_surf = pygame.image.load('graphics/pilots/lightbringer_standing_default_75.png').convert_alpha()
    lightbringer_pilot_rect = lightbringer_pilot_surf.get_rect(topleft = (1350,300))
    jet_red_surf = pygame.image.load('graphics/interface/icons/red_dot.png').convert_alpha()
    jet_red_surf = pygame.transform.scale(jet_red_surf, (10,10))
    jet_red_rect = jet_red_surf.get_rect(center = (0,0))
    jet_blue_surf = pygame.image.load('graphics/interface/icons/blue_dot.png').convert_alpha()
    jet_blue_surf = pygame.transform.scale(jet_blue_surf, (10,10))
    jet_blue_rect = jet_blue_surf.get_rect(center = (900,900))
    radio_surf = pygame.image.load('graphics/blank.png').convert_alpha()
    radio_surf = pygame.transform.scale(radio_surf, (40,40))
    radio_rect = radio_surf.get_rect(center = (800,500))
    text_continue_button_surf = pygame.image.load('graphics/interface/text_continue_75.png').convert_alpha()
    text_continue_button_rect = text_continue_button_surf.get_rect(topleft = (300,200))
    blueprint_surf = pygame.image.load('graphics/interface/blueprint_labeled.png').convert_alpha()
    blueprint_surf = pygame.transform.scale(blueprint_surf, (screen_width*0.3,screen_height*0.3))
    blueprint_rect = blueprint_surf.get_rect(center = (screen_width/2,screen_height/2))  
class Power_Core:
    def __init__(self, type):
        if type == "fusion_core":
            self.name = "Fusion Core"
            self.legal = True
        if type == "null_core":
            self.name = " "
        if type == "combustion_core":
            self.name = "Combustion Core"
            self.legal = True
        if type == "dirty_core":
            self.name = "Dirty Core"
            self.legal = False
        if type == "solar_array":
            self.name = "Solar Array"
            self.legal = True
if startup == True: #load cores  
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
if startup == True: #load weapons  
    beam_cannon = Weapon("beam_cannon")
    unassigned_weapon = Weapon("unassigned_weapon")
    null_weapon = Weapon("null_weapon")
    cryo_shot = Weapon("cryo_shot")
    power_sword = Weapon("powersword")
    flame_lance = Weapon("flame_lance")
    lightning_chain = Weapon("lightning_chain")
class Shield:
    def __init__(self, type):
        if type == "light_shield":
            self.name = "Light Shield"
            self.cooldown = 200
            self.charged = True            
if startup == True: #load shields
    light_shield = Shield("light_shield")
class Battlesuit(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
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
            self.loadout = [fusion_core, beam_cannon, unassigned_weapon, unassigned_weapon, unassigned_weapon]
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
if startup == True: #load battlesuits
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
            self.rank = 1
if startup == True: #load pilots
    unassigned_pilot = Pilot("Unassigned",copy.deepcopy(tower))
    nighthawk = Pilot("Nighthawk",copy.deepcopy(majestic))
    rose = Pilot("Intrepid_Rose",copy.deepcopy(majestic))
    lightbringer = Pilot("Lightbringer",copy.deepcopy(majestic))
    deadlift = Pilot("Deadlift",copy.deepcopy(majestic))
    kite = Pilot("Azure_Kite",copy.deepcopy(majestic))
    null_pilot = Pilot(" ",copy.deepcopy(null_suit))
    pilot_list = [unassigned_pilot, nighthawk, rose, lightbringer, deadlift, kite]
    enemy_drone = Pilot("Enemy_Drone",copy.deepcopy(drone))
    rose.battlesuit.loadout[1] = flame_lance
    nighthawk.battlesuit.loadout[1] = cryo_shot
if startup == True: #load inventory_list
    inventory_list = [fusion_core, beam_cannon, light_shield, light_shield, null_weapon, null_weapon, null_weapon]
class Selected:
    def __init__(self):
        self.pilot = null_pilot
        self.pilot_slot= -1
        self.loadout_slot = -1
        self.inventory_slot = -1
        self.item = null_weapon
        self.map_display = "none"
if startup == True: #create selected
    selected = Selected()
class Area(pygame.sprite.Sprite):
    def __init__(self,type,slot_number):
        super().__init__()
        self.slot_number = slot_number
        if type == "world_map":
            frame_0 = blank_frame
            frame_1 = pygame.image.load('graphics/maps/world_map.png')
            self.rect = frame_1.get_rect(center = centerpoint)
            self.frames = [frame_0,frame_1]
            self.name = "world_map"
        if type == "island":
            if self.slot_number == 1:
                frame_0 = blank_frame
                frame_1 = pygame.image.load('graphics/maps/island_1_map.png')
                self.pos_x = screen_width*0.3
                self.pos_y = screen_height*0.6
                self.hazards = ["bandits","drones","wind_storms"]
                self.name = "island_1"
            self.frames = [frame_0,frame_1]
        self.animation_index = 1
        self.image = self.frames[self.animation_index]
    def destroy(self):
        if selected.map_display != self.name:
            self.kill
    def update(self):
        self.image = self.frames[self.animation_index]
class Text_Names(pygame.sprite.Sprite):
    def __init__(self, type, column_number, row_number, slot_number):
        super().__init__()
        self.column_number = column_number
        self.row_number = row_number
        self.slot_number = slot_number
        self.selected = False
        self.type = type
        if type == "loadout":
            self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
            self.image = text_font_small.render(f"{self.name}",False,(0,0,0))  
            self.rect = self.image.get_rect(topleft = (screen_width*0.05 + column_number*100, screen_height*0.215 + row_number*40))             
        if type == "inventory":
            self.name = inventory_list[self.slot_number].name
            self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
            self.rect = self.image.get_rect(topleft = (screen_width*0.05 + column_number*100, screen_height*0.215 + row_number*40)) 
        if type == "pilot":
            self.name = pilot_list[self.slot_number].name
            self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
            self.rect = pygame.Rect(screen_width*0.05 + column_number*100, screen_height*0.215 + self.row_number*40,300,40) 
        if type == "swap_button":
            self.name = "swap_button"
            frame_1 = self.image = text_font.render(" ",False,(111,196,169))
            frame_2 = self.image = text_font.render("Swap Item",False,(0,0,0))
            self.animation_index = 0
            self.frames = [frame_1,frame_2]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (screen_width*0.45,screen_height*0.82))
    def update(self):
        if self.type == "loadout":
            self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
            self.image = text_font_small.render(f"{self.name}",False,(0,0,0))
        if self.type == "inventory":
            self.name = inventory_list[self.slot_number].name
            self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
        if self.type == "pilot":
            self.name = pilot_list[self.slot_number].name
            self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
        if self.type == "swap_button":
            if selected.inventory_slot > -1:
                self.animation_index = 1
            else: self.animation_index = 0
            self.image = self.frames[self.animation_index]       
class Nameplates(pygame.sprite.Sprite):
    def __init__(self,type,column_number,row_number,slot_number):
        super().__init__()
        self.column_number = column_number
        self.row_number = row_number
        self.slot_number = slot_number
        self.animation_index = 0
        self.selected = False
        self.cooldown = 0
        self.type = type
        
        if type == "inventory_line_item":
            frame_1 = pygame.image.load('graphics/interface/labels/interface_panel_name.png').convert_alpha()
            frame_1 = pygame.transform.scale(frame_1, (300,40))
            frame_2 = pygame.image.load('graphics/interface/labels/interface_panel_name_green.png').convert_alpha()
            frame_2 = pygame.transform.scale(frame_2, (300,40))
            self.name = inventory_list[self.slot_number].name
            self.height = 40
            self.frames = [frame_1,frame_2]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(topleft = (screen_width*0.1 +self.column_number*100, screen_height*0.25 + self.row_number*self.height))
        if type == "pilot_line_item":
            frame_1 = pygame.image.load('graphics/interface/labels/interface_panel_name.png').convert_alpha()
            frame_1 = pygame.transform.scale(frame_1, (300,40))
            frame_2 = pygame.image.load('graphics/interface/labels/interface_panel_name_green.png').convert_alpha()
            frame_2 = pygame.transform.scale(frame_2, (300,40))
            self.pilot = pilot_list[self.slot_number]
            self.name = self.pilot.name
            self.height = 40
            self.frames = [frame_1,frame_2]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(topleft = (screen_width*0.1 +self.column_number*100, screen_height*0.25 + self.row_number*self.height))
        if type == "loadout_label":
            frame_1 = pygame.image.load('graphics/interface/labels/label_white_lowres.png').convert_alpha()
            frame_1 = pygame.transform.scale(frame_1, (150,30))
            frame_2 = pygame.image.load('graphics/interface/labels/label_white_greenborder3.png').convert_alpha()
            frame_2 = pygame.transform.scale(frame_2, (150,30))
            self.height = 40
            self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
            self.frames = [frame_1,frame_2]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(topleft = (screen_width*0.1 +self.column_number*100, screen_height*0.25 + self.row_number*self.height))
        if type == "swap_button":
            frame_1 = pygame.image.load('graphics/blank.png')
            frame_2 = pygame.image.load('graphics/interface/labels/label_white_selected_lowres.png')
            frame_2 = pygame.transform.scale(frame_2, (300,100))
            self.height = 40
            self.name = "swap_button"
            self.frames = [frame_1,frame_2]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (screen_width*0.6, screen_height*1.1))
    def destroy(self):
        self.kill()
    def update(self):
        global selected
        self.click_button()
        if self.type == "pilot_line_item":
            if self.slot_number == selected.pilot_slot:
                self.selected = True
            else:
                self.selected = False
        if self.type == "loadout_label":
            self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
            if self.slot_number == selected.loadout_slot:
                self.selected = True
            else: self.selected = False
        if self.type == "inventory_line_item":
            if selected.loadout_slot >= -1:
                if self.slot_number == selected.inventory_slot:
                    self.selected = True
                else: self.selected = False
            else: self.selected = False
        if self.type == "swap_button":
            if selected.inventory_slot > -1:
                self.selected = True
            else: 
                self.selected = False
        
        if self.selected == True:
            self.animation_index = 1
        else: self.animation_index = 0
        self.image = self.frames[self.animation_index]
        if self.cooldown > 0:
            self.cooldown -= 1
    def click_button(self):
        global selected
        global inventory_list
        if event.type == pygame.MOUSEBUTTONDOWN: #Click
           if self.cooldown == 0:
                if self.rect.collidepoint(event.pos): #Toggle select
                    self.cooldown = 10
                    if self.type == "pilot_line_item":
                        if selected.pilot_slot == self.slot_number:
                            selected.pilot = null_pilot
                            selected.pilot_slot = -1
                        else:
                            selected.pilot_slot = self.slot_number
                            selected.pilot = self.pilot
                    if self.type == "loadout_label":
                        if self.slot_number == selected.loadout_slot:
                            selected.loadout_slot = -1
                        else:
                            selected.loadout_slot = self.slot_number
                    if self.type == "inventory_line_item":
                        if selected.loadout_slot >= 0:
                            if self.slot_number == selected.inventory_slot:
                                selected.inventory_slot = -1
                            else:
                                selected.inventory_slot = self.slot_number
                    if self.type == "swap_button":
                        if selected.inventory_slot > -1:
                            new_loadout_item = inventory_list[selected.inventory_slot]
                            new_inventory_item = selected.pilot.battlesuit.loadout[selected.loadout_slot]
                            selected.pilot.battlesuit.loadout[selected.loadout_slot] = new_loadout_item
                            inventory_list[selected.inventory_slot] = new_inventory_item
                            selected.loadout_slot = -1
                            selected.inventory_slot = -1                     
if startup == True: #create sprite groups       
    nameplates_group = pygame.sprite.Group()
    pilot_names_group = pygame.sprite.Group()
    inventory_names_group = pygame.sprite.Group()
    loadout_names_group = pygame.sprite.Group()
    area_group = pygame.sprite.Group()
def create_nameplate(type, column_number, row_number,slot_number):
    nameplates_group.add(Nameplates(type,column_number,row_number,slot_number))
if startup == True: #add nameplates
    create_nameplate("pilot_line_item",0,0,1)
    create_nameplate("pilot_line_item",0,1,2)
    create_nameplate("pilot_line_item",0,2,3)
    create_nameplate("pilot_line_item",0,3,4)
    create_nameplate("pilot_line_item",0,4,5)

    create_nameplate("inventory_line_item",7.2,0,1)
    create_nameplate("inventory_line_item",7.2,1,2)
    create_nameplate("inventory_line_item",7.2,2,3)

    create_nameplate("loadout_label", 3.2,2,1)
    create_nameplate("loadout_label", 3.2,6.3,3)
    create_nameplate("loadout_label", 5.6,2,2)
    create_nameplate("loadout_label", 5.6,4.1,0)
    create_nameplate("loadout_label", 5.6,6.3,4)
    
    create_nameplate("swap_button", 0,0,0)
        
selected.pilot = null_pilot

if startup == True: #add text names
    pilot_names_group.add(Text_Names("pilot",1,1,1))
    pilot_names_group.add(Text_Names("pilot",1,2,2))
    pilot_names_group.add(Text_Names("pilot",1,3,3))
    pilot_names_group.add(Text_Names("pilot",1,4,4))
    pilot_names_group.add(Text_Names("pilot",1,5,5))

    loadout_names_group.add(Text_Names("loadout",4,2.8,1))
    loadout_names_group.add(Text_Names("loadout",6.37,2.8,2))
    loadout_names_group.add(Text_Names("loadout",4,7.1,3))
    loadout_names_group.add(Text_Names("loadout",6.37,7.1,4))
    loadout_names_group.add(Text_Names("loadout",6.37,4.9,0))
    
    inventory_names_group.add(Text_Names("inventory",8.1,1,1))
    inventory_names_group.add(Text_Names("swap_button",0,0,0))
if startup == True: #load draw functions
    def draw_selected_pilot_name():
        selected.pilot_name_surf = text_font.render(f"{selected.pilot.name}",False,(111,196,169))
        selected.pilot_name_rect = selected.pilot_name_surf.get_rect(center = (screen_width*0.5,screen_height*0.3))
        screen.blit(selected.pilot_name_surf,(selected.pilot_name_rect))
    def draw_cockpit():
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
    def draw_mission_markers():
        if available_missions[1] == True:
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
    def draw_void():
        screen.fill((0,0,0))

while True: #game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i: #toggle inventory
                if window_display == "inventory":
                    window_display = "none"
                else:
                    window_display = "inventory"
                    x_button = True
                    continue_button = False
            if event.key == pygame.K_m:
                window_display = "map"
    if window_display == "none":
        draw_void()
        x_button = False
        continue_button = False
    if window_display == "inventory":
        pilot = selected.pilot
        draw_interface_back()
        draw_blueprint()
        nameplates_group.update()
        nameplates_group.draw(screen)
        pilot_names_group.update()
        pilot_names_group.draw(screen)
        loadout_names_group.update()
        loadout_names_group.draw(screen)
        inventory_names_group.update()
        inventory_names_group.draw(screen)
        draw_selected_pilot_name()
        draw_interface_screen_front()
        draw_small_frame("left")
        draw_small_frame("right")
        draw_ui_buttons()
    
    pygame.display.update()
    clock.tick(60)
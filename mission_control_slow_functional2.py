#clean version to test from
import pygame
import random
from sys import exit
import os
import copy
from math import atan2, degrees, pi


# none = "none"
BLACK = (0,0,0)
available_missions_list = [False,True,False,False,False,False]
continue_button = False
active_mission = 0


startup = True
def random_pos():
    pos = random.randint(-screen_width*0.5,screen_width*1.5)
def roll_1d6():
    roll_result = random.randint(1,6)
    return roll_result
def get_sprite_frames(sheet, frame_x, frame_y, width, height, colour):
    image = pygame.Surface((width, height)).convert_alpha()
    x = frame_x*width
    y = frame_y*height
    image.blit(sheet,(0,0),(x,y,width,height))
    image.set_colorkey(colour)
    return image
def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = text_font.render(fps, 1, pygame.Color("coral"))
    return fps_text

if startup: #load notes
    power_core_list = {"01":"trapped_combustion_core", "02":"dirty_fission_core", "04":"solar_array_core", "06":"cold_fusion_core", "07":"entropy_core", "08":"black_pinhole_core", "10":"wave_collapse_core", "11":"phantom_pinnacle_core", "0x":"alien_crystal_core", "00":"no_core"}
    #suit code is size class, power core type , power core capacity, product generation
    #086403 = 08.6.4.03 = size 8, fusion core, capacity 4, generation 3
    #core type determines what kind of fuel the suit needs to operate
    #can replace core with high capacity battery that does not recharge outside of base. Each unit of stored charge = 60 seconds of powercore output
    pass

if startup: #load screen
    screen_width = 1280
    screen_height = 720
    centerpoint = ((screen_width)/2, (screen_height)/2)
    pygame.init()
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("mission_control")
    text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
    text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
    text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 20)
    clock = pygame.time.Clock()

blank_frame = pygame.image.load("graphics/blank.png").convert_alpha()
blank_frame = pygame.transform.scale(blank_frame, (10,10))
explosion_sheet_1 = pygame.image.load("graphics/weapons/explosion_sprite_1.png").convert_alpha()
explosion_sheet_2 = pygame.image.load("graphics/weapons/explosion_sprite_2.png").convert_alpha()
explosion_sheet_3 = pygame.image.load("graphics/weapons/explosion_sprite_3.png").convert_alpha()
explosion_sheet_4 = pygame.image.load("graphics/weapons/explosion_sprite_4.png").convert_alpha()

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    y = rect.top
    lineSpacing = 10
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]

    return text
    
if startup: #load classes
    class Power_Core:
        def __init__(self, type):
            self.type = type
            self.function = "generator"
            self.cooldown = -1
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
    class Weapon:
        damage_types = ["thermal","cold","piercing","concussive","magnetic","shock","sonic","gravity"]
        status_effects_list = ["frozen","overheated","disrupted","blinded","knockback","energized","supressed","tethered"]
        def __init__(self, type):
            self.function = "weapon"
            self.cooldown = -1
            self.type = type
            self.distance = 0
            self.damage_type = "none"
            self.form = "none"
            self.accuracy = 0
            if type == "unassigned_weapon":
                self.name = "Unassigned"
            if type == "beam_cannon":
                self.name = "Beam Cannon"
                self.accuracy = 1
                self.distance = 200
                self.cooldown = 200
                self.form = "beam"
                self.damage_type = "thermal"
                self.apply_status = "overheated"
            if type == "cryo_shot":
                self.name = "Cryo Shot"
                self.accuracy = 2
                self.distance = 100
                self.cooldown = 200
                self.form = "beam"
                self.damage_type = "cold"
                self.apply_status = "frozen"
            if type == "powersword":
                self.name = "Powersword"
                self.accuracy = 1
                self.distance = 10
                self.cooldown = 200
                self.damage_type = "pierce"
                self.apply_status = "knockback"
            if type == "flame_lance":
                self.name = "Flame Lance"
                self.accuracy = 4
                self.distance = 60
                self.cooldown = 200
                self.form = "burst"
                self.damage_type = "thermal"
                self.apply_status = "knockback" + "overheated"
            if type == "lightning_chain":
                self.name = "Lightning Chain"
                self.accuracy = 1
                self.distance = 30
                self.cooldown = 200
                self.damage = "shock"
                self.apply_status = "disrupted" + "tethered"
            if type == "null_weapon":
                self.name = " "            
    class Weapon_Effect(pygame.sprite.Sprite):
        def __init__(self, form, damage_type, angle, pilot):
            super().__init__()
            self.form = form
            self.damage_type = damage_type
            self.attack_angle = angle
            self.pilot = pilot
            self.countdown = 1
            self.frames = [blank_frame,blank_frame]
            self.animation_index = 1
            self.image = blank_frame
            if self.form == "beam" and self.damage_type == "thermal":
                self.frame_1 = pygame.image.load("graphics/weapons/laserbeam_thin_half.png").convert_alpha()
                self.frame_0 = blank_frame
                self.frames = [self.frame_0,self.frame_1]
                self.image = self.frames[self.animation_index]
                self.image = pygame.transform.scale(self.image,(20,self.pilot.attack_target_distance_h*2.1))
                self.countdown = 20
            if self.form == "beam" and self.damage_type == "cold":
                self.frame_0 = blank_frame
                self.frame_1 = pygame.image.load("graphics/weapons/ice_laser.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1]
                self.image = self.frames[self.animation_index]
                self.image = pygame.transform.scale(self.image,(20,self.pilot.attack_target_distance_h*2.1))
                self.countdown = 20
            if self.form == "burst" and self.damage_type == "thermal":
                self.frame_0 = blank_frame
                self.frame_1 = pygame.image.load("graphics/weapons/fire1.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/weapons/fire2.png").convert_alpha()
                self.frame_3 = pygame.image.load("graphics/weapons/fire3.png").convert_alpha()
                self.frame_4 = pygame.image.load("graphics/weapons/fire4.png").convert_alpha()
                self.frame_5 = pygame.image.load("graphics/weapons/fire5.png").convert_alpha()
                self.frame_6 = pygame.image.load("graphics/weapons/fire6.png").convert_alpha()
                self.frame_7 = pygame.image.load("graphics/weapons/fire7.png").convert_alpha()
                self.frame_8 = pygame.image.load("graphics/weapons/fire8.png").convert_alpha()
                self.frames = [self.frame_0, self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5, self.frame_6, self.frame_7, self.frame_8]
                self.countdown = 60
                self.image = self.frames[self.animation_index]
            if self.form == "explosion":
                explosion_sheets_group = [explosion_sheet_1,explosion_sheet_2,explosion_sheet_3,explosion_sheet_4]
                self.animation_index = 0
                # self.frames = explosion_frames
                # self.image = blank_frame
                self.countdown = 64
                self.sheet = random.choice(explosion_sheets_group)
                self.sheet_column = 0
                self.sheet_row = 0
            self.image = pygame.transform.rotate(self.image,self.attack_angle)
            self.rect = self.image.get_rect(center = (self.pilot.pos_x,self.pilot.pos_y))
        def draw_explosion(self,sheet,height,column,row):
            screen.blit(sheet, (self.pilot.pos_x-height*0.5,self.pilot.pos_y-height*0.5),(height*column,height*row,height,height))
        def update(self):
            if self.countdown == 0:
                self.kill()
            self.countdown -= 1
            self.attack_angle = self.pilot.attack_target_angle - 90
            if self.form == "explosion":
                self.sheet_column += 1
                self.image = blank_frame
                if self.sheet_column == 8:
                    self.sheet_column = 0
                    self.sheet_row += 1
                self.draw_explosion(self.sheet, 256, self.sheet_column, self.sheet_row)
            if self.form == "beam" and self.damage_type == "thermal":
                self.image = self.frames[self.animation_index]
                self.image = pygame.transform.scale(self.frame_1,(30,self.pilot.attack_target_distance_h*2.1))
            if self.form == "beam" and self.damage_type == "cold":
                if self.animation_index == 1:
                    self.image = self.frames[self.animation_index]
                    self.image = pygame.transform.scale(self.frame_1,(20,self.pilot.attack_target_distance_h*2.1))
            if self.form == "burst" and self.damage_type == "thermal":
                self.animation_index += 0.3
                if self.animation_index > 8:
                    self.animation_index = 1
                self.image = self.frames[int(self.animation_index)]
            self.image = pygame.transform.rotate(self.image,self.attack_angle)
            self.rect = self.image.get_rect(center = (self.pilot.pos_x,self.pilot.pos_y))                    
    class Shield:
        def __init__(self, type):
            self.function = "shield"
            if type == "light_shield":
                self.name = "Light Shield"
                self.cooldown = 2000
                self.charged = True  
    class Battlesuit(pygame.sprite.Sprite):
        def __init__(self, type):
            super().__init__()
            self.type = type
            self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
            self.mobility = 1
            self.shielded = True
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
            if type == "train":
                self.name = "Train"
                self.mobility = 1
                self.refresh = 4
                self.power_core = fusion_core
                self.size = 2
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
    class Mission_Object(pygame.sprite.Sprite):
        def __init__(self, name, type, slot_number, pos_x, pos_y, team):
            super().__init__()
            self.name = name
            self.type = type
            self.slot_number = slot_number
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.team = team
            self.damaged = False
            self.animation_index = 0
            if self.type == "radio_tower":
                self.frame_0 = blank_frame
                self.frame_1 = pygame.image.load("graphics/interface/icons/radio.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1]
                for frame in self.frames:
                    frame = pygame.transform.scale(frame, (10,10))
                self.image = self.frames[self.animation_index]
                self.function = "waypoint"
                self.countdown_max = -1
            if self.type == "supply_crate":
                self.frame_0 = blank_frame
                self.frame_1 = pygame.image.load("graphics/interface/icons/box_closed.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/box_open.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                for frame in self.frames:
                    frame = pygame.transform.scale(frame, (20,20))
                self.image = self.frames[self.animation_index]
                self.function = "pickup"
                self.countdown_max = 10
            self.countdown = self.countdown_max
            self.rect = self.image.get_rect(center = (pos_x,pos_y))
        def update(self):
            if self.type == "supply_crate":
                if self.function == "pickup":
                    self.animation_index = 1
                if self.function == "picked-up":
                    self.animation_index = 2
    class Pilot(pygame.sprite.Sprite):
        def __init__(self, name, slot_number, battlesuit, team):
            super().__init__()
            self.name = name
            self.team = team
            self.function = "pilot"
            self.injured = False
            self.alive = True
            self.lines = []
            self.rank = 1
            self.checkpoint = 0
            self.slot_number = slot_number
            self.active = False
            self.orders = "objective"
            self.pos_x = random.randint(-screen_width*0.5,screen_width*1.5)
            self.pos_y = random.randint(-screen_height,0)
            self.attack_target = "null_pilot"
            self.move_target = "null_pilot"
            self.momentum_x = 0
            self.momentum_y = 0
            self.attack_target_angle = 0
            self.move_target_angle = 0
            self.attack_target_distance_h = 0
            self.move_target_distance_h = 0
            self.battlesuit = battlesuit
            self.mobility = self.battlesuit.mobility
            self.animation_index = 1
            self.frame_0 = blank_frame
            self.frame_0 = pygame.transform.scale(self.frame_0, (10,10))
            self.invuln_timer = 0
            if self.team == "friend":
                self.frame_1 = pygame.image.load("graphics/interface/icons/blue_dot.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/blue_dot_shielded.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
            if self.team == "enemy":
                self.frame_1 = pygame.image.load("graphics/interface/icons/red_dot.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/red_dot_shielded.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
            if self.name == "Tower":
                self.pos_x = screen_width*2
                self.pos_y = screen_height*2
            self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        def find_target(self, type):
            if self.name != "supply_train":
                if type == "attack":
                    if self.team == "friend":
                        for enemy in mission_enemy_group:
                            if enemy.alive == True and enemy.battlesuit.severely_damaged == False:
                                enemy_distance = self.find_target_distance(enemy)
                                if enemy_distance < self.attack_target_distance_h:
                                    self.attack_target = enemy
                    if self.team == "enemy":
                        for enemy in pilot_list:
                            enemy_distance = self.find_target_distance(enemy)
                            if enemy_distance < self.attack_target_distance_h and enemy.alive == True:
                                self.attack_target = enemy
                if type == "movement":
                    if self.orders == "aggressive":
                        if self.attack_target.battlesuit.severely_damaged == False:
                            self.move_target = self.attack_target
                        else: self.orders = "objective"
                    if self.orders == "objective":
                        for objective in mission_objects_group:
                            target_distance = self.find_target_distance(objective)
                            if target_distance < self.move_target_distance_h:
                                self.move_target = objective
        def find_target_distance(self,target):
            if target.alive == True:
                target_distance_x = target.pos_x - self.pos_x
                target_distance_y = target.pos_y - self.pos_y
                target_distance_h = (target_distance_x**2 + target_distance_y**2)**(1/2)
            else: target_distance_h = screen_width*2
            return target_distance_h
        def mission_object_interaction(self):
            objective = self.move_target
            if self.orders == "objective":
                if objective.function == "pickup" and self.move_target_distance_h < 10:
                    self.momentum_x *= 0.5
                    self.momentum_y *= 0.5
                    if objective.countdown == objective.countdown_max:
                        create_clock(objective)
                    if objective.countdown > 0:
                        objective.countdown -= 0.1
                    if objective.countdown == 0:
                        objective.function = "picked-up"
                        self.held = objective                            
        def targeting_distance(self):
            self.attack_target_distance_x = self.attack_target.pos_x - self.pos_x
            self.attack_target_distance_y = self.attack_target.pos_y - self.pos_y
            self.attack_target_distance_h = (self.attack_target_distance_x**2 + self.attack_target_distance_y**2)**(1/2)
            self.move_target_distance_x = self.move_target.pos_x - self.pos_x
            self.move_target_distance_y = self.move_target.pos_y - self.pos_y
            self.move_target_distance_h = (self.move_target_distance_x**2 + self.move_target_distance_y**2)**(1/2)
        def find_target_angle(self):
            rads = atan2(-self.attack_target_distance_y,self.attack_target_distance_x)
            rads %= 2*pi
            angle = degrees(rads)
            self.attack_target_angle = angle
            rads = atan2(-self.move_target_distance_y,self.move_target_distance_x)
            rads %= 2*pi
            angle = degrees(rads)
            self.move_target_angle = angle
        def maintain_shields(self):
            if self.battlesuit.shielded == True:
                self.animation_index = 2
            else:
                self.animation_index = 1
            self.image = self.frames[self.animation_index]
            for item in self.battlesuit.loadout:
                if item.function == "shield":
                    if item.cooldown > 0:
                            self.charged = False
                            item.cooldown -= 1
                    if item.cooldown == 0:
                        item.charged = True
                    if self.battlesuit.shielded == False and item.charged == True:
                        self.battlesuit.shielded = True
                        item.charged = False
                        item.cooldown = 200
        def attack(self, target):
            if target.team != self.team and target.injured == False:
                for item in self.battlesuit.loadout:
                # item = self.battlesuit.loadout[1]
                    if item.cooldown > 0:
                        item.cooldown -= 1
                    if item.function == "weapon" and item.cooldown <= 0 and self.attack_target.invuln_timer == 0:
                        if self.attack_target_distance_h < item.distance:
                            item.cooldown = 200
                            self.attack_target.invuln_timer = 20
                            weapon_effects_group.add(Weapon_Effect(item.form, item.damage_type, self.attack_target_angle, self))
                            hit_roll = roll_1d6() + item.accuracy
                            if hit_roll >= 3 + target.mobility:
                                if target.battlesuit.shielded == True:
                                    target.battlesuit.shielded = False
                                elif target.battlesuit.damaged == False:
                                    target.battlesuit.damaged = True
                                elif target.battlesuit.severely_damaged == False:
                                    target.battlesuit.severely_damaged = True
                                elif target.injured == False:
                                    target.injured = True
                                else: 
                                    target.alive = False
        def maneuver(self):
            if self.battlesuit.severely_damaged == True: #retreat
                if self.name != "supply_train" and self.name != "Tower":
                    self.momentum_x *= 1.1
                    self.momentum_y *= 1.1
            if self.move_target_distance_x >= 0:
                self.momentum_x += 0.01*10
                # self.momentum_x += 0.002*self.move_target_distance_x
            else:
                self.momentum_x -= 0.01*10
                # self.momentum_x -= 0.002*abs(self.move_target_distance_x) 
            if self.move_target_distance_y >= 0:
                self.momentum_y += 0.001*50
                # self.momentum_y += 0.01*self.move_target_distance_y
            else:
                # self.momentum_y -= 0.002*abs(self.move_target_distance_y)
                self.momentum_y -= 0.01*10
            #speed limit
            if abs(self.momentum_x) > 12:
                self.momentum_x *= 0.9
            if abs(self.momentum_y) >12:
                self.momentum_y *= 0.9
            if self.name == "supply_train":
                if abs(self.momentum_x) > 5:
                    self.momentum_x *= 0.9
                if abs(self.momentum_y) >5:
                    self.momentum_y *= 0.9
            #update positions
            self.pos_y = (self.pos_y + self.momentum_y*0.1*self.mobility)
            self.pos_x = (self.pos_x + self.momentum_x*0.1*self.mobility)
        def update(self):
            if self.invuln_timer > 0:
                self.invuln_timer -= 1
            if self.attack_target == "null_pilot":
                self.attack_target = tower_1
            if self.move_target == "null_pilot":
                self.move_target = tower_1
            if self.name == "supply_train":
                self.damaged = False
            self.find_target("attack")
            self.find_target("movement")
            if self.battlesuit.type == "drone": #control drones
                if self.alive == True:
                    self.ttl = 64
                if self.pos_x > screen_width*2:
                    self.kill()
                if self.battlesuit.damaged == True:
                    self.battlesuit.severely_damaged = True
                    self.injured = True
                    self.alive = False
                    if self.alive == False:
                        if self.ttl == 64:
                            weapon_effects_group.add(Weapon_Effect("explosion", "thermal", 0, self))
                        self.ttl -= 1
                    if self.ttl == 0:
                        self.kill()
            if self.name == "supply_train": #control train
                self.alive = True
            if self.alive == False:
                self.kill()
            self.targeting_distance()
            self.find_target_angle()
            self.maintain_shields()
            self.attack(self.attack_target)
            self.mission_object_interaction()
            self.maneuver()
            self.find_target("attack")
            self.find_target("movement")
            self.rect = self.image.get_rect(center = (int(self.pos_x),int(self.pos_y)))
            for pilot in pilot_list: #avoid bunching up
                if pilot.name != self.name:
                    if abs(pilot.pos_x - self.pos_x) < 0.1:
                        self.momentum_x = self.momentum_x * 1.1
    class Selected:
        def __init__(self):
            self.pilot = null_pilot
            self.pilot_slot= -1
            self.loadout_slot = -1
            self.inventory_slot = -1
            self.item = null_weapon
            self.map_display = "none"
            self.island_number = -1
            self.pointer_slot = -1
    class Island(pygame.sprite.Sprite):
        def __init__(self,type,slot_number):
            super().__init__()
            self.slot_number = slot_number
            self.missions = []
            if type == "world_map":
                self.frame_0 = blank_frame
                self.frame_1 = pygame.image.load("graphics/maps/ocean_map.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/maps/ocean_map.png").convert_alpha()
                self.rect = self.frame_1.get_rect(center = centerpoint)
                self.name = "world_map"
                self.pos_x = screen_width/2
                self.pos_y = screen_height/2
            if type == "island":
                if self.slot_number == 1:
                    self.frame_0 = blank_frame
                    self.frame_1 = pygame.image.load("graphics/maps/island_1.png").convert_alpha()
                    self.frame_2 = pygame.image.load("graphics/maps/island_1_highlight.png").convert_alpha()
                    self.pos_x = screen_width*0.43
                    self.pos_y = screen_height*0.55
                    self.hazards = ["bandits","drones","wind_storms"]
                    self.name = "island_1"
                if self.slot_number == 2:
                    self.frame_0 = blank_frame
                    self.frame_1 = pygame.image.load("graphics/maps/island_2.png").convert_alpha()
                    self.frame_2 = pygame.image.load("graphics/maps/island_2_highlight.png").convert_alpha()
                    self.pos_x = screen_width*0.45
                    self.pos_y = screen_height*0.3
                    self.hazards = ["bandits","drones","wind_storms"]
                    self.name = "island_2"
                if self.slot_number == 3:
                    self.frame_0 = blank_frame
                    self.frame_1 = pygame.image.load("graphics/maps/island_3.png").convert_alpha()
                    self.frame_2 = pygame.image.load("graphics/maps/island_3_highlight.png").convert_alpha()
                    self.pos_x = screen_width*0.54
                    self.pos_y = screen_height*2
                    self.hazards = ["bandits","drones","wind_storms"]
                    self.name = "island_3"
                if self.slot_number == 4:
                    self.frame_0 = blank_frame
                    self.frame_1 = pygame.image.load("graphics/maps/island_4.png").convert_alpha()
                    self.frame_2 = pygame.image.load("graphics/maps/island_4_highlight.png").convert_alpha()
                    self.pos_x = screen_width*0.61
                    self.pos_y = screen_height*0.35
                    self.hazards = ["bandits","drones","wind_storms"]
                    self.name = "island_4"
                if self.slot_number == 5:
                    self.frame_0 = blank_frame
                    self.frame_1 = pygame.image.load("graphics/maps/island_5.png").convert_alpha()
                    self.frame_2 = pygame.image.load("graphics/maps/island_5_highlight.png").convert_alpha()
                    self.pos_x = screen_width*0.7
                    self.pos_y = screen_height*0.55
                    self.hazards = ["bandits","drones","wind_storms"]
                    self.name = "island_5"
                if self.slot_number == 6:
                    self.frame_0 = blank_frame
                    self.frame_1 = pygame.image.load("graphics/maps/island_6.png").convert_alpha()
                    self.frame_2 = pygame.image.load("graphics/maps/island_6_highlight.png").convert_alpha()
                    self.pos_x = screen_width*0.75
                    self.pos_y = screen_height*0.75
                    self.hazards = ["bandits","drones","wind_storms"]
                    self.name = "island_6"
            self.animation_index = 1
            self.frames = [self.frame_0,self.frame_1,self.frame_2]
            self.image = self.frames[self.animation_index]
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.mask.get_rect(center = (self.pos_x,self.pos_y))
            self.highlighted = False
            self.cooldown = 0
            self.type = type
        def destroy(self):
            if selected.map_display != self.name:
                self.kill()
        def update(self):
            self.click_button()
            if self.cooldown > 0:
                self.cooldown -= 1
                if self.highlighted == True:
                    self.animation_index = 2
                else:
                    self.animation_index = 1
                self.image = self.frames[self.animation_index]
        def click_button(self):
            global selected
            if event.type == pygame.MOUSEBUTTONDOWN: #Click
                if self.type == "island":
                    if self.cooldown == 0:
                        self.cooldown = 10
                        mouse_pos = pygame.mouse.get_pos()
                        mouse_pos_in_mask = mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y
                        mouse_touching = self.rect.collidepoint(*mouse_pos) and self.mask.get_at(mouse_pos_in_mask)
                        if mouse_touching == True:
                            if self.highlighted == True:
                                self.highlighted = False
                            else:
                                self.highlighted = True
                        else:
                            self.highlighted = False
                        if self.rect.collidepoint(event.pos):
                            if selected.island_number == self.slot_number:
                                selected.island_number = -1
                            else:
                                selected.island_number = self.slot_number            
    class Text_Names(pygame.sprite.Sprite):
        def __init__(self, type, slot_number):
            super().__init__()
            self.slot_number = slot_number
            self.selected = False
            self.type = type
            if type == "loadout":
                self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
                self.image = text_font_small.render(f"{self.name}",False,(0,0,0))
                if self.slot_number == 0: self.rect = self.image.get_rect(center = (screen_width*0.6,screen_height*0.5))
                if self.slot_number == 1: self.rect = self.image.get_rect(center = (screen_width*0.32,screen_height*0.33))
                if self.slot_number == 2: self.rect = self.image.get_rect(center = (screen_width*0.6,screen_height*0.33))
                if self.slot_number == 3: self.rect = self.image.get_rect(center = (screen_width*0.32,screen_height*0.68))
                if self.slot_number == 4: self.rect = self.image.get_rect(center = (screen_width*0.6,screen_height*0.68))             
            if type == "inventory":
                self.name = inventory_list[self.slot_number].name
                self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
                self.rect = self.image.get_rect(topleft = (screen_width*0.8, screen_height*0.215 + self.slot_number*40)) 
            if type == "pilot":
                self.pilot = pilot_list[self.slot_number]
                self.name = self.pilot.name
                self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
                self.rect = pygame.Rect(screen_width*0.06, screen_height*0.215 + self.slot_number*40,300,40) 
            if type == "swap_button":
                self.name = "swap_button"
                self.frame_1 = self.image = text_font.render(" ",False,(111,196,169))
                self.frame_2 = self.image = text_font.render("Swap Item",False,(0,0,0))
                self.animation_index = 0
                self.frames = [self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
                self.rect = self.image.get_rect(center = (screen_width*0.45,screen_height*0.82))
        def update(self):
            if overlay.type == "inventory":
                if self.type == "loadout":
                    self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
                    self.image = text_font_small.render(f"{self.name}",False,(0,0,0))
                if self.type == "inventory":
                    self.name = inventory_list[self.slot_number].name
                    self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
                if self.type == "pilot":
                    if overlay.type == "inventory":
                        self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
                        self.rect = pygame.Rect(screen_width*0.06, screen_height*0.215 + self.slot_number*40,300,40) 
                if self.type == "swap_button":
                    if selected.inventory_slot > -1:
                        self.animation_index = 1
                    else: self.animation_index = 0
                    self.image = self.frames[self.animation_index]  
            if overlay.type == "combat":
                if self.type == "pilot":
                    self.image = text_font_micro.render(f"{self.name}",False,(111,196,169))
                    self.rect = self.image.get_rect(center = (self.pilot.pos_x,self.pilot.pos_y+11)) 
    class Nameplates(pygame.sprite.Sprite):
        def __init__(self,type,slot_number):
            super().__init__()
            self.type = type
            self.slot_number = slot_number
            self.animation_index = 0
            self.selected = False
            self.cooldown = 0
            if type == "inventory_line_item":
                self.frame_1 = pygame.image.load("graphics/interface/labels/interface_panel_name.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (300,40))
                self.frame_2 = pygame.image.load("graphics/interface/labels/interface_panel_name_green.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2, (300,40))
                self.name = inventory_list[self.slot_number].name
                self.height = 40
                self.frames = [self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
                self.rect = self.image.get_rect(topright = (screen_width*0.95, screen_height*0.18 + self.slot_number*self.height))
            if type == "pilot_line_item":
                self.frame_1 = pygame.image.load("graphics/interface/labels/interface_panel_name.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (300,40))
                self.frame_2 = pygame.image.load("graphics/interface/labels/interface_panel_name_green.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2, (300,40))
                self.pilot = pilot_list[self.slot_number]
                self.name = self.pilot.name
                self.height = 40
                self.frames = [self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
                self.rect = self.image.get_rect(topleft = (screen_width*0.05, screen_height*0.18 + self.slot_number*self.height))
            if type == "loadout_label":
                self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
                self.frame_1 = pygame.image.load("graphics/interface/labels/label_white_lowres.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (screen_width*0.12,screen_height*0.07))
                self.frame_2 = pygame.image.load("graphics/interface/labels/label_white_greenborder3.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2, (screen_width*0.12,screen_height*0.07))
                self.height = 40
                self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
                self.frames = [self.frame_1,self.frame_2,self.frame_0]
                self.image = self.frames[self.animation_index]
                if self.slot_number == 0: self.rect = self.image.get_rect(center = (screen_width*0.63,screen_height*0.5))
                if self.slot_number == 1: self.rect = self.image.get_rect(center = (screen_width*0.36,screen_height*0.33))
                if self.slot_number == 2: self.rect = self.image.get_rect(center = (screen_width*0.63,screen_height*0.33))
                if self.slot_number == 3: self.rect = self.image.get_rect(center = (screen_width*0.36,screen_height*0.68))
                if self.slot_number == 4: self.rect = self.image.get_rect(center = (screen_width*0.63,screen_height*0.68))
                # self.rect = self.image.get_rect(topleft = (screen_width*0.1 +self.column_number*100, screen_height*0.25 + self.slot_number*self.height))
            if type == "swap_button":
                self.frame_1 = pygame.image.load("graphics/blank.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/labels/label_white_selected_lowres.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2, (300,100))
                self.height = 40
                self.name = "swap_button"
                self.frames = [self.frame_1,self.frame_2]
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
                if self.slot_number == selected.loadout_slot and selected.pilot_slot > -1:
                    self.selected = True
                else: self.selected = False
            if self.type == "inventory_line_item":
                if selected.loadout_slot >= -1:
                    if self.slot_number == selected.inventory_slot:
                        self.selected = True
                    else: self.selected = False
                else: self.selected = False
            if self.type == "swap_button":
                if selected.inventory_slot > -1 and selected.pilot_slot > -1 and selected.loadout_slot > -1:
                    self.selected = True
                else: 
                    self.selected = False
            if self.selected == True:
                self.animation_index = 1
            else: self.animation_index = 0
            self.image = self.frames[self.animation_index]
            if self.type == "loadout_label" and overlay.type != "inventory": 
                self.image = self.frame_0
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
    class Pointer(pygame.sprite.Sprite):
        def __init__(self, type, pos_x, pos_y, slot_number):
            super().__init__()
            self.type = type
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.image = blank_frame
            self.slot_number = slot_number
            self.animation_index = 1
            self.frame_0 = blank_frame
            self.cooldown = 10
            if self.type == "rail":
                self.frame_1 = pygame.image.load("graphics/interface/pointers/rail_pointer.png")
                self.frame_2 = pygame.image.load("graphics/interface/pointers/rail_pointer_highlight.png")
                self.frames = [self.frame_0, self.frame_1, self.frame_2]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (pos_x,pos_y))
        def update(self):
            if self.cooldown > 0:
                self.cooldown -= 1
            self.image = self.frames[self.animation_index]
            if event.type == pygame.MOUSEBUTTONDOWN: #Click
                if self.rect.collidepoint(event.pos) and self.cooldown == 0:
                    overlay.type = "mission_brief"
                    dialogue.load_scene_dialogue("mission",1)
                    self.cooldown = 10
                    if self.animation_index == 2:
                        self.animation_index = 1
                        selected.pointer_slot = self.slot_number
                    else: 
                        self.animation_index = 2
                        selected.pointer_slot = -1
    class Icon(pygame.sprite.Sprite):
        def __init__(self,type, pilot):
            super().__init__()
            self.pilot = pilot
            self.frames = []
            self.animation_index = 0
            self.slot_number = 0
            self.type = type
            if type == "clock":
                self.frame_0 = pygame.image.load("graphics/interface/icons/clock_segments/clock_0.png").convert_alpha()
                self.frame_1 = pygame.image.load("graphics/interface/icons/clock_segments/clock_1.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/clock_segments/clock_2.png").convert_alpha()
                self.frame_3 = pygame.image.load("graphics/interface/icons/clock_segments/clock_3.png").convert_alpha()
                self.frame_4 = pygame.image.load("graphics/interface/icons/clock_segments/clock_4.png").convert_alpha()
                self.frame_5 = pygame.image.load("graphics/interface/icons/clock_segments/clock_5.png").convert_alpha()
                self.frame_6 = pygame.image.load("graphics/interface/icons/clock_segments/clock_6.png").convert_alpha()
                self.frame_7 = pygame.image.load("graphics/interface/icons/clock_segments/clock_7.png").convert_alpha()
                self.frame_8 = pygame.image.load("graphics/interface/icons/clock_segments/clock_8.png").convert_alpha()
                self.frame_9 = pygame.image.load("graphics/interface/icons/clock_segments/clock_9.png").convert_alpha()
                self.frame_10 = pygame.image.load("graphics/interface/icons/clock_segments/clock_10.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2,self.frame_3,self.frame_4,self.frame_5,self.frame_6,self.frame_7,self.frame_8,self.frame_9,self.frame_10]
                for frame in self.frames:
                    frame = pygame.transform.scale(frame, (40,40))
                self.pos_x = self.pilot.move_target.pos_x
                self.pos_y = self.pilot.move_target.pos_y
                self.countdown = 10
            if type == "shield":
                self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
                self.frame_0 = pygame.transform.scale(self.frame_0, (30,30))
                self.frame_1 = pygame.image.load("graphics/interface/icons/shield.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (30,30))
                self.frames = [self.frame_0,self.frame_1]
                self.slot_number = 1
            if type == "damaged":
                self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
                self.frame_0 = pygame.transform.scale(self.frame_0, (30,30))
                self.frame_1 = pygame.image.load("graphics/interface/icons/warning_white.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (30,30))
                self.frame_2 = pygame.image.load("graphics/interface/icons/warning_yellow.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2, (30,30))
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.slot_number = 2
            if type == "severely_damaged":
                self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
                self.frame_0 = pygame.transform.scale(self.frame_0, (30,30))
                self.frame_1 = pygame.image.load("graphics/interface/icons/warning_white.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (30,30))
                self.frame_2 = pygame.image.load("graphics/interface/icons/warning_red.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2, (30,30))
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.slot_number = 3
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = ((screen_width*0.17+40*self.slot_number),screen_height*0.21+40*self.pilot.slot_number))
        def update(self):
            if self.type == "shield":
                if self.pilot.battlesuit.shielded == False: 
                    self.animation_index = 0
                else: self.animation_index = 1
            if self.type == "damaged":
                if self.pilot.battlesuit.damaged == False: self.animation_index = 1
                else: self.animation_index = 2
            if self.type == "severely_damaged":
                if self.pilot.battlesuit.severely_damaged == False: self.animation_index = 1
                else: self.animation_index = 2
            if overlay.type != "health_tracker" and overlay.type != "combat":
                self.animation_index = 0
            if self.type == "segment_clock":
                self.rect = self.image.get_rect(center = (self.pilot.pos_x, self.pilot.pos_y))
                self.countdown = self.pilot.countdown
                self.animation_index = int(self.countdown)
                if overlay.type != "combat":
                    self.animation_index = 0
                self.image = self.frames[self.animation_index]
                if self.countdown == 0:
                    self.kill()
            self.image = self.frames[self.animation_index]
    class Button(pygame.sprite.Sprite):
        def __init__(self, type):
            super().__init__()
            self.type = type
            self.pos_x = 0
            self.pos_y = 0
            self.animation_index = 0
            self.frame_0 = blank_frame
            if self.type == "x_button":
                self.frame_1 = pygame.image.load("graphics/interface/icons/x_button_75.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1,(screen_width*0.05,screen_height*0.05))
                self.frames = [self.frame_0, self.frame_1]
                self.animation_index = 0
                self.image = self.frames[self.animation_index]
                self.pos_x = screen_width*0.15
                self.pos_y - screen_height*0.15
                self.rect = self.image.get_rect(topleft = (self.pos_x,self.pos_y))
            if self.type == "dashboard_map":
                self.frame_1 = pygame.image.load("graphics/interface/cockpit/clickscreen.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (screen_width*0.2,screen_height*0.2))
                self.frames = [self.frame_0, self.frame_1]
                self.animation_index = 1
                self.image = self.frames[self.animation_index]
                self.pos_x = screen_width*0.01
                self.pos_y = screen_height*0.1
                self.rect = self.image.get_rect(topleft = (self.pos_x,self.pos_y))
            if self.type == "continue_button":
                self.animation_index = 0
            self.frames = [self.frame_0, self.frame_1]
            self.image = self.frame_0
            self.rect = self.image.get_rect(topleft = (self.pos_x,self.pos_y))
        def update(self):
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(topleft = (self.pos_x,self.pos_y))
            if self.type == "dashboard_map":
                if overlay.type != "cockpit": self.animation_index = 0
                else: self.animation_index = 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    if self.type == "x_button" and overlay.type != "cockpit":
                        overlay.type = "cockpit"
                    if overlay.type == "cockpit" and self.type == "dashboard_map":
                        overlay.type = "map"
    class Overlay_Manager:
        def __init__(self, type):
            self.type = type
            self.large_frame_image = pygame.image.load("graphics/interface/frames/white_frame_large.png").convert_alpha()
            self.large_frame_image = pygame.transform.scale(self.large_frame_image, (screen_width*0.9,screen_height*0.9))
            self.large_frame_rect = self.large_frame_image.get_rect(center = (screen_width/2,screen_height/2)) 
            self.black_block_image = pygame.image.load("graphics/interface/frames/black_blocker.png").convert_alpha()
            self.black_block_image = pygame.transform.scale(self.black_block_image, (screen_width,screen_height))
            self.black_block_rect = self.black_block_image.get_rect(center = centerpoint)
            self.green_filter_image = pygame.image.load("graphics/interface/green_filter.png").convert_alpha()
            self.green_filter_image = pygame.transform.scale(self.green_filter_image, (screen_width*1,screen_height*1))
            self.green_filter_rect = self.green_filter_image.get_rect(center = (screen_width/2,screen_height/2))
            self.pause_menu_image = pygame.image.load("graphics/interface/pause_menu.png").convert_alpha()
            self.pause_menu_rect = self.pause_menu_image.get_rect(topleft = (0,0))
            self.quit_button_image = pygame.image.load("graphics/interface/quit_button.png").convert_alpha()
            self.quit_button_rect = self.quit_button_image.get_rect(topleft = (0,540))
            self.dashboard_image = pygame.image.load("graphics/interface/cockpit/cockpit_vertical2.png").convert_alpha()
            self.dashboard_image = pygame.transform.scale(self.dashboard_image, (screen_width,screen_height))
            self.dashboard_rect = self.dashboard_image.get_rect(center = centerpoint)
            self.planet_image = pygame.image.load("graphics/interface/cockpit/planet1.png").convert_alpha()
            self.planet_image = pygame.transform.scale(self.planet_image, (screen_width,screen_height))
            self.planet_rect = self.planet_image.get_rect(center = centerpoint)
            self.mission_icon_1_image = pygame.image.load("graphics/interface/icons/bionic_eye_lowres_green.png").convert_alpha()
            self.mission_icon_1_rect = self.mission_icon_1_image.get_rect(topleft = (960,540))
            self.jet_red_image = pygame.image.load("graphics/interface/icons/red_dot.png").convert_alpha()
            self.jet_red_image = pygame.transform.scale(self.jet_red_image, (10,10))
            self.jet_red_rect = self.jet_red_image.get_rect(center = (0,0))
            self.jet_blue_image = pygame.image.load("graphics/interface/icons/blue_dot.png").convert_alpha()
            self.jet_blue_image = pygame.transform.scale(self.jet_blue_image, (10,10))
            self.jet_blue_rect = self.jet_blue_image.get_rect(center = (900,900))
            self.radio_image = pygame.image.load("graphics/blank.png").convert_alpha()
            self.radio_image = pygame.transform.scale(self.radio_image, (40,40))
            self.radio_rect = self.radio_image.get_rect(center = (800,500))
            self.text_continue_button_image = pygame.image.load("graphics/interface/text_continue_75.png").convert_alpha()
            self.text_continue_button_rect = self.text_continue_button_image.get_rect(topleft = (300,200))
            self.blueprint_image = pygame.image.load("graphics/interface/blueprint_small.png").convert_alpha()
            self.blueprint_image = pygame.transform.scale(self.blueprint_image, (screen_width*0.5,screen_height*0.5))
            self.blueprint_rect = self.blueprint_image.get_rect(center = (screen_width/2,screen_height/2))
            self.desert_map = pygame.image.load("graphics/maps/small_desertplain_dark.png").convert_alpha()
            self.desert_map = pygame.transform.scale(self.desert_map, (screen_width,screen_height))
        def draw_selected_pilot_name(self):
            selected.pilot_name_image = text_font.render(f"{selected.pilot.name}",False,(111,196,169))
            selected.pilot_name_rect = selected.pilot_name_image.get_rect(center = (screen_width*0.5,screen_height*0.25))
            screen.blit(selected.pilot_name_image,(selected.pilot_name_rect))
        def draw_cockpit(self):
            screen.blit(self.planet_image,(0,0))
            screen.blit(self.dashboard_image,(0,0))
        def draw_interface_screen_front(self):
            self.large_frame_image = pygame.image.load("graphics/interface/frames/white_frame_large.png").convert_alpha()
            self.large_frame_image = pygame.transform.scale(self.large_frame_image, (screen_width*0.9,screen_height*0.9))
            self.large_frame_rect = self.large_frame_image.get_rect(center = (screen_width/2,screen_height/2)) 
            screen.blit(self.black_block_image, (self.black_block_rect))
            screen.blit(self.green_filter_image,(self.green_filter_rect))
            screen.blit(self.large_frame_image,(self.large_frame_rect))   
        def draw_pause_screen(self):
            screen.blit(self.pause_menu_image, (0,0))
            screen.blit(self.quit_button_image, (0,540))
        def draw_small_frame(self, side):
            if side == "left":
                self.frame_image = pygame.image.load("graphics/interface/frames/small_frame.png").convert_alpha()
                self.frame_image = pygame.transform.scale(self.frame_image, (screen_width*0.24,screen_height*0.82))
                self.back_image = pygame.image.load("graphics/interface/frames/small_frame_back.png").convert_alpha()
                self.back_image = pygame.transform.scale(self.back_image, (screen_width*0.24,screen_height*0.82))
                self.small_frame_rect = self.frame_image.get_rect(topleft = (self.large_frame_rect.left, screen_height*0.13))
                # screen.blit(self.back_image,(self.small_frame_rect))
                screen.blit(self.frame_image,(self.small_frame_rect))
            if side == "right":
                self.frame_image = pygame.image.load("graphics/interface/frames/small_frame_flipped.png").convert_alpha()
                self.frame_image = pygame.transform.scale(self.frame_image, (screen_width*0.24,screen_height*0.82))
                self.back_image = pygame.image.load("graphics/interface/frames/small_frame_flipped_back.png").convert_alpha()
                self.back_image = pygame.transform.scale(self.back_image, (screen_width*0.24,screen_height*0.82))
                self.small_frame_rect = self.frame_image.get_rect(topright = (self.large_frame_rect.right, screen_height*0.13))
                # screen.blit(self.back_image,(self.small_frame_rect))
                screen.blit(self.frame_image,(self.small_frame_rect))
        def draw_loadout(self):
            screen.blit(self.blueprint_image,(self.blueprint_rect))
        def draw_void(self):
            screen.fill((0,0,0))
        def draw_ui_buttons(self):
            button_group.update()
            button_group.draw(screen)
        def draw_portrait(self, pilot):
            if dialogue.speaker == nighthawk:
                portrait = pygame.image.load("graphics/pilots/nighthawk_standing.png").convert_alpha()
            elif dialogue.speaker == rose:
                portrait = pygame.image.load("graphics/pilots/rose_standing.png").convert_alpha()
            elif dialogue.speaker == lightbringer:
                 portrait = pygame.image.load("graphics/pilots/lightbringer_standing.png").convert_alpha()
            elif dialogue.speaker == deadlift:
                portrait = pygame.image.load("graphics/pilots/deadlift_standing.png").convert_alpha()
            elif dialogue.speaker == kite:
                portrait = pygame.image.load("graphics/pilots/kite_standing.png").convert_alpha()
            elif dialogue.speaker == shadowstalker:
                portrait = pygame.image.load("graphics/pilots/shadowstalker_standing.png").convert_alpha()
            else:
                portrait = pygame.image.load("graphics/pilots/unassigned_standing.png").convert_alpha()
            portrait = pygame.transform.scale(portrait,(screen_width*0.15,screen_height*0.8))
            screen.blit(portrait,(screen_width*0.75,screen_height*0.25))
        def wrap_text(self, surface, text, color, rect, font, aa=False, bkg=None):
            # rect = pygame.Rect(rect)
            y = rect.top
            lineSpacing = -2
            fontHeight = font.size("Tg")[1]
            while text:
                i = 1
                if y + fontHeight >= rect.bottom:
                    break
                while font.size(text[i])[0] < rect.width and i < len(text):
                    i += 1
                if i < len(text): 
                    i = text.rfind(" ", 0, i) + 1
                if bkg:
                    image = font.render(text[:i], 1, color, bkg)
                    image.set_colorkey(bkg)
                else:
                    image = font.render(text[:i], aa, color)
                surface.blit(image, (rect.left, y))
                y += fontHeight + lineSpacing
                text = text[i:]
            return text
        def update(self):
            self.draw_void
            screen.fill((0,0,0))
            button_group.update()
            if self.type == "inventory":
                self.draw_loadout()
                nameplates_group.update()
                nameplates_group.draw(screen)
                pilot_names_group.update()
                pilot_names_group.draw(screen)
                loadout_names_group.update()
                loadout_names_group.draw(screen)
                inventory_names_group.update()
                inventory_names_group.draw(screen)
                self.draw_selected_pilot_name()
                self.draw_interface_screen_front()
                self.draw_small_frame("left")
                self.draw_small_frame("right")
                self.draw_ui_buttons() 
            elif self.type == "map":
                island_group.update()
                island_group.draw(screen)
                mission_pointer_group.update()
                mission_pointer_group.draw(screen)
                self.draw_interface_screen_front()
                if selected.pointer_slot > 0:
                    self.draw_small_frame("right")  
            elif self.type == "combat":
                screen.blit(self.desert_map, (0,0))
                pilot_group.draw(screen)
                pilot_combat_names_group.draw(screen)
                mission_objects_group.draw(screen)
                mission_enemy_group.draw(screen)
                weapon_effects_group.update()
                weapon_effects_group.draw(screen)
                #temp
                # health_icon_group.update()
                # health_icon_group.draw(screen)
                #temp
                if active_mission == 1:
                    mission_objects_group.draw(screen)
                self.draw_interface_screen_front()
            elif self.type == "health_tracker":
                nameplates_group.update()
                nameplates_group.draw(screen)
                pilot_names_group.update()
                pilot_names_group.draw(screen)
                health_icon_group.update()
                health_icon_group.draw(screen)
                self.draw_interface_screen_front()
                self.draw_small_frame("left")
                self.draw_small_frame("right")
                self.draw_ui_buttons()
            elif overlay.type == "cockpit":
                self.draw_cockpit()
                self.draw_ui_buttons()
            elif overlay.type == "mission_brief":
                self.draw_portrait(dialogue.speaker)
                self.draw_interface_screen_front()
                self.draw_small_frame("right")
                self.draw_ui_buttons()
                dialogue.update()
                drawText(screen, dialogue.speaker.lines[dialogue.npc_line_number], (111,196,169), dialogue.npc_text_rect, text_font)
                drawText(screen, dialogue.player_lines[dialogue.player_line_number], pygame.Color("coral"), dialogue.player_text_rect, text_font)
            elif overlay.type == "pilot_select":
                self.draw_portrait()
            elif overlay.type == "none":
                x_button = False
                continue_button = False
            else:
                x_button = False
                continue_button = False
    class Mission_Manager:
        def __init__(self):
            self.current_mission = 0
            self.waypoints = []
        def create_clock(self,pilot):
            clock_icon_group.add(Icon("clock",pilot))
        def spawn_drones(self):
            drone_quantity = random.randint(2,4)
            while drone_quantity > 0:
                enemy_drone = Pilot("Enemy_Drone",1,copy.deepcopy(drone),"enemy")
                enemy_drone.orders = "objective"
                enemy_drone.battlesuit.shielded = False
                mission_enemy_group.add(enemy_drone)
                drone_quantity -= 1
        def move_train(self,train):
            global active_mission
            train.move_target = self.waypoints[train.checkpoint]
            train.move_target_distance_h = train.find_target_distance(train.move_target)
            if abs(train.move_target_distance_h) < 20:
                train.checkpoint += 1
                self.spawn_drones()
                if train.checkpoint >= len(self.waypoints):
                    train.checkpoint -= 1
                    active_mission = 2
                    overlay.type = "none"
        def update(self):
            if overlay.type == "combat":
                self.move_train(pilot_list[0])
                pilot_group.update()
                mission_objects_group.update()
                pilot_combat_names_group.update()
                mission_enemy_group.update()
                if active_mission == 1:
                    mission_objects_group.update()
        def mission_setup(self, active_mission_number):
            mission_setup = True
            if active_mission_number == 1:
                if mission_setup: #create waypoints
                    waypoint_0 = Mission_Object("waypoint_0", "radio_tower", 0, screen_width*0.1, screen_height*0.2, "friend")
                    waypoint_1 = Mission_Object("waypoint_1", "radio_tower", 1, screen_width*0.2, screen_height*0.3, "friend")
                    waypoint_2 = Mission_Object("waypoint_2", "radio_tower", 2, screen_width*0.4, screen_height*0.8, "friend")
                    waypoint_3 = Mission_Object("waypoint_3", "radio_tower", 3, screen_width*0.7, screen_height*0.5, "friend")
                    waypoint_4 = Mission_Object("waypoint_4", "radio_tower", 4, screen_width*0.9, screen_height*0.7, "friend")
                    waypoint_5 = Mission_Object("waypoint_5", "radio_tower", 5, screen_width*1.1, screen_height*0.3, "friend")
                    self.waypoints = [waypoint_0,waypoint_1,waypoint_2,waypoint_3,waypoint_4,waypoint_5]
                    for waypoint in self.waypoints: waypoint.alive = True
                if mission_setup == True: #create train
                    train_objective = Pilot("supply_train",0,copy.deepcopy(train_suit),"friend")
                    train_objective.function = "train"
                    train_objective.battlesuit.loadout.clear()
                    train_objective.pos_x = waypoint_0.pos_x
                    train_objective.pos_y = waypoint_0.pos_y
                    train_objective.checkpoint = 0
                    train_objective.move_target = self.waypoints[train_objective.checkpoint]
                    train_objective.image = pygame.image.load("graphics/interface/icons/green_blip.png").convert_alpha()
                    pilot_list[0] = train_objective
                    mission_objects_group.add(train_objective)
                    train_name = Text_Names("pilot",0)
                    pilot_combat_names_group.add(train_name)
                if mission_setup == True: #create enemies
                    mission.spawn_drones()
                    for enemy in mission_enemy_group:
                        enemy.attack_target = train_objective
                        enemy.move_target = train_objective
                        enemy.orders = "objective"
                if mission_setup == True: #prep pilots
                    rose.orders = "objective"
                    rose.active = True
                    nighthawk.orders = "objective"
                    nighthawk.active = True
                    lightbringer.active = True
                    rose.pos_x = random.randint(-screen_width*0.2+pilot_list[0].pos_x,screen_width*0.2+pilot_list[0].pos_x)
                    rose.pos_y = random.randint(-screen_height*0.2+pilot_list[0].pos_y,0)
    class Dialogue_Manager:
        def __init__(self):
            self.speaker = "speaker"
            self.scene_type = "none"
            self.portrait = blank_frame
            self.scene_index = 0
            self.npc_line_number = 0
            self.npc_text_rect = pygame.Rect((screen_width*0.1,screen_height*0.25),(screen_width*0.6,screen_height*0.5))
            self.player_line_number = 0
            self.player_lines = [" "]
            self.player_text_rect = pygame.Rect((screen_width*0.1,screen_height*0.7),(screen_width*0.6,screen_height*0.2))
            self.cooldown_max = 20
            self.cooldown = self.cooldown_max
        def load_scene_dialogue(self, scene_type, scene_index):
            #mission event 1: train under attack
            if scene_type == "mission" and scene_index == 1:
                self.speaker = nighthawk
                self.npc_line_number = 0
                self.player_line_number = 0
                nighthawk.lines = ["    Hi, you've got great timing!  Normally I'd give you the whole 'Welcome to Arcturus' bit, but someone is attacking one of our supply trains and I'm en-route to respond.  I can probably handle it, but I'd appreciate it if you could call in some backup just in case.",
                                    "Alright, showtime."]
                rose.lines = ["Nighthawk needs help? No problem, I'm on my way!"]
                lightbringer.lines = ["Understood, I've been itching for a chance to test out a new weapon."]
                shadowstalker.lines = ["Just let me know who needs killing."]
                kite.lines = ["Currently assigned on another mission. Try contacting anyway?",
                                    "Currently unavailable."]
                deadlift.lines = ["Currently assigned on another mission. Try contacting anyway?",
                                    "Currently unavailable."]
                self.player_lines = ["Understood. Let me see who's available"]
            #social event 1: free trial weapons offer
            if scene_type == "social_event" and scene_index == 1:
                benny.lines = ["Hey there, the name's Benny. I'm the local representative of Marco's Munitions LLC. I just wanted to thank you and your team for your hard work keeping us all safe.",
                                "The company lets me give out free trials of our latest products to potential buyers, so as a token of appreciation I'd like to set you up with our brand-new weapon 'The Emissary of the Void' for the next month 100% free of charge.",
                                "Fantastic! Just make sure you get that back to us in a month. Otherwise you can let us know if you'd like to make a purchase and I'll see what I can do in the way of discounts."]
            #social event 2: invitation from Falcone
            if scene_type == "social_event" and scene_index == 2:
                samuel.lines = ["Mr. Falcone has expressed an interest in speaking with you.",
                                    "He's a respectable local businessman. Pillar a' the community.",
                                    "A few words of advice; be polite, don't talk for too long, and don't ask any questions about the eye."]                    
            #social event (getting to know them)
            if scene_type == "personal" and scene_index == 1:
                nighthawk.lines = ["Good evening, Captain. It's good to meet you properly now that things have quieted down.",
                                    "Do you drink? I brought a bottle of wine as a house-warming gift, so to speak.",
                                    "So, what would you like to know?",
                                    "Before this? I actually came to this planet to be a transport operator as part of the first landing. Not glamorous, but it was important work.",
                                    "Nobody who wasn't here when it happened can really understand what it was like to live through few the first days and months of the Collapse. It's the experience of being in a tall building when the bottom few stories abruptly cease to exist. That feeling in the pit of your stomach when suddenly the floor starts to drop as gravity takes hold.",
                                    "No doubt in my mind, the biggest threat to people is the organized gangs in the city."]
                rose.lines = ["Hi there, it's nice to meet you!",
                                "So, what would you like to know?"]
        def converse(self, choice_number):
            for event in pygame.event.get():
                if self.scene_type == "mission" and self.scene_index == 1:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_1 or event.key == pygame.K_SPACE:
                            overlay.type = "pilot_select"
        def update(self):
            if self.cooldown > 0:
                self.cooldown -= 1
    class Plot_Manager():
        def __init__(self):
            self.sidequest_1 = "marko's munitions"

if startup: #load specifics 
    if startup: #create sprite groups       
        nameplates_group = pygame.sprite.Group()
        pilot_names_group = pygame.sprite.Group()
        pilot_combat_names_group = pygame.sprite.Group()
        inventory_names_group = pygame.sprite.Group()
        loadout_names_group = pygame.sprite.Group()
        island_group = pygame.sprite.Group()
        pilot_group = pygame.sprite.Group()
        weapon_effects_group = pygame.sprite.Group()
        mission_objects_group = pygame.sprite.Group()
        mission_enemy_group = pygame.sprite.Group()
        health_icon_group = pygame.sprite.Group()
        clock_icon_group = pygame.sprite.Group()
        mission_pointer_group = pygame.sprite.Group()
        button_group = pygame.sprite.Group()
    if startup: #load cores  
        fusion_core = Power_Core("fusion_core")
        null_core = Power_Core("null_core")  
    if startup: #load weapons  
        beam_cannon = Weapon("beam_cannon")
        unassigned_weapon = Weapon("unassigned_weapon")
        null_weapon = Weapon("null_weapon")
        cryo_shot = Weapon("cryo_shot")
        power_sword = Weapon("powersword")
        flame_lance = Weapon("flame_lance")
        lightning_chain = Weapon("lightning_chain")
    if startup: #load shields
        light_shield = Shield("light_shield")
    if startup: #load battlesuits
        majestic = Battlesuit("majestic")
        leviathan = Battlesuit("leviathan")
        tower = Battlesuit("tower")
        javelin = Battlesuit("javelin")
        drone = Battlesuit("drone")
        null_suit = Battlesuit("null_suit") 
        train_suit = Battlesuit("train")
    if startup: #load pilots
        unassigned_pilot = Pilot("Unassigned",0,copy.deepcopy(tower),"friend")
        nighthawk = Pilot("Nighthawk",1,copy.deepcopy(majestic),"friend")
        rose = Pilot("Rose",2,copy.deepcopy(majestic),"friend")
        lightbringer = Pilot("Lightbringer",3,copy.deepcopy(majestic),"friend")
        deadlift = Pilot("Deadlift",4,copy.deepcopy(majestic),"friend")
        kite = Pilot("Azure_Kite",5,copy.deepcopy(majestic),"friend")
        shadowstalker = Pilot("Shadowstalker",6,copy.deepcopy(majestic),"friend")
        null_pilot = Pilot(" ",-1,copy.deepcopy(null_suit),"friend")
        pilot_list = [unassigned_pilot, nighthawk, rose, lightbringer, deadlift, kite,shadowstalker]
        rose.battlesuit.loadout[1] = cryo_shot
        nighthawk.battlesuit.loadout[1] = cryo_shot
        null_pilot.pos_x = -1
        null_pilot.pos_y = -1
        tower_1 = Pilot("Tower",1,copy.deepcopy(tower),"enemy")
        benny = Pilot(" ",-1,copy.deepcopy(null_suit),"friend")
        samuel = Pilot(" ",-1,copy.deepcopy(null_suit),"friend")
    if startup: #load pilot sprites
        pilot_group.add(unassigned_pilot)
        pilot_group.add(nighthawk)
        pilot_group.add(rose)
        pilot_group.add(lightbringer)
        pilot_group.add(deadlift)
        pilot_group.add(kite)
        pilot_group.add(tower_1)
    if startup: #load buttons
        button_group.add(Button("x_button"))
        button_group.add(Button("dashboard_map"))
        # button_group.add(Button("continue_button"))
    if startup: #load resources
        inventory_list = [fusion_core, beam_cannon, light_shield, light_shield, null_weapon, null_weapon, null_weapon]
        credits_currency = 0
        scrap_metal = 0
        fuel_rods = 0
        meds = 0
        stimms = 0
    if startup: #create handlers
        selected = Selected()
        overlay = Overlay_Manager("cockpit")
        mission = Mission_Manager()
        dialogue = Dialogue_Manager()
        plot = Plot_Manager()
    if startup: #add nameplates
        nameplates_group.add(Nameplates("pilot_line_item",1))
        nameplates_group.add(Nameplates("pilot_line_item",2))
        nameplates_group.add(Nameplates("pilot_line_item",3))
        nameplates_group.add(Nameplates("pilot_line_item",4))
        nameplates_group.add(Nameplates("pilot_line_item",5))

        nameplates_group.add(Nameplates("inventory_line_item",1))
        nameplates_group.add(Nameplates("inventory_line_item",2))
        nameplates_group.add(Nameplates("inventory_line_item",3))

        nameplates_group.add(Nameplates("loadout_label", 0))
        nameplates_group.add(Nameplates("loadout_label", 1))
        nameplates_group.add(Nameplates("loadout_label", 3))
        nameplates_group.add(Nameplates("loadout_label", 2))
        nameplates_group.add(Nameplates("loadout_label", 4))
        
        nameplates_group.add(Nameplates("swap_button", 0))
    if startup: #add island maps
        island_group.add(Island("world_map",0))
        island_group.add(Island("island",1))
        island_group.add(Island("island",2))
        island_group.add(Island("island",3))
        island_group.add(Island("island",4))
        island_group.add(Island("island",5))
        island_group.add(Island("island",6))
    if startup: #add text names
        pilot_names_group.add(Text_Names("pilot",1))
        pilot_names_group.add(Text_Names("pilot",2))
        pilot_names_group.add(Text_Names("pilot",3))
        pilot_names_group.add(Text_Names("pilot",4))
        pilot_names_group.add(Text_Names("pilot",5))

        loadout_names_group.add(Text_Names("loadout",1))
        loadout_names_group.add(Text_Names("loadout",2))
        loadout_names_group.add(Text_Names("loadout",3))
        loadout_names_group.add(Text_Names("loadout",4))
        loadout_names_group.add(Text_Names("loadout",0))
        
        inventory_names_group.add(Text_Names("inventory",1))
        inventory_names_group.add(Text_Names("swap_button",0))
        
        pilot_combat_names_group.add(Text_Names("pilot",1))
        pilot_combat_names_group.add(Text_Names("pilot",2))
        pilot_combat_names_group.add(Text_Names("pilot",3))
        pilot_combat_names_group.add(Text_Names("pilot",4))
        pilot_combat_names_group.add(Text_Names("pilot",5))
    if startup: #add health icons
        for pilot in pilot_list:
            if pilot.slot_number > 0:
                health_icon_group.add(Icon("shield", pilot))
                health_icon_group.add(Icon("damaged", pilot))
                health_icon_group.add(Icon("severely_damaged", pilot))
    if startup: #add pointers
        mission_pointer_group.add(Pointer("rail", screen_width*0.6,screen_height*0.7,1))  

# selected.pilot = null_pilot

#Mission 1 setup
active_mission_number = 1
mission.mission_setup(1)

while True: #game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i: #toggle inventory
                if overlay.type == "inventory":
                    overlay.type = "cockpit"
                else:
                    overlay.type = "inventory"
                    x_button = True
                    continue_button = False
            if event.key == pygame.K_m: #toggle map
                if overlay.type == "map":
                    overlay.type = "cockpit"
                    x_button = False
                    continue_button = False
                else:
                    overlay.type = "map"
                    x_button = True
            if event.key == pygame.K_c: #go to cockpit
                overlay.type = "cockpit"
            if event.key == pygame.K_b: #toggle combat
                if overlay.type == "combat":
                    overlay.type = "cockpit"
                    x_button = False
                    continue_button = False
                else:
                    overlay.type = "combat"
                    x_button = True
            if event.key == pygame.K_p: #toggle health tracker
                if overlay.type == "health_tracker":
                    overlay.type = "cockpit"
                    x_button = False
                    continue_button = False
                else:
                    overlay.type = "health_tracker"
                    x_button = True
    mission.update()
    overlay.update()
        
    # fps_text = update_fps()
    # screen.blit(fps_text, (centerpoint)) #display fps
    pygame.display.update()
    clock.tick(60)
import pygame
import random
from sys import exit
import os
import copy
from math import atan2, degrees, pi


# none = "none"
BLACK = (0,0,0)
continue_button = False
debug_mode = False
resources = "json data file to be imported"

#game.paused = False

#temp
class Map_Center:
    def __init__(self):
        self.pos_x = screen_width*0.5
        self.pos_y = screen_height*0.5
#temp

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

def find_distance(origin, target):
    try:
        if target.alive == True:
            distance_x = target.pos_x - origin.pos_x
            distance_y = target.pos_y - origin.pos_y
            distance_h = (distance_x**2 + distance_y**2)**(1/2)
        #make sure they're no longer the closest target if they aren't alive
        else: distance_h = screen_width*2
        return distance_h
    except: 
        if debug_mode == True: print("Error: unable to find distance between", origin.name, "and", target.name)
        else: pass

def find_angle(origin, target):
            
            # if type == "attack": target = self.attack_target
            # elif type == "move": target = self.move_target
            # elif debug_mode == True: print("Error: invalid target for find_angle")
            # else: pass
                
            distance_x = target.pos_x - origin.pos_x
            distance_y = target.pos_y - origin.pos_y
            
            rads = atan2(-distance_y, distance_x)
            rads %= 2*pi
            angle = degrees(rads)
                
            return angle

if startup: #load notes
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
explosion_sheet_1 = pygame.image.load("graphics/effects/explosion_sprite_1.png").convert_alpha()
explosion_sheet_2 = pygame.image.load("graphics/effects/explosion_sprite_2.png").convert_alpha()
explosion_sheet_3 = pygame.image.load("graphics/effects/explosion_sprite_3.png").convert_alpha()
explosion_sheet_4 = pygame.image.load("graphics/effects/explosion_sprite_4.png").convert_alpha()
teleport_sheet = pygame.image.load("graphics/effects/teleport_explosion.png").convert_alpha()

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
                self.cooldown_max = 200
                self.form = "beam"
                self.damage_type = "thermal"
                self.apply_status = "overheated"
            if type == "cryo_shot":
                self.name = "Cryo Shot"
                self.accuracy = 2
                self.distance = 100
                self.cooldown_max = 200
                self.form = "beam"
                self.damage_type = "cold"
                self.apply_status = "frozen"
            if type == "powersword":
                self.name = "Powersword"
                self.accuracy = 1
                self.distance = 10
                self.cooldown_max = 200
                self.damage_type = "pierce"
                self.apply_status = "knockback"
            if type == "flame_lance":
                self.name = "Flame Lance"
                self.accuracy = 4
                self.distance = 60
                self.cooldown_max = 200
                self.form = "burst"
                self.damage_type = "thermal"
                self.apply_status = "knockback" + "overheated"
            if type == "lightning_chain":
                self.name = "Lightning Chain"
                self.accuracy = 1
                self.distance = 30
                self.cooldown_max = 200
                self.damage = "shock"
                self.apply_status = "disrupted" + "tethered"
            if type == "null_weapon":
                self.name = " "            
            
            #set cooldown to maximum
            try: self.cooldown = self.cooldown_max
            except: 
                if debug_mode == True: print("Error: unable to set cooldown to max for", self.name)
                else: pass
            
    class Visual_Effect(pygame.sprite.Sprite):
        def __init__(self, form, damage_type, origin, target):
            super().__init__()
            self.name = "undefined"
            self.form = form
            self.damage_type = damage_type
            self.origin = origin
            self.target = target
            self.countdown_max = 20
            self.countdown = 1
            
            self.frames = [blank_frame,blank_frame]
            self.animation_index = 1
            self.image = blank_frame
            self.length = self.find_distance(self.origin, self.target)*2.1 #doubled because graphic has invisible bottom half so its pivot-point is correct
            self.angle = self.find_angle(origin, target)
            
            #red laser
            if self.form == "beam" and self.damage_type == "thermal":
                self.name = "thermal beam"
                self.frame_1 = pygame.image.load("graphics/effects/laserbeam_thin_half.png").convert_alpha()
                self.frame_0 = blank_frame
                self.frames = [self.frame_0,self.frame_1]
                self.image = self.frames[self.animation_index]
                self.width = 30
                self.image = pygame.transform.scale(self.image,(self.width, self.length))
                self.countdown_max = 20
            
            #blue laser
            if self.form == "beam" and self.damage_type == "cold":
                self.name = "cryo beam"
                self.frame_0 = blank_frame
                self.frame_1 = pygame.image.load("graphics/effects/ice_laser.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1]
                self.image = self.frames[self.animation_index]
                self.width = 20
                self.image = pygame.transform.scale(self.image,(self.width, self.length))
                self.countdown_max = 20
            
            #flame thrower
            if self.form == "burst" and self.damage_type == "thermal":
                self.name = "flamer"
                self.frame_0 = blank_frame
                self.frame_1 = pygame.image.load("graphics/effects/fire1.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/effects/fire2.png").convert_alpha()
                self.frame_3 = pygame.image.load("graphics/effects/fire3.png").convert_alpha()
                self.frame_4 = pygame.image.load("graphics/effects/fire4.png").convert_alpha()
                self.frame_5 = pygame.image.load("graphics/effects/fire5.png").convert_alpha()
                self.frame_6 = pygame.image.load("graphics/effects/fire6.png").convert_alpha()
                self.frame_7 = pygame.image.load("graphics/effects/fire7.png").convert_alpha()
                self.frame_8 = pygame.image.load("graphics/effects/fire8.png").convert_alpha()
                self.frames = [self.frame_0, self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5, self.frame_6, self.frame_7, self.frame_8]
                self.countdown_max = 60
                self.image = self.frames[self.animation_index]
            
            #explosion
            if self.form == "explosion":
                self.name = "explosion"
                explosion_sheets = [explosion_sheet_1,explosion_sheet_2,explosion_sheet_3,explosion_sheet_4]
                self.animation_index = 0
                # self.frames = explosion_frames
                # self.image = blank_frame
                self.countdown_max = 64
                self.sheet = random.choice(explosion_sheets)
                self.sheet_column = 0
                self.sheet_row = 0
            
            #teleport
            if self.form == "teleport":
                self.name = "teleport"
                teleport_sheet = pygame.image.load("graphics/effects/teleport_explosion.png").convert_alpha()
                self.animation_index = 0
                # self.frames = explosion_frames
                # self.image = blank_frame
                self.countdown_max = 64
                self.sheet = teleport_sheet
                self.sheet_column = 0
                self.sheet_row = 0
            
            self.countdown = self.countdown_max
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect(center = (self.origin.pos_x, self.origin.pos_y))
        
        def draw_explosion(self,sheet,height,column,row):
            screen.blit(sheet, (self.origin.pos_x-height*0.5, self.origin.pos_y-height*0.5),(height*column, height*row, height, height))
            
        def draw_teleport(self, sheet, height, column, row):
            screen.blit(sheet, (self.origin.pos_x-height*0.5, self.origin.pos_y-height*0.5),(height*column, height*row, height, height))
        
        def find_distance(self, origin, target):
            distance_x = target.pos_x - origin.pos_x
            distance_y = target.pos_y - origin.pos_y
            distance_h = (distance_x**2 + distance_y**2)**(1/2)
            return distance_h
        
        def find_angle(self, origin, target):
                           
            distance_x = target.pos_x - origin.pos_x
            distance_y = target.pos_y - origin.pos_y
            
            rads = atan2(-distance_y, distance_x)
            rads %= 2*pi
            angle = degrees(rads) - 90
                
            return angle
        
        def update(self):
            
            if debug_mode == True:
                try: print(self.name, self.animation_index, self.length, self.width)
                except: print(self.name, "has no width")
            
            if self.length > screen_width: 
                if debug_mode == True: print("excessive length", self.origin.name, self.target.name)
                self.length = screen_width
            
            #update countdown
            if self.countdown <= 0:
                if debug_mode == True: print("End effect:", self.name)
                self.kill()
            else: self.countdown -= 1
            
            #explosion
            if self.form == "explosion":
                self.sheet_column += 1
                self.image = blank_frame
                if self.sheet_column == 8:
                    self.sheet_column = 0
                    self.sheet_row += 1
                self.draw_explosion(self.sheet, 256, self.sheet_column, self.sheet_row)
                
            #teleport
            if self.form == "teleport":
                self.sheet_column += 1
                self.image = blank_frame
                if self.sheet_column == 8:
                    self.sheet_column = 0
                    self.sheet_row += 1
                self.draw_teleport(self.sheet, 256, self.sheet_column, self.sheet_row)
            
            #red beam
            if self.form == "beam" and self.damage_type == "thermal":
                #update length and angle
                self.length = self.find_distance(self.origin, self.target)*2.1
                self.angle = self.find_angle(self.origin, self.target)
                #update image
                self.image = self.frames[self.animation_index]
                self.image = pygame.transform.scale(self.frame_1,(self.width, self.length))
            
            #blue beam
            if self.form == "beam" and self.damage_type == "cold":
                #update length and angle
                self.length = self.find_distance(self.origin, self.target)*2.1
                self.angle = self.find_angle(self.origin, self.target)
                #update image
                self.image = self.frames[self.animation_index]
                self.image = pygame.transform.scale(self.frame_1,(self.width, self.length))
            
            #flamer loop
            if self.form == "burst" and self.damage_type == "thermal":
                self.animation_index += 0.3
                if self.animation_index > 8:
                    self.animation_index = 1
                self.image = self.frames[int(self.animation_index)]
            
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect(center = (self.origin.pos_x, self.origin.pos_y))                    
    
    class Shield:
        def __init__(self, type):
            self.function = "shield"
            self.type = type
            if type == "light_shield":
                self.name = "Light Shield"
                self.cooldown_max = 2000
                self.cooldown = self.cooldown_max
                self.charged = True  
    
    class Battlesuit(pygame.sprite.Sprite):
        def __init__(self, type):
            super().__init__()
            self.type = type
            self.loadout = []
            self.mobility = 1
            self.shielded = True
            self.damaged = False
            self.severely_damaged = False
            self.pos_x = 0
            self.pos_y = 0
            if type == "majestic":
                self.name = "Majestic"
                self.mobility = 1
                self.refresh = 4
                self.size = 1
                self.loadout = [fusion_core,beam_cannon,beam_cannon,light_shield,light_shield]
            if type == "leviathan":
                self.name = "Leviathan"
                self.mobility = 0.5
                self.refresh = 4
                self.power_core = "dirty_fission_core"
                self.size = 2
                self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
            if type == "tower":
                self.name = "Tower"
                self.mobility = 0
                self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
            if type == "javelin":
                self.name = "Javelin"
                self.mobility = 2
                self.refresh = 3
                self.power_core = fusion_core
                self.size = 0.5
                self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
            if type == "drone":
                self.name = "Drone"
                self.mobility = 2
                self.refresh = 1
                self.power_core = fusion_core
                self.size = 0.3
                self.loadout = [fusion_core, beam_cannon, unassigned_weapon, unassigned_weapon, unassigned_weapon]
            if type == "train":
                self.name = "Train"
                self.mobility = 0.5
                self.refresh = 4
                self.power_core = fusion_core
                self.size = 2
                self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
            if type == "null_suit":
                self.name = " "
                self.loadout = [null_core,null_weapon,null_weapon,null_weapon,null_weapon]
        def update(self):
            self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
            self.invuln_timer -= 1
            if self.invuln_timer > 0:
                self.invuln_timer = 0
    
    class Mission_Object(pygame.sprite.Sprite):
        def __init__(self, type, slot_number, pos_x, pos_y, team):
            super().__init__()
            self.type = type
            self.slot_number = slot_number
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.team = team
            self.damaged = False
            self.animation_index = 0
            self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
            self.frame_0 = pygame.transform.scale(self.frame_0, (screen_width*0.05,screen_height*0.05))
            self.is_objective = False
            
            if self.type == "waypoint":
                self.name = "waypoint"
                self.frame_1 = pygame.image.load("graphics/interface/icons/radio.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1]
                # for frame in self.frames:
                    # frame = pygame.transform.scale(frame, (10,10))
                self.function = "waypoint"
                self.countdown_max = -1
            
            if self.type == "supply_crate":
                self.name = "supply_crate"
                self.width = screen_width*0.03
                self.height = screen_width*0.03
                self.frame_1 = pygame.image.load("graphics/interface/icons/box_closed.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (self.width, self.height))
                self.frame_2 = pygame.image.load("graphics/interface/icons/box_open.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2, (self.width, self.height))
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
                self.carried = False
                self.carrier = "none"
                self.progress_track = 0
                self.is_objective = True
            
            if self.type == "train":
                self.name = "train"
                pass
                
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        
        def update(self):
            if self.type == "supply_crate":
                if 0 < self.progress_track < 100: print(self.progress_track)
                #create clock visual when progress starts ticking up
                if self.progress_track == 1: mission.spawn_clock(self)
                
                #update image and position
                if self.carried: 
                    self.animation_index = 2
                    self.pos_x = self.carrier.pos_x
                    self.pos_y = self.carrier.pos_y + screen_height*0.05
                else: self.animation_index = 1
                
                
                
            self.image = self.frames[self.animation_index]
            #offset rect from Pilot
            self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y - screen_height*0.05))
    
    class Terrain_Piece(pygame.sprite.Sprite):
        def __init__(self, type, pos_x, pos_y, width, height):
            super().__init__()
            
            self.type = type
            self.pos_x = pos_x
            self.pos_y = pos_y
            self.width = width
            self.height = height
            self.animation_index = 1
            self.repel_force = 4
            
            self.frame_0 = pygame.image.load("graphics/blank.png")
            
            if self.type == "rock":
                self.frame_1 = pygame.image.load("graphics/terrain/rock1.png")
                self.frames = [self.frame_0, self.frame_1]
            
            self.image = self.frames[self.animation_index]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.mask.get_rect(center = (self.pos_x,self.pos_y))
            
        def repel(self):
            for pilot in mission.pilots:
                if self.rect.collidepoint((pilot.pos_x, pilot.pos_y)):
                    #keep Pilot's momentum but direct away from the terrain object
                    if pilot.pos_x < self.pos_x: pilot.momentum_x = abs(pilot.momentum_x)
                    else: pilot.momentum_x = abs(pilot.momentum_x) * -1    
    
    class Pilot(pygame.sprite.Sprite):
        def __init__(self, name, slot_number, battlesuit, team):
            super().__init__()
            self.name = name
            self.team = team
            self.function = "Pilot"
            self.lines = []
            self.rank = 1
            self.type = "Pilot"
            self.slot_number = slot_number
            self.active = False
            self.dispatching = False
            self.on_mission = False
            self.pos_x = 0
            self.pos_y = 0
            
            # combat settings
            self.checkpoint = 0
            self.injured = False
            self.alive = True
            self.ttl = -1
            self.orders = "objective"
            
            self.pos_x = random.randint(-screen_width*0.5,screen_width*0.5)
            self.pos_y = random.randint(-screen_height*0.5,0)
            
            self.attack_target = self
            self.move_target = self
            
            self.momentum_x = 0
            self.momentum_y = 0
            
            self.attack_angle = 0
            self.move_angle = 0
            self.attack_distance = 0
            self.move_distance = 0
            
            self.battlesuit = battlesuit
            self.mobility = self.battlesuit.mobility
            self.carrying = "none"
            
            self.animation_index = 1
            self.frame_0 = blank_frame
            self.frame_0 = pygame.transform.scale(self.frame_0, (10,10))
            self.invuln_timer = 0
            if self.team == "vanguard":
                self.frame_1 = pygame.image.load("graphics/interface/icons/blue_dot.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/blue_dot_shielded.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
            if self.team == "enemy":
                self.frame_1 = pygame.image.load("graphics/interface/icons/red_dot.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/red_dot_shielded.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
            # if self.name == "Tower":
                # self.pos_x = screen_width*2
                # self.pos_y = screen_height*2
            self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        
        def find_target(self, type):
            #placeholder for train functioning as Pilot
            if self.type == "train" and type == "move":
                self.move_target = mission.waypoints[self.checkpoint]
                
            elif self.type == "Pilot":
                #find attack target
                if type == "attack":
                    
                    #determine target group
                    try:
                        if self.team == "vanguard":
                            target_group = mission.enemies
                        elif self.team == "enemy":
                            target_group = mission.pilots
                    except: 
                        if debug_mode == True: print("Error: unable to assign target group")
                        else: pass
                    
                    #avoid targeting/attacking self/allies
                    if self.attack_target == self: self.attack_distance = screen_width
                    
                    #find a target from the list of enemies                    
                    for enemy in target_group:
                        if enemy.alive == True and enemy.battlesuit.severely_damaged == False and enemy.injured == False:
                            enemy_distance = self.find_distance(self, enemy)
                            if enemy_distance < self.attack_distance:
                                # if debug_mode == True: print("Pilot ", self.name, "has new target:", enemy.name) 
                                self.attack_target = enemy
                                self.attack_distance = enemy_distance
                    
                #find move target
                if type == "move":
                    #make sure targeting yourself is never the closest target
                    if self.move_target == self: self.move_distance = screen_width*2
                    
                    #determine target group
                    try:
                        if self.orders == "aggressive":
                            if self.team == "vanguard":
                                target_group = mission.enemies
                            elif self.team == "enemy":
                                target_group = mission.pilots
                        elif self.orders == "objective":
                            target_group = mission.objectives
                    except: 
                        if debug_mode == True: print("Error: unable to assign target group")
                        else: pass
                    
                    #chasing the attack target
                    if self.orders == "aggressive":
                        #change orders to objective if there are no enemies to attack
                        if len(target_group) <= 0: self.orders = "objective"
                        
                        #set move target to be attack target
                        if self.attack_target.battlesuit.severely_damaged == False:
                            try: self.move_target = self.attack_target
                            except: 
                                if debug_mode == True: print("Error: unable to set attack target as move target")
                                else: pass
                        #stop being aggressive once they're severely wounded
                        else: self.orders = "objective"
                    
                    #move towards the closest objective
                    elif self.orders == "objective":
                        target_group = mission.objectives
                        for objective in target_group:
                            target_distance = self.find_distance(self, objective)
                            try:
                                if objective.carried == True and self.carrying != objective: target_distance = screen_width
                                if target_distance < self.move_distance and objective.carried == False:
                                    self.move_target = objective
                                    self.move_distance = target_distance
                                    if debug_mode == True: print(self.name, "has new target:", self.move_target.name, self.move_distance)
                            except: pass
                    
                    #placeholder for evac orders
                    elif self.orders == "evac": pass
                    
                    #print error for invalid errors
                    else: 
                        if debug_mode == True: print("Error: invalid orders", self.name, self.orders)
                        else: pass
                                
        #find the distance between the Pilot and their target, returned as a value
        def find_distance(self, origin, target):
            distance_x = target.pos_x - origin.pos_x
            distance_y = target.pos_y - origin.pos_y
            distance_h = (distance_x**2 + distance_y**2)**(1/2)
            return distance_h
        
        #picking up or interacting with mission objects
        def mission_object_interaction(self):
            objective = self.move_target
            
            #pick up supply crate object
            if self.orders == "objective" and objective.type == "supply_crate":
                
                #slowdown stage 1
                if objective.carried == False and self.carrying == "none" and abs(self.move_distance) < screen_width*0.06:
                    #slow down momentum to stay in range of the objective instead of flying past
                    if abs(self.momentum_x) > 6: self.momentum_x *= 0.9
                    if abs(self.momentum_y) > 6: self.momentum_y *= 0.9  
                
                #check range, whether Pilot is already carrying something, and whether the object is being held by someone already
                if objective.carried == False and self.carrying == "none" and abs(self.move_distance) < screen_width*0.02:
                    #slow down stage 2 to stay in range of the objective instead of flying past
                    if abs(self.momentum_x) > 4: self.momentum_x *= 0.9
                    if abs(self.momentum_y) > 4: self.momentum_y *= 0.9  
                    
                    #tick up the progress track by 1% or pick it up if progress is full
                    if objective.progress_track < 100: objective.progress_track += 1
                    else:
                        objective.carried = True
                        objective.carrier = self
                        self.carrying = objective
                        
                        #carry the supply crate away from battle
                        self.orders = "evac"
                        
        #probably no longer need to keep the distances as variables for the Pilot, but currently that's how the data is managed
        # def targeting_distance(self,type):
            # if type == "attack":
                # distance_x_ = self.attack_target.pos_x - self.pos_x
                # distance_y = self.attack_target.pos_y - self.pos_y
                # self.attack_distance = (self.attack_target_distance_x**2 + self.attack_target_distance_y**2)**(1/2)
            # if type == "move":
                # self.move_target_distance_x = self.move_target.pos_x - self.pos_x
                # self.move_target_distance_y = self.move_target.pos_y - self.pos_y
                # self.move_distance = (self.move_target_distance_x**2 + self.move_target_distance_y**2)**(1/2)
        
        def find_angle(self, origin, target):
            
            # if type == "attack": target = self.attack_target
            # elif type == "move": target = self.move_target
            # else: 
                # if debug_mode == True: print("Error: invalid target for find_angle")
                # else: pass
                
            distance_x = target.pos_x - origin.pos_x
            distance_y = target.pos_y - origin.pos_y
            
            rads = atan2(-distance_y, distance_x)
            rads %= 2*pi
            angle = degrees(rads)
                
            return angle
                
        def maintain_shields(self):
            #update visual if Pilot is alive
            if self.alive and self.battlesuit.shielded: self.animation_index = 2
            elif self.alive and self.battlesuit.shielded == False: self.animation_index = 1
            self.image = self.frames[self.animation_index]
            
            for item in self.battlesuit.loadout:
                if item.function == "shield":
                    
                    if item.cooldown > 0:
                            item.charged = False
                            item.cooldown -= 1
                    else: item.charged = True
                    
                    #deplete shield item to restore battlesuit shields
                    if self.battlesuit.shielded == False and item.charged == True:
                        self.battlesuit.shielded = True
                        item.charged = False
                        item.cooldown = item.cooldown_max
        
        def attack(self, target):
            target = self.attack_target
            
            #don't shoot allies
            if target.team == self.team and target.name != "supply_train" and target.name != "Enemy_Drone": print("Error: target", target.name, "is on the same team as", self.name)
            
            #don't execute targets
            elif target.injured == True: 
                # if debug_mode == True: print("Killing shot not fired")
                # else: pass
                pass
            
            else:
                #find distance
                target_distance = self.find_distance(self, self.attack_target) #alternatively self.attack_distance
                    
                for item in self.battlesuit.loadout:
                    #advance cooldown
                    if item.cooldown > 0:
                        item.cooldown -= 1
                    
                    #confirm item is a weapon and target is not invulerable
                    elif item.function == "weapon" and self.attack_target.invuln_timer == 0:
                        #confirm target is in range
                        if target_distance < item.distance:
                            #reset cooldown and target invuln timer
                            item.cooldown = item.cooldown_max
                            self.attack_target.invuln_timer = 20
                            
                            #roll to hit
                            hit_roll = roll_1d6() + item.accuracy
                            if hit_roll >= 3 + target.mobility:
                                #deal damage
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
                            else: pass #placeholder, will add aim variation for missed targets later
                            
                            #create visual effect
                            group.weapon_effects.add(Visual_Effect(item.form, item.damage_type, self, target))
                            if debug_mode == True: print("Created weapon effect:", item.form, item.damage_type, self.name, target.name)
                            
        def maneuver(self):
            #retreat if severely damaged
            if self.battlesuit.severely_damaged == True: 
                self.orders = "evac"
            
            #keep increasing momentum to leave map for evac
            if self.orders == "evac":
                if self.name != "supply_train" and self.name != "Tower":
                    self.momentum_x *= 1.1
                    self.momentum_y *= 1.1
            
            #follow target
            if self.move_target.pos_x >= self.pos_x: self.momentum_x += 0.01*10 #accelerate east
            else: self.momentum_x -= 0.01*10 #accelerate west
            if self.move_target.pos_y >= self.pos_y: self.momentum_y += 0.001*50 #accelerate south
            else: self.momentum_y -= 0.01*10 #accelerate north
            
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
            
            #update position
            self.pos_y = (self.pos_y + self.momentum_y*0.1*self.mobility)
            self.pos_x = (self.pos_x + self.momentum_x*0.1*self.mobility)
        
        def explode(self):
            #start explosion graphic
            if self.ttl == -1: 
                self.ttl = 64
                group.weapon_effects.add(Visual_Effect("explosion", "thermal", self, self))
            
            #reduce remaining time to live
            self.ttl -= 1
            
            #finish exploding
            if self.ttl == 0:
                self.kill()
        
        def teleport(self):
            self.pos_x = random.randint(screen_width*0.2,screen_width*0.8)
            self.pos_y = random.randint(screen_height*0.2, screen_height*0.8)
            #set entry velocity
            momentum_x = random.randint(5,10)
            if self.pos_x < screen_width*0.5: self.momentum_x = momentum_x
            else: self.momentum_x = -1*momentum_x
            
            momentum_y = random.randint(2,10)
            if self.pos_y < screen_width*0.5: self.momentum_y = momentum_y
            else: self.momentum_y = -1*momentum_y
            angle = find_angle(self, map_center)
            group.weapon_effects.add(Visual_Effect("teleport", "thermal", self, self))
        
        def update(self):                        
            #temp invulnerability
            if self.invuln_timer > 0:
                self.invuln_timer -= 1
            
            #find targets for move and attack
            self.find_target("move")
            self.move_distance = self.find_distance(self, self.move_target)
            self.move_angle = self.find_angle(self, self.move_target)
            
            self.find_target("attack")
            self.attack_distance = self.find_distance(self, self.attack_target)
            self.attack_angle = self.find_angle(self, self.attack_target)
            
            #drones die early
            if self.battlesuit.damaged == True and self.battlesuit.type == "drone":
                self.battlesuit.severely_damaged = True
                self.injured = True
                self.alive = False
            
            #self destruct
            if self.alive == False: 
                self.explode()
                self.animation_index = 0
                self.image = self.frames[self.animation_index]
                self.momentum_x = self.momentum_x*0.8
                self.momentum_y = self.momentum_y*0.8
            
            #prevent train from dying
            if self.name == "supply_train":
                self.alive = True
            
            self.maintain_shields()
            self.attack(self.attack_target)
            self.mission_object_interaction()
            self.maneuver()
            
            #update rect
            self.image = pygame.transform.scale(self.image, (10,10))
            self.rect = self.image.get_rect(center = (int(self.pos_x),int(self.pos_y)))
            
            #avoid bunching up
            for pilot in mission.pilots: 
                if pilot.name != self.name:
                    if abs(pilot.pos_x - self.pos_x) < 0.1:
                        self.momentum_x = self.momentum_x * 1.1
                        
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
    
    class Short_Text(pygame.sprite.Sprite):
        def __init__(self, type, slot_number):
            super().__init__()
            self.slot_number = slot_number
            self.type = type
            self.active = False
            self.animation_index = 0
            
            if type == "loadout":
                self.name = " "
                self.image = text_font_small.render(f"{self.name}",False,(0,0,0))
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                if self.slot_number == 0: 
                    self.pos_x = screen_width*0.6
                    self.pos_y = screen_height*0.5
                if self.slot_number == 1: 
                    self.pos_x = screen_width*0.32
                    self.pos_y = screen_height*0.33
                if self.slot_number == 2: 
                    self.pos_x = screen_width*0.6
                    self.pos_y = screen_height*0.33
                if self.slot_number == 3: 
                    self.pos_x = screen_width*0.32
                    self.pos_y = screen_height*0.68
                if self.slot_number == 4:
                    self.pos_x = screen_width*0.6
                    self.pos_y = screen_height*0.68             
            if type == "inventory":
                self.name = group.inventory[self.slot_number].name
                self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.pos_x = screen_width*0.75
                self.pos_y = screen_height*0.2 + self.slot_number*self.height
            if type == "Pilot":
                self.pilot = group.pilot_roster[self.slot_number]
                self.name = self.pilot.name
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.pos_x = screen_width*0.1
                self.pos_y = screen_height*0.2 + self.slot_number*self.height
                self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
            if type == "stats":
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.pos_x = screen_width*0.35
                self.pos_y = screen_height*0.3 + self.slot_number*self.height
                if self.slot_number == 1:
                    self.name = "battlesuit_type"
                    self.image = text_font_small.render(f"Battlesuit: {selected.pilot.battlesuit.name}",False,(111,196,169))
                elif self.slot_number == 2:
                    self.name = "power_source"
                    self.image = text_font_small.render(f"Power Source: {selected.pilot.battlesuit.loadout[0].name}",False,(111,196,169))
                elif self.slot_number == 3:
                    self.name = "damaged"
                    if selected.pilot.battlesuit.damaged == True and selected.pilot.battlesuit.severely_damaged == False:
                        self.image = text_font_small.render(f"Moderately Damaged",False,(111,196,169))
                    elif selected.pilot.battlesuit.damaged == True and selected.pilot.battlesuit.severely_damaged == True:
                        self.image = text_font_small.render(f"Severely Damaged",False,(111,196,169))
                    else: 
                        self.image = text_font_small.render(f"Fully Operational",False,(111,196,169))
                elif self.slot_number == 4:
                    self.name = "weapons"
                    self.image = text_font_small.render(f"Weapons: {selected.pilot.battlesuit.loadout[1].name},  {selected.pilot.battlesuit.loadout[2].name}",False,(111,196,169))
                elif self.slot_number == 5:
                    self.name = "shields"
                    self.image = text_font_small.render(f"Shields: {selected.pilot.battlesuit.loadout[3].name},  {selected.pilot.battlesuit.loadout[4].name}",False,(111,196,169))
                else:
                    self.name = " "
                    self.image = blank_frame
            if type == "train":
                self.pilot = mission.train_roster[self.slot_number]
                self.name = self.pilot.name
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.pos_x = screen_width*0.2
                self.pos_y = screen_height*0.2 + self.slot_number*self.height
                self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
            if type == "swap_button":
                self.name = "swap_button"
                self.pos_x = screen_width*0.45
                self.pos_y = screen_height*0.82
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.frame_0 = self.image = text_font.render(" ",False,(111,196,169))
                self.frame_1 = self.image = text_font.render("Swap Item",False,(0,0,0))
                self.animation_index = 0
                self.frames = [self.frame_0,self.frame_1]
                self.image = self.frames[self.animation_index]
            if type == "dispatch_button":
                self.name = "dispatch_button"
                self.pos_x = screen_width*0.45
                self.pos_y = screen_height*0.82
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.frame_0 = self.image = text_font.render(" ",False,(111,196,169))
                self.frame_1 = self.image = text_font.render("Assign",False,(0,0,0))
                self.frame_2 = self.image = text_font.render("Unassign",False,(0,0,0))
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.image = self.frames[self.animation_index]
            if type == "continue_button":
                self.name = "continue_button"
                self.pos_x = screen_width*0.1
                self.pos_y = screen_height*0.13
                self.width = screen_width*0.2
                self.height = screen_height*0.05
                self.frame_0 = self.image = text_font.render(" ",False,(111,196,169))
                self.frame_1 = self.image = text_font.render("Continue",False,(0,0,0))
                self.frames = [self.frame_0, self.frame_1]
                self.image = self.frames[self.animation_index]
            
            self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height) 
        
        def update(self):
                
            if self.type == "loadout":
                if overlay.type == "inventory":
                    self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
                    self.image = text_font_small.render(f"{self.name}",False,(0,0,0))
                
            elif self.type == "inventory":
                if overlay.type == "inventory":
                    self.name = group.inventory[self.slot_number].name
                    self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
                
            elif self.type == "Pilot":
                if overlay.type == "inventory":
                    self.image = text_font_small.render(f"{self.name}",False,(111,196,169))
                    self.rect = pygame.Rect(self.pos_x, self.pos_y,self.width,self.height) 
                elif overlay.type == "combat":
                    self.image = text_font_micro.render(f"{self.name}",False,(111,196,169))
                    self.rect = self.image.get_rect(center = (self.pilot.pos_x,self.pilot.pos_y+11))
                    if self.type == "train":
                        self.pilot = mission.train_roster[self.slot_number]
                
            elif self.type == "swap_button":
                if overlay.type == "inventory":
                    if selected.inventory_slot > -1:
                        self.animation_index = 1
                    else: self.animation_index = 0
                    self.image = self.frames[self.animation_index]
                    
            elif self.type == "dispatch_button":
                if overlay.type == "pilot_select":
                    if selected.pilot.dispatching == False and selected.pilot.on_mission == False: self.animation_index = 1
                    elif selected.pilot.dispatching == True and selected.pilot.on_mission == False: self.animation_index = 2
                    else: self.animation_index = 0
                    self.image = self.frames[self.animation_index]
            
            elif self.type == "continue_button":
                #screens where continue button should always be hidden
                if overlay.type == "combat" or overlay.type == "cockpit" or overlay.type == "map" : 
                    self.active = False
                    self.animation_index = 0
                    self.image = self.frames[self.animation_index]
                
                elif overlay.type == "pilot_select":
                    self.active = False
                    for pilot in group.pilot_roster:
                        if pilot.dispatching: self.active = True
                    if self.active == True: self.animation_index = 1
                    else: self.animation_index = 0
                    self.image = self.frames[self.animation_index]
            
            elif self.type == "stats":
                if overlay.type == "pilot_select":
                    if self.slot_number == 1: self.image = text_font_small.render(f"Battlesuit: {selected.pilot.battlesuit.name}",False,(111,196,169))
                    elif self.slot_number == 2: self.image = text_font_small.render(f"Power Source: {selected.pilot.battlesuit.loadout[0].name}",False,(111,196,169))
                    elif self.slot_number == 3:
                        if selected.pilot.battlesuit.damaged == True and selected.pilot.battlesuit.severely_damaged == False:
                            self.image = text_font_small.render(f"Moderately Damaged",False,(111,196,169))
                        elif selected.pilot.battlesuit.damaged == True and selected.pilot.battlesuit.severely_damaged == True:
                            self.image = text_font_small.render(f"Severely Damaged",False,(111,196,169))
                        else:
                            self.image = text_font_small.render(f"Fully Operational",False,(111,196,169))
                    elif self.slot_number == 4: self.image = text_font_small.render(f"Weapons: {selected.pilot.battlesuit.loadout[1].name},  {selected.pilot.battlesuit.loadout[2].name}",False,(111,196,169))
                    elif self.slot_number == 5: self.image = text_font_small.render(f"Shields: {selected.pilot.battlesuit.loadout[3].name},  {selected.pilot.battlesuit.loadout[4].name}",False,(111,196,169))
                    else: self.image = blank_frame
                
            elif self.type == "train":
                if overlay.type == "combat":
                    self.image = text_font_micro.render(f"{self.name}",False,(111,196,169))
                    self.rect = self.image.get_rect(center = (self.pilot.pos_x,self.pilot.pos_y+11))
                    if self.type == "train":
                        try: self.pilot = mission.train_roster[self.slot_number]
                        except:
                            if debug_mode == True: print("no trains in roster")
                            self.image = text_font_micro.render(" ",False,(111,196,169))
    
    class Nameplates(pygame.sprite.Sprite):
        def __init__(self,type,slot_number):
            super().__init__()
            self.type = type
            self.slot_number = slot_number
            self.animation_index = 1
            self.selected = False
            self.cooldown = 0
            self.frame_0 = blank_frame
            self.frame_3 = blank_frame
            if type == "inventory_line_item":
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.pos_x = screen_width*0.83
                self.pos_y = screen_height*0.2 + self.slot_number*self.height
                self.frame_1 = pygame.image.load("graphics/interface/labels/interface_panel_name.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/labels/interface_panel_name_green.png").convert_alpha()
                self.name = group.inventory[self.slot_number].name
            if type == "pilot_line_item":
                self.width = screen_width*0.235
                self.height = screen_height*0.07
                self.pos_x = screen_width*0.17
                self.pos_y = screen_height*0.2 + self.slot_number*self.height                
                self.frame_1 = pygame.image.load("graphics/interface/labels/interface_panel_name.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/labels/interface_panel_name_green.png").convert_alpha()
                self.frame_3 = pygame.image.load("graphics/interface/labels/interface_panel_name_yellow.png").convert_alpha()
                self.pilot = group.pilot_roster[self.slot_number]
                self.name = self.pilot.name
            if type == "loadout_label":
                self.width = screen_width*0.12
                self.height = screen_height*0.07
                self.frame_1 = pygame.image.load("graphics/interface/labels/label_white_lowres.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/labels/label_white_greenborder3.png").convert_alpha()
                self.name = " "
                if self.slot_number == 0: 
                    self.pos_x = screen_width*0.63
                    self.pos_y = screen_height*0.5
                elif self.slot_number == 1: 
                    self.pos_x = screen_width*0.36
                    self.pos_y = screen_height*0.33
                elif self.slot_number == 2: 
                    self.pos_x = screen_width*0.63
                    self.pos_y = screen_height*0.33
                elif self.slot_number == 3: 
                    self.pos_x = screen_width*0.36
                    self.pos_y = screen_height*0.68
                elif self.slot_number == 4: 
                    self.pos_x = screen_width*0.63
                    self.pos_y = screen_height*0.68
                else:
                    self.pos_x = screen_width*0.5
                    self.pos_y = screen_height*0.5
            self.frame_0 = pygame.transform.scale(self.frame_0,(self.width,self.height))
            self.frame_1 = pygame.transform.scale(self.frame_1,(self.width,self.height))
            self.frame_2 = pygame.transform.scale(self.frame_2,(self.width,self.height))
            self.frame_3 = pygame.transform.scale(self.frame_3,(self.width,self.height))
            self.frames = [self.frame_0,self.frame_1,self.frame_2,self.frame_3]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
        def destroy(self):
            self.kill()
        def highlight_selected(self):
            if self.selected == True:
                self.animation_index = 2
            else: self.animation_index = 1
            if self.type == "pilot_line_item":
                if self.pilot.on_mission == True: 
                    self.pilot.dispatching = True
                if self.pilot.dispatching == True: self.animation_index = 3
        def click_button(self):
            if event.type == pygame.MOUSEBUTTONDOWN: #Toggle select
                if self.rect.collidepoint(event.pos) and self.cooldown == 0: 
                    self.cooldown = 10
                    if self.type == "pilot_line_item":
                        if selected.pilot_slot == self.slot_number:
                            selected.pilot = group.pilot_roster[0]
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
        def update(self):
            if self.cooldown > 0: self.cooldown -= 1
            self.click_button()
            self.highlight_selected()
            if self.type == "pilot_line_item":
                if self.slot_number == selected.pilot_slot:
                    self.selected = True
                else: self.selected = False
            if self.type == "loadout_label":
                self.name = selected.pilot.battlesuit.loadout[self.slot_number].name
                if self.slot_number == selected.loadout_slot and selected.pilot_slot > -1:
                    self.selected = True
                else: self.selected = False
            if self.type == "inventory_line_item":
                if selected.loadout_slot >= -1 and self.slot_number == selected.inventory_slot:
                    self.selected = True
                else: self.selected = False
            self.image = self.frames[self.animation_index]          
    
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
                    overlay.type = "dialogue"
                    nighthawk.on_mission = True
                    dialogue.load_scene_dialogue("mission",1)
                    self.cooldown = 10
                    if self.animation_index == 2:
                        self.animation_index = 1
                        selected.pointer_slot = self.slot_number
                    else: 
                        self.animation_index = 2
                        selected.pointer_slot = -1
    
    class Clock_Icon(pygame.sprite.Sprite):
        def __init__(self, reference):
            super().__init__()
            self.reference = reference
            self.animation_index = 0
            self.width = screen_height*0.08
            self.height = screen_height*0.08
            
            #load frames
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
            
            #resize frames
            self.frame_0 = pygame.transform.scale(self.frame_0, (self.width, self.height))
            self.frame_1 = pygame.transform.scale(self.frame_1, (self.width, self.height))
            self.frame_2 = pygame.transform.scale(self.frame_2, (self.width, self.height))
            self.frame_3 = pygame.transform.scale(self.frame_3, (self.width, self.height))
            self.frame_4 = pygame.transform.scale(self.frame_4, (self.width, self.height))
            self.frame_5 = pygame.transform.scale(self.frame_5, (self.width, self.height))
            self.frame_6 = pygame.transform.scale(self.frame_6, (self.width, self.height))
            self.frame_7 = pygame.transform.scale(self.frame_7, (self.width, self.height))
            self.frame_8 = pygame.transform.scale(self.frame_8, (self.width, self.height))
            self.frame_9 = pygame.transform.scale(self.frame_9, (self.width, self.height))
            self.frame_10 = pygame.transform.scale(self.frame_10, (self.width, self.height))
            
            self.frames = [self.frame_0,self.frame_1,self.frame_2,self.frame_3,self.frame_4,self.frame_5,self.frame_6,self.frame_7,self.frame_8,self.frame_9,self.frame_10]
            
            self.pos_x = self.reference.pos_x
            self.pos_y = self.reference.pos_y - screen_height*0.05
            
            self.clock_segment = 10
            self.animation_index = self.clock_segment
            
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
            
        def update(self):
            #update clock segments
            self.clock_segment = int((100 - self.reference.progress_track)/10)
            self.animation_index = self.clock_segment
            
            #update position, relevant if the reference object moves
            self.pos_x = self.reference.pos_x
            self.pos_y = self.reference.pos_y - screen_height*0.05
            
            #update image and rect
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))
    
    class Health_Icon(pygame.sprite.Sprite):
        def __init__(self,type, reference):
            super().__init__()
            self.reference = reference
            self.pilot = reference
            self.frames = []
            self.animation_index = 0
            self.slot_number = 0
            self.type = type
            self.width = screen_height*0.04
            self.height = screen_height*0.04
            self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
            
            #health status icons
            if type == "shield":
                self.frame_1 = pygame.image.load("graphics/interface/icons/shield.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/shield.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1]
                self.slot_number = 1
            
            elif type == "damaged":
                self.frame_1 = pygame.image.load("graphics/interface/icons/warning_white.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/warning_yellow.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.slot_number = 2
            
            elif type == "severely_damaged":
                self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()
                self.frame_1 = pygame.image.load("graphics/interface/icons/warning_white.png").convert_alpha()
                self.frame_2 = pygame.image.load("graphics/interface/icons/warning_red.png").convert_alpha()
                self.frames = [self.frame_0,self.frame_1,self.frame_2]
                self.slot_number = 3
            
            self.frame_0 = pygame.transform.scale(self.frame_0,(self.width,self.height))
            self.frame_1 = pygame.transform.scale(self.frame_1,(self.width,self.height))
            self.frame_2 = pygame.transform.scale(self.frame_2,(self.width,self.height))
            self.frames = [self.frame_0,self.frame_1,self.frame_2]
            
            
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = ((screen_width*0.19+self.width*1.1*self.slot_number),screen_height*0.21+self.height*1.7*self.pilot.slot_number))
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
            self.frame_2 = blank_frame
            self.active = False
            self.cooldown_max = 25
            self.cooldown = self.cooldown_max
            
            if self.type == "x_button":
                self.frame_1 = pygame.image.load("graphics/interface/icons/x_button_75.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1,(screen_width*0.05,screen_height*0.05))
                self.pos_x = screen_width*0.2
                self.pos_y - screen_height*0.2
            
            if self.type == "dashboard_map":
                self.animation_index = 1
                self.pos_x = screen_width*0.1
                self.pos_y = screen_height*0.15
                self.frame_1 = pygame.image.load("graphics/interface/cockpit/clickscreen.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1, (screen_width*0.2,screen_height*0.2))
            
            if self.type == "continue_button":
                self.pos_x = screen_width*0.15
                self.pos_y = screen_height*0.14
                self.width = screen_width*0.2
                self.height = screen_height*0.07
                self.frame_1 = pygame.image.load("graphics/interface/labels/continue_button.png")
                self.frame_1 = pygame.transform.scale(self.frame_1, (self.width,self.height))
            
            if type == "swap_button":
                self.width = screen_width*0.2
                self.height = screen_height*0.15
                self.pos_x = screen_width*0.5
                self.pos_y = screen_height*0.85 
                self.match = False
                self.frame_1 = pygame.image.load("graphics/interface/labels/label_white_selected_lowres.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1,(self.width,self.height))
                self.frame_2 = pygame.image.load("graphics/interface/labels/noswap_label.png").convert_alpha()
                self.frame_2 = pygame.transform.scale(self.frame_2,(self.width,self.height))
            
            if type == "dispatch_button":
                self.width = screen_width*0.2
                self.height = screen_height*0.15
                self.pos_x = screen_width*0.5
                self.pos_y = screen_height*0.85 
                self.frame_1 = pygame.image.load("graphics/interface/labels/label_white_selected_lowres.png").convert_alpha()
                self.frame_1 = pygame.transform.scale(self.frame_1,(self.width,self.height))
            
            self.frames = [self.frame_0, self.frame_1, self.frame_2]
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))
        
        def update(self):
            # reduce cooldown
            if self.cooldown > 0: self.cooldown -= 1
            
            # determine if active
            if self.type == "dashboard_map":
                if overlay.type == "cockpit": self.active = True
                else: self.active = False
            
            elif self.type == "swap_button":
                if overlay.type != "inventory": self.active = False
                elif selected.inventory_slot > -1 and selected.pilot_slot > -1 and selected.loadout_slot > -1: 
                    self.active = True
                    if group.inventory[selected.inventory_slot].function != selected.pilot.battlesuit.loadout[selected.loadout_slot].function: 
                        self.match = False
                    else: self.match = True
                else: self.active = False
            
            elif self.type == "dispatch_button":
                if overlay.type == "pilot_select" and selected.pilot_slot > 0 and selected.pilot.on_mission == False: self.active = True
                else: self.active = False
            
            elif self.type == "continue_button":
                # make the continue button active if at least one Pilot is dispatching
                if overlay.type == "pilot_select":
                    self.active = False
                    for pilot in group.pilot_roster:
                        if pilot.dispatching: self.active = True
                
                # make the continue button active if there are scenes in queue and game is not awaiting a choice
                elif overlay.type == "dialogue":
                    if len(scene.scene_queue) > 0 and dialogue.choices_available == False: self.active = True
                    
                # always hide continue button on world map
                elif overlay.type == "map": self.active = False
                
                #always hide continue button during combat
                elif overlay.type == "combat": self.active = False
                
                # make the continue button visible if active and hidden otherwise
                if self.active == True: self.animation_index = 1
                else: self.animation_index = 0
            
            elif self.type == "x_button":
                pass
            
            else: 
                if debug_mode == True: print("Error: unrecognized button type when checking if active", self.type)
                else: pass
            
            # mouse inputs
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos) and self.active == True and self.cooldown == 0:
                    
                    # reset cooldown
                    self.cooldown = self.cooldown_max
                    
                    # close ui window
                    if self.type == "x_button" and overlay.type != "cockpit":
                        overlay.type = "cockpit"
                    
                    # show world map
                    elif overlay.type == "cockpit" and self.type == "dashboard_map":
                        overlay.type = "map"
                    
                    # swap loadout and inventory items
                    elif self.type == "swap_button" and self.match == True:
                        # swap items
                        new_loadout_item = group.inventory[selected.inventory_slot]
                        new_inventory_item = selected.pilot.battlesuit.loadout[selected.loadout_slot]
                        selected.pilot.battlesuit.loadout[selected.loadout_slot] = new_loadout_item
                        group.inventory[selected.inventory_slot] = new_inventory_item
                        # reset which items are currently selected
                        selected.loadout_slot = -1
                        selected.inventory_slot = -1 
                        
                    # assign Pilot to mission
                    elif self.type == "dispatch_button":
                        if selected.pilot.dispatching == False: selected.pilot.dispatching = True
                        else: selected.pilot.dispatching = False
                    
                    # load the departing messages and return to dialogue screen. This should probably be a method like overlay.continue().
                    elif self.type == "continue_button" and self.active == True and overlay.type == "pilot_select":
                        scene.scene_queue.clear()
                        overlay.type = "dialogue"
                        for pilot in group.pilot_roster:
                            if pilot.dispatching: 
                                pilot.dispatching = False
                                pilot.on_mission = True
                            if pilot.on_mission:
                                scene.scene_queue.append(f"{pilot.name} departing")
                        
                        # conclude npcs with nighthawk and making sure she speaks last
                        if len(scene.scene_queue) > 1 and scene.scene_queue[0] == "Nighthawk departing":
                            scene.scene_queue.append("Nighthawk departing")
                            scene.scene_queue.remove("Nighthawk departing")
                        
                        scene.scene_queue.append("combat")
                        
                        if debug_mode == True: print(scene.scene_queue)
                            # mission.mission_setup(selected.active_mission_number)
                            
                    # advance to next scene if queue is not empty
                    elif self.type == "continue_button" and self.active == True and overlay.type == "dialogue" and dialogue.choices_available == False:
                        try: 
                            if debug_mode == True:
                                print(" ")
                                print(scene.scene_queue)
                                print("removing scene: ", scene.scene_queue[0])
                                print("advancing to scene:", scene.scene_queue[1])
                            dialogue.advance_scene(-1)
                            if debug_mode == True:
                                print("current scene is now:", scene.scene_queue[0])
                                print("next scene in queue:", scene.scene_queue[1])
                                print(scene.scene_queue)
                                print(" ")
                        except: 
                            if debug_mode == True: print("Error: no scenes in queue to remove")
                            else: pass
                            
                    # if none of the above button is not activated
                    else: self.active = False
            
            # update image
            if self.active == False: self.animation_index = 0
            else: self.animation_index = 1
            if self.type == "swap_button" and self.active == True:
                if self.match == False: self.animation_index = 2
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (self.pos_x,self.pos_y))   
    
    class Image_Holder:
        def __init__(self):
            self.portrait = {
                "Nighthawk":pygame.image.load("graphics/pilots/nighthawk/default.png").convert_alpha(),
                "kite":pygame.image.load("graphics/pilots/kite/default.png").convert_alpha(),
                "saint":pygame.image.load("graphics/pilots/saint/default.png").convert_alpha(),
                "Deadlift":pygame.image.load("graphics/pilots/deadlift/default.png").convert_alpha(),
                "Azure_Kite":pygame.image.load("graphics/pilots/kite/default.png").convert_alpha(),
                "Shadowstalker":pygame.image.load("graphics/pilots/stalker/default.png").convert_alpha(),
                "Unassigned":pygame.image.load("graphics/pilots/kite/default.png").convert_alpha()
                }
    
    class Overlay_Manager:
        def __init__(self, type):
            self.type = type
            self.large_frame_image = pygame.image.load("graphics/interface/frames/white_frame_large.png").convert_alpha()
            self.large_frame_image = pygame.transform.scale(self.large_frame_image, (screen_width*0.9,screen_height*0.9))
            self.large_frame_rect = self.large_frame_image.get_rect(center = (screen_width/2,screen_height/2)) 
            self.black_block_image = pygame.image.load("graphics/interface/frames/black_blocker.png").convert_alpha()
            self.black_block_image = pygame.transform.scale(self.black_block_image, (screen_width,screen_height))
            self.black_block_rect = self.black_block_image.get_rect(center = centerpoint)
            self.green_filter_image = pygame.image.load("graphics/interface/green_filter_full.png").convert_alpha()
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
            self.small_frame_left_image = pygame.image.load("graphics/interface/frames/small_frame.png").convert_alpha()
            self.small_frame_left_image = pygame.transform.scale(self.small_frame_left_image, (screen_width*0.24,screen_height*0.82))
            self.small_frame_left_rect = self.small_frame_left_image.get_rect(topleft = (self.large_frame_rect.left, screen_height*0.13))
            self.small_frame_right_image = pygame.image.load("graphics/interface/frames/small_frame_flipped.png").convert_alpha()
            self.small_frame_right_image = pygame.transform.scale(self.small_frame_right_image, (screen_width*0.24,screen_height*0.82))
            self.small_frame_right_rect = self.small_frame_right_image.get_rect(topright = (self.large_frame_rect.right, screen_height*0.13))
            self.nighthawk_portrait = pygame.image.load("graphics/pilots/nighthawk/default.png").convert_alpha()
            self.kite_portrait = pygame.image.load("graphics/pilots/kite/default.png").convert_alpha()
            self.saint_portrait = pygame.image.load("graphics/pilots/saint/default.png").convert_alpha()
            self.deadlift_portrait = pygame.image.load("graphics/pilots/deadlift/default.png").convert_alpha()
            self.kite_portrait = pygame.image.load("graphics/pilots/kite/default.png").convert_alpha()
            self.shadowstalker_portrait = pygame.image.load("graphics/pilots/stalker/default.png").convert_alpha()
            self.unassigned_portrait = pygame.image.load("graphics/pilots/kite/default.png").convert_alpha()
        def draw_selected_pilot_name(self):
            selected.pilot_name_image = text_font.render(f"{selected.pilot.name}",False,(111,196,169))
            selected.pilot_name_rect = selected.pilot_name_image.get_rect(center = (screen_width*0.5,screen_height*0.25))
            screen.blit(selected.pilot_name_image,(selected.pilot_name_rect))
        def draw_cockpit(self):
            screen.blit(self.planet_image,(0,0))
            screen.blit(self.dashboard_image,(0,0))
        def draw_interface_screen_front(self):
            screen.blit(self.large_frame_image,(self.large_frame_rect)) 
        def draw_pause_screen(self):
            screen.blit(self.pause_menu_image, (0,0))
            screen.blit(self.quit_button_image, (0,540))
        def draw_small_frame(self, side):
            if side == "left":
                screen.blit(self.small_frame_left_image,(self.small_frame_left_rect))
            if side == "right":
                screen.blit(self.small_frame_right_image,(self.small_frame_right_rect))
        def draw_loadout(self):
            screen.blit(self.blueprint_image,(self.blueprint_rect))
        def draw_void(self):
            screen.fill((0,0,0))
        def draw_ui_buttons(self):
            group.buttons.update()
            group.buttons.draw(screen)
        def draw_portrait(self, pilot):
            if selected.pilot == nighthawk:
                portrait = self.nighthawk_portrait
            elif selected.pilot == kite:
                portrait = self.kite_portrait
            elif selected.pilot == saint:
                 portrait = self.saint_portrait
            elif selected.pilot == deadlift:
                portrait = self.deadlift_portrait
            elif selected.pilot == kite:
                portrait = self.kite_portrait
            elif selected.pilot == shadowstalker:
                portrait = self.shadowstalker_portrait
            else:
                portrait = self.unassigned_portrait
            portrait = pygame.transform.scale(portrait,(screen_height*0.45*0.8,screen_height*0.8))
            screen.blit(portrait,(screen_width*0.72,screen_height*0.25))
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
            #fill screen with black to cover previous cycle
            screen.fill((0,0,0))
            
            #update buttons
            group.buttons.update()
            
            if self.type == "inventory":
                self.draw_loadout()
                group.inventory_nameplates.update()
                group.inventory_nameplates.draw(screen)
                group.pilot_nameplates.update()
                group.pilot_nameplates.draw(screen)
                group.pilot_text_names.update()
                group.pilot_text_names.draw(screen)
                group.loadout_text_names.update()
                group.loadout_text_names.draw(screen)
                group.inventory_text_names.update()
                group.inventory_text_names.draw(screen)
                self.draw_selected_pilot_name()
                self.draw_small_frame("left")
                self.draw_small_frame("right")
                self.draw_interface_screen_front()
            elif self.type == "map":
                group.islands.update()
                group.islands.draw(screen)
                group.mission_pointers.update()
                group.mission_pointers.draw(screen)
                if selected.pointer_slot > 0:
                    self.draw_small_frame("right") 
                self.draw_interface_screen_front()
            elif self.type == "combat":
                screen.blit(self.desert_map, (0,0))
                mission.terrain_pieces.draw(screen)
                mission.objectives.draw(screen)
                group.clock_icons.draw(screen)
                mission.pilots.draw(screen)
                group.pilot_combat_names.draw(screen)
                mission.enemies.draw(screen)
                group.weapon_effects.update()
                group.weapon_effects.draw(screen)
                #temp
                # group.health_icons.update()
                # group.health_icons.draw(screen)
                #temp
                self.draw_interface_screen_front()
            elif self.type == "health_tracker":
                group.pilot_nameplates.update()
                group.pilot_nameplates.draw(screen)
                group.pilot_text_names.update()
                group.pilot_text_names.draw(screen)
                group.health_icons.update()
                group.health_icons.draw(screen)
                self.draw_portrait(selected.pilot)
                self.draw_small_frame("left")
                self.draw_small_frame("right")
                self.draw_interface_screen_front()
            elif self.type == "cockpit":
                self.draw_cockpit()
            elif self.type == "dialogue":
                self.draw_portrait(dialogue.speaker)
                self.draw_small_frame("right")
                self.draw_ui_buttons()
                dialogue.update()
                drawText(screen, dialogue.current_npc_lines, (111,196,169), dialogue.npc_text_rect, text_font)
                drawText(screen, dialogue.current_player_lines, pygame.Color("coral"), dialogue.player_text_rect, text_font)
                self.draw_interface_screen_front()
            elif self.type == "pilot_select":
                group.pilot_nameplates.update()
                group.pilot_nameplates.draw(screen)
                group.pilot_text_names.update()
                group.pilot_text_names.draw(screen)
                group.pilot_text_stats.update()
                group.pilot_text_stats.draw(screen)
                group.health_icons.update()
                group.health_icons.draw(screen)
                self.draw_selected_pilot_name()
                self.draw_portrait(selected.pilot)
                self.draw_small_frame("left")
                self.draw_small_frame("right")
                self.draw_interface_screen_front()
            else:
                x_button = False
                continue_button = False
            
            group.buttons.update()
            group.buttons.draw(screen)
            group.text_objects.update()
            group.text_objects.draw(screen)
            
            #add green transparency and black border to hide anything outside the "window"
            if self.type != "cockpit":
                screen.blit(self.green_filter_image,(self.green_filter_rect)) #this one causes lag
                screen.blit(self.black_block_image, (self.black_block_rect))
            
    class Mission_Manager:
        def __init__(self):
            self.current_mission = 0
            self.waypoints = []
            self.pilots = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.terrain_pieces = pygame.sprite.Group()
            self.objectives = pygame.sprite.Group()
            self.train_roster = []
        
        def spawn_clock(self, reference):
            group.clock_icons.add(Clock_Icon(reference))
            
        def spawn_terrain(self, type, pos_x, pos_y, width, height):
            self.terrain_pieces.add(Terrain_Piece(type, pos_x, pos_y, width, height))
        
        def spawn_drones(self):
            drone_quantity = random.randint(2,4)
            while drone_quantity > 0:
                enemy_drone = Pilot("Enemy_Drone",1,copy.deepcopy(drone),"enemy")
                enemy_drone.orders = "objective"
                
                try: enemy_drone.move_target = mission.train_roster[0]
                except: 
                    if debug_mode == True: print("nothing in the train roster to target")
                    else: pass
                
                enemy_drone.battlesuit.shielded = False
                mission.enemies.add(enemy_drone)
                drone_quantity -= 1
        
        def spawn_crates(self, crate_quantity):
            while crate_quantity > 0:
                pos_x = random.randint(screen_width*0.2,screen_width*0.8)
                pos_y = random.randint(screen_height*0.4,screen_height*0.8)
                mission.objectives.add(Mission_Object("supply_crate",crate_quantity,pos_x,pos_y,"vanguard"))
                crate_quantity -= 1
        
        def spawn_train(self):
            train_objective = Pilot("supply_train",0,copy.deepcopy(train_suit),"vanguard")
            train_objective.type = "train"
            train_objective.is_objective = True
            train_objective.battlesuit.loadout.clear()
            train_objective.pos_x = -screen_width*0.1
            train_objective.pos_y = screen_height*0.1
            train_objective.checkpoint = 0
            train_objective.move_target = mission.waypoints[train_objective.checkpoint]
            train_objective.image = pygame.image.load("graphics/interface/icons/green_blip.png").convert_alpha()
            mission.objectives.add(train_objective)
            mission.train_roster.append(train_objective)
            slot_number = len(mission.train_roster) - 1
            train_name = Short_Text("train",slot_number)
            group.pilot_combat_names.add(train_name)
        
        def conduct_trains(self):
            for train in mission.train_roster:
            
                #immortal train
                if train.alive == False: train.alive = True
                
                target = train.move_target
                target_distance = train.find_distance(train, target)
                
                #update waypoint if close enough to current waypoint
                if target_distance < screen_width*0.02:
                    train.checkpoint += 1
                    
                    #advance to next waypoint
                    if train.checkpoint < len(self.waypoints):
                        try: 
                            train.move_target = mission.waypoints[train.checkpoint]
                            if debug_mode == True: print("advance to checkpoint: ", train.checkpoint)
                            self.spawn_drones()
                            train.move_distance = train.find_distance(train, train.move_target)
                        except: 
                            if debug_mode == True: print("Error: unable to advance train to next checkpoint")
                            else: pass
                    
                    #advance to next mission after reaching last waypoint
                    else:
                        selected.active_mission_number += 1
                        if debug_mode == True: print("advance to mission: ", selected.active_mission_number)
                        overlay.type = "map"
                
                
        def update(self):
            if overlay.type == "combat":
                self.conduct_trains()
                mission.pilots.update()
                group.pilot_combat_names.update()
                mission.enemies.update()
                mission.objectives.update()
                group.clock_icons.update()
                mission.terrain_pieces.update()
        
        def mission_setup(self, mission_number):
            if debug_mode == True: print("mission number", mission_number)
            mission_setup = True
            mission.enemies.empty()
            mission.pilots.empty()
            mission.objectives.empty()
            mission.train_roster.clear()
            
            if mission_number == 1:
                if mission_setup: #create waypoints
                    waypoint_0 = Mission_Object("waypoint", 0, screen_width*0.15, screen_height*0.2, "vanguard")
                    waypoint_1 = Mission_Object("waypoint", 1, screen_width*0.2, screen_height*0.3, "vanguard")
                    waypoint_2 = Mission_Object("waypoint", 2, screen_width*0.4, screen_height*0.8, "vanguard")
                    waypoint_3 = Mission_Object("waypoint", 3, screen_width*0.7, screen_height*0.5, "vanguard")
                    waypoint_4 = Mission_Object("waypoint", 4, screen_width*0.9, screen_height*0.7, "vanguard")
                    waypoint_5 = Mission_Object("waypoint", 5, screen_width*1.1, screen_height*0.3, "vanguard")
                    self.waypoints = [waypoint_0,waypoint_1,waypoint_2,waypoint_3,waypoint_4,waypoint_5]
                    for waypoint in self.waypoints: waypoint.alive = True
                if mission_setup == True: #create train
                    self.spawn_train()
                    train_objective = mission.train_roster[0]
                if mission_setup == True: #create enemies
                    mission.spawn_drones()
                    for enemy in mission.enemies:
                        enemy.attack_target = train_objective
                        enemy.move_target = train_objective
                        enemy.orders = "objective"
                if mission_setup == True: #prep pilots
                    for pilot in group.pilot_roster:
                        if pilot.on_mission: 
                            if debug_mode == True: print(pilot.name, "assigned to mission:", selected.active_mission_number)
                            pilot.orders = "objective"
                            mission.pilots.add(pilot)
                    kite.orders = "objective"
                    kite.active = True
                    nighthawk.orders = "objective"
                    nighthawk.active = True
                    saint.active = True
                    kite.pos_x = random.randint(-screen_width*0.2+train_objective.pos_x,screen_width*0.2+train_objective.pos_x)
                    kite.pos_y = random.randint(-screen_height*0.2+train_objective.pos_y, 0)
                    for pilot in mission.pilots: 
                        pilot.move_target = mission.train_roster[0]
                    for pilot in mission.enemies: 
                        pilot.move_target = mission.train_roster[0]
            
            elif mission_number == 2:
                #create enemies
                mission.spawn_drones()
                
                #create pickups
                mission.spawn_crates(5)
                
                #create terrain
                mission.spawn_terrain ("rock", screen_width*0.5, screen_height*0.5, screen_width*0.3, screen_height*0.3)
                
                #placeholder to add multiple pilots to mission 2
                kite.on_mission = True
                nighthawk.on_mission = True
                saint.on_mission = True
                kite.on_mission = True
                
                #prep pilots
                if mission_setup == True:
                    for pilot in group.pilot_roster:
                        if pilot.on_mission: 
                            if debug_mode == True: print(pilot.name, "assigned to mission:", selected.active_mission_number)
                            pilot.orders = "objective"
                            pilot.momentum_y = 10
                            pilot.pos_y = 0 - random.randint(0,300)
                            pilot.pos_x = screen_width/2 - 150 + random.randint(0,300)
                            mission.pilots.add(pilot)
                
                kite.orders = "objective"
                kite.active = True
                nighthawk.orders = "objective"
                nighthawk.active = True
                saint.active = True
    
    class Scene_Manager:
        def __init__(self):
            self.current_scene = "empty"
            self.scene_queue = []
        
        def update(self):
            #update the current scene
            if len(scene.scene_queue) > 0:
                try: self.current_scene = self.scene_queue[0]
                except: 
                    if debug_mode == True: print("Error: scene queue is empty")
                    else: pass
            
            # advance to combat if no scenes remain in queue and at least one Pilot is on_mission
            # if len(scene.scene_queue) == 0:
                # for Pilot in group.pilot_roster:
                    # if Pilot.on_mission: overlay.type = "combat"
            
            #update overlay to pilot_select
            if self.current_scene == "pilot_select": overlay.type = "pilot_select"
            
            #update overlay from dialogue to combat
            if overlay.type == "dialogue" and self.current_scene == "combat": 
                mission.mission_setup(selected.active_mission_number)
                overlay.type = "combat"
        
    class Dialogue_Manager:
        def __init__(self):
            self.speaker = "speaker"
            self.topic = "none"
            self.current_npc_lines = "empty"
            self.current_player_lines = "empty"
            self.portrait = blank_frame
            self.choices_available = False
            self.scene_index = 0
            self.npc_line_number = 0
            self.npc_text_rect = pygame.Rect((screen_width*0.1,screen_height*0.25),(screen_width*0.6,screen_height*0.5))
            self.player_line_number = 0
            self.player_lines = [" "]
            self.player_text_rect = pygame.Rect((screen_width*0.1,screen_height*0.7),(screen_width*0.6,screen_height*0.2))
            self.cooldown_max = 25
            self.cooldown = self.cooldown_max
        
        def load_scene_dialogue(self, topic, scene_index):
            
            #mission event 1: train under attack
            if topic == "mission" and scene_index == 1:
                self.speaker = nighthawk
                selected.pilot = nighthawk
                self.npc_line_number = 0
                self.player_line_number = 0
                self.topic = topic
                self.scene_index = scene_index
                scene.current_scene = "Mission 1 welcome"
                self.choices_available = True
                
                scene.scene_queue.clear()
                scene.scene_queue.append("Mission 1 welcome")
                
                dialogue.lines = {
                        "Nighthawk":[
                                    "    Hi, you've got great timing!  Normally I'd give you the whole 'Welcome to Arcturus' bit, but someone is attacking one of our supply trains and I'm en-route to respond.  I can probably handle it, but I'd appreciate it if you could call in some backup just in case.",
                                    "   Alright, showtime."
                                        ],  
                        
                        "kite":[
                                    " ",
                                    "   Nighthawk needs help? No problem, I'm on my way!"
                                        ],
                        
                        "saint":[
                                    " ",
                                    "   Understood, I've been itching for a chance to test out a new weapon."
                                        ],
                        
                        "Shadowstalker":[
                                    " ",
                                    "  Fine. Just let me know who needs killing."
                                        ],
                        
                        "Azure_Kite":[
                                    " ",
                                    "   Currently assigned on another mission. Try contacting anyway?",
                                    "   Currently unavailable."
                                        ],   
                        
                        "Deadlift":[
                                    " ",
                                    "   Currently assigned on another mission. Try contacting anyway?",
                                    "   Currently unavailable."
                                        ],
                        "Player":[
                                    "1) Understood. Let me see who's available",
                                    " "
                                        ]
                        }
                
                # set player's starting lines
                player_lines = dialogue.lines["Player"]
                self.current_player_lines = player_lines[0]
            
            #social event 1: free trial weapons offer
            elif topic == "social_event" and scene_index == 1:
                dialogue.lines["benny"] = ["Hey there, the name's Benny. I'm the local representative of Marco's Munitions LLC. I just wanted to thank you and your team for your hard work keeping us all safe.",
                                "The company lets me give out free trials of our latest products to potential buyers, so as a token of appreciation I'd like to set you up with our brand-new weapon 'The Emissary of the Void' for the next month 100% free of charge.",
                                "Fantastic! Just make sure you get that back to us in a month. Otherwise you can let us know if you'd like to make a purchase and I'll see what I can do in the way of discounts."]
            
            #social event 2: invitation from Falcone
            elif topic == "social_event" and scene_index == 2:
                dialogue.lines["samuel"] = ["Mr. Falcone has expressed an interest in speaking with you.",
                                    "He's a respectable local businessman. Pillar a' the community.",
                                    "A few words of advice; be polite, don't talk for too long, and don't ask any questions about the eye."]                    
            
            #social event (getting to know them)
            elif topic == "personal" and scene_index == 1:
                dialogue.lines["nighthawk"] = ["Good evening, Captain. It's good to meet you properly now that things have quieted down.",
                                    "Do you drink? I brought a bottle of wine as a house-warming gift, so to speak.",
                                    "So, what would you like to know?",
                                    "Before this? I actually came to this planet to be a transport operator as part of the first landing. Not glamorous, but it was important work.",
                                    "Nobody who wasn't here when it happened can really understand what it was like to live through few the first days and months of the Collapse. It's the experience of being in a tall building when the bottom few stories abruptly cease to exist. That feeling in the pit of your stomach when suddenly the floor starts to drop as gravity takes hold.",
                                    "No doubt in my mind, the biggest threat to people is the organized gangs in the city."]
                dialogue.lines["nighthawk"] = ["Hi there, it's nice to meet you!",
                                "So, what would you like to know?"]
        
        def advance_scene(self, choice_number):
            if self.cooldown == 0:
                if debug_mode == True: print("Choice:", choice_number)
                
                #reset cooldown
                self.cooldown = self.cooldown_max
                
                #remove current scene from queue and update
                if choice_number == -1:
                    current_scene = scene.current_scene
                    scene.scene_queue.remove(current_scene)
                    scene.current_scene = scene.scene_queue[0]
                    
                #acknowledge choice
                if choice_number > 0: 
                    
                    # specific for mission 1, advance to Pilot select
                    if scene.current_scene == "Mission 1 welcome" and choice_number == 1:
                            dialogue.choices_available = False
                            
                            #update current scene to Pilot select
                            scene.scene_queue.append("pilot_select")
                            scene.scene_queue.remove("Mission 1 welcome")
                            scene.current_scene = scene.scene_queue[0]
                            if debug_mode == True: print(scene.current_scene)
                            
                            #silence player dialogue
                            try:
                                dialogue.player_line_number = 1
                                player_lines = dialogue.lines["Player"]
                                dialogue.current_player_lines = player_lines[dialogue.player_line_number]
                            except: 
                                if debug_mode == True: print("Error: could not silence the player after choice")
                                else: pass
            
        def update(self):
            
            # reduce cooldown
            if self.cooldown > 0:
                self.cooldown -= 1
                
            # set the current scene to be whatever is at the front of the queue
            try: scene.current_scene = scene.scene_queue[0]
            except: 
                if debug_mode == True: print("Error: can't update scene because queue is empty")
                else: pass
            # if len(scene.scene_queue) > 0:
                # scene.current_scene = scene.scene_queue[0]
            
            # placeholder code specifically for departing scenes on mission 1
            
            # update current speaking npc for departures and their portrait
            for pilot in group.pilot_roster:
                pilot_departing_scene_name = f"{pilot.name} departing"
                if pilot_departing_scene_name == scene.current_scene: 
                    dialogue.speaker = pilot
                    dialogue.npc_line_number = 1
            
            # update displayed dialogue for current scene
            try:
                npc_lines = dialogue.lines[self.speaker.name]
                dialogue.current_npc_lines = npc_lines[dialogue.npc_line_number]
            except: 
                if debug_mode == True: print("Error: speaker name or lines are invalid")
                else: pass
            
            # update portrait by making the selected Pilot = the current speaking npc
            try: selected.pilot = dialogue.speaker
            except: 
                if debug_mode == True: print("Error: dialogue.speaker is invalid choice for selected.Pilot portrait")
                else: pass
            # try: self.portrait = image.portrait[f"{dialogue.speaker.name}"]
            # except: print("Error: invalid portrait")
            
            # handle unavailable pilots
            
            # insert second dialogue page for "unavailable"(placeholder) during departures
            try:
                current_npc_lines = dialogue.lines[f"{self.speaker.name}"]
                if current_npc_lines[dialogue.npc_line_number] == "   Currently assigned on another mission. Try contacting anyway?":
                    if scene.scene_queue[0] != f"{self.speaker.name} unavailable" and scene.scene_queue[1] != f"{self.speaker.name} unavailable": 
                        scene.scene_queue.insert(1, f"{self.speaker.name} unavailable")
                        if debug_mode == True:
                            print("Success: second page for 'unavailable' inserted into queue")
                            print(scene.scene_queue)
                            print(" ")
                    # elif scene.scene_queue[1] == f"{self.speaker.name} unavailable": print("second page for 'unavailable' already inserted into queue")
            except: 
                if debug_mode == True: print("Error: unable to add second page for 'unavailable' to the queue")
                else: pass
            # if scene.scene_queue[0] == f"{self.speaker.name} unavailable": dialogue.npc_line_number = 2
            
            # unassign Pilot from the mission if they are unavailable
            if scene.current_scene == f"{selected.pilot.name} unavailable":
                selected.pilot.dispatching = False
                selected.pilot.on_mission = False
                if debug_mode == True: print(selected.pilot.name, selected.pilot.dispatching, selected.pilot.on_mission)
                dialogue.npc_line_number = 2
   
    class Story_Manager:
        def __init__(self):
            self.sidequest_1 = "marko's munitions"
            self.current_mission = 0
            self.main_story_level = 1
    
    class Group_Manager:
        def __init__(self):
            self.pilot_roster = []
            self.inventory_nameplates = pygame.sprite.Group()
            self.pilot_nameplates = pygame.sprite.Group()
            self.pilot_text_names = pygame.sprite.Group()
            self.pilot_text_stats = pygame.sprite.Group()
            self.inventory_text_names = pygame.sprite.Group()
            self.loadout_text_names = pygame.sprite.Group()
            self.pilot_combat_names = pygame.sprite.Group()
            self.islands = pygame.sprite.Group()
            self.weapon_effects = pygame.sprite.Group()
            self.mission_objects = pygame.sprite.Group()
            self.health_icons = pygame.sprite.Group()
            self.clock_icons = pygame.sprite.Group()
            self.mission_pointers = pygame.sprite.Group()
            self.buttons = pygame.sprite.Group()
            self.inventory = []
            self.status_effects = ["frozen","overheated","disrupted","blinded","knockback","energized","supressed","tethered"]
            self.power_cores = {"01":"trapped_combustion_core", "02":"dirty_fission_core", "04":"solar_array_core", "06":"cold_fusion_core", "07":"entropy_core", "08":"black_pinhole_core", "10":"wave_collapse_core", "11":"phantom_pinnacle_core", "0x":"alien_crystal_core", "00":"no_core"}
            self.text_objects = pygame.sprite.Group()
    
    class Selected:
        def __init__(self):
            self.pilot = "null"
            self.pilot_slot= -1
            self.loadout_slot = -1
            self.inventory_slot = -1
            self.item = "null"
            self.map_display = "none"
            self.island_number = -1
            self.pointer_slot = -1
            self.choice_number = -1
            self.active_mission_number = -1

    class Facility():
        def __init__(self, type, location):
            
            self.type = type
            self.location = location
            self.rank = 1
            self.failure_rate = 0.60 - (0.1 * self.rank)

            if self.type == "battlesuit_hangar":
                self.capacity = self.rank
                self.repair_bays = {
                    "repair_bay 1":"empty",
                    "repair_bay 2":"empty",
                    "repair_bay 3":"empty",
                    "repair_bay 4":"empty",
                    "repair_bay 5":"empty",
                    "repair_bay 6":"empty"
                }

                # def perform_repairs(self):
                #     for suit in self.repair_bays:
                #         if resources["spare parts"] > 0 and suit != "empty":
                #          if suit.damaged == True:
                #             resources["spare parts"] -= 1
                #             percentile_roll = random.ranint(0,100)/100
                #             if percentile_roll > self.failure_rate:
                #                 if suit.severely_damaged == True: suit.severely_damaged = False
                #                 elif suit.damaged == True: suit.damaged = False
                #         if suit.damaged == False: suit = "empty"

            if self.type == "infirmary":
                self.capacity = self.rank
                self.med_beds = {
                    "bed 1":"empty",
                    "bed 2":"empty",
                    "bed 3":"empty",
                    "bed 4":"empty",
                    "bed 5":"empty",
                    "bed 6":"empty",
                }

                # #placeholder writing out Pilot health conditions
                # Pilot.health = {
                # 	"bleeding":"blood loss",
                # 	"disease":"illness",
                # 	"pain":7/10,
                # 	"skull":"fractured",
                #	"pelvis":"broken"
                #	"ribs":"fractured"
                # 	"left arm":"prosthetic (damaged)"
                # 	"left leg":"shattered",
                # 	"right arm":"lacerated"
                # 	"right leg":"maimed"
                # }
                # for condition in Pilot.health: condition = "empty"
                # #placeholder writing out Pilot health conditions



                def perform_healing(self):
                    for pilot in self.med_beds:
                        if pilot != "empty":
                            for condition in pilot.health:
                                
                                #treat illnesses
                                if condition == "illness" and resources["medications"] > 0:
                                    resources["medications"] -= 1
                                    condition = "illness (recovering)"
                                elif condition == "illness (recovering)" and resources["medications"] > 0:
                                    resources["medications"] -= 1
                                    percentile_roll = random.ranint(0,100)/100
                                    if percentile_roll > self.failure_rate: condition = "empty"
                                
                                #treat blood loss
                                elif condition == "severe blood loss": condition = "blood loss"
                                elif condition == "blood loss": condition = "blood loss (recovering)"
                                elif condition == "blood loss (recovering)": 
                                    percentile_roll = random.ranint(0,100)/100
                                    if percentile_roll > self.failure_rate: condition = "empty"

                                #treat broken bones
                                elif condition == "fractured": condition = "fractured (recovering)"
                                elif condition == "broken": condition = "broken (recovering)"
                                elif condition == "fractured (recovering)" or condition == "broken (recovering)":
                                    percentile_roll = random.ranint(0,100)/100
                                    if percentile_roll > self.failure_rate: condition = "empty"

                                #prosthetics
                                elif condition == "maimed": condition = "amputated"
                                elif condition == "amputated" and resources["cybernetics"] >= 2:
                                    resources["cybernetics"] -= 2
                                    condition = "prosthetic"
                                elif condition == "prosthetic (damaged)" and resources["cybernetics"] >= 1:
                                    resources["cybernetics"] -= 1
                                    condition = "prosthetic"

            if self.type == "prison":
                self.capacity = self.rank*2
                self.cells = {
                    "cell 1":"empty",
                    "cell 2":"empty",
                    "cell 3":"empty",
                    "cell 4":"empty",
                    "cell 5":"empty",
                    "cell 6":"empty",
                    "cell 7":"empty",
                    "cell 8":"empty",
                    "cell 9":"empty",
                    "cell 10":"empty",
                    "solitary confinement 1":"empty",
                    "solitary confinement 2":"empty",
                }

            if self.type == "research lab":
                self.current_project = "none"
                self.research_progress = 0.00
                self.completed_projects = []
                
                def complete_research(self, project):
                    if self.research_progress == 1:
                        self.completed_projects.append(self.current_project)
                        self.current_project = "none"
                        self.research_progress = 0
            
            if self.type == "drug lab":
                pass


if startup: #load specifics 
    if startup: #create handlers
        selected = Selected()
        overlay = Overlay_Manager("cockpit")
        mission = Mission_Manager()
        dialogue = Dialogue_Manager()
        plot = Story_Manager()
        group = Group_Manager()
        image = Image_Holder()
        scene = Scene_Manager()
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
        unassigned_pilot = Pilot("Unassigned",0,copy.deepcopy(tower),"vanguard")
        nighthawk = Pilot("Nighthawk",1,copy.deepcopy(majestic),"vanguard")
        kite = Pilot("kite",2,copy.deepcopy(majestic),"vanguard")
        saint = Pilot("saint",3,copy.deepcopy(majestic),"vanguard")
        deadlift = Pilot("Deadlift",4,copy.deepcopy(majestic),"vanguard")
        kite = Pilot("Azure_Kite",5,copy.deepcopy(majestic),"vanguard")
        shadowstalker = Pilot("Shadowstalker",6,copy.deepcopy(majestic),"vanguard")
        null_pilot = Pilot(" ",-1,copy.deepcopy(null_suit),"vanguard")
        group.pilot_roster = [unassigned_pilot, nighthawk, kite, saint, deadlift, kite,shadowstalker]
        selected.pilot = group.pilot_roster[0]
        null_pilot.pos_x = -1
        null_pilot.pos_y = -1
        tower_1 = Pilot("Tower",1,copy.deepcopy(tower),"enemy")
        benny = Pilot(" ",-1,copy.deepcopy(null_suit),"vanguard")
        samuel = Pilot(" ",-1,copy.deepcopy(null_suit),"vanguard")
    if startup: #load Pilot sprites
        mission.pilots.add(unassigned_pilot)
        mission.pilots.add(nighthawk)
        mission.pilots.add(kite)
        mission.pilots.add(saint)
        mission.pilots.add(deadlift)
        mission.pilots.add(kite)
        mission.pilots.add(tower_1)
        nighthawk.battlesuit.loadout[1] = cryo_shot
        kite.battlesuit.loadout[1] = cryo_shot
    #update inventory
    if startup: #load inventory
        group.inventory = [fusion_core, beam_cannon, light_shield, light_shield, null_weapon, null_weapon, null_weapon]
    if startup: #load buttons
        group.buttons.add(Button("x_button"))
        group.buttons.add(Button("dashboard_map"))
        group.pilot_nameplates.add(Button("dispatch_button"))
        group.inventory_nameplates.add(Button("swap_button"))
        group.inventory_text_names.add(Short_Text("swap_button",0))
        group.buttons.add(Button("continue_button"))
        group.text_objects.add(Short_Text("continue_button",0))
    if startup: #load resources
        credits_currency = 0
        scrap_metal = 0
        fuel_rods = 0
        meds = 0
        stimms = 0
    if startup: #add nameplates
        group.pilot_nameplates.add(Nameplates("pilot_line_item",1))
        group.pilot_nameplates.add(Nameplates("pilot_line_item",2))
        group.pilot_nameplates.add(Nameplates("pilot_line_item",3))
        group.pilot_nameplates.add(Nameplates("pilot_line_item",4))
        group.pilot_nameplates.add(Nameplates("pilot_line_item",5))

        group.inventory_nameplates.add(Nameplates("inventory_line_item",1))
        group.inventory_nameplates.add(Nameplates("inventory_line_item",2))
        group.inventory_nameplates.add(Nameplates("inventory_line_item",3))

        group.inventory_nameplates.add(Nameplates("loadout_label", 0))
        group.inventory_nameplates.add(Nameplates("loadout_label", 1))
        group.inventory_nameplates.add(Nameplates("loadout_label", 3))
        group.inventory_nameplates.add(Nameplates("loadout_label", 2))
        group.inventory_nameplates.add(Nameplates("loadout_label", 4))
    if startup: #add island maps
        group.islands.add(Island("world_map",0))
        group.islands.add(Island("island",1))
        group.islands.add(Island("island",2))
        group.islands.add(Island("island",3))
        group.islands.add(Island("island",4))
        group.islands.add(Island("island",5))
        group.islands.add(Island("island",6))
    if startup: #add text names
        group.pilot_text_names.add(Short_Text("Pilot",1))
        group.pilot_text_names.add(Short_Text("Pilot",2))
        group.pilot_text_names.add(Short_Text("Pilot",3))
        group.pilot_text_names.add(Short_Text("Pilot",4))
        group.pilot_text_names.add(Short_Text("Pilot",5))
        group.pilot_text_names.add(Short_Text("dispatch_button",0))
        
        group.pilot_text_stats.add(Short_Text("stats",1))
        group.pilot_text_stats.add(Short_Text("stats",2))
        group.pilot_text_stats.add(Short_Text("stats",3))
        group.pilot_text_stats.add(Short_Text("stats",4))
        group.pilot_text_stats.add(Short_Text("stats",5))

        group.loadout_text_names.add(Short_Text("loadout",1))
        group.loadout_text_names.add(Short_Text("loadout",2))
        group.loadout_text_names.add(Short_Text("loadout",3))
        group.loadout_text_names.add(Short_Text("loadout",4))
        group.loadout_text_names.add(Short_Text("loadout",0))
        
        group.inventory_text_names.add(Short_Text("inventory",1))
        
        group.pilot_combat_names.add(Short_Text("Pilot",1))
        group.pilot_combat_names.add(Short_Text("Pilot",2))
        group.pilot_combat_names.add(Short_Text("Pilot",3))
        group.pilot_combat_names.add(Short_Text("Pilot",4))
        group.pilot_combat_names.add(Short_Text("Pilot",5))
    if startup: #add health icons
        for pilot in mission.pilots:
            if pilot.slot_number > 0:
                group.health_icons.add(Health_Icon("shield", pilot))
                group.health_icons.add(Health_Icon("damaged", pilot))
                group.health_icons.add(Health_Icon("severely_damaged", pilot))
    if startup: #add pointers
        group.mission_pointers.add(Pointer("rail", screen_width*0.6,screen_height*0.7,1))  

#Mission 1 setup
selected.active_mission_number = 1
# mission.mission_setup(1)

map_center = Map_Center()

while True: #game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_t:
                for pilot in group.pilot_roster: pilot.teleport()
            
            #enable debug mode
            if event.key == pygame.K_q:
                if debug_mode == False: 
                    debug_mode = True
                    print("debug_mode enabled")
                
                
            #disable debug mode
            if event.key == pygame.K_z:
                if debug_mode == True: 
                    debug_mode = False
                    print("debug_mode disabled")
            
            #make dialogue choices
            if overlay.type == "dialogue" and dialogue.choices_available == True:
                if event.key == pygame.K_1: dialogue.advance_scene(1)
            
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
            
            if event.key == pygame.K_l:
                overlay.type = "level_select"
                                    
            if overlay.type == "level_select":
                if event.key == pygame.K_1:
                    mission.mission_setup(1)
                    overlay.type = "combat"
                if event.key == pygame.K_2:
                    mission.mission_setup(2)
                    overlay.type = "combat"
                
    scene.update()
    mission.update()
    overlay.update()
    
    # if overlay.type == "dialogue" and len(scene.scene_queue) > 0: print("current scene:", scene.scene_queue[0])
        
    fps_text = update_fps()
    if debug_mode == True: screen.blit(fps_text, (centerpoint)) #display fps
    pygame.display.update()
    clock.tick(60)

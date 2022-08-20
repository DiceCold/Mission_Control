import pygame
from sys import exit
import os
import copy
import random
from math import atan2, degrees, pi

scroll_velocity = 3
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

red_dot_surf = pygame.image.load('graphics/interface/icons/red_dot.png')
blue_dot_surf = pygame.image.load('graphics/interface/icons/blue_dot.png')
# laserbeam_surf = pygame.image.load('graphics/weapons/laserbeam_half.png')
# laserbeam_surf = pygame.transform.scale(laserbeam_surf,(20,1000))
# laser_rotation = -180
# laserbeam_rotated = pygame.transform.rotate(laserbeam_surf,laser_rotation)
# laserbeam_rect = laserbeam_rotated.get_rect(center = (centerpoint))
blank_frame = pygame.image.load('graphics/blank.png')





class Map_Tile(pygame.sprite.Sprite):
    def __init__(self, type, bot_y):
        super().__init__()
        if type == "grass_texture":
            self.bot_y = bot_y
            map_tile_1 = pygame.image.load('graphics/maps/grass_texture.png').convert_alpha()
            map_tile_1 = pygame.transform.scale(map_tile_1, (screen_width,screen_height))
            self.rect = map_tile_1.get_rect(bottomleft = (0,self.bot_y))
            self.image = map_tile_1
    def map_scroll(self):
        global scroll_velocity
        self.rect.y += scroll_velocity
    def update(self):
        self.map_scroll()
        if self.rect.top >= screen_height:
            self.rect.bottom = 0

def load_map_scroll_sprites():
    global map_tile_group
    map_tile_group  = pygame.sprite.Group()
    map_tile_group.add(Map_Tile("grass_texture", screen_height))
    map_tile_group.add(Map_Tile("grass_texture", 0))
    global scroll_velocity
    scroll_velocity = 5



        
        
            
rose = (Pilot("Rose","friend"))
nighthawk = (Pilot("Nighthawk","enemy"))
null_pilot = (Pilot("null_pilot","enemy"))
pilot_group.add(rose)
pilot_group.add(nighthawk)
pilot_group.add(null_pilot)


def attack():
    if self.weapons[0].cooldown == 0:
        if abs(self.target_distance_x) < 30 and abs(self.target_distance_y) <30:
            find_target_angle()
            self.attack_visual()
            roll_to_hit()
            weapon_cooldown = 200

def roll_to_hit():
    global target
    global hit_successful
    hit_roll = random.randint(1,20) + weapon.accuracy
    difficulty = target.mobility    
    if hit_roll > difficulty:
        print("Hit")
        hit_successful = True
        if target.shields == True:
            target.shields = False
        elif target.battlesuit_damaged == False:
            target.battlesuit_damaged = True
        elif target.battlesuit_heavilly_damaged == False:
            target.battlesuit_heavilly_damaged = True
        else:
            target.injured = True
    else: 
        print("Miss")
        hit_successful = False     
   

class Weapon(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        if type == "laserbeam":
            self.rotation = rose.target_angle - 90
            self.frame_1 = pygame.image.load('graphics/weapons/laserbeam_half.png')
            self.frame_1 = pygame.transform.scale(self.frame_1,(20,rose.target_distance_h*2.1))
            self.frame_1 = pygame.transform.rotate(self.frame_1,self.rotation)
            self.frame_0 = blank_frame
            self.frames = [self.frame_0,self.frame_1]
            self.animation_index = 0
            self.image = self.frames[self.animation_index]
            self.rect = self.image.get_rect(center = (rose.pos_x,rose.pos_y))
            self.cooldown_max = 120
            self.countdown_max = 60
        self.cooldown = 0
        self.countdown = self.countdown_max
    def update(self):
        if self.cooldown >= 0:
            self.cooldown -= 1
            self.animation_index = 0
        if self.cooldown == 0:
            self.countdown = self.countdown_max
        if self.countdown >= 0:
            self.countdown -= 1
            self.animation_index = 1
        if self.countdown == 0:
            self.cooldown = self.cooldown_max
        if self.type == "laserbeam":
            if self.animation_index == 1:
                self.rotation = rose.target_angle - 90
                self.frame_1 = pygame.image.load('graphics/weapons/laserbeam_half.png')
                self.frame_1 = pygame.transform.scale(self.frame_1,(20,rose.target_distance_h*2.1))
                self.frame_1 = pygame.transform.rotate(self.frame_1,self.rotation)
                self.frame_0 = blank_frame
                self.frames = [self.frame_0,self.frame_1]
                self.image = self.frames[self.animation_index]
                self.rect = self.image.get_rect(center = (rose.pos_x,rose.pos_y))
            if self.animation_index == 0:
                self.image = blank_frame
                        
weapons_group = pygame.sprite.Group()
laserbeam_weapon = Weapon("laserbeam")
rose.weapon = laserbeam_weapon
weapons_group.add(rose.weapon)

while True: #game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
    screen.fill((0,0,0))
    pilot_group.update()
    weapons_group.update()
    weapons_group.draw(screen)
    pilot_group.draw(screen)
    pygame.display.update()
    clock.tick(30)
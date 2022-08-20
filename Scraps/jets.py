#Jet fighting
import pygame
from draw_screen import draw_jet
from equipment import *
angle = 0
rotation = 0

def jet_attack():
    if jet.weapons[0].cooldown == 0:
        if abs(jet_target_distance_x) < 30 and abs(jet_target_distance_y) <30:
            find_target_angle()
            jet_attack_visual()
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
        

def jet_targeting_distance():
    global jet_target_distance_x
    global jet_target_distance_y
    global jet_target_distance_h
    jet_target_distance_x = target.pos_x - jet.pos_x
    jet_target_distance_y = target.pos_y - jet.pos_y
    jet_target_distance_h = (jet_target_distance_x**2 + jet_target_distance_y**2)**(1/2)
    
    
def jet_maneuver():
    #change velocity
    global jet
    global jet_target_distance_x
    global jet_target_distance_y
    # if jet.battlesuit_damaged == True:
        # jet.momentum_x += 0.01*jet_target_distance_x
    if jet_target_distance_x >= 0:
        jet.momentum_x += 0.01
        jet.momentum_x += 0.002*jet_target_distance_x
    else:
        jet.momentum_x -= 0.01
        jet.momentum_x -= 0.002*abs(jet_target_distance_x) 
    if jet_target_distance_y >= 0:
        jet.momentum_y += 0.001
        jet.momentum_y += 0.01*jet_target_distance_y
    else:
        jet.momentum_y -= 0.002*abs(jet_target_distance_y)
        jet.momentum_y -= 0.01
    #speed limit
    if abs(jet.momentum_x) > 10:
        jet.momentum_x *= 0.9
    if abs(jet.momentum_y) >10:
        jet.momentum_y *= 0.9
   
    #update positions
    jet.pos_y = (jet.pos_y + jet.momentum_y*0.1*jet.mobility)
    jet.pos_x = (jet.pos_x + jet.momentum_x*0.1*jet.mobility)
    jet.rect = jet.image.get_rect(center = (int(jet.pos_x), int(jet.pos_y)))
    
class WeaponEffects(pygame.sprite.Sprite):
    def __init__(self, type, rotation):
        super().__init__()
        if type == "laserbeam":
            laser1 = pygame.image.load('graphics/laserbeam.png').convert_alpha()
            laser1 = pygame.transform.scale(laser1, 5,5)
            self.image = laser1
        self.rect = self.image.get_rect(midbottom = (jet.pos_x, jet.pos_y))
        self.rotation = rotation
        self.image = pygame.transform.rotate(self.image,self.angle)
        self.countdown = 60
    def update(self):
        length = (jet_target_distance_x**2 + jet_target_distance_y**2)**(1/2)
        self.image = pygame.transform.scale(self.image, 5, length)
        self.angle = find_target_angle() - self.angle
        self.image = pygame.transform.rotate(self.image,self.angle)
        self.countdown -= 1
        if self.countdown <= 0:
            self.kill
        
weapon_effect_group = pygame.sprite.Group()            
    
    
def jet_attack_visual():
    if target_hostile == True:
            weapon_effect_group.add(WeaponEffects("laserbeam", angle))


    
def find_target_angle():
    if jet_target_distance_x < 0:
        angle_1 = jet_target_distance_y/abs(jet_target_distance_x)
        degrees = 90 + angle_1*90
        farpoint = (jet_target_distance_x*100,jet_target_distance_y*100)
    if jet_target_distance_x >= 0:
        angle_1 = (jet_target_distance_y)/abs(jet_target_distance_x)
        degrees = 270 + angle_1*90
    angle = degrees
    return angle
        
    

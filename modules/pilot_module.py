import pygame
from settings import *
from math import atan2, degrees, pi, inf
import random


def find_distance(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pox_y - origin.pos_y
    distance_h = (distance_x**2 + distance_y**2)**0.5
    return distance_h


def find_angle(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pos_y - origin.pos_y
    
    rads = atan2(-distance_y, distance_x)
    rads %= 2*pi
    angle = degrees(rads) 
    return angle


class Waypoint:
    def __init__(self, pos_x, pos_y):
        self.type = "waypoint"
        self.pos_x = pos_x
        self.pos_y = pos_y


class Pilot(pygame.sprite.Sprite):
    def __init__(self, name, data_file):
        super().__init__()
        self.name = name
        # import core information from data file
        try:
            data = data_file[f"{self.name}"]
        except(Exception, ):
            data = data_file["default"]
        self.pilot_id = data["pilot_id"]
        self.faction = data["faction"]
        # determine dot color based on faction
        if self.faction == "vanguard":
            self.image = pygame.image.load("graphics/interface/blue_dot.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (screen_width*0.01, screen_width*0.01))

        self.feats = data["feats"]
        self.chassis = data["chassis"]
        self.loadout = data["loadout"]
        self.mood = "default"

        self.attributes = data["attributes"]
        try:
            self.evasion_score = data["evasion_score"]
        except(Exception, ):
            self.evasion_score = 10
        try:
            self.accuracy_score = data["accuracy_score"]
        except(Exception, ):
            self.accuracy_score = 0

        self.on_mission = False
        self.targeting_mode = "automatic"
        self.orders = "aggressive_focus"

        self.pos_x = -1
        self.pos_y = -1
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 12
        
        # set color of the pilots dot based on faction
        if self.faction == "vanguard":
            self.color = (0, 0, 255)
        elif self.faction == "hive":
            self.color = (255, 0, 0)
        else:
            self.color = (255, 255, 255)
        
        # set health status
        self.injured = False
        self.suit_damaged = False
        self.suit_damaged_severely = False
        self.alive = True
        self.shielded = False
        self.invulnerable_timer = 0
        self.invulnerable_timer_max = 60

        # targeting
        self.target = {
            "attack": None,
            "move": None
            }
        self.target_list = {
            "enemies": [],
            "objectives": []
        }

    def tick_invulnerable_timer(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def find_target(self, target_list):
        # checks to find the closest target
        new_target = None
        new_target_distance = float(inf)
        for target in target_list:
            distance = find_distance(self, target)
            if distance <= new_target_distance:
                new_target = target
                new_target_distance = distance
        return new_target

    def maneuver(self, multiplier = 1):
        # update velocity
        if self.target["move"] is not None:
            if self.pos_x < self.target["move"].pos_x:
                self.velocity_x += 0.1
            else:
                self.velocity_x -= 0.1

            if self.pos_y < self.target["move"].pos_y:
                self.velocity_y += 0.1
            else:
                self.velocity_y -= 0.1
        
        # speed limit
        if abs(self.velocity_x) > self.max_speed:
            self.velocity_x *= 0.9
        if abs(self.velocity_y) > self.max_speed:
            self.velocity_y *= 0.9
                
        # update position
        self.pos_x = self.pos_x + self.velocity_x * multiplier
        self.pos_y = self.pos_y + self.velocity_y * multiplier

    def attack(self, item, target):
        # reset item cooldown
        item.cooldown = item.cooldown_max

        # roll to hit vs evasion
        target_number = target.evasion_score
        hit_roll = random.randint(1, 20)
        if hit_roll >= target_number:
            target.take_damage(item.damage_type)
            self.spawn_visual_effect(item.visual, self, self.attack_target)

    def use_item(self):
        for item in self.loadout:
            if item.cooldown == 0:
                if item.item_type == "weapon":
                    # check distance, and whether target has invuln_timer
                    # get values
                    target = self.target["attack"]
                    try:
                        attack_distance = find_distance(self, target)
                    except(Exception, ):
                        attack_distance = float(inf)
                    try:
                        invuln_timer = target.invuln_timer
                    except(Exception, ):
                        invuln_timer = float(inf)
                    # check values
                    if attack_distance < item.attack_range and invuln_timer == 0:
                        self.attack(item, target)
                
                elif item.type == "shield" and not self.shielded:
                    # check cooldown on shield
                    if item.cooldown == 0:
                        # restore shields and put item on cooldown
                        self.shielded = True
                        item.cooldown = item.cooldown_max
                
                # making movement item based allows suits to use multiple movement modules
                elif item.type == "movement":
                    self.pos_x += (self.velocity_x * item.mobility)
                    self.pos_y += (self.velocity_y * item.mobility)

    def take_damage(self, damage_type):
        # reset invuln timer
        self.invulnerable_timer = self.invulnerable_timer_max
        # check shields
        if self.shielded:
            self.shielded = False
        elif not self.suit_damaged:
            self.suit_damaged = True
        elif not self.suit_damaged_severely:
            self.suit_damaged_severely = True
        elif not self.injured:
            self.injured = True
        else:
            self.alive = False
        # kill pilot if not alive
        if not self.alive:
            self.kill()

    def draw_dot(self):
        pygame.draw.circle(screen, self.color, (self.pos_x, self.pos_y), screen_width*0.01)

    def update(self):
        # movement
        if self.targeting_mode == "automatic":
            self.target["move"] = self.find_target(self.target_list["enemies"])
            self.target["attack"] = self.find_target("attack")
        self.maneuver()


class MissionManager:
    def __init__ (self):
        self.pilots = pygame.sprite.Group()

        

        
    
            
    # def spawn_drones(quantity, pos_x, pos_y, position_variance, team):
    #     if quantity == "1d6": quantity = random.randint(1,6)
    #     while quantity > 0:
    #         drone = Navigator("drone", copy.deepcopy(drone_suit), team)
    #         drone.pos_x = pos_x + random.randint(-position_offset, position_variance)
    #         drone.pos_y = pos_y + random.ranint(-position_offset, position_variance)
    #         self.pilots.add(drone)
            
    def spawn_waypoint(self, pos_x, pos_y):
        self.waypoints.add(Waypoint(pos_x, pos_y))
        
    # def spawn_train(pos_x, pos_y):
    #     train = Navigator("train", "train", copy.deepcopy(train_suit), "vanguard")
    #     train.pos_x = pos_x
    #     train.pos_y = pos_y
    #     self.pilots.add(train)
            
    def reset(self):
        self.pilots.empty()
        self.objectives.empty()
        self.waypoints.empty()
        self.terrain.empty()
        self.biome = "desert"
        # for pilot in game.pilot_roster: pilot.on_mission = False
        
    def load(self, name):
        if name == "mission 1: train attack":
            #  waypoints for train
            self.spawn_waypoint(screen_width*0.2, screen_height*0.2)
            self.spawn_waypoint(screen_width*0.6, screen_height*0.3)
            self.spawn_waypoint(screen_width*0.3, screen_height*0.5)
            self.spawn_waypoint(screen_width*0.6, screen_height*0.6)
            self.spawn_waypoint(screen_width*0.2, screen_height*0.9)
            self.spawn_waypoint(screen_width*1.2, screen_height*0.7)
            # spawn train
            self.spawn_train(screen_width*0.15, screen_height*0.15)


#
import pygame
from settings import *
from math import atan2, degrees, pi, inf
import random
import json
import modules.navigation_module as nav
from modules.vfx_module import VisualEffect
from modules.items import Item


def find_distance(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pos_y - origin.pos_y
    distance_h = (distance_x**2 + distance_y**2)**0.5
    return distance_h


def find_angle(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pos_y - origin.pos_y
    
    rads = atan2(-distance_y, distance_x)
    rads %= 2*pi
    angle = degrees(rads) 
    return angle


# parent class for pilots, enemies, etc (WIP)
class MobileEntity(pygame.sprite.Sprite):
    def __init__(self, name, entity_type, faction, pos_x=-1, pos_y=-1):
        super().__init__()
        self.name = name
        self.entity_type = entity_type
        self.faction = faction

        # set position and velocity
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_speed = 4

        # set health status
        self.injured = False
        self.suit_damaged = False
        self.suit_damaged_severely = False
        self.hp_max = 100
        self.hp_current = self.hp_max
        self.alive = True
        self.shielded = True
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
        # set targeting mode (may not be relevant for non-pilots)
        self.targeting_mode = "automatic"

        # create vfx group
        self.vfx_group = pygame.sprite.Group()

    def update_items(self):
        for item in self.loadout:
            item.update()

    def tick_invulnerable_timer(self):
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def find_target(self, target_list):
        # checks to find the closest target
        new_target = None
        new_target_distance = float(inf)
        # try:
        for target in target_list:
            distance = find_distance(self, target)
            if distance <= new_target_distance:
                new_target = target
                new_target_distance = distance

        # default to center of map if pilot has no target
        if new_target is None:
            new_target = nav.Waypoint(screen_width * 0.5, screen_height * 0.5)
            # print(f"{self.name} is targeting middle of the map")
            # print(self.name, "is at", self.pos_x, self.pos_y)
        return new_target

    def maneuver(self, multiplier=1):
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
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def spawn_vfx(self, origin, target, vfx_type, damage_type, ttl=60):
        visual_effect = VisualEffect(vfx_type, damage_type, origin, target, ttl)
        self.vfx_group.add(visual_effect)

    def update_vfx(self):
        self.vfx_group.update()

    def draw_vfx(self):
        self.vfx_group.draw(screen)

    def attack(self, item, target):
        # reset item cooldown
        item.cooldown = item.cooldown_max

        # roll to hit vs evasion
        target_number = target.evasion_score
        hit_roll = random.randint(1, 20)
        if hit_roll >= target_number:
            target.take_damage(item.damage_type)
            self.spawn_vfx(self, target, item.weapon_type, item.damage_type)

    def use_items(self):
        for item in self.loadout:
            if item.cooldown == 0:
                if item.item_type == "weapon":
                    # check distance, and whether target has invulnerable_timer
                    # get values
                    target = self.target["attack"]
                    if target is not None:
                        attack_distance = find_distance(self, target)
                    else:
                        attack_distance = inf
                    try:
                        invulnerable_timer = target.invulnerable_timer
                    except(Exception,):
                        invulnerable_timer = float(inf)
                    # check values
                    if attack_distance < item.attack_range[1] and invulnerable_timer == 0:
                        self.attack(item, target)

                elif item.item_type == "shield" and not self.shielded:
                    # check cooldown on shield
                    if item.cooldown == 0:
                        # restore shields and put item on cooldown
                        self.shielded = True
                        item.cooldown = item.cooldown_max

                # making movement item based allows suits to use multiple movement modules
                elif item.item_type == "movement":
                    self.pos_x += (self.velocity_x * item.mobility)
                    self.pos_y += (self.velocity_y * item.mobility)

    def take_damage(self, damage_type, damage_amount=10):
        # reset invuln timer
        self.invulnerable_timer = self.invulnerable_timer_max
        # check shields
        if self.shielded:
            self.shielded = False
        # reduce hp if not shielded
        elif self.hp_current > 0:
            self.hp_current -= damage_amount
        else:
            self.alive = False
        # kill pilot if not alive
        if not self.alive:
            self.kill()


class Enemy(MobileEntity):
    def __init__(self, enemy_type, pos_x=-1, pos_y=-1, faction="iron_hive"):
        super().__init__(enemy_type, "enemy", faction)
        self.faction = faction
        self.name = enemy_type

        # load the data file
        data_file = json.load(open("data/enemy_data.json", "r"))
        data = data_file[f"{enemy_type}"]

        # import loadout from data file
        try:
            self.loadout = data["loadout"]
        except(Exception, ):
            self.loadout = []
        # import stats from data file
        try:
            self.evasion_score = data["evasion_score"]
            self.accuracy_score = data["accuracy_score"]
            self.hp_max = data["hp_max"]
            self.max_speed = data["max_speed"]
            self.size = data["size"]
        except(Exception, ):
            self.evasion_score = 10
            self.accuracy_score = 0
            self.hp_max = 100
            self.max_speed = 4
            self.size = 0.01
            print("Error: unable to load stats from data file")

        # set dimensions
        self.width = screen_width*0.01 * self.size
        self.height = self.width

        # load image
        self.image = pygame.image.load("graphics/icons/red_dot_icon.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        # load rect
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def update(self):
        # movement
        self.target["move"] = self.find_target(self.target_list["enemies"])
        self.target["attack"] = self.find_target(self.target_list["enemies"])
        self.maneuver()

        # update vfx
        self.update_vfx()
        
        self.tick_invulnerable_timer()


class Pilot(MobileEntity):
    def __init__(self, name):
        super().__init__(name, "pilot", "vanguard")
        self.name = name

        # import information from data file
        data_file = json.load(open("data/pilot_data.json", "r"))
        pilot_data = data_file["pilot_data"]
        try:
            data = pilot_data[f"{self.name}"]
        except(Exception, ):
            data = pilot_data["default"]
        self.pilot_id = data["pilot_id"]
        self.faction = data["faction"]

        # import loadout
        self.loadout = []
        for i in data["loadout"]:
            loadout_item = Item(i["item_name"], i["item_type"])
            print("loading item", i["item_name"], i["item_type"])
            self.loadout.append(loadout_item)

        # set mood
        self.mood = "default"

        self.attributes = data["attributes"]
        self.evasion_score = data["evasion_score"]
        self.accuracy_score = data["accuracy_score"]

        self.on_mission = False
        self.orders = "aggressive_focus"
        self.highlighted = False
        self.selected = False
        self.overcharge_system = {
            "red": True,
            "blue": False,
            "green": False
        }

        # set dimensions
        self.width = screen_width * 0.01
        self.height = self.width
        
        # set color of the pilots dot based on faction
        self.image_blue = pygame.image.load("graphics/icons/blue_dot_icon.png").convert_alpha()
        self.image_blue = pygame.transform.scale(self.image_blue, (self.width, self.height))
        self.image_white = pygame.image.load("graphics/icons/white_dot_icon.png").convert_alpha()
        self.image_white = pygame.transform.scale(self.image_white, (self.width, self.height))
        self.image_red = pygame.image.load("graphics/icons/red_dot_icon.png").convert_alpha()
        self.image_red = pygame.transform.scale(self.image_red, (self.width, self.height))

        if self.faction == "vanguard":
            self.image = self.image_blue
        else:
            self.image = self.image_white

        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def deselect(self):
        self.selected = False
        self.highlighted = False
        # reset color
        if self.faction == "vanguard" and self.image != self.image_blue:
            self.image = self.image_blue

    def handle_highlight(self):
        if self.faction == "vanguard":
            if self.selected or self.highlighted:
                self.image = self.image_white
            else:
                self.image = self.image_blue
        if self.faction == "iron_hive":
            self.image = self.image_red

    def update(self):
        # change color from blue to white if highlighted
        if self.selected:
            print(self.name, "currently selected")
        self.handle_highlight()
        if self.selected:
            print(self.name, "currently selected")

        # movement
        if self.targeting_mode == "automatic":
            self.target["move"] = self.find_target(self.target_list["enemies"])
            self.target["attack"] = self.find_target(self.target_list["enemies"])
        self.maneuver()

        # tick invuln
        self.tick_invulnerable_timer()

        # update items
        self.update_items()
        self.use_items()

        # update vfx
        self.update_vfx()


    # def load(self, name):
    #     if name == "mission 1: train attack":
    #         #  waypoints for train
    #         self.spawn_waypoint(screen_width*0.2, screen_height*0.2)
    #         self.spawn_waypoint(screen_width*0.6, screen_height*0.3)
    #         self.spawn_waypoint(screen_width*0.3, screen_height*0.5)
    #         self.spawn_waypoint(screen_width*0.6, screen_height*0.6)
    #         self.spawn_waypoint(screen_width*0.2, screen_height*0.9)
    #         self.spawn_waypoint(screen_width*1.2, screen_height*0.7)
    #         # spawn train
    #         self.spawn_train(screen_width*0.15, screen_height*0.15)


target_dummy = Pilot("target_dummy")

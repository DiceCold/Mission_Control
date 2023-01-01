import pygame
from math import atan2, degrees, pi
from settings import *
import random
from modules.vfx_module import VisualEffect
import json

debug_mode = False


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


class Item:
    def __init__(self, name, item_type):
        self.item_type = item_type
        self.name = name
        data_file = json.load(open("data/item_data.json", "r"))
        # load data depending on item type
        if self.item_type == "weapon":
            weapon_data = data_file["weapons"]
            data = weapon_data[name]
        elif self.item_type == "shield":
            shield_data = data_file["shields"]
            data = shield_data[name]

        # set attributes from data
        # weapon
        if self.item_type == "weapon":
            try:
                self.cooldown_max = data["cooldown"]
                self.damage_type = data["damage_type"]
                self.weapon_type = data["weapon_type"]
                # placeholder
                self.attack_range = [0, screen_width*0.3]
            except(Exception, ):
                self.cooldown_max = 100
                self.damage_type = "thermal"
                self.weapon_type = "beam"
                self.attack_range = [0, screen_width*0.3]
                print("error loading weapon data from file")
        # shield
        elif self.item_type == "shield":
            self.cooldown_max = data["cooldown"]
        # placeholder for mobility
        elif self.item_type == "mobility":
            self.cooldown_max = 100
        else:
            print("invalid item type")

        # set current cooldown to max
        self.cooldown = self.cooldown_max

        # elif self.item_type == "movement":
        #     # set default mobility
        #     self.mobility = 1
        #
    def update(self):
        # reduce cooldown
        if self.cooldown > 0:
            self.cooldown -= 1

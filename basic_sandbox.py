# sandbox

# import pygame
# import random
from sys import exit
# import os
# import copy
from math import atan2, degrees, pi
import json
import modules.interface as module_interface
import modules.pilot_module as pilot_module
import modules.mission_module as mission_module
from modules.settings import *
import modules.shop as module_shop

# press q to toggle debug mode
# press s to toggle shop if debug mode is enabled
print("Welcome to the Mission Control Demo")
print("To toggle debug mode, press 'q'")
print("To toggle shop while debug is enabled, press 's'")
print("To toggle combat while debug is enabled, press 'x'")
print("To set combat to the testing setup press 'z' while combat is enabled.")
print("To return to cockpit while debug is enabled, press 'c'")


def create_rect(x, y, width, height):
    rect = pygame.Rect(screen_width * x, screen_height * y, screen_width * width, screen_height * height)
    return rect


def find_distance(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pox_y - origin.pos_y
    distance_h = (distance_x ** 2 + distance_y ** 2) ** 0.5
    return distance_h


def find_angle(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pos_y - origin.pos_y

    rads = atan2(-distance_y, distance_x)
    rads %= 2 * pi
    angle = degrees(rads)
    return angle


class GameManager:
    def __init__(self):
        self.focus = "cockpit"
        self.scene_id = "intro"
        self.debug_mode = False

        self.click_cooldown_max = 15
        self.click_cooldown = self.click_cooldown_max

        self.missions_available = []
        self.missions_completed = []

        self.pilot_roster = pygame.sprite.Group()
        self.player_inventory = []
        self.player_resources = {
            "Credits": 2000,
            "Fuel": 10,
            "Scrap": 10,
            "Meds": 10
        }

    def run_combat(self):
        if self.focus == "combat":
            mission.pilots.update()
            mission.enemies.update()

    def update_graphics(self):
        graphics.draw_black()
        if self.focus == "shop":
            graphics.draw_window_frames()
            graphics.draw_shop_headers()
            # shop.highlight_shop_items()
            # shop.draw_shop_item_text()
            shop.update_shop_items()
        elif self.focus == "cockpit":
            graphics.draw_cockpit()
        elif self.focus == "combat":
            # mission.pilots.draw_dot()
            # mission.enemies.draw_dot()
            for pilot in mission.pilots:
                pygame.draw.circle(screen, pilot.color, (pilot.pos_x, pilot.pos_y), screen_width * 0.005)
            for pilot in mission.enemies:
                pygame.draw.circle(screen, pilot.color, (pilot.pos_x, pilot.pos_y), screen_width * 0.005)

        if game.focus != "cockpit":
            graphics.draw_green()

    def update(self):
        if self.click_cooldown > 0:
            self.click_cooldown -= 1
        mission.update()
        self.update_graphics()


# class Pilot(pygame.sprite.Sprite):
#     def __init__(self, name, data_file):
#         super().__init__()
#         self.name = name
#         data = data_file[f"{self.name}"]
#         self.pilot_id = data["pilot_id"]
#         self.faction = data["faction"]
#         self.attributes = data["attributes"]
#         self.feats = data["feats"]
#         self.chassis = data["chassis"]
#         self.loadout = data["loadout"]
#         self.mood = "default"
#
#         self.pos_x = -1
#         self.pos_y = -1
#         self.momentum_x = 0
#         self.momentum_y = 0


game = GameManager()
mission = mission_module.MissionManager()
shop = module_shop.ShopManager()
graphics = module_interface.GraphicsManager()

# pilots
pilot_data = json.load(open("data/pilot_data.json", "r"))


kite = pilot_module.Pilot("Kite")
nasha = pilot_module.Pilot("Nasha")
roger = pilot_module.Pilot("Roger")
game.pilot_roster.add(kite)
game.pilot_roster.add(nasha)
game.pilot_roster.add(roger)


while True:  # game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            # toggle debug mode
            if event.key == pygame.K_q:
                if not game.debug_mode:
                    game.debug_mode = True
                    print("debug_mode enabled")
                elif game.debug_mode:
                    game.debug_mode = False
                    print("debug_mode disabled")
            if game.debug_mode:
                if event.key == pygame.K_s:
                    if game.focus != "shop":
                        game.focus = "shop"
                        print("shop enabled with debug_mode")
                    else:
                        game.focus = "cockpit"
                        print("shop disabled with debug_mode")
                elif event.key == pygame.K_x:
                    if game.focus != "combat":
                        game.focus = "combat"
                        print("combat enabled with debug_mode")
                    else:
                        game.focus = "cockpit"
                        print("combat disabled with debug_mode")
                elif event.key == pygame.K_c:
                    game.focus = "cockpit"

            # load combat test
            if game.debug_mode and game.focus == "combat":
                if event.key == pygame.K_z:
                    mission.load_pilot_for_test_mission(kite)
                    mission.load_pilot_for_test_mission(nasha)
                    mission.load_enemy_for_test_mission(roger)

        if event.type == pygame.MOUSEBUTTONDOWN and game.click_cooldown == 0:
            for item in shop.shop_items:
                item.add_to_cart(game, shop)

    game.update()
    pygame.display.update()
    clock.tick(60)

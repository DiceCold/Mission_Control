# sandbox

import pygame
import random
from sys import exit
import os
import copy
from math import atan2, degrees, pi
import json
import modules.interface as module_interface
from modules.settings import *
import modules.shop as module_shop

# press q to toggle debug mode
# press s to toggle shop if debug mode is enabled


def create_rect(x, y, width, height):
    rect = pygame.Rect(screen_width * x, screen_height * y, screen_width * width, screen_height * height)
    return rect


class GameManager:
    def __init__(self):
        self.shop_active = True
        self.combat_active = False
        self.scene_id = "intro"
        self.debug_mode = False
        self.click_cooldown_max = 15
        self.click_cooldown = self.click_cooldown_max
        self.player_inventory = []
        self.player_resources = {
            "Credits": 2000,
            "Fuel": 10,
            "Scrap": 10,
            "Meds": 10
        }

    def update_graphics(self):
        graphics.draw_black()
        if self.shop_active:
            graphics.draw_window_frames()
            graphics.draw_shop_headers()
            # shop.highlight_shop_items()
            # shop.draw_shop_item_text()
            shop.update_shop_items()

        graphics.draw_green()

    def update(self):
        if self.click_cooldown > 0:
            self.click_cooldown -= 1
        self.update_graphics()


class Pilot:
    def __init__(self, name):
        self.name = name
        self.mood = "default"


game = GameManager()
shop = module_shop.ShopManager()
graphics = module_interface.GraphicsManager()

# pilots
kite = Pilot("Kite")
nasha = Pilot("Nasha")
roger = Pilot("Roger")

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
                    if not game.shop_active:
                        game.shop_active = True
                        print("shop enabled with debug_mode")
                    else:
                        game.shop_active = False
                        print("shop disabled with debug_mode")

        if event.type == pygame.MOUSEBUTTONDOWN and game.click_cooldown == 0:
            for item in shop.shop_items:
                item.add_to_cart(game, shop)

    game.update()
    pygame.display.update()
    clock.tick(60)

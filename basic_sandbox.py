# sandbox

# import pygame
# import random
from sys import exit
# import os
# import copy
from math import atan2, degrees, pi
import json
import modules.graphics_module as graphics_module
import modules.pilot_module as pilot_module
import modules.mission_module as mission_module
from modules.settings import *
import modules.shop as module_shop
import modules.ui_module as ui

# press q to toggle debug mode
# press s to toggle shop if debug mode is enabled
print("Welcome to the Mission Control Demo")
print("To toggle debug mode, press 'q'")
print("To toggle shop while debug is enabled, press 's'")
print("To toggle combat while debug is enabled, press 'x'")
print("To set combat to the testing setup press 'z' while combat is enabled.")
print("To return to cockpit while debug is enabled, press 'c'")
print("To pause or unpause combat press space")


def load_combat_test():
    print("loading combat test")
    mission.load_pilot_for_test_mission(rose)
    # mission.load_pilot_for_test_mission(nasha)
    mission.load_enemy_for_test_mission(roger)
    mission_data_file = json.load(open("data/mission_data.json", "r"))
    mission.load_mission("test_mission", mission_data_file)


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


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = text_font.render(fps, 1, pygame.Color("coral"))
    return fps_text


class GameManager:
    def __init__(self):
        self.focus = "cockpit"
        self.scene_id = "intro"
        self.selected_pilot = None
        self.debug_mode = False
        self.paused = False

        self.click_cooldown_max = 15
        self.click_cooldown = self.click_cooldown_max

        self.missions_available = []
        self.missions_completed = []

        self.buttons = pygame.sprite.Group()
        self.button_labels = pygame.sprite.Group()

        self.create_button("default_button", "test_button", screen_width*0.5, screen_height*0.5)

        self.pilot_roster = pygame.sprite.Group()
        self.player_inventory = []
        self.player_resources = {
            "Credits": 2000,
            "Fuel": 10,
            "Scrap": 10,
            "Meds": 10
        }

    def create_button(self, button_type, text, pos_x, pos_y, width=screen_width * 0.2, height=screen_height * 0.15):
        button = ui.Button(button_type, pos_x, pos_y, width, height)
        self.buttons.add(button)
        label = ui.TextLabel("button", button, text)
        self.button_labels.add(label)

    def highlight_pilot(self):
        mouse_pos = pygame.mouse.get_pos()
        for pilot in mission.pilots:
            if pilot.rect.left < mouse_pos[0] < pilot.rect.right and pilot.rect.top < mouse_pos[1] < pilot.rect.bottom:
                if not pilot.highlighted:
                    pilot.highlighted = True
            else:
                if pilot.highlighted:
                    pilot.highlighted = False

            if pilot.highlighted or pilot.selected:
                print(pilot.name, pilot.highlighted, pilot.selected)
                pilot.image = pygame.image.load("graphics/icons/white_dot_icon.png").convert_alpha()
                pilot.image = pygame.transform.scale(pilot.image, (pilot.width, pilot.height))
            else:
                pilot.image = pygame.image.load("graphics/icons/blue_dot_icon.png").convert_alpha()
                pilot.image = pygame.transform.scale(pilot.image, (pilot.width, pilot.height))

    def select_pilot(self):
        for pilot in mission.pilots:
            if pilot.highlighted:
                pilot.selected = True
                self.selected_pilot = pilot
                print(f"{pilot.name} selected")

    def highlight_button(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            if button.status != "hidden":
                rect = button.rect
                # highlight if mouse collides with rect
                if rect.left < mouse_pos[0] < rect.right and rect.top < mouse_pos[1] < rect.bottom:
                    button.status = "highlight"
                else:
                    button.status = "default"

    def click_button(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button.rect.collidepoint(event.pos) and button.active and button.cooldown == 0:
                    button.click_button()

    def run_combat(self):
        # update ally and enemy pilots while game is running
        if self.focus == "combat" and game.paused is False:
            # update ally and enemy pilots
            mission.pilots.update()
            mission.enemies.update()
        # highlight and select a pilot if the game is paused
        if self.focus == "combat" and game.paused:
            if self.selected_pilot is None:
                # highlights the pilot on mouseover if one is not currently selected
                self.highlight_pilot()
                # selects the pilot if mouse is clicked while they are highlighted
                if event.type == pygame.MOUSEBUTTONDOWN and self.click_cooldown == 0:
                    self.click_cooldown = self.click_cooldown_max
                    self.select_pilot()
            # issues orders for a pilot if they are currently selected and the player clicks on the map
            # current functionality only allows you to set a target location rather than a target pilot
            if self.selected_pilot is not None:
                if event.type == pygame.MOUSEBUTTONDOWN and self.click_cooldown == 0:
                    self.click_cooldown = self.click_cooldown_max
                    mission.issue_orders(self.selected_pilot, "waypoint")

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
            mission.pilots.draw(screen)
            graphics.draw_terrain(mission.terrain)
            for pilot in mission.enemies:
                pygame.draw.circle(screen, pilot.color, (pilot.pos_x, pilot.pos_y), screen_width * 0.005)

            # draw crosshair
            if self.paused and self.selected_pilot is not None:
                try:
                    target = self.selected_pilot.target["move"]
                    graphics.draw_crosshair(target.pos_x, target.pos_y)
                except(Exception,):
                    pass

        self.buttons.draw(screen)
        self.button_labels.draw(screen)

        if game.focus != "cockpit":
            graphics.draw_green()

    def update(self):
        if self.click_cooldown > 0:
            self.click_cooldown -= 1
        if game.focus == "combat":
            # mission.update()
            self.run_combat()
        # update buttons
        self.highlight_button()
        self.click_button()
        self.buttons.update()
        self.button_labels.update()
        # render graphics on screen
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
graphics = graphics_module.GraphicsManager()

# pilots
pilot_data = json.load(open("data/pilot_data.json", "r"))

rose = pilot_module.Pilot("rose")
rose.target["move"] = mission_module.Waypoint(screen_width*0.5, screen_height*0.5)
rose.targeting_mode = "manual"
nasha = pilot_module.Pilot("Nasha")
roger = pilot_module.Pilot("Roger")
game.pilot_roster.add(rose)
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
                    load_combat_test()

            # pause and unpause combat
            if event.key == pygame.K_SPACE and game.focus == "combat":
                if not game.paused:
                    game.paused = True
                    print("Combat has been paused")
                else:
                    game.paused = False
                    game.selected_pilot = None
                    for pilot in mission.pilots:
                        pilot.selected = False
                    print("Combat has been unpaused")

        if event.type == pygame.MOUSEBUTTONDOWN and game.click_cooldown == 0:
            for item in shop.shop_items:
                item.add_to_cart(game, shop)

    game.update()
    pygame.display.update()
    clock.tick(60)

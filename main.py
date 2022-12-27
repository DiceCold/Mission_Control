# sandbox

# import pygame
# import random
from sys import exit
# import os
# import copy
import json
import modules.graphics_module as graphics_module
import modules.pilot_module as pilot_module
import modules.mission_module as mission_module
from modules.settings import *
import modules.shop as module_shop
import modules.ui_module as ui_module
import modules.navigation_module as nav

# press q to toggle debug mode
# press s to toggle shop if debug mode is enabled
print("Welcome to the Mission Control Demo")
print("To toggle debug mode, press 'q'")
print("To toggle shop while debug is enabled, press 's'")
print("To toggle combat while debug is enabled, press 'x'")
print("To set combat to the testing setup press 'z' while combat is enabled.")
print("To return to cockpit while debug is enabled, press 'c'")
print("To pause or unpause combat press space")


# def create_rect(x, y, width, height):
#     rect = pygame.Rect(screen_width * x, screen_height * y, screen_width * width, screen_height * height)
#     return rect


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = text_font.render(fps, 1, pygame.Color("coral"))
    return fps_text


class GameManager:
    def __init__(self):
        self.mode = "cockpit"
        self.scene_id = "intro"
        self.debug_mode = False
        self.paused = False

        # load managers
        self.ui = ui_module.InterfaceManager(self)
        self.mission = mission_module.MissionManager(self)

        # self.ui.create_button("default_button", "test_button", screen_width*0.5, screen_height*0.5)

        self.pilots = pygame.sprite.Group()

        self.player_inventory = []
        self.player_resources = {
            "Credits": 2000,
            "Fuel": 10,
            "Scrap": 10,
            "Meds": 10
        }

    def update_graphics(self):
        graphics.draw_black()
        if self.mode == "shop":
            graphics.draw_window_frames()
            graphics.draw_shop_headers()
            # shop.highlight_shop_items()
            # shop.draw_shop_item_text()
            shop.update_shop_items()
        elif self.mode == "cockpit":
            graphics.draw_cockpit()
        elif self.mode == "combat":
            mission.pilots.draw(screen)
            graphics.draw_terrain(mission.terrain)

            # draw crosshair
            if self.paused and self.ui.selected_pilot is not None:
                try:
                    target = self.ui.selected_pilot.target["move"]
                    graphics.draw_crosshair(target.pos_x, target.pos_y)
                except(Exception,):
                    pass

        # self.ui.buttons.draw(screen)
        # self.ui.button_labels.draw(screen)

        if game.mode != "cockpit":
            graphics.draw_green()

    def update(self):
        if game.mode == "combat":
            self.mission.run_combat()

        # update ui
        self.ui.update()

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
mission = game.mission
shop = module_shop.ShopManager()
graphics = graphics_module.GraphicsManager()

# pilots
pilot_data = json.load(open("data/pilot_data.json", "r"))

rose = pilot_module.Pilot("rose")
rose.target["move"] = nav.Waypoint(screen_width*0.5, screen_height*0.5)
rose.targeting_mode = "manual"
nasha = pilot_module.Pilot("Nasha")
roger = pilot_module.Pilot("Roger")
game.pilots.add(rose)
game.pilots.add(nasha)
game.mission.enemies.add(roger)

while True:  # game Cycle
    mouse_pos = pygame.mouse.get_pos()

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
                    if game.mode != "shop":
                        game.mode = "shop"
                        print("shop enabled with debug_mode")
                    else:
                        game.mode = "cockpit"
                        print("shop disabled with debug_mode")
                elif event.key == pygame.K_x:
                    if game.mode != "combat":
                        game.mode = "combat"
                        print("combat enabled with debug_mode")
                    else:
                        game.mode = "cockpit"
                        print("combat disabled with debug_mode")
                elif event.key == pygame.K_c:
                    game.mode = "cockpit"

            # load combat test
            if game.debug_mode and game.mode == "combat":
                if event.key == pygame.K_z:
                    mission.load_combat_test()

            # pause and unpause combat
            if event.key == pygame.K_SPACE and game.mode == "combat":
                if not game.paused:
                    game.paused = True
                    print("Combat has been paused")
                else:
                    game.paused = False
                    game.selected_pilot = None
                    for pilot in mission.pilots:
                        pilot.selected = False
                    print("Combat has been unpaused")

        # click to select
        if event.type == pygame.MOUSEBUTTONDOWN and game.ui.click_cooldown == 0:
            # reset cooldown
            game.ui.reset_cooldown()

            # select button by clicking
            for button in game.ui.buttons:
                if button.rect.collidepoint(event.pos) and button.status != "hidden":
                    button.click_button()

            # select pilot by clicking
            if game.mode == "combat" and game.paused:
                for pilot in game.pilots:
                    # check if mouse is on pilot
                    if pilot.rect.collidepoint(event.pos):
                        # select the pilot if not currently selected
                        if pilot != game.ui.selected_pilot:
                            game.ui.select_pilot(pilot)
                        # deselect the pilot if already selected
                        else:
                            game.ui.deselect_pilot(pilot)

            # issue orders to waypoint if pilot is selected
            if game.ui.selected_pilot is not None:
                pilot = game.ui.selected_pilot
                mouse_pos = pygame.mouse.get_pos()
                print("issuing orders")
                ui_module.issue_orders(game.ui.selected_pilot, "waypoint", mouse_pos)
                # reset cooldown
                game.ui.click_cooldown = game.ui.click_cooldown_max

        # if event.type == pygame.MOUSEBUTTONDOWN and game.ui.click_cooldown == 0:
        #     for item in shop.shop_items:
        #         item.add_to_cart(game, shop)

    game.update()

    pygame.display.update()
    clock.tick(60)

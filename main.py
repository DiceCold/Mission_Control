
# import pygame
import random
from sys import exit
# import os
# import copy
import json

import pygame.sprite

import modules.graphics_module as graphics_module
import modules.pilot_module as pilot_module
import modules.mission_module as mission_module
from settings import *
import modules.shop as module_shop
import modules.ui_module as ui_module
import modules.navigation_module as nav
from modules.vfx_module import VisualEffect
import modules.sound_module as sound_module

# press q to toggle debug mode
# press s to toggle shop if debug mode is enabled
print("Welcome to the Mission Control Demo")
print("To toggle debug mode, press 'q'")
print("To toggle shop while debug is enabled, press 's'")
print("To toggle combat while debug is enabled, press 'x'")
print("To set combat to the testing setup press 'z' while combat is enabled.")
print("To return to cockpit while debug is enabled, press 'c'")
print("To pause or unpause combat press space")
print("To toggle the menu press 'o'")
print("To toggle pilot frames press 'p'")


# def create_rect(x, y, width, height):
#     rect = pygame.Rect(screen_width * x, screen_height * y, screen_width * width, screen_height * height)
#     return rect

def toggle_hidden(manager, name):
    if manager.hidden:
        manager.hidden = False
        print(f"{name} is now active")
    else:
        manager.hidden = True
        print(f"{name} is now hidden")


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
        self.sound = sound_module.SoundController()

        # self.ui.create_button("default_button", "test_button", screen_width*0.5, screen_height*0.5)

        self.pilots = pygame.sprite.Group()

        self.player_inventory = []
        self.player_resources = {
            "Credits": 2000,
            "Fuel": 10,
            "Scrap": 10,
            "Meds": 10
        }

        self.vfx_group = pygame.sprite.Group()

    def spawn_explosion(self, origin):
        explosion = VisualEffect("explosion", None, origin, origin)
        self.vfx_group.add(explosion)
        self.sound.play_sound("explosion")

    def spawn_lightning(self, origin):
        lightning = VisualEffect("lightning", None, origin, origin)
        self.vfx_group.add(lightning)

    def draw_vfx_group(self):
        self.vfx_group.draw(screen)

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
            # draw terrain
            graphics.draw_terrain(mission.terrain)

            # draw mobile entities
            game.pilots.draw(screen)
            game.mission.enemies.draw(screen)

            # draw vfx
            for pilot in game.pilots:
                pilot.draw_vfx()
            for enemy in game.mission.enemies:
                enemy.draw_vfx()

            # draw crosshair
            if self.paused and self.ui.selected_pilot is not None:
                try:
                    target = self.ui.selected_pilot.target["move"]
                    graphics.draw_crosshair(target.pos_x, target.pos_y)
                except(Exception,):
                    pass

            # draw explosions
            # temp
            try:
                if self.mode == "combat":
                    if self.paused is False:
                        self.vfx_group.update()
                    self.vfx_group.draw(screen)
            except(Exception,):
                pass

        # self.ui.buttons.draw(screen)
        # self.ui.button_labels.draw(screen)

        if game.mode != "cockpit":
            graphics.draw_green()

        # draw the menu if it's not hidden
        if not game.ui.menu.hidden:
            self.ui.menu.draw_menu()

        # draw a character frame on the left side of the screen for each pilot if not hidden
        if not game.ui.status_frame_manager.hidden:
            self.ui.status_frame_manager.draw_status_frames()

    def explode_mobs(self):
        for mob in game.pilots:
            if not mob.alive:
                self.spawn_explosion(mob)
                mob.kill()
        for mob in game.mission.enemies:
            if not mob.alive:
                self.spawn_explosion(mob)
                mob.kill()

    def update(self):
        if game.mode == "combat":
            self.mission.run_combat()
            self.explode_mobs()

        # update ui
        self.ui.update()

        # render graphics on screen
        self.update_graphics()


game = GameManager()
mission = game.mission
shop = module_shop.ShopManager()
graphics = graphics_module.GraphicsManager()
game.sound.play_music("me_map")

# pilots
pilot_data = json.load(open("data/pilot_data.json", "r"))

rose = pilot_module.PilotCharacter("Rose")
rose.target["move"] = nav.Waypoint(screen_width*0.5, screen_height*0.5)
rose.targeting_mode = "manual"
nasha = pilot_module.PilotCharacter("Nasha")
# roger = pilot_module.PilotCharacter("Roger")
game.pilots.add(rose)
game.pilots.add(nasha)
# game.mission.load_enemy_for_test_mission(roger)
game.mission.spawn_enemy("drone", 500, 500)
rose.pos_y = 500
rose.pos_x = 500

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
                    # toggle shop
                    if game.mode != "shop":
                        game.mode = "shop"
                        print("shop enabled with debug_mode")
                    else:
                        game.mode = "cockpit"
                        print("shop disabled with debug_mode")
                # toggle combat
                elif event.key == pygame.K_x:
                    if game.mode != "combat":
                        game.mode = "combat"
                        # switch to combat music
                        game.sound.play_music("me_rude_awakening")
                        print("combat enabled with debug_mode")
                    else:
                        game.mode = "cockpit"
                        # switch to map music
                        game.sound.play_music("me_map")
                        print("combat disabled with debug_mode")
                # return to cockpit
                elif event.key == pygame.K_c:
                    game.mode = "cockpit"
                    # switch to map music
                    game.sound.play_music("me_map")
                # toggle menu
                elif event.key == pygame.K_o:
                    toggle_hidden(game.ui.menu, "menu")
                    game.ui.menu.update_menu_options(game.ui.selected_pilot)

                # toggle pilot_status_frames
                elif event.key == pygame.K_p:
                    toggle_hidden(game.ui.status_frame_manager, "pilot_status_frames")

            # load combat test
            if game.debug_mode and game.mode == "combat":
                if event.key == pygame.K_z:
                    mission.load_combat_test()

            # temp function to test teleport
            if event.key == pygame.K_t:
                game.mission.teleport_pilot(rose)

            # pause and unpause combat
            if event.key == pygame.K_SPACE and game.mode == "combat":
                if not game.paused:
                    game.paused = True
                    game.ui.selected_pilot = None
                    print("Combat has been paused")
                else:
                    game.paused = False
                    game.ui.selected_pilot = None
                    for pilot in game.pilots:
                        pilot.deselect()
                    print("Combat has been unpaused")

        # click to select
        if event.type == pygame.MOUSEBUTTONDOWN and game.ui.click_cooldown == 0:
            # reset cooldown
            game.ui.reset_cooldown()

            # select button by clicking
            for button in game.ui.buttons:
                if button.rect.collidepoint(event.pos) and button.status != "hidden":
                    button.click_button()

            # toggle overcharge lights
            for pilot_frame in game.ui.status_frame_manager.status_frame_group:
                if not game.ui.status_frame_manager.hidden:
                    for button in pilot_frame.light_group:
                        if button.rect.collidepoint(event.pos):
                            button.click_button()
                            print(pilot_frame.pilot.overcharge_system)
                    for button in pilot_frame.toggle_group:
                        if button.rect.collidepoint(event.pos):
                            button.click_button()

            # toggle automatic control mode

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
                # deselect all but the most recently selected pilot
                for pilot in game.pilots:
                    if game.ui.selected_pilot != pilot:
                        pilot.selected = False

            # issue orders to waypoint if pilot is selected
            if game.ui.selected_pilot is not None:
                pilot = game.ui.selected_pilot
                mouse_pos = pygame.mouse.get_pos()
                if pilot.targeting_mode == "manual":
                    print("issuing orders to", pilot.name)
                ui_module.issue_orders(game.ui.selected_pilot, "waypoint", mouse_pos)
                # reset cooldown
                # game.ui.click_cooldown = game.ui.click_cooldown_max

        # if event.type == pygame.MOUSEBUTTONDOWN and game.ui.click_cooldown == 0:
        #     for item in shop.shop_items:
        #         item.add_to_cart(game, shop)

    game.update()

    pygame.display.update()
    clock.tick(60)



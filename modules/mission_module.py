# import pygame
import random
import modules.pilot_module as pilot_module
from settings import *

class Waypoint:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y


class MissionManager:
    def __init__(self):
        self.pilots = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.objectives = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.ally_factions = ["vanguard"]
        self.enemy_factions = ["iron_hive"]
        self.selected_pilot = None

        self.map_momentum_x = 0
        self.map_momentum_y = 0
        self.map_offset_x = 0
        self.map_offset_y = 0

    def load_pilot_for_test_mission(self, pilot):
        pilot.pos_x = random.randint(screen_width*0.25, screen_width*0.75)
        pilot.pos_y = random.randint(screen_height*0.25, screen_height*0.75)
        pilot.target_list["enemies"] = self.enemies
        print(f"Adding {pilot.name} to scene at ({pilot.pos_x}, {pilot.pos_y})")
        self.pilots.add(pilot)

    def load_enemy_for_test_mission(self, enemy):
        enemy.pos_x = random.randint(screen_width * 0.25, screen_width * 0.75)
        enemy.pos_y = random.randint(screen_height * 0.25, screen_height * 0.75)
        enemy.faction = "iron_hive"
        enemy.color = (255, 0, 0)
        enemy.target_list["enemies"] = self.pilots
        print(f"Adding enemy pilot {enemy.name} to scene at ({enemy.pos_x}, {enemy.pos_y})")
        self.enemies.add(enemy)

    def reset(self):
        for pilot in self.pilots:
            pilot.on_mission = False
        self.pilots.empty()
        self.objectives.empty()
        self.waypoints.empty()
        self.terrain.empty()

    def highlight_pilot(self):
        mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
        for pilot in self.pilots:
            if pilot.rect.left < mouse_pos[0] < pilot.rect.right and pilot.rect.top < mouse_pos[1] < pilot.rect.bottom:
                if pilot.highlighted == False:
                    pilot.highlighted = True
            else:
                if pilot.highlighted:
                    pilot.highlighted = False

            if pilot.highlighted or pilot.selected:
                pilot.image = pygame.image.load("graphics/icons/white_dot_icon.png").convert_alpha()
                pilot.image = pygame.transform.scale(pilot.image, (pilot.width, pilot.height))
            else:
                pilot.image = pygame.image.load("graphics/icons/blue_dot_icon.png").convert_alpha()
                pilot.image = pygame.transform.scale(pilot.image, (pilot.width, pilot.height))

    def select_pilot(self):
        for pilot in self.pilots:
            if pilot.highlighted:
                pilot.selected = True
                self.selected_pilot = pilot
                print(f"{pilot.name} selected")

    def issue_orders(self, target_type):
        pilot = self.selected_pilot
        pilot.targeting_mode = "manual"
        if target_type == "waypoint":
            mouse_pos = pygame.mouse.get_pos()
            pilot.target["move"] = Waypoint(mouse_pos[0], mouse_pos[1])

            print(f"{pilot.name} is targeting waypoint {mouse_pos}")

    def update(self):
        # self.pilots.update()
        # self.enemies.update()
        pass


class MissionObjective:
    def __init__(self, objective_type, name, pos_x, pos_y):
        super().__init__()

        self.objective_type = objective_type
        self.name = name

        self.pos_x = pos_x
        self.pos_y = pos_y

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

    def load_mission(self, mission_name, data_file):
        mission_data = data_file[mission_name]
        self.terrain.empty()
        terrain_objects_data = mission_data["terrain_objects"]
        for terrain_object in terrain_objects_data:
            object_type = terrain_object["object_type"]
            pos_x = terrain_object["pos_x"]*screen_width
            pos_y = terrain_object["pos_y"]*screen_height
            self.terrain.add(TerrainObject(self, object_type, pos_x, pos_y))

    def reset(self):
        for pilot in self.pilots:
            pilot.on_mission = False
        self.pilots.empty()
        self.objectives.empty()
        self.waypoints.empty()
        self.terrain.empty()

    def issue_orders(self, pilot, target_type):
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


class TerrainObject(pygame.sprite.Sprite):
    def __init__(self, manager, object_type, pos_x, pos_y, width=screen_width*0.1, height=screen_width*0.1):
        super().__init__()

        self.manager = manager
        self.type = object_type
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.animation_index = 1
        self.repel_force = 4

        self.frame_0 = pygame.image.load("graphics/blank.png").convert_alpha()

        if self.type == "mountain":
            self.frame_1 = pygame.image.load("graphics/icons/mountain.png").convert_alpha()
            self.frames = [self.frame_0, self.frame_1]

        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def repel(self, pilot_list):
        for pilot in list:
            if self.rect.collidepoint((pilot.pos_x, pilot.pos_y)):
                # keep Pilot's momentum but direct away from the terrain object
                if pilot.pos_x < self.pos_x:
                    pilot.momentum_x = abs(pilot.momentum_x)
                else:
                    pilot.momentum_x = abs(pilot.momentum_x) * -1

    def update(self):
        # self.repel(self.manager.pilots)
        # self.repel(self.manager.enemies)
        pass

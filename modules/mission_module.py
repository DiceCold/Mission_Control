# import pygame
import random
from settings import *


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

    def reset(self):
        for pilot in self.pilots:
            pilot.on_mission = False
        self.pilots.empty()
        self.objectives.empty()
        self.waypoints.empty()
        self.terrain.empty()

    def update(self):
        self.pilots.update()
        self.enemies.update()


class MissionObjective:
    def __init__(self, objective_type, name, pos_x, pos_y):
        super().__init__()

        self.objective_type = objective_type
        self.name = name

        self.pos_x = pos_x
        self.pos_y = pos_y

# import pygame
from settings import *


class MissionManager:
    def __init__(self):
        self.pilots = pygame.sprite.Group()
        self.objectives = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.ally_factions = ["vanguard"]
        self.enemy_factions = ["iron_hive"]

        self.map_momentum_x = 0
        self.map_momentum_y = 0
        self.map_offset_x = 0
        self.map_offset_y = 0

    def reset(self):
        for pilot in self.pilots:
            pilot.on_mission = False
        self.pilots.empty()
        self.objectives.empty()
        self.waypoints.empty()
        self.terrain.empty()


class MissionObjective:
    def __init__(self, objective_type, name, pos_x, pos_y):
        super().__init__()

        self.objective_type = objective_type
        self.name = name

        self.pos_x = pos_x
        self.pos_y = pos_y

# import pygame
import random
import modules.pilot_module as pilot_module
import modules.navigation_module as nav
from settings import *
import json


class MissionManager:
    def __init__(self, game_manager):
        self.game = game_manager
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

        self.missions_available = []
        self.missions_completed = []

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
        enemy.target_list["enemies"] = self.pilots
        print(f"Adding enemy pilot {enemy.name} to scene at ({enemy.pos_x}, {enemy.pos_y})")
        self.enemies.add(enemy)

    def spawn_enemy(self, enemy_type, pos_x=-1, pos_y=-1, faction="iron_hive"):
        enemy = pilot_module.Enemy(enemy_type, pos_x, pos_y, faction)
        print(f"Adding enemy {enemy.name} to scene at ({enemy.pos_x}, {enemy.pos_y})")
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

    def run_combat(self):
        game = self.game
        # update ally and enemy pilots while game is running
        if game.mode == "combat" and game.paused is False:
            # update ally and enemy pilots
            self.pilots.update()
            self.enemies.update()

            # issues orders for a pilot if they are currently selected and the player clicks on the map
            # current functionality only allows the player to set a target location rather than a target pilot

    def load_combat_test(self):
        print("loading combat test")
        for pilot in self.game.pilots:
            print(pilot.name)
            self.load_pilot_for_test_mission(pilot)
            # mission.load_pilot_for_test_mission(nasha)
            # self.load_enemy_for_test_mission(roger)
        mission_data_file = json.load(open("data/mission_data.json", "r"))
        self.load_mission("test_mission", mission_data_file)


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

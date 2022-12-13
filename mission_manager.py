import pygame
import random
from settings import *


class MissionManager:
    def __init__(self):
        self.objectives = pygame.sprite.Group()
        self.waypoints = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.terrain = pygame.sprite.Group()
        self.biome = "desert"

        # not currently in use but stored for future missions where the map is scrolling
        self.map_velocity_x = 0
        self.map_velocity_y = 0
        self.map_offset_x = 0
        self.map_offset_y = 0

    def reset(self):
        pass

    def spawn_random_crates(self, quantity):
        while quantity > 0:
            pos_x = random.ranint(screen_width*0.2, screen_width*0.8)
            pos_y = random.randint(screen_height*0.2, screen_height*0.8)
            self.objectives.add(Objective("pickup", "supply_crate", pos_x, pos_y))
            quantity -= 1


class Objective:
    def __init__(self, objective_type, objective_id, pos_x, pos_y):
        super().__init__()

        # objective types include pickup, collectable, and repair_point
        self.objective_type = objective_type
        self.objective_id = objective_id

        self.pos_x = pos_x
        self.pos_y = pos_y

        self.link = None
        self.link_radius = screen_width*0.01

        self.progress_min = 0
        self.progress_max = 100
        self.progress = 0

        self.animation_index = 1
        self.frame_0 = pygame.image.load("graphics/blank.png")

        # define appearance of supply_crate objects
        if self.objective_id == "supply_crate":
            self.width = screen_width * 0.05
            self.height = screen_width * 0.05
            self.frame_1 = pygame.image.load("graphics/interface/icons/box_closed.png")
            self.frame_2 = pygame.image.load("graphics/interface/icons/box_open.png")
            self.frames = [self.frame_0, self.frame_1, self.frame_2]

        if self.objective_type == "train":
            self.width = screen_width*0.05
            self.height = screen_width*0.05
            self.frame_1 = pygame.image.load("graphics/icons/blue_dot.png")

        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))

    # def establish_link(self):
    #     #search for unlinked pilots active on the mission
    #     for pilot in mission.pilots:
    #         if pilot.link == "empty" and self.link == "empty":
    #             #check distance
    #             if abs(self.pos_x - pilot.pos_x) < self.link_radius and abs(self.pos_y - pilot.pos_y) < self.link_radius:
    #                 #assign link to Pilot and objective
    #                 pilot.link = self
    #                 self.link = pilot
    #             else: pass

    def pull(self, pilot):
        #pull tethered Pilot closer, becoming stronger as distance decreases
        if pilot.pos_x < self.pos_x: pilot.velocity_x += self.pull_strength/abs(self.pos_x - pilot.pos_x)
        elif pilot.pos_x > self.pos_x: pilot.velocity_x -= self.pull_strength/abs(self.pos_x - pilot.pos_x)

        if pilot.pos_y < self.pos_y: pilot.velocity_y += self.pull_strength/abs(self.pos_y - pilot.pos_y)
        elif pilot.pos_y > self.pos_y: pilot.velocity_y -= self.pull_strength/abs(self.pos_y - pilot.pos_y)

    def manage_link(self):
        if self.link != "empty":
            pilot = self.link

            #unlink if the Pilot is injured or dead
            if pilot.injured == True or pilot.alive == False: self.link = "empty"

            #draw tether to linked Pilot
            pygame.draw.line(screen, (80,80,80), (self.pos_x, self.pos_y), (pilot.pos_x, pilot.pos_y, 10))

    def track_progress(self):
        #fill
        if self.link != "empty" and self.progress < self.progress_max: self.progress += 1
        #empty
        elif self.link == "empty" and self.progress_min < self.progress: self.progress -= 1
        #follow linked Pilot with y offset if progress is full
        elif self.link != "empty" and self.progress == self.progress_max:
            self.pos_x = self.link.pos_x
            self.pos_y = self.link.pos_y + screen_height*0.05

    def update(self):
        #update image and rect
        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(center = (self.pos_x, self.pos_y))

        #update link
        if self.link == "empty": self.establish_link()
        elif self.link != "empty":
            #pull Pilot if not at 100% progress
            if self.progress < self.progress_max:
                try: self.pull(self.link)
                except:
                    print("Error:", self.objective_id, "was unable to pull linked Pilot", self.link.objective_id)

            try: self.manage_link()
            except:
                print("Error: there was a problem managing link between", self.objective_id, "and", self.link.objective_id)

        #update progress
        self.track_progress()


import pygame
from settings import *
from math import atan2, degrees, pi, inf
import modules.navigation_module as nav
import random


class VisualEffect(pygame.sprite.Sprite):
    def __init__(self, vfx_type, damage_type, origin, target, ttl=60):
        super().__init__()
        self.vfx_type = vfx_type
        self.damage_type = damage_type
        self.origin = origin
        self.target = target
        self.ttl = ttl

        if self.vfx_type == "beam":
            # set size and angle
            self.length = nav.find_distance(self.origin, self.target)*2.05
            # doubled length because graphic has invisible bottom half so its pivot-point is correct
            # alternatively could create method to find pivot point as average between the origin and target positions
            self.width = screen_width * 0.03
            self.angle = nav.find_angle(self.origin, self.target)

            # set image based on damage type
            if self.damage_type == "thermal":
                self.default_image = pygame.image.load("graphics/effects/laserbeam_thin_half.png").convert_alpha()
            elif self.damage_type == "cryo":
                self.default_image = pygame.image.load("graphics/effects/ice_laser.png").convert_alpha()

            self.image = pygame.transform.scale(self.default_image, (self.width, self.length))
            self.image = pygame.transform.rotate(self.image, self.angle)
            self.rect = self.image.get_rect(center=(self.origin.pos_x, self.origin.pos_y))

        elif self.vfx_type == "projectile":
            pass

    def update_beam(self):
        self.length = nav.find_distance(self.origin, self.target)*2.05
        # doubled length because graphic has invisible bottom half so its pivot-point is correct
        self.angle = nav.find_angle(self.origin, self.target)
        self.image = pygame.transform.scale(self.default_image, (self.width, self.length))
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=(self.origin.pos_x, self.origin.pos_y))

    def update(self):
        # update rect
        self.rect = self.image.get_rect(center=(self.origin.pos_x, self.origin.pos_y))
        # update image
        if self.vfx_type == "beam":
            self.update_beam()
        # reduce time to live (ttl) and delete if time is 0
        if self.ttl > 0:
            self.ttl -= 1
        elif self.ttl == 0:
            self.kill()
#
# class VisualEffect(pygame.sprite.Sprite):
#     def __init__(self, effect_type, damage_type, origin, target, countdown_max):
#         super().__init__()
#         self.effect_type = effect_type
#         self.damage_type = damage_type
#         self.origin = origin
#         self.target = target
#         self.countdown_max = 20
#         self.countdown = self.countdown_max
#
#         self.blank_image = pygame.image.load("graphics/blank.png").convert_alpha()
#         self.frames = []
#         self.animation_index = 1
#         self.image = self.blank_image
#         self.length = self.find_distance(self.origin, self.target) * 2.1
#         # doubled because graphic has invisible bottom half so its pivot-point is correct
#         self.angle = self.find_angle(origin, target)
#
#
#
#         # flame thrower
#         if self.effect_type == "burst" and self.damage_type == "thermal":
#             self.name = "flamer"
#             self.frame_0 = self.blank_image
#             self.frame_1 = pygame.image.load("graphics/effects/fire1.png").convert_alpha()
#             self.frame_2 = pygame.image.load("graphics/effects/fire2.png").convert_alpha()
#             self.frame_3 = pygame.image.load("graphics/effects/fire3.png").convert_alpha()
#             self.frame_4 = pygame.image.load("graphics/effects/fire4.png").convert_alpha()
#             self.frame_5 = pygame.image.load("graphics/effects/fire5.png").convert_alpha()
#             self.frame_6 = pygame.image.load("graphics/effects/fire6.png").convert_alpha()
#             self.frame_7 = pygame.image.load("graphics/effects/fire7.png").convert_alpha()
#             self.frame_8 = pygame.image.load("graphics/effects/fire8.png").convert_alpha()
#             self.frames = [self.frame_0, self.frame_1, self.frame_2, self.frame_3, self.frame_4, self.frame_5,
#                            self.frame_6, self.frame_7, self.frame_8]
#             self.countdown_max = 60
#             self.image = self.frames[self.animation_index]
#
#         # explosion
#         if self.effect_type == "explosion":
#             self.name = "explosion"
#             explosion_sheets = [explosion_sheet_1, explosion_sheet_2, explosion_sheet_3, explosion_sheet_4]
#             self.animation_index = 0
#             # self.frames = explosion_frames
#             # self.image = self.blank_image
#             self.countdown_max = 64
#             self.sheet = random.choice(explosion_sheets)
#             self.sheet_column = 0
#             self.sheet_row = 0
#
#         # teleport
#         if self.effect_type == "teleport":
#             self.name = "teleport"
#             teleport_sheet = pygame.image.load("graphics/effects/teleport_explosion.png").convert_alpha()
#             self.animation_index = 0
#             # self.frames = explosion_frames
#             # self.image = self.blank_image
#             self.countdown_max = 64
#             self.sheet = teleport_sheet
#             self.sheet_column = 0
#             self.sheet_row = 0
#
#         self.countdown = self.countdown_max
#         self.image = pygame.transform.rotate(self.image, self.angle)
#         self.rect = self.image.get_rect(center=(self.origin.pos_x, self.origin.pos_y))
#
#     def draw_explosion(self, sheet, height, column, row):
#         screen.blit(sheet, (self.origin.pos_x - height * 0.5, self.origin.pos_y - height * 0.5),
#                     (height * column, height * row, height, height))
#
#     def draw_teleport(self, sheet, height, column, row):
#         screen.blit(sheet, (self.origin.pos_x - height * 0.5, self.origin.pos_y - height * 0.5),
#                     (height * column, height * row, height, height))
#
#     def find_distance(self, origin, target):
#         distance_x = target.pos_x - origin.pos_x
#         distance_y = target.pos_y - origin.pos_y
#         distance_h = (distance_x ** 2 + distance_y ** 2) ** (1 / 2)
#         return distance_h
#
#     def find_angle(self, origin, target):
#
#         distance_x = target.pos_x - origin.pos_x
#         distance_y = target.pos_y - origin.pos_y
#
#         rads = atan2(-distance_y, distance_x)
#         rads %= 2 * pi
#         angle = degrees(rads) - 90
#
#         return angle
#
#     def update(self):
#
#         if debug_mode == True:
#             try:
#                 print(self.name, self.animation_index, self.length, self.width)
#             except:
#                 print(self.name, "has no width")
#
#         if self.length > screen_width:
#             if debug_mode == True: print("excessive length", self.origin.name, self.target.name)
#             self.length = screen_width
#
#         # update countdown
#         if self.countdown <= 0:
#             if debug_mode == True: print("End effect:", self.name)
#             self.kill()
#         else:
#             self.countdown -= 1
#
#         # explosion
#         if self.effect_type == "explosion":
#             self.sheet_column += 1
#             self.image = self.blank_image
#             if self.sheet_column == 8:
#                 self.sheet_column = 0
#                 self.sheet_row += 1
#             self.draw_explosion(self.sheet, 256, self.sheet_column, self.sheet_row)
#
#         # teleport
#         if self.effect_type == "teleport":
#             self.sheet_column += 1
#             self.image = self.blank_image
#             if self.sheet_column == 8:
#                 self.sheet_column = 0
#                 self.sheet_row += 1
#             self.draw_teleport(self.sheet, 256, self.sheet_column, self.sheet_row)
#
#         # red beam
#         if self.effect_type == "beam" and self.damage_type == "thermal":
#             # update length and angle
#             self.length = self.find_distance(self.origin, self.target) * 2.1
#             self.angle = self.find_angle(self.origin, self.target)
#             # update image
#             self.image = self.frames[self.animation_index]
#             self.image = pygame.transform.scale(self.frame_1, (self.width, self.length))
#
#         # blue beam
#         if self.effect_type == "beam" and self.damage_type == "cold":
#             # update length and angle
#             self.length = self.find_distance(self.origin, self.target) * 2.1
#             self.angle = self.find_angle(self.origin, self.target)
#             # update image
#             self.image = self.frames[self.animation_index]
#             self.image = pygame.transform.scale(self.frame_1, (self.width, self.length))
#
#         # flamer loop
#         if self.effect_type == "burst" and self.damage_type == "thermal":
#             self.animation_index += 0.3
#             if self.animation_index > 8:
#                 self.animation_index = 1
#             self.image = self.frames[int(self.animation_index)]
#
#

# import pygame
import pygame.transform
from math import pi, atan2, degrees
from settings import *
import random

pygame.init()


screen_width = 1280
screen_height = 720
centerpoint = (screen_width / 2, screen_height / 2)
screen = pygame.display.set_mode((screen_width, screen_height))
greenscreen_layer = pygame.display.set_mode((screen_width, screen_height))
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 20)


def draw_text(surface, text, color, rect, font, aa=False, bkg=None):
    y = rect.top
    line_spacing = 10
    # get the height of the font
    font_height = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (rect.left, y))
        y += font_height + line_spacing
        # remove the text we just blitted
        text = text[i:]

    return text


pilot_roster = []


class GraphicsManager:
    def __init__(self):
        self.visual_effects_list = []

        # self.fullscreen_rect = pygame.Rect((screen_width, screen_height), (center=(screen_width/2,screen_height/2)))
        self.green_filter = pygame.image.load("graphics/interface/green_filter_65.png").convert_alpha()
        self.full_window_frame = pygame.image.load("graphics/interface/frames/full_frame.png").convert_alpha()
        self.vertical_bar = pygame.image.load("graphics/interface/frames/vertical_bar.png").convert_alpha()
        self.vertical_bar = pygame.image.load("graphics/interface/frames/vertical_bar.png").convert_alpha()
        self.horizontal_bar = pygame.image.load("graphics/interface/frames/horizontal_bar.png").convert_alpha()
        self.cockpit_background = pygame.image.load("graphics/interface/cockpit/cockpit1_1.png").convert_alpha()
        self.crosshair = pygame.image.load("graphics/icons/crosshair.png").convert_alpha()

        self.green_filter = pygame.transform.scale(self.green_filter, (screen_width * 1, screen_height * 1))
        self.full_window_frame = self.resize(self.full_window_frame, (screen_width * 0.95, screen_height * 0.95))
        self.fullscreen_rect = self.full_window_frame.get_rect(center=(screen_width / 2, screen_height / 2))
        self.vertical_bar = self.resize(self.vertical_bar, (screen_width * 0.01, screen_height * 0.92))
        self.vertical_bar2 = self.resize(self.vertical_bar, (screen_width * 0.01, screen_height * 0.75))
        self.horizontal_bar = self.resize(self.horizontal_bar, (screen_width * 0.68, screen_height * 0.03))
        self.cockpit_background = self.resize(self.cockpit_background, (screen_width, screen_height))
        self.crosshair = pygame.transform.scale(self.crosshair, (screen_width*0.05, screen_width*0.05))

    def resize(self, image, size):
        image = pygame.transform.scale(image, size)
        return image

    def draw_window_frames(self):
        screen.blit(self.full_window_frame, self.fullscreen_rect)
        screen.blit(self.horizontal_bar, (screen_width * 0.03, screen_height * 0.2))
        screen.blit(self.vertical_bar, (screen_width * 0.7, screen_height * 0.05))
        screen.blit(self.vertical_bar2, (screen_width * 0.45, screen_height * 0.22))

    # screen.blit(self.right_window_frame, (screen_width*0.6, screen_height*0))

    def draw_cockpit(self):
        screen.blit(self.cockpit_background, (0, 0))

    def draw_black(self):
        screen.fill((0, 0, 0))

    def draw_green(self):
        greenscreen_layer.blit(self.green_filter, (0, 0))

    def draw_shop_headers(self):
        basic_header_image = text_font.render("BASICS", False, (255, 255, 255))
        equipment_header_image = text_font.render("EQUIPMENT", False, (255, 255, 255))
        media_header_image = text_font.render("OFFWORLD MEDIA", False, (255, 255, 255))
        luxury_header_image = text_font.render("BASICS", False, (255, 255, 255))

        screen.blit(basic_header_image, (screen_width*0.05, screen_height*0.3))
        screen.blit(equipment_header_image, (screen_width * 0.05, screen_height * 0.6))
        screen.blit(media_header_image, (screen_width * 0.47, screen_height * 0.3))
        screen.blit(luxury_header_image, (screen_width * 0.47, screen_height * 0.6))

    def draw_crosshair(self, pos_x, pos_y):
        image = self.crosshair
        rect = image.get_rect(center=(pos_x, pos_y))
        screen.blit(image, rect)

    def draw_terrain(self, terrain_group):
        terrain_group.update()
        terrain_group.draw(screen)

#
# class VisualEffect(pygame.sprite.Sprite):
#     def __init__(self, effect_type, damage_type, origin, target):
#         super().__init__()
#         self.name = "undefined"
#         self.effect_type = effect_type
#         self.damage_type = damage_type
#         self.origin = origin
#         self.target = target
#         self.countdown_max = 20
#         self.countdown = 1
#
#         self.blank_image = pygame.image.load("graphics/blank.png").convert_alpha()
#         self.frames = []
#         self.animation_index = 1
#         self.image = self.blank_image
#         self.length = self.find_distance(self.origin, self.target) * 2.1
#         # doubled because graphic has invisible bottom half so its pivot-point is correct
#         self.angle = self.find_angle(origin, target)
#
#         # red laser
#         if self.effect_type == "beam" and self.damage_type == "thermal":
#             self.name = "thermal beam"
#             self.frame_1 = pygame.image.load("graphics/effects/laserbeam_thin_half.png").convert_alpha()
#             self.frame_0 = self.blank_image
#             self.frames = [self.frame_0, self.frame_1]
#             self.image = self.frames[self.animation_index]
#             self.width = 30
#             self.image = pygame.transeffect_type.scale(self.image, (self.width, self.length))
#             self.countdown_max = 20
#
#         # blue laser
#         if self.effect_type == "beam" and self.damage_type == "cold":
#             self.name = "cryo beam"
#             self.frame_0 = self.blank_image
#             self.frame_1 = pygame.image.load("graphics/effects/ice_laser.png").convert_alpha()
#             self.frames = [self.frame_0, self.frame_1]
#             self.image = self.frames[self.animation_index]
#             self.width = 20
#             self.image = pygame.transeffect_type.scale(self.image, (self.width, self.length))
#             self.countdown_max = 20
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
#         self.image = pygame.transform.rotate(self.image, self.angle)
#         self.rect = self.image.get_rect(center=(self.origin.pos_x, self.origin.pos_y))

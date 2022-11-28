import pygame
import random
from sys import exit
import os
import copy
from math import atan2, degrees, pi
import json

BLACK = (0, 0, 0)
continue_button = False

# load screen
screen_width = 1280
screen_height = 720
centerpoint = (screen_width / 2, screen_height / 2)
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("mission_control")
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 20)
clock = pygame.time.Clock()


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


def random_pos():
    pos = random.randint(-screen_width * 0.5, screen_width * 1.5)


def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = text_font.render(fps, 1, pygame.Color("coral"))
    return fps_text


def find_distance(origin, target):
    try:
        if target.alive == True:
            distance_x = target.pos_x - origin.pos_x
            distance_y = target.pos_y - origin.pos_y
            distance_h = (distance_x ** 2 + distance_y ** 2) ** (1 / 2)
        # make sure they're no longer the closest target if they aren't alive
        else:
            distance_h = screen_width * 2
        return distance_h
    except:
        if game.debug_mode == True:
            print("Error: unable to find distance between", origin.name, "and", target.name)
        else:
            pass


def find_angle(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pos_y - origin.pos_y

    rads = atan2(-distance_y, distance_x)
    rads %= 2 * pi
    angle = degrees(rads)

    return angle


class GameManager:
    def __init__(self):
        self.dialogue_active = False
        self.combat_active = True
        self.scene_id = "intro"
        self.debug_mode = False
        self.game_paused = False

        self.current_mission = 0
        self.pilot_roster = []
        self.combat_pilots = pygame.sprite.Group()

    def update(self):
        if self.combat_active:
            self.combat_pilots.update()


class GraphicsManager:
    def __init__(self):
        # self.fullscreen_rect = pygame.Rect((screen_width, screen_height), (center=(screen_width/2,screen_height/2)))
        self.green_filter = pygame.image.load("graphics/interface/green_filter_65.png").convert_alpha()
        self.full_window_frame = pygame.image.load("graphics/interface/frames/full_frame.png").convert_alpha()
        self.vertical_bar = pygame.image.load("graphics/interface/frames/vertical_bar.png")

        self.green_filter = pygame.transform.scale(self.green_filter, (screen_width * 1, screen_height * 1))
        self.full_window_frame = self.resize(self.full_window_frame, (screen_width * 0.95, screen_height * 0.95))
        self.fullscreen_rect = self.full_window_frame.get_rect(center=(screen_width / 2, screen_height / 2))
        self.vertical_bar = self.resize(self.vertical_bar, (screen_width * 0.01, screen_height * 0.92))

        self.explosion_sheet_1 = pygame.image.load("graphics/effects/explosion_sprite_1.png").convert_alpha()
        self.explosion_sheet_2 = pygame.image.load("graphics/effects/explosion_sprite_2.png").convert_alpha()
        self.explosion_sheet_3 = pygame.image.load("graphics/effects/explosion_sprite_3.png").convert_alpha()
        self.explosion_sheet_4 = pygame.image.load("graphics/effects/explosion_sprite_4.png").convert_alpha()
        self.teleport_sheet = pygame.image.load("graphics/effects/teleport_sprite_1.png").convert_alpha()

        self.effects = pygame.sprite.Group()

    def resize(self, image, size):
        image = pygame.transform.scale(image, size)
        return image

    def draw_window_frames(self):
        screen.blit(self.full_window_frame, self.fullscreen_rect)
        # screen.blit(self.vertical_bar, (screen_width * 0.7, screen_height * 0.05))

    def draw_pilots(self):
        game.combat_pilots.draw(screen)

    def update(self):
        screen.fill((0, 0, 0))
        if game.combat_active:
            self.draw_pilots()
        self.draw_window_frames()
        screen.blit(self.green_filter, (0, 0))


class Pilot(pygame.sprite.Sprite):
    def __init__(self, name, team="vanguard"):
        super().__init__()
        self.name = name
        self.mood = "default"
        self.team = team

        self.battlesuit = Battlesuit("majestic")

        # movement
        self.pos_x = -1
        self.pos_y = -1
        self.pos = (self.pos_x, self.pos_y)
        self.momentum_x = 0
        self.momentum_y = 0

        if self.team == "vanguard":
            self.image = pygame.image.load("graphics/icons/blue_dot_icon.png")
        else:
            self.image = pygame.image.load("graphics/icons/red_dot_icon.png")
        self.image = pygame.transform.scale(self.image, (screen_width*0.01, screen_width*0.01))
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

        if self.name == "Kite":
            self.pos_x = screen_width/2
            self.pos_y = screen_height/2

    def move(self):
        self.pos_x += self.momentum_x
        self.pos_y += self.momentum_y
        self.rect = self.image.get_rect(center=(self.pos_x, self.pos_y))

    def update(self):
        self.move()


class Battlesuit:
    def __init__(self, name):
        self.name = name
        file = json.load(open("data/battlesuit_data.json", "r"))
        data = file[f"{name}"]
        self.speed = data["speed"],
        self.health = data["health"]
        self.loadout = data["default_loadout"]
        self.evasion = data["evasion"]


class Weapon:
    def __init__(self, name):
        self.name = name
        item_data = json.load(open("data/item_data.json", "r"))
        weapon_data = item_data[f"{name}"]
        self.accuracy = weapon_data["accuracy"]
        try: self.key_attribute = weapon_data["key_attribute"]
        finally: self.key_attribute = "focus"
        self.cooldown_max = weapon_data["cooldown"]
        try: self.damage_type = weapon_data["damage_type"]
        finally: self.damage_type = "thermal"
        self.range = weapon_data["range"]
        self.tier = weapon_data["tier"]
        self.type = weapon_data["type"]


class VisualEffect(pygame.sprite.Sprite):
    def __init__(self, type, damage_type, origin, target):
        super().__init__()
        self.type = type
        self.damage_type = damage_type
        self.origin = origin
        self.target = target

        self.frame_0 = pygame.image.load("graphics/blank.png")
        self.animation_index = 0

        # laser beam
        if self.type == "beam":
            if self.damage_type == "thermal":
                self.frame_1 = pygame.image.load("graphics/effects/beams/red_laser.png").convert_alpha()
                self.name = "red laser"
            elif self.damage_type == "cold":
                self.frame_1 = pygame.image.load("graphics/effects/ice_laser.png").convert_alpha()
                self.name = "ice laser"
            else:
                self.frame_1 = pygame.image.load("graphics/effects/red_laser.png").convert_alpha()
                self.name = "default laser"

            self.frames = [self.frame_0, self.frame_1]
            self.width = 30
            self.countdown_max = 20

        # explosion
        if self.type == "explosion":
            self.name = "explosion"
            explosion_sheets = [
                graphics.explosion_sheet_1,
                graphics.explosion_sheet_2,
                graphics.explosion_sheet_3,
                graphics.explosion_sheet_4
            ]
            self.sheet = random.choice(explosion_sheets)
            self.countdown_max = 64
            self.sheet_column = 0
            self.sheet_row = 0

        # teleport
        if self.type == "teleport":
            self.name = "teleport"
            self.sheet = graphics.teleport_sheet
            self.animation_index = 0
            self.countdown_max = 64
            self.sheet_column = 0
            self.sheet_row = 0

        try:
            self.countdown = self.countdown_max
        finally:
            self.countdown = 60

        self.length = find_distance(self.origin, self.target)
        if self.type == "beam":  # doubled so it can pivot
            self.length = self.length*2.1
        self.angle = find_angle(origin, target)
        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.image, (self.width, self.length))
        if self.type == "beam":  # rotate beam
            self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center=(self.origin.pos_x, self.origin.pos_y))

    def draw_burst(self, height, column, row):
        screen.blit(self.sheet, (self.origin.pos_x - height * 0.5, self.origin.pos_y - height * 0.5),
                    (height * column, height * row, height, height))

    def update_laser(self):
        # update length and angle
        self.length = find_distance(self.origin, self.target)
        self.length = self.length*2.1 # doubled so it can pivot
        self.angle = find_angle(self.origin, self.target)
        # update image
        self.image = self.frames[self.animation_index]
        self.image = pygame.transform.scale(self.frame_1, (self.width, self.length))
        self.image = pygame.transform.rotate(self.image, self.angle)

    def update(self):
        # catch excessive width errors
        if self.length > screen_width:
            if game.debug_mode:
                print("excessive length", self.origin.name, self.target.name)
            self.length = screen_width

        # update countdown
        if self.countdown <= 0:
            if game.debug_mode:
                print("End effect:", self.name)
            self.kill()
        else:
            self.countdown -= 1

        # explosion
        if self.type == "explosion" or self.type == "teleport":
            self.sheet_column += 1
            self.image = self.frame_0 # blit instead of draw sprite
            if self.sheet_column == 8:
                self.sheet_column = 0
                self.sheet_row += 1
            self.draw_burst(256, self.sheet_column, self.sheet_row)

        # laser beam
        if self.type == "beam":
            self.update_laser()

        # update rect
        self.rect = self.image.get_rect(center=(self.origin.pos_x, self.origin.pos_y))


game = GameManager()
graphics = GraphicsManager()

# pilots
kite = Pilot("Kite")
nasha = Pilot("Nasha")
roger = Pilot("Roger", "baal")
nav_tower = Pilot("nav_tower")
game.pilot_roster = [kite, nasha, roger]
game.combat_pilots.add(kite)
game.combat_pilots.add(nav_tower)
nav_tower.pos_x = screen_width*0.7
nav_tower.pos_y = screen_height*0.3

while True:  # game Cycle
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Quit
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            # toggle debug mode
            if event.key == pygame.K_q:
                if game.debug_mode == False:
                    game.debug_mode = True
                    print("debug_mode enabled")
                elif game.debug_mode == True:
                    game.debug_mode = False
                    print("debug_mode disabled")
    game.update()
    graphics.update()
    pygame.display.update()
    clock.tick(60)

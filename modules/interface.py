# import pygame
import pygame.transform

from settings import *

pygame.init()


screen_width = 1280
screen_height = 720
centerpoint = (screen_width / 2, screen_height / 2)
screen = pygame.display.set_mode((screen_width, screen_height))
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


class TextLabel(pygame.sprite.Sprite):
    def __init__(self, label_type, list_index, text=""):
        super().__init__()
        self.label_type = label_type
        self.list_index = list_index
        self.text = text
        self.active = False
        self.animation_index = 0

        # set text
        try:
            if self.label_type == "Pilot":
                self.reference = pilot_roster[self.list_index]
                self.text = self.reference.name
            elif self.label_type == "button":
                self.text = text
        except (Exception, ):
            self.text = "error: invalid text"

    def update_text(self):
        try:
            if self.label_type == "Pilot":
                self.reference = pilot_roster[self.list_index]
                self.text = self.reference.name
            elif self.label_type == "button":
                self.text = "text"
        except (Exception, ):
            self.text = "error: invalid text"


text_label_group = pygame.sprite.Group()
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
        screen.blit(self.green_filter, (0, 0))

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


# class Visual_Effect:
#     def __init__(self, type, name, origin, target):
#         self.type = type
#         self.name = name
#         self.origin = origin
#         self.target = target
#
#         # set defaults
#         self.length = find_distance(self.origin, self.target)
#         self.angle = find_angle(self.origin, self.target)
#         self.countdown = 60
#
#         if self.type == "beam":
#             self.length = find_distance(self.origin, self.target)
#             self.width = screen_width * 0.01
#
#         elif self.type == "projectile":
#             pass
#
#     def update(self):
#         if self.countdown > 0:
#             self.countdown -= 1
#         elif self.countdown == 0:
#             self.kill()

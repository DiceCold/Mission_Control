# sandbox

import pygame
import random
from sys import exit
import os
import copy
from math import atan2, degrees, pi
import json

# none = "none"
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


def create_rect(x, y, width, height):
    rect = pygame.Rect(screen_width * x, screen_height * y, screen_width * width, screen_height * height)
    return rect


class GameManager:
    def __init__(self):
        self.shop_active = True
        self.combat_active = False
        self.scene_id = "intro"
        self.debug_mode = False
        self.click_cooldown_max = 15
        self.click_cooldown = self.click_cooldown_max
        self.player_inventory = []
        self.player_resources = {
            "Credits": 2000,
            "Fuel": 10,
            "Scrap": 10,
            "Meds": 10
        }

    def update(self):
        if self.click_cooldown > 0:
            self.click_cooldown -= 1


class GraphicsManager:
    def __init__(self):
        # self.fullscreen_rect = pygame.Rect((screen_width, screen_height), (center=(screen_width/2,screen_height/2)))
        self.green_filter = pygame.image.load("graphics/interface/green_filter_65.png").convert_alpha()
        self.full_window_frame = pygame.image.load("graphics/interface/frames/full_frame.png").convert_alpha()
        self.vertical_bar = pygame.image.load("graphics/interface/frames/vertical_bar.png")
        self.vertical_bar = pygame.image.load("graphics/interface/frames/vertical_bar.png")
        self.horizontal_bar = pygame.image.load("graphics/interface/frames/horizontal_bar.png")

        self.green_filter = pygame.transform.scale(self.green_filter, (screen_width * 1, screen_height * 1))
        self.full_window_frame = self.resize(self.full_window_frame, (screen_width * 0.95, screen_height * 0.95))
        self.fullscreen_rect = self.full_window_frame.get_rect(center=(screen_width / 2, screen_height / 2))
        self.vertical_bar = self.resize(self.vertical_bar, (screen_width * 0.01, screen_height * 0.92))
        self.vertical_bar2 = self.resize(self.vertical_bar, (screen_width * 0.01, screen_height * 0.75))
        self.horizontal_bar = self.resize(self.horizontal_bar, (screen_width * 0.68, screen_height * 0.03))

    def resize(self, image, size):
        image = pygame.transform.scale(image, size)
        return image

    def draw_window_frames(self):
        if game.shop_active == True:
            screen.blit(self.full_window_frame, self.fullscreen_rect)
            screen.blit(self.horizontal_bar, (screen_width * 0.03, screen_height * 0.2))
            screen.blit(self.vertical_bar, (screen_width * 0.7, screen_height * 0.05))
            screen.blit(self.vertical_bar2, (screen_width * 0.45, screen_height * 0.22))

    # screen.blit(self.right_window_frame, (screen_width*0.6, screen_height*0))

    def update(self):
        screen.fill((0, 0, 0))
        shop.update()
        self.draw_window_frames()
        screen.blit(self.green_filter, (0, 0))


class ShopManager:
    def __init__(self):
        self.brand = "Baal Corporation"
        self.headers = ["Basics", "Equipment", "Offworld Media", "Luxury Goods"]
        self.item_data = json.load(open("data/item_data.json", "r"))
        self.basics_data = self.item_data["Basics"]
        self.weapon_data = self.item_data["weapons"]
        self.media_data = self.item_data["media"]
        self.shop_items = pygame.sprite.Group()
        self.cart = {}

        self.basics_list = [
            self.basics_data[0],
            self.basics_data[1],
            self.basics_data[2]
        ]
        self.equipment_list = [
            random.choice(self.weapon_data),
            random.choice(self.weapon_data),
            random.choice(self.weapon_data)
        ]
        self.media_list = [
            random.choice(self.media_data),
            random.choice(self.media_data),
            random.choice(self.media_data)
        ]

        self.load_shop_items()

        self.basic_rect = pygame.Rect(screen_width*0.05, screen_height*0.3, screen_width*0.4, screen_height*0.2)
        self.equipment_rect = pygame.Rect(screen_width * 0.05, screen_height*0.6, screen_width * 0.4, screen_height*0.2)
        self.media_rect = pygame.Rect(screen_width * 0.5, screen_height * 0.3, screen_width * 0.4, screen_height * 0.2)
        self.luxury_rect = pygame.Rect(screen_width * 0.5, screen_height * 0.6, screen_width * 0.4, screen_height * 0.2)

    def load_shop_items(self):
        slot = 0
        for basic in self.basics_list:
            item = ShopItems("Basics", slot, self.basics_data[slot])
            self.shop_items.add(item)
            slot += 1
        slot = 0
        for equipment in self.equipment_list:
            item = ShopItems("Equipment", slot, equipment)
            self.shop_items.add(item)
            slot += 1

    # def draw_shop_items(self):
    #     self.shop_items.draw()

    def draw_headers(self):
        for header in self.headers:
            if header == "Basics":
                rect = self.basic_rect
                font = text_font
            elif header == "Equipment":
                rect = self.equipment_rect
                font = text_font
            elif header == "Offworld Media":
                rect = self.media_rect
                font = text_font_small
            elif header == "Luxury Goods":
                rect = self.luxury_rect
                font = text_font_small
            draw_text(screen, header, (255, 255, 255), rect, text_font)

    def update(self):

        self.draw_headers()
        self.shop_items.update()
        # self.draw_shop_items()
        # self.draw_store_items()


class ShopItems(pygame.sprite.Sprite):
    def __init__(self, type, slot_number, item):
        super().__init__()
        self.type = type
        self.slot_number = slot_number
        self.item = item
        self.highlighted = False
        self.width = screen_width*0.2
        self.height = screen_height*0.05
        self.name = item["name"]
        try:
            self.price = item["price"]
        except:
            self.price = 100
        try:
            self.quantity = item["quantity"]
        except:
            self.quantity = -1
        if self.type == "Basics":
            self.pos_x = screen_width*0.05
            self.pos_y = screen_height*0.35 + self.height*self.slot_number
        if self.type == "Equipment":
            self.pos_x = screen_width*0.05
            self.pos_y = screen_height*0.65 + self.height*self.slot_number
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)


    def highlight(self):
        mouse_pos = pygame.mouse.get_pos()
        # check if in bounds
        if self.rect.left < mouse_pos[0] < self.rect.right and self.rect.top < mouse_pos[1] < self.rect.bottom:
            if not self.highlighted:
                self.highlighted = True
        else:
            self.highlighted = False

        if self.highlighted:
            pygame.draw.rect(screen, (100, 100, 100), self.rect)

    def draw_text(self):
        name_image = text_font.render(self.name, False, (255, 255, 255))
        screen.blit(name_image, (self.pos_x+screen_width*0.01, self.pos_y+screen_height*0.01))

        price_image = text_font.render(f"{self.price}", False, (255, 255, 255))
        screen.blit(price_image, (self.pos_x + screen_width * 0.22, self.pos_y + screen_height * 0.01))

        if self.quantity != -1:
            quantity_image = text_font.render(f"({self.quantity})", False, (255, 255, 255))
            screen.blit(quantity_image, (self.pos_x + screen_width * 0.28, self.pos_y + screen_height * 0.01))

    def add_to_cart(self):
        if event.type == pygame.MOUSEBUTTONDOWN and game.click_cooldown == 0:
            if self.highlighted and game.player_resources["Credits"] > self.price and self.quantity != 0:
                game.click_cooldown = game.click_cooldown_max
                # pay for item
                game.player_resources["Credits"] -= self.price
                # decrease supply if limited
                if self.quantity > 0:
                    self.quantity -= 1
                # add to cart
                if self.name in shop.cart.keys():
                    item = shop.cart[f"{self.name}"]
                    item["quantity"] += 1
                    item["total_cost"] = self.price*item["quantity"]
                else:
                    shop.cart["self.name"] = {
                        "name": f"self.name",
                        "price": self.price,
                        "quantity": 1,
                        "total_cost": self.price
                    }

    def update(self):
        self.highlight()
        self.add_to_cart()
        self.draw_text()

class Pilot:
    def __init__(self, name):
        self.name = name
        self.mood = "default"


game = GameManager()
shop = ShopManager()
graphics = GraphicsManager()

# pilots
kite = Pilot("Kite")
nasha = Pilot("Nasha")
roger = Pilot("Roger")

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

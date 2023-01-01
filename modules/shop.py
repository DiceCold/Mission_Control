from settings import *
import random
import json

text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 20)


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
            random.choice(list(self.weapon_data.values())),
            random.choice(list(self.weapon_data.values())),
            random.choice(list(self.weapon_data.values()))
        ]
        self.media_list = [
            random.choice(self.media_data),
            random.choice(self.media_data),
            random.choice(self.media_data)
        ]

        self.load_shop_items()

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

    def update_shop_items(self):
        self.shop_items.update()

    def add_to_cart(self):
        self.shop_items.add_to_cart()


class ShopItems(pygame.sprite.Sprite):
    def __init__(self, item_type, slot_number, item):
        super().__init__()
        self.item_type = item_type
        self.slot_number = slot_number
        self.item = item
        self.highlighted = False
        self.width = screen_width * 0.2
        self.height = screen_height * 0.05
        self.name = item["name"]
        try:
            self.price = item["price"]
        except(Exception, ):
            self.price = 100
        try:
            self.quantity = item["quantity"]
        except(Exception, ):
            self.quantity = -1
        finally:
            pass
        if self.item_type == "Basics":
            self.pos_x = screen_width * 0.05
            self.pos_y = screen_height * 0.35 + self.height * self.slot_number
        if self.item_type == "Equipment":
            self.pos_x = screen_width * 0.05
            self.pos_y = screen_height * 0.65 + self.height * self.slot_number
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
        screen.blit(name_image, (self.pos_x + screen_width * 0.01, self.pos_y + screen_height * 0.01))

        price_image = text_font.render(f"{self.price}", False, (255, 255, 255))
        screen.blit(price_image, (self.pos_x + screen_width * 0.22, self.pos_y + screen_height * 0.01))

        if self.quantity != -1:
            quantity_image = text_font.render(f"({self.quantity})", False, (255, 255, 255))
            screen.blit(quantity_image, (self.pos_x + screen_width * 0.28, self.pos_y + screen_height * 0.01))

    # def add_to_cart(self):
    #     if event.type == pygame.MOUSEBUTTONDOWN and game.click_cooldown == 0:
    #         if self.highlighted and game.player_resources["Credits"] > self.price and self.quantity != 0:
    #             game.click_cooldown = game.click_cooldown_max
    #             # pay for item
    #             game.player_resources["Credits"] -= self.price
    #             # decrease supply if limited
    #             if self.quantity > 0:
    #                 self.quantity -= 1
    #             # add to cart
    #             if self.name in shop.cart.keys():
    #                 item = shop.cart[f"{self.name}"]
    #                 item["quantity"] += 1
    #                 item["total_cost"] = self.price*item["quantity"]
    #             else:
    #                 shop.cart["self.name"] = {
    #                     "name": f"self.name",
    #                     "price": self.price,
    #                     "quantity": 1,
    #                     "total_cost": self.price
    #                 }

    def update(self):
        self.highlight()
        self.draw_text()

    def add_to_cart(self, game, shop):
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
                item["total_cost"] = self.price * item["quantity"]
            else:
                shop.cart["self.name"] = {
                    "name": f"self.name",
                    "price": self.price,
                    "quantity": 1,
                    "total_cost": self.price
                }

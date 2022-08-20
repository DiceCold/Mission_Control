import pygame

scroll_velocity = 3
screen_width = 1920
screen_height = 1080

class Map_Tile(pygame.sprite.Sprite):
    def __init__(self, type, bot_y):
        super().__init__()
        if type == "grass_texture":
            self.bot_y = bot_y
            map_tile_1 = pygame.image.load('graphics/maps/grass_texture.png').convert_alpha()
            map_tile_1 = pygame.transform.scale(map_tile_1, (screen_width,screen_height))
            self.rect = map_tile_1.get_rect(bottomleft = (0,self.bot_y))
            self.image = map_tile_1
    def map_scroll(self):
        global scroll_velocity
        self.rect.y += scroll_velocity
    def update(self):
        self.map_scroll()
        if self.rect.top >= screen_height:
            self.rect.bottom = 0

def load_map_scroll_sprites():
    global map_tile_group
    map_tile_group  = pygame.sprite.Group()
    map_tile_group.add(Map_Tile("grass_texture", screen_height))
    map_tile_group.add(Map_Tile("grass_texture", 0))
    global scroll_velocity
    scroll_velocity = 5
    
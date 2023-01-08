# settings
import pygame

# load screen
screen_width = 1280
screen_height = 720
centerpoint = (screen_width / 2, screen_height / 2)
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("mission_control")
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 10)
text_font_10 = pygame.font.Font("font/Pixeltype.ttf", 10)
pixel_font_15 = pygame.font.Font("font/Pixeltype.ttf", 15)

clock = pygame.time.Clock()

BLACK = (0, 0, 0)
continue_button = False

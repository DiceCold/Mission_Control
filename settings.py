# settings
import pygame

screen_width = 1280
screen_height = 720
centerpoint = (screen_width / 2, screen_height / 2)

pygame.init()
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)
text_font_small = pygame.font.Font("font/Pixeltype.ttf", 30)
text_font_micro = pygame.font.Font("font/Pixeltype.ttf", 20)

screen = pygame.display.set_mode((screen_width, screen_height))

debug_mode = True

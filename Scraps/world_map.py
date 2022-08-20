#world map 

import pygame
import sys

screen_width = 1920
screen_height = 1080
centerpoint = ((screen_width)/2, (screen_height)/2)
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("mission_control")
clock = pygame.time.Clock()
text_font = pygame.font.Font("font/Pixeltype.ttf", 50)

world_map_surf = pygame.image.load("graphics/maps/world_map.png")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Quit
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN: #Click
                if clickablemap_rect.collidepoint(event.pos):
                    if interface_screen == False:
                        map_active = True
                        interface_screen = True
    screen.blit(world_map_surf, (center = (centerpoint)))
    pygame.display.update()
    clock.tick(60)

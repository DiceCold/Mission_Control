import pygame
import random
from sys import exit
import pygame

Startup = True

# class Pilot:
#     def __init__(self, name, battlesuit, battlesuit_damaged, injured, alive, weapons, attack, defence, gps_x, gps_y, momentum_x, momentum_y):
#             self.name = name
#             self.battlesuit = battlesuit
#             self.battlesuit_damaged = battlesuit_damaged
#             self.injured = injured
#             self.alive = alive
#             self.weapons = weapons
#             self.attack = attack
#             self.defence = defence
#             self.gps_x = gps_x
#             self.gps_y = gps_y
#             self.momentum_x = momentum_x
#             self.momentum_y = momentum_y
# class Battlesuit:
#     def __init__(self, name, powercells_max, mobility, generator, refresh, shields):
#             self.name = name
#             self.powercells_max = powercells_max
#             self.mobility = mobility
#             self.generator = generator
#             self.refresh = refresh
#             self.shields = shields

# if Startup == True: #Load Battlesuits
#     Majestic = Battlesuit("Majestic", 5, "Quick", "Fusion Core", 3, "Light Shields")
#     Leviathan = Battlesuit("Leviathan", 12, "Slow", "Fusion Core", 1, "Heavy Shields")

# if Startup == True: #Load Pilots
#         Rose = Pilot("Intrepid Rose", Majestic, False, False, True, ["powersword"], 3, 2, 0,0,0,0)
#         Nighthawk = Pilot("Nighthawk", Majestic, False, False, True, ["burst cannon"], 2, 3 ,0,0,0,0)
#         Scorpion = Pilot("Scorpion", Leviathan, False, False, True, ["burst cannon", "powersword"], 1, 4, 0,0,0,0)
#         AzureKite = Pilot("Azure Kite", Leviathan, False, False, True, ["burst cannon", "powersword"], 4, 1, 0,0,0,0)
#         Lightbringer = Pilot("Lightbringer", Leviathan, False, False, True, ["burst cannon", "powersword"], 4, 1, 0,0,0,0)

if Startup == True: #Load Other
        Screen_Width = 1500
        Screen_Height = 1000
        pygame.init()
        screen = pygame.display.set_mode((Screen_Width,Screen_Height))
        pygame.display.set_caption("Mission_Control")
        clock = pygame.time.Clock()
        test_font = pygame.font.Font('/Users/Graeme/Mission_Control/font/Pixeltype.ttf', 50)
        Game_Active = True
        Map_Active = True
        Map_surf = pygame.image.load('/Users/Graeme//Mission_Control/Art_assets/Interface/green_map_framed_icons_75.png').convert_alpha()
        Map_rect = Map_surf.get_rect(center = (Screen_Width/2,Screen_Height/2))
        Startup = False
print(Game_Active)
print(Map_Active)
print(Map_surf)
print(Map_rect)
screen.blit(Map_surf,(Map_rect))

while True: #Game Cycle
    screen.blit(Map_surf,(Map_rect))

    for event in pygame.event.get(): #Quit
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if Game_Active == True:
            if event.type == pygame.KEYDOWN: #Toggle Map
                if event.key == pygame.K_m:
                    if Map_Active == True:
                        Map_Active = False
                    else: Map_Active = True

    if Game_Active == True: #Render Screen
        if Map_Active == True: #Show Map
            screen.blit(Map_surf,(Map_rect))
            screen.blit(Map_surf,(0,0))
    else: #Render Black Screen
        screen.fill('Black')


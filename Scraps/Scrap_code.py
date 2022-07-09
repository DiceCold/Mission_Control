import pygame
import random
from sys import exit
import os
print(os.getcwd())

#Scrap code

# def Travel_Random():
#     n = random.randint(0,15)
#     Current_Location = Zone_List[n]
#     print(Current_Location)
#     return Current_Location
# def Rolling_to_hit(): #OLD
#     Attacker = Rose
#     Defender = Scorpion
#     # print("Attacker: ")
#     # Attacker = input()
#     # if Attacker == "": Attacker = Rose
#     # if Attacker == "Rose": Attacker = Rose
#     # print("Defender: ")
#     # Defender = input()
#     # if Defender == "": Defender = Scorpion
#     # if Defender == "Scorpion": Defender = Scorpion
#     Hit_Roll = (Attacker.attack + random.randint(0,20))
#     if "powersword" in Attacker.weapons:
#         Hit_Roll = (Attacker.attack + random.randint(0,20) + Powersword.attack)
#     Target_Number = Defender.defence + 10
#     if Hit_Roll >= Target_Number or Hit_Roll == 20:
#         if Defender.injured == True:
#             Defender.alive = False
#         if Defender.injured == False:
#             Defender.injured = True
#             print("Target Injured:" + str(Defender.injured))
#     else: print("miss")
#     Outcome = ["Hit:" + str(Hit_Roll), "Target Injured:" + str(Defender.injured), "Target Alive:" + str(Defender.alive)]
#     #print(Outcome)
#     return Outcome
# def Locate_Me():
#     print(Current_Location)
#     #pass

# pilot1_rect.x += pilot1_momentum_x*0.1
# pilot1_rect.y += pilot1_momentum_y*0.1
# screen.blit(pilot1_surf,(pilot1_rect))
# print(pilot1_target_distance_x, pilot1_target_distance_y)
# print(pilot1_momentum_x, pilot1_momentum_y)
python3
import random
 
#Pilot: "Intrepid Rose"
Rose_HP_Max = 10
Rose_HP = Rose_HP_Max
Rose_Attack = 3
Rose_Defence = 2
Rose_Alive = True
Rose_BattleSuit = "Empty"
 
#BattleSuit: Majestic
Majestic_Hardpoints_Max = 3
Majestic_Hardpoints_Available = Majestic_Hardpoints_Max
Majestic_Hardpoint_1 = "Empty"
Majestic_Hardpoint_2 = "Empty"
Majestic_Hardpoint_3 = "Empty"
 
#Powersword
Powersword_Attack = 5
Powersword_Damage = "1d3"
 
#Scorpion
Scorpion_HP = 3
Scorpion_Attack = 2
Scorpion_Defence = 1
Scorpion_Alive = True
 
#Assign Hero_1 = "Intrepid Rose"
Hero_1 = "Intrepid Rose"
if Hero_1 == "Intrepid Rose":
    Hero_1_HP = Rose_HP
    Hero_1_Attack = Rose_Attack
    Hero_1_Defence = Rose_Defence
    Hero_1_Alive = Rose_Alive
    Hero_1_BattleSuit = Rose_BattleSuit
 
#Assign Enemy_1
Enemy_1 = "Scorion"
if Enemy_1 == "Scorion":
    Enemy_1_HP = Scorpion_HP
    Enemy_1_Attack = Scorpion_Attack
    Enemy_1_Defence = Scorpion_Defence
    Enemy_1_Alive = Scorpion_Alive
 
#attack
Attacker = Hero_1
Defender = Enemy_1
Hit_Roll = Hero_1_Attack + random.randint(0,20)
Damage_Roll = 0
 
if Defender == Enemy_1:
    Target_Number = Enemy_1_Defence + 10
    Defender_HP = Enemy_1_HP
   Defender_Alive = Enemy_1_Alive
 
if Hit_Roll >= Target_Number:
    Damage_Roll = random.randint(0,6)
    print(Damage_Roll)
    Defender_HP = Defender_HP - Damage_Roll
    if Defender == Enemy_1:
        Enemy_1_HP = Defender_HP
        print(Enemy_1_HP)
else: print("miss")
 
if Defender_HP <= 0:
    Defender_Alive = False
else:
    Defender_Alive = True
 
if Defender == Enemy_1:
    Enemy_1_Alive = Defender_Alive
 
print("Done")
print(Hit_Roll)
print(Damage_Roll)
print(Defender_HP)
Outcome = ("Hit:" + str(Hit_Roll), "Damage:" + str(Damage_Roll), "Health Remaining:" + str(Defender_HP), "Enemy Alive:" + str(Enemy_1_Alive))
print(Outcome)

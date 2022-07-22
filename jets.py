#Jet fighting
def roll_to_hit():
    global hit_roll
    global hit_successful
    global attacker
    hit_roll = random.randint(1,20)
    if hit_roll > difficulty:
        hit_successful = True
        print("hit")
    else: 
        hit_successful = False
        print("Miss")
def register_hit():
    global hit_successful
    global target
    print(target.name)
    if hit_successful == True:
        if target.shields == True:
            target.shields = False
            hit_successful = False
        else:
            if target.battlesuit_damaged == False:
                target.battlesuit_damaged = True
                hit_successful = False
            else: 
                if target.battlesuit_heavilly_damaged == False:
                    target.battlesuit_heavilly_damaged = True
                    hit_successful = False
                else:
                    target.injured = True
                    hit_successful = False
def jet_targeting_distance():
    global jet_target_distance_x
    global jet_target_distance_y
    global jet
    global target
    jet_target_distance_x = jet.pos_x - target.pos_x
    jet_target_distance_y = jet.pos_y - target.pos_y
def jet_maneuver():
    #change velocity
    global jet_target_distance_x
    global jet_target_distance_y
    global jet
    global jet_red_rect
    global jet_red_surf
    global jet_blue_surf
    global jet_blue_rect
    if jet.battlesuit_damaged == True:
        jet.momentum_x += 0.01*jet_target_distance_x
    if jet_target_distance_x >= 0:
        jet.momentum_x -= 0.01
        jet.momentum_x -= 0.002*jet_target_distance_x
    else:
        jet.momentum_x += 0.01
        jet.momentum_x += 0.002*abs(jet_target_distance_x) 
    if jet_target_distance_y >= 0:
        jet.momentum_y -= 0.001
        jet.momentum_y -= 0.01*jet_target_distance_y
    else:
        jet.momentum_y += 0.002*abs(jet_target_distance_y)
        jet.momentum_y += 0.01
    #speed limit
    if abs(jet.momentum_x) > 10: #speed limit
        jet.momentum_x *= 0.9
    if abs(jet.momentum_y) >10:
        jet.momentum_y *= 0.9
    if abs(jet.momentum_x) < 2 and abs(jet.momentum_y) < 2: #Speed Boost
        jet.momentum_x *= 1.1
        jet.momentum_y *= 1.1
    #update positions
    jet.pos_y = (jet.pos_y + jet.momentum_y*0.1)
    jet.pos_x = (jet.pos_x + jet.momentum_x*0.1)
    jet.rect = jet.surf.get_rect(center = (int(jet.pos_x), int(jet.pos_y)))
def jet_attack():
    global jet
    global target
    global invuln_timer
    global hit_successful
    if target_hostile == True:
        if abs(jet_target_distance_x) < 30 and abs(jet_target_distance_y) <30:
            pygame.draw.line(screen, (200,0,0), (jet.pos_x,jet.pos_y), (target.pos_x,target.pos_y), 5)
            if invuln_timer > 200:
                roll_to_hit()
                invuln_timer = 0
            if hit_successful == True:
                register_hit()
def jet_sequence():
    jet_targeting_distance()
    jet_maneuver()
    # jet_maneuver()
    jet_attack()
    draw_jet()

from math import atan2, degrees, pi


def find_distance(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pox_y - origin.pos_y
    distance_h = (distance_x ** 2 + distance_y ** 2) ** 0.5
    return distance_h


def find_angle(origin, target):
    distance_x = target.pos_x - origin.pos_x
    distance_y = target.pos_y - origin.pos_y

    rads = atan2(-distance_y, distance_x)
    rads %= 2 * pi
    angle = degrees(rads)
    return angle

class Waypoint:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

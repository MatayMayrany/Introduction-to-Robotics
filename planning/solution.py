#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# {Matay Mayrany}
# {mayrany@kth.se}

from dubins import *
import math
# After computing the new state xn, yn, thetan = step(car, x, y, theta, phi),
# check car.obs to see if the new state is within any obstacles,
# (car.xlb, car.xub, car.ylb, car.yub) to see if it is out of bounds,
# and (car.xt, car.yt) to see if it is close the the target state

def find_best_route(car):
    # initial state
    h = distance_left_to_target(car, car.x0, car.y0)
    visited = [[car.x0, car.y0, 0, [], [0], h]]
    path = []
    possible_range_of_motion = [-math.pi/4, 0, math.pi/4]

    while len(visited) > 0:
        visited = sorted(visited, key=lambda x: x[5])
        x, y, theta, controls, times, cost = visited.pop(0)
        for phi in possible_range_of_motion:
            [
                red_flag, 
                found,
                xn, 
                yn, 
                thetan, 
                controlsn, 
                timesn
            ] = collect_steps(car, x, y, theta, controls[:], times[:], phi)
            if found: 
                return controls, times
            next_move = [round(xn,1), round(yn, 1), round(thetan,1)]
            if not red_flag and not next_move in path:
                path.append(next_move)
                cost_so_far = distance_left_to_target(car, xn, yn)
                visited.append([xn,yn,thetan,controlsn,timesn,cost_so_far])

    return [],[0]
            
def collect_steps(car, x, y, theta, controls, times, phi):
    iterations = 0
    red_flags = False
    found = False
    if phi == 0:
        iterations = 100
    else:
        iterations = 157

    for i in range(iterations):
        x, y, theta = step(car, x, y, theta, phi)
        #make sure we are not going against the rules of dubins car
        while theta >= math.pi:
            theta -= 2*math.pi
        while theta <= -2*math.pi:
            theta += math.pi
        controls.append(phi)
        times.append(times[len(times) - 1] + 0.01)
        #ensure if we hit the outofbounds or an obstical
        if will_car_crash_into_obstacle(car, x, y) or will_car_go_out_of_bounds(car, x, y):
            red_flags = True
            break
        if check_if_target_hit(car, x, y):
            red_flags = False
            found = True
            break
    return red_flags, found, x, y, theta, controls, times

def distance_left_to_target(car, xn, yn):
    return math.sqrt((xn - car.xt)**2 + (yn - car.yt)**2)


def will_car_crash_into_obstacle(car, xn, yn):
    for obsticale in car.obs:
        distance_to_centre = math.sqrt((xn - obsticale[0])**2 + (yn - obsticale[1])**2)
        if distance_to_centre <= obsticale[2]:
            print('obstical found!')
            return True
    return False

def will_car_go_out_of_bounds(car, xn, yn):
    if xn >= car.xub or yn >= car.yub:
        print("went too far")
        return True
    if xn <= car.xlb or yn <= car.ylb:
        print("where are you goin?")
        return True
    return False

def check_if_target_hit (car, xn, yn):
    if math.sqrt((xn - car.xt)**2 + (yn - car.yt)**2) <= 0.1:
        print("We here")
        return True
    return False

def solution(car):
    return find_best_route(car)

    
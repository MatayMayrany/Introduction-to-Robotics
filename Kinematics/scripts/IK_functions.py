#! /usr/bin/env python3
import math

"""
    # {Matay Mayrany}
    # {mayrany@kth.se}
"""

def scara_IK(point):
    x = point[0]
    y = point[1]
    z = point[2]
    q = [0.0, 0.0, 0.0]

    arm1 = 0.3
    arm2 = 0.35
    r = math.sqrt(y**2 + (x-0.07)**2)

    temp_angle_1 = math.atan(y/(x-0.07))
    temp_angle_2 = math.acos(((arm1**2) + (arm2**2) - (r**2))/(2*arm1*arm2))

    q3 = z
    q2 = math.pi - temp_angle_2
    
    num = y*(arm2*math.cos(q2)+arm1) - x*(arm2*math.sin(q2))
    dnum = (x-0.07)*(arm2*math.cos(q2)+arm1) + y*(arm2*math.sin(q2)) 
    q1 = math.atan2(num,dnum)
    #q1 = math.asin(y/arm1)
    #q1 = q2 - temp_angle_1
    q = [q1, q2, q3]

    """
    Fill in your IK solution here and return the three joint values in q
    """

    return q

def kuka_IK(point, R, joint_positions):
    x = point[0]
    y = point[1]
    z = point[2]
    q = joint_positions #it must contain 7 elements

    """
    Fill in your IK solution here and return the seven joint values in q
    """

    return q

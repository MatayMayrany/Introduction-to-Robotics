#! /usr/bin/env python3
import math

"""
    # {Matay Mayrany}
    # {mayrany@kth.se}
"""

def scara_IK(point):
    x = point[0] - 0.07
    y = point[1]
    z = point[2]
    q = [0.0, 0.0, 0.0]
    arm1 = 0.3
    arm2 = 0.35
    temp_value = ((x)**2 + y**2 - (arm1**2 + arm2**2)) / (2 * arm1 * arm2)
    q1 = math.atan2(y, x) - math.atan2(arm2 * math.sqrt(1 - temp_value**2), arm1 + arm2 * temp_value)
    q2 = math.acos(temp_value)
    q3 = z
    q = [q1, q2, q3]

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

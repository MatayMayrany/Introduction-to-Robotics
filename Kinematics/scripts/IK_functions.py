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

    r = math.sqrt(y**2 + (x-0.07)**2)

    q3 = z
    q2 = math.acos((r**2 - 0.0325)/(0.6*r))
    q1 = math.atan(y/(x-0.07)) - q2
    
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

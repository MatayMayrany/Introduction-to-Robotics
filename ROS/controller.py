#!/usr/bin/env python2
import rospy
import actionlib
import irob_assignment_1.msg
from irob_assignment_1.srv import GetSetpoint, GetSetpointRequest, GetSetpointResponse
from geometry_msgs.msg import Twist
from nav_msgs.msg import Path
import tf2_ros
import tf2_geometry_msgs
from math import atan2, hypot
from std_msgs.msg import String
import geometry_msgs.msg
import math

# Use to transform between frames
tf_buffer = None
listener = None

# The exploration simple action client
goal_client = None
# The collision avoidance service client
control_client = None
# The velocity command publisher
pub = None

# The robots frame
robot_frame_id = "base_link"

# Max linear velocity (m/s)
max_linear_velocity = 0.5
# Max angular velocity (rad/s)
max_angular_velocity = 1.0

def move(path):
    global control_client, robot_frame_id, pub,tf_buffer
    rate = rospy.Rate(10.0)
    while path.poses:
        # Call service client with path
        setpoint_and_new_path = control_client(path)
        #setpoint = setpoint_and_new_path.setpoint
        #new_path = setpoint_and_new_path.new_path
        
        # Transform Setpoint from service client
        try:
                transform = tf_buffer.lookup_transform(robot_frame_id,setpoint_and_new_path.setpoint.header.frame_id,rospy.Time())
                transformed_setpoint = tf2_geometry_msgs.do_transform_point(setpoint_and_new_path.setpoint, transform)
        except(tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rate.sleep()
                continue

        # Create Twist message from the transformed Setpoint
        twist_message = Twist()
        angle_v = atan2(transformed_setpoint.point.y,transformed_setpoint.point.x)
        twist_message.angular.z =  min(angle_v,max_angular_velocity)
        twist_message.linear.x = min(transformed_setpoint.point.x,max_linear_velocity)
        # Publish Twist
        pub.publish(twist_message)
        rate.sleep()

        # Call service client again if the returned path is not empty and do stuff again

        # Send 0 control Twist to stop robot
        # mess_twist = 0
        # pub.publish(mess_twist)
        # # Get new path from action server
        path = setpoint_and_new_path.new_path
    
    twist_message.angular.z = 0
    twist_message.linear.x = 0
    pub.publish(twist_message)
    

def get_path():
    global goal_client
    while True:
                # Get path from action server
                goal_client.wait_for_server()
                goal = irob_assignment_1.msg.GetNextGoalAction()
                goal_client.send_goal(goal)
                goal_client.wait_for_result()    
                # Call move with path from action server
                move(goal_client.get_result().path)

if __name__ == "__main__":
    # Init node
    rospy.init_node('controller')
    # Init publisher
    pub = rospy.Publisher('cmd_vel',Twist,queue_size=10)
    # Init simple action client
    goal_client = actionlib.SimpleActionClient('get_next_goal',irob_assignment_1.msg.GetNextGoalAction)
    # Init service client
    control_client = rospy.ServiceProxy('get_setpoint',GetSetpoint)
    #tf2
    tf_buffer = tf2_ros.Buffer()
    listener = tf2_ros.TransformListener(tf_buffer)
    # Call get path
    get_path()
    # Spin
    rospy.spin()
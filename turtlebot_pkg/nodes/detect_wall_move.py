#! /usr/bin/env python3

"""
Parking Assignment Answer

Try it out!!
"""

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
from turtlebot_pkg.srv import rotateResult



def call_rotate_client(laser_arr):
    rospy.wait_for_service('rotate_result')
    sendToServer = rospy.ServiceProxy('rotate_result', rotateResult)
    res = sendToServer(laser_arr)
    print(res.success,',', res.message)
    rospy.sleep(3)
    return res



def callback(data):
    laser_range = data.ranges[0:5]
    laser_arr = np.array(laser_range)
    print('laser_arr : ', laser_arr)
    nonzero = np.count_nonzero(laser_arr >= 0.3)
    print('nonzero :', nonzero)
    cmd_vel = Twist()

    if nonzero > 0:
        cmd_vel.linear.x = 0.2
    else:
        cmd_vel.linear.x = 0.0
        pub.publish(cmd_vel)
        #client
        result = call_rotate_client(laser_range)

       
    pub.publish(cmd_vel)


rospy.init_node("detect_wall_move", disable_signals=True)
rospy.loginfo("==== parking node Started ====\n")

pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
sub = rospy.Subscriber("/scan", LaserScan, callback)

rospy.spin()

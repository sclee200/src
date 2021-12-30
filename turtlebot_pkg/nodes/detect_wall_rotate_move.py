#! /usr/bin/env python3

"""
Parking Assignment Answer

Try it out!!
"""

import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import numpy as np
from turtlebot_pkg.srv import rotateSomeDegree
from rotate_some_degree import rotate 

def call_rotate_client():
    rospy.wait_for_service('rotate_some_degree')
    sendToServer = rospy.ServiceProxy('rotate_some_degree', rotateSomeDegree)
    res = sendToServer("How much degree I turn?")     
    # rospy.sleep(3)
    return res

standby = False
STATE = 100
DEGREE=0.1
toRAD = 0.0174533
pub = None
def callback(data):
    global STATE
    global standby
    global pub
    global DEGREE
    # print('standby : ------------------------------------------------', standby)
    # if standby:
    #     print('standby in callback')
    #     return
    laser_range = data.ranges[0:5]
    laser_arr = np.array(laser_range)
    print(data.ranges[0:5])
    # print('callback in')
    print('laser_arr : ', laser_arr)
    nonzero = np.count_nonzero(laser_arr >= 0.35)
    nonInfinity = np.any(np.isnan(laser_arr))
    print('nonzero :', nonzero, 'noninfinity :', nonInfinity)
    # cmd_vel = Twist()

    if nonzero > 0 or nonInfinity:
        # cmd_vel.linear.x = 0.2
        STATE = 1
        # standby = False
    else:
        # cmd_vel.linear.x = 0.0
        # pub.publish(cmd_vel)
        STATE=0
        # standby = True
        # result = call_rotate_client()
        # print('result.degree : ', result.degree, 'result.success :', result.success)
        # DEGREE = result.degree

    # pub.publish(cmd_vel)
    # print("callback return after pub")

def callbackChg(data):
    
    laser_range = data.ranges[0:5]
    laser_arr = np.array(laser_range)
    print(data.ranges[0:5])
    print('callback in*******************')
    print('laser_arr : ', laser_arr)
    nonzero = np.count_nonzero(laser_arr >= 0.35)
    nonInfinity = np.any(np.isnan(laser_arr))
    print('nonzero :', nonzero, 'noninfinity :', nonInfinity)
    cmd_vel = Twist()

    if nonzero > 0 or nonInfinity >0:
        cmd_vel.linear.x = 0.2
    else:
        cmd_vel.linear.x = 0.0
        pub.publish(cmd_vel)
        #client
        result = call_rotate_client(laser_range)
        print('result.degree : ', result.degree, 'result.success :', result.success)
        speed = 10
        angle = result.degree
        clockwise = 0
        angular_speed  = speed * toRAD
        relative_angle = angle * toRAD
        msg = cmd_vel
        msg.linear.x  = msg.linear.y  = msg.linear.z  = 0
        msg.angular.x = msg.angular.y = 0        
        if clockwise:
            msg.angular.z = -abs(angular_speed)
        else:
            msg.angular.z =  abs(angular_speed)
            
        duration = relative_angle / angular_speed
        time2end = rospy.Time.now() + rospy.Duration(duration)
        
        pub.publish(msg)
        rospy.sleep(duration)
            
        # while(rospy.Time.now() < time2end):
        #     pass    
            
        msg.angular.z = 0
        cmd_vel=msg
       
       
    pub.publish(cmd_vel)
    print("callback return after pub")

def callbackChg2(data):
    toRAD = 0.0174533
    laser_range = data.ranges[0:5]
    laser_arr = np.array(laser_range)
    print(data.ranges[0:5])
    print('callback in*******************')
    print('laser_arr : ', laser_arr)
    nonzero = np.count_nonzero(laser_arr >= 0.35)
    nonInfinity = np.any(np.isnan(laser_arr))
    print('nonzero :', nonzero, 'noninfinity :', nonInfinity)
    cmd_vel = Twist()

    if nonzero > 0 or nonInfinity >0:
        cmd_vel.linear.x = 0.2
    else:
        cmd_vel.linear.x = 0.0
        pub.publish(cmd_vel)
        #client
        result = call_rotate_client(laser_range)
        print('result.degree : ', result.degree, 'result.success :', result.success)
        msg =cmd_vel
        angular_speed = 5.95
        relative_angle = 3.141592/4

        duration = relative_angle / angular_speed
        cmd_vel.angular.z = angular_speed
        pub.publish(cmd_vel)
        print(duration)
        rospy.sleep(duration)
            
        cmd_vel.angular.z = 0
        pub.publish(cmd_vel)
            
        msg.angular.z = 0
        cmd_vel=msg
       
       
    pub.publish(cmd_vel)
    print("callback return after pub")

def callbackprint(data):
    print(data.ranges[0:5])

def main():
    global STATE
    global DEGREE
    global standby
    global pub
    rospy.init_node("detect_wall_move", disable_signals=True)
    # rospy.loginfo("==== parking node Started ====\n")

    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    rospy.Subscriber("/scan", LaserScan, callback)
    rate = rospy.Rate(50)
    msg = Twist()
    while not rospy.is_shutdown():
        print('STATE : ', STATE)
        if STATE == 0:            
            if not standby:
                standby = True
                speed = 30
                result = call_rotate_client()
                print('result.degree : ', result.degree, 'result.success :', result.success)
                DEGREE = result.degree
                angle = DEGREE
                print('angle : ', angle)
                clockwise = 0
                angular_speed  = speed * toRAD
                # relative_angle = angle * toRAD
                # angular_speed = 0.195
                relative_angle = 3.141592/4
                
                msg.linear.x  = msg.linear.y  = msg.linear.z  = 0
                msg.angular.x = msg.angular.y = 0        
                if clockwise:
                    msg.angular.z = -abs(angular_speed)
                else:
                    msg.angular.z =  abs(angular_speed)
                    
                duration = relative_angle / angular_speed
                time2end = rospy.Time.now() + rospy.Duration(duration)

                pub.publish(msg)
                # rospy.sleep(duration)
                while(rospy.Time.now() < time2end):
                    pass

                msg.linear.x  = msg.linear.y  = msg.linear.z  = 0
                msg.angular.x = msg.angular.y = msg.angular.z = 0 
                pub.publish(msg)
                standby = False

        elif not standby and STATE == 1:
            msg.linear.x = 0.2
            msg.linear.y  = msg.linear.z  = 0
            msg.angular.x = msg.angular.y = msg.angular.z = 0 
            pub.publish(msg)
        else:
            rospy.logerr('Unknown state!')

        rate.sleep()

if __name__ == '__main__':
    main()

#!/usr/bin/env python

# -*- coding: utf-8 -*-

import rospy

from sensor_msgs.msg import LaserScan

from geometry_msgs.msg import Twist

pub_ = None

# defines the regions of the laser, empty values.

regions_ = {

    'right': 0,

    'fright': 0,

    'front': 0,

    'fleft': 0,

    'left': 0,

}

# starting state

state_ = 0

# state dictionary

state_dict_ = {

    0: 'find the wall',

    1: 'go to the wall',

    2: 'turn left in front of the wall',

    3: 'follow the wall'

}

# function that changes the state and prints the current state number and name.

# also, stores the new state as the old state

def change_state(state):

    global state_, state_dict_

    print ('State: [%s] - %s' % (state, state_dict_[state]))

    state_ = state      # new becomes old

# Scan actions

def take_action():

    global regions_, min_scan_, state_

    regions = regions_

    min_scan = round(min_scan_,2)

    # print("min: ", min_scan)     # for debug

    # print("front: ", round(regions['front'],2))    # for debug

    msg = Twist()

    linear_x = 0

    angular_z = 0

    state_description = ''

    dist = 0.3

    # the many cases

    if round(regions['front'],2) > min_scan and state_ != 1 and state_ != 2 and state_ !=3:

        state_description = 'drejer front mod min_scan'

        change_state(0)

    

    elif round(regions['front'],2) <= min_scan and state_ != 1 and state_ != 2 and state_ != 3:

        state_description = 'kører mod væg'

        change_state(1)

    

    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] > dist:  

        state_description = 'case 2 - front'

        change_state(2)

    elif regions['front'] < dist and regions['fleft'] > dist and regions['fright'] < dist:

        state_description = 'case 5 - front and fright'

        change_state(2)

    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] > dist:

        state_description = 'case 6 - front and fleft'

        change_state(2)

    elif regions['front'] < dist and regions['fleft'] < dist and regions['fright'] < dist:

        state_description = 'case 7 - front and fleft and fright'

        change_state(2)

    elif regions['front'] > dist and regions['fleft'] > dist and regions['fright'] < dist:

        state_description = 'case 3 - fright'

        change_state(3)

    else:

        state_description = 'unknown case'

# Action functions

def find_wall():

    msg = Twist()

    msg.angular.z = -0.3    # turns right

    return msg

def go_to_wall():

    msg = Twist()

    msg.linear.x = 0.2

    return msg

def turn_wall():

    msg = Twist()

    msg.linear.x = 0.005

    msg.angular.z = 0.3      # turns left

    return msg

def follow_wall():

    global regions_

    msg = Twist()

    msg.linear.x = 0.12

    return msg

# callback

def callback_laser(msg):

    global regions_, min_scan_

    min_scan_ = min(msg.ranges) # the smallest scan value currently available

    # divides the 180 degrees of the front of the lidar into 5 sections, in increments of 36 degrees

    regions_ = {

        'right':  min(min(msg.ranges[90:126]), 10),

        'fright': min(min(msg.ranges[127:162]), 10),

        'front':  min(min(msg.ranges[163:198]), 10),

        'fleft':  min(min(msg.ranges[199:234]), 10),

        'left':   min(min(msg.ranges[235:270]), 10),

    }

    take_action()

# the main function

def main():

    global pub

    rospy.init_node('reading_laser')

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

    sub = rospy.Subscriber('/scan', LaserScan, callback_laser)

    rate = rospy.Rate(50)

    

    while not rospy.is_shutdown():

        msg = Twist()

        if state_ == 0:

            msg = find_wall()

        elif state_ == 1:

            msg = go_to_wall()

        elif state_ == 2:

            msg = turn_wall()

        elif state_ == 3:

            msg = follow_wall()

        else:

            rospy.logerr('Unknown state!')

        pub.publish(msg)

        rate.sleep()

if __name__ == '__main__':

    main()
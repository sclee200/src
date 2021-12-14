#! /usr/bin/env python3
import rospy
from service_first.srv import addtwoints

if __name__ == '__main__':
    rospy.wait_for_service('addtwo')

    add_two_ints = rospy.ServiceProxy('addtwo',addtwoints)
    result = add_two_ints(3,4)
    print(result)

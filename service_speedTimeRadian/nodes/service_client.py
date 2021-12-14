#! /usr/bin/env python3
import rospy
from service_speedTimeRadian.srv import speedTimeRadian

if __name__ == '__main__':
    rospy.wait_for_service('speedTimeRadian_service')

    distanceAndRadian = rospy.ServiceProxy('speedTimeRadian_service',speedTimeRadian)
    # distance, radianres = distanceAndRadian(30, 4, 60)
    # print('distance : ', distance, 'radianres : ', radianres)
    # li = list()
    li = distanceAndRadian(40, 5, 60)
    print(li)
    
    # print('distance : ', li[0], 'radian : ', li[1])
    # distance = distanceAndRadian(30, 4, 60)
    # print('distance : ', distance )

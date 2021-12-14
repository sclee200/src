#! /usr/bin/env python3
import rospy
# custom service messsage
from service_speedTimeRadian.srv import speedTimeRadian, speedTimeRadianResponse

def fun_callback(req):
    rospy.loginfo('%s  %s  %s' % (req.speed, req.time, req.radian))
    # rospy.loginfo('%s , %s' % (req.speed, req.time ))
    return speedTimeRadianResponse(req.speed*req.time, float(req.radian*3.14/180))
    # return speedTimeRadianResponse(req.speed*req.time,  int(req.radian*3.14/180))
    # return speedTimeRadianResponse(req.speed*req.time, req.radian*3)
    # return speedTimeRadianResponse(req.speed*req.time)
    pass

if __name__ == '__main__':
    # server 선언
    rospy.init_node('speedTimeRadian_server')
    # server 기다리기
    rospy.Service('speedTimeRadian_service',speedTimeRadian,fun_callback)

    rospy.spin()
    pass
#! /usr/bin/env python3
import rospy
# custom service messsage
from service_first.srv import addtwoints, addtwointsResponse

def fun_callback(req):
    rospy.loginfo('%s, %s' % (req.a, req.b))
    return addtwointsResponse(req.a + req.b)

if __name__ == '__main__':
    # server 선언
    rospy.init_node('addtwo_server')
    # server 기다리기
    rospy.Service('addtwo',addtwoints,fun_callback)

    rospy.spin()
    pass
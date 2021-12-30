#! /usr/bin/env python3
import rospy
# custom service messsage
from turtlebot_pkg.srv import rotateResult, rotateResultResponse

def fun_callback(req):
    # rospy.loginfo('%s ' % req.scan_sequence )
    print(req.scan_sequence )
    
    success = True
    message = "Success"
    return rotateResultResponse(success, message)

if __name__ == '__main__':
    # server 선언
    rospy.init_node('rotate_server')
    # server 기다리기
    rospy.Service('rotate_result',rotateResult,fun_callback)

    rospy.spin()
    pass
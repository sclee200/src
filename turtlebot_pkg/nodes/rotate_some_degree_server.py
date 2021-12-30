#! /usr/bin/env python3
import rospy
# custom service messsage
from turtlebot_pkg.srv import rotateSomeDegree, rotateSomeDegreeResponse

def fun_callback(req):
    # rospy.loginfo('%s ' % req.scan_sequence )
    print(req.message, ' call receieved' )    
    degree = 90    
    return rotateSomeDegreeResponse(degree, True)

if __name__ == '__main__':
    # server 선언
    rospy.init_node('rotate_some_degree_server')
    # server 기다리기
    rospy.Service('rotate_some_degree',rotateSomeDegree,fun_callback)

    rospy.spin()
    pass
#! /usr/bin/env python3
import rospy
# custom service messsage
from turtlebot_pkg.srv import rotateSomeDegree, rotateSomeDegreeResponse
count =0
degree = 90  
def fun_callback(req):
    global count
    # rospy.loginfo('%s ' % req.scan_sequence )
    count += 1

    print(req.message, count, 'th call receieved and returned : ', degree, ' degree' )    
      
    return rotateSomeDegreeResponse(degree, True)

if __name__ == '__main__':
    # server 선언
    rospy.init_node('rotate_some_degree_server')
    # server 기다리기
    rospy.Service('rotate_some_degree',rotateSomeDegree,fun_callback)

    rospy.spin()
    pass
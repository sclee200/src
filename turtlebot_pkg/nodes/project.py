import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
import cv2

speed = 0.1
bridge = CvBridge()

def callimage(image):
    frame = bridge.imgmsg_to_cv2(image, 'bgr8')
    msg = Twist()
    if frame[:,:,0].mean() < 15 and frame[:,:,1].mean() >90 and frame[:,:,2].mean() < 15:
        print(frame[:,:,0].mean(),frame[:,:,1].mean(),frame[:,:,2].mean() )
        msg.linear.x = 0
        msg.angular.z = 0
        pub.publish(msg)
        rospy.signal_shutdown("Done")
    cv2.imshow('Turtlebot3 Camera',frame)
    cv2.waitKey(1)
    return

def callback(data):
    laser_arr = np.array(data.ranges[0:329])
    min = np.argmin(laser_arr)
    msg = Twist()
    msg.linear.x = speed
    if laser_arr[min] < 0.2 :
        msg.angular.z = (min - 100) / 50 
    elif laser_arr[min] > 0.2 and laser_arr[min] < 0.25:
        msg.angular.z = (min - 95) / 50 
    elif laser_arr[min] > 0.25 and laser_arr[min] < 0.30:
        msg.angular.z = (min - 85) / 50
    elif laser_arr[min] > 0.3:
        msg.angular.z = (min -80) / 50
    else:
        pass
    pub.publish(msg)

    return

if __name__ =='__main__':
    rospy.init_node('parking')
    pub = rospy.Publisher('/cmd_vel',Twist, queue_size=1)
    rospy.Subscriber('/scan',LaserScan, queue_size = 1, callback = callback)
    rospy.Subscriber('mira/camera1/image_raw',Image, callback = callimage)
    rospy.spin()
    pass

    # laser_int = np.array(data.intensities[0:329])
    # max = np.argmax(laser_int)
    # for i in range(330):
    #     if laser_arr[i] == 0:
    #         if laser_int[i] == 0:
    #             laser_arr[i] = np.inf
    #         else:
    #             laser_arr[i] = 0.1    
    # print(min, max, laser_arr[min], laser_int[max])

from turtlebot_pkg.getcharwithoutstop import GetCharwithoutStop
import rospy
 
from geometry_msgs.msg import Twist
 

 
def resetkey():
    cmd_vel.linear.x = 0.0
    cmd_vel.linear.y = 0.0
    cmd_vel.linear.z = 0.0
    cmd_vel.angular.x = 0.0
    cmd_vel.angular.y = 0.0
    cmd_vel.angular.z = 0.0

def key_operation(key):
    global pub, cmd_vel
    resetkey()
    if key == 'w':
        cmd_vel.linear.x = 0.2
    elif key == 'x':
         cmd_vel.linear.x = -0.2
    elif key == 'e':
        cmd_vel.angular.z = 0.2
    elif key == 'c':
        cmd_vel.angular.z = -0.2
    else:
        resetkey()
    pub.publish(cmd_vel)

if __name__ == '__main__':
    rospy.init_node("key_operation", disable_signals=True)
    rospy.loginfo("==== key operation Started ====\n")
    pub = rospy.Publisher("/cmd_vel", Twist, queue_size=1)
    cmd_vel = Twist()
    kb = GetCharwithoutStop()
    print('kb started. w : forward, x: backward')
    while True:
        key = kb.getch()
        print('KEY : ', key)
        key_operation(key)
        
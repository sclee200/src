import rospy
from turtlebot_pkg.getcharwithoutstop import GetCharwithoutStop 

pass

if __name__ == '__main__':
    kb = GetCharwithoutStop()
    print('kb started. w : forward, x: backward')
    while True:
        key = kb.getch()
        if key == 'w':
            print('forward')
        elif key == 'x':
            print('backward')
        # if kb == 'w':
        #     print('forward')
        # if kb == 'w':
        #     print('forward')
#!/usr/bin/env python

# Haobo Yuan, Xiangyu Han
# Apr 3, 2023
# File Version 6
# Desp: a script to subscribe data from simulators(Namespace/joy): throttle&yoke&Rudder and publish takeoff/velocity/land/others commands to UAV
# Note: Must insert 3 devices of simulator in order: 1. Throttle; 2. Yoke; 3. Rudder

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Empty
from std_msgs.msg import UInt8
from sensor_msgs.msg import Joy


def callback1(data):
    # Use throttle to control vertical(upward/downward) and horizontal(forward/backward) movement and its buttons to takeoff/land/flip/emergency_stop
	print('##################')

	twist.linear.z = data.axes[0]
	print('vertical speed: %.2f'%(twist.linear.z)) # positive-50~100-upward

	twist.linear.y = data.axes[1]
	print('forward speed: %.2f'%(twist.linear.y)) # positive-50~100-forward

	pub1.publish(twist)
	
	print('##################')
	

def callback2(data):
    # Use yoke to control horizontal(left/right) movement and its buttons to takeoff/land/flip/emergency_stop
    # right: red = 3(emergency), white = 2(flip), 
    # left: white_top = 1(take off), white_bottom = 0 (land)
	empty1 = Empty()
	empty2 = Empty()
	empty_UInt8 = UInt8()
	empty3 = Empty()

	if data.buttons[1] == 1:
		pub2.publish(empty1)
		print('take off')

	if data.buttons[2] == 1:
		pub4.publish(empty_UInt8)
		print('flip')

	if data.buttons[3] == 1:
		pub5.publish(empty3)
		print('\n\n!!!emergency stop!!!\n\n')

	if data.buttons[0] == 1:
		pub3.publish(empty2)
		print('land')
    
    # Use yoke axes to control horizontal locomation
	print('##################')

	twist.linear.x = -data.axes[0]
	print('horizontal speed: %.2f'%(twist.linear.x)) # positive-50~100-right
	pub1.publish(twist)
	
	print('##################')

def callback3(data):
	# Use Rudder to control yaw orientation
	print('##################')

	twist.angular.z = data.axes[2]
	print('Z angular speed: %.2f'%(twist.angular.z)) # 

	pub1.publish(twist)
	
	print('##################')


# Intializes everything
def start():
	# publishing to "tello/cmd_vel" to control velocity
	global pub1
	pub1 = rospy.Publisher('tello/cmd_vel', Twist)

    # publishing to "tello/takeoff" to start
	global pub2
	pub2 = rospy.Publisher('tello/takeoff', Empty)

    # publishing to "tello/land" to end
	global pub3
	pub3 = rospy.Publisher('tello/land', Empty)

    # publishing to "tello/flip" to end
	global pub4
	pub4 = rospy.Publisher('tello/flip', UInt8)

    # publishing to "tello/emergency" to end
	global pub5
	pub5 = rospy.Publisher('tello/emergency', Empty)


    # instantiation
	global twist
	twist = Twist()

	# subscribed to throttle
	rospy.Subscriber("/throttle/joy", Joy, callback1)

	# subscribed to yoke
	rospy.Subscriber("/yoke/joy", Joy, callback2)

	# subscribed to yoke
	rospy.Subscriber("/rudder/joy", Joy, callback3)

	# starts the node
	rospy.init_node('Simulator2UAV')
	rospy.spin()


if __name__ == '__main__':
	start()

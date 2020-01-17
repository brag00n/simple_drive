#!/usr/bin/python
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor

import atexit
import rospy
import struct

from geometry_msgs.msg import Twist
from std_msgs.msg import Float32

# create a default object, no changes to I2C address or frequency
mh = Raspi_MotorHAT(addr=0x6f)
myMotor = mh.getMotor(2)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
        mh.getMotor(1).run(Raspi_MotorHAT.RELEASE)
        mh.getMotor(2).run(Raspi_MotorHAT.RELEASE)
        mh.getMotor(3).run(Raspi_MotorHAT.RELEASE)
        mh.getMotor(4).run(Raspi_MotorHAT.RELEASE)

atexit.register(turnOffMotors)


def main():
    rospy.init_node("simple_drive")
    
    
    def on_new_twist(data):
	if ( data.angular.z != 0):
           print(" data.linear.x{}, data.angular.z={}".format(data.linear.x, data.angular.z))
	   print(" Forward")
	   myMotor.run(Raspi_MotorHAT.FORWARD)
	   myMotor.setSpeed(60)
	else:
	   myMotor.setSpeed(0)
	   myMotor.run(Raspi_MotorHAT.RELEASE)

    def on_new_servo(data):
        print(" Servo={}".format(data))
        serial_msg = struct.pack("<f", data.data)

    print("Starting...")
    subscriber_twist = rospy.Subscriber("cmd_vel", Twist, on_new_twist, queue_size=10)
    subscriber_servo = rospy.Subscriber("servo_pos", Float32, on_new_servo, queue_size=10)

    rospy.spin()

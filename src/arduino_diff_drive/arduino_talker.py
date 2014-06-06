#!/usr/bin/env python


from twisted.internet import protocol, reactor
from twisted.internet.serialport import SerialPort
from twisted.protocols import basic
from twisted.internet import stdio
from twisted.internet import task

import rospy
from std_msgs.msg import String

glob_stat=""
rospy.init_node('arduino_talker', anonymous=True)
pub = rospy.Publisher('arduino_status', String, queue_size=10)

# periodically publish status to ROS topic
def timerTask():
  global glob_stat
  try:
    str = glob_stat
    rospy.loginfo(str)
    pub.publish(str)
  except rospy.ROSInterruptException: pass

# Handling data exchange with Arduino by serial
class Echo(basic.LineReceiver):
    from os import linesep as delimiter

    def __init__(self, device_connection):
        self.device_connection = device_connection
    def connectionMade(self):
        self.transport.write( "-----\n")
        self.transport.write( "1. STATUS\n")
        self.transport.write( "2. SET\n")
        self.transport.write( "3. RESET\n")

    def lineReceived(self, line):
        #self.sendLine('Echo: ' + line+']')
        #self.connectionMade()
        ch = line
        if int(ch) == 1:
            self.device_connection.sendLine('STATUS')
        elif int(ch) == 2:
            self.device_connection.sendLine('SET 1 4')
        elif int(ch) == 3:
            self.device_connection.sendLine('RESET')
        else:
            reactor.stop()

class DeviceBluetooth(basic.LineReceiver):

    def connectionMade(self):
        print 'Connection made!'

    def lineReceived(self, data):
        global glob_stat
        print "Response: {0}".format(data)
        glob_stat = data


def start():
    from twisted.internet import reactor
    arduino = DeviceBluetooth()
    std_io = Echo(arduino)
    stdio.StandardIO(std_io)
    SerialPort(arduino, '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AH01GNYJ-if00-port0', reactor, baudrate=115200)
    l = task.LoopingCall(timerTask)
    l.start(1)

    reactor.run()
# will search for 1st arduino by something like this:
#import glob
# glob.glob("/dev/tty.usbserial-*"[0])

if __name__ == '__main__':
    start()


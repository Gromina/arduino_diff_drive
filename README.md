arduino_diff_drive
==================

ROS package to talk to arduino based two wheeled vehicle (diff drive)

The idea
--------

Arduino is plugged to serial port. The package connects to the serial.
Arduino is able to receive couple of commands and react to them with info or actions
The package transaltes commands and info to/from ROS topics

Commands
--------

STATUS: report current motors power, opto counters
SET: set motors power
RESET: stop motors, reset opto counters


#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import almath
import argparse
import sys
import time
import math
from random import randrange

# will need to pip install the following libs:


########################
#
#   NaoController Class
######################## 

class NaoController:

###
# __init__:
#
###
    def __init__(self, _ip, _port=9559, _pg_display=None):
        # While walking flag is true, allow Nao to walk.

        self.DEBUG = False

        self.session = qi.Session()
        
        try:
            self.session.connect("tcp://" + _ip + ":" + str(_port))
        except RuntimeError:
            print ("Can't connect to Naoqi at ip \"" + _ip + "\" on port " + str(_port) +".\n"
                    "Please check your script arguments. Run with -h option for help.")
            sys.exit(1)

        self.ip = _ip

        """
        Tracker using a landmark.
        """
        # Get the services ALTracker, ALMotion and ALRobotPosture, ALAudioPlayer.
        self.motion_service = self.session.service("ALMotion")
        self.posture_service = self.session.service("ALRobotPosture")
        self.tracker_service = self.session.service("ALTracker")
        self.memory_service = self.session.service("ALMemory")
        self.tts_service = self.session.service("ALTextToSpeech")
        self.audio_player_service = self.session.service("ALAudioPlayer")

        
###
# speak_nao:
#
# Inputs:
#	direction: direction (left or right)
# 	(optionl) angle: angle to turn (in radians)
#
# Returns:
#	N/A
###
    def speak_nao(self, sentence):
        print("")
        print("      Saying: ", sentence)

        self.tts_service.say(sentence)
        # time.sleep(1)


        
###
# turn_nao:
#
# Inputs:
#	direction: direction (left or right)
# 	(optionl) angle: angle to turn (in radians)
#
# Returns:
#	N/A
###
    def turn_nao(self, direction, angle=1.5709):

        print("")
        print("Turning ", direction)
        if(direction == "left"):
            theta = angle
        elif(direction == "right"):
            theta = -angle
        elif(direction == "angle"):
            theta = angle

        self.motion_service.moveTo(0, 0, theta, self.pepper_slow_move_config, _async=True)


###
# turn_to_heading:
#
#	Turns to face a heading using the inbuilt gyro readings, at the moment it is hard coded @TODO set "north" as the starting direction (when code is ran) and calculate others accordingly
#
# Inputs:
#	direction: compas heading (north, south, east, west)
#
###        
    def turn_to_heading(self, direction):

        print("")
        print("Turning to heading ", direction)        
                
        if(direction == "north"):
            theta = -84
        elif(direction == "south"):
            theta = 96
        elif(direction == "east"):
            theta = 6
        elif(direction == "west"):
            theta = -174
            
        theta = self.calculate_turn_direction(theta)
        print(theta)
        self.motion_service.moveTo(0, 0, theta, self.pepper_slow_move_config)
      	
###
# calculate_turn_direction:
# 
#	calculates the required angle to turn, to make the robot face from a desired (absolute) heading 
#	@TODO check this is working correctly - it may have a problem when it is already facing direction that is desired
#
# Inputs:
#	destination_heading: angle in radians
#
# Returns:
#	angle in radian
###        
    def calculate_turn_direction(self, destination_heading):

        current_heading = self.get_heading("deg")

        print("")
        print("Current heading: ", current_heading) 
        print("Destination heading: ", destination_heading) 

        #print (current_heading - destination_heading)

        # Check direction:
        if (current_heading - destination_heading + 360) %360 > 180:
            h = (current_heading - destination_heading + 180) %360
            h = (destination_heading - current_heading)
            print("Turning + : ", h)
        else:
            
            h = (current_heading - destination_heading)
            print("Turning - : ", h)
            

        if h > 180:
            h = h - 360
        elif h < -180:
            h = h + 360
        return math.radians(h)

###
# move_nao:
#
# Inputs:
#	direction: direction (forward or backward)
# 	(optionl) distance: distance to move (in meters)
#
# Returns:
#         N/A
###
    def move_nao(self, direction, distance=0.8):

        #print("")
        #print("Moving ", direction)
        if(direction == "forward"):
            x = distance
            y = 0
        elif(direction == "backward"):
                x = -distance
                y = 0

        self.motion_service.moveTo(x, y, 0, self.pepper_slow_move_config, _async=True)
        
###
# sidestep_nao:
#
# Inputs:
#	direction: direction (forward or backward)
# 	(optionl) distance: distance to move (in meters)
#
# Returns:
#         N/A
###
    def sidestep_nao(self, direction, distance=0.8):

        #print("")
        #print("Moving ", direction)
        if(direction == "left"):
            x = 0
            y = distance
        elif(direction == "right"):
                x = 0 #-distance # DISABLED
                y = -distance

        self.motion_service.moveTo(x, y, 0, self.pepper_slow_move_config, _async=True)
        
###
# set_tracking_state:
#
# 	Sets the tracking service to start moving (when tracking)
#
# Inputs:
#	state: bool (True or False)
#
# Returns:
#         N/A
###
    def set_tracking_state(self, state):
	
        print("")
        print("Tracking: ", state)
        print("Tracking ID: ", self.TRACKER_ID)
        if(state == True):
            #self.tracker_service.setRelativePosition([1.5, 0.4, 0.5, 0.1, 0.1, 0.3])
            #self.tracker_service.setRelativePosition([0.1, 0.0, 0.25, -30.0, -30.0, -30.0])
            self.tracker_service.setRelativePosition([0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
            self.tracker_service.track(self.targetName)
            
            
        elif(state == False):
            self.tracker_service.stopTracker()

###
# walk_until:
#
#     description: check if the target is further away than distance
#
# Inputs:
#	state: (bool) True or False: 
#	distance = (int), more than this value to allow the robot to walk (in meters)
#
# Returns:
#         no target = -1
#         target, no walking = 0
#         target, walking = 1 
###

    def walk_until(self):

        if(not self.tracker_service.isTargetLost()):
            data = self.tracker_service.getTargetPosition(0)
            #if self.DEBUG:
            print(data)
            
            #self.motion_service.moveTo(distance, 0, 0, self.pepper_slow_move_config)
            
            x, y, z = data
            # while x >= distance:
            #     print("walking")

            if x >= distance:
                #if self.DEBUG:
                print("Target: walking")
                #self.set_tracking_state(True)
                
                return 1
            else:
                #if self.DEBUG	:
                print("Target: completed walking")
                self.motion_service.stopMove()
                return 0

        else:
            #if self.DEBUG:
            print("no target")
            self.motion_service.stopMove()
            return -1


###
# follow_tracker:
#
#	Set the tracker ID to desired marker
#
# Inputs:
#	tracker_id: (int) tracker ID
#
# Returns:
#	N/A
###
    def follow_tracker(self, tracker_id):
    
        self.TRACKER_ID = tracker_id
        print("Following tracker: ", tracker_id)
        self.tracker_service.registerTarget(self.targetName, self.params)

###
# rotate_to_head_gaze:
#
#	Turns the robot to the direction the head is looking. Useful to get body oriented to a tracker.
#
# Inputs:
#	N/A
#
# Returns:
#	N/A
###        

    def rotate_to_head_gaze(self):
    
        names         = "HeadYaw"
        useSensors    = False
        commandAngles = self.motion_service.getAngles(names, useSensors)
        print("")
        print("Command angles:")
        a = commandAngles[0]
        print(a)

        self.turn_nao("angle", a )
	
###
# set_head_gaze:
#
#	Turns the robot head.
#
# Inputs:
#	angle (float) degrees
#
# Returns:
#	N/A
###        

    def set_head_gaze(self, angle):
    	
        names            = "HeadYaw"
        angles           = angle*almath.TO_RAD
        fractionMaxSpeed = 0.1

        self.motion_service.setAngles(names,angles,fractionMaxSpeed)
	
###
# get_heading:
#
# 	returns the heading in rads (by default) (based on the robot base), or specify "deg" for converted
#
# Inputs:
#	return_type: (str) rad or deg
#
# Returns:
#	robot heading (in rad or deg, as set by input)
###        
    def get_heading(self, return_type="rad"):
    
        #x = self.memory_service.getData("Device/SubDeviceList/InertialSensorBase/AngleX/Sensor/Value")
        #y = self.memory_service.getData("Device/SubDeviceList/InertialSensorBase/AngleY/Sensor/Value")
        z = self.memory_service.getData("Device/SubDeviceList/InertialSensorBase/AngleZ/Sensor/Value")
        print("")
        #print "x: ", x * 180 / math.pi
        #print "y: ", y * 180 / math.pi
        print("z: ", (z) * 180 / math.pi)
        #print ""

        if return_type == "rad":
            return z
        else:
            return z * 180 / math.pi
		
###
# get_tracker_distance:
#
# 	returns the distance to the current tracker
#
#
# Returns:
#	distance to tracker (cm) (float)
###        
    def get_tracker_distance(self):
    
        target_lost = self.tracker_service.isTargetLost()
        data = self.tracker_service.getTargetPosition(0)

        if target_lost:
            return None
        else:
            return data[0]
		
###
# main:
#
###
    def main(self):

        try:
            while True:
                pass

        except KeyboardInterrupt:
            print()
            print("Interrupted by user")
            print("Stopping...")

        # Stop tracker
        self.tracker_service.stopTracker()
        self.tracker_service.unregisterAllTargets()
        print("ALTracker stopped.")

        # Goto crouch position


###
#
#   if __main__
#
### 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")
    parser.add_argument("--ballsize", type=float, default=0.06,
                        help="Diameter of ball.")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
        
    nc = NaoController(session)
    nc.main()

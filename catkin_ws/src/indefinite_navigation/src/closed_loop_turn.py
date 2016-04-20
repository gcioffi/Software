#!/usr/bin/env python
"""
Created on Fri Apr 15 10:43:02 2016

@author: alex
"""
import rospkg
import yaml
import rospy
import time
from duckietown_msgs.msg import WheelsCmdStamped, Twist2DStamped
from duckietown_msgs.msg import AprilTags, TagDetection, TagInfo, Vector2D
import numpy as np
#import kinematic as k



class ClosedLoopTurn(object):
    """ """
    def __init__(self):    
        """ """
        self.node_name = rospy.get_name()
        
        # Publisher
        self.pub_wheels_cmd = rospy.Publisher("quackmobile/wheels_driver_node/wheels_cmd", WheelsCmdStamped, queue_size=1)
        
        # Timers
        self.loop_timer     = rospy.Timer( rospy.Duration.from_sec(10.0) , self.timedloop  )
        
        # Suscribers
        self.sub_april      = rospy.Subscriber("/quackmobile/apriltags_postprocessing_global_node/apriltags_out", AprilTags, self.callback, queue_size=1)
        
        
        # Params
        self.delay = 0.2
        
        
        rospy.loginfo("[%s] Initialized.", self.node_name)
        
        
    def timedloop(self, event):    
        """ """
        
        pass
        
        """
        self.go_fwd()
        
        time.sleep( 2  )
        
        self.go_bck()
        
        time.sleep( 2  )
        
        self.go_right()
        
        time.sleep( 2  )
        
        self.go_left()
        
        time.sleep( 2  )
        """
        
        
    def callback(self, msg):
        """ """
        
        # Localization
        [x,y] = self.localization( msg )
        
        if not x == None:
        
            # Compute error
            target = 0.30
            error  = target - x
            
            print target, x, error
            
            # Select Action        
            if error > 0:
                
                self.go_bck()
                rospy.loginfo("[%s] Going backward", self.node_name)
                
            else: 
                
                #self.go_fwd()
                #rospy.loginfo("[%s] Going forward", self.node_name)
                
                if y > 0:
                    
                    self.go_left()
                    rospy.loginfo("[%s] Going left", self.node_name)
                    
                else:
                    
                    self.go_right()
                    rospy.loginfo("[%s] Going right", self.node_name)
                
        else:
            
            self.stop()
            rospy.loginfo("[%s] No Detections", self.node_name)
        
        
    def localization(self, msg):
        """ """
        
        x = None
        y = None
        
        for detection in msg.detections:
            
            x = detection.transform.translation.x
            y = detection.transform.translation.y
            
        return [x,y]

        
        
    def go_fwd(self):
        """ """
        
        self.cmd = [ 0.2 , 0.2 ]
        self.pub_cmd()
        #time.sleep( self.delay )
        #self.stop()
        
    def go_bck(self):
        """ """
        
        self.cmd = [-0.2 ,-0.2 ]
        self.pub_cmd()
        #time.sleep( self.delay )
        #self.stop()
        
    def go_right(self):
        """ """
        
        self.cmd = [ 0.1 , 0.2 ]
        self.pub_cmd()
        #time.sleep( self.delay )
        #self.stop()
        
    def go_left(self):
        """ """
        
        self.cmd = [ 0.6 , 0.1 ]
        self.pub_cmd()
        #time.sleep( self.delay )
        #self.stop()
        
    def pub_cmd(self):
        """ """   
        
        msg_wheels_cmd = WheelsCmdStamped()
        msg_wheels_cmd.vel_right = self.cmd[0]
        msg_wheels_cmd.vel_left  = self.cmd[1]
        self.pub_wheels_cmd.publish(msg_wheels_cmd)
        
    def stop(self):
        """ """   
        
        msg_wheels_cmd = WheelsCmdStamped()
        msg_wheels_cmd.vel_right = 0
        msg_wheels_cmd.vel_left  = 0
        self.pub_wheels_cmd.publish(msg_wheels_cmd)
        
        
        
        
        

if __name__ == '__main__': 
    rospy.init_node('ClosedLoopTurn',anonymous=False)
    node = ClosedLoopTurn()
    rospy.spin()
#!/usr/bin/env python
import rospy

from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Twist
from morrf_ros.msg import mutli_objective_path

import math
#import the msg file - April_tag_Pos
MAXVEL = 60
RADIUS = 10

class Follower():
    def __init__(self):
        rospy.init_node("follower", anonymous=False)
        rospy.on_shutdown(self.shutdown)

        self.robot_movement = rospy.Publisher("cmd_vel", Twist, queue_size=10)

        self.robot_position = rospy.Subscriber("robot_pos", Pose2D, self.follow)
        self.path_getter = rospy.Subscriber("follower", multi_objective_path, self.start_follow)

        self.initialize == False

        self.lin_vel = 50

        self.rate = rospy.Rate(5)

        self.index = 0

        rospy.spin()

    def start_follow(self, path):
        self.path = path.waypoints
        self.initialize = True

    def follow(self, pos):

        if self.initialize == True:

            if self.index != (len(self.path) - 1):

                distance = self.dist(pos, self.path[self.index])
                if distance > 1:
                    p2 = self.path[self.index]

                    theta = math.atan2((p2.y - ry), (p2.x - rx) )

                    rob_move = Twist()
                    if distance < MAXVEL:
                        distance = 0

                    vel = min(MAXVEL, distance)
                    rob_move.linear.x = vel * math.cos(theta)
                    rob_move.linear.y = vel * math.cos(theta)
                    self.robot_movement.publish(rob_move)

                else:
                    self.index += 1

    def update_position(self, rob_pos):

        rob_move = Twist()
        rob_move.linear.x = lin_vel

        self.robot_movement.publish(rob_move)


    def update_orientation(self, rob_pos):
        rob_theta = rob_pos.theta

        rob_turn = Twist()

        if rob_theta - self.new_theta > 0:
            rob_turn.angular.z = 0 - self.ang_vel
        else:
            rob_turn.angular.z = 0 + self.ang_vel

        self.robot_movement.publish(rob_turn)

    def dist(p1, p2):
        return math.sqrt( (p2.x - p1.x)**2 + (p2.y - p2.y)**2 )

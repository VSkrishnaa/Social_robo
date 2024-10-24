#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Transform, Point
from people_msgs.msg import Person, People, PositionMeasurementArray

def callback(data):
    rospy.loginfo("Received leg tracker data")
    
    try:    
        if len(data.people) > 0:
            new_person = Person(
                "person_1",
                Point(data.people[0].pos.x, data.people[0].pos.y, 0),
                Point(0,0,0),
                0.0,
                [],[]
            )
            converted_people = People()
            converted_people.header = data.header
            converted_people.header.frame_id = "map"
            converted_people.people.append(new_person)
            pub.publish(converted_people)
            rospy.loginfo("Published person at position: x=%f, y=%f", 
                         data.people[0].pos.x, data.people[0].pos.y)
        else:
            rospy.logwarn("No people detected in leg tracker data")
    
    except Exception as e:
        rospy.logerr("Error processing leg tracker data: %s", str(e))
    
if __name__ == '__main__':
    rospy.init_node('peoplePublisher', anonymous=True)
    pub = rospy.Publisher('/people', People, queue_size=100)
    rate = rospy.Rate(300)
    rospy.loginfo("Starting people publisher node")
    rospy.Subscriber("/leg_tracker_measurements", PositionMeasurementArray, callback)
    rospy.spin()

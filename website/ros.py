import rospy
import rosnode
from std_msgs.msg import String
import os
from os.path import expanduser

dir = expanduser("~") + '/Desktop/'
def create_directories():
    global dir
    if not os.path.exists(dir + 'cabinet_db'):
        os.makedirs(dir + 'cabinet_db')
    dir = dir + 'cabinet_db/'


class ROS:
    def __init__(self):
        self.parrot_command_name = rospy.Publisher('web/parrot_command_name', String, queue_size=10)
        self.parrot_command = rospy.Publisher('web/parrot_commands', String, queue_size=10)
        self.parrot_voice_commands = rospy.Publisher('web/parrot_voice_commands', String, queue_size=10)
        self.stage_info = rospy.Publisher('web/stage', String, queue_size=10)
        self.dir_info = rospy.Publisher('web/dir', String, queue_size=10)
        self.wheel_status = rospy.Publisher('web/wheel_status', String, queue_size= 10)
        rospy.init_node('web_logger', anonymous=False, disable_signals= True)
        create_directories()



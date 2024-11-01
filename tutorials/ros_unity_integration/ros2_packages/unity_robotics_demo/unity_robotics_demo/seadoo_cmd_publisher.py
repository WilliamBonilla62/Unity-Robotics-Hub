#!/usr/bin/env python

import rospy
import rosgraph
import time
from your_ros_package_name.msg import SeadooCmdMsg  # Replace with your actual package and message name

TOPIC_NAME = 'seadooCmd'
NODE_NAME = 'seadoo_cmd_publisher'


def post_seadoo_cmd():
    pub = rospy.Publisher(TOPIC_NAME, SeadooCmdMsg, queue_size=10)
    rospy.init_node(NODE_NAME, anonymous=True)

    # Example data (you may replace these with dynamically updated values)
    thr_cmd = 0.8  # Throttle command [0,1]
    str_cmd = 0.5  # Steering command [-1,1]
    brk_cmd = False  # Brake command
    vts_cmd = 5.0  # VTS command (nozzle angle) [-12,12]

    # Create and publish SeadooCmdMsg message
    seadoo_cmd_msg = SeadooCmdMsg()
    seadoo_cmd_msg.thr_cmd = thr_cmd
    seadoo_cmd_msg.str_cmd = str_cmd
    seadoo_cmd_msg.brk_cmd = brk_cmd
    seadoo_cmd_msg.vts_cmd = vts_cmd

    wait_for_connections(pub, TOPIC_NAME)
    pub.publish(seadoo_cmd_msg)

    time.sleep(0.1)


def wait_for_connections(pub, topic):
    ros_master = rosgraph.Master('/rostopic')
    topic = rosgraph.names.script_resolve_name('rostopic', topic)
    num_subs = 0
    for sub in ros_master.getSystemState()[1]:
        if sub[0] == topic:
            num_subs += 1

    for i in range(10):
        if pub.get_num_connections() == num_subs:
            return
        time.sleep(0.1)
    raise RuntimeError("Failed to connect publisher to subscribers")


if __name__ == '__main__':
    try:
        post_seadoo_cmd()
    except rospy.ROSInterruptException:
        pass

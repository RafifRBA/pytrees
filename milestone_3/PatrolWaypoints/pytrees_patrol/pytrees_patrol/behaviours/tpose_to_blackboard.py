# Data Gathering, menyimpan posisi turtle ke blackboard

import py_trees
import py_trees_ros
from turtlesim.msg import Pose

class PoseToBlackboard(py_trees_ros.subscribers.ToBlackboard):
    def __init__(self, name: str = "Pose to BB"):
        super().__init__(
            name=name,
            topic_name="/turtle1/pose",
            topic_type=Pose,
            qos_profile=py_trees_ros.utilities.qos_profile_unlatched(),
            blackboard_variables={"pose": None},
            initialise_variables={"pose": None},
        )

    def update(self):
        super().update()
        return py_trees.common.Status.RUNNING
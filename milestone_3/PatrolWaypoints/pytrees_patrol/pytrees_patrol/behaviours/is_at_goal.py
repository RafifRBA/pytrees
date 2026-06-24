# Mengecek jarak sekarang apakah sudah pada jarak target akhir (toleransi jarak 0.3)

import py_trees
import py_trees_ros
import math

class IsAtGoal(py_trees.behaviour.Behaviour):
    def __init__(self,
                 goal_x: float,
                 goal_y: float,
                 tolerance: float = 0.3,               
                 name: str = "Sudah sampai target?"):
        super().__init__(name=name)
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.tolerance = tolerance

        self.blackboard = self.attach_blackboard_client(name="IsAtGoal")
        self.blackboard.register_key(key="pose", access=py_trees.common.Access.READ)

    def update(self):
        if self.blackboard.pose is None:
            return py_trees.common.Status.RUNNING
        
        pose = self.blackboard.pose
        jarak = math.sqrt((pose.x - self.goal_x)**2 + (pose.y - self.goal_y)**2)

        self.feedback_message = f"Jarak ke goal: {jarak:.2f}"

        if jarak < self.tolerance:
            return py_trees.common.Status.SUCCESS
        
        return py_trees.common.Status.FAILURE


import math
import py_trees
from geometry_msgs.msg import Twist


class MoveTo(py_trees.behaviour.Behaviour):
    def __init__(self,
                 goal_x: float,
                 goal_y: float,
                 node,
                 name: str = "Gerak ke Goal"):

        super().__init__(name=name)
        self.goal_x = goal_x
        self.goal_y = goal_y
        self.node = node

        self.tolerance = 0.3
        self.heading_tolerance = 0.15

        self.kp_linear = 1.5
        self.kp_angular = 3.0
        self.max_angular = 1.5
        self.max_linear = 3.0

        self.publisher = self.node.create_publisher(
            Twist, "/turtle1/cmd_vel", 10
        )

        self.blackboard = self.attach_blackboard_client(name="Move To")
        self.blackboard.register_key(key="pose", access=py_trees.common.Access.READ)

    def initialise(self):
        self.feedback_message = "Mulai bergerak ke goal"

    def update(self):
        if self.blackboard.pose is None:
            return py_trees.common.Status.RUNNING

        pose = self.blackboard.pose

        dx = self.goal_x - pose.x
        dy = self.goal_y - pose.y
        jarak = math.sqrt(dx**2 + dy**2)

        if jarak < self.tolerance:
            self._stop()
            return py_trees.common.Status.SUCCESS

        sudut_ke_goal = math.atan2(dy, dx)
        error_sudut = math.atan2(
            math.sin(sudut_ke_goal - pose.theta),
            math.cos(sudut_ke_goal - pose.theta),
        )

        twist = Twist()
        ang = self.kp_angular * error_sudut
        ang = max(-self.max_angular, min(self.max_angular, ang))

        if abs(error_sudut) > self.heading_tolerance:
            twist.linear.x = 0.0
            twist.angular.z = ang
            self.feedback_message = f"Memutar, error: {math.degrees(error_sudut):.1f}°"
        else:
            lin = self.kp_linear * jarak
            lin = min(lin, self.max_linear)
            twist.linear.x = lin
            twist.angular.z = ang
            self.feedback_message = f"Maju lurus, jarak: {jarak:.2f}"

        self.publisher.publish(twist)
        return py_trees.common.Status.RUNNING

    def terminate(self, new_status):
        self._stop()

    def _stop(self):
        stop = Twist()
        self.publisher.publish(stop)

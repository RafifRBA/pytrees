import rclpy
import py_trees
import py_trees_ros

from pytrees_patrol.behaviours.tpose_to_blackboard import PoseToBlackboard
from pytrees_patrol.behaviours.is_at_goal import IsAtGoal
from pytrees_patrol.behaviours.move_to import MoveTo

from py_trees.composites import Parallel, Sequence, Selector
from py_trees.decorators import Timeout

def waypoints(goal_x, goal_y, index, node):
    subtree = Selector(
        name=f"Ke Wp {index}", memory=False
    )
    
    is_at_goal = IsAtGoal(
        goal_x=goal_x,
        goal_y=goal_y,
        name=f"Sudah sampai WP {index}"
    )

    move_to = Timeout(
        child=MoveTo(goal_x=goal_x, goal_y=goal_y, node=node),
        name="Timeout",
        duration=8.0
    )

    subtree.add_children([is_at_goal, move_to])
    return subtree

def create_root(node):
    target_waypoints = [
        (6.0, 5.544445),
        (6.0, 6.544445),
        (6.0, 5.544445),
        (9.6, 5.544445),
        (10.0, 4.544445),
        (10.0, 7.544445),
        (9.0, 7.544445),
        (10.0, 7.544445),
        (10.0, 10.544445),
        (8.0, 10.544445),
        (8.0, 8.544445),
        (7.0, 8.544445),
        (7.0, 10.544445),
        (3.0, 10.544445),
        (2.0, 10.0),
        (2.0, 11.0),
        (3.0, 11.0),
        (3.0, 7.544445),
        (3.0, 5.544445),
        (2.0, 5.544445),
        (3.0, 5.544445)
    ]

    root = Parallel(
        name="Patrol",
        policy=py_trees.common.ParallelPolicy.SuccessOnOne()
    )

    pose_to_bb = PoseToBlackboard()

    patrol_seq = Sequence(name="Waypoints", memory=True)
    for i, (x, y) in enumerate(target_waypoints):
        patrol_seq.add_child(waypoints(x, y, i, node))

    root.add_children([pose_to_bb, patrol_seq])

    return root

def main():
    rclpy.init()
    node = rclpy.create_node("py_trees_patrol")

    root = create_root(node)

    py_trees.display.render_dot_tree(root, name="py_trees_patrol")

    trees = py_trees_ros.trees.BehaviourTree(
        root=root,
        unicode_tree_debug=True
    )

    try:
        trees.setup(node=node, timeout=15.0)
    except Exception as e:
        print(f"Gagal setup: {e}")
        rclpy.shutdown()
        return
    
    trees.tick_tock(period_ms=500)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        trees.shutdown()
        node.destroy_node()
        rclpy.shutdown()
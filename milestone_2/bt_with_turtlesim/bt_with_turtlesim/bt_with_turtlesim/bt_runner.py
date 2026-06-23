# bt_runner.py
import rclpy
import py_trees
import py_trees_ros

from bt_with_turtlesim.behaviours.tpose_to_blackboard import PoseToBlackboard
from bt_with_turtlesim.behaviours.is_at_goal import IsAtGoal
from bt_with_turtlesim.behaviours.move_to import MoveTo


def buat_tree(node, target_x, target_y):
    
    """
    Struktur tree:

    Sequence "Ke Goal"
    ├── PoseToBlackboard   ← Data Gathering
    └── Selector "Navigasi"
        ├── IsAtGoal       ← sudah sampai? → SUCCESS, selesai
        └── Timeout(8s) → MoveTo   ← belum sampai → gerak
    """

    # Root
    root = py_trees.composites.Sequence(
        name="Ke Goal", memory=False
    )

    # Data gatherer
    pose_to_bb = PoseToBlackboard()

    # Navigasi
    navigasi = py_trees.composites.Selector(
        name="Navigasi", memory=False
    )

    is_at_goal = IsAtGoal(goal_x=target_x, goal_y=target_y)

    move_to = py_trees.decorators.Timeout(
        child=MoveTo(goal_x=target_x, goal_y=target_y, node=node),
        name="MoveTo (maks 8s)",
        duration=8.0
    )

    navigasi.add_children([is_at_goal, move_to])
    root.add_children([pose_to_bb, navigasi])

    return root


def main():
    rclpy.init()

    # Buat node ROS2 dulu, lalu pass ke tree
    node = rclpy.create_node("bt_runner")

    root = buat_tree(node, 8.6, 6.0) # Ubah ubah param x target dan y target disini

    tree = py_trees_ros.trees.BehaviourTree(
        root=root,
        unicode_tree_debug=True  # print tree state ke terminal tiap tick
    )

    try:
        tree.setup(node=node, timeout=15.0)
    except Exception as e:
        print(f"Gagal setup tree: {e}")
        rclpy.shutdown()
        return

    tree.tick_tock(period_ms=500)  # tick tiap 500ms

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        tree.shutdown()
        node.destroy_node()
        rclpy.shutdown()
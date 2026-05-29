import math

import rclpy
from rclpy.node import Node


class MissionNode(Node):
    def __init__(self):
        super().__init__('mission_node')

        self.declare_parameter('mode', 'straight_then_turn')
        self.declare_parameter('heading_ref_deg', 0.0)
        self.declare_parameter('turn_heading_deg', 30.0)
        self.declare_parameter('turn_after_sec', 20.0)

        self.start_time = self.get_clock().now()
        self.timer = self.create_timer(0.5, self.update_references)

        self.get_logger().info('Mission node started.')

    def update_references(self):
        mode = self.get_parameter('mode').value
        heading_ref_deg = float(self.get_parameter('heading_ref_deg').value)
        turn_heading_deg = float(self.get_parameter('turn_heading_deg').value)
        turn_after_sec = float(self.get_parameter('turn_after_sec').value)

        elapsed = (self.get_clock().now() - self.start_time).nanoseconds * 1e-9

        if mode == 'straight_then_turn':
            if elapsed < turn_after_sec:
                active_heading = heading_ref_deg
            else:
                active_heading = turn_heading_deg
        else:
            active_heading = heading_ref_deg

        self.set_parameters([
            rclpy.parameter.Parameter(
                'heading_ref_deg',
                rclpy.Parameter.Type.DOUBLE,
                active_heading
            )
        ])

        self.get_logger().info(
            f'Mission mode={mode}, elapsed={elapsed:.1f}s, heading_ref_deg={active_heading:.1f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = MissionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
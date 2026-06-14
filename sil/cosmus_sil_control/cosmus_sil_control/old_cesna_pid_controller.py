import math

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64


def saturate(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def wrap_pi(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


def quaternion_to_euler(x, y, z, w):
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2.0 * (w * y - z * x)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


class CesnaPidController(Node):
    def __init__(self):
        super().__init__('cesna_pid_controller')

        self.declare_parameter('odom_topic', '/plane00/odometry')
        self.declare_parameter('imu_topic', '/plane00/imu')

        self.declare_parameter('throttle_topic', '/plane00/cmd_throttle')
        self.declare_parameter('elevator_topic', '/plane00/cmd_elevator')
        self.declare_parameter('rudder_topic', '/plane00/cmd_rudder')
        self.declare_parameter('left_elevon_topic', '/plane00/cmd_left_elevon')
        self.declare_parameter('right_elevon_topic', '/plane00/cmd_right_elevon')

        self.declare_parameter('speed_ref', 20.0)
        self.declare_parameter('altitude_ref', 30.0)
        self.declare_parameter('heading_ref_deg', 0.0)

        self.declare_parameter('trim_throttle', 0.50)
        self.declare_parameter('trim_elevator', 0.00)
        self.declare_parameter('trim_roll', 0.05)
        self.declare_parameter('trim_rudder', 0.00)

        self.declare_parameter('kp_speed', 0.03)
        self.declare_parameter('ki_speed', 0.002)
        self.declare_parameter('kd_speed', 0.0)

        self.declare_parameter('kp_altitude', 0.015)
        self.declare_parameter('ki_altitude', 0.001)
        self.declare_parameter('kd_altitude', 0.0)

        self.declare_parameter('kp_pitch', 1.20)
        self.declare_parameter('kd_pitch', 0.10)

        self.declare_parameter('kp_heading', 1.00)
        self.declare_parameter('kp_roll', 1.20)
        self.declare_parameter('kd_roll', 0.10)

        self.declare_parameter('max_roll_deg', 15.0)
        self.declare_parameter('max_pitch_deg', 12.0)

        self.declare_parameter('throttle_min', 0.0)
        self.declare_parameter('throttle_max', 60.0)
        self.declare_parameter('surface_min', -2.0)
        self.declare_parameter('surface_max', 2.0)
        self.declare_parameter('rudder_min', -0.3)
        self.declare_parameter('rudder_max', 0.3)

        self.declare_parameter('loop_rate_hz', 50.0)

        self.roll = 0.0
        self.pitch = 0.0
        self.yaw = 0.0
        self.altitude = 0.0
        self.speed = 0.0

        self.p_rate = 0.0
        self.q_rate = 0.0
        self.r_rate = 0.0

        self.int_speed = 0.0
        self.int_altitude = 0.0
        self.prev_speed_error = 0.0
        self.prev_altitude_error = 0.0

        odom_topic = self.get_parameter('odom_topic').value
        imu_topic = self.get_parameter('imu_topic').value
        throttle_topic = self.get_parameter('throttle_topic').value
        elevator_topic = self.get_parameter('elevator_topic').value
        rudder_topic = self.get_parameter('rudder_topic').value
        left_elevon_topic = self.get_parameter('left_elevon_topic').value
        right_elevon_topic = self.get_parameter('right_elevon_topic').value
        loop_rate_hz = float(self.get_parameter('loop_rate_hz').value)

        self.create_subscription(Odometry, odom_topic, self.odom_callback, 10)
        self.create_subscription(Imu, imu_topic, self.imu_callback, 10)

        self.throttle_pub = self.create_publisher(Float64, throttle_topic, 10)
        self.elevator_pub = self.create_publisher(Float64, elevator_topic, 10)
        self.rudder_pub = self.create_publisher(Float64, rudder_topic, 10)
        self.left_elevon_pub = self.create_publisher(Float64, left_elevon_topic, 10)
        self.right_elevon_pub = self.create_publisher(Float64, right_elevon_topic, 10)

        self.dt = 1.0 / loop_rate_hz
        self.create_timer(self.dt, self.control_loop)

        self.get_logger().info('Cesna PID controller ready for /plane00.')

    def odom_callback(self, msg):
        q = msg.pose.pose.orientation
        self.roll, self.pitch, self.yaw = quaternion_to_euler(q.x, q.y, q.z, q.w)

        self.altitude = msg.pose.pose.position.z

        vx = msg.twist.twist.linear.x
        vy = msg.twist.twist.linear.y
        vz = msg.twist.twist.linear.z
        self.speed = math.sqrt(vx * vx + vy * vy + vz * vz)

    def imu_callback(self, msg):
        self.p_rate = msg.angular_velocity.x
        self.q_rate = msg.angular_velocity.y
        self.r_rate = msg.angular_velocity.z

    def publish_float(self, publisher, value):
        msg = Float64()
        msg.data = float(value)
        publisher.publish(msg)

    def control_loop(self):
        speed_ref = float(self.get_parameter('speed_ref').value)
        altitude_ref = float(self.get_parameter('altitude_ref').value)
        heading_ref = math.radians(float(self.get_parameter('heading_ref_deg').value))

        trim_throttle = float(self.get_parameter('trim_throttle').value)
        trim_elevator = float(self.get_parameter('trim_elevator').value)
        trim_roll = float(self.get_parameter('trim_roll').value)
        trim_rudder = float(self.get_parameter('trim_rudder').value)

        kp_speed = float(self.get_parameter('kp_speed').value)
        ki_speed = float(self.get_parameter('ki_speed').value)
        kd_speed = float(self.get_parameter('kd_speed').value)

        kp_altitude = float(self.get_parameter('kp_altitude').value)
        ki_altitude = float(self.get_parameter('ki_altitude').value)
        kd_altitude = float(self.get_parameter('kd_altitude').value)

        kp_pitch = float(self.get_parameter('kp_pitch').value)
        kd_pitch = float(self.get_parameter('kd_pitch').value)

        kp_heading = float(self.get_parameter('kp_heading').value)
        kp_roll = float(self.get_parameter('kp_roll').value)
        kd_roll = float(self.get_parameter('kd_roll').value)

        max_roll = math.radians(float(self.get_parameter('max_roll_deg').value))
        max_pitch = math.radians(float(self.get_parameter('max_pitch_deg').value))

        throttle_min = float(self.get_parameter('throttle_min').value)
        throttle_max = float(self.get_parameter('throttle_max').value)
        surface_min = float(self.get_parameter('surface_min').value)
        surface_max = float(self.get_parameter('surface_max').value)
        rudder_min = float(self.get_parameter('rudder_min').value)
        rudder_max = float(self.get_parameter('rudder_max').value)

        speed_error = speed_ref - self.speed
        self.int_speed += speed_error * self.dt
        self.int_speed = saturate(self.int_speed, -10.0, 10.0)
        d_speed_error = (speed_error - self.prev_speed_error) / self.dt

        throttle_cmd = trim_throttle + kp_speed * speed_error + ki_speed * self.int_speed + kd_speed * d_speed_error
        throttle_cmd = saturate(throttle_cmd, throttle_min, throttle_max)

        altitude_error = altitude_ref - self.altitude
        self.int_altitude += altitude_error * self.dt
        self.int_altitude = saturate(self.int_altitude, -20.0, 20.0)
        d_altitude_error = (altitude_error - self.prev_altitude_error) / self.dt

        pitch_ref = kp_altitude * altitude_error + ki_altitude * self.int_altitude + kd_altitude * d_altitude_error
        pitch_ref = saturate(pitch_ref, -max_pitch, max_pitch)

        elevator_cmd = trim_elevator + kp_pitch * (pitch_ref - self.pitch) - kd_pitch * self.q_rate
        elevator_cmd = saturate(elevator_cmd, surface_min, surface_max)

        heading_error = wrap_pi(heading_ref - self.yaw)
        roll_ref = saturate(kp_heading * heading_error, -max_roll, max_roll)

        roll_cmd = trim_roll + kp_roll * (roll_ref - self.roll) - kd_roll * self.p_rate
        roll_cmd = saturate(roll_cmd, surface_min, surface_max)

        rudder_cmd = trim_rudder + 0.10 * heading_error - 0.05 * self.r_rate
        rudder_cmd = saturate(rudder_cmd, rudder_min, rudder_max)

        left_elevon_cmd = saturate(-roll_cmd, surface_min, surface_max)
        right_elevon_cmd = saturate(roll_cmd, surface_min, surface_max)

        thrust_max = 30.0  # N, ganho inicial
        thrust_min = 0.0
        thrust_max = 30.0
        self.publish_float(self.throttle_pub, throttle_cmd * thrust_max)

        self.prev_speed_error = speed_error
        self.prev_altitude_error = altitude_error


def main(args=None):
    rclpy.init(args=args)
    node = CesnaPidController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
adicione isso para mais aviões

# ============================================================
# PLANE01

  # IMU
- ros_topic_name: "/plane01/imu"
  gz_topic_name: "/model/plane01/imu"
  ros_type_name: "sensor_msgs/msg/Imu"
  gz_type_name: "gz.msgs.IMU"
  direction: GZ_TO_ROS
  lazy: false

# GPS / NavSat
- ros_topic_name: "/plane01/navsat"
  gz_topic_name: "/model/plane01/navsat"
  ros_type_name: "sensor_msgs/msg/NavSatFix"
  gz_type_name: "gz.msgs.NavSat"
  direction: GZ_TO_ROS
  lazy: false

# Odometria
- ros_topic_name: "/plane01/odometry"
  gz_topic_name: "/model/plane01/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
  lazy: false

# TF / Pose
- ros_topic_name: "/tf"
  gz_topic_name: "/model/plane01/tf"
  ros_type_name: "tf2_msgs/msg/TFMessage"
  gz_type_name: "gz.msgs.Pose_V"
  direction: GZ_TO_ROS
  lazy: false

# Throttle (velocidade do motor / hélice)
- ros_topic_name: "/plane01/cmd_throttle"
  gz_topic_name: "/model/plane01/joint/rotor_puller_joint/cmd_vel"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron esquerdo
- ros_topic_name: "/plane01/cmd_left_elevon"
  gz_topic_name: "/model/plane01/joint/left_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron direito
- ros_topic_name: "/plane01/cmd_right_elevon"
  gz_topic_name: "/model/plane01/joint/right_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Elevator (profundor)
- ros_topic_name: "/plane01/cmd_elevator"
  gz_topic_name: "/model/plane01/joint/elevator_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Rudder (leme direcional)
- ros_topic_name: "/plane01/cmd_rudder"
  gz_topic_name: "/model/plane01/joint/rudder_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

  # ============================================================
# PLANE02

  # IMU
- ros_topic_name: "/plane02/imu"
  gz_topic_name: "/model/plane02/imu"
  ros_type_name: "sensor_msgs/msg/Imu"
  gz_type_name: "gz.msgs.IMU"
  direction: GZ_TO_ROS
  lazy: false

# GPS / NavSat
- ros_topic_name: "/plane02/navsat"
  gz_topic_name: "/model/plane02/navsat"
  ros_type_name: "sensor_msgs/msg/NavSatFix"
  gz_type_name: "gz.msgs.NavSat"
  direction: GZ_TO_ROS
  lazy: false

# Odometria
- ros_topic_name: "/plane02/odometry"
  gz_topic_name: "/model/plane02/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
  lazy: false

# TF / Pose
- ros_topic_name: "/tf"
  gz_topic_name: "/model/plane02/tf"
  ros_type_name: "tf2_msgs/msg/TFMessage"
  gz_type_name: "gz.msgs.Pose_V"
  direction: GZ_TO_ROS
  lazy: false

# Throttle (velocidade do motor / hélice)
- ros_topic_name: "/plane02/cmd_throttle"
  gz_topic_name: "/model/plane02/joint/rotor_puller_joint/cmd_vel"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron esquerdo
- ros_topic_name: "/plane02/cmd_left_elevon"
  gz_topic_name: "/model/plane02/joint/left_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron direito
- ros_topic_name: "/plane02/cmd_right_elevon"
  gz_topic_name: "/model/plane02/joint/right_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Elevator (profundor)
- ros_topic_name: "/plane02/cmd_elevator"
  gz_topic_name: "/model/plane02/joint/elevator_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Rudder (leme direcional)
- ros_topic_name: "/plane02/cmd_rudder"
  gz_topic_name: "/model/plane02/joint/rudder_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

  # ============================================================
# PLANE03

  # IMU
- ros_topic_name: "/plane03/imu"
  gz_topic_name: "/model/plane03/imu"
  ros_type_name: "sensor_msgs/msg/Imu"
  gz_type_name: "gz.msgs.IMU"
  direction: GZ_TO_ROS
  lazy: false

# GPS / NavSat
- ros_topic_name: "/plane03/navsat"
  gz_topic_name: "/model/plane03/navsat"
  ros_type_name: "sensor_msgs/msg/NavSatFix"
  gz_type_name: "gz.msgs.NavSat"
  direction: GZ_TO_ROS
  lazy: false

# Odometria
- ros_topic_name: "/plane03/odometry"
  gz_topic_name: "/model/plane03/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
  lazy: false

# TF / Pose
- ros_topic_name: "/tf"
  gz_topic_name: "/model/plane03/tf"
  ros_type_name: "tf2_msgs/msg/TFMessage"
  gz_type_name: "gz.msgs.Pose_V"
  direction: GZ_TO_ROS
  lazy: false

# Throttle (velocidade do motor / hélice)
- ros_topic_name: "/plane03/cmd_throttle"
  gz_topic_name: "/model/plane03/joint/rotor_puller_joint/cmd_vel"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron esquerdo
- ros_topic_name: "/plane03/cmd_left_elevon"
  gz_topic_name: "/model/plane03/joint/left_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron direito
- ros_topic_name: "/plane03/cmd_right_elevon"
  gz_topic_name: "/model/plane03/joint/right_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Elevator (profundor)
- ros_topic_name: "/plane03/cmd_elevator"
  gz_topic_name: "/model/plane03/joint/elevator_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Rudder (leme direcional)
- ros_topic_name: "/plane03/cmd_rudder"
  gz_topic_name: "/model/plane03/joint/rudder_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

  # ============================================================
# PLANE04

  # IMU
- ros_topic_name: "/plane04/imu"
  gz_topic_name: "/model/plane04/imu"
  ros_type_name: "sensor_msgs/msg/Imu"
  gz_type_name: "gz.msgs.IMU"
  direction: GZ_TO_ROS
  lazy: false

# GPS / NavSat
- ros_topic_name: "/plane04/navsat"
  gz_topic_name: "/model/plane04/navsat"
  ros_type_name: "sensor_msgs/msg/NavSatFix"
  gz_type_name: "gz.msgs.NavSat"
  direction: GZ_TO_ROS
  lazy: false

# Odometria
- ros_topic_name: "/plane04/odometry"
  gz_topic_name: "/model/plane04/odometry"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS
  lazy: false

# TF / Pose
- ros_topic_name: "/tf"
  gz_topic_name: "/model/plane04/tf"
  ros_type_name: "tf2_msgs/msg/TFMessage"
  gz_type_name: "gz.msgs.Pose_V"
  direction: GZ_TO_ROS
  lazy: false

# Throttle (velocidade do motor / hélice)
- ros_topic_name: "/plane04/cmd_throttle"
  gz_topic_name: "/model/plane04/joint/rotor_puller_joint/cmd_vel"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron esquerdo
- ros_topic_name: "/plane04/cmd_left_elevon"
  gz_topic_name: "/model/plane04/joint/left_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Aileron direito
- ros_topic_name: "/plane04/cmd_right_elevon"
  gz_topic_name: "/model/plane04/joint/right_elevon_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Elevator (profundor)
- ros_topic_name: "/plane04/cmd_elevator"
  gz_topic_name: "/model/plane04/joint/elevator_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false

# Rudder (leme direcional)
- ros_topic_name: "/plane04/cmd_rudder"
  gz_topic_name: "/model/plane04/joint/rudder_joint/cmd_pos"
  ros_type_name: "std_msgs/msg/Float64"
  gz_type_name: "gz.msgs.Double"
  direction: ROS_TO_GZ
  lazy: false


#!/usr/bin/env python3
"""
COSMUS Serial Bridge — ESP32 <-> ROS 2
Versão completa com:
- Reconexão automática da serial
- Input do teclado no terminal (sem precisar do Serial Monitor)
- Publica direto no ROS (funciona sem ESP32)
- Recebe IMU e GPS do Gazebo e envia para o ESP32
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu, NavSatFix
import serial
import threading
import time

SERIAL_PORT = '/dev/ttyACM0'   # trocar para /dev/ttyUSB0 se necessário
BAUD_RATE   = 115200


class CosmosSerialBridge(Node):
    def __init__(self):
        super().__init__('cosmus_serial_bridge')

        # ── Publishers → envia para o Gazebo ──────────────────────────
        self.throttle_pub     = self.create_publisher(Float64, '/plane00/cmd_throttle',     10)
        self.elevator_pub     = self.create_publisher(Float64, '/plane00/cmd_elevator',     10)
        self.rudder_pub       = self.create_publisher(Float64, '/plane00/cmd_rudder',       10)
        self.left_elevon_pub  = self.create_publisher(Float64, '/plane00/cmd_left_elevon',  10)
        self.right_elevon_pub = self.create_publisher(Float64, '/plane00/cmd_right_elevon', 10)

        # ── Subscribers ← recebe do Gazebo ────────────────────────────
        self.create_subscription(Imu,       '/plane00/imu',    self.imu_cb,    10)
        self.create_subscription(NavSatFix, '/plane00/navsat', self.navsat_cb, 10)

        # ── Serial ────────────────────────────────────────────────────
        self.ser = None
        self.connect_serial()

        # ── Threads ───────────────────────────────────────────────────
        self.serial_thread = threading.Thread(target=self.read_serial_loop, daemon=True)
        self.serial_thread.start()

        self.input_thread = threading.Thread(target=self.keyboard_input_loop, daemon=True)
        self.input_thread.start()

    # ──────────────────────────────────────────────────────────────────
    # Serial
    # ──────────────────────────────────────────────────────────────────

    def connect_serial(self):
        """Tenta conectar/reconectar na serial (não bloqueia se falhar)"""
        try:
            self.ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1.0)
            time.sleep(2.0)   # aguarda ESP32 inicializar
            self.get_logger().info(f'Serial conectada em {SERIAL_PORT}')
        except Exception as e:
            self.get_logger().warning(f'Serial não disponível ({e}) — modo ROS-only ativo')
            self.ser = None

    def read_serial_loop(self):
        """Lê comandos vindos do ESP32 e publica no ROS"""
        while rclpy.ok():
            try:
                if not self.ser or not self.ser.is_open:
                    time.sleep(2.0)
                    self.connect_serial()
                    continue

                line = self.ser.readline().decode('utf-8').strip()
                if not line:
                    continue

                # Ignorar mensagens de eco/status do ESP32
                if line.startswith('COSMUS') or line.startswith('CMD_RECEIVED'):
                    self.get_logger().info(f'ESP32: {line}')
                    continue

                self.get_logger().info(f'Serial→ROS: {line}')
                self._publish_command(line)

            except serial.SerialException as e:
                self.get_logger().warning(f'Serial desconectada: {e}')
                self.ser = None
                time.sleep(2.0)
                self.connect_serial()
            except (ValueError, UnicodeDecodeError):
                pass
            except Exception as e:
                self.get_logger().warning(f'Erro leitura serial: {e}')

    # ──────────────────────────────────────────────────────────────────
    # Keyboard input
    # ──────────────────────────────────────────────────────────────────

    def keyboard_input_loop(self):
        """Lê comandos do teclado e publica no ROS (e envia pela serial)"""
        print("\n╔══════════════════════════════════════════╗")
        print("║      COSMUS HIL — Controle Serial        ║")
        print("╠══════════════════════════════════════════╣")
        print("║  T:<val>   Throttle      ex: T:500       ║")
        print("║  E:<val>   Elevator      ex: E:0.3       ║")
        print("║  R:<val>   Rudder        ex: R:0.2       ║")
        print("║  L:<val>   Left elevon   ex: L:0.1       ║")
        print("║  D:<val>   Right elevon  ex: D:0.1       ║")
        print("║  STOP      Para todos os atuadores       ║")
        print("║  q         Encerra o bridge              ║")
        print("╚══════════════════════════════════════════╝\n")

        while rclpy.ok():
            try:
                cmd = input("cmd> ").strip()

                if not cmd:
                    continue

                if cmd.lower() == 'q':
                    self.get_logger().info('Encerrando bridge...')
                    rclpy.shutdown()
                    break

                if cmd.upper() == 'STOP':
                    for c in ['T:0', 'E:0', 'R:0', 'L:0', 'D:0']:
                        self._send_and_publish(c)
                    print(">>> STOP — todos os atuadores zerados")
                    continue

                self._send_and_publish(cmd)

            except EOFError:
                break
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.get_logger().warning(f'Erro input: {e}')

    # ──────────────────────────────────────────────────────────────────
    # Helpers
    # ──────────────────────────────────────────────────────────────────

    def _send_and_publish(self, cmd: str):
        """Envia pela serial para o ESP32 E publica direto no ROS"""

        # 1 — Enviar pela serial (se disponível)
        if self.ser and self.ser.is_open:
            try:
                self.ser.write(f'{cmd}\n'.encode())
            except Exception as e:
                self.get_logger().warning(f'Erro ao escrever na serial: {e}')

        # 2 — Publicar direto no ROS
        self._publish_command(cmd)

    def _publish_command(self, cmd: str):
        """Interpreta o comando e publica no tópico ROS correto"""
        try:
            if cmd.startswith('T:'):
                msg = Float64(); msg.data = float(cmd[2:])
                self.throttle_pub.publish(msg)
                print(f'    ✓ Throttle     → {msg.data}')

            elif cmd.startswith('E:'):
                msg = Float64(); msg.data = float(cmd[2:])
                self.elevator_pub.publish(msg)
                print(f'    ✓ Elevator     → {msg.data}')

            elif cmd.startswith('R:'):
                msg = Float64(); msg.data = float(cmd[2:])
                self.rudder_pub.publish(msg)
                print(f'    ✓ Rudder       → {msg.data}')

            elif cmd.startswith('L:'):
                msg = Float64(); msg.data = float(cmd[2:])
                self.left_elevon_pub.publish(msg)
                print(f'    ✓ Left elevon  → {msg.data}')

            elif cmd.startswith('D:'):
                msg = Float64(); msg.data = float(cmd[2:])
                self.right_elevon_pub.publish(msg)
                print(f'    ✓ Right elevon → {msg.data}')

            else:
                print(f'    ? Comando desconhecido: {cmd}')

        except ValueError:
            print(f'    ! Valor inválido em: {cmd}')

    # ──────────────────────────────────────────────────────────────────
    # Callbacks dos sensores (Gazebo → ESP32)
    # ──────────────────────────────────────────────────────────────────

    def imu_cb(self, msg: Imu):
        """Recebe IMU do Gazebo e envia para o ESP32 via serial"""
        if not self.ser or not self.ser.is_open:
            return
        try:
            ax = msg.linear_acceleration.x
            ay = msg.linear_acceleration.y
            az = msg.linear_acceleration.z
            wx = msg.angular_velocity.x
            wy = msg.angular_velocity.y
            wz = msg.angular_velocity.z
            linha = f'IMU:{ax:.3f},{ay:.3f},{az:.3f},{wx:.4f},{wy:.4f},{wz:.4f}\n'
            self.ser.write(linha.encode())
        except Exception as e:
            self.get_logger().warning(f'Erro ao enviar IMU: {e}')

    def navsat_cb(self, msg: NavSatFix):
        """Recebe GPS do Gazebo e envia para o ESP32 via serial"""
        if not self.ser or not self.ser.is_open:
            return
        try:
            linha = f'GPS:{msg.latitude:.6f},{msg.longitude:.6f},{msg.altitude:.2f}\n'
            self.ser.write(linha.encode())
        except Exception as e:
            self.get_logger().warning(f'Erro ao enviar GPS: {e}')


# ──────────────────────────────────────────────────────────────────────
def main():
    rclpy.init()
    node = CosmosSerialBridge()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

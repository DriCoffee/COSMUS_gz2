# COSMUS_gz2 — Simulação Gazebo Sim Harmonic + ROS 2 Jazzy

Projeto derivado do [COSMUS Design](https://github.com/FCostaS/COSMUSDesign) (Co-Simulation Multi-UAV for Systems Design).  
O mundo de simulação original foi extraído e convertido do **Gazebo Classic** para o **Gazebo Sim Harmonic 8.11.0**, com integração ao **ROS 2 Jazzy**.

> **Stack de referência:**  
> -  Simulador: [Gazebo Sim Harmonic 8.11.0](https://gazebosim.org/docs/harmonic/)  
> -  Middleware: ROS 2 Jazzy Jalisco  
> -  HIL (Hardware-in-the-Loop): MicroROS para ESP32 compatível com ROS 2 Jazzy  
> -  SIL (Software-in-the-Loop): Python com ROS 2 Jazzy  

***

## Estrutura do Projeto

```
COSMUS_gz2/
├── models/
│   └── plane/
│        ├── model.config
│        ├── plane.sdf
│        ├── plane.sdf.jinja
│        ├── plane00.sdf  ← avião individual (x5: 00~04)
│        └── meshes/
├── worlds/
│   ├── empty.sdf               ← mundo mínimo de teste
│   ├── cosmus_outdoor.sdf      ← terreno com árvores
│   └── cosmus_airfield.sdf     ← aeródromo completo com UAVs
├── config/
│   └── ros_gz_bridge.yaml      ← mapeamento de 40+ tópicos ROS↔Gz
├── scripts/
│   └── cosmus_serial_bridge.py ← bridge MicroROS/ESP32 ↔ ROS 2 (HIL)
└── launch/
    └── cosmus_airfield.launch.py  ← launch ROS 2
```

***

## Pré-requisitos

| Componente | Versão requerida |
|---|---|
| Ubuntu | 24.04 LTS (Noble) |
| ROS 2 | Jazzy Jalisco |
| Gazebo Sim | Harmonic 8.11.0 |
| ros_gz (bridge) | jazzy / harmonic |
| Python | 3.12+ |
| MicroROS (HIL) | micro_ros_agent Jazzy |

***

## Como Rodar

### Opção 1 — Direto pelo terminal (gz sim)

```bash
export GZ_SIM_RESOURCE_PATH=/home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/models
gz sim -v 4 /home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/worlds/cosmus_airfield.sdf
```

### Opção 2 — Via ROS 2 launch

```bash
source /opt/ros/jazzy/setup.bash
export GZ_SIM_RESOURCE_PATH=/home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/models
ros2 launch /home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/launch/cosmus_airfield.launch.py
```

### Opção 3 — Aliases no `~/.bashrc`

Adicione no seu `~/.bashrc`:

```bash
export COSMUS_PATH="$HOME/Projetos/_Mestrado/sim/COSMUS_gz2"
alias cosmus_kill='pkill -f gz-sim-main; pkill -f parameter_bridge; pkill -f gz_sim; sleep 2; echo "Gazebo limpo!"'
alias cosmus_up='source /opt/ros/jazzy/setup.bash && export GZ_SIM_RESOURCE_PATH=$COSMUS_PATH/models && ros2 launch $COSMUS_PATH/launch/cosmus_airfield.launch.py'
```

Recarregue o terminal e execute:

```bash
cosmus_kill && cosmus_up
```

***

## Modelos Disponíveis (herdados do COSMUSDesign)

- `model://ground_plane`
- `model://mcmillan_airfield`
- `model://plane`
- `model://tailsitter`
- `model://techpod`

***

## Como Adicionar Mais Aeronaves

Para colocar mais de uma aeronave na mesma simulação, adicione blocos `<include>` dentro de `worlds/cosmus_airfield.sdf`.

Cada aeronave deve ter:
- Um `<name>` **único**.
- Um `<uri>` apontando para o modelo (usando `file://` com caminho absoluto para SDFs individuais).
- Um `<pose>` diferente para evitar sobreposição.

### Exemplo com múltiplas aeronaves

```xml
<include>
  <name>plane00</name>
  <uri>file:///home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/models/plane/plane00.sdf</uri>
  <pose>0 0 1.0 0 0 0</pose>
</include>

<include>
  <name>plane01</name>
  <uri>file:///home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/models/plane/plane01.sdf</uri>
  <pose>8 0 1.0 0 0 0</pose>
</include>
```

### Regras Importantes

- O `<name>` não pode se repetir entre aeronaves.
- O `<pose>` deve ser único para cada aeronave.
- Usar `file://` com caminho absoluto para SDFs individuais (evita conflito com `model.config`).
- Para manter o projeto independente, copie cada modelo para dentro de `COSMUS_gz2/models/`.
- Os plugins `<topic>` no SDF **não** devem ter `MODEL_NAME` hardcoded — deixe vazio para o Gazebo gerar automaticamente.

### Se uma aeronave não aparecer, verifique:

- Se o nome do modelo no `<uri>` está correto.
- Se o arquivo `.sdf` do modelo existe no caminho especificado.
- Se o modelo não depende de submodelos ou sensores ausentes.
- Se a aeronave não nasceu sobreposta a outra ou abaixo do solo.

### Executando com os modelos locais

```bash
export GZ_SIM_RESOURCE_PATH=/home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/models
gz sim -v 4 /home/$USER/Projetos/_Mestrado/sim/COSMUS_gz2/worlds/cosmus_airfield.sdf
```

***

## SIL — Software-in-the-Loop com Python + ROS 2

Esta seção descreve a simulação do controlador via software, utilizando **Python com ROS 2 Jazzy** para publicar comandos e assinar dados de sensores diretamente nos tópicos do Gazebo.

### Arquitetura SIL

```
[Script Python ROS 2]
        ↕  tópicos ROS 2 (via ros_gz_bridge)
   [Gazebo Sim Harmonic]
        ↕
  /plane00/cmd_throttle  → Gazebo (hélice)
  /plane00/cmd_elevator  → Gazebo (profundor)
  /plane00/cmd_rudder    → Gazebo (leme)
  /plane00/imu           ← Gazebo (IMU)
  /plane00/navsat        ← Gazebo (GPS)
```

### Executando um nó SIL

```bash
source /opt/ros/jazzy/setup.bash
python3 scripts/cosmus_sil_controller.py
```

> A implementação inicial segue os modelos de controle PID dos projetos de Ricardo e Fabrício (citações completas em desenvolvimento).

***

## HIL — Hardware-in-the-Loop com ESP32 via MicroROS

Esta seção descreve como conectar um **ESP32 físico** ao simulador usando **MicroROS** (micro_ros_arduino / micro_ros_agent) compatível com **ROS 2 Jazzy**, permitindo enviar comandos reais de hardware para os UAVs simulados e receber dados de sensores.

### Arquitetura HIL

```
  [ESP32 + Firmware MicroROS]
          ↕  USB Serial / WiFi UDP
  [micro_ros_agent (Jazzy)]
          ↕  tópicos ROS 2 nativos
  [Gazebo Sim Harmonic]

  /plane00/cmd_throttle  →  Gazebo (hélice)
  /plane00/cmd_elevator  →  Gazebo (profundor)
  /plane00/cmd_rudder    →  Gazebo (leme)
  /plane00/imu           ←  Gazebo (acelerômetro + giroscópio)
  /plane00/navsat        ←  Gazebo (GPS)
```

### Instalação do micro_ros_agent (ROS 2 Jazzy)

```bash
# Via snap (recomendado para Jazzy)
sudo snap install micro-ros-agent

# OU via build from source
source /opt/ros/jazzy/setup.bash
mkdir -p ~/microros_ws/src
cd ~/microros_ws/src
git clone -b jazzy https://github.com/micro-ROS/micro_ros_setup.git
cd ~/microros_ws
colcon build
source install/setup.bash
ros2 run micro_ros_setup create_agent_ws.sh
ros2 run micro_ros_setup build_agent.sh
source install/setup.bash
```

### Firmware do ESP32 (MicroROS via Arduino IDE / PlatformIO)

Utilize a biblioteca [micro_ros_arduino](https://github.com/micro-ROS/micro_ros_arduino) compatível com Jazzy:  
https://github.com/micro-ROS/micro_ros_arduino/releases

**Exemplo básico de publisher/subscriber no ESP32:**

```cpp
#include <micro_ros_arduino.h>
#include <rcl/rcl.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>
#include <std_msgs/msg/float32.h>

rcl_publisher_t publisher_imu;
rcl_subscription_t subscriber_throttle;
std_msgs__msg__Float32 throttle_msg;
std_msgs__msg__Float32 imu_msg;

rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;

void subscription_callback(const void * msgin) {
  const std_msgs__msg__Float32 * msg = (const std_msgs__msg__Float32 *)msgin;
  // Aplicar valor de throttle ao ESC/servo
}

void setup() {
  set_microros_transports();  // Serial USB (padrão)
  allocator = rcl_get_default_allocator();
  rclc_support_init(&support, 0, NULL, &allocator);
  rclc_node_init_default(&node, "cosmus_esp32_node", "", &support);

  rclc_publisher_init_default(
    &publisher_imu, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
    "/plane00/imu_raw");

  rclc_subscription_init_default(
    &subscriber_throttle, &node,
    ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Float32),
    "/plane00/cmd_throttle");

  rclc_executor_init(&executor, &support.context, 1, &allocator);
  rclc_executor_add_subscription(&executor, &subscriber_throttle, &throttle_msg, &subscription_callback, ON_NEW_DATA);
}

void loop() {
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(10));
  // Publicar dados IMU do sensor físico
  imu_msg.data = 9.8;  // exemplo
  rcl_publish(&publisher_imu, &imu_msg, NULL);
  delay(10);
}
```

### Rodar o micro_ros_agent (Serial USB)

Com o Gazebo já rodando via `cosmus_up`, em outro terminal:

```bash
source /opt/ros/jazzy/setup.bash

# Verificar porta serial do ESP32
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null

# Iniciar o agent (ajuste a porta conforme necessário)
micro-ros-agent serial --dev /dev/ttyUSB0 -b 115200
# ou
ros2 run micro_ros_agent micro_ros_agent serial --dev /dev/ttyUSB0 -b 115200
```

### Permissão na porta serial

```bash
sudo usermod -aG dialout $USER   # fazer logout/login após este comando
```

### Protocolo de Tópicos ROS 2 (ESP32 ↔ Gazebo)

| Direção | Tópico ROS 2 | Tipo de Mensagem | Descrição |
|---|---|---|---|
| ESP32 → Gz | `/plane00/cmd_throttle` | `std_msgs/Float32` | Controle da hélice |
| ESP32 → Gz | `/plane00/cmd_elevator` | `std_msgs/Float32` | Controle do profundor |
| ESP32 → Gz | `/plane00/cmd_rudder` | `std_msgs/Float32` | Controle do leme |
| Gz → ESP32 | `/plane00/imu` | `sensor_msgs/Imu` | Acelerômetro + giroscópio |
| Gz → ESP32 | `/plane00/navsat` | `sensor_msgs/NavSatFix` | GPS |

### Observações HIL

- O ESP32 atua como **nó ROS 2 nativo** via MicroROS — comunicação direta no middleware sem bridge serial intermediária.
- Para múltiplos aviões, instanciar o firmware com namespaces diferentes (`/plane01`, `/plane02`...).
- Para WiFi UDP em vez de Serial, use `set_microros_wifi_transports("SSID", "PASSWORD", "192.168.1.100", 8888)` no `setup()`.
- O arquivo de bridge auxiliar está disponível em `scripts/cosmus_serial_bridge.py` (compatibilidade legada).

***

## Referências

- [COSMUSDesign — projeto original](https://github.com/FCostaS/COSMUSDesign)
- [Gazebo Sim Harmonic — documentação oficial](https://gazebosim.org/docs/harmonic/)
- [ROS 2 Jazzy Jalisco](https://docs.ros.org/en/jazzy/)
- [micro-ROS para Arduino/ESP32](https://github.com/micro-ROS/micro_ros_arduino)
- [micro_ros_agent](https://github.com/micro-ROS/micro-ROS-Agent)
- [ros_gz bridge (Jazzy)](https://github.com/gazebosim/ros_gz/tree/jazzy)
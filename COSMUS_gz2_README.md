# Projeto de conversão do mundo simulado do COSMUS Design

Projeto original - https://github.com/FCostaS/COSMUSDesign - COSMUS Design (Co-Simulation Multi-UAV for Systems Design).
Sendo extrado o mundo de simulação e convertido do Gazebo Classic para o Gazebo Jetty.

# COSMUS_gz2 — Simulação Gazebo Jetty + ROS 2 Rolling

## Estrutura
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
│   ├── empty.sdf             ← mundo mínimo de teste
│   ├── cosmus_outdoor.sdf    ← terreno com árvores
│   └── cosmus_airfield.sdf   ← aeródromo completo com UAVs
├── config/
│   └── ros_gz_bridge.yaml    ← mapeamento de 40+ tópicos ROS↔Gz
├── scripts/
│   └── cosmus_serial_bridge.py  ← bridge ESP32 ↔ ROS 2
└── launch/
    └── cosmus_airfield.launch.py  ← launch ROS 2
```

## Como rodar

### Opção 1 — direto pelo terminal (gz sim)
```bash
export GZ_SIM_RESOURCE_PATH=/home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/models
gz sim -v 4 /home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/worlds/cosmus_airfield.sdf
```

### Opção 2 — via ROS 2 launch

```bash
source /opt/ros/rolling/setup.bash
export GZ_SIM_RESOURCE_PATH=//home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/models
ros2 launch /home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/launch/cosmus_airfield.launch.py
```

### Opção 3 — aliases no ~/.bashrc

Adicione este alias no seu `~/.bashrc`:

```bash
alias cosmus_kill='pkill -f gz-sim-main; pkill -f parameter_bridge; pkill -f gz_sim; sleep 2; echo "Gazebo limpo!"'
alias cosmus_up='source /opt/ros/rolling/setup.bash && ros2 launch /home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/launch/cosmus_airfield.launch.py'
```

Feche e abra o terminal, e chame os comandos:
```bash
cosmus_kill && cosmus_up
```

## Modelos disponíveis no COSMUSDesign
- model://ground_plane
- model://mcmillan_airfield
- model://plane
- model://tailsitter
- model://techpod

## Como adicionar mais aeronaves

Para colocar mais de uma aeronave na mesma simulação, basta adicionar novos blocos `<include>` dentro do arquivo `worlds/cosmus_airfield.sdf`.

Cada aeronave deve ter:
- Um `<name>` único.
- Um `<uri>` apontando para o modelo (usando `file://` para SDFs individuais).
- Um `<pose>` diferente para não nascer sobreposta a outra.

### Exemplo com múltiplas aeronaves

```xml
<include>
  <name>plane00</name>
  <uri>file:///home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/models/plane/plane00.sdf</uri>
  <pose>0 0 1.0 0 0 0</pose>
</include>

<include>
  <name>plane01</name>
  <uri>file:///home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/models/plane/plane01.sdf</uri>
  <pose>8 0 1.0 0 0 0</pose>
</include>
```

### Regras importantes

- O valor de `<name>` não pode se repetir.
- O valor de `<pose>` deve mudar para cada aeronave.
- Usar `file://` com caminho absoluto para SDFs individuais (evita conflito com `model.config`).
- Se o modelo tiver dependências próprias, ele precisa estar completo dentro de `COSMUS_gz2/models/`.
- Para manter o projeto independente, copie cada modelo para a pasta local do projeto.

### Executando com os modelos locais

Depois de copiar os modelos para `COSMUS_gz2/models`, execute a simulação com:

```bash
export GZ_SIM_RESOURCE_PATH=/home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/models
gz sim -v 4 /home/drik/Projetos/_Mestrado/sim/COSMUS_gz2/worlds/cosmus_airfield.sdf
```

### Observação

Se uma aeronave não aparecer, verifique:
- Se o nome do modelo no `<uri>` está correto.
- Se o arquivo `.sdf` do modelo existe.
- Se o modelo não depende de sensores ou submodelos ausentes.
- Se a aeronave não nasceu em cima de outra ou abaixo do solo.
- Se os plugins `<topic>` no SDF **não** têm `MODEL_NAME` hardcoded (deve estar vazio — o Gazebo gera automaticamente).

---


## SIL — Software-in-the-Loop com python

Esta seção descreve a simulação básica do controlador simples - inicialmente do modelo PDI seguindo modelos de controle dos projetos dos alunos Ricardo e Fabrício. Citações completas mais a frente.


---

## HIL — Hardware-in-the-Loop com ESP32 via Serial USB

Esta seção descreve como conectar um **ESP32 físico** ao simulador via USB Serial, permitindo enviar comandos reais de hardware para os UAVs simulados e receber dados de sensores no terminal.

### Arquitetura

```
[Arduino IDE Serial Monitor]
        ↕  USB Serial (115200 baud)
     [ESP32]
        ↕  /dev/ttyUSB0 ou /dev/ttyACM0
  [cosmus_serial_bridge.py]  ← nó ROS 2
        ↕  tópicos ROS 2
  /plane00/cmd_throttle  →  Gazebo (hélice)
  /plane00/cmd_elevator  →  Gazebo (profundor)
  /plane00/cmd_rudder    →  Gazebo (leme)
  /plane00/imu           ←  Gazebo (acelerômetro + giroscópio)
  /plane00/navsat        ←  Gazebo (GPS)
```

### Protocolo Serial (ESP32 ↔ ROS 2)

| Direção | Formato | Exemplo | Ação |
|---|---|---|---|
| IDE → ROS | `T:<valor>` | `T:500` | Publica throttle no `/plane00/cmd_throttle` |
| IDE → ROS | `E:<valor>` | `E:0.3` | Publica elevator no `/plane00/cmd_elevator` |
| IDE → ROS | `R:<valor>` | `R:0.2` | Publica rudder no `/plane00/cmd_rudder` |
| ROS → IDE | `IMU:ax,ay,az,wx,wy,wz` | `IMU:0.001,-0.011,9.800,...` | Dados do IMU do Gazebo |
| ROS → IDE | `GPS:lat,lon,alt` | `GPS:-22.12,-47.65,820.00` | Dados GPS do Gazebo |

### Código do ESP32 (Arduino IDE)

```cpp
#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  Serial.println("COSMUS_ESP32_READY");
}

void loop() {
  // Receber comando do Serial Monitor e repassar ao ROS
  if (Serial.available()) {
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    Serial.print("CMD_RECEIVED:");
    Serial.println(cmd);
  }
}
```

### Instalação das dependências ROS

```bash
pip3 install pyserial
sudo usermod -aG dialout $USER   # permissão na porta serial
# fazer logout/login após esse comando
```

### Verificar porta serial do ESP32

```bash
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null
```

Editar o arquivo `scripts/cosmus_serial_bridge.py` e ajustar a variável:
```python
SERIAL_PORT = '/dev/ttyUSB0'   # ou /dev/ttyACM0
```

### Rodar o bridge HIL

Com o Gazebo já em execução via `cosmus_up`, em outro terminal:

```bash
source /opt/ros/rolling/setup.bash
python3 ~/Projetos/_COSMUS/COSMUS_gz2/scripts/cosmus_serial_bridge.py
```

### Testar pelo Serial Monitor (baud 115200)

Digite no Serial Monitor do Arduino IDE:

```
T:500
```
→ Hélice do `plane00` gira no Gazebo

```
T:0
```
→ Para a hélice

```
E:0.3
```
→ Move o elevator

O Serial Monitor imprimirá em tempo real os dados do simulador:
```
IMU:0.001,-0.011,9.800,0.0004,0.0004,-0.00004
GPS:-22.123456,-47.654321,820.00
```

### Observações HIL

- O ESP32 age como **interface física** — qualquer microcontrolador com Serial USB funciona (Arduino Uno, Mega, STM32, etc.).
- Para múltiplos aviões, criar instâncias do bridge com parâmetro de namespace (`/plane01`, `/plane02`...).
- Para latência menor, reduzir o rate dos subscribers de IMU/GPS no código Python (`create_subscription` com `QoSProfile` adequado).
- O arquivo completo do bridge está em `scripts/cosmus_serial_bridge.py`.

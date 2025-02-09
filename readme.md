# Proyecto: Máquina de Café Automatizada

Este repositorio contiene los archivos necesarios para replicar el prototipo de una máquina de café automatizada basada en Raspberry Pi. 
Desarrollado como proyecto final del curso de Prototipado de Sistemas Embebidos, del Técnico Básico en Desarrollo de Sistemas Embebidos de la universidad Fidélitas. 
Incluye la integración de múltiples componentes electrónicos, la optimización del uso de GPIO mediante integrados como el 74HC595 y el diseño de una interfaz gráfica funcional y amigable.

## Tabla de Contenidos
- [Requisitos de Hardware](#requisitos-de-hardware)
- [Requisitos de Software](#requisitos-de-software)
- [Estructura del Repositorio](#estructura-del-repositorio)
- [Configuración de Raspberry Pi](#Configuración-de-Raspberry-Pi)
- [Instalación de Software en Raspberry Pi](#Instalación-de-Software-en-Raspberry-Pi)
- [Documentación Específica](#documentación-específica)

---

## Requisitos de Hardware

1. **Raspberry Pi 4/5** con GPIO habilitado.
2. Componentes electrónicos:
    - 4 botones (Arriba, Abajo, Seleccionar, Iniciar)
    - 2 LEDs (proceso de pago, temperatura del agua)
    - Sensor de proximidad (HC-SR04)
    - Display 7 segmentos (controlado con 74HC595)
    - Barra LED (controlada con 74HC595)
    - Servo (para simular colocación del vaso)
    - LCD I2C (16x2)
    - Buzzer pasivo
3. Fuente de alimentación adecuada para la Raspberry Pi.
4. Protoboard y cables de conexión.

---

## Requisitos de Software

1. **Sistema Operativo:** Raspberry Pi OS (32/64 bits).
2. Librerías necesarias:
    - `gpiozero`
    - `tkinter`
    - `smbus2`
    - `Freenove_DHT`
3. **Fritzing** para visualizar el diagrama del circuito.
4. **Python 3.7** o superior.
5. **Configuraciones adicionales:**
    - Habilitar el protocolo I2C utilizando `sudo raspi-config`.
    - Instalar las herramientas I2C con `sudo apt-get install i2c-tools`.
    - Instalar el módulo SMBus con `sudo apt-get install python3-smbus`. 
6. Código base de Freenove para el manejo de DHT11 y LCD1602.

---

## Estructura del Repositorio

```plaintext
├── README.md                   # Descripción general del proyecto.
├── Circuito/
│   ├── Diagrama.fzz            # Archivo Fritzing del circuito.
│   └── README.md               # Explicación del circuito.
├── Software/
│   ├── CafeTechGUI.py          # Interfaz gráfica en Tkinter.
│   ├── CafeTechBL.py           # Lógica y control de componentes.
│   ├── CafeTechRecetas.py      # Recetas de bebidas en formato JSON.
│   ├── LCD1602.py              # Módulo para el manejo de la pantalla LCD I2C.
│   ├── DHT11/                  # Carpeta para manejar el sensor DHT11.
│      ├── WiringPi/            # Carpeta con dependencias de WiringPi.
│      ├── libdht.so            # Biblioteca compartida para el sensor DHT11.
│      ├── setup.py             # Script de configuración de la biblioteca del DHT11.
│      ├── DHT.h                # Archivo de cabecera para el sensor.
│      ├── DHT.c                # Implementación en C para el manejo del sensor.
│      └── DHT.o                # Archivo objeto compilado del sensor.
└── 
```

--- 

## Configuración de Raspberry Pi

1. **Preparar el sistema operativo de Raspberry Pi**:
   - Instalar Raspberry Pi OS en una tarjeta microSD y configurarlo en tu Raspberry Pi.
   - Actualizar los paquetes del sistema:
     ```bash
     sudo apt-get update
     sudo apt-get upgrade
     ```

2. **Habilitar el protocolo I2C**:
   - Ejecutar:
     ```bash
     sudo raspi-config
     ```
   - Seleccionar:
     ```
     3 Interfacing Options > I5 I2C > Yes
     ```
   - Reiniciar la Raspberry Pi después de habilitar el protocolo I2C.

3. **Instalar las librerías necesarias**:
   ```bash
   sudo apt-get install python3-gpiozero python3-smbus i2c-tools
   ```
   
4. **Verificar la conexión de la Raspberry Pi**:
   - Ejecutar el siguiente comando para encontrar la IP del dispositivo:
     ```bash
     hostname -I
     ```  
   - Conectar por SSH:
     ```bash
     ssh <usuario>@<IP_de_la_Raspberry>
     ```

## Instalación de Software en Raspberry Pi

1. **Clonar este repositorio:**:
     ```bash
     git clone https://github.com/JoseMoyaCR/CafeTechMachine.git
	 cd CafeTechMachine
     ```

2. **Configurar un entorno virtual (opcional):**:
   - Crear y activar un entorno virtual:
     ```bash
     python -m venv .cafetechmachine
	 source .cafetechmachine/bin/activate
     ```
   - Instalar las dependencias del proyecto:
     ```
     pip install -r Software/requirements.txt
     ```

3. **Ejecución del programa**:
   - Ejecutar el archivo principal:
     ```
     python3 Software/CafeTechGUI.py
     ```
---

## Documentación Específica

- [Circuito](Circuito/README.md): Explicación del diagrama y componentes.
- [Software](Software/README.md): Descripción del código, funciones y bibliotecas usadas.
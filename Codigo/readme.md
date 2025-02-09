# Software del Proyecto: Máquina de Café Automatizada

Este documento detalla el diseño, desarrollo y configuración del software que controla el prototipo de la Máquina de Café Automatizada. El software está diseñado para gestionar eficientemente los componentes del circuito, garantizar la funcionalidad requerida y mejorar la experiencia del usuario.

## Descripción General del Software

El software de la máquina de café se estructuró en tres scripts principales, siguiendo buenas prácticas de modularidad y separación de responsabilidades:

1. **Interfaz gráfica (`CafeTechGUI.py`):** Desarrollada en Tkinter, permite al usuario interactuar con la máquina de café a través de botones físicos y muestra información en tiempo real.
2. **Lógica y control de componentes (`CafeTechBL.py`):** Gestiona las operaciones internas, como la preparación de bebidas, validación de pagos y manejo de sensores.
3. **Recetas de bebidas (`CafeTechRecetas.py`):** Contiene las recetas en formato JSON dentro de un archivo .py, lo que facilita su importación y uso en el proyecto.

Este diseño se inspiró en proyectos previos del curso, como la [máquina de café del profesor Randy Céspedes](https://github.com/rscd27p/Maquina_de_Cafe/), y en los ejemplos de FreeNove, adaptando las funcionalidades para las necesidades específicas del prototipo.

---

## Funcionalidades Principales

### Preparación de Bebidas
- Verifica el stock de ingredientes antes de iniciar el proceso.
- Controla el calentamiento del agua, utilizando un **timeout** para garantizar que se alcance la temperatura necesaria.
- Realiza tres lecturas iniciales del sensor DHT11 para estabilizar los valores y evitar lecturas residuales.
- Ejecuta en paralelo la cuenta regresiva en el display de 7 segmentos, la simulación del vaso con el servo motor, y la actualización de la barra de progreso (tanto en la interfaz gráfica como en la barra LED).
- Emite sonidos con el buzzer para asociar eventos específicos a sonidos.

### Verificación del Pago
- Implementa una lógica de banderas para evitar que el proceso de validación se ejecute simultáneamente en múltiples hilos.
- Utiliza el sensor de proximidad HC-SR04 para simular el pago con tarjeta, manejando lecturas en un hilo separado para evitar bloqueos en el hilo principal de la interfaz.

### Gestión de Ingredientes
- Realiza verificaciones del stock antes de iniciar la preparación de bebidas.
- Actualiza automáticamente las cantidades de ingredientes después de cada preparación.

### Interfaz Gráfica
- Desarrollada con **Tkinter**, simula el panel de usuario de la máquina.
- Permite la navegación entre opciones y tamaños de bebidas utilizando botones físicos.
- Muestra mensajes informativos y de error en cuadros de diálogo que se cierran automáticamente después de 3 segundos.

---

## Retos Encontrados

1. **Calibración del Sensor de Proximidad:**
   - Las lecturas del HC-SR04 se vieron afectadas por factores externos, como la reflexión de las ondas en diferentes superficies.
   - Ajustes en los tiempos de espera y lecturas consecutivas ayudaron a mejorar la estabilidad, pero el problema persiste parcialmente debido a limitaciones del hardware.

2. **Lectura del Sensor de Temperatura:**
   - El DHT11 mostró lentitud en las lecturas y residuos de valores anteriores en memoria.
   - Se implementó un ciclo de espera con **timeout** y lecturas iniciales para estabilizar los valores y garantizar precisión.

3. **Interferencia en los Pines GPIO:**
   - Falsos positivos en los botones físicos se resolvieron implementando resistencias pull-down y pausas temporales para evitar activaciones múltiples.

4. **PWM Residual en el Buzzer:**
   - Se observó un "chillido" causado por señales residuales después de la reproducción de tonos.
   - Esto se resolvió reiniciando el pin GPIO tras cada uso.

5. **Limitación del Servo Motor:**
   - Su rango de rotación de 180 grados requirió ajustes específicos para simular correctamente el movimiento del vaso.
   
6. **Bloqueo de lecturas por el hilo principal:**
   - La lectura de sensores, como el HC-SR04 y el DHT11, fue bloqueada por el hilo principal de la interfaz gráfica debido a las limitaciones del Global Interpreter Lock (GIL) de Python, que impide la ejecución paralela real. Este problema se resolvió mediante la creación de hilos independientes para las operaciones de lectura y el uso de callbacks asincrónicos para actualizar los componentes de la interfaz gráfica, asegurando un flujo fluido y evitando conflictos entre los hilos.

---

## Ejemplos de FreeNove

El desarrollo del software se basó en ejemplos del kit FreeNove, que proporcionaron la base técnica para implementar los componentes:

- **[Project 20.1 I2C LCD1602](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_GPIOZero_Code/20.1.1_I2CLCD1602):** Para la pantalla LCD.
- **[Project 21.1 Hygrothermograph](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_GPIOZero_Code/21.1.1_DHT11):** Para la lectura del sensor DHT11.
- **[Project 18.1 7-Segment Display](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_GPIOZero_Code/18.1.1_SevenSegmentDisplay):** Para el control del display de 7 segmentos.
- **[Project 6.1 Doorbell](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_GPIOZero_Code/06.1.1_Doorbell):** Para la integración del buzzer.
- **[Project 17.1 Flowing Water Light](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_GPIOZero_Code/17.1.1_LightWater02):** Para el manejo de la barra LED.
- **[Project 15.1 Servo Sweep](https://github.com/Freenove/Freenove_Ultimate_Starter_Kit_for_Raspberry_Pi/tree/master/Code/Python_GPIOZero_Code/15.1.1_Sweep):** Para el control del servo motor.


En los casos del sensor DHT11 y la pantalla LCD, se realizaron configuraciones adicionales basadas en los scripts proporcionados por FreeNove, como `DHT.h`, `DHT.c`, `setup.py` y `LCD1602.py`.

## Configuración del Sensor DHT11

El sensor DHT11 mide la temperatura y la humedad, pero requiere de configuraciones específicas para funcionar correctamente en Raspberry Pi. Sigue estos pasos:

1. **Navegar al directorio del sensor:**
   ```bash
   cd ~/Documents/CafeTechMachine/Codigo/DHT11
   ```

2. **Compilar los archivos del sensor:** Utiliza el script setup.py para configurar las bibliotecas necesarias:
   ```bash
   sudo python setup.py
   ```

## Configuración del LCD1602 I2C

En caso de que no se haya habilitado el protocolo I2C se debe de seguir los siguientes pasos:

1. **Habilitar el protocolo I2C**:
   - Ejecutar:
     ```bash
     sudo raspi-config
     ```
   - Seleccionar:
     ```
     3 Interfacing Options > I5 I2C > Yes
     ```
   - Reiniciar la Raspberry Pi después de habilitar el protocolo I2C.

2. **Instalar las librerías necesarias**:
   ```bash
   sudo apt-get install python3-smbus i2c-tools
   ```

---

## Archivos del Software

```plaintext
├── CafeTechGUI.py          # Interfaz gráfica en Tkinter.
├── CafeTechBL.py           # Lógica y control de componentes.
├── CafeTechRecetas.py      # Recetas de bebidas en formato JSON.
├── LCD1602.py              # Módulo para el manejo de la pantalla LCD I2C.
├── DHT11/                  # Carpeta para manejar el sensor DHT11.
│   ├── WiringPi/           # Carpeta con dependencias de WiringPi.
│   ├── libdht.so           # Biblioteca compartida para el sensor DHT11.
│   ├── setup.py            # Script de configuración de la biblioteca del DHT11.
│   ├── DHT.h               # Archivo de cabecera para el sensor.
│   ├── DHT.c               # Implementación en C para el manejo del sensor.
│   └── DHT.o               # Archivo objeto compilado del sensor.
└──
```

---

## Ejecución del software

1. **Configurar el entorno virtual (opcional)**:
     ```bash
     python -m venv .cafetechmachine
	 source .cafetechmachine/bin/activate
     ```

2. **Ejecutar el programa principal**:
   ```bash
   python CafeTechGUI.py
   ```

# Circuito del Proyecto: Máquina de Café Automatizada

Este documento detalla el diseño y configuración del circuito implementado para el prototipo de la Máquina de Café Automatizada. El circuito está diseñado para optimizar el uso de los recursos de hardware, mejorar la experiencia del usuario y cumplir con los requisitos funcionales del proyecto.

## Descripción General del Circuito

El circuito utiliza una **Raspberry Pi 5** como controlador principal, integrando una serie de componentes electrónicos para replicar las funcionalidades de una máquina de café automatizada. Entre los componentes principales destacan:

- **Botones físicos:** Controlan las opciones de selección y el inicio del proceso.
- **LEDs:** Indican el estado del proceso de pago y la temperatura del agua.
- **Display de 7 segmentos:** Muestra una cuenta regresiva para la preparación de la bebida.
- **Barra LED:** Proporciona una retroalimentación visual del progreso del proceso.
- **Servo motor:** Simula la colocación y devolución del vaso.
- **Pantalla LCD I2C:** Muestra información como el estado del sistema y las selecciones del usuario.
- **Buzzer:** Emite señales audibles durante el proceso.

El uso de los integrados **74HC595** para manejar el display de 7 segmentos y la barra LED permite reducir significativamente la cantidad de pines GPIO necesarios, optimizando el diseño del hardware.

## Componentes Utilizados

1. **Raspberry Pi 5**
2. **Botones:** 4 unidades (Arriba, Abajo, Seleccionar e Iniciar).
3. **LEDs:** 2 unidades (Indicadores de proceso y temperatura).
4. **Sensor de proximidad HC-SR04:** Para detectar el pago con tarjeta.
5. **Display de 7 segmentos (común anodo):** Controlado con un integrado 74HC595.
6. **Barra LED:** Controlada con otro integrado 74HC595.
7. **Servo motor:** Para simular el manejo del vaso.
8. **Pantalla LCD I2C (16x2):** Para mostrar información al usuario.
9. **Buzzer:** Para emitir sonidos durante los procesos.
10. **Protoboard, resistencias y cables de conexión.**

## Implementación del Circuito

### Uso del 74HC595

El integrado **74HC595** se utilizó para controlar tanto el display de 7 segmentos como la barra LED, reduciendo los pines GPIO requeridos a solo 3 por componente (datos, reloj y latch). Esto fue inspirado en los tutoriales de FreeNove "Project 17.1 Flowing Water Light" y "Project 18.1 7-Segment Display". Este enfoque permite manejar múltiples salidas digitales con una configuración eficiente.

### Pantalla LCD I2C

La pantalla LCD I2C facilita la comunicación utilizando solo dos pines GPIO (SDA y SCL). Esta pantalla muestra información en tiempo real sobre el estado del sistema y las selecciones de bebidas. La implementación se basó en el tutorial "Project 20.1 I2C LCD1602" de FreeNove.

### Sensor de Proximidad HC-SR04

El sensor de proximidad se utilizó para simular el proceso de pago mediante la detección de objetos. Sin embargo, se encontraron retos como lecturas inconsistentes debido a la reflexión de las ondas ultrasónicas en diferentes superficies. Para este problema se ajustaron los tiempos de espera y haciendo varias lecturas para "calibrar" el sensor.

### Buzzer

El **buzzer** se empleó para mejorar la experiencia del usuario al asociar eventos específicos a sonidos personalizados, generados mediante señales PWM. Esto incluyó configuraciones avanzadas a nivel de código para evitar ruidos no deseados y asegurar una retroalimentación sonora clara.

### Barra LED

La **barra LED** ofrece una visualización del progreso del proceso de preparación de las bebidas. Su control a través del integrado 74HC595 optimiza el uso de pines GPIO, garantizando un funcionamiento eficiente y atractivo visualmente.

### Servo Motor

El **servo motor** permitió la simulación del movimiento necesario para la colocación y devolución del vaso. Este componente requiere una programación precisa para manejar su rango limitado de rotación de 180 grados, asegurando su integración adecuada con el sistema.

## Conexiones Principales

| Componente           | GPIO Raspberry Pi |
|----------------------|-------------------|
| Botón Arriba         | GPIO 16          |
| Botón Abajo          | GPIO 12          |
| Botón Seleccionar    | GPIO 20          |
| Botón Iniciar        | GPIO 21          |
| LED Pago             | GPIO 26          |
| LED Temperatura      | GPIO 19          |
| Sensor Proximidad    | GPIO 23, 24      |
| Sensor Temperatura   | GPIO 4           |
| 7 Segmentos          | GPIO 17, 27, 22 (74HC595)|
| Barra LED            | GPIO 5, 6, 23 (74HC595)|
| Servo                | GPIO 18          |
| LCD I2C              | SDA: GPIO 2, SCL: GPIO 3 |
| Buzzer               | GPIO 25          |

## Retos Encontrados

1. **Configuración de los GPIO:** Fue necesario implementar resistencias pull-down en los botones para evitar falsos positivos.
2. **Calibración del sensor HC-SR04:** La reflexión de las ondas ultrasónicas varió dependiendo del entorno, lo que dificultó lecturas consistentes.
3. **Señales PWM residuales en el buzzer:** Generaron sonidos no deseados, lo que se resolvió ajustando las frecuencias y "cerrando" el pin GPIO cada vez que se emite un sonido.
4. **Rango limitado del servo motor:** Su rotación de 180 grados requirió una programación precisa para simular el movimiento necesario.
5. **Interferencia entre componentes:** El manejo simultáneo de múltiples periféricos demandó una gestión eficiente de los recursos de hardware a nivel de los pines GPIO.

## Inspiración y Recursos de FreeNove

El diseño y configuración del circuito se basaron en los siguientes proyectos del kit FreeNove:

- **Project 2.1:** Push Button Switch & LED
- **Project 6.1:** Doorbell (buzzer)
- **Project 15.1:** Servo Sweep
- **Project 17.1:** Flowing Water Light
- **Project 18.1:** 7-Segment Display
- **Project 20.1:** I2C LCD1602
- **Project 21.1:** Hygrothermograph (DHT11)
- **Project 24.1:** Ultrasonic Ranging

Estos proyectos proporcionaron las bases técnicas para implementar y optimizar cada componente en el circuito de la máquina de café automatizada.

## Diagrama del Circuito

El diagrama del circuito está disponible en el archivo [Diagrama.fzz](./Diagrama.fzz) y puede visualizarse utilizando el software Fritzing.

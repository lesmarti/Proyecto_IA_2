# Contador de Dedos con Arduino y Python

Este proyecto permite detectar cuántos y cuáles dedos de una mano están levantados usando la cámara y la biblioteca MediaPipe en Python, y enciende LEDs conectados a un Arduino según los dedos detectados.


## Link del Video
https://drive.google.com/file/d/1_YrqCm5LSSheengVTgogfnMX4aZnc0yH/view?usp=sharing


## Descripción General

El proyecto se compone de dos partes principales:

- **contadordedos.py**: Un script en Python que captura video en tiempo real, detecta los dedos levantados usando la biblioteca MediaPipe, y envía la información sobre los dedos levantados a un Arduino a través de la comunicación serial.
- **contadordedos.ino**: Un programa para el Arduino que recibe los datos de los dedos levantados y enciende los LEDs correspondientes, con un LED por cada dedo.

Ambos componentes trabajan en conjunto para permitir la interacción con los dedos a través de un sistema visual y de hardware.

---

## 1. contadordedos.py

Este archivo en Python se encarga de las siguientes tareas:

- **Captura de video**: Utiliza la cámara del dispositivo para obtener un flujo de video en tiempo real.
- **Detección de manos y dedos**: A través de MediaPipe, se detecta la posición de los dedos y las manos, y se calcula cuáles dedos están levantados.
- **Comunicación serial con Arduino**: Después de detectar los dedos levantados, el script envía esta información al Arduino a través de la comunicación serial. Por ejemplo, si el pulgar y el índice están levantados, el código enviará el número "12", lo que significa que esos dos dedos están levantados.

### Funcionamiento

1. MediaPipe analiza cada fotograma del video y calcula la posición de las articulaciones de los dedos.
2. Si un dedo está levantado, el sistema envía el número correspondiente (del 1 al 5, donde 1 es el pulgar y 5 es el meñique) al Arduino.
3. La información se transmite como una cadena de números (por ejemplo, "12" para pulgar e índice levantados).

### Requisitos de Python

Para ejecutar este archivo, necesitarás instalar las siguientes dependencias:

```bash
pip install opencv-python mediapipe pyserial
```

---

## 2. contadordedos.ino

### Descripción

Este archivo contiene el código que se ejecuta en el Arduino para controlar LEDs en función de los datos recibidos desde un script Python. Cada LED representa un dedo de la mano, y el código enciende los LEDs correspondientes según los dedos levantados detectados por la cámara.

### Funcionamiento

#### Configuración inicial

- Se define un arreglo `leds[]` que contiene los pines del Arduino (del 8 al 12) donde están conectados los LEDs.
- Cada LED corresponde a un dedo de la mano:
    - **Pin 8**: Pulgar
    - **Pin 9**: Índice
    - **Pin 10**: Medio
    - **Pin 11**: Anular
    - **Pin 12**: Meñique
- En la función `setup()`, los pines se configuran como salidas utilizando `pinMode(leds[i], OUTPUT);`.

#### Recepción de datos desde Python

- El Arduino utiliza `Serial.readStringUntil('\n')` para leer una cadena de datos enviada desde el script Python.
- La cadena indica qué dedos están levantados. Por ejemplo:
    - `"12"` significa que los dedos pulgar e índice están levantados.

#### Control de LEDs

- Antes de encender cualquier LED, el programa apaga todos los LEDs para evitar que queden encendidos de ejecuciones anteriores.
- Luego, recorre cada número en la cadena recibida y enciende el LED correspondiente utilizando `digitalWrite(leds[ledIndex], HIGH);`.

#### Lógica del código

- Cada número en la cadena recibida se convierte en un índice que se utiliza para encender el LED correspondiente al dedo levantado.
- Esto permite que el Arduino controle los LEDs en tiempo real según los datos enviados por el script Python.

---

### Resumen de Pines y Dedos

| **Pin** | **Dedo**    |
|---------|-------------|
| 8       | Pulgar      |
| 9       | Índice      |
| 10      | Medio       |
| 11      | Anular      |
| 12      | Meñique     |

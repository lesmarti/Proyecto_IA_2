import cv2
import mediapipe as mp
import serial
import time

# Conexión con Arduino
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

# Configurar MediaPipe para detectar manos
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Verifica si un dedo (excepto pulgar) está levantado
def dedo_levantado(landmarks, tip, pip, eje='y', threshold=0.03):
    if eje == 'y':
        return landmarks[tip].y < landmarks[pip].y - threshold
    elif eje == 'x':
        return landmarks[tip].x > landmarks[pip].x + threshold
    return False

# Verifica si el pulgar está estirado hacia el lado
def pulgar_levantado_horizontal(landmarks, threshold=0.04):
    return landmarks[4].x > landmarks[2].x + threshold

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            dedos = []

            # Pulgar
            dedos.append(pulgar_levantado_horizontal(hand_landmarks.landmark))
            # Otros dedos
            dedos.append(dedo_levantado(hand_landmarks.landmark, 8, 6))   # Índice
            dedos.append(dedo_levantado(hand_landmarks.landmark, 12, 10)) # Medio
            dedos.append(dedo_levantado(hand_landmarks.landmark, 16, 14)) # Anular
            dedos.append(dedo_levantado(hand_landmarks.landmark, 20, 18)) # Meñique

            # Crear mensaje con los dedos levantados
            mensaje = ''.join([str(i + 1) for i, d in enumerate(dedos) if d])
            if mensaje == '':
                mensaje = '0'

            # Enviar a Arduino
            arduino.write((mensaje + '\n').encode())
            time.sleep(0.05)

    # Mostrar la cámara
    cv2.imshow("Seguimiento", frame)

    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

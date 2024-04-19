import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import filedialog

# Función para seleccionar el archivo de video
def select_video_file():
    file_path = filedialog.askopenfilename()
    return file_path

# Inicializar el módulo de MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Crear ventana de Tkinter
root = tk.Tk()
root.withdraw()  # Ocultar la ventana principal de Tkinter

# Solicitar al usuario que seleccione un archivo de video
video_file_path = select_video_file()

# Inicializar la captura de video desde el archivo seleccionado
cap = cv2.VideoCapture(video_file_path)

# Crear la ventana de OpenCV
cv2.namedWindow('Reconocimiento de Personas', cv2.WINDOW_NORMAL)

# Definir la variable para el tiempo actual del video
current_time = 0

while cap.isOpened():
    # Leer el frame del video
    ret, frame = cap.read()
    if not ret:
        break

    # Convertir el frame a color
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detectar las poses en el frame
    results = pose.process(rgb_frame)

    # Contar el número de personas en escena basado en la detección de cabezas
    person_count = 0
    if results.pose_landmarks is not None:
        for landmark in results.pose_landmarks.landmark:
            # Verificar si el landmark está cerca de la parte superior de la pose
            if landmark.visibility > 0.5 and landmark.y < 0.2:
                person_count += 1

    # Mostrar el número de personas en escena
    cv2.putText(frame, f'Personas: {person_count}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Mostrar el frame
    cv2.imshow('Reconocimiento de Personas', frame)

    # Esperar 1 milisegundo y verificar si se ha presionado la tecla 'q' para salir
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break
    elif key == ord('b'):  # Retroceder el video en 5 segundos al presionar la tecla 'b'
        current_time = max(0, current_time - 5000)  # Retroceder 5000 milisegundos (5 segundos)
        cap.set(cv2.CAP_PROP_POS_MSEC, current_time)  # Establecer la posición del video al tiempo actual

# Liberar la captura y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

import cv2

# Inicia la captura de video desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Lee un fotograma de la cámara
    if not ret:
        print("Error: No se pudo capturar el video.")
        break

    # Convierte el fotograma a escala de grises y aplica Canny
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 10, 150)
    canny = cv2.dilate(canny, None, iterations=1)
    canny = cv2.erode(canny, None, iterations=1)

    cnts, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Muestra el frame en tiempo real
    cv2.imshow('Presiona "Espacio" para detectar', frame)

    # Espera una tecla
    key = cv2.waitKey(1) & 0xFF

    if key == ord(' '):  # Detecta la siguiente figura al presionar la barra espaciadora
        for c in cnts[:1]:  # Detecta solo el primer contorno
            epsilon = 0.01 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, epsilon, True)
            x, y, w, h = cv2.boundingRect(approx)

            if len(approx) == 3:
                cv2.putText(frame, 'Triangulo', (x, y - 5), 1, 1, (0, 255, 0), 1)
            elif len(approx) == 4:
                aspect_ratio = float(w) / h
                if aspect_ratio == 1:
                    cv2.putText(frame, 'Cuadrado', (x, y - 5), 1, 1, (0, 255, 0), 1)
                else:
                    cv2.putText(frame, 'Rectangulo', (x, y - 5), 1, 1, (0, 255, 0), 1)
            elif len(approx) == 5:
                cv2.putText(frame, 'Pentagono', (x, y - 5), 1, 1, (0, 255, 0), 1)
            elif len(approx) == 6:
                cv2.putText(frame, 'Hexagono', (x, y - 5), 1, 1, (0, 255, 0), 1)
            elif len(approx) == 10:
                cv2.putText(frame, 'Circulo', (x, y - 5), 1, 1, (0, 255, 0), 1)

            cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)

        # Muestra el frame con las detecciones
        cv2.imshow('Deteccion', frame)

    if key == ord('q'):  # Termina el programa al presionar "q"
        break

cap.release()
cv2.destroyAllWindows()

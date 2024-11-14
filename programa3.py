import cv2

captura = cv2.VideoCaptura(0)
ret, frame = captura.read()

if ret:
    cv2.imwrite('captura.jpg', frame)
    
captura.relase()
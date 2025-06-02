import numpy as np
import cv2 as cv
import math 

# Ruta corregida con r'' para evitar secuencias de escape
rostro = cv.CascadeClassifier(r'C:\Users\Brandon\Desktop\ITM\IA\Ejercicio_Eigenfaces\haarcascade_frontalface_alt.xml')
cap = cv.VideoCapture(0)
i = 0  

while True:
    ret, frame = cap.read()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    rostros = rostro.detectMultiScale(gray, 1.3, 5)
    
    for (x, y, w, h) in rostros:
        frame2 = frame[y:y+h, x:x+w]
        frame2 = cv.resize(frame2, (100, 100), interpolation=cv.INTER_AREA)  # Escalar a 100x100

        if i % 5 == 0:
            # Ruta corregida para guardar imágenes
            cv.imwrite(r'C:\Users\Brandon\Desktop\ITM\IA\Ejercicio_Eigenfaces\Brandon\Brandon' + str(i) + '.jpg', frame2)
            cv.imshow('Rostro detectado', frame2)

    cv.imshow('Detección de rostros', frame)
    i += 1
    k = cv.waitKey(1)
    if k == 27:  # Presionar ESC para salir
        break

cap.release()
cv.destroyAllWindows()

import cv2 
import numpy as np



img = cv2.imread("C:\\Users\\Brandon\\Downloads\\images.jpeg")
imgn = np.zeros(img.shape[:2], np.uint8)
cv2.imshow('salida Original',img)
# cv2.imshow('salidaNuevo',imgn)
b,g,r = cv2.split(img)

imgb = cv2.merge([b,imgn,imgn])
imgg = cv2.merge([imgn,g,imgn])
imgr = cv2.merge([imgn,imgn,r])

cv2.imshow('salida Blue',imgb)
cv2.imshow('salida Green',imgg)
cv2.imshow('salida Red',imgr)

#quitar color
# img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow('salida3',img2)

# img3 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# cv2.imshow('salida4',img3)

# img4 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# cv2.imshow('salida5',img4)

cv2.waitKey(0)
cv2.destroyAllWindows()
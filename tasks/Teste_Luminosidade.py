import cv2
import numpy as np

#Teste - Luminosidade

camera = cv2.VideoCapture(0)
while(True):

    conectado, imagem = camera.read()       

    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) 
    print(np.average(imagemCinza))   
  
    cv2.imshow("Face", imagem)    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
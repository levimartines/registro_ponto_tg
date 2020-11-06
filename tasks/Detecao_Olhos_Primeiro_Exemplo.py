import cv2
import numpy as np

classificador = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
classificadorOlho = cv2.CascadeClassifier("haarcascade/haarcascade_eye.xml")

camera = cv2.VideoCapture(0)

while(True):

    conectado, imagem = camera.read()   
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)        
    facesDetectadas = classificador.detectMultiScale(imagemCinza,scaleFactor=1.5,minSize=(100,100))

    for (x,y,l,a) in facesDetectadas:
        cv2.rectangle(imagem,(x,y),(x+l,y+a),(0,0,255),2)
        regiao = imagem[y:y + a, x:x + l]
        regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
        olhosDetectados = classificadorOlho.detectMultiScale(regiaoCinzaOlho)

        for(ox, oy, ol, oa) in olhosDetectados:
            cv2.rectangle(regiao,(ox, oy),(ox+50,oy+50),(0,255,0),2)           

    cv2.imshow("Face", imagem)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
camera.release()
cv2.destroyAllWindows()
import cv2
import os
import numpy as np

classificador = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

amostra = 1

id = input('Digite seu id: ')
largura, altura = 220, 220
print("Capturando as faces...")

def getImagemComId():
    caminhos = [os.path.join('folderTreino', f) for f in os.listdir('FolderTreino')]
    #print(caminhos)
    faces = []
    ids = []

    for caminhoImagem in caminhos:
        imagemCinza = cv2.cvtColor(cv2.imread(caminhoImagem), cv2.COLOR_BGR2GRAY) 
        facesDetectadas = classificador.detectMultiScale(imagemCinza,scaleFactor=1.5,minSize=(150,150))
        for (x,y,l,a) in facesDetectadas:               
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))        
            ids.append(id)
            faces.append(imagemFace)                          
            cv2.imwrite("folderTreino/pessoa." + str(id) + "." + str(amostra) + ".jpg", imagemFace)
            print("[foto " + str(amostra) + " capturada com sucesso]")
            amostra+=1
    return np.array(ids), faces

ids, faces = getImagemComId()



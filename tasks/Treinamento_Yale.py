import cv2
import os
import numpy as np
from PIL import Image

eigenface = cv2.face.EigenFaceRecognizer_create(50,7000)
fisherface = cv2.face.FisherFaceRecognizer_create(50,7000)
lbph = cv2.face.LBPHFaceRecognizer_create(2,6,2,4,5)

def getImagemComId():
    caminhos = [os.path.join('yalefaces/treinamento', f) for f in os.listdir('yalefaces/treinamento')]
    faces = []
    ids = []
    for caminhoImagem in caminhos:
       imagemFace = Image.open(caminhoImagem).convert('L')
       imagemNP = np.array(imagemFace, 'uint8')
       id = int(os.path.split(caminhoImagem)[1].split(".")[0].replace("subject", ""))
       ids.append(id)
       faces.append(imagemNP)

    return np.array(ids), faces

ids, faces = getImagemComId()

print("Treinando...")
eigenface.train(faces, ids)
eigenface.write('classificadores/classificadorEigenYale.yml')

fisherface.train(faces, ids)
fisherface.write('classificadores/classificadorFisherYale.yml')

lbph.train(faces, ids)
lbph.write('classificadores/classificadorLBPHYale.yml')

print("Treinamento realizado")
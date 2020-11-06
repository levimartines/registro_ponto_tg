import cv2
import os
import numpy as np
from PIL import Image

detectorFace = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
reconhecedor = cv2.face.EigenFaceRecognizer_create()
reconhecedor.read("classificadores/classificadorEigenYale.yml")
#reconhecedor = cv2.face.LBPHFaceRecognizer_create()
#reconhecedor.read("classificadores/classificadorLBPHYale.yml")

totalAcertos = 0
percentualAcerto = 0.0
totalConfianca = 0.0

caminhos = [os.path.join('yalefaces/teste', f) for f in os.listdir('yalefaces/teste')]
for caminhoImagem in caminhos:
    imagemFace = Image.open(caminhoImagem).convert('L')
    imagemFaceNP = np.array(imagemFace, 'uint8')
    facesDetectadas = detectorFace.detectMultiScale(imagemFaceNP)
    for (x, y, l, a) in facesDetectadas:
        cv2.rectangle(imagemFaceNP, (x, y), (x + l, y + a), (0, 0, 255), 2)
        cv2.imshow("Face", imagemFaceNP)
        cv2.waitKey(1000)


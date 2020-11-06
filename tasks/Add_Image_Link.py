import cv2
import urllib.request
import numpy as np

#input por link

def url_to_image(url):
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, 1)
	return image


classificador = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
classificadorOlho = cv2.CascadeClassifier("haarcascade/haarcascade_eye.xml")

amostra = 1

id = input('Digite seu id: ')
largura, altura = 220, 220

url = "https://static1.preparadopravaler.com.br/articles/2/28/35/2/@/132800-esta-com-o-rosto-liso-confira-alguns-mo-660x0-2.jpg"
imagem = url_to_image(url)

# No caso para o processamento é indicado processar em uma escala de cinza 
# para melhor precisão e desempenho

imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY) 
facesDetectadas = classificador.detectMultiScale(imagemCinza,scaleFactor=1.5,minSize=(100,100))

for (x,y,l,a) in facesDetectadas:
    
    imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
    cv2.imwrite("fotos/pessoa." + str(id) + "." + str(amostra) + ".jpg", imagemFace)
	
print("Foto capturada com sucesso - " + str(amostra))
amostra +=1

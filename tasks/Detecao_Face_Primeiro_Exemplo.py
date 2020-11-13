import cv2

classificador = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")
camera = cv2.VideoCapture(0)

while (True):

    conectado, imagem = camera.read()

    # No caso para o processamento é indicado processar em uma escala de cinza 
    # para melhor precisão e desempenho
    imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    facesDetectadas = classificador.detectMultiScale(imagemCinza, scaleFactor=1.5, minSize=(100, 100))

    for (x, y, l, a) in facesDetectadas:
        cv2.rectangle(imagem, (x, y), (x + l, y + a), (0, 0, 255), 2)

    cv2.imshow("Face", imagem)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

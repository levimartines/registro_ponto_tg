import datetime
import sqlite3
import cv2
import time
from datetime import datetime

# EigenFace

detector_face = cv2.CascadeClassifier("haarcascade/haarcascade_frontalface_default.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("classificadores/classificadorLBPH.yml")

width, height = 220, 220

font = cv2.FONT_HERSHEY_COMPLEX_SMALL = 1

cap = cv2.VideoCapture(0)
time.sleep(2)
i = 0
findface = False

while cap.isOpened():
    i += 1
    ret, img = cap.read()
    msg = 'PONTO REGISTRADO COM SUCESSO'

    if findface and i < 20:
        cv2.putText(img, msg, (100, 100), font, 1, (0, 255, 0))

    image_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_faces = detector_face.detectMultiScale(image_grey, scaleFactor=1.5, minSize=(30, 30))
    if ret:
        for (x, y, l, a) in detected_faces:
            image_face = cv2.resize(image_grey[y:y + a, x:x + l], (width, height))
            cv2.rectangle(img, (x, y), (x + l, y + a), (0, 0, 255), 2)
            class_id, confidence = recognizer.predict(image_face)

            print(str(class_id))
            print(str(confidence))
            if i >= 40 and confidence < 58 and class_id == 2:
                findface = True
                i = 0
                data = datetime.now()
                with sqlite3.connect("db/ponto.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT into REGISTRO (COL_ID, REG_DATA) values (?,?)",
                                (class_id, data))
                    con.commit()

            if i >= 40 and confidence < 50 and (class_id == 1 or class_id == 3):
                findface = True
                i = 0

                data = datetime.now()
                with sqlite3.connect("db/ponto.db") as con:
                    cur = con.cursor()
                    cur.execute("INSERT into REGISTRO (COL_ID, REG_DATA) values (?,?)",
                                (class_id, data))
                    con.commit()

        frame = cv2.imencode('.jpg', img)[1].tobytes()
        time.sleep(0.1)

    cv2.imshow("Face", img)
    if cv2.waitKey(1) == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit(0)


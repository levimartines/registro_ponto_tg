import datetime
import sqlite3
import time
import Treinamento3

import cv2
import numpy as np
from flask import Flask, render_template, Response, request, redirect
from datetime import datetime

detector_face = cv2.CascadeClassifier("./haarcascade/haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("classificadores/classificadorLBPH.yml")
width, height = 220, 220
font = cv2.FONT_HERSHEY_COMPLEX_SMALL

app = Flask(__name__)
codigo: int = 0
session_id: int = 0
user_id: int = 0


@app.route('/')
def index():
    return render_template('index.html')


def altera_session_id(id):
    global session_id
    session_id = id


def altera_codigo(novo_codigo):
    global codigo
    codigo = novo_codigo


def altera_user_id(new_user_id):
    global user_id
    user_id = new_user_id


@app.route("/login", methods=["POST", "GET"])
def login_post():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]

        if email == '' or password == '':
            return redirect('/')

        with sqlite3.connect("db/ponto.db") as con:
            cur = con.cursor()
            print(email)
            cur.execute("SELECT * FROM COLABORADORES WHERE COL_EMAIL LIKE ?", [email])
            rows = cur.fetchall()
            colaborador = rows[0]
            print(str(colaborador))
            if colaborador is None:
                return redirect('/')

            senha = colaborador[5]
            if password == senha:
                altera_user_id(colaborador[0])
                admin = colaborador[7]
                if admin == 2:
                    altera_session_id(2)
                else:
                    altera_session_id(1)
                return redirect('/consulta')
            else:
                return redirect('/')


@app.route('/consulta')
def consulta():
    global session_id
    if session_id == 0:
        return redirect('/')

    try:
        con = sqlite3.connect("db/ponto.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if session_id == 2:
            cur.execute("SELECT * FROM REGISTRO ORDER BY REG_DATA DESC")
            rows = cur.fetchall()
            con.close()
            return render_template("consulta.html", rows=rows)
        else:
            global user_id
            cur.execute("SELECT * FROM REGISTRO WHERE COL_ID = ? ORDER BY REG_DATA DESC", (str(user_id)))
            rows = cur.fetchall()
            con.close()
            return render_template("consulta-pessoa.html", rows=rows)
    except:
        return render_template("fail.html")


@app.route('/cadastro')
def cadastro():
    global session_id
    if session_id == 0:
        return redirect('/')

    return render_template('cadastro.html')


@app.route("/cadastro", methods=["POST", "GET"])
def my_form_post():
    if request.method == "POST":
        try:
            matricula = request.form["matricula"]
            name = request.form["name"]
            cpf = request.form["cpf"]
            rg = request.form["rg"]
            email = request.form["email"]
            senha = request.form["senha"]
            rh = request.form["admin"]
            print(str(rh))
            if matricula == '' or name == '' or cpf == '' or rg == '' or email == '' or senha == '':
                return redirect('/cadastro')

            isRh = 1
            if rh == 'on':
                isRh = 2

            with sqlite3.connect("db/ponto.db") as con:
                cur = con.cursor()
                con.execute(
                    "INSERT INTO COLABORADORES (COL_MATRICULA, COL_NOME,COL_CPF,COL_RG,COL_SENHA,COL_EMAIL,COL_ADMIN) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (matricula, name, cpf, rg, senha, email, 0))
                con.commit()
                global codigo
                altera_codigo(matricula)
        finally:
            con.close()
    return redirect('/cadastro-camera')


@app.route('/cadastro-camera')
def cadastro_camera():
    return render_template('cadastroCam.html')


@app.route('/registro')
def registro():
    global session_id
    if session_id == 0:
        return redirect('/')

    return render_template('registro.html')


def work():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    i = 0
    findface = False
    while cap.isOpened():
        i += 1
        ret, img = cap.read()

        if findface and i < 20:
            msg = 'PONTO REGISTRADO COM SUCESSO'
            cv2.putText(img, msg, (100, 100), font, 1, (0, 255, 0))

        image_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_faces = detector_face.detectMultiScale(image_grey, scaleFactor=1.5, minSize=(30, 30))
        if ret:
            for (x, y, l, a) in detected_faces:
                image_face = cv2.resize(image_grey[y:y + a, x:x + l], (width, height))
                cv2.rectangle(img, (x, y), (x + l, y + a), (0, 0, 255), 2)
                class_id, confidence = recognizer.predict(image_face)
                if i >= 30 and class_id == 1 and confidence < 65:
                    findface = True
                    i = 0
                    try:
                        name = 'Renan Alcolea'
                        data = datetime.now()
                        with sqlite3.connect("db/ponto.db") as con:
                            cur = con.cursor()
                            cur.execute("INSERT into REGISTRO (COL_ID,REG_NOME,REG_DATA) values (?,?,?)",
                                        (class_id, name, data))
                            con.commit()
                    except:
                        con.rollback()
                    finally:
                        con.close()
                elif i >= 30 and class_id == 2 and confidence < 65:
                    findface = True
                    i = 0
                    try:
                        name = 'Sandra Lucia'
                        data = datetime.now()
                        with sqlite3.connect("db/ponto.db") as con:
                            cur = con.cursor()
                            cur.execute("INSERT into REGISTRO (COL_ID,REG_NOME,REG_DATA) values (?,?,?)",
                                        (class_id, name, data))
                            con.commit()

                    except:
                        con.rollback()
                    finally:
                        con.close()
                elif i >= 30 and class_id == 3 and confidence < 65:
                    findface = True
                    i = 0
                    try:
                        name = 'Levi Martines'
                        data = datetime.now()
                        with sqlite3.connect("db/ponto.db") as con:
                            cur = con.cursor()
                            cur.execute("INSERT into REGISTRO (COL_ID,REG_NOME,REG_DATA) values (?,?,?)",
                                        (class_id, name, data))
                            con.commit()
                    except:
                        con.rollback()
                    finally:
                        con.close()

            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            time.sleep(0.1)
        else:
            break


@app.route("/post-registro", methods=["POST", "GET"])
def registro_post():
    msg = "msg"
    if request.method == "POST":
        try:
            operador_registro = request.form["codigo"]
            data = request.form["horario"]
            if data == '':
                return redirect('/consulta')

            data = data.replace("T", " ")
            data_format = data + ":00.000000"
            with sqlite3.connect("db/ponto.db") as con:
                cur = con.cursor()
                cur.execute("SELECT * FROM COLABORADORES WHERE COL_MATRICULA = ?", operador_registro)
                rows = cur.fetchall()
                colaborador = rows[0]
                nome = colaborador[2]
                cur.execute("INSERT into REGISTRO (COL_ID,REG_NOME,REG_DATA) values (?,?,?)",
                            (operador_registro, nome, data_format))
                con.commit()
                return redirect('/consulta')
        except:
            con.rollback()
        finally:
            con.close()
            return redirect('/consulta')
    return redirect('/consulta')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route("/view")
def view():
    global session_id
    if session_id == 0:
        return redirect('/')

    try:
        con = sqlite3.connect("db/ponto.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * from COLABORADORES")
        rows = cur.fetchall()
        con.close()
        return render_template("view.html", rows=rows)
    except:
        return render_template("fail.html")


@app.route('/regponto')
def regponto():
    return Response(work(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def capture():
    cap = cv2.VideoCapture(0)

    larg, alt = 220, 220
    amostra: int = 1
    while cap.isOpened():
        ret, img = cap.read()
        image_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected_faces = detector_face.detectMultiScale(image_grey, scaleFactor=1.5, minSize=(100, 100))
        if ret:
            for (x, y, l, a) in detected_faces:
                cv2.rectangle(img, (x, y), (x + l, y + a), (0, 0, 255), 2)
                if np.average(image_grey) > 70:
                    global codigo
                    imagemface = cv2.resize(image_grey[y:y + a, x:x + l], (larg, alt))
                    cv2.imwrite("fotos/pessoa." + str(codigo) + "." + str(amostra) + ".jpg", imagemface) + amostra
                    print("Foto capturada com sucesso - " + str(amostra))
                    amostra += 1

                    if amostra > 50:
                        cap.release()
                        Treinamento3.treinar()
                        return redirect('/success')

            frame = cv2.imencode('.jpg', img)[1].tobytes()
            yield b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
            time.sleep(0.15)
        else:
            break


@app.route('/video_capture')
def video_capture():
    return Response(capture(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

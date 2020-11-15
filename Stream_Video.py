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
            # cur.execute("SELECT * FROM REGISTRO ORDER BY REG_DATA DESC")
            cur.execute("SELECT REGISTRO.REG_DATA, COLABORADORES.COL_MATRICULA, "
                        "COLABORADORES.COL_NOME, COLABORADORES.COL_EMAIL "
                        "FROM REGISTRO "
                        "INNER JOIN COLABORADORES "
                        "ON REGISTRO.COL_ID = COLABORADORES.COL_ID "
                        "ORDER BY REGISTRO.REG_DATA DESC")
            rows = cur.fetchall()
            print(str(rows))
            for row in rows:
                print(str(row))
            con.close()
            return render_template("consulta.html", rows=rows)
        else:
            global user_id
            # cur.execute("SELECT * FROM REGISTRO WHERE COL_ID = ? ORDER BY REG_DATA DESC", (str(user_id)))
            cur.execute("SELECT REGISTRO.REG_DATA, COLABORADORES.COL_MATRICULA, COLABORADORES.COL_NOME "
                        "FROM REGISTRO "
                        "LEFT JOIN COLABORADORES "
                        "ON REGISTRO.COL_ID = COLABORADORES.COL_ID "
                        "WHERE REGISTRO.COL_ID = ? "
                        "ORDER BY REGISTRO.REG_DATA DESC", (str(user_id)))
            rows = cur.fetchall()
            print(str(rows))
            con.close()
            return render_template("consulta-pessoa.html", rows=rows)
    except:
        return render_template("fail.html")


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

            is_rh = 1
            if rh == 'on':
                is_rh = 2

            with sqlite3.connect("db/ponto.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO COLABORADORES (COL_MATRICULA, COL_NOME,COL_CPF,COL_RG,COL_SENHA,COL_EMAIL,COL_ADMIN) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (matricula, name, cpf, rg, senha, email, is_rh))
                con.commit()
                global codigo
                altera_codigo(int(matricula))
        finally:
            con.close()
    return redirect('/cadastro-camera')


@app.route('/cadastro-camera')
def cadastro_camera():
    global session_id
    if session_id == 0:
        return redirect('/')

    try:
        with sqlite3.connect("db/ponto.db") as con:
            cur = con.cursor()
            global codigo
            str_codigo = str(codigo)
            print(str_codigo)
            cur.execute("SELECT * FROM COLABORADORES WHERE COL_MATRICULA = ?", str_codigo)
            rows = cur.fetchall()
            print(str(rows))
            return render_template('cadastroCam.html', rows=rows)
    finally:
        con.close()


@app.route("/post-registro", methods=["POST", "GET"])
def registro_post():
    global session_id
    if session_id == 0:
        return redirect('/')

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
                print(str(colaborador))
                col_id = colaborador[0]
                cur.execute("INSERT into REGISTRO (COL_ID,REG_DATA) values (?,?)",
                            (col_id, data_format))
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
    global session_id
    if session_id == 0:
        return redirect('/')

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
        return render_template("gestao_colab.html", rows=rows)
    except:
        return render_template("fail.html")


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
                    str_codigo = str(codigo)
                    str_codigo = '3'
                    imagemface = cv2.resize(image_grey[y:y + a, x:x + l], (larg, alt))
                    cv2.imwrite("fotos/pessoa." + str_codigo + "." + str(amostra) + ".jpg", imagemface) + amostra
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


@app.template_filter('to_date')
def format_datetime(value):
    fdate = value[:16]
    print(fdate)
    data = datetime.strptime(fdate, '%Y-%m-%d  %H:%M')
    print(str(data))
    return data.strftime('%d/%m/%Y %H:%M')


@app.template_filter('format_rh')
def format_rh(value):
    if value == 2:
        return 'Sim'
    else:
        return 'Não'


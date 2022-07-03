import io
import os
import pathlib
import shutil
import PIL.Image as Image

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request
from sqlalchemy import true
from services.auth_service import get_image_webcam, compare_images

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ale@localhost:5432/Practicas_Cliente'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id_user = db.Column(db.Integer, db.Sequence(
        'user_id_seq'), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    crypt = db.Column(db.String(200))
    password = db.Column(db.String(200))
    image_bytes = db.Column(db.LargeBinary(500))

    def __init__(self, name, crypt, password, image_bytes):
        self.name = name
        self.crypt = crypt
        self.password = password
        self.image_bytes = image_bytes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if name == '' or password == '':
            return render_template('index.html', message='Por favor llene todo los campos')
        result = db.session.query(User).filter(
            User.name == name, User.password == password).first()
        if result:
            image = Image.open(io.BytesIO(result.image_bytes))
            image_path = "/Escuela/Universidad/3er_año/Practicas/Cliente/Client/python_feedback_app/static/image_users"
            try:
                shutil.rmtree('/Escuela/Universidad/3er_año/Practicas/Cliente/Client/python_feedback_app/static/image_users')
                os.mkdir(image_path)
                image = image.save(f"{image_path}/image_user.png")
                user = {
                    "id_user": result.id_user,
                    "name": result.name,
                    "password": result.password,
                    "crypt": result.password,
                    #"image_bytes": result.image_bytes.decode()
                }
                return render_template('image_verification.html', user=user)
            except:
                print("No se encontro la ruta descrita")
            
        return render_template('index.html', message='Usuario o contraseña incorrecto')

@app.route('/face-identification', methods=['POST'])
def submitFaceIdentification():
    message = get_image_webcam()
    if message == "Success":
        result = compare_images()
        print(result)
        if(result['statusCode']==405):
            return render_template("home.html", message="Token Inválido")
        if(result['statusCode']==406):
            return render_template("home.html", message="Token no enviado")
        if(result['similarity']== True):
            return render_template("home.html", message="Autenticación exitosa")
        if(result['statusCode']== 501):
            return render_template("index.html", message="Autenticación fallida")
        if(result['statusCode']==502):
            return render_template("index.html", message="Mala calidad de imagen")
        else:
            return render_template("index.html", message="Error en la autenticación facial")
    return render_template("index.html", message="Error en la autenticación facial")
if __name__ == '__main__':
    app.run()

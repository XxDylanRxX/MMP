import os
from modelos import *
from flask import Flask, session, render_template, request, redirect, url_for, send_file, flash
from flask_session import Session
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
from datetime import datetime
from flask_mail import Mail, Message
import pandas as pd
import time, datetime, serial, csv
import requests

load_dotenv()
app = Flask(__name__)
app = Flask(__name__, static_folder='static')
app.secret_key = 'xdxdxd'
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Configuracion de email
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = 'mmpdrizo@gmail.com'
app.config["MAIL_PASSWORD"] = "ktietwpxsekaiwpm"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False

mail = Mail(app)


id = 0 

@app.route('/')
def layout():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombres = request.form.get('nombres')
        apellidos = request.form.get('apellidos')
        edad = request.form.get('edad')
        usuario = request.form.get('usuario')
        correo = request.form.get('correo')
        contraseña = request.form.get('contraseña')
        telefono = request.form.get('telefono')

        if not nombres:
            return render_template("templates/login_registro/registro.html", alert="Ingrese sus nombres")

        if not apellidos:

            return render_template("login_registro/registro.html", alert="Ingrese sus apellidos")

        if not edad:
            return render_template("login_registro/registro.html", alert="Ingrese su edad")

        if not usuario:
            return render_template("login_registro/registro.html", alert="Ingrese un usuario")

        if not correo:
            return render_template("login_registro/registro.html", alert="Ingrese un correo")

        if not contraseña:
            return render_template("login_registro/registro.html", alert="Ingrese una contraseña")
        
    
       
        nuevo_usuario = Usuario()
           
        user = nuevo_usuario.add_user(nombres, apellidos, edad, correo, telefono, usuario, generate_password_hash(contraseña))

        

        msg = Message('Gracias por tu registro, lo haz hecho correctamente!', 
                        sender = app.config["MAIL_USERNAME"], recipients=[correo])

        msg.html = render_template('E-mails/resgistroEmail.html', nombre=nombres)
        mail.send(msg)
        user = Usuario.query.filter_by(usuario=usuario).first()
        print(user.id)
        session["id_usuario"] = user.id
    

        return render_template("index.html", success="Se ha registrado correctamente")
       
    else:
        return render_template('login_registro/registro.html')
    

@app.route('/cerrar')
def logout():
	session['id_usuario'] = None

	return render_template("index.html", success="Se ha Cerrado la sesión")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        contraseña = request.form.get('clave')
        
        if Usuario.login_user(usuario, contraseña):
            user = Usuario.query.filter_by(usuario=usuario).first()
            print(user.id)
            session["id_usuario"] = user.id
            return render_template("index.html", success="Se ha ingresado correctamente")
        elif os.getenv("USER_ADMIN") == usuario and os.getenv("PASSWORD_ADMIN") == contraseña:
           return redirect(url_for('admon'))

        else:
            return render_template("login_registro/registro.html", alert="No se ha podido ingresar correctamente")
    return render_template('login_registro/login.html')

@app.route("/medicionbase", methods=["GET", "POST"])
def medicionbase():
    if session['id_usuario'] == None:
        return redirect('/login')
    if request.method == "POST":
        return redirect(url_for('medicion'))
    else:
        return render_template('mediciones/mediciónPulso.html')
    

@app.route("/medicionP", methods=["GET", "POST"])
def medicion():
    if session['id_usuario'] == None:
        return redirect('/login')
    if request.method == "GET":
        usuario_id = session['id_usuario']
        a=0.0
        b=0.0
        c=0.0
        i=0.0
        a=time.time()
        try:
            serialArduino = serial.Serial("COM5", 115200)
        except serial.serialutil.SerialException:
              return render_template("mediciones/mediciónPulso.html", alert="Ha ocurrido un error al abrir el puerto COM5. Verifica la conexión del dispositivo.")
        # with open('medicionP.ino', 'r') as f:
        #     codigo = f.read()

        # serialArduino.write(codigo.encode())
        time.sleep(2)
        flash("Espere 30 segundos", "error")
        lista = []
        lista_aux = []
        sum = 0
        promedio = 0
        fecha = datetime.datetime.now()
        while i < 40:
            bpm = serialArduino.readline().decode('ascii')
            bpm = int(bpm.replace("\r\n",""))
            lista.append(bpm)
            b=time.time()
            c=b-a
            if c>=1.0:
                a=time.time()
                i=i+1
                print(i)
            else:
                continue
            for j in lista:
                if j > 50 and j < 100:
                    lista_aux.append(j)
                    sum += j
                else:
                    continue
        serialArduino.close()
        try:            
            promedioP =  int(sum/len(lista_aux))
            print(promedioP)
            print(session['id_usuario'])
            # Insertar en la base de datos
            nueva_medicion = Medicion()
            medicion1 = nueva_medicion.add_medicion(usuario_id, promedioP)
            print(f"BPM = {promedioP}")
            
            #Enviar mensaje de medicion al usuario

            usuario= Usuario.query.get(usuario_id)
            
            msg = Message('Haz obtenido una nueva medición!', 
                        sender = app.config["MAIL_USERNAME"], recipients=[usuario.correo])

            msg.html = render_template('E-mails/medicionEmail.html', nombre=usuario.nombres, promedio=promedioP)
            mail.send(msg)
        except:
            return render_template("mediciones/mediciónPulso.html", alert = "Ha ocurrido un error, vuelva a intentarlo")

        return render_template("mediciones/mediciónPulso.html", success = "Ha obtenido una nueva medición", promedioP=promedioP)
    else:
        return redirect("/")
    

@app.route("/medicionbase1", methods=["GET", "POST"])
def medicionbase1():
    if session['id_usuario'] == None:
        return redirect('/login')
    if request.method == "POST":
        return redirect(url_for('medicionO'))
    else:
        return render_template('mediciones/mediciónPulso.html')


@app.route("/medicionO", methods=["GET", "POST"])
def medicionO():
    if session['id_usuario'] == None:
        return redirect('/login')
    if request.method == "GET":
        usuario_id = session['id_usuario']
        a=0.0
        b=0.0
        c=0.0
        i=0.0
        a=time.time()
        try:
            serialArduino = serial.Serial("COM5", 115200)
        except serial.serialutil.SerialException:
              return render_template("mediciones/mediciónPulso.html", alert="Ha ocurrido un error al abrir el puerto COM5. Verifica la conexión del dispositivo.")
        with open('medicionS.ino', 'r') as f:
            codigo = f.read()

        serialArduino.write(codigo.encode())
        time.sleep(2)
        lista = []
        lista_aux = []
        sum = 0
        promedio = 0
        while i < 30:
            spo2 = serialArduino.readline().decode('ascii')
            spo2 = int(spo2.replace("\r\n",""))
            lista.append(spo2)
            b=time.time()
            c=b-a
            if c>=1.0:
                a=time.time()
                i=i+1
                print(i)
            else:
                continue
            for j in lista:
                if j > 90 and j < 100:
                    lista_aux.append(j)
                    sum += j
                else:
                    continue
        serialArduino.close()
        try:            
            promedioO =  int(sum/len(lista_aux))
            print(promedioO)
            usuario= Usuario.query.get(usuario_id)
            # Insertar en la base de datos
            nueva_medicion = Medicion2()
            medicion2 = nueva_medicion.add_medicion(usuario_id,promedioO)
            print(f"SPO2 = {promedioO}")
            
            #Enviar mensaje de medicion al usuario
            print(usuario.correo)
            print(usuario.nombres)
            msg = Message('Haz obtenido una nueva medición!', 
                         sender = app.config["MAIL_USERNAME"], recipients=[usuario.correo])

            msg.html = render_template('E-mails/medicionEmailS.html', nombre=usuario.nombres, promedio=promedioO)
            mail.send(msg)
        except:
            return render_template("mediciones/mediciónPulso.html", alert = "Ha ocurrido un error, vuelva a intentarlo")

        return render_template("mediciones/mediciónPulso.html", success = "Ha obtenido una nueva medición", promedioO=promedioO)
    else:
        return redirect("/")
    
@app.route('/tuto')
def tutorial():
    return render_template('tutorial.html')

@app.route('/TablasMediciones')
def TablasM():
     medicionesP = Medicion.query.filter_by(usuario_id=session['id_usuario']).all()
     medicionesS = Medicion2.query.filter_by(usuario_id=session['id_usuario']).all()
     return render_template('mediciones/mediciones_pulso.html', mediciones=medicionesP, mediciones2= medicionesS)

@app.route('/admin')
def admon():
    return render_template("admin/mediciones_admin.html", success="Se ha ingresado correctamente como administrador")

@app.route('/MedicionadminPulso')
def MedicionAdminP():
    usuarios = db.session.query(Usuario.id, Usuario.nombres, Medicion.medicion_cardiaca, Medicion.fecha, Medicion.hora).join(Medicion).all()
    return render_template('admin/TablaGeneralPulso.html', usuarios = usuarios)

@app.route('/MedicionadminSpo2')
def MedicionAdminS():
    usuarios = db.session.query(Usuario.id, Usuario.nombres, Medicion2.medicion_spo2, Medicion2.fecha, Medicion2.hora).join(Medicion2).all()
    return render_template('admin/TablaGeneralSpo2.html', usuarios = usuarios)


@app.route("/descargaP")
def descarga():
    usuarios = db.session.query(Usuario.nombres.label('NombreCompleto'), Usuario.edad.label('Edad'), Usuario.usuario.label('Usuario'), Usuario.correo.label('Correo'), Medicion.medicion_cardiaca.label('Bpm'), Medicion.fecha.label('Fecha')).join(Medicion).order_by(Usuario.nombres).all()

   
    data = {
        'NombreCompleto': [usuario.NombreCompleto for usuario in usuarios],
        'Edad': [usuario.Edad for usuario in usuarios],
        'Usuario': [usuario.Usuario for usuario in usuarios],
        'Correo': [usuario.Correo for usuario in usuarios],
        'Bpm': [usuario.Bpm for usuario in usuarios],
        'Fecha': [usuario.Fecha.strftime('%Y-%m-%d') for usuario in usuarios]
    }
    df = pd.DataFrame(data)

    nombre_archivo = 'datos_Pulso.xlsx'
    df.to_excel(nombre_archivo, index=False)

    return send_file(nombre_archivo, as_attachment=True)

@app.route("/descargaS")
def descarga1():
    usuarios = db.session.query(Usuario.nombres.label('NombreCompleto'), Usuario.edad.label('Edad'), Usuario.usuario.label('Usuario'), Usuario.correo.label('Correo'), Medicion2.medicion_spo2.label('spo2'), Medicion2.fecha.label('Fecha')).join(Medicion2).order_by(Usuario.nombres).all()

    # Crear un DataFrame con los datos de los usuarios
    data = {
        'NombreCompleto': [usuario.NombreCompleto for usuario in usuarios],
        'Edad': [usuario.Edad for usuario in usuarios],
        'Usuario': [usuario.Usuario for usuario in usuarios],
        'Correo': [usuario.Correo for usuario in usuarios],
        'spo2': [usuario.spo2 for usuario in usuarios],
        'Fecha': [usuario.Fecha.strftime('%Y-%m-%d') for usuario in usuarios]
    }
    df = pd.DataFrame(data)

    # Guardar el DataFrame en un archivo Excel
    nombre_archivo = 'datos_Spo2.xlsx'
    df.to_excel(nombre_archivo, index=False)

    return send_file(nombre_archivo, as_attachment=True)

@app.route("/editar")
def edit():
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@app.route('/usuario/<int:id>', methods=['GET', 'POST'])
def editar_usuario(id):
    usuario = Usuario.query.get(id)
    if request.method == 'POST':
        usuario.nombres = request.form['nombres']
        usuario.apellidos = request.form['apellidos']
        usuario.edad = int(request.form['edad'])
        usuario.correo = request.form['correo']
        usuario.telefono = request.form['telefono']
        db.session.commit()
        return redirect(url_for('edit'))
    return render_template('admin/editar_usuario.html', usuario=usuario)

@app.route('/usuario/<int:id>/borrar', methods=['POST'])
def borrar_usuario(id):
    usuario = Usuario.query.get(id)
    
    mediciones_pul = Medicion.query.filter_by(usuario_id=id).all()
    for medicion_pul in mediciones_pul:
        db.session.delete(medicion_pul)
    
  
    mediciones_po2 = Medicion2.query.filter_by(usuario_id=id).all()
    for medicion_po2 in mediciones_po2:
        db.session.delete(medicion_po2)
    
    db.session.delete(usuario)
    db.session.commit()
    return redirect(url_for('edit'))


if __name__ =='__main__':
    app.run(debug = True)
    mail.init_app(app)
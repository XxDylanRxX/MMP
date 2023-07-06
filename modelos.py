import os
import time, serial, csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import date, datetime, timedelta

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = "registro_usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    correo = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    usuario = db.Column(db.String(20), unique=True, nullable=False)
    contraseña = db.Column(db.String(200), nullable=False)

    def add_user(self, nombres, apellidos, edad, correo, telefono, usuario, contraseña):
        nuevo_usuario = Usuario(nombres=nombres, apellidos=apellidos, edad=edad, correo=correo, 
                                telefono=telefono, usuario=usuario, contraseña=contraseña)
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            print("Usuario agregado correctamente")
        except IntegrityError:
            db.session.rollback()
            print("El nombre de usuario ya existe")

    def login_user(usuario, contraseña):
        user = Usuario.query.filter_by(usuario=usuario).first()
        if user and check_password_hash(user.contraseña, contraseña):
            print('Inicio de sesión exitoso.', 'success')
            return True
        else:
            print('Nombre de usuario o contraseña incorrectos. Por favor, inténtalo nuevamente.', 'error')
            return False
        

class Medicion(db.Model):
    __tablename__ = "medicionespul"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('registro_usuarios.id'), nullable=False)
    medicion_cardiaca = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

    def add_medicion(self, usuario_id, medicion_cardiaca):
        nueva_medicion = Medicion(usuario_id=usuario_id, medicion_cardiaca=medicion_cardiaca,
                                  fecha=date.today(), hora=datetime.now().time())
        db.session.add(nueva_medicion)
        db.session.commit()

class Medicion2(db.Model):
    __tablename__ = "medicionespo2"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('registro_usuarios.id'), nullable=False)
    medicion_spo2 = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)

    def add_medicion(self, usuario_id, medicion_spo2):
        nueva_medicion = Medicion2(usuario_id=usuario_id, medicion_spo2=medicion_spo2,
                                  fecha=date.today(), hora=datetime.now().time())
        db.session.add(nueva_medicion)
        db.session.commit()

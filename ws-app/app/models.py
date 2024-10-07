from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Class Definition

class Votacion(db.Model):
    __tablename__ = "votaciones"
    idVotacion =db.Column(db.Integer, primary_key=True, index=True)
    created_at =db.Column(db.DateTime, default=datetime.now)
    status =db.Column(db.String, index=True,default='open')
    summary =db.Column(db.String, index=True)
    escanio_total =db.Column(db.Integer, index=True, default= 1)
    deleted =db.Column(db.Integer, index=True, default= 0)
    listas = db.relationship('Lista', backref='votacion', lazy=True)
     
    

class Lista(db.Model):
    __tablename__ = "listas"
    idLista =db.Column(db.Integer, primary_key=True, index=True)
    idVotacion = db.Column(db.Integer, db.ForeignKey('votaciones.idVotacion'), nullable=False)
    created_at =db.Column(db.DateTime, default=datetime.now)
    created_by =db.Column(db.String, index=True,default='batch')
    status =db.Column(db.String, index=True,default='open')
    summary =db.Column(db.String, index=True,default='-')
    description =db.Column(db.String, index=True)
    votos_total =db.Column(db.Integer, index=True, default=0)
    escanios_total =db.Column(db.Integer, index=True, default=0)
    votos = db.relationship('Voto', backref='lista', lazy=True)
    escanios = db.relationship('Escanio', backref='lista', lazy=True)

class Voto(db.Model):
    __tablename__ = "votos"
    idVoto =db.Column(db.Integer, primary_key=True, index=True)
    idLista = db.Column(db.Integer, db.ForeignKey('listas.idLista'), nullable=False)
    created_at =db.Column(db.DateTime, default=datetime.now)
    created_by =db.Column(db.String, index=True,default='batch')
    votos_cant =db.Column(db.Integer, index=True, default= 1)

class Escanio(db.Model):
    __tablename__ = "escanios"
    idEscanio =db.Column(db.Integer, primary_key=True, index=True)
    idLista = db.Column(db.Integer, db.ForeignKey('listas.idLista'), nullable=False)
    created_at =db.Column(db.DateTime, default=datetime.now)
    votos_total = db.Column(db.Integer, index=True,  default=0)
    escanios_asignado = db.Column(db.Integer, index=True,  default=0)

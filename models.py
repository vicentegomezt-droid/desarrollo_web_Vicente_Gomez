from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Tabla region
class Region(db.Model):
    __tablename__ = 'region'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    comunas = db.relationship('Comuna', backref='region', lazy=True)

# Tabla comuna
class Comuna(db.Model):
    __tablename__ = 'comuna'

    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('region.id'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)

# Tabla ave
class Ave(db.Model):
    __tablename__ = 'ave'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)

# Tabla voluntario
class Voluntario(db.Model):
    __tablename__ = 'voluntario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.Text, nullable=False)
    region = db.Column(db.String(50), nullable=False)
    comuna = db.Column(db.String(50), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.now)

# Tabla avistamiento
class Avistamiento(db.Model):
    __tablename__ = 'avistamiento'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    voluntario_id = db.Column(db.Integer, db.ForeignKey('voluntario.id'), nullable=False)
    tipo_ave = db.Column(db.String(50), nullable=False)
    nombre_ave = db.Column(db.String(100), nullable=False)
    lugar = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
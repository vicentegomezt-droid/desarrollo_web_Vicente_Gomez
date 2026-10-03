from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Region, Comuna, Ave, Voluntario, Avistamiento
from datetime import datetime
import re

app = Flask(__name__)
app.secret_key = 'clave_secreta_tarea2'

# Configuración de base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cc5002:programacionweb@localhost/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ruta 1: Inicio / Portada
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para cargar comunas dinámicamente según la región elegida
@app.route('/get-comunas/<int:region_id>')
def get_comunas(region_id):
    comunas = Comuna.query.filter_by(region_id=region_id).all()
    lista_comunas = [{'id': c.id, 'nombre': c.nombre} for c in comunas]
    return jsonify(lista_comunas)

# Ruta 2: Registrar Voluntario
@app.route('/agregar-voluntario', methods=['GET', 'POST'])
def agregar_voluntario():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        apellido = request.form.get('apellido', '').strip()
        email = request.form.get('email', '').strip()
        telefono = request.form.get('telefono', '').strip()
        direccion = request.form.get('direccion', '').strip()
        region_id = request.form.get('region')
        comuna_id = request.form.get('comuna')

        # Validaciones del lado del servidor
        errores = []
        if not nombre or not apellido:
            errores.append("El nombre y el apellido son obligatorios.")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errores.append("Ingresa un correo electrónico válido.")
        if not telefono or not re.match(r"^\+?\d{8,15}$", telefono):
            errores.append("Ingresa un número de teléfono válido.")
        if not direccion or not region_id or not comuna_id:
            errores.append("Debe completar todos los campos de ubicación.")

        if errores:
            for error in errores:
                flash(error, 'danger')
            regiones = Region.query.all()
            return render_template('agregar_voluntario.html', regiones=regiones)

        # Buscar nombres de región y comuna seleccionadas
        region_obj = Region.query.get(region_id)
        comuna_obj = Comuna.query.get(comuna_id)

        nuevo_voluntario = Voluntario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            telefono=telefono,
            direccion=direccion,
            region=region_obj.nombre if region_obj else '',
            comuna=comuna_obj.nombre if comuna_obj else ''
        )

        try:
            db.session.add(nuevo_voluntario)
            db.session.commit()
            flash('¡Voluntario registrado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar en la base de datos.', 'danger')

    regiones = Region.query.all()
    return render_template('agregar_voluntario.html', regiones=regiones)

# Ruta 3: Registrar Avistamiento
@app.route('/agregar-avistamiento', methods=['GET', 'POST'])
def agregar_avistamiento():
    if request.method == 'POST':
        voluntario_id = request.form.get('voluntario_id')
        tipo_ave = request.form.get('tipo_ave')
        nombre_ave = request.form.get('nombre_ave')
        lugar = request.form.get('lugar', '').strip()
        fecha_str = request.form.get('fecha')
        hora_str = request.form.get('hora')

        errores = []
        if not voluntario_id or not tipo_ave or not nombre_ave or not lugar or not fecha_str or not hora_str:
            errores.append("Todos los campos del avistamiento son obligatorios.")

        if errores:
            for error in errores:
                flash(error, 'danger')
            voluntarios = Voluntario.query.all()
            aves = Ave.query.all()
            return render_template('agregar_avistamiento.html', voluntarios=voluntarios, aves=aves)

        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        hora_obj = datetime.strptime(hora_str, '%H:%M').time()

        nuevo_avistamiento = Avistamiento(
            voluntario_id=voluntario_id,
            tipo_ave=tipo_ave,
            nombre_ave=nombre_ave,
            lugar=lugar,
            fecha=fecha_obj,
            hora=hora_obj
        )

        try:
            db.session.add(nuevo_avistamiento)
            db.session.commit()
            flash('¡Avistamiento registrado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar el avistamiento.', 'danger')

    voluntarios = Voluntario.query.all()
    aves = Ave.query.all()
    return render_template('agregar_avistamiento.html', voluntarios=voluntarios, aves=aves)

# Ruta 4: Ver Voluntarios
@app.route('/voluntarios')
def ver_voluntarios():
    lista = Voluntario.query.order_by(Voluntario.fecha_registro.desc()).all()
    return render_template('ver_voluntarios.html', voluntarios=lista)

# Ruta 5: Ver Avistamientos
@app.route('/avistamientos')
def ver_avistamientos():
    lista = Avistamiento.query.order_by(Avistamiento.fecha.desc()).all()
    return render_template('ver_avistamientos.html', avistamientos=lista)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Region, Comuna, Ave, Voluntario, Avistamiento, Comentario, Registro
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import re

app = Flask(__name__)
app.secret_key = 'clave_secreta_tarea2'

# Configuración de base de datos MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cc5002:programacionweb@localhost/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuración para subir imágenes o videos
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'webm', 'mov'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
def archivo_permitido(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ruta 1: Inicio / Portada
@app.route('/')
def index():
    ultimos_avistamientos = Avistamiento.query.order_by(Avistamiento.id.desc()).limit(2).all()

    total_avistamientos = Avistamiento.query.count()
    total_voluntarios = Voluntario.query.count()

    por_tipo_raw = db.session.query(
        Avistamiento.tipo_ave,
        db.func.count(Avistamiento.id)
    ).group_by(Avistamiento.tipo_ave).all()

    estadisticas_tipo = {tipo: cantidad for tipo, cantidad in por_tipo_raw}

    return render_template(
        'index.html',
        ultimos_avistamientos=ultimos_avistamientos,
        total_avistamientos=total_avistamientos,
        total_voluntarios=total_voluntarios,
        estadisticas_tipo=estadisticas_tipo
    )

# Ruta para cargar comunas dinámicamente según la región elegida
@app.route('/get-comunas/<int:region_id>')
def get_comunas(region_id):
    comunas = Comuna.query.filter_by(region_id=region_id).all()
    lista_comunas = [{'id': c.id, 'nombre': c.nombre} for c in comunas]
    return jsonify(lista_comunas)

# Ruta 2: Registrar Voluntario
@app.route('/agregar-voluntario', methods=['GET', 'POST'])
def agregar_voluntario():
    regiones = Region.query.all()

    if request.method == 'POST':
        form_data = {
            'nombre': request.form.get('nombre', '').strip(),
            'apellido': request.form.get('apellido', '').strip(),
            'email': request.form.get('email', '').strip(),
            'telefono': request.form.get('telefono', '').strip(),
            'direccion': request.form.get('direccion', '').strip(),
            'region': request.form.get('region', ''),
            'comuna': request.form.get('comuna', '')
        }

        errores = []
        if not form_data['nombre'] or not form_data['apellido']:
            errores.append("El nombre y el apellido son obligatorios.")
        if not form_data['email'] or not re.match(r"[^@]+@[^@]+\.[^@]+", form_data['email']):
            errores.append("Ingresa un correo electrónico válido.")
        if not form_data['telefono'] or not re.match(r"^\+?\d{8,15}$", form_data['telefono']):
            errores.append("Ingresa un número de teléfono válido.")
        if not form_data['direccion'] or not form_data['region'] or not form_data['comuna']:
            errores.append("Debe completar todos los campos de ubicación.")

        if errores:
            for error in errores:
                flash(error, 'danger')
            return render_template('agregar_voluntario.html', regiones=regiones, form_data=form_data)

        region_obj = Region.query.get(form_data['region'])
        comuna_obj = Comuna.query.get(form_data['comuna'])

        nuevo_voluntario = Voluntario(
            nombre=form_data['nombre'],
            apellido=form_data['apellido'],
            email=form_data['email'],
            telefono=form_data['telefono'],
            direccion=form_data['direccion'],
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
            return render_template('agregar_voluntario.html', regiones=regiones, form_data=form_data)

    return render_template('agregar_voluntario.html', regiones=regiones, form_data={})
# Ruta 3: Registrar Avistamiento
@app.route('/agregar-avistamiento', methods=['GET', 'POST'])
def agregar_avistamiento():
    voluntarios = Voluntario.query.all()
    aves = Ave.query.all()

    if request.method == 'POST':
        form_data = {
            'voluntario_id': request.form.get('voluntario_id', ''),
            'tipo_ave': request.form.get('tipo_ave', ''),
            'nombre_ave': request.form.get('nombre_ave', ''),
            'lugar': request.form.get('lugar', '').strip(),
            'fecha': request.form.get('fecha', ''),
            'hora': request.form.get('hora', '')
        }

        archivo = request.files.get('archivo')
        errores = []

        if not form_data['voluntario_id'] or not form_data['tipo_ave'] or not form_data['nombre_ave'] or not form_data['lugar'] or not form_data['fecha'] or not form_data['hora']:
            errores.append("Todos los campos del avistamiento son obligatorios.")

        if not archivo or archivo.filename == '':
            errores.append("Debes adjuntar una imagen o video del avistamiento.")
        elif not archivo_permitido(archivo.filename):
            errores.append("Formato de archivo no permitido (usa imagen o video).")

        fecha_obj = None
        hora_obj = None

        if not errores:
            try:
                fecha_obj = datetime.strptime(form_data['fecha'], '%Y-%m-%d').date()
                hora_obj = datetime.strptime(form_data['hora'], '%H:%M').time()
            except ValueError:
                errores.append("La fecha u hora ingresada no tiene un formato válido.")

        if not errores and fecha_obj:
            hoy = datetime.now().date()
            if fecha_obj > hoy:
                errores.append("No puedes registrar un avistamiento en una fecha futura.")
            elif fecha_obj.year < 1900:
                errores.append("Ingresa una fecha válida (desde el año 1900 en adelante).")

        if errores:
            for error in errores:
                flash(error, 'danger')
            return render_template(
                'agregar_avistamiento.html',
                voluntarios=voluntarios,
                aves=aves,
                form_data=form_data
            )

        nuevo_avistamiento = Avistamiento(
            voluntario_id=form_data['voluntario_id'],
            tipo_ave=form_data['tipo_ave'],
            nombre_ave=form_data['nombre_ave'],
            lugar=form_data['lugar'],
            fecha=fecha_obj,
            hora=hora_obj
        )

        try:
            db.session.add(nuevo_avistamiento)
            db.session.flush()

            nombre_seguro = secure_filename(archivo.filename)
            nombre_final = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{nombre_seguro}"
            ruta_fisica = os.path.join(app.config['UPLOAD_FOLDER'], nombre_final)
            archivo.save(ruta_fisica)

            ext = nombre_seguro.rsplit('.', 1)[1].lower()
            tipo_media = 'video' if ext in {'mp4', 'webm', 'mov'} else 'imagen'

            nuevo_registro = Registro(
                avistamiento_id=nuevo_avistamiento.id,
                ruta_archivo=f"uploads/{nombre_final}",
                tipo_archivo=tipo_media
            )
            db.session.add(nuevo_registro)
            db.session.commit()

            flash('¡Avistamiento registrado exitosamente!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('Error al guardar el avistamiento.', 'danger')
            return render_template(
                'agregar_avistamiento.html',
                voluntarios=voluntarios,
                aves=aves,
                form_data=form_data
            )

    return render_template('agregar_avistamiento.html', voluntarios=voluntarios, aves=aves, form_data={})

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

# ==========================================
# RUTAS Y APIS PARA COMENTARIOS (TAREA 3)
# ==========================================

@app.route('/avistamiento/<int:id>')
def detalle_avistamiento(id):
    avistamiento = Avistamiento.query.get_or_404(id)
    return render_template('detalle_avistamiento.html', avistamiento=avistamiento)

@app.route('/api/avistamiento/<int:id>/comentarios')
def get_comentarios(id):
    comentarios = Comentario.query.filter_by(avistamiento_id=id).order_by(Comentario.fecha.desc()).all()
    data = [{
        'nombre': c.nombre,
        'texto': c.texto,
        'fecha': c.fecha.strftime('%d/%m/%Y %H:%M')
    } for c in comentarios]
    return jsonify(data)

@app.route('/api/comentario/agregar', methods=['POST'])
def agregar_comentario():
    datos = request.get_json()
    nombre = datos.get('nombre', '').strip()
    texto = datos.get('texto', '').strip()
    avistamiento_id = datos.get('avistamiento_id')

    if not nombre or len(nombre) < 3 or len(nombre) > 50:
        return jsonify({'success': False, 'mensaje': 'El nombre debe tener entre 3 y 50 caracteres.'}), 400

    if not texto or len(texto) < 5:
        return jsonify({'success': False, 'mensaje': 'El comentario debe tener al menos 5 caracteres.'}), 400

    if not avistamiento_id:
        return jsonify({'success': False, 'mensaje': 'Avistamiento no válido.'}), 400

    try:
        nuevo_comentario = Comentario(
            nombre=nombre,
            texto=texto,
            avistamiento_id=avistamiento_id
        )
        db.session.add(nuevo_comentario)
        db.session.commit()
        return jsonify({'success': True, 'mensaje': 'Comentario agregado exitosamente.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'mensaje': 'Error interno al guardar el comentario.'}), 500

if __name__ == '__main__':
    app.run(debug=True)
# Importación de módulos necesarios de Flask
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from functools import wraps
import os
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Inicialización de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'clave-secreta-12345'

# Configuración de usuarios
USERS = {
    'admin': 'admin123',
    'usuario': 'password123'
}

# Configuración SMTP
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp')
SMTP_PORT = int(os.getenv('SMTP_PORT', 1025))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Por favor inicia sesión primero', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            flash('Has iniciado sesión correctamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session.get('username'))

@app.route('/enviar', methods=['POST'])
@login_required
def enviar_correo():
    destinatario = request.form.get('destinatario')
    asunto = request.form.get('asunto')
    contenido = request.form.get('contenido')
    
    if not all([destinatario, asunto, contenido]):
        flash('Todos los campos son requeridos', 'error')
        return redirect(url_for('index'))

    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = f"{session['username']}@ejemplo.com"
        msg['To'] = destinatario
        msg['Subject'] = asunto
        msg.attach(MIMEText(contenido, 'plain'))

        # Conectar y enviar
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.send_message(msg)

        # Guardar registro
        guardar_registro_correo({
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'remitente': session['username'],
            'destinatario': destinatario,
            'asunto': asunto,
            'estado': 'enviado'
        })
        
        flash('Correo enviado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al enviar el correo: {str(e)}', 'error')
        guardar_registro_correo({
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'remitente': session['username'],
            'destinatario': destinatario,
            'asunto': asunto,
            'estado': 'error',
            'error': str(e)
        })

    return redirect(url_for('index'))

@app.route('/historial')
@login_required
def historial():
    registros = cargar_registros_correo()
    return render_template('historial.html', registros=registros)

def guardar_registro_correo(registro):
    """Guarda un registro de correo enviado en un archivo JSON"""
    registros = cargar_registros_correo()
    registros.append(registro)
    
    with open('correos_log.json', 'w') as f:
        json.dump(registros, f, indent=2)

def cargar_registros_correo():
    """Carga los registros de correos desde el archivo JSON"""
    try:
        with open('correos_log.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
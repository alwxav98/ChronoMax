from flask import Flask, render_template, request, redirect, url_for, session, jsonify, send_file
from flask_restful import Api
from werkzeug.security import generate_password_hash, check_password_hash

from db_config import db
from models.activity_model import  CronometroModel
from models.user_model import UserModel
from models.cronometro_model import Cronometro

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from sqlalchemy import cast, Date
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
db.init_app(app)
api = Api(app)

# Crear un objeto Cronometro
cronometro = Cronometro()

# Página principal (Bienvenida)
@app.route('/')
def home():
    return render_template('index.html')

# Página de registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        # Crear un nuevo usuario
        new_user = UserModel(email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template('register.html')

# Página de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Buscar usuario en la base de datos
        user = UserModel.query.filter_by(Email=email).first()

        if user:
            # Verificar contraseña
            if check_password_hash(user.PasswordHash, password):
                session['user_id'] = user.ID  # Almacenar el user_id en la sesión
                return redirect(url_for('cronometro_page'))  # Redirigir a la página del cronómetro
            else:
                return "Contraseña incorrecta.", 401
        else:
            return "Usuario no encontrado.", 404

    return render_template('login.html')

@app.route('/cronometro', methods=['GET', 'POST'])
def cronometro_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirigir a login si no hay sesión activa

    if request.method == 'POST':
        action = request.form.get('action')
        activity_name = request.form.get('activity_name')  # Obtener el nombre de la actividad

        if action == 'start':
            cronometro.start()

            # Guardar actividad en la base de datos
            new_activity = CronometroModel(
                UserID=session['user_id'],
                ActivityName=activity_name,
                Duration=0  # Inicialmente 0, actualizar después de detener el cronómetro
            )
            db.session.add(new_activity)
            db.session.commit()

            # Almacenar el ID de la actividad en la sesión para actualizar su duración después
            session['activity_id'] = new_activity.ID

        elif action == 'stop':
            cronometro.stop()

            # Actualizar la duración de la actividad en la base de datos
            if 'activity_id' in session:
                elapsed_seconds = cronometro.get_elapsed_time()
                activity = CronometroModel.query.get(session['activity_id'])
                if activity:
                    activity.Duration = elapsed_seconds
                    db.session.commit()

                # Eliminar el ID de la actividad de la sesión
                session.pop('activity_id', None)

        elif action == 'reset':
            cronometro.reset()

    return render_template('cronometro.html', elapsed_time=cronometro.get_elapsed_time())

# Guardar el tiempo transcurrido en la base de datos
@app.route('/save_time', methods=['POST'])
def save_time():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    activity_name = data.get('activityName')
    time_elapsed = data.get('timeElapsed')

    if not activity_name or time_elapsed is None:
        return jsonify({"error": "Datos incompletos"}), 400

    # Crear un nuevo registro en la tabla Activities
    cronometro_entry = CronometroModel(
        user_id=session['user_id'],
        activity_name=activity_name,
        duration=time_elapsed  # Usar "duration" en lugar de "time_elapsed"
    )
    db.session.add(cronometro_entry)
    db.session.commit()

    return jsonify({"message": "Tiempo guardado correctamente"}), 200


@app.route('/generate_report', methods=['GET'])
def generate_report():
    print("Generando reporte...")
    report_date = request.args.get('date')  # Obtener la fecha desde el query string
    if not report_date:
        print("Fecha no proporcionada")
        return "Fecha no proporcionada", 400

    # Convertir la fecha al formato adecuado
    try:
        report_date = datetime.strptime(report_date, "%Y-%m-%d").date()
    except ValueError:
        print("Fecha en formato incorrecto")
        return "Fecha en formato incorrecto", 400

    # Obtener el ID del usuario logueado
    user_id = session.get('user_id')
    print(f"User ID: {user_id}")  # Verificar que el usuario está logueado
    if not user_id:
        print("Usuario no autenticado")
        return "Usuario no autenticado", 403

    # Obtener el correo del usuario logueado
    user = UserModel.query.get(user_id)  # Asumiendo que UserModel es el modelo del usuario
    if not user:
        print("Usuario no encontrado")
        return "Usuario no encontrado", 404

    email = user.Email  # Extraemos el correo del usuario

    # Obtener las actividades del usuario logueado en esa fecha
    activities = CronometroModel.query.filter(
        cast(CronometroModel.ActivityDate, Date) == report_date,
        CronometroModel.UserID == user_id
    ).all()

    if not activities:
        print("No hay actividades para la fecha seleccionada")
        return "No hay actividades para la fecha seleccionada", 404

    # Crear el PDF en memoria
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setFont("Helvetica", 12)

    # Agregar el título con el correo del usuario
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, 730, f"Reporte de Actividades del Usuario: {email}")
    pdf.setFont("Helvetica", 12)

    # Agregar el título del reporte con la fecha
    pdf.drawString(50, 710, f"Fecha del reporte: {report_date}")

    # Espacio para la tabla (justo debajo del título)
    y_position = 660

    # Dibujar los encabezados de la tabla
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(80, y_position, "Actividad")
    pdf.drawString(200, y_position, "Duración (segundos)")
    pdf.drawString(380, y_position, "Fecha")

    # Dibujar líneas horizontales (para los encabezados)
    pdf.line(50, y_position - 5, 550, y_position - 5)  # Línea superior de la tabla
    y_position -= 20  # Decrecer la posición para las filas

    # Dibujar cada fila de la tabla
    pdf.setFont("Helvetica", 10)
    for activity in activities:
        formatted_date = activity.ActivityDate.strftime('%Y-%m-%d %H:%M:%S')

        # Dibujar los valores de la fila
        pdf.drawString(50, y_position, f"{activity.ActivityName}")
        pdf.drawString(250, y_position, f"{activity.Duration}")
        pdf.drawString(350, y_position, f"{formatted_date}")

        # Dibujar líneas horizontales (para cada fila)
        pdf.line(50, y_position - 5, 550, y_position - 5)  # Línea inferior de la fila

        # Decrecer la posición para la siguiente fila
        y_position -= 20  # Espacio entre filas

        # Comprobar si la posición excede el límite de la página
        if y_position < 100:
            pdf.showPage()
            pdf.setFont("Helvetica", 12)
            y_position = 750  # Reiniciar la posición vertical para una nueva página

    # Finalizar el PDF
    pdf.showPage()
    pdf.save()

    # Enviar el PDF como respuesta
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"reporte_{report_date}.pdf", mimetype="application/pdf")


# Flask buscará el archivo 'index.html' en la carpeta 'templates'

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Eliminar datos de la sesión
    return redirect(url_for('home'))  # Redirigir a la página de inicio

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Crear las tablas si no existen
    app.run(debug=True)

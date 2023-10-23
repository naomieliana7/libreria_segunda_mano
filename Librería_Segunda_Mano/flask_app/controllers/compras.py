from flask import flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from flask_app.models.usuarios import Usuario
from flask_app.models.libros import Libro
from flask_app import app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def enviar_correo_compra(libro, current_user):
    
    smtp_server = 'smtp.example.com'
    smtp_port = 587
    smtp_user = current_user.email
    smtp_password = Usuario.get(session['contraseña'])

    
    mensaje = MIMEMultipart()
    mensaje['From'] = smtp_user
    mensaje['To'] = libro.usuario
    mensaje['Subject'] = 'Confirmación de Compra - ' + libro.título

    
    cuerpo_mensaje = f'Has comprado el libro "{libro.título}" por ${libro.precio}. Gracias por tu compra.'
    mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  
        server.login(smtp_user, smtp_password)

        
        server.sendmail(smtp_user, current_user.email, mensaje.as_string())

        
        server.quit()

        print('Correo de confirmación de compra enviado con éxito')
    except Exception as e:
        print('Error al enviar el correo:', str(e))


@app.route('/comprar/<int:id>', methods=['POST'])
def comprar_libro(id):
    libro = Libro.obtener_libro(id)
    print('TTTTTTTTT')
    if libro:
        enviar_correo_compra(libro, current_user)

        flash('Has comprado el libro. El vendedor recibirá un correo con tus detalles de contacto.', 'success')
        return redirect('/inicio') 
    else:
        flash('Libro no encontrado', 'error')
        return redirect('/inicio') 








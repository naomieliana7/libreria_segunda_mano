import os
from flask import flash, redirect, request, session, render_template, send_file
from flask_app.models.libros import Libro
from flask_app.models.usuarios import Usuario
from werkzeug.utils import send_from_directory, secure_filename
from flask_app import app


@app.route('/procesar_libro', methods=["POST"])
def procesar_libro():
    print(request.form)

    errores = Libro.validar_libro(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/inicio")

    portada = request.files["portada"]
    if portada.filename == '':
        flash("Debes seleccionar un archivo de imagen para la portada", "error")
        return redirect("/inicio")

    if not Libro.archivo_permitido(portada.filename):
        flash("El archivo de imagen de la portada no es válido. Deben ser archivos de imagen (por ejemplo, JPG, PNG).", "error")
        return redirect("/inicio")
    
    # Genera un nombre de archivo único para la imagen 
    nombre_archivo = secure_filename(portada.filename)

    # Guarda la imagen en el directorio /static/portada
    ruta_guardado = os.path.join(r'C:\Users\user\Desktop\Librería_Segunda_Mano\flask_app\static\portada', nombre_archivo)
    portada.save(ruta_guardado)
    
    data = {
        'título': request.form["título"],
        'autor': request.form["autor"],
        'categoría': request.form["categoría"],
        'precio': request.form["precio"],
        'descripción': request.form["descripción"],
        'portada': nombre_archivo,  # Aquí asignamos el archivo de la portada
        'usuario_id': session['usuario_id']
    }
    print(data)
    id = Libro.guardar_libro(data)
    print(id)
    flash("Libro añadido", "success")

    return redirect("/inicio")

@app.route('/uploads/<filename>')
def uploaded(filename):
    uploads_dir = app.config['UPLOADED_PHOTOS_DEST']
    return send_from_directory(uploads_dir, filename)


@app.route("/nuevo/<int:id>")
def nuevo(id):
    if not session.get('usuario_id'):
        flash("No estás logeado!!!!", "error")
        return redirect("/login")

    user_in_session = Usuario.get(session['usuario_id'])
    
    return render_template('nuevo_libro.html', user_in_session=user_in_session, id=id)

@app.route('/mis_libros/<id>')
def mis_libros(id):
    print('HHHHHHHH')
    user_in_session= Libro.obtener_usuario_con_libros(session['usuario_id'])
    return render_template('mis_libros.html', user_in_session=user_in_session)


@app.route('/editar/<id>')
def editar(id):
    user_in_session = Usuario.get(session['usuario_id'])
    libro = Libro.obtener_libro(id)
    return render_template('editar_libro.html', libro=libro, user_in_session=user_in_session)

@app.route('/procesar_libro_editar/<id>', methods=["POST"])
def procesar_libro_editar(id):
    print(request.form)

    errores = Libro.validar_libro(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/inicio")
    libro = Libro.obtener_libro(id)
    
    libro.título = request.form['título']
    libro.autor = request.form['autor']
    libro.categoría = request.form['categoría']
    libro.precio = request.form['precio']
    libro.descripción = request.form['descripción']
    libro.portada = request.files['portada']

    libro.actualizar_libro()
    
    flash( "Libro editado", "success")

    return redirect("/inicio")

@app.route('/eliminar/<id>')
def eliminar(id):
    Libro.eliminar_libro(id)
    return redirect('/inicio')

@app.route('/mostrar_imagen/<nombre_imagen>')
def mostrar_imagen(nombre_imagen):
    try:
        # Obtiene la ruta completa de la imagen
        ruta_imagen = 'static/portada/' + nombre_imagen

        # Usa send_file para enviar la imagen como respuesta HTTP
        return send_file(ruta_imagen, as_attachment=False)
    except FileNotFoundError:
        # Si la imagen no se encuentra, puedes manejar el error aquí
        return 'Imagen no encontrada', 404

@app.route('/comprar/<int:id>')
def comprar(id):
    libro = Libro.obtener_libro(id)

    if libro:
        usuario = Usuario.get(libro.usuario_id)

        return render_template('datos_compra.html', libro=libro, usuario=usuario)
    else:
        return "Libro no encontrado", 404
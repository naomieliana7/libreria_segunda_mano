from flask import render_template, flash, redirect, session
from flask_app import app
from flask_app.models.usuarios import Usuario
from flask_app.models.libros import Libro



@app.route('/')
def portada():
    return render_template('portada.html')

@app.route('/inicio')
def inicio():
    
    if not session.get('usuario_id'):
        flash("No estás logeado!!!!", "error")
        return redirect("/login")

    user_in_session = Usuario.get(session['usuario_id'])
    
    return render_template(
        'inicio.html',
        libros=Libro.obtener_todos_libros(),
        usuario=user_in_session,
        user_in_session=user_in_session  # También pasamos user_in_session al contexto
    )
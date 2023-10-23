from flask import flash, redirect, render_template, request, session

from flask_app import app
from flask_app.models.usuarios import Usuario
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)  

@app.route('/login')
def login():

    if 'usuario' in session:
        flash("ya estás LOGEADO!!!! eres " + session['usuario']['correo'], "info")
        return redirect("/inicio")

    return render_template("login.html")

@app.route('/procesar_login', methods=["POST"])
def procesar_login():
    print(request.form)

    usuario  = Usuario.get_by_email(request.form['correo'])
    if not usuario:
        flash("el correo o la contraseña no es válido", "error")
        return redirect("/login")
    
    resultado = bcrypt.check_password_hash(usuario.contraseña, request.form['contraseña'])
    
    if resultado:
        session['usuario_id']=usuario.id
        return redirect("/inicio")

    flash("la contraseña o el correo no es válido", "error")
    return redirect("/login")

@app.route('/registro')
def registro():
    return render_template("registro.html")

@app.route('/procesar_registro', methods=["POST"])
def procesar_registro():
    print(request.form)

    errores = Usuario.validar(request.form)
    if len(errores) > 0:
        for error in errores:
            flash(error, "error")
        return redirect("/login")
    
    if request.form["contraseña"] != request.form["confirmar_contraseña"]:
        flash("las contraseñas no son iguales", "error")
        return redirect("/login")

    data = {
    'nombre': request.form["nombre"],
    'apellido': request.form["apellido"],
    'correo': request.form["correo"],
    'contraseña': bcrypt.generate_password_hash(request.form["contraseña"])
}

    id = Usuario.save(data)

    flash("Usuario registrado correctamente", "success")
    return redirect("/login")



@app.route('/salir')
def salir():
    session.clear()
    return redirect("/")
import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.utils.expresiones_regulares import EMAIL_REGEX


class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo = data['correo']
        self.contraseña = data['contraseña']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.libros = []

    def __str__(self) -> str:
        return f"{self.correo} ({self.id})"

    @classmethod
    def validar(cls, formulario):

        errores = []
        if 'correo' not in formulario or not  EMAIL_REGEX.match(formulario['correo']):
            errores.append(
                "El correo indicado es inválido"
            )

        if cls.get_by_email(formulario['correo']):
            errores.append(
                "El correo ya existe"
            )
        if len(formulario['nombre']) < 2:
            errores.append(
                "Nombre debe tener al menos 2 caracteres"
            )

        if len(formulario['apellido']) < 2:
            errores.append(
                "Apellido debe tener al menos 2 caracteres"
            )

        
        if len(formulario['contraseña']) < 8:
            errores.append(
                "Password debe tener al menos 8 caracteres"
            )

        for llave, valor in formulario.items():
            if len(valor) == 0:
                errores.append(
                    f"{llave} no está presente. Dato obligatorio"
                )
        return errores

    @classmethod
    def get_all(cls):
        resultados_instancias = []
        query = "SELECT * FROM usuarios"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)

        return resultados_instancias

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO usuarios (nombre, apellido, correo, contraseña, created_at, updated_at) VALUES (%(nombre)s,%(apellido)s,%(correo)s, %(contraseña)s, NOW(), NOW());"
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
    
    @classmethod
    def get(cls, id ):
        query = "SELECT * FROM usuarios WHERE id = %(id)s;"
        data = { 'id': id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    @classmethod
    def get_by_email(cls, correo ):
        query = "SELECT * FROM usuarios WHERE correo = %(correo)s;"
        data = { 'correo': correo }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        
        return None
    
    
    @classmethod
    def eliminar(cls, id ):
        query = "DELETE FROM usuarios WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
    def update(self):
        query = "UPDATE usuarios SET contraseña = %(contraseña)s, updated_at = NOW() WHERE id = %(id)s"
        data = {
            'id': self.id,
            'contraseña': self.contraseña
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

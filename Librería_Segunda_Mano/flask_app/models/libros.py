import os

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.usuarios import Usuario

from flask_app import app

class Libro: 
    def __init__(self, data) -> None:
        self.id = data['id']
        self.título = data['título']
        self.autor = data['autor']
        self.categoría = data['categoría']
        self.precio = data['precio']
        self.descripción = data['descripción']
        self.portada = data['portada']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.usuario_id = data['usuario_id']
        self.usuario = Usuario.get(data['usuario_id'])

    def json(self):
        return {
            "id": self.id,
            "título": self.título,
            "autor": self.autor,
            "categoría": self.categoría,
            "precio": self.precio,
            "descripción": self.descripción,
            "portada": self.portada,
            "usuario_id": self.usuario_id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "usuario": str(self.usuario),
        }

    @classmethod
    def validar_libro(cls, formulario):
        errores = []

        if len(formulario['título']) < 1:
            errores.append("Título del libro debe tener al menos un caracter")

        if len(formulario['autor']) < 3:
            errores.append("Autor debe tener al menos tres caracteres")

        
        for llave, valor in formulario.items():
            if len(valor) == 0:
                errores.append(f"{llave} no está presente. Dato obligatorio")
        return errores
    
    @classmethod
    def archivo_permitido(cls, filename):
        extensiones_permitidas = {'jpg', 'jpeg', 'png', 'gif'}  
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in extensiones_permitidas


    @classmethod
    def obtener_todos_libros(cls):
        resultados_instancias = []
        query = "SELECT * FROM libros"
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db(query)
        print(resultados)
        for resultado in resultados:
            instancia = cls(resultado)
            resultados_instancias.append(instancia)
        print(resultados_instancias)
        return resultados_instancias
    
    @classmethod
    def guardar_libro(cls, data):
        query = "INSERT INTO libros (título, autor, categoría, precio, descripción, portada, created_at, updated_at, usuario_id) VALUES (%(título)s, %(autor)s, %(categoría)s, %(precio)s, %(descripción)s, %(portada)s, NOW(), NOW(), %(usuario_id)s);"
    
        return connectToMySQL(os.getenv('BASE_DATOS')).query_db(query, data)


    
    @classmethod
    def obtener_libro(cls, libro_id ):
        query = "SELECT * FROM libros WHERE id = %(id)s;"
        data = { 'id': libro_id }
        resultados = connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        if resultados:
            return cls(resultados[0])
        return None
    
    @classmethod
    def eliminar_libro(cls, id ):
        query = "DELETE FROM libros WHERE id = %(id)s;"
        data = { 'id': id }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True
    
    
    def actualizar_libro(self):
        query = "UPDATE libros SET título=%(título)s,autor=%(autor)s,categoría=%(categoría)s,precio=%(precio)s,descripción=%(descripción)s,portada=%(portada)s,updated_at=NOW() WHERE id = %(id)s;"
        data = {
            'id': self.id,
            'título': self.título,
            'autor': self.autor,
            'categoría': self.categoría,
            'precio': self.precio,
            'descripción': self.descripción,
            'portada': self.portada,
        }
        connectToMySQL(os.getenv('BASE_DATOS')).query_db( query, data )
        return True

    @classmethod
    def obtener_usuario_con_libros(cls, usuario_id):
        query = "SELECT * FROM usuarios LEFT JOIN libros ON libros.usuario_id = usuarios.id WHERE usuarios.id = %(id)s;"
        data = {"id" : usuario_id}
        results = connectToMySQL(os.getenv("BASE_DATOS")).query_db(query,data)
        print("RESULTADOS",results)
        if results:
            usuario = Usuario(results[0])
            for row in results:
                        dato_libro = {
                            "id" : row["libros.id"],
                            "título" : row["título"],
                            "autor" : row["autor"],
                            "categoría" : row["categoría"],
                            "precio" : row["precio"],
                            "descripción" : row["descripción"],
                            "portada" : row["portada"],
                            "usuario_id" : row["usuario_id"],
                            "created_at" : row["created_at"],
                            "updated_at" : row["updated_at"],
                        }

                        usuario.libros.append(Libro(dato_libro))
            
            
            return usuario
        return None

    @app.context_processor
    def inject_libro():
        def mostrar_imagen(nombre_imagen):
            # Construye la URL para mostrar la imagen
            return f'/mostrar_imagen/{nombre_imagen}'
    
        return dict(Libro=Libro, mostrar_imagen=mostrar_imagen)
            

    
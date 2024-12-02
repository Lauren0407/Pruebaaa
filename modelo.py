import mysql.connector

class Modelo:
    def __init__(self):
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="tu_base_de_datos"
        )
        self.cursor = self.conexion.cursor()

    def verificar_usuario(self, usuario, contrasena):
        query = "SELECT nombre_usuario, contrasena, rol FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s"
        self.cursor.execute(query, (usuario, contrasena))
        return self.cursor.fetchone()

    def agregar_paciente(self, cedula, nombre, archivo_dcm):
        query = "INSERT INTO pacientes (cedula, nombre, archivo_dcm) VALUES (%s, %s, %s)"
        with open(archivo_dcm, 'rb') as file:
            blob = file.read()
        self.cursor.execute(query, (cedula, nombre, blob))
        self.conexion.commit()

    def buscar_paciente(self, cedula):
        query = "SELECT cedula, nombre, archivo_dcm FROM pacientes WHERE cedula = %s"
        self.cursor.execute(query, (cedula,))
        return self.cursor.fetchone()

    def editar_paciente(self, cedula, nombre, archivo_dcm):
        query = "UPDATE pacientes SET nombre = %s, archivo_dcm = %s WHERE cedula = %s"
        with open(archivo_dcm, 'rb') as file:
            blob = file.read()
        self.cursor.execute(query, (nombre, blob, cedula))
        self.conexion.commit()

    def eliminar_paciente(self, cedula):
        query = "DELETE FROM pacientes WHERE cedula = %s"
        self.cursor.execute(query, (cedula,))
        self.conexion.commit()

import os
from modelo import Modelo
from vista import Vista

class Controlador:
    def __init__(self):
        self.modelo = Modelo()
        self.vista = Vista()
        self.usuario_actual = None
        self.rol_actual = None

    def login(self):
        usuario, contrasena = self.vista.obtener_credenciales()
        usuario_data = self.modelo.verificar_usuario(usuario, contrasena)
        if usuario_data:
            self.usuario_actual = usuario_data[0]
            self.rol_actual = usuario_data[2]
            self.vista.mostrar_mensaje(f"Bienvenido, {self.usuario_actual} (Rol: {self.rol_actual})")
            self.menu_principal()
        else:
            self.vista.mostrar_mensaje("Credenciales incorrectas.")

    def menu_principal(self):
        if self.rol_actual == "medico":
            self.menu_medico()
        elif self.rol_actual == "paciente":
            self.menu_paciente()
        elif self.rol_actual == "estudiante":
            self.menu_estudiante()
        else:
            self.vista.mostrar_mensaje("Rol desconocido.")

    def menu_medico(self):
        while True:
            opcion = input("1. Agregar Paciente\n2. Buscar Paciente\n3. Salir\nSeleccione: ")
            if opcion == "1":
                self.agregar_paciente()
            elif opcion == "2":
                self.buscar_paciente()
            elif opcion == "3":
                break
            else:
                self.vista.mostrar_mensaje("Opción no válida.")

    def menu_paciente(self):
        self.vista.mostrar_mensaje("Acceso restringido. Solo puedes ver tu información.")
        self.buscar_paciente(autolimitado=True)

    def menu_estudiante(self):
        while True:
            opcion = input("1. Buscar Paciente\n2. Salir\nSeleccione: ")
            if opcion == "1":
                self.buscar_paciente(autolimitado=True)
            elif opcion == "2":
                break
            else:
                self.vista.mostrar_mensaje("Opción no válida.")

    def agregar_paciente(self):
        cedula, nombre, archivo_dcm = self.vista.obtener_datos_paciente()
        if os.path.exists(archivo_dcm):
            self.modelo.agregar_paciente(cedula, nombre, archivo_dcm)
            self.vista.mostrar_mensaje("Paciente agregado exitosamente.")
        else:
            self.vista.mostrar_mensaje("Archivo no encontrado.")

    def buscar_paciente(self, autolimitado=False):
        cedula = self.usuario_actual if autolimitado else input("Ingrese la cédula del paciente: ")
        paciente = self.modelo.buscar_paciente(cedula)
        if paciente:
            self.vista.mostrar_paciente(paciente)
            archivo_path = f"temp_{cedula}.dcm"
            with open(archivo_path, 'wb') as file:
                file.write(paciente[2])
            self.vista.mostrar_mensaje(f"Archivo descargado en: {archivo_path}")

            if self.rol_actual == "medico":
                opcion = input("1. Editar\n2. Eliminar\n3. Regresar\nSeleccione: ")
                if opcion == "1":
                    self.editar_paciente(cedula)
                elif opcion == "2":
                    self.eliminar_paciente(cedula)
                    os.remove(archivo_path)
        else:
            self.vista.mostrar_mensaje("Paciente no encontrado.")

    def editar_paciente(self, cedula):
        nombre = input("Nuevo nombre: ")
        archivo_dcm = input("Nueva ruta del archivo .dcm: ")
        self.modelo.editar_paciente(cedula, nombre, archivo_dcm)
        self.vista.mostrar_mensaje("Paciente editado exitosamente.")

    def eliminar_paciente(self, cedula):
        self.modelo.eliminar_paciente(cedula)
        self.vista.mostrar_mensaje("Paciente eliminado exitosamente.")

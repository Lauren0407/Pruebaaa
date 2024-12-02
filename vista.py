class Vista:
    def mostrar_mensaje(self, mensaje):
        print(f"[INFO] {mensaje}")

    def obtener_credenciales(self):
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")
        return usuario, contrasena

    def obtener_datos_paciente(self):
        cedula = input("Cédula del paciente: ")
        nombre = input("Nombre del paciente: ")
        archivo_dcm = input("Ruta del archivo .dcm: ")
        return cedula, nombre, archivo_dcm

    def mostrar_paciente(self, paciente):
        print(f"Cédula: {paciente[0]}")
        print(f"Nombre: {paciente[1]}")
        print(f"Archivo DCM: {paciente[2][:20]}... (contenido binario truncado)")

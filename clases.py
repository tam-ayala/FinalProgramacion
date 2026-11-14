from datetime import datetime

class Colaborador:
    def __init__(self, legajo: int, nombre: str, apellido: str, dni: int, usuario: str,
                 contrasena: str, jerarquia: str, fecha_ingreso: str, francos: str, area: str, email: str):
        self.legajo = legajo
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.usuario = usuario
        self.contrasena = contrasena
        self.jerarquia = jerarquia
        self.fecha_ingreso = fecha_ingreso
        self.estado = True
        self.historial_licencias = []
        self.francos = francos
        self.area = area
        self.email = email

    def login(self, usr: str, pwd: str) -> bool:
        return self.usuario == usr and self.contrasena == pwd

class Supervisor(Colaborador):
    def __init__(self, legajo: int, nombre: str, apellido: str, dni: int, usuario: str,
                 contrasena: str, jerarquia: str, fecha_ingreso: str, francos: str, area: str, email: str):
        super().__init__(legajo, nombre, apellido, dni, usuario, contrasena, jerarquia, fecha_ingreso, francos, area, email)

    def validar_intercambio(self, licencia_id: int) -> bool:
        return True

class AdministradorRRHH(Colaborador):
    def __init__(self, legajo: int, nombre: str, apellido: str, dni: int, usuario: str,
                 contrasena: str, jerarquia: str, fecha_ingreso: str, francos: str, area: str, email: str):
        super().__init__(legajo, nombre, apellido, dni, usuario, contrasena, jerarquia, fecha_ingreso, francos, area, email)

    def confirmar_licencia(self, licencia) -> bool:
        if licencia.estado == "aprobada":
            licencia.estado = "confirmada"
            return True
        return False

class Licencia:
    def __init__(self, id_licencia: int, fecha_inicio: str, fecha_fin: str, tipo: str,
                 nivel_preferencia: int = 3, legajo_empleado: int = None):
        self.id_licencia = id_licencia
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo = tipo
        self.estado = "pendiente"  # pendiente, aprobada, confirmada
        self.nivel_preferencia = nivel_preferencia
        self.legajo_empleado = legajo_empleado

    def __repr__(self):
        return f"Licencia(ID={self.id_licencia}, Inicio='{self.fecha_inicio}', Prioridad={self.nivel_preferencia}, Estado='{self.estado}')"
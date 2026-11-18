from datetime import date

class Colaborador:
    def __init__(
        self,
        id_legajo: int,
        nombre: str,
        apellido: str,
        dni: int,
        usuario: str,
        contrasena: str,
        fecha_ingreso: date,
        area: str,
        email_corporativo: str,
        francos: str = "Sábado y Domingo",# En el proyecto todos los colaboradores tienen francos Sábado y Domingo
        tiene_hijos: bool = False,
        esta_casado: bool = False,
        nivel_jerarquia: int = 1,
    ):
        self.id_legajo = id_legajo
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.usuario = usuario
        self.contrasena = contrasena
        self.nivel_jerarquia = nivel_jerarquia
        self.fecha_ingreso = fecha_ingreso
        self.estado = True 
        self.historial_licencias: list["Licencia"] = []
        self.francos = francos
        self.area = area
        self.email_corporativo = email_corporativo

        # Regla de prioridad: 0 por defecto, 1 si tiene hijos, 3 si está casado
        self.tiene_hijos = tiene_hijos
        self.esta_casado = esta_casado
        self.nivel_prioridad = self.calcular_prioridad()

    def calcular_prioridad(self) -> int:
        if self.esta_casado:
            self.nivel_prioridad = 3
        elif self.tiene_hijos:
            self.nivel_prioridad = 1
        else:
            self.nivel_prioridad = 0
        return self.nivel_prioridad

    def login(self, usuario: str, contrasena: str) -> bool:
        if not self.estado:
            return False
        return self.usuario == usuario and self.contrasena == contrasena

    def solicitar_licencia(self, licencia: "Licencia") -> None:
        self.historial_licencias.append(licencia)

    def firmar_vacaciones(self, licencia: "Licencia") -> bool:
        # CU N6: Cambia estado de asignada a aprobada
        if licencia in self.historial_licencias and licencia.estado == "asignada":
            licencia.estado = "aprobada"
            return True
        return False

    def __repr__(self) -> str:
        return (
            f"[{self.id_legajo}] {self.nombre} {self.apellido} | "
            f"Área: {self.area} | Jerarquía: {self.nivel_jerarquia} | "
            f"Prioridad: {self.nivel_prioridad}"
        )


class Supervisor(Colaborador):
    def __init__(self, *args, **kwargs):
        kwargs["nivel_jerarquia"] = 2
        super().__init__(*args, **kwargs)

    def gestionar_licencia(self, licencia: "Licencia", aprobar: bool) -> bool:
        # Restricción: solo sobre licencias pendientes
        if licencia.estado == "pendiente" and licencia.nivel_preferencia is not None:
            licencia.estado = "aprobada" if aprobar else "rechazada"
            return True
        return False


class AdministradorRRHH(Colaborador):
    def __init__(self, *args, **kwargs):
        kwargs["nivel_jerarquia"] = 3
        super().__init__(*args, **kwargs)

    def confirmar_licencia(self, licencia: "Licencia", confirmar: bool = True) -> bool:
        # Restricción: solo sobre licencias aprobadas y de otro legajo
        if (
            licencia.estado == "aprobada"
            and licencia.colaborador_legajo != self.id_legajo
        ):
            licencia.estado = "confirmada" if confirmar else "rechazada"
            return True
        return False


class Licencia:
    def __init__(
        self,
        id_licencia: int,
        colaborador_legajo: int,
        fecha_inicio: date,
        fecha_fin: date,
        tipo: str = "vacaciones",
        estado: str = "pendiente",
        nivel_preferencia: int | None = None,  # None hasta que cada empleado rankee (1 a 3)
    ):
        self.id_licencia = id_licencia
        self.colaborador_legajo = colaborador_legajo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo = tipo
        self.estado = estado
        self.nivel_preferencia = nivel_preferencia 

    def validar_periodo(self) -> bool:
        return self.fecha_fin >= self.fecha_inicio

    def __repr__(self) -> str:
        pref_texto = (
            self.nivel_preferencia
            if self.nivel_preferencia is not None
            else "Sin asignar"
        )
        return (
            f"Licencia #{self.id_licencia} (Legajo {self.colaborador_legajo}) | "
            f"{self.fecha_inicio} al {self.fecha_fin} | "
            f"Preferencia: {pref_texto} | Estado: {self.estado}"
        )

class CalendarioCorporativo:
    def __init__(self, id_calendario: int, area_asociada: str, dias_disponibles: int):
        self.id_calendario = id_calendario
        self.area_asociada = area_asociada
        self.dias_disponibles = dias_disponibles
        self.licencias_agregadas: list[Licencia] = []

    def agregar_vacaciones(self, licencia: Licencia) -> bool:
        dias = (licencia.fecha_fin - licencia.fecha_inicio).days + 1
        if licencia.estado == "confirmada" and self.dias_disponibles >= dias:
            self.licencias_agregadas.append(licencia)
            self.dias_disponibles -= dias
            return True
        return False
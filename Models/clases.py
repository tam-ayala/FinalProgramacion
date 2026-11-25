from datetime import date


# ==========================================================
# CLASE COLABORADOR
# ==========================================================

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
        francos: str = "Sábado y Domingo",
        tiene_hijos: bool = False,
        esta_casado: bool = False,
        nivel_jerarquia: int = 1,
    ):
        # Datos personales y laborales
        self.id_legajo = id_legajo
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni

        # Credenciales de acceso
        self.usuario = usuario
        self.contrasena = contrasena

        # Información laboral
        self.fecha_ingreso = fecha_ingreso
        self.area = area
        self.email_corporativo = email_corporativo
        self.francos = francos

        # Jerarquía dentro de la empresa
        self.nivel_jerarquia = nivel_jerarquia

        # True significa que el usuario está habilitado
        self.estado = True

        # Historial de licencias del colaborador
        self.historial_licencias: list["Licencia"] = []

        # Información familiar
        self.tiene_hijos = tiene_hijos
        self.esta_casado = esta_casado

        # Calculamos automáticamente la prioridad familiar
        self.nivel_prioridad = self.calcular_prioridad()

    def calcular_prioridad(self) -> int:
        """
        Determina la prioridad familiar del colaborador.

        Casado: 3
        Tiene hijos: 1
        Sin hijos y soltero: 0
        """

        if self.esta_casado:
            return 3

        if self.tiene_hijos:
            return 1

        return 0

    def login(self, usuario: str, contrasena: str) -> bool:
        """Comprueba que el usuario esté activo y las credenciales sean correctas."""

        return (
            self.estado
            and self.usuario == usuario
            and self.contrasena == contrasena
        )

    def solicitar_licencia(self, licencia: "Licencia") -> None:
        """Agrega una licencia al historial del colaborador."""

        if licencia.colaborador_legajo != self.id_legajo:
            raise ValueError("La licencia no pertenece a este colaborador.")

        if any(
            licencia_existente.id_licencia == licencia.id_licencia
            for licencia_existente in self.historial_licencias
        ):
            raise ValueError("La licencia ya está registrada.")

        self.historial_licencias.append(licencia)

    def firmar_vacaciones(self, licencia: "Licencia") -> bool:
        """
        El colaborador firma una licencia previamente asignada.

        El estado cambia de asignada a aprobada.
        """

        if (
            licencia in self.historial_licencias
            and licencia.estado == "asignada"
        ):
            licencia.estado = "aprobada"
            return True

        return False

    def __repr__(self) -> str:
        return (
            f"[{self.id_legajo}] {self.nombre} {self.apellido} | "
            f"Área: {self.area} | "
            f"Jerarquía: {self.nivel_jerarquia} | "
            f"Prioridad familiar: {self.nivel_prioridad}"
        )


# ==========================================================
# CLASE SUPERVISOR
# ==========================================================

class Supervisor(Colaborador):

    def __init__(self, *args, **kwargs):
        # Todo supervisor tiene jerarquía 2
        kwargs["nivel_jerarquia"] = 2
        super().__init__(*args, **kwargs)

    def gestionar_licencia(self, licencia: "Licencia", aprobar: bool) -> bool:
        """
        El supervisor revisa una licencia pendiente y rankeada.

        Si aprueba, la licencia pasa a asignada.
        Si rechaza, pasa a rechazada.
        """

        if (
            licencia.estado == "pendiente"
            and licencia.nivel_preferencia is not None
        ):
            licencia.estado = "asignada" if aprobar else "rechazada"
            return True

        return False


# ==========================================================
# CLASE ADMINISTRADOR DE RRHH
# ==========================================================

class AdministradorRRHH(Colaborador):

    def __init__(self, *args, **kwargs):
        # Todo administrador tiene jerarquía 3
        kwargs["nivel_jerarquia"] = 3
        super().__init__(*args, **kwargs)

    def confirmar_licencia(
        self,
        licencia: "Licencia",
        confirmar: bool = True
    ) -> bool:
        """
        RRHH confirma o rechaza una licencia firmada.

        Solo puede gestionar licencias aprobadas
        que pertenezcan a otro legajo.
        """

        if (
            licencia.estado == "aprobada"
            and licencia.colaborador_legajo != self.id_legajo
        ):
            licencia.estado = "confirmada" if confirmar else "rechazada"
            return True

        return False


# ==========================================================
# CLASE LICENCIA
# ==========================================================

class Licencia:

    ESTADOS_VALIDOS = {
        "pendiente",
        "asignada",
        "aprobada",
        "confirmada",
        "rechazada",
    }

    def __init__(
        self,
        id_licencia: int,
        colaborador_legajo: int,
        fecha_inicio: date,
        fecha_fin: date,
        tipo: str = "vacaciones",
        estado: str = "pendiente",
        nivel_preferencia: int | None = None,
    ):

        self.id_licencia = id_licencia
        self.colaborador_legajo = colaborador_legajo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.tipo = tipo

        # Comprobamos que el estado sea válido
        if estado not in self.ESTADOS_VALIDOS:
            raise ValueError("Estado de licencia no válido.")

        self.estado = estado

        # La preferencia debe estar entre 1 y 3
        if nivel_preferencia is not None and nivel_preferencia not in (1, 2, 3):
            raise ValueError("La preferencia debe ser 1, 2 o 3.")

        self.nivel_preferencia = nivel_preferencia

    def validar_periodo(self) -> bool:
        """Comprueba que la fecha final no sea anterior a la inicial."""

        return self.fecha_fin >= self.fecha_inicio

    def calcular_dias(self) -> int:
        """Calcula la cantidad de días calendario de la licencia."""

        if not self.validar_periodo():
            raise ValueError("El período de la licencia no es válido.")

        return (self.fecha_fin - self.fecha_inicio).days + 1

    def __repr__(self) -> str:

        preferencia = (
            self.nivel_preferencia
            if self.nivel_preferencia is not None
            else "Sin asignar"
        )

        return (
            f"Licencia #{self.id_licencia} | "
            f"Legajo: {self.colaborador_legajo} | "
            f"Desde: {self.fecha_inicio} | "
            f"Hasta: {self.fecha_fin} | "
            f"Preferencia: {preferencia} | "
            f"Estado: {self.estado}"
        )


# ==========================================================
# CLASE CALENDARIO CORPORATIVO
# ==========================================================

class CalendarioCorporativo:

    def __init__(
        self,
        id_calendario: int,
        area_asociada: str,
        dias_disponibles: int
    ):

        if dias_disponibles < 0:
            raise ValueError("Los días disponibles no pueden ser negativos.")

        self.id_calendario = id_calendario
        self.area_asociada = area_asociada
        self.dias_disponibles = dias_disponibles

        # Licencias confirmadas incorporadas al calendario
        self.licencias_agregadas: list[Licencia] = []

    def agregar_vacaciones(self, licencia: Licencia) -> bool:
        """
        Incorpora una licencia confirmada al calendario.

        Controla:
        - Estado de la licencia.
        - Validez del período.
        - Que no esté agregada previamente.
        - Disponibilidad de días.
        """

        if licencia.estado != "confirmada":
            return False

        if not licencia.validar_periodo():
            return False

        if any(
            licencia_existente.id_licencia == licencia.id_licencia
            for licencia_existente in self.licencias_agregadas
        ):
            return False

        cantidad_dias = licencia.calcular_dias()

        if self.dias_disponibles < cantidad_dias:
            return False

        self.licencias_agregadas.append(licencia)
        self.dias_disponibles -= cantidad_dias

        return True

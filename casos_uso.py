from clases import Colaborador, Licencia, AdministradorRRHH
from algoritmo_ordenamiento import ordenar_licencias_por_prioridad

class SistemaGestionVacaciones:
    def __init__(self):
        self.usuarios = {}
        self.licencias = {}
        self._inicializar_datos()

    def _inicializar_datos(self):
        # Admin inicial
        admin = AdministradorRRHH(100, "Admin", "RRHH", 11111111, "admin", "admin123",
                                  "Admin", "2020-01-01", "Sab-Dom", "RRHH", "admin@apex.com")
        self.usuarios[admin.usuario] = admin

    # CU ID N1: Login
    def login(self, usuario: str, contrasena: str):
        colaborador = self.usuarios.get(usuario)
        if colaborador and colaborador.login(usuario, contrasena):
            return colaborador
        return None

    # CU ID N10: Alta de colaborador
    def alta_colaborador(self, admin: AdministradorRRHH, colaborador: Colaborador) -> bool:
        if isinstance(admin, AdministradorRRHH) and colaborador.usuario not in self.usuarios:
            self.usuarios[colaborador.usuario] = colaborador
            return True
        return False

    # CU ID N4: Rankeo de fechas (Ordenamiento aplicado)
    def rankear_licencias(self, licencias_candidatas: list) -> list:
        return ordenar_licencias_por_prioridad(licencias_candidatas)

    # CU ID N6: Firma de licencia
    def firmar_licencia(self, licencia: Licencia) -> bool:
        if licencia.estado in ["pendiente", "asignada"]:
            licencia.estado = "aprobada"
            return True
        return False
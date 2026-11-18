from datetime import date
from Models.clases import Colaborador, Supervisor, AdministradorRRHH, CalendarioCorporativo, Licencia



class SistemaVacacionesApex:
    def __init__(self):
        self.colaboradores: list[Colaborador] = []
        self.licencias: list[Licencia] = []
        self.calendarios: list[CalendarioCorporativo] = []
        self.usuario_logueado: Colaborador | None = None
        self.intentos_fallidos: dict[str, int] = {}
        self._cargar_datos_iniciales()

    def _cargar_datos_iniciales(self):
        # 1. Administrador RRHH (Jerarquía 3)
        admin = AdministradorRRHH(
            1001, "Mercedes", "Moran", 35111222, "mmoran", "admin123",
            date(2020, 3, 1), "RRHH", "mmoran@apexamerica.com",
            tiene_hijos=True, esta_casado=True
        )

        # 2. Supervisores (Jerarquía 2)
        sup1 = Supervisor(
            1002, "Ivan", "Pineda", 36222333, "ipineda", "sup123",
            date(2021, 6, 15), "Customer Care", "ipineda@apexamerica.com",
            tiene_hijos=True, esta_casado=False
        )
        sup2 = Supervisor(
            1003, "Ricardo", "Darín", 18444555, "rdarin", "sup123",
            date(2019, 4, 10), "Back Office", "rdarin@apexamerica.com",
            tiene_hijos=True, esta_casado=True
        )

        # 3. Colaboradores (Jerarquía 1)
        colab1 = Colaborador(
            1004, "Juan", "Pérez", 38333444, "jperez", "colab123",
            date(2023, 1, 10), "Customer Care", "jperez@apexamerica.com",
            tiene_hijos=False, esta_casado=False
        )
        colab2 = Colaborador(
            1005, "Guillermo", "Francella", 17555666, "gfrancella", "colab123",
            date(2021, 8, 20), "Customer Care", "gfrancella@apexamerica.com",
            tiene_hijos=True, esta_casado=True
        )
        colab3 = Colaborador(
            1006, "Mercedes", "Morán", 19666777, "emoran", "colab123",
            date(2022, 2, 14), "Customer Care", "mmoran@apexamerica.com",
            tiene_hijos=True, esta_casado=False
        )
        colab4 = Colaborador(
            1007, "Luis", "Brandoni", 12777888, "lbrandoni", "colab123",
            date(2018, 11, 5), "Back Office", "lbrandoni@apexamerica.com",
            tiene_hijos=False, esta_casado=True
        )
        colab5 = Colaborador(
            1008, "Nancy", "Dupláa", 24888999, "nduplaa", "colab123",
            date(2022, 7, 1), "Back Office", "nduplaa@apexamerica.com",
            tiene_hijos=True, esta_casado=False
        )
        colab6 = Colaborador(
            1009, "Leonardo", "Sbaraglia", 22999000, "lsbaraglia", "colab123",
            date(2023, 5, 19), "Customer Care", "lsbaraglia@apexamerica.com",
            tiene_hijos=False, esta_casado=False
        )
        colab7 = Colaborador(
            1010, "Carla", "Peterson", 26123456, "cpeterson", "colab123",
            date(2021, 9, 30), "Back Office", "cpeterson@apexamerica.com",
            tiene_hijos=True, esta_casado=True
        )

        self.colaboradores.extend([
            admin, sup1, sup2,
            colab1, colab2, colab3, colab4, colab5, colab6, colab7
        ])

        # Mapa auxiliar para vincular automáticamente cada licencia al historial de su colaborador
        mapa_colabs = {c.id_legajo: c for c in self.colaboradores}

        # Licencias precargadas (nivel_preferencia=None hasta que cada usuario rankee)
        licencias_iniciales = [
            # Admin RRHH (1001 - Prioridad 3)
            Licencia(1, 1001, date(2026, 4, 1), date(2026, 4, 14), "vacaciones", "pendiente"),
            Licencia(2, 1001, date(2026, 9, 10), date(2026, 9, 20), "vacaciones", "pendiente"),

            # Supervisores (1002 - Prioridad 1 | 1003 - Prioridad 3)
            Licencia(3, 1002, date(2026, 2, 1), date(2026, 2, 14), "vacaciones", "pendiente"),
            Licencia(4, 1002, date(2026, 7, 15), date(2026, 7, 25), "vacaciones", "pendiente"),
            Licencia(5, 1003, date(2026, 3, 1), date(2026, 3, 15), "vacaciones", "pendiente"),

            # Juan Pérez (1004 - Soltero, Prioridad 0) -> Superposición en enero con Francella (1005)
            Licencia(6, 1004, date(2026, 1, 10), date(2026, 1, 24), "vacaciones", "pendiente"),
            Licencia(7, 1004, date(2026, 1, 12), date(2026, 1, 26), "vacaciones", "pendiente"),
            Licencia(8, 1004, date(2026, 8, 3), date(2026, 8, 12), "vacaciones", "pendiente"),

            # Guillermo Francella (1005 - Casado + hijos, Prioridad 3) -> Misma fecha de enero que Pérez
            Licencia(9, 1005, date(2026, 1, 12), date(2026, 1, 26), "vacaciones", "pendiente"),
            Licencia(10, 1005, date(2026, 6, 1), date(2026, 6, 10), "vacaciones", "pendiente"),

            # Mercedes Morán (1006 - Hijos, Prioridad 1)
            Licencia(11, 1006, date(2026, 1, 12), date(2026, 1, 26), "vacaciones", "pendiente"),
            Licencia(12, 1006, date(2026, 5, 4), date(2026, 5, 15), "vacaciones", "pendiente"),

            # Luis Brandoni (1007 - Casado, Prioridad 3)
            Licencia(13, 1007, date(2026, 10, 5), date(2026, 10, 18), "vacaciones", "pendiente"),

            # Nancy Dupláa (1008 - Hijos, Prioridad 1)
            Licencia(14, 1008, date(2026, 11, 2), date(2026, 11, 14), "vacaciones", "pendiente"),

            # Leonardo Sbaraglia (1009 - Soltero, Prioridad 0)
            Licencia(15, 1009, date(2026, 7, 1), date(2026, 7, 14), "vacaciones", "pendiente"),

            # Carla Peterson (1010 - Casada + hijos, Prioridad 3)
            Licencia(16, 1010, date(2026, 12, 14), date(2026, 12, 28), "vacaciones", "pendiente"),
        ]

        for lic in licencias_iniciales:
            mapa_colabs[lic.colaborador_legajo].solicitar_licencia(lic)
            self.licencias.append(lic)

        self.calendarios.extend([
            CalendarioCorporativo(1, "Customer Care", 90),
            CalendarioCorporativo(2, "Back Office", 75),
        ])

    # --- CASO DE USO N1: LOGIN ---
    def cu1_login(self, usuario: str, contrasena: str) -> Colaborador:
        for colab in self.colaboradores:
            if colab.usuario == usuario:
                if not colab.estado:
                    raise PermissionError("Usuario inhabilitado. Debe blanquear contraseña (CU N2).")

                if colab.login(usuario, contrasena):
                    self.intentos_fallidos[usuario] = 0
                    self.usuario_logueado = colab
                    return colab
                else:
                    intentos = self.intentos_fallidos.get(usuario, 0) + 1
                    self.intentos_fallidos[usuario] = intentos
                    if intentos >= 3:
                        colab.estado = False
                        raise PermissionError("3 intentos fallidos: usuario inhabilitado.")
                    raise ValueError(f"Credenciales incorrectas. Intento {intentos}/3.")
        raise LookupError("Usuario no encontrado.")

    # --- CASO DE USO N4: RANKEO DE FECHAS ---
    def cu4_rankear_fechas(
        self, colaborador: Colaborador, preferencias_por_id: dict[int, int]
    ) -> list[Licencia]:
        """
        Asigna nivel de preferencia (1 a 3) a las licencias candidatas del colaborador.
        """
        if not self.usuario_logueado:
            raise PermissionError("Debe iniciar sesión primero (CU N1).")

        actualizadas = []
        for lic in colaborador.historial_licencias:
            if lic.id_licencia in preferencias_por_id:
                pref = preferencias_por_id[lic.id_licencia]
                if pref not in (1, 2, 3):
                    raise ValueError("La preferencia debe ser 1 (máxima), 2 o 3 (mínima).")
                lic.nivel_preferencia = pref
                actualizadas.append(lic)
        return actualizadas

    # --- CASO DE USO N6: FIRMA DE LICENCIA ---
    def cu6_firmar_licencia(self, colaborador: Colaborador, id_licencia: int) -> Licencia:
        """
        El colaborador firma en conformidad la licencia asignada -> pasa a 'aprobada'.
        """
        if not self.usuario_logueado:
            raise PermissionError("Debe iniciar sesión primero (CU N1).")

        for lic in colaborador.historial_licencias:
            if lic.id_licencia == id_licencia:
                if colaborador.firmar_vacaciones(lic):
                    return lic
                raise ValueError("La licencia no está en estado 'asignada' para firmar.")
        raise LookupError("Licencia no encontrada para este colaborador.")

    # --- CASO DE USO N10: ALTA DE COLABORADOR ---
    def cu10_alta_colaborador(
        self,
        id_legajo: int,
        nombre: str,
        apellido: str,
        dni: int,
        fecha_ingreso: date,
        area: str,
        email_corporativo: str,
        tiene_hijos: bool = False,
        esta_casado: bool = False,
    ) -> Colaborador:
        """
        Solo un AdministradorRRHH autenticado puede dar de alta un nuevo colaborador.
        Valida legajo/DNI únicos y genera usuario y contraseña automáticamente.
        """
        if not isinstance(self.usuario_logueado, AdministradorRRHH):
            raise PermissionError("Acceso denegado: solo Administrador de RRHH puede dar de alta.")

        for c in self.colaboradores:
            if c.id_legajo == id_legajo or c.dni == dni:
                raise ValueError("Ya existe un colaborador con ese legajo o DNI.")

        # Generación automática de credenciales
        usuario_gen = f"{nombre[0].lower()}{apellido.lower()}"
        contrasena_gen = f"apex{dni}"

        nuevo = Colaborador(
            id_legajo=id_legajo,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            usuario=usuario_gen,
            contrasena=contrasena_gen,
            fecha_ingreso=fecha_ingreso,
            area=area,
            email_corporativo=email_corporativo,
            tiene_hijos=tiene_hijos,
            esta_casado=esta_casado,
        )
        self.colaboradores.append(nuevo)
        return nuevo

# --- CERRAR SESIÓN ---
    def cu1_logout(self) -> None:
        self.usuario_logueado = None

    # --- ACCIÓN DE SUPERVISOR: APROBAR O RECHAZAR LICENCIA PENDIENTE ---
    def supervisor_gestionar_licencia(self, id_licencia: int, aprobar: bool) -> Licencia:
        if not isinstance(self.usuario_logueado, Supervisor):
            raise PermissionError("Acceso denegado: solo un Supervisor puede realizar esta acción.")

        for lic in self.licencias:
            if lic.id_licencia == id_licencia:
                if self.usuario_logueado.gestionar_licencia(lic, aprobar):
                    return lic
                raise ValueError("La licencia debe estar en estado 'pendiente' para ser evaluada.")
        raise LookupError("Licencia no encontrada.")

    # --- ACCIÓN DE ADMIN RRHH: CONFIRMAR O RECHAZAR LICENCIA APROBADA ---
    def admin_confirmar_licencia(self, id_licencia: int, confirmar: bool) -> Licencia:
        if not isinstance(self.usuario_logueado, AdministradorRRHH):
            raise PermissionError("Acceso denegado: solo un Administrador de RRHH puede realizar esta acción.")

        for lic in self.licencias:
            if lic.id_licencia == id_licencia:
                if self.usuario_logueado.confirmar_licencia(lic, confirmar):
                    return lic
                raise ValueError(
                    "La licencia debe estar en estado 'aprobada' y no pertenecer al mismo administrador."
                )
        raise LookupError("Licencia no encontrada.")


import pytest
from datetime import date

from Models.clases import (
    Colaborador,
    Supervisor,
    AdministradorRRHH,
    Licencia,
    CalendarioCorporativo
)

from Service.casos_uso import SistemaVacacionesApex

from Estructuras.algoritmo_ordenamiento import (
    ordenar_licencias_merge_sort
)


class TestClasesYCasosDeUso:

    # ==========================================
    # TESTS DE LAS CLASES (5)
    # ==========================================

    def test_clase_colaborador_prioridad(self):

        c_soltero = Colaborador(
            1, "Ana", "Gómez", 111, "agomez", "123",
            date(2022, 1, 1), "IT", "a@apex.com"
        )

        c_hijos = Colaborador(
            2, "Luis", "Díaz", 222, "ldiaz", "123",
            date(2022, 1, 1), "IT", "l@apex.com",
            tiene_hijos=True
        )

        c_casado = Colaborador(
            3, "Sofía", "Ruiz", 333, "sruiz", "123",
            date(2022, 1, 1), "IT", "s@apex.com",
            esta_casado=True
        )

        assert c_soltero.nivel_prioridad == 3
        assert c_hijos.nivel_prioridad == 2
        assert c_casado.nivel_prioridad == 1

    def test_clase_supervisor(self):

        sup = Supervisor(
            10, "Luca", "Guzmán", 444, "lguzman", "123",
            date(2021, 1, 1), "Ops", "l@apex.com"
        )

        lic = Licencia(
            1, 20,
            date(2026, 5, 1),
            date(2026, 5, 10),
            estado="pendiente",
            nivel_preferencia=1
        )

        assert sup.nivel_jerarquia == 2
        assert sup.gestionar_licencia(lic, aprobar=True) is True
        assert lic.estado == "asignada"

    def test_clase_administrador_rrhh(self):

        admin = AdministradorRRHH(
            11, "Mercedes", "Moran", 555, "mmoran", "123",
            date(2020, 1, 1), "RRHH", "mmoran@apex.com"
        )

        lic = Licencia(
            2, 20,
            date(2026, 5, 1),
            date(2026, 5, 10),
            estado="aprobada"
        )

        assert admin.nivel_jerarquia == 3
        assert admin.confirmar_licencia(lic) is True
        assert lic.estado == "confirmada"

    def test_clase_licencia(self):

        lic_valida = Licencia(
            3, 20,
            date(2026, 6, 1),
            date(2026, 6, 14)
        )

        lic_invalida = Licencia(
            4, 20,
            date(2026, 6, 15),
            date(2026, 6, 1)
        )

        assert lic_valida.validar_periodo() is True
        assert lic_invalida.validar_periodo() is False

    def test_clase_calendario_corporativo(self):

        cal = CalendarioCorporativo(1, "Customer Care", 30)

        lic = Licencia(
            5, 20,
            date(2026, 7, 1),
            date(2026, 7, 10),
            estado="confirmada"
        )

        assert cal.agregar_vacaciones(lic) is True
        assert cal.dias_disponibles == 20

    # ==========================================
    # TESTS DE CASOS DE USO (4)
    # ==========================================

    def test_cu1_login(self):

        sistema = SistemaVacacionesApex()

        usuario = sistema.cu1_login("jperez", "colab123")

        assert usuario.id_legajo == 1004
        assert sistema.usuario_logueado == usuario

    def test_cu4_rankear_fechas(self):

        sistema = SistemaVacacionesApex()

        colab = sistema.cu1_login("jperez", "colab123")

        sistema.cu4_rankear_fechas(
            colab,
            {6: 2, 7: 1, 8: 3}
        )

        colaboradores_por_legajo = {
            c.id_legajo: c
            for c in sistema.colaboradores
        }

        ordenadas = ordenar_licencias_merge_sort(
            colab.historial_licencias,
            colaboradores_por_legajo
        )

        assert ordenadas[0].id_licencia == 7
        assert ordenadas[0].nivel_preferencia == 1
        assert ordenadas[1].nivel_preferencia == 2
        assert ordenadas[2].nivel_preferencia == 3

    def test_cu6_firmar_licencia(self):

        sistema = SistemaVacacionesApex()

        colab = sistema.cu1_login("jperez", "colab123")

        # Simulamos una licencia previamente asignada.
        licencia = next(
            lic for lic in colab.historial_licencias
            if lic.id_licencia == 6
        )

        licencia.estado = "asignada"

        lic_firmada = sistema.cu6_firmar_licencia(
            colab, 6
        )

        assert lic_firmada.estado == "aprobada"
        
    def test_cu10_alta_colaborador(self):

        sistema = SistemaVacacionesApex()

        sistema.cu1_login("mmoran", "admin123")

        nuevo = sistema.cu10_alta_colaborador(
            1011,
            "Carlos",
            "López",
            40111222,
            date(2026, 1, 1),
            "Back Office",
            "clopez@apexamerica.com",
            tiene_hijos=True,
            esta_casado=False
        )

        assert nuevo.usuario == "clópez"
        assert nuevo.nivel_prioridad == 2
        assert nuevo in sistema.colaboradores



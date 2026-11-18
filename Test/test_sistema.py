import unittest
from datetime import date
from Models.clases import Colaborador, Supervisor, AdministradorRRHH, Licencia, CalendarioCorporativo
from Service.casos_uso import SistemaVacacionesApex
from Estructuras.algoritmo_ordenamiento import ordenar_licencias_por_preferencia


class TestClasesYCasosDeUso(unittest.TestCase):
    # ==========================================
    # TESTS DE LAS CLASES (5 tests - 1 por clase)
    # ==========================================

    def test_clase_colaborador_prioridad(self):
        c_soltero = Colaborador(1, "Ana", "Gómez", 111, "agomez", "123", date(2022, 1, 1), "IT", "a@apex.com")
        c_hijos = Colaborador(2, "Luis", "Díaz", 222, "ldiaz", "123", date(2022, 1, 1), "IT", "l@apex.com", tiene_hijos=True)
        c_casado = Colaborador(3, "Sofía", "Ruiz", 333, "sruiz", "123", date(2022, 1, 1), "IT", "s@apex.com", esta_casado=True)

        self.assertEqual(c_soltero.nivel_prioridad, 0)
        self.assertEqual(c_hijos.nivel_prioridad, 1)
        self.assertEqual(c_casado.nivel_prioridad, 3)

    def test_clase_supervisor(self):
        sup = Supervisor(10, "Luca", "Guzman", 444, "lguzman", "123", date(2021, 1, 1), "Ops", "l@apex.com")
        lic = Licencia(1, 20, date(2026, 5, 1), date(2026, 5, 10), estado="pendiente",nivel_preferencia=1)
        self.assertEqual(sup.nivel_jerarquia, 2)
        self.assertTrue(sup.gestionar_licencia(lic, aprobar=True))
        self.assertEqual(lic.estado, "aprobada")

    def test_clase_administrador_rrhh(self):
        admin = AdministradorRRHH(11, "Mercedes", "Moran", 555, "mmoran", "123", date(2020, 1, 1), "RRHH", "mmoran@apex.com")
        lic = Licencia(2, 20, date(2026, 5, 1), date(2026, 5, 10), estado="aprobada")
        self.assertEqual(admin.nivel_jerarquia, 3)
        self.assertTrue(admin.confirmar_licencia(lic))
        self.assertEqual(lic.estado, "confirmada")

    def test_clase_licencia(self):
        lic_valida = Licencia(3, 20, date(2026, 6, 1), date(2026, 6, 14))
        lic_invalida = Licencia(4, 20, date(2026, 6, 15), date(2026, 6, 1))
        self.assertTrue(lic_valida.validar_periodo())
        self.assertFalse(lic_invalida.validar_periodo())

    def test_clase_calendario_corporativo(self):
        cal = CalendarioCorporativo(1, "Customer Care", 30)
        lic = Licencia(5, 20, date(2026, 7, 1), date(2026, 7, 10), estado="confirmada")  # 10 días
        self.assertTrue(cal.agregar_vacaciones(lic))
        self.assertEqual(cal.dias_disponibles, 20)

    # ==============================================
    # TESTS DE CASOS DE USO (4 tests - 1 por CU)
    # ==============================================

    def test_cu1_login(self):
        sistema = SistemaVacacionesApex()
        usuario = sistema.cu1_login("jperez", "colab123")
        self.assertEqual(usuario.id_legajo, 1004)
        self.assertEqual(sistema.usuario_logueado, usuario)

    def test_cu4_rankear_fechas(self):
        sistema = SistemaVacacionesApex()
        colab = sistema.cu1_login("jperez", "colab123")
        sistema.cu4_rankear_fechas(colab, {6: 2, 7: 1, 8: 3})
        ordenadas = ordenar_licencias_por_preferencia(colab.historial_licencias)
        self.assertEqual(ordenadas[0].id_licencia, 7)
        self.assertEqual(ordenadas[0].nivel_preferencia, 1)
        self.assertEqual(ordenadas[1].nivel_preferencia, 2)
        self.assertEqual(ordenadas[2].nivel_preferencia, 3)

    def test_cu6_firmar_licencia(self):
        sistema = SistemaVacacionesApex()
        colab = sistema.cu1_login("jperez", "colab123")
        lic_firmada = sistema.cu6_firmar_licencia(colab, 6)
        self.assertEqual(lic_firmada.estado, "aprobada")

    def test_cu10_alta_colaborador(self):
        sistema = SistemaVacacionesApex()
        sistema.cu1_login("mmoran", "admin123")
        nuevo = sistema.cu10_alta_colaborador(
            1011, "Carlos", "López", 40111222, date(2026, 1, 1),
            "Back Office", "clopez@apexamerica.com", tiene_hijos=True, esta_casado=False
        )
        self.assertEqual(nuevo.usuario, "clópez")
        self.assertEqual(nuevo.nivel_prioridad, 1)
        self.assertIn(nuevo, sistema.colaboradores)


if __name__ == "__main__":
    unittest.main()
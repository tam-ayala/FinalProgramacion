import unittest
from clases import Colaborador, Supervisor, AdministradorRRHH, Licencia
from casos_uso import SistemaGestionVacaciones

class TestClasesYCasosDeUso(unittest.TestCase):

    def test_clase_colaborador(self):
        colab = Colaborador(1, "Ana", "Pérez", 30000000, "aperez", "1234", "Operario", "2022-03-01", "Dom", "Customer Care", "aperez@apex.com")
        self.assertEqual(colab.nombre, "Ana")
        self.assertTrue(colab.estado)

    def test_clase_supervisor(self):
        sup = Supervisor(2, "Carlos", "Gómez", 25000000, "cgomez", "1234", "Supervisor", "2018-05-10", "Sab-Dom", "Back Office", "cgomez@apex.com")
        self.assertTrue(sup.validar_intercambio(101))

    def test_clase_admin_rrhh(self):
        admin = AdministradorRRHH(3, "Laura", "Sosa", 20000000, "lsosa", "1234", "Admin RRHH", "2015-01-01", "Sab-Dom", "RRHH", "lsosa@apex.com")
        lic = Licencia(1, "2026-01-01", "2026-01-15", "Vacaciones")
        lic.estado = "aprobada"
        self.assertTrue(admin.confirmar_licencia(lic))
        self.assertEqual(lic.estado, "confirmada")

    def test_clase_licencia(self):
        lic = Licencia(10, "2026-05-01", "2026-05-15", "Vacaciones", nivel_preferencia=1)
        self.assertEqual(lic.estado, "pendiente")
        self.assertEqual(lic.nivel_preferencia, 1)

    # --- TESTS POR CASO DE USO (4 tests) ---
    def setUp(self):
        self.sistema = SistemaGestionVacaciones()

    def test_cu_n1_login(self):
        user = self.sistema.login("admin", "admin123")
        self.assertIsNotNone(user)
        self.assertEqual(user.usuario, "admin")

    def test_cu_n10_alta_colaborador(self):
        admin = self.sistema.usuarios["admin"]
        nuevo = Colaborador(50, "Juan", "Rios", 40000000, "jrios", "pass", "Operario", "2024-01-01", "Dom", "IT", "jrios@apex.com")
        resultado = self.sistema.alta_colaborador(admin, nuevo)
        self.assertTrue(resultado)
        self.assertIn("jrios", self.sistema.usuarios)

    def test_cu_n4_rankeo_y_ordenamiento(self):
        l1 = Licencia(1, "2026-01-01", "2026-01-14", "Vacaciones", nivel_preferencia=3)
        l2 = Licencia(2, "2026-02-01", "2026-02-14", "Vacaciones", nivel_preferencia=1)
        licencias_ordenadas = self.sistema.rankear_licencias([l1, l2])
        self.assertEqual(licencias_ordenadas[0].nivel_preferencia, 1)
        self.assertEqual(licencias_ordenadas[1].nivel_preferencia, 3)

    def test_cu_n6_firmar_licencia(self):
        lic = Licencia(1, "2026-01-01", "2026-01-14", "Vacaciones")
        resultado = self.sistema.firmar_licencia(lic)
        self.assertTrue(resultado)
        self.assertEqual(lic.estado, "aprobada")

if __name__ == '__main__':
    unittest.main()
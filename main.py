from clases import Colaborador, AdministradorRRHH, Licencia
from casos_uso import SistemaGestionVacaciones

def ejecutar_menu():
    sistema = SistemaGestionVacaciones()
    usuario_logeado = None

    while True:
        print("\n" + "="*45)
        print("  SISTEMA DE GESTIÓN DE VACACIONES - APEX  ")
        print("="*45)
        if not usuario_logeado:
            print("1. Iniciar Sesión (CU N1 - Login)")
            print("0. Salir")
        else:
            print(f"Usuario: {usuario_logeado.nombre} ({usuario_logeado.jerarquia})")
            print("2. Registrar Nuevo Colaborador (CU N10 - Alta Colaborador)")
            print("3. Rankear Fechas de Licencia (CU N4 - Rankeo y Ordenamiento)")
            print("4. Firmar Licencia de Vacaciones (CU N6 - Firma Licencia)")
            print("5. Cerrar Sesión")
            print("0. Salir")

        opcion = input("\nSeleccione una opción: ")

        if opcion == "1" and not usuario_logeado:
            usr = input("Usuario: ")
            pwd = input("Contraseña: ")
            user = sistema.login(usr, pwd)
            if user:
                usuario_logeado = user
                print(f"\n[OK] Bienvenido/a {user.nombre} {user.apellido}.")
            else:
                print("\n[ERROR] Credenciales inválidas.")

        elif opcion == "2" and usuario_logeado:
            if not isinstance(usuario_logeado, AdministradorRRHH):
                print("\n[ERROR] Solo el Admin de RRHH puede realizar esta acción.")
                continue
            legajo = int(input("Legajo: "))
            nom = input("Nombre: ")
            ape = input("Apellido: ")
            dni = int(input("DNI: "))
            usr = input("Usuario: ")
            pwd = input("Contraseña: ")
            nuevo = Colaborador(legajo, nom, ape, dni, usr, pwd, "Colaborador", "2023-01-01", "Sab-Dom", "Customer Care", f"{usr}@apex.com")
            if sistema.alta_colaborador(usuario_logeado, nuevo):
                print(f"\n[OK] Colaborador {nom} registrado con éxito.")
            else:
                print("\n[ERROR] El usuario ya existe.")

        elif opcion == "3" and usuario_logeado:
            print("\n--- Rankeo y Ordenamiento de Licencias Candidatas ---")
            l1 = Licencia(1, "2026-01-10", "2026-01-24", "Vacaciones", nivel_preferencia=3)
            l2 = Licencia(2, "2026-02-01", "2026-02-15", "Vacaciones", nivel_preferencia=1)
            l3 = Licencia(3, "2026-03-05", "2026-03-19", "Vacaciones", nivel_preferencia=2)

            cand = [l1, l2, l3]
            print("\nFechas desordenadas recibidas:")
            for l in cand:
                print(f"  - Option ID {l.id_licencia} | Inicio: {l.fecha_inicio} | Prioridad asignada: {l.nivel_preferencia}")

            ordenadas = sistema.rankear_licencias(cand)
            print("\nFechas procesadas y ordenadas por algoritmo (Bubble Sort):")
            for l in ordenadas:
                print(f"  - Prioridad {l.nivel_preferencia} -> Inicio: {l.fecha_inicio} (ID Licencia: {l.id_licencia})")

        elif opcion == "4" and usuario_logeado:
            lic = Licencia(101, "2026-01-15", "2026-01-29", "Vacaciones", legajo_empleado=usuario_logeado.legajo)
            print(f"\nLicencia Asignada: ID {lic.id_licencia} | Estado actual: {lic.estado}")
            confirmar = input("¿Desea firmar en conformidad? (s/n): ")
            if confirmar.lower() == 's':
                sistema.firmar_licencia(lic)
                print(f"\n[OK] Licencia firmada exitosamente. Nuevo estado: {lic.estado}")
            else:
                print("\nOperación cancelada.")

        elif opcion == "5" and usuario_logeado:
            usuario_logeado = None
            print("\n[OK] Sesión cerrada.")

        elif opcion == "0":
            print("\n¡Hasta luego!")
            break
        else:
            print("\n[ERROR] Opción no válida.")

if __name__ == "__main__":
    ejecutar_menu()
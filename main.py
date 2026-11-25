from datetime import date

from Service.casos_uso import SistemaVacacionesApex

from Estructuras.algoritmo_ordenamiento import (
    ordenar_licencias_merge_sort,
)

from Models.clases import Supervisor, AdministradorRRHH


def mostrar_menu():

    sistema = SistemaVacacionesApex()

    while True:

        print("\n========================================")
        print("APEX AMERICA - SISTEMA DE VACACIONES")
        print("========================================")

        # USUARIO NO AUTENTICADO
        if sistema.usuario_logueado is None:

            print("\n1. Iniciar sesion")
            print("0. Salir")

            opcion = input("Seleccione una opcion: ").strip()

            try:

                if opcion == "1":

                    print("\nCredenciales de prueba:")
                    print("Admin: mmoran / admin123")
                    print("Supervisor: ipineda / sup123")
                    print("Colaborador: jperez / colab123")

                    usuario = input("Usuario: ").strip()
                    contrasena = input("Contrasena: ").strip()

                    colaborador = sistema.cu1_login(
                        usuario,
                        contrasena
                    )

                    print(
                        f"Bienvenido/a {colaborador.nombre} "
                        f"{colaborador.apellido}"
                    )

                elif opcion == "0":

                    print("Saliendo del sistema...")
                    break

                else:

                    print("Opcion invalida.")

            except Exception as error:

                print(f"ERROR: {error}")

        # USUARIO AUTENTICADO
        else:

            usuario_actual = sistema.usuario_logueado

            es_supervisor = isinstance(
                usuario_actual,
                Supervisor
            )

            es_administrador = isinstance(
                usuario_actual,
                AdministradorRRHH
            )

            colaboradores_por_legajo = {
                colaborador.id_legajo: colaborador
                for colaborador in sistema.colaboradores
            }

            print("\n----------------------------------------")
            print(
                f"Usuario: {usuario_actual.nombre} "
                f"{usuario_actual.apellido}"
            )

            print(
                f"Rol: {type(usuario_actual).__name__}"
            )

            print("----------------------------------------")

            print("1. [CU N4] Rankear fechas")
            print("2. [CU N6] Firmar licencia")

            if es_supervisor:
                print("3. Aprobar o rechazar licencias")
                print("4. Listar licencias con Merge Sort")

            if es_administrador:
                print("3. Confirmar o rechazar licencias")
                print("4. [CU N10] Alta de colaborador")
                print("5. Listar licencias con Merge Sort")

            print("9. Cerrar sesion")
            print("0. Salir")

            opcion = input("Seleccione una opcion: ").strip()

            try:

                                # CU N4: RANKEAR FECHAS

                if opcion == "1":

                    licencias_colaborador = (
                        usuario_actual.historial_licencias
                    )

                    if not licencias_colaborador:
                        print("No tiene licencias registradas.")
                        continue

                    preferencias_por_id = {}

                    for licencia in licencias_colaborador:

                        print(licencia)

                        while True:

                            try:

                                preferencia = int(
                                    input(
                                        "Ingrese preferencia (1, 2 o 3): "
                                    )
                                )

                                if preferencia in (1, 2, 3):
                                    preferencias_por_id[
                                        licencia.id_licencia
                                    ] = preferencia
                                    break

                                print("Ingrese 1, 2 o 3.")

                            except ValueError:
                                print("Debe ingresar un numero.")

                    sistema.cu4_rankear_fechas(
                        usuario_actual,
                        preferencias_por_id
                    )

                    licencias_ordenadas = ordenar_licencias_merge_sort(
                        licencias_colaborador
                    )

                    print("\nLicencias ordenadas por preferencia:")

                    for licencia in licencias_ordenadas:
                        print(licencia)

                # CU N6: FIRMAR LICENCIA

                elif opcion == "2":

                    licencias_asignadas = [
                        licencia
                        for licencia in usuario_actual.historial_licencias
                        if licencia.estado == "asignada"
                    ]

                    if not licencias_asignadas:
                        print("No hay licencias asignadas.")
                        continue

                    for licencia in licencias_asignadas:
                        print(licencia)

                    id_licencia = int(
                        input("Ingrese el ID de la licencia: ")
                    )

                    licencia = sistema.cu6_firmar_licencia(
                        usuario_actual,
                        id_licencia
                    )

                    print(
                        f"Licencia firmada. Estado: {licencia.estado}"
                    )

                # SUPERVISOR: APROBAR O RECHAZAR

                elif opcion == "3" and es_supervisor:

                    licencias_pendientes = [
                        licencia
                        for licencia in sistema.licencias
                        if (
                            licencia.estado == "pendiente"
                            and licencia.nivel_preferencia is not None
                        )
                    ]

                    licencias_pendientes = ordenar_licencias_merge_sort(
                        licencias_pendientes,
                        colaboradores_por_legajo
                    )

                    if not licencias_pendientes:
                        print("No hay licencias pendientes.")
                        continue

                    for licencia in licencias_pendientes:
                        print(licencia)

                    id_licencia = int(
                        input("ID de licencia a evaluar: ")
                    )

                    accion = input(
                        "Aprobar (s) o rechazar (n): "
                    ).strip().lower()

                    if accion not in ("s", "n"):
                        print("Accion invalida.")
                        continue

                    licencia = sistema.supervisor_gestionar_licencia(
                        id_licencia,
                        aprobar=(accion == "s")
                    )

                    print(f"Nuevo estado: {licencia.estado}")

                # SUPERVISOR: LISTAR CON MERGE SORT

                elif opcion == "4" and es_supervisor:

                    licencias_ordenadas = ordenar_licencias_merge_sort(
                        sistema.licencias,
                        colaboradores_por_legajo
                    )

                    for licencia in licencias_ordenadas:
                        print(licencia)

                            # ADMINISTRADOR: CONFIRMAR O RECHAZAR

                elif opcion == "3" and es_administrador:

                    licencias_aprobadas = [
                        licencia
                        for licencia in sistema.licencias
                        if licencia.estado == "aprobada"
                    ]

                    licencias_aprobadas = ordenar_licencias_merge_sort(
                        licencias_aprobadas,
                        colaboradores_por_legajo
                    )

                    if not licencias_aprobadas:
                        print("No hay licencias aprobadas.")
                        continue

                    for licencia in licencias_aprobadas:
                        print(licencia)

                    id_licencia = int(
                        input("ID de licencia a resolver: ")
                    )

                    accion = input(
                        "Confirmar (s) o rechazar (n): "
                    ).strip().lower()

                    if accion not in ("s", "n"):
                        print("Accion invalida.")
                        continue

                    licencia = sistema.admin_confirmar_licencia(
                        id_licencia,
                        confirmar=(accion == "s")
                    )

                    print(f"Nuevo estado: {licencia.estado}")

                # CU N10: ALTA DE COLABORADOR

                elif opcion == "4" and es_administrador:

                    legajo = int(input("Legajo: "))
                    nombre = input("Nombre: ").strip()
                    apellido = input("Apellido: ").strip()
                    dni = int(input("DNI: "))
                    area = input("Area: ").strip()
                    email = input("Email corporativo: ").strip()

                    tiene_hijos = (
                        input("Tiene hijos? (s/n): ")
                        .strip().lower() == "s"
                    )

                    esta_casado = (
                        input("Esta casado/a? (s/n): ")
                        .strip().lower() == "s"
                    )

                    nuevo_colaborador = sistema.cu10_alta_colaborador(
                        legajo,
                        nombre,
                        apellido,
                        dni,
                        date.today(),
                        area,
                        email,
                        tiene_hijos,
                        esta_casado
                    )

                    print("Colaborador creado correctamente.")
                    print(nuevo_colaborador)

                    print(
                        f"Usuario: {nuevo_colaborador.usuario}"
                    )

                    print(
                        f"Contrasena: {nuevo_colaborador.contrasena}"
                    )

                # ADMINISTRADOR: LISTAR CON MERGE SORT

                elif opcion == "5" and es_administrador:

                    licencias_ordenadas = ordenar_licencias_merge_sort(
                        sistema.licencias,
                        colaboradores_por_legajo
                    )

                    for licencia in licencias_ordenadas:
                        print(licencia)

                # CERRAR SESION

                elif opcion == "9":

                    sistema.cu1_logout()
                    print("Sesion cerrada correctamente.")

                # SALIR

                elif opcion == "0":

                    print("Saliendo del sistema...")
                    break

                else:

                    print("Opcion invalida para su jerarquia.")

            except Exception as error:

                print(f"ERROR: {error}")


if __name__ == "__main__":
    mostrar_menu()
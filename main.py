from datetime import date
from Service.casos_uso import SistemaVacacionesApex
from Estructuras.algoritmo_ordenamiento import (
    ordenar_licencias_por_preferencia,
    ordenar_colaboradores_por_prioridad,
)
from Models.clases import (
    Colaborador,
    Supervisor,
    AdministradorRRHH,
    CalendarioCorporativo,
    Licencia,
)


def mostrar_menu():
    sistema = SistemaVacacionesApex()

    while True:
        print("  APEX AMÉRICA - SISTEMA DE GESTIÓN DE VACACIONES")

        # ==========================================================
        # CASO A: USUARIO NO AUTENTICADO (Solo Login y Salir)
        # ==========================================================
        if not sistema.usuario_logueado:
            print("  Sesión: No autenticado")
            print("1. [CU N1] Iniciar Sesión (Login)")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            try:
                if opcion == "1":
                    print("--- Credenciales de prueba ---")
                    print("Admin RRHH (Jerarquía 3) : mmoran / admin123")
                    print("Supervisor (Jerarquía 2) : ipineda / sup123")
                    print("Colaborador (Jerarquía 1): jperez  / colab123")
                    user = input("Usuario: ").strip()
                    pwd = input("Contraseña: ").strip()
                    colab = sistema.cu1_login(user, pwd)
                    print(
                        f"Bienvenido/a {colab.nombre} {colab.apellido} "
                    )
                elif opcion == "0":
                    print("Saliendo del sistema...")
                    break
                else:
                    print("Opción inválida. Debe iniciar sesión para acceder al sistema.")
            except Exception as e:
                print(f"[ERROR]: {e}")

        # ==========================================================
        # CASO B: USUARIO AUTENTICADO (Panel según Jerarquía)
        # ==========================================================
        else:
            u = sistema.usuario_logueado
            es_supervisor = isinstance(u, Supervisor)
            es_admin = isinstance(u, AdministradorRRHH)
            mapa_colabs = {c.id_legajo: c for c in sistema.colaboradores}

            print(
                f" Sesión activa: {u.nombre} {u.apellido} | "
                f"Rol: {type(u).__name__} (Jerarquía {u.nivel_jerarquia})"
            )
            print("=" * 62)

            # Opciones comunes a todo empleado autenticado (Jerarquía 1, 2 y 3)
            print("1. [CU N4] Rankear Fechas de Vacaciones (Preferencia 1-3)")
            print("2. [CU N6] Firmar Licencia Asignada")

            # Opciones exclusivas de Supervisor (Jerarquía 2)
            if es_supervisor:
                print("3. [Supervisor] Aprobar o Rechazar Licencias Pendientes")
                print("4. [Ordenamiento] Listar Licencias por Prioridad Familiar y Preferencia")

            # Opciones exclusivas de Administrador RRHH (Jerarquía 3)
            if es_admin:
                print("3. [Admin RRHH] Confirmar o Rechazar Licencias Aprobadas")
                print("4. [CU N10] Alta de Colaborador")
                print("5. [Ordenamiento] Listar Licencias por Prioridad Familiar y Preferencia")
                print("6. [Ordenamiento] Listar Colaboradores por Prioridad Familiar (Bubble Sort)")

            print("9. Cerrar Sesión (Cambiar de usuario)")
            print("0. Salir")

            opcion = input("Seleccione una opción: ").strip()

            try:
                # --- Opción 1: CU N4 Rankeo (Todos los roles) ---
                if opcion == "1":
                    lics = u.historial_licencias
                    if not lics:
                        print("No tiene licencias registradas para rankear.")
                        continue

                    print("--- Sus opciones de fechas disponibles ---")
                    for idx, l in enumerate(lics, start=1):
                        pref_actual = (
                            l.nivel_preferencia
                            if l.nivel_preferencia is not None
                            else "Sin asignar"
                        )
                        print(
                            f"Opción {idx} -> [ID Licencia: {l.id_licencia}] "
                            f"Del {l.fecha_inicio} al {l.fecha_fin} | "
                            f"Preferencia actual: {pref_actual} | Estado: {l.estado}"
                        )

                    prefs = {}
                    for idx, l in enumerate(lics, start=1):
                        p = int(
                            input(
                                f"Ingrese prioridad (1=máxima, 2=media, 3=mínima) para Opción {idx} (ID {l.id_licencia}): "
                            )
                        )
                        prefs[l.id_licencia] = p

                    sistema.cu4_rankear_fechas(u, prefs)

                    print("Rankeo guardado correctamente. Sus licencias ordenadas por preferencia:")
                    for l in ordenar_licencias_por_preferencia(u.historial_licencias):
                        print(
                            f"Prioridad {l.nivel_preferencia} -> [ID Licencia: {l.id_licencia}] "
                            f"Del {l.fecha_inicio} al {l.fecha_fin} | Estado: {l.estado}"
                        )

                # --- Opción 2: CU N6 Firma de licencia (Todos los roles) ---
                elif opcion == "2":
                    asignadas = [l for l in u.historial_licencias if l.estado == "asignada"]
                    if not asignadas:
                        print("No tiene licencias en estado 'asignada' listas para firmar.")
                        continue

                    print("--- Licencias asignadas disponibles para firmar ---")
                    for idx, l in enumerate(asignadas, start=1):
                        pref_actual = (
                            l.nivel_preferencia
                            if l.nivel_preferencia is not None
                            else "Sin asignar"
                        )
                        print(
                            f"Opción {idx} -> [ID Licencia: {l.id_licencia}] "
                            f"Del {l.fecha_inicio} al {l.fecha_fin} | Preferencia: {pref_actual}"
                        )

                    ids_validos = [l.id_licencia for l in asignadas]
                    id_lic = int(input(f"Ingrese el ID de la licencia a firmar {ids_validos}: "))
                    lic = sistema.cu6_firmar_licencia(u, id_lic)
                    print(f"Licencia ID {lic.id_licencia} firmada con éxito. Nuevo estado: {lic.estado}")

                # --- Opciones exclusivas de SUPERVISOR ---
                
                elif opcion == "3" and es_supervisor:
                    pendientes = ordenar_licencias_por_preferencia(
                        [
                            l
                            for l in sistema.licencias
                            if l.estado == "pendiente" and l.nivel_preferencia is not None
                        ],
                        mapa_colabs,
                    )
                    if not pendientes:
                        print("No hay licencias pendientes rankeadas para revisar.")
                        continue
                    print("--- Licencias pendientes rankeadas (ordenadas por prioridad familiar y preferencia) ---")
                    for l in pendientes:
                        colab_lic = mapa_colabs.get(l.colaborador_legajo)
                        prio_fam = colab_lic.nivel_prioridad if colab_lic else 0
                        print(f"{l} | Prioridad Familiar: {prio_fam}")
                    id_lic = int(input("Ingrese ID de la licencia a evaluar: "))
                    accion = input("¿Desea aprobarla? (s = aprobar / n = rechazar): ").strip().lower()
                    lic = sistema.supervisor_gestionar_licencia(id_lic, aprobar=(accion == "s"))
                    print(f"Licencia #{lic.id_licencia} actualizada a estado: {lic.estado}")

                elif opcion == "4" and es_supervisor:
                    print("--- Licencias ordenadas por Prioridad Familiar y Preferencia (Bubble Sort) ---")
                    for lic in ordenar_licencias_por_preferencia(sistema.licencias, mapa_colabs):
                        colab_lic = mapa_colabs.get(lic.colaborador_legajo)
                        prio_fam = colab_lic.nivel_prioridad if colab_lic else 0
                        print(f"{lic} | Prioridad Familiar: {prio_fam}")

                # --- Opciones exclusivas de ADMINISTRADOR RRHH ---
                elif opcion == "3" and es_admin:
                    aprobadas = ordenar_licencias_por_preferencia(
                        [l for l in sistema.licencias if l.estado == "aprobada"],
                        mapa_colabs,
                    )
                    if not aprobadas:
                        print("No hay licencias aprobadas pendientes de confirmación.")
                        continue
                    print("--- Licencias aprobadas (ordenadas por prioridad familiar y preferencia) ---")
                    for l in aprobadas:
                        colab_lic = mapa_colabs.get(l.colaborador_legajo)
                        prio_fam = colab_lic.nivel_prioridad if colab_lic else 0
                        print(f"{l} | Prioridad Familiar: {prio_fam}")
                    id_lic = int(input("Ingrese ID de la licencia aprobada a resolver: "))
                    accion = input("¿Confirmar licencia? (s = confirmar / n = rechazar): ").strip().lower()
                    lic = sistema.admin_confirmar_licencia(id_lic, confirmar=(accion == "s"))
                    print(f"Licencia #{lic.id_licencia} actualizada a estado: {lic.estado}")

                elif opcion == "4" and es_admin:
                    legajo = int(input("Legajo: "))
                    nombre = input("Nombre: ").strip()
                    apellido = input("Apellido: ").strip()
                    dni = int(input("DNI: "))
                    area = input("Área (ej. Customer Care): ").strip()
                    email = input("Email corporativo: ").strip()
                    hijos = input("¿Tiene hijos? (s/n): ").strip().lower() == "s"
                    casado = input("¿Está casado/a? (s/n): ").strip().lower() == "s"

                    nuevo = sistema.cu10_alta_colaborador(
                        legajo, nombre, apellido, dni, date.today(), area, email, hijos, casado
                    )
                    print(f"Colaborador creado: {nuevo}")
                    print(
                        f"Credenciales generadas -> Usuario: {nuevo.usuario} | Contraseña: {nuevo.contrasena}"
                    )

                elif opcion == "5" and es_admin:
                    print("--- Licencias ordenadas por Prioridad Familiar y Preferencia (Bubble Sort) ---")
                    for lic in ordenar_licencias_por_preferencia(sistema.licencias, mapa_colabs):
                        colab_lic = mapa_colabs.get(lic.colaborador_legajo)
                        prio_fam = colab_lic.nivel_prioridad if colab_lic else 0
                        print(f"{lic} | Prioridad Familiar: {prio_fam}")

                elif opcion == "6" and es_admin:
                    print("--- Colaboradores ordenados por Prioridad Familiar (Bubble Sort) ---")
                    for col in ordenar_colaboradores_por_prioridad(sistema.colaboradores):
                        print(col)

                # --- Cerrar sesión y Salir ---
                elif opcion == "9":
                    sistema.cu1_logout()
                    print("Sesión cerrada correctamente.")

                elif opcion == "0":
                    print("Saliendo del sistema...")
                    break
                else:
                    print("Opción inválida para su nivel de jerarquía.")

            except Exception as e:
                print(f"[ERROR]: {e}")


if __name__ == "__main__":
    mostrar_menu()
from Models.clases import Licencia, Colaborador


def ordenar_licencias_por_preferencia(
    licencias: list[Licencia],
    colaboradores_por_legajo: dict[int, Colaborador] | None = None,
) -> list[Licencia]:
    """
    Ordenamiento Burbuja (Bubble Sort):
    1. Si se proveen colaboradores, ordena primero por prioridad familiar descendente (3=casado, 1=hijos, 0=sin cargas).
    2. A igual prioridad familiar (o si no se proveen colaboradores), ordena por preferencia ascendente (1=máxima, 3=mínima).
    """
    lista = licencias.copy()
    n = len(lista)

    def clave_orden(lic: Licencia) -> tuple[int, int]:
        prio_familiar = 0
        if colaboradores_por_legajo and lic.colaborador_legajo in colaboradores_por_legajo:
            prio_familiar = colaboradores_por_legajo[lic.colaborador_legajo].nivel_prioridad
        pref_orden = lic.nivel_preferencia if lic.nivel_preferencia is not None else 99
        return (-prio_familiar, pref_orden)

    for i in range(n):
        for j in range(0, n - i - 1):
            if clave_orden(lista[j]) > clave_orden(lista[j + 1]):
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista


def ordenar_colaboradores_por_prioridad(
    colaboradores: list[Colaborador],
) -> list[Colaborador]:
    """
    Ordenamiento Burbuja (Bubble Sort) descendente por nivel_prioridad
    (3 = casado, 1 = con hijos, 0 = sin cargas).
    """
    lista = colaboradores.copy()
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j].nivel_prioridad < lista[j + 1].nivel_prioridad:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista
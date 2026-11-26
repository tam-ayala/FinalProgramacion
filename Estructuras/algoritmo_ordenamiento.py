from Models.clases import Licencia, Colaborador


def ordenar_licencias_merge_sort(
    licencias: list[Licencia],
    colaboradores_por_legajo: dict[int, Colaborador] | None = None,
) -> list[Licencia]:
    """
    Ordena licencias mediante Merge Sort.

    Criterios:
    1. Prioridad familiar ascendente (1 = máxima, 2 = intermedia, 3 = mínima).
    2. Preferencia ascendente (1 = primera opción).
    3. Mantiene el orden original cuando ambas prioridades coinciden.

    Complejidad temporal: O(n log n).
    Complejidad espacial: O(n).
    """

    def obtener_clave(licencia: Licencia) -> tuple[int, int]:
        prioridad_familiar = 3

        if (
            colaboradores_por_legajo is not None
            and licencia.colaborador_legajo in colaboradores_por_legajo
        ):
            colaborador = colaboradores_por_legajo[
                licencia.colaborador_legajo
            ]
            prioridad_familiar = colaborador.nivel_prioridad

        preferencia = (
            licencia.nivel_preferencia
            if licencia.nivel_preferencia is not None
            else 99
        )

        return (prioridad_familiar, preferencia)

    def fusionar(
        mitad_izquierda: list[Licencia],
        mitad_derecha: list[Licencia],
    ) -> list[Licencia]:
        resultado = []
        indice_izquierda = 0
        indice_derecha = 0

        # Comparamos los elementos de ambas mitades.
        while (
            indice_izquierda < len(mitad_izquierda)
            and indice_derecha < len(mitad_derecha)
        ):
            licencia_izquierda = mitad_izquierda[indice_izquierda]
            licencia_derecha = mitad_derecha[indice_derecha]

            if (
                obtener_clave(licencia_izquierda)
                <= obtener_clave(licencia_derecha)
            ):
                resultado.append(licencia_izquierda)
                indice_izquierda += 1
            else:
                resultado.append(licencia_derecha)
                indice_derecha += 1

        # Incorporamos los elementos restantes.
        resultado.extend(mitad_izquierda[indice_izquierda:])
        resultado.extend(mitad_derecha[indice_derecha:])

        return resultado

    def merge_sort(lista: list[Licencia]) -> list[Licencia]:
        # Caso base: una lista de cero o un elemento ya está ordenada.
        if len(lista) <= 1:
            return lista

        punto_medio = len(lista) // 2

        # Dividimos la lista en dos mitades.
        mitad_izquierda = merge_sort(lista[:punto_medio])
        mitad_derecha = merge_sort(lista[punto_medio:])

        # Fusionamos las dos mitades ordenadas.
        return fusionar(mitad_izquierda, mitad_derecha)

    return merge_sort(licencias.copy())
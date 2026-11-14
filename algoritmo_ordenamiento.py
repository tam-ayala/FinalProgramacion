def ordenar_licencias_por_prioridad(licencias: list) -> list:
    """
    Ordena una lista de objetos Licencia por el atributo nivel_preferencia
    utilizando el algoritmo Bubble Sort.
    """
    n = len(licencias)
    for i in range(n):
        for j in range(0, n - i - 1):
            if licencias[j].nivel_preferencia > licencias[j + 1].nivel_preferencia:
                licencias[j], licencias[j + 1] = licencias[j + 1], licencias[j]
    return licencias
def comparar_binarios(b1, b2):
    """Retorna el binario con un guion si solo difieren en 1 bit, sino None."""
    diferencias = 0
    posicion = -1
    res = list(b1)
    for i in range(len(b1)):
        if b1[i] != b2[i]:
            diferencias += 1
            posicion = i
    if diferencias == 1:
        res[posicion] = '-'
        return "".join(res)
    return None

def obtener_implicantes_primos(num_vars, minterms, dont_cares):
    """Paso 1 y 2 de QM: Agrupación y Reducción."""
    terminos = sorted(list(set(minterms + dont_cares)))
    tabla = {}
    for t in terminos:
        b = bin(t).replace('0b', '').zfill(num_vars)
        unos = b.count('1')
        tabla.setdefault(unos, []).append(b)

    implicantes_primos = set()
    while True:
        nueva_tabla = {}
        usados = set()
        encontrado = False
        claves = sorted(tabla.keys())

        for i in range(len(claves) - 1):
            for b1 in tabla[claves[i]]:
                for b2 in tabla[claves[i+1]]:
                    combinado = comparar_binarios(b1, b2)
                    if combinado:
                        encontrado = True
                        usados.add(b1)
                        usados.add(b2)
                        nueva_tabla.setdefault(combinado.count('1'), []).append(combinado)
                        # Limpiar duplicados en el nuevo nivel
                        nueva_tabla[combinado.count('1')] = list(set(nueva_tabla[combinado.count('1')]))

        for g in tabla.values():
            for b in g:
                if b not in usados:
                    implicantes_primos.add(b)

        if not encontrado: break
        tabla = nueva_tabla
    return list(implicantes_primos)

def cubre_minterm(implicante, minterm_bin):
    """Verifica si un implicante (con guiones) cubre un minterm específico."""
    for i in range(len(implicante)):
        if implicante[i] != '-' and implicante[i] != minterm_bin[i]:
            return False
    return True

def resolver_cobertura(implicantes, minterms, num_vars):
    """Paso 3: Tabla de implicantes primos para encontrar la solución mínima."""
    minterms_bin = [bin(m).replace('0b', '').zfill(num_vars) for m in minterms]
    seleccionados = []
    restantes = list(minterms_bin)

    # Bucle simple de cobertura (Greedy)
    while restantes:
        # Encontrar el implicante que cubra más minterms restantes
        mejor_implicante = None
        max_cubiertos = -1
        para_eliminar = []

        for imp in implicantes:
            cubiertos_ahora = [m for m in restantes if cubre_minterm(imp, m)]
            if len(cubiertos_ahora) > max_cubiertos:
                max_cubiertos = len(cubiertos_ahora)
                mejor_implicante = imp
                para_eliminar = cubiertos_ahora

        if mejor_implicante:
            seleccionados.append(mejor_implicante)
            for m in para_eliminar:
                restantes.remove(m)
        else: break

    return seleccionados

def formatear_ecuacion(implicantes, nombres_vars):
    """Convierte binarios con guiones a álgebra booleana."""
    terminos_finales = []
    for imp in implicantes:
        partes = []
        for i, bit in enumerate(imp):
            if bit == '1':
                partes.append(nombres_vars[i])
            elif bit == '0':
                partes.append(f"{nombres_vars[i]}'")
        terminos_finales.append("".join(partes))
    return " + ".join(terminos_finales) if terminos_finales else "0"

def procesar_funcion(nombre_salida, nombres_vars):
    print(f"\n--- Configuración para {nombre_salida} ---")
    m_input = input(f"Ingrese Minterms de {nombre_salida} separados por coma: ")
    d_input = input(f"Ingrese Don't Cares (X) separados por coma (Enter si no hay): ")

    minterms = [int(x.strip()) for x in m_input.split(',')] if m_input else []
    dont_cares = [int(x.strip()) for x in d_input.split(',')] if d_input else []

    num_vars = len(nombres_vars)
    primos = obtener_implicantes_primos(num_vars, minterms, dont_cares)
    minimos = resolver_cobertura(primos, minterms, num_vars)
    ecuacion = formatear_ecuacion(minimos, nombres_vars)

    print(f"RESULTADO {nombre_salida}: {ecuacion}")
    return ecuacion
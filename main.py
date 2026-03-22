import quinemccluskey as qm

print("="*50)
print("  ALGORITMO DE QUINE-MCCLUSKEY")
print("="*50)

    # 1. CONFIGURACIÓN DE ENTRADAS (Variables) 
while True:
    try:
        num_vars = int(input("\nIngrese el número de variables de entrada (ej. 4, 5): "))
        break
    except ValueError:
        print("Error: Ingrese un número entero válido.")

nombres_vars = input(f"Ingrese los nombres de las {num_vars} variables separados por espacio (ej. A B C D): ").split()
    
    # Validación de cantidad
while len(nombres_vars) != num_vars:
    print(f"Error: Ingresó {len(nombres_vars)} nombres, pero indicó que eran {num_vars} variables.")
    nombres_vars = input(f"Vuelva a ingresar los {num_vars} nombres separados por espacio: ").split()

    # 2. CONFIGURACIÓN DE SALIDAS (Funciones)
while True:
    try:
        num_salidas = int(input("\nIngrese el número de salidas (ej. 1, 2): "))
        break
    except ValueError:
        print("Error: Ingrese un número entero válido.")

nombres_salidas = input(f"Ingrese los nombres de las {num_salidas} salidas separados por espacio (ej. Q1+ Q0+ F1): ").split()
    
    # Validación de cantidad
while len(nombres_salidas) != num_salidas:
    print(f"Error: Ingresó {len(nombres_salidas)} nombres, pero indicó que eran {num_salidas} salidas.")
    nombres_salidas = input(f"Vuelva a ingresar los {num_salidas} nombres separados por espacio: ").split()

    # 3. PROCESAMIENTO
resultados = {}
    
for salida in nombres_salidas:
        # Se llama a la función original para cada salida
        resultados[salida] = qm.procesar_funcion(salida, nombres_vars)

    # 4. RESUMEN  
print("\n" + "="*50)
print("               RESUMEN DE MINIMIZACIÓN")
print("="*50)
for salida, ecuacion in resultados.items():
        print(f"{salida} = {ecuacion}")
print("="*50)
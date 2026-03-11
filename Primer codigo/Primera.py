import heapq

# --- ENFOQUE 1: SISTEMA SIMBÓLICO (Base de Conocimientos y Reglas) ---
def obtener_reglas_trafico(hora):
    """Simula el conocimiento de un experto sobre la ciudad."""
    # Regla: Entre las 17 y 19 horas, la Avenida Central es un caos.
    if 17 <= hora <= 19:
        return {"Av_Central": 10, "Calle_Norte": 2, "Calle_Sur": 1}
    # Regla: Por la noche, la Calle Sur es peligrosa (aumentamos 'costo' por riesgo).
    elif hora >= 21 or hora <= 5:
        return {"Av_Central": 1, "Calle_Norte": 1, "Calle_Sur": 15}
    else:
        return {"Av_Central": 1, "Calle_Norte": 1, "Calle_Sur": 1}

# --- ENFOQUE 2: BÚSQUEDA HEURÍSTICA (Algoritmo A*) ---
def a_estrella(grafo, inicio, meta, trafico, heuristicas):
    # priority_queue: (prioridad, costo_real, nodo_actual, camino)
    frontera = [(0 + heuristicas[inicio], 0, inicio, [])]
    visitados = set()

    while frontera:
        f_n, g_n, nodo_actual, camino = heapq.heappop(frontera)

        if nodo_actual in visitados:
            continue
        
        camino = camino + [nodo_actual]

        if nodo_actual == meta:
            return camino, g_n

        visitados.add(nodo_actual)

        for vecino, distancia_base in grafo.get(nodo_actual, {}).items():
            if vecino not in visitados:
                # El peso se ve afectado por las reglas del experto (tráfico)
                multiplicador = trafico.get(vecino, 1)
                nuevo_g_n = g_n + (distancia_base * multiplicador)
                f_n_vecino = nuevo_g_n + heuristicas.get(vecino, 0)
                heapq.heappush(frontera, (f_n_vecino, nuevo_g_n, vecino, camino))
    return None, 0

# --- ENFOQUE 3: EXPLICACIÓN (Árbol de Decisión / Justificación) ---
def mostrar_arbol_decision(camino, trafico, hora):
    print("\n" + "="*40)
    print(f"🌳 ÁRBOL DE DECISIÓN DEL EXPERTO (Hora: {hora}:00)")
    print("="*40)
    print(f"Inicio: {camino[0]}")
    
    for i in range(len(camino) - 1):
        actual = camino[i]
        siguiente = camino[i+1]
        peso_extra = trafico.get(siguiente, 1)
        
        print(f"  |")
        print(f"  └──> ¿Ir por {siguiente}?")
        if peso_extra >= 10:
            print(f"       [!] RECHAZADO: Regla de Tráfico Pesado detectada.")
        elif peso_extra > 1 and peso_extra < 10:
            print(f"       [?] PRECAUCIÓN: Retraso moderado, pero aceptable.")
        else:
            print(f"       [✓] ACEPTADO: Ruta despejada según base de conocimientos.")
    
    print(f"  |")
    print(f"  └──> DESTINO ALCANZADO: {camino[-1]}")

# --- CONFIGURACIÓN DEL CASO ---
mapa = {
    'Farmacia': {'Av_Central': 5, 'Calle_Norte': 3},
    'Av_Central': {'Hospital': 10},
    'Calle_Norte': {'Calle_Sur': 2, 'Hospital': 8},
    'Calle_Sur': {'Hospital': 2}
}

# Heurística: Distancia en línea recta "al ojo" hasta el Hospital
distancias_estimadas = {'Farmacia': 12, 'Av_Central': 8, 'Calle_Norte': 6, 'Calle_Sur': 2, 'Hospital': 0}

# --- EJECUCIÓN ---
def ejecutar_sistema(hora_actual):
    print(f"\n--- Iniciando Sistema Experto de Rutas ---")
    reglas = obtener_reglas_trafico(hora_actual)
    ruta, costo = a_estrella(mapa, 'Farmacia', 'Hospital', reglas, distancias_estimadas)
    
    if ruta:
        print(f"Ruta óptima encontrada: {' -> '.join(ruta)}")
        print(f"Costo logístico total: {costo}")
        mostrar_arbol_decision(ruta, reglas, hora_actual)
    else:
        print("No se encontró una ruta segura.")

# Probar con hora pico (18:00)
ejecutar_sistema(18)
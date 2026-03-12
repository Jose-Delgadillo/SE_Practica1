import tkinter as tk
import heapq

# --- 1. BASE DE CONOCIMIENTOS (Grafo de 11 nodos, 3 rutas principales) ---
# Caso de la vida diaria: Un camión de reparto saliendo del Almacén hacia el Cliente.
MAPA = {
    'Almacen': {'Norte_1': 15, 'Centro_1': 10, 'Sur_1': 20},
    
    # Ruta 1 (Norte) - Parece rápida al principio, pero se complica
    'Norte_1': {'Norte_2': 10, 'Desvio_N': 25},
    'Norte_2': {'Cliente': 30},
    'Desvio_N': {'Cliente': 10},
    
    # Ruta 2 (Centro) - Mucho tráfico en el medio
    'Centro_1': {'Centro_2': 25, 'Atajo_C': 40},
    'Centro_2': {'Cliente': 15},
    'Atajo_C': {'Cliente': 5},
    
    # Ruta 3 (Sur) - Larga al inicio, muy rápida al final (ÓPTIMA)
    'Sur_1': {'Sur_2': 12, 'Desvio_S': 15},
    'Sur_2': {'Cliente': 8},
    'Desvio_S': {'Cliente': 20},
    
    'Cliente': {}
}

# Coordenadas para el MAPA (Lado Izquierdo)
POS_MAPA = {
    'Almacen': (50, 250),
    'Norte_1': (150, 100), 'Norte_2': (300, 50), 'Desvio_N': (300, 150),
    'Centro_1': (150, 250), 'Centro_2': (300, 220), 'Atajo_C': (300, 280),
    'Sur_1': (150, 400), 'Sur_2': (300, 350), 'Desvio_S': (300, 450),
    'Cliente': (450, 250)
}

# Coordenadas para el ÁRBOL (Lado Derecho)
POS_ARBOL = {
    'Almacen': (700, 30),
    # Nivel 1
    'Norte_1': (550, 120), 'Centro_1': (700, 120), 'Sur_1': (850, 120),
    # Nivel 2
    'Norte_2': (500, 250), 'Desvio_N': (600, 250),
    'Centro_2': (650, 250), 'Atajo_C': (750, 250),
    'Sur_2': (820, 250), 'Desvio_S': (900, 250),
    # Nivel 3 (Múltiples llegadas al cliente para mostrar comparación)
    'C_N1': (500, 380), 'C_N2': (600, 380),
    'C_C1': (650, 380), 'C_C2': (750, 380),
    'C_S1': (820, 380), 'C_S2': (900, 380)
}

# --- 2. MOTOR DE BÚSQUEDA (Dijkstra) ---
def buscar_ruta_y_generar_arbol(inicio, meta):
    cola = [(0, inicio, [])]
    costos_minimos = {inicio: 0}
    
    # Guardamos TODAS las exploraciones para dibujar el árbol
    historial_arbol = []
    ruta_final = []
    costo_final = float('inf')

    while cola:
        costo_actual, nodo_actual, camino = heapq.heappop(cola)
        camino = camino + [nodo_actual]

        if nodo_actual == meta:
            if costo_actual < costo_final:
                costo_final = costo_actual
                ruta_final = camino
            continue

        for vecino, peso in MAPA[nodo_actual].items():
            nuevo_costo = costo_actual + peso
            
            # El experto registra la evaluación para el árbol
            estado = "Explorando"
            if vecino not in costos_minimos or nuevo_costo < costos_minimos[vecino]:
                costos_minimos[vecino] = nuevo_costo
                heapq.heappush(cola, (nuevo_costo, vecino, camino))
                estado = "Viable"
            else:
                estado = "Descartado (Más caro)"
                
            historial_arbol.append((nodo_actual, vecino, nuevo_costo, estado))

    return ruta_final, costo_final, historial_arbol

# --- 3. INTERFAZ GRÁFICA ---
class AppRutaExperta:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Algoritmo Dijkstra con Árbol de Exploración")
        # Ventana ancha para que quepa el mapa y el gran árbol
        self.canvas = tk.Canvas(root, width=1000, height=600, bg="#F4F6F6")
        self.canvas.pack()

        self.ruta, self.costo, self.historial = buscar_ruta_y_generar_arbol('Almacen', 'Cliente')
        
        self.dibujar_interfaz()

    def dibujar_interfaz(self):
        # Separador visual
        self.canvas.create_line(500, 0, 500, 600, fill="gray", dash=(4,4))
        self.canvas.create_text(250, 30, text="1. GRAFO DE LA CIUDAD (MAPA)", font=("Arial", 14, "bold"))
        self.canvas.create_text(750, 30, text="2. ÁRBOL DE DECISIÓN DEL EXPERTO", font=("Arial", 14, "bold"))

        self.dibujar_mapa()
        self.dibujar_arbol()

    def dibujar_mapa(self):
        # Dibujar líneas del mapa
        for origen, vecinos in MAPA.items():
            x1, y1 = POS_MAPA[origen]
            for dest, peso in vecinos.items():
                x2, y2 = POS_MAPA[dest]
                es_optima = (origen in self.ruta and dest in self.ruta and self.ruta.index(dest) == self.ruta.index(origen)+1)
                color = "#2ECC71" if es_optima else "#BDC3C7"
                ancho = 5 if es_optima else 2
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2 - 10, text=f"{peso}m", font=("Arial", 9, "bold"), fill="#34495E")

        # Dibujar nodos del mapa
        for nodo, (x, y) in POS_MAPA.items():
            color = "#F39C12" if nodo in self.ruta else "#34495E"
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black")
            self.canvas.create_text(x, y+30, text=nodo, font=("Arial", 9, "bold"))

    def nodo_arbol(self, x, y, texto, color="#E8F8F5", ancho=80):
        self.canvas.create_rectangle(x-ancho/2, y-20, x+ancho/2, y+20, fill=color, outline="black")
        self.canvas.create_text(x, y, text=texto, font=("Arial", 8), justify="center")

    def dibujar_arbol(self):
        # Relaciones padre-hijo manuales para dibujar el árbol perfectamente alineado
        relaciones = {
            'Almacen': [('Norte_1', 15), ('Centro_1', 10), ('Sur_1', 20)],
            'Norte_1': [('Norte_2', 25), ('Desvio_N', 40)],
            'Centro_1': [('Centro_2', 35), ('Atajo_C', 50)],
            'Sur_1': [('Sur_2', 32), ('Desvio_S', 35)],
            'Norte_2': [('C_N1', 55)], 'Desvio_N': [('C_N2', 50)],
            'Centro_2': [('C_C1', 50)], 'Atajo_C': [('C_C2', 55)],
            'Sur_2': [('C_S1', 40)], 'Desvio_S': [('C_S2', 55)]
        }

        # Dibujar líneas del árbol
        for padre, hijos in relaciones.items():
            x1, y1 = POS_ARBOL[padre]
            for hijo, costo_acumulado in hijos:
                hijo_limpio = hijo if not hijo.startswith('C_') else 'Cliente'
                x2, y2 = POS_ARBOL[hijo]
                
                # Identificar si este enlace es parte de la ruta ganadora
                es_ganador = (padre in self.ruta and hijo_limpio in self.ruta and self.ruta.index(hijo_limpio) == self.ruta.index(padre)+1)
                color_linea = "#27AE60" if es_ganador else "#A6ACAF"
                ancho_linea = 3 if es_ganador else 1
                dash_style = None if es_ganador else (4,4)
                
                self.canvas.create_line(x1, y1+20, x2, y2-20, fill=color_linea, width=ancho_linea, dash=dash_style, arrow=tk.LAST)

        # Dibujar los nodos del árbol con sus costos acumulados
        for nodo, (x, y) in POS_ARBOL.items():
            nombre_real = nodo if not nodo.startswith('C_') else 'Cliente'
            color = "#ABEBC6" if nombre_real in self.ruta else "#FDEDEC"
            
            # Buscar el costo acumulado para este nodo
            costo_txt = ""
            for p, h_list in relaciones.items():
                for h, c in h_list:
                    if h == nodo: costo_txt = f"\nTotal: {c}m"

            texto_nodo = f"{nombre_real}{costo_txt}"
            if nodo == 'Almacen': texto_nodo = "RAÍZ\nAlmacén"
            
            self.nodo_arbol(x, y, texto_nodo, color)

        # Veredicto debajo del árbol
        texto_final = (f"EL EXPERTO CONCLUYE:\n"
                       f"Se exploraron 3 rutas principales y 6 variantes.\n"
                       f"Ruta óptima: {' -> '.join(self.ruta)}\n"
                       f"Tiempo total: {self.costo} minutos.")
        self.canvas.create_text(750, 480, text=texto_final, font=("Arial", 11, "bold"), fill="#145A32", justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRutaExperta(root)
    root.mainloop()
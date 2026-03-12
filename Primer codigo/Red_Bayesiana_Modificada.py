import tkinter as tk
import heapq

# --- 1. BASE DE CONOCIMIENTOS (Grafo de 11 nodos) ---
MAPA = {
    'Almacen': {'Norte_1': 15, 'Centro_1': 10, 'Sur_1': 20},
    
    'Norte_1': {'Norte_2': 10, 'Desvio_N': 25},
    'Norte_2': {'Cliente': 30},
    'Desvio_N': {'Cliente': 10},
    
    'Centro_1': {'Centro_2': 25, 'Atajo_C': 40},
    'Centro_2': {'Cliente': 15},
    'Atajo_C': {'Cliente': 5},
    
    'Sur_1': {'Sur_2': 12, 'Desvio_S': 15},
    'Sur_2': {'Cliente': 8},
    'Desvio_S': {'Cliente': 20},
    
    'Cliente': {}
}

# Coordenadas ajustadas y centradas para el mapa
POS_MAPA = {
    'Almacen': (100, 250),
    'Norte_1': (250, 100), 'Norte_2': (400, 50), 'Desvio_N': (400, 150),
    'Centro_1': (250, 250), 'Centro_2': (400, 220), 'Atajo_C': (400, 280),
    'Sur_1': (250, 400), 'Sur_2': (400, 350), 'Desvio_S': (400, 450),
    'Cliente': (550, 250)
}

# --- 2. MOTOR DE BÚSQUEDA (Dijkstra) ---
def buscar_ruta(inicio, meta):
    cola = [(0, inicio, [])]
    costos_minimos = {inicio: 0}
    
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
            
            if vecino not in costos_minimos or nuevo_costo < costos_minimos[vecino]:
                costos_minimos[vecino] = nuevo_costo
                heapq.heappush(cola, (nuevo_costo, vecino, camino))

    return ruta_final, costo_final

# --- 3. INTERFAZ GRÁFICA (Solo el Grafo) ---
class AppGrafo:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Grafo de Rutas (Dijkstra)")
        self.canvas = tk.Canvas(root, width=700, height=550, bg="#F4F6F6")
        self.canvas.pack()

        self.ruta, self.costo = buscar_ruta('Almacen', 'Cliente')
        self.dibujar_interfaz()

    def dibujar_interfaz(self):
        self.canvas.create_text(350, 30, text="MAPA DE RUTAS (GRAFO)", font=("Arial", 16, "bold"))
        
        # Dibujar las conexiones (aristas)
        for origen, vecinos in MAPA.items():
            x1, y1 = POS_MAPA[origen]
            for dest, peso in vecinos.items():
                x2, y2 = POS_MAPA[dest]
                es_optima = (origen in self.ruta and dest in self.ruta and self.ruta.index(dest) == self.ruta.index(origen)+1)
                
                color = "#2ECC71" if es_optima else "#BDC3C7"
                ancho = 5 if es_optima else 2
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)
                
                # Texto del peso (minutos)
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2 - 12, text=f"{peso}m", font=("Arial", 10, "bold"), fill="#34495E")

        # Dibujar las ubicaciones (nodos)
        for nodo, (x, y) in POS_MAPA.items():
            color = "#F39C12" if nodo in self.ruta else "#34495E"
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black")
            self.canvas.create_text(x, y+30, text=nodo, font=("Arial", 10, "bold"))

        # Veredicto final en la parte inferior
        texto_final = (f"VERDICTO DEL EXPERTO:\n"
                       f"Ruta óptima encontrada: {' -> '.join(self.ruta)}\n"
                       f"Tiempo total: {self.costo} minutos.")
        self.canvas.create_text(350, 500, text=texto_final, font=("Arial", 12, "bold"), fill="#145A32", justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGrafo(root)
    root.mainloop()
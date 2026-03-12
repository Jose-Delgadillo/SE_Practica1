import tkinter as tk
import heapq

# --- 1. BASE DE CONOCIMIENTOS (Tráfico post-partido) ---
MAPA = {
    'Estadio_Akron': {'JVC_Norte': 30, 'Periferico': 25, 'JVC_Sur': 15},
    
    'JVC_Norte': {'Vallarta_Concentro': 12, 'Galerias': 20},
    'Vallarta_Concentro': {'Tacos_Chapalita': 35},
    'Galerias': {'Tacos_Chapalita': 15},
    
    'Periferico': {'P_Metropolitano': 10, 'Rafael_Sanzio': 15},
    'P_Metropolitano': {'Tacos_Chapalita': 25},
    'Rafael_Sanzio': {'Tacos_Chapalita': 12},
    
    'JVC_Sur': {'Guadalupe': 18, 'Tepeyac': 22},
    'Guadalupe': {'Tacos_Chapalita': 20},
    'Tepeyac': {'Tacos_Chapalita': 25},
    
    'Tacos_Chapalita': {}
}

POS_MAPA = {
    'Estadio_Akron': (100, 325),
    
    'JVC_Norte': (275, 125), 
    'Vallarta_Concentro': (475, 50), 
    'Galerias': (475, 175),
    
    'Periferico': (275, 325), 
    'P_Metropolitano': (475, 300), 
    'Rafael_Sanzio': (475, 400),
    
    'JVC_Sur': (275, 525), 
    'Guadalupe': (475, 500), 
    'Tepeyac': (475, 600),
    
    'Tacos_Chapalita': (700, 325)
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

# --- 3. INTERFAZ GRÁFICA ---
class AppGrafoRestaurantes:
    def __init__(self, root):
        self.root = root
        self.root.title("Rutas Gastronómicas: Salida Estadio Akron")
        self.canvas = tk.Canvas(root, width=800, height=720, bg="#EAF2F8") # Fondo azul tenue
        self.canvas.pack()

        self.ruta, self.costo = buscar_ruta('Estadio_Akron', 'Tacos_Chapalita')
        self.dibujar_interfaz()

    def dibujar_interfaz(self):
        self.canvas.create_text(400, 30, text="SALIDA DEL AKRON: RUTA A CENAR", font=("Arial", 16, "bold"), fill="#154360")
        
        # 3.1 Dibujar conexiones
        for origen, vecinos in MAPA.items():
            x1, y1 = POS_MAPA[origen]
            for dest, peso in vecinos.items():
                x2, y2 = POS_MAPA[dest]
                es_optima = (origen in self.ruta and dest in self.ruta and self.ruta.index(dest) == self.ruta.index(origen)+1)
                
                color = "#2980B9" if es_optima else "#BDC3C7" # Azul si es óptima
                ancho = 5 if es_optima else 2
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2 - 15, text=f"{peso}m", font=("Arial", 10, "bold"), fill="#154360")

        # 3.2 Dibujar ubicaciones
        for nodo, (x, y) in POS_MAPA.items():
            color = "#F39C12" if nodo in self.ruta else "#34495E"
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline="black")
            texto_limpio = nodo.replace("_", " ")
            self.canvas.create_text(x, y+35, text=texto_limpio, font=("Arial", 9, "bold"))

        # 3.3 Veredicto
        texto_final = (f"VEREDICTO DE TU COPILOTO:\n"
                       f"Ruta más rápida para cenar: {' -> '.join([n.replace('_', ' ') for n in self.ruta])}\n"
                       f"Tiempo de viaje sorteando el tráfico: {self.costo} minutos.")
        self.canvas.create_text(400, 680, text=texto_final, font=("Arial", 13, "bold"), fill="#154360", justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGrafoRestaurantes(root)
    root.mainloop()
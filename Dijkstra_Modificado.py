import tkinter as tk
import heapq

# --- 1. BASE DE CONOCIMIENTOS (Calles de GDL) ---
MAPA = {
    'Accidente_Minerva': {'Lopez_Mateos_N': 5, 'Vallarta': 8, 'Lopez_Mateos_S': 10},
    
    'Lopez_Mateos_N': {'Americas': 12, 'Terranova': 15},
    'Americas': {'Hosp_San_Javier': 10},
    'Terranova': {'Hosp_San_Javier': 5},
    
    'Vallarta': {'Las_Rosas': 15, 'Golfo_Mexico': 10},
    'Las_Rosas': {'Hosp_San_Javier': 18},
    'Golfo_Mexico': {'Hosp_San_Javier': 12},
    
    'Lopez_Mateos_S': {'Ninos_Heroes': 14, 'Washington': 20},
    'Ninos_Heroes': {'Hosp_San_Javier': 25},
    'Washington': {'Hosp_San_Javier': 30},
    
    'Hosp_San_Javier': {}
}

# Coordenadas respetando tu plantilla original para que no se encimen
POS_MAPA = {
    'Accidente_Minerva': (100, 325),
    
    'Lopez_Mateos_N': (275, 125), 
    'Americas': (475, 50), 
    'Terranova': (475, 175),
    
    'Vallarta': (275, 325), 
    'Las_Rosas': (475, 300), 
    'Golfo_Mexico': (475, 400),
    
    'Lopez_Mateos_S': (275, 525), 
    'Ninos_Heroes': (475, 500), 
    'Washington': (475, 600),
    
    'Hosp_San_Javier': (700, 325)
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
class AppGrafoHospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Emergencia Médica GDL: Ruta más rápida")
        self.canvas = tk.Canvas(root, width=800, height=720, bg="#F9EBEA") # Fondo rojizo tenue
        self.canvas.pack()

        self.ruta, self.costo = buscar_ruta('Accidente_Minerva', 'Hosp_San_Javier')
        self.dibujar_interfaz()

    def dibujar_interfaz(self):
        self.canvas.create_text(400, 30, text="EMERGENCIA GDL: MAPA DE RUTAS AL HOSPITAL", font=("Arial", 16, "bold"), fill="#922B21")
        
        # 3.1 Dibujar conexiones
        for origen, vecinos in MAPA.items():
            x1, y1 = POS_MAPA[origen]
            for dest, peso in vecinos.items():
                x2, y2 = POS_MAPA[dest]
                es_optima = (origen in self.ruta and dest in self.ruta and self.ruta.index(dest) == self.ruta.index(origen)+1)
                
                color = "#E74C3C" if es_optima else "#BDC3C7" # Rojo si es óptima
                ancho = 5 if es_optima else 2
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)
                self.canvas.create_text((x1+x2)/2, (y1+y2)/2 - 15, text=f"{peso}m", font=("Arial", 10, "bold"), fill="#641E16")

        # 3.2 Dibujar ubicaciones
        for nodo, (x, y) in POS_MAPA.items():
            color = "#F1C40F" if nodo in self.ruta else "#34495E"
            self.canvas.create_oval(x-25, y-25, x+25, y+25, fill=color, outline="black")
            texto_limpio = nodo.replace("_", " ")
            self.canvas.create_text(x, y+35, text=texto_limpio, font=("Arial", 9, "bold"))

        # 3.3 Veredicto
        texto_final = (f"VEREDICTO DEL GPS DE LA AMBULANCIA:\n"
                       f"Ruta óptima calculada: {' -> '.join([n.replace('_', ' ') for n in self.ruta])}\n"
                       f"Tiempo estimado de llegada: {self.costo} minutos.")
        self.canvas.create_text(400, 680, text=texto_final, font=("Arial", 13, "bold"), fill="#922B21", justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGrafoHospital(root)
    root.mainloop()
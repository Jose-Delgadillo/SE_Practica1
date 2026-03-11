import heapq
import tkinter as tk
from tkinter import messagebox

# --- 1. ENFOQUE SIMBÓLICO (Reglas del Experto) ---
# Definimos el mapa: Conexiones y distancias base
MAPA = {
    'Farmacia': {'Av_Central': 5, 'Calle_Norte': 3},
    'Av_Central': {'Hospital': 10},
    'Calle_Norte': {'Calle_Sur': 2, 'Hospital': 8},
    'Calle_Sur': {'Hospital': 2},
    'Hospital': {}
}

# Coordenadas para dibujar los nodos en la pantalla (X, Y)
POSICIONES = {
    'Farmacia': (50, 150),
    'Av_Central': (200, 50),
    'Calle_Norte': (200, 250),
    'Calle_Sur': (350, 250),
    'Hospital': (500, 150)
}

def obtener_reglas_trafico(hora):
    """Reglas expertas: Devuelven penalización por tráfico/riesgo."""
    if 17 <= hora <= 19: # Hora pico en la avenida
        return {"Av_Central": 10, "Calle_Norte": 1, "Calle_Sur": 1}
    elif 22 <= hora or hora <= 5: # Noche (Calle Sur peligrosa)
        return {"Av_Central": 1, "Calle_Norte": 1, "Calle_Sur": 15}
    else:
        return {"Av_Central": 1, "Calle_Norte": 1, "Calle_Sur": 1}

# --- 2. ENFOQUE HEURÍSTICO (Algoritmo A*) ---
def calcular_ruta_a_estrella(inicio, meta, penalizaciones):
    # f = g + h (h es distancia lineal simple al Hospital)
    h = {'Farmacia': 10, 'Av_Central': 5, 'Calle_Norte': 5, 'Calle_Sur': 2, 'Hospital': 0}
    
    frontera = [(0 + h[inicio], 0, inicio, [])]
    visitados = set()

    while frontera:
        f, g, nodo, camino = heapq.heappop(frontera)
        if nodo in visitados: continue
        
        camino = camino + [nodo]
        if nodo == meta: return camino, g
        
        visitados.add(nodo)
        for vecino, distancia in MAPA[nodo].items():
            peso_extra = penalizaciones.get(vecino, 1)
            nuevo_g = g + (distancia * peso_extra)
            heapq.heappush(frontera, (nuevo_g + h[vecino], nuevo_g, vecino, camino))
    return None, 0

# --- 3. ENFOQUE DE EXPLICACIÓN Y DIBUJO (Interfaz Gráfica) ---
class AppRutaExperta:
    def __init__(self, root, hora):
        self.root = root
        self.root.title(f"Sistema Experto de Rutas - Hora: {hora}:00")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(pady=20)
        
        self.hora = hora
        self.reglas = obtener_reglas_trafico(hora)
        self.ruta, self.costo = calcular_ruta_a_estrella('Farmacia', 'Hospital', self.reglas)
        
        self.dibujar_grafo()
        self.mostrar_explicacion()

    def dibujar_grafo(self):
        # Dibujar conexiones (Aristas)
        for origen, vecinos in MAPA.items():
            x1, y1 = POSICIONES[origen]
            for destino in vecinos:
                x2, y2 = POSICIONES[destino]
                # Si es parte de la ruta elegida, pintar en verde
                color = "green" if origen in self.ruta and destino in self.ruta and \
                        self.ruta.index(destino) == self.ruta.index(origen) + 1 else "gray"
                ancho = 4 if color == "green" else 1
                self.canvas.create_line(x1, y1, x2, y2, fill=color, width=ancho)

        # Dibujar puntos (Nodos)
        for nombre, (x, y) in POSICIONES.items():
            color = "#f39c12" if nombre in self.ruta else "#bdc3c7"
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill=color, outline="black")
            self.canvas.create_text(x, y+35, text=nombre, font=("Arial", 10, "bold"))

    def mostrar_explicacion(self):
        # Árbol de decisión simplificado en texto
        texto_arbol = f"--- ÁRBOL DE DECISIÓN DEL EXPERTO ---\n"
        texto_arbol += f"Objetivo: Llegar al Hospital (Costo total: {self.costo})\n\n"
        
        for i in range(len(self.ruta)-1):
            nodo = self.ruta[i+1]
            p = self.reglas.get(nodo, 1)
            razon = "Ruta fluida" if p == 1 else "Elegida a pesar del tráfico" if p < 5 else "Riesgo alto evitado"
            texto_arbol += f"-> Ir a {nodo}: {razon}\n"
        
        lbl = tk.Label(self.root, text=texto_arbol, justify="left", font=("Consolas", 10), bg="#ecf0f1", padx=10, pady=10)
        lbl.pack(fill="x", padx=20, pady=10)

# --- INICIAR PROGRAMA ---
if __name__ == "__main__":
    root = tk.Tk()
    # PROBAMOS CON HORA PICO (18:00) PARA VER AL EXPERTO EVITAR EL TRÁFICO
    app = AppRutaExperta(root, hora=18) 
    root.mainloop()
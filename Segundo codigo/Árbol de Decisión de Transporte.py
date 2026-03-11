import tkinter as tk
import heapq

# --- 1. BASE DE CONOCIMIENTOS (Mapa de la ciudad) ---
# Formato: 'Origen': {'Destino': (Distancia_KM, Tiempo_Minutos)}
MAPA_COMPLEJO = {
    'Inicio': {'A': (5, 10), 'B': (8, 15)},
    'A': {'C': (2, 5), 'D': (10, 20)},
    'B': {'D': (4, 8), 'E': (7, 12)},
    'C': {'D': (3, 4), 'Destino': (12, 25)},
    'D': {'Destino': (5, 10)},
    'E': {'Destino': (15, 30)},
    'Destino': {}
}

# Coordenadas para dibujar el mapa
POS_MAPA = {
    'Inicio': (50, 200), 'A': (150, 100), 'B': (150, 300),
    'C': (250, 50), 'D': (300, 200), 'E': (350, 300), 'Destino': (500, 200)
}

# --- 2. MOTOR DE INFERENCIA (Dijkstra para Ruta Óptima) ---
def encontrar_mejor_ruta(inicio, fin, criterio_indice):
    # criterio_indice: 0 para Distancia, 1 para Tiempo
    cola = [(0, inicio, [])]
    visitados = set()
    arbol_exploracion = [] # Guardará cómo se expandió la búsqueda

    while cola:
        (costo, actual, camino) = heapq.heappop(cola)
        
        if actual in visitados: continue
        
        camino = camino + [actual]
        if actual == fin:
            return camino, costo, arbol_exploracion

        visitados.add(actual)
        
        for vecino, valores in MAPA_COMPLEJO[actual].items():
            if vecino not in visitados:
                nuevo_costo = costo + valores[criterio_indice]
                heapq.heappush(cola, (nuevo_costo, vecino, camino))
                # Registramos la rama para el árbol visual
                arbol_exploracion.append((actual, vecino, nuevo_costo))
                
    return None, 0, []

# --- 3. INTERFAZ GRÁFICA (Visualización de Mapa y Árbol) ---
class SistemaExpertoRutas:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa 2: Optimizador de Rutas y Árbol de Búsqueda")
        
        # Canvas para el Mapa
        self.canvas_mapa = tk.Canvas(root, width=600, height=350, bg="#F8F9F9", highlightthickness=1, highlightbackground="black")
        self.canvas_mapa.pack(pady=10)
        
        # Canvas para el Árbol de Decisiones
        self.canvas_arbol = tk.Canvas(root, width=600, height=300, bg="white", highlightthickness=1, highlightbackground="blue")
        self.canvas_arbol.pack(pady=10)

        # Ejecutar Lógica
        self.ruta, self.costo, self.exploracion = encontrar_mejor_ruta('Inicio', 'Destino', 1) # 1 = Tiempo
        
        self.dibujar_mapa()
        self.dibujar_arbol_busqueda()

    def dibujar_mapa(self):
        self.canvas_mapa.create_text(300, 20, text="MAPA DE UBICACIONES (Red de Caminos)", font=("Arial", 12, "bold"))
        # Dibujar conexiones
        for origen, vecinos in MAPA_COMPLEJO.items():
            x1, y1 = POS_MAPA[origen]
            for destino, vals in vecinos.items():
                x2, y2 = POS_MAPA[destino]
                # Color verde si es la ruta ganadora
                es_ganadora = (origen in self.ruta and destino in self.ruta and 
                               self.ruta.index(destino) == self.ruta.index(origen) + 1)
                color = "#2ECC71" if es_ganadora else "#BDC3C7"
                ancho = 4 if es_ganadora else 1
                self.canvas_mapa.create_line(x1, y1, x2, y2, fill=color, width=ancho)
                self.canvas_mapa.create_text((x1+x2)/2, (y1+y2)/2-10, text=f"{vals[1]}min", font=("Arial", 8))

        # Dibujar puntos
        for nodo, (x, y) in POS_MAPA.items():
            color = "#273746" if nodo in ['Inicio', 'Destino'] else "#5D6D7E"
            self.canvas_mapa.create_oval(x-15, y-15, x+15, y+15, fill=color)
            self.canvas_mapa.create_text(x, y+25, text=nodo, font=("Arial", 9, "bold"))

    def dibujar_arbol_busqueda(self):
        self.canvas_arbol.create_text(300, 20, text="ÁRBOL DE EXPLORACIÓN LÓGICA (Por qué eligió esta ruta)", font=("Arial", 12, "bold"))
        
        # Dibujamos las ramas que el experto evaluó
        # Esto representa el árbol de búsqueda generado en memoria
        x_base = 50
        y_base = 60
        espacio_x = 100
        
        # Nodo Raíz del Árbol
        self.canvas_arbol.create_rectangle(x_base, y_base, x_base+80, y_base+30, fill="#D6EAF8")
        self.canvas_arbol.create_text(x_base+40, y_base+15, text="Inicio", font=("Arial", 8, "bold"))

        for i, (padre, hijo, costo) in enumerate(self.exploracion):
            col = (i % 5) + 1
            fila = (i // 5) + 1
            x = x_base + (col * espacio_x)
            y = y_base + (fila * 50)
            
            # Dibujar rama del árbol
            self.canvas_arbol.create_line(x-20, y-10, x-50, y-30, arrow=tk.LAST)
            color_nodo = "#ABEBC6" if hijo in self.ruta else "white"
            self.canvas_arbol.create_rectangle(x, y, x+80, y+30, fill=color_nodo)
            self.canvas_arbol.create_text(x+40, y+15, text=f"{hijo}\nCosto:{costo}", font=("Arial", 7))

        veredicto = f"VERDICTO: Ruta más rápida {' -> '.join(self.ruta)} (Total: {self.costo} min)"
        self.canvas_arbol.create_text(300, 270, text=veredicto, font=("Arial", 10, "bold"), fill="green")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoRutas(root)
    root.mainloop()
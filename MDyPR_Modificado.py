import tkinter as tk
import random
from collections import Counter

# --- 1. BASE DE CONOCIMIENTOS (Grafo de 7 Nodos) ---
P = {
    'Tormenta': {True: 0.15, False: 0.85},
    'Evento_Deportivo': {True: 0.10, False: 0.90},
    
    'Inundacion': {
        (True,): {True: 0.7, False: 0.3},
        (False,): {True: 0.05, False: 0.95}
    },
    'Trafico_Centro': {
        (True,): {True: 0.85, False: 0.15},
        (False,): {True: 0.2, False: 0.8}
    },
    
    'Ruta_Principal_Cerrada': {
        (True,): {True: 0.9, False: 0.1},
        (False,): {True: 0.1, False: 0.9}
    },
    'Ruta_Alterna_Lenta': {
        (True, True): {True: 0.95, False: 0.05},
        (True, False): {True: 0.6, False: 0.4},
        (False, True): {True: 0.7, False: 0.3},
        (False, False): {True: 0.1, False: 0.9}
    },
    
    'Llegada_Tarde': {
        (True, True): {True: 0.99, False: 0.01},
        (True, False): {True: 0.8, False: 0.2},
        (False, True): {True: 0.7, False: 0.3},
        (False, False): {True: 0.05, False: 0.95}
    }
}

# --- 2. MOTOR DE MUESTREO (MD y PR) ---
def sample_boolean(prob):
    return random.random() < prob

def muestreo_por_rechazo(n_muestras, evidencia):
    muestras = []
    intentos = 0
    while len(muestras) < n_muestras and intentos < n_muestras * 50:
        muestra = {}
        
        # Muestreo Top-Down (Cascada)
        t = sample_boolean(P['Tormenta'][True])
        ed = sample_boolean(P['Evento_Deportivo'][True])
        muestra['Tormenta'], muestra['Evento_Deportivo'] = t, ed
        
        i = sample_boolean(P['Inundacion'][(t,)][True])
        tc = sample_boolean(P['Trafico_Centro'][(ed,)][True])
        muestra['Inundacion'], muestra['Trafico_Centro'] = i, tc
        
        rp = sample_boolean(P['Ruta_Principal_Cerrada'][(i,)][True])
        ra = sample_boolean(P['Ruta_Alterna_Lenta'][(i, tc)][True])
        muestra['Ruta_Principal_Cerrada'], muestra['Ruta_Alterna_Lenta'] = rp, ra
        
        lt = sample_boolean(P['Llegada_Tarde'][(rp, ra)][True])
        muestra['Llegada_Tarde'] = lt
        
        intentos += 1

        # Filtro de Rechazo: ¿Coincide con la evidencia?
        if all(muestra.get(var) == val for var, val in evidencia.items()):
            muestras.append(muestra)
            
    return muestras

def estimar_distribucion(muestras, variable):
    contador = Counter(muestra[variable] for muestra in muestras)
    total = sum(contador.values())
    return {k: v / total for k, v in contador.items()}

# --- 3. INTERFAZ GRÁFICA ---
class AppMuestreo:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa 3: MD - Muestreo Directo y por Rechazo")
        self.canvas = tk.Canvas(root, width=950, height=750, bg="#E8F8F5")
        self.canvas.pack()

        # Simulamos 10,000 días, pero solo nos quedamos con los días donde hubo Inundación
        self.n = 5000
        self.evidencia = {'Inundacion': True}
        self.muestras = muestreo_por_rechazo(self.n, self.evidencia)
        self.dist = estimar_distribucion(self.muestras, 'Llegada_Tarde')
        
        self.dibujar_grafo()

    def dibujar_grafo(self):
        self.canvas.create_text(475, 40, text="SIMULACIÓN: MUESTREO POR RECHAZO (MDyPR)", font=("Arial", 16, "bold"), fill="#0E6251")
        
        # Nodos del DAG
        nodos = {
            'Tormenta': (300, 150), 'Evento Deportivo': (650, 150),
            'Inundacion': (300, 300), 'Trafico Centro': (650, 300),
            'Ruta Principal Cerrada': (300, 450), 'Ruta Alterna Lenta': (650, 450),
            'Llegada Tarde': (475, 600)
        }

        conexiones = [
            ('Tormenta', 'Inundacion'), ('Evento Deportivo', 'Trafico Centro'),
            ('Inundacion', 'Ruta Principal Cerrada'), ('Inundacion', 'Ruta Alterna Lenta'),
            ('Trafico Centro', 'Ruta Alterna Lenta'),
            ('Ruta Principal Cerrada', 'Llegada Tarde'), ('Ruta Alterna Lenta', 'Llegada Tarde')
        ]

        for orig, dest in conexiones:
            x1, y1 = nodos[orig]
            x2, y2 = nodos[dest]
            self.canvas.create_line(x1, y1+20, x2, y2-20, arrow=tk.LAST, width=3, fill="#73C6B6")

        for nombre, (x, y) in nodos.items():
            es_evidencia = 'Inundacion' in nombre
            color = "#F1C40F" if es_evidencia else "#EAFAF1"
            self.canvas.create_rectangle(x-80, y-25, x+80, y+25, fill=color, outline="#0E6251", width=2)
            self.canvas.create_text(x, y, text=nombre, font=("Arial", 9, "bold"))

        texto = (
            f"RESULTADOS DE LA SIMULACIÓN DE MONTE CARLO:\n"
            f"Se generaron escenarios aleatorios hasta obtener {self.n} muestras válidas\n"
            f"donde la evidencia observada (Inundación = True) se cumpliera. El resto se rechazó.\n\n"
            f"Basado en las simulaciones exitosas, la probabilidad de llegar tarde es: {self.dist[True]*100:.2f}%."
        )
        self.canvas.create_text(475, 680, text=texto, font=("Consolas", 11), justify="center", fill="#0E6251")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMuestreo(root)
    root.mainloop()
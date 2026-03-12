import tkinter as tk
import random
from collections import Counter

# --- 1. BASE DE CONOCIMIENTOS (Red Bayesiana: Salida del Estadio Akron) ---
# Nota: Tu motor de Muestreo original sí usa tuplas (True,) para un solo padre.
P = {
    'Partido_Estadio_Akron': {True: 0.30, False: 0.70},
    'Lluvia_Zapopan': {True: 0.25, False: 0.75},
    
    'Caos_Av_Vallarta': { # 2 Padres
        (True, True): {True: 0.99, False: 0.01},
        (True, False): {True: 0.85, False: 0.15},
        (False, True): {True: 0.60, False: 0.40},
        (False, False): {True: 0.20, False: 0.80}
    },
    'Caos_Periferico_Poniente': { # 1 Padre
        (True,): {True: 0.90, False: 0.10},
        (False,): {True: 0.30, False: 0.70}
    },
    
    'Ruta_Andares_Bloqueada': { # 1 Padre (Periferico)
        (True,): {True: 0.80, False: 0.20},
        (False,): {True: 0.15, False: 0.85}
    },
    'Ruta_Chapalita_Bloqueada': { # 2 Padres (Vallarta y Periferico)
        (True, True): {True: 0.95, False: 0.05},
        (True, False): {True: 0.70, False: 0.30},
        (False, True): {True: 0.65, False: 0.35},
        (False, False): {True: 0.10, False: 0.90}
    },
    
    'Cena_Rapida_Conseguida': { # 2 Padres (Depende de tus 2 rutas principales)
        (True, True): {True: 0.10, False: 0.90}, # Si ambas rutas fallan, casi imposible cenar rápido
        (True, False): {True: 0.85, False: 0.15},
        (False, True): {True: 0.85, False: 0.15},
        (False, False): {True: 0.98, False: 0.02} # Ambas libres = Cena asegurada
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
        
        # Cascada de eventos (Top-Down)
        p_akron = sample_boolean(P['Partido_Estadio_Akron'][True])
        l_zapo = sample_boolean(P['Lluvia_Zapopan'][True])
        muestra['Partido_Estadio_Akron'], muestra['Lluvia_Zapopan'] = p_akron, l_zapo
        
        c_vallarta = sample_boolean(P['Caos_Av_Vallarta'][(p_akron, l_zapo)][True])
        c_peri = sample_boolean(P['Caos_Periferico_Poniente'][(p_akron,)][True])
        muestra['Caos_Av_Vallarta'], muestra['Caos_Periferico_Poniente'] = c_vallarta, c_peri
        
        r_andares = sample_boolean(P['Ruta_Andares_Bloqueada'][(c_peri,)][True])
        r_chapa = sample_boolean(P['Ruta_Chapalita_Bloqueada'][(c_vallarta, c_peri)][True])
        muestra['Ruta_Andares_Bloqueada'], muestra['Ruta_Chapalita_Bloqueada'] = r_andares, r_chapa
        
        cena = sample_boolean(P['Cena_Rapida_Conseguida'][(r_andares, r_chapa)][True])
        muestra['Cena_Rapida_Conseguida'] = cena
        
        intentos += 1

        # Filtro de Rechazo
        if all(muestra.get(var) == val for var, val in evidencia.items()):
            muestras.append(muestra)
            
    return muestras

def estimar_distribucion(muestras, variable):
    contador = Counter(muestra[variable] for muestra in muestras)
    total = sum(contador.values())
    return {k: v / total for k, v in contador.items()}

# --- 3. INTERFAZ GRÁFICA ---
class AppRestaurantes:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulación por Muestreo: Restaurantes post-Estadio Akron")
        self.canvas = tk.Canvas(root, width=950, height=750, bg="#EAF2F8")
        self.canvas.pack()

        # EVIDENCIA: Hay partido en el Akron, pero no está lloviendo en Zapopan.
        self.n = 5000
        self.evidencia = {'Partido_Estadio_Akron': True, 'Lluvia_Zapopan': False}
        self.muestras = muestreo_por_rechazo(self.n, self.evidencia)
        self.dist = estimar_distribucion(self.muestras, 'Cena_Rapida_Conseguida')
        
        self.dibujar_grafo()

    def dibujar_grafo(self):
        self.canvas.create_text(475, 30, text="RUTAS GASTRONÓMICAS - ESTADIO AKRON (MUESTREO)", font=("Arial", 16, "bold"), fill="#154360")
        
        nodos = {
            'Partido_Estadio_Akron': (300, 100), 'Lluvia_Zapopan': (650, 100),
            'Caos_Periferico_Poniente': (200, 250), 'Caos_Av_Vallarta': (750, 250),
            'Ruta_Andares_Bloqueada': (200, 420), 'Ruta_Chapalita_Bloqueada': (750, 420),
            'Cena_Rapida_Conseguida': (475, 580)
        }

        conexiones = [
            ('Partido_Estadio_Akron', 'Caos_Av_Vallarta'), ('Lluvia_Zapopan', 'Caos_Av_Vallarta'),
            ('Partido_Estadio_Akron', 'Caos_Periferico_Poniente'),
            ('Caos_Periferico_Poniente', 'Ruta_Andares_Bloqueada'), 
            ('Caos_Av_Vallarta', 'Ruta_Chapalita_Bloqueada'), ('Caos_Periferico_Poniente', 'Ruta_Chapalita_Bloqueada'),
            ('Ruta_Andares_Bloqueada', 'Cena_Rapida_Conseguida'), ('Ruta_Chapalita_Bloqueada', 'Cena_Rapida_Conseguida')
        ]

        for orig, dest in conexiones:
            x1, y1 = nodos[orig]
            x2, y2 = nodos[dest]
            self.canvas.create_line(x1, y1+20, x2, y2-20, arrow=tk.LAST, width=3, fill="#5499C7")

        for nombre, (x, y) in nodos.items():
            es_evidencia = nombre in self.evidencia
            color = "#F4D03F" if es_evidencia else "#D4E6F1"
            grosor = 3 if es_evidencia else 1
            
            self.canvas.create_rectangle(x-90, y-25, x+90, y+25, fill=color, outline="#154360", width=grosor)
            texto = nombre.replace("_", " ")
            self.canvas.create_text(x, y, text=texto, font=("Arial", 8, "bold"), fill="#154360")

        texto = (
            f"SIMULACIÓN DE MONTE CARLO ({self.n} Escenarios Virtuales):\n"
            f"Evidencia impuesta: Partido en el Akron = TRUE | Lluvia en Zapopan = FALSE\n\n"
            f"El algoritmo descartó las noches lluviosas y simuló el caos vial en Vallarta/Periférico.\n"
            f"Probabilidad de llegar rápido a cenar a Andares o Chapalita: {self.dist[True]*100:.2f}%."
        )
        self.canvas.create_text(475, 680, text=texto, font=("Consolas", 11), justify="center", fill="#154360")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRestaurantes(root)
    root.mainloop()
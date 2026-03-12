import tkinter as tk
import random
from collections import Counter

# --- 1. BASE DE CONOCIMIENTOS (Eventos en Cascada) ---
P = {
    'Tormenta': {True: 0.3, False: 0.7},
    'Inundacion_Av': { # Depende de Tormenta
        (True,): {True: 0.8, False: 0.2},
        (False,): {True: 0.1, False: 0.9}
    },
    'Ruta_Cerrada': { # Depende de Inundacion_Av
        (True,): {True: 0.9, False: 0.1},
        (False,): {True: 0.2, False: 0.8}
    }
}

# --- 2. MOTOR DE MUESTREO (Tu código exacto) ---
def sample_boolean(prob):
    return random.random() < prob

def muestreo_por_rechazo(n_muestras, evidencia):
    muestras = []
    intentos = 0
    while len(muestras) < n_muestras and intentos < n_muestras * 20:
        muestra = {}
        a = sample_boolean(P['Tormenta'][True])
        muestra['Tormenta'] = a
        b = sample_boolean(P['Inundacion_Av'][(a,)][True])
        muestra['Inundacion_Av'] = b
        c = sample_boolean(P['Ruta_Cerrada'][(b,)][True])
        muestra['Ruta_Cerrada'] = c
        intentos += 1

        cumple = all(muestra.get(var) == val for var, val in evidencia.items())
        if cumple: muestras.append(muestra)
    return muestras

def estimar_distribucion(muestras, variable):
    contador = Counter(muestra[variable] for muestra in muestras)
    total = sum(contador.values())
    return {k: v / total for k, v in contador.items()}

# --- 3. INTERFAZ GRÁFICA ---
class AppMuestreo:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Simulación por Muestreo (Rechazo)")
        self.canvas = tk.Canvas(root, width=800, height=720, bg="#E8F8F5")
        self.canvas.pack()

        self.n_simulaciones = 2000
        self.evidencia = {'Inundacion_Av': True}
        self.muestras = muestreo_por_rechazo(self.n_simulaciones, self.evidencia)
        self.distribucion = estimar_distribucion(self.muestras, 'Ruta_Cerrada')
        
        self.dibujar_simulacion()

    def dibujar_simulacion(self):
        self.canvas.create_text(400, 40, text="SIMULADOR DE RIESGOS (MUESTREO POR RECHAZO)", font=("Arial", 16, "bold"))
        
        # Dibujar la cadena de eventos (Horizontal)
        nodos = [("1. Tormenta", 200), ("2. Inundación Av.", 400), ("3. Ruta Cerrada", 600)]
        for i, (nombre, x) in enumerate(nodos):
            y = 200
            # Dibujar flechas entre nodos
            if i > 0: self.canvas.create_line(nodos[i-1][1]+60, y, x-60, y, arrow=tk.LAST, width=3)
            
            color = "#F39C12" if "Inundación" in nombre else "#D6EAF8"
            self.canvas.create_rectangle(x-70, y-30, x+70, y+30, fill=color, outline="black", width=2)
            self.canvas.create_text(x, y, text=nombre, font=("Arial", 10, "bold"))

        self.canvas.create_text(400, 260, text="Variables en Cascada. Evidencia fija: Inundación en la Avenida = TRUE", font=("Arial", 10, "italic"))

        # Panel de resultados de la simulación
        self.canvas.create_rectangle(150, 350, 650, 550, fill="white", outline="#117A65", width=3, dash=(5,5))
        self.canvas.create_text(400, 380, text="📊 RESULTADOS DE LAS SIMULACIONES 📊", font=("Arial", 12, "bold"))
        
        texto_simulacion = (
            f"Se corrieron {self.n_simulaciones} simulaciones aleatorias.\n"
            f"El algoritmo descartó todos los escenarios donde NO hubo inundación.\n\n"
            f"De las simulaciones exitosas, la estadística es:\n"
            f"Probabilidad de que la Ruta esté Cerrada: {self.distribucion[True]*100:.1f}%\n"
            f"Probabilidad de que la Ruta esté Abierta: {self.distribucion[False]*100:.1f}%"
        )
        self.canvas.create_text(400, 460, text=texto_simulacion, font=("Consolas", 11), justify="center")

        # Veredicto Final
        veredicto = "CONCLUSIÓN: Riesgo crítico de cierre. El GPS debe buscar rutas alternativas." if self.distribucion[True] > 0.6 else "Ruta transitable, aunque con precaución."
        self.canvas.create_text(400, 620, text=veredicto, font=("Arial", 13, "bold"), fill="#900C3F")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppMuestreo(root)
    root.mainloop()
import tkinter as tk
from itertools import product

# --- 1. BASE DE CONOCIMIENTOS (Red Bayesiana de Tráfico) ---
# Adaptado de tu código de Robo/Terremoto a Lluvia/Accidente
P = {
    'Lluvia': {True: 0.15, False: 0.85},
    'Accidente': {True: 0.05, False: 0.95},
    'Trafico_Masivo': {
        (True, True): {True: 0.99, False: 0.01},  # Lluvia + Accidente = Tráfico seguro
        (True, False): {True: 0.80, False: 0.20}, # Solo Lluvia = Tráfico probable
        (False, True): {True: 0.90, False: 0.10}, # Solo Accidente = Tráfico muy probable
        (False, False): {True: 0.10, False: 0.90} # Nada = Tráfico raro
    },
    'RutaA_Lenta': {
        True: {True: 0.85, False: 0.15}, # Si hay tráfico masivo, Ruta A se alenta
        False: {True: 0.20, False: 0.80}
    },
    'RutaB_Lenta': {
        True: {True: 0.75, False: 0.25}, # Si hay tráfico masivo, Ruta B se alenta
        False: {True: 0.10, False: 0.90}
    }
}

padres = {
    'Lluvia': [],
    'Accidente': [],
    'Trafico_Masivo': ['Lluvia', 'Accidente'],
    'RutaA_Lenta': ['Trafico_Masivo'],
    'RutaB_Lenta': ['Trafico_Masivo']
}

# --- 2. MOTOR DE INFERENCIA (Tu código exacto) ---
def probabilidad(variable, valor, asignacion):
    if not padres[variable]:
        return P[variable][valor]
    else:
        if len(padres[variable]) == 1:
            valor_padre = asignacion[padres[variable][0]]
            return P[variable][valor_padre][valor]
        else:
            valores_padres = tuple(asignacion[p] for p in padres[variable])
            return P[variable][valores_padres][valor]

def enumerar_todas(variables, asignacion):
    if not variables: return 1.0
    Y = variables[0]
    resto = variables[1:]
    if Y in asignacion:
        prob = probabilidad(Y, asignacion[Y], asignacion)
        return prob * enumerar_todas(resto, asignacion)
    else:
        total = 0
        for y in [True, False]:
            asignacion[Y] = y
            prob = probabilidad(Y, y, asignacion)
            total += prob * enumerar_todas(resto, asignacion)
            del asignacion[Y]
        return total

def inferencia_por_enumeracion(variable_consulta, evidencia):
    resultado = {}
    for valor in [True, False]:
        evidencia[variable_consulta] = valor
        prob = enumerar_todas(list(P.keys()), evidencia.copy())
        resultado[valor] = prob
        del evidencia[variable_consulta]
    
    total = sum(resultado.values())
    for val in resultado: resultado[val] /= total
    return resultado

# --- 3. INTERFAZ GRÁFICA ---
class AppRedBayesiana:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Inferencia por Enumeración")
        self.canvas = tk.Canvas(root, width=800, height=720, bg="#F9EBEA")
        self.canvas.pack()

        # CASO DE PRUEBA: Ambas rutas reportan lentitud. ¿Habrá accidente?
        self.evidencia = {'RutaA_Lenta': True, 'RutaB_Lenta': True}
        self.consulta = 'Accidente'
        self.resultado = inferencia_por_enumeracion(self.consulta, self.evidencia)
        
        self.dibujar_red()

    def dibujar_red(self):
        self.canvas.create_text(400, 40, text="DIAGNÓSTICO DE TRÁFICO (RED BAYESIANA)", font=("Arial", 16, "bold"))
        
        # Coordenadas de los nodos (Diseño en Diamante)
        nodos = {
            'Lluvia': (250, 150), 'Accidente': (550, 150),
            'Trafico_Masivo': (400, 300),
            'RutaA_Lenta': (250, 450), 'RutaB_Lenta': (550, 450)
        }

        # Dibujar flechas de dependencia
        relaciones = [('Lluvia', 'Trafico_Masivo'), ('Accidente', 'Trafico_Masivo'), 
                      ('Trafico_Masivo', 'RutaA_Lenta'), ('Trafico_Masivo', 'RutaB_Lenta')]
        
        for orig, dest in relaciones:
            x1, y1 = nodos[orig]
            x2, y2 = nodos[dest]
            self.canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=3, fill="#85929E")

        # Dibujar nodos
        for nombre, (x, y) in nodos.items():
            es_evidencia = nombre in self.evidencia
            es_consulta = nombre == self.consulta
            
            color = "#F5B041" if es_evidencia else ("#5DADE2" if es_consulta else "#FFFFFF")
            grosor = 3 if es_evidencia or es_consulta else 1
            
            self.canvas.create_oval(x-60, y-30, x+60, y+30, fill=color, outline="#2C3E50", width=grosor)
            self.canvas.create_text(x, y, text=nombre, font=("Arial", 10, "bold"))

        # Leyenda visual
        self.canvas.create_text(400, 520, text="Amarillo = Evidencia Observada | Azul = Variable a Inferir", font=("Arial", 10, "italic"))

        # Veredicto
        prob_accidente = self.resultado[True] * 100
        texto_final = (f"RAZONAMIENTO DEL EXPERTO:\n"
                       f"Evidencia: El GPS marca la Ruta A y Ruta B como lentas.\n"
                       f"Probabilidad calculada de que exista un Accidente: {prob_accidente:.2f}%\n")
        
        color_v = "#C0392B" if prob_accidente > 30 else "#27AE60"
        recomendacion = "ALERTA: Alta probabilidad de accidente. Evitar la zona." if prob_accidente > 30 else "Tráfico normal, proceder con precaución."
        
        self.canvas.create_text(400, 600, text=texto_final, font=("Arial", 12, "bold"), fill="#2C3E50", justify="center")
        self.canvas.create_text(400, 660, text=recomendacion, font=("Arial", 13, "bold"), fill=color_v)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRedBayesiana(root)
    root.mainloop()
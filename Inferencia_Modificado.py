import tkinter as tk
from itertools import product

# --- 1. BASE DE CONOCIMIENTOS (Red Bayesiana: Hospitales en GDL) ---
P = {
    'Lluvia_GDL': {True: 0.2, False: 0.8},
    'Choque_Lopez_Mateos': {True: 0.15, False: 0.85},

    'Caos_Norte_Periferico': { # 1 Padre: Solo Lluvia (Sin tupla)
        True: {True: 0.75, False: 0.25},
        False: {True: 0.20, False: 0.80}
    },
    'Caos_Sur_Las_Rosas': { # 2 Padres: Lluvia y Choque (Con tupla)
        (True, True): {True: 0.99, False: 0.01},
        (True, False): {True: 0.70, False: 0.30},
        (False, True): {True: 0.85, False: 0.15},
        (False, False): {True: 0.30, False: 0.70}
    },

    'Puerta_Hierro_Inaccesible': { # 1 Padre: Norte
        True: {True: 0.80, False: 0.20},
        False: {True: 0.10, False: 0.90}
    },
    'Real_San_Jose_Inaccesible': { # 1 Padre: Sur
        True: {True: 0.85, False: 0.15},
        False: {True: 0.15, False: 0.85}
    },
    'San_Javier_Inaccesible': { # 2 Padres: Norte y Sur
        (True, True): {True: 0.90, False: 0.10},
        (True, False): {True: 0.60, False: 0.40},
        (False, True): {True: 0.65, False: 0.35},
        (False, False): {True: 0.05, False: 0.95}
    },

    'Llegada_A_Tiempo': { # 2 Padres: Depende de las opciones Puerta Hierro y Real San Jose
        (True, True): {True: 0.05, False: 0.95}, # Ambos inaccesibles = No llegas a tiempo
        (True, False): {True: 0.80, False: 0.20}, # Uno libre = Llegas
        (False, True): {True: 0.80, False: 0.20}, 
        (False, False): {True: 0.99, False: 0.01} # Ambos libres = Llegas rapidísimo
    }
}

padres = {
    'Lluvia_GDL': [],
    'Choque_Lopez_Mateos': [],
    'Caos_Norte_Periferico': ['Lluvia_GDL'],
    'Caos_Sur_Las_Rosas': ['Lluvia_GDL', 'Choque_Lopez_Mateos'],
    'Puerta_Hierro_Inaccesible': ['Caos_Norte_Periferico'],
    'Real_San_Jose_Inaccesible': ['Caos_Sur_Las_Rosas'],
    'San_Javier_Inaccesible': ['Caos_Norte_Periferico', 'Caos_Sur_Las_Rosas'],
    'Llegada_A_Tiempo': ['Puerta_Hierro_Inaccesible', 'Real_San_Jose_Inaccesible']
}

# --- 2. MOTOR DE INFERENCIA ---
def probabilidad(variable, valor, asignacion):
    if not padres[variable]: return P[variable][valor]
    if len(padres[variable]) == 1:
        return P[variable][asignacion[padres[variable][0]]][valor]
    valores_padres = tuple(asignacion[p] for p in padres[variable])
    return P[variable][valores_padres][valor]

def enumerar_todas(variables, asignacion):
    if not variables: return 1.0
    Y = variables[0]
    resto = variables[1:]
    if Y in asignacion:
        return probabilidad(Y, asignacion[Y], asignacion) * enumerar_todas(resto, asignacion)
    total = 0
    for y in [True, False]:
        asignacion[Y] = y
        total += probabilidad(Y, y, asignacion) * enumerar_todas(resto, asignacion)
        del asignacion[Y]
    return total

def inferencia_por_enumeracion(variable_consulta, evidencia):
    resultado = {}
    for valor in [True, False]:
        evidencia[variable_consulta] = valor
        resultado[valor] = enumerar_todas(list(P.keys()), evidencia.copy())
        del evidencia[variable_consulta]
    total = sum(resultado.values())
    for val in resultado: resultado[val] /= total
    return resultado

# --- 3. INTERFAZ GRÁFICA ---
class AppHospitales:
    def __init__(self, root):
        self.root = root
        self.root.title("Inferencia: Rutas a Hospitales en Guadalajara")
        self.canvas = tk.Canvas(root, width=950, height=750, bg="#F9EBEA")
        self.canvas.pack()

        # EVIDENCIA: Hay choque en López Mateos y el San Javier reporta bloqueo.
        self.evidencia = {'Choque_Lopez_Mateos': True, 'San_Javier_Inaccesible': True}
        self.consulta = 'Llegada_A_Tiempo'
        self.resultado = inferencia_por_enumeracion(self.consulta, self.evidencia)
        
        self.dibujar_red()

    def dibujar_red(self):
        self.canvas.create_text(475, 30, text="EMERGENCIA MÉDICA GDL (INFERENCIA EXACTA)", font=("Arial", 16, "bold"), fill="#922B21")
        
        nodos = {
            'Lluvia_GDL': (300, 100), 'Choque_Lopez_Mateos': (650, 100),
            'Caos_Norte_Periferico': (200, 250), 'Caos_Sur_Las_Rosas': (750, 250),
            'Puerta_Hierro_Inaccesible': (200, 420), 'San_Javier_Inaccesible': (475, 420), 'Real_San_Jose_Inaccesible': (750, 420),
            'Llegada_A_Tiempo': (475, 580)
        }

        for hijo, lista_padres in padres.items():
            x_hijo, y_hijo = nodos[hijo]
            for padre in lista_padres:
                x_padre, y_padre = nodos[padre]
                self.canvas.create_line(x_padre, y_padre+20, x_hijo, y_hijo-20, arrow=tk.LAST, width=3, fill="#CD6155")

        for nombre, (x, y) in nodos.items():
            es_evidencia = nombre in self.evidencia
            es_consulta = nombre == self.consulta
            color = "#F4D03F" if es_evidencia else ("#85C1E9" if es_consulta else "#FDEDEC")
            grosor = 3 if es_evidencia or es_consulta else 1
            
            self.canvas.create_rectangle(x-90, y-25, x+90, y+25, fill=color, outline="#641E16", width=grosor)
            texto = nombre.replace("_", " ")
            self.canvas.create_text(x, y, text=texto, font=("Arial", 8, "bold"), fill="#17202A")

        prob = self.resultado[True] * 100
        texto_inferencia = (
            f"EVIDENCIA OBSERVADA:\n"
            f"- Choque grave en López Mateos (Sur).\n"
            f"- El Hospital San Javier está inaccesible en este momento.\n\n"
            f"DIAGNÓSTICO DEL SISTEMA:\n"
            f"Considerando el redireccionamiento hacia Puerta Hierro o el Real San José,\n"
            f"la probabilidad matemática de Llegar a Tiempo a Urgencias es del {prob:.2f}%."
        )
        self.canvas.create_text(475, 680, text=texto_inferencia, font=("Consolas", 11), justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppHospitales(root)
    root.mainloop()
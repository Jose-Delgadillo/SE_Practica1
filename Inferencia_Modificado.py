import tkinter as tk
from itertools import product

# --- 1. BASE DE CONOCIMIENTOS (Red Bayesiana Compleja de 9 Nodos) ---
P = {
    'Lluvia': {True: 0.3, False: 0.7},
    'Manifestacion': {True: 0.1, False: 0.9},

    'Trafico_Norte': { # Depende solo de Lluvia (CORREGIDO: Sin tupla)
        True: {True: 0.8, False: 0.2},
        False: {True: 0.2, False: 0.8}
    },
    'Trafico_Centro': { # Depende de Lluvia y Manifestacion (Dos padres = Tupla)
        (True, True): {True: 0.99, False: 0.01},
        (True, False): {True: 0.70, False: 0.30},
        (False, True): {True: 0.85, False: 0.15},
        (False, False): {True: 0.15, False: 0.85}
    },
    'Trafico_Sur': { # Depende solo de Manifestacion (CORREGIDO)
        True: {True: 0.75, False: 0.25},
        False: {True: 0.10, False: 0.90}
    },

    'Ruta_A_Lenta': { # Depende solo de Trafico_Norte (CORREGIDO)
        True: {True: 0.9, False: 0.1},
        False: {True: 0.05, False: 0.95}
    },
    'Ruta_B_Lenta': { # Depende solo de Trafico_Centro (CORREGIDO)
        True: {True: 0.85, False: 0.15},
        False: {True: 0.1, False: 0.9}
    },
    'Ruta_C_Lenta': { # Depende de Trafico_Centro y Trafico_Sur
        (True, True): {True: 0.95, False: 0.05},
        (True, False): {True: 0.60, False: 0.40},
        (False, True): {True: 0.70, False: 0.30},
        (False, False): {True: 0.05, False: 0.95}
    },

    'Llegada_Tarde': { # Depende de Ruta_B_Lenta y Ruta_C_Lenta
        (True, True): {True: 0.98, False: 0.02},
        (True, False): {True: 0.80, False: 0.20},
        (False, True): {True: 0.80, False: 0.20},
        (False, False): {True: 0.01, False: 0.99}
    }
}

padres = {
    'Lluvia': [],
    'Manifestacion': [],
    'Trafico_Norte': ['Lluvia'],
    'Trafico_Centro': ['Lluvia', 'Manifestacion'],
    'Trafico_Sur': ['Manifestacion'],
    'Ruta_A_Lenta': ['Trafico_Norte'],
    'Ruta_B_Lenta': ['Trafico_Centro'],
    'Ruta_C_Lenta': ['Trafico_Centro', 'Trafico_Sur'],
    'Llegada_Tarde': ['Ruta_B_Lenta', 'Ruta_C_Lenta']
}

# --- 2. MOTOR DE INFERENCIA (Lógica Original Intacta) ---
def probabilidad(variable, valor, asignacion):
    if not padres[variable]: 
        return P[variable][valor]
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
class AppRedBayesiana:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Experto: Inferencia de Rutas por Red Bayesiana")
        self.canvas = tk.Canvas(root, width=950, height=750, bg="#F4F6F7")
        self.canvas.pack()

        # Evidencia observada
        self.evidencia = {'Lluvia': True, 'Ruta_C_Lenta': True}
        self.consulta = 'Llegada_Tarde'
        
        self.resultado = inferencia_por_enumeracion(self.consulta, self.evidencia)
        self.dibujar_red()

    def dibujar_red(self):
        self.canvas.create_text(475, 30, text="RED BAYESIANA: ANÁLISIS MULTI-RUTA", font=("Arial", 16, "bold"), fill="#2C3E50")
        
        # Coordenadas formando un árbol profundo de 4 niveles
        nodos = {
            'Lluvia': (300, 100), 'Manifestacion': (650, 100),
            'Trafico_Norte': (150, 250), 'Trafico_Centro': (475, 250), 'Trafico_Sur': (800, 250),
            'Ruta_A_Lenta': (150, 420), 'Ruta_B_Lenta': (475, 420), 'Ruta_C_Lenta': (800, 420),
            'Llegada_Tarde': (475, 580)
        }

        # Dibujar las flechas de causa y efecto
        for hijo, lista_padres in padres.items():
            x_hijo, y_hijo = nodos[hijo]
            for padre in lista_padres:
                x_padre, y_padre = nodos[padre]
                self.canvas.create_line(x_padre, y_padre+20, x_hijo, y_hijo-20, arrow=tk.LAST, width=3, fill="#BDC3C7")

        # Dibujar los nodos (Cajas anchas para que quepa el texto)
        for nombre, (x, y) in nodos.items():
            es_evidencia = nombre in self.evidencia
            es_consulta = nombre == self.consulta
            
            # Colores: Amarillo (Evidencia), Azul (Pregunta), Blanco (Cálculo interno)
            color = "#F1C40F" if es_evidencia else ("#3498DB" if es_consulta else "#FFFFFF")
            grosor = 3 if es_evidencia or es_consulta else 1
            
            self.canvas.create_rectangle(x-70, y-25, x+70, y+25, fill=color, outline="#34495E", width=grosor)
            texto_pantalla = nombre.replace("_", " ")
            self.canvas.create_text(x, y, text=texto_pantalla, font=("Arial", 9, "bold"), fill="#17202A")

        # Explicación de la Inferencia (Veredicto)
        prob = self.resultado[True] * 100
        texto_inferencia = (
            f"DATOS DEL ENTORNO (EVIDENCIA):\n"
            f"- Está lloviendo (Lluvia = True)\n"
            f"- El GPS reporta la Ruta C colapsada (Ruta C Lenta = True)\n\n"
            f"INFERENCIA MATEMÁTICA EXACTA:\n"
            f"Dadas las dependencias del tráfico central y sur,\n"
            f"la probabilidad calculada de llegar tarde a tu destino es del {prob:.2f}%."
        )
        
        self.canvas.create_text(475, 680, text=texto_inferencia, font=("Consolas", 11), justify="center")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppRedBayesiana(root)
    root.mainloop()
import tkinter as tk

# --- 1. LÓGICA DE RED BAYESIANA (Basada en tu código) ---
def calcular_riesgo_ruta(prob_lluvia, prob_accidente_dado_lluvia, prob_retraso_dado_lluvia_y_acc):
    """
    Calcula la probabilidad de que haya un retraso crítico en la ruta.
    """
    P_retraso_total = 0.0
    # Iteramos sobre todas las combinaciones (Lluvia y Accidente)
    for lluvia in [True, False]:
        for accidente in [True, False]:
            # P(L)
            P_L = prob_lluvia if lluvia else 1 - prob_lluvia
            # P(A|L)
            P_A_dado_L = prob_accidente_dado_lluvia[lluvia] if accidente else 1 - prob_accidente_dado_lluvia[lluvia]
            # P(R|L,A)
            P_R_dado_LA = prob_retraso_dado_lluvia_y_acc[(lluvia, accidente)]
            
            # Regla de probabilidad total
            P_retraso_total += P_L * P_A_dado_L * P_R_dado_LA

    return P_retraso_total

# --- 2. CONFIGURACIÓN DEL SISTEMA EXPERTO ---
# Probabilidades de entrada (Vida diaria)
P_lluvia = 0.6  # Hoy está nublado (60% lluvia)

P_accidente_dado_lluvia = {
    True: 0.3,   # Si llueve, hay 30% de probabilidad de accidente
    False: 0.05  # Si no llueve, solo 5%
}

P_retraso_critico = {
    (True, True): 0.95,   # Lluvia + Accidente = Retraso seguro
    (True, False): 0.6,   # Solo lluvia = Retraso moderado
    (False, True): 0.8,   # Solo accidente = Retraso alto
    (False, False): 0.1   # Nada = Camino despejado
}

# --- 3. INTERFAZ GRÁFICA (Árbol y Mapa) ---
class RedBayesianaRutas:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa 3: Red Bayesiana - Sistema Experto de Riesgo")
        self.canvas = tk.Canvas(root, width=700, height=500, bg="white")
        self.canvas.pack()
        
        # Calculamos el riesgo usando tu función original adaptada
        self.riesgo = calcular_riesgo_ruta(P_lluvia, P_accidente_dado_lluvia, P_retraso_critico)
        self.dibujar_red_y_arbol()

    def dibujar_red_y_arbol(self):
        # Dibujar Grafo Dirigido (Red Bayesiana)
        self.canvas.create_text(350, 30, text="RED BAYESIANA DE DECISIÓN", font=("Arial", 14, "bold"))
        
        nodos = {'Lluvia': (150, 100), 'Accidente': (350, 100), 'Retraso': (250, 200)}
        for nombre, (x, y) in nodos.items():
            color = "#AED6F1" if nombre != 'Retraso' else "#F1948A"
            self.canvas.create_oval(x-40, y-25, x+40, y+25, fill=color)
            self.canvas.create_text(x, y, text=nombre, font=("Arial", 9, "bold"))

        # Flechas de dependencia
        self.canvas.create_line(190, 100, 310, 100, arrow=tk.LAST) # Lluvia -> Accidente
        self.canvas.create_line(150, 125, 220, 180, arrow=tk.LAST) # Lluvia -> Retraso
        self.canvas.create_line(350, 125, 280, 180, arrow=tk.LAST) # Accidente -> Retraso

        # --- ÁRBOL DE DECISIÓN (Explicación) ---
        y_ar = 300
        self.canvas.create_rectangle(50, y_ar, 650, y_ar+150, outline="gray", dash=(2,2))
        self.canvas.create_text(350, y_ar+20, text="ÁRBOL DE INFERENCIA", font=("Arial", 10, "bold"))
        
        explicacion = (
            f"1. Se detecta probabilidad de lluvia: {P_lluvia*100}%\n"
            f"2. Probabilidad de accidente calculada: {P_accidente_dado_lluvia[True]*100}%\n"
            f"3. Inferencia: El riesgo total de retraso es del {self.riesgo*100:.2f}%\n\n"
        )
        
        veredicto = "RECOMENDACIÓN: "
        if self.riesgo > 0.5:
            veredicto += "TOMAR RUTA ALTERNA (EVITAR VÍA RÁPIDA)"
            color_v = "red"
        else:
            veredicto += "RUTA PRINCIPAL DESPEJADA"
            color_v = "green"

        self.canvas.create_text(350, y_ar+70, text=explicacion, font=("Consolas", 10), justify="center")
        self.canvas.create_text(350, y_ar+120, text=veredicto, font=("Arial", 11, "bold"), fill=color_v)

if __name__ == "__main__":
    root = tk.Tk()
    app = RedBayesianaRutas(root)
    root.mainloop()
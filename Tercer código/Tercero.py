import tkinter as tk

# --- LÓGICA DEL EXPERTO ---
def diagnostico_experto(temp, vibracion, ruido):
    # Reglas simbólicas + pesos
    riesgo = 0
    razones = []
    
    if temp > 80:
        riesgo += 40
        razones.append("- Temperatura Crítica (>80°C)")
    elif temp > 60:
        riesgo += 15
        razones.append("- Temperatura Elevada")
        
    if vibracion > 7:
        riesgo += 40
        razones.append("- Vibración Mecánica Peligrosa")
        
    if ruido == "Inusual":
        riesgo += 20
        razones.append("- Ruido extraño detectado")

    veredicto = "PELIGRO" if riesgo >= 60 else "PRECAUCIÓN" if riesgo >= 30 else "NORMAL"
    return riesgo, veredicto, razones

# --- INTERFAZ ---
class AppDiagnostico:
    def __init__(self, root):
        self.root = root
        self.root.title("Programa 3: Diagnóstico de Fallas")
        self.canvas = tk.Canvas(root, width=500, height=400, bg="#f0f0f0")
        self.canvas.pack()
        
        # DATOS DE ENTRADA (Simulando sensores)
        self.t, self.v, self.r = 85, 4, "Inusual" 
        self.riesgo, self.ver, self.razones = diagnostico_experto(self.t, self.v, self.r)
        
        self.dibujar_dashboard()

    def dibujar_dashboard(self):
        # Título y Datos
        self.canvas.create_text(250, 30, text="REPORTE DEL SISTEMA EXPERTO", font=("Arial", 14, "bold"))
        self.canvas.create_text(120, 80, text=f"Sensores:\n- Temp: {self.t}°C\n- Vib: {self.v}/10\n- Ruido: {self.r}", justify="left")
        
        # Barra de Riesgo (Resultado entre la data)
        self.canvas.create_rectangle(50, 150, 450, 180, fill="white", outline="black")
        color_barra = "red" if self.riesgo >= 60 else "yellow" if self.riesgo >= 30 else "green"
        ancho_riesgo = 50 + (self.riesgo * 4) # Escalar 0-100 a pixeles
        self.canvas.create_rectangle(50, 150, ancho_riesgo, 180, fill=color_barra)
        self.canvas.create_text(250, 165, text=f"Nivel de Riesgo: {self.riesgo}%", font=("Arial", 10, "bold"))

        # Veredicto y Por Qué (Árbol de Razonamiento)
        self.canvas.create_text(250, 220, text=f"VERDICTO: {self.ver}", font=("Arial", 16, "bold"), fill=color_barra)
        
        explicacion = "Justificación del Experto:\n" + "\n".join(self.razones)
        self.canvas.create_text(250, 300, text=explicacion, font=("Consolas", 10), fill="#333")

if __name__ == "__main__":
    root = tk.Tk()
    AppDiagnostico(root)
    root.mainloop()
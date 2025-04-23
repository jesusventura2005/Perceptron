import numpy as np
from perceptron import Perceptron 
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

class PerceptronGUI:
    def __init__(self, window):
        self.window = window
        self.window.geometry("800x800")
        self.window.title("Basic Perceptron")
        
        self.entradas = []
        self.pesos = []
        self.bias = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        input_frame = ttk.Frame(self.window)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Entrada X1:").grid(row=0, column=0, padx=5)
        self.entry_x1 = ttk.Entry(input_frame)
        self.entry_x1.grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Entrada X2:").grid(row=1, column=0, padx=5)
        self.entry_x2 = ttk.Entry(input_frame)
        self.entry_x2.grid(row=1, column=1, padx=5)
        
        ttk.Label(input_frame, text="Peso 1:").grid(row=2, column=0, padx=5)
        self.entry_peso1 = ttk.Entry(input_frame)
        self.entry_peso1.grid(row=2, column=1, padx=5)
        
        ttk.Label(input_frame, text="Peso 2:").grid(row=3, column=0, padx=5)
        self.entry_peso2 = ttk.Entry(input_frame)
        self.entry_peso2.grid(row=3, column=1, padx=5)
        
        ttk.Label(input_frame, text="Bias:").grid(row=4, column=0, padx=5)
        self.entry_bias = ttk.Entry(input_frame)
        self.entry_bias.grid(row=4, column=1, padx=5)
        
        ttk.Label(input_frame, text="Respuesta esperada:").grid(row=5, column=0, padx=5)
        self.entry_respuesta = ttk.Entry(input_frame)
        self.entry_respuesta.grid(row=5, column=1, padx=5)

        ttk.Label(input_frame, text="Función de Activación:").grid(row=6, column=0, padx=5)
        self.activation_var = StringVar(value="escalon")
        self.activation_combo = ttk.Combobox(input_frame, textvariable=self.activation_var, values=["escalon", "sigmoide"], state="readonly")
        self.activation_combo.grid(row=6, column=1, padx=5)
        
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Calcular", command=self.calcular).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Reiniciar", command=self.reiniciar).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Cargar Archivo", command=self.cargar_archivo).pack(side=LEFT, padx=5)
        
        self.tree = ttk.Treeview(self.window, columns=("Entrada X1", "Entrada X2", "Respuesta", "Pesos", "Bias", "Salida"), show="headings")
        self.tree.heading("Entrada X1", text="Entrada X1")
        self.tree.heading("Entrada X2", text="Entrada X2")
        self.tree.heading("Respuesta", text="Respuesta")
        self.tree.heading("Pesos", text="Pesos")
        self.tree.heading("Bias", text="Bias")
        self.tree.heading("Salida", text="Salida")
        self.tree.pack(padx=5, pady=5)

    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    lines = file.readlines()
                    if len(lines) >= 1:
                        config = [float(x) for x in lines[0].strip().split(',')]
                        self.bias = config[0]
                        self.pesos = config[1:]
                        
                        self.entry_bias.delete(0, END)
                        self.entry_bias.insert(0, str(self.bias))
                        self.entry_peso1.delete(0, END)
                        self.entry_peso1.insert(0, str(self.pesos[0]))
                        self.entry_peso2.delete(0, END)
                        self.entry_peso2.insert(0, str(self.pesos[1]))
                        
                        for line in lines[1:]:
                            values = [float(x) for x in line.strip().split(',')]
                            if len(values) >= 3:  # x1, x2, expected response
                                self.entry_x1.delete(0, END)
                                self.entry_x1.insert(0, str(values[0]))
                                self.entry_x2.delete(0, END)
                                self.entry_x2.insert(0, str(values[1]))
                                self.entry_respuesta.delete(0, END)
                                self.entry_respuesta.insert(0, str(values[2]))
                                self.calcular()
                                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")
            
    def calcular(self):
        try:
            x1 = float(self.entry_x1.get())
            x2 = float(self.entry_x2.get())
            peso1 = float(self.entry_peso1.get())
            peso2 = float(self.entry_peso2.get())
            bias = float(self.entry_bias.get())
            respuesta = float(self.entry_respuesta.get())
            activation_type = self.activation_var.get()
            
            perceptron = Perceptron([x1, x2], [peso1, peso2], bias, activation_type)
            salida = perceptron.finalValue()
            
            self.tree.insert("", "end", values=(x1, x2, respuesta, f"[{peso1}, {peso2}]", bias, salida))
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def reiniciar(self):
        self.entry_x1.delete(0, END)
        self.entry_x2.delete(0, END)
        self.entry_peso1.delete(0, END)
        self.entry_peso2.delete(0, END)
        self.entry_bias.delete(0, END)
        self.entry_respuesta.delete(0, END)
        self.activation_var.set("escalon")
        
        for item in self.tree.get_children():
            self.tree.delete(item)

if __name__ == "__main__":
    window = Tk()
    app = PerceptronGUI(window)
    window.mainloop()









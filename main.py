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
        self.input_entries = []  
        self.weight_entries = []  
        
        self.dynamic_frame = None 
        self.create_widgets()
        
        # Cargar archivo de configuración al iniciar
        self.cargar_archivo_inicial("configuracion.txt")

    def create_widgets(self):
        input_frame = ttk.Frame(self.window)
        input_frame.pack(pady=10)
        
        self.bias_label = ttk.Label(input_frame, text="Bias:")
        self.bias_label.grid(row=0, column=0, padx=5)
        self.entry_bias = ttk.Entry(input_frame)
        self.entry_bias.grid(row=0, column=1, padx=5)
        
        self.activation_label = ttk.Label(input_frame, text="Función de Activación:")
        self.activation_label.grid(row=1, column=0, padx=5)
        self.activation_var = StringVar(value="escalon")
        self.activation_combo = ttk.Combobox(input_frame, textvariable=self.activation_var, values=["escalon", "sigmoide"], state="readonly")
        self.activation_combo.grid(row=1, column=1, padx=5)
        
        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Calcular", command=self.calcular).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Reiniciar", command=self.reiniciar).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Cargar Archivo", command=self.cargar_archivo).pack(side=LEFT, padx=5)
        ttk.Button(button_frame, text="Entrada desde Archivo", command=self.entrada_desde_archivo).pack(side=LEFT, padx=5)
        
        self.tree = ttk.Treeview(self.window, columns=("Entradas", "Pesos", "Bias", "Salida"), show="headings")
        self.tree.heading("Entradas", text="Entradas")
        self.tree.heading("Pesos", text="Pesos")
        self.tree.heading("Bias", text="Bias")
        self.tree.heading("Salida", text="Salida")
        self.tree.pack(padx=5, pady=5)
        
        self.dynamic_frame = ttk.Frame(self.window)
        self.dynamic_frame.pack(pady=10)

    def cargar_archivo_inicial(self, file_path):
        """Carga automáticamente el archivo de configuración al iniciar."""
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 1:
                    config = [float(x) for x in lines[0].strip().split(',')]
                    self.bias = config[0]
                    self.pesos = config[1:]
                    
                    self.entry_bias.delete(0, END)
                    self.entry_bias.insert(0, str(self.bias))
                    
                    self.limpiar_dinamico()
                    for peso in self.pesos:
                        self.add_input(peso)
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo: {str(e)}")

    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.cargar_archivo_inicial(file_path)

    def entrada_desde_archivo(self):
        """Procesa un archivo con múltiples líneas de entradas."""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    entradas = [float(x) for x in line.strip().split(',')]
                    if len(entradas) != len(self.pesos):
                        messagebox.showerror("Error", "El número de entradas no coincide con el número de pesos")
                        return
                    
                    perceptron = Perceptron(entradas, self.pesos, self.bias, self.activation_var.get())
                    salida = perceptron.finalValue()
                    
                    # Mostrar resultados en el Treeview
                    self.tree.insert("", "end", values=(entradas, self.pesos, self.bias, salida))
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {file_path}")
        except ValueError:
            messagebox.showerror("Error", "El archivo contiene valores no válidos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al procesar el archivo: {str(e)}")

    def add_input(self, peso):
        row = len(self.input_entries)  
        
        input_label = ttk.Label(self.dynamic_frame, text=f"Entrada X{row + 1}:")
        input_label.grid(row=row, column=0, padx=5)
        input_entry = ttk.Entry(self.dynamic_frame)
        input_entry.grid(row=row, column=1, padx=5)
        self.input_entries.append(input_entry)
        
        weight_label = ttk.Label(self.dynamic_frame, text=f"Peso {row + 1}:")
        weight_label.grid(row=row, column=2, padx=5)
        weight_entry = ttk.Entry(self.dynamic_frame)
        weight_entry.grid(row=row, column=3, padx=5)
        weight_entry.insert(0, str(peso))  
        self.weight_entries.append(weight_entry)

    def limpiar_dinamico(self):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()
        self.input_entries.clear()
        self.weight_entries.clear()

    def calcular(self):
        try:
            entradas = [float(entry.get()) for entry in self.input_entries]
            pesos = [float(entry.get()) for entry in self.weight_entries]
            bias = float(self.entry_bias.get())
            activation_type = self.activation_var.get()
            
            perceptron = Perceptron(entradas, pesos, bias, activation_type)
            salida = perceptron.finalValue()
            
            self.tree.insert("", "end", values=(entradas, pesos, bias, salida))
            
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")
    
    def reiniciar(self):
        self.entry_bias.delete(0, END)
        self.activation_var.set("escalon")
        self.limpiar_dinamico()
        
        for item in self.tree.get_children():
            self.tree.delete(item)

if __name__ == "__main__":
    window = Tk()
    app = PerceptronGUI(window)
    window.mainloop()









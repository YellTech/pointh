import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Window")
        
        # Botão para abrir a janela de configuração
        self.open_config_button = tk.Button(root, text="Abrir Configurações", command=self.open_config_window)
        self.open_config_button.pack(pady=20)

    def open_config_window(self):
        # Cria a janela de configuração
        top = tk.Toplevel(self.root)
        top.title("Configurações")
        top.geometry("300x200")
        top.iconbitmap("config.ico")
        top.grab_set()
        
        # Configurações dos widgets
        ttk.Label(top, text="Carga Horária:").pack(padx=10, pady=(10, 5), anchor="w")

        self.entry_carga_horaria = ttk.Entry(top)
        self.entry_carga_horaria.pack(padx=10, pady=(0, 10), fill=tk.X)
        self.entry_carga_horaria.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_carga_horaria))
        
        # Checkbuttons
        self.check_sequencial = tk.Checkbutton(top, text="Sequencial")
        self.check_sequencial.pack(padx=10, pady=5, anchor="w")

        self.check_sabado = tk.Checkbutton(top, text="Sábado")
        self.check_sabado.pack(padx=10, pady=5, anchor="w")

        self.check_domingo = tk.Checkbutton(top, text="Domingo")
        self.check_domingo.pack(padx=10, pady=5, anchor="w")

        # Botão Salvar
        ttk.Button(top, text="Salvar", command=lambda: self.save_config(top)).pack(pady=10)

    def format_time_entry(self, entry):
        # Exemplo de formatação para a Entry, ajuste conforme necessário
        pass

    def save_config(self, top):
        # Exemplo de função de salvamento, ajuste conforme necessário
        carga_horaria = self.entry_carga_horaria.get()
        sequencial = self.check_sequencial.var.get()
        sabado = self.check_sabado.var.get()
        domingo = self.check_domingo.var.get()
        
        print(f"Carga Horária: {carga_horaria}")
        print(f"Sequencial: {sequencial}")
        print(f"Sábado: {sabado}")
        print(f"Domingo: {domingo}")
        
        top.destroy()

root = tk.Tk()
app = MyApp(root)
root.mainloop()

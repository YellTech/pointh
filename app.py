import tkinter as tk
from tkinter import ttk, messagebox
from db_access import DbAccess

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("PointH")
        self.root.geometry("1024x720")
        
        self.db = DbAccess()
        self.db.create_table()
        
        self.create_menu()
        
        self.label = ttk.Label(self.root, text="Controle de Ponto", font=("Helvetica", 16))
        self.label.pack(pady=10)

        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
    def create_menu(self):
        # Cria a barra de menus
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # Cria o menu "Arquivo"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="MENU", menu=file_menu)
        file_menu.add_command(label="Funcionários")
        file_menu.add_command(label="Sair", command=self.root.quit)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import ttk
from tkcalendar import DateEntry
from controller.manager import Manager
import json
import os

class View(ThemedTk):
    def __init__(self, theme="radiance"):
        super().__init__(theme=theme)
        
        self.config_file = "config.json"
        self.manager = Manager()
        
        self.title("Controle de Ponto")
        self.geometry("1024x720")
        self.minsize(1024, 720)
        self.iconbitmap("icon.ico")
        
        # Configuração das colunas e linhas principais
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=2, uniform="group1")
        self.grid_columnconfigure(2, weight=3, uniform="group1")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

        # Frames
        self.create_frames()
        self.load_config()
        self.update_treeviews_by_id(1)
        
    def create_frames(self):
        # Frame para CRUD de Funcionários
        self.frame_funcionarios = ttk.LabelFrame(self, padding=10, text="Funcionários")
        self.frame_funcionarios.grid(row=0, column=0, sticky="nsew", padx=(10, 5))
        self.frame_funcionarios.grid_columnconfigure(0, weight=1)
        self.frame_funcionarios.grid_rowconfigure(2, weight=1)

        # Frame para Adicionar Ponto
        self.frame_ponto = ttk.LabelFrame(self, padding=10, text="Lançamento de Ponto")
        self.frame_ponto.grid(row=0, column=1, sticky="nsew", padx=(5, 10))
        self.frame_ponto.grid_columnconfigure(0, weight=1)
        self.frame_ponto.grid_columnconfigure(1, weight=1)

        # Frame para Exibir Pontos
        self.frame_treeview = ttk.LabelFrame(self, padding=10, text="Pontos lançados")
        self.frame_treeview.grid(row=1, column=0, columnspan=2, sticky="nsew", padx= (10, 10))
        self.frame_treeview.grid_columnconfigure(0, weight=1)
        self.frame_treeview.grid_columnconfigure(1, weight=1)
        self.frame_treeview.grid_columnconfigure(2, weight=1)
        self.frame_treeview.grid_rowconfigure(2, weight=1)

        # Frame para Dashboards
        self.frame_dashboard = ttk.LabelFrame(self, padding=10, text="Dashboard")
        self.frame_dashboard.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(5, 10))
        self.frame_dashboard.grid_columnconfigure(0, weight=1)
        self.frame_dashboard.grid_rowconfigure(1, weight=1)
        
        # Frame Footer
        self.frame_footer = ttk.Frame(self, padding=10)
        self.frame_footer.grid(row=4, column=0, columnspan=3, sticky="nsew")
        self.frame_footer.grid_columnconfigure(0, weight=1)
        self.frame_footer.grid_rowconfigure(1, weight=1)
        self.footer_label = ttk.Label(self.frame_footer, text="by: YellTech Solutions")
        self.footer_label.grid()

        # Criando os componentes
        self.create_menu()
        self.create_funcionarios_components()
        self.create_ponto_components()
        self.create_treeview_components()
        self.create_dashboard_components()
    
    def create_menu(self):
        # Criação do menu
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)
        
        # Menu Arquivo
        menu_arquivo = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="MENU", menu=menu_arquivo)
        menu_arquivo.add_command(label="Configurações", command=self.open_config_window)
        menu_arquivo.add_command(label="Ajuda")
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.quit)
    
    def create_funcionarios_components(self):
        # Entry para nome do funcionário
        self.label_nome = ttk.Label(self.frame_funcionarios, text="Nome:")
        self.label_nome.grid(row=0, column=0, sticky="ew")
        self.entry_nome = ttk.Entry(self.frame_funcionarios)
        self.entry_nome.grid(row=1, column=0, sticky="ew", pady=5)
        
        # Treeview para listar funcionários
        self.tree_funcionarios = ttk.Treeview(self.frame_funcionarios, columns=("ID", "Nome"), show="headings")
        self.tree_funcionarios.heading("ID", text="ID")
        self.tree_funcionarios.heading("Nome", text="Nome")
        self.tree_funcionarios.column("ID", width=30, anchor="center")
        self.tree_funcionarios.column("Nome", width=150, anchor="center")
        self.tree_funcionarios.grid(row=2, column=0, sticky="nsew", pady=5)

        # Botões CRUD
        self.btn_adicionar = ttk.Button(self.frame_funcionarios, text="Adicionar")
        self.btn_adicionar.grid(row=3, column=0, sticky="ew", padx=5, pady=2)
        self.btn_atualizar = ttk.Button(self.frame_funcionarios, text="Atualizar")
        self.btn_atualizar.grid(row=4, column=0, sticky="ew", padx=5, pady=2)
        self.btn_deletar = ttk.Button(self.frame_funcionarios, text="Deletar")
        self.btn_deletar.grid(row=5, column=0, sticky="ew", padx=5, pady=2)
    
    def create_ponto_components(self):
        # Entradas para os pontos (Entrada 1, Saída 1, etc.)
        self.entry_data = DateEntry(self.frame_ponto, date_pattern='dd/mm/YYYY').grid(row=0, column=0, sticky="ew", pady=5, padx=5)
        ttk.Label(self.frame_ponto, text="Entrada 1").grid(row=1, column=0, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Saída 1").grid(row=1, column=1, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Entrada 2").grid(row=3, column=0, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Saída 2").grid(row=3, column=1, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Entrada 3").grid(row=5, column=0, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Saída 3").grid(row=5, column=1, sticky="w", pady=1)

        # Entradas e saídas
        self.entry_entrada_1 = ttk.Entry(self.frame_ponto)
        self.entry_saida_1 = ttk.Entry(self.frame_ponto)
        self.entry_entrada_2 = ttk.Entry(self.frame_ponto)
        self.entry_saida_2 = ttk.Entry(self.frame_ponto)
        self.entry_entrada_3 = ttk.Entry(self.frame_ponto)
        self.entry_saida_3 = ttk.Entry(self.frame_ponto)

        # Posicionar as entradas e saídas com grid
        
        self.entry_entrada_1.grid(row=2, column=0, sticky="ew", pady=10, padx=5)
        self.entry_saida_1.grid(row=2, column=1, sticky="ew", pady=10)
        self.entry_entrada_2.grid(row=4, column=0, sticky="ew", pady=10, padx=5)
        self.entry_saida_2.grid(row=4, column=1, sticky="ew", pady=10)
        self.entry_entrada_3.grid(row=6, column=0, sticky="ew", pady=10, padx=5)
        self.entry_saida_3.grid(row=6, column=1, sticky="ew", pady=10)
        
        # Botão para adicionar ponto
        self.btn_adicionar_ponto = ttk.Button(self.frame_ponto, text="Adicionar Ponto")
        self.btn_adicionar_ponto.grid(row=7, column=0, columnspan=2, sticky="ew", pady=5)
    
    def create_treeview_components(self):
        # Entradas para intervalo de datas
        self.label_datas = ttk.Label(self.frame_treeview, text="Filtrar por Datas:")
        self.label_datas.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        self.entry_data_inicio = DateEntry(self.frame_treeview, date_pattern='dd/mm/YYYY')
        self.entry_data_inicio.grid(row=1, column=0, sticky="ew", padx=5)
        self.entry_data_fim = DateEntry(self.frame_treeview, date_pattern='dd/mm/YYYY')
        self.entry_data_fim.grid(row=1, column=1, sticky="ew", padx=5)
        self.btn_filtrar = ttk.Button(self.frame_treeview, text="Filtrar")
        self.btn_filtrar.grid(row=1, column=2, sticky="ew", padx=5)
        
        # Treeview para exibir pontos do funcionário selecionado
        self.tree_pontos = ttk.Treeview(self.frame_treeview, columns=("Data", "Total", "Saldo"), show="headings")
        self.tree_pontos.heading("Data", text="Data")
        self.tree_pontos.heading("Total", text="Total")
        self.tree_pontos.heading("Saldo", text="Saldo")
        self.tree_pontos.column("Data", anchor="center")
        self.tree_pontos.column("Total", anchor="center")
        self.tree_pontos.column("Saldo", anchor="center")
        self.tree_pontos.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=5)
    
    def create_dashboard_components(self):
        # Placeholder para dashboards
        pass
        # Gráficos e outras visualizações poderiam ser adicionados aqui
        # Exemplo:
        # self.canvas_dashboard = tk.Canvas(self.frame_dashboard)
        # self.canvas_dashboard.grid(row=1, column=0, sticky="nsew")
    
    def update_treeviews_by_id(self, view_id):
        if view_id == 1:
            data = self.manager.get_employee()
            self.update_treeview(self.tree_funcionarios, data)
        elif view_id == 2:
            pass
        elif view_id == 3:
            data1 = self.manager.get_employee()
            self.update_treeview(self.tree_funcionarios, data1)
        else:
            messagebox.showerror("Erro", "Erro ao atualizar as treeviews.")
                
    def update_treeview(self, treeview, data):
        treeview.delete(*treeview.get_children())
        
        for row in data:
            treeview.insert("", "end", values=row)    
        
    def open_config_window(self):
        # Cria a janela de configuração
        top = tk.Toplevel(self)
        top.title("Configurações")
        top.geometry("300x200")
        top.resizable(False, False)
        top.iconbitmap("config.ico")
        top.grab_set()
        
        
        # Configurações dos widgets
        ttk.Label(top, text="Carga Horária:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_carga_horaria = ttk.Entry(top)
        self.entry_carga_horaria.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        self.load_config()
        self.entry_carga_horaria.insert(0, self.carga_horaria)
          
        ttk.Button(top, text="Salvar", command=lambda: self.save_config(top)).grid(row=1, column=0, columnspan=2, pady=10)
        
    def load_config(self):
        self.config_file = "config.json"
        if not os.path.exists(self.config_file):
            self.ensure_default_config()
        with open(self.config_file, "r") as file:
            config = json.load(file)
            self.carga_horaria = config.get("carga_horaria", "")
            
    
    def save_config(self, top):
        carga_horaria = self.entry_carga_horaria.get()
        config = {"carga_horaria": carga_horaria}
        with open(self.config_file, "w") as file:
            json.dump(config, file, indent=4)
        top.destroy()

    def ensure_default_config(self):
        default_config = {"carga_horaria": ""}
        with open(self.config_file, "w") as file:
            json.dump(default_config, file, indent=4)
        

if __name__ == "__main__":
    app = View()
    app.mainloop()

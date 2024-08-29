import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk

class App(ThemedTk):
    def __init__(self, theme="radiance"):
        super().__init__(theme=theme)
        
        self.title("Controle de Ponto")
        self.geometry("1024x720")
        self.minsize(1024, 720)
        
        # Configuração das colunas e linhas principais
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=2, uniform="group1")
        self.grid_columnconfigure(2, weight=3, uniform="group1")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

        # Frames
        self.create_frames()
        
    def create_frames(self):
        # Frame para CRUD de Funcionários
        self.frame_funcionarios = ttk.LabelFrame(self, padding=10, text="Funcionários")
        self.frame_funcionarios.grid(row=0, column=0, sticky="nsew", padx=(10, 2))

        # Frame para Adicionar Ponto
        self.frame_ponto = ttk.LabelFrame(self, padding=10, text="Lançamento de Ponto")
        self.frame_ponto.grid(row=0, column=1, sticky="nsew")

        # Frame para Exibir Pontos
        self.frame_treeview = ttk.Frame(self, padding=10)
        self.frame_treeview.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Frame para Dashboards
        self.frame_dashboard = ttk.Frame(self, padding=10)
        self.frame_dashboard.grid(row=0, column=2, rowspan=2, sticky="nsew")

        # Criando os componentes
        self.create_funcionarios_components()
        self.create_ponto_components()
        self.create_treeview_components()
        self.create_dashboard_components()
    
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
        self.tree_funcionarios.column("ID", width=30)
        self.tree_funcionarios.column("Nome", width=150)
        self.tree_funcionarios.grid(row=2, column=0, sticky="nsew", pady=5)

        # Configurar grid no frame de funcionários
        self.frame_funcionarios.grid_rowconfigure(2, weight=1)
        self.frame_funcionarios.grid_columnconfigure(0, weight=1)

        # Botões CRUD
        self.btn_adicionar = ttk.Button(self.frame_funcionarios, text="Adicionar")
        self.btn_adicionar.grid(row=3, column=0, sticky="ew", padx=5, pady=2)
        self.btn_atualizar = ttk.Button(self.frame_funcionarios, text="Atualizar")
        self.btn_atualizar.grid(row=4, column=0, sticky="ew", padx=5, pady=2)
        self.btn_deletar = ttk.Button(self.frame_funcionarios, text="Deletar")
        self.btn_deletar.grid(row=5, column=0, sticky="ew", padx=5, pady=2)
    
    def create_ponto_components(self):
        # Entradas para os pontos (Entrada 1, Saída 1, etc.)
        ttk.Label(self.frame_ponto, text="Entrada 1").grid(row=0, column=0, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Saída 1").grid(row=0, column=1, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Entrada 2").grid(row=2, column=0, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Saída 2").grid(row=2, column=1, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Entrada 3").grid(row=4, column=0, sticky="w", pady=1)
        ttk.Label(self.frame_ponto, text="Saída 3").grid(row=4, column=1, sticky="w", pady=1)

        # Entradas e saídas
        self.entry_entrada_1 = ttk.Entry(self.frame_ponto)
        self.entry_saida_1 = ttk.Entry(self.frame_ponto)
        self.entry_entrada_2 = ttk.Entry(self.frame_ponto)
        self.entry_saida_2 = ttk.Entry(self.frame_ponto)
        self.entry_entrada_3 = ttk.Entry(self.frame_ponto)
        self.entry_saida_3 = ttk.Entry(self.frame_ponto)

        # Posicionar as entradas e saídas com grid
        self.entry_entrada_1.grid(row=1, column=0, sticky="ew", pady=5, padx=5)
        self.entry_saida_1.grid(row=1, column=1, sticky="ew", pady=5)
        self.entry_entrada_2.grid(row=3, column=0, sticky="ew", pady=5, padx=5)
        self.entry_saida_2.grid(row=3, column=1, sticky="ew", pady=5)
        self.entry_entrada_3.grid(row=5, column=0, sticky="ew", pady=5, padx=5)
        self.entry_saida_3.grid(row=5, column=1, sticky="ew", pady=5)
        
        # Botão para adicionar ponto
        self.btn_adicionar_ponto = ttk.Button(self.frame_ponto, text="Adicionar Ponto")
        self.btn_adicionar_ponto.grid(row=6, column=0, columnspan=2, sticky="ew", pady=5)
    
    def create_treeview_components(self):
        # Entradas para intervalo de datas
        self.label_datas = ttk.Label(self.frame_treeview, text="Filtrar por Datas:")
        self.label_datas.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        self.entry_data_inicio = ttk.Entry(self.frame_treeview)
        self.entry_data_inicio.grid(row=1, column=0, sticky="ew", padx=5)
        self.entry_data_fim = ttk.Entry(self.frame_treeview)
        self.entry_data_fim.grid(row=1, column=1, sticky="ew", padx=5)
        self.btn_filtrar = ttk.Button(self.frame_treeview, text="Filtrar")
        self.btn_filtrar.grid(row=1, column=2, sticky="ew", padx=5)
        
        # Treeview para exibir pontos do funcionário selecionado
        self.tree_pontos = ttk.Treeview(self.frame_treeview, columns=("Entrada", "Saída"), show="headings")
        self.tree_pontos.heading("Entrada", text="Entrada")
        self.tree_pontos.heading("Saída", text="Saída")
        self.tree_pontos.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=5)

        # Configuração do grid para expansão do Treeview
        self.frame_treeview.grid_rowconfigure(2, weight=1)
        self.frame_treeview.grid_columnconfigure(0, weight=1)
        self.frame_treeview.grid_columnconfigure(1, weight=1)
        self.frame_treeview.grid_columnconfigure(2, weight=1)
    
    def create_dashboard_components(self):
        # Placeholder para dashboards
        self.label_dashboard = ttk.Label(self.frame_dashboard, text="Dashboards")
        self.label_dashboard.grid(row=0, column=0, sticky="ew")
        
        # Gráficos e outras visualizações poderiam ser adicionados aqui
        # Exemplo:
        # self.canvas_dashboard = tk.Canvas(self.frame_dashboard)
        # self.canvas_dashboard.grid(row=1, column=0, sticky="nsew")

        # Configuração do grid para expansão do dashboard
        self.frame_dashboard.grid_rowconfigure(1, weight=1)
        self.frame_dashboard.grid_columnconfigure(0, weight=1)

if __name__ == "__main__":
    app = App()
    app.mainloop()

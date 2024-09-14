import tkinter as tk
from tkinter import messagebox
from ttkthemes import ThemedTk
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import filedialog
from manager import Manager
import shutil
import datetime
from datetime import timedelta
import json
import os
import re

class View(ThemedTk):
    def __init__(self, theme="radiance"):
        super().__init__(theme=theme)
        
        self.config_file = "config.json"
        self.mg = Manager()
        self.employee_id = 0
        self.id_point = 0
        self.presence_flag = None
        self.data_dash = []
        self.control_date = None
        self.sequence_var = tk.BooleanVar()
        self.sabado_var = tk.BooleanVar()
        self.domingo_var = tk.BooleanVar()
        self.protocol("WM_DELETE_WINDOW", self.close_destroy)
        
        self.title("Controle de Ponto")
        self.geometry("1024x720")
        self.iconbitmap("icon.ico")
        
        # Configuração das colunas e linhas principais
        self.grid_columnconfigure(0, weight=1, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_columnconfigure(2, weight=2, uniform="group1")
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=2)

        # Frames
        self.create_frames()
        self.create_menu()
        self.load_config()
        self.update_treeviews_by_id(1)
        self.next_day_sequence(True)
        self.backup_start()
        
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
        self.frame_dashboard = ttk.LabelFrame(self, padding=10, text="Resumo")
        self.frame_dashboard.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=(5, 10))
        self.frame_dashboard.grid_columnconfigure(0, weight=2)
        self.frame_dashboard.grid_columnconfigure(1, weight=1)
        self.frame_dashboard.grid_columnconfigure(2, weight=2)
        self.frame_dashboard.grid_rowconfigure(17, weight=1)
        
        # Frame Footer
        self.frame_footer = ttk.Frame(self, padding=10)
        self.frame_footer.grid(row=4, column=0, columnspan=3, sticky="nsew")
        self.frame_footer.grid_columnconfigure(0, weight=1)
        self.frame_footer.grid_rowconfigure(1, weight=1)
        self.footer_label = ttk.Label(self.frame_footer, text="by: YellTech Solutions")
        self.footer_label.grid()

        # Criando os componentes
        self.create_funcionarios_components()
        self.create_ponto_components()
        self.create_treeview_components()
        self.create_dashboard_components()
        
        #self.update_idletasks()
    
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
        style = ttk.Style()
        style.configure("Treeview", font=("TkDefaultFont", 9))
        self.tree_funcionarios = ttk.Treeview(self.frame_funcionarios, columns=("ID", "Nome"), show="headings")
        self.tree_funcionarios.heading("ID", text="ID")
        self.tree_funcionarios.heading("Nome", text="Nome")
        self.tree_funcionarios.column("ID", width=20, anchor="center")
        self.tree_funcionarios.column("Nome", width=150, anchor="w")
        self.tree_funcionarios.grid(row=2, column=0, sticky="nsew", pady=5)
        
        self.tree_funcionarios.bind("<Double-1>", self.selected_employee)

        # Botões CRUD
        self.btn_adicionar = ttk.Button(self.frame_funcionarios, text="Adicionar",
                                        command= self.add_employee_view)
        self.btn_adicionar.grid(row=3, column=0, sticky="ew", padx=5, pady=2)
        self.btn_atualizar = ttk.Button(self.frame_funcionarios, text="Editar",
                                        command=self.update_employee_view)
        self.btn_atualizar.grid(row=4, column=0, sticky="ew", padx=5, pady=2)
        self.btn_deletar = ttk.Button(self.frame_funcionarios, text="Deletar", command=self.delete_employee)
        self.btn_deletar.grid(row=5, column=0, sticky="ew", padx=5, pady=2)
    
    def create_ponto_components(self):
        self.employee_label = ttk.Label(self.frame_ponto, text="Selecione um funcionário", foreground="red")
        self.employee_label.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5, padx=5)
        # Entradas para os pontos (Entrada 1, Saída 1, etc.)
        self.entry_data = DateEntry(self.frame_ponto, date_pattern='dd-mm-YYYY')
        self.entry_data.grid(row=1, column=0, sticky="ew", pady=5, padx=(0, 15))
        self.presence_box = ttk.Combobox(self.frame_ponto, state="readonly")
        self.presence_box['values'] = ("NORMAL", "FALTOU", "ATESTADO", "FERIADO")
        self.presence_box.current(0)
        self.presence_box.grid(row=1, column=1, sticky="ew", pady=5, padx=(15, 0))
        self.presence_box.bind("<<ComboboxSelected>>", lambda event: self.presence_selected())
        
        ttk.Label(self.frame_ponto, text="Entrada 1").grid(row=2, column=0, sticky="ew", pady=1, padx=(0, 15))
        ttk.Label(self.frame_ponto, text="Saída 1").grid(row=2, column=1, sticky="ew", pady=1, padx=(15, 0))
        ttk.Label(self.frame_ponto, text="Entrada 2").grid(row=4, column=0, sticky="ew", pady=1, padx=(0, 15))
        ttk.Label(self.frame_ponto, text="Saída 2").grid(row=4, column=1, sticky="ew", pady=1, padx=(15, 0))
        ttk.Label(self.frame_ponto, text="Entrada 3").grid(row=6, column=0, sticky="ew", pady=1, padx=(0, 15))
        ttk.Label(self.frame_ponto, text="Saída 3").grid(row=6, column=1, sticky="ew", pady=1, padx=(15, 0))

        # Entradas e saídas
        self.entry_entrada_1 = ttk.Entry(self.frame_ponto)
        self.entry_saida_1 = ttk.Entry(self.frame_ponto)
        self.entry_entrada_2 = ttk.Entry(self.frame_ponto)
        self.entry_saida_2 = ttk.Entry(self.frame_ponto)
        self.entry_entrada_3 = ttk.Entry(self.frame_ponto)
        self.entry_saida_3 = ttk.Entry(self.frame_ponto)

        # Posicionar as entradas e saídas com grid
        
        self.entry_entrada_1.grid(row=3, column=0, sticky="ew", pady=(1, 10), padx=(0, 15))
        self.entry_saida_1.grid(row=3, column=1, sticky="ew", pady=(1, 10), padx=(15, 0))
        self.entry_entrada_2.grid(row=5, column=0, sticky="ew", pady=(1, 10), padx=(0, 15))
        self.entry_saida_2.grid(row=5, column=1, sticky="ew", pady=(1, 10), padx=(15, 0))
        self.entry_entrada_3.grid(row=7, column=0, sticky="ew", pady=(1, 10), padx=(0, 15))
        self.entry_saida_3.grid(row=7, column=1, sticky="ew", pady=(1, 10), padx=(15, 0))
        
        # Binds entrys
        self.entry_entrada_1.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_entrada_1))
        self.entry_saida_1.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_saida_1))
        self.entry_entrada_2.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_entrada_2))
        self.entry_saida_2.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_saida_2))
        self.entry_entrada_3.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_entrada_3))
        self.entry_saida_3.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_saida_3))
        
        # Botôes para ponto
        self.btn_adicionar_ponto = ttk.Button(self.frame_ponto, text="Adicionar", command=self.add_point)
        self.btn_adicionar_ponto.grid(row=8, column=0, columnspan=2, sticky="ew", pady=2)
        self.btn_edit_point = ttk.Button(self.frame_ponto, text="Editar", command=self.update_point)
        self.btn_edit_point.grid(row=9, column=0, columnspan=2, sticky="ew", pady=2)
        self.btn_delete_point = ttk.Button(self.frame_ponto, text="Deletar", command=self.delete_point)
        self.btn_delete_point.grid(row=10, column=0, columnspan=2, sticky="ew", pady=2)
    
    def create_treeview_components(self):
        # Entradas para intervalo de datas
        self.label_datas = ttk.Label(self.frame_treeview, text="Filtrar por Datas:")
        self.label_datas.grid(row=0, column=0, columnspan=3, sticky="ew")
        
        self.entry_data_inicio = DateEntry(self.frame_treeview, date_pattern='dd-mm-YYYY')
        self.entry_data_inicio.grid(row=1, column=0, sticky="ew", padx=5)
        self.entry_data_fim = DateEntry(self.frame_treeview, date_pattern='dd-mm-YYYY')
        self.entry_data_fim.grid(row=1, column=1, sticky="ew", padx=5)
        self.btn_filtrar = ttk.Button(self.frame_treeview, text="Filtrar", command= self.filter_treeview_point)
        self.btn_filtrar.grid(row=1, column=2, sticky="ew", padx=5)
        
        # Treeview para exibir pontos do funcionário selecionado
        self.tree_pontos = ttk.Treeview(self.frame_treeview, columns=("ID", "Data", "Total", "Saldo", "Status"), show="headings")
        self.tree_pontos.heading("ID", text="ID")
        self.tree_pontos.heading("Data", text="Data")
        self.tree_pontos.heading("Total", text="Total")
        self.tree_pontos.heading("Saldo", text="Saldo")
        self.tree_pontos.heading("Status", text="Status")
        self.tree_pontos.column("ID", anchor="center", width=30)
        self.tree_pontos.column("Data", anchor="center", width=105)
        self.tree_pontos.column("Total", anchor="center", width=105)
        self.tree_pontos.column("Saldo", anchor="center", width=105)
        self.tree_pontos.column("Status", anchor="w", width=105)
        self.tree_pontos.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=5)
        
        self.tree_pontos.bind("<Double-1>", self.selected_point)
    
    def create_dashboard_components(self):
        # Exemplo de dados
        self.clear_frame(self.frame_dashboard)
        horas_trabalhadas_normais, horas_esperadas = self.mg.calc_hours_trabalhadas(self.data_dash)
        horas_atestados, quantidade_atestados = self.mg.calc_hours_atestado(self.data_dash) 
        horas_feriado, quantidade_feriados = self.mg.calc_hour_feriado(self.data_dash)
        horas_faltou, quantidade_faltas = self.mg.calc_hours_faltou(self.data_dash)
        horas_extras = self.mg.calc_hours_extra(self.data_dash)
        horas_negativas = self.mg.calc_hours_negativas(self.data_dash)
        
        if self.data_dash:
            label_employee_dash = ttk.Label(self.frame_dashboard, text=f"Funcionário: {self.entry_nome.get()}", font=("TkDefaultFont", 12,"bold"))
            label_employee_dash.grid(row=0, column=0, sticky="ew")
            label_filter_data = ttk.Label(self.frame_dashboard, text=f"Período: {self.entry_data_inicio.get()} a {self.entry_data_fim.get()}\n", font=("TkDefaultFont", 12,"bold"))
            label_filter_data.grid(row=1, column=0, sticky="ew")
            
            fonte = ("TkDefaultFont", 12,"bold")
            
            label_horas_trabalhadas = ttk.Label(self.frame_dashboard, text=f"Horas trabalhadas: {horas_trabalhadas_normais}", font=fonte)
            label_horas_trabalhadas.grid(row=2, column=0, sticky="ew")
            
            label_horas_atestado = ttk.Label(self.frame_dashboard, text=f"Horas atestado: {horas_atestados}", font=fonte)
            label_horas_atestado.grid(row=3, column=0, sticky="ew")
            
            label_horas_feriado = ttk.Label(self.frame_dashboard, text=f"Horas feriados: {horas_feriado}", font=fonte)
            label_horas_feriado.grid(row=4, column=0, sticky="ew")
            
            label_horas_extras = ttk.Label(self.frame_dashboard, text=f"Horas extras: {horas_extras}", font=fonte)
            label_horas_extras.grid(row=5, column=0, sticky="ew")
            
            label_horas_esperadas = ttk.Label(self.frame_dashboard, text=f"Horas esperadas: {horas_esperadas}", font=fonte)
            label_horas_esperadas.grid(row=6, column=0, sticky="ew")
            
            separador = ttk.Separator(self.frame_dashboard, orient="horizontal")
            separador.grid(row=7, column=0, columnspan=3, sticky="nsew")
            
            horas_totais = self.mg.minutes_to_time(self.mg.time_to_minute(horas_trabalhadas_normais) + self.mg.time_to_minute(horas_atestados) + self.mg.time_to_minute(horas_feriado))
            
            label_horas_totais_trabalhadas = ttk.Label(self.frame_dashboard, font=fonte, foreground="blue", text=f"Horas totais: {horas_totais}\n")
            label_horas_totais_trabalhadas.grid(row=8, column=0, sticky="ew")
            
            balanço = self.mg.minutes_to_time(self.mg.time_to_minute(horas_totais) - self.mg.time_to_minute(horas_esperadas))
            
            label_quantidade_atestados = ttk.Label(self.frame_dashboard, foreground="green" if self.mg.time_to_minute(balanço) >= 0 else "red", text=f"Balanço total de horas: {balanço}\n", font=fonte)
            label_quantidade_atestados.grid(row=9, column=0, sticky="ew")
            
            label_horas_faltou = ttk.Label(self.frame_dashboard, text=f"Horas faltou: {horas_faltou}", font=fonte)
            label_horas_faltou.grid(row=10, column=0, sticky="ew")
            
            label_horas_negativas = ttk.Label(self.frame_dashboard, text=f"Deficit Horas diárias: {horas_negativas}", font=fonte)
            label_horas_negativas.grid(row=11, column=0, sticky="ew")
            
            separador1 = ttk.Separator(self.frame_dashboard, orient="horizontal")
            separador1.grid(row=12, column=0, columnspan=3, sticky="nsew")
    
            label_horas_nao_cumpridas = ttk.Label(self.frame_dashboard, font=fonte, foreground="red", text=f"Horas totais não cumpridas: {self.mg.minutes_to_time(self.mg.time_to_minute(horas_faltou) + self.mg.time_to_minute(horas_negativas))}\n")
            label_horas_nao_cumpridas.grid(row=13, column=0, sticky="ew")
            
            label_quantidade_atestados = ttk.Label(self.frame_dashboard, text=f"Quantidade de atestados: {quantidade_atestados}", font=fonte)
            label_quantidade_atestados.grid(row=14, column=0, sticky="ew")
            
            label_quantidade_feriados = ttk.Label(self.frame_dashboard, text=f"Quantidade de feriados: {quantidade_feriados}", font=fonte)
            label_quantidade_feriados.grid(row=15, column=0, sticky="ew")
            
            label_quantidade_faltas = ttk.Label(self.frame_dashboard, text=f"Quantidade faltas: {quantidade_faltas}", font=fonte)
            label_quantidade_faltas.grid(row=16, column=0, sticky="ew")      
            
    def selected_point(self, event):
        try:
            item = self.tree_pontos.selection()[0]
            value = self.tree_pontos.item(item, 'values')
            point = self.mg.handle_get_point_tree(value[0], self.employee_id)
            self.id_point = value[0]
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, point[2])
            presence_map = {"NORMAL": 0, "FALTOU": 1, "ATESTADO": 2, "FERIADO": 3}
            if point[12] in presence_map:
                index = presence_map[point[12]]
                if index < len(self.presence_box["values"]):
                    self.presence_box.current(index)
            self.entry_entrada_1.delete(0, tk.END)
            self.entry_entrada_1.insert(0, point[3])
            self.entry_saida_1.delete(0, tk.END)
            self.entry_saida_1.insert(0, point[4])
            self.entry_entrada_2.delete(0, tk.END)
            self.entry_entrada_2.insert(0, point[5])
            self.entry_saida_2.delete(0, tk.END)
            self.entry_saida_2.insert(0, point[6])
            self.entry_entrada_3.delete(0, tk.END)
            self.entry_entrada_3.insert(0, point[7])
            self.entry_saida_3.delete(0, tk.END)
            self.entry_saida_3.insert(0, point[8])
        except:
            pass
    
    def selected_employee(self, event):
        try:
            today = datetime.date.today()
            item = self.tree_funcionarios.selection()[0]
            self.values = self.tree_funcionarios.item(item, 'values')
            self.employee_id = self.values[0]
            self.employee_label.configure(text=self.values[1])
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, self.values[1])
            self.entry_data.set_date(today)
            self.next_day_sequence(True)
            self.clear_entrys([self.entry_entrada_1, self.entry_entrada_2, self.entry_entrada_3, 
                               self.entry_saida_1, self.entry_saida_2, self.entry_saida_3])
            self.update_treeviews_by_id(2)
            self.presence_box_reset()
            self.clear_frame(self.frame_dashboard)
        except:
            pass
    
    def add_employee_view(self):
        self.mg.handle_add_employee(self.entry_nome.get())
        self.entry_nome.delete(0, tk.END)
        self.employee_id = None
        self.label_selected_employee()
        self.update_treeviews_by_id(1)
        
    def update_employee_view(self):
        if self.entry_nome.get() and self.employee_id:
            alert =  messagebox.askyesno("Atenção", f"Deseja mesmo editar o funcionário com o ID:\n\n{self.employee_id}")
            if alert:
                self.mg.handle_update_employee(self.employee_id, self.values[1], self.entry_nome.get())
                self.entry_nome.delete(0, tk.END)
                self.employee_id = None
                self.label_selected_employee()
                self.clear_entrys([self.entry_entrada_1, self.entry_entrada_2, self.entry_entrada_3, 
                               self.entry_saida_1, self.entry_saida_2, self.entry_saida_3])
                self.update_treeviews_by_id(1)
        elif self.employee_id:
            messagebox.showerror("Erro", "O nome nao pode ser vazio.")
        else:
            messagebox.showerror("Erro", "Selecione um funcionário para editar.")
            
    def delete_employee(self):
        if self.entry_nome.get() and self.employee_id:
            alert =  messagebox.askyesno("Atenção", f"Deseja mesmo deletar o funcionário com o ID:\n\n{self.employee_id}")
            if alert:
                self.mg.handle_delete_employee(self.employee_id)
                self.entry_nome.delete(0, tk.END)
                self.employee_id = None
                self.label_selected_employee()
                self.update_treeviews_by_id(1)
                self.update_treeviews_by_id(2)
                self.clear_entrys([self.entry_entrada_1, self.entry_entrada_2, self.entry_entrada_3, 
                               self.entry_saida_1, self.entry_saida_2, self.entry_saida_3])
                self.presence_box_reset()
        else:
            messagebox.showerror("Erro", "Selecione um funcionário para deletar.")
    
    def add_point(self):
        entrys_points = [self.employee_id, self.entry_data.get(), self.entry_entrada_1.get(), self.entry_saida_1.get(),
                                      self.entry_entrada_2.get(), self.entry_saida_2.get(), self.entry_entrada_3.get(),
                                      self.entry_saida_3.get(), self.presence_box.get()]
        result = self.mg.handle_add_point(entrys_points, self.presence_flag)
        if result:
            self.clear_entrys([self.entry_entrada_1, self.entry_entrada_2, self.entry_entrada_3, 
                               self.entry_saida_1, self.entry_saida_2, self.entry_saida_3])
            self.update_treeviews_by_id(2)
            self.presence_flag = None
            self.presence_box_reset()
            self.presence_selected()
            self.next_day_sequence()
    
    def update_point(self):
        entrys_point_update = [self.id_point, self.entry_data.get(), self.entry_entrada_1.get(), self.entry_saida_1.get(),
                                      self.entry_entrada_2.get(), self.entry_saida_2.get(), self.entry_entrada_3.get(),
                                      self.entry_saida_3.get(), self.presence_box.get()]
        result = self.mg.handle_update_point(entrys_point_update, self.presence_flag)
        if result:
            self.clear_entrys([self.entry_entrada_1, self.entry_entrada_2, self.entry_entrada_3, 
                               self.entry_saida_1, self.entry_saida_2, self.entry_saida_3])
            self.update_treeviews_by_id(2)
            self.presence_flag = None
            self.presence_box_reset()
            self.presence_selected()
            
    def delete_point(self):
        if self.id_point:
            alert =  messagebox.askyesno("Atenção", f"Deseja mesmo deletar o ponto com o ID:\n\n{self.id_point}")
            if alert:
                self.mg.handle_delete_point(self.id_point)
                self.entry_nome.delete(0, tk.END)
                self.id_point = None
                self.clear_entrys([self.entry_entrada_1, self.entry_entrada_2, self.entry_entrada_3, 
                               self.entry_saida_1, self.entry_saida_2, self.entry_saida_3])
                self.update_treeviews_by_id(2)
                self.presence_box_reset()
        else:
            messagebox.showerror("Erro", "Selecione um ponto para deletar.") 

    def presence_selected(self):
        presence = self.presence_box.get()
        if presence in ("FALTOU", "ATESTADO", "FERIADO"):
            self.entry_entrada_1.delete(0, tk.END)
            self.entry_entrada_1.insert(0, "00:00")
            self.entry_entrada_1.configure(state="disable")
            self.entry_saida_1.delete(0, tk.END)
            self.entry_saida_1.insert(0, "00:00")
            self.entry_saida_1.configure(state="disable")
            self.entry_entrada_2.delete(0, tk.END)
            self.entry_entrada_2.insert(0, "00:00")
            self.entry_entrada_2.configure(state="disable")
            self.entry_saida_2.delete(0, tk.END)
            self.entry_saida_2.insert(0, "00:00")
            self.entry_saida_2.configure(state="disable")
            self.entry_entrada_3.delete(0, tk.END)
            self.entry_entrada_3.insert(0, "00:00")
            self.entry_entrada_3.configure(state="disable")
            self.entry_saida_3.delete(0, tk.END)
            self.entry_saida_3.insert(0, "00:00")
            self.entry_saida_3.configure(state="disable")
            if presence == "FALTOU":
                self.presence_flag = 1
            elif presence == "ATESTADO":
                self.presence_flag = 2
            elif presence == "FERIADO":
                self.presence_flag = 3
        else:
            self.presence_box_reset()
            self.presence_flag = None
            self.entry_entrada_1.configure(state="normal")
            self.entry_entrada_1.delete(0, tk.END)
            self.entry_entrada_1.insert(0, "")
            self.entry_saida_1.configure(state="normal")
            self.entry_saida_1.delete(0, tk.END)
            self.entry_saida_1.insert(0, "")
            self.entry_entrada_2.configure(state="normal")
            self.entry_entrada_2.delete(0, tk.END)
            self.entry_entrada_2.insert(0, "")
            self.entry_saida_2.configure(state="normal")
            self.entry_saida_2.delete(0, tk.END)
            self.entry_saida_2.insert(0, "")
            self.entry_entrada_3.configure(state="normal")
            self.entry_entrada_3.delete(0, tk.END)
            self.entry_entrada_3.insert(0, "")
            self.entry_saida_3.configure(state="normal")
            self.entry_saida_3.delete(0, tk.END)
            self.entry_saida_3.insert(0, "")

    def filter_treeview_point(self):
        self.update_treeviews_by_id(2, self.entry_data_inicio.get(), self.entry_data_fim.get())
        self.create_dashboard_components()
        
    def update_treeviews_by_id(self, view_id, data_initial = None, data_end = None):
        if view_id == 1:
            data = self.mg.get_employee()
            self.update_treeview(self.tree_funcionarios, data)
        elif view_id == 2:
            indices = [0, 2, 9, 11, 12]
            self.data_dash = self.mg.get_point_employee(self.employee_id, data_initial, data_end)
            data = [tuple(tupla[i] for i in indices) for tupla in self.data_dash]
            self.update_treeview(self.tree_pontos, data)
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
        top.geometry("270x400")
        top.resizable(False, False)
        top.iconbitmap("config.ico")
        top.grab_set()
        
        
        # Configurações dos widgets
        ttk.Label(top, text="Carga Horária:").pack(pady=(10, 0), padx=70, anchor="w")
        self.entry_carga_horaria = ttk.Entry(top)
        self.entry_carga_horaria.pack(padx=70, anchor="w")
        self.entry_carga_horaria.bind('<FocusOut>', lambda e: self.format_time_entry(self.entry_carga_horaria))
        
        self.sequence_check = ttk.Checkbutton(top, text="Sequencial?", variable=self.sequence_var)
        self.sequence_check.pack(pady=(25, 10), padx=70, anchor="w")
        self.sabado_check = ttk.Checkbutton(top, text="Sabádo?", variable=self.sabado_var)
        self.sabado_check.pack(pady=10, padx=70, anchor="w")
        self.domingo_check = ttk.Checkbutton(top, text="Domingo?", variable=self.domingo_var)
        self.domingo_check.pack(pady=10, padx=70, anchor="w")
        
        self.backup = ttk.Button(top, text="Backup", command=self.backup_select)
        self.backup.pack(pady=(10, 0), padx=70, anchor="w")
        self.load_config()
        self.entry_carga_horaria.insert(0, self.carga_horaria)
          
        ttk.Button(top, text="Salvar", command=lambda: self.save_config(top)).pack(pady=10, padx=70, anchor="w")
        
    def load_config(self):
        self.config_file = "config.json"
        if not os.path.exists(self.config_file):
            self.ensure_default_config()
        with open(self.config_file, "r") as file:
            config = json.load(file)
            self.carga_horaria = config.get("carga_horaria", "")
            self.sequence_var.set(config.get("sequencial", ""))
            self.sabado_var.set(config.get("sabado", ""))
            self.domingo_var.set(config.get("domingo", ""))
            self.backup_dir = config.get("backup_dir", "")  
              
    def save_config(self, top):
        carga_horaria = self.entry_carga_horaria.get()
        digits = re.sub(r'\D', '', carga_horaria)
        if not digits or int(digits) == "0":
            messagebox.showerror("Erro", "A carga horária dever conter apenas numeros e\nser difente de zero ou vazio.")
            return
        config = {"carga_horaria": carga_horaria,
                  "sequencial": self.sequence_var.get(),
                  "sabado": self.sabado_var.get(),
                  "domingo": self.domingo_var.get(),
                  "backup_dir": self.backup_dir
                  }
        with open(self.config_file, "w") as file:
            json.dump(config, file, indent=4)
        top.destroy()

    def ensure_default_config(self):
        default_config = {"carga_horaria": "8:48",
                          "sequencial": False,
                          "sabado": False,
                          "domingo": False,
                          "backup_dir": None
                          }
        with open(self.config_file, "w") as file:
            json.dump(default_config, file, indent=4)
    
    def label_selected_employee(self):
        self.employee_label.configure(text="Selecione um funcionário")

    def format_time_entry(self, entry_widget):
        """
        Formata a entrada de tempo em uma Entry widget para o formato HH:MM.
        :param entry_widget: O widget Entry que contém a entrada de tempo.
        """
        # Obtém o texto atual da Entry
        current_text = entry_widget.get()
        
        # Remove tudo que não é dígito
        digits = re.sub(r'\D', '', current_text)
        
        # Adiciona zeros à esquerda se necessário
        if len(digits) > 4:
            digits = digits[:4]
        if len(digits) == 4:
            if int(digits[:2]) < 24 and int(digits[2:]) < 60 :
                formatted_time = f"{digits[:2]}:{digits[2:]}"
            else:
                formatted_time = f""
        elif len(digits) == 3:
            if int(digits[:1]) < 24 and int(digits[1:]) < 60:
                formatted_time = f"0{digits[:1]}:{digits[1:]}"
            else:
                formatted_time = f""
        elif len(digits) == 2:
            if int(digits[:2]) < 24:
                formatted_time = f"{digits[:2]}:00"
            else:
                formatted_time = f""
        elif len(digits) == 1:
            formatted_time = f"0{digits[:1]}:00"
        else:
            formatted_time = digits
        
        # Atualiza o texto da Entry com o formato correto
        entry_widget.delete(0, 'end')
        entry_widget.insert(0, formatted_time)
        
        # Move o cursor para o final da entrada
        entry_widget.icursor('end')

    def presence_box_reset(self):
        self.presence_box.current(0)
        
    def clear_entrys(self, entrys):
        for i in entrys:
            i.delete(0, tk.END)

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def close_destroy(self):
        self.mg.close_connection_manager()
        self.quit()

    def backup_select(self):
        root = tk.Tk()
        root.withdraw()
        self.backup_dir = filedialog.askdirectory()

        if self.backup_dir:
            return self.backup_dir
        else:
            return None
        
    def backup_start(self):
        if self.backup_dir:
            database = "database.db"
            pasta = os.path.join(self.backup_dir, "backup_pointh")
            os.makedirs(pasta, exist_ok=True)
            destino = os.path.join(pasta, database)
            shutil.copy2(database, destino)
        else:
            question = messagebox.askyesno("Atenção", "Backup não configurado, configurar?")
            if question:
                self.open_config_window()
    
    def next_day_sequence(self, init=None):
        
        new_date = self.entry_data.get_date() + timedelta(days=1)
        new_date_str = str(new_date)
        
        if self.sequence_var.get() and self.sabado_var.get() and not self.domingo_var.get():
            while new_date.weekday() ==5:
                new_date += timedelta(days=1)
            new_date_str = str(new_date)
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, self.mg.convert_to_br_date(new_date_str))
            return
        elif self.sequence_var.get() and self.domingo_var.get() and not self.sabado_var.get():
            while new_date.weekday() == 6:
                new_date += timedelta(days=1)
            new_date_str = str(new_date)
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, self.mg.convert_to_br_date(new_date_str))
            return
        elif self.sequence_var.get() and self.sabado_var.get() and self.domingo_var.get():
            while new_date.weekday() >= 5:
                new_date += timedelta(days=1)
            new_date_str = str(new_date)
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, self.mg.convert_to_br_date(new_date_str))
            return
        elif self.sequence_var.get() and not init: 
            new_date_str = str(new_date)
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, self.mg.convert_to_br_date(new_date_str))
            return
        else:
            date_save = self.entry_data.get()
            self.entry_data.delete(0, tk.END)
            self.entry_data.insert(0, date_save)
            return
    
if __name__ == "__main__":
    app = View()
    app.mainloop()

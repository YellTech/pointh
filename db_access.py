import sqlite3
from tkinter import messagebox

class DbAccess:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor() if self.conn else None
            
    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados:\n {e}")
            return None    
            
    def create_table(self):
        if self.conn:
            try:
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS funcionarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL
                )                    
                """)
                
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS banco_horas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    funcionario_id INTEGER,
                    data  TEXT NOT NULL,
                    entrada_1 REAL,
                    saida_1 REAL,
                    entrada_2 REAL,
                    saida_2 REAL,
                    entrada_3 REAL,
                    saida_3,
                    total REAL,
                    carga_dia REAL,
                    saldo_dia REAL,
                    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
                )                    
                """)
                
                self.conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao criar tabelas:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para criar tabelas.")
            
    def add_employee(self, name):
        if self.conn:
            try:
                self.cursor.execute("""
                INSERT INTO funcionarios (nome)
                VALUE (?)                    
                """, (name))
                
                self.conn.commit()
                messagebox.showinfo("Atenção", f"Funcionário {name} adicionado com sucesso.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao adicionar funcionário:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para adicionar funcionário.")
    
    def close_connection(self):
        if self.conn:
            self.conn.close()
        else:
            messagebox.showerror("Erro", "Erro nenhuma conexão para fechar.")
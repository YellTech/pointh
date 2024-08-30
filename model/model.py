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
                    entrada_1 REAL NOT NULL,
                    saida_1 REAL NOT NULL,
                    entrada_2 REAL NOT NULL,
                    saida_2 REAL NOT NULL,
                    entrada_3 REAL NOT NULL,
                    saida_3 NOT NULL,
                    total REAL NOT NULL,
                    carga_dia REAL NOT NULL,
                    saldo_dia REAL NOT NULL,
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
    
    def update_employee(self, id, name):
        if self.conn:
            try:
                self.cursor.execute("""
                UPDATE funcionarios SET nome = ? WHERE id = ?
                """, (name, id))
                
                self.conn.commit()
                messagebox.showinfo("Atenção", f"Funcionário atualizado com sucesso.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao atualizar funcionário:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para atualizar funcionário.")  
            
    def delete_employee(self, id):
        if self.conn:
            try:
                self.cursor.execute("""
                DELETE FROM funcionarios WHERE id = ?                    
                """, (id))
                
                self.conn.commit()
                messagebox.showinfo("Atenção", f"Funcionário deletado com sucesso.")   
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao deletar Funcionário:\n {e}")      
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para deletar funcionário.")
            
    def add_time_entry(self, funcionario_id, data, entrada_1, saida_1, 
                       entrada_2, saida_2, entrada_3, saida_3,
                       total, carga_dia, saldo_dia):
        if self.conn:
            try:
                self.cursor.execute("""
                INSERT INTO banco_horas (funcionario_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia)                    
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (funcionario_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia)
                )

                self.conn.commit()
                messagebox.showinfo("Atenção", f"Ponto adicionado com sucesso.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao adicionar ponto:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para adicionar ponto.")

    def update_time_entry(self, entry_id, entrada_1, saida_1, 
                       entrada_2, saida_2, entrada_3, saida_3,
                       total, carga_dia, saldo_dia):
        if self.conn:
            try:
                self.cursor.execute("""
                UPDATE banco_horas
                SET entrada_1 = ?, saida_1 = ?, entrada_2 = ?, saida_2 = ?, entrada_3 = ?, saida_3 = ?, total = ?, carga_dia = ?, saldo_dia = ?
                WHERE id = ?
                """, (entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia, entry_id))
                
                self.conn.commit()
                messagebox.showinfo("Atenção", f"Ponto atualizado com sucesso.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao atualizar ponto:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para atualizar ponto.")
            
    def delete_time_entry(self, entry_id):
        if self.conn:
            try:
                self.cursor.execute("""
                DELETE FROM banco_horas WHERE id = ?
                """, (entry_id))
                
                self.conn.commit()
                messagebox.showinfo("Atenção", f"Ponto deletado com sucesso.")
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao deletar ponto:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para deletar ponto.")
            
    def close_connection(self):
        if self.conn:
            self.conn.close()
        else:
            messagebox.showerror("Erro", "Erro nenhuma conexão para fechar.")
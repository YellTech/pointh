import sqlite3
from tkinter import messagebox

"""
Optei por usar messagebox no model ao invez de retornar para controller->view e entao exibir a messagebox por questões
de produtividade, sinta-se a vontade para modificar.
"""

class DbAccess:
    def __init__(self, db_name="model/database.db"):
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
                    data  DATE NOT NULL,
                    entrada_1 REAL NOT NULL,
                    saida_1 REAL NOT NULL,
                    entrada_2 REAL NOT NULL,
                    saida_2 REAL NOT NULL,
                    entrada_3 REAL NOT NULL,
                    saida_3 REAL NOT NULL,
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
                VALUES (?)                    
                """, (name,))
                
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
            
    def verify_employee(self, name):
        if self.conn:
            try:
                self.cursor.execute("""
                SELECT COUNT(1) FROM funcionarios WHERE LOWER(nome) = LOWER(?)
                """, (name,))
                result = self.cursor.fetchone()
                if result[0]>0:
                    return True
                else:
                    return False
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao listar Funcionário:\n {e}") 
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para listar funcionário.") 
            
    def get_all_employee(self):
        if self.conn:
            try:
                self.cursor.execute("""
                SELECT id, nome FROM funcionarios ORDER BY nome ASC
                """)
                rows = self.cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao listar Funcionário:\n {e}") 
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para listar funcionário.")
                
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
            
    def get_all_entry(self):
        if self.conn:
            try:
                self.cursor.execute("""
                SELECT * FROM banco_horas
                """)
                rows = self.cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao listar pontos:\n {e}") 
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para listar pontos.")
            
    def close_connection(self):
        if self.conn:
            self.conn.close()
        else:
            messagebox.showerror("Erro", "Erro nenhuma conexão para fechar.")
            
if __name__ == "__main__":
    db = DbAccess()
    print(db.verify_employee("samuel da silva proença"))
    
    
import sqlite3
from tkinter import messagebox

"""
Optei por usar messagebox no model  e não ter que retornar para controller->view e entao exibir a messagebox por questões
de produtividade, sinta-se a vontade para modificar.
"""

class DbAccess:
    def __init__(self, db_name="model/database.db"):
        """
        The function initializes a database connection with a default database name.
        
        :param db_name: The `db_name` parameter in the `__init__` method is a default parameter that
        specifies the name of the database file. If no value is provided when creating an instance of
        the class, it will default to "model/database.db", defaults to model/database.db (optional)
        """
        self.db_name = db_name
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor() if self.conn else None
            
    def create_connection(self):
        """
        The function creates a connection to a SQLite database and handles any potential errors.
        :return: The `create_connection` method is returning a connection object `conn` if the
        connection to the SQLite database is successfully established. If there is an error during the
        connection attempt, it will display an error message using `messagebox.showerror` and return
        `None`.
        """
        try:
            conn = sqlite3.connect(self.db_name)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados:\n {e}")
            return None    
            
    def create_table(self):
        """
        The `create_table` function in Python creates two tables, `funcionarios` and `banco_horas`, with
        specified columns and constraints, and handles potential errors during the table creation
        process.
        """
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
                    entrada_1 TEXT NOT NULL,
                    saida_1 TEXT NOT NULL,
                    entrada_2 TEXT NOT NULL,
                    saida_2 TEXT NOT NULL,
                    entrada_3 TEXT NOT NULL,
                    saida_3 TEXT NOT NULL,
                    total TEXT NOT NULL,
                    carga_dia TEXT NOT NULL,
                    saldo_dia TEXT NOT NULL,
                    presenca TEXT NOT NULL,
                    FOREIGN KEY (funcionario_id) REFERENCES funcionarios(id) ON DELETE CASCADE
                )                    
                """)
                
                self.conn.commit()
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao criar tabelas:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para criar tabelas.")
            
    def add_employee(self, name):
        """
        The `add_employee` function inserts a new employee's name into a SQLite database table and
        displays success or error messages using `messagebox`.
        
        :param name: The `add_employee` method you provided is used to add an employee to a database
        table named `funcionarios`. The `name` parameter represents the name of the employee that you
        want to add to the database
        """
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
        """
        This Python function updates an employee's name in a SQLite database table based on the provided
        ID.
        
        :param id: The `id` parameter in the `update_employee` method is used to specify the unique
        identifier of the employee whose information is being updated in the database. It is typically
        an integer value that corresponds to the primary key of the employee record in the database
        table
        :param name: The `name` parameter in the `update_employee` method represents the new name that
        you want to update for the employee with the specified `id`. This parameter should be a string
        containing the updated name for the employee in the database
        """
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
        """
        This Python function deletes an employee record from a SQLite database based on the provided ID.
        
        :param id: The `delete_employee` method is a function that deletes an employee from a database
        table based on the provided `id`. The `id` parameter is the unique identifier of the employee
        that you want to delete from the database. When calling this method, you need to pass the
        specific `id` of
        """
        if self.conn:
            try:
                self.cursor.execute("""
                DELETE FROM funcionarios WHERE id = ?                    
                """, (id,))
                
                self.conn.commit()
                messagebox.showinfo("Atenção", f"Funcionário deletado com sucesso.")   
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao deletar Funcionário:\n {e}")      
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para deletar funcionário.")
            
    def verify_employee(self, name):
        """
        This function verifies if an employee with a given name exists in a database table.
        
        :param name: The `verify_employee` method you provided is a function that checks if an employee
        with a given name exists in a database table named `funcionarios`. It uses a SQL query to count
        the number of rows where the name matches the input name (case-insensitive comparison)
        :return: The `verify_employee` method is returning a boolean value. It returns `True` if an
        employee with the given name exists in the database table `funcionarios`, and `False` if no
        employee with that name is found.
        """
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
        """
        This Python function retrieves all employee IDs and names from a database table and returns them
        in ascending order by name.
        :return: The `get_all_employee` method is returning a list of tuples containing the `id` and
        `nome` (name) of employees from the `funcionarios` table in ascending order of names.
        """
        if self.conn:
            try:
                self.cursor.execute("""
                SELECT id, nome FROM funcionarios ORDER BY nome ASC
                """)
                rows = self.cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao resgatar dados de ponto:\n {e}") 
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para resgatar dados de ponto.")
                
    def add_time_entry(self, funcionario_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia, presenca):
        """
        This Python function adds a time entry record to a database table with error handling for SQLite
        operations.
        
        :param funcionario_id: The `funcionario_id` parameter is used to specify the ID of the employee
        for whom the time entry is being added. This ID is typically a unique identifier for each
        employee in the database
        :param data: The `data` parameter in the `add_time_entry` method represents the date for which
        the time entry is being added. It is a required parameter and should be in a specific format
        that your application expects, such as a string in the format 'YYYY-MM-DD'. This parameter is
        used to specify
        :param entrada_1: The parameter `entrada_1` in the `add_time_entry` method represents the time
        when an employee clocks in for work for the first time in a day. It is the entry time for the
        first shift or work period of the day
        :param saida_1: The parameter `saida_1` in the `add_time_entry` function represents the time
        when an employee leaves work for the first time during the day. It is typically the clock-out
        time for the first shift or period of work
        :param entrada_2: The parameter `entrada_2` in the `add_time_entry` function represents the
        second clock-in time for an employee. This function seems to be inserting time entry data into a
        database table for tracking work hours. The `entrada_2` parameter would typically store the time
        when the employee clocks in
        :param saida_2: The parameter `saida_2` in the `add_time_entry` function represents the time
        when the employee leaves work for the second time in a day. It is used to record the second exit
        time of the employee for that particular day
        :param entrada_3: The parameter `entrada_3` in the `add_time_entry` method appears to represent
        the third entry time for a specific employee on a given date. This function seems to be adding
        time entries for an employee's work shifts into a database table named `banco_horas` which
        likely tracks their
        :param saida_3: The parameter `saida_3` in the `add_time_entry` function represents the time
        when the employee leaves work for the third time in a day. This function seems to be adding time
        entries for an employee's work shifts, including the times they clock in and out throughout the
        day
        :param total: The `total` parameter in the `add_time_entry` method seems to represent the total
        hours worked for a specific time entry. This value is likely calculated based on the difference
        between the clock-in and clock-out times recorded in the `entrada_1`, `saida_1`, `entrada_2
        :param carga_dia: The parameter `carga_dia` in the `add_time_entry` method represents the total
        working hours scheduled for the day. It is the planned or expected number of hours that the
        employee is supposed to work on that specific day. This value is typically set by the employer
        or manager based on the
        :param saldo_dia: The parameter `saldo_dia` in the `add_time_entry` method appears to represent
        the daily balance of hours worked by an employee. This value is likely calculated based on the
        total hours worked (`total`) and the expected daily workload (`carga_dia`). The `saldo_dia`
        would
        """
        if self.conn:
            try:
                self.cursor.execute("""
                INSERT INTO banco_horas (funcionario_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia, presenca)                    
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (funcionario_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia, presenca)
                )

                self.conn.commit()
                messagebox.showinfo("Atenção", f"Ponto adicionado com sucesso.")
                return True
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao adicionar ponto:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para adicionar ponto.")

    def update_time_entry(self, entry_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia, presenca):
        """
        This Python function updates a time entry in a database table with the provided entry ID and
        time values.
        
        :param entry_id: The `entry_id` parameter in the `update_time_entry` method is used to specify
        the ID of the time entry that needs to be updated in the `banco_horas` table. This ID is used in
        the `WHERE` clause of the SQL `UPDATE` statement to identify the specific
        :param entrada_1: The `update_time_entry` method you provided seems to be updating a time entry
        in a database table named `banco_horas`. The method takes several parameters including
        `entry_id`, `entrada_1`, `saida_1`, `entrada_2`, `saida_2`, `entrada_
        :param saida_1: The `saida_1` parameter in the `update_time_entry` method represents the time
        when the person leaves work for the first time during the day. It is typically the time of the
        first clock-out or the end of the first work period for the day
        :param entrada_2: The `entrada_2` parameter in the `update_time_entry` method represents the
        time of the second entry (check-in) for a time entry record in a database table named
        `banco_horas`. This parameter is used to update the `entrada_2` field in the database table for
        :param saida_2: The parameter `saida_2` in the `update_time_entry` function appears to represent
        the time when the second exit or departure occurred. This function seems to be updating time
        entries in a database table named `banco_horas`. The `saida_2` parameter is used to update the
        time
        :param entrada_3: The parameter `entrada_3` in the `update_time_entry` method seems to represent
        the third entry time in a time tracking system. This function is updating a time entry record in
        a database table named `banco_horas` with the provided entry times (`entrada_1`, `entrada_
        :param saida_3: The parameter `saida_3` in the `update_time_entry` function likely represents
        the time when the person leaves work for the third time in a day. It is part of a time tracking
        system where multiple check-in and check-out times are recorded for a given day
        :param total: The `total` parameter in the `update_time_entry` method seems to represent the
        total hours worked for a specific time entry. This value is likely calculated based on the
        individual time entries for `entrada_1`, `saida_1`, `entrada_2`, `saida_2`, `entrada
        :param carga_dia: The parameter `carga_dia` in the `update_time_entry` function seems to
        represent the "daily workload" or "workload for the day" in Portuguese. It is likely a value
        that indicates the total number of hours an employee is expected to work on that particular day
        :param saldo_dia: The parameter `saldo_dia` in the `update_time_entry` method seems to represent
        the "daily balance" in Portuguese. It is likely used to store the calculated balance for the day
        after processing the time entries. This balance could be the difference between the total hours
        worked and the expected hours for
        """
        if self.conn:
            try:
                self.cursor.execute("""
                UPDATE banco_horas
                SET data = ?, entrada_1 = ?, saida_1 = ?, entrada_2 = ?, saida_2 = ?, entrada_3 = ?, saida_3 = ?, total = ?, carga_dia = ?, saldo_dia = ?, presenca = ?
                WHERE id = ?
                """, (data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3, total, carga_dia, saldo_dia, presenca, entry_id))
                
                self.conn.commit()
                messagebox.showinfo("Atenção", f"Ponto atualizado com sucesso.")
                return True
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao atualizar ponto:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para atualizar ponto.")
            
    def delete_time_entry(self, entry_id):
        """
        This Python function deletes a time entry from a database table based on the provided entry ID.
        
        :param entry_id: The `entry_id` parameter in the `delete_time_entry` method is used to specify
        the unique identifier of the time entry that needs to be deleted from the database table
        `banco_horas`. This identifier is typically used to locate and delete the specific record
        corresponding to the time entry in the database
        """
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
            
    def get_all_entry(self, employee_id, data_initial = None, data_end=None):
        if self.conn:
            try:
                if data_initial and data_end:
                    query = """
                    SELECT * FROM banco_horas
                    WHERE funcionario_id = ?
                    AND data BETWEEN ? AND ?
                    """
                    params = (employee_id, data_initial, data_end)
                    
                elif data_initial:
                    query = """
                    SELECT * FROM banco_horas
                    WHERE funcionario_id = ?
                    AND data = ?
                    """
                    params = (employee_id, data_initial)
                    
                else:
                    query = """
                    SELECT * FROM banco_horas
                    WHERE funcionario_id = ?
                    """
                    params = (employee_id,)
                    
                if not data_initial:
                    query += "ORDER BY data DESC LIMIT 10"
                else:
                    query += "ORDER BY data DESC"
                self.cursor.execute(query, params)    
                rows = self.cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao listar pontos:\n {e}")
            except ValueError as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para listar pontos.")
    
    def get_point_tree(self, point_id, employee_id):
        if self.conn:
            try:
                self.cursor.execute("""
                SELECT * FROM banco_horas WHERE id = ? AND funcionario_id = ?
                """, (point_id, employee_id))
                
                rows = self.cursor.fetchall()
                return rows
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao regatar ponto:\n {e}")
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para resgatar ponto.")
                        
    def verify_entry_date(self, funcionario_id, data):
        if self.conn:
            try:
                self.cursor.execute("""
                SELECT COUNT(1) FROM banco_horas WHERE funcionario_id = ? AND data = ?
                """, (funcionario_id, data))
                result = self.cursor.fetchone()
                if result[0]>0:
                    return True
                else:
                    return False
            except sqlite3.Error as e:
                messagebox.showerror("Erro", f"Erro ao listar entrada de ponto:\n {e}") 
        else:
            messagebox.showerror("Erro", f"Nenhuma conexão ativa para listar entrada de ponto.") 
            
    def close_connection(self):
        """
        The `close_connection` function closes the connection if it exists, otherwise it shows an error
        message.
        """
        if self.conn:
            self.conn.close()
        else:
            messagebox.showerror("Erro", "Erro nenhuma conexão para fechar.")
            
if __name__ == "__main__":
    db = DbAccess()
    print(db.get_all_entry(1))
    
    
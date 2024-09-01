from model.dbaccess import DbAccess
from tkinter import messagebox
import json

class Manager:
    def __init__(self) -> None:
        self.db = DbAccess()
        
    def handle_add_employee(self, name):
        """
        The function `handle_add_employee` checks if a given employee name is valid and adds it to the
        database if it does not already exist.
        
        :param name: The `handle_add_employee` method takes in two parameters: `self` and `name`. The
        `name` parameter represents the name of the employee that is being added to the database. The
        method first checks if a name is provided, then verifies if the employee already exists in the
        database using the
        """
        if name:
            if not self.db.verify_employee(name):
                self.db.add_employee(name)
            else:
                messagebox.showerror("Erro", "Funcionário ja existe no banco de dados.")
        else:
            messagebox.showerror("Erro", "Insira um nome de funcionário para adicionar.")
            
    def handle_update_employee(self, id, name, new_name):
        """
        This function updates an employee's name in a database if the new name is different from the
        current name, otherwise it displays an error message.
        
        :param id: The `id` parameter in the `handle_update_employee` function likely represents the
        unique identifier of the employee whose information is being updated. This identifier is used to
        locate the specific employee record in the database that needs to be updated with the new name
        :param name: The `name` parameter in the `handle_update_employee` function represents the
        current name of the employee with the specified `id`
        :param new_name: The `new_name` parameter in the `handle_update_employee` function represents
        the updated name that you want to assign to the employee with the specified `id`. If the
        `new_name` is different from the current name of the employee, the function will update the
        employee's name in the database
        """
        if name != new_name:
            self.db.update_employee(id, new_name)
        else:
            messagebox.showerror("Erro", f"Não há diferenças entre o nome atual e o novo:\nNome atual: {name}\nNovo nome: {new_name}")
        
    def handle_delete_employee(self, id):
        """
        This function deletes an employee from the database based on the provided ID.
        
        :param id: The `id` parameter in the `handle_delete_employee` function is the unique identifier
        of the employee that you want to delete from the database. This identifier is used to locate and
        remove the specific employee record from the database
        """
        self.db.delete_employee(id)
        
    def get_employee(self):
        """
        This function retrieves all employees from a database.
        :return: The `get_employee` method is returning a list of all employees retrieved from the
        database using the `get_all_employee` method.
        """
        employees = self.db.get_all_employee()
        return employees
    
    def handle_add_point(self, funcionario_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3):
        dados = [funcionario_id, data, entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3]
        check = True
        for i in dados:
            if not i:
                check = False
        if check:
            entrys_time = [entrada_1, saida_1, entrada_2, saida_2, entrada_3, saida_3]
            entrys_minutes = []
            for i in entrys_time:
                i = self.time_to_minute(i)
                entrys_minutes.append(i)
            for i in range(0, len(entrys_minutes), 2):
                primeiro = entrys_minutes[i]
                segundo = entrys_minutes[i+1]
                if primeiro > segundo:
                    messagebox.showerror("Erro", "Revise as entrada:\nValor da entrada maior que valor da saida.")
                    return
            if not self.db.verify_entry_date(funcionario_id, data):
                self.db.add_time_entry(funcionario_id, data, entrys_minutes[0], entrys_minutes[1], entrys_minutes[2],
                                    entrys_minutes[3], entrys_minutes[4], entrys_minutes[5], 
                                    self.total_add_point(entrys_minutes), self.load_config_workload(),
                                    self.total_add_point(entrys_minutes) - self.load_config_workload())  
            else:
                messagebox.showerror("Erro", f"O funcionário ID: {funcionario_id}\nJá tem ponto adicionado com a data: {data}")            
        else:
             messagebox.showerror("Erro", "Selecione um funcionário e preencha todos os campos.")
             return
    
    def get_point_employee(self, employee_id):
        """
        This function retrieves specific data points for a given employee from a database.
        
        :param employee_id: The `get_point_employee` method takes an `employee_id` as a parameter. This
        method retrieves specific entries from a database for the given `employee_id` and returns a list
        of tuples containing selected values from those entries
        :return: The `get_point_employee` method returns a list of tuples containing specific data
        points for a given employee. The data points are extracted from the entries retrieved from the
        database for the specified employee ID.
        """
        indices = [0, 2, 9, 11]
        entrys = self.db.get_all_entry(employee_id)
        entrys = [tuple(tupla[i] for i in indices) for tupla in entrys]
        return entrys
    
    def time_to_minute(self, time_str):
        hour, minute = map(int, time_str.split(":"))
        return hour * 60 + minute
    
    def minutes_to_time(self, minutes):
        hours = minutes // 60
        minutes = minutes % 60
        return f"{hours:02}:{minutes:02}"
        
    def load_config_workload(self):
        self.config_file = "config.json"
        with open(self.config_file, "r") as file:
            config = json.load(file)
            self.carga_horaria = config.get("carga_horaria", "")
            self.carga_horaria = self.time_to_minute(self.carga_horaria)
            print(self.carga_horaria)
            return self.carga_horaria
        
    def total_add_point(self, entrys):
        total = 0
        for i in range(0, len(entrys), 2):
            primeiro = entrys[i]
            segundo = entrys[i+1]
            total = total + (segundo - primeiro)
        return int(total)
            
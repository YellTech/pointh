from dbaccess import DbAccess
from tkinter import messagebox
import json

# The `Manager` class in Python contains methods for managing employees and time entries in a
# database, handling operations such as adding, updating, deleting employees, and processing time
# entries.
class Manager:
    def __init__(self) -> None:
        """
        The above function is a Python constructor that initializes an instance variable `db` with an
        instance of `DbAccess`.
        """
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
            name = name.upper()
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
        new_name = new_name.upper()
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
    
    def handle_add_point(self, entrys_data, flag_presence):
        """
        The function `handle_add_point` checks and processes time entries for a specific employee,
        displaying errors for invalid entries.
        
        :param entrys_data: The `handle_add_point` function you provided seems to handle adding time
        entries for employees. The `entrys_data` parameter likely contains information about the
        employee and their time entry details. Based on the code snippet, `entrys_data` seems to be a
        list containing the following information in order:
        :return: The function `handle_add_point` returns either an error message displayed in a
        messagebox or it returns nothing (None) if the conditions are not met.
        """
        check = True
        for i in entrys_data:
            if not i:
                check = False
        if check:
            entrys_time = [entrys_data[2], entrys_data[3], entrys_data[4], entrys_data[5], entrys_data[6], entrys_data[7]]
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
            if not self.db.verify_entry_date(entrys_data[0], self.convert_to_sql_date(entrys_data[1])):
                result = self.db.add_time_entry(entrys_data[0], self.convert_to_sql_date(entrys_data[1]), entrys_time[0], entrys_time[1], entrys_time[2],
                                                entrys_time[3], entrys_time[4], entrys_time[5], 
                                                self.minutes_to_time(self.total_add_point(entrys_minutes)),
                                                self.minutes_to_time(self.load_config_workload()),
                                                (self.minutes_to_time(self.total_add_point(entrys_minutes) - self.load_config_workload())) if not flag_presence
                                                else f"-{self.minutes_to_time(self.load_config_workload())}" if flag_presence == 1
                                                else f"{self.minutes_to_time(self.load_config_workload())}" if flag_presence == 2
                                                else f"{self.minutes_to_time(self.load_config_workload())}" if flag_presence == 3
                                                else "ERRO"
                                                , entrys_data[8]) 
                return result 
            else:
                messagebox.showerror("Erro", f"O funcionário ID: {entrys_data[0]}\nJá tem ponto adicionado com a data: {entrys_data[1]}")            
        else:
            if entrys_data[0] == 0:
                messagebox.showerror("Erro", "Selecione um funcionário antes de adicionar o ponto.")
                return
            else:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return
    
    def handle_update_point(self, entrys_data_update, flag_presence):
        check = True
        for i in entrys_data_update:
            if not i:
                check = False
        if check:
            entrys_time = [entrys_data_update[2], entrys_data_update[3], entrys_data_update[4], entrys_data_update[5], entrys_data_update[6], entrys_data_update[7]]
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
                
            result = self.db.update_time_entry(entrys_data_update[0], self.convert_to_sql_date(entrys_data_update[1]), entrys_time[0], entrys_time[1], entrys_time[2],
                                            entrys_time[3], entrys_time[4], entrys_time[5], 
                                            self.minutes_to_time(self.total_add_point(entrys_minutes)),
                                            self.minutes_to_time(self.load_config_workload()),
                                            self.minutes_to_time(self.total_add_point(entrys_minutes) - self.load_config_workload()) if not flag_presence
                                            else f"-{self.minutes_to_time(self.load_config_workload())}" if flag_presence == 1
                                            else f"{self.minutes_to_time(self.load_config_workload())}" if flag_presence == 2
                                            else f"{self.minutes_to_time(self.load_config_workload())}" if flag_presence == 3
                                            else "ERRO" ,
                                            entrys_data_update[8]) 
            return result           
        else:
            messagebox.showerror("Erro", "Preencha todos os campos.")
            return
    
    def handle_delete_point(self, id):
        self.db.delete_time_entry(id)
    
    def get_point_employee(self, employee_id, data_initial=None, data_end = None):
        """
        This function retrieves specific data points for a given employee from a database.
        
        :param employee_id: The `get_point_employee` method takes an `employee_id` as a parameter. This
        method retrieves specific entries from a database for the given `employee_id` and returns a list
        of tuples containing selected values from those entries
        :return: The `get_point_employee` method returns a list of tuples containing specific data
        points for a given employee. The data points are extracted from the entries retrieved from the
        database for the specified employee ID.
        """
        entrys = self.db.get_all_entry(employee_id, self.convert_to_sql_date(data_initial), self.convert_to_sql_date(data_end))
        if not entrys:
            if employee_id == 0:
                messagebox.showerror("Erro", "Selecione um funcionário.")
                return []
            if data_initial:
                messagebox.showerror("Erro", "Nenhum registro encontrado para o intervalo de datas especificado.")
                return []
            else:
                return []
        entrys = self.convert_dates_in_tuples(entrys, [2])
        return entrys
 
    def handle_get_point_tree(self, point_id, employee_id):
        point = self.db.get_point_tree(point_id, employee_id)
        point = self.convert_dates_in_tuples(point, [2])
        return point[0]
    
    def time_to_minute(self, time_str):
        """
        The function `time_to_minute` converts a time string in the format "HH:MM" to the total number
        of minutes.
        
        :param time_str: The `time_str` parameter is a string representing a time in the format "HH:MM"
        where HH is the hour and MM is the minute
        :return: The function `time_to_minute` is returning the total number of minutes represented by
        the input `time_str`. It calculates this by converting the hours to minutes (hour * 60) and
        adding the minutes to it.
        """
        sign = -1 if time_str.startswith("-") else 1  # Check if the time is negative
        time_str = time_str.lstrip("-")  # Remove the negative sign for processing
        hour, minute = map(int, time_str.split(":"))
        return sign * ((hour * 60) + minute)
    
    def convert_to_sql_date(self, date_str):
        # Converte uma data de 'dd-mm-YYYY' para 'YYYY-MM-DD'
        if date_str:
            day, month, year = date_str.split('-')
            return f"{year}-{month}-{day}"
        else:
            return None
        
    def convert_to_br_date(self, date_str):
        # Converte uma data de 'YYYY-MM-DD' para 'DD-MM-YYYY'
        year, month, day = date_str.split('-')
        return f"{day}-{month}-{year}"
    
    def convert_dates_in_tuples(self, data_list, date_indices = [1]):
        converted_list = []
        for item in data_list:
            converted_item = list(item) 
            for index in date_indices:
                if isinstance(converted_item[index], str):
                    converted_item[index] = self.convert_to_br_date(converted_item[index])
            
            converted_list.append(tuple(converted_item))
        
        return converted_list
    
    def minutes_to_time(self, minutes):
        """
        The function `minutes_to_time` converts total minutes into hours and minutes in a formatted
        string.
        
        :param minutes: The `minutes_to_time` function takes in a number of minutes as input and
        converts it into hours and minutes format
        :return: The function `minutes_to_time` takes a number of minutes as input and converts it into
        hours and minutes format. It then returns a string in the format "HH:MM" where HH represents the
        hours and MM represents the minutes.
        """
        sign = "-" if minutes < 0 else ""
        
        minutes = abs(minutes)
        
        hours = minutes // 60
        minutes = minutes % 60
        return f"{sign}{hours:02}:{minutes:02}"
        
    def load_config_workload(self):
        """
        This Python function loads a configuration file, extracts the "carga_horaria" value, converts it
        to minutes using a helper function, and returns the result.
        :return: The method `load_config_workload` is returning the value of `self.carga_horaria`, which
        is the workload converted to minutes using the `time_to_minute` method.
        """
        self.config_file = "config.json"
        with open(self.config_file, "r") as file:
            config = json.load(file)
            self.carga_horaria = config.get("carga_horaria", "")
            self.carga_horaria = self.time_to_minute(self.carga_horaria)
            return self.carga_horaria
        
    def total_add_point(self, entrys):
        """
        This Python function calculates the total sum of differences between pairs of elements in a
        list.
        
        :param entrys: The `total_add_point` function takes a list of numbers as input in the `entrys`
        parameter. The function then calculates the total sum of the differences between every pair of
        consecutive numbers in the list
        :return: The `total_add_point` function is returning the total sum of the differences between
        every pair of consecutive elements in the `entrys` list. The function calculates this total by
        iterating through the list and adding the difference between the second element and the first
        element of each pair. The final result is then returned as an integer.
        """
        total = 0
        for i in range(0, len(entrys), 2):
            primeiro = entrys[i]
            segundo = entrys[i+1]
            total = total + (segundo - primeiro)
        return int(total)

    def calc_hours_trabalhadas(self, data):
        horas_normais = 0
        horas_eperadas = 0
        for tupla in data:
            horas_eperadas += self.time_to_minute("08:48")
            if tupla[12] == "NORMAL":
                minutos = self.time_to_minute(tupla[9])
                horas_normais += minutos
        return self.minutes_to_time(horas_normais), self.minutes_to_time(horas_eperadas)
    
    def calc_hours_atestado(self, data):
        horas_atestado = 0
        quantidade_atestados = 0
        for tupla in data:
            if tupla[12] == "ATESTADO":
                minutos = self.time_to_minute(tupla[10])
                quantidade_atestados += 1
                horas_atestado += minutos
        return self.minutes_to_time(horas_atestado), quantidade_atestados

    def calc_hour_feriado(self, data):
        horas_feriado = 0
        quantidade_feriados = 0
        for tupla in data:
            if tupla[12] == "FERIADO":
                minutos = self.time_to_minute(tupla[10])
                quantidade_feriados += 1
                horas_feriado += minutos
        return self.minutes_to_time(horas_feriado), quantidade_feriados

    def calc_hours_faltou(self, data):
        horas_faltou = 0
        quantidade_faltas = 0
        for tupla in data:
            if tupla[12] == "FALTOU":
                minutos = self.time_to_minute(tupla[10])
                quantidade_faltas += 1
                horas_faltou += minutos
        return f"-{self.minutes_to_time(horas_faltou)}", quantidade_faltas
    
    def calc_hours_extra(self, data):
        horas_extras = 0
        for tupla in data:
            if tupla[12] == "NORMAL":
                minutos = self.time_to_minute(tupla[11])
                if minutos > 0:
                    horas_extras += minutos
        return self.minutes_to_time(horas_extras)
    
    def calc_hours_negativas(self, data):
        horas_negativas = 0
        for tupla in data:
            if tupla[12] == "NORMAL":
                minutos = self.time_to_minute(tupla[11])
                if minutos < 0:
                    horas_negativas += minutos  
        return self.minutes_to_time(horas_negativas)
   
    def close_connection_manager(self):
        self.db.close_connection()         
from model.dbaccess import DbAccess
from tkinter import messagebox

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
    
    def get_entry(self):
        """
        This function retrieves specific entries from a database based on given indices.
        :return: A list of tuples containing values from specific indices (0, 2, 9, 11) of each entry
        retrieved from the database.
        """
        indices = [0, 2, 9, 11]
        entrys = self.db.get_all_entry()
        entrys = [tuple(tupla[i] for i in indices) for tupla in entrys]
        return entrys
    
if __name__ == "__main__":
    mg = Manager()

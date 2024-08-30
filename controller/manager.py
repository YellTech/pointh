from model.dbaccess import DbAccess
from tkinter import messagebox

class Manager:
    def __init__(self) -> None:
        self.db = DbAccess()
        
    def handle_add_employee(self, name):
        if name:
            if not self.db.verify_employee(name):
                self.db.add_employee(name)
            else:
                messagebox.showerror("Erro", "Funcionário ja existe no banco de dados.")
        else:
            messagebox.showerror("Erro", "Insira um nome de funcionário para adicionar.")
            
    def handle_update_employee(self, id, name, new_name):
        if name != new_name:
            self.db.update_employee(id, new_name)
        else:
            messagebox.showerror("Erro", f"Não há diferenças entre o nome atual e o novo:\nNome atual: {name}\nNovo nome: {new_name}")
        
    def handle_delete_employee(self, id):
        pass
        
    def get_employee(self):
        employees = self.db.get_all_employee()
        return employees
    
    def get_entry(self):
        indices = [0, 2, 9, 11]
        entrys = self.db.get_all_entry()
        entrys = [tuple(tupla[i] for i in indices) for tupla in entrys]
        return entrys
    
if __name__ == "__main__":
    mg = Manager()

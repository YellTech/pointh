from model.model import DbAccess
from tkinter import messagebox

class Manager:
    def __init__(self) -> None:
        self.db = DbAccess()
        
    def handle_add_employee(self, name):
        self.db.add_employee(name)
        
    def get_employee(self):
        employees = self.db.get_all_employee()
        return employees
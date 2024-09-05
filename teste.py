import tkinter as tk
from tkinter import Toplevel, StringVar

class DropdownEntry(tk.Entry):
    def __init__(self, master=None, values=[], **kwargs):
        super().__init__(master, **kwargs)
        self.values = values
        self.var = StringVar()
        self.config(textvariable=self.var)
        self.bind("<Button-1>", self.show_dropdown)
        self.bind("<FocusOut>", self.on_focus_out)
        
        self.dropdown = None
    
    def show_dropdown(self, event):
        if self.dropdown is not None:
            self.dropdown.destroy()
        
        self.dropdown = Toplevel(self)
        self.dropdown.wm_overrideredirect(True)
        
        listbox = tk.Listbox(self.dropdown)
        listbox.pack()
        
        for value in self.values:
            listbox.insert(tk.END, value)
        
        listbox.bind("<ButtonRelease-1>", self.select_value)
        
        # Position the dropdown
        x, y, _, _ = self.bbox("insert")
        x += self.winfo_rootx()
        y += self.winfo_rooty() + self.winfo_height()
        self.dropdown.wm_geometry(f"+{x}+{y}")

    def select_value(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            value = widget.get(selection[0])
            self.var.set(value)
        self.dropdown.destroy()

    def on_focus_out(self, event):
        if self.dropdown:
            self.dropdown.destroy()

def main():
    root = tk.Tk()
    root.title("Custom Dropdown Entry")

    values = ["NORMAL", "FALTOU", "ATESTADO"]
    entry = DropdownEntry(root, values=values, width=20)
    entry.pack(pady=10, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()

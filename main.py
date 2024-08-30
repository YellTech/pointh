from view.view import View
from model.model import DbAccess

def run():
    db_init = DbAccess()
    db_init.create_table()
    app = View()
    app.mainloop()

run()
from view import View
from dbaccess import DbAccess

def run():
    db_init = DbAccess()
    db_init.create_table()
    app = View()
    app.mainloop()

if __name__ == "__main__":
    run()
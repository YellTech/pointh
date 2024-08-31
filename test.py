import tkinter as tk
 
class Hours(tk.Tk):
 
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
 
        tk.Label(self, text="Clock Page").grid(row=0, column=0, columnspan=2)
 
        vcmd = (self.register(self.onValidate), '%d', '%s', '%S')
 
        tk.Label(self, text="12h format").grid(row=1, column=0)
        # Entry to insert a 12 hour format
        entry1 = tk.Entry(self, validate="key", validatecommand=vcmd, width=10, justify=tk.CENTER)
        entry1.bind("<KeyRelease>", self.hour_12)
        entry1.grid(row=1, column=1)
 
        tk.Label(self, text="24h format").grid(row=2, column=0)
        # Entry to insert a 24 hour format
        entry2 = tk.Entry(self, validate="key", validatecommand=vcmd, width=10, justify=tk.CENTER)
        entry2.bind("<KeyRelease>", self.hour_24)
        entry2.grid(row=2, column=1)
 
    def onValidate(self, d, s, S):
        # if it's deleting return True
        if d == "0":
            return True
        # Allow only digit, ":" and check the length of the string
        if ((S == ":" and len(s) != 2) or (not S.isdigit() and
                S != ":") or (len(s) == 3 and int(S) > 5) or len(s) > 4):
            self.bell()
            return False
         
        return True
 
    def hour_24(self, event):
        """
        Check and build the correct format hour: hh:mm in 24 format
        it keep in mind the 0x, 1x and 2x hours and the max minutes can be 59
        """
 
        # get the object that triggered the event
        s = event.widget
        # if delete a char do return ok or delete the char ":" and the previous number
        if len(s.get()) == 2 and event.keysym=="BackSpace":
            s.delete(len(s.get())-1, tk.END)
        if event.keysym=="BackSpace":
            return
         
        # check the hour format and add : between hours and minutes
        if len(s.get()) == 1 and int(s.get()) > 2:
            s.insert(0, "0")
            s.insert("end", ":")
        elif len(s.get()) == 2 and int(s.get()) < 24:
            s.insert(2, ":")
        elif len(s.get()) >= 2 and s.get()[2:3] != ":":
            self.bell()
            s.delete(1, tk.END)
        
    def hour_12(self, event):
        """
        Check and build the correct format hour: hh:mm in am, pm mode
        it keep in mind the 0x, 1x hours and the max minutes can be 59
        """
 
        # get the object that triggered the event
        s = event.widget
 
        # if delete a char do return ok or delete the char ":" and the previous number
        if len(s.get()) == 2 and event.keysym=="BackSpace":
            s.delete(len(s.get())-1, tk.END)
        if event.keysym=="BackSpace":
            return
         
        # check the hour format and add : between hours and minutes
        if len(s.get()) == 1 and int(s.get()) > 1:
            s.insert(0, "0")
            s.insert("end", ":")
        elif len(s.get()) == 2 and int(s.get()) <= 12:
            s.insert(2, ":")
        elif len(s.get()) >= 2 and s.get()[2:3] != ":":
            self.bell()
            s.delete(1, tk.END)
 
       
def main():
    app = Hours()
    app.mainloop()
 
if __name__ == '__main__':
    main()
else:
    print('I would like to be the main module.')
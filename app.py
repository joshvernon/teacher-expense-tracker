import sys
import tkinter as tk

from data_access import DataAccess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sum = DataAccess().sum_expenses()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.add_new_expense = tk.Button(self)
        self.add_new_expense['text'] = 'Add new expense'
        self.add_new_expense.pack(side='top')

        self.expenses_label = tk.Label(self)
        self.expenses_label['text'] = 'Total expenses: ${0:0.2f}'.format(self.sum)
        self.expenses_label.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=root.destroy)
        self.quit.pack(side="bottom")

root = tk.Tk()
app = Application(master=root)
app.master.title('Teacher Expense Tracker')
app.mainloop()

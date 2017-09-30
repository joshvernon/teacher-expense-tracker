import sys
import tkinter as tk

from data_access import DataAccess

def _get_sum():
    sum_data_access = DataAccess()
    sum_result = sum_data_access.sum_expenses()
    sum_data_access.close()
    print(sum_result)
    return sum_result

def _format_sum_string(sum_value):
    return 'Total expenses: ${0:0.2f}'.format(sum_value)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.sum = _get_sum()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.add_new_expense = tk.Button(self)
        self.add_new_expense['text'] = 'Add new expense'
        self.add_new_expense.pack(side='top')

        self.expenses_label = tk.Label(self)
        self.label_text = tk.StringVar()
        self.label_text.set(_format_sum_string(self.sum))
        self.expenses_label['textvariable'] = self.label_text
        self.expenses_label.pack()

        self.quit = tk.Button(self, text="Quit", command=root.destroy)
        self.quit.pack(side="bottom")

root = tk.Tk()
app = Application(master=root)
app.master.title('Teacher Expense Tracker')
app.mainloop()

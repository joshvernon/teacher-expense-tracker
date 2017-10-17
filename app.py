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
        self.add_new_expense = tk.Button(
            self, text='Add new expense', command=self.create_add_window
        )
        self.add_new_expense.pack(side='top')

        self.expenses_label = tk.Label(self)
        self.label_text = tk.StringVar()
        self.label_text.set(_format_sum_string(self.sum))
        self.expenses_label['textvariable'] = self.label_text
        self.expenses_label.pack()

        self.quit = tk.Button(self, text="Quit", command=root.destroy)
        self.quit.pack(side="bottom")

    def create_add_window(self):
        self.add_window = tk.Toplevel(root)
        self.add_window.title('Add New Expense')
        self.amount_label = tk.Label(self.add_window, text='Expense Amount: $')
        self.amount_label.grid(column=1, row=1)
        self.amount_entry = tk.Entry(self.add_window)
        self.amount_entry.grid(column=2, row=1)

root = tk.Tk()
app = Application(master=root)
app.master.title('Teacher Expense Tracker')
app.mainloop()

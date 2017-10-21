import os
import tkinter as tk
from tkinter import filedialog

from data_access import DataAccess

def _get_sum():
    sum_data_access = DataAccess()
    sum_result = sum_data_access.sum_expenses()
    sum_data_access.close()
    return sum_result

def _format_sum_string(sum_value):
    return 'Total expenses: ${0:0.2f}'.format(sum_value)

class Application(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master, padx=75, pady=50)
        self.sum = _get_sum()
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.add_new_expense = tk.Button(
            self,
            text='Add new expense',
            command=self.create_add_window,
            pady=15,
        )
        self.add_new_expense.pack(side='top')

        self.expenses_label = tk.Label(self)
        self.label_text = tk.StringVar()
        self.label_text.set(_format_sum_string(self.sum))
        self.expenses_label['textvariable'] = self.label_text
        self.expenses_label.pack

    def create_add_window(self):
        self.add_window = tk.Toplevel(root, padx=35, pady=40)
        self.add_window.title('Add New Expense')

        self.description_label = tk.Label(self.add_window, text='Description: ')
        self.description_label.grid(column=1, row=1)
        self.description_entry = tk.Entry(self.add_window)
        self.description_entry.grid(column=2, row=1)

        self.amount_label = tk.Label(self.add_window, text='Amount: $')
        self.amount_label.grid(column=1, row=2)
        self.amount_entry = tk.Entry(self.add_window)
        self.amount_entry.grid(column=2, row=2)

        self.date_label = tk.Label(self.add_window, text='Date: ')
        self.date_label.grid(column=1, row=3)
        self.date_entry = tk.Entry(self.add_window)
        self.date_entry.grid(column=2, row=3)

        self.receipt_label = tk.Label(self.add_window, text='Receipt: ')
        self.receipt_label.grid(column=1, row=4)
        self.receipt_button = tk.Button(self.add_window, text='Choose file', command=self.launch_file_dialog)
        self.receipt_button.grid(column=2, row=4)

    def launch_file_dialog(self):
        filedialog.askopenfilename(
            initialdir=os.path.expanduser('~/Documents'),
            title="Select file",
            filetypes=(("PDF files","*.pdf"),("all files","*.*"))
        )

root = tk.Tk()
app = Application(master=root)
app.master.title('Teacher Expense Tracker')
app.mainloop()

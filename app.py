import os.path
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
        self.receipt = 'dummy_path'
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        add_new_expense = tk.Button(
            self,
            text='Add new expense',
            command=self.create_add_window,
            pady=15,
        )
        add_new_expense.pack(side='top')

        expenses_label = tk.Label(self)
        self.label_text = tk.StringVar()
        self.label_text.set(_format_sum_string(self.sum))
        expenses_label['textvariable'] = self.label_text
        expenses_label.pack()

    def create_add_window(self):
        add_window = tk.Toplevel(root, padx=35, pady=40)
        add_window.title('Add New Expense')

        description_label = tk.Label(add_window, text='Description: ')
        description_label.grid(column=1, row=1)
        description_entry = tk.Entry(add_window)
        description_entry.grid(column=2, row=1)

        amount_label = tk.Label(add_window, text='Amount: $')
        amount_label.grid(column=1, row=2)
        amount_entry = tk.Entry(add_window)
        amount_entry.grid(column=2, row=2)

        date_label = tk.Label(add_window, text='Date: ')
        date_label.grid(column=1, row=3)
        date_entry = tk.Entry(add_window)
        date_entry.grid(column=2, row=3)

        receipt_label = tk.Label(add_window, text='Receipt: ')
        receipt_label.grid(column=1, row=4)
        receipt_button = tk.Button(
            add_window,
            text='Choose file',
            command=self.launch_file_dialog,
        )
        receipt_button.grid(column=2, row=4)

        add_button = tk.Button(add_window, text='Add', pady=10, padx=25)
        add_button.grid(row=5, columnspan=5, pady=5)

    def launch_file_dialog(self):
        file_path = filedialog.askopenfilename(
            initialdir=os.path.expanduser('~/Documents'),
            title="Select file",
            filetypes=(("PDF files", "*.pdf"), ("all files", "*.*"))
        )
        self.receipt = os.path.basename(file_path)

root = tk.Tk()
app = Application(master=root)
app.master.title('Teacher Expense Tracker')
app.mainloop()

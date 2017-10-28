import os.path
import tkinter as tk
from tkinter import filedialog

from data_access import DataAccess

def get_sum():
    sum_data_access = DataAccess()
    sum_result = sum_data_access.sum_expenses()
    sum_data_access.close()
    return sum_result

def format_sum_string(sum_value):
    return 'Total expenses: ${0:0.2f}'.format(sum_value)

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, padx=75, pady=50)
        self.sum = get_sum()
        self.add_window = None
        self.description = ''
        self.amount = 0.0
        self.date = '1900-01-01 00:00:00'
        self.receipt = 'dummy_path'
        self.pack()
        self.create_widgets()

    def _is_float(self):
        try:
            float(self.amount.get())
            return True
        except ValueError:
            return False

    def _on_invalid_amount(self):
        self.amount.set('Not a number!')

    def create_widgets(self):
        add_new_expense = tk.Button(
            self,
            text='Add new expense',
            command=self.create_add_window,
            pady=15,
        )
        add_new_expense.pack(side='top')

        self.sum_label = tk.StringVar()
        self.sum_label.set(format_sum_string(self.sum))
        expenses_label = tk.Label(self, textvariable=self.sum_label)
        expenses_label.pack()

    def create_add_window(self):
        self.add_window = tk.Toplevel(root, padx=35, pady=40)
        self.add_window.title('Add New Expense')

        self.description = tk.StringVar()
        description_label = tk.Label(self.add_window, text='Description: ')
        description_label.grid(column=1, row=1)
        description_entry = tk.Entry(
            self.add_window,
            textvariable=self.description
        )
        description_entry.grid(column=2, row=1)

        self.amount = tk.StringVar()
        amount_label = tk.Label(self.add_window, text='Amount: $')
        amount_label.grid(column=1, row=2)
        validator = self.register(self._is_float)
        invalid_amount_action = self.register(self._on_invalid_amount)
        amount_entry = tk.Entry(
            self.add_window,
            textvariable=self.amount,
            validate='focusout',
            validatecommand=validator,
            invalidcommand=invalid_amount_action
        )
        amount_entry.grid(column=2, row=2)

        self.date = tk.StringVar()
        date_label = tk.Label(self.add_window, text='Date: ')
        date_label.grid(column=1, row=3)
        date_entry = tk.Entry(self.add_window, textvariable=self.date)
        date_entry.grid(column=2, row=3)

        receipt_label = tk.Label(self.add_window, text='Receipt: ')
        receipt_label.grid(column=1, row=4)
        receipt_button = tk.Button(
            self.add_window,
            text='Choose file',
            command=self.launch_file_dialog,
        )
        receipt_button.grid(column=2, row=4)

        add_button = tk.Button(
            self.add_window,
            text='Add',
            pady=10,
            padx=25,
            command=self.insert_expense
        )
        add_button.grid(row=5, columnspan=5, pady=5)

    def launch_file_dialog(self):
        file_path = filedialog.askopenfilename(
            initialdir=os.path.expanduser('~/Documents'),
            title="Select file",
            filetypes=(("PDF files", "*.pdf"), ("all files", "*.*"))
        )
        self.receipt = os.path.basename(file_path)

    def insert_expense(self):
        insert_data_access = DataAccess()
        insert_dict = {
            'description': self.description.get(),
            'amount': self.amount.get(),
            'file_path': self.receipt,
            'date': self.date.get(),
        }
        insert_data_access.insert(**insert_dict)
        insert_data_access.close()
        self.sum += float(self.amount.get())
        self.sum_label.set(format_sum_string(self.sum))
        self.add_window.destroy()

root = tk.Tk()
app = Application(master=root)
app.master.title('Teacher Expense Tracker')
app.mainloop()

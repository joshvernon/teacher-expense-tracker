import os.path
import tkinter as tk
from tkinter import filedialog

import drive_sync
from data_access import DataAccess

# Set to True to enable uploading the expense database to Google Drive.
# This feature is experimental and requires extra third-party libraries
# and non-default security configuations.
UPLOAD_TO_GOOGLE_DRIVE = False

def get_sum():
    sum_data_access = DataAccess()
    sum_result = sum_data_access.sum_expenses()
    sum_data_access.close()
    return sum_result

def format_sum_string(sum_value):
    return 'Total expenses: ${0:0.2f}'.format(sum_value)

def close_window():
    """On window close, upload the database to Google Drive."""
    if UPLOAD_TO_GOOGLE_DRIVE:
        drive_sync.upload()
    root.destroy()

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master, padx=75, pady=50)
        self.sum = get_sum()
        self.add_window = None
        self.description = tk.StringVar()
        self.amount = tk.StringVar()
        self.date = tk.StringVar()
        self.receipt = tk.StringVar()
        self.pack()
        self.create_widgets()

    def _amount_is_float(self):
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

        self.description.set('')
        description_label = tk.Label(self.add_window, text='Description: ')
        description_label.grid(column=1, row=1)
        description_entry = tk.Entry(
            self.add_window,
            textvariable=self.description
        )
        description_entry.grid(column=2, row=1)

        self.amount.set('')
        amount_label = tk.Label(self.add_window, text='Amount: $')
        amount_label.grid(column=1, row=2)
        validator = self.register(self._amount_is_float)
        invalid_amount_action = self.register(self._on_invalid_amount)
        amount_entry = tk.Entry(
            self.add_window,
            textvariable=self.amount,
            validate='focusout',
            validatecommand=validator,
            invalidcommand=invalid_amount_action
        )
        amount_entry.grid(column=2, row=2)

        self.date.set('')
        date_label = tk.Label(self.add_window, text='Date: ')
        date_label.grid(column=1, row=3)
        date_entry = tk.Entry(self.add_window, textvariable=self.date)
        date_entry.grid(column=2, row=3)

        self.receipt.set('Choose file')
        receipt_label = tk.Label(self.add_window, text='Receipt: ')
        receipt_label.grid(column=1, row=4)
        receipt_button = tk.Button(
            self.add_window,
            command=self.launch_file_dialog,
            textvariable=self.receipt
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
        self.receipt.set(os.path.basename(file_path))

    def insert_expense(self):
        insert_data_access = DataAccess()
        insert_dict = {
            'description': self.description.get(),
            'amount': self.amount.get(),
            'file_path': self.receipt.get(),
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
app.master.protocol('WM_DELETE_WINDOW', close_window)
app.mainloop()

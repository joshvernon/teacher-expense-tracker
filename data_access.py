# data_access.py

import sqlite3

DATABASE = 'expenses.db'
TABLE_NAME = 'expenses'

class DataAccess():

    def __init__(self, database=DATABASE, table_name=TABLE_NAME):
        self.database = database
        self.table_name = table_name
        self.connection = _get_connection(database)

    def __repr__(self):
        return ("DataAccess(database:'{0}', table_name:'{1}')"
                .format(self.database, self.table_name))

    def close(self):
        self.connection.close()

    def create(self):
        create_stmt = "CREATE TABLE IF NOT EXISTS {0}(\
            description TEXT,\
            amount REAL,\
            file_path TEXT,\
            date TEXT)".format(_scrub_table_name(self.table_name))
        with self.connection as conn:
            conn.execute(create_stmt)

    def insert(self):
        print('Dummy insert.')
    
    def sum_expenses(self):
        print('Dummy sum_expenses.')

def _get_connection(database):
    return sqlite3.connect(database)

def _scrub_table_name(table_name):
    # Provides sanitization of input table names in SQL queries,
    # since SQLite doesn't allow query parameterization of table names.
    # Shamelessly stolen from here:
    # http://stackoverflow.com/questions/3247183/variable-table-name-in-sqlite
    allowed_chrs = ['_']
    return ''.join(
        chr for chr in table_name
        if (chr.isalnum()) or (chr in allowed_chrs)
    )

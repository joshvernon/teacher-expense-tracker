# data_access.py

import sqlite3

DATABASE = 'expenses.db'
TABLE_NAME = 'expenses'

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

class DataAccess():

    def __init__(self, database=DATABASE, table_name=TABLE_NAME):
        self.database = database
        self.table_name = _scrub_table_name(table_name)
        self.connection = _get_connection(database)

    def __repr__(self):
        return ("DataAccess(database:'{0}', table_name:'{1}')"
                .format(self.database, self.table_name))

    def _table_exists(self, table_name):
        select_stmt = "SELECT count(*) FROM sqlite_master\
            WHERE type = 'table' AND name = ?"
        cursor = self.connection.execute(select_stmt, (table_name,))
        result = cursor.fetchone()[0]
        return False if result == 0 else True

    def close(self):
        self.connection.close()

    def create(self):
        create_stmt = "CREATE TABLE IF NOT EXISTS {0}(\
            description TEXT,\
            amount REAL,\
            file_path TEXT,\
            date TEXT)".format(self.table_name)
        with self.connection as conn:
            conn.execute(create_stmt)

    def insert(self, **kwargs):
        if not kwargs:
            raise InvalidDataError("Can't insert an empty row")
        if not self._table_exists(self.table_name):
            self.create()
        insert_stmt = "INSERT INTO {0} VALUES(\
            :description,\
            :amount,\
            :file_path,\
            datetime(:date))".format(self.table_name)
        with self.connection as conn:
            conn.execute(insert_stmt, kwargs)
    
    def sum_expenses(self):
        if not self._table_exists(self.table_name):
            return 0
        select_stmt = "SELECT SUM(amount) FROM {0}".format(self.table_name)
        cursor = self.connection.execute(select_stmt)
        sum_result = cursor.fetchone()[0]
        cursor.close()
        return 0 if sum_result is None else sum_result

class InvalidDataError(Exception):
    pass

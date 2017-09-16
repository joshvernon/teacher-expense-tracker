# data_access.py

def sum_expenses(table_name='expenses'):
    # Sum stuff.
    print('Dummy sum')

def insert():
    print('Dummy insert')

def create():
    print('Dummy create')

def scrub_table_name(table_name):
    # Provides sanitization of input table names in SQL queries,
    # since SQLite doesn't allow query parameterization of table names.
    # Shamelessly stolen from here:
    # http://stackoverflow.com/questions/3247183/variable-table-name-in-sqlite
    allowed_chrs = ['_']
    return ''.join(
        chr for chr in table_name
        if (chr.isalnum()) or (chr in allowed_chrs)
    )

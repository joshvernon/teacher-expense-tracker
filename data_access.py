# data_access.py

def sum(table_name='expenses'):
    # Sum stuff.

def insert():
    # Insert stuff.

def create():
    # Create stuff.

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

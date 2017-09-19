import os
import sqlite3
import unittest

from data_access import DataAccess

test_db = 'test.db'

def _table_exists():
    conn = sqlite3.connect(test_db)
    c = conn.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='expenses'")
    result = c.fetchone()[0]
    c.close()
    conn.close()
    return result

class DataAccessTestCase(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(test_db):
            os.remove(test_db)

    def test_constructor_with_default_params(self):
        da = DataAccess()
        self.assertEqual(da.database, 'expenses.db')
        self.assertEqual(da.table_name, 'expenses')
        da.close()

    def test_create_when_table_does_not_exist(self):
        da = DataAccess(database=test_db)
        da.create()
        da.close()
        self.assertEqual(_table_exists(), 1)
    
    def test_create_when_table_already_exists(self):
        da = DataAccess(database=test_db)
        da.create()
        da.create()
        da.close()
        self.assertEqual(_table_exists(), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)

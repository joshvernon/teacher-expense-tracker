import os
import sqlite3
import unittest

import data_access

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
        os.remove(test_db)

    def test_create_when_table_does_not_exist(self):
        data_access.create()
        self.assertEqual(_table_exists(), 1)
    
    def test_create_when_table_already_exists(self):
        data_access.create()
        data_access.create()
        self.assertEqual(_table_exists(), 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
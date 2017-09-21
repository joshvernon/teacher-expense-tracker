import os
import sqlite3
import unittest
from datetime import datetime

from data_access import DataAccess, InvalidDataError

TEST_DB = 'test.db'

TEST_ROW_1 = {
    'description': 'description1',
    'amount': 12.75,
    'file_path': '/some/file/path',
    'date': datetime.now(),
}

TEST_ROW_2 = {
    'description': 'description2',
    'amount': 14.24,
    'file_path': '/some/other/path',
    'date': datetime.now(),
}

TEST_ROW_3 = {
    'description': 'description3',
    'amount': 5.96,
    'file_path': '/yet/another/path',
    'date': datetime.now(),
    'other_field': 'other_value'
}

def _table_exists():
    conn = sqlite3.connect(TEST_DB)
    c = conn.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='expenses'")
    result = c.fetchone()[0]
    c.close()
    conn.close()
    return result

def _get_row_count():
    conn = sqlite3.connect(TEST_DB)
    cur = conn.execute("SELECT count(rowid) from expenses")
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result

class DataAccessTestCase(unittest.TestCase):

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_constructor_with_default_params(self):
        da = DataAccess()
        self.assertEqual(da.database, 'expenses.db')
        self.assertEqual(da.table_name, 'expenses')
        da.close()

    def test_create_when_table_does_not_exist(self):
        da = DataAccess(database=TEST_DB)
        da.create()
        da.close()
        self.assertEqual(_table_exists(), 1)
    
    def test_create_when_table_already_exists(self):
        da = DataAccess(database=TEST_DB)
        da.create()
        da.create()
        da.close()
        self.assertEqual(_table_exists(), 1)
    
    def test_insert_adding_one_row(self):
        da = DataAccess(database=TEST_DB)
        da.insert(**TEST_ROW_1)
        da.close()
        self.assertEqual(_get_row_count(), 1)

    def test_insert_adding_two_rows(self):
        da = DataAccess(database=TEST_DB)
        da.insert(**TEST_ROW_1)
        da.insert(**TEST_ROW_2)
        da.close()
        self.assertEqual(_get_row_count(), 2)

    def test_insert_extra_fields(self):
        da = DataAccess(database=TEST_DB)
        da.insert(**TEST_ROW_3)
        self.assertEqual(_get_row_count(), 1)
    
    def test_insert_no_kwargs_raises_InvalidDataError(self):
        da = DataAccess(database=TEST_DB)
        self.assertRaises(InvalidDataError, da.insert)

    def test_sum_expenses_one_row(self):
        da = DataAccess(database=TEST_DB)
        da.insert(**TEST_ROW_1)
        sum_result = da.sum_expenses()
        da.close()
        self.assertEqual(sum_result, 12.75)

    def test_sum_expeneses_two_rows(self):
        da = DataAccess(database=TEST_DB)
        da.insert(**TEST_ROW_1)
        da.insert(**TEST_ROW_2)
        sum_result = da.sum_expenses()
        da.close()
        self.assertAlmostEqual(sum_result, 26.99)

    def test_sum_expenses_no_rows_is_None(self):
        da = DataAccess(database=TEST_DB)
        da.create()
        sum_result = da.sum_expenses()
        da.close()
        self.assertIsNone(sum_result)

    def test_sum_expenses_missing_table_raises_OperationalError(self):
        da = DataAccess(database=TEST_DB)
        self.assertRaises(sqlite3.OperationalError, da.sum_expenses)
        da.close()

if __name__ == '__main__':
    unittest.main(verbosity=2)

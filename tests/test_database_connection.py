import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import time

from data_loader import connect_to_database

class TestDatabaseConnection(unittest.TestCase):
    
    @patch('sqlite3.connect')
    @patch('time.sleep', return_value=None)
    def test_successful_connection_first_attempt(self, mock_sleep, mock_connect):
        mock_connect.return_value = MagicMock(spec=sqlite3.Connection)  # Simulates a successful connection
        conn = connect_to_database("test.db")
        self.assertIsNotNone(conn)
        self.assertEqual(mock_connect.call_count, 1)
        mock_sleep.assert_not_called()

    
    @patch('sqlite3.connect')
    @patch('time.sleep', return_value=None)
    def test_successful_connection_after_retries(self, mock_sleep, mock_connect):
        # Fail on first two attempts, succeed on third
        mock_connect.side_effect = [sqlite3.Error("Mock failure"), sqlite3.Error("Mock failure"), MagicMock(spec=sqlite3.Connection)] # simulates 2 exceptions, and then a successful connection
        conn = connect_to_database("test.db")
        self.assertIsNotNone(conn)
        self.assertEqual(mock_connect.call_count, 3)    # call_count, ist ein Attribut des Mock-Objekts, das die Anzahl der Aufrufe der gemockten Funktion enthält
        self.assertEqual(mock_sleep.call_count, 2)

    @patch('sqlite3.connect')
    @patch('time.sleep', return_value=None)
    def test_all_retries_failed(self, mock_sleep, mock_connect):
        mock_connect.side_effect = sqlite3.Error("Mock failure")
        conn = connect_to_database("test.db")
        self.assertIsNone(conn)
        self.assertEqual(mock_connect.call_count, 6)
        self.assertEqual(mock_sleep.call_count, 4)

if __name__ == '__main__':
    unittest.main()

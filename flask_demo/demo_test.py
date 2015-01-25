import unittest
import md5

import demo

class TestDB(unittest.TestCase):
    def setUp(self):
        self.db_connection = demo.GetDatabaseConnection()

    def testTableCreation(self):
        cur = self.db_connection.cursor()
        cur.execute('SELECT * FROM sqlite_master WHERE type=?', ('table',))
        rows = cur.fetchall()
        self.assertEqual(1, len(rows), "Should contain one table")
        cur.execute('SELECT * FROM sqlite_master WHERE type=?', ('index',))
        rows = cur.fetchall()
        self.assertEqual(2, len(rows), "Should contain two indexes")

    def testDefaultUser(self):
        cur = self.db_connection.cursor()
        cur.execute('SELECT * FROM users')
        rows = cur.fetchall()
        self.assertEquals(1, len(rows), "Should contain only one user")
        self.assertEquals(('admin', md5.new('admin_password').hexdigest(), 'site_news'),
                          rows[0], "Check values for default user.")

    def testConnectionSettings(self):
        self.assertEquals(str, self.db_connection.text_factory,
                          "Ensure we recieve strings, not unicode")

if __name__ == '__main__':
    unittest.main()

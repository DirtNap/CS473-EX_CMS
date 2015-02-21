import hashlib
import unittest
from sqlalchemy.exc import IntegrityError

import users
from ..config import test
from .. import create_application, db

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.config_class = test.MemoryConfig
        self.app = create_application(config_object=self.config_class)
        with self.app.test_request_context():
            db.create_all()

    def testCreateUser(self):
        test_user_username = u'testuser'
        test_user_name = u'test user'
        test_user_email = u'test@letterbucket.net'
        test_user_password = u'test'
        with self.app.test_request_context():
            self.assertEqual([], users.User.query.all(), 'Should be no users in the db.')
            new_user = users.User(test_user_username,
                                  test_user_email,
                                  test_user_name,
                                  test_user_password)
            self.assertEqual(test_user_username, new_user.username, 'Usernames should match')
            self.assertEqual(test_user_name, new_user.name, 'Names should match')
            self.assertEqual(test_user_email, new_user.email, 'Email addresses should match')
            self.assertEqual([], users.User.query.all(), 'Should be no users in the db.')
            self.assertFalse(new_user.IsPersisted(), 'User has not yet been committed.')
            new_user.Persist()
            self.assertEqual([new_user], users.User.query.all(), 'User should be in the db.')
            self.assertTrue(new_user.IsPersisted(), 'User should be committed.')

    def testUserConstraints(self):
        test_user_username = u'testuser'
        test_user_name = u'test user'
        test_user_email = u'test@letterbucket.net'
        test_user_password = u'test'
        with self.app.test_request_context():
            self.assertEqual([], users.User.query.all(), 'Should be no users in the db.')
            new_user = users.User(test_user_username,
                                  test_user_email,
                                  test_user_name,
                                  test_user_password)
            new_user.Persist()
            self.assertEqual([new_user], users.User.query.all(), 'User should be in the db.')
            second_user = users.User(u'foo',
                                     test_user_email,
                                     test_user_name,
                                     test_user_password)
            self.assertRaises(IntegrityError, second_user.Persist)
            db.session.rollback()
            second_user.username = test_user_username
            second_user.email = u'foo@bar.baz'
            self.assertRaises(IntegrityError, second_user.Persist)
            db.session.rollback()
            second_user.username = u'foo'
            second_user.name = None
            self.assertRaises(IntegrityError, second_user.Persist)
            db.session.rollback()
            second_user.username = u'foo'
            second_user.name = test_user_name
            second_user.Persist()
            self.assertEqual([new_user, second_user], users.User.query.all(), 'Both users should be in the db.')

        
if __name__ == '__main__':
    unittest.main()

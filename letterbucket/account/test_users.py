import faker
import unittest
from sqlalchemy.exc import IntegrityError

import users
from ..config import test
from .. import create_application, db

class UserModelTest(unittest.TestCase):

    def _AssertConstraintError(self, callable, type, column, msg='', *args, **kwargs):
        re = ''.join((r'.*\b', type.upper(), r'\b.*\b', column.lower(), r'\b.*'))
        if msg:
            try:
                with self.assertRaisesRegexp(IntegrityError, re):
                    callable(*args, **kwargs)
            except AssertionError as ex:
                raise AssertionError('%s (%s)' % (msg, ex.message))
        else:
            self.assertRaisesRegexp(IntegrityError, re, callable, *args, **kwargs)
        db.session.rollback()

    def setUp(self):
        self.config_class = test.MemoryConfig
        self.app = create_application(config_object=self.config_class)
        with self.app.test_request_context():
            db.create_all()
        self.fake_data = faker.Faker()

    def testCreateUser(self):
        test_user_username = self.fake_data.user_name()
        test_user_name = self.fake_data.name()
        test_user_email = self.fake_data.email()
        test_user_password = self.fake_data.word()
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
        with self.app.test_request_context():
            self.assertEqual([], users.User.query.all(), 'Should be no users in the db.')
            new_user = users.User(self.fake_data.user_name(),
                                  self.fake_data.email(),
                                  self.fake_data.name(),
                                  self.fake_data.word())
            new_user.Persist()
            self.assertEqual([new_user], users.User.query.all(), 'User should be in the db.')
            second_user = users.User(self.fake_data.user_name(),
                                     self.fake_data.email(),
                                     self.fake_data.name(),
                                     self.fake_data.word())
            second_user.username = new_user.username
            self._AssertConstraintError(second_user.Persist, 'UNIQUE', 'username',
                                        msg='Username must be unique.')
            second_user.username = self.fake_data.user_name()
            second_user.email = new_user.email
            self._AssertConstraintError(second_user.Persist, 'UNIQUE', 'email',
                                        msg='Email must be unique.')
            second_user.email = self.fake_data.email()
            second_user.name = None
            self._AssertConstraintError(second_user.Persist, 'NOT NULL', 'name',
                                        msg='Name must not be null.')
            second_user.name = self.fake_data.name()
            second_user.password_hash = None
            self._AssertConstraintError(second_user.Persist, 'NOT NULL', 'password_hash',
                                        msg='Password must not be null.')
            second_user.SetPassword(self.fake_data.word())
            second_user.Persist()
            self.assertEqual([new_user, second_user], users.User.query.all(), 'Both users should be in the db.')


    def testUserPasswords(self):
        with self.app.test_request_context():
            test_password = self.fake_data.word()
            new_user = users.User(self.fake_data.user_name(),
                                  self.fake_data.email(),
                                  self.fake_data.name(),
                                  test_password)
            self.assertEquals(users.GetPasswordHash(test_password),
                              new_user.password_hash,
                              'Ensure password set correctly at creation.')
            test_password = self.fake_data.word()
            new_user.SetPassword(test_password)
            self.assertEquals(users.GetPasswordHash(test_password),
                              new_user.password_hash,
                              'Ensure password set correctly after creation.')
            # Make sure null passwords are not allowed.
            self.assertRaises(ValueError, new_user.SetPassword, None)
            self.assertRaises(ValueError, new_user.SetPassword, '')
            self.assertRaises(ValueError, users.User, self.fake_data.user_name(),
                              self.fake_data.email(), self.fake_data.name(), None)
            self.assertRaises(ValueError, users.User, self.fake_data.user_name(),
                              self.fake_data.email(), self.fake_data.name(), '')

    def testUserFlaskLoginInterface(self):
        with self.app.test_request_context():
            test_password = self.fake_data.word()
            new_user = users.User(self.fake_data.user_name(),
                                  self.fake_data.email(),
                                  self.fake_data.name(),
                                  self.fake_data.word())
            new_user.Persist()
            self.assertTrue(new_user.is_authenticated(),
                            'User model is always authenticaed.')
            # TODO(dirtnap): Update this when privileges are implemented.
            self.assertTrue(new_user.is_active(),
                            'User model is always active.')
            self.assertFalse(new_user.is_anonymous(),
                             'User model is never anonymous.')
            self.assertEquals(unicode(new_user.id), new_user.get_id(),
                              'get_id must return primary key.')
            self.assertEquals(new_user, users.User.GetById(new_user.get_id()),
                              'User loader must load by get_id.')

        
if __name__ == '__main__':
    unittest.main()

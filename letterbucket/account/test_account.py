import faker
import faker.providers
import unittest
import urlparse

from . import view, users
from ..config import test
from .. import create_application, db

class AccountTest(unittest.TestCase):

    def _CreateTestUser(self):
        test_username = self.fake_data.user_name()
        test_password = self.fake_data.password()
        with self.app.app_context():
            test_user = users.User(test_username, self.fake_data.email(),
                                   self.fake_data.name(), test_password)
            test_user.Persist()
        return (test_username, test_password)

    def setUp(self):
        self.config_class = test.MemoryConfig
        self.app = create_application(config_object=self.config_class)
        with self.app.test_request_context():
            db.create_all()
        self.fake_data = faker.Faker()
        self.client = self.app.test_client()

    def testLogin(self):
        test_username, test_password = self._CreateTestUser()
        rv = self.client.post('/login', data=dict(username=test_username,
                              password=test_password,
                              remember=0),
                              follow_redirects=True)
        self.assertEquals(200, rv.status_code, 'Status OK after login request.')
        self.assertIn('Login Succeeded', rv.data, 'Login Succeeded.')

    def testCreate(self):
        test_username = self.fake_data.user_name()
        test_email = self.fake_data.email()
        test_name = self.fake_data.name()
        test_password = self.fake_data.password()
        test_blog_name = self.fake_data.catch_phrase()
        test_blog_path = self.fake_data.uri_page()
        rv = self.client.post('/create', data=dict(username=test_username,
                              email=test_email,
                              name=test_name,
                              password=test_password,
                              blog_path=test_blog_path,
                              blog_name=test_blog_name),
                              follow_redirects=True)
        self.assertEquals(200, rv.status_code, 'Status OK after create request.')
        with self.app.app_context():
            user = users.User.GetByUsername(test_username)
            self.assertEquals(test_username, user.username,
                              'Username correct in database.')
            self.assertEquals(test_email, user.email,
                              'Email correct in database.')
            self.assertEquals(test_name, user.name,
                              'Name correct in database.')
            self.assertTrue(user.ValidatePassword(test_password),
                            'Password correct in database.')
            self.assertEquals(test_blog_path, user.blog.path,
                              'Blog path correct in database.')
            self.assertEquals(test_blog_name, user.blog.name,
                              'Blog name correct in database.')

    def testPasswordReset(self):
        test_username, test_password = self._CreateTestUser()
        rv = self.client.post('/login', data=dict(username=test_username,
                              password=test_password,
                              remember='on'),
                              follow_redirects=True)
        self.assertEquals(200, rv.status_code, 'Log-in OK')
        new_password = self.fake_data.password()
        rv = self.client.post('/reset', data=dict(old_password=test_password,
                              new_password=new_password,
                              repeat_password=new_password),
                              follow_redirects=True)
        self.assertEquals(200, rv.status_code, 'Status OK after reset.')
        self.assertIn('Password Updated', rv.data, 'Password updated.')
        with self.app.app_context():
            user = users.User.GetByUsername(test_username)
            self.assertTrue(user.ValidatePassword(new_password),
                            'Password updated by reset.')

class LoginGateTest(unittest.TestCase):

    def setUp(self):
        self.config_class = test.MemoryConfig
        self.app = create_application(config_object=self.config_class)
        with self.app.test_request_context():
            db.create_all()
        self.fake_data = faker.Faker()
        self.client = self.app.test_client()

    def testProfile(self):
        rv = self.client.get('/profile')
        self.assertEquals(302, rv.status_code, 'Response should be a redirect.')
        location = urlparse.urlparse(rv.headers.get('Location'))
        self.assertEquals('/login', location.path, 'Redirect to login page.')
        query = urlparse.parse_qs(location.query)
        self.assertIn('next', query, 'Query string contains the "next" parameter.')
        self.assertEquals(1, len(query['next']), '"next" has one value.')
        self.assertEquals('/profile', query['next'][0], 'Redirect to profile page.')

    def testProfile(self):
        rv = self.client.get('/reset')
        self.assertEquals(302, rv.status_code, 'Response should be a redirect.')
        location = urlparse.urlparse(rv.headers.get('Location'))
        self.assertEquals('/login', location.path, 'Redirect to login page.')
        query = urlparse.parse_qs(location.query)
        self.assertIn('next', query, 'Query string contains the "next" parameter.')
        self.assertEquals(1, len(query['next']), '"next" has one value.')
        self.assertEquals('/reset', query['next'][0], 'Redirect to reset page.')

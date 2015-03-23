import faker
import unittest

import blogs, posts
from ..account import users
from ..config import test
from ..utilities import testing
from .. import create_application, db

class PostStatusModelTest(testing.DbModelTestCase):

    def setUp(self):
        self.config_class = test.MemoryConfig
        self.app = create_application(config_object=self.config_class)
        with self.app.test_request_context():
            db.create_all()
        self.fake_data = faker.Faker()

    def testNewStatus(self):
        test_status_code = self.fake_data.word().lower()
        with self.app.test_request_context():
            self.assertEqual([], posts.PostStatus.query.all(), 'Should Have No Statuses.')
            test_post_status = posts.PostStatus(test_status_code)
            self.assertEqual([], posts.PostStatus.query.all(), 'Should Have No Statuses.')
            db.session.add(test_post_status)
            db.session.commit()
            self.assertEqual([test_post_status], posts.PostStatus.query.all(), 'Should be committed.')
            self.assertEqual(test_status_code.upper(), test_post_status.code, 'Code should match in uppercase.')
            self.assertEqual(None, test_post_status.description, 'Status has no description')
            new_id = test_post_status.id
            test_status_description = self.fake_data.catch_phrase()
            test_post_status = posts.PostStatus(test_status_code, test_status_description)
            self.assertEqual(new_id, test_post_status.id, 'ID should be re-used by code')
            self.assertEqual(test_status_description, test_post_status.description,
                             'Description should be updated when null.')
            db.session.commit()
            test_post_status = posts.PostStatus.query.get(new_id)
            self.assertEqual(test_status_code.upper(), test_post_status.code,
                             'Code should be stored to the db.')
            self.assertEqual(test_status_description, test_post_status.description,
                             'Description should be stored to the db.')
            test_status_description = self.fake_data.catch_phrase()
            test_post_status = posts.PostStatus(test_status_code, test_status_description)
            self.assertEqual(test_status_description, test_post_status.description,
                             'Description should be updated by new value.')
            db.session.commit()
            test_post_status = posts.PostStatus(test_status_code, description=None)
            self.assertEqual(test_status_description, test_post_status.description,
                             'Description should not be overwritten by None.')
            self.assertEqual(test_post_status, posts.PostStatus.GetByCode(test_status_code),
                             'Retrieve by code should match.')

    def testGetPostById(self):
        with self.app.test_request_context():
            self.assertEqual([], users.User.query.all(), 'Should be no users in the db.')
            test_user_username = self.fake_data.user_name()
            test_user_name = self.fake_data.name()
            test_user_email = self.fake_data.email()
            test_user_password = self.fake_data.word()

            new_user = users.User(test_user_username,
                                  test_user_email,
                                  test_user_name,
                                  test_user_password)
            new_user.Persist()

            self.assertEqual([], blogs.Blog.query.all(), 'Should be no blogs in the db.')
            test_blog_path = self.fake_data.word()
            test_blog_name = self.fake_data.name()
            new_blog = blogs.Blog(test_blog_path,
                                  test_blog_name,
                                  new_user)
            new_blog.Persist()

            self.assertEqual([], posts.Post.query.all(), 'Should be no posts in the db.')
            test_post_title = self.fake_data.word()
            test_post_body = self.fake_data.text()
            new_post = posts.Post(new_blog,
                                  test_post_title,
                                  test_post_body)

class PostModelTest(testing.DbModelTestCase):
    # TODO(bryanxcole): Implement tests for the Post Model
    pass

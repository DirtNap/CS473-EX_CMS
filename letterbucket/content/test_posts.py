import faker
import unittest

import posts
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
            self.assertEqual(test_post_status, posts.PostStatus.GetStatusByCode(test_status_code),
                             'Retrieve by code should match.')

class PostModelTest(testing.DbModelTestCase):
    # TODO(bryanxcole): Implement tests for the Post Model
    pass

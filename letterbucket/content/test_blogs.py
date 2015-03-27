import faker
import unittest

import blogs

from .. import db, create_application
from ..account import users
from ..config import test
from ..utilities import testing

class BlogModelTest(testing.DbModelTestCase):

    def setUp(self):
        self.config_class = test.MemoryConfig
        self.app = create_application(config_object=self.config_class)
        with self.app.test_request_context():
            db.create_all()
        self.fake_data = faker.Faker()
        
    
    def testCreateBlog(self):
        test_blog_path = self.fake_data.uri_path()
        test_blog_name = self.fake_data.name()

        with self.app.test_request_context():
            self.assertEqual([], blogs.Blog.query.all(), 'Should be no blogs in the db.')
            new_user = users.User(self.fake_data.user_name(),
                                  self.fake_data.email(),
                                  self.fake_data.name(),
                                  self.fake_data.word())
            new_user.Persist()
            new_blog = blogs.Blog(test_blog_path,
                                  test_blog_name,
                                  new_user)
            self.assertEqual(test_blog_path, new_blog.path, 'Paths should match')
            self.assertEqual(test_blog_name, new_blog.name, 'Names should match')
            self.assertEqual(new_user.id, new_blog.owner_id, 'user_id addresses should match')
            self.assertEqual([], blogs.Blog.query.all(), 'Should be no blogs in the db.')
            self.assertFalse(new_blog.IsPersisted(), 'Blog has not yet been committed.')
            new_blog = blogs.Blog(self.fake_data.uri_page(),
                                  self.fake_data.catch_phrase(),
                                  new_user)
            new_blog.Persist()
            self.assertEqual([new_blog], blogs.Blog.query.all(), 'Blog should be in the db.')
            self.assertTrue(new_blog.IsPersisted(), 'Blog should be committed.')

	
    def testBlogConstraints(self):
        with self.app.test_request_context():
            self.assertEqual([], blogs.Blog.query.all(), 'Should be no blogs in the db.')
            new_user = users.User(self.fake_data.user_name(),
                                  self.fake_data.email(),
                                  self.fake_data.name(),
                                  self.fake_data.word())
            new_user.Persist()            
            
            no2_user = users.User(self.fake_data.user_name(),
                                  self.fake_data.email(),
                                  self.fake_data.name(),
                                  self.fake_data.word())
            no2_user.Persist()            
            
            new_blog = blogs.Blog(self.fake_data.uri_path(),
                                  self.fake_data.name(),
                                  new_user)
            new_blog.Persist()                      
            self.assertEqual([new_blog], blogs.Blog.query.all(), 'Blog should be in the db.')
                                  
            second_blog = blogs.Blog(self.fake_data.uri_path(),
                                     self.fake_data.name(),
                                     no2_user)
            second_blog.path = new_blog.path
            self._AssertConstraintError(db, self.UNIQUE_ASSERTION_RE, 'path',
                                        second_blog.Persist,
                                        msg='Path must be unique.')
            second_blog.path = self.fake_data.uri_path()

            second_blog.owner_id = new_blog.owner_id            
            self._AssertConstraintError(db, self.UNIQUE_ASSERTION_RE, 'owner_id',
                                        second_blog.Persist,
                                        msg='Owner_ID must be unique.')
            second_blog.owner_id = no2_user.id

            second_blog.name = None
            self._AssertConstraintError(db, self.NOT_NULL_ASSERTION_RE, 'name',
                                        second_blog.Persist,
                                        msg='Name must not be null.')
            second_blog.name = self.fake_data.name()
            second_blog.Persist()
            self.assertEquals([new_blog, second_blog], blogs.Blog.query.all(), 'Both users should be in the db.')

        
if __name__ == '__main__':
    unittest.main()
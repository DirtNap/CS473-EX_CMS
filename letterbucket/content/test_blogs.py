import faker
import unittest
#import blogs
import posts

import blogs
from ..config import test
from ..utilities import testing
from .. import create_application, db


class BlogModelTest(testing.DbModelTestCase):

    def setUp(self):
        self.config_class = test.MemoryConfig
        self.app = create_application(config_object=self.config_class)
        with self.app.test_request_context():
            db.create_all()
        self.fake_data = faker.Faker()
        
    
    def testCreateBlog(self):
        test_blog_path = self.fake_data.path()
        test_blog_name = self.fake_data.name()
        test_user_owner_id = self.fake_owner_id()
        with self.app.test_request_context():
            self.assertEqual([], blogs.Blogs.query.all(), 'Should be no blogs in the db.')
            new_blog = blogs.Blogs(test_blog_path,
                                  test_blog_name,
                                  test_blog_owner_id)
            self.assertEqual(test_blog_path, new_blog.path, 'Paths should match')
            self.assertEqual(test_blog_name, new_blog.path, 'Names should match')
            self.assertEqual(test_blog_user_id, new_blog.user_id, 'user_id addresses should match')
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
            new_blog = blogs.Blog(self.fake_data.path(),
                                  self.fake_data.name(),
                                  self.fake_data.user_id())
            # new_blog.Persist()
            self.assertEqual([new_blog], blogs.Blog.query.all(), 'Blog should be in the db.')
            second_blog = blogs.Blog(self.fake_data.path(),
                                     self.fake_data.name(),
                                     self.fake_data.user_id())

            second_blog.path = new_blog.path
            self._AssertConstraintError(second_blog.Persist, 'UNIQUE', 'path',
                                        msg='Path must be unique.')
            second_blog.path = self.fake_data.uri_path()

            second_blog.owner_id = new_user.id            
            self._AssertConstraintError(second_blog.Persist, 'UNIQUE', 'owner_id',
                                        msg='User_ID must be unique.')
            second_blog.owner_id = second_user.id()            

            second_user.name = None
            self._AssertConstraintError(second_user.Persist, 'NOT NULL', 'name',
                                        msg='Name must not be null.')
            second_user.name = self.fake_data.name()
            
            second_blog.owner_id = second_user.id + 10 # should not exist
            second_blog.Persist()
            
            second_user.Persist()
            self.assertEquals([new_user, second_user], users.User.query.all(), 'Both users should be in the db.')

        
if __name__ == '__main__':
    unittest.main()
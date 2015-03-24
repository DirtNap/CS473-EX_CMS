import faker
import random

from flask import Flask

from letterbucket import create_application, db
from letterbucket.account import users
from letterbucket.config import test
from letterbucket.content import blogs, posts



# TODO(dirtnap): Make this argument based
config = test.LocalConfig

# Get a letterbucket application
app = create_application(config_object=config)

if __name__ == '__main__':
    with app.app_context():
        # Create the necessary base database, if needed
        db.create_all(app=app)
        admin_user = users.User.GetByUsername('admin')
        if not admin_user:
            admin_user = users.User('admin', 'cms@letterbucket.net',
                                    'Site Administrator', 'site_admin')
            db.session.add(admin_user)
            db.session.commit()
            admin_blog = blogs.Blog('site-news', 'LetterBucket Site News', admin_user)
            db.session.add(admin_blog)
            db.session.commit()
        print "Adding additional content."
        fake_data = faker.Faker()
        for user_ct in range(random.randint(1, 32)):
            created_user = users.User(fake_data.user_name(),
                                      fake_data.email(),
                                      fake_data.name(),
                                      fake_data.word()
            )
            created_user.Persist()
            print 'Added user %s' % created_user
            new_blog = True
            try:
                created_blog = blogs.Blog(fake_data.word(),
                                          fake_data.catch_phrase(),
                                          created_user
                                      )
                created_blog.Persist()
                print 'Added blog %s' % created_blog
            except:
                db.session.rollback()
                new_blog = False
            if new_blog:
                for _ in range(random.randint(1,24)):
                    created_post = posts.Post(created_blog,
                                              fake_data.catch_phrase(),
                                              '\n\n'.join(fake_data.paragraphs(
                                                  random.randrange(2, 6))),
                                              posts.PostStatus('Published')
                    )
                new_date = fake_data.date_time_between(start_date='-90d',
                                                       end_date='now')
                created_post.create_date = new_date
                created_post.pub_date = new_date
                created_post.last_modified_by = created_user.id
                created_post.last_modified_date = new_date
                db.session.add(created_post)
            db.session.commit()

    # Run the app
    app.run()

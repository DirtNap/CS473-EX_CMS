from flask import Flask

from letterbucket import create_application, db
from letterbucket.account import users
from letterbucket.config import test



config = test.LocalConfig

app = create_application(config_object=config)

if __name__ == '__main__':
    with app.app_context():
        db.create_all(app=app)
        admin_user = users.User.GetByUsername('admin')
        if not admin_user:
            admin_user = users.User('admin', 'cms@letterbucket.net', 'site_admin')
            db.session.add(admin_user)
            db.session.commit()
    app.run()

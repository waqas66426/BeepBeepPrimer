import os
from flask import Flask
from monolith.database import db, User
from monolith.views import blueprints
from monolith.auth import login_manager


def create_app():
    app = Flask(__name__)
    app.config['WTF_CSRF_SECRET_KEY'] = 'A SECRET KEY'
    app.config['SECRET_KEY'] = 'ANOTHER ONE'
    # app.config['STRAVA_CLIENT_ID'] = 29641
    # app.config['STRAVA_CLIENT_SECRET'] = "097321492b94a769fe8be68a50ab2a780f30b6dc"

    app.config['STRAVA_CLIENT_ID'] = os.environ['STRAVA_CLIENT_ID']
    app.config['STRAVA_CLIENT_SECRET'] = os.environ['STRAVA_CLIENT_SECRET']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///beepbeep.db'
    # app.config['MAIL_SERVER']='smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = os.environ['EMAIL_ID']
    # app.config['MAIL_PASSWORD'] = os.environ['EMAIL_PASS']
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True




    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    db.init_app(app)
    login_manager.init_app(app)
    db.create_all(app=app)

    # create a first admin user
    with app.app_context():
        q = db.session.query(User).filter(User.email == 'example@example.com')
        user = q.first()
        if user is None:
            example = User()
            example.email = 'example@example.com'
            example.is_admin = True
            example.set_password('admin')
            db.session.add(example)
            db.session.commit()
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

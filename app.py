from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = "randomstring"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    db.init_app(app)

    from englix.views import englix
    app.register_blueprint(englix)

    
    from englix.models import User, Lesson, Activity, Quiz, Answer

    admin = Admin(app, name='Englix')
    login_manager = LoginManager(app)
    
    login_manager.login_view = 'englix.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Lesson, db.session))
    admin.add_view(ModelView(Activity, db.session))
    admin.add_view(ModelView(Quiz, db.session))
    admin.add_view(ModelView(Answer, db.session))
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
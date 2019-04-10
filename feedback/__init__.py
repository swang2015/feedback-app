import os
from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


## App

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmpl_dir = os.path.join(parent_dir, 'templates')
static_dir = os.path.join(parent_dir, 'static')

app = Flask('subs-feedback', template_folder=tmpl_dir, static_folder=static_dir)
app.config.from_pyfile('config.py')


## Extensions

login_manager = LoginManager(app)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


## Blueprints

from feedback.main.view import main_blueprint
from feedback.user.view import user_blueprint
app.register_blueprint(main_blueprint)
app.register_blueprint(user_blueprint)


## Login users

from feedback.model import User

login_manager.login_view = "usersys.login"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()

## Error handlers

# @app.errorhandler(403)
# def forbidden_page(error):
#     return render_template("errors/403.html"), 403


# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template("errors/404.html"), 404


# @app.errorhandler(500)
# def server_error_page(error):
#     return render_template("errors/500.html"), 500

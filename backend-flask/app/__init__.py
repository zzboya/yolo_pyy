from flask import Flask
from config import Config
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
    app.config['UPLOAD_FOLDER'] = config_class.UPLOAD_FOLDER
    app.static_folder = config_class.STATIC_FOLDER 
    app.template_folder = config_class.TEMPLATE_FOLDER
    app.config["SQLALCHEMY_DATABASE_URI"] = config_class.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)
    from app.Controller.user import authentication_blueprint as auth
    app.register_blueprint(auth)
    from app.Controller.routes import bp_routes as routes
    app.register_blueprint(routes)
    if not app.debug and not app.testing:
        pass
        # ... no changes to logging setup

    return app

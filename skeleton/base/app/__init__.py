from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from config import config
from app.common.database import Database as db

bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    db.initialize(config[config_name].DATABASE_NAME)

    from app.models import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
import os
from flask import Flask
from application.main.routes import powerball

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.register_blueprint(powerball)
    return app
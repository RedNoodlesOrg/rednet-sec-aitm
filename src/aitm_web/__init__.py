from __future__ import annotations

from asgiref.wsgi import WsgiToAsgi
from flask import Flask

from .routes import main


def create_app():
    app = Flask(__name__)
    # app.config.from_object("config")

    app.register_blueprint(main)

    return WsgiToAsgi(app)

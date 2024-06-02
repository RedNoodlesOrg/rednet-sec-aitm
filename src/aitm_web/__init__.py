from __future__ import annotations

import logging

from flask import Flask

from .routes import main
from .socket import socketio


class SocketIOHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        socketio.emit("new_log", log_entry)


def create_app():
    app = Flask(__name__)
    # app.config.from_object("config")
    logging.root.addHandler(SocketIOHandler())
    app.register_blueprint(main)
    socketio.init_app(app)
    return app

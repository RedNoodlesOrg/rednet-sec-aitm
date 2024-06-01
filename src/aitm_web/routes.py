from __future__ import annotations

from flask import Blueprint, jsonify, render_template

main = Blueprint("main", __name__)


@main.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})


@main.route("/")
def index():
    return render_template("base.html.j2")


@main.route("/mock")
def mock():
    return render_template("mock.html.j2")

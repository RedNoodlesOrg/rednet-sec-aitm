from __future__ import annotations

from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/status")
def index():
    return render_template("status.html.j2")


@main.route("/logs")
def logs():
    return render_template("logs.html.j2")

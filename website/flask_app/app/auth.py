from app import logger
from app.models import User
from helpers.logger import exception

from werkzeug.security import check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)


@exception(logger)
@auth.route("/login999", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User(id=username).get_user()
        if user:
            if check_password_hash(user.password, password):
                # connexion
                login_user(user)
                return redirect(
                    url_for("views.admin"), code=303
                )  # code 303 sinon fail2ban detecte comme une mauvaise auth

        flash("wrong password or username", category="error")
        return redirect(url_for("auth.login"), code=302)
    return render_template("login.html", user=current_user)


@exception(logger)
@auth.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

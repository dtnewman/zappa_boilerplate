# -*- coding: utf-8 -*-
'''Public section, including homepage and signup.'''
from flask import (Blueprint, request, render_template, flash, url_for,
                    redirect, session, jsonify)
from flask.ext.login import login_user, login_required, logout_user

from basic_zappa_project.database import db_session
from basic_zappa_project.extensions import login_manager
from basic_zappa_project.user.models import User
from basic_zappa_project.public.forms import LoginForm
from basic_zappa_project.user.forms import RegisterForm
from basic_zappa_project.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(db_session, int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", 'success')
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
    return redirect(url_for('public.home'))


@blueprint.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
        db_session.add(new_user)
        db_session.commit()
        flash("Thank you for registering. You can now log in.", 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route("/about")
def about():
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route("/status")
def status():
    return jsonify({'status': 'ok'})



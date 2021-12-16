from flask import Blueprint, request, render_template, redirect, url_for, abort
from main import db, lm
from models.users import User
from models.projects import Project
from schemas.user_schema import user_schema, users_schema, user_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError
from sqlalchemy import func

# Getting a user instance based on the session information in their browser cookie
@lm.user_loader
def load_user(user):
    return User.query.get(user)

# Bouncing users who aren't authorized over to the login page,
# if they try to access something that needs authorization. 
@lm.unauthorized_handler
def unauthorized():
    return redirect('/users/login/')

users = Blueprint('users', __name__)

# The get routes endpoint.
@users.route("/users/", methods=["GET"])
def get_users():
    data = {
        "page_title": "User Index",
        "users": users_schema.dump(User.query.all())
    }
    return render_template("user_index.html", page_data = data)

# The signup route endpoint.
@users.route("/users/signup/", methods=["GET", "POST"])
def sign_up():
    data = {"page_title": "Sign Up"}
    
    if request.method == "GET":
        return render_template("signup.html", page_data = data)
    
    new_user = user_schema.load(request.form)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for("users.get_users"))

# The login route
@users.route("/users/login/", methods=["GET", "POST"])
def log_in():
    data = {"page_title": "Log In"}

    if request.method == "GET":
        return render_template("login.html", page_data = data)

    user = User.query.filter_by(email=request.form["email"]).first()
    if user and user.check_password(password=request.form["password"]):
        login_user(user)
        return redirect(url_for('projects.get_projects'))
    
    abort(401, "Login unsuccessful. Did you supply the correct username and password?")

# User details
@users.route("/users/account/", methods=["GET", "POST"])
@login_required
def user_detail():
    if request.method == "GET":
        data = {
            "page_title": "Account Details",
            "projects_count": db.session.query(func.count(Project.project_id)).filter(Project.creator_id==current_user.id).scalar()
        }
        return render_template("user_details.html", page_data = data)
    
    # anything past the GET return must be for POST requests
    user = User.query.filter_by(id = current_user.id)
    updated_fields = user_schema.dump(request.form)
    errors = user_update_schema.validate(updated_fields)
    
    if errors:
        raise ValidationError(message=errors)

    user.update(updated_fields)
    db.session.commit()
    return redirect(url_for("users.get_users"))

# Logout
@users.route("/users/logout/", methods=["POST"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("users.log_in"))
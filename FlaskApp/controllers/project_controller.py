from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.projects import Project
from schemas.project_schema import project_schema, projects_schema
from flask_login import login_required, current_user
import boto3

projects = Blueprint('projects', __name__)


### VIEWS ###

# Homepage route endpoint
@projects.route('/')
def home_page():
    data = {
    "page_title": "Homepage"
    }
    return render_template("homepage.html", page_data=data)


# The GET routes endpoint
@projects.route("/projects/", methods=["GET"])
def get_projects():

    """ s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': project.image_filename
        },
        ExpiresIn=100
    ) """
    
    data = {
    "page_title": "Project Gallery",
    "projects": projects_schema.dump(Project.query.group_by(Project.project_id).all())
    # "image": image_url
    }
    return render_template("project_gallery.html", page_data=data)


# The POST route endpoint
@projects.route("/projects/", methods=["POST"])
@login_required
def create_project():
    new_project = project_schema.load(request.form)
    new_project.creator = current_user
    db.session.add(new_project)
    db.session.commit()

    # check 
    print(project_schema.dump(new_project))
    return redirect(url_for("projects.get_projects")) 


# The GET specific route endpoint
@projects.route("/projects/<int:id>/", methods=["GET"])
def get_project(id):
    project = Project.query.get_or_404(id)

    s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': project.image_filename
        },
        ExpiresIn=100
    )

    data = {
        "page_title": "Project Details",
        "project": project_schema.dump(project),
        "image": image_url
    }
    return render_template("project_details.html", page_data=data)


# The PUT/PATCH route
@projects.route("/projects/<int:id>/", methods=["POST"])
@login_required
def update_project(id):

    project = Project.query.filter_by(project_id=id)

    if current_user.id != project.first().creator_id:
        abort(403, "You do not have permission to alter this project!")

    updated_fields = project_schema.dump(request.form)
    if updated_fields:
        project.update(updated_fields)
        db.session.commit()
    
    data = {
        "page_title": "Project Details",
        "project": project_schema.dump(project.first())
    }
    return render_template("project_details.html", page_data=data)

# Add pattern to project
""" @projects.route("/projects/<int:id>/add_pattern/", methods=["POST"])
@login_required
def add_to_project(id):
    project = Project.query.get_or_404(id)
    project.patterns.append(current_pattern)
    db.session.commit()
    return redirect(url_for('project.project_details')) """

# Remove pattern from project
""" @projects.route("/projects/<int:id>/drop/", methods=["POST"])
@login_required
def remove_pattern(id):
    project = Project.query.get_or_404(id)
    project.students.remove(current_user)
    db.session.commit()
    return redirect(url_for('users.user_detail')) """

# The DELETE endpoint
@projects.route("/projects/<int:id>/delete/", methods=["POST"])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)

    if current_user.id != project.creator_id:
        abort(403, "You do not have permission to delete this project!")

    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("projects.get_projects"))


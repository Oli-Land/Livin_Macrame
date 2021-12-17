from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.patterns import Pattern
from schemas.pattern_schema import pattern_schema, patterns_schema
from flask_login import login_required, current_user
import boto3

patterns = Blueprint('patterns', __name__)


### VIEWS ###


# The GET routes endpoint
@patterns.route("/patterns/", methods=["GET"])
def get_patterns():

    """ s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': pattern.image_filename
        },
        ExpiresIn=100
    ) """
    
    data = {
    "page_title": "Pattern Gallery",
    "patterns": patterns_schema.dump(Pattern.query.group_by(Pattern.pattern_id).all())
    # "image": image_url
    }
    return render_template("pattern_gallery.html", page_data=data)


# The POST route endpoint
@patterns.route("/patterns/", methods=["POST"])
@login_required
def create_pattern():
    new_pattern = pattern_schema.load(request.form)
    new_pattern.creator = current_user
    db.session.add(new_pattern)
    db.session.commit()

    return redirect(url_for("patterns.get_patterns")) 


# The GET specific route endpoint
@patterns.route("/patterns/<int:id>/", methods=["GET"])
def get_pattern(id):
    pattern = Pattern.query.get_or_404(id)

    s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': pattern.image_filename
        },
        ExpiresIn=100
    )

    data = {
        "page_title": "Pattern Details",
        "pattern": pattern_schema.dump(pattern),
        "image": image_url
    }
    return render_template("pattern_details.html", page_data=data)


# The PUT/PATCH route
@patterns.route("/patterns/<int:id>/", methods=["POST"])
@login_required
def update_pattern(id):

    pattern = Pattern.query.filter_by(pattern_id=id)

    if current_user.id != pattern.first().creator_id:
        abort(403, "You do not have permission to alter this pattern!")

    updated_fields = pattern_schema.dump(request.form)
    if updated_fields:
        pattern.update(updated_fields)
        db.session.commit()
    
    data = {
        "page_title": "Pattern Details",
        "pattern": pattern_schema.dump(pattern.first())
    }
    return render_template("pattern_details.html", page_data=data)

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
@patterns.route("/patterns/<int:id>/delete/", methods=["POST"])
@login_required
def delete_pattern(id):
    pattern = Pattern.query.get_or_404(id)

    if current_user.id != pattern.creator_id:
        abort(403, "You do not have permission to delete this pattern!")

    db.session.delete(pattern)
    db.session.commit()
    return redirect(url_for("patterns.get_patterns"))


from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.knots import Knot
from schemas.knot_schema import knot_schema, knots_schema
from flask_login import login_required, current_user
import boto3

knots = Blueprint('knots', __name__)


### VIEWS ###


# The GET routes endpoint
@knots.route("/knots/", methods=["GET"])
def get_knots():

    data = {
        "page_title": "Knot Gallery",
        "knots": Knot.query.group_by(Knot.knot_id).all()
    }

    for knot in data["knots"]:
        

        s3_client=boto3.client('s3')
        bucket_name=current_app.config["AWS_S3_BUCKET"]
        image_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': knot.image_filename
            },
            ExpiresIn=100
        )

        knot.image_url = image_url
    
    
    return render_template("knot_gallery.html", page_data=data)


# The POST route endpoint
@knots.route("/knots/", methods=["POST"])
@login_required
def create_knot():
    new_knot = knot_schema.load(request.form)
    new_knot.creator = current_user
    db.session.add(new_knot)
    db.session.commit()

    return redirect(url_for("knots.get_knots")) 


# The GET specific route endpoint
@knots.route("/knots/<int:id>/", methods=["GET"])
def get_knot(id):
    knot = Knot.query.get_or_404(id)

    s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': knot.image_filename
        },
        ExpiresIn=100
    )

    data = {
        "page_title": "Knot Details",
        "knot": knot_schema.dump(knot),
        "image": image_url
    }
    return render_template("knot_details.html", page_data=data)


# The PUT/PATCH route
@knots.route("/knots/<int:id>/", methods=["POST"])
@login_required
def update_knot(id):

    knot = Knot.query.filter_by(knot_id=id)

    if current_user.id != knot.first().creator_id:
        abort(403, "You do not have permission to alter this knot!")

    updated_fields = knot_schema.dump(request.form)
    if updated_fields:
        knot.update(updated_fields)
        db.session.commit()
    
    data = {
        "page_title": "Knot Details",
        "knot": knot_schema.dump(knot.first())
    }
    return render_template("knot_details.html", page_data=data)

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
@knots.route("/knots/<int:id>/delete/", methods=["POST"])
@login_required
def delete_knot(id):
    knot = Knot.query.get_or_404(id)

    if current_user.id != knot.creator_id:
        abort(403, "You do not have permission to delete this knot!")

    db.session.delete(knot)
    db.session.commit()
    return redirect(url_for("knots.get_knots"))


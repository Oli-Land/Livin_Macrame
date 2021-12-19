from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.knots import Knot
from schemas.knot_schema import knot_schema, knots_schema
from flask_login import login_required, current_user
import boto3

from models.cords import Cord
from schemas.cord_schema import cord_schema

knots = Blueprint('knots', __name__)


### VIEWS ###


# The GET endpoint
@knots.route("/knots/", methods=["GET"])
def get_knots():

    data = {
        "page_title": "Knot Gallery",
        "knots": Knot.query.order_by(Knot.knot_id).all()
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


# The POST endpoint
@knots.route("/knots/", methods=["POST"])
@login_required
def create_knot():
    new_knot = knot_schema.load(request.form)
    new_knot.creator = current_user
    db.session.add(new_knot)
    db.session.commit()

    return redirect(url_for("knots.get_knot", id=new_knot.knot_id)) 


# The GET specific endpoint
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


# The PUT/PATCH endpoint
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

# Add cord to knot endpoint
@knots.route("/knots/<int:id>/add_cord/", methods=["POST"])
@login_required
def add_cord_to_knot(id):
    knot = Knot.query.get_or_404(id) 
    current_cord_id = cord_schema.dump(request.form)
    current_cord = Cord.query.get_or_404(current_cord_id)
    knot.cord = current_cord
    db.session.commit()
    return redirect(url_for('knots.get_knot', id=id))

# Remove cord from knot endpoint
@knots.route("/knots/<int:id>/remove_cord/", methods=["POST"])
@login_required
def remove_cord_from_knot(id):
    knot = Knot.query.get_or_404(id)
    knot.cord = None
    db.session.commit()
    return redirect(url_for('knots.get_knot', id=id))
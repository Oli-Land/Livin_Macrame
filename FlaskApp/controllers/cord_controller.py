from flask import Blueprint, jsonify, request, render_template, redirect, url_for, abort, current_app
from main import db
from models.cords import Cord
from schemas.cord_schema import cord_schema, cords_schema
from flask_login import login_required, current_user
import boto3

cords = Blueprint('cords', __name__)


### VIEWS ###


# The GET endpoint
@cords.route("/cords/", methods=["GET"])
def get_cords():

    data = {
        "page_title": "Cord Gallery",
        "cords": Cord.query.order_by(Cord.cord_id).all()
    }

    for cord in data["cords"]:
        

        s3_client=boto3.client('s3')
        bucket_name=current_app.config["AWS_S3_BUCKET"]
        image_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': bucket_name,
                'Key': cord.image_filename
            },
            ExpiresIn=100
        )

        cord.image_url = image_url
    
    
    return render_template("cord_gallery.html", page_data=data)


# The POST endpoint
@cords.route("/cords/", methods=["POST"])
@login_required
def create_cord():
    new_cord = cord_schema.load(request.form)
    new_cord.creator = current_user
    db.session.add(new_cord)
    db.session.commit()

    return redirect(url_for("cords.get_cord", id=new_cord.cord_id)) 


# The GET specific endpoint
@cords.route("/cords/<int:id>/", methods=["GET"])
def get_cord(id):
    cord = Cord.query.get_or_404(id)

    s3_client=boto3.client('s3')
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': cord.image_filename
        },
        ExpiresIn=100
    )

    data = {
        "page_title": "Cord Details",
        "cord": cord_schema.dump(cord),
        "image": image_url
    }
    return render_template("cord_details.html", page_data=data)


# The PUT/PATCH endpoint
@cords.route("/cords/<int:id>/", methods=["POST"])
@login_required
def update_cord(id):

    cord = Cord.query.filter_by(cord_id=id)

    if current_user.id != cord.first().creator_id:
        abort(403, "You do not have permission to alter this cord!")

    updated_fields = cord_schema.dump(request.form)
    if updated_fields:
        cord.update(updated_fields)
        db.session.commit()
    
    data = {
        "page_title": "Cord Details",
        "cord": cord_schema.dump(cord.first())
    }
    return render_template("cord_details.html", page_data=data)


# The DELETE endpoint
@cords.route("/cords/<int:id>/delete/", methods=["POST"])
@login_required
def delete_cord(id):
    cord = Cord.query.get_or_404(id)

    if current_user.id != cord.creator_id:
        abort(403, "You do not have permission to delete this cord!")

    db.session.delete(cord)
    db.session.commit()
    return redirect(url_for("cords.get_cords"))


from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.projects import Project
import boto3

project_images = Blueprint('project_images', __name__)

@project_images.route("/projects/<int:id>/image/", methods=["POST"])
def update_image(id):

    project = Project.query.get_or_404(id)

    if "image" in request.files:

        image = request.files["image"]

        if Path(image.filename).suffix != ".png":
            return abort(400, description="Invalid file type, please ensure image is a png")

        bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        bucket.upload_fileobj(image, project.image_filename)

        return redirect(url_for("projects.get_project", id=id))

    return abort(400, description="No image")
from main import db

class Course(db.Model):
    __tablename__ = "courses"

    # Specify what columns the table should have
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    price = db.Column(db.Integer(), nullable=False, server_default="0")


    @property
    def image_filename(self):
        return f"course_images/{self.course_id}.png"

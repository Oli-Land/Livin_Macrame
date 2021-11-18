from main import db

class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), default="No Description Provided")

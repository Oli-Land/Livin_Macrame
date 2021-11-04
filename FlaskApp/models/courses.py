from main import db

# call it what makes sense for your database
class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, course_name):
        self.course_name = course_name
    

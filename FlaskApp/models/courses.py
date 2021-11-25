from main import db
from models.users import User

enrolments = db.Table(
    'enrolments',
    db.Column('user_id', db.Integer, db.ForeignKey('flasklogin-users.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('courses.course_id'), primary_key=True)
)

# The model tells the ORM what tables should exist
# And lets us retrieve info from them
class Course(db.Model):
    __tablename__ = "courses"

    # Specify what columns the table should have
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    price = db.Column(db.Integer(), nullable=False, server_default="0")

    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin-users.id'))    # add , unique=True) here to make the relationship one-to-one

    students = db.relationship(
        User,
        secondary=enrolments,
        backref=db.backref('enrolled_courses'),
        lazy="joined"
    )

    @property
    def image_filename(self):
        return f"course_images/{self.course_id}.png"

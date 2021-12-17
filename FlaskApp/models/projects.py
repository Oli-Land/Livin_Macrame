from main import db
#from models.patterns import Pattern

#project_has_pattern = db.Table(
#    'project_has_pattern',
#    db.Column('pattern_id', db.Integer, db.ForeignKey('patterns.pattern_id'), primary_key=True),
#    db.Column('project_id', db.Integer, db.ForeignKey('projects.project_id'), primary_key=True)
#    # insert column for repeats here?
#)

# The model tells the ORM what tables should exist
# And lets us retrieve info from them
class Project(db.Model):
    __tablename__ = "projects"

    # Specify what columns the table should have
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    price = db.Column(db.Integer(), nullable=False, server_default="0")
    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin_users.id'))    # add , unique=True) here to make the relationship one-to-one

#    patterns = db.relationship(
#        Pattern,
#        secondary=project_has_pattern,
#        backref=db.backref('in_project'),
#        lazy="joined"
#    )

    @property
    def image_filename(self):
        return f"project_images/{self.project_id}.png"

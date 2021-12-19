from main import db


class Knot(db.Model):
    __tablename__ = "knots"

    knot_id = db.Column(db.Integer, primary_key=True)
    knot_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    length = db.Column(db.Integer)
    width = db.Column(db.Integer)
    num_of_cords = db.Column(db.Integer)
    cords_length = db.Column(db.Integer)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin_users.id'))
    cord_id = db.Column(db.Integer, db.ForeignKey('cords.cord_id'))

    patterns = db.relationship('Pattern', backref='knot', lazy="joined")


    @property
    def image_filename(self):
        return f"knot_images/{self.knot_id}.png"
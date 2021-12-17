from main import db


class Pattern(db.Model):
    __tablename__ = "patterns"

    pattern_id = db.Column(db.Integer, primary_key=True)
    pattern_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    length = db.Column(db.Integer)
    width = db.Column(db.Integer)
    num_of_cords = db.Column(db.Integer)
    cords_length = db.Column(db.Integer)
    total_cord = db.Column(db.Integer)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin_users.id')) 
    # knot_id = relation


    @property
    def image_filename(self):
        return f"pattern_images/{self.pattern_id}.png"
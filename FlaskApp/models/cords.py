from main import db


class Cord(db.Model):
    __tablename__ = "cords"

    cord_id = db.Column(db.Integer, primary_key=True)
    cord_name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), server_default="No Description Provided")
    material = db.Column(db.String(80))
    thickness = db.Column(db.Integer)
    cost_per_meter = db.Column(db.Integer)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('flasklogin_users.id')) 


    @property
    def image_filename(self):
        return f"cord_images/{self.cord_id}.png"
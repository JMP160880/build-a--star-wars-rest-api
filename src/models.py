from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    favorite_personaje_name = db.Column(db.String(250), unique=False, nullable=False)
    favorite_planet_name = db.Column(db.String(250), unique=False, nullable=False)
    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Personaje(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    
    def __repr__(self):
        return '<Personaje %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Planeta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    
    def __repr__(self):
        return '<Planeta %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
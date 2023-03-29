from main import db, app

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    year = db.Column(db.Integer)
    description = db.Column(db.String())
    actors = db.relationship('Role', back_populates='movie', cascade = 'all, delete-orphan')

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable = False)
    birthdate = db.Column(db.String(30))
    movies = db.relationship('Role', back_populates='actor', cascade = 'all, delete-orphan')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable = False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id'), nullable = False)
    role = db.Column(db.String(80), nullable = False)
    actor = db.relationship('Actor', back_populates='movies')
    movie = db.relationship('Movie', back_populates='actors')
with app.app_context():
  db.create_all()
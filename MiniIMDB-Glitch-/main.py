from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///imdb.db"
db.init_app(app)

import models

# home route
@app.route('/')
def home():
    return render_template('home.html', page_title='IT WORKS!')
  
@app.route('/about_us')
def about():
    return render_template('about_us.html', page_title='IT WORKS!')

@app.route('/all_movies')
def all_movies():
  movies = db.session.execute(db.select(models.Movie)).scalars()
  return render_template("all_movies.html", page_title="ALL MOVIES", movies=movies)

@app.route('/create_movies', methods = ["GET", "POST"])
def create_movie():
  if request.method == "POST":
    movie = models.Movie(
      title = request.form["title"],
      year = request.form["year"],
      description = request.form["description"]
    )
    db.session.add(movie)
    db.session.commit()
    return redirect(url_for('all_movies'))
  return render_template('create_movies.html')


@app.route('/movies/<int:id>')
def movie_info(id):
  movie = db.get_or_404(models.Movie, id)
  title = movie.title
  return render_template('movie_info.html', page_title=f"Movie - {title}", movie=movie)

#movie delete
@app.route('/movies/<int:id>/delete', methods = ["GET", "POST"])
def movie_delete(id):
  if request.method == "POST":
    movie = db.get_or_404(models.Movie, id)
    db.Session = db.Session.object_session(movie)
    db.Session.delete(movie)
    db.Session.commit()
    # flash
    return redirect(url_for('all_movies'))

@app.route('/all_actors')
def all_actors():
  actors = db.session.execute(db.select(models.Actor)).scalars()
  return render_template("all_actors.html", page_title="ALL ACTORS", actors=actors)

@app.route('/create_actors', methods = ["GET", "POST"])
def create_actor():
  if request.method == "POST":
    actor = models.Actor(
      name = request.form["name"],
      birthdate = request.form["DOB"]
    )
    db.session.add(actor)
    db.session.commit()
    return redirect(url_for('all_actors'))
  return render_template('create_actors.html')

@app.route('/actors/<int:id>')
def actor_info(id):
  actor = db.get_or_404(models.Actor, id)
  name = actor.name
  movies = db.session.execute(db.select(models.Movie)).scalars()
  return render_template('actor_info.html', page_title=f"Actor - {name}", actor=actor, movies = movies)

#movie delete
@app.route('/actors/<int:id>/delete', methods = ["GET", "POST"])
def actor_delete(id):
  if request.method == "POST":
    actor = db.get_or_404(models.Actor, id)
    db.Session = db.Session.object_session(actor)
    db.Session.delete(actor)
    db.Session.commit()
    # flash
    return redirect(url_for('all_actors'))

@app.route('/actors/<int:id>/role', methods = ["GET", "POST"])
def actor_role(id):
  if request.method == "POST":
    role = models.Role(
      movie_id = request.form["movie"],
      actor_id = id,
      role = request.form["role"]     
    )
    db.session.add(role)
    db.session.commit()
    return redirect(url_for('all_movies'))

@app.errorhandler(404)
def page_not_found(e):
  return render_template("404.html")
  
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
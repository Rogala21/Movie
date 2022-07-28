from flask import render_template, redirect, request, session
from flask_app.__init__ import app
from flask_app.models.movie import movie, movie_watched
from flask_app.models.login_register import user


@app.route('/movie')
def movie_home():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('movie.html', movies = movie.get_all_movies_movie(), user = user.get_by_id(session['user_id']))

@app.route('/movie/watch_later/<movie_id>')
def watch_later(movie_id):
    if 'user_id' not in session:
        return redirect('/logout')
    movies = movie.get_1_movie(movie_id)
    return render_template('watch_later.html', user = user.get_by_id(session['user_id']), movie = movies)

@app.route("/movie/add/watch_later", methods=['POST'])
def add_watch_later():
    movie.add_watch_later(request.form)
    return redirect('/movie')

@app.route("/movie/add/watched", methods=['POST'])
def add_watched():
    movie.add_watched(request.form)
    movie.remove_watch_later(request.form)
    return redirect('/account')

@app.route("/account/remove/later/<movie_id>")
def remove_later(movie_id):
    if 'user_id' not in session:
        return redirect('/logout')
    movie.remove_watch_later({"movie_id": movie_id, "user_id":session['user_id']})
    return redirect('/account')

@app.route("/account/remove/watched/<movie_id>")
def remove_watched(movie_id):
    if 'user_id' not in session:
        return redirect('/logout')
    movie.remove_watched({"movie_id": movie_id, "user_id":session['user_id']})
    movie.add_watch_later({"movie_id": movie_id, "user_id":session['user_id']})
    return redirect('/account')

@app.route('/new_movie')
def new_movie_page():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('new_movie.html', user = user.get_by_id(session['user_id']))

@app.route('/new_movie/process', methods=['POST'])
def new_movie_process():
    if not movie.check_stats(request.form):
        return redirect("/new_movie")
    data = movie.new_movie(request.form)
    return redirect('/home')

@app.route('/edit_movie/<movie_id>')
def edit_movie_page(movie_id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('edit_movie.html', user = user.get_by_id(session['user_id']), movie = movie.get_1_movie(movie_id))

@app.route('/edit_movie/<movie_id>/process', methods=['POST'])
def edit_movie_process(movie_id):
    if not movie.check_stats(request.form):
        return redirect(f"/edit_movie/{movie_id}")
    movie.edit_movie(request.form)
    return redirect('/movie')
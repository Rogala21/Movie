from flask import render_template, redirect, request, session
from flask_app.__init__ import app
from flask_app.models.login_register import user
from flask_app.models.users import user_follow
from flask_app.models.movie import movie, movie_watched


@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('account.html', later = movie.get_all_movies_movie(), watched = movie_watched.get_all_movies_watched_account(session['user_id']), user = user.get_by_id(session['user_id']), main = session['user_id'])

@app.route('/account/<user_id>')
def user_account(user_id):
    if 'user_id' not in session:
        return redirect('/logout')
    return render_template('account.html', later = movie.get_all_movies_movie(), watched = movie_watched.get_all_movies_watched_account(user_id), user = user.get_by_id(user_id), follower = user_follow.get_all_user_followers(user_id), main = session['user_id'])

@app.route("/account/following")
def following():
    if 'user_id' not in session:
        return redirect('/logout')
    following = []
    users = user_follow.get_all_user_following(session['user_id'])
    if len(users[0].following_id) != 0:
        if len(users[0].following_id) == 1:
            lst = [users[0].following_id[0],"none"]
            ids = tuple(lst)
        else:
            ids = tuple(users[0].following_id)
        following = user_follow.get_all_following(ids)
    user = user_follow.get_by_id(session['user_id'])
    return render_template("following.html", users = users, following = following, later = movie.get_all_movies_movie(), watched = movie_watched.get_all_movies_watched(), user = user, ausers = user_follow.get_all_users())

@app.route("/account/new_following", methods=['POST'])
def new_following():
    data = {
        "follower_id": session['user_id'],
        "following_id": request.form['following_id']
    }
    user_follow.new_following(data)
    return redirect("/account/following")

@app.route("/account/un_following", methods=['POST'])
def un_following():
    data = {
        "follower_id": session['user_id'],
        "following_id": request.form['following_id']
    }
    user_follow.un_following(data)
    return redirect("/account/following")
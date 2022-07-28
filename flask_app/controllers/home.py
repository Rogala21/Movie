from flask import render_template, redirect, request, session
from flask_app.__init__ import app
from flask_app.models.login_register import user
from flask_app.models.movie import movie
import sys

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    feed = []
    feed += user.get_all_users()
    feed += movie.get_all_movies()
    selectionSort(feed, len(feed))
    return render_template('home.html', feeds = feed)

def selectionSort(array, size):
    for step in range(size):
        max_idx = step
        for i in range(step + 1, size):
            if array[i].created_at > array[max_idx].created_at:
                max_idx = i
        (array[step], array[max_idx]) = (array[max_idx], array[step])

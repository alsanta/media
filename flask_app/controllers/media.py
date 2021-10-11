from flask_app import app
from flask import render_template, redirect, session, request,flash,jsonify
from flask_app.models.movies import Movie
from flask_app.models.reviews import Review
from flask_bcrypt import Bcrypt
import os
import requests
import urllib

bcrypt = Bcrypt(app)


@app.route('/dashboard')
def index():
    if 'user_id' not in session:
        flash('Please log in to see this page.')
        return redirect('/')
    movie_list = Movie.get_all_movies()
    anime_list = Movie.get_all_animes()
    return render_template('dashboard.html', movie_list = movie_list, anime_list = anime_list)

@app.route('/movies')
def movie_index():
    if 'user_id' not in session:
        flash('Please log in to see this page.')
        return redirect('/')
    movie_list = Movie.get_all_movies()
    return render_template('movies.html', movie_list = movie_list)

@app.route('/myprofile/<int:id>')
def myprofile(id):
    if 'user_id' not in session:
        flash('Please log in to see this page.')
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    all_reviews = Review.get_all_reviews_by_userid(data)
    return render_template('myprofile.html', all_reviews = all_reviews)

@app.route('/add_movie')
def add_movie():
    if 'user_id' not in session:
        flash('Please log in to see this page.')
        return redirect('/')
    
    return render_template('add_movie.html')

@app.route('/add_movie_db')
def add_movie_db():
    if 'user_id' not in session:
        flash('Please log in to see this page.')
        return redirect('/')

    urllib.request.urlretrieve(session['poster'], f"flask_app/static/movie_imgs/{session['movie_name']}.png")
    data ={
        'name':session['movie_name'],
        'description':session['plot'],
        'poster':f"/static/movie_imgs/{session['movie_name']}.png",
        'media':session['media']
    }
    
    single_movie = Movie.add_movie(data)
    session.pop('movie_name')
    session.pop('plot')
    session.pop('poster')
    session.pop('media')

    return redirect(f'/review/{single_movie}')

@app.route('/review/<int:movie_id>')
def review(movie_id):
    if 'user_id' not in session:
        flash('Please log in to see this page.')
        return redirect('/')

    data = {
        'id': movie_id
    }
    
    single_movie = Movie.get_movie_by_id(data)
    return render_template('review.html', single_movie = single_movie, movie_id = movie_id)

@app.route('/add_review/<int:movie_id>', methods=['POST'])
def add_review(movie_id):
    if 'user_id' not in session:
        flash('Please log in to see this page.')
        return redirect('/')

    data = {
        'movie_id': movie_id,
        'user_id': session['user_id'],
        'rating': request.form['rating'],
        'reason': request.form['reason']
    }
    
    Review.add_review(data)

    return redirect('/dashboard')

@app.route('/edit/<int:user_id>/<int:movie_id>')
def edit_review(user_id, movie_id):
    data={
        'user_id': user_id,
        'movie_id': movie_id
    }

    single_review = Review.get_review_by_id(data)
    return render_template('edit.html', single_review = single_review)

@app.route('/update/<int:user_id>/<int:movie_id>', methods=['POST'])
def update_review(user_id, movie_id):
    data={
        'user_id': user_id,
        'movie_id': movie_id,
        'rating': request.form['rating'],
        'reason': request.form['reason']
    }

    Review.update_review(data)

    return redirect('/dashboard')

@app.route('/delete/<int:user_id>/<int:movie_id>')
def delete_review(user_id, movie_id):
    data={
        'user_id': user_id,
        'movie_id': movie_id,
    }

    Review.delete_review(data)

    return redirect('/dashboard')

@app.route('/view/<int:movie_id>')
def view_review(movie_id):
    data = {
        'id':movie_id
    }

    all_reviews = Review.get_all_reviews_by_movieid(data)
    print(all_reviews)
    return render_template('view.html', all_reviews = all_reviews, movie_id = movie_id)

@app.route('/search', methods=['POST'])
def search_imdb():
    type = request.form['media_type']

    if type == 'movie':

        url = f"https://imdb-internet-movie-database-unofficial.p.rapidapi.com/film/{request.form['search']}"

        headers = {
            'x-rapidapi-key': f"{os.environ.get('alt_imdb_key')}",
            'x-rapidapi-host': "imdb-internet-movie-database-unofficial.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers).json()

        session['poster'] = response['poster']
        session['movie_name'] = response['title']
        session['plot'] = response['plot']
        session['media'] = type


        check = Movie.get_movie_by_name({'name':response['title']})
        if len(check) == 0:
            return redirect ('/results')
        return redirect(f'/review/{check[0].id}')
    
    if type == 'anime':

        url = "https://jikan1.p.rapidapi.com/search/anime"

        querystring = {"q":f"{request.form['search']}"}

        headers = {
            'x-rapidapi-key': f"{os.environ.get('mal_key')}",
            'x-rapidapi-host': "jikan1.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring).json()
        
        session['poster'] = response['results'][0]['image_url']
        session['movie_name'] = response['results'][0]['title']
        session['plot'] = response['results'][0]['synopsis']
        session['media'] = type

        check = Movie.get_movie_by_name({'name':response['results'][0]['title']})
        if len(check) == 0:
            return redirect ('/results')
        return redirect(f'/review/{check[0].id}')

    return render_template('/dashboard')

@app.route('/results')
def search_results():
    return render_template('search_results.html')


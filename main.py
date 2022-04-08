from flask import Flask, jsonify, request
import csv
from demographic_filtering import output
from content_filtering import get_recommendations
all_movies = []

with open("movies.csv")as f:
    reader = csv.reader(f)
    data = list(reader)
    all_movies = data[1:]

liked_movies = []
not_liked_movies = []
did_not_watch = []

app = Flask(__name__)

@app.route("/get-movie")
def get_movie():
    return jsonify({
        "data": all_movies[0],
        "status": "success"
    })


@app.route("/liked-movie",methods = ["POST"])
def liked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    liked_movies.append(movie)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/unliked-movie",methods = ["POST"])
def unliked_movie():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    not_liked_movies.append(movie)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/did-not-watch",methods = ["POST"])
def did_not_watch():
    movie = all_movies[0]
    all_movies = all_movies[1:]
    did_not_watch.getappend(movie)
    return jsonify({
        "status": "success"
    }), 201

@app.route("/popular-movies")
def popular_movies():
    movie_data = []
    for movie in output:
        _d={
            "title":movie[0],
            "poster_link": movie[1],
            "release_date":movie[2] or "N/A",
            "duration": movie[3],
            "rating":movie[4],
            "overview": movie[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data":movie_data,
        "status":"success"
    }),200

@app.route("/recommended-movies")
def recommended_movies():
    all_recommended = []
    for liked_movie in liked_movies:
        output = get_recommendations(liked_movie[19])
        for data in output:
            all_recommended.append(data)
    import itertools
    all_recommended.sort()
    all_recommended = list(all_recommended for all_recommended,_ in itertools.groupby(all_recommended))
    movie_data = []
    for recommended in all_recommended:
        _d = {
            "title": recommended[0],
            "poster_link": recommended[1],
            "release_date": recommended[2] or "N/A",
            "duration": recommended[3],
            "rating": recommended[4],
            "overview": recommended[5]
        }
        movie_data.append(_d)
    return jsonify({
        "data": movie_data,
        "status": "success"
    }), 200


if __name__  == "__main__":
    app.run()

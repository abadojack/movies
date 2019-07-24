from flask import Flask
from flask_restplus import Resource, Api
import json
from flask_restplus import reqparse

import re

app = Flask(__name__)
api = Api(app)

data = json.load(open('data.json'))


@api.route('/movies')
class Movies(Resource):
    def get(self):
        return {"movies": data}


@api.route('/movies/<int:movie_id>')
class MoviesDetail(Resource):
    def get(self, movie_id):
        try:
            if movie_id < 1:
                return {"error": "Not found. Invalid ID"}, 404
            return data[movie_id - 1]
        except IndexError:
            return {"error": "Not found. Invalid ID"}, 404


@api.route('/search')
class MoviesSearch(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('genre')
        args = parser.parse_args()

        name = args["name"]
        genre = args["genre"]

        if not name:
            return {"error": "Include name in search parameters"}, 400
        if genre:
            if not re.match('^[a-zA-Z0-9]*$', genre):
                return {"error": "Invalid genre"}, 400
        return self.search(name, genre)

    def search(self, name, genre):
        response = []

        for item in data:
            if name.lower() in item["name"].lower():
                if genre:
                    if genre.lower() in item["genre"].lower():
                        response.append(item)
                else:
                    response.append(item)

        if not response:
            return {"error": "Movie not found"}, 404
        return response


if __name__ == '__main__':
    app.run(debug=True)

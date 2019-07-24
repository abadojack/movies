from flask import Flask
from flask_restplus import Resource, Api
import json
from flask_restplus import reqparse

app = Flask(__name__)
api = Api(app)

data = json.load(open('data.json'))


@api.route('/status')
class HelloWorld(Resource):
    def get(self):
        return {'message': 'online'}


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

        return self.search(args)

    def search(self, request_args):
        response = []
        name = request_args["name"]
        genre = request_args["genre"]

        for item in data:
            if name.lower() in item["name"].lower():
                if genre:
                    if genre.lower() in item["genre"].lower():
                        response.append(item)
                else:
                    response.append(item)

        if not response:
            return {"message": "Movie not found"}, 404
        return response


if __name__ == '__main__':
    app.run(debug=True)

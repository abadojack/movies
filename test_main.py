import unittest
import json

from main import app


class BaseTest(unittest.TestCase):
    # executed before each test
    def setUp(self):
        app.testing = True
        self.app = app
        self.client = self.app.test_client()


class MoviesTest(BaseTest):
    def test_get_movies_pass(self):
        response = self.client.get('/movies')
        res_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(res_data['movies'])


class MoviesDetailTest(BaseTest):
    def test_get_movies_details_pass(self):
        response = self.client.get('/movies/1')
        res_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(res_data['id'], 1)

    def test_get_movies_details_404_fail(self):
        response = self.client.get('/movies/1001')

        self.assertEqual(response.status_code, 404)

    def test_get_movies_details_404_0_fail(self):
        response = self.client.get('/movies/0')

        self.assertEqual(response.status_code, 404)


class SearchTest(BaseTest):
    def test_search_name_pass(self):
        response = self.client.get('/search?name=Knick Knack')
        res_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_data), 1)
        self.assertEqual(res_data[0]['name'], 'Knick Knack')

    def test_search_name_genre_pass(self):
        response = self.client.get('/search?name=story&genre=drama')
        res_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(res_data), 4)

    def test_search_no_name_fail(self):
        response = self.client.get('/search?name=')
        res_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(res_data['error'],
                         'Include name in search parameters')

    def test_search_invalid_genre_fail(self):
        response = self.client.get('/search?name=story&genre=*')
        res_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 400)
        self.assertEqual(res_data['error'],
                         'Invalid genre')

    def test_search_404_fail(self):
        response = self.client.get('/search?name=Avengers:Endgame')
        res_data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 404)
        self.assertEqual(res_data['error'],
                         'Movie not found')


if __name__ == "__main__":
    unittest.main()

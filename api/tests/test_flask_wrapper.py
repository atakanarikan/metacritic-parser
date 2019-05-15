from unittest import TestCase
from api.flask_wrapper import FlaskWrapper
from .mocks.parser_data import mock_data


class FlaskWrapperApiTest(TestCase):

    def setUp(self):
        app = FlaskWrapper(mock_data).app
        app.testing = True
        self.client = app.test_client()

    def test_retrieve_games_list(self):
        response = self.client.get('/games')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_data)

    def test_retrieve_game_when_game_exists(self):
        response = self.client.get('/games/Darkwood')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_data['Darkwood'])

    def test_retrieve_game_when_game_doesnt_exist(self):
        response = self.client.get('/games/Bloodborne')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data,
            b"Bloodborne does not exist in our records!"
        )

    def test_retrieve_game_with_url_quotes(self):
        response = self.client.get('/games/Devil%20May%20Cry%205')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, mock_data['Devil May Cry 5'])

    def test_retrieve_game_is_case_sensitive(self):
        response = self.client.get('/games/DarkWood')
        self.assertEqual(response.status_code, 404)

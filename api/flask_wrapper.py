from flask import Flask, Response, jsonify
from urllib.parse import unquote


class FlaskWrapper:

    def __init__(self, data):
        self.data = data
        self.app = Flask(__name__)
        self.app.add_url_rule(
            '/games', 'retrieve_games_list', self.retrieve_games_list
        )
        self.app.add_url_rule(
            '/games/<game_name>', 'retrieve_game', self.retrieve_game
        )

    def retrieve_games_list(self):
        return jsonify(self.data), 200

    def retrieve_game(self, game_name):
        try:
            return jsonify(self.data[unquote(game_name)])
        except KeyError:
            return Response(
                f"{unquote(game_name)} does not exist in our records!",
                404
            )

    def run(self):
        return self.app.run(host="0.0.0.0")

from parser.metacritic_html_parser import MetacriticPS4HtmlParser
from flask import Flask, Response, jsonify
from urllib.parse import unquote


class FlaskWrapper:

    def __init__(self):
        self.parser = MetacriticPS4HtmlParser()
        self.parser.parse()
        self.app = Flask(__name__)
        self.app.add_url_rule(
            '/games', 'retrieve_games_list', self.retrieve_games_list
        )
        self.app.add_url_rule(
            '/games/<game_name>', 'retrieve_game', self.retrieve_game
        )

    def retrieve_games_list(self):
        return jsonify(self.parser.top_ps4_games), 200

    def retrieve_game(self, game_name):
        try:
            return jsonify(self.parser.top_ps4_games[unquote(game_name)])
        except KeyError:
            return Response(
                f"{unquote(game_name)} does not exist in our records!",
                404
            )

    def run(self):
        return self.app.run(port=8008, debug=True)

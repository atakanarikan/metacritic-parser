import requests
import re
from uuid import uuid4
from lxml import html


class ClientSideException(Exception):
    pass


class ServerSideException(Exception):
    pass


class MetacriticPS4HtmlParser:
    def __init__(self):
        self._url = "https://www.metacritic.com/game/playstation-4"
        self._top_games = {}

    @property
    def top_ps4_games(self):
        return self._top_games

    def parse(self):
        html_string = self._get_website_content()
        top_games_list = self._get_parsed_html_string(html_string)
        self._parse_top_games_list(top_games_list)

    def _get_website_content(self):
        headers = {
            "x-instart-request-id": str(uuid4()),
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0",  # noqa
        }
        response = requests.get(self._url, headers=headers)
        if not response.ok:
            self._handle_http_error_and_reraise(response)
        return response.content

    def _get_parsed_html_string(self, response_content):
        tree = html.fromstring(response_content)
        top_games_table_content = tree.xpath(
            "//div[contains(@class, 'browse_list_wrapper')]//table//tr/td//text()"
        )
        return [
            elem.strip()
            for elem in top_games_table_content
            if self._non_empty_string(elem)
        ]

    def _non_empty_string(self, string):
        return not re.search(r"^[\n\t\s]*$", string)

    def _parse_top_games_list(self, top_games_list):
        for i in range(0, len(top_games_list), 10):
            current_game = top_games_list[i:i + 10]
            name = current_game[2]
            self._top_games[name] = {
                "metascore": current_game[0],
                "rank": current_game[1][:-1],  # remove the . at the end (1. -> 1)
                "name": current_game[2],
                "release_date": current_game[4],
                "summary": current_game[5],
                "user_score": current_game[9],
            }

    def _handle_http_error_and_reraise(self, response):
        if 400 <= response.status_code < 500:
            raise ClientSideException(response.text)
        if response.status_code >= 500:
            raise ServerSideException(response.text)

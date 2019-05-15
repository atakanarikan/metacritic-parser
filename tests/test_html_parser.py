from httmock import all_requests, HTTMock
from unittest import TestCase
from metacritic_html_parser import (
    MetacriticPS4HtmlParser,
    ServerSideException,
    ClientSideException,
)

from .mocks.response_mocks import success_response_content


@all_requests
def success_response(*args):
    return {"status_code": 200, "content": success_response_content}


@all_requests
def client_error_response(*args):
    return {"status_code": 403, "content": "Forbidden"}


@all_requests
def server_error_response(*args):
    return {"status_code": 502, "content": "Bad gateway"}


class MetacriticHtmlParserTest(TestCase):
    def setUp(self):
        self.parser = MetacriticPS4HtmlParser()

    def test_get_website_content_success(self):
        with HTTMock(success_response):
            self.parser._get_website_content()

    def test_get_website_content_client_error(self):
        with HTTMock(client_error_response):
            with self.assertRaises(ClientSideException):
                self.parser._get_website_content()

    def test_get_website_content_server_error(self):
        with HTTMock(server_error_response):
            with self.assertRaises(ServerSideException):
                self.parser._get_website_content()

    def test_get_parsed_html_string(self):
        parsed_html = self.parser._get_parsed_html_string(success_response_content)
        assert len(parsed_html) == 100
        assert parsed_html[1] == "1."
        assert parsed_html[2] == "NieR: Automata - Game of the YoRHa Edition"

    def test_parse_top_game_list(self):
        parsed_html = self.parser._get_parsed_html_string(success_response_content)
        self.parser._parse_top_games_list(parsed_html)
        assert len(self.parser.top_ps4_games) == 10
        assert "Devil May Cry 5" in self.parser.top_ps4_games
        sekiro = self.parser.top_ps4_games["Sekiro: Shadows Die Twice"]
        assert sekiro['rank'] == '2'
        assert sekiro['metascore'] == '90'
        assert sekiro['release_date'] == 'March 22, 2019'
        assert type(sekiro['summary']) == str

    def test_non_empty_string(self):
        assert self.parser._non_empty_string(" Bloodborne ")
        assert self.parser._non_empty_string("99")
        assert not self.parser._non_empty_string(" ")
        assert not self.parser._non_empty_string("  ")
        assert not self.parser._non_empty_string("\n")
        assert not self.parser._non_empty_string("\n\n\n")

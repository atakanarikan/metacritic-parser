#!/usr/bin/env python3
from api import FlaskWrapper
from parser.metacritic_html_parser import MetacriticPS4HtmlParser


parser = MetacriticPS4HtmlParser()
parser.parse()
FlaskWrapper(data=parser.top_ps4_games).run()

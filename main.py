from metacritic_html_parser import MetacriticPS4HtmlParser


class Runner:
    def main(self):
        parser = MetacriticPS4HtmlParser()
        parser.parse()
        print(parser.top_ps4_games)


Runner().main()

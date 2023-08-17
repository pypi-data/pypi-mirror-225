from html.parser import HTMLParser


# https://docs.python.org/3/library/html.parser.html#examples
class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.content = ""
        self.a_exist = False

    def handle_starttag(self, tag, attrs):
        self.a_exist = True

    def handle_data(self, data):
        self.content += " " + data

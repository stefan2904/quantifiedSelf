from HTMLParser import HTMLParser
import dateutil.parser

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "abbr":
            if attrs[0][1] == "time published":
                print dateutil.parser.parse(attrs[1][1]).replace(day=15, hour=0, minute=0, second=0, microsecond=0).strftime('%s')


parser = MyHTMLParser()
f = open('stefan2904/html/messages.html')
parser.feed(f.read())

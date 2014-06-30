from HTMLParser import HTMLParser
import dateutil.parser

class MyHTMLParser(HTMLParser):
    def __init__(self):
    	HTMLParser.__init__(self)
        self.inMeta = False

    def handle_starttag(self, tag, attrs):
    	if tag == "span":
            if attrs[0][0] == "class" and attrs[0][1] == "meta":
            	self.inMeta = True
                #

    def handle_data(self, data):
        if self.inMeta: print dateutil.parser.parse(data).replace(day=15, hour=0, minute=0, second=0, microsecond=0).strftime('%s')

    def handle_endtag(self, tag):
        if self.inMeta: 
        	self.inMeta = False

parser = MyHTMLParser()
f = open('2014-07-01_facebook-testuser/html/messages.htm')
parser.feed(f.read())

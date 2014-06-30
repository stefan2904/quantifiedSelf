# via https://gist.github.com/jehiah/745750

"""

this script parses Adium XML log files into a csv

use -u to specify your usernames to look for
use -d to specify the path (with wildcards) to adium xml logs (be careful to check all installed adium versions)

you can then read data with

import csv
reader = csv.DictReader(open('adium.csv', 'r'))
for row in reader:
    print row

"""

import glob
import os
import sys
import csv
from optparse import OptionParser
from xml.dom import minidom
import dateutil.parser
import logging
import calendar

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
   format='%(asctime)s %(process)d %(filename)s %(lineno)d %(levelname)s #| %(message)s',
   datefmt='%H:%M:%S')

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
        elif node.childNodes:
            rc.append(getText(node.childNodes))
    return ''.join(rc)

class AdiumLogParser(object):
    def __init__(self, target_year, output_filename, log_pattern, valid_usernames, readOnlyDate):
        self.onlyDate = readOnlyDate
        self.target_year = target_year
        assert isinstance(target_year, int)
        self.output_filename = output_filename
        self.valid_usernames = valid_usernames
        self.log_pattern = os.path.expanduser(log_pattern)
        logging.info('matching for year %d' % self.target_year)
        
        
    def setupOutput(self):
        logging.info('outputing data to %s' % self.output_filename)
        output_file = open(self.output_filename, 'wb')
        
        if self.onlyDate:
            headers = ['date']
        else:
            headers = ['date', 'protocol', 'msg', 'from_addr', 'to_addr', 'account']
        self.writer = csv.DictWriter(output_file, headers)
        self.writer.writerow(dict([[x,x] for x in headers]))
        
    def findFiles(self):
        files = glob.glob(self.log_pattern)
        
        for filename in files:
            yield filename
        if not files:
            print >>sys.stderr, "no files found matching %r" % self.log_pattern
    
    def parseLogFile(self, filename):
        logging.info('reading %r' % filename)
        contents = open(filename, 'rb').read()
        doc = minidom.parseString(contents)
        source_account = doc.getElementsByTagName('chat')[0].getAttribute("account")
        destination_account = filename.split('/')[-2] 
        protocol = doc.getElementsByTagName('chat')[0].getAttribute("service")
        
        for message in doc.getElementsByTagName('message'):
            message_text = getText(message.childNodes)
            
            from_addr = message.getAttribute('sender')
            if from_addr == source_account:
                to_addr = destination_account
            else:
                to_addr = source_account

            timestamp = message.getAttribute('time')
            dt = dateutil.parser.parse(timestamp)
            if self.onlyDate:
                yield {'date' : dt}
            else:
                yield {'protocol' : protocol,
                    'date' : dt,
                    'msg' : message_text,
                    'account' : source_account,
                    'from_addr' : from_addr,
                    'to_addr' : to_addr
                    }
    
    def run(self):
        self.setupOutput()
        errors = 0
        success = 0
        skipped = 0
        
        for filename in self.findFiles():
            try:
                for message in self.parseLogFile(filename):
                    if self.valid_usernames and message['account'] not in self.valid_usernames:
                        skipped += 1
                        continue
                    if not self.onlyDate and message['date'].year != self.target_year:
                        skipped += 1
                        continue
                    if not self.onlyDate: message['date'] = message['date'].strftime('%Y/%m/%d %H:%M')
                    else: message['date'] = message['date'] = message['date'].replace(day=15, hour=0, minute=0, second=0, microsecond=0).strftime('%s')
                    message = dict([[k,_utf8(v)] for k,v in message.items()])
                    self.writer.writerow(message)
                    success += 1
            except:
                logging.exception('failed parsing %r' % filename)
                errors += 1
        logging.info('output %d records skipped %d and %d failed files' % (success, skipped, errors))

def _utf8(s):
    if isinstance(s, unicode):
        s = s.encode('utf-8')
    assert isinstance(s, str), "%r is not a string" % s
    return s

def main():
    parser = OptionParser()
    parser.add_option("-d", "--log-data", dest="log_pattern", default="~/Library/Application Support/Adium*/Users/Default/Logs/*/*/*.chatlog/*.xml",
                    help="write output to FILE", metavar="FILE")
    parser.add_option("-o", "--output", dest="output_filename",
                    help="write output to FILE", metavar="FILE", default="adium.csv")
    parser.add_option("-u", "--username", dest="valid_usernames", type='str',
                    help="filter on USERNAME in adium log", metavar="USERNAME", action="append")
    parser.add_option("-y", "--year", dest="year", default=2010,
                    help="transaction year", metavar="YEAR")
    parser.add_option("-s", "--onlydate", dest="onlydate", default=True,
                    help="only the date?", metavar="ONLYDATE")

    (options, args) = parser.parse_args()
    
    adium_parse = AdiumLogParser(options.year, options.output_filename, options.log_pattern, options.valid_usernames, options.onlydate)
    adium_parse.run()

if __name__ == "__main__":
    main()

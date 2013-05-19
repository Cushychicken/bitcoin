import json
import urllib2
import sys

debug = 0

for arg in sys.argv[1:]:
    if arg == 'debug':
        debug = 1 

if debug:
    with open('ticker.ex.json', 'r') as content_file:
        content = content_file.read()
        t = json.loads(content)
else:
    url = 'https://data.mtgox.com/api/2/BTCUSD/money/ticker'
    t = json.loads(urllib2.urlopen(url).read())
    
if t['result'] == "success":
    print "Buy  : " + str(t['data']['buy']['value']) + " " + str(t['data']['buy']['currency'])
    print "Sell : " + str(t['data']['sell']['value']) + " " + str(t['data']['sell']['currency'])
    print "Last : " + str(t['data']['last']['value']) + " " + str(t['data']['last']['currency'])
    # print json.dumps(t, sort_keys=True, indent=4, separators=(',', ': '))

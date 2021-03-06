from urllib import urlencode
import urllib2
import time
from hashlib import sha512
from hmac import HMAC
import base64
import json

def getNonce():
    return int(time.time() * 100000)

def signData(secret, data):
    return base64.b64encode(str(HMAC(secret, data, sha512).digest()))

class Monitor:
    def __init__(self, auth_key, auth_secret):
        self.auth_key = auth_key
        self.auth_secret = base64.b64decode(auth_secret)

    def buildQuery(self, req={}):
        req = {'nonce': getNonce()}
        postData = urlencode(req)
        headers = {}
        headers["User-Agent"] = "GoxApi"
        headers["Rest-Key"] = self.auth_key
        headers["Rest-Sign"] = signData(self.auth_secret, postData)
        return (postData, headers)

    def perform(self, path, args):
        data, headers = self.buildQuery(args)
        req = urllib2.Request("https://data.mtgox.com/api/0/"+path, data, headers)
        res = urllib2.urlopen(req, data)
        return json.load(res)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print "Feed me an API key. Exiting..."
        exit
    m = Monitor(sys.argv[1], sys.argv[2])
    t = m.perform("getFunds.php", [])
    print json.dumps(t, sort_keys=True, indent=4, separators=(',', ': '))

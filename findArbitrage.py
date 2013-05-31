import json
import urllib2
from itertools import permutations
import sys
import operator

# Flag for example string vs API call
get = 0
for i in sys.argv[1:]:
    if i == '-go':
        get = 1

convert  = {} # Conversion rate from (first key) to (second key)
arbitrage = {} # Hash of arbitrage opportunities, keyed by transfer sequence

# Uses local copy of API call to avoid abuse
j = ''
if get:
    url = 'http://fx.priceonomics.com/v1/rates/'
    data = urllib2.urlopen(url).read()
    j = json.loads(data)
else:
    f = open('index.html')
    j = json.loads(f.read())

# Sanitize to float, organize by conversion
for x in j.keys():
    fields = x.split('_')
    if convert.has_key(fields[0]):
        convert[fields[0]][fields[1]] = float(j[x])
    else:
        convert[fields[0]] = {}
        convert[fields[0]][fields[1]] = float(j[x])


# Develops lists of permutations 
p = permutations(convert.keys())
p = list(list(p) + list(permutations(convert.keys(), 3)))

for i in p:
    i = i + (i[0],) # Adds initial value to end to complete transfer cycle
    last_key = ''
    last_val = 0
    # Cycles through list to calculate final value of transfers 
    for r in i:
        if r == i[0] and not last_key:
            last_key = r
            last_val = 1
            continue
        else:
           last_val = convert[last_key][r] * last_val
           last_key = r

    # If final value is greater than initial, it's arbitrage!
    if last_val > 1:
        arbitrage[i] = last_val

# Gets sorted arbitrage values and prints
sorted_arb = sorted(arbitrage.iteritems(), key=operator.itemgetter(1))
print "Best Arbitrage Sequence"
sorted_arb.reverse()
for i in sorted_arb:
    print i



import urllib2
import re
from bs4 import BeautifulSoup
import unicodedata

curr = re.compile('bitcoinexchangerate\.org/c/(\S+)')
val  = re.compile('\s+\D*(\d+\.\d+)\s+(\S+)', re.UNICODE)
exch = re.compile('href=\"/graph/\?from=USD\&amp;to=(\S+)\"\>(\S+)\<\/a\>')
country = []

exchange = dict() # Dict to hold the exchange rate of a dollar to a foreign currency
bitcoin  = dict() # Dict to hold the sell prices of a bitcoin to a foreign currency

url = 'http://bitcoinexchangerate.org'

soup = BeautifulSoup(urllib2.urlopen(url).read())

# Gets all the countries that have bitcoin values
values = soup.find_all('a')
for link in values:
    p = curr.search(link.get('href'))
    if p:
        country.append(p.group(1))

# Gets the value for a bitcoin for each country
for nat in country:
    url = 'http://bitcoinexchangerate.org/c/' + nat
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    for div in soup.b:
        # Parses thru each page; prints bitcoin value if found
        p = val.search(div)
        if p:
            temp = p.group(1)
            if type(temp) == 'unicode':
                temp = unicodedata.normalize('NFKD', temp).encode('ascii')
            bitcoin[p.group(2)] = temp

# Gets the dollar to each country's exchange rate
url = 'http://www.x-rates.com/table/?from=USD&amount=1'
soup = BeautifulSoup(urllib2.urlopen(url).read())
values = soup.find_all("td", class_='rtRates')

for value in values:
    if exch.search(str(value)):
        if exch.search(str(value)).group(1) in country:
            exchange[exch.search(str(value)).group(1)] = exch.search(str(value)).group(2)

rates = exchange.keys()
str(rates)
rates.sort()
print 'Cntry\tExchangeUSA\tBitcoin Rate\tBitcoinPP(USD)\tUSDPP\tBuy?'

for cntry in rates:
    if cntry in bitcoin.keys():
        power = (float(bitcoin[cntry]))/float(exchange[cntry])
        print cntry + '\t' + str(exchange[cntry]) + '\t' + str(bitcoin[cntry]) + '\t' + str(power) + '\t' + str(bitcoin['USD']) + "\t" + str(power > float(bitcoin['USD']))

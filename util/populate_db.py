import sqlalchemy as sa
import thursdays.model as model
import thursdays.model.meta as meta
from dateutil.parser import *
import urllib, re

DB_URL = "sqlite:///development.db"

engine = sa.create_engine(DB_URL)
model.init_model(engine)

opener = urllib.FancyURLopener({})

f = open('parsedoutput.txt', 'r')
line = f.readline()
while len(line) > 0:
    assert line.find('######') >= 0
    print line
    date_str = f.readline()
    date = parse(date_str)
    url = f.readline()
    print url

    page = opener.open(url)
    html = page.read()

    name = re.search('<h1.*>(.*)</h1>', html).group(1)
    addr = re.search('<span class="street-address">(.*?)</span>', html).group(1)

    print "adding " + name + " at " + addr + " on " + str(date)

    v = model.Venue()
    v.name = name
    v.address = addr
    v.date = date
    meta.Session.add(v)

    line = f.readline()
print "\n\n.... committing"
meta.Session.commit()

import getpass, imaplib
import email, re

m = imaplib.IMAP4_SSL('imap.gmail.com', 993)
m.login('christineyen@gmail.com', 'pank/ac3s')
m.select('thursdays')
typ, data = m.search(None, '(FROM "christineyen")', '(SUBJECT "thursday!")')

list_nums = data[0].split()

for num in list_nums:
    print "\n########################"
    typ, data = m.fetch(num, '(RFC822)')
    message = email.message_from_string(data[0][1])
    if type(message.get_payload()) is list:
        msg_text = str(message.get_payload(0))
    else:
        msg_text = message.get_payload()

    yelp = re.search('http://.*yelp.*(?=\s)', msg_text)
    print message['date']
    if yelp:
        print re.findall('On \w+, \w+ \d+, \d+ at \d+:\d+ .M', msg_text)
        print yelp.group(0)
    else:
        print msg_text

m.close()
m.logout()


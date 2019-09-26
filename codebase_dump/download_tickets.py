import os
import requests
import xml.etree.ElementTree as ET


USER = os.environ['CODEBASE_USER']
PASSWORD = os.environ['CODEBASE_PASSWORD']

session = requests.sessions.Session()
session.auth = (USER, PASSWORD)
session.headers['Accept'] = 'application/xml'

page = 1
while True:
    r = session.get('https://api3.codebasehq.com/chroma/tickets/', params={'page': page})
    r.raise_for_status()
    root = ET.fromstring(r.text)
    for c in root:
        ticket_id = c.find('ticket-id').text
        print(page, ticket_id)
        with open(f'tickets/{ticket_id}.xml', 'wb') as f:
            f.write(ET.tostring(c))
    page += 1


import sys
import os
import requests
import xml.etree.ElementTree as ET
from pathlib import Path


USER = os.environ['CODEBASE_USER']
PASSWORD = os.environ['CODEBASE_PASSWORD']

session = requests.sessions.Session()
session.auth = (USER, PASSWORD)
session.headers['Accept'] = 'application/xml'

project = sys.argv[1]

path = Path(__file__).parent / Path(project) / 'tickets'
path.mkdir(exist_ok=True, parents=True)

page = 1
while True:
    r = session.get(f'https://api3.codebasehq.com/{project}/tickets/', params={'page': page})
    if r.status_code == 404:
        break
    r.raise_for_status()
    root = ET.fromstring(r.text)
    for c in root:
        ticket_id = c.find('ticket-id').text
        print(page, ticket_id)
        with open(path / f'{ticket_id}.xml', 'wb') as f:
            f.write(ET.tostring(c))
    page += 1


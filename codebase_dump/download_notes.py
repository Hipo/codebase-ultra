import os
import time
import requests
from pathlib import Path


USER = os.environ['CODEBASE_USER']
PASSWORD = os.environ['CODEBASE_PASSWORD']

session = requests.sessions.Session()
session.auth = (USER, PASSWORD)
session.headers['Accept'] = 'application/xml'

note_ticket_ids = set(s.name.split('.')[0] for s in Path('notes').glob('*.xml'))

ticket_ids = [s.name.split('.')[0] for s in Path('tickets').glob('*.xml')]
ticket_ids = [ticket_id for ticket_id in ticket_ids if ticket_id not in note_ticket_ids]
ticket_ids = sorted(ticket_ids, key=int, reverse=True)

for ticket_id in ticket_ids:
    r = session.get(f'https://api3.codebasehq.com/chroma/tickets/{ticket_id}/notes')
    r.raise_for_status()
    print(ticket_id)
    with open(f'notes/{ticket_id}.xml', 'w') as f:
        f.write(r.text)
    time.sleep(0.2)


import sys
import os
import time
import requests
from pathlib import Path


USER = os.environ['CODEBASE_USER']
PASSWORD = os.environ['CODEBASE_PASSWORD']

session = requests.sessions.Session()
session.auth = (USER, PASSWORD)
session.headers['Accept'] = 'application/xml'

project = sys.argv[1]

project_path = Path(__file__).parent / Path(project)

tickets_path = project_path / 'tickets'
notes_path = project_path / 'notes'
notes_path.mkdir(exist_ok=True, parents=True)


note_ticket_ids = set(s.name.split('.')[0] for s in notes_path.glob('*.xml'))

ticket_ids = [s.name.split('.')[0] for s in tickets_path.glob('*.xml')]
ticket_ids = [ticket_id for ticket_id in ticket_ids if ticket_id not in note_ticket_ids]
ticket_ids = sorted(ticket_ids, key=int, reverse=True)

for ticket_id in ticket_ids:
    r = session.get(f'https://api3.codebasehq.com/{project}/tickets/{ticket_id}/notes')
    r.raise_for_status()
    print(ticket_id)
    with open(notes_path / f'{ticket_id}.xml', 'w') as f:
        f.write(r.text)
    time.sleep(0.2)


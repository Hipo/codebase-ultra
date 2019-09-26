import os
import json
import requests
import xml.etree.ElementTree as ET


USER = os.environ['CODEBASE_USER']
PASSWORD = os.environ['CODEBASE_PASSWORD']

session = requests.sessions.Session()
session.auth = (USER, PASSWORD)
session.headers['Accept'] = 'application/xml'


def activity_stream(since=None):
    page = 1
    while True:
        r = session.get('https://api3.codebasehq.com/chroma/activity?raw=true', params={'page': page, 'since': since})
        r.raise_for_status()
        root = ET.fromstring(r.text)
        if not len(root):
            break
        for c in root:
            yield c
        page += 1


def get_ticket(ticket_id):
    r = session.get(f'https://api3.codebasehq.com/chroma/tickets/{ticket_id}')
    r.raise_for_status()
    root = ET.fromstring(r.text)
    return root


def get_ticket_notes(ticket_id):
    r = session.get(f'https://api3.codebasehq.com/chroma/tickets/{ticket_id}/notes')
    r.raise_for_status()
    root = ET.fromstring(r.text)
    return list(root)

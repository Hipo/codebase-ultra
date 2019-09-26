import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError

from ticketbase.codebase.models import Ticket, TicketNote, Project


class Command(BaseCommand):
    help = 'Load data'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str)

    def handle(self, *args, **options):
        path = Path(options['directory'])

        files = (path / 'tickets').glob('*.xml')

        project, _ = Project.objects.get_or_create(project_id=53230, name='chroma')

        n = 0
        for filename in files:
            ticket_id = int(filename.name.split('.xml')[0])
            with open(filename) as f:
                xml = f.read()
            root = ET.fromstring(xml)
            ticket, _ = Ticket.objects.get_or_create(project=project, ticket_id=ticket_id)
            ticket.update_from_xml(xml)
            ticket.save()

            notes_filename = path / 'notes' / f'{ticket_id}.xml'
            if notes_filename.exists():
                with open(notes_filename) as f:
                    notes_xml = f.read()
                root = ET.fromstring(notes_xml)
                for c in root:
                    xml = ET.tostring(c).decode()
                    note_id = c.find('id').text
                    note, _ = TicketNote.objects.get_or_create(ticket=ticket, note_id=note_id)
                    note.update_from_xml(xml)
                    note.save()
            n += 1
            print(n, ticket_id)


        self.stdout.write(self.style.SUCCESS(f'Imported {n} tickets'))

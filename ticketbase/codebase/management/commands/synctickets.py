import os
import xml.etree.ElementTree as ET
from pathlib import Path
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError

from ticketbase.codebase.models import Ticket, TicketNote


class Command(BaseCommand):
    help = 'Load data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        tickets = Ticket.objects.filter(needs_update=True)
        for ticket in tickets:
            print(ticket.ticket_id)
            update_ticket(ticket)



def update_ticket(ticket):
    ticket_id = ticket.ticket_id
    ticket_node = api.get_ticket(ticket_id)
    ticket.xml = ET.tostring(ticket_node)
    ticket.updated_at = ticket_node.find('updated-at').text
    ticket.needs_update = False
    ticket.save()

    ticket_note_nodes = api.get_ticket_notes(ticket_id)
    for c in ticket_note_nodes:
        xml = ET.tostring(c)
        note_id = c.find('id').text
        note, _ = TicketNote.objects.get_or_create(ticket=ticket, note_id=note_id)
        note.xml = xml
        note.updated_at = c.find('updated-at').text
        note.needs_update = False
        note.save()

import os
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError

from ticketbase.codebase.models import Ticket, TicketNote


class Command(BaseCommand):
    help = 'Load data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        tickets = Ticket.objects.all()
        for ticket in tickets:
            ticket.update_from_xml(ticket.xml)
            ticket.save()
            for note in ticket.ticketnote_set.all():
                try:
                    note.update_from_xml(note.xml)
                    note.save()
                except Exception as e:
                    print(ticket.ticket_id, note.note_id)
                    print(note.xml)

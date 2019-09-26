import os
import json
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from dateutil.parser import parse
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError

from . import api
from ticketbase.codebase.models import Ticket, TicketNote


class Command(BaseCommand):
    help = 'Load data'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        since = str(Ticket.objects.latest('updated_at').updated_at)
        for c in api.activity_stream(since):
            event_type = c.find('type').text
            if event_type in ('ticketing_note', 'ticketing_ticket'):
                timestamp = c.find('timestamp').text
                title = c.find('title').text
                properties = c.find('raw-properties')
                ticket_id = int(properties.find('number').text)
                # subject = properties.find('subject').text
                print(timestamp, ticket_id, title)
                ticket, _ = Ticket.objects.get_or_create(ticket_id=ticket_id)
                ticket.needs_update = True
                ticket.updated_at = parse(timestamp)
                ticket.save()
            else:
                pass

import os
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from django.core.files.images import ImageFile
from django.core.management.base import BaseCommand, CommandError

from ticketbase.codebase.models import Ticket, TicketNote, Project
from ticketbase.codebase import api
from ticketbase.users.models import User


class Command(BaseCommand):
    help = 'Fetch users from codebase'

    def add_arguments(self, parser):
        parser.add_argument('project_name', type=str)

    def handle(self, *args, **options):
        n = 0
        project = Project.objects.get(name=options['project_name'])
        user_nodes = api.get_users(options['project_name'])
        for node in user_nodes:
            username = node.find('username').text
            user, _ = User.objects.get_or_create(username=username, defaults=dict(
                first_name=node.find('first-name').text,
                last_name=node.find('last-name').text,
                codebase_id=int(node.find('id').text),
                email=node.find('email-address').text,
                company=node.find('company').text,
                is_active=False,
            ))
            user.projects.add(project)
            n += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {n} users'))

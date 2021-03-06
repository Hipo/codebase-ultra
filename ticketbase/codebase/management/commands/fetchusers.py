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
        project_node = api.get_project(options['project_name'])
        project_id = project_node.find('project-id').text
        project_name = project_node.find('name').text
        project, _ = Project.objects.get_or_create(project_id=project_id, slug=options['project_name'], name=project_name)
        project = Project.objects.get(slug=options['project_name'])
        user_nodes = api.get_users(options['project_name'])
        for node in user_nodes:
            print(project)
            username = node.find('username').text
            user, _ = User.objects.get_or_create(username=username, defaults=dict(
                first_name=node.find('first-name').text,
                last_name=node.find('last-name').text,
                codebase_id=int(node.find('id').text),
                email=node.find('email-address').text,
                company=node.find('company').text,
                is_active=False,
            ))

            if user.projects:
                user.projects.add(project)
            else:
                user.projects = [project]

            user.save()
            n += 1

        self.stdout.write(self.style.SUCCESS(f'Imported {n} users'))

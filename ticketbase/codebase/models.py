from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField

import xml.etree.ElementTree as ET


class Project(models.Model):
    project_id = models.IntegerField(primary_key=True)
    name = models.TextField(null=True, blank=True)


class Ticket(models.Model):
    ticket_id = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    xml = models.TextField(null=True, blank=True)
    needs_update = models.BooleanField(default=False)
    updated_at = models.DateTimeField(null=True, default=timezone.now)
    created_at = models.DateTimeField(null=True, default=timezone.now)
    summary = models.TextField(null=True, blank=True)
    reporter_id = models.IntegerField(null=True)
    assignee_id = models.IntegerField(null=True)

    class Meta:
        unique_together = ['ticket_id', 'project']

    def update_from_xml(self, xml):
        node = ET.fromstring(xml)
        self.xml = xml
        self.updated_at = node.find('updated-at').text
        self.ceated_at = node.find('created-at').text
        self.summary = node.find('summary').text
        self.reporter_id = node.find('reporter-id').text
        self.assignee_id = node.find('assignee-id').text


class TicketNote(models.Model):
    note_id = models.IntegerField(primary_key=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
    xml = models.TextField(null=True, blank=True)
    needs_update = models.BooleanField(default=False)
    updated_at = models.DateTimeField(null=True, default=timezone.now)
    content = models.TextField(null=True, blank=True)
    user_id = models.IntegerField(null=True)
    updates = JSONField(null=True, blank=True)

    class Meta:
        ordering = ['note_id']

    def update_from_xml(self, xml):
        node = ET.fromstring(xml)
        self.xml = xml
        self.updated_at = node.find('updated-at').text
        self.ceated_at = node.find('created-at').text
        self.content = node.find('content').text
        self.user_id = node.find('user-id').text
        self.updates = node.find('updates').text

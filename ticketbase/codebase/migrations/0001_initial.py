# Generated by Django 2.2.4 on 2019-09-22 06:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('project_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.IntegerField()),
                ('xml', models.TextField(blank=True, null=True)),
                ('needs_update', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('summary', models.TextField(blank=True, null=True)),
                ('reporter_id', models.IntegerField(null=True)),
                ('assignee_id', models.IntegerField(null=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='codebase.Project')),
            ],
            options={
                'unique_together': {('ticket_id', 'project')},
            },
        ),
        migrations.CreateModel(
            name='TicketNote',
            fields=[
                ('note_id', models.IntegerField(primary_key=True, serialize=False)),
                ('xml', models.TextField(blank=True, null=True)),
                ('needs_update', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('user_id', models.IntegerField(null=True)),
                ('updates', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('ticket', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='codebase.Ticket')),
            ],
            options={
                'ordering': ['note_id'],
            },
        ),
    ]

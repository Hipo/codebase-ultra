# Generated by Django 2.2.4 on 2019-09-27 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codebase', '0005_ticket_is_closed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='category',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='milestone',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_type',
            field=models.TextField(null=True),
        ),
    ]

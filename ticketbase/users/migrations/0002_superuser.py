import os
from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial')
    ] 

    def generate_superuser(apps, schema_editor):
        # NB. This DOESN'T WORK if the user models gets changed later :()

        # from django.contrib.auth import get_user_model
        # User = get_user_model()

        # DJANGO_SU_NAME = 'admin'
        # DJANGO_SU_EMAIL = 'admin@example.com'
        # DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD')

        # superuser = User.objects.create_superuser(
        #     username=DJANGO_SU_NAME,
        #     email=DJANGO_SU_EMAIL,
        #     password=DJANGO_SU_PASSWORD)

        # superuser.save()
        pass

    operations = [
        migrations.RunPython(generate_superuser),
    ]
# Generated by Django 5.1.2 on 2024-11-07 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file_api', '0003_alter_filedata_status_alter_filedata_uploaded_at'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Conditions',
        ),
    ]

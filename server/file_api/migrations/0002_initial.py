# Generated by Django 5.1.2 on 2024-11-07 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('file_api', '0001_initial'),
        ('user_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='filedata',
            name='client_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.clients'),
        ),
        migrations.AddField(
            model_name='filedata',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_api.projects'),
        ),
    ]

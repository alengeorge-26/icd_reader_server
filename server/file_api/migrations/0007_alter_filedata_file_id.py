# Generated by Django 5.1.2 on 2024-11-07 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_api', '0006_alter_uploadedfile_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedata',
            name='file_id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
    ]

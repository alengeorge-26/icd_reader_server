# Generated by Django 5.1.2 on 2024-11-07 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file_api', '0008_alter_fileconditions_file_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedata',
            name='input_path',
            field=models.CharField(default=None, max_length=500),
        ),
        migrations.AlterField(
            model_name='filedata',
            name='output_path',
            field=models.CharField(default=None, max_length=500, null=True),
        ),
    ]

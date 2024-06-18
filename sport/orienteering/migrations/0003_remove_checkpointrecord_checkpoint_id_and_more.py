# Generated by Django 5.0.6 on 2024-06-18 15:28

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orienteering', '0002_alter_grouprunner_members'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checkpointrecord',
            name='checkpoint_id',
        ),
        migrations.AddField(
            model_name='checkpointrecord',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
    ]

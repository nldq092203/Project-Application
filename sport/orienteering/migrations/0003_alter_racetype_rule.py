# Generated by Django 5.0.6 on 2024-06-17 23:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orienteering', '0002_checkpoint_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racetype',
            name='rule',
            field=models.TextField(blank=True, null=True),
        ),
    ]
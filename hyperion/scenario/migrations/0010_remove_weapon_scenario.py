# Generated by Django 3.0.8 on 2020-07-30 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scenario', '0009_warhead_target_display_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='weapon',
            name='scenario',
        ),
    ]
# Generated by Django 5.0.1 on 2024-02-12 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guest',
            name='assigned_table',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='assigned_table_seat',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='attending_ceremony_rehearsal',
        ),
        migrations.RemoveField(
            model_name='guest',
            name='rehearsal_rsvp_answer',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='invited_to_rehearsal',
        ),
    ]

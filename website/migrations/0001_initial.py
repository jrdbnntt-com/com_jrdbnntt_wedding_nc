# Generated by Django 5.0 on 2024-01-01 02:42

import django.db.models.deletion
import django.utils.timezone
import website.models.mail.template
import website.models.reservation
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSubscriptionGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sendgrid_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('kwargs', models.CharField(max_length=1000)),
                ('target_unix_time', models.BigIntegerField()),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('from_email', models.CharField(default=website.models.mail.template.default_from_email, max_length=200)),
                ('sendgrid_template_id', models.CharField(max_length=200)),
                ('sendgrid_subscription_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.emailsubscriptiongroup')),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('access_code', models.CharField(default=website.models.reservation.generate_access_code, max_length=6, unique=True)),
                ('activated', models.BooleanField(default=False)),
                ('activated_at', models.DateTimeField(blank=True, null=True)),
                ('max_guests', models.IntegerField(default=2)),
                ('rsvp_updated_at', models.DateTimeField(blank=True, null=True)),
                ('mailing_address_line_1', models.CharField(blank=True, max_length=200)),
                ('mailing_address_line_2', models.CharField(blank=True, max_length=200)),
                ('mailing_address_city', models.CharField(blank=True, max_length=200)),
                ('mailing_address_state', models.CharField(blank=True, max_length=5)),
                ('mailing_address_zip', models.CharField(blank=True, max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('invited_to_rehearsal', models.BooleanField(default=False)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('rsvp_answer', models.BooleanField(blank=True, default=None, null=True)),
                ('rehearsal_rsvp_answer', models.BooleanField(blank=True, default=None, null=True)),
                ('food_vegan_option', models.BooleanField(blank=True, default=False, null=True)),
                ('assigned_table', models.IntegerField(blank=True, null=True)),
                ('assigned_table_seat', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('attending_ceremony_rehearsal', models.BooleanField(default=False)),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.reservation')),
            ],
        ),
    ]

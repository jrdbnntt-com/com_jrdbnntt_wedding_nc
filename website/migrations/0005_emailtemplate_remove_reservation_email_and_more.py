# Generated by Django 4.0.1 on 2022-03-06 00:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import website.models.reservation


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0004_auto_20220110_2322'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('sendgrid_template_id', models.CharField(max_length=200)),
                ('from_email', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='email',
        ),
        migrations.AddField(
            model_name='reservation',
            name='name',
            field=models.CharField(default='test', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='access_code',
            field=models.CharField(default=website.models.reservation.generate_access_code, max_length=6, unique=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-20 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0036_submission_dead_line'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='dead_line',
        ),
    ]

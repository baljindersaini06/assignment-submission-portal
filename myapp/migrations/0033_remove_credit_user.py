# Generated by Django 2.2.5 on 2019-09-18 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0032_auto_20190918_1219'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credit',
            name='user',
        ),
    ]

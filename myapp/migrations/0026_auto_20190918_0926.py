# Generated by Django 2.2.5 on 2019-09-18 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0025_auto_20190918_0923'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ('sent_time',)},
        ),
        migrations.AlterOrderWithRespectTo(
            name='message',
            order_with_respect_to=None,
        ),
    ]

# Generated by Django 2.2.5 on 2019-09-20 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0035_remove_credit_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='dead_line',
            field=models.ForeignKey(blank=True, null=True, on_delete=True, related_name='dead_line', to='myapp.Assignment'),
        ),
    ]

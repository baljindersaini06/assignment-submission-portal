# Generated by Django 2.2.5 on 2019-09-12 10:07

from django.db import migrations, models
import myapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_auto_20190912_0929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='document',
            field=models.FileField(blank=True, upload_to='documents/', validators=[myapp.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='submission',
            name='title',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]

# Generated by Django 2.2.6 on 2019-10-23 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kulecnik', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
# Generated by Django 2.2.5 on 2019-10-24 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kulecnik', '0007_auto_20191024_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament_t',
            name='place',
            field=models.CharField(blank=True, max_length=60, null=True),
        ),
    ]

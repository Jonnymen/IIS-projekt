# Generated by Django 2.2.6 on 2019-10-23 13:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Kulecnik', '0004_team_captain'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game_S',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('phase', models.CharField(max_length=40)),
                ('player_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_1_s', to=settings.AUTH_USER_MODEL)),
                ('player_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_2_s', to=settings.AUTH_USER_MODEL)),
                ('referee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referee_s', to=settings.AUTH_USER_MODEL)),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Kulecnik.Table')),
            ],
        ),
        migrations.CreateModel(
            name='Game_T',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('phase', models.CharField(max_length=40)),
                ('player_1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_1_t', to=settings.AUTH_USER_MODEL)),
                ('player_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_2_t', to=settings.AUTH_USER_MODEL)),
                ('referee', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='referee_t', to=settings.AUTH_USER_MODEL)),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Kulecnik.Table')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament_S',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('entry_fee', models.IntegerField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('reg_deadline', models.DateTimeField(blank=True, null=True)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament_T',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('entry_fee', models.IntegerField(blank=True, null=True)),
                ('place', models.TextField(blank=True, null=True)),
                ('capacity', models.IntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('reg_deadline', models.DateTimeField(blank=True, null=True)),
                ('host', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='player',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='captain',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='captain', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Player',
        ),
        migrations.AddField(
            model_name='game_t',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Kulecnik.Tournament_T'),
        ),
        migrations.AddField(
            model_name='game_t',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner_t', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='game_s',
            name='tournament',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Kulecnik.Tournament_S'),
        ),
        migrations.AddField(
            model_name='game_s',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='winner_s', to=settings.AUTH_USER_MODEL),
        ),
    ]

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=30)

class Team(models.Model):
    name = models.CharField(max_length=20)
    logo = models.FileField(blank=True, null=True)
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="captain")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="player")

class Tournament_S(models.Model):
    title = models.CharField(max_length=60)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    entry_fee = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=60, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reg_deadline = models.DateTimeField(blank=True, null=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

class Tournament_T(models.Model):
    title = models.CharField(max_length=60)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    entry_fee = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=60, blank=True, null=True)
    capacity = models.IntegerField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    reg_deadline = models.DateTimeField(blank=True, null=True)
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

class Game_S(models.Model):
    start_time = models.DateTimeField()
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="player_1")
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="player_2")
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="referee_s")
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="winner_s")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament_S, on_delete=models.CASCADE, null=True)
    phase = models.CharField(max_length=40)

class Game_T(models.Model):
    start_time = models.DateTimeField()
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="team_1")
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="team_2")
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="referee_t")
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="winner_t")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament_T, on_delete=models.CASCADE, null=True)
    phase = models.CharField(max_length=40)


class Tournament_Players(models.Model):
    tournament = models.ForeignKey(Tournament_S, on_delete=models.CASCADE)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tourney_player")

class Tournament_Teams(models.Model):
    tournament = models.ForeignKey(Tournament_T, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tourney_team")

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='avatars', null=True)

    def __str__(self):
        return self.user.username

from datetime import date
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.
class Table(models.Model):
    name = models.CharField(max_length=30)

class Team(models.Model):
    name = models.CharField(max_length=20)
    logo = models.ImageField(default='default.png', upload_to='avatars/teams')
    captain = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="captain")
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="player")

class Tournament_S(models.Model):
    title = models.CharField(max_length=60)
    start_date = models.DateField()
    end_date = models.DateField()
    entry_fee = models.IntegerField(blank=True, null=True)
    place = models.CharField(max_length=60, blank=True, null=True)
    capacity = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    reg_deadline = models.DateTimeField()
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    @property
    def is_past_start(self):
        return date.today() > self.start_date

    @property
    def is_past_reg(self):
        return timezone.now() > self.reg_deadline

    @property
    def is_past_end(self):
        return date.today() > self.end_date

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
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    @property
    def is_past_start(self):
        return date.today() > self.start_date

    @property
    def is_past_reg(self):
        return timezone.now() > self.reg_deadline

    @property
    def is_past_end(self):
        return date.today() > self.end_date

class Game_S(models.Model):
    player_1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="player_1")
    player_2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="player_2")
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="referee_s")
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="winner_s")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament_S, on_delete=models.CASCADE)
    stage = models.IntegerField(blank=True, null=True)
    next_game = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

class Game_T(models.Model):
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="team_1")
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="team_2")
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name="referee_t")
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name="winner_t")
    table = models.ForeignKey(Table, on_delete=models.CASCADE, null=True)
    tournament = models.ForeignKey(Tournament_T, on_delete=models.CASCADE)
    stage = models.IntegerField(blank=True, null=True)
    next_game = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)

class Tournament_Players(models.Model):
    tournament = models.ForeignKey(Tournament_S, on_delete=models.CASCADE)
    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tourney_player")
    registered = models.NullBooleanField(default=None)

class Tournament_Teams(models.Model):
    tournament = models.ForeignKey(Tournament_T, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="tourney_team")
    registered = models.NullBooleanField(default=None)

class Tournament_S_referees(models.Model):
    tournament = models.ForeignKey(Tournament_S, on_delete=models.CASCADE)
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referee_ss")
    registered = models.NullBooleanField(default=None)

class Tournament_T_referees(models.Model):
    tournament = models.ForeignKey(Tournament_T, on_delete=models.CASCADE)
    referee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referee_tt")
    registered = models.NullBooleanField(default=None)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='avatars')

    def __str__(self):
        return self.user.username

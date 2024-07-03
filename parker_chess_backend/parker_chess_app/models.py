from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    elo = models.FloatField(default=1000)
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f"ID {self.id} :: {self.username} : {self.elo}"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=25)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)
    date_time_played = models.DateTimeField(auto_now_add=True)

    def get_profile_info(self):
        """ Returns a dict of profile info """
        return {
            'user_id': self.user.id,
            'elo': self.user.elo,
            'profile_name': self.profile_name,
            'bio': self.bio,
            'profile_picture' : self.profile_picture
        }

    def __str__(self):
        return f"{self.user.username}'s - Profile"


class Game(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    white_player = models.ForeignKey(CustomUser, related_name='white', on_delete=models.SET_NULL)
    black_player = models.ForeignKey(CustomUser, related_name='black', on_delete=models.SET_NULL)
    white_player_elo = models.IntegerField(default=None)
    black_player_elo = models.IntegerField(default=None)
    game_winner = models.ForeignKey(CustomUser, related_name='wins', on_delete=models.SET_NULL, null=True, blank=True)
    game_color_winner = models.TextField()
    date_time_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Game ID {self.id} - {self.white_player.username} vs {self.black_player.username}'
    
    def get_game(self):
        return {
            'id' : self.id,
            'white_player' : self.white_player,
            'black_player' : self.black_player,
            'white_player_elo' : self.white_player_elo,
            'black_player_elo' : self.black_player_elo,
            'game_winner' : self.game_winner,
            'game_color_winner' : self.game_color_winner,
            'date_time_played' : self.date_time_played,
        }


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    move_id = models.IntegerField()
    move = models.CharField(max_length=6) # formatted like 'A1A2' or 'A1O-O-O' or 'A7A8=Q'
    mover = models.ForeignKey(CustomUser, related_name='white_games', on_delete=models.SET_NULL)
    piece = models.CharField(max_length=1)
    fen_string = models.CharField(max_length=90)
    date_time_move_played = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('game', 'move_id')

    def __str__(self):
        return f'Move {self.move_id} in Game {self.game.id}'


class Following(models.Model):
    main_account = models.ForeignKey(CustomUser, related_name='follower', on_delete=models.CASCADE)
    account_following = models.ForeignKey(CustomUser, related_name='followee', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('main_account', 'following')

    def get_friend(self):
        return {
            'main_account' : self.main_account,
            'following' : self.account_following,
            'date_time' : self.date_time,
        }

    def __str__(self):
        return f'{self.main_account.username} is following {self.account_following.username}'

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    urgency = models.IntegerField(default=0) # 0, 1, 2
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} at {self.timestamp} : {self.message}'

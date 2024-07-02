from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):
    elo = models.FloatField(default=1000)
    id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f"{self.username}'s - Account"
    
    def get_rounded_elo(self):
        """ Returns Elo rounded down, use for display """
        return int(self.elo)


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=25)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics', blank=True)

    def get_profile_info(self):
        """ Returns a dict of profile info """
        return {
            'user_id': self.user.id,
            'elo': self.user.elo,
            'name': self.profile_name,
            'bio': self.bio,
            'image' : self.profile_picture
        }

    def __str__(self):
        return f"{self.user.username}'s - Profile"


class Game(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    white_player = models.ForeignKey(CustomUser, related_name='white_games', on_delete=models.CASCADE)
    black_player = models.ForeignKey(CustomUser, related_name='black_games', on_delete=models.CASCADE)
    game_winner = models.ForeignKey(CustomUser, related_name='wins', on_delete=models.CASCADE, null=True, blank=True)
    date_time_played = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Game ID {self.id} - {self.white_player.username} vs {self.black_player.username}'


class Move(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    move_id = models.IntegerField()
    move = models.CharField(max_length=6)
    fen_string = models.CharField(max_length=90)
    date_time_moved = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('game', 'move_id')

    def __str__(self):
        return f'Move {self.move_id} in Game {self.game.id}'


class Friend(models.Model):
    main_account = models.ForeignKey(CustomUser, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friended_by', on_delete=models.CASCADE)
    date_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('main_account', 'friend')

    def __str__(self):
        return f'{self.main_account.username} is friends with {self.friend.username}'

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f'Notification for {self.user.username} at {self.timestamp} : {self.message}'

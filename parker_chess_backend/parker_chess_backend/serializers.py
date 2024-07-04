from rest_framework import serializers
from parker_chess_app.models import *

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'elo')

class ProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ('user', 'profile_name', 'bio', 'profile_picture', 'date_time_played')

class GameSerializer(serializers.ModelSerializer):
    white_player = CustomUserSerializer(read_only=True)
    black_player = CustomUserSerializer(read_only=True)

    class Meta:
        model = Game
        fields = ('id', 'white_player', 'black_player', 'white_player_elo', 'black_player_elo', 'game_winner', 'game_color_winner', 'date_time_played')

class MoveSerializer(serializers.ModelSerializer):
    game = GameSerializer(read_only=True)
    mover = CustomUserSerializer(read_only=True)

    class Meta:
        model = Move
        fields = ('game', 'move_id', 'move', 'mover', 'piece', 'fen_string', 'date_time_move_played')

class FollowingSerializer(serializers.ModelSerializer):
    main_account = CustomUserSerializer(read_only=True)
    account_following = CustomUserSerializer(read_only=True)

    class Meta:
        model = Following
        fields = ('main_account', 'account_following', 'date_time')

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Notification
        fields = ('user', 'message', 'timestamp', 'urgency', 'read')

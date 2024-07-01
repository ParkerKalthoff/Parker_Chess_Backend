def calculate_elo(player1_rating, player2_rating, result, k=32):
    """
    Calculate the new Elo ratings for two players after a game.

    Parameters:
    player1_rating (int): The current rating of player 1.
    player2_rating (int): The current rating of player 2.
    result (float): The result of the game from player 1's perspective:
                    1.0 if player 1 wins, 0.0 if player 1 loses, 0.5 for a draw.
    k (int): The maximum possible change in rating (default is 32).

    Returns:
    (float, float): The new ratings for player 1 and player 2.
    """
    # Expected score for player 1
    expected_score_p1 = 1 / (1 + 10 ** ((player2_rating - player1_rating) / 400))
    # Expected score for player 2
    expected_score_p2 = 1 / (1 + 10 ** ((player1_rating - player2_rating) / 400))

    # New ratings
    new_player1_rating = player1_rating + k * (result - expected_score_p1)
    new_player2_rating = player2_rating + k * ((1 - result) - expected_score_p2)

    return new_player1_rating, new_player2_rating


if __name__ == '__main__':
    print(calculate_elo(1600, 1600, 0.5))
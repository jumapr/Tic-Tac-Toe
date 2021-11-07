"""Game class for holding game-related parameters"""
from typing import List


class Game:
    def __init__(self):
        """
        Creates initial game screen
        """
        # starts with player 0's turn
        self.whose_turn = 0
        # positions on the grid are labeled as follows:
        # 0 1 2
        # 3 4 5
        # 6 7 8
        # will hold 1 or 0, indicating whether this player has occupied this position
        self.player_0_positions = [0] * 9
        self.player_1_positions = [0] * 9
        # number of games won in this session
        self.player_0_score = 0
        self.player_1_score = 0
        self.num_ties = 0

    def update_game(self, position: int) -> str:
        """
        :param position: index of last button clicked
        :return: result - win, tie, or continue
        """
        if self.whose_turn == 0:
            self.player_0_positions[position] = 1
            result = self.check_result(self.player_0_positions)
        else:
            self.player_1_positions[position] = 1
            result = self.check_result(self.player_1_positions)
        return result

    def check_result(self, current_player_positions: List[int]) -> str:
        """
        Checks for a win or draw. Also, updates whose turn it is if the game will continue.
        :param current_player_positions: list of current player's positions
        :return: result - win, tie, or continue
        """
        total_moves = sum(self.player_0_positions) + sum(self.player_1_positions)
        # check for tie, which occurs when the board is full
        if total_moves >= 9:
            self.num_ties += 1
            result = 'tie'
        # only check for win if they have player has a a chance for at least 3 moves (4 previous combined moves for
        # both players)
        elif total_moves >= 5 and self.check_for_win(current_player_positions):
            result = 'win'
            if self.whose_turn == 0:
                self.player_0_score += 1
            else:
                self.player_1_score += 1
        # no win or tie -> other player's turn
        else:
            result = 'continue'
            self.flip_turns()
        return result

    def reset_game_data(self):
        """
        Resets player positions
        """
        self.player_0_positions = [0] * 9
        self.player_1_positions = [0] * 9
        self.flip_turns()

    @staticmethod
    def check_for_win(player_positions: List[int]) -> bool:
        """
        Checks to see if someone has won
        :param player_positions: list indicating current player's occupied positions on the grid
        :return: True if current player has won, False if not
        """
        has_won = False
        # check for tic-tac-toes through the middle first
        if player_positions[4]:
            # center vertical
            if player_positions[1] and player_positions[7]:
                has_won = True
            # center horizontal
            elif player_positions[3] and player_positions[5]:
                has_won = True
            # top left, bottom right diagonal
            elif player_positions[0] and player_positions[8]:
                has_won = True
            # top right, bottom left diagonal
            elif player_positions[2] and player_positions[6]:
                has_won = True
        if not has_won and player_positions[0]:
            # left vertical
            if player_positions[3] and player_positions[6]:
                has_won = True
            # top horizontal
            elif player_positions[1] and player_positions[2]:
                has_won = True
        if not has_won and player_positions[8]:
            # right vertical
            if player_positions[2] and player_positions[5]:
                has_won = True
            # bottom horizontal
            elif player_positions[6] and player_positions[7]:
                has_won = True
        return has_won

    def flip_turns(self):
        """
        Sets `self.whose_turn` to the opposite (0 -> 1 or 1-> 0)
        """
        if self.whose_turn == 0:
            self.whose_turn = 1
        else:
            self.whose_turn = 0

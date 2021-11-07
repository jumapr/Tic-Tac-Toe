"""Interface class for UI"""

import tkinter as tk
from tkinter import messagebox
from game import Game


END_MESSAGES = {"tie": "Cat's game! Would you like to play again?",
                "win": "{0} wins! Would you like to play again?"}


class Interface:

    def __init__(self):
        """
        Creates initial game screen
        """
        # create game object
        self.game = Game()
        self.players = ("X's", "O's")

        # define string constants for UI
        self.BG_COLOR = "#DBF6E9"
        self.FONT = "Verdana"
        self.PROMPT = "{0}, it's your turn."
        self.SCORE_LABEL = "{0}: {1}"
        self.TIE_LABEL = "Ties: {0}"

        # create window and instructions at the top
        self.window = tk.Tk()
        self.window.title("Tic-tac-toe")
        self.window.configure(padx=30, pady=30, bg=self.BG_COLOR)
        self.window.geometry("450x450")
        self.instructions = self.create_label(self.window, self.PROMPT.format(self.players[self.game.whose_turn]))
        self.instructions.grid(row=0, column=0)
        # create score frame to hold results of previous games in this session
        self.score_frame = tk.Frame(self.window, bg=self.BG_COLOR)
        self.score_frame.grid(row=1, column=1, padx=20, pady=20, sticky='n')
        self.score_label = self.create_label(self.score_frame, 'Score')
        self.score_label.grid(row=0, column=0, sticky='w')
        self.player_0_score_label = self.create_label(self.score_frame,
                                                      self.SCORE_LABEL.format(self.players[0], self.game.player_0_score))
        self.player_0_score_label.grid(row=1, column=0)
        self.player_1_score_label = self.create_label(self.score_frame,
                                                      self.SCORE_LABEL.format(self.players[1], self.game.player_1_score))
        self.player_1_score_label.grid(row=2, column=0)
        self.num_ties_label = self.create_label(self.score_frame, self.TIE_LABEL.format(self.game.num_ties))
        self.num_ties_label.grid(row=3, column=0, sticky='w')
        # create game frame; each of the nine squares on the grid is represented as a button
        self.game_frame = tk.Frame(self.window)
        self.game_frame.grid(row=1, column=0, pady=20)
        self.button_list = self.create_buttons()
        self.place_buttons()

        self.window.mainloop()

    def create_buttons(self):
        """
        Convenience function to create a tkinter button
        :return: list of tkinter buttons
        """
        buttons = []
        for i in range(9):
            buttons.append(tk.Button(self.game_frame, bg="white", relief="ridge", height=1, width=3,
                                     command=self.get_button_callback(i), font=(self.FONT, 48)))
        return buttons

    def create_label(self, on, text: str):
        """
        Convenience function to create a tkinter label
        :param on: tkinter object to put the label on
        :param text: text for label
        :return: tkinter Label object
        """
        return tk.Label(on, font=self.FONT, bg=self.BG_COLOR, text=text)

    def get_button_callback(self, button_idx: int):
        def button_callback():
            self.update_button(self.button_list[button_idx])
            self.update_game_ui(button_idx)
        return button_callback

    def place_buttons(self):
        """
        Places buttons on the grid
        """
        grid_size = 3
        button_index = 0
        for i in range(grid_size):
            for j in range(grid_size):
                self.button_list[button_index].grid(row=i, column=j)
                button_index += 1

    def update_button(self, button: tk.Button):
        """
        Updates button, representing one square of the tic-tac-toe grid, when a player clicks to draw an X or O there
        :param button: button to update
        """
        if self.game.whose_turn == 0:
            button_text = "X"
        else:
            button_text = "O"
        button.configure(state='disabled', text=button_text)

    def update_game_ui(self, position: int):
        """
        Calls game.update_game to determine if the latest move has resulted in a win, tie, or continuation of the game.
        Calls self.end_game to end the game if the latest move has result in win or tie. If the game is continuing,
        prompts the next player.
        :param position: index of button that was just clicked
        """
        game_state = self.game.update_game(position)
        if game_state == "continue":
            self.instructions.configure(text=self.PROMPT.format(self.players[self.game.whose_turn]))
        else:
            self.end_game(game_state)

    def end_game(self, game_state: str):
        """
        Configures the UI for the end of the game. Displays the end_message, and asks the user if they would like to
        start a new game. If the user chooses to start a new game, it calls the methods to reset the game.
        :param game_state: "win", "win", or "continue"
        """
        if game_state == "win":
            end_message = "{0} wins! Would you like to play again?".format(self.players[self.game.whose_turn])
        else:
            end_message = "Cat's game! Would you like to play again?"
        play_again = messagebox.askyesno(title='Game over', message=end_message)
        if play_again:
            self.game.reset_game_data()
            self.reset_game_ui()
        else:
            self.window.destroy()

    def reset_game_ui(self):
        """
        Resets UI for new game
        """
        for button in self.button_list:
            button.configure(state='normal', text='')
        self.instructions.configure(text=self.PROMPT.format(self.players[self.game.whose_turn]))
        self.player_0_score_label.configure(text=self.SCORE_LABEL.format(self.players[0], self.game.player_0_score))
        self.player_1_score_label.configure(text=self.SCORE_LABEL.format(self.players[1], self.game.player_1_score))
        self.num_ties_label.configure(text=self.TIE_LABEL.format(self.game.num_ties))

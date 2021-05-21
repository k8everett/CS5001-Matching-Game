'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the Leaderboard class for my final project.
'''

from ValidationService import ValidationService
from Board import Board
import turtle


class Leaderboard():
    def __init__(self, leaderboard_file_name, board):
        self.leaderboard_file_name = leaderboard_file_name
        self.board = board

        self.leaderboard_contents = []

    def set_leaderboard(self, leaderboard_file):
        ''' Function: set_leaderboard
            Description: Gets the content from the validated_leaderboard_file
            to display at the start of the game.
            Returns: None
        '''
        leaderboard_info = []
        if leaderboard_file.get_validity_status():
            leaderboard_info = (leaderboard_file.get_file_contents())

            # Split score from user name
            for content in leaderboard_info:
                content = content.split()
                if len(content) > 1:

                    # Check to ensure the score is in the right position in
                    # case the user altered the leaderboard file
                    try:
                        int(content[0])
                        self.leaderboard_contents.append(content)
                    except ValueError:
                        try:
                            int(content[1])
                            content.reverse()
                            self.leaderboard_contents.append(content)

                        # Ignore data in leaderboard file without a valid
                        # integer
                        except ValueError:
                            continue

        self.order_leaderboard_contents()
        self.board.display_leaderboard(self.leaderboard_contents)

    def order_leaderboard_contents(self):
        ''' Function: order_leaderboard_contents
            Description: Put leaderboard scores in order in case they are out
            of order when the file is read.
            Returns: None
        '''
        ordered_leaderboard = []

        if len(self.leaderboard_contents) > 0:
            for i in range(len(self.leaderboard_contents)):
                if i == 0:
                    ordered_leaderboard.append(self.leaderboard_contents[i])

                # Check to see if the current score is lower (better)than the
                # one before it.
                else:
                    if (int(self.leaderboard_contents[i][0]) <
                       int(ordered_leaderboard[i - 1][0])):
                        ordered_leaderboard.insert(i - 1,
                                                   self.leaderboard_contents[i])
                    else:
                        ordered_leaderboard.append(self.leaderboard_contents[i])
        self.leaderboard_contents = ordered_leaderboard

    def update_leaderboard(self, guesses, user_name):
        ''' Function: update_leaderboard
            Description: Update the leaderboard at the end of the game with the
            user's name and score.
            Returns: None
        '''
        if len(self.leaderboard_contents) > 0:
            for i in range(len(self.leaderboard_contents)):
                score = int(self.leaderboard_contents[i][0])
                # Add the score to leaderboard_contents if it is lower
                # (better) than an existing score and break the loop
                if guesses <= score:
                    self.leaderboard_contents.insert(i, [guesses, user_name])
                    break

            # Runs if the user's score is higher (worse) than all other current
            # scores on the leaderboard
            if i == len(self.leaderboard_contents) - 1:
                self.leaderboard_contents.append([guesses, user_name])

        self.write_leaderboard()

    def write_leaderboard(self):
        ''' Function: write_leaderboard
            Description: Write the new leaderboard file with the update list
            of leaders and their scores..
            Returns: None
        '''
        self.leaderboard_contents = self.leaderboard_contents[:8]
        with open(self.leaderboard_file_name, mode='w') as outfile:
            for i in range(len(self.leaderboard_contents)):
                content = self.leaderboard_contents[i]
                if len(content) > 1:
                    outfile.write('{} {}\n'.format(content[0], content[1]))

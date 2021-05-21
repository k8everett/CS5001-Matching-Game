'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the Board class for my final project.
'''
import turtle
from Rectangle import Rectangle
from TextService import TextService

GAME_AREA_WIDTH = 500
GAME_AREA_HEIGHT = 550
GAME_AREA_X_START = -350
GAME_AREA_Y_START = -225

STATUS_AREA_HEIGHT = 50
STATUS_AREA_Y_START = -300

STATUS_AREA_TEXT_X_START = -340
STATUS_AREA_TEXT_Y_START = -275

LEADERBOARD_AREA_WIDTH = 150
LEADERBOARD_AREA_X_START = 175

LEADERBOARD_TEXT_X_START = 185
LEADERBOARD_TEXT_Y_START = 300

WARNING_TEXT_X_START = -150
WARNING_TEXT_Y_START = -150

GAME_COLOR = "blueviolet"
LEADERBOARD_COLOR = "deeppink"

CARD_NUMBER_WARNING_IMAGE_NAME = "card_warning.gif"


class Board:
    def __init__(self, screen):
        ''' Function: __init__
            Parameters:
                screen (turtle object): Screen from the Game class
            Returns: None (constructor method)
        '''
        self.s = screen

        # Set up turtle object for updating the status board
        self.t = turtle.Turtle()
        self.t.hideturtle()

        self.user_name = None
        self.number_of_cards = None

    def make_game_area(self):
        ''' Function: make_game_area
            Description: Create and display the game area
            Returns: None
        '''
        game_area = Rectangle(GAME_AREA_WIDTH, GAME_AREA_HEIGHT,
                              GAME_AREA_X_START, GAME_AREA_Y_START, GAME_COLOR)
        game_area.draw()

    def make_status_area(self):
        ''' Function: make_status_area
            Description: Create and display the status area
            Returns: None
        '''
        status_area = Rectangle(GAME_AREA_WIDTH, STATUS_AREA_HEIGHT,
                                GAME_AREA_X_START, STATUS_AREA_Y_START,
                                GAME_COLOR)
        status_area.draw()

    def make_leaderboard_area(self):
        ''' Function: make_leaderboard_area
            Description: Create and display the leaderboard area
            Returns: None
        '''
        leaderboard_area = Rectangle(LEADERBOARD_AREA_WIDTH, GAME_AREA_HEIGHT,
                                     LEADERBOARD_AREA_X_START,
                                     GAME_AREA_Y_START, LEADERBOARD_COLOR)
        leaderboard_area.draw()

    def set_user_input(self):
        ''' Function: set_user_input
            Description: Get user's name and number of cards they want to
            play with.
            Returns: None
        '''
        self.user_name = turtle.textinput("User Name", "Your Name:")

        # Default user name
        if self.user_name is None or len(self.user_name) == 0:
            self.user_name = "Player 1"

        self.number_of_cards = turtle.numinput("Set Up", "# of Cards to Play:" +
                                               " (8, 10, or 12)", 8, 8, 12)
        self.validate_number_of_cards()

    def validate_number_of_cards(self):
        ''' Function: validate_number_of_cards
            Description: Validate the user's input
            Returns: None
        '''
        # Ensure that the user enters a number or hits cancel
        while (type(self.number_of_cards) != float and
               self.number_of_cards is not None):
            self.number_of_cards = turtle.numinput("Set Up", "# of Cards to" +
                                                   " Play: (8, 10, or 12)",
                                                   8, 8, 12)

        # Check to see if the number is even or odd
        if type(self.number_of_cards) == float:
            if self.number_of_cards % 2 != 0:
                turtle.bgpic(CARD_NUMBER_WARNING_IMAGE_NAME)
                self.s.ontimer(self.remove_image, 2000)

    def display_leaderboard(self, leaderboard_info):
        ''' Function: display_leaderboard
            Parameters:
                leaderboard_info (list): List of high scores and the users
            Description: Display leaderboard info on the screen
            Returns: None
        '''
        y = LEADERBOARD_TEXT_Y_START
        t = turtle.Turtle()

        # Check for empty leaderboard file
        if len(leaderboard_info) > 0:
            TextService("Leaders", LEADERBOARD_TEXT_X_START, y,
                        LEADERBOARD_COLOR, t).add_text()
            y -= 32
            for content in leaderboard_info:
                if len(content) > 1:
                    score = content[0]
                    name = content[1]
                    info = ' {} : {}'.format(score, name)
                TextService(info, LEADERBOARD_TEXT_X_START, y,
                            LEADERBOARD_COLOR, t).add_text()
                y -= 32

        # Runs if leaderboard file is empty or doesn't exist
        else:
            TextService("No Leaders", LEADERBOARD_TEXT_X_START, y,
                        LEADERBOARD_COLOR, t).add_text()

    def display_status(self, guesses, matches):
        ''' Function: display_status
            Parameters:
                guesses (int): Number of guesses the user has made
                matches (int): Number of matches the user has made
            Description: Display the score status
            Returns: None
        '''
        status = 'Status: {} moves, {} matches'.format(guesses, matches)
        text = TextService(status, STATUS_AREA_TEXT_X_START,
                           STATUS_AREA_TEXT_Y_START, GAME_COLOR, self.t)

        # Remove previous status and replace it with the new one
        text.remove_text()
        text.add_text()

    def create_board(self):
        ''' Function: create_board
            Description: Display the board areas
            Returns: None
        '''
        self.make_game_area()
        self.make_status_area()
        self.make_leaderboard_area()

    def get_user_name(self):
        ''' Function: get_user_name
            Description: Helper function
            Returns: self.user_name
        '''
        return self.user_name

    def get_number_of_cards(self):
        ''' Function: get_number_of_cards
            Description: Helper function
            Returns: self.number_of_cards
        '''
        return self.number_of_cards

    def remove_image(self):
        ''' Function: remove_image
            Description: Removes a background image (helper function).
            Returns: None
        '''
        turtle.bgpic("nopic")

    def display_warning(self):
        ''' Function: display_warning
            Description: Display warning if the cfg file does not contain
            enough valid face cards to play with the amount of cards requested
            (helper function).
            Returns: None
        '''
        t = turtle.Turtle()
        text = TextService("Not enough cards for the this file.\nClassic game"
                           " will be used instead.", WARNING_TEXT_X_START,
                           WARNING_TEXT_Y_START, GAME_COLOR, t)
        text.add_text()
        self.s.ontimer(text.remove_text, 2000)

    def display_back_card_warning(self):
        ''' Function: display_back_card_warning
            Description: Display warning if the image for the back of the card
            is invalid.
            Returns: None
        '''
        t = turtle.Turtle()
        text = TextService("Image for the back of the card is invalid\nDefault"
                           " will be used instead.", WARNING_TEXT_X_START,
                           WARNING_TEXT_Y_START, GAME_COLOR, t)
        text.add_text()
        self.s.ontimer(text.remove_text, 2000)

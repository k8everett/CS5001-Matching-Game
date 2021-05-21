'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the Game class for my project which allows a user to
play a memory matching game.
'''

import turtle
from Card import Card
from Board import Board
from ValidationService import ValidationService
from TextService import TextService
from QuitService import QuitService
from Leaderboard import Leaderboard
from random import sample
from random import shuffle

GAME_AREA_HEIGHT = 550
GAME_AREA_X_START = -350
GAME_AREA_Y_START = -225

QUIT_X_START = 205
QUIT_Y_START = -280

THEME_TEXT_X_START = -175

DEFAULT_CARD_IMAGE_NAMES = ["ace_of_diamonds.gif", "2_of_clubs.gif",
                            "2_of_diamonds.gif", "3_of_hearts.gif",
                            "jack_of_spades.gif", "queen_of_hearts.gif",
                            "king_of_diamonds.gif"]
DEFAULT_CARD_BACK_NAME = "card_back_logo.gif"
THEME_FILE_NAMES = ["bachelorette.cfg", "parks_and_rec.cfg", "the_office.cfg",
                    "the_crown.cfg", "schitts_creek.cfg", "britney.cfg",
                    "child_actors.cfg", "classic_game.cfg"]
CONFIGURATION_FILE = "themes.cfg"
LEADERBOARD_FILE = "leaderboard.txt"
FILES_TO_VALIDATE = [CONFIGURATION_FILE, LEADERBOARD_FILE]
FILE_NOT_FOUND_IMAGE_NAMES = ["file_error.gif", "leaderboard_error.gif"]
WINNER_PIC_NAME = "winner.gif"
QUIT_BUTTON_IMAGE = "quitbutton.gif"
QUIT_MESSAGE = "quitmsg.gif"
GAME_COLOR = "blueviolet"


class Game:
    def __init__(self):
        ''' Function: __init__
            Parameters: None (initialize variables for the class)
            Returns: None (constructor method)
        '''
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.s = turtle.Screen()
        self.s.bgcolor("deepskyblue")
        turtle.title("CS5001 Memory Game")

        # Validated files and their contents
        self.validated_cfg_file = None
        self.validated_leaderboard_file = None
        self.cfg_contents = []

        # Initialize Board and QuitService classes
        self.board = Board(self.s)
        self.quit_button = QuitService(QUIT_BUTTON_IMAGE, QUIT_MESSAGE,
                                       QUIT_X_START, QUIT_Y_START, self.s)
        self.leaderboard = Leaderboard(LEADERBOARD_FILE, self.board)

        # Attributes to keep track of themes
        self.theme_number = 0
        self.invalid_theme_numbers = []
        self.theme_files = []

        # User input attributes
        self.user_name = None
        self.number_of_cards = None

        # Score tracking attributes
        self.matches = 0
        self.guesses = 0

        # Card image attributes
        self.card_image_names = DEFAULT_CARD_IMAGE_NAMES
        self.card_back = DEFAULT_CARD_BACK_NAME

        # Lists of cards with certain attributes
        self.cards = []
        self.clicked_cards = []
        self.matched_cards = []

    def get_user_input(self):
        ''' Function: get_user_input
            Description: Gets user name and number of cards from the Board
            class.
            Returns: None
        '''
        self.user_name = self.board.get_user_name()
        self.number_of_cards = self.board.get_number_of_cards()

    def validate_files(self):
        ''' Function: validate_files
            Description: Validates the congfiguration and leaderboard files.
            Returns: None
        '''
        file_delay = 0
        for i in range(len(FILES_TO_VALIDATE)):
            file = ValidationService(FILES_TO_VALIDATE[i],
                                     FILE_NOT_FOUND_IMAGE_NAMES[i], self.s)
            if i == 0:
                file.validate_file()
                file_delay += 2000 * file.get_timer_status()
                self.validated_cfg_file = file
            else:
                self.validated_leaderboard_file = file

                # Accounts for delay if the first file doesn't open and an
                # error message is on the screen.
                if file_delay > 0:
                    self.s.ontimer(file.validate_file, file_delay)
                    self.s.ontimer(self.input_start, file_delay)
                else:
                    file.validate_file()
                    file_delay += 2000 * file.get_timer_status()
                    self.s.ontimer(self.input_start, file_delay)

    def check_theme_availability(self):
        ''' Function: check_theme_availability
            Description: Checks if the imported cfg file is the theme file.
            Returns: None
        '''
        self.cfg_contents = self.validated_cfg_file.get_file_contents()
        theme_availability = False

        if self.cfg_contents:

            # Checks if the last line of the cfg file says themes
            if self.cfg_contents[len(self.cfg_contents) - 1] == 'themes':
                theme_availability = True
                if theme_availability:

                    # Ignore last line of theme file
                    self.cfg_contents = (self.cfg_contents
                                         [:len(self.cfg_contents) - 1])
                    self.make_theme_files()

    def make_theme_files(self):
        ''' Function: make_theme_files
            Description: Makes a list of the valid themes for the user to
            choose from.
            Returns: None
        '''
        y = 100
        for i in range(len(self.cfg_contents)):
            content = ValidationService(self.cfg_contents[i], "nopic", self.s)
            content.validate_file()

            # Runs if the cfg is valid
            if content.get_validity_status():
                theme_name = content.get_file_contents()[0]
                TextService("{} : {}".format(i + 1, theme_name),
                            THEME_TEXT_X_START, y, GAME_COLOR, self.t).add_text()
                theme_content = content.get_file_contents()[1:]
                validated_theme_content = content.validate_images(theme_content)
                self.theme_files.append(validated_theme_content)
                y -= 32

            # Append invalid file to not throw off theme number input
            else:
                self.theme_files.append(content)
                self.invalid_theme_numbers.append(i + 1)
        self.validate_theme_number()

    def validate_theme_number(self):
        ''' Function: validate_theme_number
            Description: Asks user to choose a theme, then ensures that it is
            both a number and a theme with enough cards to play the game.
            Returns: None
        '''
        # Runs if there is 1 or more valid themes to choose from
        if (1 < len(self.theme_files) and len(self.invalid_theme_numbers)
           != len(self.theme_files)):
            self.theme_number = turtle.numinput("Theme Choice",
                                                "Choose a Theme", 1, 1,
                                                len(self.cfg_contents))

            # Check to make sure first entry wasn't cancel
            if self.theme_number is not None:
                if (type(self.theme_number) == float and self.theme_number
                   not in self.invalid_theme_numbers):
                    imported_card_images = (self.theme_files
                                            [int(self.theme_number - 1)])

                # Use length of default card images so the while loop runs if a
                # theme number is entered that's in self.invalid_theme_numbers
                else:
                    imported_card_images = self.card_image_names

                # Validation loop in case the user hits cancel, there aren't
                # enough valid pictures for the chosen theme, or the number
                # entered is associated with an invalid themed file.
                while (type(self.theme_number) != float or
                       len(imported_card_images) <= int(self.number_of_cards / 2)
                       or self.theme_number in self.invalid_theme_numbers):
                    self.theme_number = turtle.numinput("Theme Choice",
                                                        "Unavailable theme.\n"
                                                        "Please select a "
                                                        "different one.", 1, 1,
                                                        len(self.cfg_contents))
                    if (type(self.theme_number) == float and self.theme_number
                       not in self.invalid_theme_numbers):
                        imported_card_images = self.theme_files[int(self.theme_number - 1)]

                    # Break the loop if the user hits cancel
                    elif self.theme_number is None:
                        break
        self.t.clear()

    def create_card_images(self):
        ''' Function: create_card_images
            Description: Updates self.card_back and self.card_image_names as
            is necessary based on the contents of the cfg file.
            Returns: None
        '''
        # Runs if the main cfg file contains a list of the themed files and at
        # least one of those themes is valid for the number of cards
        if (0 < len(self.theme_files) and len(self.theme_files)
           != len(self.invalid_theme_numbers)):
            imported_card_images = self.theme_files[int(self.theme_number - 1)]
            self.check_back_card(imported_card_images)

        # Runs if cfg file is one of the invdividual themed files
        elif (self.validated_cfg_file.get_validity_status() and
              CONFIGURATION_FILE in THEME_FILE_NAMES):
            self.cfg_contents = (self.validated_cfg_file.
                                 validate_images(self.cfg_contents[1:]))

            # Check to make sure there are enough valid card images for the
            # game
            if len(self.cfg_contents) > int(self.number_of_cards / 2):
                self.check_back_card(self.cfg_contents)
            else:
                self.board.display_warning()

        # Runs if the cfg file is not the list of themes or one of the
        # individual themed files
        elif self.validated_cfg_file.get_validity_status():
            self.cfg_contents = (self.validated_cfg_file.
                                 validate_images(self.cfg_contents))

            # Check to make sure there are enough valid card images for the
            # game
            if len(self.cfg_contents) >= int(self.number_of_cards / 2):
                self.card_image_names = self.cfg_contents
            else:
                self.board.display_warning()
        self.create_cards()

    def check_back_card(self, images):
        ''' Function: check_back_card
            Parameters:
                images (list): List of card image names
            Description: Checks to make sure that the first item in the list of
            images is a valid card back (only applicable to themed files).
            Returns: None
        '''
        # The first image in every themed file is the card back for that theme
        # and contains the word logo.
        logo_find = images[0].find("logo")
        if logo_find > -1:
            self.card_back = images[0]
            self.card_image_names = images[1:]

        # If there is no valid card back for the theme, the default will be
        # used instead.
        else:
            self.card_image_names = images
            self.board.display_back_card_warning()

    def create_cards(self):
        ''' Function: create_cards
            Description: Creates the card objects and appends them to a master
            list.
            Returns: None
        '''
        available_card_names = sample(self.card_image_names,
                                      int(self.number_of_cards / 2))

        for name in available_card_names:

            # Create two matching copies
            first_copy = Card(name, self.card_back, self.s)
            second_copy = Card(name, self.card_back, self.s)

            self.cards.append(first_copy)
            self.cards.append(second_copy)

        self.deal_cards()

    def deal_cards(self):
        ''' Function: deal_cards
            Description: Displays the cards on the game board.
            Returns: None
        '''
        shuffle(self.cards)
        card_x_loc = GAME_AREA_X_START + 60

        # Different card location depending on number of cards
        # if self.number_of_cards == 10 or self.number_of_cards == 12:
        #     card_y_loc = GAME_AREA_Y_START + GAME_AREA_HEIGHT - 85
        # else:
        #     card_y_loc = GAME_AREA_Y_START + GAME_AREA_HEIGHT - 180

        for i in range(len(self.cards)):
            self.cards[i].position_card(card_x_loc, card_y_loc)

            # Start a new row of cards after every 4
            if (i + 1) % 4 == 0:
                card_x_loc -= 375
                card_y_loc -= 175
            else:
                card_x_loc += 125

    def check_end_game(self):
        ''' Function: check_end_game
            Description: Determine if all the cards have been matched.
            Returns: None
        '''
        self.update_matched_cards()
        if len(self.matched_cards) == len(self.cards):
            turtle.bgpic(WINNER_PIC_NAME)
            self.leaderboard.update_leaderboard(self.guesses, self.user_name)
            self.s.ontimer(turtle.bye, 2100)

    def check_click_location(self, x, y):
        ''' Function: check_click_location
            Parameters:
                x (int): x value of the click location
                y (int): y value of the click location
            Description: Determines where the click was, and what, if anything,
            need to be done
            Returns: None
        '''
        quit_boundaries = self.quit_button.get_button_boundaries()
        x_upper_boundary = quit_boundaries[0]
        x_lower_boundary = quit_boundaries[1]
        y_upper_boundary = quit_boundaries[2]
        y_lower_boundary = quit_boundaries[3]

        # Check if the click was on the quit botton
        if ((x_lower_boundary <= x <= x_upper_boundary) and
           (y_lower_boundary <= y <= y_upper_boundary)):
            self.quit_button.quit_game()

        # Check if the click was on a card
        else:
            for card in self.cards:
                card_boundaries = card.get_card_boundaries()
                if card_boundaries:
                    x_upper_boundary = card_boundaries[0]
                    x_lower_boundary = card_boundaries[1]
                    y_upper_boundary = card_boundaries[2]
                    y_lower_boundary = card_boundaries[3]

                    if ((x_lower_boundary <= x <= x_upper_boundary) and
                       (y_lower_boundary <= y <= y_upper_boundary)):

                        # Ensure that only two cards can be clicked at a time
                        if len(self.clicked_cards) < 2:
                            card.set_clicked()
                            card.flip_card_up()
                            self.game_control()

    def check_for_match(self):
        ''' Function: check_for_match
            Description: Check the two clicked cards to see if they are equal
            (matched).
            Returns: None
        '''
        card1 = self.clicked_cards[0]
        card2 = self.clicked_cards[1]

        # Timer set to make sure the cards stay up for a few seconds so the
        # user can remember where the cards are before the disappear or
        # flip back down
        self.guesses += 1
        if card1 == card2:
            self.matches += 1
            self.s.ontimer(self.set_matched_cards, 1000)
        else:
            self.s.ontimer(self.unclick_cards, 1000)
        self.board.display_status(self.guesses, self.matches)
        self.s.ontimer(self.update_clicked_cards, 1000)
        self.s.ontimer(self.check_end_game, 1100)

    def game_control(self):
        ''' Function: game_control
            Description: Controls the clicking/match checking for the cards.
            Returns: None
        '''
        self.update_clicked_cards()
        self.get_click_location()
        if len(self.clicked_cards) == 2:
            self.check_for_match()

    def input_start(self):
        ''' Function: input_start
            Description: Get user's name, the number of cards they want to play
            with, and their theme choice (if applicable).
            Returns: None
        '''
        self.board.set_user_input()
        self.get_user_input()

        # Delay creating the board/displaying cards if there is a warning
        # for odd number of cards
        if type(self.number_of_cards) == float:
                self.check_theme_availability()
                self.game_start()

        # Quit game if user hits cancel for number of cards input
        else:
            self.quit_button.quit_game()

    def game_start(self):
        ''' Function: game_start
            Description: Display the game board, leaderboard, score status,
            and cards. Allows the user to start clicking to play.
            Returns: None
        '''
        # Quit game if user hits cancel for theme choice input
        if self.theme_number is None:
            self.quit_button.quit_game()
        else:
            self.board.create_board()
            self.quit_button.display_button()
            self.leaderboard.set_leaderboard(self.validated_leaderboard_file)
            self.board.display_status(self.guesses, self.matches)
            self.create_card_images()
            self.game_control()

    def unclick_cards(self):
        ''' Function: unclick_cards
            Description: Unclick the clicked cards if there is no match found
            (helper function).
            Returns: None
        '''
        for card in self.clicked_cards:
            card.set_unclicked()
            card.flip_card_down()

    def update_matched_cards(self):
        ''' Function: update_matched_cards
            Description: Update the cards that are in the matched_cards list
            (helper function).
            Returns: None
        '''
        self.matched_cards = []
        for card in self.cards:
            if card.get_matched_status():
                self.matched_cards.append(card)

    def set_matched_cards(self):
        ''' Function: set_matched_cards
            Description: Update the card status if two cards are matched and
            remove them from the screen (helper function).
            Returns: None
        '''
        for card in self.clicked_cards:
            card.set_matched()
            card.set_unclicked()
            card.hide_turtle()

    def update_clicked_cards(self):
        ''' Function: update_clicked_cards
            Description: Update the cards that are in the clicked_cards list
            (helper function).
            Returns: None
        '''
        self.clicked_cards = []
        for card in self.cards:
            if card.get_clicked_status():
                self.clicked_cards.append(card)

    def get_click_location(self):
        ''' Function: get_click_location
            Description: Get the click location and pass it to
            check_click_location (helper function).
            Returns: None
        '''
        self.s.onclick(self.check_click_location)

'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the Card class for my final project.
'''
import turtle

CARD_WIDTH = 100
CARD_HEIGHT = 150


class Card():
    def __init__(self, name, back, screen):
        ''' Function: __init__
            Parameters:
                name (str): Card face image name
                back (str): Card back image name
                screen (turtle object): Screen from the Game class
            Returns: None (constructor method)
        '''
        self.name = name
        self.back = back
        self.s = screen

        # Set up the turtle for the individual cards
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.s.addshape(self.name)
        self.s.addshape(self.back)

        # Coordinates of each card and their boundaries
        self.x = 0
        self.y = 0
        self.boundaries = []

        # Attributes of the cards for game play
        self.clicked = False
        self.matched = False

    def position_card(self, x, y):
        ''' Function: position_card
            Parameters:
                x (int): x value of the card location
                y (int): y value of the card location
            Description: Places the card at the given Coordinates
            Returns: None
        '''
        self.x = x
        self.y = y

        # Start with card face down
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.shape(self.back)
        self.t.pendown()
        self.t.showturtle()

    def get_card_boundaries(self):
        ''' Function: get_card_boundaries
            Description: Return the boundaries of the unmatched card (won't
            allow cards that have been matched and hidden to be clicked).
            Returns: None
        '''
        if not self.matched:
            x_upper_boundary = self.x + (CARD_WIDTH / 2)
            self.boundaries.append(x_upper_boundary)
            x_lower_boundary = self.x - (CARD_WIDTH / 2)
            self.boundaries.append(x_lower_boundary)

            y_upper_boundary = self.y + (CARD_HEIGHT / 2)
            self.boundaries.append(y_upper_boundary)
            y_lower_boundary = self.y - (CARD_HEIGHT / 2)
            self.boundaries.append(y_lower_boundary)

            return self.boundaries

    def flip_card_up(self):
        ''' Function: flip_card_up
            Description: Shows the card's face (helper function)
            Returns: None
        '''
        self.t.shape(self.name)

    def flip_card_down(self):
        ''' Function: flip_card_down
            Description: Shows the card's back (helper function)
            Returns: None
        '''
        self.t.shape(self.back)

    def set_clicked(self):
        ''' Function: set_clicked
            Description: Sets the card's clicked status as True
            (helper function)
            Returns: None
        '''
        self.clicked = True

    def set_unclicked(self):
        ''' Function: set_clicked
            Description: Sets the card's clicked status as False
            (helper function)
            Returns: None
        '''
        self.clicked = False

    def hide_turtle(self):
        ''' Function: hide_turtle
            Description: Hides the card (helper function)
            Returns: None
        '''
        self.t.hideturtle()

    def set_matched(self):
        ''' Function: set_matched
            Description: Sets the card's clicked status as False and matched
            status as True (helper function)
            Returns: None
        '''
        self.matched = True
        self.clicked = False

    def get_clicked_status(self):
        ''' Function: set_clicked
            Description: Helper function
            Returns: self.clicked
        '''
        return self.clicked

    def get_matched_status(self):
        ''' Function: get_matched_status
            Description: Helper function
            Returns: self.matched
        '''
        return self.matched

    def __eq__(self, other):
        ''' Function: __eq__
            Description: Determines if two Card objects are equal
            Returns: Boolean depending on if the two cards are equal
        '''
        if self.name == other.name:
            return True
        return False

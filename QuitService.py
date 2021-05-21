'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the QuitService class for my final project.
'''
import turtle

BUTTON_WIDTH = 60
BUTTON_HEIGHT = 40


class QuitService():
    def __init__(self, button, message, x, y, screen):
        ''' Function: __init__
            Parameters:
                button (str): Name of button image
                message (str): Name of message image
                x (int): x value of the quit image location
                y (int): y value of the quit image location
                screen (turtle object): Screen from the Game class
            Returns: None (constructor method)
        '''
        self.button = button
        self.message = message
        self.x = x
        self.y = y
        self.s = screen

        # Set up the turtle for the quit button
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.s.addshape(self.button)
        self.s.addshape(self.message)

        # Initialize attributes of the button
        self.boundaries = []

    def display_button(self):
        ''' Function: display_button
            Description: Create and display the quit button
            Returns: None
        '''
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.shape(self.button)
        self.t.pendown()
        self.t.showturtle()

    def get_button_boundaries(self):
        ''' Function: get_button_boundaries
            Description: Return the boundaries of the quit button
            Returns: None
        '''
        x_upper_boundary = self.x + (BUTTON_WIDTH / 2)
        self.boundaries.append(x_upper_boundary)
        x_lower_boundary = self.x - (BUTTON_WIDTH / 2)
        self.boundaries.append(x_lower_boundary)

        y_upper_boundary = self.y + (BUTTON_HEIGHT / 2)
        self.boundaries.append(y_upper_boundary)
        y_lower_boundary = self.y - (BUTTON_HEIGHT / 2)
        self.boundaries.append(y_lower_boundary)

        return self.boundaries

    def quit_game(self):
        ''' Function: quit_game
            Description: Closes the turtle screen when the quit button
            is clicked.
            Returns: None
        '''
        new_turtle = turtle.Turtle()
        new_turtle.hideturtle()

        new_turtle.shape(self.message)
        new_turtle.showturtle()
        self.s.ontimer(turtle.bye, 2100)

    def remove_image(self):
        ''' Function: remove_image
            Description: Removes a background image (helper function).
            Returns: None
        '''
        turtle.bgpic("nopic")

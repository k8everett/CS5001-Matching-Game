'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the TextService class for my final project.
'''

import turtle


class TextService():
    def __init__(self, text, x, y, color, turtl):
        ''' Function: __init__
            Parameters:
                text (str): Text to be displayed
                x (int): x value of the Text starting location
                y (int): y value of the Text starting location
                color (str): Color of the Text
                turtl (turtle object): Turtle for the Text object
            Returns: None (constructor method)
        '''
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.t = turtl

        # Initialize turtle attributes
        self.t.speed(0)
        self.t.penup()
        self.t.hideturtle()
        self.t.pencolor(self.color)

    def move_pen(self):
        ''' Function: move_pen
            Description: Moves the pen without drawing line
            Returns: None
        '''
        self.t.goto(self.x, self.y)

    def add_text(self):
        ''' Function: add_text
            Description: Adds text at the designated location
            Returns: None
        '''
        self.move_pen()
        self.t.write(self.text, False, 'left', ('Times', 16, 'normal'))

    def remove_text(self):
        ''' Function: remove_text
            Description: Removes previously written text
            Returns: None
        '''
        self.t.clear()

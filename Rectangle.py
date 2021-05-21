'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the Rectangle class for my final project.
'''
import turtle


class Rectangle():
    def __init__(self, width, height, x, y, color):
        ''' Function: __init__
            Parameters:
                width (int): Width of the rectangle
                height (int): Height of the rectangle
                x (int): x value of the Rectangle starting location
                y (int): y value of the Rectangle starting location
                color (str): Color of the rectangle
            Returns: None (constructor method)
        '''
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color

        # Initialize attributes of the Rectangle's turtle
        self.t = turtle.Turtle()
        self.t.hideturtle()
        self.t.pencolor(self.color)
        self.t.pensize(6)
        self.t.speed(0)

    def move_pen(self):
        ''' Function: move_pen
            Description: Moves the pen without drawing line
            Returns: None
        '''
        self.t.penup()
        self.t.goto(self.x, self.y)
        self.t.pendown()

    def draw(self):
        ''' Function: draw
            Description: Draws the Rectangle
            Returns: None
        '''
        self.move_pen()

        for side in range(4):
            if side % 2 == 0:
                self.t.forward(self.width)
                self.t.left(90)
            else:
                self.t.forward(self.height)
                self.t.left(90)

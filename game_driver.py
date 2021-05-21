'''
Kate Everett
CS5001, Fall 2020
Final Project

This program is the driver for my Game class.
'''
from Game import Game
import turtle

def main():
    game = Game()
    game.validate_files()
    turtle.mainloop()

main()

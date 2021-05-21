'''
Kate Everett
CS5001, Fall 2020
Final Project

This program contains the ValidationService class for my final project.
'''

import turtle


class ValidationService():
    def __init__(self, file_name, file_not_found_image, screen):
        ''' Function: __init__
            Parameters:
                file_name (str): Name of file being validated
                file_not_found_image (str): Name of image to display
                if file is not found
                screen (turtle object): Screen from the Game class
            Returns: None (constructor method)
        '''
        self.file_name = file_name
        self.file_not_found_image = file_not_found_image
        self.s = screen

        # Initialize attributes of the class
        self.valid = False
        self.file_contents = []
        self.timer_status = 0

    def validate_file(self):
        ''' Function: validate_file
            Description: Validates the given file and appends its valid
            contents to self.file_contents
            Returns: None (constructor method)
        '''
        try:
            with open(self.file_name, mode='r') as infile:
                lines = infile.readlines()
                for line in lines:
                    line = line.strip('\n')
                    self.file_contents.append(line)
                self.valid = True

        # Display file not found image
        except FileNotFoundError:
            self.timer_status += 1
            self.s.bgpic(self.file_not_found_image)
            self.s.ontimer(self.remove_image, 2000)

    def validate_images(self, image_names):
        ''' Function: validate_images
            Parameters:
                image_names (list): List of image names
            Description: Validates the images in the list
            Returns: validated_images (list)
        '''
        validated_images = []
        for image in image_names:
            try:
                with open(image, mode='r') as line:
                    if image:
                        validated_images.append(image)

            # Ignore invalid images
            except FileNotFoundError:
                continue
        return validated_images

    def remove_image(self):
        ''' Function: remove_image
            Description: Removes a background image (helper function).
            Returns: None
        '''
        self.s.bgpic("nopic")

    def get_validity_status(self):
        ''' Function: get_validity_status
            Description: Helper function
            Returns: return self.valid
        '''
        return self.valid

    def get_file_contents(self):
        ''' Function: get_file_contents
            Description: Helper function
            Returns: return self.file_contents
        '''
        return self.file_contents

    def get_timer_status(self):
        ''' Function: get_timer_status
            Description: Helper function
            Returns: return self.timer_status
        '''
        return self.timer_status

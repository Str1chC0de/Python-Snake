""" Python Evolving Snake game
    
    Description:
        Menu file includes Menu and Menu_button classes, together you can craft an individual Game menu

    Param:
        Author  : Simon Jess 
        Date    : 06.06.2021
        Version : 1.0.0 
        License : free
"""

import pygame
import logging

# Set config for logging
logging.basicConfig(format='%(asctime)s - %(message)s', filename='logs\\logfile.log', datefmt='%y-%m-%d %H:%M')

pygame.init()

class Menu():
    """
    Description:
        create an object of the class Menu, to be able to change the background with the provided methods

    Attributes:
        game         : Instance of an object of the Game class
        screen_height: height of the game screen
        screen_width : width of the game screen
        game_screen  : pygame.display, with screen width and height as size
        area         : pygame.Surface, with the playarea as size
        color        : color as parameter for the background color
        alpha        : alpha as strength of transparency of the background color

    Params:
        game (Game): the instance of the game object
        color (RGB color): a color in RGB style ([0-255], [0-255], [0-255])
        alpha (int): an integer value from 0-255 for the strength of transparency

    Tests:
        1. Check if the object: game_over_menu was created
        1. Check if the object: game_pause_menu was created
    """

    def __init__(self, game, color, alpha):
        try:
            self.game = game
            self.screen_height = self.game.screen_height
            self.screen_width  = self.game.screen_width
            self.game_screen = self.game.game_screen
            self.area = pygame.Surface((self.game.screen_width-420, self.game.screen_height-80))
            self.color = color
            self.alpha = alpha
        
        except Exception as e:
            logging.error("Error occurred when setting initial values to the Menu object", exc_info=True)


    def blit_background(self):
        """
        Description:
            change the background color of the playarea to an other color

        Params:
            none 
        
        Returns:
            none

        Tests:
            1. If you die, the background should change to an slightly transparent red
            2. If the game is paused, the background should be sliightly transparent white
        """
        try:
            # pause area --> change background 
            self.area.set_alpha(self.alpha)
            self.area.fill(self.color)
            self.game_screen.blit(self.area, (40, 40))
        
        except Exception as e:
            logging.error("Error occurred when changing background", exc_info=True)


class Menu_Button():
    """
    Description:
        Creating a button object through an image and the reaction to a click event

    Attribute:
        game_screen : pygame.display, with screen width and height as size
        image       : Image specifying the appearance of the button
        rect        : rect filled with the image and forming the button
        rect.x      : x coordinate of the rect
        rect.y      : y coordinate of the rect
        clicked     : bool to check if the button was clicked
    
    Params:
        x (int): x coordinate  for rect
        y (int): y coordinate for rect
        image (pygame.image): images source
        screen (pygmae.display): game screen, pygame window

    Tests:
        1. check if the object button_pause was created
        2. check if the object button_resume was created
    """

    def __init__(self, x, y, image, screen):
        try:
            self.game_screen = screen
            self.image = image
            
            # get rect the rect of the image
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.clicked = False
        
        except Exception as e:
            logging.error("Error occurred when setting initial values to the Button object ", exc_info=True)


    def draw_Button(self):
        """
        Description:
            drawing the buttons to the game_screen
            query mouse position to check collisions and click events

        Params:
            none

        Returns:
            bool: returns if the button was clicked or not

        Tests:
            1. check of the button_pause button was drawed on the screen
            2. check if the game starts there are 2 buttons: "play", "exit" are displayed on the play area

        Inspiration:
            https://github.com/russs123/pygame_button/blob/main/button.py last call: 05.06.2021
        """

        try:
            clickstatus = False

            # get mouse position
            mous_position = pygame.mouse.get_pos()

            # prove if mouse collides with the button rect
            if self.rect.collidepoint(mous_position):

                # prove if the mouse is clicked
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    clickstatus = True
                    self.clicked = True

                # mouse not clicked
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

            self.game_screen.blit(self.image, self.rect)

            # return bool for event check
            return clickstatus

        except Exception as e:
            logging.error("Error occurred when button interaction happens ", exc_info=True)
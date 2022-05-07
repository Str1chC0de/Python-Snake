""" Python Evolving Snake game
    
    Description:
        Food file includes food class, a food object can be eaten by a snake 

    Param:
        Author  : Simon Jess 
        Date    : 06.06.2021
        Version : 1.0.0 
        License : free
"""

import pygame
import random
import logging

from pygame.math import Vector2

# Set config for logging
logging.basicConfig(format='%(asctime)s - %(message)s', filename='logs\\logfile.log', datefmt='%y-%m-%d %H:%M')

class Food():
    """
    Description:
        Create an object of the food object an provide a possibility to draw and get new position for the object

    Attributes:
        game: game object
        randomize: radomizing a position
        x: x coordinate
        y: y coordinate
        food_img: image source for the food object --> cookie image

    Prams: 
        game (Game): the instance of the game object

    Tests:
        1. check if the object: food in the class game was created
        2. check if the object food got a position with x and y coordinates

    
    Image Source:
        Cookie: https://imgbin.com/png/KtAD54ir/chocolate-chip-cookie-food-biscuits-emoji-png last call 05.06.2021
    """

    def __init__(self, game):
        try:
            self.game = game

            # set a randomized position -> x and y coordinate
            self.randomize()

            # preload and transforme image
            self.food_img = pygame.image.load("Images\Cookie.png")
            self.food_img = pygame.transform.scale(self.food_img, (self.game.grid_cell_size, self.game.grid_cell_size))

        except Exception as e:
            logging.error("Error occurred while food object creating", exc_info=True)


    def draw_food(self):
        """
        Description:
            draw the food object to the game_screen 

        Prams:
            none

        Returns:
            none

        Tests:
            1. check if the food object was printed on the game_screen with one position 
            2. check if the cookie image was printed to the game_screen
        """

        try:
            food_rect = pygame.Rect((self.pos.x * self.game.grid_cell_size), (self.pos.y * self.game.grid_cell_size), self.game.grid_cell_size, self.game.grid_cell_size)

            # adding the image to the rect and blit it on the screen
            self.game.game_screen.blit(self.food_img, food_rect)
        
        except Exception as e:
            logging.error("Error occurred when drawing food on the screen", exc_info=True)


    def randomize(self):
        """
        Desription:
            randomize the position (x and y coordinates) of the food object by randomizing two int values
            x --> random int between the frist grid and the last grid in x direction
            y --> random int between the frist grid and the last grid in y direction

        Params:
            none

        Returns:
            none

        Tests:
            1. check if the x coordinate is changed for each new food object
            2. check if the pos attribute got two coordinates, which change for a new food object
        """
        try:
            # ramdomize an int for x coordinate
            self.x = random.randint(1, self.game.grid_cell_count_x)

            # randomize an int for y coordinate
            self.y = random.randint(1, self.game.grid_cell_count_y)

            # set position to the randomized coordinates
            self.pos = Vector2(self.x, self.y)

            # check if food is on the position of a snake block, if true, randomize a new position
            for block in self.game.snake.body:
                if self.pos == block:
                    self.randomize()
        
        except Exception as e:
            logging.error("Error occurred while generate a randomized position for the object", exc_info=True)
    

    def randomize_effect(self):
        """
        Desription:
            generate a random number, to get a random effect out of 5 effects and do this effect

        Params:
            none

        Returns:
            none

        Tests:
            1. Check if the game.random_effect_status is reset after the function call
            2. check if a random number was generated and stored in effect_index
            3. check if the game.random_effec_message changes
        """

        try:
            # if random effect is requested return a random index for a random effect
            if self.game.random_effect_status == True:
                self.game.random_effect_status = False

                # generate random index, to choose a ramdom effect
                effect_index = random.randint( 0, 49)

                if effect_index < 10:
                    # set health loss up
                    self.game.healt_loss = 0.75

                    # change the random effect message
                    self.game.random_effect_message = "Your health - loss increased"
                    
                elif effect_index < 20:
                    # set health loss down
                    self.game.healt_loss = 0.25
                    
                    # change the random effect message
                    self.game.random_effect_message = "Your health - loss decreased"

                elif effect_index < 30:
                    # reset health loss
                    self.game.healt_loss = 0.5
                    
                    # lose half of current health
                    self.game.current_health = self.game.current_health / 2

                    # change the random effect message
                    self.game.random_effect_message = "Your current health - has been reduced - by half"

                elif effect_index < 40:
                    # reset health loss
                    self.game.healt_loss = 0.5
                    
                    # set Health to the double
                    if (self.game.current_health * 2) <= self.game.max_health:
                        self.game.current_health = self.game.current_health * 2
                    else:
                        # set it fix to maximum, so health can`t be greater than 100
                        self.game.current_health = self.game.max_health
                    
                    self.game.random_effect_message = "Your current health - was doubled"

                elif effect_index < 50:
                    # reset health loss and health regeneration
                    self.game.healt_loss = 0.5

                    # set the length of the snake to a third --> round it to an integer because the index
                    length = round(len(self.game.snake.body) / 3)
                    
                    # take the first body element until the length element and override the body with them
                    self.game.snake.body = self.game.snake.body[0:length]

                    self.game.random_effect_message = "The length of your - snake was reduced - by two thirds"


        except Exception as e:
            logging.error("Error occurred while activating a random effect", exc_info=True)
""" Python Evolving Snake game
    
    Description:
        Snake file includes snake class, a snake object is the "player" of the snake game

    Param:
        Author  : Simon Jess 
        Date    : 06.06.2021
        Version : 1.0.0 
        License : free
"""

import pygame
import logging

from pygame.math import Vector2

# Set config for logging
logging.basicConfig(format='%(asctime)s - %(message)s', filename='logs\\logfile.log', datefmt='%y-%m-%d %H:%M')

class Snake:
    """
    Description:
        The snake class is building the snake object, contains the body (position of the body blocks and the total length of the snake) and the direction of the snake

    Attributes:
        game : the game object which contains the snake
        body : the initial snake body and theire position
        direction : the initial direktion of the snake
        new_block : bool, which idicates the snake body getting a new block
        head_img : the image source for the head block
        body_img : the image source for the body blocks

    Prams:
        game (Game) : the game, which calls the snake constructor

    Returns:
        none

    Tests: 
        1. check if the snake object in game was created
        2. check if the inital body length is 3 blocks and it`s direction is downwards


    Image Source:
        Head: https://favpng.com/png_view/cookie-monster-cookie-monster-elmo-drawing-clip-art-png/BSB2vxN3 last call 05.06.2021
        Body: Selfmade from Head.png
    """

    def __init__(self, game):
        try:
            self.game = game

            # initial snake
            self.body = [Vector2(14,12), Vector2(14,11), Vector2(14,10)]

            # initial snake moving direction
            self.direction = Vector2(0,1)
            self.new_block = False

            # pre loading images --> better performance
            self.head_img = pygame.image.load("Images\Head.png")
            self.body_img = img = pygame.image.load("Images\Body.png")

            # pre transforming images
            self.head_img = pygame.transform.scale(self.head_img, (self.game.grid_cell_size, self.game.grid_cell_size))
            self.body_img = pygame.transform.scale(self.body_img, (self.game.grid_cell_size, self.game.grid_cell_size))

        except Exception as e:
            logging.error("Error occurred while creating a snake object", exc_info=True)


    def draw_snake(self):
        """
        Description:
            Create rect for Snake body and draw them on the screen, as well as filling the rect with the images for the body parts

        Params:
            none

        Returns:
            none

        Tests: 
            1. check if the images where loaded
            2. check if the snake body is printed to the game screen
        """

        try:
            for block in self.body:
                # body[0] <-- represents the head of the snake
                if block == self.body[0]:
                    block_rect = pygame.Rect((block.x * self.game.grid_cell_size) , (block.y * self.game.grid_cell_size), self.game.grid_cell_size , self.game.grid_cell_size)
                    self.game.game_screen.blit(self.head_img, block_rect)
                # body[1:], means each index until n starting at 1  <-- represents the body of the snake
                else:
                    block_rect = pygame.Rect((block.x * self.game.grid_cell_size) , (block.y * self.game.grid_cell_size), self.game.grid_cell_size , self.game.grid_cell_size)
                    self.game.game_screen.blit(self.body_img, block_rect)
        
        except Exception as e:
            logging.error("Error occurred while drawing the snake to the screen", exc_info=True)


    def move_snake(self):
        """
        Description:
            Moving the snake forward in the direction of the snakes direction
            if the snake growes, it also add a new block to the position of the last bodyblock the snake was befor

        Params:
            none

        Returns:
            none

        Tests: 
            1. check the position of the snake changes
            2. check if the snake grows 1 block if new_block is true
        """

        try:
            if(self.direction != (0,0)):
                if self.new_block == True:
                    # temp copy the full body
                    body_copy = self.body[:]

                    # Adding the new head by adding the direction vector to the first index
                    body_copy.insert(0, body_copy[0] + self.direction)

                    # set the body to the "new" temp body
                    self.body = body_copy[:]

                    # reset the new_block flag 
                    self.new_block = False
                else:
                    # temp copy the body without the last element 
                    body_copy = self.body[:-1]

                    # Adding the new head by adding the direction vector to the first index
                    body_copy.insert(0, body_copy[0] + self.direction)

                    # set the body to the "new" temp body
                    self.body = body_copy[:]

        except Exception as e:
            logging.error("Error occurred while moving the snakes body blocks positions", exc_info=True)
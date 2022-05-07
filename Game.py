""" Python Evolving Snake game
    
    Description:
        Game file includes game class, each instance of a game object is a new game 

    Param:
        Author  : Simon Jess 
        Date    : 06.06.2021
        Version : 1.0.0 
        License : free
"""

import pygame
import sys
import logging

from pygame.locals import *
from pygame.math import Vector2
from pygame import mixer

from Menu import *  
from Snake import *
from Food import *

# Set config for logging
logging.basicConfig(format='%(asctime)s - %(message)s', filename='logs\\logfile.log', datefmt='%y-%m-%d %H:%M')

# set used colors
darkgrey = (85,85,85)
black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)


class Game:
    """
    Description:
        create an object of the game, which controles the game functions and provide all functions to create a snake game
        Includes the game logic like collision detection and food snack detection
        aswell as all menu fuctions like the Buttons to controle the menu 

    Attributes:
        screen_height: height of the game window
        screen_width: width of the game window
        grid_cell_size: size of a grid cell --> one 1 grid has the size (grid_cell_size x grid_cell_size)
        grid_cell_count_x: number of grid_cells in x direction
        grid_cell_count_y: number of gid_cells in y direction
        sound_active: bool, which set sound on or off --> initial set on
        game_over_status: bool, which indicates the end of the game --> when turns true, the game is over
        healt_loss: the value, health is decreasing everytime
        health_bar_length: width of the healthbar 
        max_health: maximum health the snake game has
        current_health: the current health left on the healthbar
        highscore: the highscore calculated by current_health and food eaten
        play_area_x: the playarea width for the snake game
        play_area_y: the playarea height for the snake game
        game_screen: the displayed window with screen_height x screen_width as size
        background_img: background image
        restart_button_img: "restart" button image
        exit_button_img: "exit" button image
        start_button_img: "play" button image
        resume_button_img: "resume" button image
        pause_button_img: "pause" button image
        sound_on_img: "sound on"  button image
        sound_off_img: "sound off" button image
        snack_sound: soundfile for snack sound
        snake: instance of an object of the Snake class
        food: instance of an object of the Food class
        game_over_menu: instance on an object of the Menu class for the game over menu, when the game is over
        game_start_menu: instance on an object of the Menu class for the start menu, when game starts
        game_pause_menu: instance on an object of the Menu class for the pause menu, when the game is paused
        button_restart: button object for the "restart" button 
        button_start: button object for the "play" button
        button_exit: button object for the "exit" button
        button_resume: button object for the "resume" button
        button_pause: button object for the "pause" button
        button_sound_on: button object for the "sound on" button
        button_sound_off: button object for the "sound off" button

        random_effect_interval: every 250 Points a random effect appears
        ramdom_effect_status: flag, if random effect is activated or false
        random_effect_message: the message displayed for the player at the stats area

    Params:
        sound_active (bool): displayes if sound is set to on or set to off

    Returns:
        none
    
    Tests:
        1. check if the game class in the Main.py was created
        2. check if the initial values are set, like sound_active from Main.py in self.soud_active 


    Source:
        Images:
        background image: https://www.roundedhexagon.com/texture/polygonal-low-poly-41/ last call: 31.05.2021
        restart, exit, start, resume, pause button: Selfmade
        sound_on image: https://www.softicons.com/toolbar-icons/mono-general-icons-4-by-custom-icon-design/sound-icon + Selfmade   last call: 05.06.2021
        sound_off image: https://www.softicons.com/toolbar-icons/mono-general-icons-4-by-custom-icon-design/sound-off-icon + Selfmade    last call: 05.06.2021

        snack_sound: https://www.soundboard.com/sb/Cookie_Monster_Soundboard  last call: 04.06.2021
    """

    def __init__(self, sound_active):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        mixer.init()
        pygame.init()
        pygame.display.set_caption("Evolving Snake")

        # declare constants and references
        self.screen_height = 1000        #window height
        self.screen_width = 1500         #window width

        self.grid_cell_size = 40
        self.grid_cell_count_y = 23       # 23 blocks height - playarea
        self.grid_cell_count_x = 27       # 27 blocks width  - playarea

        self.sound_active = sound_active    # get from the main.py as parameter
        self.game_over_status = False       # default value --> game running --> True

        self.healt_loss = 0.5               # value of health loss
        self.health_bar_length = 200        # healthbar width
        self.max_health = 100               # maximum health 
        self.current_health = 100           # value of health --> inner healthbar width

        self.highscore = 0                  # highscore --> default 0

        self.play_area_x = self.screen_width - 420  # width of the playarea on the screen 
        self.play_area_y = self.screen_height - 80  # height of the playarea on the screen

        self.game_screen = pygame.display.set_mode((self.screen_width, self.screen_height)) # game screen/ window size of pygame 

        self.random_effect_interval= 250    # first random effect at Highscore = 250, than increase by 250 and so on
        self.random_effect_status = False   # Default False, set to true after reaching 250 Points
        self.random_effect_message = "No effect"    # Default there is no used effect

        # try load local data
        try:
            # load Images:
            self.background_img = pygame.image.load("Images\Background.png")
            self.restart_button_img = pygame.image.load("Images\\restart_btn.png")  
            self.exit_button_img = pygame.image.load("Images\exit_btn.png")         
            self.start_button_img = pygame.image.load("Images\start_btn.png")       
            self.resume_button_img = pygame.image.load("Images\\resume_btn.png")    
            self.pause_button_img = pygame.image.load("Images\pause.png")           
            
            self.sound_on_img = pygame.image.load("Images\sound_on.png")
            self.sound_off_img = pygame.image.load("Images\sound_off.png")

            self.controle_img = pygame.image.load("Images\\Controls.png")


            # Transform images to scale them to the expected size
            self.background_img = pygame.transform.scale(self.background_img, (self.screen_width, self.screen_height))
            self.restart_button_img = pygame.transform.scale(self.restart_button_img, (self.grid_cell_size * 5, self.grid_cell_size *2))
            self.exit_button_img = pygame.transform.scale(self.exit_button_img, (self.grid_cell_size * 5, self.grid_cell_size *2))
            self.start_button_img = pygame.transform.scale(self.start_button_img, (self.grid_cell_size * 5, self.grid_cell_size *2))
            self.resume_button_img = pygame.transform.scale(self.resume_button_img, (self.grid_cell_size * 5, self.grid_cell_size *2))
            self.pause_button_img = pygame.transform.scale(self.pause_button_img, (self.grid_cell_size * 5, self.grid_cell_size *2))

            self.sound_off_img = pygame.transform.scale(self.sound_off_img, (self.grid_cell_size * 5, self.grid_cell_size * 2))
            self.sound_on_img = pygame.transform.scale(self.sound_on_img, (self.grid_cell_size * 5, self.grid_cell_size * 2))

            self.control_img =  pygame.transform.scale(self.controle_img, (280, 100))

            # load Sound:
            self.snack_sound = pygame.mixer.Sound("Sounds\EatingSound.wav")
            
            # call function to set the sound to the expected status: on or off
            self.sound_volume()

        except Exception as e:
            logging.error("Error occurred while loading extern files", exc_info=True)

        # try create instances of an object for Snake, Food, Menu and Menu_Button
        try:
            # Create object instances
            self.snake = Snake(self)
            self.food = Food(self)

            # Create Menu objects for the Background 
            self.game_over_menu = Menu(self, red, 100)
            self.game_start_menu = Menu(self, white, 100)
            self.game_pause_menu = Menu(self, white, 100)


            # Create menu button objects and set theire position and image
            self.button_restart = Menu_Button(self.play_area_x / 2  -60, self.play_area_y / 2 - 100, self.restart_button_img,   self.game_screen)
            self.button_start   = Menu_Button(self.play_area_x / 2  -60, self.play_area_y / 2 - 100, self.start_button_img,     self.game_screen)
            self.button_exit    = Menu_Button(self.play_area_x / 2 - 60, self.play_area_y / 2 + 20,  self.exit_button_img,      self.game_screen)
            self.button_resume  = Menu_Button(self.play_area_x / 2 - 60, self.play_area_y / 2 - 220, self.resume_button_img,    self.game_screen)
            self.button_pause   = Menu_Button(self.screen_width - 290,   90,   self.pause_button_img,     self.game_screen)

            self.button_sound_on    = Menu_Button(self.screen_width - 290, self.screen_height - 320, self.sound_on_img,  self.game_screen)
            self.button_sound_off   = Menu_Button(self.screen_width - 290, self.screen_height - 320, self.sound_off_img, self.game_screen)

        except Exception as e:
            logging.error("Error occurred while trying to create object instances", exc_info=True)


    def update(self):
        """
        Description:
            call function to:
            - updating the position of snake by moving the snake
            - Check if the snake has eaten something
            - check if the snake has a collision 

        Params:
            none

        Returns:
            none

        Tests:
            1. check if snake has a new position after function call
            2. check if game still runs after check_collision function call -> game over or game still running
        """
        try:
            self.snake.move_snake()
            self.check_snack()
            self.check_collision()
        
        except Exception as e:
            logging.error("Error occurred when the display update functions where called", exc_info=True)


    def check_snack(self):
        """
        Description:
            When the snake collides with the food, a new position of the food is determined, sound is played and the snake grows by one block
            also the highscore is updated depending on the rest of the life display and the current healt is growing again

        Params:
            none

        Returns:
            none

        Tests:
            1. Check if the highscore changes when the snake eat some food and health is regenerated 
            2. Check if the food is displayed, with a new position on the playarea
        """
        try:
            # food position is snakes head position
            if self.food.pos == self.snake.body[0]:
                # play sound
                self.snack_sound.play()
                
                # generate new food position
                self.food.randomize()

                # indicate to add a new blcok
                self.snake.new_block = True
                
                # Increas Highscore 
                if self.current_health <= 25:
                    self.highscore += 75
                elif self.current_health <= 50:
                    self.highscore += 50
                else:
                    self.highscore += 25

                # Regenerate Health
                if self.current_health <= 90:
                    self.current_health += 10
                else:
                    self.current_health = 100

                # Call a random effect
                if self.highscore >= self.random_effect_interval:
                    self.random_effect_status = True
                    self.random_effect_interval += 250

                    # fucntion call
                    self.food.randomize_effect()


        except Exception as e:
            logging.error("Error occurred after snake ate food", exc_info=True)


    def update_health(self):
        """
        Description:
            Reduces the current health at each function call and as soon as they are 0, the game ends

        Params:
            none
        
        Returns:
            none

        Tests:
            1. Test, if health is 0 the game over screen appears
            2. check if the life indicator is falling continuously
        """

        try:
            # while the game is running, decrease the health every 150 ms 
            if self.current_health > 0:
                self.current_health -= self.healt_loss
            # when health is 0 --> end the game
            else:
                self.game_over()

        except Exception as e:
            logging.error("Error occurred while trying to update health", exc_info=True)


    def check_collision(self):
        """
        Description:
            - check collision between the snake obect and the border
            - check collision between snake head and any part of the snake body

        Params:
            none
        
        Returns:
            none

        Tests:
            1. Check, snake crashes a border and would "move" out of the playarea the game will end and game over screen appears
            2. Check, the snake head crashes the snake body will end the game and the game over screen appears
        """
        try:    
            # check collision between snake head and field boundaries
            if not 1 <= self.snake.body[0].x <= self.grid_cell_count_x or not 1 <= self.snake.body[0].y <= self.grid_cell_count_y: 
                self.game_over()

            # for each body block from 1 to n
            for block in self.snake.body[1:]:
                # head = (body[0]), check collision between body block and head
                if block == self.snake.body[0]:
                    self.game_over()

        except Exception as e:
            logging.error("Error occurred when a snake collision was detected", exc_info=True)


    def game_over(self):
        """
        Description:
            stop the snakes moving by setting the direction vector to (0,0), and set the game_over_status to True to indicate the end of the game

        Params:
            none

        Returns:
            none

        Tests:
            1. Prove the status of the game_over_status after function call
            2. Check the direction of the snake after function call, this should be changed from (1,0)/(0,1)/(-1,0)/(0,-1) to (0,0)
        """
        try:
            # set direction vector to (0,0) so the snake stops moving
            self.snake.direction = Vector2(0,0)

            # change the game status, to indicate the end of the game
            self.game_over_status = True
        
        except Exception as e:
            logging.error("Error occurred when game over was detected", exc_info=True)


    def game_quit(self):
        """
        Description:
            close the game window and exit pygame

        Params:
            none

        Returns:
            none

        Tests:
            1. After function call the game window will close
            2. Check if pygame is quitted
        """

        try:
            # quit pygame and close the game window
            pygame.quit()
            quit()

        except Exception as e:
            logging.error("Error occurred when game should be closed", exc_info=True)


    def draw_text(self, text, size, x, y, color):
        """
        Description:
            drawing individual text and it`s size and color to the game_screen with individual coordinates

        Params:
            text (String): the given text to display
            size (Int): the size of the text font
            x (Int): the x position/coordinate of the rect, which contains the text
            y (Int): the y position/coordinate of the rect, which contains the text
            color (RGB Tupel ([0-255],[0-255],[0-255])): the color in which the text should be displayed

        Returns:
            none

        Tests:
            1. Check if a rect is createt with the size of the rect of the text_surface
            2. Check if the text appears on the game_screen
        """

        try:
            # font settings
            font = pygame.font.SysFont("comicsans", size)
            text_surface = font.render(text, True, color)

            #get the size of the rect, for the given text
            text_rect = text_surface.get_rect()

            # centered positioning for the rect
            text_rect.center = (x,y)
            
            # fill the rect with the text and blit it to the game_screen 
            self.game_screen.blit(text_surface, text_rect)
        
        except Exception as e:
            logging.error("Error occurred while trying to display text on the screen", exc_info=True)


    def draw_elements(self):
        """ 
        Description:
            This method draws all fix objects on the screen, including the background image and the playarea and the grid of the playarea

        Params:
            none

        Returns: 
            none

        Tests:
            1. Check if the window has a backgoundimage
            2. Check if the Game shows an transparent area on the background, with a black grid on it


        Inspiration Source:
            Draw transparent rectangle: https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
        """

        try:
            # Backgroundimage 
            self.game_screen.blit(self.background_img, (0,0))

            # Background for the playarea
            play_area = pygame.Surface((self.play_area_x, self.play_area_y))
            # set transparency value
            play_area.set_alpha(230)
            play_area.fill(darkgrey)
            self.game_screen.blit(play_area, (40, 40))

            # The Stats on the right block
            score_block = pygame.Surface((300, self.screen_height-80))
            # set transparency value
            score_block.set_alpha(200)
            score_block.fill(black)
            self.game_screen.blit(score_block, (self.screen_width-340, 40))

            # Draw grid for play area
            i = 1
            while i <= self.grid_cell_count_x +1:    # draw vertical lines
                pygame.draw.line(self.game_screen, black, (self.grid_cell_size* i ,self.screen_height-40),(self.grid_cell_size* i, 40))
                i += 1

            i = 1
            while i <= self.grid_cell_count_y +1:    # draw horizontal lines 
                pygame.draw.line(self.game_screen, black, (40 ,self.grid_cell_size * i),(self.screen_width- 380, self.grid_cell_size * i))
                i += 1

        except Exception as e:
            logging.error("Error occurred while drawing the background", exc_info=True)


    def draw_stats(self):
        """
        Description:
            Drawing:
            - the Highscore display 
            - the health display
            - the lables 
            to the game_screen


        Params:
            none

        Returns:
            none

        Tests:
            1. Check if lable: "Highscore" is printed in the right stats area next to te playarea
            2. Check if the healthbare with a white border is printed to stats area

        Source:
            Controls_img: https://freepikpsd.com/media/2019/10/wasd-png-8-Transparent-Images.png  + selfmade
        """

        try:
            # draw text methode 
            self.draw_text("Highscore:", 40, self.play_area_x + 230, 220, white)
            self.draw_text(str(self.highscore), 40, self.play_area_x + 230, 250, white)

            # parse int to string
            tempstr = str(round(self.current_health))

            # draw text methode --> current health
            self.draw_text("Health: " + tempstr + "/100", 40, self.play_area_x + 230, 320,white)

            # drawing inner rect for the healthbar
            pygame.draw.rect(self.game_screen, (255, 255, 0), (self.play_area_x + 130, 350, self.current_health * 2, 20))
            
            # drawing outline for the healthbar with the parameter 2 at the end of the draw.rect 
            pygame.draw.rect(self.game_screen, (255, 255, 255), (self.play_area_x + 130, 350, self.max_health * 2, 20), 2)

            # draw text methode --> effect message
            message = self.random_effect_message.split("-")
            height = 420
            for msg in message:
                self.draw_text(msg, 40, self.play_area_x + 230, height, (255,255,0))
                height += 40

            # draw text methode
            self.draw_text("Sound on/off:", 34, self.play_area_x + 230, self.screen_height - 340, white)
            
            # draw text methode
            self.draw_text("Controls:", 34, self.play_area_x + 230, self.screen_height - 180, white)
            
            # create rect and set position to blit control_img into it
            control_rect = pygame.Rect(1170, self.screen_height - 150, 280, 100)
            self.game_screen.blit(self.control_img, control_rect)
            

        except Exception as e:
            logging.error("Error occurred while drawing gamestats on the screen", exc_info=True)


    def sound_volume(self):
        """
        Description:
            Toggles the sound on and off

        Params:
            none

        Returns:
            none

        Tests:
            1. sound_active = true  -> Check if the volume is on and sound is played, when food is eaten
            2. sound_active is not true -> Check if the volume of the sound is set to 0
        """

        try:
            if self.sound_active:
                # change sound volume to 0.25 --> game sound is on
                self.snack_sound.set_volume(0.25)
            else: 
                # change sound volumen to 0 --> game sound is off
                self.snack_sound.set_volume(0.0)
        
        except Exception as e:
            logging.error("Error occurred by changing sound volumen", exc_info=True)
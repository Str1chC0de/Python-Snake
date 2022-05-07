""" Python Evolving Snake game
    
    Description:
        Includes the main function called at the beginning of the program.
        The game loop is called here, which ensures that a game object is created and the game cyclically updates all changes and game events.


    Param:
        Author  : Simon Jess 
        Date    : 06.06.2021
        Version : 1.0.0 
        License : free
"""

import logging

from Game import *

# Set config for logging
logging.basicConfig(format='%(asctime)s - %(message)s', filename='logs\\logfile.log', datefmt='%y-%m-%d %H:%M')

# Tickrate of the UI 
clock = pygame.time.Clock()
tickrate = 60
game_speed = 150    

# Initial start the infinity game loop
game_pause = False
main_menu = True


def game_loop(game_pause, main_menu):
    """
    Description:
        while the game is not paused, this method is an infinity game loop, waiting for the events/user interaction to handle the game
        also drawing the game elements and updating the display 

    Params:
        game_pause (bool): bool, to check if the game is paused
        main_menu (bool): Bool to check if the game is already started, to not display the main menu

    Returm:
        none
        
    Tests:
        1. Game starts and the window displayes something
        2. The game can be exited with the quit X on the top right
    """


    sound_active = True                 # sound is default set on

    game = Game(sound_active)           # create game object instance
    temp_direction = Vector2(0,0)       # initial value of temp direction vector of the snake



    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, game_speed)    # timer can speed the game up or down

    try:
        while True:
            # eventlistener
            for event in pygame.event.get():
                # close the window
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


                # Screen update rate
                if event.type == SCREEN_UPDATE:
                    # updating the game everytime the timer force the Screenupdate --> move snake, check if food was eaten etc.
                    game.update()
                    
                    # only update the health if the game is running
                    if game_pause == False and main_menu == False and game.game_over_status == False:
                        game.update_health() 


                # Controles for the snake
                if event.type == pygame.KEYDOWN:
                    # Move up       - with "Arrow up" or "w"
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and game_pause == False and game.game_over_status == False:     
                        if game.snake.direction.y != 1:
                            # change direction vector
                            game.snake.direction = Vector2(0, -1)

                    # Move Right     - with "Arrow right" or "d"
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and game_pause == False and game.game_over_status == False:
                        if game.snake.direction.x != -1:
                            # change direction vector
                            game.snake.direction = Vector2(1, 0)

                    # Move Down     - with "Arrow down" or "s"
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and game_pause == False and game.game_over_status == False:
                        if game.snake.direction.y != -1:
                            # change direction vector
                            game.snake.direction = Vector2(0, 1)

                    # Move Left     - with "Arrow left" or "a"
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and game_pause == False and game.game_over_status == False:
                        if game.snake.direction.x != 1:
                            # change direction vector
                            game.snake.direction = Vector2(-1, 0)  


                # If sound is set on, sound will be set to off
                if game.button_sound_on.draw_Button():
                    
                    # move the sound button on rect out of screen, so there aren`t two rects on each other
                    game.button_sound_on.rect.x = 1500

                    # move the sound button off into position
                    game.button_sound_off.rect.x = game.screen_width - 290

                    # change bool
                    sound_active = False
                    game.sound_active = False

                    # update the volume
                    game.sound_volume()
                    
                # If sound is set off, sound will be set to on
                elif game.button_sound_off.draw_Button():

                    # move the sound button on into position
                    game.button_sound_on.rect.x = game.screen_width - 290

                    # move the sound button off rect out of screen, so there aren`t two rects on each other
                    game.button_sound_off.rect.x = 1500

                    # change bool
                    sound_active = True
                    game.sound_active = True

                    # update the volume
                    game.sound_volume()

                # Open the Pause Menu and pause the game, when the pause button is clicked
                if game.button_pause.draw_Button():
                    game_pause = True

                    # save direction to resume to game, we need the direction Vector befor pausing game
                    temp_direction = game.snake.direction

                    # stop the snake, with direction Vector (0,0) --> no movement will ahppen
                    game.snake.direction = Vector2(0,0)


            draw_screen(game, sound_active)


            # Open the Main Menu when the game was started
            if main_menu == True:
                # stop snake movement
                game.snake.direction = Vector2(0,0)

                # draw buttons
                game.button_start.draw_Button()
                game.button_exit.draw_Button()

                for event in pygame.event.get():
                    # Close window
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    # waiting for mouse click to leave main menu with set the variable to false
                    if game.button_start.draw_Button():
                        game = Game(sound_active)
                        main_menu = False

                    # When the exit button was clicked --> close the pygame window
                    if game.button_exit.draw_Button():
                        pygame.quit()
                        quit()

            # Draw the game elements
            else:
                # call the health function and the clock, draw the rest of the game elements    
                if(game_pause == False and game.game_over_status == False):
                    game.snake.draw_snake()
                    game.food.draw_food()          
                    
                    game.button_pause.draw_Button()

                    # timer tick
                    clock.tick(tickrate)

                # open the pause menu
                elif(game_pause == True and game.game_over_status == False):
                    game.snake.draw_snake()
                    game.food.draw_food()
                    
                    game.game_pause_menu.blit_background()

                    game.button_restart.draw_Button()
                    game.button_resume.draw_Button()
                    game.button_exit.draw_Button()

                    # When the window is closed, quit pygame
                    for event in pygame.event.get():
                        # When the exit button was clicked --> close the pygame window
                        if event.type == pygame.QUIT or game.button_exit.draw_Button():
                            pygame.quit()
                            quit()

                        # When the restart button got clicked --> reset game object instance to restart game
                        if game.button_restart.draw_Button():
                            game_pause = False
                            game = Game(sound_active)

                        # Unpause the game and set the direction vector to the direction vector from before
                        if game.button_resume.draw_Button():
                            game_pause = False
                            # set direction vector to the direction vectore befor pausing the game
                            game.snake.direction = temp_direction

                # open the game over menu
                elif(game_pause == False and game.game_over_status == True):
                        game.game_over_menu.blit_background()

                        # Draw buttons on the game play area
                        game.button_restart.draw_Button()
                        game.button_exit.draw_Button()
                    
                        # When the window is closed, quit pygame
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                quit()

                            # When the restart button got clicked --> reset game object instance to restart game
                            if game.button_restart.draw_Button():
                                # create new game object --> creating a new game --> simulates a restart
                                game = Game(sound_active)

                            # When the exit button was clicked --> close the pygame window
                            if game.button_exit.draw_Button():
                                pygame.quit()
                                quit()  

            pygame.display.flip()
        
    except Exception as e:
        logging.error("Error occurred in the gameloop", exc_info=True)


def draw_screen(game, sound_active):
    """
    Description:
        calling the draw functions of the background for the playarea and the game stats 

    Params:
        game (game): instance of the game object
        sound_active (bool): saving the status if sound is on or off

    Return: 
        none

    Tests:
        1. Highscore and Healtbare are displayed in the slightly transparent right bar
        2. Sound off OR sound on icon is displayed on the bottom slightly transparent of the right bar
    """
    try:
        # draw elements, stats and buttons on the screen
        game.draw_elements()
        game.draw_stats()

        if sound_active ==  True:
            game.button_sound_on.draw_Button()
        elif sound_active == False:
            game.button_sound_off.draw_Button()
    
    except Exception as e:
        logging.error("Error occurred while drawing the elements", exc_info=True)


if __name__ == "__main__":
    # call the gameloop and set parameters
    game_loop(game_pause, main_menu)
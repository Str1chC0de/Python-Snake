# Evolving Snake

## Requirements:
* **OS:** Windows 10 and Visual Studio Code
* **Python Version:** python == 3.9.5 
<br><br>
* pygame == 2.0.1
* logging== 0.4.9.6

## How to play the game:
Here is explained what must be given so that the game can be executed and how it can then be executed

**1) Install required libraries:** <br>
    ```$ pip install pygame```<br>
    ```$ pip install logging ``` <br>
    or  <br>
    ```$ pip install -r Requirements.txt ```


**2) Run the game script:** <br>
    ```$ python Main.py ```

**3) Game controles:** <br>
To control the snake, you can use W A S D but also the arrow keys.
All other interactions take place via mouse clicks on the corresponding blue buttons.

## Game description:
The game is a slight variation of Snake. The gameplay is that of snake. 
You control a cookie monster, which grows longer as soon as it eats a cookie.
As soon as you touch your own body or the borders of the playing area, you "die" and the game is over.

The extensions to this normal game principle is the time factor. During the game you continuously lose
lives. With each cookie eaten, you regenerate a fixed number of lives. As soon as the life bar drops to
zero,the game is over. Depending on the current health, the highscore is increased when eating a cookie.
Furthermore, every time the highscore has increased by 250, a randomly selected effect from 5 effects is
triggered. These include: faster life loss, slower life loss, direct life loss, direct life regeneration
but also the shortening of the snake by a factor of 2/3.



## Bugs I know about:
* sometimes the button to toggle the sound on/off status click is not changing the status. In this case just click again until the button aka. the image changes.
  Most times, this happens in the Menues
* sometimes if more than one Key is pressed, the game detectes a game over and the game ends
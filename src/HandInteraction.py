import cv2
import pygame
from Screen.Game import Game
from Screen.Menu import Menu
from Sprites.Menu.Logo import Logo

# Declare screen and cv dimensions
wCam = 640
hCam = 480
# Configure the camera and its dimensions
cap = cv2.VideoCapture(0)
# Dimensions of camera
cap.set(3, wCam)
cap.set(4, hCam)
# Screen change variables
in_menu = True
in_game = False
# Creating the sprites
logo_sprite = Logo(150, 150)
# Set up pygame
pygame.init()
pygame.mixer.init()
# Background music
pygame.mixer.music.load('resources/Audio/artblock.ogg')
# Window information
pygame.display.set_icon(logo_sprite.logo)
pygame.display.set_caption("Joty says")
# Cursor from pygame to access the functions of it
cursor = pygame.mouse
# Customizing the cursor
cursor.set_cursor(pygame.SYSTEM_CURSOR_HAND)
# Game and Menu setups
menu = Menu(cursor=cursor)
game = Game(cursor=cursor)
pygame.mixer.music.play()

while cap.isOpened():
    if in_menu:
        in_menu = menu.start_menu(cap)
        in_game = False if in_menu else True
    elif in_game:
        # set volume of the background_music
        pygame.mixer.music.set_volume(0.30)
        in_game = game.start_game(cap)
    else:
        break

pygame.quit()
cap.release()
cv2.destroyAllWindows()

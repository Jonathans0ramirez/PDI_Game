import cv2
import pygame
from Screen.Game import Game
from Screen.Menu import Menu
from Sprites.Menu.Logo import Logo
from src.Enums.ApplicationState import ApplicationState


class HandInteractor:
    def __init__(self):
        # Declare screen and cv dimensions
        self.wCam = 640
        self.hCam = 480
        # Screen change variables
        self.in_menu = ApplicationState.RUNNING
        self.in_game = ApplicationState.BREAK
        self.in_game_over = ApplicationState.BREAK
        # Creating the sprites
        self.logo_sprite = Logo(150, 150)
        # Cursor from pygame to access the functions of it
        self.cursor = pygame.mouse


def main():
    interactor = HandInteractor()
    # Configure the camera and its dimensions
    cap = cv2.VideoCapture(0)
    # Dimensions of camera
    cap.set(3, interactor.wCam)
    cap.set(4, interactor.hCam)
    # Set up pygame
    pygame.init()
    pygame.mixer.init()
    # Background music
    pygame.mixer.music.load('resources/Audio/artblock.ogg')
    # Window information
    pygame.display.set_icon(interactor.logo_sprite.logo)
    pygame.display.set_caption("Joty says")
    # Customizing the cursor
    interactor.cursor.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    # Game and Menu setups
    menu = Menu(cursor=interactor.cursor)
    game = Game(cursor=interactor.cursor)
    # Background music
    pygame.mixer.music.play()
    while cap.isOpened():
        if interactor.in_menu == ApplicationState.RUNNING:
            interactor.in_menu = menu.start_menu(cap)
            interactor.in_game = ApplicationState.BREAK if \
                interactor.in_menu == ApplicationState.RUNNING else \
                ApplicationState.RUNNING
        elif interactor.in_game == ApplicationState.RUNNING:
            # set volume of the background_music
            pygame.mixer.music.set_volume(0.30)
            interactor.in_game = game.start_game(cap)
        if (interactor.in_menu == ApplicationState.STOP) or \
                (interactor.in_game == ApplicationState.STOP) or \
                ((interactor.in_menu == ApplicationState.BREAK) and (interactor.in_game == ApplicationState.BREAK)):
            break

    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

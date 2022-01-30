import cv2
import pygame
from Screen.Game import Game
from Screen.Menu import Menu
from Sprites.Menu.Logo import Logo
from src.Screen.GameOver import GameOver
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
        # Score copy
        self.score = 0


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
    # pygame.mixer.music.load('resources/Audio/artblock.ogg')
    pygame.mixer.music.load('resources/Audio/Cyberpunk Moonlight Sonata v2.mp3')
    # Window information
    pygame.display.set_icon(interactor.logo_sprite.logo)
    pygame.display.set_caption("Joty says")
    # Customizing the cursor
    interactor.cursor.set_cursor(pygame.SYSTEM_CURSOR_HAND)
    # Game and Menu setups
    menu = Menu(cursor=interactor.cursor)
    game = Game(cursor=interactor.cursor)
    game_over = GameOver(cursor=interactor.cursor)
    # Background music
    pygame.mixer.music.play(loops=-1)
    while cap.isOpened():
        # Handle music function
        interactor.in_menu, interactor.in_game, interactor.in_game_over = handle_music(interactor.in_menu,
                                                                                       interactor.in_game,
                                                                                       interactor.in_game_over,
                                                                                       pygame.mixer.music)
        if interactor.in_menu == ApplicationState.RUNNING:
            interactor.score = 0
            interactor.in_menu = menu.start_menu(cap)
            interactor.in_game = ApplicationState.BREAK if \
                interactor.in_menu == ApplicationState.RUNNING else \
                ApplicationState.RUNNING
        elif interactor.in_game == ApplicationState.RUNNING:
            interactor.in_game, interactor.score = game.start_game(cap)
            interactor.in_game_over = ApplicationState.BREAK if \
                interactor.in_game == ApplicationState.RUNNING else \
                ApplicationState.RUNNING
        elif interactor.in_game_over == ApplicationState.RUNNING:
            interactor.in_game_over = game_over.lose_screen(cap, interactor.score)
            if interactor.in_game_over == ApplicationState.RESTART:
                interactor.in_menu = ApplicationState.RUNNING
                interactor.in_game = ApplicationState.BREAK
                interactor.in_game_over = ApplicationState.BREAK
                pygame.mixer.music.load('resources/Audio/Cyberpunk Moonlight Sonata v2.mp3')
                pygame.mixer.music.play(loops=-1)
                pygame.mixer.music.set_volume(1)
        if (interactor.in_menu == ApplicationState.STOP) or \
                (interactor.in_game == ApplicationState.STOP) or \
                (interactor.in_game_over == ApplicationState.STOP) or \
                (
                        (interactor.in_menu == ApplicationState.BREAK) and
                        (interactor.in_game == ApplicationState.BREAK) and
                        (interactor.in_game_over == ApplicationState.BREAK)
                ):
            break

    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()


def handle_music(in_menu, in_game, in_game_over, pygame_music):
    if in_menu == ApplicationState.MUSIC_BREAK:
        pygame_music.set_volume(0.30)
        in_menu = ApplicationState.BREAK
    if in_game == ApplicationState.MUSIC_BREAK:
        pygame_music.load('resources/Audio/game_over_sound.ogg')
        pygame_music.play(loops=-1)
        pygame_music.set_volume(1)
        in_game = ApplicationState.BREAK
    if in_game_over == ApplicationState.MUSIC_BREAK:
        pygame_music.set_volume(0)
        in_game_over = ApplicationState.BREAK
    return in_menu, in_game, in_game_over


if __name__ == "__main__":
    main()

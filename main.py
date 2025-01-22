import pygame
from game import Game
from settings import WIDTH, HEIGHT, FPS
from menu import MainMenu

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Batty Game")

    clock = pygame.time.Clock()
    menu = MainMenu(screen)
    game = Game(screen)

    current_state = "menu"  # Текущее состояние: "menu" или "game"

    running = True
    while running:
        if current_state == "menu":
            action = menu.handle_events()
            menu.draw()

            if action == "start_game":
                current_state = "game"
                game.reset_game()  # Сброс игры перед началом
            elif action == "quit":
                running = False

        elif current_state == "game":
            action = game.handle_events()
            if action == "menu":  # Если нажат ESC и выбрано "Да", вернуться в меню
                current_state = "menu"
                game.show_exit_dialog = False  # Сброс диалога
            else:
                running = game.update()
                game.draw()

                if game.lives == 0:  # Если игра окончена, вернуться в меню
                    current_state = "menu"

        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
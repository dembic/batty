import pygame
from settings import WIDTH, HEIGHT, WHITE, BLACK, FONT_SIZE

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.options = ["Начать игру", "Настройки", "Выход"]
        self.selected_option = 0
        self.show_exit_dialog = False  # Показывать ли диалог выхода
        self.dialog_options = ["Да", "Нет"]
        self.selected_dialog_option = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if self.show_exit_dialog:
                    # Обработка событий для диалога выхода
                    if event.key == pygame.K_LEFT:
                        self.selected_dialog_option = (self.selected_dialog_option - 1) % len(self.dialog_options)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_dialog_option = (self.selected_dialog_option + 1) % len(self.dialog_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_dialog_option == 0:  # Выбрано "Да"
                            return "quit"
                        else:  # Выбрано "Нет"
                            self.show_exit_dialog = False
                else:
                    # Обработка событий для главного меню
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_option == 0:
                            return "start_game"
                        elif self.selected_option == 1:
                            return "settings"
                        elif self.selected_option == 2:
                            self.show_exit_dialog = True  # Показать диалог выхода
                    elif event.key == pygame.K_ESCAPE:
                        self.show_exit_dialog = True  # Показать диалог выхода при нажатии ESC
        return None

    def draw(self):
        self.screen.fill(BLACK)
        if self.show_exit_dialog:
            # Отрисовка диалога выхода
            text_surface = self.font.render("Вы уверены, что хотите выйти?", True, WHITE)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            self.screen.blit(text_surface, text_rect)

            for i, option in enumerate(self.dialog_options):
                color = WHITE if i == self.selected_dialog_option else (128, 128, 128)
                text_surface = self.font.render(option, True, color)
                text_rect = text_surface.get_rect(center=(WIDTH // 2 + (i - 0.5) * 100, HEIGHT // 2 + 50))
                self.screen.blit(text_surface, text_rect)
        else:
            # Отрисовка главного меню
            for i, option in enumerate(self.options):
                color = WHITE if i == self.selected_option else (128, 128, 128)
                text_surface = self.font.render(option, True, color)
                text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
                self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
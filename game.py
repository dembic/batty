# game.py

import pygame
import random
from settings import *
from objects import *
from utils import draw_text, load_sounds, play_music  # Импорт функций из utils.py

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.bat = Bat()
        self.ball = Ball()
        self.level = 0
        self.tiles = self.create_tiles()
        self.bonus = Bonus()
        self.score = 0
        self.lives = 3
        self.balls = [self.ball]
        self.explosions = []
        self.bonus_effects = []
        self.bonus_texts = []  # Список для хранения текстов бонусов
        self.sounds = load_sounds()
        self.paused = False
        self.show_exit_dialog = False
        self.dialog_options = ["Да", "Нет"]
        self.selected_dialog_option = 0

        # Таймеры для бонусов
        self.bat_extend_timer = 0  # Таймер для расширения платформы
        self.slow_ball_timer = 0  # Таймер для замедления мяча
        self.speed_up_timer = 0  # Таймер для ускорения мяча
        self.invisibility_timer = 0  # Таймер для невидимости платформы

        # Сохраняем исходные значения
        self.original_bat_width = self.bat.width
        self.original_ball_speed = self.ball.speed.copy()
        play_music()

    def create_tiles(self):
        """Создание массива плиток."""
        tiles = []
        for row in range(6):  # 6 рядов плиток
            for col in range(8):  # 8 плиток в ряду
                tile_data = random.choice(LEVELS[self.level]["tiles"])
                x = col * (TILE_WIDTH + TILE_PADDING) + TILE_PADDING
                y = row * (TILE_HEIGHT + TILE_PADDING) + TILE_OFFSET_Y
                tiles.append(Tile(x, y, tile_data["color"], tile_data["hits"]))
        return tiles

    def handle_events(self):
        """Обработка событий."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.show_exit_dialog:
                    # Обработка событий для диалога выхода
                    if event.key == pygame.K_LEFT:
                        self.selected_dialog_option = (self.selected_dialog_option - 1) % len(self.dialog_options)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_dialog_option = (self.selected_dialog_option + 1) % len(self.dialog_options)
                    elif event.key == pygame.K_RETURN:
                        if self.selected_dialog_option == 0:  # Выбрано "Да"
                            return "menu"  # Возврат в главное меню
                        else:  # Выбрано "Нет"
                            self.show_exit_dialog = False
                            self.paused = False  # Снимаем паузу
                else:
                    # Обработка событий для игры
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    elif event.key == pygame.K_ESCAPE:
                        self.show_exit_dialog = True  # Показать диалог выхода
                        self.paused = True  # Ставим игру на паузу
            return True

    def draw_exit_dialog(self):
        """Отрисовка диалога выхода."""
        dialog_width = 400
        dialog_height = 200
        dialog_x = (WIDTH - dialog_width) // 2
        dialog_y = (HEIGHT - dialog_height) // 2

        # Отрисовка фона диалога
        pygame.draw.rect(self.screen, BLACK, (dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(self.screen, WHITE, (dialog_x, dialog_y, dialog_width, dialog_height), 2)

        # Отрисовка текста
        draw_text(self.screen, "Вы хотите вернуться в главное меню?", dialog_x + 10, dialog_y + 50, font_size=30)

        # Отрисовка кнопок
        for i, option in enumerate(self.dialog_options):
            color = WHITE if i == self.selected_dialog_option else (128, 128, 128)
            draw_text(self.screen, option, dialog_x + 100 + i * 150, dialog_y + 120, color=color, font_size=30)

    def update(self):
        """Обновление состояния игры."""
        if self.paused or self.show_exit_dialog:  # Если игра на паузе или открыт диалог
            return True

        current_time = pygame.time.get_ticks()

        # Отмена эффекта расширения платформы
        if self.bat_extend_timer and current_time >= self.bat_extend_timer:
            self.bat.width = self.original_bat_width  # Возвращаем исходную ширину
            self.bat.is_extended = False  # Сбрасываем флаг расширения
            self.bat_extend_timer = 0  # Сбрасываем таймер

        # Отмена эффекта замедления мяча
        if self.slow_ball_timer and current_time >= self.slow_ball_timer:
            for ball in self.balls:
                ball.speed[0] = self.original_ball_speed[0]
                ball.speed[1] = self.original_ball_speed[1]
            self.slow_ball_timer = 0  # Сбрасываем таймер

        # Отмена эффекта ускорения мяча
        if self.speed_up_timer and current_time >= self.speed_up_timer:
            for ball in self.balls:
                ball.speed[0] = self.original_ball_speed[0]
                ball.speed[1] = self.original_ball_speed[1]
            self.speed_up_timer = 0  # Сбрасываем таймер

        # Отмена эффекта невидимости платформы
        if self.invisibility_timer and current_time >= self.invisibility_timer:
            self.bat_visible = True  # Возвращаем видимость платформы
            self.invisibility_timer = 0  # Сбрасываем таймер

        # Обновление текстов бонусов
        for bonus_text in self.bonus_texts[:]:
            bonus_text.update()
            if bonus_text.is_exploded and all(particle["life"] <= 0 for particle in bonus_text.particles):
                self.bonus_texts.remove(bonus_text)  # Удаляем текст, если анимация завершена

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.bat.move_left()
        if keys[pygame.K_RIGHT]:
            self.bat.move_right()

        for ball in self.balls:
            ball.update()

        self.check_collisions()
        return True

    def check_collisions(self):
        """Проверка столкновений."""
        for ball in self.balls:
            # Отскок мяча от стен
            if ball.pos[0] <= ball.radius or ball.pos[0] >= WIDTH - ball.radius:
                ball.speed[0] = -ball.speed[0]
            if ball.pos[1] <= ball.radius:
                ball.speed[1] = -ball.speed[1]

            # Проверка столкновения мяча с платформой
            if (self.bat.pos[0] <= ball.pos[0] <= self.bat.pos[0] + self.bat.width) and (
                ball.pos[1] >= self.bat.pos[1] - ball.radius
            ):
                relative_intersect_x = (self.bat.pos[0] + (self.bat.width / 2)) - ball.pos[0]
                normalized_intersect_x = relative_intersect_x / (self.bat.width / 2)
                ball.speed[0] = -normalized_intersect_x * 5
                ball.speed[1] = -abs(ball.speed[1])
                self.score += 1
                self.sounds["hit"].play()
                self.bat.jump = 10

                # Создаем бонус с вероятностью 10%
                if random.randint(1, 10) == 1:
                    self.bonus.active = True
                    self.bonus.pos = [random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 200)]

            # Проверка столкновения мяча с плитками
            for tile in self.tiles[:]:
                if tile.active and tile.rect.colliderect(
                    pygame.Rect(ball.pos[0] - ball.radius, ball.pos[1] - ball.radius, ball.radius * 2, ball.radius * 2)
                ):
                    tile.hits -= 1
                    if tile.hits <= 0:
                        tile.active = False
                        self.explosions.append(TileExplosion(tile.rect.centerx, tile.rect.centery))
                    ball.speed[1] = -ball.speed[1]
                    self.score += 10
                    self.sounds["hit"].play()

            # Проверка столкновения мяча с бонусом
            if self.bonus.active:
                distance = ((ball.pos[0] - self.bonus.pos[0]) ** 2 + (ball.pos[1] - self.bonus.pos[1]) ** 2) ** 0.5
                if distance <= ball.radius + self.bonus.radius:
                    self.activate_bonus(random.choice(BONUS_TYPES))
                    self.bonus.active = False
                    self.bonus_effects.append(BonusEffect(self.bonus.pos[0], self.bonus.pos[1]))

            # Проверка проигрыша (мяч ушел за платформу)
            if ball.pos[1] >= HEIGHT - ball.radius:
                self.lives -= 1
                self.explosions.append(TileExplosion(ball.pos[0], ball.pos[1]))
                self.sounds["lose"].play()

                # Удаляем все мячи, кроме одного
                if len(self.balls) > 1:
                    self.balls = [self.balls[0]]  # Оставляем только первый мяч

                # Сброс позиции оставшегося мяча
                self.balls[0].pos = [WIDTH // 2, HEIGHT // 2]
                self.balls[0].speed = LEVELS[self.level]["ball_speed"]

                if self.lives == 0:
                    self.game_over()

    def activate_bonus(self, bonus_type):
        """Активация бонуса."""
        if bonus_type == "extend_bat":
            self.bat.width *= 1.5  # Увеличиваем ширину платформы
            self.bat.is_extended = True  # Устанавливаем флаг расширения
            self.bat_extend_timer = pygame.time.get_ticks() + 30000  # Устанавливаем таймер на 30 секунд
            self.bonus_texts.append(BonusText(self.bonus.pos[0], self.bonus.pos[1], "Расширение платформы!"))
        elif bonus_type == "slow_ball":
            for ball in self.balls:
                ball.speed[0] *= 0.5
                ball.speed[1] *= 0.5
            self.slow_ball_timer = pygame.time.get_ticks() + 30000  # Устанавливаем таймер на 30 секунд
            self.bonus_texts.append(BonusText(self.bonus.pos[0], self.bonus.pos[1], "Замедление мяча!"))
        elif bonus_type == "extra_life":
            self.lives += 1  # Бонус на жизнь не требует таймера
            self.bonus_texts.append(BonusText(self.bonus.pos[0], self.bonus.pos[1], "+1 жизнь!"))
        elif bonus_type == "speed_up":
            for ball in self.balls:
                ball.speed[0] *= 1.5
                ball.speed[1] *= 1.5
            self.speed_up_timer = pygame.time.get_ticks() + 30000  # Устанавливаем таймер на 30 секунд
            self.bonus_texts.append(BonusText(self.bonus.pos[0], self.bonus.pos[1], "Ускорение мяча!"))
        elif bonus_type == "multi_ball":
            for _ in range(2):
                new_ball = Ball()
                new_ball.pos = self.ball.pos.copy()
                new_ball.speed = [random.choice([-5, 5]), random.choice([-5, 5])]
                self.balls.append(new_ball)
            self.bonus_texts.append(BonusText(self.bonus.pos[0], self.bonus.pos[1], "Мульти-мяч!"))
        elif bonus_type == "invisibility":
            self.bat_visible = False
            self.invisibility_timer = pygame.time.get_ticks() + 30000  # Устанавливаем таймер на 30 секунд
            self.bonus_texts.append(BonusText(self.bonus.pos[0], self.bonus.pos[1], "Невидимость!"))

        self.sounds["bonus"].play()

    def game_over(self):
        """Завершение игры."""
        self.screen.fill(BLACK)
        draw_text(self.screen, f"Игра окончена! Ваш счет: {self.score}", WIDTH // 2 - 150, HEIGHT // 2 - 50)
        draw_text(self.screen, "Нажмите ПРОБЕЛ, чтобы сыграть снова", WIDTH // 2 - 250, HEIGHT // 2)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        self.reset_game()

    def reset_game(self):
        """Сброс игры."""
        self.score = 0
        self.lives = 3
        self.level = 0
        self.balls = [self.ball]
        self.tiles = self.create_tiles()
        self.bonus.active = False
        self.ball.pos = [WIDTH // 2, HEIGHT // 2]
        self.ball.speed = LEVELS[self.level]["ball_speed"]
        self.bat.pos = [WIDTH // 2 - self.bat.width // 2, HEIGHT - 50]

    def draw(self):
        """Отрисовка всех объектов."""
        self.screen.fill(BLACK)
        for tile in self.tiles:
            tile.draw(self.screen)
        self.bat.draw(self.screen)
        for ball in self.balls:
            ball.draw(self.screen)
        self.bonus.draw(self.screen)

        for explosion in self.explosions[:]:
            explosion.update()
            explosion.draw(self.screen)
            if all(particle["life"] <= 0 for particle in explosion.particles):
                self.explosions.remove(explosion)

        for effect in self.bonus_effects[:]:
            effect.update()
            effect.draw(self.screen)
            if all(particle["life"] <= 0 for particle in effect.particles):
                self.bonus_effects.remove(effect)
        # Отрисовка текстов бонусов
        for bonus_text in self.bonus_texts:
            bonus_text.draw(self.screen)

        draw_text(self.screen, f"Очки: {self.score}", 10, 10)
        draw_text(self.screen, f"Жизни: {self.lives}", WIDTH - 150, 10)
        draw_text(self.screen, f"Уровень: {self.level + 1}", WIDTH // 2 - 50, 10)

        if self.paused or self.show_exit_dialog:  # Если игра на паузе или открыт диалог
            draw_text(self.screen, "Пауза", WIDTH // 2 - 50, HEIGHT // 2, font_size=50)

        if self.show_exit_dialog:
            self.draw_exit_dialog()  # Отрисовка диалога выхода

        def reset_game(self):
            """Сброс игры."""
            self.score = 0
            self.lives = 3
            self.level = 0
            self.balls = [self.ball]
            self.tiles = self.create_tiles()
            self.bonus.active = False
            self.ball.pos = [WIDTH // 2, HEIGHT // 2]
            self.ball.speed = LEVELS[self.level]["ball_speed"]
            self.bat.pos = [WIDTH // 2 - self.bat.width // 2, HEIGHT - 50]

        pygame.display.flip()
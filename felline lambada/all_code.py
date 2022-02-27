# Add background image and music

import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


class Cat:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/cat.png").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 19) * SIZE
        self.y = random.randint(1, 11) * SIZE


class Main_cat:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/new_cat.png").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Game:

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Feline lambada')
        pygame.mixer.init()
        self.play_background_music()
        self.surface = pygame.display.set_mode((800, 500))
        self.main_cat = Main_cat(self.surface)
        self.main_cat.draw()
        self.cat = Cat(self.surface)
        self.cat.draw()

    def play_background_music(self):
        pygame.mixer.music.load('resources/ламбада.mp3')
        pygame.mixer.music.set_volume(0.3)

    def play_sound(self, sound_name):
        if sound_name == 'пр1':
            sound = pygame.mixer.Sound("resources/пр1.mp3")
        elif sound_name == 'котхрип':
            sound = pygame.mixer.Sound("resources/котхрип.mp3")
            sound.set_volume(2)

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.main_cat = Main_cat(self.surface)
        self.cat = Cat(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/new_floor.png")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.main_cat.walk()
        self.cat.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.main_cat.x[0], self.main_cat.y[0], self.cat.x, self.cat.y):
            self.play_sound("котхрип")
            self.main_cat.increase_length()
            self.cat.move()

        for i in range(3, self.main_cat.length):
            if self.is_collision(self.main_cat.x[0], self.main_cat.y[0], self.main_cat.x[i], self.main_cat.y[i]):
                self.play_sound('пр1')
                raise

    def display_score(self):
        font = pygame.font.SysFont('Georgia', 30)
        score = font.render(f"Счет: {self.main_cat.length}", True, (0, 0, 0))
        self.surface.blit(score, (680, 15))  # координаты надписи счет

    def show_game_over(self):
        black = (0, 0, 0)
        self.render_background()
        font = pygame.font.SysFont('Georgia', 25)
        line1 = font.render(f"Игра окончена! Вас счет {self.main_cat.length}.", True, black)
        self.surface.blit(line1, (10, 230))
        line2 = font.render("Чтобы начать заново нажмите Enter. Чтобы выйти нажмите Escape!", True, black)
        self.surface.blit(line2, (10, 275))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        pause = False
        end_it = False
        cat_hor = pygame.mixer.Sound('resources/хоркотов.mp3')
        cat_hor_stop = cat_hor.play()
        pygame.mixer.music.set_volume(0.3)
        while (end_it == False):
            bg = pygame.image.load("resources/zast.png")
            bgz = pygame.transform.scale(bg, (800, 500))
            self.surface.blit(bgz, (0, 0))
            myfont = pygame.font.SysFont("Georgia", 30)
            nlabel = myfont.render("Нажмите Enter, чтобы начать игру", 1, (0, 0, 0))
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        end_it = True
                        cat_hor_stop.pause()
                        pygame.mixer.music.play()
            self.surface.blit(nlabel, (100, 400))
            pygame.display.flip()

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.main_cat.move_left()

                        if event.key == K_RIGHT:
                            self.main_cat.move_right()

                        if event.key == K_UP:
                            self.main_cat.move_up()

                        if event.key == K_DOWN:
                            self.main_cat.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)


if __name__ == '__main__':
    game = Game()
    game.run()

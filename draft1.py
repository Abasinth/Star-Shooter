import pygame
from pygame import *
import random
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PASTEL_RED = (255, 105, 97)
MAGENTA_RED = (194, 30, 86)
TOMATO = (255,99,71)
SCARLET = (86, 3, 25)
PINK = (255, 105, 180)
BLUE = (0, 0, 255)
LIME_GREEN = (50, 205, 50)
SKY_BLUE = (135, 206, 235)
TURQUOISE = (175, 238, 238)

screen_width = 1000
screen_height = 1000

class Player(pygame.sprite.Sprite):

    def __init__(self):
        super(Player, self).__init__()
        self.life = 3
        self.idle = pygame.image.load("earth.png")

        self.speed_x = 0
        
        self.image = self.idle
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.speed_x

    def left(self):
        self.speed_x = -7

    def right(self):
        self.speed_x = 7

    def stop(self):
        self.speed_x = 0

    def spawn(self, x, y):
        self.rect.x = x
        self.rect.y = y - self.rect.height

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_y, factor):
        super(Enemy, self).__init__()
        self.factor = factor
        self.meteor = pygame.image.load("meteorite.png")
        self.star = pygame.image.load("star.png")
        if self.factor == 1:
            self.image = self.star
        else:
            self.image = self.meteor
        self.image = pygame.transform.scale(self.image, (60,60))
        self.rect = self.image.get_rect()
        self.speed_y = speed_y

    def update(self):
        self.rect.y += self.speed_y

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super(Boss, self).__init__()

        self.image = pygame.image.load("boss1.png")
        self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.hits = 12

        self.rect.y = -10
        self.rect.x = 400

    def update(self):
        self.rect.y += 2

    def reset(self):
        self.rect.y = -10
        self.rect.x = 400
        self.hits = 15

class Bullet(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4, 10])
        self.image.fill(RED)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 15

player = Player()
boss = Boss()

GAME_MENU = 1
GAME_LOOP = 2
CONTROLS = 3
GAME_OVER = 4
QUIT_GAME = -1

class Game:
    def __init__(self):
        self.on_screen = GAME_MENU

    def initializeGame(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.score = 0
        self.enemy_speed = 2

        self.size = [screen_width, screen_height]
        self.screen = pygame.display.set_mode(self.size)

        pygame.display.set_caption("Star Shooter")

        self.font = pygame.font.SysFont("TimesNewRoman", 40)
        self.title_text_font = pygame.font.SysFont("TimesNewRoman", 90)
        self.start_text_font = pygame.font.SysFont("TimesNewRoman", 75)
        self.lvl_select_text_font = pygame.font.SysFont("TimesNewRoman", 75)
        self.back_text_font = pygame.font.SysFont("TimeNewRoman", 50)
        self.lvl_text_font = pygame.font.SysFont("TimesNewRoman", 40)
        self.game_over_text_font = pygame.font.SysFont("TimesNewRoman", 100)

    def game_menu(self):
        menu_done = False

        title_text = self.title_text_font.render("Star Shooter", True, PASTEL_RED)
        title_text_rect = title_text.get_rect()
        title_text_rect.centerx = 500
        title_text_rect.centery = 450

        start_text = self.start_text_font.render("START!", True, WHITE)
        start_text_rect = start_text.get_rect()
        start_text_rect.centerx = 500
        start_text_rect.centery = 650

        while not menu_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_done = True
                    self.on_screen = QUIT_GAME

                self.screen.fill(BLACK)

                    # x, y, width, height

                mouse = pygame.mouse.get_pos()

                # start button
                if 700 > mouse[0] > 300 and 700 > mouse[1] > 600:
                    pygame.draw.rect(self.screen, GREEN, (300, 600, 400, 100))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu_done = True
                        self.on_screen = GAME_LOOP

        # x, y, width, height
                else:
                    pygame.draw.rect(self.screen, LIME_GREEN, (300, 600, 400, 100))

                # width + x > mouse[0] > x and vice versa
                # controls button
                if 750 > mouse[0] > 250 and 900 > mouse[1] > 800:
                    pygame.draw.rect(self.screen, PINK, (250, 800, 500, 100))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        menu_done = True
                        self.on_screen = CONTROLS

                else:
                    pygame.draw.rect(self.screen, MAGENTA_RED, (250, 800, 500, 100))

                controls_text = self.lvl_select_text_font.render("CONTROLS", True, WHITE)
                controls_text_rect = controls_text.get_rect()
                controls_text_rect.centerx = 500
                controls_text_rect.centery = 850

                self.screen.blit(title_text, title_text_rect)
                self.screen.blit(start_text, start_text_rect)
                self.screen.blit(controls_text, controls_text_rect)

                self.clock.tick(60)

                pygame.display.flip()

    def controls_loop(self):

        controls_done = False

        back_text = self.back_text_font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect()
        back_text_rect.centerx = 100
        back_text_rect.centery = 925

        control1 = self.back_text_font.render("A = Move Left", True, WHITE)
        control1_rect = control1.get_rect()
        control1_rect.centerx = 500
        control1_rect.centery = 100

        control2 = self.back_text_font.render("D = Move Right", True, WHITE)
        control2_rect = control2.get_rect()
        control2_rect.centerx = 500
        control2_rect.centery = 300

        control3 = self.back_text_font.render("Left/Right Click = Shoot", True, WHITE)
        control3_rect = control3.get_rect()
        control3_rect.centerx = 500
        control3_rect.centery = 500

        while not controls_done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    controls_done = True
                    self.on_screen = QUIT_GAME

            self.screen.fill(BLACK)

            mouse = pygame.mouse.get_pos()

            if 175 > mouse[0] > 25 and 950 > mouse[1] > 900:
                pygame.draw.rect(self.screen, PASTEL_RED, (25, 900, 150, 50))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    controls_done = True
                    self.on_screen = GAME_MENU

            else:
                pygame.draw.rect(self.screen, SCARLET, (25, 900, 150, 50))

            self.screen.blit(back_text, back_text_rect)
            self.screen.blit(control1, control1_rect)
            self.screen.blit(control2, control2_rect)
            self.screen.blit(control3, control3_rect)
            self.clock.tick(60)
            pygame.display.flip()

    def game_loop(self):
        game_done = False
        # cooldown for enemy spawn
        counter = 0
        cooldown = 100
        # cooldown for cooldown decrease
        lowercounter = 0
        cooldownlower = 2000
        factor = 2
        boss_time = False
        added = False

        active_sprite_list = pygame.sprite.Group()
        enemy_list = pygame.sprite.Group()
        bullet_list = pygame.sprite.Group()
        star_list = pygame.sprite.Group()

        # spawn enemies
        enemy = Enemy(self.enemy_speed, factor)

        enemy.rect.x = random.randrange(screen_width-60)
        if enemy.rect.x < 0:
            enemy.rect.x = 0

        enemy_list.add(enemy)
        active_sprite_list.add(enemy)

        player.speed_x = 0
        player.speed_y = 0

        player.spawn(500, 900)
        active_sprite_list.add(player)

        while not game_done:
            counter += 1
            lowercounter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                            game_done = True
                            self.on_screen = QUIT_GAME

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        player.left()
                    if event.key == pygame.K_d:
                        player.right()
                    if event.key == pygame.K_r:
                        self.enemy_speed += 1
                        print("enemy speed now " + str(self.enemy_speed))
                    if event.key == pygame.K_ESCAPE:
                        game_done = True
                        self.on_screen = GAME_OVER
                    if event.key == pygame.K_f:
                        player.life += 1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    bullet = Bullet()

                    bullet.rect.x = player.rect.centerx
                    bullet.rect.y = player.rect.centery

                    active_sprite_list.add(bullet)
                    bullet_list.add(bullet)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a and player.speed_x < 0:
                        player.stop()
                    if event.key == pygame.K_d and player.speed_x > 0:
                        player.stop()

            if counter == cooldown and not boss_time:
                # spawn enemies every few seconds
                added = False
                counter = 0
                # 1/10 chance  to spawn a star instead of an enemy
                factor = random.randrange(9)
                enemy = Enemy(self.enemy_speed, factor)

                enemy.rect.x = random.randrange(screen_width - 60)
                if enemy.rect.x < 0:
                    enemy.rect.x = 0

                if factor == 1:
                    star_list.add(enemy)
                else:
                    enemy_list.add(enemy)
                active_sprite_list.add(enemy)

            # cooldown decrease
            if lowercounter == cooldownlower:
                if cooldown >= 10:
                    cooldown -= 5
                lowercounter = 0
                print("Cooldown now " + str(cooldown))

            # spawn boss every 10 points and handles boss attributes, adds 1 to enemy speed
            if self.score % 10 == 0 and self.score != 0:
                if not added:
                    self.enemy_speed += 1
                    print("enemy speed now " + str(self.enemy_speed))
                    added = True
                for enemy in enemy_list:
                    enemy_list.remove(enemy)
                    active_sprite_list.remove(enemy)
                boss_time = True
                enemy_list.add(boss)
                active_sprite_list.add(boss)

            # player loses life if an enemy passes them
            for enemy in enemy_list:
                if enemy.rect.y >= 900:
                    enemy.rect.y = -80
                    enemy_list.remove(enemy)
                    active_sprite_list.remove(enemy)
                    if boss_time:
                        player.life = 0
                    else:
                        player.life -= 1

            for star in star_list:
                if star.rect.y >= 900:
                    star.rect.y = -80
                    star_list.remove(star)
                    active_sprite_list.remove(star)

            active_sprite_list.update()

            if player.rect.left < 0:
                player.rect.left = 0
            if player.rect.right > 1000:
                player.rect.right = 1000
            if player.life == 0:
                game_done = True
                self.on_screen = GAME_OVER

            for bullet in bullet_list:

                enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
                star_hit_list = pygame.sprite.spritecollide(bullet, star_list, True)
                # enemy hit chec
                for enemy in enemy_hit_list:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                    if boss_time:
                        boss.hits -= 1
                        if boss.hits == 0:
                            enemy_list.remove(enemy)
                            active_sprite_list.remove(enemy)
                            self.score += 1
                            boss.reset()
                            boss_time = False
                            counter = 0
                    else:
                        enemy_list.remove(enemy)
                        active_sprite_list.remove(enemy)
                        self.score += 1
                # star hit check
                for star in star_hit_list:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)
                    star_list.remove(star)
                    active_sprite_list.remove(star)
                    player.life += 1

                if bullet.rect.y < -10:
                    bullet_list.remove(bullet)
                    active_sprite_list.remove(bullet)

            # drawing code

            self.screen.fill(BLACK)
            active_sprite_list.draw(self.screen)

            life_text = self.font.render("Lives: " + str(player.life), True, PINK)
            life_text_rect = life_text.get_rect()
            life_text_rect.centerx = 500
            life_text_rect.centery = 50

            score_text = self.font.render("Score: " + str(self.score), True, RED)
            score_text_rect = score_text.get_rect()
            score_text_rect.centerx = 500
            score_text_rect.centery = 100

            self.screen.blit(life_text, life_text_rect)
            self.screen.blit(score_text, score_text_rect)
            # anims go here

            self.clock.tick(60)

            pygame.display.flip()

    def game_over_screen(self):
        game_over_done = False

        game_over_text = self.game_over_text_font.render("GAME OVER!", True, PASTEL_RED)
        game_over_text_rect = game_over_text.get_rect()
        game_over_text_rect.centerx = 500
        game_over_text_rect.centery = 500

        click_spawn_text = self.font.render("Try Again?", True, WHITE)
        click_spawn_text_rect = click_spawn_text.get_rect()
        click_spawn_text_rect.centerx = 500
        click_spawn_text_rect.centery = 605

        while not game_over_done:
            mouse_click = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over_done = True
                    self.on_screen = QUIT_GAME
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_click = 1

            mouse = pygame.mouse.get_pos()

            self.screen.fill(BLACK)

            if 650 > mouse[0] > 350 and 630 > mouse[1] > 580:
                pygame.draw.rect(self.screen, GREEN, (350, 580, 300, 50))
                if mouse_click == 1:
                    game_over_done = True
                    self.score = 0
                    self.enemy_speed = 2
                    player.life = 3
                    self.on_screen = GAME_MENU

                    # x, y, width, height
            else:
                pygame.draw.rect(self.screen, LIME_GREEN, (350, 580, 300, 50))


            self.screen.blit(game_over_text, game_over_text_rect)
            self.screen.blit(click_spawn_text, click_spawn_text_rect)
            self.clock.tick(60)
            pygame.display.flip()

    # runs entire game, determines which loop to run
    def main_loop(self):
        self.initializeGame()
        done = False
        while not done:
            if self.on_screen == GAME_LOOP:
                self.game_loop()

            elif self.on_screen == GAME_MENU:
                self.game_menu()

            elif self.on_screen == CONTROLS:
                self.controls_loop()

            elif self.on_screen == GAME_OVER:
                self.game_over_screen()

            elif self.on_screen == QUIT_GAME:
                done = True

game = Game()
game.main_loop()

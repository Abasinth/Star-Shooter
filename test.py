import pygame
from pygame import *
import random


black = ( 0, 0, 0)
white = ( 255, 255, 255)
red = ( 255, 0, 0)
blue = ( 0, 0, 255)

player_x, player_y = 0, 0
move_player_x, move_player_y = 0, 0


class Block(pygame.sprite.Sprite):

    def __init__(self, color):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20, 15])
        self.image.fill(color)

        self.rect = self.image.get_rect()


class Player(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([20,20])
        self.image.fill(red)

        self.rect = self.image.get_rect()
    def update(self):

        pos = pygame.mouse.get_pos()


        self.rect.x = player_x
        self.rect.y = player_y

class Bullet(pygame.sprite.Sprite):

    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface([4, 10])
        self.image.fill(black)

        self.rect = self.image.get_rect()
    def update(self):



        self.rect.y -= 5


pygame.init()


screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width,screen_height])


all_sprites_list = pygame.sprite.Group()


block_list = pygame.sprite.Group()


bullet_list = pygame.sprite.Group()


for i in range(50):

    block = Block(blue)


    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(350)

    block_list.add(block)
    all_sprites_list.add(block)


player = Player()
all_sprites_list.add(player)


done = False


clock = pygame.time.Clock()

score = 0
player.rect.y = 370

# -------- Main Program Loop -----------
while not done:

    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:

            bullet = Bullet()

            bullet.rect.x = player.rect.x
            bullet.rect.y = player.rect.y

            all_sprites_list.add(bullet)
            bullet_list.add(bullet)

    if event.type== pygame.KEYDOWN:
        if event.key==K_a:
                move_player_x=-1
        elif event.key==K_d:
                move_player_x=+1
        elif event.key==K_w:
                move_player_y=-1
        elif event.key==K_s:
                move_player_y=+1
    if event.type== pygame.KEYUP:
        if event.key==K_a:
                move_player_x=0
        elif event.key==K_d:
                move_player_x=0
        elif event.key==K_w:
                move_player_y=0
        elif event.key==K_s:
                move_player_y=0

    # --- Game logic




    all_sprites_list.update()

    player_x += move_player_x
    player_y += move_player_y



    for bullet in bullet_list:


        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)


        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
            print( score )


        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)




    screen.fill(white)


    all_sprites_list.draw(screen)


    pygame.display.flip()


    clock.tick(20)

pygame.quit()
import pygame, sys, random
from Tools.demo.spreadsheet import center
from pygame import *
from os import path
import math
import os
pygame.init()

class Player(pygame.sprite.Sprite):
    '''create Player class'''
    def __init__(self, player_image, bullet_image, missile_image, sprites_list, bullet_list):
        super().__init__()

        #this part comes under the player specs, just like color, width etc.
        # bullet attributes related to player
        self.bullet_image = bullet_image
        self.missile_image = missile_image
        self.bullets = bullet_list
        self.shoot_delay = 250 # milliseconds
        self.last_shot = pygame.time.get_ticks()

        # other player attributes
        #here you set shield equal to 100 and if it is picked up upgrade is 1
        self.shield = 100
        self.upgrade = 1
        self.upgrade_timer = pygame.time.get_ticks()

    # updating the player class, so the changes you made can be implemented
    def update(self):
        '''update the player'''

        # timer for upgrades
        #this part means that if you pick up a missile sel.upgrade will increase with on and decrease after 4.5 seconds
        if self.upgrade >= 2 and pygame.time.get_ticks() - self.upgrade_timer > 4500:
            self.upgrade -= 1
            self.upgrade_timer = pygame.time.get_ticks()

        #this part comes under the keys function
        # fire weapons by holding the 'space' key
        if keys[pygame.K_SPACE]:
            self.shoot()


    def shoot(self):
        #this is where you update the shooting, so if you pick up a missile it will start shooting it and end after 4.5 seconds, if you don't pick up a missile you will only shoot bullets
        '''fire bullets'''
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            if self.upgrade == 1:
                #bullet = Bullet this is the name for the bullet that shoots, this needs to be changed
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
            # this part means that if you pick up a missile you can shoot bullets and some missiles
            if self.upgrade == 2:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                missile1 = Missile(self.missile_image, self.rect.left, self.rect.centery)
                self.sprites.add(missile1)
                self.bullets.add(missile1)
            # this part means that if you pick up a missile you can shoot bullets and a lot of missiles
            if self.upgrade == 3:
                bullet = Bullet(self.bullet_image, self.rect.centerx, self.rect.top)
                self.sprites.add(bullet)
                self.bullets.add(bullet)
                missile1 = Missile(self.missile_image, self.rect.left, self.rect.centery)
                self.sprites.add(missile1)
                self.bullets.add(missile1)
                missile2 = Missile(self.missile_image, self.rect.right, self.rect.centery)
                self.sprites.add(missile2)
                self.bullets.add(missile2)

    def upgrade_power(self):
        #this part is so you can't pick up more than 2 missile upgrades
        if self.upgrade >= 3:
            self.upgrade = 3
        elif self.upgrade < 3:
            self.upgrade += 1
        self.upgrade_timer = pygame.time.get_ticks()

#Then there is a large portion for the enemy related things, enemies, enemy bullets etc

#after that you make the bullet class for your own player

# this needs to be in the while loop, creating a group for the power ups
powerups = pygame.sprite.Sprite.Group()
class Missile(pygame.sprite.Sprite):
    "create Missile class"
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.image = pygame.transform.scale(image, (25, 38))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        "update missiles"
        self.rect.y += self.speedy
        if self.rect.bottom < 35:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    "create PowerUp class"
    def __init__(self, center, powerup_images):
        super().__init__()
        self.type = random.choice(['shield', 'missile'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        #spawn the powerup according to current position of enemy
        self.rect.center = center
        self.speedy = 6

    def update(self):
        "power up movement"
        self.rect.y += self.speedy
        #destroy sprite if we do not collect it and it moves past WINDOWHEIGHT
        if self.rect.top > WINDOWHEIGHT + 10:
            self.kill()

class Shield(pygame.sprite.Sprite):
    "create Shield class"
    def __init__(self, image, x, y):
        super().__init__()
        self.image = pygame.transform.scale(image, (85, 85))
        self.center = center
        self.rect = self.image.get_rect(center=(self.center))

    def update(self):
        "update shield location"
        self.rect.centerx = self.player.rect.centerx
        self.rect.centery = self.player.rect.centery

        if self.player.shield <= 30:
            #the WINDOWDITH needs to be replaced with our name of the screenwidth, this part is to figure out what the middle is of the ship
            self.rect.center = (WINDOWWIDTH/2, WINDOWWIDTH + 115)
        #this part is so that the shield is in the center of the ship
        elif self.player.shield > 30:
            self.rect.centerx = self.player.rect.centerx
            self.rect.centery = self.player.rect.centery

# This needs to be in the def main()
img_dir = path.join(path.dirname(__file__), 'assets')

missile_img = pygame.image.load('assets/missile.png').convert_alpha()
energy_shield = pygame.image.load('assets/energy_shield.png').convert_alpha()

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert_alpha()
powerup_images['shield'] = pygame.transform.scale(powerup_images['shield'], (35, 35))
powerup_images['missile'] = pygame.image.load(path.join(img_dir, 'missile_powerup.png')).convert_alpha()
powerup_images['missile'] = pygame.transform.scale(powerup_images['missile'], (45, 45))

#this whole section under here needs to be in the main loop

    # to make it look insightfull make a seperate part for all the sprite groups
    powerups = pygame.sprite.Sprite.Group()
    all_active_sprites = pygame.sprite.Group()

    #This is to update the player object and add a shield in the main game while loop, Player is the class
    player = Player(player_image, bullet_image, missile_img, all_active_sprites, bullets)
    shield = Shield(energy_shield, player.rect.center, player)
    all_active_sprites.add(player, shield)

    #this part is for the collision detection, did the bullet hit a enemy and what is the chance he drops an powerup
    for hit in enemy_hit:
        #this is to see if a bullet hits a enemy b.v.
        #enemy_hit = pygame.sprite.groupcollide(enemy_ships, bullets, True, pygame.sprite.collide_circle)
        if random.random() > 0.85:
            powerup = PowerUp(hit.rect.center, powerup_images)
            all_active_sprites.add(powerup)
            powerups.add(powerup)

    #this is to check if the player collides with a power up
    powerup_hit = pygame.sprite.Sprite.spritecollide(player(), powerups, True)

    #this is what happens when the player collides with a power up
    for hit in powerup_hit:
        if hit.type == "shield":
            player.shield += 20
            if player.shield >= 100:
                player.shield = 100
        if hit.type == "missile":
            player.upgrade_power()


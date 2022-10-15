# import the library
import sys
from random import randint, choice, random
import pygame
from os import path
from Tools.demo.spreadsheet import center



pygame.init()

# create display window
SCREEN_HEIGHT = 650
SCREEN_WIDTH = 900



background = pygame.image.load("images/background_img.png")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")
fps = 60
# timer means how fast the game will be played
timer = pygame.time.Clock()
font = pygame.font.SysFont("Timesnewroman", 62)
text_surface = font.render("Main Menu", False, (128, 128, 250))
score_img = font.render("Score:{score}", True, "white")

#Set background
background_ingame = pygame.image.load('images/ingamebackground_img.jpg')

#Track the x-position of two different images
backgroundX = 0
backgroundX2 = background.get_width()

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

    def shoot(self):
        #this is where you update the shooting, so if you pick up a missile it will start shooting it and end after 4.5 seconds, if you don't pick up a missile you will only shoot bullets
        '''fire bullets'''
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > self.shoot_delay:
            self.last_shot = current_time
            if self.upgrade == 1:
                #bullet = Bullet this is the name for the bullet that shoots, this needs to be changed
                bullet = Bullet
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




Rocket = pygame.image.load("images/rocket.png")
RocketX = 25
RocketY = 40
Bullet = pygame.image.load("images/bullet.png")
Bullet_rect = Bullet.get_rect(center=(RocketX, RocketY))

check = False
BulletX = 100
BulletY = 55
Rocket_speed = 8
x = 25
y = 40



def redrawWindow():
    screen.blit(background, (backgroundX, 0))
    screen.blit(background, (backgroundX2, 0))

    pygame.display.update()


# load button images
start_image = pygame.image.load("images/start_button_orange.png").convert_alpha()
exit_image = pygame.image.load("images/exit_button_orange.png").convert_alpha()



#  Highscore displaying on the main menu (NEED TO BE TESTED)!
file = open("highscore.txt", "r")
content = file.read()
content = str(content)

if content < str(score_img):

    file = open("highscore.txt", "w")
    file.write(str(score_img))
    highscore = "You got a new highscore"
    font = pygame.font.SysFont("Timesnewroman", 34)
    hs_text = font.render("Highscore:", True, (128, 128, 250))
    screen.blit(hs_text, (200, 50))
    pygame.display.update()
else:
    highscore = "Highscore: " + content
    font = pygame.font.SysFont("Timesnewroman", 34)
    hs_text = font.render("Highscore:", True, (128, 128, 250))
    screen.blit(hs_text, (200, 50))
    pygame.display.update()

file.close()





# button class - code is based on the video: 'PyGame beginner tutorial in python - adding buttons - by coding with Russ
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw_menu(self):
        menu = False

        # get mouse position
        position = pygame.mouse.get_pos()

        # check mouseover and clicked conditions
        if self.rect.collidepoint(position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                menu = True
            else:
                menu = False

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # draw button on screen
        screen.blit(self.image, (self.rect.x, self.rect.y))
        return menu

# collision between the bullet and alien - CHECK COLLISION.PY FILE!


def score_text():
    score_img = font.render("Score:{score}", True, "white")
    screen.blit(score_img, (10, 10,))
score_text()


# create button instances
start_button = Button(130, 270, start_image, 0.80)
exit_button = Button(580, 270, exit_image, 0.80)

#Muhammed obstacle code, https://youtu.be/AY9MnQ4x3zk
class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'enemy':
            enemy_1 = pygame.image.load('images/enemy.png').convert_alpha()
            enemy_2 = pygame.image.load('images/enemy1.png').convert_alpha()
            self.frames = [enemy_1, enemy_2]
            y_pos = randint(100, 600)
        else:
            grunt_1 = pygame.image.load('images/grunt.png').convert_alpha()
            grunt_2 = pygame.image.load('images/grunt1.png').convert_alpha()
            self.frames = [grunt_2, grunt_1]
            y_pos = randint(100, 600)

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(center = (randint(900, 1100), y_pos))
#animatie van de vijand
    def animation_state(self):
        self.animation_index += 0.05
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
#verplaatsen van vijand
    def update(self):
        self.animation_state()

        #if type == 'enemy'
        #else :

        self.rect.x -= 3

        self.destroy()
#dood maken van enemy wanneer buiten scherm
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
        if self.rect.collidepoint(BulletX, BulletY):
            self.kill()







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
        if self.rect.top > SCREEN_HEIGHT + 10:
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
            self.rect.center = (SCREEN_HEIGHT/2, SCREEN_HEIGHT + 115)
        #this part is so that the shield is in the center of the ship
        elif self.player.shield > 30:
            self.rect.centerx = self.player.rect.centerx
            self.rect.centery = self.player.rect.centery


img_dir = path.join(path.dirname(__file__), 'images')

missile_img = pygame.image.load('images/missile.png').convert_alpha()
energy_shield = pygame.image.load('images/energy_shield.png').convert_alpha()

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield.png')).convert_alpha()
powerup_images['shield'] = pygame.transform.scale(powerup_images['shield'], (35, 35))
powerup_images['missile'] = pygame.image.load(path.join(img_dir, 'missile_powerup.png')).convert_alpha()
powerup_images['missile'] = pygame.transform.scale(powerup_images['missile'], (45, 45))







#gegevens van bullet en rocket.



#obstacle code die er bij hoort.
clock = pygame.time.Clock()
obstacle_group = pygame.sprite.Group()
sky_surface = pygame.image.load('images/ingamebackground_img.jpg').convert()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1000)
spawn_rate = 1000
powerups = pygame.sprite.Group()

# Main Menu game loop
run = True
while run:

    screen.blit(background, (0, 0))

    if start_button.draw_menu():
        gamespeed = pygame.time.Clock()
        screen = pygame.display.set_mode((900, 650))
        pygame.display.set_caption("Game")

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()



                if event.type == obstacle_timer:
                    pygame.time.set_timer(obstacle_timer, spawn_rate)
                    obstacle_group.add(Obstacle(choice(['enemy', 'grunt', 'enemy', 'grunt'])))


            backgroundX -= 1.4
            backgroundX2 -= 1.4
            if backgroundX < background.get_width() * -1:
                backgroundX = background.get_width()
            if backgroundX2 < background.get_width() * -1:
                backgroundX2 = background.get_width()

            screen.blit(background_ingame, (backgroundX, 0))
            screen.blit(background_ingame, (backgroundX2, 0))


            obstacle_group.draw(screen)
            obstacle_group.update()

            print("de game")



            # Movement of the Rocket when pressing the buttons
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                RocketX -= Rocket_speed
            if keys[pygame.K_d]:
                RocketX += Rocket_speed
            if keys[pygame.K_w]:
                RocketY -= Rocket_speed
            if keys[pygame.K_s]:
                RocketY += Rocket_speed


            #If you press space bar you shoot

            if keys[pygame.K_SPACE]:
                if check is False:
                    check = True

                    #This is where the bullet spawns

                    BulletX = RocketX + 66
                    BulletY = RocketY + 15
            # This indicates the border for the bullet, once the bullet hits the right side of the screen you can shoot again

            if BulletX >= 870:
                check = False

            #Bullet movement

            if check is True:
                screen.blit(Bullet, (BulletX, BulletY))
                BulletX += 30

            #Bullet hits enemy

            #if Bullet_rect.collidepoint():

                # to make it look insightfull make a seperate part for all the sprite groups
                powerups = pygame.sprite.Sprite.Group()
                all_active_sprites = pygame.sprite.Group()
                enemy_hit = pygame.sprite.groupcollide(enemy_ships, bullets, True, pygame.sprite.collide_circle)

                # This is to update the player object and add a shield in the main game while loop, Player is the class
                player = Player(Rocket, Bullet, missile_img, all_active_sprites, Bullet)
                shield = Shield(energy_shield, player.rect.center, player)
                all_active_sprites.add(player, shield)

                # this part is for the collision detection, did the bullet hit a enemy and what is the chance he drops an powerup
                for hit in obstacle_group:
                    # this is to see if a bullet hits an enemy e.g.

                    if random.random() > 0.85:
                        powerup = PowerUp(hit.rect.center, powerup_images)
                        all_active_sprites.add(powerup)
                        powerups.add(powerup)

                # this is to check if the player collides with a power up
                powerup_hit = pygame.sprite.Sprite.spritecollide(player(), powerups, True)

                # this is what happens when the player collides with a power up
                for hit in powerup_hit:
                    if hit.type == "shield":
                        player.shield += 20
                        if player.shield >= 100:
                            player.shield = 100
                    if hit.type == "missile":
                        player.upgrade_power()

             # This indicates the borders for the Rocket, so it won't go out of the screen:
            #  This is for the left and right side of the screen
            if RocketX <= 5:
                RocketX = 5
            elif RocketX >= 830:
                RocketX = 830
            #  This is for the top and bottom side of the screen
            if RocketY <= 42:
                RocketY = 42
            elif RocketY >= 550:
                RocketY = 550
            screen.blit(Rocket, (RocketX, RocketY))












            score_text()
            pygame.display.update()
            gamespeed.tick(60)




    if exit_button.draw_menu():
        run = False
        print("Exit")


    # event handler
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

        screen.blit(text_surface, (310, 90))
        screen.blit(hs_text, (380, 430))

        pygame.display.update()

pygame.quit()
sys.exit()

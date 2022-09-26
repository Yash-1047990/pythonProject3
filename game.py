import pygame
from random import randint

pygame.init()

score = 0

screen_widhte = 1024
screen_lengte = 768
display_output = (screen_widhte, screen_lengte)
screen = pygame.display.set_mode(display_output)
pygame.display.set_caption('Basketball!')
Background = pygame.image.load("Basketball court.jpg.")
tick = pygame.mixer.Sound("gunshot.wav")
tick_2 = pygame.mixer.Sound("Sound scored.wav")
tick_3 = pygame.mixer.Sound("dynamite.wav")
tick_nope = pygame.mixer.Sound("Nope.ogg")

basketball = pygame.image.load("Basketball.png")
x = randint(0, screen_widhte)
y = 0
radius = 100
speed = 5
ball_rep_x = x + 50
ball_rep_y = y + 50

basket = pygame.image.load("Basketball hoop.png")
basket_width = 125
basket_pos_x = 450
basket_pos_y = 600
basket_rep_x = [basket_pos_x + 31, basket_pos_x + 94]
basket_rep_y = [basket_pos_y + 14, basket_pos_y + 20]
basket_speed = 8

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

text_x = 15
text_y = 15
font = pygame.font.Font("freesansbold.ttf", 40)

play = True

clock = pygame.time.Clock()

def check_for_event():
    global x, y, play, basket_pos_y, basket_pos_x
    for event in pygame.event.get():
        if __name__ == '__main__':
            if event.type == pygame.QUIT:
                play = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        basket_pos_x -= basket_speed
    if keys[pygame.K_RIGHT]:
        basket_pos_x += basket_speed
    #if keys[pygame.K_UP]:
    #    y -= speed
    #if keys[pygame.K_DOWN]:
    #    y += speed


def update_ball_pos():
    global y, ball_rep_x, ball_rep_y
    y += speed
    ball_rep_x = x + 50
    ball_rep_y = y + 50
    initialise_ball()


def initialise_ball():
    global x, y
    if y > screen_lengte - radius:
        y = 0
        x = randint(0, screen_widhte)

def enforce_border():
    global x, y, basket_pos_x, basket_pos_y
    if x < 0:
        x = 0
    if x > screen_widhte - radius:
        x = screen_widhte - radius
    if y < 0:
        y = 0
    if y > screen_lengte - radius:
        y = screen_lengte - radius
    if basket_pos_x < 0:
        basket_pos_x = 0
    if basket_pos_x > screen_widhte - basket_width:
        basket_pos_x = screen_widhte - basket_width

def show_images():
    global basket_rep_x, basket_rep_y
    screen.blit(Background, (0, 0))
    screen.blit(basketball, (x, y))
    #pygame.draw.line(screen, black, (x + 50, 0), (x + 50, screen_lengte), 2)
    #pygame.draw.line(screen, black, (0, y + 50), (screen_widhte, y + 50), 2)
    basket_rep_x = [basket_pos_x + 31, basket_pos_x + 94]
    basket_rep_y = [basket_pos_y + 14, basket_pos_y + 20]
    screen.blit(basket, (basket_pos_x, basket_pos_y))
    #pygame.draw.line(screen, black, (basket_pos_x + 31, 0), (basket_pos_x + 31, screen_lengte), 2)
    #pygame.draw.line(screen, black, (basket_pos_x + 94, 0), (basket_pos_x + 94, screen_lengte), 2)
    #pygame.draw.line(screen, black, (0, basket_pos_y + 14), (screen_widhte, basket_pos_y + 14), 2)
    #pygame.draw.line(screen, black, (0, basket_pos_y + 20), (screen_widhte, basket_pos_y + 20), 2)

def check_for_score():
    global score
    if ball_rep_x in range(basket_rep_x[0], basket_rep_x[1]) and ball_rep_y in range(basket_rep_y[0], basket_rep_y[1]):
        score += 1
        #tick_2.play()
        #tick.play()
        tick_3.play()
    elif ball_rep_y in range(basket_rep_y[0], basket_rep_y[1]) and ball_rep_x not in range(basket_rep_x[0], basket_rep_x[1]):
        score = 0
        tick_nope.play()
    show_score()

def show_score():
    score_disp = font.render("Score: " + str(score), True, black)
    screen.blit(score_disp, (text_x, text_y))
    print(score)


while play:
    clock.tick(60)
    screen.fill(white)
    check_for_event()
    update_ball_pos()
    enforce_border()
    show_images()
    check_for_score()
    #pygame.draw.circle(screen, red, [x, y], radius)
    # pygame.draw.rect(screen, blue, [200, 200, 50, 100])
    pygame.display.flip()

pygame.quit()

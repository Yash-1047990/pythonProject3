import pygame
pygame.init()

# the lengte and widhte for the screen you are using
screen_widhte = 1024
screen_lengte = 768
display_output = (screen_widhte, screen_lengte)
screen = pygame.display.set_mode(display_output)
pygame.display.set_caption('Basketball!')

#giving the ball size a smaller name
x = 50
y = 50
radius = 50

speed = 5
# giving colours there correct code
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


play = True

clock = pygame.time.Clock()

while play:
    clock.tick(-60)
    #This is the command Loop so the game keeps on running until you exit it
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
   # These are the commands so you can use the key buttons to play with your drawing
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

# this is the border set, you don't need to set specific coordinates
    if x < radius:
        x = radius
    if x > screen_widhte - radius:
        x = screen_widhte - radius
    if y < radius:
        y = radius
    if y > screen_lengte - radius:
        y = screen_lengte - radius

    # to let the code work you have to refresh te screen you do this by using this command
    screen.fill(black)
    pygame.draw.circle(screen, red, [x, y], radius)
    # pygame.draw.rect(screen, blue, [200, 200, 50, 100])
    pygame.display.flip()

pygame.quit()

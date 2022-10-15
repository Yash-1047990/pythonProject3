import pygame
from sys import exist

pygame.init()
screen=pygame.display.set_mode((900,650))
gamespeed = pygame.time.Clock()

surface = pygame.Surface((100,2000))
hill = pygame.Surface(( 50,150))


while True:
    for event in pygame.event.get():
        if event.type == pygame.Quit:
            pygame.quit()
            exit()

    screen.blit(test_surface,(200,100))

pygame.display.update()
gamespeed.tick(60)
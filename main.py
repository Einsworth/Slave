import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Slave")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
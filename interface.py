import pygame

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)

#use for finding the image path of the object
def image(obj):
    path =  "pictures/" + str(obj) + ".png"
    return pygame.image.load(path)

#use for return font render
def text(obj):
    return font.render(str(obj), 1, (0, 0, 0))

#use for show hand of player
def showHand(game, player, screen):
    hand = game.findPlayerHand(player)
    for index in range(len(hand)):
        screen.blit(pygame.transform.scale(image(hand[index]), (125, 180)), (90*(index), 540))
    if player == 1:
        screen.blit(text(len(game.p1hand)), (140, 470))
        screen.blit(text(len(game.p2hand)), (1140, 70))
        screen.blit(text(len(game.p3hand)), (640, 70))
        screen.blit(text(len(game.p4hand)), (140, 70))
    elif player == 2:
        screen.blit(text(len(game.p2hand)), (140, 470))
        screen.blit(text(len(game.p3hand)), (1140, 70))
        screen.blit(text(len(game.p4hand)), (640, 70))
        screen.blit(text(len(game.p1hand)), (140, 70))
    elif player == 3:
        screen.blit(text(len(game.p3hand)), (140, 470))
        screen.blit(text(len(game.p4hand)), (1140, 70))
        screen.blit(text(len(game.p1hand)), (640, 70))
        screen.blit(text(len(game.p2hand)), (140, 70))
    elif player == 4:
        screen.blit(text(len(game.p4hand)), (140, 470))
        screen.blit(text(len(game.p1hand)), (1140, 70))
        screen.blit(text(len(game.p2hand)), (640, 70))
        screen.blit(text(len(game.p3hand)), (140, 70))

#use for show icon and name in position of each player
def showPos(loop, screen):
    screen.blit(pygame.transform.scale(image("Player"), (100, 100)), (20, 420))
    screen.blit(pygame.transform.scale(image("Hand"), (50, 50)), (180, 470))
    screen.blit(text(loop[0]), (140, 420))
    screen.blit(pygame.transform.scale(image("Player"), (100, 100)), (1020, 20))
    screen.blit(pygame.transform.scale(image("Hand"), (50, 50)), (1180, 70))
    screen.blit(text(loop[1]), (1140, 20))
    screen.blit(pygame.transform.scale(image("Player"), (100, 100)), (520, 20))
    screen.blit(pygame.transform.scale(image("Hand"), (50, 50)), (680, 70))
    screen.blit(text(loop[2]), (640, 20))
    screen.blit(pygame.transform.scale(image("Player"), (100, 100)), (20, 20))
    screen.blit(pygame.transform.scale(image("Hand"), (50, 50)), (180, 70))
    screen.blit(text(loop[3]), (140, 20))

#use for redrawing window every frame
def redrawWindow(game, player, loop, screen):
    screen.fill((0, 100, 0))                    #fill background with green
    showHand(game, player, screen)
    showPos(loop, screen)
    pygame.display.update()                     #update screen
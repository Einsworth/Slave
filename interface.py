import pygame

#use for finding the image path of the object
def image(obj):
    path =  "pictures/" + str(obj) + ".png"
    return pygame.image.load(path)

#use for showhand of player
def showHand(hand, screen):
    for index in range(len(hand)):
        screen.blit(pygame.transform.scale(image(hand[index]), (125, 180)), (90*(index), 540))

#use for redrawing window every frame
def redrawWindow(game, player, screen):
    playerHand = game.findPlayerHand(player)    #find our hand
    screen.fill((0, 100, 0))                    #fill background with green
    showHand(playerHand, screen)                #show cards in our hand
    pygame.display.update()                     #update screen
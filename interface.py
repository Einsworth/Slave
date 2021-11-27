import pygame

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)

#finding the image path of the object
def image(obj, type):
    if type == "card":
        path =  "pictures/card/" + str(obj) + ".png"
    elif type == "object":
        path =  "pictures/object/" + str(obj) + ".png"
    return pygame.image.load(path).convert_alpha()

#return font render
def text(obj):
    return font.render(str(obj), 1, (0, 0, 0))

#show our hand and a number of remaining cards in each player's hand
def showHand(game, player, chosenCard, screen):
    hand = game.findPlayerHand(player)
    for index in range(len(hand)):
        screen.blit(pygame.transform.scale(image(hand[index], "card"), (hand[index].width, hand[index].height)), (90*(index), 540))
        if hand[index] in chosenCard:
            screen.blit(pygame.transform.scale(image("Arrow", "object"), (100, 100)), (90*(index), 440))
    if player == 1:
        screen.blit(text(len(game.p1hand)), (140, 370))
        screen.blit(text(len(game.p2hand)), (1140, 70))
        screen.blit(text(len(game.p3hand)), (640, 70))
        screen.blit(text(len(game.p4hand)), (140, 70))
    elif player == 2:
        screen.blit(text(len(game.p2hand)), (140, 370))
        screen.blit(text(len(game.p3hand)), (1140, 70))
        screen.blit(text(len(game.p4hand)), (640, 70))
        screen.blit(text(len(game.p1hand)), (140, 70))
    elif player == 3:
        screen.blit(text(len(game.p3hand)), (140, 370))
        screen.blit(text(len(game.p4hand)), (1140, 70))
        screen.blit(text(len(game.p1hand)), (640, 70))
        screen.blit(text(len(game.p2hand)), (140, 70))
    elif player == 4:
        screen.blit(text(len(game.p4hand)), (140, 370))
        screen.blit(text(len(game.p1hand)), (1140, 70))
        screen.blit(text(len(game.p2hand)), (640, 70))
        screen.blit(text(len(game.p3hand)), (140, 70))

#show icon and name in position of each player
def showPos(loop, screen):
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (20, 320))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (180, 370))
    screen.blit(text(loop[0]), (140, 320))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (1020, 20))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (1180, 70))
    screen.blit(text(loop[1]), (1140, 20))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (520, 20))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (680, 70))
    screen.blit(text(loop[2]), (640, 20))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (20, 20))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (180, 70))
    screen.blit(text(loop[3]), (140, 20))

#show the current direction of turn
def showLoop(game, screen):
    loop = image("Loop", "object")
    if game.loop == 0:
        loop = pygame.transform.flip(loop, True, False)
    screen.blit(pygame.transform.scale(loop, (50, 50)), (20, 200))

#show the name of player's turn and object required in playing
def showTurn(game, player, buttons, screen):
    turn = str(game.turn) + "'s turn"
    screen.blit(text(turn), (100, 200))
    if player == game.turn:
        for button in buttons:
            screen.blit(pygame.transform.scale(image(button.name, "object"), (button.width, button.height)), (button.x, button.y))

def showCurrentCard(game, screen):
    cards = game.currentCard
    for index in range(len(cards)):
        screen.blit(pygame.transform.scale(image(cards[index], "card"), (cards[index].width, cards[index].height)), (520 + 90*(index), 240))

#use for redrawing window every frame
def redrawWindow(game, player, loop, chosenCard, buttons, screen):
    screen.fill((0, 100, 0))                    #fill background with green
    showPos(loop, screen)
    showHand(game, player, chosenCard, screen)
    showLoop(game, screen)
    showTurn(game, player, buttons, screen)
    showCurrentCard(game, screen)
    pygame.display.update()                     #update screen
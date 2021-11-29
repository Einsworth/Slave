#---------- import setting ----------#
import pygame
from network import Network
from interface import redrawWindow
from game import findPos

pygame.init()

#---------- class setting ----------#

class Button:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.width = 116
        self.height = 50
        self.rect = pygame.Rect(x, y, self.width, self.height)

#---------- game setting ----------#

width = 1280                                                    #set width resolution
height = 720                                                    #set height resolution
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slave")                             #set window caption
icon = pygame.image.load('pictures/Icon.png').convert_alpha()   #set icon
pygame.display.set_icon(icon)
buttons = [Button("Play", 1020, 370), Button("Pass", 1150, 370)]

#---------- other function ----------#

#update our hand and make new rect for each card
def updateHand(game, player):
    hand = game.findPlayerHand(player)
    for index in range(len(hand)):
        #check if it's last card then it get full rect
        if index == len(hand) - 1:
            hand[index].rect = pygame.Rect(90*(index), 540, hand[index].width, hand[index].height)
        #if it's not last card then it get overlapping rect
        else:
            hand[index].rect = pygame.Rect(90*(index), 540, hand[index].width - 35, hand[index].height)
    return hand

#pick or remove a card to play
def pickACard(card, chosenCard):
    pick = len(chosenCard)
    #if you already choose it, remove it
    if card in chosenCard:
        chosenCard.remove(card)
    #if you not choose card yet, add it
    elif pick == 0:
        print("Select card: ", card)
        chosenCard.append(card)
    #if you already choose a card (or more)
    elif 1 <= pick <= 3:
        #that card you choose must have same value as previous one
        if card.value == chosenCard[-1].value:
            print("Select card : ", card)
            chosenCard.append(card)
        #else remove previous cards and add a new one
        else:
            chosenCard.clear()
            chosenCard.append(card)
            print("You pick a new card")
    #if not, do nothing
    else:
        print("You can't choose it!")
    chosenCard.sort()

#check if you can play your card that you choose
def checkPlay(game, chosenCard):
    type = len(game.currentCard)    #tpye of card in play (none, single, pair, triple, fourth)
    play = len(chosenCard)          #number of card you play
    #if you are the first player of the game, you must play Three of Clubs (can be any type)
    if game.first:
        if chosenCard[0].rank == 1:
            return True
        return False
    #if you are not the first player of turn but you click play without choosing card, return False
    if play == 0:
        print("Please choose your card first!")
        return False
    #if you are the first player of turn, you can play any card
    elif type == 0:
        print("You are the first one!!!")
        return True
    #if you play the same type, you must play bigger card than the current one
    elif type == play:
        return chosenCard[-1] > game.currentCard[-1]
    #if you play triple into single or fourth into pair, you win! 
    elif play - type == 2:
        return True
    #if not you can't play!
    else:
        print("You can't play!!!")
        return False

#check if you can pass
def checkPass(game):
    #if there are no cards in play, you can't pass
    if not game.currentCard:
        print("can't pass!!!")
        return False
    #if yes you can pass
    return True

#---------- main game function ----------#

def main():

    #prepare before game start
    running = True                  #use for checking if quit the game
    clock = pygame.time.Clock()     #create clock
    n = Network()                   #connect to server
    player = int(n.getPlayer())
    print("You are player: ", player)
    playerPos = findPos(player)
    chosenCard = []

    #start the game
    while running:
        clock.tick(60)
        try:
            game = n.send("get")
            #print("Your game is ", game)
        except:
            running = False
            print("Couldn't get into server...")
            break

        redrawWindow(game, player, playerPos, chosenCard, buttons, screen)

        for event in pygame.event.get():

            #check if you quit the game
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            #check if it's your turn then take a turn
            if player == game.turn:
                hand = updateHand(game, player)

                #check if you click mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    #check what button you click
                    for button in buttons:
                        if button.rect.collidepoint(pos):
                            print("Button: ", button.name)
                            if button.name == "Play":
                                if checkPlay(game, chosenCard):
                                    print("Chosen cards: ",chosenCard)
                                    game = n.send(chosenCard)
                                    chosenCard.clear()
                                else:
                                    print("can't play!!!")
                            elif button.name == "Pass":
                                if checkPass(game):
                                    game = n.send("pass")
                                    chosenCard.clear()

                    #check what card you click
                    for card in hand:
                        if card.rect.collidepoint(pos):
                            print("Card: ", card)
                            pickACard(card, chosenCard)
                            print("Chosen card: ", chosenCard)

main()
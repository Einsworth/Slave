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
buttons = [Button("Play", 1020, 370), Button("Pass", 1150, 370), Button("Send", 1150, 370)]

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
def pickACard(game, card, chosenCard):
    pick = len(chosenCard)
    #if you already choose it, remove it
    if card in chosenCard:
        chosenCard.remove(card)
    #if you not choose card yet, add it
    elif pick == 0:
        print("Select card: ", card)
        chosenCard.append(card)
    #if in game state 2 where King has to send 2 cards, you can not choose more than 2 cards
    elif game.state == 2:
        if pick == 1:
            print("Select card: ", card)
            chosenCard.append(card)
        else:
            print("You can't pick anymore card!")
    #if in game state 3 where Queen has to send 1 card, you can not choose more than 1 cards
    elif game.state == 3:
        chosenCard.clear()
        chosenCard.append(card)
        print("You pick a new card")
    #if in other game state and you already choose a card (or more)
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
    #if you click play without choosing card, return False
    if play == 0:
        print("Please choose your card first!")
        return False
    #if you are the first player of the game, you must play Three of Clubs (can be any type)
    elif game.first:
        if chosenCard[0].rank == 1:
            return True
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

#check if you can send
def checkSend(game, chosenCard):
    send = len(chosenCard)
    print(send)
    if game.state == 2:
        if send == 2:
            if send == 2:
                return True
            print("you have to choose 2 cards!")
            return False
    elif game.state == 3:
        if send == 1:
            return True
        print("you have to choose 1 card!")
        return False

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

                    #if game prepares to start round 2, you have to send card to other roles instead of playing
                    if game.state == 2 or game.state == 3:
                        #if you click send button
                        if buttons[2].rect.collidepoint(pos):
                            print("Click send button")
                            if checkSend(game, chosenCard):
                                print("Chosen cards: ",chosenCard)
                                game = n.send(chosenCard)
                                chosenCard.clear()
                            else:
                                print("can't send!!!")
                    
                    #if game is in round 1 or 2
                    else:
                        #if you click play button
                        if buttons[0].rect.collidepoint(pos):
                            print("Click play button")
                            if checkPlay(game, chosenCard):
                                print("Chosen cards: ",chosenCard)
                                game = n.send(chosenCard)
                                chosenCard.clear()
                            else:
                                print("can't play!!!")

                        #if you click pass button
                        elif buttons[1].rect.collidepoint(pos):
                            print("Click pass button")
                            if checkPass(game):
                                game = n.send("pass")
                                chosenCard.clear()

                    #check what card you click
                    for card in hand:
                        if card.rect.collidepoint(pos):
                            print("Card: ", card)
                            pickACard(game, card, chosenCard)
                            print("Chosen card: ", chosenCard)

main()
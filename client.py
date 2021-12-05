#   Slave
#       This program is a online card game called Slave, where
#   4 players play cards until their hand is empty.
#
#       client is the main module of the game that control everything
#   about client, including interaction with player and all scene function.
#
#   Created by Thanawat Patite ID 62070501027 (Oct 27, 2021)

#---------- import setting ----------#
import pygame
import math
from pygame_textinput import TextInputVisualizer, TextInputManager
from sys import exit
from network import Network
from interface import redrawWindow, redrawMenu, redrawRules, redrawLeaderboard, font
from game import findPos

pygame.init()

#---------- class setting ----------#

class Button:
    def __init__(self, name, x, y, width, height):
        self.name = name    #button's name
        self.x = x  #horizontal position
        self.y = y  #vertical position
        self.width = width  #width of button's image
        self.height = height    #height of button's image
        self.rect = pygame.Rect(x, y, self.width, self.height)  #collision detection rectangle of image

#---------- game setting ----------#

width = 1280    #set width resolution
height = 720    #set height resolution
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slave")
icon = pygame.image.load("pictures/Icon.png").convert_alpha()
pygame.display.set_icon(icon)
#list of all Button
buttons = [Button("Play", 1020, 370, 116, 50), Button("Pass", 1150, 370, 116, 50), Button("Send", 1150, 370, 116, 50), 
Button("Start", 579, 435, 122, 50), Button("Rules", 579, 505, 122, 50), Button("Quit", 579, 575, 122, 50), Button("Back", 1070, 600, 122, 50)]

#---------- other function ----------#

#This function update our card in hand and make new rect for each card in hand.
#   game is the Game that you are playing
#   player is your player's number in game
def updateHand(game, player):
    hand = game.findPlayerHand(player)
    for index in range(len(hand)):
        #if it's last card then it get full rect
        if index == len(hand) - 1:
            hand[index].rect = pygame.Rect(90*index, 540, hand[index].width, hand[index].height)
        #if it's not last card then it get overlapping rect
        else:
            hand[index].rect = pygame.Rect(90*index, 540, hand[index].width - 35, hand[index].height)
    return hand

#This function check whether to add or remove a card from the chosen card list, the update the list
#   game is the Game that you are playing
#   card is a Card that you pick
#   chosenCard is the current chosen card list
def pickACard(game, card, chosenCard):
    pick = len(chosenCard)
    #if you already choose it, remove it
    if card in chosenCard:
        chosenCard.remove(card)
    #if you not choose card yet, add it
    elif pick == 0:
        chosenCard.append(card)
    #if in game state 2 where King has to send 2 cards, you can not choose more than 2 cards
    elif game.state == 2:
        if pick == 1:
            chosenCard.append(card)
    #if in game state 3 where Queen has to send 1 card, you can not choose more than 1 card
    elif game.state == 3:
        chosenCard.clear()
        chosenCard.append(card)
    #if in other game state and you already choose a card (or more)
    elif 1 <= pick <= 3:
        #that card you choose must have same value as previous one
        if card.value == chosenCard[-1].value:
            chosenCard.append(card)
        #else remove previous cards and add a new one
        else:
            chosenCard.clear()
            chosenCard.append(card)
    chosenCard.sort()

#This function check if you can play your card that you have chosen
#   game is the Game that you are playing
#   chosenCard is the current chosen card list
#return True when you can play the chosen card, False if you can't
def checkPlay(game, chosenCard):
    type = len(game.currentCard)    #type of play has none(0), single(1), pair(2), triple(3) and fourth(4)
    play = len(chosenCard)
    #if not choosing any card, you can't play
    if play == 0:
        return False
    #if you are the first player of the game, you must play Three of Clubs (can be any type)
    elif game.first:
        if chosenCard[0].rank == 1:
            return True
        return False
    #if you are the first player of turn, you can play any card
    elif type == 0:
        return True
    #if you play the same type, you must play bigger card than the current one
    elif type == play:
        return chosenCard[-1] > game.currentCard[-1]
    #if you play triple into single or fourth into pair, you can play 
    elif play - type == 2:
        return True
    else:
        return False

#This function check check if you can pass
#   game is the Game that you are playing
#return True when you can pass, False if you can't
def checkPass(game):
    #you can't pass if there are no cards in play (means you must play)
    if not game.currentCard:
        return False
    return True

#This function check if you can send your card that you have chosen
#   game is the Game that you are playing
#   chosenCard is the current chosen card list
#return True when you can send the chosen card, False if you can't
def checkSend(game, chosenCard):
    send = len(chosenCard)
    #if in game state 2 where King has to send 2 cards, you must choose only 2 cards
    if game.state == 2:
        if send == 2:
            if send == 2:
                return True
            return False
    #if in game state 3 where Queen has to send 1 card, you must choose only 1 card
    elif game.state == 3:
        if send == 1:
            return True
        return False

#This function update action flag to check what current action you can take
#   game is the Game that you are playing
#   chosenCard is the current chosen card list
#   action is an list of flag to check what action you can take
def updateAction(game, chosenCard, action):
    #if in state of round 1 or 2, update only play and pass flag
    if game.state == 1 or game.state == 4:
        action[0] = checkPlay(game, chosenCard)
        action[1] = checkPass(game)
    #if in state of trading card, update only send flag
    elif game.state == 2 or game.state == 3:
        action[2] = checkSend(game, chosenCard)

#---------- scene control function ----------#

#This function control menu scene at the start of the game
def menu():
    scene = 0   #flag to check what is next scene, 1 is move to main and 2 is move to rules
    running = True  #use for running the scene, False means the scene end
    clock = pygame.time.Clock() #start program clock
    manager = TextInputManager(validator = lambda input: len(input) <= 7)
    name = TextInputVisualizer(manager = manager, font_object = font)   #create object to check what you type
    pygame.key.set_repeat(500, 50)

    while running:
        clock.tick(60)  #control frame rate (up to 60 fps)
        redrawMenu(buttons, screen)
        events = pygame.event.get()
        name.update(events)
        screen.blit(name.surface, (640, 360))

        for event in events:
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons[3].rect.collidepoint(pos):
                    if name.value:
                        running = False
                        scene = 1

                elif buttons[4].rect.collidepoint(pos):
                    running = False
                    scene = 2

                elif buttons[5].rect.collidepoint(pos):
                    running = False
                    pygame.quit()
                    exit()

        pygame.display.update()
  
    if scene == 1:
        main(name.value)
    elif scene == 2:
        rules()

#This function control rules scene
def rules():
    running = True  #use for running the scene, False means the scene end
    clock = pygame.time.Clock() #start program clock

    while running:
        clock.tick(60)  #control frame rate (up to 60 fps)
        redrawRules(buttons, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons[6].rect.collidepoint(pos):
                    running = False

        pygame.display.update()

    menu()

#This function control results scene
#   game is the Game that you are playing
#   network is the network system that connect client to server
def leaderboard(game, network):
    running = True  #use for running the scene, False means the scene end
    clock = pygame.time.Clock() #start program clock

    while running:
        clock.tick(60)  #control frame rate (up to 60 fps)
        redrawLeaderboard(game, buttons, screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if buttons[6].rect.collidepoint(pos):
                    running = False
                    network.disconnect()

        pygame.display.update()

    menu()

#---------- main game function ----------#

#This function control main game scene
#   name is the name you enter before start the game
def main(name):
    #prepare before game start
    scene = 0   #flag to check what is next scene, 1 is move to menu and 2 is move to leaderboard
    running = True  #use for running the scene, False means the scene end
    timestart = True    #use for start and stop countdown
    sec = 20    #second left to take action (start at 20 second)
    clock = pygame.time.Clock() #start program clock
    chosenCard = [] #list to keep track of current chosen cards
    action = [False, False, False]  #flag to check what action you can take, action by index = [play, pass, send]

    try:
        #try to connect to the server
        n = Network()
        player = int(n.getPlayer())
        game = n.send(name)
        playerPos = findPos(player)
    except:
        #if can't connect to the server, disconnect and return to menu
        running = False
        scene = 1

    while running:
        clock.tick(60)  #control frame rate (up to 60 fps)
        try:
            #try to connect to the server, if connected, get the game data
            game = n.send("get")
        except:
            #if can't connect to the server, disconnect and return to menu
            running = False
            scene = 1
            break

        #setting thing before you take a turn
        if player == game.turn:
            updateAction(game, chosenCard, action)

            #start countdown
            if timestart:
                start = pygame.time.get_ticks()
                sec = 20
                timestart = False
            elif sec > 0:
                timediff = pygame.time.get_ticks() - start
                sec = 20 - math.floor((timediff%60000)/1000)
            #if time run out (20 seconds), the system will take action for you
            else:
                if game.state == 1 or game.state == 4:
                    chosenCard.clear()
                    if game.currentCard:
                        game = n.send("pass")
                    else:
                        hand = game.findPlayerHand(player)
                        chosenCard.append(hand[0])
                        game = n.send(chosenCard)
                        chosenCard.clear()
                elif game.state == 2:
                    hand = game.findPlayerHand(player)
                    chosenCard.append(hand[0])
                    chosenCard.append(hand[1])
                    game = n.send(chosenCard)
                    chosenCard.clear()
                elif game.state == 3:
                    hand = game.findPlayerHand(player)
                    chosenCard.append(hand[0])
                    game = n.send(chosenCard)
                    chosenCard.clear()
                timestart = True

        redrawWindow(game, player, playerPos, chosenCard, action, buttons, sec, screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()

            if game.state == 5:
                running = False
                scene = 2

            #if it's your turn then take a turn
            if player == game.turn:
                hand = updateHand(game, player)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()

                    #in state of round 1 or 2, you can play or pass
                    if game.state == 1 or game.state == 4:
                        if buttons[0].rect.collidepoint(pos):
                            if action[0]:
                                game = n.send(chosenCard)
                                chosenCard.clear()
                                timestart = True

                        elif buttons[1].rect.collidepoint(pos):
                            if action[1]:
                                game = n.send("pass")
                                chosenCard.clear()
                                timestart = True

                    #in state of trading cards, you must send
                    elif game.state == 2 or game.state == 3:
                        if buttons[2].rect.collidepoint(pos):
                            if action[2]:
                                game = n.send(chosenCard)
                                chosenCard.clear()
                                timestart = True

                    #pick a card
                    for card in hand:
                        if card.rect.collidepoint(pos):
                            pickACard(game, card, chosenCard)

    if scene == 1:
        menu()
    elif scene == 2:
        leaderboard(game, n)

menu()
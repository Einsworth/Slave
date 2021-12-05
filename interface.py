#   interface module control all UI by display images and texts
#
#   Created by Thanawat Patite ID 62070501027 (Nov 11, 2021)

#---------- import setting ----------#
import pygame

pygame.font.init()
font = pygame.font.SysFont("Comic Sans MS", 30)

#---------- other function ----------#

#This function finding the image path of the object
#   obj is the name of the object (same name with the image)
#   type is the type of the object (path to the obj image)
#return path that already load by pygame
def image(obj, type):
    if type == "card":
        path =  "pictures/card/" + str(obj) + ".png"
    elif type == "object":
        path =  "pictures/object/" + str(obj) + ".png"
    elif type == "bg":
        path =  "pictures/bg/" + str(obj) + ".png"
    return pygame.image.load(path).convert_alpha()

#This function render text for the object
#   obj is any object that you want to revert it to text
#return font render of the object
def text(obj):
    return font.render(str(obj), 1, (0, 0, 0))

#This function display icon and name in position of each player
#   game is the Game that you are playing
#   loop is the position of each player in your screen
#   screen is the screen of your game
def showPos(game, loop, screen):
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (20, 320))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (180, 370))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (920, 40))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (1080, 90))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (470, 40))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (630, 90))
    screen.blit(pygame.transform.scale(image("Player", "object"), (100, 100)), (20, 40))
    screen.blit(pygame.transform.scale(image("Hand", "object"), (50, 50)), (180, 90))
    if len(game.players) == 4:
        screen.blit(text(game.players[loop[0] - 1]), (140, 320))
        screen.blit(text(game.players[loop[1] - 1]), (1040, 40))
        screen.blit(text(game.players[loop[2] - 1]), (590, 40))
        screen.blit(text(game.players[loop[3] - 1]), (140, 40))

#This function display our hand and a number of remaining cards in each player's hand
#   game is the Game that you are playing
#   player is your player's number in game
#   chosenCard is the current chosen card list
#   screen is the screen of your game
def showHand(game, player, chosenCard, screen):
    hand = game.findPlayerHand(player)
    for index in range(len(hand)):
        screen.blit(pygame.transform.scale(image(hand[index], "card"), (hand[index].width, hand[index].height)), (90*(index), 540))
        if hand[index] in chosenCard:
            screen.blit(pygame.transform.scale(image("Arrow", "object"), (100, 100)), (90*(index), 440))
    if player == 1:
        screen.blit(text(len(game.p1hand)), (140, 370))
        screen.blit(text(len(game.p2hand)), (1040, 90))
        screen.blit(text(len(game.p3hand)), (590, 90))
        screen.blit(text(len(game.p4hand)), (140, 90))
    elif player == 2:
        screen.blit(text(len(game.p2hand)), (140, 370))
        screen.blit(text(len(game.p3hand)), (1040, 90))
        screen.blit(text(len(game.p4hand)), (590, 90))
        screen.blit(text(len(game.p1hand)), (140, 90))
    elif player == 3:
        screen.blit(text(len(game.p3hand)), (140, 370))
        screen.blit(text(len(game.p4hand)), (1040, 90))
        screen.blit(text(len(game.p1hand)), (590, 90))
        screen.blit(text(len(game.p2hand)), (140, 90))
    elif player == 4:
        screen.blit(text(len(game.p4hand)), (140, 370))
        screen.blit(text(len(game.p1hand)), (1040, 90))
        screen.blit(text(len(game.p2hand)), (590, 90))
        screen.blit(text(len(game.p3hand)), (140, 90))

#This function display the current status of turn
#   game is the Game that you are playing
#   screen is the screen of your game
def showCurrentTurn(game, screen):
    #show the name of the current player that taking a turn
    if len(game.players) == 4:
        name = game.players[game.turn - 1]
        turn = name + "'s turn"
        screen.blit(text(turn), (100, 200))

    #show the current direction of turn
    loop = image("Loop", "object")
    if game.loop == 0:
        loop = pygame.transform.flip(loop, True, False)
    screen.blit(pygame.transform.scale(loop, (50, 50)), (20, 200))

    #show the current card in play
    cards = game.currentCard
    for index in range(len(cards)):
        screen.blit(pygame.transform.scale(image(cards[index], "card"), (cards[index].width, cards[index].height)), (520 + 90*(index), 240))

#This function display the status of each player
#   game is the Game that you are playing
#   loop is the position of each player in your screen
#   screen is the screen of your game
def showStatus(game, loop, screen):
    for player in loop:
        pos = loop.index(player)

        #update the image of the current player that taking a turn
        if player == game.turn:
            if pos == 0:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (20, 320))
            elif pos == 1:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (920, 40))
            elif pos == 2:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (470, 40))
            elif pos == 3:
                screen.blit(pygame.transform.scale(image("Inplay", "object"), (100, 100)), (20, 40))

        elif player not in game.inplay:
            if player not in game.inround:
                if len(game.win2) >= 2:

                    #update the image of King if there has been an overthrow in round 2
                    if game.win1[0] != game.win2[0]:
                        if player == game.win2[1]:
                            if pos == 0:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (20, 330))
                            elif pos == 1:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (920, 50))
                            elif pos == 2:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (470, 50))
                            elif pos == 3:
                                screen.blit(pygame.transform.scale(image("Checkmate", "object"), (100, 100)), (20, 50))
                        else:
                            if pos == 0:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 330))
                            elif pos == 1:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (920, 50))
                            elif pos == 2:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (470, 50))
                            elif pos == 3:
                                screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 50))
                    
                    #update the image of finished player in round 2 if there has been an overthrow 
                    else:
                        if pos == 0:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 330))
                        elif pos == 1:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (920, 50))
                        elif pos == 2:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (470, 50))
                        elif pos == 3:
                            screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 50))

                #update the image of finished player in round 1 and round 2 that hasn't been an overthrow 
                else:
                    if pos == 0:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 330))
                    elif pos == 1:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (920, 50))
                    elif pos == 2:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (470, 50))
                    elif pos == 3:
                        screen.blit(pygame.transform.scale(image("Finish", "object"), (100, 100)), (20, 50))
            
            #update the image of the player who pass
            else:
                if pos == 0:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (20, 330))
                elif pos == 1:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (920, 50))
                elif pos == 2:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (470, 50))
                elif pos == 3:
                    screen.blit(pygame.transform.scale(image("Out", "object"), (100, 100)), (20, 50))

#This function display role of each player
#   game is the Game that you are playing
#   loop is the position of each player in your screen
#   screen is the screen of your game
def showRole(game, loop, screen):
    role = ["King", "Queen", "People", "Slave"]
    for index in range(len(game.win1)):
        pos = loop.index(game.win1[index])
        if pos == 0:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (45, 290))
        elif pos == 1:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (945, 10))
        elif pos == 2:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (495, 10))
        elif pos == 3:
            screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (45, 10))

#This function display all object requires for you to take a turn
#   game is the Game that you are playing
#   player is your player's number in game
#   action is an list of flag to check what action you can take
#   buttons is an list of Button
#   sec is second left to take action
#   screen is the screen of your game
def showPlay(game, player, action, buttons, sec, screen):
    if player == game.turn:
        #show current time left in second unit
        screen.blit(text(sec), (1150, 300))
        screen.blit(pygame.transform.scale(image("Hourglass", "object"), (30, 30)), (1190, 310))

        #if in state of trading cards, show send button
        if game.state == 2 or game.state == 3:
            if game.state == 2:
                screen.blit(text("Choose 2 cards to send to Slave!"), (490, 310))
            elif game.state == 3:
                screen.blit(text("Choose 1 card to send to People!"), (490, 310))
            if action[2]:
                screen.blit(pygame.transform.scale(image(buttons[2].name, "object"), (buttons[2].width, buttons[2].height)), (buttons[2].x, buttons[2].y))

        #if in state of normal take a turn, show pick and pass button
        else:
            if game.first:
                screen.blit(text("You must play Three of Clubs!"), (490, 310))
            if action[0]:
                screen.blit(pygame.transform.scale(image(buttons[0].name, "object"), (buttons[0].width, buttons[0].height)), (buttons[0].x, buttons[0].y))
            if action[1]:
                screen.blit(pygame.transform.scale(image(buttons[1].name, "object"), (buttons[1].width, buttons[1].height)), (buttons[1].x, buttons[1].y))

#---------- scene redraw function ----------#

#This function redraw ingame window every frame
#   game is the Game that you are playing
#   player is your player's number in game
#   loop is the position of each player in your screen
#   chosenCard is the current chosen card list
#   action is an list of flag to check what action you can take
#   buttons is an list of Button
#   sec is second left to take action
#   screen is the screen of your game
def redrawWindow(game, player, loop, chosenCard, action, buttons, sec, screen):
    screen.fill((0, 100, 0))
    #if game isn't start yet, show waiting screen
    if game.state == 0:
        redrawWaiting(game, screen)
    else:
        showPos(game, loop, screen)
        showHand(game, player, chosenCard, screen)
        showCurrentTurn(game, screen)
        showStatus(game, loop, screen)
        showRole(game, loop, screen)
        showPlay(game, player, action, buttons, sec, screen)
        pygame.display.update()

#This function redraw menu window every frame
#   buttons is an list of Button
#   screen is the screen of your game
def redrawMenu(buttons, screen):
    screen.blit(pygame.transform.scale(image("MainMenu", "bg"), (1280, 720)), (0, 0))
    screen.blit(text("Enter your name: "), (380, 360))
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(630, 355, 250, 50))
    screen.blit(pygame.transform.scale(image(buttons[3].name, "object"), (buttons[3].width, buttons[3].height)), (buttons[3].x, buttons[3].y))
    screen.blit(pygame.transform.scale(image(buttons[4].name, "object"), (buttons[4].width, buttons[4].height)), (buttons[4].x, buttons[4].y))
    screen.blit(pygame.transform.scale(image(buttons[5].name, "object"), (buttons[5].width, buttons[5].height)), (buttons[5].x, buttons[5].y))

#This function redraw rules window every frame
#   buttons is an list of Button
#   screen is the screen of your game
def redrawRules(buttons, screen):
    screen.blit(pygame.transform.scale(image("HowToPlay", "bg"), (1280, 720)), (0, 0))
    screen.blit(pygame.transform.scale(image(buttons[6].name, "object"), (buttons[6].width, buttons[6].height)), (buttons[6].x, buttons[6].y))

#This function redraw waiting window every frame
#   game is the Game that you are playing
#   screen is the screen of your game
def redrawWaiting(game, screen):
    screen.blit(pygame.transform.scale(image("Waiting", "bg"), (1280, 720)), (0, 0))
    waittext = "Waiting for player (" + str(len(game.players)) + "/4)"
    screen.blit(text(waittext), (490, 345))
    pygame.display.update()

#This function redraw results window every frame
#   game is the Game that you are playing
#   buttons is an list of Button
#   screen is the screen of your game
def redrawLeaderboard(game, buttons, screen):
    role = ["King", "Queen", "People", "Slave"]
    screen.blit(pygame.transform.scale(image("Leaderboard", "bg"), (1280, 720)), (0, 0))

    screen.blit(text(game.players[0]), (320, 200))
    screen.blit(text(game.score[0]), (960, 200))
    screen.blit(text(game.players[1]), (320, 300))
    screen.blit(text(game.score[1]), (960, 300))
    screen.blit(text(game.players[2]), (320, 400))
    screen.blit(text(game.score[2]), (960, 400))
    screen.blit(text(game.players[3]), (320, 500))
    screen.blit(text(game.score[3]), (960, 500))

    if len(game.win1) == 4 and len(game.win2) == 4:
        for index in range(4):
            player = game.win1[index]
            if player == 1:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (640, 200))
            elif player == 2:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (640, 300))
            elif player == 3:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (640, 400))
            elif player == 4:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (640, 500))

        #if there is an overthrow, player 2 is Slave
        if game.win1[0] != game.win2[0]:
            role = ["King", "Slave", "Queen", "People"]

        for index in range(4):
            player = game.win2[index]
            if player == 1:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (700, 200))
            elif player == 2:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (700, 300))
            elif player == 3:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (700, 400))
            elif player == 4:
                screen.blit(pygame.transform.scale(image(role[index], "object"), (50, 50)), (700, 500))
    
    screen.blit(pygame.transform.scale(image(buttons[6].name, "object"), (buttons[6].width, buttons[6].height)), (buttons[6].x, buttons[6].y))
#---------- import setting ----------#
import pygame
from network import Network
from interface import image, redrawWindow
from game import findPos

pygame.init()

#---------- screen & window setting ----------#

width = 1280                                        #set width resolution
height = 720                                        #set height resolution
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slave")                 #set window caption
icon = pygame.image.load('pictures/Icon.png')       #set icon
pygame.display.set_icon(icon)

#---------- main game function ----------#

def main():

    #prepare before game start
    running = True                  #use for checking if quit the game
    clock = pygame.time.Clock()     #create clock
    n = Network()                   #connect to server
    player = int(n.getPlayer())
    print("You are player: ", player)
    playerPos = findPos(player)

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

        for event in pygame.event.get():

            #check if you quit the game
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            #check if it's your turn then take a turn
            if player == game.turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for button in game.buttons:
                        if button.click(pos):
                            n.send(button.text)

        redrawWindow(game, player, playerPos, screen)

main()
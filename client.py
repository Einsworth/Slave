#---------- import setting ----------#
import pygame
from network import Network
from interface import redrawWindow
from game import findPos

pygame.init()

#---------- screen & window setting ----------#
width = 1280                            #set width resolution
height = 720                            #set height resolution
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slave")     #set window caption
icon = pygame.image.load('icon.png')    #set icon
pygame.display.set_icon(icon)

#---------- main game function ----------#

def main():

    #prepare before game start
    running = True                  #use for checking if quit the game
    clock = pygame.time.Clock()     #create clock
    n = Network()                   #connect to server
    player = int(n.getPlayer())
    print("You are player: ", player)
    pos = findPos(player)

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

        #check if quit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        redrawWindow(game, player, pos, screen)

main()
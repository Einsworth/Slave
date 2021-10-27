#import library
import pygame
import random
pygame.init()

#screen & window setting
width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Slave")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

class Card( object ):
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def __repr__(self):
        return str(self.value) + " of " + str(self.suit)

class Deck( list ):
    def __init__(self):
        suits = {"Clubs":1, "Diamonds":2, "Hearts":3, "Spades":4}
        values = {  "Three":3,
                    "Four":4,
                    "Five":5,
                    "Six":6,
                    "Seven":7,
                    "Eight":8,
                    "Nine":9,
                    "Ten":10,
                    "Jack":11,
                    "Queen":12,
                    "King":13,
                    "Ace":14,
                    "Two":15    }
        for value in values:
            for suit in suits:
                self.append(Card(value, suit))
                    
#background setting
def background():
    screen.fill((0, 100, 0))
    pygame.display.update()

#prepare before game start
def gameSetting():
    deck = Deck()
    print(deck)
    random.shuffle(deck)
    print(deck)
    
#main game function
def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

        background()

gameSetting()
main()

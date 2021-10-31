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
    def deal(self):
        return self.pop()

class Player( object ):
    def __init__(self, name):
        self.name = name
        self.hand = []
    def draw(self, deck):
        self.hand.append(deck.deal())

def image(x):
    path =  "pictures/" + str(x) + ".png"
    return pygame.image.load(path)

#main game function
#prepare before game start
running = True
deck = Deck()
random.shuffle(deck)
p1 = Player("Player 1")
p2 = Player("Player 2")
p3 = Player("Player 3")
p4 = Player("Player 4")
for card in deck:
    p1.draw(deck)
    p2.draw(deck)
    p3.draw(deck)
    p4.draw(deck)
print("Player1 = "); print(p1.hand)
print("Player2 = "); print(p2.hand)
print("Player3 = "); print(p3.hand)
print("Player4 = "); print(p4.hand)

while running:
    screen.fill((0, 100, 0))
    screen.blit(pygame.transform.scale(image(p1.hand[1]), (125, 180)), (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    
    pygame.display.update()
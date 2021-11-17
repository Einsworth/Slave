import random

class Game:
    def __init__(self, id):
        self.turn = 0
        self.loop = 0
        self.ready = False
        self.id = id
        self.win = [0, 0, 0, 0]
        self.players = []
        self.p1hand = []
        self.p2hand = []
        self.p3hand = []
        self.p4hand = []

    def drow(self, deck):
        self.p1hand.append(deck.deal())
        self.p2hand.append(deck.deal())
        self.p3hand.append(deck.deal())
        self.p4hand.append(deck.deal())

    def sortHand(self):
        self.p1hand.sort()
        self.p2hand.sort()
        self.p3hand.sort()
        self.p4hand.sort()

    def findPlayerHand(self, player):
        if player == 1:
            return self.p1hand
        elif player == 2:
            return self.p2hand
        elif player == 3:
            return self.p3hand
        elif player == 4:
            return self.p4hand
        print("Can't find player: ", player)
        return None

class Card( object ):
    def __init__(self, value, suit, rank):
        self.value = value
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return str(self.value) + " of " + str(self.suit)

    def __lt__(self, other):
        return self.rank < other.rank

class Deck( list ):
    def __init__(self):
        suits = {"Clubs":1, "Diamonds":2, "Hearts":3, "Spades":4}
        values = {"Three":1, "Four":2, "Five":3, "Six":4, "Seven":5, "Eight":6, "Nine":7, "Ten":8,
        "Jack":9, "Queen":10, "King":11 ,"Ace":12, "Two":13 }
        rank = 1
        for value in values:
            for suit in suits:
                self.append(Card(value, suit, rank))
                rank += 1

    def deal(self):
        return self.pop()

#deal cards to each player (13 cards for each player)
def dealCards(game):
    deck = Deck()                   #generate deck (52 cards)
    random.shuffle(deck)            #shuffle deck
    while deck:                     #each player draw card until deck is empty
        game.drow(deck)
    game.sortHand()                 #sort hand for each player

#find position of each player
def findPos(player):
        if player == 1:
            return [1, 2, 3, 4]
        elif player == 2:
            return [2, 3, 4, 1]
        elif player == 3:
            return [3, 4, 1, 2]
        elif player == 4:
            return [4, 1, 2, 3]
        print("Can't find player: ", player)
        return None
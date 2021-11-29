import random

class Game:
    def __init__(self, id):
        self.id = id
        self.players = []
        self.ready = False
        self.first = True
        self.turn = 0
        self.loop = 0
        self.currentCard = []
        self.p1hand = []
        self.p2hand = []
        self.p3hand = []
        self.p4hand = []
        self.inplay = [1, 2, 3, 4]
        self.inround = [1, 2, 3, 4]
        self.keepLoop = False
        self.win1 = []
        self.win2 = []

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

    def findFirstPlayer(self):
        if self.p1hand[0].rank == 1:
            self.turn = 1
        elif self.p2hand[0].rank == 1:
            self.turn = 2
        elif self.p3hand[0].rank == 1:
            self.turn = 3
        elif self.p4hand[0].rank == 1:
            self.turn = 4
        else:
            print("Can't find three of clubs.")

    def updateTurn(self, playCard, player):
        self.moveTurn(player)

        #reset flag if it the first turn of the game (in the first turn of the game player must play Three of Clubs)
        if self.first:
            self.first = False

        #if player play card
        if playCard:
            #move card from player hand to current playing card
            for card in playCard:
                self.findPlayerHand(player).remove(card)
            self.currentCard = playCard
            #if player play after another player win, set keepLoop to False (means not reverse loop)
            if self.keepLoop:
                self.keepLoop = False
                #if that player is the last one inplay, reset current playing card and player inplay
                if len(self.inplay) == 1:
                    self.currentCard.clear()
                    self.inplay = self.inround.copy()
            self.checkWin(player)                       #check if the player win this turn

        #if player pass
        else:
            self.inplay.remove(player)                  #remove that player from inplay
            #check if player pass after another player win
            if self.keepLoop:
                #if all players pass after another player win, reverse loop
                if len(self.inplay) == 0:
                    if self.loop == 0:
                        self.loop = 1
                    else:
                        self.loop = 0
                    self.keepLoop = False               #set keepLoop to False again
                    self.currentCard.clear()            #clear current card in play
                    self.inplay = self.inround.copy()   #reset player inplay
                    self.moveTurn(player)
                    print("Reverse loop to: ", self.loop)

            #if player pass normally
            else:
                #if there is only one play inplay left
                if len(self.inplay) == 1:
                    self.turn = self.inplay[0]    #make him plays first next turn
                    self.currentCard.clear()            #clear current card in play
                    self.inplay = self.inround.copy()   #reset player inplay

        print("Keep loop: ", self.keepLoop)
        print("Current turn: ", self.turn)
        print("Remaining player in play: ", self.inplay)
        print("Remaining player in round: ", self.inround)

    def moveTurn(self, player):
        turn = self.inplay.index(player)
        #check loop (0 means anti-clockwise, 1 means clockwise)
        if self.loop == 0:
            #move to the right player, but if you are the last player, move to the first player instead
            if player == self.inplay[-1]:
                self.turn = self.inplay[0]
            else:
                self.turn = self.inplay[turn + 1]
        else:
            #move to the left player, but if you are the first player, move to the last player instead
            if player == self.inplay[0]:
                self.turn = self.inplay[-1]
            else:
                self.turn = self.inplay[turn - 1]

    def checkWin(self, player):
        if not self.findPlayerHand(player):
            self.inplay.remove(player)
            self.inround.remove(player)
            self.win1.append(player)
            if len(self.inround) == 1:
                self.win1.append(self.inround[0])
                self.findPlayerHand(self.inround[0]).clear()
                self.currentCard.clear()
                self.startNewRound()
            else:
                self.keepLoop = True

    def startNewRound(self):
        print("Round 1 score: ", self.win1)
        print("Start new round!!!")
        dealCards(self)

class Card( object ):
    def __init__(self, value, suit, rank):
        self.value = value
        self.suit = suit
        self.rank = rank
        self.width = 125
        self.height = 180
        self.rect = None

    def __repr__(self):
        return str(self.value) + " of " + str(self.suit)

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        if not isinstance(other, Card):
            return False
        if self.rank != other.rank:
            return False
        return True

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
    game.findFirstPlayer()          #find first player turn

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
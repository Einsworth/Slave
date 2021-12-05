#   game module store all game data, used by both client and server
#
#   Created by Thanawat Patite ID 62070501027 (Nov 11, 2021)

#---------- import setting ----------#
import random

#---------- class setting ----------#

class Game:
    def __init__(self, id):
        self.id = id     #game id from server
        self.players = []   #name of each player in game
        #state of the game 
        # 0 means not start yet
        # 1 means start round 1
        # 2 means trade card between King and Slave
        # 3 means trade card between Queen and People
        # 4 means start round 2 
        # 5 means game end
        self.state = 0
        self.first = True   #flag for checking the if it's the first turn of the game 
        self.turn = 0   #current player's turn (1 - 4)
        self.loop = 0   #direction of the turn, 0 means anti clockwise and 1 means clockwise
        self.currentCard = []   #list of current card in playing of each turn
        self.p1hand = []    #list of cards in player 1's hand
        self.p2hand = []    #list of cards in player 2's hand
        self.p3hand = []    #list of cards in player 3's hand
        self.p4hand = []    #list of cards in player 4's hand
        self.inplay = [1, 2, 3, 4]  #player that is not pass yet
        self.inround = [1, 2, 3, 4] #player that is not win yet
        self.keepLoop = False   #flag for checking reverse loop, True means there is player who finished in previous turn
        self.win1 = []  #order of player that win in round 1, role by index = [King, Queen, People, Slave]
        self.win2 = []  #order of player that win in round 2
        self.score = [0, 0, 0, 0]   #score of each player from 1 - 4

    #This function update the state of the game
    def updateState(self):
        self.state += 1

        #start round 1
        if self.state == 1:
            print("Game state: ", self.state)
            print("Start round 1!")
            dealCards(self)
            self.findFirstPlayer()

        #prepare to start round 2, King have to send any 2 cards to slave
        elif self.state == 2:
            print("Round 1 score: ", self.win1)
            print("Round 1 end ;w;")
            print("Game state: ", self.state)
            print("Prepare to start round 2...")

            #reset parameters for round 2
            self.inplay = [1, 2, 3, 4]
            self.inround = [1, 2, 3, 4]
            dealCards(self)

            print("Slave send their 2 highest card to King")
            print("King have to send any 2 cards to Slave")
            self.turn = self.win1[0]

        #after king sent cards, Queen have to send any card to people
        elif self.state == 3:
            print("Game state: ", self.state)
            print("People send their highest card to Queen")
            print("Queen have to send any card to People")
            self.turn = self.win1[1]

        #start round 2
        elif self.state == 4:
            print("Game state: ", self.state)
            print("Start round 2!!")
            self.findFirstPlayer()

        #end game
        elif self.state == 5:
            print("Game state: ", self.state)
            print("Game end!!")
            print("Win in round 1", self.win1)
            print("Win in round 2", self.win2)

            #calculate score
            point = 2
            for player in self.win1:
                if point == 0:
                    point -= 1
                self.score[player - 1] += point
                point -= 1
            
            point = 2
            #if there is an overthrow, King got 0 point
            if self.win1[0] != self.win2[0]:
                for player in self.win2:
                    if point == 0:
                        point -= 1
                    if player == self.win1[0]:
                        self.score[player - 1] = 0
                    else:
                        self.score[player - 1] += point
                        point -= 1
            #if not, calculate normally
            else:
                for player in self.win2:
                    if point == 0:
                        point -= 1
                    self.score[player - 1] += point
                    point -= 1

            print("Score of each player: ", self.score)

        else:
            print("Game state: ", self.state)
            print("Game end!!!")

    #This function make all player drow a card form deck
    def drow(self, deck):
        self.p1hand.append(deck.deal())
        self.p2hand.append(deck.deal())
        self.p3hand.append(deck.deal())
        self.p4hand.append(deck.deal())

    #This function sort hand of all player
    def sortHand(self):
        self.p1hand.sort()
        self.p2hand.sort()
        self.p3hand.sort()
        self.p4hand.sort()

    #This function return a list of card in hand of a player
    #   player is that player's number in game
    #return that player's hand or don't if not found
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

    #This function find first player of the round
    def findFirstPlayer(self):
        #player who has Three of Clubs play first turn of round 1
        if self.state == 1:
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

        #Slave play first turn of round 2 and reset loop
        elif self.state == 4:
            slave = self.win1[3]
            king = self.win1[0]
            queen = self.win1[1]

            #if Slave's left player is King, loop anti-clockwise from slave
            #and if Slave's opposite player is King and Queen is on the left, loop anti-clockwise from slave
            #otherwise loop clockwise from slave
            if slave == 1:
                if king == 4:
                    self.loop = 0
                elif king == 3 and queen == 4:
                    self.loop = 0
            elif slave - king == 1:
                self.loop = 0
            elif abs(slave - king) == 2 and slave - queen == 1:
                self.loop = 0
            else:
                self.loop = 1

            self.turn = slave

    #This function update the status of turn when a player take a turn
    #   playCard is the card that player play (or empty if player pass)
    #   player is that player's number in game
    def updateTurn(self, playCard, player):
        self.moveTurn(player)

        #reset flag if it the first turn of the game
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
                    #move turn again in case that player is winning
                    if not self.findPlayerHand(player):
                        self.moveTurn(player)
            self.checkWin(player)

        #if player pass
        else:
            self.inplay.remove(player)

            #check if player pass after another player win
            if self.keepLoop:
                #if all players pass after another player win, reverse loop and the player who pass before reverse loop play again
                if len(self.inplay) == 0:
                    if self.loop == 0:
                        self.loop = 1
                    else:
                        self.loop = 0
                    self.keepLoop = False
                    self.currentCard.clear()
                    self.inplay = self.inround.copy()
                    self.turn = player
                    print("Reverse loop to: ", self.loop)

            #if player pass normally
            else:
                #if there is only one play inplay left, make him plays first next turn by move to his turn
                if len(self.inplay) == 1:
                    self.turn = self.inplay[0]
                    self.currentCard.clear()
                    self.inplay = self.inround.copy()

        print("Keep loop: ", self.keepLoop)
        print("Current turn: ", self.turn)
        print("Remaining player in play: ", self.inplay)
        print("Remaining player in round: ", self.inround)

    #This function move a turn when a player take a turn
    #   player is that player's number in game
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

    #This function check if the player win this turn
    #   player is that player's number in game
    def checkWin(self, player):
        #if player has no card left in hand that means he win
        if not self.findPlayerHand(player):
            self.inplay.remove(player)
            self.inround.remove(player)

            #if win in round 1
            if self.state == 1:
                self.win1.append(player)
                #if there is last player who is not win yet, end round
                if len(self.inround) == 1:
                    self.win1.append(self.inround[0])
                    self.findPlayerHand(self.inround[0]).clear()
                    self.currentCard.clear()
                    self.updateState()
                #if round is not end yet, raise the keepLoop flag to check reverse loop condition
                else:
                    self.keepLoop = True

            #if win in round 2
            if self.state == 4:
                #if it is the first win in round 2
                if not self.win2:
                    self.win2.append(player)
                    #if player who win first isn't King that mean it is an overthrow (means King is auto lose)
                    if player != self.win1[0]:
                        #if next turn is that King, move turn again before remove him
                        if self.turn == self.win1[0]:                   
                            self.moveTurn(self.win1[0])
                        self.inplay.remove(self.win1[0])
                        self.inround.remove(self.win1[0])
                        self.win2.append(self.win1[0])
                        self.findPlayerHand(self.win1[0]).clear()
                #if there is a last player who is not win yet, end game
                elif len(self.inround) == 1:
                    self.win2.append(player)
                    self.win2.append(self.inround[0])
                    self.findPlayerHand(self.inround[0]).clear()
                    self.currentCard.clear()
                    self.updateState()
                #if round is not end yet, raise the keepLoop flag to check reverse loop condition   
                else:
                    self.win2.append(player)
                    self.keepLoop = True

    #This function trade card between players
    #   sendCard is the card that player send
    def tradeCard(self, sendCard):
        print("Trade card...")

        #King and Slave trade card
        if self.state == 2:
            slave = self.win1[3]
            king = self.win1[0]
            
            #Slave send their 2 highest cards to King
            self.findPlayerHand(king).append(self.findPlayerHand(slave).pop(-1))
            self.findPlayerHand(king).append(self.findPlayerHand(slave).pop(-1))

            #King have to send any 2 cards to Slave
            for card in sendCard:
                self.findPlayerHand(king).remove(card)
                self.findPlayerHand(slave).append(card)

            self.sortHand()
            self.updateState()

        #Queen and People trade card
        elif self.state == 3:
            people = self.win1[2]
            queen = self.win1[1]

            #People send their highest card to Queen
            self.findPlayerHand(queen).append(self.findPlayerHand(people).pop(-1))

            #Queen have to send any card to People
            for card in sendCard:
                self.findPlayerHand(queen).remove(card)
                self.findPlayerHand(people).append(card)

            self.sortHand()
            self.updateState()

class Card( object ):
    def __init__(self, value, suit, rank):
        self.value = value  #value of card (1 - 10, Jack, Queen, King)
        self.suit = suit    #suit of card (Clubs, Diamonds, Hearts, Spades)
        self.rank = rank    #rank of card (Three of Clubs as 1 to Two of Spades as 52)
        self.width = 125    #width of card's image
        self.height = 180   #height of card's image
        self.rect = None    #collision detection rectangle of image

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
        #append card in order of rank to deck
        for value in values:
            for suit in suits:
                self.append(Card(value, suit, rank))
                rank += 1

    #This function deal a card from deck
    #return a card that pop from deck
    def deal(self):
        return self.pop()

#---------- other function ----------#

#This function deal cards to each player (13 cards for each player) and sort their hands
#   game is the Game that players are playing
def dealCards(game):
    deck = Deck()                   #generate deck (52 cards)
    random.shuffle(deck)            #shuffle deck
    while deck:                     #each player draw card until deck is empty
        game.drow(deck)
    game.sortHand()                 #sort hand for each player

#This function find position of each player in the player screen
#   player is that player's number in game
#return list of players in each position of the screen
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
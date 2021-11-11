class Player( object ):
    def __init__(self, name):
        self.name = name
        self.hand = []
    def draw(self, deck):
        self.hand.append(deck.deal())
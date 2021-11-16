# Slave
Final project of CPE327 (Software Engineering).

# Version
Oct 27, 2021
  - Just start working
  - Set resolution 1280x720
  - Set caption
  - Set background green
  - Set icon
  - Upload icon and card pictures

Nov 1, 2021
  - Working on gamesetting
  - Can create deck with 52 cards
  - Deck can deal 13 cards to each players
  - Can show a card in the screen (just one for now)

Nov 6, 2021
  - Can deal card to each player correctly (there is a bug that only deal 11 cards to each player)
  - Can sort each player's hand
  - Can show cards in entirely hand (just for Player 1)
  - Add a lot of code comment (every function except class setting)

Nov 11, 2021
  - Create server
  - Client can connect to server via network
  - Divide main.py script to
      - client.py (include all main function)
      - player.py (include player class)
      - interface.py (include all interface and UI function)

Nov 16, 2021
  - Server can detect player
      - Create a new game if player has no game to join
      - Ready and start game when there are four players in game
  - Server can support unlimited player (but up to my labtop ;w;)
  - Server can deal card to each player in game correctly
  - Change player.py script to game.py (include all class)
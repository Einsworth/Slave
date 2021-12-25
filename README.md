# Slave
Final project of CPE327 (Software Engineering).

# Description
Slave is inspired by Slave In Wonderland, using Pygame to develop. it's a turn based 4 players card game, using socket server to play together,  where you have to play card until your hands is empty to win!

# Note
You have to open server by running server.py script in order to start playing. If client can't connect to the server, the game won't start even if you click start button. The IP in the script and exe file is my IPV4, if you want to play with your IP you must run both server.py and client.py scripts with the your IP. IP in server.py and network.py scripts must be match in order to connect togheter. If you just want to play with your friends, I suggest to use LAN to have same IP, but if you want to open public server, you must port forward your IP.

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

Nov 17, 2021
  - Can show position of each player in each client correctly
  - Can show player's name (which is currently player number)
  - Can show a number of remaining cards in each player's hand

Nov 20, 2021
  - Can show which player's turn currently
  - Can show the "Play" and "Pass" button in the screen when you take a turn
  - Can send data correctly when clicking the button

Nov 27, 2021
  - Working on take a turn function (not complete yet)
  - Can choose cards to play by the rules correctly
  - Can show which cards you choose to play
  - Can show current cards in play
  - Turn system work just fine (there is a bug that after turn of player 4 it go to turn of player 8)
  - Make all data transfer between network and server become "pickle"

Nov 30, 2021
  - Working on second round and end game!
  - Can play first round without a bug (as far as I test it now)
  - Can show role correctly
  - Can reverse loop of turn correctly
  - Improve pick a card function
  - Adjust in game interface a little bit
  - Fix a lot of minor bug

Dec 2, 2021
  - Game are now complete, all important feature are working now
  - Fix a lot of minor bug

Dec 6, 2021
  - Add game menu, rules and leaderboard
  - Fix some minor bug
  - This (maybe) is the last update!

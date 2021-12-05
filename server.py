#   server module is use for open and maintain the server
#
#   Created by Thanawat Patite ID 62070501027 (Nov 11, 2021)

#---------- import setting ----------#
import socket
import pickle
from _thread import *
from game import Game


#---------- server setting ----------#

server = "26.12.84.96"  #server IPV4 (right now this is our group LAN IPV4)
port = 5555 #server port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Server started, wating for a connection...")

games = {}  #a list that contain all game in the server
playerCount = 0 #number of players in the server

#---------- other function ----------#

#this function create thread of the player's client in the server
#   conn is the connection between player's client and server
#   player is that player's number in game
#   gameId is the index of game in the server
def threadCilent(conn, player, gameId):
    global playerCount
    conn.send(str.encode(str(player)))

    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if gameId in games:
                game = games[gameId]

                if not data:
                    break

                else:

                    #if game is not start yet, data other than "get" will become name of the player
                    if len(game.players) != 4 and data != "get":
                        game.players.append(data)
                        print("Players in game: ", game.players)
                    else:
                        #if player pass
                        if data == "pass":
                            print("Data: ", data)
                            print("From player: ", player)
                            game.updateTurn([], player)
                        #if player play or send card
                        elif data != "get":
                            print("Data: ", data)
                            print("From player: ", player)
                            if game.state == 1 or game.state == 4:
                                game.updateTurn(data, player)
                            elif game.state == 2 or game.state == 3:
                                game.tradeCard(data)

                    conn.sendall(pickle.dumps(game))

            else:
                break

        except:
            break

    #if the server can't receive one of the player data anymore, closing that game
    print("Lost connection from player: ", player)
    try:
        del games[gameId]
        print("Closing GameID: ", gameId)
    except:
        pass
    playerCount -= 1
    conn.close()

#---------- main server function ----------#

# gameId start at 0
# playerCount start at 1
# number of players in each game are 1 - 4
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    playerCount += 1
    gameId = (playerCount - 1) // 4

    #if it's the first player, create a new game
    if playerCount % 4 == 1:
        games[gameId] = Game(gameId)
        player = 1
        print("Creating a new gameID: ", gameId)

    #if it's the fourth player, start the game
    elif playerCount % 4 == 0:
        games[gameId].updateState()
        player = 4
        print("Starting gameID: ", gameId)

    else:
        player = playerCount % 4

    start_new_thread(threadCilent, (conn, player, gameId))
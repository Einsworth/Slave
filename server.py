#---------- import library ----------#
import socket
import pickle
from _thread import *
from game import Game

server = "26.12.84.96"    #enter your IPV4 (it may change everyday but default is "192.168.1.103")
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Server started, wating for a connection...")

games = {}
playerCount = 0

def threadCilent(conn, player, gameId):
    global playerCount
    conn.send(str.encode(str(player)))
    #print("Hello : ", player, gameId)

    #reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048))

            if gameId in games:
                game = games[gameId]

                if not data:
                    break

                else:

                    if data == "pass":
                        print("Data: ", data)
                        print("From player: ", player)
                        game.updateTurn([], player)
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

    #if cannot receive one of player data anymore then closing that game
    print("Lost connection from player: ", player)
    try:
        del games[gameId]
        print("Closing GameID: ", gameId)
    except:
        pass
    playerCount -= 1
    conn.close()

# gameId start at 0
# playerCount start at 1
# player are 1 - 4
while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)
    playerCount += 1
    gameId = (playerCount - 1) // 4

    #if it's first player then create newgame
    if playerCount % 4 == 1:
        games[gameId] = Game(gameId)
        player = 1
        print("Creating a new gameID: ", gameId)

    #if it's fourth player then ready to start the game
    elif playerCount % 4 == 0:
        games[gameId].ready = True
        games[gameId].updateState()
        player = 4
        print("Starting gameID: ", gameId)

    #if it's second or third player
    else:
        player = playerCount % 4

    #games[gameId].players.append(player)

    start_new_thread(threadCilent, (conn, player, gameId))
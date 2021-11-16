#---------- import library ----------#
import socket
import pickle
from _thread import *
from game import Game, dealCards

server = "192.168.1.102"
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

    #reply = ""
    while True:
        try:
            data = conn.recv(2048).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break

                else:

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
        dealCards(games[gameId])
        player = 4
        print("Starting gameID: ", gameId)

    #if it's two - three
    else:
        player = playerCount % 4

    start_new_thread(threadCilent, (conn, player, gameId))
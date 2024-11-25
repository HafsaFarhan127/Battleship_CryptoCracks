import socket

def byteArrayToGrid(byteArray, size):
    grid = []
    for i in range(0, len(byteArray), size):
        grid.append(list(byteArray[i:i + size]))  # Convert each row to a list
    return grid

def byteArrayToList(byteArray):
    return [int(byte) for byte in byteArray]

def listToByteArray(data):
    return bytearray(data)

def displayGrid(grid):
    print("   ", end="")
    for i in range(len(grid)):
        print(f"{i:2}", end=" ")
    print("\n   " + "-" * (3 * len(grid)))
    for i, row in enumerate(grid):
        print(f"{i:2} |", " ".join(map(str, row)))

# Server connection
host = '127.0.0.1'
port = 12001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print(f"Connected to the game server at {host}:{port}")

# Initialize grids
gridSize = 10
myGrid = byteArrayToGrid(client_socket.recv(1024), gridSize)
guessGrid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]

print("Your Grid:")
displayGrid(myGrid)

sink = False
while not sink:
    try:
        server_message = byteArrayToList(client_socket.recv(1024))

        if 1 in server_message:  # Player's turn
            print("\nYour turn!")
            while True:
                try:
                    x, y = map(int, input("Enter coordinates to attack (x, y): ").split(","))
                    if 0 <= x < gridSize and 0 <= y < gridSize:
                        break
                    print("Coordinates out of bounds, try again.")
                except ValueError:
                    print("Invalid input, try again.")

            client_socket.sendall(listToByteArray([x, y]))
            attack_result = byteArrayToList(client_socket.recv(1024))

            if len(attack_result) < 2:
                print("Invalid response from server.")
                continue

            if attack_result[0] == 1:
                print("HIT!")
                guessGrid[x][y] = 'X'
                if attack_result[1] == 1:
                    print("You sunk the ship! You win!")
                    break
            else:
                print("MISS!")
                guessGrid[x][y] = 'O'

            print("Opponent's Grid:")
            displayGrid(guessGrid)

        elif 0 in server_message:  # Opponent's turn
            print("\nWaiting for the opponent's move...")
            opponent_attack = byteArrayToList(client_socket.recv(1024))

            if len(opponent_attack) < 2:
                print("Invalid attack from server.")
                continue

            print(f"Opponent attacked at ({opponent_attack[0]}, {opponent_attack[1]})")
            x, y = opponent_attack
            result = "MISS"
            if myGrid[x][y] != 0:
                result = "HIT"
                myGrid[x][y] = 0
                if sum(sum(row) for row in myGrid) == 0:
                    sink = True
                    print("All ships sunk! You lose.")

            resultArray = [1 if result == "HIT" else 0, 1 if sink else 0]
            client_socket.sendall(listToByteArray(resultArray))

            print("Your Grid:")
            displayGrid(myGrid)

    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
print("Disconnected from the server.")

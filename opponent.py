import socket

def byteArrayToGrid(byteArray, size):
    grid = []
    for i in range(0, len(byteArray), size):
        grid.append(list(byteArray[i:i + size]))
    return grid

def byteArrayToList(byteArray):
    return [int(byte) for byte in byteArray]

def listToByteArray(data):
    return bytearray(data)

def displayGrid(grid):
    for row in grid:
        print(" ".join(map(str, row)))

# Server connection
host = '127.0.0.1'
port = 12001
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
print("Connected to the server")

# Initialize grids
gridSize = 10
myGrid = byteArrayToGrid(client_socket.recv(1024), gridSize)
guessGrid = [[0 for _ in range(gridSize)] for _ in range(gridSize)]

print("Your Grid:")
displayGrid(myGrid)

while True:
    try:
        # Wait for turn signal
        server_message = byteArrayToList(client_socket.recv(1024))
        if 1 in server_message:  # Player's turn
            x, y = map(int, input("Enter coordinates to attack (x, y): ").split(","))
            client_socket.sendall(listToByteArray([x, y]))
            result = byteArrayToList(client_socket.recv(1024))
            if result[1] == 1:
                print("You sunk the ship! You win!")
                break
            guessGrid[x][y] = "X" if result[0] == 1 else "O"
            print("Opponent's Grid:")
            displayGrid(guessGrid)
        elif 0 in server_message:  # Opponent's turn
            print("Waiting for opponent's move...")
            move = byteArrayToList(client_socket.recv(1024))
            x, y = move
            result = "HIT" if myGrid[x][y] != 0 else "MISS"
            myGrid[x][y] = 0
            sink = 1 if sum(sum(row) for row in myGrid) == 0 else 0
            client_socket.sendall(listToByteArray([1 if result == "HIT" else 0, sink]))
            if sink == 1:
                print("All ships sunk! You lose.")
                break
    except Exception as e:
        print(f"Error: {e}")
        break

client_socket.close()
print("Disconnected from the server.")

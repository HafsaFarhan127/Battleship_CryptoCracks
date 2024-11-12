# Display Matrix and Option to choose encryption or no encryption mode
# Display Matrix - Hafsa

def byteArray2Grid(arrayByte):
    transmissionMatrix = []
    for i in range(len(arrayByte)):
        transmissionMatrix.append(arrayByte[i])
    grid = []
    for i in range(0, len(transmissionMatrix), 10):
        innerList = []
        for j in range(10):
            innerList.append(transmissionMatrix[i + j])
        grid.append(innerList)
    return grid

from socket import *
serverName = '127.0.0.1'
serverPort = 12001

# Create TCP socket and connect once
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

try:
    while True:
        # Receive the initial response or grid data
        response = clientSocket.recv(1024)
        grid = byteArray2Grid(response)
        print("Received grid:", grid)

        # Input message to send to the server
        message = input('Input a message (or type "exit" to quit): ')

        # Check if the user wants to exit
        if message.lower() == "exit":
            print("Closing connection.")
            break

        # Send the message in bytes
        clientSocket.send(message.encode())

        #receive a response after sending a message
        #maybe we can use this for receiving the response for the attack coordinates sent
        response = clientSocket.recv(1024)
        print("Server response:", response.decode())

finally:
    clientSocket.close()
    print("Client has exited.")

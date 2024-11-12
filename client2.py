from socket import *
serverName = '127.0.0.1'
serverPort = 12001
# Create TCP socket
clientSocket = socket(AF_INET, SOCK_STREAM)
# Establish a connection with server (IP, port#)
clientSocket.connect((serverName, serverPort))
try:
    while True:
        message = input('Input a message (or type "exit" to quit): ')

        byteMessage = message.encode() #converts to bytes

        if message.lower() == "exit":
            print("Closing connection.")
            break

        # Create a new socket and connect to the server for each message
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((serverName, serverPort))
        
        # Send the message
        clientSocket.send(byteMessage) #message can be only sent in bytes

        # Receive the response
        response = clientSocket.recv(1024)
        
        # Close the socket after each message
        clientSocket.close()

finally:
    print("Client has exited.")
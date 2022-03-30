import socket
import threading 

HOST = input("IP to Connect to,  \nPort: ")
CLIENTNAME = socket.gethostbyname(socket.gethostname())
PORT = input("Press Enter without any text to use default Port (Default Port: 8090) \nPort: ")
if (PORT == ""):
    PORT = 8090
else:
    PORT = int(PORT)
ADDR = (HOST, PORT)
HEADER = 16
ENCODEFORMAT = "utf-8"


DISCONNECT_MESSAGE = "exit"
global DISCONNECT
DISCONNECT = False


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(ADDR)

def getMessages():
    while True:
        if DISCONNECT:
            break
        try:
            recv_message = sock.recv(1024).decode(ENCODEFORMAT)
            print(recv_message)
        except:
            print("\n[Server] Server is stopping of lost connection!")
            print("[Server] Terminating Connection")
            #sock.close()
            break



def textToServer(message):

    text = message.encode(ENCODEFORMAT)
    sock.send(text)
    
    

def disconnect():
    sock.send(DISCONNECT_MESSAGE.encode(ENCODEFORMAT))


thread = threading.Thread(target=getMessages)
thread.start()
while True:
    msg = str(input(f"[Client] {CLIENTNAME}: "))
    
    if msg.lower() == DISCONNECT_MESSAGE:
        disconnect()
        DISCONNECT = True
        DISCONNECT_MESSAGE_TEXT = "[Client] User Disconnected"
        print(DISCONNECT_MESSAGE_TEXT)
        break
    else:
        textToServer(msg)

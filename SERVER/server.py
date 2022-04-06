import socket
import threading


HOST = socket.gethostbyname(socket.gethostname())
PORT = input("Default Port is 8090 \nPort: ")
if (PORT == ""):
    PORT = 8090
else:
    PORT = int(PORT)
ADDR = (HOST, PORT)
HEADER = 16
DECODEFORMAT = "utf-8"
SERVERSTOP = False
SERVER_STOP_MESSAGE = "[Server] Stopping..."


DISCONNECT_MESSAGE = "exit!"
HELP_MESSAGE = "help!"
helpText = """

Commands:
exit! -  exit connection
help! - gets this message

"""



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(ADDR)

clients = set()
clients_lock = threading.Lock()

def clientComm(conn, addr):
    print(f"[Server] Client Connected [{addr}], Number of Active Connections: {threading.active_count() - 1}")

    with clients_lock:
        clients.add(conn)

    DISCONNECT_MESSAGE_CLIENT = f"[Server] Client Disconnected [{addr}]"
    DISCONNECT_MESSAGE_SERVER = f"[Server] Client Disconnected [{addr}]"
    DISCONNECT_MESSAGE_ABORT = f"[Server] Client ABORTED [{addr}]"

    try:
        while True:
            try:
                data = conn.recv(1024).decode(DECODEFORMAT)
            except:
                break

            if str(data) == DISCONNECT_MESSAGE:
                break
            elif str(data) == HELP_MESSAGE:
            
                conn.sendall(helpText.encode(DECODEFORMAT))

            else:
                data = f"[Client][{addr}] {data}"
                print(data)
                
                with clients_lock:
                    for c in clients:
                        if c != conn:
                            c.sendall(data.encode(DECODEFORMAT))
        
    finally:
        with clients_lock:
            conn.close
            
            clients.remove(conn)
            print(DISCONNECT_MESSAGE_SERVER)
            for c in clients:
                c.sendall(DISCONNECT_MESSAGE_CLIENT.encode(DECODEFORMAT))
    
    

    conn.close()


def startUp():
    sock.listen()
    print(f"[Server] Server is on {ADDR}")
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=clientComm, args=(conn, addr))
        thread.start()
        


startUp()

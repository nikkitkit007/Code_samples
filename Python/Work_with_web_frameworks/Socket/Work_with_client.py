import socket

class Client_connector(object):
    def __init__(self, IP_to_connect: str, Port_to_connect: int):
        try:
            connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            IP = IP_to_connect
            PORT = Port_to_connect
            
            connection.connect((IP, PORT))

            self.connection = connection
            print("Connecting to server with IP: " + IP + " ...")
            
            print(self.receive_message())
        except:
            print("Server does not work.")
    
    def receive_message(self):
        message = self.connection.recv(1024).decode('utf8')
        return message
    
    def send_message(self, message):
        message = str(message)
        self.connection.send(message.encode('utf8'))

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass


if __name__ == "__main__":
    IP = "127.0.0.1"
    PORT = 12334

    my_client = Client_connector(IP, PORT)
    
    mess = input("Message to send:")
    my_client.send_message(mess)

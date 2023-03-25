import socket
from threading import Thread

class Server_listener(object):
    def __init__(self, IP_server, PORT_server, backlog_server):
        try:
            listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # задамем семейство протоколов 'Интернет' (INET) задаем тип передачи данных 'потоковый' (TCP)
            listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)       
            listener.bind((IP_server, PORT_server))                   
            listener.listen(backlog_server)                                 # Размер очереди входящих испорченных подключений

            self.listener = listener

            print("Server start working. IP = %s, Port = %d"%(IP,PORT))
        except:
            print("Some errors were founded...")

    def recieve_connection(self):                               # подключаю клиент к серверу
        connection, address_client = self.listener.accept()
        self.connection = connection
        self.address_client = address_client
        print("New connection from: "+str(address_client))
        
        self.send_message("You connected.")

    def send_message(self, message):                            # отправка сообщения клиенту
        try:
            message = str(message)
            self.connection.send(message.encode('utf-8'))
        except:
            print("Some errors with sending message.")

    def receive_message(self):                                  # получение сообщения от клиента
        message = self.connection.recv(1024).decode('utf8')
        return message

    def close_connection(self):                                 # завершаю работу с клиентом
        try:
            self.connection.close()
        except:
            pass
    
    def close_server(self):                                     # завершаю работу сервера
        try:
            self.listener.close()
        except:
            pass

# def parse(connection, address):             # общение с клиентом
#     data_recv = []
#     while True:
#         data = connection.recv(1024).decode("utf8")
#         data_recv+=data
#         if data == "close" or not data:     # условие выхода из сессии
#             print("\nSession was closen")
#             break
#     return 0

if __name__ == "__main__":
    IP = socket.gethostbyname(socket.gethostname())
    PORT = 12334
    backlog = 1

    my_server = Server_listener(IP, PORT, backlog)
    while True:
        # th = Thread(target =  my_server.recieve_connection())     #  в новом потоке создать не удалось()
        # th.start()
        my_server.recieve_connection()
        print(my_server.receive_message())
        # break

    my_server.close_server()
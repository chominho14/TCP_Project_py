from socket import *
from threading import *
import random # 랜덤 모듈
import sys

class UpDownServer:
    clients = []
    final_received_message = ""
    senders_num = 0
    draw_num = 5
    recv_num = []
    win_number = random.randrange(1,51)
    
    counter_lock = Lock()
    counter=0
    
    user_done = True
        

    def __init__(self): #메인 함수
        self.s_sock = socket(AF_INET, SOCK_STREAM) #소켓 생성
        self.ip = ''
        self.port = 2500
        self.s_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s_sock.bind((self.ip, self.port))
        print("Waiting for clients...")
        self.s_sock.listen(100)
        self.accept_client()
    
    def accept_client(self): #클라이언트와 연결
        while True:
            client = c_socket, (ip, port) = self.s_sock.accept()
            if client not in self.clients:
                self.clients.append(client)
            self.senders_num += 1
            print (self.senders_num,'번째 클라이언트, ',ip, ' : ', str(port), '가 연결되었습니다.')
            t = Thread(target=self.receive_messages, args=(c_socket,)) #쓰레드 생성
            t.start()
            

    def receive_messages(self, c_socket):
        while self.user_done:
            
            try:
                incoming_message = c_socket.recv(1024)
                if not incoming_message:
                    break
            except:
                continue
            else: # 클라이언트가 보낸 데이터를 받아서 각 변수에 삽입
                
                """
                뮤택스 - acquire()를 이용하여 Lock을 걸어준다.
                """
                self.counter_lock.acquire()
                
                self.final_received_message = incoming_message.decode('utf-8')
                sender = self.final_received_message.split()[0]
                num = self.final_received_message.split()[1]
                
                
                self.final_received_message = (sender+"이(가) 선택한 번호 : {0} \n".format(num))
                if self.draw_num == 1:
                    self.recv_num.append(sender)         
                    self.recv_num.append(num)         
                            
                    print(self.recv_num)
                if self.draw_num == 2:
                    self.recv_num.append(sender)         
                    self.recv_num.append(num)         
                            
                    print(self.recv_num)
                if self.draw_num == 3:
                    self.recv_num.append(sender)         
                    self.recv_num.append(num)         
                           
                    print(self.recv_num)
                if self.draw_num == 4:
                    self.recv_num.append(sender)         
                    self.recv_num.append(num)         
                            
                    print(self.recv_num)
                if self.draw_num == 5:
                    self.recv_num.append(sender)         
                    self.recv_num.append(num)         
                            
                    print(self.recv_num)
                self.send_all_clients(self.final_received_message)
                self.draw_num -= 1
                
                if self.win_number < int(num):
                    self.final_received_message = ('Down\n')
                    self.send_all_clients(self.final_received_message)
                    print("Down")
                elif self.win_number > int(num):
                    self.final_received_message = ('Up\n')
                    self.send_all_clients(self.final_received_message)
                    print("Up")
                elif self.win_number == int(num):
                    self.final_received_message = ('정답입니다!\n')
                    self.send_all_clients(self.final_received_message)
                    print("정답입니다!")
                    self.user_done=False
                    
                if self.draw_num > 0: # 정답 기회가 남았을 경우
                    self.final_received_message = ('정답까지 남은 횟수 : '+str(self.draw_num)+'개\n')
                    self.send_all_clients(self.final_received_message)
                
                else: #정답 기회가 남지 않았을 경우
                    self.final_received_message = ('실패!\n\n')
                    self.send_all_clients(self.final_received_message)
                    self.drawing_of_Lots(c_socket)
                    self.user_done=False
                
                """
                뮤택스 - release()를 이용하여 Lock을 풀어준다.
                """
                self.counter_lock.release()
            
                
        c_socket.close()
    
    def send_all_clients(self, senders_socket): #서버에게 보내는 메시지
        for client in self.clients:
            socket, (ip, port) = client
            if socket is not senders_socket:
                try:
                    socket.sendall(self.final_received_message.encode('utf-8'))
                except:
                    pass

    def drawing_of_Lots(self, senders_socket): #정답 발표
        self.final_received_message = ('정답은 ') #정답 출력
        self.final_received_message += str(self.win_number)+' '
        self.final_received_message += ('입니다!\n')
        self.send_all_clients(self.final_received_message)
                

if __name__ == "__main__":
    try:
        UpDownServer()
    except KeyboardInterrupt:
        pass
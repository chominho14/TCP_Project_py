from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *
import tkinter as tk

class UpDownClient:
    client_socket = None

    def __init__(self, ip, port): #메인함수
        self.initialize_socket(ip, port)
        self.initialize_gui()
        self.listen_thread()
    
    def initialize_socket(self, ip, port): #server에 연결
        '''
        TCP socket을 생성하고 server에게 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))
    
    def send_chat(self):
        '''
        message를 전송하는 callback함수
        '''
        senders_name = self.name_widget.get().strip() #사용자 이름을 가져온다
        # 각 숫자들을 가져온다.
        data1 = self.enter_number1.get()+' '
        

        data_num = (data1)

        send_to_server_message = (senders_name+' '+data_num).encode('utf-8') #전체 숫자 데이터를 인코딩화

        self.chat_transcript_area.yview(END)
        self.client_socket.send(send_to_server_message) 
        return 'break'

    def initialize_gui(self):
        '''
        위젯을 배치하고 초기화한다.
        '''
        self.root = tk.Tk()
        
        self.name_label = Label(self.root, text='사용자 이름')
        self.result_label = Label(self.root, text='결과 화면')
        self.send_label = Label(self.root, text='1~50 사이의 숫자를 입력해 주세요')
        self.send_btn = Button(self.root, text='전송', command=self.send_chat)
        self.chat_transcript_area = ScrolledText(self.root, height=20, width=60)
        self.name_widget = Entry(self.root, width=15)
        
        self.enter_number1 = Entry(self.root, width=5)
        
 
        self.name_label.pack()
        self.name_widget.pack()
        self.result_label.pack()
        self.chat_transcript_area.pack()
        self.send_label.pack()
        
        self.enter_number1.pack()
        self.send_btn.pack()
        

    def listen_thread(self):
        '''
        Thread를 생성하고 시작한다
        '''
        
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()
        
    def receive_message(self, so):
        '''
        서버로부터 메시지를 수신하고 문서창에 표시한다
        '''
        
        while True:
            buf = so.recv(1024) #결과 문자열이 길어 1024로 설정
            if not buf:
                break
            self.chat_transcript_area.insert('end', buf.decode('utf-8') + '\n')
            self.chat_transcript_area.yview(END)
        so.close()
    

if __name__ == "__main__":
    ip = input("server IP addr: ")
    if ip =='':
        ip = '127.0.0.1'
    port = 2500
    UpDownClient(ip,port)
    mainloop()

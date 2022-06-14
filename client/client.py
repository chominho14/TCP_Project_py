from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *


class UpDownClient:
    client_socket = None
    
    # 메인 함수
    def __init__(self, ip, port):
        self.initialize_socket(ip, port)
        self.initialize_gui()
        self.listen_thread()
    
    
    def initialize_socket(self, ip, port): 
        '''
        TCP socket을 생성하고 server에게 연결
        '''
        self.client_socket = socket(AF_INET, SOCK_STREAM) # 
        remote_ip = ip
        remote_port = port
        self.client_socket.connect((remote_ip, remote_port))
    
    def send_chat(self):
        '''
        사용자 이름과 사용자가 입력한 숫자 전송하는 callback함수
        '''
        senders_name = self.name_widget.get().strip() #사용자 이름을 가져온다
        
        data = self.input_num.get() # 사용자가 입력한 숫자를 가져온다.

        send_to_server_message = (senders_name+' '+data).encode('utf-8') #전체 숫자 데이터를 인코딩화

        self.ScrTxt_Area.yview(END)
        self.client_socket.send(send_to_server_message) 
        return 'break'

    def initialize_gui(self):
        '''
        tkinter을 이용해 위젯을 배치하고 초기화한다.
        '''
        self.root = Tk()
        
        self.lbl_name = Label(self.root, text='사용자 이름')
        self.lbl_result = Label(self.root, text='결과 화면')
        self.lbl_send = Label(self.root, text='1~50 사이의 숫자를 입력해 주세요')
        self.btn_send = Button(self.root, text='전송', command=self.send_chat)
        self.ScrTxt_Area = ScrolledText(self.root, height=20, width=60)
        self.name_widget = Entry(self.root, width=15)
        
        self.input_num = Entry(self.root, width=5)
        
 
        self.lbl_name.pack()
        self.name_widget.pack()
        self.lbl_result.pack()
        self.ScrTxt_Area.pack()
        self.lbl_send.pack()
        
        self.input_num.pack()
        self.btn_send.pack()
        

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
            self.ScrTxt_Area.insert('end', buf.decode('utf-8') + '\n')
            self.ScrTxt_Area.yview(END)
        so.close()
    

if __name__ == "__main__":
    ip = input("server IP addr: ")
    
    # 사용자가 ip를 입력하지 않았을 시에 기본 ip를 넣어준다.
    if ip =='':
        ip = '127.0.0.1'
    port = 2500
    UpDownClient(ip,port)
    mainloop()

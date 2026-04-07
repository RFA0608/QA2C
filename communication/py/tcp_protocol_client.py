import socket

class tcp_client:
    # host and port for init connection
    host = ""
    port = 0
    time_out = 10
    byte = 1024
    
    # socket instance
    socket_instance = socket.socket

    # print information flag
    print_flag = False

    def __init__(self, host, port):
        if isinstance(host, str) and isinstance(port, int):
            try:
                self.host = host
                self.port = port

            except:
                if self.print_flag:
                    print(f"def: init | error | host and port set false")
                exit(-1)
        else:
            if self.print_flag:
                print(f"def: init | error | host and port type false")
            exit(-1)

    def __enter__(self):
        try:
            self.socket_instance = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket_instance.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    
            self.socket_instance.settimeout(self.time_out)
                    
            try:
                self.socket_instance.connect((self.host, self.port))
                if self.print_flag:
                    print(f"def: enter | alert | connect")
            except:
                if self.print_flag:
                    print(f"def: enter | error | bind set false or timeout {self.time_out} second")
                exit(-1)
            
            return self
        except:
            if self.print_flag:
                print(f"def: enter | error | socket instance false")
            exit(-1)
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.socket_instance:
            self.socket_instance.close()

        if self.print_flag:    
            print(f"def: exit | alert | close sever")

    def set_byte(self, byte):
        if isinstance(byte, int):
            self.byte = byte
        else:
            if self.print_flag:
                print(f"def: set_byte | error | type false")
            exit(-1)

    def set_timeout(self, timeout):
        if isinstance(timeout, int):
            self.time_out = timeout
        else:
            if self.print_flag:
                print(f"def: set_timeout | error | type false")
            exit(-1)

    def set_printflag(self, flag):
        if isinstance(flag, bool):
            self.print_flag = flag
        else:
            if self.print_flag:
                print(f"def: set_printflag | error | type false")
            exit(-1)

    def send(self, data):
        if isinstance(data, int):
            try:
                send_data = f"<INT>{data}<END>"
                send_data_byte = send_data.encode()

                try:
                    self.socket_instance.sendall(send_data_byte)
                except:
                    if self.print_flag:
                        print(f"def: send | error | communication false")
                    exit(-1)
                        
                recv_data_byte = b""
                while True:
                    recv_data_byte += self.socket_instance.recv(self.byte)

                    if recv_data_byte.endswith(b"<END>"):
                        break
                        
                recv_data = recv_data_byte.decode()
                recv_data = recv_data.replace("<END>", "")
                        
                if recv_data == "<CHK>":
                    if self.print_flag:
                        print(f"def: send | alert | communication complete")
                else:
                    if self.print_flag:
                        print(f"def: send | error | communication false")
                    exit(-1)
            except:
                if self.print_flag:
                    print(f"def: send | error | process false")
                exit(-1)
        elif isinstance(data, float):
            try:
                send_data = f"<FLOAT>{data}<END>"
                send_data_byte = send_data.encode()

                try:
                    self.socket_instance.sendall(send_data_byte)
                except:
                    if self.print_flag:
                        print(f"def: send | error | communication false")
                    exit(-1)
                        
                recv_data_byte = b""
                while True:
                    recv_data_byte += self.socket_instance.recv(self.byte)

                    if recv_data_byte.endswith(b"<END>"):
                        break
                        
                recv_data = recv_data_byte.decode()
                recv_data = recv_data.replace("<END>", "")
                        
                if recv_data == "<CHK>":
                    if self.print_flag:
                        print(f"def: send | alert | communication complete")
                else:
                    if self.print_flag:
                        print(f"def: send | error | communication false")
                    exit(-1)
            except:
                if self.print_flag:
                    print(f"def: send | error | process false")
                exit(-1)
        elif isinstance(data, str):
            try:
                send_data = f"<STR>{data}<END>"
                send_data_byte = send_data.encode()

                try:
                    self.socket_instance.sendall(send_data_byte)
                except:
                    if self.print_flag:
                        print(f"def: send | error | communication false")
                    exit(-1)
                        
                recv_data_byte = b""
                while True:
                    recv_data_byte += self.socket_instance.recv(self.byte)

                    if recv_data_byte.endswith(b"<END>"):
                        break
                        
                recv_data = recv_data_byte.decode()
                recv_data = recv_data.replace("<END>", "")
                        
                if recv_data == "<CHK>":
                    if self.print_flag:
                        print(f"def: send | alert | communication complete")
                else:
                    if self.print_flag:
                        print(f"def: send | error | communication false")
                    exit(-1)
            except:
                if self.print_flag:
                    print(f"def: send | error | process false")
                exit(-1)
        else:
            if self.print_flag:
                print(f"def: send | error | type false")
            exit(-1)
    def recv(self):
        send_data = f"<RED><END>"
        send_data_byte = send_data.encode()

        try:
            self.socket_instance.sendall(send_data_byte)
        except:
            if self.print_flag:
                print(f"def: recv | error | communication false")
            exit(-1)

        try:
            recv_data_byte = b""

            while True:
                recv_data_byte += self.socket_instance.recv(self.byte)

                if recv_data_byte.endswith(b"<END>"):
                    break
                    
            recv_data = recv_data_byte.decode()
            recv_data = recv_data.replace("<END>", "")
            type =""
            
            if "<INT>" in recv_data:
                type = "INT"
                recv_data = recv_data.replace("<INT>", "")
                recv_data = int(recv_data)
            elif "<FLOAT>" in recv_data:
                type = "FLOAT"
                recv_data = recv_data.replace("<FLOAT>", "")
                recv_data = float(recv_data)
            elif "<STR>" in recv_data:
                type = "STR"
                recv_data = recv_data.replace("<STR>", "")
                recv_data = str(recv_data)
            else:
                if self.print_flag:
                    print(f"def: recv | error | type false")
                exit(-1)
        except:
            if self.print_flag:
                print(f"def: recv | error | communication false")
            exit(-1)
                
        return type, recv_data


    



    
import socket
import time
import math

class tcp_server:
    # host and port for init connection
    host = ""
    port = 0
    time_out = 10
    byte = 1024
    
    # socket instance
    socket_instance = socket.socket

    # connection instance
    connection = any

    # print information flag
    print_flag = False

    # metric information
    metric_flag = False
    stack = 100
    metric_buf = []
    last_time = any
    mean_time = any
    std_time = any

    # sample constant time
    sampleconst_flag = False
    sampleconst_time = int

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
            self.socket_instance.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket_instance.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                    
            self.socket_instance.bind((self.host, self.port))
            self.socket_instance.listen()

            self.socket_instance.settimeout(self.time_out)
                    
            try:
                self.connection, _ = self.socket_instance.accept()
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

    def set_metric(self, metric_flag, stack):
        if isinstance(metric_flag, bool) and isinstance(stack, int):
            self.metric_flag = metric_flag
            self.stack = stack
        else:
            if self.print_flag:
                print(f"def: set_metric | error | type false")
            exit(-1)

    def diagnostic_metric(self):
        if self.metric_flag:
            length = len(self.metric_buf)
            
            sum_time = 0

            if length == 0:
                print(f"def: diagnostic_metric | error | metric_buf length is zero")
                exit(-1)
            else:
                for i in range(length):
                    sum_time = sum_time + self.metric_buf[i]
                
                self.mean_time = sum_time / length

                sum_time = 0
                for i in range(length):
                    sum_time = sum_time + (self.mean_time - self.metric_buf[i])**2

                self.std_time = math.sqrt(sum_time / length)

                if self.print_flag:
                    print(f"def: diagnostic_metric | alert | last_time: {self.last_time}ms, mean_time: {self.mean_time}ms, std_time: {self.std_time}ms, length: {length}")
        else:
            if self.print_flag:
                print(f"def: diagnostic_metric | error | metric flag false")

    def set_sampleconst(self, sampleconst_flag, sampleconst_time):
        if isinstance(sampleconst_flag, bool) and isinstance(sampleconst_time, int):
            self.sampleconst_flag = sampleconst_flag
            self.sampleconst_time = sampleconst_time
        else:
            if self.print_flag:
                print(f"def: set_sampleconst | error | type false")
            exit(-1)

    def wait(self, last_time):
        if self.sampleconst_flag:
            if last_time < self.sampleconst_time:
                start_time = time.perf_counter_ns()
                end_time = time.perf_counter_ns()

                wait_time = self.sampleconst_time - last_time
                while True:
                    if (end_time - start_time) / 1000000 < wait_time:
                        time.sleep(0.000001)
                    else:
                        break
                    end_time = time.perf_counter_ns()
            else:
                if self.print_flag:
                    print(f"def: wait | alert | sampleconst time insufficient")
        else:
            if self.print_flag:
                print(f"def: wait | error | sampleconst flag false")

    def send(self, data):
        if self.metric_flag:
            start_point = time.perf_counter_ns()
        if isinstance(data, int):
            try:
                recv_data_byte = b""
                while True:
                    recv_data_byte += self.connection.recv(self.byte)

                    if recv_data_byte.endswith(b"<END>"):
                        break
                        
                recv_data = recv_data_byte.decode()
                recv_data = recv_data.replace("<END>", "")
                        
                if recv_data == "<RED>":
                    send_data = f"<INT>{data}<END>"
                    send_data_byte = send_data.encode()
                    try:
                        self.connection.sendall(send_data_byte)
                    except:
                        if self.print_flag:
                            print(f"def: send | error | communication false")
                        exit(-1)
                else:
                    if self.print_flag:
                        print(f"def: send | error | invalid data received")
                    exit(-1)
            except:
                if self.print_flag:
                    print(f"def: send | error | process false")
                exit(-1)
        elif isinstance(data, float):
            try:
                recv_data_byte = b""
                while True:
                    recv_data_byte += self.connection.recv(self.byte)

                    if recv_data_byte.endswith(b"<END>"):
                        break
                        
                recv_data = recv_data_byte.decode()
                recv_data = recv_data.replace("<END>", "")
                        
                if recv_data == "<RED>":
                    send_data = f"<FLOAT>{data}<END>"
                    send_data_byte = send_data.encode()
                    try:
                        self.connection.sendall(send_data_byte)
                    except:
                        if self.print_flag:
                            print(f"def: send | error | communication false")
                        exit(-1)
                else:
                    if self.print_flag:
                        print(f"def: send | error | invalid data received")
                    exit(-1)
            except:
                if self.print_flag:
                    print(f"def: send | error | process false")
                exit(-1)
        elif isinstance(data, str):
            try:
                recv_data_byte = b""
                while True:
                    recv_data_byte += self.connection.recv(self.byte)

                    if recv_data_byte.endswith(b"<END>"):
                        break
                        
                recv_data = recv_data_byte.decode()
                recv_data = recv_data.replace("<END>", "")
                        
                if recv_data == "<RED>":
                    send_data = f"<STR>{data}<END>"
                    send_data_byte = send_data.encode()
                    try:
                        self.connection.sendall(send_data_byte)
                    except:
                        if self.print_flag:
                            print(f"def: send | error | communication false")
                        exit(-1)
                else:
                    if self.print_flag:
                        print(f"def: send | error | invalid data received")
                    exit(-1)
            except:
                if self.print_flag:
                    print(f"def: send | error | process false")
                exit(-1)
        else:
            if self.print_flag:
                print(f"def: send | error | type false")
            exit(-1)
            
        if self.metric_flag:
            end_point = time.perf_counter_ns()
            run_time = (end_point - start_point)/1000000

            length = len(self.metric_buf)
            if length > self.stack - 1:
                del self.metric_buf[self.stack - 1]

            if self.sampleconst_flag:
                self.wait(run_time)
                end_point = time.perf_counter_ns()
                run_time = (end_point - start_point)/1000000
                if self.print_flag:
                    print(f"def: send | alert | wait until {self.sampleconst_time}ms, run time: {run_time}ms")

            self.metric_buf.insert(0, run_time)
            self.last_time = run_time

    def recv(self):
        if self.metric_flag:
            start_point = time.perf_counter_ns()
        try:
            recv_data_byte = b""

            while True:
                recv_data_byte += self.connection.recv(self.byte)

                if recv_data_byte.endswith(b"<END>"):
                    break
                    
            recv_data = recv_data_byte.decode()
            recv_data = recv_data.replace("<END>", "")
            type = ""
            
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

        send_data = f"<CHK><END>"
        send_data_byte = send_data.encode()

        try:
            self.connection.sendall(send_data_byte)
        except:
            if self.print_flag:
                print(f"def: recv | error | communication false")
            exit(-1)
        
        if self.metric_flag:
            end_point = time.perf_counter_ns()
            run_time = (end_point - start_point)/1000000

            length = len(self.metric_buf)
            if length > self.stack - 1:
                del self.metric_buf[self.stack - 1]

            if self.sampleconst_flag:
                self.wait(run_time)
                end_point = time.perf_counter_ns()
                run_time = (end_point - start_point)/1000000
                if self.print_flag:
                    print(f"def: recv | alert | wait until {self.sampleconst_time}ms, run time: {(run_time)}ms")
            
            self.metric_buf.insert(0, run_time)
            self.last_time = run_time
                
        return type, recv_data


    



    

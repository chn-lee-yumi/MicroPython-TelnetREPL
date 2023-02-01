import _thread
import webrepl

REPL_PASSWORD = ".12345"


def telnet_server():
    """实现一个telnet的REPL"""
    address = socket.getaddrinfo("0.0.0.0", 23)[0][-1]
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(1)
    while True:
        conn, address = sock.accept()
        print("new telnet connection from ", address)
        conn.setblocking(False)
        conn.read()  # 读取多余字符
        conn.setblocking(True)
        try:
            file = conn.makefile('rwb', 0)
            is_login = False
            while not is_login:
                file.write(b"Password: ")
                input_password = file.readline().rstrip(b"\r\n")
                if input_password == REPL_PASSWORD.encode("utf8"):
                    is_login = True
                    file.write(b"TelnetREPL connected\r\n>>> ")
            conn.setblocking(False)
            conn.setsockopt(socket.SOL_SOCKET, 20, os.dupterm_notify)
            os.dupterm(file)
        except Exception as e:
            print("Exception in telnet_server: ", e)
            os.dupterm(None)
            conn.close()

            
webrepl.start(port=8266, password=REPL_PASSWORD)  # 启动WebREPL
_thread.start_new_thread(telnet_server, ())  # 启动TelnetREPL

